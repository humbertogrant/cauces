# -*- coding: utf-8 -*-
"""Genera src/data/ilustraciones.js (solo edición amplia): una ilustración por animal a partir de un contorno real.

El contorno no se dibuja a mano: sale de una silueta de PhyloPic (phylopic.org) de dominio público o CC0, guardada en
tools/ilustraciones/ con su autor y licencia en fuentes.json. Esta herramienta la pasa a la caja 0 0 120 90 mirando a la
derecha, y calcula sobre el contorno lo que da volumen: la banda de sombra (lo que el contorno deja al correrse hacia la luz),
el filo de brillo del lomo y las zonas de color (patas lejanas, pico, cola), que son polígonos toscos recortados por el contorno.
A mano solo va lo que el contorno no trae: dónde está el ojo y la boca (los dibuja caraDe en motor.js según el ánimo), unas
pocas líneas y el indicio del lugar donde vive. Perfil estricto: un solo ojo.

Uso: python tools/ilustraciones.py            escribe src/data/ilustraciones.js
     python tools/ilustraciones.py --crudo    lo mismo pero sin cara ni detalles (para ubicar coordenadas sobre la cuadrícula)
"""
import io, json, os, re, sys
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.affinity import translate, scale, rotate
from shapely.ops import unary_union

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DIR = os.path.join(AQUI, 'ilustraciones')
SALIDA = os.path.join(RAIZ, 'src', 'data', 'ilustraciones.js')
CAJA = (120, 90)
LUZ = (2.2, -5.5)      # hacia dónde está la luz (arriba y adelante): la sombra queda abajo y atrás
NUM = r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?'
ARIDAD = {'M': 2, 'L': 2, 'C': 6, 'Z': 0, 'H': 1, 'V': 1, 'S': 4, 'Q': 4, 'T': 2}


def anillos(svg):
    """Subtrazos de todos los <path> como listas de puntos, con la transformación del grupo (translate y scale) aplicada."""
    tx = ty = 0.0
    sx = sy = 1.0
    t = re.search(r'<g[^>]*transform="([^"]+)"', svg)
    if t:
        m = re.search(r'translate\(\s*(%s)[ ,]+(%s)\s*\)' % (NUM, NUM), t.group(1))
        if m:
            tx, ty = float(m.group(1)), float(m.group(2))
        m = re.search(r'scale\(\s*(%s)(?:[ ,]+(%s))?\s*\)' % (NUM, NUM), t.group(1))
        if m:
            sx = float(m.group(1))
            sy = float(m.group(2) or m.group(1))
    salida = []
    for d in re.findall(r'<path[^>]*?\sd="([^"]+)"', svg, flags=re.S):
        fichas = re.findall(r'[MmLlCcZzHhVvSsQqTt]|' + NUM, d)
        i, x, y, x0, y0, ctrl, cmd, anillo = 0, 0.0, 0.0, 0.0, 0.0, None, None, []

        def cerrar():
            nonlocal anillo
            if len(anillo) >= 3:
                salida.append([(tx + sx * px, ty + sy * py) for px, py in anillo])
            anillo = []
        while i < len(fichas):
            if re.match(r'[A-Za-z]', fichas[i]):
                cmd = fichas[i]
                i += 1
            c, rel = cmd.upper(), cmd.islower()
            n = ARIDAD[c]
            a = [float(v) for v in fichas[i:i + n]]
            i += n
            ox, oy = (x, y) if rel else (0.0, 0.0)
            if c == 'Z':
                x, y = x0, y0
                cerrar()
                ctrl = None
                continue
            if c == 'M':
                cerrar()
                x, y = ox + a[0], oy + a[1]
                x0, y0 = x, y
                anillo = [(x, y)]
                cmd = 'l' if rel else 'L'
                ctrl = None
            elif c == 'L':
                x, y = ox + a[0], oy + a[1]
                anillo.append((x, y))
                ctrl = None
            elif c == 'H':
                x = (x if rel else 0.0) + a[0]
                anillo.append((x, y))
                ctrl = None
            elif c == 'V':
                y = (y if rel else 0.0) + a[0]
                anillo.append((x, y))
                ctrl = None
            elif c in 'CS':
                if c == 'C':
                    p1 = (ox + a[0], oy + a[1])
                    p2 = (ox + a[2], oy + a[3])
                    p3 = (ox + a[4], oy + a[5])
                else:
                    p1 = (2 * x - ctrl[0], 2 * y - ctrl[1]) if ctrl else (x, y)
                    p2 = (ox + a[0], oy + a[1])
                    p3 = (ox + a[2], oy + a[3])
                for k in range(1, 13):
                    u = k / 12.0
                    v = 1 - u
                    anillo.append((v ** 3 * x + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u ** 3 * p3[0],
                                   v ** 3 * y + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u ** 3 * p3[1]))
                ctrl = p2
                x, y = p3
            elif c in 'QT':
                if c == 'Q':
                    p1 = (ox + a[0], oy + a[1])
                    p2 = (ox + a[2], oy + a[3])
                else:
                    p1 = (2 * x - ctrl[0], 2 * y - ctrl[1]) if ctrl else (x, y)
                    p2 = (ox + a[0], oy + a[1])
                for k in range(1, 9):
                    u = k / 8.0
                    v = 1 - u
                    anillo.append((v * v * x + 2 * v * u * p1[0] + u * u * p2[0], v * v * y + 2 * v * u * p1[1] + u * u * p2[1]))
                ctrl = p1
                x, y = p2
        cerrar()
    return salida


def forma(svg):
    """Los subtrazos combinados con la regla par-impar (así los huecos quedan huecos)."""
    g = Polygon()
    for a in anillos(svg):
        g = g.symmetric_difference(Polygon(a).buffer(0))
    return g


def encajar(g, espejo, zona, apoyo):
    """Lleva la forma a `zona` (x0, y0, x1, y1) de la caja: apoyada en el borde de abajo ('suelo') o centrada ('centro')."""
    x0, y0, x1, y1 = g.bounds
    if espejo:
        g = scale(g, -1, 1, origin=((x0 + x1) / 2, 0))
    zx0, zy0, zx1, zy1 = zona
    s = min((zx1 - zx0) / (x1 - x0), (zy1 - zy0) / (y1 - y0))
    g = scale(g, s, s, origin=(0, 0))
    x0, y0, x1, y1 = g.bounds
    dx = (zx0 + zx1) / 2 - (x0 + x1) / 2
    dy = zy1 - y1 if apoyo == 'suelo' else (zy0 + zy1) / 2 - (y0 + y1) / 2
    return translate(g, dx, dy)


def partes(g, minimo=0.0):
    ps = [g] if isinstance(g, Polygon) else [p for p in getattr(g, 'geoms', []) if isinstance(p, Polygon)]
    return [p for p in ps if not p.is_empty and p.area > minimo]


def n(v):
    s = '%.1f' % v
    if s.endswith('.0'):
        s = s[:-2]
    return '0' if s == '-0' else s


def trazo(g, minimo=0.0, tol=0.08):
    d = ''
    for p in partes(g.simplify(tol, preserve_topology=True), minimo):
        for a in [p.exterior] + list(p.interiors):
            pts = list(a.coords)[:-1]
            d += 'M' + ' '.join(n(x) + ' ' + n(y) for x, y in pts) + 'Z'
    return d


def hilo(g, minimo=1.0, tol=0.08):
    """Líneas sueltas (el borde interior de una zona) como trazo abierto."""
    d = ''
    ls = [g] if g.geom_type == 'LineString' else [p for p in getattr(g, 'geoms', []) if p.geom_type == 'LineString']
    from shapely.ops import linemerge
    unidas = linemerge(ls) if len(ls) > 1 else (ls[0] if ls else None)
    if unidas is None:
        return d
    for l in ([unidas] if unidas.geom_type == 'LineString' else list(unidas.geoms)):
        if l.length >= minimo:
            d += 'M' + ' '.join(n(x) + ' ' + n(y) for x, y in l.simplify(tol).coords)
    return d


def poligono(pts):
    return Polygon(pts).buffer(0)


def ilustrar(clave, e, crudo=False):
    g = forma(io.open(os.path.join(DIR, e['fuente']), encoding='utf8').read())
    g = encajar(g, e.get('espejo', False), e.get('zona', (8, 14, 112, 82)), e.get('apoyo', 'suelo'))
    if e.get('giro'):
        g = rotate(g, e['giro'], origin='centroid')
        g = encajar(g, False, e.get('zona', (8, 14, 112, 82)), e.get('apoyo', 'suelo'))
    x0, y0, x1, y1 = g.bounds
    # sombra: lo que el contorno no tapa al correrse hacia la luz; se alisa para que no queden hilos
    sombra = g.difference(translate(g, LUZ[0], LUZ[1])).buffer(-0.3).buffer(0.3)
    # brillo: un filo por dentro del contorno, del lado de la luz, solo en la mitad de arriba
    dentro = g.buffer(-1.1)
    brillo = dentro.difference(translate(dentro, -LUZ[0] * 0.8, -LUZ[1] * 0.55)).buffer(-0.25).buffer(0.25)
    brillo = brillo.intersection(box(x0, y0, x1, y0 + (y1 - y0) * e.get('brillo', 0.5)))
    d = ''
    zonas = {} if crudo else e.get('zonas', {})
    d += '<path class="cuerpo" d="%s"/>' % trazo(g)
    bordes = ''
    for clase, pols in zonas.items():
        z = unary_union([poligono(p).buffer(-1.5).buffer(1.5) for p in pols]).intersection(g)     # esquinas redondeadas
        d += '<path class="%s" d="%s" style="stroke:none"/>' % (clase, trazo(z, 0.3))
        # la línea donde la zona se separa del resto del cuerpo (por dentro del contorno)
        bordes += hilo(z.boundary.intersection(g.buffer(-0.62)))
        if clase == 'acento':      # sobre el dorado, la sombra es oro tinta y no verde
            d += '<path d="%s" style="fill:var(--oro-tinta);opacity:.4"/>' % trazo(sombra.intersection(z), 0.5)
        if clase in ('acento', 'oscuro'):
            sombra = sombra.difference(z)
    d += '<path class="sombra" d="%s" style="opacity:.8"/>' % trazo(sombra, 0.8)
    d += '<path class="claro" d="%s" style="opacity:.3;stroke:none"/>' % trazo(brillo, 0.8)
    if bordes:
        d += '<path class="bigote" d="%s" style="stroke-width:.7;opacity:.7"/>' % bordes
    # el contorno otra vez, solo trazo, para que las zonas y la sombra no lo pisen
    d += '<path class="cuerpo" d="%s" style="fill:none"/>' % trazo(g)
    if not crudo:
        d += e.get('lineas', '')
    c = None if crudo else e.get('cara')
    return g, d, c, ('' if crudo else e.get('fondo', ''))


def js(v):
    return json.dumps(v, separators=(',', ':')).replace('"', '')


ENCABEZADO = """// Ilustraciones de los animales, solo en la edición amplia: la ficha «Conocé a …» y el globo (primer plano de la cabeza).
// GENERADO por tools/ilustraciones.py: no editar a mano. El contorno de cada animal es una silueta real de PhyloPic (dominio
// público o CC0; autor y licencia en tools/ilustraciones/fuentes.json), de perfil estricto y mirando a la derecha, en la caja
// 0 0 120 90. La sombra, el brillo y las zonas de color se calculan sobre el contorno. Sin ojo ni boca: los dibuja caraDe
// (motor.js) en `c` (ojo, boca, k, kb, giro, marco e inclinación del primer plano) según el ánimo. `f` es el fondo: el lugar donde vive.
/*@amplia*/
const ILUSTRACIONES={
"""


def main():
    crudo = '--crudo' in sys.argv
    from ilustraciones_datos import ANIMALES
    lineas = []
    for clave, e in ANIMALES.items():
        g, d, c, f = ilustrar(clave, e, crudo)
        lineas.append("%s:{v:'0 0 %d %d',%s%sd:'%s'}," % (clave, CAJA[0], CAJA[1], ('c:' + js(c) + ',') if c else '', ("f:'%s'," % f) if f else '', d))
        print('%-14s %5.1f KB  caja %s' % (clave, len(d) / 1024.0, ' '.join(n(v) for v in g.bounds)))
    io.open(SALIDA, 'w', encoding='utf8', newline='\n').write(ENCABEZADO + '\n'.join(lineas) + '\n};\n/*@fin:amplia*/\n')
    print('escrito', os.path.relpath(SALIDA, RAIZ))


if __name__ == '__main__':
    sys.path.insert(0, DIR)
    main()
