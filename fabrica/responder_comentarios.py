# -*- coding: utf-8 -*-
r"""
BOT DE COMENTARIOS de The Sentinel Global (API oficial de YouTube, gratis).

Funciona en 3 pasos, una vez al día:
  1) python fabrica/responder_comentarios.py leer
     GitHub Actions lee los comentarios nuevos del canal (los que aún no tienen respuesta nuestra)
     y los deja en comentarios/pendientes.json.
  2) La tarea de Claude en la nube ("Comentarios – The Sentinel Global") lee pendientes.json,
     decide qué hacer con cada uno y escribe comentarios/respuestas.json:
       {"fecha": "AAAA-MM-DD",
        "responder": [{"id": "...", "texto": "..."}],
        "avisar":    [{"id": "...", "motivo": "..."}],    <- NO se responde: se avisa a Haniel
        "ignorar":   [{"id": "...", "motivo": "spam"}]}
  3) python fabrica/responder_comentarios.py responder
     Actions publica las respuestas (máx. MAX_RESPUESTAS al día), apunta todo en
     comentarios/hechos.json (para no repetir nunca) y deja comentarios/resumen.md para el Issue.

Necesita los secretos YT_CLIENT_ID, YT_CLIENT_SECRET y YT_REFRESH_TOKEN, con un permiso que incluya
el alcance youtube.force-ssl (el de solo subir vídeos NO deja leer ni responder comentarios).

Cupo de YouTube: leer = 1-3 unidades; cada respuesta = 50. Las subidas de vídeos gastan ~9.600 de 10.000,
por eso el límite es de 7 respuestas al día. Si YouTube dice que no hay cupo, para y lo deja para mañana.
"""
import json
import os
import sys
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CANAL = os.environ.get("YT_CANAL", "UCO9S_OGSBvu3YKLCW7Mqjjg")  # @TheSentinelGlobal
MAX_RESPUESTAS = int(os.environ.get("MAX_RESPUESTAS", "7"))
CARPETA = "comentarios"
P_PEND = os.path.join(CARPETA, "pendientes.json")
P_RESP = os.path.join(CARPETA, "respuestas.json")
P_HECHOS = os.path.join(CARPETA, "hechos.json")
P_RESUMEN = os.path.join(CARPETA, "resumen.md")


def youtube():
    cred = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("youtube", "v3", credentials=cred, cache_discovery=False)


def cargar(p, defecto):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return defecto


def guardar(p, datos):
    os.makedirs(CARPETA, exist_ok=True)
    json.dump(datos, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def sin_cupo(e):
    return isinstance(e, HttpError) and ("quotaExceeded" in str(e) or "dailyLimitExceeded" in str(e))


def falta_permiso(e):
    return isinstance(e, HttpError) and e.resp.status in (401, 403) and (
        "insufficient" in str(e).lower() or "scope" in str(e).lower() or "forbidden" in str(e).lower()
    )


def leer():
    """Busca comentarios principales sin respuesta nuestra y los guarda en pendientes.json."""
    yt = youtube()
    hechos = cargar(P_HECHOS, {})
    nuevos, pagina, paginas = [], None, 0
    while paginas < 5:  # 5 páginas x 100 = 500 hilos más recientes (1 unidad cada página)
        r = yt.commentThreads().list(
            part="snippet,replies", allThreadsRelatedToChannelId=CANAL,
            maxResults=100, order="time", textFormat="plainText", pageToken=pagina,
        ).execute()
        for h in r.get("items", []):
            top = h["snippet"]["topLevelComment"]
            s = top["snippet"]
            if top["id"] in hechos:
                continue
            if s.get("authorChannelId", {}).get("value") == CANAL:
                continue  # comentario nuestro
            respuestas = h.get("replies", {}).get("comments", [])
            if any(c["snippet"].get("authorChannelId", {}).get("value") == CANAL for c in respuestas):
                continue  # ya respondido (a mano o por el bot)
            nuevos.append({
                "id": top["id"],
                "video": h["snippet"].get("videoId", ""),
                "autor": s.get("authorDisplayName", ""),
                "texto": s.get("textOriginal") or s.get("textDisplay", ""),
                "me_gusta": s.get("likeCount", 0),
                "fecha": s.get("publishedAt", ""),
                "respuestas_de_otros": [c["snippet"].get("textOriginal", "")[:300] for c in respuestas[:3]],
            })
        pagina, paginas = r.get("nextPageToken"), paginas + 1
        if not pagina:
            break

    # Títulos de los vídeos, para que Claude sepa de qué habla cada comentario (1 unidad por 50 vídeos)
    ids = sorted({c["video"] for c in nuevos if c["video"]})
    titulos = {}
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet", id=",".join(ids[i:i + 50])).execute()
        for v in r.get("items", []):
            titulos[v["id"]] = {"titulo": v["snippet"]["title"], "descripcion": v["snippet"]["description"][:1500]}
    for c in nuevos:
        c["video_titulo"] = titulos.get(c["video"], {}).get("titulo", "")

    # Primero los que tienen más "me gusta"; a igualdad, los más recientes
    nuevos.sort(key=lambda c: (c["me_gusta"], c["fecha"]), reverse=True)
    guardar(P_PEND, {
        "leido": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "max_respuestas_hoy": MAX_RESPUESTAS,
        "videos": titulos,
        "comentarios": nuevos,
    })
    print(f"{len(nuevos)} comentarios nuevos sin responder → {P_PEND}")


def responder():
    """Publica lo que decidió Claude en respuestas.json y apunta todo en hechos.json."""
    plan = cargar(P_RESP, None)
    if not plan:
        print("No hay respuestas.json: nada que hacer.")
        return
    hechos = cargar(P_HECHOS, {})
    pend = {c["id"]: c for c in cargar(P_PEND, {}).get("comentarios", [])}
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hechas_hoy = sum(1 for h in hechos.values() if h.get("accion") == "respondido" and h.get("fecha") == hoy)
    yt = None
    publicadas, avisos, ignorados, quedan = [], [], [], []

    for r in plan.get("responder", []):
        cid, texto = r.get("id"), (r.get("texto") or "").strip()
        if not cid or not texto or cid in hechos:
            continue
        if hechas_hoy >= MAX_RESPUESTAS:
            quedan.append(cid)
            continue
        try:
            yt = yt or youtube()
            yt.comments().insert(part="snippet", body={"snippet": {"parentId": cid, "textOriginal": texto[:900]}}).execute()
        except HttpError as e:
            if sin_cupo(e):
                print("Se acabó el cupo de YouTube por hoy: el resto se queda para mañana.")
                quedan.append(cid)
                break
            if e.resp.status == 404:  # el comentario se borró
                hechos[cid] = {"accion": "borrado", "fecha": hoy}
                continue
            if falta_permiso(e):
                print("::error::El permiso de YouTube no deja responder comentarios (falta el alcance youtube.force-ssl).")
                raise
            print(f"::warning::No se pudo responder a {cid}: {e}")
            continue
        hechas_hoy += 1
        hechos[cid] = {"accion": "respondido", "fecha": hoy, "texto": texto}
        publicadas.append((cid, texto))

    for clave, lista, accion in (("avisar", avisos, "avisado"), ("ignorar", ignorados, "ignorado")):
        for r in plan.get(clave, []):
            cid = r.get("id")
            if cid and cid not in hechos:
                hechos[cid] = {"accion": accion, "fecha": hoy, "motivo": r.get("motivo", "")}
                lista.append((cid, r.get("motivo", "")))

    guardar(P_HECHOS, hechos)

    def linea(cid):
        c = pend.get(cid, {})
        enlace = f"https://www.youtube.com/watch?v={c.get('video', '')}&lc={cid}"
        return f"**{c.get('autor', '?')}** en «{c.get('video_titulo', '?')}»: _{c.get('texto', '')[:250]}_ — [ver]({enlace})"

    md = [f"Resumen del bot de comentarios ({hoy})", ""]
    if avisos:
        md += ["## ⚠️ Para ti (el bot NO ha respondido)", ""] + [f"- {linea(c)}\n  - Motivo: {m}" for c, m in avisos] + [""]
    md += [f"## 💬 Respondidos ({len(publicadas)})", ""] + [f"- {linea(c)}\n  - ➜ {t}" for c, t in publicadas] + [""]
    if quedan:
        md += [f"## ⏳ Para mañana ({len(quedan)})", "Límite diario de respuestas o cupo de YouTube.", ""]
    if ignorados:
        md += [f"## 🗑️ Ignorados ({len(ignorados)})", ""] + [f"- {linea(c)} ({m})" for c, m in ignorados] + [""]
    open(P_RESUMEN, "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))
    # Para el paso del Issue: hay algo que contar?
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"hay={'1' if (publicadas or avisos) else '0'}\n")
            f.write(f"avisos={len(avisos)}\n")


if __name__ == "__main__":
    {"leer": leer, "responder": responder}[sys.argv[1] if len(sys.argv) > 1 else "leer"]()
