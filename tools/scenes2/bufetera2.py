# Bufetera v2: pasillo con la bufetera de listones, espejo redondo y los tres esquejes.
import random, sys, os
import numpy as np
from PIL import Image, ImageDraw
import pathlib; ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'tools' / 'scenes')); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gala import hx
from estudio2 import C, BAYER

SEASON = None
FL = 160
W0, H0 = 360, 210

def walls(c):
    c.rect(0, 0, W0 - 1, FL, hx('#efebe2')); c.noise(0, 8, W0 - 1, FL, [hx('#e3ddd0'), hx('#f8f5ee')], 0.2)
    c.rect(0, 0, W0 - 1, 7, hx('#f5f2ea')); c.noise(0, 0, W0 - 1, 7, [hx('#e3dfd4'), hx('#fbfaf6')], 0.35); c.line([(0, 8), (W0 - 1, 8)], hx('#d6cfbe'))
    # marco de puerta café a la izquierda
    c.rect(0, 8, 13, H0 - 1, hx('#6a3a26')); c.line([(13, 8), (13, H0 - 1)], hx('#4e2a1b')); c.line([(2, 8), (2, H0 - 1)], hx('#8a5236'))
    c.rect(40, 96, 48, 106, hx('#f7f7f4'), hx('#bdbab2')); c.rect(43, 99, 43, 101, hx('#5a5a5a')); c.rect(45, 99, 45, 101, hx('#5a5a5a'))
    c.line([(44, 106), (52, 130), (64, 140)], hx('#1f1f1f'))
    # vano hacia la sala (derecha): sillón, ventana con luz, candil
    c.rect(300, 8, W0 - 1, FL, hx('#e9e4d8')); c.line([(300, 8), (300, FL)], hx('#cfc8b6'), 2)
    c.rect(318, 34, W0 - 1, 96, hx('#e6eef5'));
    for x in range(320, W0, 5): c.line([(x, 34), (x + 2, 96)], hx('#c9d4de'))
    c.rect(306, 108, W0 - 1, 150, hx('#cbb79b'), hx('#9c8a70')); c.rect(310, 98, W0 - 1, 112, hx('#d8c6ab'), hx('#9c8a70'))
    for gx, gy in ((326, 20), (338, 16), (350, 22)): c.ell(gx, gy, gx + 4, gy + 4, hx('#fff4c2'), hx('#c9a24a'))
    c.line([(326, 22), (354, 18)], hx('#c9a24a'))

def floor(c):
    c.rect(0, FL, W0 - 1, H0 - 1, hx('#a2462a'))
    rows = [FL]; y, h = FL, 9
    while y < H0: y += h; h += 5; rows.append(y)
    vx = W0 / 2
    for j in range(len(rows) - 1):
        ya, yb = rows[j], min(rows[j + 1], H0 - 1)
        for i in range(-9, 9):
            ta, tb = (ya - FL) / (H0 - FL), (yb - FL) / (H0 - FL)
            pts = [(vx + i * 30 * (1 + .9 * ta), ya), (vx + (i + 1) * 30 * (1 + .9 * ta), ya), (vx + (i + 1) * 30 * (1 + .9 * tb), yb), (vx + i * 30 * (1 + .9 * tb), yb)]
            c.poly(pts, [hx('#a2462a'), hx('#9a4025'), hx('#ab4f30')][(i + j) % 3])
    c.noise(0, FL, W0 - 1, H0 - 1, [hx('#8f3b20'), hx('#b75c3a'), hx('#c06a48')], 0.3)
    for y in rows[1:]: c.line([(0, y), (W0 - 1, y)], hx('#6e2c16'))
    for i in range(-9, 10): c.line([(vx + i * 30, FL), (vx + i * 30 * 1.9, H0)], hx('#6e2c16'))
    for y in rows[1:]:
        t = (y - FL) / (H0 - FL); s = 2.5 + t * 4
        for i in range(-9, 10):
            x = vx + i * 30 * (1 + .9 * t)
            if 0 <= x < W0:
                c.poly([(x, y - s), (x + s * .35, y), (x, y + s), (x - s * .35, y)], hx('#f2efe8')); c.poly([(x - s, y), (x, y - s * .35), (x + s, y), (x, y + s * .35)], hx('#f2efe8')); c.rect(x, y, x, y, hx('#3a4f8a'))

def mirror(c):
    c.shadow(116, 12, 222, 118, 45)
    c.ell(112, 8, 216, 112, hx('#a8743f')); c.ell(115, 11, 213, 109, hx('#c8935a')); c.ell(118, 14, 210, 106, hx('#d6dadd'))
    # reflejo: techo, puerta café del pasillo y un cuadrito
    c.rect(140, 28, 160, 106, hx('#6a3a26')); c.rect(184, 30, 198, 106, hx('#6a3a26'))
    c.rect(162, 52, 176, 70, hx('#f2ece0'), hx('#9a8a70')); c.ell(166, 56, 172, 64, hx('#e2a0a8'))
    c.d.arc([118 * c.k, 14 * c.k, 210 * c.k, 106 * c.k], 200, 250, fill=hx('#ffffff'), width=2 * c.k)
    if SEASON == 'halloween':
        for gx, gy in ((126, 40), (196, 26), (124, 78), (188, 84), (150, 18)):
            c.ell(gx, gy, gx + 9, gy + 9, hx('#fbfbfb'), hx('#9a9a9a')); c.rect(gx, gy + 5, gx + 9, gy + 12, hx('#fbfbfb'))
            c.rect(gx + 3, gy + 4, gx + 3, gy + 4, hx('#444444')); c.rect(gx + 6, gy + 4, gx + 6, gy + 4, hx('#444444'))
        for i, ch in enumerate('BOO'): c.ell(150 + i * 8, 46, 156 + i * 8, 54, None, hx('#e75a9a'), 1)
        for sx, sy in ((160, 24), (176, 92), (204, 60)): c.poly([(sx, sy - 2), (sx + 1, sy), (sx, sy + 2), (sx - 1, sy)], hx('#e2c044'))

def buffet(c):
    c.ao(62, 186, 306, 194, 70)
    c.rect(62, 122, 306, 127, hx('#f6f2ea'), hx('#b9ad97')); c.line([(62, 122), (306, 122)], hx('#ffffff'))
    c.rect(66, 128, 302, 184, hx('#e7d1a6'))
    for x in range(68, 302, 5):
        c.line([(x, 129), (x, 183)], hx('#c8ac7a')); c.line([(x + 1, 129), (x + 1, 183)], hx('#f1e0bc'))
    c.line([(184, 129), (184, 183)], hx('#8f7650'), 2); c.line([(128, 152), (184, 152)], hx('#8f7650')); c.line([(128, 129), (128, 183)], hx('#8f7650'))
    c.rect(66, 184, 302, 188, hx('#b99a68'))
    for lx in (72, 296): c.rect(lx, 188, lx + 3, 194, hx('#6a5232'))
    # cosas encima (todo el año): vasos, platos, florero con flores naranjas
    for gx in (92, 100, 108): c.rect(gx, 112, gx + 6, 122, hx('#dfe7ea'), hx('#9aa6aa')); c.line([(gx + 1, 113), (gx + 1, 120)], hx('#ffffff'))
    for i in range(5): c.line([(234, 121 - i * 2), (254, 121 - i * 2)], hx('#eceff1'));
    c.rect(234, 112, 254, 121, None, hx('#9aa6aa'))
    c.rect(262, 106, 268, 122, hx('#cfe0e6'), hx('#8aa0a8'))
    for fx, fy in ((258, 96), (266, 92), (272, 100)): c.line([(265, 106), (fx + 2, fy + 3)], hx('#4e7a2a')); c.ell(fx, fy, fx + 6, fy + 6, hx('#f08a3a'), hx('#b8561a'))
    if SEASON == 'halloween':
        c.ell(70, 108, 88, 122, hx('#e8833a'), hx('#9c4e1c')); c.line([(79, 104), (79, 109)], hx('#5e7a35'), 2)
        c.ell(76, 100, 86, 110, hx('#f0e6d0'), hx('#a99a7a'))
        for i, bx in enumerate((112, 214, 276, 290)):   # bolsitas de dulces
            c.rect(bx, 106 - (i % 2) * 4, bx + 10, 122, hx('#c9a26b'), hx('#8a6a3d')); c.line([(bx, 108 - (i % 2) * 4), (bx + 10, 108 - (i % 2) * 4)], hx('#a8834e'))
    # robot aspiradora
    c.shadow(18, 194, 58, 204, 70)
    c.ell(18, 186, 56, 200, hx('#3a3a3a'), hx('#1a1a1a')); c.ell(28, 189, 46, 196, hx('#6d6d6d')); c.rect(36, 190, 38, 191, hx('#4fc06a'))

def lighting(img, k):
    a = np.asarray(img).astype(np.float32); H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    L = 0.88 + 0.14 * np.exp(-(((xx - 330 * k) / (90 * k)) ** 2 + ((yy - 60 * k) / (90 * k)) ** 2)) + 0.06 * np.exp(-(((yy - 0) / (100 * k)) ** 2)) - 0.06 * np.exp(-(((xx) / (80 * k)) ** 2))
    by = BAYER[yy.astype(int) % 4, xx.astype(int) % 4]; Lq = np.floor(L * 12 + by) / 12
    rgb = a[..., :3] * Lq[..., None]; rgb[..., 0] *= 1.02; rgb[..., 2] *= 0.97
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a[..., 3].astype(np.uint8)]), 'RGBA')

def background(k=1):
    c = C(k); walls(c); floor(c); mirror(c); buffet(c)
    return lighting(c.im, k)

POS = {'P12': (112, 30), 'P10': (150, 30), 'P11': (184, 30)}
def compose(moods=None):
    S = str(ROOT / 'public' / 'sprites') + '/'; moods = moods or {}
    bg = background(1)
    for pid, (x, y) in POS.items(): bg.alpha_composite(Image.open(f'{S}{pid}_{moods.get(pid, "feliz")}.png').convert('RGBA'), (x, y))
    return bg

if __name__ == '__main__':
    out = os.environ.get('OUT', '.') + '/'
    a = compose().resize((W0 * 2, H0 * 2), Image.NEAREST)
    SEASON = 'halloween'; b = compose().resize((W0 * 2, H0 * 2), Image.NEAREST)
    s = Image.new('RGBA', (W0 * 2, H0 * 4 + 16), (42, 47, 43, 255)); s.alpha_composite(a); s.alpha_composite(b, (0, H0 * 2 + 16)); s.save(out + 'bufetera_temporadas.png')
