import random
from PIL import Image, ImageDraw
from gala import gala_sit, gala_sleep, gala_stalk, hx, outline
import pathlib; S=str(pathlib.Path(__file__).resolve().parents[2]/'public'/'sprites')+'/'
def sp(i,m): return Image.open(f'{S}{i}_{m}.png').convert('RGBA')
W,H=360,210; FLOOR=140
def base():
    r=random.Random(3)
    im=Image.new('RGBA',(W,H),hx('#efece4')); d=ImageDraw.Draw(im)
    for _ in range(900):  # pared texturizada
        x,y=r.randrange(W),r.randrange(FLOOR); d.point((x,y),fill=hx('#e2ded4'))
    d.rectangle([0,0,W,7],fill=hx('#f7f6f2'))
    for _ in range(200): d.point((r.randrange(W),r.randrange(7)),fill=hx('#dedad0'))
    d.ellipse([160,1,200,9],fill=hx('#fffbe8'),outline=hx('#b9b4a6'))         # plafón
    # piso de loseta gris con junta oscura
    d.rectangle([0,FLOOR,W,H],fill=hx('#bdb9b5'))
    for _ in range(1400): d.point((r.randrange(W),r.randrange(FLOOR,H)),fill=hx('#a9a5a1') if r.random()<.6 else hx('#d2cfcb'))
    y=FLOOR; step=12
    while y<H: d.line([(0,y),(W,y)],fill=hx('#5b5754')); y+=step; step+=4
    for i in range(-6,14):
        x0=180+i*34; d.line([(180+i*24,FLOOR),(x0+i*14,H)],fill=hx('#5b5754'))
    d.rectangle([0,FLOOR-3,W,FLOOR],fill=hx('#d8d3c8'))                       # zoclo
    # muro de block de vidrio escalonado
    gx=298
    for row in range(14):
        yy=18+row*9
        x_start=gx+max(0,(5-row))*9 if row<5 else gx
        for xx in range(x_start,W,10):
            d.rectangle([xx,yy,xx+9,yy+8],fill=hx('#8f9a8f'),outline=hx('#5d665d'))
            d.point([(xx+2,yy+2),(xx+6,yy+5)],fill=hx('#c4cfc4'))
    # candil
    d.line([(334,0),(334,22)],fill=hx('#3a3a3a'))
    d.arc([316,18,352,32],0,180,fill=hx('#3a3a3a'))
    for cx in (316,334,352): d.polygon([(cx-5,30),(cx+5,30),(cx+3,36),(cx-3,36)],fill=hx('#f5f0e4'),outline=hx('#8a8478'))
    # librero
    d.rectangle([0,28,46,FLOOR+40],fill=hx('#4a3426')); d.rectangle([4,32,42,FLOOR+36],fill=hx('#3a281c'))
    cols=['#c0392b','#2e86c1','#f1c40f','#27ae60','#8e44ad','#e67e22','#ecf0f1']
    for sy in (32,62,92,122,152):
        d.line([(4,sy+28),(42,sy+28)],fill=hx('#5a4030'),width=2)
        x=6
        while x<40:
            w=r.randint(2,4); h=r.randint(14,24)
            d.rectangle([x,sy+28-h,x+w,sy+27],fill=hx(r.choice(cols))); x+=w+1
    d.ellipse([20,108,30,118],fill=hx('#e67e22'))   # figurita
    # La Gran Ola (tu cuadro)
    d.rectangle([66,12,196,76],fill=hx('#8a8478')); d.rectangle([68,14,194,74],fill=hx('#d9d3c2'))
    d.polygon([(68,74),(68,52),(84,36),(104,26),(124,24),(138,30),(130,34),(118,32),(106,40),(100,52),(112,58),(128,60),(150,62),(176,60),(194,56),(194,74)],fill=hx('#2f5aa8'))
    d.polygon([(104,26),(124,24),(138,30),(134,36),(126,30),(116,30),(108,36)],fill=hx('#f4f4f0'))
    for fx in range(108,138,4): d.polygon([(fx,30),(fx+2,35),(fx+4,30)],fill=hx('#f4f4f0'))
    d.polygon([(68,62),(80,48),(92,40),(86,52),(78,62)],fill=hx('#5d86cf'))
    d.polygon([(150,62),(160,56),(172,58),(184,52),(194,56),(194,64)],fill=hx('#f4f4f0'))
    d.polygon([(158,58),(166,50),(174,58)],fill=hx('#f7f7f2'),outline=hx('#8a8478'))   # Fuji
    d.polygon([(118,62),(146,58),(148,61),(120,65)],fill=hx('#c9a35c'))                 # barca
    # escritorio de Vic
    d.rectangle([56,124,220,130],fill=hx('#e8e2d2'),outline=hx('#6b6355')); d.rectangle([60,130,64,178],fill=hx('#6b6355')); d.rectangle([212,130,216,170],fill=hx('#6b6355'))
    d.rectangle([180,131,208,168],fill=hx('#e9edf0'),outline=hx('#8a96a0'))            # cajonera
    for yy in (142,154): d.line([(180,yy),(208,yy)],fill=hx('#8a96a0'))
    d.rectangle([186,134,196,140],fill=hx('#6aa0d8')); d.rectangle([188,146,200,151],fill=hx('#f1c40f'))
    # monitores
    d.rectangle([70,86,112,116],fill=hx('#141414')); d.rectangle([72,88,110,114],fill=hx('#1d2a36'))
    for yy in range(91,112,3): d.line([(75,yy),(75+r.randint(8,30),yy)],fill=hx('#7fb6e0'))
    d.rectangle([116,84,160,116],fill=hx('#141414')); d.rectangle([118,86,158,114],fill=hx('#f2b234'))
    for gx2 in range(122,156,7):
        for gy in (90,99,107): d.rectangle([gx2,gy,gx2+3,gy+4],fill=hx('#7a5a1c'))
    for sx in (90,138): d.rectangle([sx,116,sx+3,124],fill=hx('#141414')); d.rectangle([sx-6,122,sx+9,124],fill=hx('#141414'))
    d.rectangle([84,119,128,123],fill=hx('#2b2b2b'))   # teclado
    # escritorio de Fer (blanco, rosa)
    d.rectangle([276,150,360,156],fill=hx('#fbfbfb'),outline=hx('#9a9a9a')); d.rectangle([282,156,285,210],fill=hx('#cfcfcf'))
    d.rectangle([296,143,336,149],fill=hx('#f6b8cc'),outline=hx('#c97d96'))
    for kx in range(298,335,4): d.point((kx,145),fill=hx('#ffffff'))
    d.ellipse([340,138,356,150],fill=hx('#f3a6b4'),outline=hx('#c97d96')); d.point([(345,143),(350,143)],fill=hx('#4a2a30'))  # peluche
    d.rectangle([344,124,354,150],fill=hx('#e5e5e5'),outline=hx('#9a9a9a'))            # base de laptop
    return im
def chairs(im):
    d=ImageDraw.Draw(im)
    # silla gamer de Vic
    d.rounded_rectangle([66,96,104,150],6,fill=hx('#2a2a2a'),outline=hx('#121212')); d.rounded_rectangle([72,102,98,128],4,fill=hx('#6e6252'))
    d.rectangle([62,148,108,158],fill=hx('#2a2a2a')); d.rectangle([83,158,87,180],fill=hx('#1a1a1a'))
    d.line([(68,184),(102,184)],fill=hx('#1a1a1a'),width=3)
    # silla rosa de Fer
    d.rounded_rectangle([292,160,334,206],6,fill=hx('#f2d4dc'),outline=hx('#9a8a8f'))
    for yy in range(166,202,4): d.line([(296,yy),(330,yy)],fill=hx('#e8a9ba'))
    d.rounded_rectangle([302,150,324,162],4,fill=hx('#f5f5f5'),outline=hx('#9a8a8f'))
def scene(thirsty, nogala=False):
    im=base()
    p9=sp('P09','feliz'); im.alpha_composite(p9,(206,190-93))
    m13='con_sed' if thirsty else 'feliz'; p13=sp('P13',m13); im.alpha_composite(p13,(146,131-93))
    chairs(im)
    if nogala: return im
    if thirsty:
        g=gala_stalk().transpose(Image.FLIP_LEFT_RIGHT); im.alpha_composite(g,(104,206-54))
    else:
        g=gala_sleep(); im.alpha_composite(g,(130,205-46)); d=ImageDraw.Draw(im)
        for (x,y,s) in ((212,150,4),(220,142,5)): d.line([(x,y),(x+s,y),(x,y+s),(x+s,y+s)],fill=hx('#4a554c'))
    return im
if __name__=='__main__':
  for n,t in (('estudio_sed',True),('estudio_salvo',False)):
    s=scene(t); s.resize((W*3,H*3),Image.NEAREST).save(n+'.png')
