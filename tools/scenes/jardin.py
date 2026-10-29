import random, math
from PIL import Image, ImageDraw
from gala import hx
from common import wall
def lights(d,W,y0=6,sag=10):
    pts=[(x, y0+sag*math.sin(math.pi*((x%160)/160))) for x in range(0,W+1,2)]
    d.line(pts,fill=hx('#2a2a2a'))
    for x in range(10,W,22):
        y=y0+sag*math.sin(math.pi*((x%160)/160))
        d.line([(x,y),(x,y+3)],fill=hx('#2a2a2a')); d.ellipse([x-2,y+3,x+2,y+8],fill=hx('#fff2b8'),outline=hx('#c9b56a'))
def stones(d,box,r):
    x0,y0,x1,y1=box; d.rectangle(box,fill=hx('#e9e6dc'))
    y=y0; row=0
    while y<y1:
        h=r.randint(8,11); x=x0-(row%2)*9
        while x<x1:
            w=r.randint(14,22); d.rectangle([max(x,x0),y,min(x+w,x1),min(y+h,y1)],outline=hx('#b9b4a5'))
            for _ in range(4): d.point((r.randint(max(x,x0),min(x+w,x1)),r.randint(y,min(y+h,y1))),fill=hx('#cfcabc'))
            x+=w
        y+=h; row+=1
def bamboo(d,x,base,h,r):
    for k in range(5):
        sx=x+k*5+r.randint(-1,1); top=base-h+r.randint(0,14)
        d.line([(sx,base),(sx,top)],fill=hx('#6f9a3a'),width=2)
        for y in range(top,base,9): d.point((sx,y),fill=hx('#4e7428'))
        for y in range(top,base-10,7):
            dx=r.choice((-1,1)); d.polygon([(sx,y),(sx+dx*10,y-3),(sx+dx*11,y-1)],fill=hx(r.choice(['#8fbf4a','#79ab3c','#a6cf5c'])))
def ground(d,W,H,y0,r,tiles=None):
    d.rectangle([0,y0,W,H],fill=hx('#6b5236'))
    for _ in range(W*(H-y0)//5): d.point((r.randrange(W),r.randrange(y0,H)),fill=hx(r.choice(['#5d4730','#7a5f40','#4f6a32','#5e7d3a'])))
    for _ in range(W//3):
        x,y=r.randrange(W),r.randrange(y0+3,H); c=hx(r.choice(['#6f9a3a','#5e8a30','#86ad48']))
        d.line([(x,y),(x-1,y-4)],fill=c); d.line([(x+1,y),(x+2,y-3)],fill=c)
def cochera():
    W,H=480,220; FL=160; r=random.Random(21); im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    wall(d,[150,24,430,FL],r,base='#e7c86a',dots=('#d9b956','#f0d47e'))
    stones(d,[0,40,150,FL],r)
    d.polygon([(0,40),(150,40),(160,52),(0,52)],fill=hx('#a2502d'))           # tejas
    for x in range(0,156,8): d.arc([x,44,x+8,56],180,360,fill=hx('#7a3a1e'))
    d.rectangle([0,0,W,24],fill=hx('#f4f1e8')); d.rectangle([0,22,W,26],fill=hx('#d6d1c3'))
    lights(d,W)
    for lx in (220,360):                                                        # faroles
        d.line([(lx,26),(lx,46)],fill=hx('#3a3a3a')); d.ellipse([lx-6,46,lx+6,62],fill=hx('#fff4c8'),outline=hx('#5a5a5a'))
        d.rectangle([lx-3,62,lx+3,65],fill=hx('#5a5a5a'))
    d.ellipse([276,54,304,94],outline=hx('#5a3a2a'),width=3); d.ellipse([281,60,299,88],fill=hx('#b8502a'))
    d.line([(290,50),(290,98)],fill=hx('#5a3a2a')); d.line([(272,74),(308,74)],fill=hx('#5a3a2a'))
    for a in range(0,360,20):                                                   # corona de cempasúchil
        x=118+14*math.cos(math.radians(a)); y=80+14*math.sin(math.radians(a)); d.ellipse([x-3,y-3,x+3,y+3],fill=hx('#f39a1e'))
    for gy in range(96,124,5): d.ellipse([115,gy,121,gy+5],fill=hx('#f39a1e'))
    for y in range(24,FL): d.line([(430,y),(W,y)],fill=(170+(y-24)//3,205+(y-24)//6,232,255))
    IRON=hx('#1e1f1f')                                                          # reja derecha
    for x in range(434,W,7): d.line([(x,20),(x,FL+30)],fill=IRON)
    for y in (30,90,FL): d.line([(430,y),(W,y)],fill=IRON,width=2)
    for cy in range(40,86,16): d.ellipse([448,cy,462,cy+14],outline=IRON); d.ellipse([464,cy,478,cy+14],outline=IRON)
    ground(d,W,H,FL,r)
    for (x,y,w,h) in ((170,200,34,14),(214,184,30,11),(250,170,26,9),(300,196,34,14),(338,178,30,11)):   # pasos de piedra
        d.polygon([(x,y),(x+w,y),(x+w-4,y+h),(x-4,y+h)],fill=hx('#b8b3a6'),outline=hx('#8c877a'))
    d.rectangle([4,170,148,198],fill=hx('#e2c27a'),outline=hx('#a58a4a'))      # jardinera
    stones(d,[4,198,40,219],r)
    pos={'P04':(-6,120),'P18':(52,92),'P24':(150,120),'P17':(222,120),'P22':(290,120),'P15':(372,118)}
    return im,pos,{'W':W,'H':H,'floor':214,'sleep':(240,170)}
def pasillo():
    W,H=680,220; O=80; FL=150; r=random.Random(22); im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    for y in range(0,FL): d.line([(0,y),(W,y)],fill=(170+y//3,205+y//6,232,255))
    d.rectangle([0,96,500+O,FL],fill=hx('#d9a48c'))                              # barda rosada
    IRON=hx('#1e1f1f')
    for x in range(4,500+O,7): d.line([(x,30),(x,96)],fill=IRON)
    d.line([(0,30),(500+O,30)],fill=IRON,width=2); d.line([(0,92),(500+O,92)],fill=IRON,width=2)
    for cx in range(24,500+O,40):
        d.ellipse([cx-14,40,cx+14,68],outline=IRON,width=2); d.arc([cx-7,47,cx+7,61],0,270,fill=IRON)
    for cx in range(8,500+O,10): d.ellipse([cx-4,80,cx+4,90],outline=IRON)
    # copa del liquidámbar arriba
    for _ in range(140):
        x,y=r.randrange(60,330),r.randrange(0,34); c=hx(r.choice(['#3f6b33','#4f7d3d','#2f5527']))
        for a in range(5):
            ang=math.radians(a*72-90); d.line([(x,y),(x+5*math.cos(ang),y+5*math.sin(ang))],fill=c,width=2)
    # la casita: entrada de piedra con techo blanco y reja en arco
    stones(d,[500+O,40,W,FL+40],r)
    d.polygon([(490+O,44),(550+O,8),(610+O,44)],fill=hx('#f6f4ee'),outline=hx('#c9c4b6'))
    d.rectangle([520+O,70,580+O,FL+40],fill=hx('#4a2a1a')); d.pieslice([520+O,46,580+O,96],180,360,fill=hx('#4a2a1a'))
    d.rectangle([530+O,90,570+O,140],fill=hx('#f4c25a')); d.line([(550+O,90),(550+O,140)],fill=hx('#4a2a1a'),width=2)
    for x in range(524+O,580+O,6): d.line([(x,72),(x,FL+40)],fill=IRON)
    d.arc([520+O,46,580+O,96],180,360,fill=IRON,width=2); d.line([(520+O,140),(580+O,140)],fill=IRON,width=2)
    for cx in (534+O,550+O,566+O): d.ellipse([cx-5,52,cx+5,62],outline=IRON)
    ground(d,W,H,FL,r)
    d.rectangle([0,FL,W,FL+3],fill=hx('#c9b8a4'))
    d.polygon([(0,200),(W,190),(W,H),(0,H)],fill=hx('#e9e4da'))                 # piso de loseta clara
    for x in range(0,W,26): d.line([(x,200-(x/W)*10),(x-6,H)],fill=hx('#cfc8ba'))
    d.line([(0,208),(W,199)],fill=hx('#cfc8ba'))
    for rx,ry in ((30,176),(46,172)): d.ellipse([rx,ry,rx+18,ry+14],fill=hx('#b9a58c'),outline=hx('#7d6b55'))   # piedras
    pos={'P21':(-4,108),'P25':(54,110),'P14':(118,104),'P16':(190,112),'P03':(252,108),'P26':(318,110),'P19':(384,108),'P20':(446,112),'P23':(500,112),'P27':(548,112)}
    return im,pos,{'W':W,'H':H,'floor':214,'sleep':(280,170)}
if __name__=='__main__':
    from common import sp
    for name,fn in (('cochera',cochera),('pasillo',pasillo)):
        im,pos,meta=fn()
        for pid,(x,y) in pos.items(): im.alpha_composite(sp(pid,'feliz'),(x,y))
        im.resize((im.width*2,im.height*2),Image.NEAREST).save(f'{name}_v1.png')
