# -*- coding: utf-8 -*-
"""Genera src/data/ilustraciones.js (solo edición amplia): una ilustración por animal a partir de un contorno real.

El contorno no se dibuja a mano: sale de una silueta de PhyloPic (phylopic.org) de dominio público o CC0, guardada en
tools/ilustraciones/ con su autor y licencia en fuentes.json. Esta herramienta la pasa a la caja 0 0 120 90 mirando a la
derecha, y calcula sobre el contorno lo que da volumen: la banda de sombra (lo que el contorno deja al correrse hacia la luz),
el filo de brillo del lomo y las zonas de color (patas lejanas, pico, cola), que son polígonos toscos recortados por el contorno.
A mano solo va lo que el contorno no trae: dónde está el ojo y la boca (los dibuja caraDe en motor.js según el ánimo), unas
pocas líneas y el indicio del lugar donde vive. Perfil estricto: un solo ojo.

Uso: python tools/ilustraciones.py
Escribe dos archivos. src/data/ilustraciones.js, el del juego, recibe SOLO los animales terminados (los que ya tienen `cara` en
ilustraciones_datos.py). tools/ilustraciones/revision.js (fuera de git) los recibe todos, y los que están en borrador salen en
crudo, solo contorno con sombra y brillo, para leer coordenadas sobre la cuadrícula de las hojas. Así un borrador nunca llega al
juego: el 2026-09-18 un modo «--crudo» que escribía sobre el archivo del juego dejó a Hipo y a Pico sin cara en la copia de trabajo.
"""
import io, json, math, os, re, sys
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.affinity import translate, scale, rotate
from shapely.ops import unary_union

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DIR = os.path.join(AQUI, 'ilustraciones')
SALIDA = os.path.join(RAIZ, 'src', 'data', 'ilustraciones.js')
REVISION = os.path.join(DIR, 'revision.js')
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


def limpiar(g, liso=0.15, hueco=1.5, mota=1.0):
    """Alisa el contorno (cierre y apertura morfológicos de radio `liso`) y quita los huecos y las motas chicas que deja el trazado
    automático de una lámina con textura (la piel del elefante trae medio centenar)."""
    if liso:
        g = g.buffer(liso).buffer(-2 * liso).buffer(liso)
    ps = []
    for p in partes(g, mota):
        ps.append(Polygon(p.exterior, [h for h in p.interiors if Polygon(h).area >= hueco]))
    return unary_union(ps)


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


def redondear(p):
    """Esquinas redondeadas, con un radio a la medida de la pieza (1,5 como mucho; una pieza chica, como un diente, casi nada)."""
    x0, y0, x1, y1 = p.bounds
    r = min(1.5, 0.22 * min(x1 - x0, y1 - y0))
    return p.buffer(-r).buffer(r)


def trama(pol, g, paso, angulos):
    """Rayado dentro de un polígono tosco que el contorno recorta: la cola escamosa del castor."""
    from shapely.geometry import LineString
    zona = poligono(pol).intersection(g.buffer(-0.8))
    if zona.is_empty:
        return ''
    x0, y0, x1, y1 = zona.bounds
    cx, cy, r, d = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0), ''
    for ang in angulos:
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        k = -r
        while k <= r:
            d += hilo(LineString([(cx - uy * k - ux * r, cy + ux * k - uy * r), (cx - uy * k + ux * r, cy + ux * k + uy * r)]).intersection(zona), 0.8)
            k += paso
    return d


def ilustrar(clave, e):
    crudo = 'cara' not in e      # en borrador: solo el contorno
    g = forma(io.open(os.path.join(DIR, e['fuente']), encoding='utf8').read())
    g = encajar(g, e.get('espejo', False), e.get('zona', (8, 14, 112, 82)), e.get('apoyo', 'suelo'))
    g = limpiar(g, e.get('liso', 0))
    if e.get('giro'):
        g = rotate(g, e['giro'], origin='centroid')
        g = encajar(g, False, e.get('zona', (8, 14, 112, 82)), e.get('apoyo', 'suelo'))
    x0, y0, x1, y1 = g.bounds
    # sombra: lo que el contorno no tapa al correrse hacia la luz; se alisa para que no queden hilos
    luz = e.get('luz', 1.0)      # cuánto se corre el contorno: 1 para un cuerpo alto; menos para uno chato (el cocodrilo)
    sombra = g.difference(translate(g, LUZ[0] * luz, LUZ[1] * luz)).buffer(-0.3).buffer(0.3)
    # brillo: un filo por dentro del contorno, del lado de la luz, solo en la mitad de arriba
    dentro = g.buffer(-1.1)
    brillo = dentro.difference(translate(dentro, -LUZ[0] * 0.8 * luz, -LUZ[1] * 0.55 * luz)).buffer(-0.25).buffer(0.25)
    brillo = brillo.intersection(box(x0, y0, x1, y0 + (y1 - y0) * e.get('brillo', 0.5)))
    d = ''
    zonas = {} if crudo else e.get('zonas', {})
    borde = (';stroke-width:%s' % n(e['borde'])) if e.get('borde') else ''      # contorno más fino para un animal muy delgado (el gavial)
    d += '<path class="cuerpo" d="%s"%s/>' % (trazo(g), (' style="%s"' % borde[1:]) if borde else '')
    bordes = encima = ''
    for clase, pols in zonas.items():
        arriba = clase.endswith('^')                # «…^»: encima de la sombra y del brillo, como lo oscuro (la cara del bonobo)
        clase = clase.rstrip('^')
        sin_linea = clase.endswith('~')             # «lejos@.6~»: sin la línea de borde (la cara sin pelo del bonobo)
        clase, _, opaco = clase.rstrip('~').partition('@')      # «lejos@.55»: la misma tinta, más suave (la oreja sobre el hombro)
        z = unary_union([redondear(poligono(p)) for p in pols]).intersection(g)
        if z.is_empty:
            print('  aviso: la zona %s de %s no toca el contorno' % (clase, clave))
            continue
        pieza = '<path class="%s" d="%s" style="stroke:none%s"/>' % (clase, trazo(z, 0.3), (';opacity:' + opaco) if opaco else '')
        if clase == 'oscuro' or arriba:      # lo oscuro (la protuberancia del cisne) va encima de la sombra y del brillo, que lo agrisaban
            encima += pieza
            brillo = brillo.difference(z)
        else:
            d += pieza
        # la línea donde la zona se separa del resto del cuerpo (por dentro del contorno)
        if not sin_linea:
            bordes += hilo(z.boundary.intersection(g.buffer(-0.62)))
        if clase == 'acento':      # sobre el dorado, la sombra es oro tinta y no verde
            d += '<path d="%s" style="fill:var(--oro-tinta);opacity:.4"/>' % trazo(sombra.intersection(z), 0.5)
        if clase in ('acento', 'oscuro'):
            sombra = sombra.difference(z)
    d += '<path class="sombra" d="%s" style="opacity:.8"/>' % trazo(sombra, 0.8)
    d += '<path class="claro" d="%s" style="opacity:.3;stroke:none"/>' % trazo(brillo, 0.8)
    rayas = ''.join(trama(t['pol'], g, t.get('paso', 2.4), t.get('angulos', (30, -30))) for t in ([] if crudo else e.get('tramas', [])))
    if rayas:
        d += '<path class="bigote" d="%s" style="stroke-width:.5;opacity:.45"/>' % rayas
    d += encima
    if bordes:
        d += '<path class="bigote" d="%s" style="stroke-width:.7;opacity:.7"/>' % bordes
    # el contorno otra vez, solo trazo, para que las zonas y la sombra no lo pisen
    d += '<path class="cuerpo" d="%s" style="fill:none%s"/>' % (trazo(g), borde)
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
    from ilustraciones_datos import ANIMALES
    juego, revision = [], []
    for clave, e in ANIMALES.items():
        g, d, c, f = ilustrar(clave, e)
        vista = ' '.join(n(v) for v in e.get('vista', (0, 0) + CAJA))      # el encuadre de la lámina: la caja entera o la franja que ocupa
        linea = "%s:{v:'%s',%s%sd:'%s'}," % (clave, vista, ('c:' + js(c) + ',') if c else '', ("f:'%s'," % f) if f else '', d)
        revision.append(linea)
        if c:
            juego.append(linea)
        print('%-14s %-9s %5.1f KB  caja %s' % (clave, 'terminado' if c else 'BORRADOR', (len(d) + len(f)) / 1024.0, ' '.join(n(v) for v in g.bounds)))
    io.open(SALIDA, 'w', encoding='utf8', newline='\n').write(ENCABEZADO + '\n'.join(juego) + '\n};\n/*@fin:amplia*/\n')
    io.open(REVISION, 'w', encoding='utf8', newline='\n').write(
        '// Revisión: todos los animales, los borradores en crudo. No es del juego ni va a git.\nconst ILUSTRACIONES={\n'
        + '\n'.join(revision) + '\n};\n')
    print('juego: %d terminados en %s · revisión: %d en %s' % (len(juego), os.path.relpath(SALIDA, RAIZ), len(revision), os.path.relpath(REVISION, RAIZ)))


if __name__ == '__main__':
    sys.path.insert(0, DIR)
    main()
