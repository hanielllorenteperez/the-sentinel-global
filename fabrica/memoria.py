# -*- coding: utf-8 -*-
r"""
La "libreta" del bot: recuerda qué noticias ya se montaron y cuáles ya están en YouTube,
para que si algo falla la próxima vez siga desde donde se quedó (no empieza de 0).

Cada noticia guarda su memoria en noticias/<id>/estado.json, por ejemplo:
  {"montado_run": "44893046169", "largo": "https://youtu.be/...", "short": "https://youtube.com/shorts/..."}
  {"omitir": true}   ← no hacer nada más con esta noticia

  python fabrica/memoria.py pendientes [max]      → ids de noticias que aún no están del todo en YouTube
  python fabrica/memoria.py ver <id> <campo>      → imprime el valor (o nada)
  python fabrica/memoria.py marcar <id> <campo> <valor>
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTICIAS = os.path.join(RAIZ, "noticias")


def ruta(nid):
    return os.path.join(NOTICIAS, nid, "estado.json")


def leer(nid):
    try:
        return json.load(open(ruta(nid), encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def guardar(nid, datos):
    json.dump(datos, open(ruta(nid), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def marcar(nid, campo, valor):
    d = leer(nid)
    d[campo] = valor
    guardar(nid, d)


def falta(nid):
    """Qué partes de la noticia faltan por subir: lista con 'largo' y/o 'short'."""
    d = leer(nid)
    if d.get("omitir"):
        return []
    partes = []
    if os.path.exists(os.path.join(NOTICIAS, nid, "guion.json")) and not d.get("largo"):
        partes.append("largo")
    if os.path.exists(os.path.join(NOTICIAS, nid, "guion-short.json")) and not d.get("short"):
        partes.append("short")
    return partes


def pendientes(maximo=3):
    ids = sorted(n for n in os.listdir(NOTICIAS) if os.path.isdir(os.path.join(NOTICIAS, n)))
    return [n for n in ids if falta(n)][:maximo]


if __name__ == "__main__":
    orden = sys.argv[1]
    if orden == "pendientes":
        print(" ".join(pendientes(int(sys.argv[2]) if len(sys.argv) > 2 else 3)))
    elif orden == "ver":
        v = leer(sys.argv[2]).get(sys.argv[3])
        print("" if v is None else v)
    elif orden == "marcar":
        marcar(sys.argv[2], sys.argv[3], sys.argv[4])
    elif orden == "falta":
        print(" ".join(falta(sys.argv[2])))
