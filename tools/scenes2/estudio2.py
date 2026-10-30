# Estudio v2: misma escena en dos densidades (k=1 resolución actual pulida, k=2 doble resolución).
import math, random, sys, os
import numpy as np
from PIL import Image, ImageDraw
import pathlib; ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'tools' / 'scenes')); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gala import hx

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0

def mixc(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3)) + (255,)

class C:
    """Lienzo escalado: todas las coordenadas se dan en la rejilla nativa 360x210."""
    def __init__(self, k, seed=7):
        self.k = k; self.W, self.H = 360 * k, 210 * k
        self.im = Image.new('RGBA', (self.W, self.H)); self.d = ImageDraw.Draw(self.im)
        self.r = random.Random(seed)
    def P(self, *v): return [x * self.k for x in v]
    def rect(self, x0, y0, x1, y1, fill, outline=None, w=1):
        k = self.k; self.d.rectangle([x0 * k, y0 * k, x1 * k + k - 1, y1 * k + k - 1], fill=fill, outline=outline, width=w)
    def poly(self, pts, fill, outline=None):
        self.d.polygon([(x * self.k, y * self.k) for x, y in pts], fill=fill, outline=outline)
    def line(self, pts, fill, w=1):
        self.d.line([(x * self.k, y * self.k) for x, y in pts], fill=fill, width=w)
    def ell(self, x0, y0, x1, y1, fill, outline=None, w=1):
        k = self.k; self.d.ellipse([x0 * k, y0 * k, x1 * k, y1 * k], fill=fill, outline=outline, width=w)
    def noise(self, x0, y0, x1, y1, cols, density):
        k = self.k; n = int((x1 - x0) * (y1 - y0) * k * k * density)
        for _ in range(n):
            self.d.point((self.r.randint(x0 * k, x1 * k + k - 1), self.r.randint(y0 * k, y1 * k + k - 1)), fill=self.r.choice(cols))
    def shadow(self, x0, y0, x1, y1, a=90):
        k = self.k; lay = Image.new('RGBA', self.im.size); ImageDraw.Draw(lay).ellipse([x0 * k, y0 * k, x1 * k, y1 * k], fill=(20, 14, 10, a))
        self.im.alpha_composite(lay)
    def ao(self, x0, y0, x1, y1, a=70):   # sombra rectangular suave (oclusión)
        k = self.k; lay = Image.new('RGBA', self.im.size); ImageDraw.Draw(lay).rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=(20, 14, 10, a))
        self.im.alpha_composite(lay)

FL = 140
VX = 180
SEASON = None   # 'halloween' activa los adornos de temporada

def wall_and_floor(c):
    WALL, WALL_D, WALL_L = hx('#ece6d8'), hx('#ddd5c3'), hx('#f6f2e8')
    c.rect(0, 0, 359, FL, WALL)
    c.noise(0, 8, 359, FL, [WALL_D, WALL_L, hx('#e4ddcd')], 0.22)   # estuco
    # techo texturizado y plafón
    c.rect(0, 0, 359, 7, hx('#f4f1ea')); c.noise(0, 0, 359, 7, [hx('#e3dfd4'), hx('#fbfaf6')], 0.35)
    c.line([(0, 8), (359, 8)], hx('#d6cfbe'))
    c.ell(162, 0, 198, 9, hx('#fffbea'), hx('#c9c2ae')); c.ell(170, 1, 190, 6, hx('#ffffff'))
    # zoclo
    c.rect(0, FL - 4, 359, FL - 1, hx('#d9d1bf')); c.line([(0, FL - 4), (359, FL - 4)], hx('#efe9dc'))
    # piso de loseta gris con junta oscura, en perspectiva
    TILE, TILE_D, TILE_L, GROUT = hx('#c8c3bc'), hx('#b3ada6'), hx('#dad6d0'), hx('#5a544f')
    c.rect(0, FL, 359, 209, TILE)
    rows = [FL]; y, h = FL, 9
    while y < 210: y += h; h += 4; rows.append(y)
    vx = VX
    cols = [vx + i * 26 for i in range(-9, 10)]
    for j in range(len(rows) - 1):
        ya, yb = rows[j], min(rows[j + 1], 209)
        for i in range(len(cols) - 1):
            ta, tb = (ya - FL) / 70, (yb - FL) / 70
            xa0 = vx + (cols[i] - vx) * (1 + 1.6 * ta); xa1 = vx + (cols[i + 1] - vx) * (1 + 1.6 * ta)
            xb0 = vx + (cols[i] - vx) * (1 + 1.6 * tb); xb1 = vx + (cols[i + 1] - vx) * (1 + 1.6 * tb)
            tone = [TILE, hx('#c1bcb5'), hx('#cec9c3')][(i + j) % 3]
            c.poly([(xa0, ya), (xa1, ya), (xb1, yb), (xb0, yb)], tone)
    c.noise(0, FL, 359, 209, [TILE_D, TILE_L, hx('#95908a')], 0.30)  # granito
    for y in rows[1:]: c.line([(0, y), (359, y)], GROUT)
    for x in cols:
        c.line([(x, FL), (vx + (x - vx) * 2.6, 210)], GROUT)
    # brillo del plafón en el piso
    lay = Image.new('RGBA', c.im.size); ImageDraw.Draw(lay).ellipse([110 * c.k, 146 * c.k, 250 * c.k, 176 * c.k], fill=(255, 250, 235, 45)); c.im.alpha_composite(lay)

def painting(c):
    c.ao(70, 16, 200, 80, 45)
    c.rect(64, 10, 196, 76, hx('#7a705f')); c.rect(65, 11, 195, 75, hx('#9a8f7c'))
    c.line([(64, 10), (196, 10)], hx('#b8ad98')); c.line([(64, 10), (64, 76)], hx('#b8ad98'))
    c.rect(68, 14, 192, 72, hx('#d6cdb6')); c.noise(68, 14, 192, 72, [hx('#cdc3aa'), hx('#e0d8c4')], 0.15)
    BL, BL2, BL3, FOAM = hx('#24489a'), hx('#4b7bd0'), hx('#16316a'), hx('#f6f5f0')
    # ola izquierda grande con cresta blanca
    c.poly([(68, 72), (68, 40), (78, 30), (92, 22), (108, 18), (122, 19), (132, 24), (126, 30), (116, 26), (106, 30), (100, 40), (98, 52), (104, 62), (120, 66), (150, 68), (192, 66), (192, 72)], BL)
    c.poly([(70, 66), (72, 46), (82, 34), (94, 28), (88, 42), (84, 56)], BL2)
    c.poly([(98, 52), (100, 40), (106, 30), (104, 44), (104, 56)], BL3)
    c.poly([(80, 26), (92, 18), (108, 14), (124, 16), (136, 22), (132, 28), (122, 22), (108, 22), (94, 26), (84, 32)], FOAM)
    for i in range(12):
        x = 104 + i * 3; c.poly([(x, 24 + (i % 3)), (x + 1.5, 31 + (i % 2) * 2), (x + 3, 24 + (i % 3))], FOAM)
    for i in range(5): c.ell(70 + i * 5, 60 - i * 6, 75 + i * 5, 64 - i * 6, FOAM)
    # ola derecha y barcas
    c.poly([(150, 70), (160, 56), (172, 50), (186, 46), (192, 48), (192, 70)], BL2)
    c.poly([(160, 56), (172, 50), (186, 46), (192, 48), (190, 52), (176, 54), (164, 60)], FOAM)
    c.poly([(140, 60), (148, 50), (156, 60)], hx('#f8f8f4'), hx('#8a8070')); c.poly([(145, 55), (148, 50), (151, 55)], hx('#9fb0c4'))   # Fuji
    for bx, by in ((108, 64), (150, 62)):
        c.poly([(bx, by), (bx + 24, by - 4), (bx + 25, by - 1), (bx + 2, by + 3)], hx('#e0b440'), hx('#8a6a32'))
    c.line([(68, 70), (192, 70)], hx('#1d3a75'))

def bookshelf(c):
    c.ao(0, 182, 54, 189, 70)
    SIDE, SIDE_D, BACK, BOARD = hx('#5b3d2c'), hx('#432c1f'), hx('#6e5240'), hx('#7a5843')
    # papeles y cartulinas asomando arriba
    for pts, col in ((((6,24),(10,6),(22,4),(18,24)), '#e8d6b8'), (((14,24),(24,2),(30,6),(24,24)), '#e9a6b6'),
                     (((22,24),(30,8),(42,10),(38,24)), '#d9c29a'), (((30,24),(44,4),(48,8),(40,24)), '#f2ead8'),
                     (((36,24),(40,12),(46,12),(44,24)), '#2f3b66')):
        c.poly(list(pts), hx(col), hx('#8a7a60'))
    c.rect(0, 22, 47, 184, SIDE_D); c.rect(3, 25, 43, 182, BACK)
    c.noise(3, 25, 43, 182, [hx('#634937'), hx('#76594a')], 0.25)        # veta del fondo
    c.rect(44, 22, 47, 184, SIDE); c.line([(47, 22), (47, 184)], hx('#7d5a44')); c.line([(0, 22), (47, 22)], hx('#7d5a44'))
    shelves = (25, 54, 84, 114, 144, 182)
    for sy in shelves[1:-1]:
        c.rect(3, sy, 43, sy + 2, BOARD); c.line([(3, sy), (43, sy)], hx('#9a7258')); c.ao(3, sy + 3, 43, sy + 5, 70)
    # repisa 1: carpetas, bocina, calabaza
    for i, col in enumerate(('#c0392b', '#f4efe2', '#e9c46a', '#2f3b66', '#f4efe2')):
        c.rect(14 + i * 4, 30, 16 + i * 4, 53, hx(col)); c.line([(14 + i * 4, 30), (14 + i * 4, 53)], mixc(hx(col), (255,255,255), .3))
    if SEASON == 'halloween': c.ell(5, 44, 13, 53, hx('#e8833a'), hx('#9c4e1c')); c.line([(9, 41), (9, 45)], hx('#5e7a35'))
    c.rect(34, 44, 42, 53, hx('#1f1f1f')); c.ell(36, 46, 40, 50, hx('#4a4a4a'))
    # repisa 2: balón, vaso rojo, calabacitas verde y blanca, figuritas
    c.ell(18, 62, 32, 72, hx('#8a4a24'), hx('#4e2a14')); c.line([(21, 67), (29, 67)], hx('#f4efe2')); 
    for x in (23, 25, 27): c.line([(x, 66), (x, 68)], hx('#f4efe2'))
    c.rect(32, 64, 38, 83, hx('#d2342b')); c.line([(32, 64), (32, 83)], hx('#f08a7a')); c.rect(33, 70, 37, 74, hx('#1f1f1f'))
    if SEASON == 'halloween':
        c.ell(10, 74, 20, 83, hx('#4f7d3d'), hx('#2f5527')); c.line([(13, 75), (13, 82)], hx('#2f5527')); c.line([(17, 75), (17, 82)], hx('#2f5527'))
        c.ell(37, 76, 43, 83, hx('#f3ead2'), hx('#b0a280'))
    else:   # carrito F1 a escala, color papaya
        PAP, PAPD = hx('#ff8000'), hx('#b85a00')
        c.poly([(4, 81), (8, 78), (16, 77), (22, 79), (24, 81)], PAP, PAPD)
        c.rect(14, 76, 16, 78, hx('#1f1f1f')); c.rect(21, 76, 24, 77, hx('#47c7fc')); c.rect(3, 80, 6, 81, hx('#47c7fc'))
        c.ell(5, 80, 9, 84, hx('#1f1f1f')); c.ell(18, 80, 22, 84, hx('#1f1f1f'))
    for x in (5, 8): c.rect(x, 78, x + 1, 83, hx('#e9c46a'))
    # repisa 3: libros inclinados y figura de astronauta
    for i, col in enumerate(('#f4efe2', '#e9c46a', '#d9534f', '#f4efe2', '#2e86c1', '#c0392b')):
        x = 16 + i * 4; c.poly([(x, 113), (x + 3, 113), (x + 7, 90), (x + 4, 90)], hx(col), mixc(hx(col), (0,0,0), .35))
    c.poly([(14, 92), (40, 86), (41, 88), (15, 94)], hx('#f4efe2'), hx('#b0a280'))   # folder acostado
    c.ell(4, 98, 14, 108, hx('#f4f4f4'), hx('#9a9a9a')); c.ell(6, 100, 12, 105, hx('#2b2b3b')); c.rect(5, 107, 13, 113, hx('#f4f4f4'), hx('#9a9a9a'))
    # repisa 4: peluche verde y lámpara redonda
    c.ell(7, 126, 21, 143, hx('#5fbf4a'), hx('#2f7a2a'))                 # periquito de peluche
    c.ell(9, 120, 19, 130, hx('#7fd35a'), hx('#2f7a2a')); c.ell(11, 133, 17, 141, hx('#e9f5a8'))
    c.rect(11, 123, 12, 124, hx('#1f1f1f')); c.poly([(13, 125), (16, 125), (14, 128)], hx('#f2a33a'))
    c.poly([(19, 128), (24, 136), (20, 140)], hx('#3f9a3a')); c.poly([(12, 143), (14, 148), (16, 143)], hx('#2e86c1'))
    c.ell(24, 134, 42, 143, hx('#ececec'), hx('#9a9a9a')); c.line([(26, 136), (36, 135)], hx('#ffffff'))
    # abajo: cuadernos y bolsa rosa
    for i, col in enumerate(('#7fb04a', '#f4efe2', '#e8e0f4', '#f4efe2')):
        c.rect(14, 176 - i * 4, 34, 179 - i * 4, hx(col), hx('#8a8070'))
    c.rect(5, 150, 13, 181, hx('#8e7bd0'), hx('#5d4c9a')); c.ell(18, 148, 40, 160, hx('#f3b6c4'), hx('#c97d96'))

def glass_blocks(c):
    gx = 298
    for row in range(14):
        yy = 18 + row * 9
        xs = gx + max(0, (5 - row)) * 9 if row < 5 else gx
        for xx in range(xs, 360, 10):
            c.rect(xx, yy, xx + 9, yy + 8, hx('#c9c2b6'))
            c.rect(xx + 1, yy + 1, xx + 8, yy + 7, hx('#efe7dc'))
            c.poly([(xx + 1, yy + 7), (xx + 8, yy + 1), (xx + 8, yy + 7)], hx('#e3d8ca'))
            c.line([(xx + 2, yy + 5), (xx + 5, yy + 2)], hx('#ffffff'))
            c.noise(xx + 1, yy + 1, xx + 8, yy + 7, [hx('#f8f2ea'), hx('#d9cfc1')], 0.15)
    c.ao(296, 18, 298, 138, 40)

def chandelier(c):
    IRON = hx('#1f1f1f')
    c.line([(332, 0), (332, 18)], IRON)
    c.line([(312, 26), (318, 20), (326, 22), (332, 18), (338, 22), (346, 20), (352, 26)], IRON)
    c.ell(328, 20, 336, 28, None, IRON)
    for cx in (312, 322, 332, 342, 352):
        cy = 26 if cx in (312, 352) else 30
        c.poly([(cx - 4, cy), (cx + 4, cy), (cx + 3, cy + 7), (cx - 3, cy + 7)], hx('#f8f4ea'), hx('#a59c8a'))
        c.line([(cx - 2, cy + 1), (cx - 1, cy + 5)], hx('#ffffff'))
    if SEASON == 'halloween':
        c.line([(332, 37), (332, 44)], IRON)
        c.ell(325, 42, 339, 50, None, IRON)
        for x in range(326, 339, 2): c.line([(x, 46), (x, 62)], IRON)
        c.ell(328, 50, 336, 57, hx('#fbfbfb')); c.rect(328, 54, 336, 60, hx('#fbfbfb'))
        c.rect(330, 53, 330, 53, hx('#333333')); c.rect(333, 53, 333, 53, hx('#333333'))
        c.rect(324, 61, 340, 62, IRON)

def his_desk(c):
    c.ao(56, 131, 222, 178, 55)
    TOP, TOP_L, EDGE, LEG = hx('#d9c39c'), hx('#ecdcbc'), hx('#b39a72'), hx('#1f1f1f')
    c.rect(56, 123, 220, 127, TOP); c.line([(56, 123), (220, 123)], TOP_L); c.rect(56, 128, 220, 130, EDGE)
    c.noise(56, 123, 220, 127, [hx('#d1b990'), hx('#e2cda8')], 0.25)
    # marco negro de escritorio elevable
    c.rect(66, 131, 69, 176, LEG); c.rect(58, 174, 78, 177, LEG)
    c.rect(170, 131, 173, 176, LEG); c.line([(66, 131), (66, 176)], hx('#3a3a3a'))
    # repisa de madera con Mac mini y libros
    c.rect(98, 112, 158, 114, hx('#c9a978')); c.rect(98, 115, 100, 122, hx('#b39a72')); c.rect(156, 115, 158, 122, hx('#b39a72'))
    c.rect(102, 107, 118, 111, hx('#d9dadc'), hx('#9a9ca0')); c.line([(103, 108), (116, 108)], hx('#f2f3f4'))
    for i, col in enumerate(('#1f1f1f', '#e9c46a', '#1f1f1f', '#c0392b')): c.rect(122, 108 - i * 2, 146, 109 - i * 2, hx(col))
    for i, col in enumerate(('#e9c46a', '#c0392b', '#f4efe2')): c.rect(148 + i * 3, 96, 150 + i * 3, 111, hx(col))
    # monitores: izquierdo ancho y derecho más alto
    c.rect(62, 82, 110, 108, hx('#141414')); c.rect(64, 84, 108, 106, hx('#dfe9f5'))
    c.rect(64, 84, 84, 106, hx('#5b8fd6')); c.rect(86, 84, 108, 106, hx('#1f2530'))
    for yy in range(87, 104, 3): c.line([(88, yy), (88 + (yy * 7) % 16, yy)], hx('#8aa0c0'))
    for yy in range(88, 104, 4): c.line([(66, yy), (80, yy)], hx('#ffffff'))
    c.rect(112, 74, 152, 100, hx('#141414')); c.rect(114, 76, 150, 98, hx('#fbfbfb'))
    for yy in range(79, 96, 3): c.line([(116, yy), (128, yy)], hx('#9aa0a8'))
    for yy in (79, 86, 93): c.rect(134, yy, 147, yy + 5, hx('#e8d9b8')); c.rect(136, yy + 1, 140, yy + 4, hx('#5e7a35'))
    c.rect(84, 108, 87, 112, hx('#1f1f1f')); c.rect(130, 100, 133, 106, hx('#1f1f1f'))
    # teclado, mousepad, libreta, jaulita
    c.rect(72, 118, 112, 122, hx('#262626'))
    for kx in range(74, 111, 3): c.line([(kx, 119), (kx + 1, 119)], hx('#4a4a4a')); c.line([(kx, 121), (kx + 1, 121)], hx('#4a4a4a'))
    c.ell(114, 117, 132, 123, hx('#5f8f9a'), hx('#3f6a72')); c.ell(121, 118, 126, 121, hx('#2b2b2b'))
    c.poly([(134, 122), (140, 115), (156, 116), (152, 123)], hx('#fbfbfb'), hx('#9a9ca0')); c.line([(142, 118), (150, 119)], hx('#8aa0c0'))
    # bolsa de regalo azul
    c.rect(200, 96, 216, 122, hx('#22397a'), hx('#14224a')); c.line([(202, 98), (202, 120)], hx('#3d5aa8'))
    c.arc = None
    c.line([(204, 96), (206, 90), (210, 90), (212, 96)], hx('#c0392b'))
    # cajonera de plástico con stickers
    c.rect(176, 131, 208, 172, hx('#e8ecef'), hx('#8a96a0'))
    r = random.Random(12)
    for i, yy in enumerate((134, 147, 160)):
        c.rect(179, yy, 205, yy + 11, hx('#f4f6f8'), hx('#a3aeb6')); c.line([(188, yy + 11), (196, yy + 11)], hx('#7b8790'))
        for _ in range(4):
            sx, sy = r.randint(181, 200), r.randint(yy + 2, yy + 7); col = hx(r.choice(['#e74c3c', '#3498db', '#f1c40f', '#2ecc71', '#9b59b6', '#e67e22']))
            if r.random() < .5: c.ell(sx, sy, sx + 4, sy + 4, col)
            else: c.rect(sx, sy, sx + 5, sy + 2, col)

def fer_desk(c):
    c.ao(270, 157, 360, 196, 50)
    # carrito rosa a la izquierda
    c.rect(258, 132, 276, 200, hx('#f6d3db'), hx('#c48d9b'))
    for yy in (132, 150, 168, 186): c.rect(258, yy, 276, yy + 3, hx('#efb9c6'))
    c.ell(260, 128, 268, 134, hx('#efb9c6'), hx('#c48d9b')); c.ell(268, 128, 276, 134, hx('#efb9c6'), hx('#c48d9b'))
    for wx in (260, 274): c.ell(wx - 2, 199, wx + 2, 203, hx('#4a4a4a'))
    # escritorio blanco
    c.rect(272, 149, 359, 154, hx('#fbfbfb')); c.line([(272, 149), (359, 149)], hx('#ffffff')); c.rect(272, 155, 359, 157, hx('#c9c9c9'))
    c.rect(282, 158, 285, 209, hx('#d9d9d9')); c.line([(282, 158), (282, 209)], hx('#efefef'))
    c.poly([(276, 148), (300, 144), (306, 148), (282, 152)], hx('#7a4e8a'), hx('#4e2f5a'))       # laptop con stickers
    for sx, col in ((284, '#f1c40f'), (290, '#e74c3c'), (296, '#2ecc71')): c.ell(sx, 147, sx + 3, 149, hx(col))
    c.rect(282, 134, 292, 146, hx('#f3b6c4'), hx('#c97d96'))                                    # portalápices
    for i, col in enumerate(('#e74c3c', '#3498db', '#2ecc71', '#f1c40f')): c.line([(283 + i * 3, 126), (284 + i * 2, 134)], hx(col))
    c.poly([(318, 148), (330, 128), (346, 128), (338, 148)], hx('#ececec'), hx('#a0a0a0'))      # base de laptop
    c.rect(326, 142, 352, 148, hx('#f6b8cc'), hx('#c97d96'))                                    # teclado rosa
    for kx in range(328, 351, 3): c.line([(kx, 144), (kx + 1, 144)], hx('#fde3eb')); c.line([(kx, 146), (kx + 1, 146)], hx('#fde3eb'))
    c.ell(302, 139, 324, 149, hx('#f6c1cc'), hx('#c48d9b'))                     # puerquito de peluche
    c.ell(318, 136, 328, 146, hx('#f6c1cc'), hx('#c48d9b')); c.ell(324, 140, 329, 144, hx('#ee9fb0'), hx('#c48d9b'))
    c.point_ = None; c.rect(326, 141, 326, 142, hx('#a05a6a')); c.rect(321, 139, 321, 139, hx('#4a2a30'))
    c.poly([(318, 137), (319, 133), (322, 136)], hx('#ee9fb0')); c.line([(302, 143), (299, 141), (300, 139)], hx('#c48d9b'))
    for i, col in enumerate(('#f6d3db', '#e8e0f4', '#d8ecf5', '#f6e3c4')): c.rect(342 + i * 4, 136, 345 + i * 4, 142, hx(col), hx('#a0a0a0'))
    c.rect(352, 138, 359, 148, hx('#d2342b'), hx('#8f1f19'))

def chairs(c):
    c.shadow(56, 182, 112, 190, 70)
    BLK, BLK_L, BRN = hx('#262626'), hx('#3d3d3d'), hx('#6e6252')
    c.poly([(68, 96), (102, 96), (106, 104), (106, 150), (64, 150), (64, 104)], BLK)
    c.line([(66, 100), (66, 148)], BLK_L); c.line([(70, 96), (100, 96)], BLK_L)
    c.poly([(74, 104), (96, 104), (98, 128), (72, 128)], BRN); c.line([(74, 104), (96, 104)], hx('#8a7d6a'))
    c.rect(78, 132, 94, 140, BRN)
    c.rect(60, 148, 110, 158, BLK); c.line([(60, 148), (110, 148)], BLK_L)
    c.rect(83, 158, 87, 178, hx('#1a1a1a'))
    c.line([(66, 182), (104, 182)], hx('#1a1a1a'), 3 if c.k == 1 else 5)
    for wx in (64, 84, 104): c.ell(wx - 2, 181, wx + 2, 186, hx('#111111'))
    # silla rosa con cojín y marco blanco
    c.shadow(290, 200, 346, 209, 60)
    c.poly([(298, 158), (336, 158), (340, 206), (294, 206)], hx('#efc9d2'), hx('#9a8a8f'))
    for yy in range(162, 204, 3): c.line([(300, yy), (336, yy)], hx('#e3aebd'))
    c.rounded = None
    c.rect(300, 176, 334, 190, hx('#f6dce2'), hx('#c4a0aa')); c.line([(302, 178), (332, 178)], hx('#fff0f3'))
    c.line([(294, 160), (292, 206)], hx('#f4f4f4'), 2); c.line([(338, 160), (342, 206)], hx('#f4f4f4'), 2)
    c.rect(304, 150, 330, 160, hx('#f7f7f7'), hx('#9a8a8f')); c.line([(306, 152), (328, 152)], hx('#ffffff'))

def plant_shadows(c):
    c.shadow(226, 184, 276, 193, 85)    # Dieffenbachia (P09) en el piso
    c.shadow(158, 127, 200, 132, 70)    # frasco (P13) sobre el escritorio

def lighting(img, k):
    a = np.asarray(img).astype(np.float32)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lx, ly = 180 * k, 2 * k
    d2 = ((xx - lx) / (210 * k)) ** 2 + ((yy - ly) / (170 * k)) ** 2
    L = 0.88 + 0.20 * np.exp(-d2 * 1.6)
    # brillo cálido del monitor ámbar en la pared
    m2 = ((xx - 138 * k) / (40 * k)) ** 2 + ((yy - 100 * k) / (30 * k)) ** 2
    warm = 0.10 * np.exp(-m2 * 2.0)
    # bandas con trama Bayer (look retro)
    steps = 12 if k == 1 else 20
    by = BAYER[(yy.astype(int)) % 4, (xx.astype(int)) % 4]
    Lq = np.floor(L * steps + by) / steps
    Wq = np.floor(warm * steps * 2 + by) / (steps * 2)
    rgb = a[..., :3] * Lq[..., None]
    rgb[..., 0] *= 1.03; rgb[..., 2] *= 0.96
    rgb[..., 0] += 255 * Wq * 0.9; rgb[..., 1] += 255 * Wq * 0.6; rgb[..., 2] += 255 * Wq * 0.15
    out = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([out, a[..., 3].astype(np.uint8)]), 'RGBA')

def background(k):
    c = C(k)
    wall_and_floor(c); painting(c); glass_blocks(c); chandelier(c)
    his_desk(c); bookshelf(c); fer_desk(c); plant_shadows(c)
    img = lighting(c.im, k)
    c.im = img; c.d = ImageDraw.Draw(img)
    chairs(c)        # las sillas van delante; se iluminan aparte (ya tienen su tono)
    return c.im

def compose(k, moods=None):
    S = str(ROOT / 'public' / 'sprites') + '/'
    moods = moods or {}
    bg = background(k)
    for pid, (x, y) in (('P13', (146, 38)), ('P09', (206, 97))):
        sp = Image.open(f'{S}{pid}_{moods.get(pid, "feliz")}.png').convert('RGBA')
        if k == 2: sp = sp.resize((160, 192), Image.NEAREST)
        bg.alpha_composite(sp, (x * k, y * k))
    return bg

if __name__ == '__main__':
    out = os.environ.get('OUT', '.') + '/'
    a = compose(1).resize((720, 420), Image.NEAREST)   # actual pulida, vista a ×2
    SEASON = 'halloween'; compose(1).resize((720, 420), Image.NEAREST).save(out + 'estudio_halloween.png'); SEASON = None
    b = compose(2)                                      # doble resolución, vista a ×1
    a.save(out + 'estudio_A.png'); b.save(out + 'estudio_B.png')
    sheet = Image.new('RGBA', (720, 420 * 2 + 16), (42, 47, 43, 255))
    sheet.alpha_composite(a, (0, 0)); sheet.alpha_composite(b, (0, 436)); sheet.save(out + 'check.png')
    box = (300, 160, 560, 400)   # acercamiento: escritorio, frasco y Dieffenbachia
    za = a.crop(box).resize((520, 480), Image.NEAREST); zb = b.crop(box).resize((520, 480), Image.NEAREST)
    z = Image.new('RGBA', (1056, 480), (42, 47, 43, 255)); z.alpha_composite(za, (0, 0)); z.alpha_composite(zb, (536, 0)); z.save(out + 'zoom.png')
