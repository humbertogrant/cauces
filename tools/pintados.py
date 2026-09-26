# -*- coding: utf-8 -*-
"""Genera src/data/barcas.js, bienes.js y postales.js (solo edición amplia) con las barcas, las mercancías y las postales pintadas.

Las barcas son las embarcaciones de cada ruta (tools/dibujos/barcas/<ruta>.py), para el bloque «Tu embarcación» al empezar;
las mercancías, los bienes del mercado de una ruta (tools/dibujos/bienes/<ruta>.py, en el orden de MERCADOS[ruta]); las postales,
las de un río (tools/dibujos/postales/<ruta>.py: el nacimiento, una por ciudad y el mar, en ese orden). Las pinta tools/pintor.py;
esta herramienta vuelve a pintar las que quedaron viejas (si su dibujo, un ayudante o el pintor cambiaron después de la última
pintada) y escribe los tres archivos con las que tienen LISTO. tools/ilustraciones.py la llama al final.

Uso: python tools/pintados.py
"""
import base64
import glob
import io
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import pintor  # noqa: E402

ENCABEZADO_BARCAS = """// Barcas pintadas, solo en la edición amplia: la lámina del bloque «Tu embarcación» al empezar cada ruta. GENERADO por
// tools/pintados.py desde tools/dibujos/barcas/<ruta>.py (pintadas por tools/pintor.py): no editar a mano. De perfil, con la proa a
// la derecha; `i` es un WebP que cubre el encuadre `v`, y `f` el agua de vectores que va detrás. Las rutas sin barca (la caravana,
// los jinetes) siguen con su glifo.
/*@amplia*/
const BARCAS={
"""
ENCABEZADO_POSTALES = """// Postales pintadas, solo en la edición amplia: las de un río, en el orden del recorrido: el nacimiento, una por ciudad y el
// mar (null donde no hay). GENERADO por tools/pintados.py desde tools/dibujos/postales/<ruta>.py: no editar a mano. Cada una es un
// WebP de 3 × 1, como la postal de pictogramas, que pinta la imagen para recordar de la parada; el motor la pone en su lugar.
/*@amplia*/
const POSTALES={
"""
ENCABEZADO_BIENES = """// Mercancías pintadas, solo en la edición amplia: una por cada bien de MERCADOS[ruta], en su mismo orden (null donde no hay).
// GENERADO por tools/pintados.py desde tools/dibujos/bienes/<ruta>.py: no editar a mano. Cada una es un WebP cuadrado que el
// mercado y la bodega muestran en lugar del icono de línea.
/*@amplia*/
const BIENES={
"""


def _vieja(salidas, fuentes):
    if not all(os.path.exists(s) for s in salidas):
        return True
    return max(os.path.getmtime(f) for f in fuentes) > min(os.path.getmtime(s) for s in salidas)


def _fuentes(archivo):
    carpeta = os.path.dirname(archivo)
    return ([archivo, os.path.abspath(pintor.__file__)] + glob.glob(os.path.join(carpeta, '_*.py'))
            + glob.glob(os.path.join(pintor.DIBUJOS, '_*.py')))


def _webp(archivo):
    return 'data:image/webp;base64,' + base64.b64encode(io.open(archivo, 'rb').read()).decode('ascii')


def barcas():
    lineas = []
    for ruta in pintor.rutas(pintor.BARCAS):
        base = os.path.join(pintor.SALIDA, 'barcas', ruta)
        if _vieja([base + '.webp', base + '.json'], _fuentes(os.path.join(pintor.BARCAS, ruta + '.py'))):
            print('barca %-12s se pinta de nuevo' % ruta)
            pintor.pintar_barca(ruta, previa=False)
        datos = json.load(io.open(base + '.json', encoding='utf8'))
        img = _webp(base + '.webp')
        print('barca %-12s %-9s %5.1f KB' % (ruta, 'terminada' if datos['listo'] else 'BORRADOR', len(img) / 1024))
        if datos['listo']:
            lineas.append("%s:{v:'%s',%si:'%s'}," % (ruta, datos['v'], ("f:'%s'," % datos['f']) if datos['f'] else '', img))
    io.open(os.path.join(RAIZ, 'src', 'data', 'barcas.js'), 'w', encoding='utf8', newline='\n').write(
        ENCABEZADO_BARCAS + '\n'.join(lineas) + '\n};\n/*@fin:amplia*/\n')
    return len(lineas)


def mercados():
    """los nombres de los bienes de cada ruta, en su orden, leídos de src/data/mercados.js"""
    import re
    s = io.open(os.path.join(RAIZ, 'src', 'data', 'mercados.js'), encoding='utf8').read()
    return {m.group(1): re.findall(r'\{n:"([^"]*)"', m.group(2)) for m in re.finditer(r'^\s*([a-z]+):\[(.*?)\],?\s*(?:/\*.*)?$', s, re.M)}


def bienes():
    lineas = []
    nombres = mercados()
    for ruta in pintor.rutas(pintor.BIENES):
        archivo = os.path.join(pintor.BIENES, ruta + '.py')
        mod = pintor.cargar(archivo, 'bienes_' + ruta)
        # cada dibujo va en el lugar de su bien: la clave tiene que ser el nombre del bien en MERCADOS[ruta], en el mismo orden
        claves = [b['clave'] if b else None for b in mod.BIENES]
        esperado = nombres.get(ruta)
        if esperado is None or len(claves) != len(esperado) or any(c is not None and c != n for c, n in zip(claves, esperado)):
            raise SystemExit('los bienes de tools/dibujos/bienes/%s.py %s no calzan con MERCADOS.%s %s' % (ruta, claves, ruta, esperado))
        bases = [os.path.join(pintor.SALIDA, 'bienes', '%s-%d' % (ruta, i)) if b else None for i, b in enumerate(mod.BIENES)]
        if _vieja([b + s for b in bases if b for s in ('.webp', '.json')], _fuentes(archivo)):
            print('bienes %-11s se pintan de nuevo' % ruta)
            pintor.pintar_bienes(ruta, previa=False)
        imgs = []
        for base in bases:
            ok = base and json.load(io.open(base + '.json', encoding='utf8'))['listo']
            imgs.append("'%s'" % _webp(base + '.webp') if ok else 'null')
        print('bienes %-11s %d de %d' % (ruta, sum(i != 'null' for i in imgs), len(imgs)))
        if any(i != 'null' for i in imgs):
            lineas.append('%s:[%s],' % (ruta, ','.join(imgs)))
    io.open(os.path.join(RAIZ, 'src', 'data', 'bienes.js'), 'w', encoding='utf8', newline='\n').write(
        ENCABEZADO_BIENES + '\n'.join(lineas) + '\n};\n/*@fin:amplia*/\n')
    return len(lineas)


def recorridos():
    """de cada río, sus postales en orden: 'nace', el nombre de cada ciudad y 'mar', leídos de src/data/rios.js"""
    import re
    s = io.open(os.path.join(RAIZ, 'src', 'data', 'rios.js'), encoding='utf8').read()
    out = {}
    marcas = [m for m in re.finditer(r'\{id:"([a-z]+)"', s)]
    for i, m in enumerate(marcas):
        bloque = s[m.end():marcas[i + 1].start() if i + 1 < len(marcas) else len(s)]
        ciudades = bloque[bloque.index('ciudades:['):]
        out[m.group(1)] = ['nace'] + re.findall(r'\{nombre:"([^"]*)",pais:', ciudades) + ['mar']
    return out


def postales():
    lineas = []
    esperados = recorridos()
    for ruta in pintor.rutas(pintor.POSTALES):
        archivo = os.path.join(pintor.POSTALES, ruta + '.py')
        mod = pintor.cargar(archivo, 'postales_' + ruta)
        # cada postal va en su lugar del recorrido: la clave es 'nace', el nombre de la ciudad o 'mar', en el mismo orden
        claves = [p['clave'] if p else None for p in mod.POSTALES]
        esperado = esperados.get(ruta)
        if esperado is None or len(claves) != len(esperado) or any(c is not None and c != n for c, n in zip(claves, esperado)):
            raise SystemExit('las postales de tools/dibujos/postales/%s.py %s no calzan con el recorrido %s' % (ruta, claves, esperado))
        bases = [os.path.join(pintor.SALIDA, 'postales', '%s-%d' % (ruta, i)) if p else None for i, p in enumerate(mod.POSTALES)]
        if _vieja([b + s_ for b in bases if b for s_ in ('.webp', '.json')], _fuentes(archivo)):
            print('postales %-9s se pintan de nuevo' % ruta)
            pintor.pintar_postales(ruta, previa=False)
        imgs = []
        for base in bases:
            ok = base and json.load(io.open(base + '.json', encoding='utf8'))['listo']
            imgs.append("'%s'" % _webp(base + '.webp') if ok else 'null')
        peso = sum(len(i) for i in imgs if i != 'null')
        print('postales %-9s %d de %d  %5.1f KB' % (ruta, sum(i != 'null' for i in imgs), len(imgs), peso / 1024))
        if any(i != 'null' for i in imgs):
            lineas.append('%s:[%s],' % (ruta, ','.join(imgs)))
    io.open(os.path.join(RAIZ, 'src', 'data', 'postales.js'), 'w', encoding='utf8', newline='\n').write(
        ENCABEZADO_POSTALES + '\n'.join(lineas) + '\n};\n/*@fin:amplia*/\n')
    return len(lineas)


def main():
    nb, nm, npo = barcas(), bienes(), postales()
    print('juego: %d barcas en src/data/barcas.js · mercancías de %d rutas en src/data/bienes.js · postales de %d ríos en '
          'src/data/postales.js' % (nb, nm, npo))


if __name__ == '__main__':
    main()
