# Plantitas tamagochi: sprites kawaii 16-bit con 4 estados (80x96 nativo)
import math, random
from kawaii import *          # new, px, shade_blob, outline, blob_leaf, heart, kawaii_face, ground_shadow, LEAF_P, E, W, H, GROUND
from engine import hexc, mix, bubble, drop as small_drop
from PIL import Image, ImageDraw

STATES = ["feliz","con_sed","sedienta","enferma"]
YEL = hexc("#D9C35A"); BRN = hexc("#8A5A2B")
SHIFT = {"feliz":0.0,"con_sed":0.15,"sedienta":0.5,"enferma":0.08}
BIAS  = {"feliz":0.0,"con_sed":0.35,"sedienta":0.85,"enferma":0.25}

def spal(base, state):
    t = SHIFT[state]
    p = {k:(mix(v,YEL,t) if k!="out" else v) for k,v in base.items()}
    if state=="sedienta": p["dark"]=mix(base["dark"],BRN,0.45); p["out"]=mix(base["out"],hexc("#3A2A14"),0.5)
    return p

def spots(layer, rng, n):
    l = layer.load(); done=0; tries=0
    while done<n and tries<4000:
        tries+=1
        x,y = rng.randint(2,W-4), rng.randint(2,H-12)
        ok = all(l[x+dx,y+dy][3] for dx in (-1,0,1,2) for dy in (-1,0,1,2))
        if not ok: continue
        for dx,dy in [(-1,-1),(0,-1),(1,-1),(2,-1),(-1,0),(2,0),(-1,1),(2,1),(-1,2),(0,2),(1,2),(2,2)]: l[x+dx,y+dy]=hexc("#C9B54A")
        for dx,dy in [(0,0),(1,0),(0,1),(1,1)]: l[x+dx,y+dy]=hexc("#6B4423")
        done+=1

def big_drop(img, x, y):
    T=hexc("#7CC8F4"); D=hexc("#3C86CF"); O=hexc("#1F4E80"); WH=hexc("#FFFFFF")
    shape=["  X  "," XXX ","XXXXX","XXXXX"," XXX "]
    for j,row in enumerate(shape):
        for i,ch in enumerate(row):
            if ch=="X": px(img,x+i,y+j,T)
    for dx,dy in [(3,3),(2,4),(3,4),(4,3)]: px(img,x+dx,y+dy,D)
    px(img,x+1,y+2,WH)
    for dx,dy in [(2,-1),(1,0),(3,0),(0,1),(4,1),(-1,2),(5,2),(-1,3),(5,3),(0,4),(4,4),(1,5),(2,5),(3,5)]: px(img,x+dx,y+dy,O)

def bandaid(img, x, y):
    B=hexc("#F2C49B"); Bd=hexc("#D79A68"); O=hexc("#9A6A44")
    lay=new()
    for k in range(9):
        for w in range(3): px(lay,x+k,y+4-k//2+w,B)
    for k in (3,4,5):
        for w in range(3): px(lay,x+k,y+4-k//2+w,Bd)
    px(lay,x+1,y+5,O); px(lay,x+7,y+2,O)
    img.alpha_composite(outline(lay,O))

def fallen_leaf(img, x, y, pal, flip=False):
    lay=new(); blob_leaf(lay, heart(x,y,180 if flip else 0,8,6), pal); img.alpha_composite(lay)

def overlays(img, state, bpos, sweat, ground_leaves=True, leafpal=None):
    if state=="con_sed":
        bubble(img,*bpos); big_drop(img,*sweat)
    elif state=="sedienta":
        bubble(img,*bpos,alert=True)
        if ground_leaves and leafpal:
            fallen_leaf(img, 4, GROUND-3, leafpal); fallen_leaf(img, 75, GROUND-2, leafpal, flip=True)

def soil_strip(img, x0, x1, y, state):
    s=new(); d=ImageDraw.Draw(s)
    if state=="sedienta":
        d.rectangle([x0,y,x1,y+1], fill=hexc("#A88462"))
        for x in range(x0+3,x1-2,7): px(s,x,y,hexc("#4A3220")); px(s,x+1,y+1,hexc("#4A3220"))
    else:
        d.rectangle([x0,y,x1,y+1], fill=hexc("#5A3E2B"))
    img.alpha_composite(s)

# ---------------- P01 Pothos ----------------
def k01(state="feliz", seed=11):
    rng=random.Random(seed); img=new(); b=BIAS[state]; pal=spal(LEAF_P,state)
    keep={"feliz":1,"con_sed":1,"sedienta":0.72,"enferma":0.95}[state]
    ORG={"mid":hexc("#E8743F"),"light":hexc("#F7A06A"),"dark":hexc("#B9542A"),"out":hexc("#6B2A14"),"hi":hexc("#FFD2B0")}
    hang=new(); d=ImageDraw.Draw(hang)
    for a,c in [((40,8),(16,40)),((40,8),(64,40))]: d.line([a,c],fill=ORG["mid"])
    for x,y in [(39,1),(40,0),(41,0),(42,1),(42,2),(41,3),(40,4),(40,5),(40,6),(40,7),(39,8),(40,8),(41,8)]: px(hang,x,y,ORG["mid"])
    hang=outline(hang,ORG["out"]); img.alpha_composite(hang)
    tuft=new()
    for a,L in [(-165,13),(-140,14),(-112,15),(-88,15),(-66,15),(-40,14),(-15,13)]:
        if rng.random()>keep: continue
        a2 = a + b*((-195 if a<-90 else 15) - a)*0.55
        bx=40+math.cos(math.radians(a))*8; by=38+math.sin(math.radians(a))*3
        blob_leaf(tuft, heart(bx,by,a2,L,11), pal, cream=hexc("#F3E7A2"), rng=rng)
    if state=="enferma": spots(tuft, rng, 2)
    img.alpha_composite(tuft)
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([14,24,66,72], fill=ORG["mid"]); d.rectangle([12,38,68,43], fill=ORG["mid"])
    c=pot.load()
    for y in range(0,38):
        for x in range(W): c[x,y]=(0,0,0,0)
    pot=shade_blob(pot, ORG, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(13,38),(67,38)], fill=ORG["hi"]); d.line([(13,43),(67,43)], fill=ORG["dark"])
    pot=outline(pot, ORG["out"]); img.alpha_composite(pot)
    vl=new(); dv=ImageDraw.Draw(vl); jobs=[]
    for (x,y,a,L) in [(16,42,106,40),(64,42,74,38),(25,57,96,24),(55,57,84,26)]:
        pts=E.curve(x,y,a,L*(1.08 if state=="sedienta" else 1),0.9+b,steps=16)
        dv.line([(p[0],p[1]) for p in pts], fill=mix(hexc("#5E9E3E"),YEL,SHIFT[state]))
        side=1
        for i in range(4,len(pts),4):
            if rng.random()>keep: side*=-1; continue
            px_,py_,dx,dy=pts[i]
            jobs.append((px_,py_,90+side*rng.uniform(30,50)*(1-b*0.6),11,10)); side*=-1
    vl=outline(vl,hexc("#24401C")); img.alpha_composite(vl)
    vv=new()
    for bx,by,la,L,Wd in jobs: blob_leaf(vv, heart(bx,by,la,L,Wd), pal, cream=hexc("#F3E7A2"), rng=rng)
    if state=="enferma": spots(vv, rng, 4)
    img.alpha_composite(vv)
    kawaii_face(img, 40, 46, state)
    if state=="enferma": bandaid(img, 17, 46)
    overlays(img, state, bpos=(64,4), sweat=(62,46), leafpal=spal(LEAF_P,"sedienta"))
    return img

# ---------------- P03 Limonero ----------------
def k03(state="feliz", seed=13):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    CP=spal({"dark":hexc("#3E8A3A"),"mid":hexc("#5DB04E"),"light":hexc("#8AD46A"),"hi":hexc("#CFF39A"),"out":hexc("#1F4F24")},state)
    sag={"feliz":0,"con_sed":1,"sedienta":4,"enferma":1}[state]; shrink={"feliz":1,"con_sed":0.97,"sedienta":0.86,"enferma":0.97}[state]
    tr=new(); d=ImageDraw.Draw(tr)
    d.rectangle([38,30,41,60], fill=hexc("#9A8672")); d.line([(38,30),(38,60)], fill=hexc("#C2B19C")); d.line([(41,30),(41,60)], fill=hexc("#6E5E50"))
    d.line([(39,40),(31,32+sag)], fill=hexc("#9A8672"), width=2); d.line([(40,38),(49,30+sag)], fill=hexc("#9A8672"), width=2)
    tr=outline(tr,hexc("#3A2F26")); img.alpha_composite(tr)
    cp=new(); d=ImageDraw.Draw(cp)
    for (x,y,r) in [(40,20,15),(27,25,10),(53,25,10),(33,12,9),(48,12,9),(40,30,9)]:
        r2=r*shrink; y2=y+sag+(y-20)*(1-shrink)
        d.ellipse([x-r2,y2-r2,x+r2,y2+r2], fill=CP["mid"])
    cp=shade_blob(cp, CP, (-3,-3), (3,3)); l=cp.load()
    for _ in range(70):
        x,y=rng.randint(14,66),rng.randint(2,44)
        if l[x,y][3] and l[x,y][:3]==CP["mid"][:3]:
            l[x,y]=CP["light"]
            if x+1<W and l[x+1,y][3]: l[x+1,y]=CP["dark"]
    for _ in range(14):
        x,y=rng.randint(18,62),rng.randint(4,36)
        if l[x,y][3] and l[x,y][:3]!=CP["dark"][:3]: l[x,y]=CP["hi"]
    if state=="enferma": spots(cp, rng, 5)
    cp=outline(cp, CP["out"]); img.alpha_composite(cp)
    LEM={"mid":hexc("#FFD93D"),"dark":hexc("#E0A91E"),"hi":hexc("#FFF6B8"),"out":hexc("#7A5A14")}
    lemons=[(29,26+sag),(51,22+sag),(41,33+sag)]
    if state=="sedienta": lemons=lemons[:2]
    lm=new()
    for (x,y) in lemons:
        dl=ImageDraw.Draw(lm); dl.ellipse([x-3,y-3,x+3,y+4], fill=LEM["mid"])
        px(lm,x+2,y+2,LEM["dark"]); px(lm,x+1,y+3,LEM["dark"]); px(lm,x+3,y+1,LEM["dark"]); px(lm,x-1,y-1,LEM["hi"]); px(lm,x-2,y,LEM["hi"])
        px(lm,x,y-4,hexc("#3E8A3A"))
    if state=="sedienta":
        dl=ImageDraw.Draw(lm); x,y=70,GROUND-4; dl.ellipse([x-3,y-3,x+3,y+3], fill=LEM["dark"]); px(lm,x-1,y-1,LEM["mid"])
    lm=outline(lm,LEM["out"]); img.alpha_composite(lm)
    GP={"mid":hexc("#3F8A5A"),"light":hexc("#68B57F"),"dark":hexc("#2B6442"),"out":hexc("#123522"),"hi":hexc("#A7DDB5")}
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([12,48,68,98], fill=GP["mid"]); c=pot.load()
    for y in range(0,58):
        for x in range(W): c[x,y]=(0,0,0,0)
    for y in range(GROUND,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    d=ImageDraw.Draw(pot); d.rounded_rectangle([9,55,71,61], radius=2, fill=GP["mid"])
    pot=shade_blob(pot, GP, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(10,55),(70,55)], fill=GP["hi"]); d.line([(10,61),(70,61)], fill=GP["dark"])
    pot=outline(pot, GP["out"])
    soil_strip(img, 12, 68, 53, state); img.alpha_composite(pot)
    kawaii_face(img, 40, 66, state)
    if state=="enferma": bandaid(img, 15, 66)
    lp=spal({"dark":hexc("#3E8A3A"),"mid":hexc("#5DB04E"),"light":hexc("#8AD46A"),"hi":hexc("#CFF39A"),"out":hexc("#1F4F24")},"sedienta")
    if state=="sedienta": fallen_leaf(img, 4, GROUND-3, lp)
    overlays(img, state, bpos=(66,38), sweat=(70,63), ground_leaves=False)
    return img

# ---------------- P07 Palo de Brasil ----------------
CROWN=28
def k07(state="feliz", seed=17):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,44)
    base={"dark":hexc("#2F6E34"),"mid":hexc("#459150"),"light":hexc("#6CB86A"),"hi":hexc("#B5E59A"),"out":hexc("#173A1D")}
    DP=spal(base,state); rib=mix(hexc("#8FD07A"),YEL,SHIFT[state])
    mult={"feliz":1.0,"con_sed":1.4,"sedienta":2.6,"enferma":1.2}[state]
    cane=new(); d=ImageDraw.Draw(cane)
    d.rectangle([37,CROWN,42,58], fill=hexc("#C9A272")); d.line([(37,CROWN),(37,58)], fill=hexc("#E6C899")); d.line([(42,CROWN),(42,58)], fill=hexc("#9A7448"))
    for y in range(CROWN+3,58,4): d.line([(37,y),(42,y)], fill=hexc("#9A7448"))
    cane=outline(cane,hexc("#4A3220"))
    leaves=new()
    specs=[(-178,30,9,1.05),(-2,30,9,1.05),(-150,30,9,0.8),(-30,30,9,0.8),(-122,26,9,0.55),(-58,26,9,0.55),(-98,20,8,0.3),(-82,20,8,0.3)]
    for a,L,w,dr in specs:
        pts=E.curve(40,CROWN+1,a,L,dr*mult,steps=18)
        lay=new(); dd=ImageDraw.Draw(lay)
        left=[];right=[];n=len(pts)-1
        for i,(x,y,dx,dy) in enumerate(pts):
            t=i/n; ww=w*(0.6+0.4*math.sin(math.pi*min(1,t*1.1)))*(1-t**4)+0.6
            nx,ny=-dy,dx; left.append((x+nx*ww/2,y+ny*ww/2)); right.append((x-nx*ww/2,y-ny*ww/2))
        dd.polygon(left+right[::-1], fill=DP["mid"])
        if state=="sedienta":
            k=int(n*0.72); dd.polygon(left[k:]+right[k:][::-1], fill=hexc("#A9773F"))
        lay=shade_blob(lay, DP, (-1,-2), (1,2))
        dd=ImageDraw.Draw(lay); dd.line([(p[0],p[1]) for p in pts[2:-5]], fill=rib)
        lay=outline(lay, DP["out"]); leaves.alpha_composite(lay)
    if state=="enferma": spots(leaves, rng, 5)
    img.alpha_composite(leaves); img.alpha_composite(cane)
    WP={"mid":hexc("#F1EEE6"),"light":hexc("#FFFFFF"),"dark":hexc("#CFC8B6"),"out":hexc("#7A7262"),"hi":hexc("#FFFFFF")}
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([14,50,66,100], fill=WP["mid"]); c=pot.load()
    for y in range(0,60):
        for x in range(W): c[x,y]=(0,0,0,0)
    for y in range(GROUND-2,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    d=ImageDraw.Draw(pot); d.rectangle([26,86,54,89], fill=WP["dark"]); d.rounded_rectangle([10,56,70,62], radius=2, fill=WP["mid"])
    pot=shade_blob(pot, WP, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(11,56),(69,56)], fill=WP["light"]); d.line([(11,62),(69,62)], fill=WP["dark"])
    pl=pot.load()
    for x in range(18,64,5):
        for y in range(64,86):
            if pl[x,y][3] and pl[x,y][:3]==WP["mid"][:3] and not (26<x<54 and 66<y<80): pl[x,y]=WP["dark"]
    pot=outline(pot, WP["out"])
    soil_strip(img, 13, 67, 54, state); img.alpha_composite(pot)
    # en sedienta las hojas caen por delante de la maceta: redibujar las puntas encima
    if state=="sedienta":
        front=leaves.copy(); f=front.load()
        for y in range(0,57):
            for x in range(W): f[x,y]=(0,0,0,0)
        for y in range(57,H):
            for x in range(26,55): f[x,y]=(0,0,0,0)
        img.alpha_composite(front)
    kawaii_face(img, 40, 67, state)
    if state=="enferma": bandaid(img, 16, 66)
    overlays(img, state, bpos=(66,2), sweat=(68,62), leafpal=spal(base,"sedienta"))
    return img

if __name__=="__main__":
    import os
    from PIL import ImageFont
    k=4; os.makedirs("kawaii_out",exist_ok=True)
    F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",20)
    F2=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",30)
    rows=[("P01","Pothos colgante (escalera)",k01),("P03","Limonero",k03),("P07","Palo de Brasil (maceta blanca)",k07)]
    labels=["Feliz","Con sed","Sedienta","Enferma"]
    TW,TH=W*k,H*k; G=16
    S=Image.new("RGBA",(G+4*(TW+G), 80+len(rows)*(TH+90)),(246,244,236,255)); d=ImageDraw.Draw(S)
    d.text((G,20),"Plantitas tamagochi · kawaii 16-bit · 4 estados",fill=(40,70,45),font=F2)
    y=80
    for pid,name,fn in rows:
        d.text((G,y),f"{pid}  {name}",fill=(30,30,30),font=F); y+=34
        for i,st in enumerate(STATES):
            im=fn(st); up=im.resize((TW,TH),Image.NEAREST)
            up.save(f"kawaii_out/{pid}_{st}.png")
            x=G+i*(TW+G)
            d.rounded_rectangle([x-4,y-4,x+TW+4,y+TH+4],radius=10,fill=(255,255,255,255),outline=(225,221,208,255))
            S.alpha_composite(up,(x,y)); d.text((x+4,y+TH+10),labels[i],fill=(40,70,45),font=F)
        y+=TH+56
    S.convert("RGB").save("Kawaii estados - P01 P03 P07.png"); print(S.size)
