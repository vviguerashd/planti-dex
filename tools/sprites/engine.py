# Plantitas: motor de sprites 16-bit (64x96 nativo)
import math, random
from PIL import Image, ImageDraw

W, H = 64, 96
GROUND = 90
STATES = ["feliz", "con_sed", "sedienta", "enferma"]

def hexc(h, a=255):
    h = h.lstrip("#"); return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), a)

def mix(c1, c2, t):
    return tuple(int(round(c1[i]*(1-t)+c2[i]*t)) for i in range(3)) + (255,)

def new():
    return Image.new("RGBA", (W, H), (0,0,0,0))

def outline(layer, color):
    src = layer.load(); out = layer.copy(); o = out.load()
    for y in range(H):
        for x in range(W):
            if src[x,y][3] == 0:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny = x+dx,y+dy
                    if 0<=nx<W and 0<=ny<H and src[nx,ny][3] > 0:
                        o[x,y] = color; break
    return out

def paste(base, layer):
    base.alpha_composite(layer); return base

def px(img, x, y, c):
    if 0 <= x < W and 0 <= y < H: img.putpixel((int(x),int(y)), c)

# ---------- curvas ----------
def curve(x, y, ang, length, droop, steps=14):
    """Punto a punto; ang en grados (0=derecha, -90=arriba). droop=gravedad."""
    pts = []; dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    seg = length/steps
    for i in range(steps+1):
        pts.append((x, y, dx, dy))
        x += dx*seg; y += dy*seg
        dy += droop*0.12
        n = math.hypot(dx,dy); dx/=n; dy/=n
    return pts

def strap_poly(pts, width, taper="dracaena"):
    left=[]; right=[]; n=len(pts)-1
    for i,(x,y,dx,dy) in enumerate(pts):
        t=i/n
        if taper=="dracaena": w = width*(0.55+0.45*math.sin(math.pi*min(1,t*1.15)))*(1-t**3)
        else: w = width*math.sin(math.pi*t)
        nx, ny = -dy, dx
        left.append((x+nx*w/2, y+ny*w/2)); right.append((x-nx*w/2, y-ny*w/2))
    return left + right[::-1]

# ---------- hojas ----------
def leaf_poly(x, y, ang, L, Wd, shape="heart"):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    if shape == "heart":
        loc = [(0,0),(L*0.12,-Wd*0.42),(L*0.4,-Wd*0.52),(L*0.75,-Wd*0.3),(L,0),(L*0.75,Wd*0.3),(L*0.4,Wd*0.52),(L*0.12,Wd*0.42)]
    else:  # ellipse-ish (citrus)
        loc = [(0,0),(L*0.25,-Wd*0.45),(L*0.6,-Wd*0.5),(L*0.9,-Wd*0.25),(L,0),(L*0.9,Wd*0.25),(L*0.6,Wd*0.5),(L*0.25,Wd*0.45)]
    return [(x+px_*ca-py_*sa, y+px_*sa+py_*ca) for px_,py_ in loc]

def draw_leaf(target, poly, pal, rng, variegate=0.0, spots=0.0, outline_c=None, rib=True, ang=0, base=None, L=0, blotch=False):
    lay = new(); d = ImageDraw.Draw(lay)
    d.polygon(poly, fill=pal["mid"])
    # luz arriba-izquierda: banda clara en la mitad superior
    cx = sum(p[0] for p in poly)/len(poly); cy = sum(p[1] for p in poly)/len(poly)
    hl = [(cx+(p[0]-cx)*0.62-0.8, cy+(p[1]-cy)*0.62-0.9) for p in poly]
    d.polygon(hl, fill=pal["light"])
    sh = [(cx+(p[0]-cx)*0.5+1.2, cy+(p[1]-cy)*0.5+1.2) for p in poly]
    mask = new(); ImageDraw.Draw(mask).polygon(poly, fill=(255,255,255,255))
    m = mask.load(); l = lay.load()
    # sombra inferior derecha
    shl = new(); ImageDraw.Draw(shl).polygon(sh, fill=pal["dark"]); s = shl.load()
    for yy in range(H):
        for xx in range(W):
            if m[xx,yy][3] and s[xx,yy][3] and l[xx,yy][:3]==pal["mid"][:3]:
                l[xx,yy] = pal["dark"]
    if rib and base is not None:
        bx,by = base; a=math.radians(ang)
        for k in range(1, int(L*0.75)):
            xx,yy = int(round(bx+math.cos(a)*k)), int(round(by+math.sin(a)*k))
            if 0<=xx<W and 0<=yy<H and m[xx,yy][3]: l[xx,yy] = pal["rib"]
    # puntos de luz
    hi = 0
    for yy in range(H):
        for xx in range(W):
            if not m[xx,yy][3]: continue
            if variegate and rng.random() < variegate: l[xx,yy] = pal["var"] if rng.random()<0.7 else pal["var2"]
            if spots and rng.random() < spots: l[xx,yy] = pal["spot"]
            if l[xx,yy][:3]==pal["light"][:3] and hi < 1 and rng.random()<0.08:
                l[xx,yy] = pal["hi"]; hi += 1
    if blotch:
        bx = int(round(cx+rng.uniform(-1,1))); by = int(round(cy+rng.uniform(-1,1)))
        for ox,oy in [(-1,-1),(0,-1),(1,-1),(2,-1),(-1,0),(2,0),(-1,1),(2,1),(-1,2),(0,2),(1,2),(2,2)]:
            xx,yy=bx+ox,by+oy
            if 0<=xx<W and 0<=yy<H and m[xx,yy][3]: l[xx,yy]=hexc("#C9B54A")
        for ox,oy in [(0,0),(1,0),(0,1),(1,1)]:
            xx,yy=bx+ox,by+oy
            if 0<=xx<W and 0<=yy<H and m[xx,yy][3]: l[xx,yy]=hexc("#6B4423")
    for yy in range(H):
        for xx in range(W):
            if not m[xx,yy][3]: l[xx,yy] = (0,0,0,0)
    lay = outline(lay, outline_c or pal["out"])
    target.alpha_composite(lay)

# ---------- paletas de hoja por estado ----------
def leaf_palette(base, state, kind="green"):
    yellow = hexc("#D9C35A"); brown = hexc("#8A5A2B")
    t = {"feliz":0.0, "con_sed":0.18, "sedienta":0.48, "enferma":0.12}[state]
    p = {k: mix(v, yellow, t) for k,v in base.items()}
    if state == "sedienta":
        p["dark"] = mix(base["dark"], brown, 0.45)
    p["out"] = mix(p["dark"], hexc("#10180F"), 0.55)
    p["spot"] = hexc("#6B4423")
    return p

# ---------- cara ----------
EYE = hexc("#1C1714"); WHITE = hexc("#FFFFFF"); BLUSH = hexc("#F29A9A")
TEAR = hexc("#7CC8F4"); TEAR_D = hexc("#3C86CF")

def face(img, cx, cy, state, blush=True):
    ex1, ex2 = cx-4, cx+3
    if state == "feliz":
        for ex in (ex1, ex2):
            for dy in range(3): px(img, ex, cy+dy, EYE); px(img, ex+1, cy+dy, EYE)
            px(img, ex, cy, WHITE)
        for x,y in [(cx-2,cy+4),(cx-1,cy+5),(cx,cy+5),(cx+1,cy+4)]: px(img,x,y,EYE)
        if blush:
            for ex in (ex1-2, ex2+2): px(img, ex, cy+3, BLUSH); px(img, ex+1, cy+3, BLUSH)
    elif state == "con_sed":
        for ex in (ex1, ex2):
            px(img, ex, cy+1, EYE); px(img, ex+1, cy+1, EYE); px(img, ex, cy+2, EYE); px(img, ex+1, cy+2, EYE)
            px(img, ex, cy+1, WHITE)
        # cejas preocupadas
        px(img, ex1-1, cy-1, EYE); px(img, ex1, cy-1, EYE)
        px(img, ex2+1, cy-1, EYE); px(img, ex2+2, cy-1, EYE)
        for x in range(cx-1, cx+1): px(img, x, cy+5, EYE)
        if blush:
            for ex in (ex1-2, ex2+2): px(img, ex, cy+3, BLUSH)
    elif state == "sedienta":
        # ojos cerrados tristes ^ invertido
        for ex in (ex1, ex2):
            px(img, ex-1, cy+2, EYE); px(img, ex, cy+1, EYE); px(img, ex+1, cy+1, EYE); px(img, ex+2, cy+2, EYE)
        # lagrima
        px(img, ex1, cy+3, TEAR); px(img, ex1, cy+4, TEAR_D)
        # boca triste
        for x,y in [(cx-2,cy+6),(cx-1,cy+5),(cx,cy+5),(cx+1,cy+6)]: px(img,x,y,EYE)
    elif state == "enferma":
        # ojos entrecerrados
        for ex in (ex1, ex2):
            px(img, ex-1, cy+1, EYE); px(img, ex, cy+1, EYE); px(img, ex+1, cy+1, EYE)
            px(img, ex, cy+2, EYE)
        # boca de malestar
        for x,y in [(cx-2,cy+5),(cx-1,cy+5),(cx,cy+5),(cx+1,cy+6)]: px(img,x,y,EYE)
        for ex in (ex1-2, ex2+2): px(img, ex, cy+3, hexc("#A8C98A"))

def drop(img, x, y, c1=TEAR, c2=TEAR_D):
    pts = [(1,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2),(1,3)]
    for dx,dy in pts: px(img, x+dx, y+dy, c1)
    px(img, x+2, y+2, c2); px(img, x+1, y+3, c2); px(img, x, y+1, WHITE)

def bubble(img, x, y, alert=False):
    """globito de pensamiento con gota (y signo de alerta)"""
    BW = hexc("#FFFFFF"); BO = hexc("#2B2B2B")
    w, h = 13, 11
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x+w-1, y+h-1], radius=3, fill=BW, outline=BO)
    px(img, x+2, y+h+1, BW); px(img, x+1, y+h+2, BO)
    px(img, x+2, y+h, BW)
    big = [(2,0),(1,1),(2,1),(3,1),(0,2),(1,2),(2,2),(3,2),(4,2),(0,3),(1,3),(2,3),(3,3),(4,3),(1,4),(2,4),(3,4)]
    ox = x+2 if alert else x+4
    for dx,dy in big: px(img, ox+dx, y+3+dy, TEAR)
    for dx,dy in [(3,3),(4,3),(3,4),(2,4)]: px(img, ox+dx, y+3+dy, TEAR_D)
    px(img, ox+1, y+5, WHITE)
    if alert:
        R = hexc("#E0393E")
        for dy in range(3): px(img, x+9, y+2+dy, R); px(img, x+10, y+2+dy, R)
        px(img, x+9, y+7, R); px(img, x+10, y+7, R)

def shadow(img, cx, w):
    d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", (W,H), (0,0,0,0))
    ImageDraw.Draw(sh).ellipse([cx-w//2, GROUND-2, cx+w//2, GROUND+2], fill=(30,30,30,70))
    img.alpha_composite(sh)

def upscale(img, k=4):
    return img.resize((W*k, H*k), Image.NEAREST)
