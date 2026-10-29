import random
from PIL import Image, ImageDraw
from gala import gala_sleep, gala_stalk, hx
from common import sp, wall, terracotta, zz
W,H=360,210; FL=158
def scene(state):
    r=random.Random(11); im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    wall(d,[0,0,W,FL],r)
    # vista a la sala por la derecha
    d.rectangle([296,0,W,FL],fill=hx('#e6e1d4')); d.rectangle([296,0,300,FL],fill=hx('#d8d2c3'))
    d.rectangle([318,40,360,96],fill=hx('#dfe9f2')); 
    for x in range(320,360,6): d.line([(x,40),(x+2,96)],fill=hx('#c9d4de'))
    d.rounded_rectangle([306,110,360,150],5,fill=hx('#cbb9a0')); d.ellipse([326,102,344,118],fill=hx('#e8833a'))
    for gx,gy in ((330,26),(340,22),(350,28)): d.ellipse([gx,gy,gx+5,gy+5],fill=hx('#fff4c2'))
    # marco de puerta a la izquierda
    d.rectangle([0,0,12,H],fill=hx('#6a3a26')); d.rectangle([12,0,15,H],fill=hx('#4e2a1b'))
    d.rectangle([40,96,48,106],fill=hx('#f7f7f4'),outline=hx('#bdbab2'))   # contacto
    terracotta(im,FL,r); d=ImageDraw.Draw(im)
    # espejo redondo
    d.ellipse([112,8,216,112],fill=hx('#b07a43')); d.ellipse([117,13,211,107],fill=hx('#d9dde0'))
    d.rectangle([140,30,158,107],fill=hx('#6a3a26')); d.rectangle([186,30,200,107],fill=hx('#6a3a26'))
    d.ellipse([117,13,211,107],outline=hx('#8f5f30'),width=2)
    for gx,gy in ((128,40),(196,28),(126,80),(190,84)):     # fantasmitas de papel
        d.ellipse([gx,gy,gx+9,gy+9],fill=hx('#fbfbfb')); d.rectangle([gx,gy+5,gx+9,gy+12],fill=hx('#fbfbfb'))
        d.point([(gx+3,gy+4),(gx+6,gy+4)],fill=hx('#555555'))
    for sx,sy in ((160,24),(176,92),(204,60)): d.point([(sx,sy),(sx-1,sy),(sx+1,sy),(sx,sy-1),(sx,sy+1)],fill=hx('#e2c044'))
    # bufetera de listones
    d.rectangle([62,122,306,128],fill=hx('#f3efe6'),outline=hx('#b9ad97'))
    d.rectangle([66,128,302,184],fill=hx('#e6cfa3'))
    for x in range(68,302,6): d.line([(x,129),(x,183)],fill=hx('#c9ae7d'))
    d.line([(184,129),(184,183)],fill=hx('#8f7650'),width=2); d.line([(130,152),(184,152)],fill=hx('#8f7650'))
    d.rectangle([66,184,302,188],fill=hx('#b99a68'))
    # cosas encima: calabacitas, vasos, platos
    d.ellipse([70,108,88,122],fill=hx('#e8833a'),outline=hx('#9c4e1c')); d.line([(79,104),(79,109)],fill=hx('#5e7a35'),width=2)
    d.ellipse([76,100,86,110],fill=hx('#f0e6d0'),outline=hx('#a99a7a'))
    for gx in (98,106,114): d.rectangle([gx,110,gx+6,122],fill=hx('#dfe7ea'),outline=hx('#9aa6aa'))
    for py in range(114,122,2): d.line([(236,py),(254,py)],fill=hx('#e9ecef')); 
    d.rectangle([236,113,254,122],outline=hx('#9aa6aa'))
    # roomba
    d.ellipse([18,186,56,200],fill=hx('#3a3a3a'),outline=hx('#1a1a1a')); d.ellipse([28,189,46,196],fill=hx('#6d6d6d'))
    if state is None: return im
    # plantas
    m11='con_sed' if state=='sed' else 'feliz'
    for pid,x,m in (('P12',112,'feliz'),('P10',152,'feliz'),('P11',186,m11)):
        p=sp(pid,m); im.alpha_composite(p,(x,123-93))
    if state=='sed':
        g=gala_stalk().transpose(Image.FLIP_LEFT_RIGHT); im.alpha_composite(g,(110,207-54))
    else:
        g=gala_sleep(); im.alpha_composite(g,(120,206-46)); zz(ImageDraw.Draw(im),206,146)
    return im
if __name__=='__main__':
    for st in ('sed','salvo'): scene(st).resize((W*3,H*3),Image.NEAREST).save(f'bufetera_{st}.png')
