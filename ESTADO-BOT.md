# 🤖 ESTADO-BOT — la memoria del bot (léela SIEMPRE antes de empezar)

Este archivo es la memoria de The Sentinel Global entre una ejecución y otra.
- La **fábrica** (GitHub Actions) apunta sola abajo el resultado de cada noticia en "Diario de la fábrica".
- El **guionista** (Claude en la nube) apunta sus lecciones en "Diario del guionista".
- Arriba, en "Lecciones aprendidas", quedan las reglas que salieron de errores. **No repetirlos.**
- La libreta técnica de cada noticia (qué está montado / subido) está en `noticias/<id>/estado.json`.

## Lecciones aprendidas (no repetir)
- 2026-11-21 · Los secretos de GitHub se pegan SIN comillas (con comillas → `invalid_client`).
- 2026-11-21 · El proyecto de Google Cloud necesita la "YouTube Data API v3" HABILITADA (si no → error 403).
- 2026-11-21 · YouTube deja unas 6 subidas al día por API (3 largos + 3 Shorts). Si se pasa, la libreta lo deja pendiente.
- 2026-11-21 · Pexels pausó las claves nuevas → los clips salen de Pixabay. Búsquedas concretas en inglés funcionan mejor.
- 2026-11-21 · Vídeos de más de 5 minutos, estilo intriga/suspenso; máx. 1 foto por cada 6 clips (reglas de Haniel).
- 2026-11-21 · No hacer push de nada fuera de `noticias/<id>/` y `ESTADO-BOT.md` (el resto del repo lo toca solo Haniel/Claude local).

## Temas ya publicados (no repetir)
- 2026-11-21 · Fiona, la hipopótama (prueba, no se sube)
- 2026-11-21 · ¿Un pterodáctilo en México?
- 2026-11-21 · El camello vampiro

## Diario del guionista
<!-- 1–3 líneas por ejecución: fecha · noticia · lección nueva (si la hay) -->

## Diario de la fábrica
<!-- lo escribe GitHub Actions solo -->
