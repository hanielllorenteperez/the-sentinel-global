# -*- coding: utf-8 -*-
r"""
FÁBRICA DE NOTICIAS (versión BOT, corre en GitHub Actions o en cualquier PC)

  python fabrica/fabrica.py noticias/<id>/guion.json          → salida/<id>/<id>.mp4        (largo 1920x1080, +5 min)
  python fabrica/fabrica.py noticias/<id>/guion-short.json    → salida/<id>/<id>-short.mp4  (Short 1080x1920, <60 s)

Gratis: voz edge-tts Álvaro (-8 %), clips de Pexels (API gratis, variable PEXELS_API_KEY),
música Kevin MacLeod (CC BY) según el ambiente, render con Remotion.

Clips en el guion: un enlace "https://videos.pexels.com/video-files/..." o una búsqueda "pexels:hippo zoo"
(el bot elige solo un vídeo horizontal en HD que no se haya usado ya en esa noticia).
Formato completo del guion: ver RECETA-GUION.md.
"""
import glob
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTION = os.path.join(RAIZ, "remotion")
VOZ = "es-ES-AlvaroNeural"
RATE = "-8%"
NPX = "npx.cmd" if os.name == "nt" else "npx"

AMBIENTES = {  # ambiente → canción (remotion/public/musica/<nombre>.mp3)
    "tension": "tension--interloper",
    "triste": "triste--heavy-heart",
    "misterio": "misterio--hidden-past",
    "curiosidad": "curiosidad--investigations",
    "epica": "epica--rising-tide",
    "aventura": "epica--call-to-adventure",
    "guerra": "guerra--impending-boom",
    "drama": "triste--decline",
    "reflexion": "reflexion--rumination",
    "noche": "noche--midnight-tale",
    "humor": "gracia--sneaky-snitch",
    "industrial": "industrial--americana",
}


def log(*a):
    print(*a, flush=True)


def ffprobe():
    for p in glob.glob(os.path.join(REMOTION, "node_modules", "@remotion", "compositor-*", "ffprobe*")):
        if not p.endswith((".d.ts", ".js")):
            return p
    return shutil.which("ffprobe") or "ffprobe"


FFPROBE = None


def duracion(ruta):
    global FFPROBE
    FFPROBE = FFPROBE or ffprobe()
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                         capture_output=True, text=True)
    return float(out.stdout.strip())


def _voz_api(texto, destino):
    """Voz Álvaro con edge-tts guardando también CUÁNDO suena cada palabra (para los subtítulos)."""
    import asyncio
    import edge_tts

    async def run():
        com = edge_tts.Communicate(texto, VOZ, rate=RATE, boundary="WordBoundary")
        palabras = []
        with open(destino, "wb") as f:
            async for c in com.stream():
                if c["type"] == "audio":
                    f.write(c["data"])
                elif c["type"] == "WordBoundary":
                    palabras.append({"t": round(c["offset"] / 1e7, 3), "d": round(c["duration"] / 1e7, 3), "w": c["text"]})
        return palabras

    return asyncio.run(run())


def hacer_voz(texto, destino, intentos=8):
    marca = destino + ".txt"
    pal = destino + ".palabras.json"
    if os.path.exists(destino) and os.path.exists(pal) and os.path.exists(marca) and open(marca, encoding="utf-8").read() == texto:
        return
    with open(marca, "w", encoding="utf-8") as f:
        f.write(texto)
    for i in range(1, intentos + 1):
        try:
            palabras = _voz_api(texto, destino)
            if os.path.getsize(destino) > 2000:
                json.dump(palabras, open(pal, "w", encoding="utf-8"), ensure_ascii=False)
                return
        except Exception as e:  # noqa: BLE001
            log(f"   voz cortada (intento {i}), reintento…", str(e)[-200:])
        time.sleep(2 * i)
    raise SystemExit(f"No se pudo generar la voz: {destino}")


def palabras_de(mp3):
    try:
        return json.load(open(mp3 + ".palabras.json", encoding="utf-8"))
    except (OSError, ValueError):
        return []


def bajar(url, destino, ua="Mozilla/5.0"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r, open(destino + ".part", "wb") as f:
                shutil.copyfileobj(r, f)
            os.replace(destino + ".part", destino)
            return
        except Exception as e:  # noqa
            log("   fallo al bajar, reintento:", e)
            time.sleep(3)
    raise SystemExit("No se pudo bajar " + url)


def buscar_pexels(consulta, usados, vertical=False):
    clave = os.environ.get("PEXELS_API_KEY")
    if not clave:
        raise SystemExit("Falta PEXELS_API_KEY para buscar clips: " + consulta)
    q = urllib.parse.urlencode({"query": consulta, "per_page": 15, "orientation": "landscape", "size": "medium"})
    req = urllib.request.Request("https://api.pexels.com/videos/search?" + q,
                                 headers={"Authorization": clave, "User-Agent": "fabrica-noticias"})
    datos = json.load(urllib.request.urlopen(req, timeout=60))
    candidatos = []
    for v in datos.get("videos", []):
        if v["id"] in usados or v.get("duration", 0) < 5:
            continue
        files = [f for f in v["video_files"] if f.get("width") and f["width"] >= f.get("height", 0)]
        files.sort(key=lambda f: abs(f["width"] - 1280))  # 1280x720: ligero y suficiente bajo el oscurecido
        if files:
            candidatos.append((v["id"], files[0]["link"]))
    if not candidatos:
        raise SystemExit("Pexels no devolvió clips para: " + consulta)
    vid, link = random.choice(candidatos[:4])
    usados.add(vid)
    return link


def buscar_pixabay(consulta, usados):
    clave = os.environ.get("PIXABAY_API_KEY")
    if not clave:
        raise SystemExit("Falta PIXABAY_API_KEY para buscar clips: " + consulta)
    q = urllib.parse.urlencode({"key": clave, "q": consulta, "per_page": 20, "safesearch": "true"})
    req = urllib.request.Request("https://pixabay.com/api/videos/?" + q, headers={"User-Agent": "fabrica-noticias"})
    datos = json.load(urllib.request.urlopen(req, timeout=60))
    candidatos = []
    for v in datos.get("hits", []):
        if ("pb", v["id"]) in usados or v.get("duration", 0) < 5:
            continue
        tam = [t for t in ("medium", "large", "small") if v["videos"].get(t, {}).get("url")]
        tam = [t for t in tam if v["videos"][t]["width"] >= v["videos"][t]["height"]]
        if tam:
            candidatos.append((v["id"], v["videos"][tam[0]]["url"]))
    if not candidatos:
        raise SystemExit("Pixabay no devolvió clips para: " + consulta)
    vid, link = random.choice(candidatos[:4])
    usados.add(("pb", vid))
    return link


def buscar_clip(consulta, usados):
    """Busca en Pexels y, si no hay clave o resultados, en Pixabay (los dos gratis)."""
    errores = []
    for nombre, fn, var in (("Pexels", buscar_pexels, "PEXELS_API_KEY"), ("Pixabay", buscar_pixabay, "PIXABAY_API_KEY")):
        if not os.environ.get(var):
            continue
        try:
            link = fn(consulta, usados)
            log(f"   clip {nombre}:", link[:90])
            return link
        except SystemExit as e:
            errores.append(str(e))
    raise SystemExit("Sin clips para '" + consulta + "': " + " | ".join(errores or ["no hay claves de Pexels ni Pixabay"]))


UA_WIKI = "fabrica-noticias/1.0 (bot de noticias para YouTube; uso no comercial de la API)"
CREDITOS_FOTOS = []  # se escriben en la descripción (licencias CC BY / CC BY-SA lo exigen)
LICENCIAS_OK = ("cc0", "public domain", "dominio público", "pd", "cc by")  # sin NC ni ND


def buscar_wikimedia(consulta, usados):
    """Foto real de Wikimedia Commons (la galería de Wikipedia). Gratis y sin clave."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": 15,
        "gsrsearch": f"{consulta} filetype:bitmap", "prop": "imageinfo",
        "iiprop": "url|size|extmetadata", "iiurlwidth": 1920,
    })
    req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers={"User-Agent": UA_WIKI})
    datos = json.load(urllib.request.urlopen(req, timeout=60))
    paginas = sorted(datos.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in paginas:
        info = (p.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        l = lic.lower()
        if p["pageid"] in usados or not any(x in l for x in LICENCIAS_OK) or "nc" in l.split("-") or "nd" in l.split("-"):
            continue
        if info.get("width", 0) < 1000 or info.get("width", 0) < info.get("height", 1):  # horizontal y grande
            continue
        autor = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "Desconocido")).strip()[:80]
        usados.add(p["pageid"])
        CREDITOS_FOTOS.append(f"{p['title'].replace('File:', '')} — {autor} — {lic} — {info.get('descriptionurl', '')}")
        log("   foto Wikimedia:", p["title"], "|", lic)
        return info.get("thumburl") or info["url"]
    raise SystemExit("Wikimedia no devolvió fotos libres para: " + consulta)


def traer_clip(origen, carpeta, usados):
    if origen.startswith("wiki:"):
        url = buscar_wikimedia(origen[5:].strip(), usados)
        ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
        ext = ext if ext in (".jpg", ".jpeg", ".png", ".webp") else ".jpg"
        destino = os.path.join(carpeta, hashlib.md5(url.encode()).hexdigest()[:10] + ext)
        if not os.path.exists(destino):
            bajar(url, destino, UA_WIKI)
        return destino
    for pref in ("pexels:", "pixabay:", "buscar:"):
        if origen.startswith(pref):
            origen = buscar_clip(origen[len(pref):].strip(), usados)
            break
    if origen.startswith("http"):
        destino = os.path.join(carpeta, hashlib.md5(origen.encode()).hexdigest()[:10] + ".mp4")
        if not os.path.exists(destino):
            bajar(origen, destino)
        return destino
    ruta = origen if os.path.isabs(origen) else os.path.join(RAIZ, origen)
    destino = os.path.join(carpeta, os.path.basename(ruta))
    shutil.copy(ruta, destino)
    return destino


def preparar_musica(nombre, usadas):
    nombre = AMBIENTES.get(nombre, nombre).replace(".mp3", "")
    if not os.path.exists(os.path.join(REMOTION, "public", "musica", nombre + ".mp3")):
        raise SystemExit(f"No existe la música '{nombre}'. Ambientes: {', '.join(AMBIENTES)}")
    titulo = nombre.split("--", 1)[1].replace("-", " ").title()
    if titulo not in usadas:
        usadas.append(titulo)
    return f"musica/{nombre}.mp3"


def credito_musica(usadas):
    return "\n".join(f"Música: {t} Kevin MacLeod (incompetech.com)\n"
                     "Licensed under Creative Commons: By Attribution 4.0 License\n"
                     "http://creativecommons.org/licenses/by/4.0/" for t in usadas)


def main():
    guion_path = os.path.abspath(sys.argv[1])
    g = json.load(open(guion_path, encoding="utf-8"))
    nid = g["id"]
    short = g.get("formato") == "short"
    suf = "-short" if short else ""
    pub_rel = f"fabrica/{nid}{suf}"
    pub = os.path.join(REMOTION, "public", "fabrica", nid + suf)
    salida_dir = os.path.join(RAIZ, "salida", nid)
    os.makedirs(pub, exist_ok=True)
    os.makedirs(salida_dir, exist_ok=True)
    t0 = time.time()

    usadas, usados = [], set()
    # REGLA de Haniel: siempre muchos más vídeos que fotos → máximo 1 foto (wiki:) por cada 6 clips.
    todos = [c for e in g["escenas"] for c in e.get("clips", [])]
    max_fotos = max(1, len(todos) // 6)
    vistas = 0
    for e in g["escenas"]:
        nuevos = []
        for c in e.get("clips", []):
            if c.startswith("wiki:"):
                vistas += 1
                if vistas > max_fotos:
                    log(f"   demasiadas fotos: '{c}' se cambia por vídeo")
                    c = "buscar:" + c[5:]
            nuevos.append(c)
        e["clips"] = nuevos
    musica = preparar_musica(g.get("musica", "tension"), usadas)
    escenas = []
    for i, e in enumerate(g["escenas"], 1):
        log(f"Escena {i}/{len(g['escenas'])}")
        mp3 = os.path.join(pub, f"v{i}.mp3")
        hacer_voz(e["voz"], mp3)
        clips = []
        for c in e.get("clips", []):
            ruta = traer_clip(c, pub, usados)
            foto = ruta.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            clips.append({"src": f"{pub_rel}/{os.path.basename(ruta)}", "dur": 999 if foto else round(duracion(ruta), 2)})
        sal = {k: v for k, v in e.items() if k not in ("voz", "clips", "musica")}
        if e.get("musica"):
            sal["musica"] = preparar_musica(e["musica"], usadas)
        sal.update({"voz": f"{pub_rel}/v{i}.mp3", "dur": round(duracion(mp3), 3), "clips": clips, "palabras": palabras_de(mp3)})
        escenas.append(sal)

    props = {"cinta": g.get("cinta", ""), "rotulos": g.get("rotulos", []), "musica": musica, "volumenMusica": 0.07, "escenas": escenas}
    props_path = os.path.join(salida_dir, f"props{suf}.json")
    json.dump(props, open(props_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    total = sum(e["dur"] + 0.3 for e in escenas) + 0.5
    log(f"Voces y clips listos ({time.time() - t0:.0f} s). Duración: {total:.0f} s. Renderizando…")
    if short and total > 59:
        log(f"OJO: el Short dura {total:.0f} s (mejor < 60 s).")

    salida = os.path.join(salida_dir, f"{nid}{suf}.mp4")
    cmd = [NPX, "remotion", "render", "NoticiaRapidaShort" if short else "NoticiaRapida", salida,
           f"--props={props_path}", "--log=error"]
    if os.environ.get("CONCURRENCIA"):
        cmd.append(f"--concurrency={os.environ['CONCURRENCIA']}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        raise SystemExit("Falló el render")

    descripcion = g.get("descripcion", "").strip()
    if g.get("fuentes"):
        descripcion += "\n\nFuentes:\n" + "\n".join(g["fuentes"])
    descripcion += "\n\nImágenes: clips de Pexels/Pixabay (licencia libre)."
    if CREDITOS_FOTOS:
        descripcion += "\nFotos de Wikimedia Commons:\n" + "\n".join(CREDITOS_FOTOS)
    descripcion += "\n" + credito_musica(usadas)
    meta = {
        "archivo": salida,
        "titulo": (g.get("titulo", nid) + (" #shorts" if short else ""))[:100],
        "descripcion": descripcion[:4900],
        "etiquetas": g.get("etiquetas", []),
        "short": short,
        "duracion": round(total),
    }
    json.dump(meta, open(os.path.join(salida_dir, f"meta{suf}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(salida_dir, f"{nid}{suf}-youtube.txt"), "w", encoding="utf-8") as f:
        f.write(f"TÍTULO:\n{meta['titulo']}\n\nDESCRIPCIÓN:\n{descripcion}\n\nETIQUETAS:\n{', '.join(meta['etiquetas'])}\n")
    log(f"LISTO en {time.time() - t0:.0f} s → {salida}")


if __name__ == "__main__":
    main()
