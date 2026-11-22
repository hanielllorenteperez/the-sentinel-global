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
- 2026-11-22 · El corzo «unicornio» de Estonia (Saaremaa)
- 2026-11-22 · Insecto sin alas junto a un glaciar de la isla Navarino (Chile)

## Diario del guionista
<!-- 1–3 líneas por ejecución: fecha · noticia · lección nueva (si la hay) -->
- 2026-11-22 · Corzo «unicornio» de Estonia · WebFetch no resuelve la mayoría de dominios en la nube (solo WebSearch); las fuentes se contrastan con snippets. Día flojo de noticias: tema suave y verificable, sin inventar.
- 2026-11-22 · Insecto de glaciar en Navarino (Chile) · Búsqueda genérica de «viral hoy» sale vacía; mejor buscar «hallazgo insólito científicos» y contrastar con 3-4 medios. Contar 800+ palabras exige ~42 escenas de ~20 palabras.

## Diario de la fábrica
<!-- lo escribe GitHub Actions solo -->
- 2026-11-22 00:43 UTC · 2026-11-21-pterodactilo-mexico · ✅ subido a YouTube · run 44964848127
- 2026-11-22 00:43 UTC · 2026-11-22-corzo-unicornio-estonia · ✅ subido a YouTube · run 44964848127
- 2026-11-22 08:43 UTC · 2026-11-22-insecto-glaciar-patagonia · ✅ subido a YouTube · run 45001119725
