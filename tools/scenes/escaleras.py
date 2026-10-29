import random, math
from PIL import Image, ImageDraw
from gala import gala_sleep, gala_stalk, hx
import pathlib; S=str(pathlib.Path(__file__).resolve().parents[2]/'public'/'sprites')+'/'
def sp(i,m): return Image.open(f'{S}{i}_{m}.png').convert('RGBA')
W,H=360,210
def tex(d,box,base,dots,r,n):
    d.rectangle(box,fill=hx(base))
    for _ in range(n):
        d.point((r.randint(box[0],box[2]),r.randint(box[1],box[3])),fill=hx(r.choice(dots)))
def base():
    r=random.Random(7); im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    tex(d,[0,0,W,H],'#cfd1c6',['#b9bbb0','#e0e2d8','#a9ab9f'],r,4000)
    # vista por el arco: cielo, casa amarilla genérica, barda
    view=Image.new('RGBA',(W,H)); v=ImageDraw.Draw(view)
    for y in range(0,150): v.line([(0,y),(W,y)],fill=(140+y//3,190+y//5,230,255))
    v.rectangle([30,70,170,150],fill=hx('#e9c33a')); v.rectangle([30,64,170,70],fill=hx('#c79a2a'))
    for wx in (44,84,124):
        v.rectangle([wx,82,wx+22,104],fill=hx('#f4f1e6')); v.rectangle([wx+2,84,wx+20,102],fill=hx('#9fb6c9'))
    v.rectangle([30,122,170,150],fill=hx('#f2f0ea'))
    for x in range(34,170,6): v.line([(x,124),(x,150)],fill=hx('#c9c5bb'))
    v.rectangle([10,40,30,150],fill=hx('#6b8f5a'))   # arbolito
    mask=Image.new('L',(W,H)); m=ImageDraw.Draw(mask)
    m.rectangle([24,60,196,152],fill=255); m.pieslice([24,10,196,110],180,360,fill=255)
    im.paste(view,(0,0),mask)
    d.arc([22,8,198,112],180,360,fill=hx('#9a9c91'),width=3)
    d.line([(22,60),(22,152)],fill=hx('#9a9c91'),width=3); d.line([(197,60),(197,152)],fill=hx('#9a9c91'),width=3)
    # herrería que llena el arco y termina en arco
    IRON=hx('#1e1f1f'); lay=Image.new('RGBA',(W,H)); L=ImageDraw.Draw(lay)
    for x in range(28,196,8):
        L.line([(x,10),(x,150)],fill=IRON); L.polygon([(x-1,96),(x,90),(x+1,96)],fill=IRON)
    L.line([(24,96),(196,96)],fill=IRON,width=2); L.line([(24,150),(196,150)],fill=IRON,width=2); L.line([(24,138),(196,138)],fill=IRON)
    for cx in range(44,196,34): L.ellipse([cx-12,105,cx+12,129],outline=IRON,width=2); L.arc([cx-6,111,cx+6,123],0,270,fill=IRON)
    for cx in range(30,196,10): L.ellipse([cx-4,140,cx+4,148],outline=IRON)
    L.line([(24,62),(196,62)],fill=IRON,width=2)
    for cx in range(58,190,26): L.ellipse([cx-9,68,cx+9,86],outline=IRON,width=2)
    L.arc([60,26,160,96],180,360,fill=IRON,width=2); L.arc([84,44,136,86],180,360,fill=IRON)
    for cx,cy in ((110,36),(80,46),(140,46)): L.ellipse([cx-5,cy-5,cx+5,cy+5],outline=IRON)
    am=Image.new('L',(W,H)); ImageDraw.Draw(am).rectangle([24,60,196,152],fill=255); ImageDraw.Draw(am).pieslice([24,10,196,110],180,360,fill=255)
    im.paste(lay,(0,0),Image.composite(am,Image.new('L',(W,H)),lay.split()[3]))
    d.arc([24,10,196,110],180,360,fill=IRON,width=3); d.line([(25,60),(25,152)],fill=IRON,width=2); d.line([(195,60),(195,152)],fill=IRON,width=2)
    # piso del balcón: tierra seca con pasto
    d.rectangle([0,152,W,H],fill=hx('#8b6b47'))
    for _ in range(900): d.point((r.randrange(W),r.randrange(152,H)),fill=hx(r.choice(['#7a5c3b','#9c7b55','#6e5234'])))
    for _ in range(60):
        x,y=r.randrange(W),r.randrange(156,H)
        c=hx(r.choice(['#c2ab5c','#b39a4a','#d1bd73','#7d9a4a']))
        d.line([(x,y),(x-1,y-3)],fill=c); d.line([(x+1,y),(x+2,y-4)],fill=c); d.line([(x+2,y),(x+3,y-2)],fill=c)
    # jaula del canario
    d.rectangle([34,0,92,3],fill=hx('#5f8f6a'))
    for x in range(36,92,4): d.line([(x,3),(x,36)],fill=hx('#7fb08a'))
    d.rectangle([32,36,94,40],fill=hx('#e9e9e2'),outline=hx('#9a9a92')); d.rectangle([38,24,52,34],fill=hx('#2f6fd1'))
    d.line([(44,22),(86,14)],fill=hx('#b08a5a'),width=2)
    d.ellipse([60,4,72,16],fill=hx('#f2cf2a')); d.ellipse([68,2,76,10],fill=hx('#f2cf2a')); d.point((73,5),fill=hx('#111111'))
    d.polygon([(76,6),(79,7),(76,8)],fill=hx('#e88a2a')); d.polygon([(58,10),(52,16),(60,14)],fill=hx('#d9b21f'))
    return im
def stairs(im):
    """Caracol visto de lado: escalones en cuña alrededor del poste, pasamanos en hélice."""
    d=ImageDraw.Draw(im); M=hx('#2f3332'); M2=hx('#4d5250'); MB=hx('#232626'); OUTL=hx('#151716')
    px=282; R=72; rise=22; step=math.radians(32)
    treads=[]
    for k in range(16):
        th=k*step; yb=236-k*rise
        treads.append((th,yb))
    def pt(th,yb,r): return (px+r*math.cos(th), yb+ r*math.sin(th)*0.28)
    back=[t for t in treads if math.sin(t[0])<0]; front=[t for t in treads if math.sin(t[0])>=0]
    def wedge(th,yb,col):
        a=pt(th-step*0.48,yb,R); b=pt(th+step*0.48,yb,R)
        d.polygon([(px,yb),a,(a[0],a[1]+4),(b[0],b[1]+4),b],fill=col,outline=OUTL)
        for f in (0.35,0.6,0.85):
            p=pt(th-step*0.4,yb,R*f); q=pt(th+step*0.4,yb,R*f); d.line([p,q],fill=M2)
    for th,yb in back: wedge(th,yb,MB)
    rail=[]
    for t in range(0,16*32):
        th=math.radians(t); yb=236-(t/32)*rise
        rail.append((pt(th,yb,R+2)[0], pt(th,yb,R+2)[1]-24, math.sin(th)))
    for i in range(len(rail)-1):
        if rail[i][2]<0: d.line([rail[i][:2],rail[i+1][:2]],fill=MB,width=2)
    for th,yb in back:
        o=pt(th,yb,R); d.line([o,(o[0],o[1]-24)],fill=MB)
    d.rectangle([px-3,0,px+3,H],fill=M); d.line([(px-1,0),(px-1,H)],fill=M2)
    for th,yb in front: wedge(th,yb,M)
    for th,yb in front:
        o=pt(th,yb,R); d.line([o,(o[0],o[1]-24)],fill=M,width=2)
    for i in range(len(rail)-1):
        if rail[i][2]>=0: d.line([rail[i][:2],rail[i+1][:2]],fill=M,width=3)
    # escalón izquierdo más alto para colgar la maceta
    cand=[(th,yb) for th,yb in treads if math.cos(th)<-0.6 and 60<yb<100]
    th,yb=cand[0]; o=pt(th,yb,R*0.9)
    return int(o[0]),int(o[1])+4

def scene(state):  # state: 'sed' o 'salvo'
    im=base(); hx_,hy_=stairs(im)
    m2='con_sed' if state=='sed' else 'feliz'
    p5=sp('P05','feliz'); im.alpha_composite(p5,(14,206-82))
    p2=sp('P02',m2); im.alpha_composite(p2,(92,206-92))
    d=ImageDraw.Draw(im); d.line([(hx_,hy_-4),(hx_,hy_+6)],fill=hx('#2f3332'),width=2)
    p1=sp('P01','feliz'); im.alpha_composite(p1,(hx_-40,hy_+6))     # cuelga del escalón
    if state=='sed':
        g=gala_stalk(); im.alpha_composite(g,(176,207-54))
    else:
        g=gala_sleep(); im.alpha_composite(g,(186,206-46))
        for (x,y,s) in ((262,158,4),(270,150,5)): d.line([(x,y),(x+s,y),(x,y+s),(x+s,y+s)],fill=hx('#2f3332'))
    return im
if __name__=='__main__':
    for st in ('sed','salvo'):
        scene(st).resize((W*3,H*3),Image.NEAREST).save(f'escaleras_{st}.png')
