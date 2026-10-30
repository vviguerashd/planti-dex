# Sala v2: escalera de loseta, puerta con cortina, comedor, sillón con la tele (Gala con Dios), ventana.
import math, random, sys, os, os
import numpy as np
from PIL import Image, ImageDraw
import pathlib; ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'tools' / 'scenes')); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gala import hx
from estudio2 import C, mixc, BAYER

SEASON = None
FL = 150
W0, H0 = 540, 220
TV_IMG = os.environ.get('TV_IMG', '')

class CS(C):
    def __init__(self, k, seed=7):
        super().__init__(k, seed); self.W, self.H = W0 * k, H0 * k
        self.im = Image.new('RGBA', (self.W, self.H)); self.d = ImageDraw.Draw(self.im)

def walls(c):
    c.rect(0, 0, W0 - 1, FL, hx('#efe9dc')); c.noise(0, 8, W0 - 1, FL, [hx('#e3dccc'), hx('#f7f3ea')], 0.22)
    c.rect(0, 0, W0 - 1, 7, hx('#f5f2ea')); c.noise(0, 0, W0 - 1, 7, [hx('#e3dfd4'), hx('#fbfaf6')], 0.35)
    c.line([(0, 8), (W0 - 1, 8)], hx('#d6cfbe'))
    c.rect(0, FL - 4, W0 - 1, FL - 1, hx('#a5482a')); c.line([(0, FL - 4), (W0 - 1, FL - 4)], hx('#c56a48'))   # zoclo de loseta

def floor(c):
    r = random.Random(5)
    c.rect(0, FL, W0 - 1, H0 - 1, hx('#a2462a'))
    rows = [FL]; y, h = FL, 10
    while y < H0: y += h; h += 5; rows.append(y)
    vx = W0 / 2
    for j in range(len(rows) - 1):
        ya, yb = rows[j], min(rows[j + 1], H0 - 1)
        for i in range(-12, 12):
            ta, tb = (ya - FL) / (H0 - FL), (yb - FL) / (H0 - FL)
            xa0 = vx + i * 30 * (1 + 0.9 * ta); xa1 = vx + (i + 1) * 30 * (1 + 0.9 * ta)
            xb0 = vx + i * 30 * (1 + 0.9 * tb); xb1 = vx + (i + 1) * 30 * (1 + 0.9 * tb)
            tone = [hx('#a2462a'), hx('#9a4025'), hx('#ab4f30')][(i + j) % 3]
            c.poly([(xa0, ya), (xa1, ya), (xb1, yb), (xb0, yb)], tone)
    c.noise(0, FL, W0 - 1, H0 - 1, [hx('#8f3b20'), hx('#b75c3a'), hx('#c06a48')], 0.3)
    for y in rows[1:]: c.line([(0, y), (W0 - 1, y)], hx('#6e2c16'))
    for i in range(-12, 13): c.line([(vx + i * 30, FL), (vx + i * 30 * 1.9, H0)], hx('#6e2c16'))
    for y in rows[1:]:
        t = (y - FL) / (H0 - FL); s = 2.5 + t * 4
        for i in range(-12, 13):
            x = vx + i * 30 * (1 + 0.9 * t)
            if 0 <= x < W0:
                c.poly([(x, y - s), (x + s * .35, y), (x, y + s), (x - s * .35, y)], hx('#f2efe8'))
                c.poly([(x - s, y), (x, y - s * .35), (x + s, y), (x, y + s * .35)], hx('#f2efe8'))
                c.rect(x, y, x, y, hx('#3a4f8a'))
    # reflejo de la ventana y del candil en el piso brillante
    lay = Image.new('RGBA', c.im.size); L = ImageDraw.Draw(lay); k = c.k
    L.polygon([(480 * k, FL * k), (536 * k, FL * k), (520 * k, H0 * k), (440 * k, H0 * k)], fill=(255, 245, 230, 28))
    L.ellipse([380 * k, 160 * k, 470 * k, 178 * k], fill=(255, 235, 190, 30))
    c.im.alpha_composite(lay); c.d = ImageDraw.Draw(c.im)

def stairs(c):
    # escalones de loseta que suben hacia la izquierda y se esconden tras el muro curvo
    steps = 9; hgt = 13
    for k_ in range(steps):
        yb = FL - k_ * hgt; x1 = 212 - k_ * 4; x0 = 110 - k_ * 3
        c.rect(x0, yb - hgt, x1, yb, hx('#a9472a'))                                # contrahuella
        c.noise(x0, yb - hgt, x1, yb - 1, [hx('#9a4025'), hx('#b75c3a')], 0.25)
        c.line([(x0, yb - 1), (x1, yb - 1)], hx('#7c3218'))
        c.line([(x0, yb - hgt), (x1, yb - hgt)], hx('#e08a62'))                     # nariz del escalón
        c.line([(x0, yb - hgt + 1), (x1, yb - hgt + 1)], hx('#c76a44'))
        c.rect(x1, yb - hgt - 3, x1 + 3, yb, hx('#f6f3ec')); c.line([(x1 + 3, yb - hgt - 3), (x1 + 3, yb)], hx('#d0c8b6'))   # zoclo blanco escalonado
    # muro blanco curvo a la izquierda (tapa el arranque de los escalones)
    c.poly([(0, 8), (96, 8), (110, 40), (124, 96), (132, FL), (0, FL)], hx('#f3efe6'))
    c.noise(0, 8, 92, FL - 5, [hx('#e6dfd0'), hx('#f8f5ee')], 0.2)
    c.line([(96, 8), (110, 40), (124, 96), (132, FL)], hx('#d0c8b6'), 2)
    c.line([(98, 8), (112, 40), (126, 96), (134, FL)], hx('#fbf9f4'))
    for row in range(7):   # block de vidrio escalonado (como en la foto)
        for j in range(min(row, 3), 5):
            bx, by = 186 + j * 7, 10 + row * 7
            c.rect(bx, by, bx + 6, by + 6, hx('#8fa9ad'), hx('#5d7a7e')); c.line([(bx + 1, by + 5), (bx + 5, by + 1)], hx('#d6e6e8'))
    if SEASON == 'halloween':   # guirnaldas de cempasúchil y calabacitas en el block
        for gx, glen in ((20, 92), (30, 110), (42, 80), (54, 118), (66, 96)):
            for gy in range(14, 14 + glen, 5): c.ell(gx - 3, gy, gx + 3, gy + 6, hx('#f39a1e'), hx('#d27a0e'))
        for bx, by in ((195, 32), (202, 39), (209, 46)): c.ell(bx, by, bx + 4, by + 4, hx('#e8833a'))
    # platos de Gala en su base de madera
    c.rect(82, FL + 14, 120, FL + 18, hx('#8a5a32')); c.line([(82, FL + 14), (120, FL + 14)], hx('#b07a4a'))
    for lx in (86, 116): c.line([(lx, FL + 18), (lx - 2, FL + 28)], hx('#222222'))
    for bx in (86, 102): c.ell(bx, FL + 10, bx + 13, FL + 16, hx('#c9ced2'), hx('#7e858a')); c.ell(bx + 3, FL + 11, bx + 10, FL + 14, hx('#9aa1a6'))

def door(c):
    # manguera enrollada colgada
    for i in range(4): c.ell(218 - i, 64 + i, 232 + i, 84 + i, None, hx('#e9e9e4'))
    c.line([(225, 84), (225, 120)], hx('#e9e9e4'))
    c.rect(236, 28, 284, FL - 1, hx('#2a2d2c')); c.rect(240, 34, 280, 96, hx('#5d6563'))
    for y in range(38, 96, 5): c.line([(242, y), (278, y)], hx('#444b49'))
    c.rect(240, 100, 280, FL - 4, hx('#33373a'))
    c.line([(232, 24), (290, 24)], hx('#8c8c8c'), 2)
    c.poly([(262, 26), (292, 26), (290, FL - 1), (268, FL - 1), (272, 90)], hx('#fbfbf8'), hx('#d6d6d0'))   # cortina recogida
    for x in (270, 278, 286): c.line([(x, 30), (x + 1, FL - 4)], hx('#e6e6e0'))
    if SEASON == 'halloween':
        c.poly([(246, 40), (258, 40), (252, 52)], hx('#f3a6c4')); c.rect(250, 44, 251, 44, hx('#1f1f1f')); c.rect(254, 44, 254, 44, hx('#1f1f1f'))

def dining(c):
    # cuadro sobre la mesa
    c.ao(304, 34, 340, 78, 40)
    c.rect(300, 30, 336, 74, hx('#ffffff'), hx('#c9c9c9'))
    if SEASON == 'halloween':
        c.rect(303, 33, 333, 71, hx('#e3dceb'))
        for gx in (310, 322): c.ell(gx, 46, gx + 8, 56, hx('#fbfbfb')); c.rect(gx, 51, gx + 8, 62, hx('#fbfbfb')); c.rect(gx + 2, 50, gx + 2, 50, hx('#555555')); c.rect(gx + 5, 50, gx + 5, 50, hx('#555555'))
        c.noise(303, 58, 333, 71, [hx('#c9b8dc'), hx('#f3c4cf')], 0.3)
    else:
        c.rect(303, 33, 333, 71, hx('#eef0e6'))
        c.noise(303, 50, 333, 71, [hx('#c9d8b0'), hx('#f3c4cf'), hx('#d9c8ec'), hx('#a8c48a')], 0.5)
        c.line([(303, 52), (333, 48)], hx('#b8c9a0'))
    # sillas tapizadas con textura de petatillo
    for x0 in (290, 396):
        c.rect(x0, 94, x0 + 26, FL + 10, hx('#cdb68f'), hx('#9a8462'))
        for yy in range(96, FL + 8, 3):
            for xx in range(x0 + 2, x0 + 25, 4): c.line([(xx + (yy // 3) % 2 * 2, yy), (xx + 1 + (yy // 3) % 2 * 2, yy)], hx('#b9a079'))
        c.line([(x0 + 1, 95), (x0 + 25, 95)], hx('#e2cfa8'))
    c.ao(312, FL, 408, FL + 8, 60)
    # mantel de cuadros amarillos
    c.poly([(312, 110), (404, 110), (412, FL + 2), (306, FL + 2)], hx('#f3df6a'))
    for x in range(312, 406, 7): c.line([(x, 110), (x - 3 + (x - 358) * 0.08, FL + 2)], hx('#fbf5d8'), 2)
    for y in range(114, FL + 2, 6): c.line([(308, y), (410, y)], hx('#fbf5d8'), 2)
    c.line([(312, 110), (404, 110)], hx('#e5c94a'))
    c.ell(322, 96, 334, 110, hx('#f3b6c4'), hx('#c48d9b'))              # termo rosa
    c.rect(340, 100, 362, 109, hx('#9fc4e0'), hx('#4a5a6a'))            # tablet
    c.rect(370, 102, 380, 109, hx('#c9a26b'), hx('#8a6a3d'))            # bolsita

def sofa_tv_window(c, tv):
    # ventana con visillos
    c.rect(486, 16, W0 - 1, 106, hx('#dfe9f2'))
    for x in range(488, W0, 6): c.line([(x, 16), (x + 2, 106)], hx('#c4d0db'))
    c.rect(482, 12, W0 - 1, 14, hx('#8c8c8c'))
    c.noise(486, 16, W0 - 1, 106, [hx('#eef4f8'), hx('#cbd7e2')], 0.2)
    # cuadritos
    c.rect(426, 64, 440, 84, hx('#d9c39c'), hx('#a88a5a')); c.rect(428, 66, 438, 82, hx('#f6f1e6')); c.ell(430, 72, 436, 80, hx('#c9a07a'))   # conejito
    # la tele (Gala con Dios)
    c.ao(396, 12, 486, 64, 45)
    c.rect(392, 8, 482, 60, hx('#b99a6a')); c.line([(392, 8), (482, 8)], hx('#d9bf8f')); c.rect(395, 11, 479, 57, hx('#111214'))
    if tv is not None: c.im.alpha_composite(tv.resize((tv.width * c.k, tv.height * c.k), Image.NEAREST), (396 * c.k, 12 * c.k)); c.d = ImageDraw.Draw(c.im)
    if SEASON == 'halloween':
        for lx in range(392, 484, 7): c.poly([(lx, 8), (lx + 3, 4), (lx + 6, 8), (lx + 3, 11)], hx('#e8722a'))
    # candil dorado tipo sputnik
    c.line([(436, 0), (436, 3)], hx('#c9a24a'))
    for a, b in (((418, 6), (454, 0)), ((422, 0), (450, 8)), ((436, 3), (436, 9))): c.line([a, b], hx('#c9a24a'))
    for bx, by in ((418, 6), (454, 0), (422, 0), (450, 8), (436, 9)): c.ell(bx - 2, by - 1, bx + 2, by + 3, hx('#fff6cc'), hx('#c9a24a'))
    # sillón en L
    c.shadow(392, FL + 2, W0 + 10, FL + 12, 70)
    c.rounded = None
    c.rect(404, 96, W0 - 1, FL + 6, hx('#cbb79b'), hx('#9c8a70'))
    c.rect(408, 82, W0 - 1, 100, hx('#d8c6ab'), hx('#9c8a70'))
    c.noise(404, 82, W0 - 1, FL + 6, [hx('#c2ad90'), hx('#dccbb2')], 0.25)
    c.line([(408, 100), (W0 - 1, 100)], hx('#b5a184')); c.line([(470, 100), (470, FL + 6)], hx('#b5a184'))
    c.rect(398, 104, 412, FL + 8, hx('#bba78b'), hx('#9c8a70'))
    # cojines
    if SEASON == 'halloween':
        c.ell(420, 80, 444, 102, hx('#e8833a'), hx('#9c4e1c'))
        c.poly([(427, 88), (430, 86), (431, 90)], hx('#3a2010')); c.poly([(437, 86), (440, 88), (436, 90)], hx('#3a2010')); c.line([(427, 95), (437, 95)], hx('#3a2010'))
        c.rect(452, 82, 474, 100, hx('#7fb04a'), hx('#4e7a2a')); c.line([(456, 88), (470, 88)], hx('#2f5527'))
        c.rect(480, 84, 506, 102, hx('#f3c4cf'), hx('#b98592'))
        c.rect(510, 78, 534, 98, hx('#e9e6df'), hx('#a9a59b')); c.rect(514, 84, 530, 88, hx('#1f1f1f'))
    else:
        for x0, col in ((418, '#e9e6df'), (446, '#d9d3c6'), (476, '#e9e6df'), (506, '#f3c4cf')):
            c.rect(x0, 80, x0 + 24, 100, hx(col), hx('#a9a59b'))
            for i in range(3): c.line([(x0 + 3 + i * 7, 84), (x0 + 6 + i * 7, 96)], hx('#c9c3b6'))

def lighting(img, k):
    a = np.asarray(img).astype(np.float32); H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    L = 0.90 + 0.14 * np.exp(-(((xx - 436 * k) / (120 * k)) ** 2 + ((yy - 10 * k) / (90 * k)) ** 2)) \
        + 0.10 * np.exp(-(((xx - 520 * k) / (70 * k)) ** 2 + ((yy - 60 * k) / (80 * k)) ** 2)) \
        - 0.06 * np.exp(-(((xx - 60 * k) / (90 * k)) ** 2))
    by = BAYER[yy.astype(int) % 4, xx.astype(int) % 4]
    Lq = np.floor(L * 12 + by) / 12
    rgb = a[..., :3] * Lq[..., None]; rgb[..., 0] *= 1.02; rgb[..., 2] *= 0.97
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a[..., 3].astype(np.uint8)]), 'RGBA')

def tv_image():
    if not os.path.exists(TV_IMG): return None
    src = Image.open(TV_IMG).convert('RGB'); tw, th = 82, 44; sw, sh = src.size; kk = max(tw / sw, th / sh)
    src = src.resize((round(sw * kk), round(sh * kk)), Image.LANCZOS); l = (src.width - tw) // 2; t = (src.height - th) // 2
    return src.crop((l, t, l + tw, t + th)).quantize(colors=28, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGBA')

def background(k=1):
    c = CS(k); walls(c); floor(c); stairs(c); door(c); dining(c); sofa_tv_window(c, tv_image())
    return lighting(c.im, k)

POS = {'P06': (-2, 121), 'P08': (198, 121), 'P07': (462, 121)}
def compose(moods=None):
    S = str(ROOT / 'public' / 'sprites') + '/'; moods = moods or {}
    bg = background(1)
    for pid, (x, y) in POS.items():
        bg.alpha_composite(Image.open(f'{S}{pid}_{moods.get(pid, "feliz")}.png').convert('RGBA'), (x, y))
    return bg

if __name__ == '__main__':
    out = os.environ.get('OUT', '.') + '/'
    a = compose().resize((W0 * 2, H0 * 2), Image.NEAREST)
    SEASON = 'halloween'; b = compose().resize((W0 * 2, H0 * 2), Image.NEAREST)
    s = Image.new('RGBA', (W0 * 2, H0 * 4 + 16), (42, 47, 43, 255)); s.alpha_composite(a); s.alpha_composite(b, (0, H0 * 2 + 16)); s.save(out + 'sala_temporadas.png')
