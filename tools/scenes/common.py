import random
from PIL import Image, ImageDraw
from gala import hx
import pathlib; S=str(pathlib.Path(__file__).resolve().parents[2]/'public'/'sprites')+'/'
def sp(i,m): return Image.open(f'{S}{i}_{m}.png').convert('RGBA')
def wall(d,box,r,base='#f1eee6',dots=('#e4e0d6','#f8f6f0'),n=None):
    d.rectangle(box,fill=hx(base))
    n=n or (box[2]-box[0])*(box[3]-box[1])//18
    for _ in range(n): d.point((r.randint(box[0],box[2]),r.randint(box[1],box[3])),fill=hx(r.choice(dots)))
def terracotta(im,y0,r):
    d=ImageDraw.Draw(im); W,H=im.size
    d.rectangle([0,y0,W,H],fill=hx('#9e4426'))
    for _ in range((H-y0)*W//6): d.point((r.randrange(W),r.randrange(y0,H)),fill=hx(r.choice(['#8f3b20','#ad5232','#a9492a','#b75c3a'])))
    rows=[]; y=y0; h=10
    while y<H: rows.append(y); y+=h; h+=5
    for y in rows[1:]: d.line([(0,y),(W,y)],fill=hx('#6e2c16'))
    cx=W/2
    for i in range(-30,31):
        top=cx+i*30; bot=cx+i*30*1.9
        d.line([(top,y0),(bot,H)],fill=hx('#6e2c16'))
    # estrellas blancas en las esquinas
    for j,y in enumerate(rows[1:]):
        t=(y-y0)/(H-y0); s=int(3+t*4)
        for i in range(-30,31):
            x=cx+i*30*(1+0.9*t)
            if 0<=x<W:
                d.polygon([(x,y-s),(x+s*0.35,y),(x,y+s),(x-s*0.35,y)],fill=hx('#f2efe8'))
                d.polygon([(x-s,y),(x,y-s*0.35),(x+s,y),(x,y+s*0.35)],fill=hx('#f2efe8'))
                d.point((x,y),fill=hx('#3a4f8a'))
def zz(d,x,y,col='#4a554c'):
    for (dx,dy,s) in ((0,8,4),(8,0,5)): d.line([(x+dx,y+dy),(x+dx+s,y+dy),(x+dx,y+dy+s),(x+dx+s,y+dy+s)],fill=hx(col))
