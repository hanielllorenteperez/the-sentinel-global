# -*- coding: utf-8 -*-
r"""
MINIATURA del vídeo largo (1280x720, JPG < 2 MB), estilo The Sentinel:
foto oscurecida de un clip de la noticia + 2-3 palabras GIGANTES en blanco + bloque rojo con un dato.

En el guion (opcional, recomendado):
  "miniatura": {"texto": "HACKEARON AL FBI", "rojo": "20 MINUTOS", "escena": 1}
    texto  = 2-4 palabras gigantes (NO repetir el título)
    rojo   = 1-3 palabras o cifra del bloque rojo (opcional)
    escena = de qué escena sale la imagen de fondo (por defecto la 1, el gancho)
Si no hay "miniatura", usa el titular de la escena 1 o el principio del título.

  python fabrica/miniatura.py <guion.json> <carpeta-con-clips> <salida.jpg>   (prueba a mano)
"""
import glob
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1280, 720
ROJO = (214, 28, 36)


def _fuente(tam):
    for p in (glob.glob("/usr/share/fonts/truetype/msttcorefonts/[Aa]rial_[Bb]lack.ttf")
              + glob.glob("/usr/share/fonts/truetype/msttcorefonts/ariblk.ttf")
              + [r"C:\Windows\Fonts\ariblk.ttf"]
              + glob.glob("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    return ImageFont.load_default()


def _ffmpeg(remotion):
    for p in glob.glob(os.path.join(remotion, "node_modules", "@remotion", "compositor-*", "ffmpeg*")):
        if not p.endswith((".d.ts", ".js")):
            return p
    return shutil.which("ffmpeg") or "ffmpeg"


def fotograma(clip, destino, remotion, seg=2.0):
    if clip.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        return Image.open(clip).convert("RGB")
    subprocess.run([_ffmpeg(remotion), "-y", "-loglevel", "error", "-ss", str(seg), "-i", clip,
                    "-frames:v", "1", destino], check=False)
    if not os.path.exists(destino):  # clip más corto que 2 s
        subprocess.run([_ffmpeg(remotion), "-y", "-loglevel", "error", "-i", clip, "-frames:v", "1", destino], check=False)
    return Image.open(destino).convert("RGB")


def _recortar(img):
    """Rellena 1280x720 sin deformar (recorta lo que sobra)."""
    r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


def _lineas(texto, fuente, ancho, d):
    pal, out, act = texto.split(), [], ""
    for p in pal:
        prueba = (act + " " + p).strip()
        if d.textlength(prueba, font=fuente) <= ancho or not act:
            act = prueba
        else:
            out.append(act)
            act = p
    if act:
        out.append(act)
    return out


def textos_de(g):
    m = g.get("miniatura") or {}
    texto = (m.get("texto") or "").strip()
    if not texto:
        e1 = (g.get("escenas") or [{}])[0]
        texto = (e1.get("texto") or e1.get("titular") or g.get("titulo", "")).strip()
        texto = " ".join(texto.replace(":", " ").split()[:4])
    return texto.upper(), (m.get("rojo") or "").strip().upper(), int(m.get("escena") or 1)


def hacer(fondo, texto, rojo, destino):
    img = _recortar(fondo)
    img = ImageEnhance.Brightness(img).enhance(0.55)
    img = ImageEnhance.Contrast(img).enhance(1.25)
    # Viñeta y degradado oscuro a la izquierda (donde va el texto)
    sombra = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(sombra)
    for x in range(W):
        ds.line([(x, 0), (x, H)], fill=int(max(0, 200 - x * 0.28)))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, sombra)
    vin = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vin).ellipse((-200, -150, W + 200, H + 150), fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(img, Image.new("RGB", (W, H), (0, 0, 0)), vin)

    d = ImageDraw.Draw(img)
    margen, ancho = 60, 820
    # Texto gigante: el mayor tamaño que quepa en 3 líneas
    for tam in range(150, 60, -6):
        f = _fuente(tam)
        lineas = _lineas(texto, f, ancho, d)
        alto = len(lineas) * tam * 1.05
        if len(lineas) <= 3 and alto <= (H - 260 if rojo else H - 160):
            break
    y = (H - alto - (140 if rojo else 0)) / 2
    for ln in lineas:
        d.text((margen, y), ln, font=f, fill=(255, 255, 255), stroke_width=max(4, tam // 18), stroke_fill=(0, 0, 0))
        y += tam * 1.05
    if rojo:
        fr = _fuente(68)
        tw = d.textlength(rojo, font=fr)
        y += 24
        d.rectangle((margen - 10, y, margen + tw + 30, y + 98), fill=ROJO)
        d.text((margen + 10, y + 10), rojo, font=fr, fill=(255, 255, 255))
    # Marca del canal, pequeña, abajo a la derecha
    fm = _fuente(26)
    marca = "THE SENTINEL"
    d.text((W - d.textlength(marca, font=fm) - 34, H - 58), marca, font=fm, fill=(232, 190, 90),
           stroke_width=2, stroke_fill=(0, 0, 0))
    img.save(destino, "JPEG", quality=90, optimize=True)
    return destino


def desde_guion(g, carpeta_clips, clips_por_escena, destino, remotion):
    """clips_por_escena: lista (una por escena) con las rutas de sus clips ya bajados."""
    texto, rojo, n = textos_de(g)
    orden = [n - 1] + [i for i in range(len(clips_por_escena)) if i != n - 1]
    fondo = None
    for i in orden:
        if 0 <= i < len(clips_por_escena) and clips_por_escena[i]:
            try:
                fondo = fotograma(clips_por_escena[i][0], destino + ".frame.png", remotion)
                break
            except Exception as e:  # noqa: BLE001
                print("   miniatura: no se pudo sacar fotograma:", e, flush=True)
    if fondo is None:
        fondo = Image.new("RGB", (W, H), (20, 20, 24))
    hacer(fondo, texto, rojo, destino)
    try:
        os.remove(destino + ".frame.png")
    except OSError:
        pass
    return destino


if __name__ == "__main__":
    import json
    g = json.load(open(sys.argv[1], encoding="utf-8"))
    clips = sorted(glob.glob(os.path.join(sys.argv[2], "*.mp4")))
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(desde_guion(g, sys.argv[2], [clips], sys.argv[3], os.path.join(raiz, "remotion")))
