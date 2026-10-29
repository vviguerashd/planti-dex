from PIL import Image, ImageDraw
def hx(h,a=255): h=h.lstrip('#'); return (int(h[:2],16),int(h[2:4],16),int(h[4:],16),a)
BK=hx('#1f1f28'); BK2=hx('#33333f'); WH=hx('#f6f2ea'); WH2=hx('#dcd5c7'); OUT=hx('#121016')
EAR=hx('#5e3a36'); EYE=hx('#2a150b'); EYE2=hx('#7a3f17'); SP=hx('#ffffff'); PINK=hx('#ef8496')
BL=hx('#f3a6b4'); NOSE=hx('#0d0d12'); GRAY=hx('#8f949b'); GRAY2=hx('#6c7178'); RED=hx('#d8262e'); RED2=hx('#9e141b')
def outline(im,c=OUT):
    W,H=im.size; s=im.load(); o=im.copy(); oo=o.load()
    for y in range(H):
        for x in range(W):
            if s[x,y][3]==0:
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<W and 0<=ny<H and s[nx,ny][3]>0: oo[x,y]=c;break
    return o
def heart(d,x,y):
    d.point([(x,y),(x+1,y),(x+3,y),(x+4,y)],fill=RED)
    d.line([(x-1,y+1),(x+5,y+1)],fill=RED); d.line([(x-1,y+2),(x+5,y+2)],fill=RED)
    d.line([(x,y+3),(x+4,y+3)],fill=RED2); d.line([(x+1,y+4),(x+3,y+4)],fill=RED2); d.point((x+2,y+5),fill=RED2)
    d.point((x,y+1),fill=hx('#ff8a8f'))
def ruff(d,box):
    x0,y0,x1,y1=box; d.ellipse(box,fill=WH)
    for x in range(x0+2,x1-2,4): d.polygon([(x,y1-3),(x+2,y1+2),(x+4,y1-3)],fill=WH)   # mechones abajo
    for x in range(x0+7,x1-7,7): d.line([(x,y1-9),(x+1,y1-5)],fill=WH2)
def face(d,cx,ey,tongue=True):
    # ojos cafés kawaii
    for ex in (cx-15,cx+9):
        d.ellipse([ex,ey,ex+6,ey+7],fill=EYE); d.rectangle([ex+1,ey+4,ex+5,ey+6],fill=EYE2)
        d.rectangle([ex+1,ey+1,ex+2,ey+2],fill=SP); d.point((ex+4,ey+5),fill=SP)
    d.rectangle([cx-17,ey+9,cx-14,ey+10],fill=BL); d.rectangle([cx+14,ey+9,cx+17,ey+10],fill=BL)
def gala_sit(paw=True):
    W,H=66,80; im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im); cx=33
    d.ellipse([40,66,62,77],fill=BK); d.ellipse([46,68,58,75],fill=BK2)          # cola negra esponjada
    d.ellipse([13,40,53,76],fill=BK); d.ellipse([16,46,26,64],fill=BK2)           # cuerpo
    d.ellipse([9,62,24,78],fill=BK); d.ellipse([42,62,57,78],fill=BK)             # patas traseras
    d.ellipse([8,73,18,79],fill=WH); d.ellipse([48,73,58,79],fill=WH)
    ruff(d,[19,38,47,60])                                                          # melena blanca
    d.rectangle([23,63,28,75],fill=WH); d.ellipse([20,72,29,79],fill=WH)           # pata delantera
    d.point([(24,66),(26,69)],fill=BK2)
    if not paw: d.rectangle([38,62,43,75],fill=WH); d.ellipse([37,72,46,79],fill=WH); d.point([(40,67)],fill=BK2)
    # orejas altas
    d.polygon([(13,26),(16,0),(29,15)],fill=BK); d.polygon([(53,26),(50,0),(37,15)],fill=BK)
    d.polygon([(17,19),(17,6),(25,15)],fill=EAR); d.polygon([(49,19),(49,6),(41,15)],fill=EAR)
    d.ellipse([11,10,55,46],fill=BK); d.ellipse([13,12,25,22],fill=BK2)            # cabeza
    d.polygon([(cx-2,10),(cx+2,10),(cx+3,28),(cx-3,28)],fill=WH)                  # lista blanca
    d.ellipse([cx-11,26,cx+11,45],fill=WH)                                         # hocico
    for p in ((cx-7,36),(cx-5,39),(cx+6,37),(cx+8,34)): d.point(p,fill=BK2)        # pequitas
    d.ellipse([cx-4,27,cx+4,32],fill=NOSE); d.point((cx-2,28),fill=SP)
    d.line([(cx,32),(cx,33)],fill=OUT); d.line([(cx-4,34),(cx-1,34)],fill=OUT); d.line([(cx+1,34),(cx+4,34)],fill=OUT)
    d.ellipse([cx-2,34,cx+3,41],fill=PINK); d.line([(cx,36),(cx,39)],fill=hx('#d0607a'))  # lengua
    face(d,cx,20)
    d.rectangle([19,45,47,47],fill=GRAY); d.line([(19,47),(47,47)],fill=GRAY2)      # collar gris
    heart(d,cx-2,48)
    im=outline(im)
    if paw:
        lay=Image.new('RGBA',(W,H)); e=ImageDraw.Draw(lay)
        e.polygon([(38,62),(44,65),(56,46),(51,43)],fill=WH); e.ellipse([49,36,61,48],fill=WH)
        e.point([(52,38),(55,37),(58,38)],fill=WH2); e.point([(47,55),(45,59)],fill=BK2)
        im.alpha_composite(outline(lay))
    return im
def gala_sleep():
    W,H=84,46; im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    d.ellipse([0,26,26,42],fill=BK); d.ellipse([4,28,16,36],fill=BK2)              # cola
    d.ellipse([8,14,62,44],fill=BK); d.ellipse([14,16,40,26],fill=BK2)            # cuerpo
    d.ellipse([14,34,28,45],fill=BK); d.ellipse([13,40,22,46],fill=WH)            # pata trasera
    ruff(d,[38,22,62,42])
    d.rounded_rectangle([50,38,82,44],3,fill=WH); d.rounded_rectangle([46,40,78,46],3,fill=WH)  # patas al frente
    d.point([(60,41),(66,43)],fill=BK2)
    d.polygon([(47,18),(49,0),(58,12)],fill=BK); d.polygon([(77,18),(75,0),(66,12)],fill=BK)
    d.polygon([(50,13),(50,5),(55,11)],fill=EAR); d.polygon([(74,13),(74,5),(69,11)],fill=EAR)
    d.ellipse([46,8,78,38],fill=BK)
    d.polygon([(61,8),(63,8),(64,22),(60,22)],fill=WH); d.ellipse([53,21,71,38],fill=WH)
    d.ellipse([59,22,65,26],fill=NOSE); d.point([(57,31),(68,30)],fill=BK2)
    for ex in (50,67): d.line([(ex,18),(ex+2,20),(ex+4,18)],fill=hx('#9a9aae'))   # ojitos cerrados
    d.rectangle([49,23,52,24],fill=BL); d.rectangle([72,23,75,24],fill=BL)
    d.line([(60,30),(62,31),(64,30)],fill=OUT)
    d.rectangle([52,36,72,37],fill=GRAY); heart(d,61,37)
    return outline(im)
if __name__=='__main__':
    a=gala_sit(True); b=gala_sit(False); c=gala_sleep(); k=6
    out=Image.new('RGBA',((a.width*2+c.width)*k+80,a.height*k+20),(232,226,212,255))
    out.alpha_composite(a.resize((a.width*k,a.height*k),Image.NEAREST),(10,10))
    out.alpha_composite(b.resize((b.width*k,b.height*k),Image.NEAREST),(a.width*k+40,10))
    out.alpha_composite(c.resize((c.width*k,c.height*k),Image.NEAREST),(a.width*2*k+70,10+(a.height-c.height)*k))
    out.save('gala_check.png')

def gala_stalk():
    """Al acecho / reverencia de juego: pecho abajo, cadera arriba. Mira a la izquierda."""
    W,H=86,54; im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im); o=4
    d.polygon([(64+o,14),(72+o,2),(80+o,2),(72+o,20)],fill=BK); d.ellipse([70+o,0,81+o,9],fill=BK)
    d.line([(70+o,8),(76+o,3)],fill=BK2)
    d.rectangle([54+o,28,60+o,49],fill=BK); d.rectangle([64+o,28,70+o,49],fill=BK)
    d.ellipse([52+o,46,62+o,53],fill=WH); d.ellipse([62+o,46,72+o,53],fill=WH)
    d.ellipse([44+o,6,76+o,32],fill=BK); d.ellipse([50+o,9,64+o,17],fill=BK2)
    d.polygon([(50+o,8),(74+o,18),(66+o,30),(32+o,42),(24+o,30)],fill=BK)
    d.ellipse([22+o,30,38+o,42],fill=WH)
    d.rounded_rectangle([0+o,46,28+o,50],2,fill=WH); d.rounded_rectangle([6+o,49,34+o,53],2,fill=WH)
    d.point([(14+o,47),(22+o,51)],fill=BK2)
    d.polygon([(16+o,22),(19+o,0),(28+o,18)],fill=BK); d.polygon([(19+o,15),(20+o,6),(25+o,15)],fill=EAR)
    d.ellipse([8+o,18,32+o,42],fill=BK); d.ellipse([12+o,20,20+o,26],fill=BK2)
    d.polygon([(9+o,22),(12+o,21),(10+o,32),(6+o,32)],fill=WH)
    d.ellipse([-2+o,30,13+o,40],fill=WH)
    d.ellipse([-3+o,30,1+o,34],fill=NOSE)
    d.rectangle([4+o,38,7+o,41],fill=PINK)
    d.ellipse([14+o,25,20+o,31],fill=EYE); d.rectangle([15+o,29,19+o,30],fill=EYE2); d.rectangle([15+o,26,16+o,27],fill=SP)
    d.line([(13+o,23),(20+o,25)],fill=OUT)
    d.rectangle([20+o,33,23+o,34],fill=BL)
    d.line([(28+o,30),(31+o,41)],fill=GRAY,width=2); heart(d,26+o,41)
    return outline(im)

def gala_happy(tail=0):
    """Sentada, ojos felices ^^, para cuando la acarician. tail: -1/0/1 meneo."""
    W,H=66,80; im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im); cx=33
    tx=[36,40,44][tail+1]; ty=[60,66,60][tail+1]
    d.ellipse([tx,ty,tx+20,ty+11],fill=BK)
    d.ellipse([13,40,53,76],fill=BK); d.ellipse([16,46,26,64],fill=BK2)
    d.ellipse([9,62,24,78],fill=BK); d.ellipse([42,62,57,78],fill=BK)
    d.ellipse([8,73,18,79],fill=WH); d.ellipse([48,73,58,79],fill=WH)
    ruff(d,[19,38,47,60])
    d.rectangle([23,63,28,75],fill=WH); d.ellipse([20,72,29,79],fill=WH)
    d.rectangle([38,63,43,75],fill=WH); d.ellipse([37,72,46,79],fill=WH)
    d.polygon([(13,26),(16,0),(29,15)],fill=BK); d.polygon([(53,26),(50,0),(37,15)],fill=BK)
    d.polygon([(17,19),(17,6),(25,15)],fill=EAR); d.polygon([(49,19),(49,6),(41,15)],fill=EAR)
    d.ellipse([11,10,55,46],fill=BK); d.ellipse([13,12,25,22],fill=BK2)
    d.polygon([(cx-2,10),(cx+2,10),(cx+3,28),(cx-3,28)],fill=WH)
    d.ellipse([cx-11,26,cx+11,45],fill=WH)
    for p in ((cx-7,36),(cx-5,39),(cx+6,37),(cx+8,34)): d.point(p,fill=BK2)
    d.ellipse([cx-4,27,cx+4,32],fill=NOSE); d.point((cx-2,28),fill=SP)
    d.line([(cx-4,34),(cx-1,34)],fill=OUT); d.line([(cx+1,34),(cx+4,34)],fill=OUT)
    d.ellipse([cx-3,34,cx+3,42],fill=PINK); d.line([(cx,36),(cx,40)],fill=hx('#d0607a'))
    for ex in (cx-15,cx+9):   # ojitos ^^
        d.line([(ex,25),(ex+3,21),(ex+6,25)],fill=SP,width=2)
    d.rectangle([cx-18,28,cx-14,30],fill=BL); d.rectangle([cx+14,28,cx+18,30],fill=BL)
    d.rectangle([19,45,47,47],fill=GRAY); d.line([(19,47),(47,47)],fill=GRAY2); heart(d,cx-2,48)
    return outline(im)

def heart_big(im,x,y,a=255):
    pat=["0110110","1111111","1111111","0111110","0011100","0001000"]
    for j,row in enumerate(pat):
        for i,c in enumerate(row):
            if c=='1':
                col=(232,52,72,a) if not (i==1 and j==1) else (255,170,180,a)
                for dx in range(2):
                    for dy in range(2):
                        X,Y=x+i*2+dx,y+j*2+dy
                        if 0<=X<im.width and 0<=Y<im.height: im.putpixel((X,Y),col)
