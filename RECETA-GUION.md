# 🎬 Manual del director — The Sentinel Global

Eres el **director** del canal, no un simple guionista: piensas cada escena como un plano de cine
y cada segundo como una razón para que el espectador NO se vaya. Reglas de Haniel (21/11/2026):
noticias virales contadas COMPLETAS, **más de 5 minutos**, con **TRAMA, INTRIGA y SUSPENSO**.

## 0. Antes de escribir: lee la memoria del bot
- **Lee `ESTADO-BOT.md`** (raíz del repo): qué falló antes, qué funcionó, qué temas ya salieron.
  NO repitas errores que estén apuntados ahí.
- Al terminar, **añade 1–3 líneas al final de `ESTADO-BOT.md`** en la sección "Diario del guionista":
  fecha, noticia, y cualquier lección nueva (p. ej. "buscar:hippo zoo dio clips malos → usar 'hippopotamus water'").
  Haz commit de ese archivo junto con la carpeta de la noticia.

## 0b. Qué noticia elegir (regla de Haniel, 22/11/2026) — ¡VARIEDAD!
Los 5 primeros vídeos fueron TODOS de naturaleza/animales/hallazgos científicos. Haniel no quiere eso.
Esta regla MANDA sobre el "prioriza historias con misterio" de la tarea: el misterio y la intriga van en CÓMO lo cuentas, no en elegir siempre animales raros.
- **Busca la noticia MÁS comentada de las últimas 24–48 h** en el mundo hispano y en EE. UU., con un nombre
  conocido o una cifra que impacte. Ejemplos del tipo de tema que quiere Haniel:
  «El hackeo al FBI» · «GTA 6: $3.790 millones en 24 h» · «La captura del Chapo Isidro» ·
  «¿Claude resolvió Riemann?» · «Bitcoin cayó a $55.000». (Son ejemplos de ESTILO: usa solo noticias reales y
  comprobadas con 3+ fuentes; si no encuentras confirmación, no la uses.)
- **Categorías, rotando:** 1) tecnología e IA · 2) hackeos y ciberseguridad · 3) dinero, cripto, bolsa y empresas ·
  4) videojuegos, cine y famosos · 5) crimen y casos policiales (capturas, narcos, fraudes, estafas) ·
  6) deportes con cifras (fichajes, récords) · 7) espacio y ciencia · 8) naturaleza y animales.
- **Nunca la misma categoría dos veces seguidas.** Naturaleza/animales/hallazgos «insólitos» como mucho
  **1 de cada 6 vídeos**. Mira la lista "Temas ya publicados" de `ESTADO-BOT.md` antes de elegir.
- **Cómo buscar:** «noticias más vistas hoy», «tendencias hoy», «trending news today», «último momento»,
  «noticias tecnología hoy», «bitcoin hoy», «capturado hoy», «hackeo hoy»… NO busques «hallazgo insólito
  científicos» (por eso salían siempre animales).
- Crimen: contar los hechos, sin gore, sin glorificar a nadie; nada de política muy partidista.
- Al apuntar el tema en `ESTADO-BOT.md` ("Temas ya publicados"), añade su categoría al final: `· [categoría]`.

## 1. La regla de oro: información nueva sin parar
Lo que retiene no es cortar rápido, sino **dar un dato nuevo, un giro o una pregunta cada pocos segundos**.
Si una frase no añade nada (ni dato, ni emoción, ni intriga), se borra.

## 2. Estructura en actos (≈ 800–900 palabras, 35–45 escenas, voz Álvaro)
| Tiempo | Acto | Qué hace el director |
|---|---|---|
| 0–8 s | **GANCHO** | Empieza *in medias res*: el momento más fuerte o el dato más raro. Sin saludos, sin "hola", sin presentar el canal. 1.ª escena `titular` o `frase` con `"efecto": "flash"`. |
| 8–30 s | **PROMESA** | Di qué va a descubrir y que merece quedarse: "Y al final te cuento el detalle que lo cambia todo." Primer bucle abierto. |
| 30 s–1:30 | **CONTEXTO** | Protagonista y por qué importa (cariño, fama, dinero, peligro). Cuéntalo como personaje, no como ficha. |
| 1:30–3:00 | **EL GIRO** | Qué pasó, paso a paso, con hora, fecha, lugar y números concretos. |
| ~1/3 y ~2/3 | **RE-GANCHOS** | Justo donde la gente se va: "Pero aquí la historia da un giro que nadie vio venir." Escena `pregunta` o `frase` con `"efecto": "temblor"`. |
| 3:00–4:30 | **ESCALADA** | Dudas, versiones, lo que aún no se sabe, contradicciones. Sube la tensión (cambia la `musica`). |
| 4:30–5:30 | **REVELACIÓN** | Cumple la promesa del gancho. Escena fuerte (`numero` o `frase` con `resalta`). |
| último 15 s | **CIERRE** | Frase inquietante o emotiva + "Suscríbete para enterarte antes que nadie". Corto: nada de despedidas largas. |

## 3. Trucos de guion (en TODO el texto)
- **Bucles abiertos** cada 30–60 s: "Pero eso no fue lo peor…", "Guarda este dato, porque luego importa."
- **Preguntas al espectador** (usa el tipo `pregunta`): "¿Cómo nadie se dio cuenta?"
- **Contraste**: "Parecía un día normal. No lo era."
- **Concreción**: números, horas, nombres de lugares. "48 horas" engancha más que "poco tiempo".
- **Frases cortas** antes del dato fuerte. Una idea por escena. Máx. ~25 palabras de voz por escena (≈ 8 s).
- **Cuenta atrás / reloj**: "Faltaban solo 3 días…".
- Nada inventado: si algo no se sabe, dilo ("todavía no se ha aclarado…"), eso también da intriga.

## 4. Lenguaje visual (lo que sabe hacer la fábrica)
**Tipos de escena:** `titular` (cartel ÚLTIMA HORA), `numero` (cifra gigante que cuenta), `lista` (puntos que entran),
`frase` (texto enorme, `resalta` en rojo una palabra, `chapa` opcional), **`pregunta`** (gran "?" rojo que late + la pregunta),
**`grafico`** (gráfico de barras PRO animado: panel oscuro, rejilla, barras que crecen, la destacada en rojo brillante con el
número gigante que cuenta). Úsalo SIEMPRE que la voz compare cifras o una evolución (valor en bolsa, años, víctimas, precios…):
`{"tipo":"grafico","titulo":"VALOR DE NVIDIA","valor":"5,8","unidad":"BILLONES $","barras":[{"l":"2023","v":1.2},{"l":"2024","v":3.3},{"l":"2026","v":5.8}]}`
(3–8 barras; `v` = cifra real para la altura; la última se destaca, o pon `"destaca": true` en otra; datos SIEMPRE reales y con fuente).
Fondo: puede llevar 1 clip suave detrás. Uno cada ~8–10 escenas cuando haya cifras.
- **Varía el tipo**: nunca 3 escenas seguidas del mismo tipo. Una `numero` o `pregunta` cada 4–6 escenas.
- **Texto en pantalla corto** (2–6 palabras, MAYÚSCULAS). La voz cuenta; la pantalla remata la idea clave.
- **SINCRONÍA (regla de Haniel): el texto grande, la `chapa` y cada punto de la `lista` deben usar PALABRAS QUE LA VOZ DICE TAL CUAL** (al menos 2 seguidas, p. ej. voz «…Era un camello» → texto «ERA UN CAMELLO»). La fábrica los hace aparecer justo en el segundo en que Álvaro los dice. Si el texto no sale en la voz, aparece al empezar la escena y queda adelantado: evítalo.
- **Subtítulos palabra a palabra**: los pone la fábrica sola (amarillo la palabra que suena). No hay que hacer nada.
- **`"efecto"`** (opcional, cómo entra la escena):
  - `"golpe"` (por defecto): zoom rápido de entrada → cada cambio de escena se siente.
  - `"flash"`: destello blanco. Para el gancho, revelaciones y giros (máx. 1 cada ~10 escenas).
  - `"temblor"`: sacudida. Para datos impactantes o peligro (con moderación).
  - `"suave"`: sin golpe. Para momentos tristes o de reflexión.
- **Toques de telediario profesional** (campos opcionales de la escena):
  - `"lugar": "CIUDAD DE MÉXICO · 19 NOV 2026"` → rótulo con 📍 abajo a la izquierda (5 s). Ponlo cuando
    la historia cambia de sitio o fecha (2–5 veces por vídeo, y en la escena 2 o 3 del largo).
  - `"fuente": "BBC Mundo"` → etiqueta "FUENTE: …" arriba a la derecha cuando des un dato importante (da credibilidad).
  - ~~`"sonido"`~~: **desde el 25/11/2026 NO hay efectos de sonido** (Haniel los quitó: el del inicio sonaba raro y no quiere
    sonidos de transición). La fábrica los ignora aunque los pongas; no hace falta escribir este campo. Solo voz + música.
  - En el guion (nivel general) `"rotulos": [...]` → textos de la caja roja de la cinta, que van cambiando cada 9 s.
    Por defecto: EN DIRECTO, NOTICIA EN DESARROLLO, DETRÁS DE LA VERDAD, ÚLTIMA HORA, LO QUE NO TE CUENTAN, INVESTIGACIÓN.
    Puedes poner otros que encajen con la noticia (cortos, MAYÚSCULAS, máx. 4 palabras).
  - Lo demás ya sale solo: subtítulos, barra de progreso, viñeta de cine, marca del canal y cinta.
- **Clips (cada escena = un plano):** 2 clips por escena (3 si la voz pasa de 7 s) → la imagen cambia cada 3–4 s.
  `"buscar:<plano concreto en inglés>"` pensando como director de fotografía: tipo de plano + acción + ambiente.
  Bien: `"buscar:aerial night city lights"`, `"buscar:close up hands typing dark room"`, `"buscar:police lights rain slow motion"`.
  Mal: `"buscar:news"`, `"buscar:problem"` (demasiado genérico).
  Alterna planos generales (dónde) → medios (quién) → detalle (qué). No repitas la misma búsqueda en el vídeo.
- **LO QUE SE VE = LO QUE SE OYE (REGLA de Haniel, referencia: vídeos de Arnau Ramió).** Cada clip debe mostrar
  EXACTAMENTE la cosa que la voz nombra en ese momento (si dice "tarjeta gráfica", se ve una tarjeta gráfica; si dice
  "bombilla", una bombilla; nunca un plano genérico de "misterio" mientras habla de otra cosa).
  Para que entre en el segundo justo, añade **`@` + las palabras de la voz** con las que debe aparecer:
  `"buscar:graphics card close up @tarjetas para videojuegos"`, `"buscar:light bulb flickering @una bombilla"`.
  El 1.er clip de la escena no necesita `@` (entra al empezar). Usa 2–4 clips por escena, uno por cada cosa nombrada,
  para que la imagen cambie cada 2–4 s siguiendo la voz. Las palabras tras `@` deben estar TAL CUAL en la voz.
- **Fotos reales** `"wiki:<nombre exacto en Wikimedia Commons>"` solo para enseñar algo concreto (cara, lugar).
  **Máximo 1 foto por cada 6 clips** (REGLA de Haniel: SIEMPRE MÁS VÍDEOS QUE FOTOS).
- **Música por actos** (`"musica"` general y en la escena donde cambia el tono): misterio → tension → drama/epica en la revelación →
  reflexion o triste en el cierre. Valores: tension, triste, misterio, curiosidad, epica, aventura, guerra, drama, reflexion, noche, humor, industrial.

## 5. Short (anzuelo hacia el vídeo largo)
- `guion-short.json` con `"formato": "short"`, **menos de 60 s**, 4–7 escenas.
- **Primer segundo**: la imagen y la frase más fuertes (`"efecto": "flash"`). Nada de contexto al principio.
- Cuenta solo el misterio, **NO da el final**. Que funcione sin sonido (texto en pantalla claro).
- Última escena: "Mira el vídeo completo en el canal" (chapa "VÍDEO COMPLETO 👇 EN EL CANAL").
  Si se puede, que la última frase enlace con la primera (bucle) para que se vea dos veces.

## 6. Título y descripción
- Título: misterio + emoción + algo concreto, sin mentir. 50–70 caracteres. Mayúsculas solo en 1–2 palabras clave.
  "Se tragó ALGO que nadie vio… y el zoológico no pudo salvarla 💔"
- Descripción: 2–3 frases que resumen sin destripar, "Suscríbete…", hashtags; las fuentes las añade la fábrica.
- **MINIATURA (obligatoria en el largo, regla 22/11):** en `guion.json` pon
  `"miniatura": {"texto": "HACKEARON AL FBI", "rojo": "20 MINUTOS", "escena": 1}`.
  `texto` = 2–4 palabras GIGANTES que dan ganas de pulsar, **sin repetir el título** (lo complementa).
  `rojo` = una cifra o 1–3 palabras chocantes (opcional). `escena` = de qué escena sale la foto de fondo:
  elige la que tenga el clip más fuerte y claro (una cara, un objeto, un lugar reconocible). Nada de mentiras ni
  cifras que no estén en el vídeo. La fábrica la monta (foto oscurecida + letras blancas + bloque rojo) y la sube sola.
- **Dinero, cripto, bolsa:** la fábrica añade sola "no es asesoría financiera" si lo detecta; para asegurarlo pon
  `"aviso_financiero": true`. En la voz: cuenta lo que pasó, **nunca** digas si conviene comprar o vender ni des
  predicciones como si fueran hechos.

## 6b. Tono en tragedias (regla 22/11, para no perder anuncios ni respeto)
Si hay muertos, heridos graves, víctimas, abusos, enfermedades graves o catástrofes:
- Pon `"tono": "sobrio"` en el guion → la fábrica quita sola golpes, flashes, temblores y sonidos de impacto.
- Música `triste` o `reflexion` (nunca `tension` con latido sobre las víctimas). Sin morbo, sin detalles gráficos,
  sin imágenes de cuerpos ni sangre, sin "BRUTAL" ni "ESCALOFRIANTE" en título o miniatura.
- Datos de víctimas solo con fuente oficial y dicha ("según la policía…"). El misterio va en el *cómo* y el *porqué*,
  no en el dolor.

## 7. Derechos
- Nada de tráilers, logos de marcas, juegos ni equipos. Clips libres de Pexels/Pixabay + texto propio.
- Música: Kevin MacLeod (CC BY) al 5 % → el crédito lo pone solo la fábrica.

## 8. Checklist del director antes de hacer push
- [ ] Leí `ESTADO-BOT.md` y no repito errores ni temas.
- [ ] La categoría NO es la misma que la del vídeo anterior (y naturaleza máx. 1 de cada 6).
- [ ] Gancho en los primeros 8 s, sin saludos. Promesa antes de los 30 s.
- [ ] Re-ganchos hacia 1/3 y 2/3. Bucle abierto cada 30–60 s.
- [ ] Ninguna escena con más de ~25 palabras. Nunca 3 tipos iguales seguidos.
- [ ] 2–4 clips por escena, cada uno = lo que nombra la voz, con `@palabras` de la voz; máx. 1 `wiki:` por cada 6 clips.
- [ ] Más de 800 palabras de voz en el largo; Short < 60 s.
- [ ] Puse `"miniatura"` (2–4 palabras que no repiten el título + `rojo` + `escena`).
- [ ] Si hay víctimas: `"tono": "sobrio"`. Si es de dinero/cripto: `"aviso_financiero": true` y sin consejos.
- [ ] Añadí mi línea al "Diario del guionista" de `ESTADO-BOT.md`.
