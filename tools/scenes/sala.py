import random
from PIL import Image, ImageDraw
from gala import gala_sleep, gala_stalk, gala_happy, hx
from common import sp, wall, terracotta, zz
W,H=540,220; FL=150
def tv_wallpaper(d,box):
    """Placeholder: Gala en el fondo de pantalla (se reemplaza con la imagen que mande Vic)."""
    x0,y0,x1,y1=box
    for y in range(y0,y1): d.line([(x0,y),(x1,y)],fill=(120+(y-y0)*2,170+(y-y0),220,255))
    d.rectangle([x0,y1-10,x1,y1],fill=hx('#7db35a'))
def scene(state, tv=None):
    r=random.Random(5); im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    wall(d,[0,0,W,FL],r)
    d.rectangle([0,0,W,6],fill=hx('#f6f4ee'))
    # ---- escaleras curvas de loseta (izquierda)
    d.polygon([(96,0),(150,0),(150,FL),(120,FL),(118,90),(108,40)],fill=hx('#f6f4ee'))
    d.line([(96,0),(108,40),(118,90),(120,FL)],fill=hx('#d9d4c6'),width=2)
    for k in range(9):
        y=FL-6-k*15; x0=122+k*3; x1=200-k*6
        d.polygon([(x0,y),(x1,y-2),(x1,y+6),(x0,y+8)],fill=hx('#b4532f'),outline=hx('#7c3218'))
        d.line([(x0,y+1),(x1,y-1)],fill=hx('#c76a44'))
        d.rectangle([x0,y+8,x1,y+10],fill=hx('#8f3b20'))
    d.polygon([(206,FL),(200,110),(186,60),(166,14),(150,6),(214,6),(214,FL)],fill=hx('#f6f4ee'))
    d.line([(206,FL),(200,110),(186,60),(166,14),(150,6)],fill=hx('#d9d4c6'),width=2)
    for k in range(6):   # block de vidrio escalonado
        for j in range(6-k):
            bx,by=170+j*9,4+k*9+ (5-k)*0
            if by<60: d.rectangle([bx,by+j*0,bx+8,by+8],fill=hx('#9fb2b6'),outline=hx('#6f8488'))
    d.rectangle([150,0,210,4],fill=hx('#f6f4ee'))
    # guirnaldas de cempasúchil
    for gx,glen in ((22,92),(32,110),(44,80),(56,118),(68,96)):
        for gy in range(14,14+glen,5): d.ellipse([gx-3,gy,gx+3,gy+6],fill=hx('#f39a1e'),outline=hx('#d27a0e'))
    # ---- puerta con cortina
    d.rectangle([214,30,262,FL],fill=hx('#2b2d2c')); d.rectangle([218,36,258,100],fill=hx('#5d6563'))
    for y in range(40,100,6): d.line([(220,y),(256,y)],fill=hx('#444b49'))
    d.polygon([(208,26),(240,26),(236,80),(246,FL),(214,FL),(222,80)],fill=hx('#fbfbf8'),outline=hx('#d6d6d0'))
    for x in (216,224,232): d.line([(x,30),(x+2,FL-4)],fill=hx('#e6e6e0'))
    d.line([(204,25),(268,25)],fill=hx('#8c8c8c'),width=2)
    # ---- mesa con mantel amarillo de cuadros y sillas
    d.rectangle([276,30,306,70],fill=hx('#ffffff'),outline=hx('#c9c9c9')); d.rectangle([279,33,303,67],fill=hx('#dcd8e6'))
    for gx in (284,293): d.ellipse([gx,44,gx+6,52],fill=hx('#fbfbfb')); d.rectangle([gx,48,gx+6,58],fill=hx('#fbfbfb'))
    d.rounded_rectangle([264,96,292,FL+10],4,fill=hx('#cdb68f')); d.rounded_rectangle([372,96,400,FL+10],4,fill=hx('#cdb68f'))
    for yy in range(100,FL+8,4):
        d.line([(266,yy),(290,yy)],fill=hx('#b9a079')); d.line([(374,yy),(398,yy)],fill=hx('#b9a079'))
    d.polygon([(288,112),(378,112),(386,150),(282,150)],fill=hx('#f3df6a'))
    for x in range(288,384,8): d.line([(x,112),(x-3,150)],fill=hx('#f8f3d8'),width=2)
    for y in range(116,150,7): d.line([(284,y),(384,y)],fill=hx('#f8f3d8'),width=2)
    d.ellipse([300,98,312,112],fill=hx('#f3b6c4')); d.rectangle([318,102,340,112],fill=hx('#9fc4e0'),outline=hx('#555555'))
    d.rectangle([346,104,356,112],fill=hx('#c9a26b'))
    # ---- sillón en L, TV encima, cuadros, ventana, candil
    d.rectangle([488,18,540,104],fill=hx('#dfe9f2'))
    for x in range(490,540,7): d.line([(x,18),(x+2,104)],fill=hx('#c4d0db'))
    d.rectangle([484,14,540,16],fill=hx('#8c8c8c'))
    d.rectangle([392,8,482,60],fill=hx('#b99a6a')); d.rectangle([395,11,479,57],fill=hx('#111214'))   # TV
    if tv is not None: im.alpha_composite(tv,(396,12))
    else: tv_wallpaper(d,[396,12,478,56])
    for lx in range(392,484,7):
        d.polygon([(lx,8),(lx+3,4),(lx+6,8),(lx+3,11)],fill=hx('#e8722a'))
    d.line([(436,0),(436,4)],fill=hx('#c9a24a'))
    for a,b in (((420,6),(452,2)),((424,1),(448,8))): d.line([a,b],fill=hx('#c9a24a'))
    for bx,by in ((418,4),(452,1),(424,0),(448,8)): d.ellipse([bx-2,by-1,bx+2,by+3],fill=hx('#fff4c2'))
    d.rounded_rectangle([404,96,540,FL+6],6,fill=hx('#cbb79b'),outline=hx('#9c8a70'))
    d.rounded_rectangle([408,84,540,104],6,fill=hx('#d8c6ab'),outline=hx('#9c8a70'))
    d.rounded_rectangle([400,104,414,FL+8],4,fill=hx('#bba78b'),outline=hx('#9c8a70'))
    d.ellipse([420,82,444,104],fill=hx('#e8833a'),outline=hx('#9c4e1c'))           # cojín calabaza
    d.polygon([(427,90),(430,88),(431,92)],fill=hx('#3a2010')); d.polygon([(437,88),(440,90),(436,92)],fill=hx('#3a2010')); d.line([(427,97),(437,97)],fill=hx('#3a2010'))
    d.rounded_rectangle([452,84,474,102],4,fill=hx('#7fb04a'),outline=hx('#4e7a2a'))  # cojín verde
    d.rounded_rectangle([480,86,506,104],4,fill=hx('#f3c4cf'),outline=hx('#b98592'))  # cojín rosa
    d.rounded_rectangle([510,80,534,100],4,fill=hx('#e9e6df'),outline=hx('#a9a59b'))
    # plato de croquetas de Gala
    d.rectangle([84,FL+18,118,FL+22],fill=hx('#8a5a32')); d.line([(88,FL+22),(86,FL+30)],fill=hx('#222222')); d.line([(114,FL+22),(116,FL+30)],fill=hx('#222222'))
    for bx in (88,102): d.ellipse([bx,FL+14,bx+12,FL+20],fill=hx('#c9ced2'),outline=hx('#7e858a'))
    terracotta(im,FL+10,r) if False else None
    return im
def full(state, tv=None):
    im=Image.new('RGBA',(W,H)); r=random.Random(5)
    terracotta(im,FL,r)
    top=scene(state,tv); mask=Image.new('L',(W,H),0); ImageDraw.Draw(mask).rectangle([0,0,W,FL],fill=255)
    im.paste(top,(0,0),mask)
    # muebles que bajan al piso (sillas, sillón, plato) se repintan encima
    over=scene(state,tv); m2=Image.new('L',(W,H),0); md=ImageDraw.Draw(m2)
    for box in ([264,96,292,FL+10],[372,96,400,FL+10],[282,112,386,FL],[400,84,540,FL+8],[84,FL+12,118,FL+31]): md.rectangle(box,fill=255)
    im.paste(over,(0,0),m2)
    if state is None: return im
    m8='con_sed' if state=='sed' else 'feliz'
    for pid,x,m in (('P06',-2,'feliz'),('P08',190,m8),('P07',462,'feliz')):
        p=sp(pid,m); im.alpha_composite(p,(x,214-93))
    if state=='sed':
        g=gala_stalk().transpose(Image.FLIP_LEFT_RIGHT); im.alpha_composite(g,(110,216-54))
    elif state=='salvo':
        g=gala_sleep(); im.alpha_composite(g,(300,214-46)); zz(ImageDraw.Draw(im),384,152)
    return im
if __name__=='__main__':
    from gala import gala_happy
    tv=Image.new('RGBA',(60,34),hx('#9cc8ea')); ImageDraw.Draw(tv).rectangle([0,28,60,34],fill=hx('#7db35a'))
    g=gala_happy(0).resize((28,34)); tv.alpha_composite(g,(16,0))
    for st in ('sed','salvo'): full(st,tv).resize((W*3,H*3),Image.NEAREST).save(f'sala_{st}.png')
