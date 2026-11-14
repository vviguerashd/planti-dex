import sys, math, random, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'/'scenes2')); sys.path.insert(0, str(ROOT/'tools'/'scenes'))
from PIL import Image, ImageDraw
from gala import hx, gala_stalk, gala_sleep
from estudio2 import C
from jardin2 import light
FL = 150
SEASON = None
POS = {'L1': (30, 62), 'L2': (112, 86)}
HOTSPOTS = {'L1': (78, 138), 'L2': (106, 112)}
def scene(k=1):
    c = C(k); r = random.Random(4)
    c.rect(0,0,359,FL,hx('#e6dfd2')); c.noise(0,0,359,FL,[hx('#d8d0c0'),hx('#f1ebe0'),hx('#cfc6b4')],0.35)
    for _ in range(900):
        x,y=r.randint(0,359),r.randint(0,FL); c.rect(x,y,x,y,hx('#f6f1e8')); c.rect(x,y+1,x,y+1,hx('#bdb3a2'))
    c.rect(0,FL,359,209,hx('#b9b4aa')); c.noise(0,FL,359,209,[hx('#a9a399'),hx('#c9c4ba')],0.35)
    for y in (FL,168,190): c.line([(0,y),(359,y)],hx('#8f8a80'))
    for x in range(0,360,40): c.line([(x,FL),(x-10,209)],hx('#8f8a80'))
    # ropero de resina (herramientas)
    c.shadow(214,196,346,206,70)
    c.poly([(220,40),(340,32),(342,44),(218,48)],hx('#6f7378'))
    c.rect(222,46,338,198,hx('#e9e1d2'),hx('#a79c88'))
    c.line([(280,48),(280,198)],hx('#a79c88'),2)
    for x0 in (226,284):
        for y in range(54,90,5): c.line([(x0+4,y),(x0+48,y)],hx('#d3c8b4'))
        c.rect(x0+2,94,x0+50,194,None,hx('#cfc3ae'))
        c.line([(x0+6,190),(x0+44,100)] if x0==226 else [(x0+46,190),(x0+8,100)],hx('#d6cbb6'),2)
    c.ell(274,118,286,136,hx('#5a5e63')); c.rect(222,196,338,199,hx('#6f7378'))
    # depósito 1: dos cubetas apiladas con tapete
    c.shadow(28,198,102,206,70)
    for y0,y1 in ((128,198),(66,128)):
        c.poly([(30,y0),(100,y0),(96,y1),(34,y1)][::1],hx('#f4f4f2'),hx('#a9adb0'))
        c.line([(30,y0+5),(100,y0+5)],hx('#d9dcde')); c.line([(31,y0+9),(99,y0+9)],hx('#d9dcde'))
        c.line([(36,y0+12),(36,y1-2)],hx('#ffffff'))
    c.d.arc([30*k,72*k,100*k,112*k],20,160,fill=hx('#8a8e92'),width=k)
    c.rect(56,108,72,111,hx('#2a2a2a'))
    c.poly([(22,62),(108,62),(112,70),(18,70)],hx('#c9922f'),hx('#8a5f1a'))
    c.noise(18,62,112,70,[hx('#b5801f'),hx('#ddb04a')],0.5)
    # depósito 2: talavera de girasoles en base de fierro
    c.shadow(118,198,208,206,70)
    IRON=hx('#1c1d1d')
    for x0,x1 in ((128,122),(198,204)):
        c.line([(x0,150),(x1,196)],IRON,2); c.d.arc([(x1-6)*k,190*k,(x1+2)*k,198*k],90,300,fill=IRON,width=k)
    c.line([(163,160),(163,196)],IRON,2); c.d.arc([159*k,190*k,167*k,198*k],0,200,fill=IRON,width=k)
    c.ell(120,140,206,154,None,IRON,2)
    c.ell(118,96,208,160,hx('#16244f'),hx('#0b1430'))
    c.rect(124,92,202,100,hx('#16244f'),hx('#0b1430'))
    for cx,cy,rr in ((140,128,13),(178,124,15),(205,128,8),(122,128,7)):
        for a in range(0,360,30):
            x=cx+rr*math.cos(math.radians(a)); y=cy+rr*0.9*math.sin(math.radians(a))
            c.ell(x-4,y-4,x+4,y+4,hx('#f2a12a'),hx('#d0521e'))
        c.ell(cx-rr*0.55,cy-rr*0.5,cx+rr*0.55,cy+rr*0.5,hx('#5a2a14'),hx('#2a120a'))
    for lx,ly in ((158,108),(196,146),(130,150),(160,148)): c.poly([(lx,ly),(lx+6,ly-4),(lx+10,ly+2)],hx('#2f8a4a'))
    c.line([(126,104),(150,100)],hx('#5a72c8'))
    c.poly([(112,86),(214,86),(218,94),(108,94)],hx('#c9922f'),hx('#8a5f1a'))
    c.noise(108,86,218,94,[hx('#b5801f'),hx('#ddb04a')],0.5)
    return light(c.im,k)
def background(k=1): return scene(k)
