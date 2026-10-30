# Escaleras v2: balcón techado con policarbonato, escalera de caracol de solera, arco con herrería.
import math, random, sys, os
import numpy as np
from PIL import Image, ImageDraw
import pathlib; ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'tools' / 'scenes')); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gala import hx
from estudio2 import C, mixc, BAYER

SEASON = None
FL = 168
IRON, IRON_L = hx('#1c1d1d'), hx('#3a3c3c')

def walls(c):
    r = random.Random(3)
    c.rect(0, 0, 359, FL, hx('#d8d4cc'))
    # estuco rugoso: grumos con luz arriba y sombra abajo
    for _ in range(2600):
        x, y = r.randint(0, 359), r.randint(10, FL)
        c.rect(x, y, x, y, hx('#ece9e2')); c.rect(x, y + 1, x, y + 1, hx('#b9b4aa'))
    c.noise(0, 10, 359, FL, [hx('#c9c4ba'), hx('#e4e0d8')], 0.18)
    # techo de policarbonato blanco
    c.rect(0, 0, 359, 9, hx('#eef3f6'))
    for x in range(0, 360, 60): c.line([(x, 0), (x, 9)], hx('#55595a'))
    c.line([(0, 9), (359, 9)], hx('#55595a'))
    c.noise(0, 0, 359, 8, [hx('#dfe8ee'), hx('#ffffff')], 0.25)
    # tubo de PVC blanco y mariposas doradas
    c.rect(292, 10, 294, FL, hx('#f4f4f2')); c.line([(294, 10), (294, FL)], hx('#c9c9c4'))
    for bx, by in ((304, 104), (312, 112)):
        c.poly([(bx, by), (bx - 4, by - 4), (bx - 4, by + 2)], hx('#c9a24a')); c.poly([(bx, by), (bx + 4, by - 4), (bx + 4, by + 2)], hx('#d9b45a'))
    # ventana esmerilada con marco oscuro
    c.rect(306, 36, 350, 74, hx('#2b2e2e')); c.rect(309, 39, 347, 71, hx('#cfd8d6'))
    c.noise(309, 39, 347, 71, [hx('#e2eae8'), hx('#b9c4c2')], 0.35)
    c.line([(309, 39), (347, 39)], hx('#f2f6f5'))
    # llave de agua
    c.rect(326, 118, 334, 121, hx('#9a8f7c')); c.rect(328, 121, 330, 127, hx('#5e7e6e')); c.rect(325, 115, 333, 116, hx('#7a2a1e'))
    c.line([(331, 127), (331, 166)], hx('#7a6a5a'))

def arch(c):
    # vista de la calle (genérica) por el arco
    view = Image.new('RGBA', c.im.size); v = ImageDraw.Draw(view); k = c.k
    for y in range(0, 160 * k): v.line([(0, y), (c.W, y)], fill=(130 + y // (3 * k), 186 + y // (6 * k), 236, 255))
    for cx, cy in ((60, 30), (130, 40), (100, 24)): v.ellipse([(cx - 14) * k, (cy - 5) * k, (cx + 14) * k, (cy + 5) * k], fill=(250, 252, 255, 255))
    v.rectangle([40 * k, 70 * k, 120 * k, 150 * k], fill=hx('#e9c33a')); v.rectangle([40 * k, 66 * k, 120 * k, 70 * k], fill=hx('#b5523a'))
    for wx in (48, 78, 100): v.rectangle([wx * k, 80 * k, (wx + 14) * k, 96 * k], fill=hx('#f4f1e6')); v.rectangle([(wx + 2) * k, 82 * k, (wx + 12) * k, 94 * k], fill=hx('#9fb6c9'))
    v.rectangle([0, 84 * k, 40 * k, 150 * k], fill=hx('#b56a4a')); v.rectangle([4 * k, 110 * k, 34 * k, 150 * k], fill=hx('#4f86c9'))
    v.rectangle([120 * k, 76 * k, 180 * k, 150 * k], fill=hx('#9a8f86'))
    v.ellipse([86 * k, 100 * k, 112 * k, 150 * k], fill=hx('#5e8f4a'))
    v.rectangle([0, 132 * k, c.W, 150 * k], fill=hx('#9a9a96'))
    mask = Image.new('L', c.im.size); m = ImageDraw.Draw(mask)
    m.rectangle([34 * k, 70 * k, 160 * k, 152 * k], fill=255); m.pieslice([34 * k, 20 * k, 160 * k, 120 * k], 180, 360, fill=255)
    c.im.paste(view, (0, 0), mask)
    # derrame del arco color malva
    lay = Image.new('RGBA', c.im.size); L = ImageDraw.Draw(lay)
    L.rectangle([24 * k, 70 * k, 170 * k, 152 * k], fill=hx('#7b5d66')); L.pieslice([24 * k, 10 * k, 170 * k, 130 * k], 180, 360, fill=hx('#7b5d66'))
    hole = Image.new('L', c.im.size); hm = ImageDraw.Draw(hole)
    hm.rectangle([24 * k, 70 * k, 170 * k, 152 * k], fill=255); hm.pieslice([24 * k, 10 * k, 170 * k, 130 * k], 180, 360, fill=255)
    hm.rectangle([34 * k, 70 * k, 160 * k, 152 * k], fill=0); hm.pieslice([34 * k, 20 * k, 160 * k, 120 * k], 180, 360, fill=0)
    c.im.paste(lay, (0, 0), hole)
    c.d = ImageDraw.Draw(c.im)
    # herrería: lanzas arriba, barrotes torcidos, banda de volutas y círculos
    g = Image.new('RGBA', c.im.size); G = C.__new__(C); G.k = k; G.W, G.H = c.W, c.H; G.im = g; G.d = ImageDraw.Draw(g); G.r = random.Random(5)
    for i, x in enumerate(range(42, 156, 12)):
        top = 34 + abs(x - 97) * 0.35
        G.line([(x, top + 6), (x, 150)], IRON, 2 if k == 1 else 3)
        for y in range(int(top + 8), 150, 6): G.line([(x - 1, y), (x + 1, y + 3)], IRON_L)
        G.poly([(x - 2, top + 6), (x, top - 2), (x + 2, top + 6)], IRON); G.poly([(x - 3, top + 7), (x + 3, top + 7), (x, top + 9)], IRON)
    for yb in (78, 112, 146):
        G.line([(36, yb), (158, yb)], IRON, 2)
        for x in range(40, 156, 8): G.d.arc([x * k, (yb - 6) * k, (x + 6) * k, yb * k], 180, 450, fill=IRON, width=1)
    for cx in (52, 80, 108, 136):
        G.ell(cx - 11, 84, cx + 11, 106, None, IRON, 2)
        for a in range(0, 360, 90):
            x = cx + 6 * math.cos(math.radians(a)); y = 95 + 6 * math.sin(math.radians(a)); G.d.arc([(x - 3) * k, (y - 3) * k, (x + 3) * k, (y + 3) * k], a, a + 270, fill=IRON)
    for cx in range(42, 158, 10): G.ell(cx - 4, 140, cx + 4, 148, None, IRON)
    for cx in range(48, 150, 18): G.d.arc([(cx - 7) * k, 56 * k, (cx + 7) * k, 70 * k], 180, 360, fill=IRON, width=1); G.ell(cx - 3, 64, cx + 3, 70, None, IRON)
    am = Image.new('L', c.im.size); ImageDraw.Draw(am).rectangle([34 * k, 70 * k, 160 * k, 152 * k], fill=255); ImageDraw.Draw(am).pieslice([34 * k, 20 * k, 160 * k, 120 * k], 180, 360, fill=255)
    c.im.paste(g, (0, 0), Image.composite(am, Image.new('L', c.im.size), g.split()[3]))
    c.d = ImageDraw.Draw(c.im)

def planter_and_floor(c):
    r = random.Random(8)
    # jardinera de tierra seca al pie del arco
    c.rect(24, 150, 176, 170, hx('#6e5236'))
    c.noise(24, 150, 176, 170, [hx('#5b4330'), hx('#7f6142'), hx('#8a7a4a')], 0.5)
    for _ in range(70):
        x, y = r.randint(26, 174), r.randint(152, 169); col = hx(r.choice(['#c2ab5c', '#b39a4a', '#d1bd73']))
        c.line([(x, y), (x - 1, y - 3)], col); c.line([(x + 1, y), (x + 2, y - 2)], col)
    for lx, ly in ((70, 158), (78, 154), (86, 160)):   # hierbita verde
        c.poly([(lx, ly + 8), (lx - 6, ly), (lx + 1, ly + 4), (lx + 6, ly - 2), (lx + 3, ly + 8)], hx('#5e9a3e'))
    c.rect(24, 168, 176, 171, hx('#b9b4aa'))
    # piedra rosada
    c.poly([(150, 172), (148, 140), (154, 126), (170, 124), (178, 136), (176, 172)], hx('#c98f72'), hx('#7a4e3a'))
    c.poly([(154, 128), (166, 126), (162, 150), (156, 160)], hx('#dcae92')); c.noise(150, 126, 176, 170, [hx('#b07a60'), hx('#e2bba4')], 0.25)
    # piso de lámina antiderrapante
    c.rect(0, FL, 359, 209, hx('#8d9090'))
    for y in range(FL + 2, 210, 4):
        for x in range(((y // 4) % 2) * 3, 360, 6): c.line([(x, y), (x + 2, y - 1)], hx('#b3b6b6'))
    c.line([(0, FL), (359, FL)], hx('#5e6262'))
    # sombras rayadas del barandal
    lay = Image.new('RGBA', c.im.size); L = ImageDraw.Draw(lay); k = c.k
    for x in range(40, 300, 12): L.polygon([(x * k, 210 * k), ((x + 5) * k, 210 * k), ((x + 25) * k, FL * k), ((x + 20) * k, FL * k)], fill=(30, 30, 30, 55))
    c.im.alpha_composite(lay); c.d = ImageDraw.Draw(c.im)
    # regadera verde
    c.poly([(312, 186), (338, 186), (336, 204), (314, 204)], hx('#2f9a3a'), hx('#1c5e24'))
    c.poly([(312, 190), (298, 182), (296, 184), (312, 194)], hx('#2f9a3a'), hx('#1c5e24')); c.ell(293, 180, 299, 186, hx('#2f9a3a'), hx('#1c5e24'))
    c.d.arc([316 * c.k, 176 * c.k, 336 * c.k, 194 * c.k], 180, 360, fill=hx('#1c5e24'), width=2 * c.k)
    c.line([(316, 190), (334, 190)], hx('#4fbf5a'))

def stairs(c):
    px, R, rise, step = 244, 64, 20, math.radians(34)
    treads = [(i * step + 0.6, 214 - i * rise) for i in range(14)]
    def pt(th, yb, r): return (px + r * math.cos(th), yb + r * math.sin(th) * 0.28)
    def wedge(th, yb, col, slat):
        a = pt(th - step * 0.5, yb, R); b = pt(th + step * 0.5, yb, R)
        c.poly([(px, yb), a, (a[0], a[1] + 3), (b[0], b[1] + 3), b], col, hx('#0e0f0f'))
        for f in (0.3, 0.45, 0.6, 0.75, 0.9):
            p = pt(th - step * 0.45, yb, R * f); q = pt(th + step * 0.45, yb, R * f); c.line([p, q], slat)
    back = [t for t in treads if math.sin(t[0]) < 0]; front = [t for t in treads if math.sin(t[0]) >= 0]
    for th, yb in back: wedge(th, yb, hx('#151616'), hx('#2b2d2d'))
    rail = [(pt(math.radians(t) + 0.6, 214 - (t / math.degrees(step)) * rise, R + 2), math.sin(math.radians(t) + 0.6)) for t in range(0, 14 * 34)]
    for i in range(len(rail) - 1):
        if rail[i][1] < 0: c.line([(rail[i][0][0], rail[i][0][1] - 26), (rail[i + 1][0][0], rail[i + 1][0][1] - 26)], hx('#151616'), 2)
    c.rect(px - 2, 0, px + 2, 209, IRON); c.line([(px - 1, 0), (px - 1, 209)], hx('#4a4d4d'))
    for th, yb in front: wedge(th, yb, IRON, IRON_L)
    for th, yb in front:
        o = pt(th, yb, R); c.line([o, (o[0], o[1] - 26)], IRON, 2)
    for i in range(len(rail) - 1):
        if rail[i][1] >= 0: c.line([(rail[i][0][0], rail[i][0][1] - 26), (rail[i + 1][0][0], rail[i + 1][0][1] - 26)], IRON, 3)
    # ganchos para las dos macetas colgantes (escalones del lado izquierdo)
    hooks = []
    for th, yb in treads:
        if math.cos(th) < 0.2 and 30 < yb < 130: o = pt(th, yb, R * 0.8); hooks.append((int(o[0]), int(o[1]) + 3))
    hooks = sorted(hooks, key=lambda h: h[1]); hooks = [hooks[0], hooks[-1]]
    for hxp, hyp in hooks: c.line([(hxp, hyp - 3), (hxp, hyp + 3)], hx('#e0582a'), 2)
    return hooks

def canary(c):
    c.line([(60, 9), (60, 14)], hx('#5f8f6a'))
    c.d.arc([42 * c.k, 12 * c.k, 78 * c.k, 30 * c.k], 180, 360, fill=hx('#7fb08a'), width=1)
    for x in range(44, 78, 3): c.line([(x, 20), (x, 44)], hx('#7fb08a'))
    c.rect(40, 44, 80, 48, hx('#ececec'), hx('#9a9a92')); c.rect(44, 36, 52, 43, hx('#2f6fd1'))
    c.line([(50, 32), (74, 28)], hx('#b08a5a'), 2)
    c.ell(60, 20, 70, 30, hx('#f2cf2a'), hx('#b8931a')); c.ell(66, 17, 73, 24, hx('#f2cf2a'), hx('#b8931a'))
    c.rect(70, 19, 70, 19, hx('#111111')); c.poly([(73, 20), (76, 21), (73, 22)], hx('#e88a2a'))

def lighting(img, k):
    a = np.asarray(img).astype(np.float32); H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    L = 0.86 + 0.20 * np.exp(-((yy / (120 * k)) ** 2) * 1.2) + 0.08 * np.exp(-(((xx - 97 * k) / (70 * k)) ** 2 + ((yy - 90 * k) / (60 * k)) ** 2))
    by = BAYER[yy.astype(int) % 4, xx.astype(int) % 4]
    Lq = np.floor(L * 12 + by) / 12
    rgb = a[..., :3] * Lq[..., None]
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a[..., 3].astype(np.uint8)]), 'RGBA')

def background(k=1):
    c = C(k); walls(c); arch(c); planter_and_floor(c)
    c.im = lighting(c.im, k); c.d = ImageDraw.Draw(c.im)
    canary(c); hooks = stairs(c)
    return c.im, hooks

def compose(moods=None):
    S = str(ROOT / 'public' / 'sprites') + '/'; moods = moods or {}
    bg, hooks = background(1)
    pos = {'P05': (123, 46)}
    (h1x, h1y), (h2x, h2y) = hooks
    pos['P01'] = (h1x - 40, h1y); pos['P02'] = (h2x - 40, h2y)
    for pid, (x, y) in pos.items():
        bg.alpha_composite(Image.open(f'{S}{pid}_{moods.get(pid, "feliz")}.png').convert('RGBA'), (x, y))
    return bg, pos

if __name__ == '__main__':
    out = os.environ.get('OUT', '.') + '/'
    im, pos = compose(); print(pos)
    im.resize((720, 420), Image.NEAREST).save(out + 'escaleras_A.png')
