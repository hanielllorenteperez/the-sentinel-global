# -*- coding: utf-8 -*-
r"""
Sube a YouTube el vídeo largo y el Short de una noticia (API oficial, gratis).

  python fabrica/subir_youtube.py salida/<id>

Necesita (secretos de GitHub): YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Opcional: YT_PRIVACIDAD = private (por defecto) | unlisted | public
Deja salida/<id>/subidos.json con los enlaces. El Short lleva en su descripción el enlace al vídeo largo.
"""
import json
import os
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def youtube():
    cred = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    return build("youtube", "v3", credentials=cred, cache_discovery=False)


def subir(yt, meta, extra_desc=""):
    cuerpo = {
        "snippet": {
            "title": meta["titulo"],
            "description": (extra_desc + meta["descripcion"])[:4990],
            "tags": meta.get("etiquetas", [])[:30],
            "categoryId": "25",  # Noticias y política
            "defaultLanguage": "es",
            "defaultAudioLanguage": "es",
        },
        "status": {
            "privacyStatus": os.environ.get("YT_PRIVACIDAD", "private"),
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(meta["archivo"], mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    pet = yt.videos().insert(part="snippet,status", body=cuerpo, media_body=media)
    resp = None
    while resp is None:
        estado, resp = pet.next_chunk()
        if estado:
            print(f"   subido {int(estado.progress() * 100)} %", flush=True)
    return resp["id"]


def main():
    carpeta = sys.argv[1]
    yt = youtube()
    hecho = {}
    largo = os.path.join(carpeta, "meta.json")
    corto = os.path.join(carpeta, "meta-short.json")
    if os.path.exists(largo):
        m = json.load(open(largo, encoding="utf-8"))
        vid = subir(yt, m)
        hecho["largo"] = {"titulo": m["titulo"], "url": f"https://youtu.be/{vid}"}
        print("Vídeo largo subido:", hecho["largo"]["url"])
    if os.path.exists(corto):
        m = json.load(open(corto, encoding="utf-8"))
        extra = f"▶ Vídeo completo: {hecho['largo']['url']}\n\n" if "largo" in hecho else ""
        vid = subir(yt, m, extra)
        hecho["short"] = {"titulo": m["titulo"], "url": f"https://youtube.com/shorts/{vid}"}
        print("Short subido:", hecho["short"]["url"])
    json.dump(hecho, open(os.path.join(carpeta, "subidos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
