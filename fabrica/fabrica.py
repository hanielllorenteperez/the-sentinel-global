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


def hacer_voz(texto, destino, intentos=8):
    marca = destino + ".txt"
    if os.path.exists(destino) and os.path.exists(marca) and open(marca, encoding="utf-8").read() == texto:
        return
    with open(marca, "w", encoding="utf-8") as f:
        f.write(texto)
    for i in range(1, intentos + 1):
        r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", VOZ, f"--rate={RATE}", "-f", marca,
                            "--write-media", destino], capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(destino) and os.path.getsize(destino) > 2000:
            return
        log(f"   voz cortada (intento {i}), reintento…", r.stderr[-200:])
        time.sleep(2 * i)
    raise SystemExit(f"No se pudo generar la voz: {destino}")


def bajar(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
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


def traer_clip(origen, carpeta, usados):
    if origen.startswith("pexels:"):
        origen = buscar_pexels(origen[7:].strip(), usados)
        log("   clip Pexels:", origen[:90])
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
    musica = preparar_musica(g.get("musica", "tension"), usadas)
    escenas = []
    for i, e in enumerate(g["escenas"], 1):
        log(f"Escena {i}/{len(g['escenas'])}")
        mp3 = os.path.join(pub, f"v{i}.mp3")
        hacer_voz(e["voz"], mp3)
        clips = []
        for c in e.get("clips", []):
            ruta = traer_clip(c, pub, usados)
            clips.append({"src": f"{pub_rel}/{os.path.basename(ruta)}", "dur": round(duracion(ruta), 2)})
        sal = {k: v for k, v in e.items() if k not in ("voz", "clips", "musica")}
        if e.get("musica"):
            sal["musica"] = preparar_musica(e["musica"], usadas)
        sal.update({"voz": f"{pub_rel}/v{i}.mp3", "dur": round(duracion(mp3), 3), "clips": clips})
        escenas.append(sal)

    props = {"cinta": g.get("cinta", ""), "musica": musica, "volumenMusica": 0.07, "escenas": escenas}
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
    descripcion += "\n\nImágenes: clips de Pexels (licencia Pexels).\n" + credito_musica(usadas)
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
