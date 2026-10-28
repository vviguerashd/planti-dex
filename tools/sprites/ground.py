# Plantas en suelo: cara en un montículo de tierra (o en el tronco, para árboles)
import math, random
from kawaii import *
from engine import hexc, mix
from PIL import Image, ImageDraw

SOIL={"mid":hexc("#9A6A44"),"light":hexc("#C08A5C"),"dark":hexc("#6B4429"),"out":hexc("#3A2414"),"hi":hexc("#E0AD7E")}
GRASS={"dark":hexc("#3E8A3A"),"mid":hexc("#5DB04E"),"light":hexc("#8AD46A"),"out":hexc("#1F4F24")}

def edge_pixels(lay):
    l=lay.load(); out=[]
    for y in range(H):
        for x in range(W):
            if l[x,y][3]:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if not (0<=nx<W and 0<=ny<H) or l[nx,ny][3]==0: out.append((x,y)); break
    return out

def mound(img, rng, top=66, half=30, face_y=73, stones=True, state="feliz"):
    SOILc = SOIL if state!="sedienta" else {"mid":hexc("#B88F68"),"light":hexc("#D6AE86"),"dark":hexc("#8A6646"),"out":hexc("#4A3220"),"hi":hexc("#EBC9A2")}
    m=new(); d=ImageDraw.Draw(m)
    d.ellipse([40-half, top, 40+half, top+2*(GROUND-top)], fill=SOILc["mid"])
    c=m.load()
    for y in range(GROUND,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    m=shade_blob(m, SOILc, (-3,-3), (3,3))
    l=m.load()
    for _ in range(18):
        x,y=rng.randint(40-half+4,40+half-4), rng.randint(top+4,GROUND-3)
        if l[x,y][3] and l[x,y][:3]==SOILc["mid"][:3]: l[x,y]=SOILc["dark"]
    if state=="sedienta":
        for (x0,y0) in [(40-half+8,top+8),(40+half-12,top+10),(40-half+14,GROUND-6),(40+half-16,GROUND-5)]:
            for k in range(4):
                xx,yy=x0+k,y0+(k%2)
                if 0<=xx<W and 0<=yy<H and l[xx,yy][3]: l[xx,yy]=SOILc["out"]
    m=outline(m, SOILc["out"]); img.alpha_composite(m)
    # pasto en el borde superior
    g=new(); dg=ImageDraw.Draw(g)
    for x in range(40-half+3, 40+half-2, 3):
        yy = top + int(((x-40)/half)**2*(GROUND-top)*0.9)
        h = rng.randint(2,4)
        dg.line([(x,yy),(x+rng.choice([-1,0,1]),yy-h)], fill=GRASS["mid"] if state!="sedienta" else hexc("#B8A84E"))
    g=outline(g, GRASS["out"]); img.alpha_composite(g)
    if stones:
        st=new()
        for x in range(40-half-4, 40+half+6, 7):
            ImageDraw.Draw(st).ellipse([x-3,GROUND-4,x+3,GROUND+1], fill=hexc("#B9B4AA"))
            px(st,x-1,GROUND-3,hexc("#E2DED6"))
        sc=st.load()
        for y in range(GROUND+1,H):
            for x in range(W): sc[x,y]=(0,0,0,0)
        st=outline(st, hexc("#6E6A62")); img.alpha_composite(st)
    kawaii_face(img, 40, face_y, state)

def sword(target, x0, y0, ang, L, w, pal, rng, band=True, margin=None, droop=0.0):
    pts=E.curve(x0,y0,ang,L,droop,steps=16)
    left=[];right=[];n=len(pts)-1
    for i,(x,y,dx,dy) in enumerate(pts):
        t=i/n; ww = w*(1.0 if t<0.62 else max(0.0,1-(t-0.62)/0.38))+0.4
        nx,ny=-dy,dx; left.append((x+nx*ww/2,y+ny*ww/2)); right.append((x-nx*ww/2,y-ny*ww/2))
    lay=new(); ImageDraw.Draw(lay).polygon(left+right[::-1], fill=pal["mid"])
    lay=shade_blob(lay, pal, (-1,-1), (1,1))
    l=lay.load()
    if band:
        for i in range(2,n-2,2):
            x,y=pts[i][0],pts[i][1]
            for ox in range(-int(w/2),int(w/2)+1):
                xx,yy=int(round(x+ox)),int(round(y+(ox%2)))
                if 0<=xx<W and 0<=yy<H and l[xx,yy][3] and l[xx,yy][:3]==pal["mid"][:3]: l[xx,yy]=pal["band"]
    if margin:
        for (x,y) in edge_pixels(lay):
            if y < y0-1: l[x,y]=margin
    lay=outline(lay, pal["out"]); target.alpha_composite(lay)

def ovate(x,y,ang,L,Wd):
    a=math.radians(ang); ca,sa=math.cos(a),math.sin(a)
    half=[(0,0),(L*0.15,-Wd*0.35),(L*0.4,-Wd*0.5),(L*0.7,-Wd*0.38),(L*0.9,-Wd*0.15),(L,0)]
    loc=half+[(u,-v) for u,v in half[-2:0:-1]]
    return [(x+u*ca-v*sa, y+u*sa+v*ca) for u,v in loc]

def star(cx,cy,r,rot=0,points=5,inner=0.5):
    pts=[]
    for i in range(points*2):
        rr = r if i%2==0 else r*inner
        a = math.radians(rot + i*180/points - 90)
        pts.append((cx+math.cos(a)*rr, cy+math.sin(a)*rr))
    return pts

# ---------- P16 Lengua de suegra ----------
def g16(seed=16):
    rng=random.Random(seed); img=new()
    pal={"dark":hexc("#24563A"),"mid":hexc("#3A7D52"),"light":hexc("#5FA36E"),"band":hexc("#8CC79A"),"out":hexc("#123222")}
    lv=new()
    for x0,ang,L in [(31,-104,30),(35,-96,40),(40,-90,46),(45,-84,40),(49,-76,30),(38,-110,24),(43,-70,24)]:
        sword(lv, x0, 70, ang, L, 7, pal, rng, band=True, margin=hexc("#E8D96A"))
    img.alpha_composite(lv)
    mound(img, rng)
    return img

# ---------- P17 Nochebuena ----------
def g17(seed=17):
    rng=random.Random(seed); img=new()
    st=new(); d=ImageDraw.Draw(st)
    for a in (-120,-90,-60):
        x1=40+math.cos(math.radians(a))*22; y1=70+math.sin(math.radians(a))*26
        d.line([(40,70),(x1,y1)], fill=hexc("#8A3A2E"), width=2)
    st=outline(st,hexc("#3A1A14")); img.alpha_composite(st)
    G={"dark":hexc("#2E6B34"),"mid":hexc("#468A44"),"light":hexc("#6FB25E"),"hi":hexc("#B6E08F"),"out":hexc("#173A1D")}
    R={"dark":hexc("#A3192B"),"mid":hexc("#D62839"),"light":hexc("#F2546A"),"hi":hexc("#FFB3BE"),"out":hexc("#5A0B14")}
    gl=new()
    for a,(bx,by) in [(-160,(30,50)),(-20,(50,50)),(-140,(28,58)),(-40,(52,58)),(-175,(32,64)),(-5,(48,64))]:
        blob_leaf(gl, ovate(bx,by,a,16,9), G)
    img.alpha_composite(gl)
    rl=new()
    for k,a in enumerate(range(-170,10,30)):
        cx,cy=40,40
        blob_leaf(rl, ovate(cx+math.cos(math.radians(a))*3, cy+math.sin(math.radians(a))*2, a, 15, 8), R)
    for a in (-135,-90,-45):
        blob_leaf(rl, ovate(40,40,a,12,7), R)
    img.alpha_composite(rl)
    for x,y in [(39,39),(41,39),(40,41),(38,41),(42,41)]: px(img,x,y,hexc("#F2D13A"))
    mound(img, rng)
    return img

# ---------- P21 Iris africano ----------
def g21(seed=21):
    rng=random.Random(seed); img=new()
    pal={"dark":hexc("#2C5E3A"),"mid":hexc("#3F7D4C"),"light":hexc("#62A36B"),"band":hexc("#3F7D4C"),"out":hexc("#14301D")}
    lv=new()
    for ang,L,dr in [(-150,30,0.9),(-130,36,0.7),(-112,40,0.4),(-97,44,0.2),(-83,44,0.2),(-68,40,0.4),(-50,36,0.7),(-30,30,0.9)]:
        sword(lv, 40, 70, ang, L, 3.2, pal, rng, band=False, droop=dr)
    img.alpha_composite(lv)
    # flores blancas
    fl=new(); d=ImageDraw.Draw(fl)
    for (sx,sy,tx,ty) in [(42,70,52,26),(38,70,27,32)]:
        d.line([(sx,sy),(tx,ty+3)], fill=hexc("#4F8A4F"))
    fl=outline(fl,hexc("#14301D")); img.alpha_composite(fl)
    WP={"dark":hexc("#D8D8E4"),"mid":hexc("#F4F4FA"),"light":hexc("#FFFFFF"),"hi":hexc("#FFFFFF"),"out":hexc("#7C7C96")}
    for (tx,ty) in [(52,26),(27,32)]:
        pet=new()
        for a in (-100,20,140):
            blob_leaf(pet, ovate(tx,ty,a,8,8), WP)
        for a in (-40,80,200):
            blob_leaf(pet, ovate(tx,ty,a,5,4), WP)
        img.alpha_composite(pet)
        for dx,dy in [(0,0),(1,0),(-1,1),(1,1)]: px(img,tx+dx,ty+dy,hexc("#F2B33A"))
        px(img,tx-3,ty-2,hexc("#E07B39")); px(img,tx+4,ty+1,hexc("#E07B39"))
    mound(img, rng)
    return img

# ---------- P14 Liquidambar (copa de estrellas) ----------
def canopy_stars(img, rng, cx, cy, R):
    G={"dark":hexc("#2F7A3A"),"mid":hexc("#4DA64F"),"light":hexc("#7CCB66"),"hi":hexc("#C2EE95"),"out":hexc("#174A22")}
    cp=new(); d=ImageDraw.Draw(cp)
    d.ellipse([cx-R+3,cy-R*0.8+3,cx+R-3,cy+R*0.8-3], fill=G["mid"])
    for k in range(14):
        a=k*360/14; r=R-4
        sx,sy=cx+math.cos(math.radians(a))*r, cy+math.sin(math.radians(a))*r*0.8
        d.polygon(star(sx,sy,7,rot=rng.uniform(-20,20),inner=0.45), fill=G["mid"])
    cp=shade_blob(cp, G, (-3,-3), (3,3)); l=cp.load()
    for _ in range(10):
        sx,sy=rng.uniform(cx-R+8,cx+R-8), rng.uniform(cy-R*0.6,cy+R*0.5)
        for (x,y) in [(int(p[0]),int(p[1])) for p in star(sx,sy,3,inner=0.4)]:
            if 0<=x<W and 0<=y<H and l[x,y][3]: l[x,y]=G["dark"]
        if l[int(sx),int(sy)][3]: l[int(sx),int(sy)]=G["light"]
    cp=outline(cp, G["out"]); img.alpha_composite(cp)

def g14_mound(seed=14):
    rng=random.Random(seed); img=new()
    tr=new(); d=ImageDraw.Draw(tr)
    d.rectangle([36,30,43,70], fill=hexc("#8A6E58")); d.line([(36,30),(36,70)], fill=hexc("#B39780")); d.line([(43,30),(43,70)], fill=hexc("#5E4838"))
    for y in range(34,70,5): px(tr,39,y,hexc("#5E4838")); px(tr,40,y+1,hexc("#5E4838"))
    tr=outline(tr,hexc("#33251B")); img.alpha_composite(tr)
    canopy_stars(img, rng, 40, 25, 21)
    mound(img, rng)
    return img

def g14_trunk(seed=14):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    BARK={"mid":hexc("#8A6E58"),"light":hexc("#B39780"),"dark":hexc("#5E4838"),"out":hexc("#33251B"),"hi":hexc("#D4BBA4")}
    tr=new(); d=ImageDraw.Draw(tr)
    d.polygon([(28,40),(52,40),(54,82),(60,GROUND),(20,GROUND),(26,82)], fill=BARK["mid"])
    tr=shade_blob(tr, BARK, (-3,-2), (3,2)); l=tr.load()
    for y in range(44,GROUND-2,4):
        for x in (29,33,47,51):
            if l[x,y][3] and l[x,y][:3]==BARK["mid"][:3]: l[x,y]=BARK["dark"]; 
            if l[x,y+1][3] and l[x,y+1][:3]==BARK["mid"][:3]: l[x,y+1]=BARK["dark"]
    tr=outline(tr, BARK["out"]); img.alpha_composite(tr)
    canopy_stars(img, rng, 40, 28, 24)
    g=new(); dg=ImageDraw.Draw(g)
    for x in range(14,68,3): dg.line([(x,GROUND-1),(x+rng.choice([-1,0,1]),GROUND-1-rng.randint(2,4))], fill=GRASS["mid"])
    g=outline(g,GRASS["out"]); img.alpha_composite(g)
    kawaii_face(img, 40, 60, "feliz", gap=13)
    return img

if __name__=="__main__":
    from PIL import ImageFont
    k=4; TW,TH=W*k,H*k; G=16
    F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",20)
    F2=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",30)
    F3=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
    tiles=[("P16 Lengua de suegra","montículo",g16),("P17 Nochebuena","montículo",g17),("P21 Iris africano","montículo",g21),
           ("P14 Liquidambar","montículo",g14_mound),("P14 Liquidambar","cara en el tronco",g14_trunk)]
    S=Image.new("RGBA",(G+5*(TW+G), 80+TH+80),(246,244,236,255)); d=ImageDraw.Draw(S)
    d.text((G,20),"Plantas en suelo · estado feliz",fill=(40,70,45),font=F2)
    for i,(n,sub,fn) in enumerate(tiles):
        x=G+i*(TW+G); y=80
        d.rounded_rectangle([x-4,y-4,x+TW+4,y+TH+4],radius=10,fill=(255,255,255,255),outline=(225,221,208,255))
        im=fn(); S.alpha_composite(im.resize((TW,TH),Image.NEAREST),(x,y))
        d.text((x+4,y+TH+10),n,fill=(40,70,45),font=F); d.text((x+4,y+TH+36),sub,fill=(110,110,110),font=F3)
    S.convert("RGB").save("Plantas en suelo - propuesta.png"); print(S.size)
