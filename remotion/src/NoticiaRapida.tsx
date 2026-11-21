import React from "react";
import {
  AbsoluteFill,
  Audio,
  CalculateMetadataFunction,
  Img,
  Loop,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// ============================================================
// FÁBRICA DE NOTICIAS RÁPIDAS (estilo aprobado v4, 21/11/2026)
// Lo rellena solo el script YouTube Faceless\fabrica\fabrica.py
// (props.json). Voz Álvaro −8 %, clips Pexels oscurecidos con zoom
// lento, letras rojo/blanco/azul, cinta "EN DIRECTO", música al 7 %.
// ============================================================

export const NR_FPS = 30;
const PAUSA = 0.3; // segundos de aire después de cada frase
const COLA = 15; // frames de fundido al final

export type ClipInfo = { src: string; dur: number };
export type Escena = {
  tipo: "titular" | "numero" | "lista" | "frase" | "pregunta";
  voz: string; // ruta dentro de public/
  dur: number; // segundos de la voz
  clips: ClipInfo[];
  etiqueta?: string;
  texto?: string;
  arriba?: string;
  numero?: string;
  chapa?: string;
  titulo?: string;
  items?: string[];
  resalta?: string;
  musica?: string; // cambia la música desde esta escena
  // GANCHOS VISUALES (manual del director): cómo entra la escena
  efecto?: "golpe" | "flash" | "temblor" | "suave";
  palabras?: Palabra[]; // cuándo suena cada palabra (lo pone la fábrica) → subtítulos
};
export type Palabra = { t: number; d: number; w: string };
export type NoticiaProps = {
  cinta: string;
  musica: string;
  volumenMusica?: number;
  marca?: string; // nombre del canal arriba a la izquierda
  subtitulos?: boolean; // subtítulos palabra a palabra (por defecto sí)
  escenas: Escena[];
};

const tramo = (e: Escena) => Math.round((e.dur + PAUSA) * NR_FPS);
export const duracionNoticia = (p: NoticiaProps) => p.escenas.reduce((a, e) => a + tramo(e), 0) + COLA;

export const calcularNoticia: CalculateMetadataFunction<NoticiaProps> = ({ props }) => ({
  durationInFrames: Math.max(30, duracionNoticia(props)),
});

const ROJO = "#d7141a";
const AZUL = "#0b1f4b";
const CREMA = "#f4efe6";
const FUENTE = "'Arial Black', 'Helvetica Neue', Arial, sans-serif";
const SOMBRA = "0 10px 40px rgba(0,0,0,.6)";

// Tamaño de letra que se adapta al largo del texto
const useVertical = () => {
  const { width, height } = useVideoConfig();
  return height > width;
};

const tam = (t: string, grande: number, minimo: number, cabe: number) =>
  Math.max(minimo, Math.min(grande, Math.round((grande * cabe) / Math.max(cabe, t.length))));

const Cinta: React.FC<{ texto: string }> = ({ texto }) => {
  const f = useCurrentFrame();
  const x = -((f * 4) % 1400);
  const v = useVertical();
  return (
    <div style={{ position: "absolute", bottom: v ? 330 : 0, left: 0, right: 0, height: 86, display: "flex" }}>
      <div style={{ background: ROJO, color: "white", fontFamily: FUENTE, fontSize: 34, padding: "0 34px", display: "flex", alignItems: "center", zIndex: 2 }}>
        EN DIRECTO
      </div>
      <div style={{ flex: 1, background: CREMA, overflow: "hidden", display: "flex", alignItems: "center" }}>
        <div style={{ whiteSpace: "nowrap", transform: `translateX(${x}px)`, fontFamily: FUENTE, fontSize: 32, color: AZUL }}>
          {(texto.toUpperCase() + " · ").repeat(6)}
        </div>
      </div>
    </div>
  );
};

const Marca: React.FC<{ texto: string }> = ({ texto }) => {
  const v = useVertical();
  if (!texto) return null;
  return (
    <div style={{ position: "absolute", top: v ? 120 : 40, left: v ? 50 : 50, display: "flex", alignItems: "center", gap: 14 }}>
      <div style={{ width: 18, height: 18, borderRadius: 9, background: ROJO, boxShadow: "0 0 12px rgba(215,20,26,.8)" }} />
      <div style={{ fontFamily: FUENTE, fontSize: v ? 34 : 30, color: "white", letterSpacing: 3, textShadow: "0 3px 12px rgba(0,0,0,.8)" }}>{texto}</div>
    </div>
  );
};

const Chapa: React.FC<{ t?: string; desde: number }> = ({ t, desde }) => {
  const f = useCurrentFrame();
  if (!t) return null;
  const o = interpolate(f, [desde, desde + 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ marginTop: 36, opacity: o, display: "inline-block", background: ROJO, color: "white", fontFamily: FUENTE, fontSize: 52, padding: "12px 40px" }}>
      {t}
    </div>
  );
};

const Titular: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 12 } });
  const parpadeo = Math.floor(f / 8) % 2 === 0 ? 1 : 0.9;
  const t = e.texto ?? "";
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", textAlign: "center", padding: "0 100px 86px" }}>
      <div style={{ transform: `scale(${s})`, background: ROJO, padding: "22px 64px", fontFamily: FUENTE, fontSize: 120, color: "white", letterSpacing: 4, opacity: parpadeo, boxShadow: "0 20px 60px rgba(0,0,0,.5)" }}>
        {e.etiqueta ?? "ÚLTIMA HORA"}
      </div>
      <div style={{ marginTop: 40, fontFamily: FUENTE, fontSize: tam(t, 84, 50, 22), color: "white", textShadow: SOMBRA, lineHeight: 1.1, opacity: interpolate(f, [12, 30], [0, 1], { extrapolateRight: "clamp" }) }}>
        {t}
      </div>
    </AbsoluteFill>
  );
};

const Numero: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const raw = e.numero ?? "";
  const esNum = /^\d+$/.test(raw) && raw.length < 4; // años (2017) no se cuentan
  const n = esNum ? Math.round(interpolate(f, [5, 40], [0, Number(raw)], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })) : raw;
  const entra = spring({ frame: f - 30, fps, config: { damping: 14 } });
  const zoomNum = esNum ? 1 : spring({ frame: f, fps, config: { damping: 12 } });
  const t = e.texto ?? "";
  const v = useVertical();
  return (
    <AbsoluteFill style={v ? { flexDirection: "column", justifyContent: "center", alignItems: "center", textAlign: "center", padding: "0 70px 420px", gap: 30 } : { flexDirection: "row", alignItems: "center", padding: "0 120px 86px", gap: 70 }}>
      <div style={{ fontFamily: FUENTE, fontSize: raw.length > 3 ? 260 : 360, color: ROJO, lineHeight: 1, textShadow: SOMBRA, transform: `scale(${zoomNum})` }}>{n}</div>
      <div style={{ transform: v ? `translateY(${(1 - entra) * 200}px)` : `translateX(${(1 - entra) * 300}px)`, opacity: entra, flex: v ? undefined : 1 }}>
        {e.arriba && <div style={{ fontFamily: FUENTE, fontSize: 50, color: CREMA }}>{e.arriba}</div>}
        <div style={{ fontFamily: FUENTE, fontSize: tam(t, 92, 56, 20), color: "white", lineHeight: 1.05, textShadow: SOMBRA }}>{t}</div>
        {e.chapa && (
          <div style={{ marginTop: 26, display: "inline-block", background: CREMA, color: AZUL, fontFamily: FUENTE, fontSize: 44, padding: "8px 24px" }}>{e.chapa}</div>
        )}
      </div>
    </AbsoluteFill>
  );
};

const Lista: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const items = e.items ?? [];
  const paso = Math.max(18, Math.min(40, Math.round((e.dur * fps * 0.6) / Math.max(1, items.length))));
  return (
    <AbsoluteFill style={{ justifyContent: "center", padding: "0 160px 86px" }}>
      {e.titulo && <div style={{ fontFamily: FUENTE, fontSize: 52, color: CREMA, marginBottom: 40, letterSpacing: 6 }}>{e.titulo}</div>}
      {items.map((c, i) => {
        const s = spring({ frame: f - 15 - i * paso, fps, config: { damping: 13 } });
        return (
          <div key={c} style={{ display: "flex", alignItems: "center", gap: 30, marginBottom: 34, opacity: s, transform: `translateX(${(1 - s) * -400}px)` }}>
            <div style={{ width: 70, height: 70, flexShrink: 0, background: ROJO, color: "white", fontFamily: FUENTE, fontSize: 44, display: "flex", justifyContent: "center", alignItems: "center" }}>
              {i + 1}
            </div>
            <div style={{ fontFamily: FUENTE, fontSize: tam(c, 84, 52, 22), color: "white", textShadow: SOMBRA }}>{c}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Frase: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 10 } });
  const t = e.texto ?? "";
  const r = e.resalta;
  const partes = r && t.includes(r) ? t.split(r) : [t];
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", textAlign: "center", padding: "0 100px 86px" }}>
      <div style={{ fontFamily: FUENTE, fontSize: tam(t, 140, 70, 16), color: "white", transform: `scale(${s})`, textShadow: SOMBRA, lineHeight: 1.1 }}>
        {partes.length > 1 ? (
          <>
            {partes[0]}
            <span style={{ color: ROJO }}>{r}</span>
            {partes.slice(1).join(r)}
          </>
        ) : (
          t
        )}
      </div>
      <Chapa t={e.chapa} desde={Math.round(e.dur * fps * 0.5)} />
    </AbsoluteFill>
  );
};

// Pregunta al espectador: gran "?" rojo que late + la pregunta
const Pregunta: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 9 } });
  const late = 1 + Math.sin(f / 6) * 0.04;
  const t = e.texto ?? "";
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", textAlign: "center", padding: "0 100px 86px" }}>
      <div style={{ fontFamily: FUENTE, fontSize: 300, color: ROJO, lineHeight: 0.9, transform: `scale(${s * late})`, textShadow: SOMBRA }}>?</div>
      <div style={{ marginTop: 20, fontFamily: FUENTE, fontSize: tam(t, 100, 58, 20), color: "white", textShadow: SOMBRA, lineHeight: 1.1, opacity: interpolate(f, [8, 22], [0, 1], { extrapolateRight: "clamp" }) }}>
        {t}
      </div>
    </AbsoluteFill>
  );
};

// SUBTÍTULOS palabra a palabra: grupos de hasta 3 palabras, la que suena en amarillo y más grande.
const AMARILLO = "#ffd400";
const grupos = (ps: Palabra[]) => {
  const out: Palabra[][] = [];
  let g: Palabra[] = [];
  ps.forEach((p, i) => {
    const pausa = i > 0 ? p.t - (ps[i - 1].t + ps[i - 1].d) : 0;
    if (g.length >= 3 || (g.length > 0 && pausa > 0.35)) {
      out.push(g);
      g = [];
    }
    g.push(p);
  });
  if (g.length) out.push(g);
  return out;
};
const Subtitulos: React.FC<{ ps: Palabra[] }> = ({ ps }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const v = useVertical();
  const s = f / fps;
  const gs = grupos(ps);
  const g = gs.find((x, i) => s >= x[0].t - 0.05 && s < (gs[i + 1]?.[0].t ?? x[x.length - 1].t + x[x.length - 1].d + 0.4));
  if (!g) return null;
  const ini = Math.round(g[0].t * fps);
  const pop = spring({ frame: f - ini, fps, config: { damping: 11, mass: 0.6 } });
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: v ? 560 : 120, display: "flex", justifyContent: "center", gap: v ? 22 : 18, padding: "0 60px", flexWrap: "wrap", transform: `scale(${0.85 + pop * 0.15})` }}>
      {g.map((p, i) => {
        const activa = s >= p.t - 0.03 && s < p.t + p.d + 0.08;
        return (
          <span key={i} style={{ fontFamily: FUENTE, fontSize: v ? 78 : 58, color: activa ? AMARILLO : "white", transform: activa ? "translateY(-6px)" : "none", display: "inline-block", textTransform: "uppercase", WebkitTextStroke: v ? "3px black" : "2px black", textShadow: "0 6px 18px rgba(0,0,0,.9)" }}>
            {p.w}
          </span>
        );
      })}
    </div>
  );
};

// ENTRADA de cada escena (gancho visual / "pattern interrupt"): cada cambio de escena se SIENTE.
const Entrada: React.FC<{ efecto?: Escena["efecto"]; children: React.ReactNode }> = ({ efecto = "golpe", children }) => {
  const f = useCurrentFrame();
  let escala = 1;
  let x = 0;
  let y = 0;
  if (efecto === "golpe" || efecto === "flash") escala = interpolate(f, [0, 7], [1.12, 1], { extrapolateRight: "clamp" });
  if (efecto === "temblor" && f < 14) {
    const k = (14 - f) * 1.6;
    x = Math.sin(f * 2.7) * k;
    y = Math.cos(f * 3.1) * k;
  }
  const blanco = efecto === "flash" ? interpolate(f, [0, 5], [0.85, 0], { extrapolateRight: "clamp" }) : 0;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ transform: `translate(${x}px, ${y}px) scale(${escala})` }}>{children}</AbsoluteFill>
      {blanco > 0 && <AbsoluteFill style={{ background: "white", opacity: blanco }} />}
    </AbsoluteFill>
  );
};

// Barra de progreso arriba (solo vídeo largo): el espectador ve que avanza y se queda.
const Barra: React.FC<{ total: number }> = ({ total }) => {
  const f = useCurrentFrame();
  return <div style={{ position: "absolute", top: 0, left: 0, height: 8, width: `${(f / total) * 100}%`, background: ROJO, boxShadow: "0 0 10px rgba(215,20,26,.8)" }} />;
};

// Clip real de fondo con zoom lento, oscurecido; se repite si es corto.
const Clip: React.FC<{ c: ClipInfo }> = ({ c }) => {
  const f = useCurrentFrame();
  const esFoto = /\.(jpe?g|png|webp)$/i.test(c.src);
  // Fotos (Wikimedia Commons): zoom y desplazamiento lentos tipo documental
  const zoom = esFoto ? 1.08 + f * 0.0012 : 1.05 + f * 0.0008;
  const mover = esFoto ? `translateX(${-f * 0.15}px)` : "";
  const dur = Math.max(15, Math.floor(c.dur * NR_FPS) - 2);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `scale(${zoom}) ${mover}` }}>
        {esFoto ? (
          <Img src={staticFile(c.src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : (
          <Loop durationInFrames={dur}>
            <OffthreadVideo src={staticFile(c.src)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </Loop>
        )}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(5,13,34,.82) 0%, rgba(5,13,34,.55) 55%, rgba(5,13,34,.35) 100%)" }} />
    </AbsoluteFill>
  );
};

const Fondos: React.FC<{ clips: ClipInfo[]; total: number }> = ({ clips, total }) => {
  if (clips.length === 0) return <AbsoluteFill style={{ background: AZUL }} />;
  const cada = Math.floor(total / clips.length);
  return (
    <>
      {clips.map((c, i) => (
        <Sequence key={i} from={i * cada} durationInFrames={i === clips.length - 1 ? total - i * cada : cada}>
          <Clip c={c} />
        </Sequence>
      ))}
    </>
  );
};

// Tramos de música: [desde, hasta) en frames, cambiando cuando una escena trae "musica".
const tramosMusica = (p: NoticiaProps) => {
  const total = duracionNoticia(p);
  const out: { src: string; desde: number; hasta: number }[] = [];
  let t = 0;
  let actual = p.musica;
  p.escenas.forEach((e, i) => {
    if (i === 0 || (e.musica && e.musica !== actual)) {
      if (e.musica) actual = e.musica;
      if (out.length) out[out.length - 1].hasta = t;
      out.push({ src: actual, desde: t, hasta: total });
    }
    t += tramo(e);
  });
  return out;
};

const TIPOS = { titular: Titular, numero: Numero, lista: Lista, frase: Frase, pregunta: Pregunta };

export const NoticiaRapida: React.FC<NoticiaProps> = (p) => {
  const f = useCurrentFrame();
  const total = duracionNoticia(p);
  const vol = p.volumenMusica ?? 0.07;
  const fin = interpolate(f, [total - COLA, total], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  let inicio = 0;
  const { width, height } = useVideoConfig();
  const v = height > width;
  const k = v ? 0.8 : 1; // en vertical las letras se encogen un poco
  const capa = v ? { width: width / k, height: height / k, transform: `scale(${k})`, transformOrigin: "top left" } : {};
  return (
    <AbsoluteFill style={{ opacity: fin, background: AZUL }}>
      {/* Música según el ambiente (Kevin MacLeod, CC BY 4.0 → la fábrica pone el crédito en la descripción).
          Una escena con "musica" cambia de canción desde ahí, con fundido de 1 s. */}
      {tramosMusica(p).map((m, i) => {
        const X = 30;
        const desde = Math.max(0, m.desde - (i > 0 ? X : 0));
        const largo = m.hasta - desde;
        const finM = m.hasta >= total ? 40 : X;
        return (
          <Sequence key={`m${i}`} from={desde} durationInFrames={largo}>
            <Audio
              src={staticFile(m.src)}
              loop
              volume={(fr) =>
                interpolate(fr, [0, i > 0 ? X : 20, largo - finM, largo], [0, vol, vol, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
              }
            />
          </Sequence>
        );
      })}
      {p.escenas.map((e, i) => {
        const T = TIPOS[e.tipo] ?? Frase;
        const dur = tramo(e) + (i === p.escenas.length - 1 ? COLA : 0);
        const desde = inicio;
        inicio += tramo(e);
        return (
          <Sequence key={i} from={desde} durationInFrames={dur}>
            <Entrada efecto={e.efecto ?? (i === 0 ? "flash" : "golpe")}>
              <Fondos clips={e.clips} total={dur} />
              <AbsoluteFill style={capa}>
                <T e={e} />
              </AbsoluteFill>
            </Entrada>
            {p.subtitulos !== false && e.palabras && e.palabras.length > 0 && <Subtitulos ps={e.palabras} />}
            <Audio src={staticFile(e.voz)} />
          </Sequence>
        );
      })}
      {!v && <Barra total={total} />}
      <Marca texto={p.marca ?? "THE SENTINEL GLOBAL"} />
      <Cinta texto={p.cinta} />
    </AbsoluteFill>
  );
};

export const NOTICIA_EJEMPLO: NoticiaProps = {
  cinta: "Fábrica de noticias · ejemplo",
  musica: "musica/tension--interloper.mp3",
  escenas: [
    { tipo: "titular", voz: "noticia/v1.mp3", dur: 3.12, clips: [{ src: "noticia/c1-policia.mp4", dur: 10 }], etiqueta: "ÚLTIMA HORA", texto: "EJEMPLO DE NOTICIA" },
  ],
};
