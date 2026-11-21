# -*- coding: utf-8 -*-
r"""
Se usa UNA SOLA VEZ en el PC de Haniel para dar permiso al bot de subir vídeos a su canal
y de leer y responder comentarios (alcance youtube.force-ssl).
OJO: al entrar con Google, elegir el canal @TheSentinelGlobal.

  python fabrica/obtener_permiso_youtube.py ruta\client_secret.json

Abre el navegador, Haniel entra con su cuenta de YouTube y acepta. Guarda el permiso en
permiso_youtube.json (NO se sube a GitHub; Claude copia sus 3 valores a los secretos del repositorio).
"""
import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"])
cred = flow.run_local_server(port=0, prompt="consent", access_type="offline")
json.dump(
    {"YT_CLIENT_ID": cred.client_id, "YT_CLIENT_SECRET": cred.client_secret, "YT_REFRESH_TOKEN": cred.refresh_token},
    open("permiso_youtube.json", "w"),
    indent=1,
)
print("Permiso guardado en permiso_youtube.json")
