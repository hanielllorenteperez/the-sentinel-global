# -*- coding: utf-8 -*-
r"""
ESTADÍSTICAS de The Sentinel Global (API oficial de YouTube, gratis).

Cada 3 horas (GitHub Actions, estadisticas.yml) apunta en estadisticas/videos.json:
  - del canal: suscriptores, vistas totales y número de vídeos;
  - de cada vídeo (largo y Short de noticias/*/estado.json): vistas, likes, comentarios
    y los últimos comentarios que ha recibido.
Hiam (Agentes › The Sentinel Global) lo lee de GitHub y lo enseña debajo de cada miniatura.

Cupo de YouTube: ~3 unidades cada vez (de 10.000 al día), así no quita sitio a las subidas.
Usa los mismos secretos que el bot de comentarios (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN).
"""
import glob
import json
import os
import re
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CANAL = os.environ.get("YT_CANAL", "UCO9S_OGSBvu3YKLCW7Mqjjg")  # @TheSentinelGlobal
SALIDA = os.path.join("estadisticas", "videos.json")
ULTIMOS = 5  # comentarios guardados por vídeo


def youtube():
    cred = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("youtube", "v3", credentials=cred, cache_discovery=False)


def id_de(url):
    m = re.search(r"(?:youtu\.be/|shorts/|v=)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else None


def num(d, k):
    try:
        return int(d.get(k, 0))
    except (TypeError, ValueError):
        return 0


def main():
    yt = youtube()
    ids = []
    for p in sorted(glob.glob("noticias/*/estado.json")):
        try:
            e = json.load(open(p, encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for k in ("largo", "short"):
            v = id_de(e.get(k))
            if v and v not in ids:
                ids.append(v)

    # Canal (1 unidad)
    canal = {}
    r = yt.channels().list(part="statistics,snippet", id=CANAL).execute()
    if r.get("items"):
        s = r["items"][0]["statistics"]
        canal = {
            "nombre": r["items"][0]["snippet"].get("title", ""),
            "suscriptores": num(s, "subscriberCount"),
            "suscriptores_ocultos": bool(s.get("hiddenSubscriberCount")),
            "vistas": num(s, "viewCount"),
            "videos": num(s, "videoCount"),
        }

    # Vídeos (1 unidad por cada 50)
    videos = {}
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="statistics,status,snippet", id=",".join(ids[i:i + 50])).execute()
        for v in r.get("items", []):
            s = v.get("statistics", {})
            videos[v["id"]] = {
                "titulo": v["snippet"].get("title", ""),
                "visible": v.get("status", {}).get("privacyStatus", ""),
                "vistas": num(s, "viewCount"),
                "likes": num(s, "likeCount"),
                "comentarios": num(s, "commentCount"),
                "ultimos": [],
            }

    # Últimos comentarios del canal, repartidos por vídeo (1 unidad por página de 100)
    pagina = None
    for _ in range(2):
        try:
            r = yt.commentThreads().list(
                part="snippet", allThreadsRelatedToChannelId=CANAL, maxResults=100,
                order="time", textFormat="plainText", pageToken=pagina,
            ).execute()
        except Exception as e:  # si falla, las cifras siguen valiendo
            print("No pude leer los comentarios:", str(e)[:200])
            break
        for h in r.get("items", []):
            vid = h["snippet"].get("videoId", "")
            s = h["snippet"]["topLevelComment"]["snippet"]
            if vid in videos and len(videos[vid]["ultimos"]) < ULTIMOS:
                videos[vid]["ultimos"].append({
                    "autor": s.get("authorDisplayName", ""),
                    "texto": (s.get("textOriginal") or s.get("textDisplay", ""))[:400],
                    "likes": num(s, "likeCount"),
                    "fecha": s.get("publishedAt", ""),
                    "nuestro": s.get("authorChannelId", {}).get("value") == CANAL,
                })
        pagina = r.get("nextPageToken")
        if not pagina:
            break

    os.makedirs("estadisticas", exist_ok=True)
    datos = {
        "leido": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "canal": canal,
        "videos": videos,
    }
    json.dump(datos, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Canal: {canal.get('suscriptores')} suscriptores, {canal.get('vistas')} vistas · {len(videos)} vídeos → {SALIDA}")


if __name__ == "__main__":
    main()
