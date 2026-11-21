# -*- coding: utf-8 -*-
r"""
Sube a YouTube el vídeo largo y el Short de una noticia (API oficial, gratis).

  python fabrica/subir_youtube.py salida/<id>

Necesita (secretos de GitHub): YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Opcional: YT_PRIVACIDAD = private (por defecto) | unlisted | public
Opcional: YT_PUBLICAR = "02:00,10:00,18:00" (horas UTC) -> se programa para hacerse público solo a esa hora
          (ver cuando_publicar). Si YouTube no lo deja, se sube en privado como antes.
Deja salida/<id>/subidos.json con los enlaces. El Short lleva en su descripción el enlace al vídeo largo.

MEMORIA: lo que ya se subió se apunta en noticias/<id>/estado.json (ver memoria.py) y NO se vuelve a subir.
Si YouTube dice que se acabó el cupo del día, para sin error y lo deja pendiente para la próxima vez.
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memoria  # noqa: E402


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


def cuando_publicar(ahora=None):
    """Con YT_PUBLICAR="02:00,10:00,18:00" (horas UTC) decide cuándo se hace público el vídeo:
    - si la hora que le tocaba pasó hace menos de 3 h (llegó tarde) -> ("public", None): público ya.
    - si no -> ("private", "<fecha ISO>"): YouTube lo hace público solo a la próxima hora de la lista.
    Sin YT_PUBLICAR -> (YT_PRIVACIDAD, None), como antes."""
    horas = [h.strip() for h in os.environ.get("YT_PUBLICAR", "").split(",") if h.strip()]
    if not horas:
        return os.environ.get("YT_PRIVACIDAD", "private"), None
    ahora = ahora or datetime.now(timezone.utc)
    huecos = []
    for dia in (-1, 0, 1):
        base = (ahora + timedelta(days=dia)).replace(second=0, microsecond=0)
        for h in horas:
            hh, mm = (int(x) for x in h.split(":"))
            huecos.append(base.replace(hour=hh, minute=mm))
    pasados = [t for t in huecos if t <= ahora]
    if pasados and ahora - max(pasados) < timedelta(hours=3):
        return "public", None
    siguiente = min(t for t in huecos if t > ahora)
    if siguiente - ahora < timedelta(minutes=10):  # casi a su hora: público ya
        return "public", None
    return "private", siguiente.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def subir(yt, meta, extra_desc=""):
    privacidad, publicar_en = cuando_publicar()
    try:
        return _subir(yt, meta, extra_desc, privacidad, publicar_en)
    except HttpError as e:
        if cupo_agotado(e) or (privacidad == "private" and not publicar_en):
            raise
        # Si YouTube no deja programar/publicar con esta app, se sube en privado como antes.
        print(f"   YouTube no dejó publicarlo solo ({e.resp.status}): se sube en privado.", flush=True)
        return _subir(yt, meta, extra_desc, "private", None)


def _subir(yt, meta, extra_desc, privacidad, publicar_en):
    if publicar_en:
        print(f"   Se hará público solo el {publicar_en} (UTC)", flush=True)
    elif privacidad == "public":
        print("   Se publica ya (llegó tarde a su hora)", flush=True)
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
            "privacyStatus": privacidad,
            "selfDeclaredMadeForKids": False,
        },
    }
    if publicar_en:
        cuerpo["status"]["publishAt"] = publicar_en
    media = MediaFileUpload(meta["archivo"], mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    pet = yt.videos().insert(part="snippet,status", body=cuerpo, media_body=media)
    resp = None
    while resp is None:
        estado, resp = pet.next_chunk()
        if estado:
            print(f"   subido {int(estado.progress() * 100)} %", flush=True)
    return resp["id"]


def meta_de(carpeta, nid, suf):
    """Lee meta.json; si no está (vídeos antiguos), lo rehace con el <id>-youtube.txt."""
    mp4 = os.path.join(carpeta, f"{nid}{suf}.mp4")
    if not os.path.exists(mp4):
        return None
    p = os.path.join(carpeta, f"meta{suf}.json")
    if os.path.exists(p):
        m = json.load(open(p, encoding="utf-8"))
    else:
        txt = open(os.path.join(carpeta, f"{nid}{suf}-youtube.txt"), encoding="utf-8").read()
        titulo = txt.split("TÍTULO:\n", 1)[1].split("\n\nDESCRIPCIÓN:", 1)[0].strip()
        desc = txt.split("DESCRIPCIÓN:\n", 1)[1].split("\n\nETIQUETAS:", 1)[0].strip()
        etiq = txt.split("ETIQUETAS:\n", 1)[1].strip() if "ETIQUETAS:\n" in txt else ""
        m = {"titulo": titulo, "descripcion": desc, "etiquetas": [e.strip() for e in etiq.split(",") if e.strip()]}
    m["archivo"] = mp4  # la ruta guardada puede ser de otra máquina
    return m


def cupo_agotado(err):
    return isinstance(err, HttpError) and err.resp.status in (403, 429) and (
        b"quotaExceeded" in err.content or b"uploadLimitExceeded" in err.content or b"rateLimitExceeded" in err.content)


def main():
    carpeta = sys.argv[1].rstrip("/\\")
    nid = os.path.basename(carpeta)
    falta = memoria.falta(nid)
    if not falta:
        print(f"{nid}: ya estaba todo subido, no se repite.")
        return
    yt = youtube()
    try:
        if "largo" in falta:
            m = meta_de(carpeta, nid, "")
            if m:
                vid = subir(yt, m)
                memoria.marcar(nid, "largo", f"https://youtu.be/{vid}")
                memoria.marcar(nid, "titulo_largo", m["titulo"])
                print("Vídeo largo subido:", f"https://youtu.be/{vid}")
        if "short" in falta:
            m = meta_de(carpeta, nid, "-short")
            if m:
                largo = memoria.leer(nid).get("largo")
                extra = f"▶ Vídeo completo: {largo}\n\n" if largo else ""
                vid = subir(yt, m, extra)
                memoria.marcar(nid, "short", f"https://youtube.com/shorts/{vid}")
                memoria.marcar(nid, "titulo_short", m["titulo"])
                print("Short subido:", f"https://youtube.com/shorts/{vid}")
    except HttpError as e:
        if cupo_agotado(e):
            print(f"{nid}: YouTube no deja subir más hoy (cupo). Queda pendiente para la próxima vez.")
            memoria.marcar(nid, "aviso", "cupo de YouTube agotado, se reintentará")
        else:
            raise
    finally:
        d = memoria.leer(nid)
        hecho = {}
        if d.get("largo"):
            hecho["largo"] = {"titulo": d.get("titulo_largo", nid), "url": d["largo"]}
        if d.get("short"):
            hecho["short"] = {"titulo": d.get("titulo_short", nid), "url": d["short"]}
        json.dump(hecho, open(os.path.join(carpeta, "subidos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
