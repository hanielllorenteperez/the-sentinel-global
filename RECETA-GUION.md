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
`frase` (texto enorme, `resalta` en rojo una palabra, `chapa` opcional), **`pregunta`** (gran "?" rojo que late + la pregunta).
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
  - `"sonido"`: `"whoosh"`, `"impacto"`, `"latido"` o `"ninguno"`. Por defecto la fábrica pone sola impacto en flash/temblor,
    latido en las preguntas y whoosh en algunos cambios. Solo cámbialo si hace falta (p. ej. `"ninguno"` en escenas tristes).
  - En el guion (nivel general) `"rotulos": [...]` → textos de la caja roja de la cinta, que van cambiando cada 9 s.
    Por defecto: EN DIRECTO, NOTICIA EN DESARROLLO, DETRÁS DE LA VERDAD, ÚLTIMA HORA, LO QUE NO TE CUENTAN, INVESTIGACIÓN.
    Puedes poner otros que encajen con la noticia (cortos, MAYÚSCULAS, máx. 4 palabras).
  - Lo demás ya sale solo: subtítulos, barra de progreso, viñeta de cine, marca del canal y cinta.
- **Clips (cada escena = un plano):** 2 clips por escena (3 si la voz pasa de 7 s) → la imagen cambia cada 3–4 s.
  `"buscar:<plano concreto en inglés>"` pensando como director de fotografía: tipo de plano + acción + ambiente.
  Bien: `"buscar:aerial night city lights"`, `"buscar:close up hands typing dark room"`, `"buscar:police lights rain slow motion"`.
  Mal: `"buscar:news"`, `"buscar:problem"` (demasiado genérico).
  Alterna planos generales (dónde) → medios (quién) → detalle (qué). No repitas la misma búsqueda en el vídeo.
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

## 7. Derechos
- Nada de tráilers, logos de marcas, juegos ni equipos. Clips libres de Pexels/Pixabay + texto propio.
- Música: Kevin MacLeod (CC BY) al 7 % → el crédito lo pone solo la fábrica.

## 8. Checklist del director antes de hacer push
- [ ] Leí `ESTADO-BOT.md` y no repito errores ni temas.
- [ ] Gancho en los primeros 8 s, sin saludos. Promesa antes de los 30 s.
- [ ] Re-ganchos hacia 1/3 y 2/3. Bucle abierto cada 30–60 s.
- [ ] Ninguna escena con más de ~25 palabras. Nunca 3 tipos iguales seguidos.
- [ ] 2 clips por escena, búsquedas concretas y variadas; máx. 1 `wiki:` por cada 6 clips.
- [ ] Más de 800 palabras de voz en el largo; Short < 60 s.
- [ ] Añadí mi línea al "Diario del guionista" de `ESTADO-BOT.md`.
