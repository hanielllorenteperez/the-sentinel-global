# Fábrica de noticias — The Sentinel Global

Bot que fabrica cada día un vídeo de noticias virales (más de 5 min, con intriga) + su Short, y los sube a YouTube en **privado**.

- `noticias/<fecha-tema>/guion.json` y `guion-short.json` → los escribe el bot (Claude) cada día siguiendo `RECETA-GUION.md`.
- Al subir un guion, GitHub (pestaña **Actions**) monta los vídeos y los sube a YouTube. Avisa abriendo un **Issue**.
- Secretos necesarios (Settings → Secrets → Actions): `PEXELS_API_KEY`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
- Voz: edge-tts es-ES-AlvaroNeural −8 %. Clips: Pexels. Música: Kevin MacLeod (CC BY 4.0), crédito automático.
