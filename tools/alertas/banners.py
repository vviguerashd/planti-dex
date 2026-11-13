# Banners pixel para los correos de alerta (200x70 nativo, se guardan a x3 = 600x210).
# Uso: python3 tools/alertas/banners.py
import math, random, pathlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parents[2]
SP = ROOT / 'public' / 'sprites'; OUT = ROOT / 'public' / 'alertas'
W, H, K = 200, 70, 3

FONT = {  # 5x7
 'A':["01110","10001","10001","11111","10001","10001","10001"], 'B':["11110","10001","10001","11110","10001","10001","11110"],
 'D':["11110","10001","10001","10001","10001","10001","11110"], 'E':["11111","10000","10000","11110","10000","10000","11111"],
 'G':["01111","10000","10000","10111","10001","10001","01111"], 'H':["10001","10001","10001","11111","10001","10001","10001"],
 'I':["11111","00100","00100","00100","00100","00100","11111"], 'L':["10000","10000","10000","10000","10000","10000","11111"],
 'M':["10001","11011","10101","10101","10001","10001","10001"], 'N':["10001","11001","10101","10011","10001","10001","10001"],
 'O':["01110","10001","10001","10001","10001","10001","01110"], 'P':["11110","10001","10001","11110","10000","10000","10000"],
 'R':["11110","10001","10001","11110","10100","10010","10001"], 'T':["11111","00100","00100","00100","00100","00100","00100"],
 'U':["10001","10001","10001","10001","10001","10001","01110"], 'Z':["11111","00001","00010","00100","01000","10000","11111"],
 '!':["00100","00100","00100","00100","00100","00000","00100"], '¡':["00100","00000","00100","00100","00100","00100","00100"],
 ' ':["00000"]*7,
}
def text(d, s, x, y, col, sh, sc=2):
    for ox, oy, c in ((1, 1, sh), (0, 0, col)):
        cx = x
        for ch in s:
            g = FONT[ch]
            for j, row in enumerate(g):
                for i, b in enumerate(row):
                    if b == '1': d.rectangle([cx + (i + ox) * sc, y + (j + oy) * sc, cx + (i + ox) * sc + sc - 1, y + (j + oy) * sc + sc - 1], fill=c)
            cx += 6 * sc
def twidth(s, sc=2): return len(s) * 6 * sc - sc

def sprite(pid, mood='feliz', tint=None):
    im = Image.open(SP / f'{pid}_{mood}.png').convert('RGBA')
    if tint:
        r, g, b, a = im.split(); ov = Image.new('RGBA', im.size, tint + (0,)); ov.putalpha(a.point(lambda v: 70 if v else 0)); im.alpha_composite(ov)
    return im

def helada():
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im); r = random.Random(3)
    for y in range(H): d.line([(0, y), (W, y)], fill=(18 + y // 3, 28 + y // 3, 70 + y // 2, 255))
    for _ in range(40): x, y = r.randrange(W), r.randrange(H - 20); d.point((x, y), fill=(230, 236, 255, 255))
    d.ellipse([168, 6, 184, 22], fill=(244, 240, 214, 255)); d.ellipse([174, 4, 190, 20], fill=(30, 40, 92, 255))
    d.rectangle([0, H - 12, W, H], fill=(214, 228, 240, 255))
    for x in range(0, W, 3): d.point((x, H - 12 + (x * 7) % 5), fill=(255, 255, 255, 255))
    for i, pid in enumerate(('P04', 'P18', 'P24')):
        s = sprite(pid, 'feliz', (120, 170, 255)).resize((40, 48), Image.NEAREST); im.alpha_composite(s, (4 + i * 34, H - 50))
    for _ in range(26):   # copos
        x, y = r.randrange(0, 110), r.randrange(2, H - 14)
        d.point([(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], fill=(255, 255, 255, 255))
    text(d, '¡HELADA!', W - twidth('¡HELADA!') - 6, 34, (236, 246, 255, 255), (30, 60, 140, 255))
    # termómetro bajito
    d.rectangle([150, 6, 153, 22], fill=(255, 255, 255, 255), outline=(40, 50, 90, 255)); d.ellipse([148, 20, 156, 28], fill=(80, 150, 255, 255), outline=(40, 50, 90, 255)); d.rectangle([151, 16, 152, 22], fill=(80, 150, 255, 255))
    return im

def tormenta(hail):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im); r = random.Random(5)
    for y in range(H): d.line([(0, y), (W, y)], fill=(70 + y // 2, 76 + y // 2, 92 + y // 2, 255))
    for cx, cy, rr in ((30, 8, 18), (60, 4, 22), (95, 10, 18), (140, 6, 24), (180, 10, 20)):
        d.ellipse([cx - rr, cy - rr // 2, cx + rr, cy + rr // 2 + 6], fill=(54, 58, 72, 255))
    d.polygon([(124, 10), (118, 21), (123, 21), (119, 31), (130, 18), (125, 18), (129, 10)], fill=(255, 226, 80, 255))
    d.rectangle([0, H - 12, W, H], fill=(96, 120, 70, 255))
    for i, pid in enumerate(('P04', 'P18', 'P24')):
        s = sprite(pid, 'feliz').resize((40, 48), Image.NEAREST); im.alpha_composite(s, (4 + i * 34, H - 50))
    for _ in range(40 if hail else 60):
        x, y = r.randrange(0, W), r.randrange(16, H - 12)
        if hail: d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(240, 244, 250, 255))
        else: d.line([(x, y), (x - 1, y + 3)], fill=(170, 200, 240, 255))
    word = '¡GRANIZO!' if hail else 'TORMENTA'
    text(d, word, W - twidth(word) - 6, 34, (255, 236, 120, 255), (40, 40, 50, 255))
    return im

def prueba():
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(150 + y // 2, 205 + y // 4, 240, 255))
    d.ellipse([168, 6, 190, 28], fill=(255, 214, 80, 255))
    d.rectangle([0, H - 12, W, H], fill=(110, 170, 80, 255))
    for i, pid in enumerate(('P04', 'P18', 'P24')):
        s = sprite(pid, 'feliz').resize((40, 48), Image.NEAREST); im.alpha_composite(s, (4 + i * 34, H - 50))
    text(d, 'PRUEBA', W - twidth('PRUEBA') - 6, 34, (255, 255, 255, 255), (40, 100, 60, 255))
    return im

OUT.mkdir(parents=True, exist_ok=True)
for name, img in (('helada', helada()), ('tormenta', tormenta(False)), ('granizo', tormenta(True)), ('prueba', prueba())):
    img.convert('RGB').resize((W * K, H * K), Image.NEAREST).save(OUT / f'{name}.png', optimize=True)
print('ok')
