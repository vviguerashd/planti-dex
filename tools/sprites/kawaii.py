import math, random
import engine as E
E.W, E.H = 80, 96
W, H = E.W, E.H
GROUND = 90
from engine import hexc, mix
from PIL import Image, ImageDraw

def new(): return Image.new("RGBA",(W,H),(0,0,0,0))
def px(img,x,y,c):
    if 0<=x<W and 0<=y<H: img.putpixel((int(x),int(y)),c)
outline = E.outline

def shade_blob(lay, pal, light_off=(-2,-2), dark_off=(2,2)):
    """sombrea una capa rellena: banda clara arriba-izq y oscura abajo-der"""
    src = lay.load(); out = lay.copy(); o = out.load()
    for y in range(H):
        for x in range(W):
            if src[x,y][3] == 0: continue
            def inside(dx,dy):
                xx,yy=x+dx,y+dy
                return 0<=xx<W and 0<=yy<H and src[xx,yy][3]>0
            if not inside(*dark_off): o[x,y] = pal["dark"]
            elif not inside(*light_off): o[x,y] = pal["light"]
    return out

# ---------- cara kawaii ----------
EYE = hexc("#2B1A14"); IRIS = hexc("#6A4433"); WHITE = hexc("#FFFFFF")
BL1 = hexc("#F59AA6"); BL2 = hexc("#FBC3CB"); MOUTH = hexc("#3A1C16"); TONGUE = hexc("#E86F7E")
EYE_SHAPE = [" XXXXX ","XXXXXXX","XXXXXXX","XXXXXXX","XXXXXXX","XXXXXXX","XXXXXXX"," XXXXX "]
def kawaii_face_feliz(img, cx, cy, gap=15):
    for ex in (cx-gap//2-4, cx+gap//2-2):
        for j,row in enumerate(EYE_SHAPE):
            for i,ch in enumerate(row):
                if ch=="X": px(img, ex+i, cy+j, EYE if j<5 else IRIS)
        for dx,dy in [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(2,3)]: px(img, ex+dx, cy+dy, WHITE)
        px(img, ex+5, cy+5, WHITE); px(img, ex+4, cy+6, WHITE)
    # boca "u" abierta
    my = cy+8
    for x,y,c in [(cx-2,my,MOUTH),(cx+2,my,MOUTH),(cx-2,my+1,MOUTH),(cx+2,my+1,MOUTH),(cx-1,my+2,MOUTH),(cx,my+2,MOUTH),(cx+1,my+2,MOUTH),
                  (cx-1,my+1,TONGUE),(cx,my+1,TONGUE),(cx+1,my+1,TONGUE),(cx-1,my,MOUTH),(cx,my,MOUTH),(cx+1,my,MOUTH)]:
        px(img,x,y,c)
    # chapitas
    for bx in (cx-gap//2-9, cx+gap//2+4):
        for dx in range(5):
            px(img, bx+dx, cy+9, BL1); px(img, bx+dx, cy+10, BL1)
        px(img, bx+1, cy+9, BL2); px(img, bx+2, cy+9, BL2)


SPIRAL=["XXXXXXX","X.....X","X.XXX.X","X.X.X.X","X.X...X","X.XXXXX","X......"," XXXXXX"]
TEAR=hexc("#7CC8F4"); TEAR_D=hexc("#3C86CF")
def kawaii_face(img, cx, cy, state="feliz", gap=15, pot_dark=None):
    if state=="feliz": return kawaii_face_feliz(img,cx,cy,gap)
    L=cx-gap//2-4; R=cx+gap//2-2
    if state=="con_sed":
        for ex in (L,R):
            for j,row in enumerate(EYE_SHAPE):
                if j<1: continue
                for i,ch in enumerate(row):
                    if ch=="X": px(img, ex+i, cy+j, EYE if j<5 else IRIS)
            for dx,dy in [(1,2),(2,2),(1,3),(2,3)]: px(img, ex+dx, cy+dy, WHITE)
            px(img, ex+5, cy+5, WHITE)
        # cejas preocupadas
        for i in range(4): px(img, L+1+i, cy-1-(i//2), EYE); px(img, R+5-i, cy-1-(i//2), EYE)
        # boca ondulada pequeña
        for x,y in [(cx-2,cy+9),(cx-1,cy+8),(cx,cy+9),(cx+1,cy+8),(cx+2,cy+9)]: px(img,x,y,MOUTH)
        for bx in (cx-gap//2-9, cx+gap//2+4):
            for dx in range(4): px(img, bx+dx, cy+9, BL1)
    elif state=="sedienta":
        for ex in (L,R):
            # ojo cerrado triste (arco)
            for i,dy in enumerate([3,2,2,2,2,2,3]): px(img, ex+i, cy+dy, EYE)
            px(img, ex, cy+4, EYE); px(img, ex+6, cy+4, EYE)
            # lágrimas en cascada
            for k in range(6):
                px(img, ex+1, cy+4+k, TEAR); px(img, ex+5, cy+4+k, TEAR)
            px(img, ex+1, cy+10, TEAR_D); px(img, ex+5, cy+10, TEAR_D)
        # boca abierta llorando
        for x,y in [(cx-2,cy+8),(cx-1,cy+7),(cx,cy+7),(cx+1,cy+7),(cx+2,cy+8),(cx-2,cy+9),(cx+2,cy+9),(cx-1,cy+10),(cx,cy+10),(cx+1,cy+10)]: px(img,x,y,MOUTH)
        for x,y in [(cx-1,cy+8),(cx,cy+8),(cx+1,cy+8),(cx-1,cy+9),(cx,cy+9),(cx+1,cy+9)]: px(img,x,y,TONGUE if y==cy+9 else MOUTH)
    elif state=="enferma":
        for ex in (L,R):
            for j,row in enumerate(SPIRAL):
                for i,ch in enumerate(row):
                    if ch=="X": px(img, ex+i, cy+j, EYE)
        # termómetro en la boca
        T=hexc("#E9ECEF"); RD=hexc("#E0393E"); O=hexc("#555B66")
        for k in range(9):
            x,y=cx-1+k, cy+9-k//2
            px(img,x,y,T); px(img,x,y-1,O); px(img,x,y+1,O)
        px(img,cx-2,cy+9,RD); px(img,cx-1,cy+9,RD); px(img,cx-2,cy+10,O); px(img,cx-1,cy+10,O); px(img,cx-3,cy+9,O)
        for x,y in [(cx-3,cy+8),(cx-2,cy+8),(cx-3,cy+10),(cx-2,cy+11)]: px(img,x,y,MOUTH)
        for bx in (cx-gap//2-9, cx+gap//2+4):
            for dx in range(5): px(img, bx+dx, cy+9, hexc("#B9D98F")); px(img, bx+dx, cy+10, hexc("#B9D98F"))

def ground_shadow(img, cx, w):
    sh = new(); ImageDraw.Draw(sh).ellipse([cx-w//2, GROUND-2, cx+w//2, GROUND+2], fill=(30,30,30,60)); img.alpha_composite(sh)

def blob_leaf(target, poly, pal, cream=None, rng=None):
    lay = new(); ImageDraw.Draw(lay).polygon(poly, fill=pal["mid"])
    lay = shade_blob(lay, pal, (-1,-2), (1,2))
    l = lay.load()
    # nervio y vetas
    cx = sum(p[0] for p in poly)/len(poly); cy = sum(p[1] for p in poly)/len(poly)
    if cream and rng:
        for _ in range(2):
            x0,y0 = cx+rng.uniform(-2,2), cy+rng.uniform(-2,1)
            for k in range(3):
                xx,yy=int(x0+k*0.8),int(y0-k*0.6)
                if 0<=xx<W and 0<=yy<H and l[xx,yy][3]: l[xx,yy]=cream
    # brillo
    hx,hy = int(cx-1), int(cy-2)
    for xx in (hx,hx+1):
        if 0<=xx<W and 0<=hy<H and l[xx,hy][3]: l[xx,hy]=pal["hi"]
    lay = outline(lay, pal["out"]); target.alpha_composite(lay)

def heart(x,y,ang,L,Wd):
    a=math.radians(ang); ca,sa=math.cos(a),math.sin(a)
    half=[(L*0.12,0),(0,-Wd*0.3),(L*0.07,-Wd*0.47),(L*0.24,-Wd*0.53),(L*0.45,-Wd*0.46),(L*0.68,-Wd*0.3),(L*0.87,-Wd*0.13),(L,0)]
    loc=half+[(u,-v) for u,v in half[-2:0:-1]]
    return [(x+u*ca-v*sa, y+u*sa+v*ca) for u,v in loc]

LEAF_P = {"dark":hexc("#2E7A33"),"mid":hexc("#4FA544"),"light":hexc("#7FCB5C"),"hi":hexc("#C3EE8A"),"out":hexc("#1D4A22")}

# ---------- P01 pothos kawaii ----------
def k01(seed=11):
    rng=random.Random(seed); img=new()
    ORG={"mid":hexc("#E8743F"),"light":hexc("#F7A06A"),"dark":hexc("#B9542A"),"out":hexc("#6B2A14"),"hi":hexc("#FFD2B0")}
    hang=new(); d=ImageDraw.Draw(hang)
    for a,b in [((40,8),(16,40)),((40,8),(64,40))]: d.line([a,b],fill=ORG["mid"])
    for x,y in [(39,1),(40,0),(41,0),(42,1),(42,2),(41,3),(40,4),(40,5),(40,6),(40,7),(39,8),(40,8),(41,8)]: px(hang,x,y,ORG["mid"])
    hang=outline(hang,ORG["out"]); img.alpha_composite(hang)
    # mechón de hojas arriba
    tuft=new()
    for a,L in [(-165,13),(-140,14),(-112,15),(-88,15),(-66,15),(-40,14),(-15,13)]:
        bx=40+math.cos(math.radians(a))*8; by=38+math.sin(math.radians(a))*3
        blob_leaf(tuft, heart(bx,by,a,L,11), LEAF_P, cream=hexc("#F3E7A2"), rng=rng)
    img.alpha_composite(tuft)
    # maceta regordeta (media esfera)
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([14,24,66,72], fill=ORG["mid"])
    d.rectangle([12,38,68,43], fill=ORG["mid"])
    cut=pot.load()
    for y in range(0,38):
        for x in range(W): cut[x,y]=(0,0,0,0)
    pot=shade_blob(pot, ORG, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(13,38),(67,38)], fill=ORG["hi"]); d.line([(13,43),(67,43)], fill=ORG["dark"])
    pot=outline(pot, ORG["out"]); img.alpha_composite(pot)
    # guías colgantes con hojas grandes
    vl=new(); dv=ImageDraw.Draw(vl); jobs=[]
    for (x,y,a,L) in [(16,42,106,40),(64,42,74,38),(25,57,96,24),(55,57,84,26)]:
        pts=E.curve(x,y,a,L,0.9,steps=16)
        dv.line([(p[0],p[1]) for p in pts], fill=hexc("#5E9E3E"))
        side=1
        for i in range(4,len(pts),4):
            px_,py_,dx,dy=pts[i]; va=math.degrees(math.atan2(dy,dx))
            jobs.append((px_,py_,90+side*rng.uniform(30,50),11,10)); side*=-1
    vl=outline(vl,hexc("#24401C")); img.alpha_composite(vl)
    vv=new()
    for bx,by,la,L,Wd in jobs: blob_leaf(vv, heart(bx,by,la,L,Wd), LEAF_P, cream=hexc("#F3E7A2"), rng=rng)
    img.alpha_composite(vv)
    kawaii_face(img, 40, 46)
    return img

# ---------- P03 limonero kawaii ----------
def k03(seed=13):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    CP={"dark":hexc("#3E8A3A"),"mid":hexc("#5DB04E"),"light":hexc("#8AD46A"),"hi":hexc("#CFF39A"),"out":hexc("#1F4F24")}
    # tronco
    tr=new(); d=ImageDraw.Draw(tr)
    d.rectangle([38,30,41,60], fill=hexc("#9A8672")); d.line([(38,30),(38,60)], fill=hexc("#C2B19C")); d.line([(41,30),(41,60)], fill=hexc("#6E5E50"))
    d.line([(39,40),(31,32)], fill=hexc("#9A8672"), width=2); d.line([(40,38),(49,30)], fill=hexc("#9A8672"), width=2)
    tr=outline(tr,hexc("#3A2F26")); img.alpha_composite(tr)
    # copa redonda tipo nube
    cp=new(); d=ImageDraw.Draw(cp)
    for (x,y,r) in [(40,20,15),(27,25,10),(53,25,10),(33,12,9),(48,12,9),(40,30,9)]:
        d.ellipse([x-r,y-r,x+r,y+r], fill=CP["mid"])
    cp=shade_blob(cp, CP, (-3,-3), (3,3))
    l=cp.load()
    # textura de hojitas
    for _ in range(70):
        x,y=rng.randint(14,66),rng.randint(2,40)
        if l[x,y][3] and l[x,y][:3]==CP["mid"][:3]:
            l[x,y]=CP["light"]; 
            if x+1<W and l[x+1,y][3]: l[x+1,y]=CP["dark"]
    for _ in range(14):
        x,y=rng.randint(18,62),rng.randint(4,32)
        if l[x,y][3] and l[x,y][:3]!=CP["dark"][:3]: l[x,y]=CP["hi"]
    cp=outline(cp, CP["out"]); img.alpha_composite(cp)
    # limones
    LEM={"mid":hexc("#FFD93D"),"dark":hexc("#E0A91E"),"hi":hexc("#FFF6B8"),"out":hexc("#7A5A14")}
    lm=new()
    for (x,y) in [(29,26),(51,22),(41,33)]:
        dl=ImageDraw.Draw(lm); dl.ellipse([x-3,y-3,x+3,y+4], fill=LEM["mid"])
        px(lm,x+2,y+2,LEM["dark"]); px(lm,x+1,y+3,LEM["dark"]); px(lm,x+3,y+1,LEM["dark"]); px(lm,x-1,y-1,LEM["hi"]); px(lm,x-2,y,LEM["hi"])
        px(lm,x,y-4,hexc("#3E8A3A"))
    lm=outline(lm,LEM["out"]); img.alpha_composite(lm)
    # maceta regordeta verde
    GP={"mid":hexc("#3F8A5A"),"light":hexc("#68B57F"),"dark":hexc("#2B6442"),"out":hexc("#123522"),"hi":hexc("#A7DDB5")}
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([12,48,68,98], fill=GP["mid"])
    c=pot.load()
    for y in range(0,58):
        for x in range(W): c[x,y]=(0,0,0,0)
    for y in range(GROUND,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    d=ImageDraw.Draw(pot); d.rounded_rectangle([9,55,71,61], radius=2, fill=GP["mid"])
    pot=shade_blob(pot, GP, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(10,55),(70,55)], fill=GP["hi"]); d.line([(10,61),(70,61)], fill=GP["dark"])
    pot=outline(pot, GP["out"])
    soil=new(); ImageDraw.Draw(soil).rectangle([12,53,68,54], fill=hexc("#5A3E2B"))
    img.alpha_composite(soil); img.alpha_composite(pot)
    kawaii_face(img, 40, 66)
    return img

# ---------- P07 palo de Brasil kawaii ----------
CROWN=28
def k07(seed=17):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,44)
    DP={"dark":hexc("#2F6E34"),"mid":hexc("#459150"),"light":hexc("#6CB86A"),"hi":hexc("#B5E59A"),"out":hexc("#173A1D"),"rib":hexc("#8FD07A")}
    cane=new(); d=ImageDraw.Draw(cane)
    d.rectangle([37,CROWN,42,58], fill=hexc("#C9A272")); d.line([(37,CROWN),(37,58)], fill=hexc("#E6C899")); d.line([(42,CROWN),(42,58)], fill=hexc("#9A7448"))
    for y in range(CROWN+3,58,4): d.line([(37,y),(42,y)], fill=hexc("#9A7448"))
    cane=outline(cane,hexc("#4A3220"))
    leaves=new()
    specs=[(-178,30,9,1.05),(-2,30,9,1.05),(-150,30,9,0.8),(-30,30,9,0.8),(-122,26,9,0.55),(-58,26,9,0.55),(-98,20,8,0.3),(-82,20,8,0.3)]
    for a,L,w,dr in specs:
        pts=E.curve(40,CROWN+1,a,L,dr,steps=18)
        lay=new(); dd=ImageDraw.Draw(lay)
        left=[];right=[];n=len(pts)-1
        for i,(x,y,dx,dy) in enumerate(pts):
            t=i/n; ww=w*(0.6+0.4*math.sin(math.pi*min(1,t*1.1)))*(1-t**4)+0.6
            nx,ny=-dy,dx; left.append((x+nx*ww/2,y+ny*ww/2)); right.append((x-nx*ww/2,y-ny*ww/2))
        dd.polygon(left+right[::-1], fill=DP["mid"])
        lay=shade_blob(lay, DP, (-1,-2), (1,2))
        dd=ImageDraw.Draw(lay); dd.line([(p[0],p[1]) for p in pts[2:-3]], fill=DP["rib"])
        lay=outline(lay, DP["out"]); leaves.alpha_composite(lay)
    img.alpha_composite(leaves); img.alpha_composite(cane)
    # maceta blanca regordeta tipo urna
    WP={"mid":hexc("#F1EEE6"),"light":hexc("#FFFFFF"),"dark":hexc("#CFC8B6"),"out":hexc("#7A7262"),"hi":hexc("#FFFFFF")}
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([14,50,66,100], fill=WP["mid"])
    c=pot.load()
    for y in range(0,60):
        for x in range(W): c[x,y]=(0,0,0,0)
    for y in range(GROUND-2,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    d=ImageDraw.Draw(pot)
    d.rectangle([26,86,54,89], fill=WP["dark"])
    d.rounded_rectangle([10,56,70,62], radius=2, fill=WP["mid"])
    pot=shade_blob(pot, WP, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(11,56),(69,56)], fill=WP["light"]); d.line([(11,62),(69,62)], fill=WP["dark"])
    pl=pot.load()
    for x in range(18,64,5):
        for y in range(64,86):
            if pl[x,y][3] and pl[x,y][:3]==WP["mid"][:3] and not (26<x<54 and 66<y<80): pl[x,y]=WP["dark"]
    pot=outline(pot, WP["out"])
    soil=new(); ImageDraw.Draw(soil).rectangle([13,54,67,55], fill=hexc("#5A3E2B"))
    img.alpha_composite(soil); img.alpha_composite(pot)
    kawaii_face(img, 40, 67)
    return img

if __name__=="__main__":
    from PIL import ImageFont
    k=4
    tiles=[(n,f()) for n,f in [("P01 Pothos",k01),("P03 Limonero",k03),("P07 Palo de Brasil",k07)]]
    S=Image.new("RGBA",(16+3*(W*k+16), H*k+70),(246,244,236,255)); d=ImageDraw.Draw(S)
    F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",20)
    for i,(n,t) in enumerate(tiles):
        x=16+i*(W*k+16)
        d.rounded_rectangle([x-4,12,x+W*k+4,16+H*k+4],radius=10,fill=(255,255,255,255),outline=(225,221,208,255))
        S.alpha_composite(t.resize((W*k,H*k),Image.NEAREST),(x,16))
        d.text((x+4,H*k+30),n,fill=(40,70,45),font=F)
        t.resize((W*k,H*k),Image.NEAREST).save(f"out/{n.split()[0]}_kawaii_feliz.png")
    S.convert("RGB").save("Kawaii feliz - P01 P03 P07.png"); print(S.size)
