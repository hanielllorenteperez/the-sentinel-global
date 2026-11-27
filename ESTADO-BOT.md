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

- 2026-11-22 · Haniel: los 5 primeros vídeos fueron TODOS de naturaleza/animales/hallazgos → VARIEDAD: tecnología/IA, hackeos, dinero/cripto, videojuegos/famosos, crimen, deportes, espacio. Nunca la misma categoría seguida; naturaleza máx. 1 de cada 6 (ver RECETA-GUION.md §0b). El próximo NO puede ser de naturaleza ni de ciencia.

## Temas ya publicados (no repetir)
- 2026-11-21 · Fiona, la hipopótama (prueba, no se sube) · [naturaleza]
- 2026-11-21 · ¿Un pterodáctilo en México? · [naturaleza]
- 2026-11-21 · El camello vampiro · [naturaleza]
- 2026-11-22 · El corzo «unicornio» de Estonia (Saaremaa) · [naturaleza]
- 2026-11-22 · Insecto sin alas junto a un glaciar de la isla Navarino (Chile) · [naturaleza]
- 2026-11-22 · Welopōʻai: sistema de tres estrellas a 28 años luz «que no debería existir» · [espacio]
- 2026-11-23 · Ciberataque a 178 webs (BBC, CNN, Zoom, HSBC, IKEA) vía Optimizely · [hackeos]
- 2026-11-23 · Marc Márquez, décimo título mundial (remontada de 102 puntos, Portimão) · [deportes]
- 2026-11-24 · Anthropic: OPI récord de 81.300 M$ en el Nasdaq (ANT) · [dinero/bolsa]
- 2026-11-24 · GTA VI: récord de ventas (32,5 M copias, 3.790 M$ en 24 h), nota 99 vs 5,6 y caída de Take-Two en bolsa · [videojuegos]
- 2026-11-25 · Ueno Bank (Paraguay): colapso, renuncia de Peña, fondos del IPS · [dinero/crimen]
- 2026-11-25 · Google vende sus chips TPU a sus rivales (Apple, Meta, Anthropic) y reta a Nvidia · [tecnología/IA]
- 2026-11-26 · Final Libertadores Estudiantes–Palmeiras (28 nov, Centenario) y la revancha de 1968 · [deportes]
- 2026-11-26 · Bitcoin cae hacia los 60.000 (−50 % desde el máximo de 126.080; liquidaciones, ETF, miedo extremo) · [dinero/cripto]
- 2026-11-26 · FIFA confirma ciberataque (Handsome Boy Hacking Club, 12 GB, suplantación de identidad) · [hackeos]
- 2026-11-27 · Captura del «Chapo Isidro» (Guasave, Sinaloa), juicio en México vs extradición a EE. UU. · [crimen]
- 2026-11-27 · Jensen Huang renuncia a Nvidia (12 nov) y vuelve (23 nov): acción +31 % en un día · [tecnología/dinero]

## Diario del guionista
<!-- 1–3 líneas por ejecución: fecha · noticia · lección nueva (si la hay) -->
- 2026-11-22 · Corzo «unicornio» de Estonia · WebFetch no resuelve la mayoría de dominios en la nube (solo WebSearch); las fuentes se contrastan con snippets. Día flojo de noticias: tema suave y verificable, sin inventar.
- 2026-11-22 · Insecto de glaciar en Navarino (Chile) · Búsqueda genérica de «viral hoy» sale vacía; mejor buscar «hallazgo insólito científicos» y contrastar con 3-4 medios. Contar 800+ palabras exige ~42 escenas de ~20 palabras.
- 2026-11-22 · Sistema triple Welopōʻai (28 años luz) · Búsqueda «científicos hallazgo misterioso noviembre 2026» en modo extended da buenos temas; el script generador en Python con comprobación de @palabras y de 3 tipos seguidos ahorra revisiones. WebFetch sigue sin resolver dominios.

- 2026-11-23 · Ciberataque Optimizely (178 webs) · Buscar «hackeo ciberataque hoy» y luego el nombre técnico (Optimizely, Scott Helme) da fuentes en español e inglés; cifras que no aparecen en 2+ fuentes (p. ej. 7.040 $ / 9 h) se descartan; WebFetch sigue sin resolver dominios.
- 2026-11-23 · Márquez décimo título (MotoGP) · Buscar «noticias más vistas hoy» da portadas; luego «<tema> campeón crónica» confirma con 4+ medios. Datos dudosos (operación de hombro, 8º/9º puesto) se omiten o se señalan como no aclarados. Para 800+ palabras con escenas de ~21 palabras bastan 39 escenas.

- 2026-11-24 · Anthropic, OPI récord · Buscar «<empresa> IPO priced/debut» y luego «prospectus loss» da cifras con 5+ medios; las valoraciones (1,5/1,8/2,1 billones) difieren por momento/dilución → se explican en un gráfico en vez de elegir una. Nota: el tema trata de la empresa creadora de Claude; se contó neutral y con aviso financiero.
- 2026-11-24 · GTA VI récord y polémica · Buscar «videojuego estreno récord OR polémica noticias esta semana» (modo extended) encontró el tema; las cifras difieren por fuente (Rockstar 3.790 M$ vs Sensor Tower 2.360 M$; 39 M son jugadores, no copias) → se cuentan atribuidas y sin elegir. Búsquedas con cifras exactas ya dichas dan «no encontrado»: mejor buscar el titular de Infobae/Reuters.
- 2026-11-25 · Caso Ueno Bank · Tema muy político con fechas/cifras discrepantes entre fuentes (516/355/700 M$; resolución 2 vs 3 nov; estado de la renuncia) → se atribuyen y se aclara «analizar no es imputar». Buscar «noticias más vistas hoy <fecha>» y mirar portadas de ABC Color/Infobae dio el tema.
- 2026-11-25 · Google TPU vs Nvidia · Las búsquedas «trending hoy» de tecnología devuelven agregadores sin fecha; hay que fijar fechas con una búsqueda del nombre técnico (TPU 8tx, 9 nov). Fecha de Nvidia/OpenAI Ohio es de agosto (no es noticia de hoy) → contextualizada. Proyecciones y reportes sin confirmar (OpenAI comprando TPU) se dicen como tales.
- 2026-11-26 · Final Libertadores (previa + final de 1968) · Noticia de «mañana»: se cuenta como previa sin inventar resultado. Datos de 1968 (2-1, 1-3, desempate 2-0 en el Centenario) contrastados en RSSSF/Wikipedia/Estadio Centenario; ojo con «datos históricos» recordados de memoria (descartadas frases sin fuente). Buscar «<tema> final previa árbitro horario» da varias fuentes.
- 2026-11-26 · Bitcoin cayendo a 60.000 · WebFetch sigue sin resolver dominios; resultados de «bitcoin hoy» mezclan 2024/2025/feb-2026 → solo usar cifras con fecha 2026 visible (13-15 nov) y atribuir el cierre del 23/25 nov a Investing.com (fuente única, dicho como tal). Búsqueda «Interpol 266 detenidos» descartada: una sola fuente.
- 2026-11-26 · Hackeo a la FIFA · Buscar «hackeo ciberataque filtración datos esta semana» (extended) dio el tema con 8+ medios. Cifras de los atacantes (12 GB) vs. FIFA (<0,1 %) se atribuyen por separado; LaLiga/Comisión Europea solo aparecían en un snippet → descartados. Cuidado: sin wiki:, todo clips genéricos para no usar logos.
- 2026-11-27 · Caso Chapo Isidro · Buscar «capturado detenido narco … noviembre 2026» (extended) dio el tema; cifras de muertos/detenidos difieren → no se citan; «92 entregados» y «vigilado desde 2022» son de un solo medio → atribuidos como reporte. Tono sobrio por violencia.
- 2026-11-27 · Jensen Huang / Nvidia · Buscar «<nombre> renuncia CEO» tras ver un snippet suelto confirmó la noticia con 8+ medios; las fechas difieren (12 vs 13 nov; Forbes pone 8 nov la investigación) → se usa 12 nov y «a principios de noviembre». Temas de vida personal: solo atribuidos al New York Times y dichos como no confirmados; presión de Trump/Casa Blanca y Wachtell, de una sola fuente → omitido o marcado «no confirmado».

## Diario de la fábrica
<!-- lo escribe GitHub Actions solo -->
- 2026-11-22 00:43 UTC · 2026-11-21-pterodactilo-mexico · ✅ subido a YouTube · run 44964848127
- 2026-11-22 00:43 UTC · 2026-11-22-corzo-unicornio-estonia · ✅ subido a YouTube · run 44964848127
- 2026-11-22 08:43 UTC · 2026-11-22-insecto-glaciar-patagonia · ✅ subido a YouTube · run 45001119725
- 2026-11-22 16:46 UTC · 2026-11-22-tres-estrellas-imposibles · ✅ subido a YouTube · run 45041811222
- 2026-11-23 00:36 UTC · 2026-11-23-ciberataque-178-webs-optimizely · ✅ subido a YouTube · run 45086683789
- 2026-11-23 08:35 UTC · 2026-11-23-marquez-decimo-titulo · ✅ subido a YouTube · run 45135743577
- 2026-11-24 00:42 UTC · 2026-11-24-anthropic-salida-bolsa-record · ✅ subido a YouTube · run 45294307428
- 2026-11-24 16:43 UTC · 2026-11-24-gta6-record-ventas · ✅ subido a YouTube · run 45433083288
- 2026-11-25 00:44 UTC · 2026-11-25-ueno-bank-paraguay · ✅ subido a YouTube · run 45515199342
- 2026-11-25 08:40 UTC · 2026-11-25-google-chips-contra-nvidia · ✅ subido a YouTube · run 45573305371
- 2026-11-26 00:47 UTC · 2026-11-26-final-libertadores-estudiantes-palmeiras · ✅ subido a YouTube · run 45726190334
- 2026-11-26 08:35 UTC · 2026-11-26-bitcoin-cae-60000 · ✅ subido a YouTube · run 45780173887
- 2026-11-26 16:41 UTC · 2026-11-26-fifa-hackeo-12gb · ✅ subido a YouTube · run 45855467166
- 2026-11-27 00:39 UTC · 2026-11-27-chapo-isidro-captura · ✅ subido a YouTube · run 45914568116
