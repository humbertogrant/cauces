# -*- coding: utf-8 -*-
"""Cuánto pesan las postales pintadas y cuánto pesaría la edición amplia de Cauces con todas, para no pasar de sus 5 MB.

Cuenta las postales que lleva cada río (el nacimiento, una por ciudad y el mar, según src/data/rios.js) y las que ya están en
src/data/postales.js, y mide la amplia como la mide test/dist.js. Después recodifica las vistas grandes de
tools/dibujos/salida/postales/ (lo que pinta el pintor antes de achicarlo) con cada resolución y calidad, como lo haría
tools/pintor.py, y proyecta el peso de la amplia con todas las postales al peso medio de las que hay. Para cambiar la de todas:
ANCHO_POSTAL y CALIDAD_POSTAL en tools/pintor.py y `python tools/pintados.py`, que repinta lo pintado.

Uso: python tools/peso_postales.py [ancho/calidad…]       (sin argumentos: 744/84, 744/75, 600/84 y 600/75)
"""
import glob
import io
import os
import re
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import pintados  # noqa: E402
import pintor  # noqa: E402

TOPE = 5120                      # KB: el tope de la edición amplia (Humberto, 2026-10-26); test/dist.js lo exige
OPCIONES = ((744, 84), (744, 75), (600, 84), (600, 75))


def recodificar(grande, ancho, calidad):
    """El WebP que guardaría el pintor con ese ancho y esa calidad, desde la vista grande de una postal."""
    im = Image.open(grande)
    b = io.BytesIO()
    im.resize((ancho, int(round(ancho * im.size[1] / im.size[0]))), Image.LANCZOS).convert('RGB').save(
        b, 'WEBP', quality=calidad, method=6)
    return b.getvalue()


def main(opciones):
    sys.stdout.reconfigure(encoding='utf-8')
    total = sum(len(v) for v in pintados.recorridos().values())
    hechas, en_datos = 0, 0
    for linea in io.open(os.path.join(RAIZ, 'src', 'data', 'postales.js'), encoding='utf8').read().splitlines():
        if re.match(r'[a-z]+:\[', linea):
            urls = re.findall(r"'data:image/webp;base64,[^']+'", linea)
            hechas += len(urls)
            en_datos += sum(len(u) for u in urls)
    html = io.open(os.path.join(RAIZ, 'dist', 'cauces-amplia.html'), encoding='utf8').read()
    amplia = len(html.encode('utf-16-le')) / 2 / 1024       # como test/dist.js: el largo del texto en JavaScript
    resto = amplia - en_datos / 1024
    medio = en_datos / 1024 / max(hechas, 1)
    print('postales: %d de %d (faltan %d); en los datos, %.0f KB: %.1f KB cada una' % (hechas, total, total - hechas,
                                                                                     en_datos / 1024, medio))
    print('amplia de Cauces: %.0f KB, %.0f sin las postales; el tope es %d KB: así como están, caben unas %d postales más'
          % (amplia, resto, TOPE, (TOPE - amplia) / medio))
    grandes = sorted(glob.glob(os.path.join(pintor.SALIDA, 'postales', '*-grande.png')))
    print('con las %d, recodificando las %d pintadas:' % (total, len(grandes)))
    for ancho, calidad in opciones:
        cada = sum(len(recodificar(g, ancho, calidad)) * 4 / 3 / 1024 for g in grandes) / len(grandes)   # en base64
        final = resto + total * cada
        ahora = ' (así están)' if (ancho, calidad) == (pintor.ANCHO_POSTAL, pintor.CALIDAD_POSTAL) else ''
        print('  %d px, calidad %d%s: %.1f KB cada una; la amplia, %.0f KB: %s' % (
            ancho, calidad, ahora, cada, final,
            'sobran %.0f KB' % (TOPE - final) if final <= TOPE else 'pasa del tope por %.0f KB' % (final - TOPE)))


if __name__ == '__main__':
    main([tuple(int(x) for x in a.split('/')) for a in sys.argv[1:]] or OPCIONES)
