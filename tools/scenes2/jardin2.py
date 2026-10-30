# Jardín v2 ("la casita"): cochera y pasillo del patio, de día.
import math, random, sys, os
import numpy as np
from PIL import Image, ImageDraw
import pathlib; ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'tools' / 'scenes')); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gala import hx
from estudio2 import C, BAYER

SEASON = None
IRON, IRON_L = hx('#1c1d1d'), hx('#3a3c3c')

class CW(C):
    def __init__(self, k, W0, H0, seed=7):
        super().__init__(k, seed); self.W, self.H = W0 * k, H0 * k
        self.im = Image.new('RGBA', (self.W, self.H)); self.d = ImageDraw.Draw(self.im)

def stone_wall(c, x0, y0, x1, y1, seed=1):
    r = random.Random(seed); c.rect(x0, y0, x1, y1, hx('#cfc9bb'))
    y, row = y0, 0
    while y < y1:
        h = r.randint(8, 11); x = x0 - (row % 2) * 10
        while x < x1:
            w = r.randint(14, 24); xa, xb, yb = max(x, x0), min(x + w, x1), min(y + h, y1)
            if xb - xa < 3 or yb - y < 3: x += w; continue
            tone = hx(r.choice(['#ece7dc', '#e2dccf', '#f3efe6', '#d9d2c3']))
            c.rect(xa + 1, y + 1, xb - 1, yb - 1, tone)
            c.line([(xa + 1, y + 1), (xb - 1, y + 1)], hx('#fbf9f4')); c.line([(xa + 1, yb - 1), (xb - 1, yb - 1)], hx('#b9b2a2'))
            c.noise(xa + 1, y + 1, xb - 1, yb - 1, [hx('#c9c2b2'), hx('#faf8f2'), hx('#a9a292')], 0.25)
            x += w
        y += h; row += 1

def sky(c, x0, y0, x1, y1):
    for y in range(y0, y1): c.line([(x0, y), (x1, y)], (140 + (y - y0) // 2, 196 + (y - y0) // 5, 238, 255))

def ground(c, W0, y0, H0, seed=4):
    r = random.Random(seed)
    c.rect(0, y0, W0 - 1, H0 - 1, hx('#6f553a'))
    c.noise(0, y0, W0 - 1, H0 - 1, [hx('#5f4831'), hx('#7f6446'), hx('#4f6a32'), hx('#5e7d3a')], 0.45)
    for _ in range(W0 // 2):
        x, y = r.randrange(W0), r.randrange(y0 + 3, H0); col = hx(r.choice(['#6f9a3a', '#5e8a30', '#86ad48', '#9aba5a']))
        c.line([(x, y), (x - 1, y - 4)], col); c.line([(x + 1, y), (x + 2, y - 3)], col)

def string_lights(c, W0, y0=4, sag=9):
    def yy(x): return y0 + sag * math.sin(math.pi * ((x % 160) / 160))
    c.line([(x, yy(x)) for x in range(0, W0 + 1, 2)], hx('#2a2a2a'))
    for x in range(10, W0, 22):
        y = yy(x); c.line([(x, y), (x, y + 3)], hx('#2a2a2a')); c.ell(x - 2, y + 3, x + 2, y + 8, hx('#fff2b8'), hx('#c9b56a'))

def iron_fence(c, x0, x1, y0, y1, circles=True):
    for x in range(x0 + 3, x1, 7): c.line([(x, y0), (x, y1)], IRON)
    for y in (y0, y1): c.line([(x0, y), (x1, y)], IRON, 2)
    if circles:
        for cx in range(x0 + 14, x1 - 6, 26):
            c.ell(cx - 10, y0 + 8, cx + 10, y0 + 28, None, IRON, 2); c.d.arc([(cx - 5) * c.k, (y0 + 13) * c.k, (cx + 5) * c.k, (y0 + 23) * c.k], 0, 270, fill=IRON)
        for cx in range(x0 + 6, x1, 10): c.ell(cx - 4, y1 - 10, cx + 4, y1 - 2, None, IRON)

def light(img, k, sun=(0.9, 0.22)):
    a = np.asarray(img).astype(np.float32); H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    L = sun[0] + sun[1] * np.exp(-((yy / (110 * k)) ** 2))
    by = BAYER[yy.astype(int) % 4, xx.astype(int) % 4]; Lq = np.floor(L * 12 + by) / 12
    rgb = a[..., :3] * Lq[..., None]; rgb[..., 0] *= 1.03; rgb[..., 2] *= 0.96
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a[..., 3].astype(np.uint8)]), 'RGBA')

# ---------------- cochera ----------------
CO_W, CO_H, CO_FL = 480, 220, 160
CO_POS = {'P04': (-6, 120), 'P18': (52, 92), 'P24': (150, 120), 'P17': (222, 120), 'P22': (290, 120), 'P15': (372, 118)}

def cochera_bg(k=1):
    c = CW(k, CO_W, CO_H); r = random.Random(21)
    # alero de la casa arriba
    c.rect(0, 0, CO_W - 1, 24, hx('#f4f1e8')); c.rect(0, 22, CO_W - 1, 26, hx('#d6d1c3'))
    # muro amarillo texturizado
    c.rect(150, 26, 430, CO_FL, hx('#e8c86a')); c.noise(150, 26, 430, CO_FL, [hx('#d9b956'), hx('#f2d684'), hx('#caa848')], 0.4)
    # muro de piedra con tejado de barro
    stone_wall(c, 0, 52, 150, CO_FL, seed=3)
    c.poly([(0, 38), (152, 38), (164, 54), (0, 54)], hx('#a2502d'))
    for x in range(0, 164, 8): c.d.arc([x * k, 44 * k, (x + 8) * k, 56 * k], 180, 360, fill=hx('#7a3a1e'), width=k)
    c.line([(0, 38), (152, 38)], hx('#c9744a'))
    # faroles colgantes
    for lx in (220, 360):
        c.line([(lx, 26), (lx, 44)], hx('#3a3a3a')); c.ell(lx - 7, 22, lx + 7, 28, hx('#8a5a3a'))
        c.ell(lx - 6, 44, lx + 6, 62, hx('#fff4c8'), hx('#5a5a5a')); c.ell(lx - 3, 48, lx + 1, 54, hx('#ffffff'))
        c.rect(lx - 3, 62, lx + 3, 65, hx('#5a5a5a'))
    # óvalo de herrería
    c.ell(276, 54, 304, 94, None, hx('#5a3a2a'), 3); c.ell(281, 60, 299, 88, hx('#b8502a'), hx('#7a3a1e'))
    c.line([(290, 50), (290, 98)], hx('#5a3a2a')); c.line([(272, 74), (308, 74)], hx('#5a3a2a'))
    if SEASON == 'halloween':   # corona de cempasúchil
        for a in range(0, 360, 18):
            x = 118 + 14 * math.cos(math.radians(a)); y = 82 + 14 * math.sin(math.radians(a)); c.ell(x - 3, y - 3, x + 3, y + 3, hx('#f39a1e'), hx('#c9700a'))
        for gy in range(98, 128, 5): c.ell(115, gy, 121, gy + 5, hx('#f39a1e'), hx('#c9700a'))
    # reja derecha con cielo detrás
    sky(c, 430, 26, CO_W - 1, CO_FL)
    iron_fence(c, 430, CO_W - 1, 30, CO_FL)
    string_lights(c, CO_W)
    ground(c, CO_W, CO_FL, CO_H, 5)
    for (x, y, w, h) in ((170, 200, 34, 14), (214, 184, 30, 11), (250, 170, 26, 9), (300, 196, 34, 14), (338, 178, 30, 11)):
        c.poly([(x, y), (x + w, y), (x + w - 4, y + h), (x - 4, y + h)], hx('#c2bdb0'), hx('#8c877a')); c.line([(x, y), (x + w, y)], hx('#e2ded4'))
    # jardinera de la bugambilia grande
    c.rect(4, 170, 148, 198, hx('#e2c27a'), hx('#a58a4a')); c.noise(4, 170, 148, 198, [hx('#d4b46a'), hx('#ecd090')], 0.3)
    stone_wall(c, 4, 198, 40, CO_H - 1, seed=9)
    for pid, (x, y) in CO_POS.items(): c.shadow(x + 18, 206, x + 64, 214, 70)
    return light(c.im, k)

# ---------------- pasillo ----------------
PA_W, PA_H, PA_FL = 680, 220, 150
PA_POS = {'P21': (-4, 108), 'P25': (54, 110), 'P14': (118, 104), 'P16': (190, 112), 'P03': (252, 108), 'P26': (318, 110), 'P19': (384, 108), 'P20': (446, 112), 'P23': (500, 112), 'P27': (548, 112)}

def pasillo_bg(k=1):
    c = CW(k, PA_W, PA_H); r = random.Random(22); O = 80
    sky(c, 0, 0, PA_W - 1, PA_FL)
    # casas de enfrente, genéricas y desenfocadas
    for x0, x1, col in ((0, 120, '#e9c33a'), (130, 260, '#b9c6d2'), (270, 420, '#e7d6c0'), (430, 580, '#e9c33a')):
        c.rect(x0, 40, x1, 96, hx(col)); c.rect(x0, 36, x1, 40, hx('#b5523a'))
        for wx in range(x0 + 10, x1 - 16, 34): c.rect(wx, 50, wx + 14, 64, hx('#f4f1e6')); c.rect(wx + 2, 52, wx + 12, 62, hx('#9fb6c9'))
    c.rect(0, 96, 500 + O, PA_FL, hx('#d9a48c')); c.noise(0, 96, 500 + O, PA_FL, [hx('#cc957c'), hx('#e6b39c')], 0.3)
    c.line([(0, 96), (500 + O, 96)], hx('#f0c6b2'))
    iron_fence(c, 0, 500 + O, 30, 96)
    for x in range(0, 500 + O, 4):   # malla de gallinero
        for y in range(34, 94, 4): c.rect(x, y, x, y, hx('#9a9c9c'))
    # copa del liquidámbar
    for _ in range(170):
        x, y = r.randrange(70, 350), r.randrange(0, 40); col = hx(r.choice(['#3f6b33', '#4f7d3d', '#2f5527', '#5e8f45']))
        for a in range(5):
            ang = math.radians(a * 72 - 90); c.line([(x, y), (x + 5 * math.cos(ang), y + 5 * math.sin(ang))], col, 2)
    # la casita: entrada de piedra, techo blanco a dos aguas, reja en arco y puerta con vitral
    stone_wall(c, 500 + O, 40, PA_W - 1, PA_H - 1, seed=12)
    c.poly([(486 + O, 46), (550 + O, 6), (614 + O, 46)], hx('#f6f4ee'), hx('#c9c4b6')); c.line([(486 + O, 46), (550 + O, 6)], hx('#ffffff'))
    c.rect(520 + O, 70, 580 + O, PA_FL + 40, hx('#4a2a1a')); c.pieslice = None
    c.d.pieslice([(520 + O) * k, 46 * k, (580 + O) * k, 96 * k], 180, 360, fill=hx('#4a2a1a'))
    c.rect(530 + O, 84, 569 + O, 138, hx('#f4c25a')); c.line([(550 + O, 84), (550 + O, 138)], hx('#4a2a1a'), 2)
    for gx in (534 + O, 556 + O): c.d.arc([gx * k, 92 * k, (gx + 10) * k, 112 * k], 180, 360, fill=hx('#c99a3a'), width=k)
    c.ell(538 + O, 76, 562 + O, 96, hx('#6a4a2a'), hx('#3a2a1a'))   # corona de la puerta
    for x in range(524 + O, 580 + O, 6):
        c.line([(x, 70), (x, PA_FL + 40)], IRON); c.poly([(x - 1, 74), (x, 70), (x + 1, 74)], IRON)
    c.d.arc([(520 + O) * k, 46 * k, (580 + O) * k, 96 * k], 180, 360, fill=IRON, width=2 * k)
    for cx in (534 + O, 550 + O, 566 + O): c.ell(cx - 5, 52, cx + 5, 62, None, IRON)
    c.line([(520 + O, 140), (580 + O, 140)], IRON, 2)
    for cx in (536 + O, 564 + O): c.ell(cx - 9, 144, cx + 9, 162, None, IRON)
    string_lights(c, PA_W, y0=2, sag=8)
    # jardinera y piso de loseta clara
    ground(c, PA_W, PA_FL, PA_H, 6)
    c.rect(0, PA_FL, PA_W - 1, PA_FL + 3, hx('#c9b8a4'))
    c.poly([(0, 200), (PA_W - 1, 190), (PA_W - 1, PA_H - 1), (0, PA_H - 1)], hx('#e9e4da'))
    c.noise(0, 196, PA_W - 1, PA_H - 1, [hx('#ddd7cb'), hx('#f4f1ea')], 0.3)
    for x in range(0, PA_W, 26): c.line([(x, 200 - (x / PA_W) * 10), (x - 6, PA_H)], hx('#cfc8ba'))
    c.line([(0, 208), (PA_W - 1, 199)], hx('#cfc8ba'))
    for rx, ry in ((30, 176), (46, 172), (100, 180)): c.ell(rx, ry, rx + 18, ry + 14, hx('#b9a58c'), hx('#7d6b55')); c.line([(rx + 4, ry + 3), (rx + 10, ry + 2)], hx('#d8c7ae'))
    if SEASON == 'halloween':
        for px_, py_ in ((150, 182), (166, 186)): c.ell(px_, py_, px_ + 14, py_ + 11, hx('#e8833a'), hx('#9c4e1c')); c.line([(px_ + 7, py_ - 2), (px_ + 7, py_ + 1)], hx('#5e7a35'), 2)
        c.ell(430, 186, 442, 196, hx('#f3ead2'), hx('#b0a280'))
    for pid, (x, y) in PA_POS.items(): c.shadow(x + 18, 202, x + 64, 210, 60)
    return light(c.im, k, (0.92, 0.18))

def compose(name, moods=None):
    S = str(ROOT / 'public' / 'sprites') + '/'; moods = moods or {}
    bg, pos = (cochera_bg(), CO_POS) if name == 'cochera' else (pasillo_bg(), PA_POS)
    for pid, (x, y) in pos.items(): bg.alpha_composite(Image.open(f'{S}{pid}_{moods.get(pid, "feliz")}.png').convert('RGBA'), (x, y))
    return bg

if __name__ == '__main__':
    out = os.environ.get('OUT', '.') + '/'
    co = compose('cochera'); SEASON = 'halloween'; coh = compose('cochera'); pa_h = compose('pasillo'); SEASON = None; pa = compose('pasillo')
    s = Image.new('RGBA', (PA_W * 2, (CO_H * 2 + 16) * 2 + PA_H * 4 + 16), (42, 47, 43, 255)); y = 0
    for im in (co, coh, pa, pa_h):
        s.alpha_composite(im.resize((im.width * 2, im.height * 2), Image.NEAREST), (0, y)); y += im.height * 2 + 16
    s.save(out + 'jardin_temporadas.png')
