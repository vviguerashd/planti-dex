# Plantitas tamagochi: las 23 plantas kawaii 16-bit con 4 estados (80x96 nativo, se exporta x4)
import math, random
from kawaii_states import *            # k01, k03, k07, spal, spots, big_drop, bandaid, fallen_leaf, overlays, soil_strip, STATES, SHIFT, BIAS
import ground as GR
from ground import mound, sword, ovate, star, GRASS
from engine import hexc, mix
from PIL import Image, ImageDraw

def face(img, cx, cy, state, ring=None, gap=15):
    t=new(); kawaii_face(t,cx,cy,state,gap=gap)
    if ring: t=outline(t, ring)
    img.alpha_composite(t)

def finish(img, state, fxy, bpos, sweat, band=None, leafpal=None, ring=None, gap=15, fallen=True):
    face(img, fxy[0], fxy[1], state, ring, gap)
    if state=="enferma" and band: bandaid(img, *band)
    overlays(img, state, bpos=bpos, sweat=sweat, ground_leaves=fallen, leafpal=leafpal)
    return img

def P(mid, light, dark, out, hi=None):
    return {"mid":hexc(mid),"light":hexc(light),"dark":hexc(dark),"out":hexc(out),"hi":hexc(hi or light)}

def pot_round(img, Pp, rim=55, x0=12, x1=68, ribs=False, flutes=False, state="feliz"):
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([x0, rim-7, x1, rim+43], fill=Pp["mid"]); c=pot.load()
    for y in range(0,rim+3):
        for x in range(W): c[x,y]=(0,0,0,0)
    for y in range(GROUND,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    d=ImageDraw.Draw(pot); d.rounded_rectangle([x0-3,rim,x1+3,rim+6], radius=2, fill=Pp["mid"])
    pot=shade_blob(pot, Pp, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(x0-2,rim),(x1+2,rim)], fill=Pp["hi"]); d.line([(x0-2,rim+6),(x1+2,rim+6)], fill=Pp["dark"])
    pl=pot.load()
    if ribs:
        for x in range(x0-1,x1+3,3):
            for y in (rim+2,rim+3,rim+4):
                if pl[x,y][3]: pl[x,y]=Pp["dark"]
    if flutes:
        for x in range(x0+6,x1-4,5):
            for y in range(rim+9,GROUND-3):
                if pl[x,y][3] and pl[x,y][:3]==Pp["mid"][:3] and not (x0+14<x<x1-14 and rim+10<y<rim+25): pl[x,y]=Pp["dark"]
    pot=outline(pot, Pp["out"])
    soil_strip(img, x0, x1, rim-2, state); img.alpha_composite(pot)

def pot_hanging(img, Pp, wire, top=38, hook_y=0, stone=None):
    hang=new(); d=ImageDraw.Draw(hang)
    for a,c in [((40,hook_y+8),(16,top+2)),((40,hook_y+8),(64,top+2))]: d.line([a,c],fill=wire["mid"])
    for x,y in [(39,1),(40,0),(41,0),(42,1),(42,2),(41,3),(40,4),(40,5),(40,6),(40,7),(39,8),(40,8),(41,8)]: px(hang,x,y+hook_y,wire["mid"])
    hang=outline(hang,wire["out"]); img.alpha_composite(hang)

def pot_hanging_body(img, Pp, top=38):
    pot=new(); d=ImageDraw.Draw(pot)
    d.ellipse([14,top-14,66,top+34], fill=Pp["mid"]); d.rectangle([12,top,68,top+5], fill=Pp["mid"])
    c=pot.load()
    for y in range(0,top):
        for x in range(W): c[x,y]=(0,0,0,0)
    pot=shade_blob(pot, Pp, (-3,-3), (3,3))
    d=ImageDraw.Draw(pot); d.line([(13,top),(67,top)], fill=Pp["hi"]); d.line([(13,top+5),(67,top+5)], fill=Pp["dark"])
    pot=outline(pot, Pp["out"]); img.alpha_composite(pot)

def heart_leaves(target, jobs, pal, rng, cream=None):
    for bx,by,la,L,Wd in jobs: blob_leaf(target, heart(bx,by,la,L,Wd), pal, cream=cream, rng=rng)

def vines(img, rng, specs, pal, state, keep, cream, droop=0.9):
    b=BIAS[state]; vl=new(); dv=ImageDraw.Draw(vl); jobs=[]
    for (x,y,a,L) in specs:
        pts=E.curve(x,y,a,L*(1.08 if state=="sedienta" else 1),droop+b,steps=16)
        dv.line([(p[0],p[1]) for p in pts], fill=mix(hexc("#5E9E3E"),YEL,SHIFT[state]))
        side=1
        for i in range(4,len(pts),4):
            if rng.random()>keep: side*=-1; continue
            jobs.append((pts[i][0],pts[i][1],90+side*rng.uniform(30,50)*(1-b*0.6),11,10)); side*=-1
    vl=outline(vl,hexc("#24401C")); img.alpha_composite(vl)
    vv=new(); heart_leaves(vv, jobs, pal, rng, cream)
    if state=="enferma": spots(vv, rng, 3)
    img.alpha_composite(vv)

KEEP={"feliz":1,"con_sed":1,"sedienta":0.72,"enferma":0.95}

# ======== P02 Pothos colgante (piedra) ========
LIGHTPOTHOS = P("#78B84A","#A6D86A","#4E8F33","#2B5A1E","#DDF5A8")
def p02(state, seed=2):
    rng=random.Random(seed); img=new(); b=BIAS[state]; pal=spal(LIGHTPOTHOS,state)
    ROCK=P("#C9A08A","#E2C2AE","#9A7462","#5A3E32")
    r=new(); ImageDraw.Draw(r).polygon([(16,90),(14,80),(20,72),(34,70),(52,71),(62,76),(66,86),(64,90)], fill=ROCK["mid"])
    r=shade_blob(r, ROCK, (-3,-3), (3,3)); r=outline(r, ROCK["out"]); img.alpha_composite(r)
    ORG=P("#C9663A","#E68A58","#9A4826","#5C2614","#FFC9A6")
    pot_hanging(img, ORG, ORG, top=48, hook_y=10)
    tuft=new()
    for a,L in [(-160,12),(-125,13),(-95,13),(-65,13),(-25,12)]:
        if rng.random()>KEEP[state]: continue
        a2=a+b*((-195 if a<-90 else 15)-a)*0.55
        blob_leaf(tuft, heart(40+math.cos(math.radians(a))*8, 48+math.sin(math.radians(a))*3, a2, L, 10), pal, cream=hexc("#F3E7A2"), rng=rng)
    if state=="enferma": spots(tuft, rng, 1)
    img.alpha_composite(tuft)
    pot_hanging_body(img, ORG, top=48)
    vines(img, rng, [(66,52,60,26),(62,60,80,22),(14,52,140,16)], pal, state, KEEP[state], hexc("#F3E7A2"), droop=0.8)
    return finish(img, state, (40,55), (64,2), (64,54), band=(16,56), leafpal=spal(LIGHTPOTHOS,"sedienta"))

# ======== P04 Bugambilia roja (bolsa de vivero) ========
BUG_G = P("#4C8F3A","#78B85A","#2F6526","#173A16","#B8E08F")
def bougain(img, rng, state, bract, cx=40, base=58, top=10, width=30, n=7):
    keep=KEEP[state]; st=new(); d=ImageDraw.Draw(st)
    tips=[]
    for k in range(n):
        a=-90+(k-(n-1)/2)*(140/n)+rng.uniform(-8,8)
        L=rng.uniform(base-top-18, base-top-4)
        x1=cx+math.cos(math.radians(a))*L*0.9; y1=base+math.sin(math.radians(a))*L+BIAS[state]*8
        d.line([(cx+rng.uniform(-2,2),base),(x1,y1)], fill=hexc("#7A5A3A"), width=1); tips.append((x1,y1))
    st=outline(st,hexc("#3A2A1A")); img.alpha_composite(st)
    gl=new(); gp=spal(BUG_G,state)
    for (x,y) in tips:
        for j in range(3):
            if rng.random()>keep: continue
            a=rng.uniform(-180,0)+BIAS[state]*60
            blob_leaf(gl, ovate(x+rng.uniform(-6,6), y+rng.uniform(-2,8), a, 8, 6), gp)
    if state=="enferma": spots(gl, rng, 3)
    img.alpha_composite(gl)
    bl=new(); bp=dict(bract)
    if state=="sedienta": bp={k:mix(v,hexc("#B07A5A"),0.35) if k!="out" else v for k,v in bract.items()}
    for (x,y) in tips:
        if state=="sedienta" and rng.random()<0.45: continue
        for a in (-150,-90,-30):
            blob_leaf(bl, ovate(x,y,a+rng.uniform(-10,10),6,6), bp)
        px(bl,int(x),int(y),hexc("#FFF2B0"))
    img.alpha_composite(bl)
def p04(state, seed=4):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,46)
    bougain(img, rng, state, P("#E0306A","#FF6B95","#A8174A","#5A0A24","#FFC2D4"))
    BAG=P("#3E4248","#5E636C","#26282D","#101113","#7A808A")
    bg=new(); d=ImageDraw.Draw(bg); d.polygon([(15,58),(65,58),(62,89),(18,89)], fill=BAG["mid"])
    bg=shade_blob(bg, BAG, (-3,-3), (3,3)); d=ImageDraw.Draw(bg)
    d.rectangle([14,57,66,62], fill=BAG["light"]); d.line([(14,62),(66,62)], fill=BAG["dark"])
    for x in (24,33,49,56): d.line([(x,64),(x+1,86)], fill=BAG["dark"])
    bg=outline(bg, BAG["out"]); soil_strip(img,16,64,55,state); img.alpha_composite(bg)
    return finish(img, state, (40,67), (66,4), (66,62), band=(17,66), leafpal=spal(BUG_G,"sedienta"), ring=hexc("#E8E8EE"))

# ======== P05 Begonia colgante ========
def p05(state, seed=5):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    WIRE=P("#9AA0AA","#C9CED6","#6B717C","#33363C")
    pot_hanging(img, None, WIRE, top=46, hook_y=6)
    G=spal(P("#3F8A3A","#6DB85A","#2A6328","#153A16","#B6E59A"),state)
    lv=new()
    for k in range(11):
        a=-175+k*17+rng.uniform(-6,6); a2=a+b*((-195 if a<-90 else 15)-a)*0.6
        if rng.random()>KEEP[state]: continue
        blob_leaf(lv, ovate(40+math.cos(math.radians(a))*8, 43+math.sin(math.radians(a))*4, a2, 15, 12), G)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    fl=new(); FP=P("#FFFFFF","#FFFFFF","#E8D0DA","#9A6A80")
    nfl = 5 if state!="sedienta" else 2
    for k in range(nfl):
        x,y = 24+k*8+rng.uniform(-2,2), 30+rng.uniform(-3,3)+b*8
        fp = FP if k%2 else P("#FFD3E0","#FFE8EF","#E8A8BE","#9A5A70")
        f1=new(); d1=ImageDraw.Draw(f1)
        for (ox,oy) in ((-2,-2),(2,-2),(-2,2),(2,2)): d1.ellipse([x+ox-2.5,y+oy-2.5,x+ox+2.5,y+oy+2.5], fill=fp["mid"])
        f1=outline(f1, fp["out"]); fl.alpha_composite(f1)
        for dx,dy in ((0,0),(1,0),(0,1),(1,1)): px(fl,int(x)+dx,int(y)+dy,hexc("#F2C23A"))
    img.alpha_composite(fl)
    POT=P("#565C68","#7A8292","#3A3F48","#15171C","#A9B1C2")
    pot_hanging_body(img, POT, top=46)
    return finish(img, state, (40,53), (64,2), (64,50), band=(16,54), leafpal=spal(G,"sedienta"), ring=hexc("#EDEFF3"))

# ======== Dracaena helper ========
def dracaena_crown(target, cx, cy, state, rng, scale=1.0, specs=None):
    base=P("#459150","#6CB86A","#2F6E34","#173A1D","#B5E59A"); DP=spal(base,state); rib=mix(hexc("#8FD07A"),YEL,SHIFT[state])
    mult={"feliz":1.0,"con_sed":1.4,"sedienta":2.6,"enferma":1.2}[state]
    specs = specs or [(-178,30,9,1.05),(-2,30,9,1.05),(-150,30,9,0.8),(-30,30,9,0.8),(-122,26,9,0.55),(-58,26,9,0.55),(-98,20,8,0.3),(-82,20,8,0.3)]
    lvs=new()
    for a,L,w,dr in specs:
        pts=E.curve(cx,cy,a,L*scale,dr*mult,steps=18); n=len(pts)-1
        lay=new(); dd=ImageDraw.Draw(lay); left=[];right=[]
        for i,(x,y,dx,dy) in enumerate(pts):
            t=i/n; ww=w*scale*(0.6+0.4*math.sin(math.pi*min(1,t*1.1)))*(1-t**4)+0.6
            nx,ny=-dy,dx; left.append((x+nx*ww/2,y+ny*ww/2)); right.append((x-nx*ww/2,y-ny*ww/2))
        dd.polygon(left+right[::-1], fill=DP["mid"])
        if state=="sedienta": k=int(n*0.72); dd.polygon(left[k:]+right[k:][::-1], fill=hexc("#A9773F"))
        lay=shade_blob(lay, DP, (-1,-2), (1,2)); dd=ImageDraw.Draw(lay); dd.line([(p[0],p[1]) for p in pts[2:-5]], fill=rib)
        lay=outline(lay, DP["out"]); lvs.alpha_composite(lay)
    if state=="enferma": spots(lvs, rng, 3)
    target.alpha_composite(lvs)
    return spal(base,"sedienta")

def cane(img, x0, x1, top, bottom=58, banded=False):
    c=new(); d=ImageDraw.Draw(c)
    d.rectangle([x0,top,x1,bottom], fill=hexc("#C9A272")); d.line([(x0,top),(x0,bottom)], fill=hexc("#E6C899")); d.line([(x1,top),(x1,bottom)], fill=hexc("#9A7448"))
    for y in range(top+3,bottom,4): d.line([(x0,y),(x1,y)], fill=hexc("#6E5236") if banded else hexc("#9A7448"))
    img.alpha_composite(outline(c,hexc("#4A3220")))

# ======== P06 Palo de Brasil (dos cañas) ========
def p06(state, seed=6):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    cr=new(); lp=dracaena_crown(cr, 46, 36, state, rng, scale=0.8)
    dracaena_crown(cr, 35, 16, state, rng, scale=0.85)
    img.alpha_composite(cr)
    cane(img, 33, 37, 16, banded=True); cane(img, 44, 48, 36, banded=True)
    # reponer hojas frente a la caña
    pot_round(img, P("#2F6B45","#4F9466","#1F4A30","#0C2416","#86C79A"), rim=55, ribs=True, state=state)
    return finish(img, state, (40,66), (66,2), (70,62), band=(15,66), leafpal=lp, ring=hexc("#E6F2EA"))

# ======== P08 Palo de Brasil (maceta verde) ========
def p08(state, seed=8):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    cr=new(); lp=dracaena_crown(cr, 40, 18, state, rng, scale=0.95)
    dracaena_crown(cr, 49, 38, state, rng, scale=0.45, specs=[(-150,22,8,0.8),(-30,22,8,0.8),(-100,16,7,0.3),(-70,16,7,0.3)])
    img.alpha_composite(cr)
    cane(img, 37, 43, 18); cane(img, 47, 50, 38, banded=True)
    pot_round(img, P("#4C9A5A","#74BE80","#357A42","#163A1E","#A8E0B2"), rim=55, ribs=True, state=state)
    return finish(img, state, (40,66), (66,2), (70,62), band=(15,66), leafpal=lp)

# ======== P09 Dieffenbachia ========
def p09(state, seed=9):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,44); b=BIAS[state]
    G=spal(P("#3E7A3A","#5E9E52","#2A5A28","#13301A","#A6D888"),state); cream=mix(hexc("#E8EBA0"),YEL,SHIFT[state]*0.5)
    st=new(); ImageDraw.Draw(st).line([(40,58),(40,34)], fill=hexc("#7FA05A"), width=3); img.alpha_composite(outline(st,hexc("#2A4A1E")))
    lv=new()
    for k,(a,L) in enumerate([(-160,26),(-20,26),(-135,28),(-45,28),(-110,26),(-70,26),(-90,22)]):
        if rng.random()>KEEP[state]: continue
        y0=50-k*2.5; a2=a+b*((-195 if a<-90 else 15)-a)*0.6
        lay=new(); blob_leaf(lay, ovate(40,y0,a2,L,11), G)
        l=lay.load()
        for _ in range(26):
            x,y=rng.randint(0,W-1),rng.randint(0,H-1)
            if l[x,y][3] and l[x,y][:3] in (G["mid"][:3],G["light"][:3]): l[x,y]=cream
        lv.alpha_composite(lay)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    WP=P("#EEEFEA","#FFFFFF","#C9CBC2","#7A7C72")
    pot=new(); d=ImageDraw.Draw(pot); d.rounded_rectangle([18,58,62,89], radius=4, fill=WP["mid"])
    pot=shade_blob(pot, WP, (-3,-3), (3,3)); pl=pot.load()
    for x in range(21,61,4):
        for y in range(60,88):
            if pl[x,y][3] and pl[x,y][:3]==WP["mid"][:3] and not (26<x<54 and 62<y<80): pl[x,y]=WP["dark"]
    pot=outline(pot, WP["out"]); soil_strip(img,19,61,56,state); img.alpha_composite(pot)
    return finish(img, state, (40,64), (66,2), (64,60), band=(20,62), leafpal=spal(P("#3E7A3A","#5E9E52","#2A5A28","#13301A"),"sedienta"), gap=13)

# ======== Esquejes ========
WATER = {"feliz":(150,205,235,150),"con_sed":(175,205,200,150),"sedienta":(150,150,90,190),"enferma":(165,190,170,160)}
LEVEL = {"feliz":0,"con_sed":4,"sedienta":10,"enferma":2}
def cutting(img, rng, state, x, y, n, pal, cream=None, spread=1.0, L=11):
    b=BIAS[state]; st=new(); d=ImageDraw.Draw(st); jobs=[]
    for k in range(n):
        a=-90+(k-(n-1)/2)*36*spread+rng.uniform(-6,6)
        ln=rng.uniform(10,18); x1=x+math.cos(math.radians(a))*ln; y1=y+math.sin(math.radians(a))*ln*(1-b*0.5)
        d.line([(x,y),(x1,y1)], fill=mix(hexc("#6FA84A"),YEL,SHIFT[state]))
        la=a+ b*((150 if a<-90 else 30)-a)*0.8
        if rng.random()<=KEEP[state]: jobs.append((x1,y1,la,L,L*0.9))
    img.alpha_composite(outline(st,hexc("#2A4A1E")))
    lv=new(); heart_leaves(lv, jobs, pal, rng, cream)
    if state=="enferma": spots(lv, rng, 1)
    img.alpha_composite(lv)

def glass_vessel(img, rng, state, shape, roots=6, tint=(200,225,235,120), cap=None, label=None):
    lay=new(); d=ImageDraw.Draw(lay)
    d.polygon(shape, fill=tint); ys=[p[1] for p in shape]; top=min(ys); bot=max(ys)
    # agua
    wl=new(); dw=ImageDraw.Draw(wl); wy=top+14+LEVEL[state]
    dw.polygon(shape, fill=WATER[state]); wlp=wl.load()
    for yy in range(0,int(wy)):
        for xx in range(W): wlp[xx,yy]=(0,0,0,0)
    lay.alpha_composite(wl)
    # raíces
    rt=new(); dr=ImageDraw.Draw(rt); xs=[p[0] for p in shape]; cx=(min(xs)+max(xs))/2
    for k in range(roots):
        x0=cx+rng.uniform(-2,2); pts=[(x0,top+6)]
        for j in range(5): pts.append((pts[-1][0]+rng.uniform(-2.5,2.5), pts[-1][1]+rng.uniform(3,5)))
        dr.line(pts, fill=(222,206,170,255))
    rp=rt.load(); lp=lay.load()
    for yy in range(H):
        for xx in range(W):
            if rp[xx,yy][3] and lp[xx,yy][3] and yy<bot-2: lp[xx,yy]=(222,206,170,255)
    if label: d2=ImageDraw.Draw(lay); d2.rectangle(label[0], fill=label[1])
    # brillo del vidrio
    for yy in range(top+8,bot-4):
        x=int(min(xs))+3
        if lp[x,yy][3]: lp[x,yy]=(255,255,255,200)
    lay=outline(lay,hexc("#5E7E94")); img.alpha_composite(lay)
    if cap:
        c=new(); ImageDraw.Draw(c).rectangle(cap[0], fill=cap[1]); img.alpha_composite(outline(c,hexc("#123A66")))

POTHOS_P = P("#4FA544","#7FCB5C","#2E7A33","#1D4A22","#C3EE8A")
NEON_P   = P("#B8D82E","#DDF26A","#86A81E","#3E5210","#F4FFB0")
def p10(state, seed=10):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,30)
    cutting(img, rng, state, 40, 46, 5, spal(POTHOS_P,state), cream=hexc("#F3E7A2"))
    glass_vessel(img, rng, state, [(34,40),(46,40),(46,52),(54,60),(54,89),(26,89),(26,60),(34,52)], roots=8)
    return finish(img, state, (40,68), (60,4), (56,60), band=(27,64), leafpal=spal(POTHOS_P,"sedienta"), gap=11)
def p11(state, seed=11):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,24)
    cutting(img, rng, state, 40, 52, 2, spal(POTHOS_P,state), spread=1.6, L=12)
    glass_vessel(img, rng, state, [(36,50),(44,50),(44,58),(50,64),(50,89),(30,89),(30,64),(36,58)], roots=2, cap=([(35,47),(45,52)],hexc("#2F7FD6")))
    return finish(img, state, (40,72), (60,10), (52,64), band=(31,70), leafpal=spal(POTHOS_P,"sedienta"), gap=9)
def p12(state, seed=12):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,30)
    cutting(img, rng, state, 40, 62, 4, spal(POTHOS_P,state), spread=1.2)
    CAN=P("#D8443A","#F0705E","#A82C24","#4A120E","#FFB0A0")
    c=new(); d=ImageDraw.Draw(c); d.rounded_rectangle([27,62,53,89], radius=3, fill=CAN["mid"])
    c=shade_blob(c, CAN, (-3,-2), (3,2)); d=ImageDraw.Draw(c)
    d.rectangle([27,62,53,64], fill=hexc("#C9CED6")); d.rectangle([27,87,53,89], fill=hexc("#C9CED6"))
    d.rectangle([28,78,52,82], fill=hexc("#FFFFFF"))
    img.alpha_composite(outline(c,CAN["out"]))
    return finish(img, state, (40,67), (60,10), (54,64), band=(28,66), leafpal=spal(POTHOS_P,"sedienta"), ring=hexc("#FFE9E4"), gap=11)
def p13(state, seed=13):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,32)
    cutting(img, rng, state, 40, 48, 6, spal(NEON_P,state), spread=0.9)
    glass_vessel(img, rng, state, [(28,46),(52,46),(54,52),(54,89),(26,89),(26,52)], roots=5, tint=(215,205,170,120), label=([(27,74),(53,86)],hexc("#5A3A26")))
    return finish(img, state, (40,57), (60,4), (56,52), band=(27,60), leafpal=spal(NEON_P,"sedienta"), gap=11)

# ======== Árboles con cara en el tronco ========
def trunk(img, Bk, top=40, w=12, shaggy=False):
    tr=new(); d=ImageDraw.Draw(tr)
    d.polygon([(40-w,top),(40+w,top),(40+w+2,82),(40+w+8,GROUND),(40-w-8,GROUND),(40-w-2,82)], fill=Bk["mid"])
    tr=shade_blob(tr, Bk, (-3,-2), (3,2)); l=tr.load()
    for y in range(top+3,GROUND-2,4 if not shaggy else 3):
        for x in range(40-w+1,40+w,4 if not shaggy else 3):
            if shaggy and (34<x<46 and top+8<y<top+26): continue
            if l[x,y][3] and l[x,y][:3]==Bk["mid"][:3]:
                l[x,y]=Bk["dark"]
                if shaggy and x+1<W and l[x+1,y+1][3]: l[x+1,y+1]=Bk["dark"]
    img.alpha_composite(outline(tr, Bk["out"]))

def grass_line(img, rng, state, x0=14, x1=68):
    g=new(); dg=ImageDraw.Draw(g)
    for x in range(x0,x1,3): dg.line([(x,GROUND-1),(x+rng.choice([-1,0,1]),GROUND-1-rng.randint(2,4))], fill=GRASS["mid"] if state!="sedienta" else hexc("#B8A84E"))
    img.alpha_composite(outline(g,GRASS["out"]))

def p14(state, seed=14):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    trunk(img, P("#8A6E58","#B39780","#5E4838","#33251B","#D4BBA4"), top=40)
    Gb=P("#4DA64F","#7CCB66","#2F7A3A","#174A22","#C2EE95"); G=spal(Gb,state)
    cp=new(); d=ImageDraw.Draw(cp); cx,cy,R=40,28-0,24
    if state=="sedienta": R=21; cy=31
    d.ellipse([cx-R+3,cy-R*0.8+3,cx+R-3,cy+R*0.8-3], fill=G["mid"])
    for k in range(14):
        a=k*360/14; sx,sy=cx+math.cos(math.radians(a))*(R-4), cy+math.sin(math.radians(a))*(R-4)*0.8
        d.polygon(star(sx,sy,7,rot=rng.uniform(-20,20),inner=0.45), fill=G["mid"])
    cp=shade_blob(cp, G, (-3,-3), (3,3)); l=cp.load()
    for _ in range(10):
        sx,sy=rng.uniform(cx-R+8,cx+R-8), rng.uniform(cy-R*0.6,cy+R*0.5)
        for (x,y) in [(int(p[0]),int(p[1])) for p in star(sx,sy,3,inner=0.4)]:
            if 0<=x<W and 0<=y<H and l[x,y][3]: l[x,y]=G["dark"]
    if state=="enferma": spots(cp, rng, 4)
    img.alpha_composite(outline(cp, G["out"]))
    grass_line(img, rng, state)
    if state=="sedienta":
        for (x,y) in [(8,GROUND-3),(70,GROUND-2)]:
            s=new(); ImageDraw.Draw(s).polygon(star(x,y,4,inner=0.45), fill=hexc("#C99A3A")); img.alpha_composite(outline(s,hexc("#6A4A14")))
    return finish(img, state, (40,60), (66,40), (54,56), band=(29,58), gap=13, fallen=False)

def p19(state, seed=19):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,46)
    Gb=P("#4C9A4A","#78C26A","#2F6E30","#163A18","#BDE89A"); G=spal(Gb,state); b=BIAS[state]
    fr=new(); d=ImageDraw.Draw(fr)
    for a in [-172,-150,-126,-104,-76,-54,-30,-8]:
        if rng.random()>KEEP[state]: continue
        pts=E.curve(40,44,a,34,0.45+b*1.3,steps=22)
        d.line([(p[0],p[1]) for p in pts], fill=G["dark"])
        for i in range(2,len(pts)-1,2):
            x,y,dx,dy=pts[i]; nx,ny=-dy,dx; ln=6*(1-i/len(pts))+2
            for sg in (1,-1):
                d.line([(x,y),(x+(nx*sg*0.8+dx*0.6)*ln, y+(ny*sg*0.8+dy*0.6)*ln+2+b*2)], fill=G["mid"])
    fr=shade_blob(fr, G, (-1,-1), (1,1))
    if state=="enferma": spots(fr, rng, 3)
    img.alpha_composite(outline(fr, G["out"]))
    trunk(img, P("#7A5A3E","#A07A56","#4E3826","#2A1C12","#C8A27E"), top=44, w=10, shaggy=True)
    grass_line(img, rng, state)
    return finish(img, state, (40,58), (66,2), (54,54), band=(30,56), leafpal=spal(Gb,"sedienta"), gap=13)

# ======== Plantas en montículo ========
def p15(state, seed=15):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    CU=P("#9CB84A","#C8DA72","#6E8A2E","#33421A"); LG=spal(P("#5DA84A","#8ACF6A","#3A7A30","#1A3E18","#C6EE98"),state)
    cl=new(); d=ImageDraw.Draw(cl); tops=[]
    for x0,top,lean in [(26,14,-3),(32,6,-1),(38,2,0),(44,8,1),(50,16,3),(35,22,-2),(47,24,2)]:
        d.line([(x0,72),(x0+lean,top)], fill=CU["mid"], width=3); tops.append((x0+lean,top))
    cl=shade_blob(cl, CU, (-1,0), (1,0)); l=cl.load()
    for y in range(top,72,7):
        for x in range(20,60):
            if l[x,y][3]: l[x,y]=CU["dark"]
    img.alpha_composite(outline(cl, CU["out"]))
    lv=new()
    for (x,t) in tops:
        for j in range(5):
            if rng.random()>KEEP[state]: continue
            y=t+4+j*6; side=1 if j%2 else -1
            a=(-30 if side>0 else -150)+b*((30 if side>0 else 150)-(-30 if side>0 else -150))*0.5
            blob_leaf(lv, ovate(x,y,a,11,4), LG)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    mound(img, rng, state=state)
    return _mfinish(img,state,rng,LG)

def _mfinish(img, state, rng, leafpal, bpos=(66,30)):
    if state=="enferma": bandaid(img, 16, 74)
    overlays(img, state, bpos=bpos, sweat=(66,70), ground_leaves=True, leafpal=spal(leafpal,"sedienta") if state!="sedienta" else leafpal)
    return img

def p16(state, seed=16):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    pal=spal({"dark":hexc("#24563A"),"mid":hexc("#3A7D52"),"light":hexc("#5FA36E"),"band":hexc("#8CC79A"),"out":hexc("#123222")},state); pal["band"]=mix(hexc("#8CC79A"),YEL,SHIFT[state])
    lv=new()
    for x0,ang,L in [(31,-104,30),(35,-96,40),(40,-90,46),(45,-84,40),(49,-76,30),(38,-110,24),(43,-70,24)]:
        ang2=ang+(ang+90)*b*1.6; L2=L*(1-b*0.2)
        sword(lv, x0, 70, ang2, L2, 7, pal, rng, band=True, margin=mix(hexc("#E8D96A"),hexc("#A9773F"),0.5 if state=="sedienta" else 0), droop=b*0.5)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    mound(img, rng, state=state)
    return _mfinish(img, state, rng, P("#3A7D52","#5FA36E","#24563A","#123222"))

def p17(state, seed=17):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    st=new(); d=ImageDraw.Draw(st)
    for a in (-120,-90,-60):
        d.line([(40,70),(40+math.cos(math.radians(a))*22, 70+math.sin(math.radians(a))*26+b*6)], fill=hexc("#8A3A2E"), width=2)
    img.alpha_composite(outline(st,hexc("#3A1A14")))
    G=spal(P("#468A44","#6FB25E","#2E6B34","#173A1D","#B6E08F"),state)
    R=P("#D62839","#F2546A","#A3192B","#5A0B14","#FFB3BE")
    if state=="sedienta": R={k:mix(v,hexc("#9A5A3A"),0.35) if k!="out" else v for k,v in R.items()}
    gl=new()
    for a,(bx,by) in [(-160,(30,50)),(-20,(50,50)),(-140,(28,58)),(-40,(52,58)),(-175,(32,64)),(-5,(48,64))]:
        a2=a+b*((-195 if a<-90 else 15)-a)*0.6
        if rng.random()<=KEEP[state]: blob_leaf(gl, ovate(bx,by+b*4,a2,16,9), G)
    if state=="enferma": spots(gl, rng, 2)
    img.alpha_composite(gl)
    rl=new(); cy=40+b*6
    for a in range(-170,10,30):
        if state=="sedienta" and rng.random()<0.3: continue
        blob_leaf(rl, ovate(40+math.cos(math.radians(a))*3, cy+math.sin(math.radians(a))*2, a+b*40, 15, 8), R)
    for a in (-135,-90,-45): blob_leaf(rl, ovate(40,cy,a,12,7), R)
    img.alpha_composite(rl)
    for x,y in [(39,cy-1),(41,cy-1),(40,cy+1),(38,cy+1),(42,cy+1)]: px(img,x,int(y),hexc("#F2D13A"))
    mound(img, rng, state=state)
    return _mfinish(img, state, rng, P("#468A44","#6FB25E","#2E6B34","#173A1D"))

def p18(state, seed=18):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,64)
    bougain(img, rng, state, P("#B5308C","#DA5CB4","#86206A","#4A0C38","#F4B6E2"), base=58, top=6, n=9)
    ST=P("#E6C48E","#F4DDB0","#C29E68","#6E5432","#FFF0D2")
    box=new(); d=ImageDraw.Draw(box); d.rectangle([8,58,72,89], fill=ST["mid"])
    box=shade_blob(box, ST, (-3,-3), (3,3)); d=ImageDraw.Draw(box)
    d.rectangle([8,86,72,89], fill=hexc("#A85A3A"))
    for (x,y) in [(8,58),(8,70),(64,58),(64,70)]: d.rectangle([x,y,x+7,y+10], fill=hexc("#C9C2B4")); d.line([(x,y+10),(x+7,y+10)], fill=hexc("#8E877A"))
    soil_strip(img,9,71,56,state); img.alpha_composite(outline(box, ST["out"]))
    return finish(img, state, (40,67), (66,2), (72,62), band=(17,66), leafpal=spal(BUG_G,"sedienta"))

def p20(state, seed=20):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    pal=spal({"dark":hexc("#4A7A5A"),"mid":hexc("#6E9E7A"),"light":hexc("#9CC4A2"),"band":hexc("#6E9E7A"),"out":hexc("#22402C")},state)
    lv=new()
    for ang,L in [(-165,30),(-15,30),(-140,34),(-40,34),(-118,38),(-62,38),(-100,40),(-80,40),(-90,34)]:
        sword(lv, 40, 64, ang, L*(1-b*0.1), 6, pal, rng, band=False, droop=0.25+b*1.2)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    t=new(); ImageDraw.Draw(t).rectangle([37,62,43,70], fill=hexc("#A08262")); img.alpha_composite(outline(t,hexc("#4A3220")))
    mound(img, rng, state=state)
    return _mfinish(img, state, rng, P("#6E9E7A","#9CC4A2","#4A7A5A","#22402C"))

def p21(state, seed=21):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    pal=spal({"dark":hexc("#2C5E3A"),"mid":hexc("#3F7D4C"),"light":hexc("#62A36B"),"band":hexc("#3F7D4C"),"out":hexc("#14301D")},state)
    lv=new()
    for ang,L,dr in [(-150,30,0.9),(-130,36,0.7),(-112,40,0.4),(-97,44,0.2),(-83,44,0.2),(-68,40,0.4),(-50,36,0.7),(-30,30,0.9)]:
        sword(lv, 40, 70, ang, L, 3.2, pal, rng, band=False, droop=dr+b*1.4)
    if state=="enferma": spots(lv, rng, 2)
    img.alpha_composite(lv)
    if state!="sedienta":
        fl=new(); d=ImageDraw.Draw(fl)
        for (sx,sy,tx,ty) in [(42,70,52,26+b*10),(38,70,27,32+b*10)]: d.line([(sx,sy),(tx,ty+3)], fill=hexc("#4F8A4F"))
        img.alpha_composite(outline(fl,hexc("#14301D")))
        WP=P("#F4F4FA","#FFFFFF","#D8D8E4","#7C7C96")
        for (tx,ty) in [(52,26+b*10),(27,32+b*10)]:
            pet=new()
            for a in (-100,20,140): blob_leaf(pet, ovate(tx,ty,a,8,8), WP)
            for a in (-40,80,200): blob_leaf(pet, ovate(tx,ty,a,5,4), WP)
            img.alpha_composite(pet)
            for dx,dy in [(0,0),(1,0),(-1,1),(1,1)]: px(img,tx+dx,int(ty+dy),hexc("#F2B33A"))
    mound(img, rng, state=state)
    return _mfinish(img, state, rng, P("#3F7D4C","#62A36B","#2C5E3A","#14301D"))

def p22(state, seed=22):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    Gb=P("#B3D23A","#D8EE6A","#7FA22A","#3E5214","#F2FFB0"); G=spal(Gb,state)
    for (cx,cy,r,tx) in [(29,36,15,29),(53,44,11,53)]:
        t=new(); ImageDraw.Draw(t).rectangle([tx-1,cy,tx+1,70], fill=hexc("#7A5A3A")); img.alpha_composite(outline(t,hexc("#3A2A1A")))
        bl=new(); ImageDraw.Draw(bl).ellipse([cx-r,cy-r+b*3,cx+r,cy+r*(1-b*0.15)+b*3], fill=G["mid"])
        bl=shade_blob(bl, G, (-3,-3), (3,3)); l=bl.load()
        for _ in range(40):
            x,y=rng.randint(cx-r,cx+r),rng.randint(cy-r,cy+r)
            if 0<=x<W and 0<=y<H and l[x,y][3] and l[x,y][:3]==G["mid"][:3]: l[x,y]=G["light"] if rng.random()<0.6 else G["dark"]
        if state=="enferma": spots(bl, rng, 2)
        img.alpha_composite(outline(bl, G["out"]))
    mound(img, rng, state=state)
    return _mfinish(img, state, rng, Gb, bpos=(66,6))

def p23(state, seed=23):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,52); b=BIAS[state]
    LG=spal(P("#4C8A3A","#76B25A","#2F6226","#163A12"),state)
    lv=new()
    for k in range(9):
        a=-178+k*22
        if rng.random()<=KEEP[state]: blob_leaf(lv, ovate(40,50,a+b*40,17,6), LG)
    img.alpha_composite(lv)
    O=P("#F29A1F","#FFC24A","#D06A12","#6A3006","#FFE29A")
    if state=="sedienta": O={k:mix(v,hexc("#9A6A3A"),0.4) if k!="out" else v for k,v in O.items()}
    fl=new(); d=ImageDraw.Draw(fl)
    pos=[(28,44),(40,38),(52,44),(34,50),(46,50)]
    if state=="sedienta": pos=[(30,48+2),(42,44+3),(52,50)]
    for (x,y) in pos:
        y=y+b*4
        d.ellipse([x-5,y-5,x+5,y+5], fill=O["mid"])
        for k in range(10):
            a=math.radians(k*36); d.ellipse([x+math.cos(a)*5-2,y+math.sin(a)*5-2,x+math.cos(a)*5+2,y+math.sin(a)*5+2], fill=O["mid"])
    fl=shade_blob(fl, O, (-2,-2), (2,2)); l=fl.load()
    for (x,y) in pos:
        y=int(y+b*4)
        for r in (2,4):
            for k in range(12):
                a=math.radians(k*30+r*7); xx,yy=int(round(x+math.cos(a)*r)),int(round(y+math.sin(a)*r))
                if 0<=xx<W and 0<=yy<H and l[xx,yy][3]: l[xx,yy]=O["dark"]
        if l[x-1,y-2][3]: l[x-1,y-2]=O["hi"]
    img.alpha_composite(outline(fl,O["out"]))
    PK=P("#F07A22","#FFA04A","#C25412","#5E2406","#FFC88A")
    pk=new(); d=ImageDraw.Draw(pk); d.ellipse([10,54,70,96], fill=PK["mid"]); c=pk.load()
    for y in range(GROUND,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    pk=shade_blob(pk, PK, (-3,-3), (3,3)); l=pk.load()
    for x in (22,31,49,58):
        for y in range(57,GROUND-1):
            if l[x,y][3] and l[x,y][:3]!=PK["out"][:3] and not (28<x<52 and 64<y<80): l[x,y]=PK["dark"]
    img.alpha_composite(outline(pk, PK["out"]))
    return finish(img, state, (40,66), (66,6), (68,60), band=(14,66), leafpal=LG)

# ======== registro ========
PLANTS = [
 ("P01","Pothos colgante (escalera)",k01),("P02","Pothos colgante (piedra)",p02),("P03","Limonero",k03),
 ("P04","Bugambilia roja",p04),("P05","Begonia colgante",p05),("P06","Palo de Brasil (dos cañas)",p06),
 ("P07","Palo de Brasil (maceta blanca)",k07),("P08","Palo de Brasil (maceta verde)",p08),("P09","Dieffenbachia",p09),
 ("P10","Esqueje (botella de vidrio)",p10),("P11","Esqueje (tapa azul)",p11),("P12","Esqueje (lata)",p12),
 ("P13","Esqueje neón (frasco)",p13),("P14","Liquidambar",p14),("P15","Bambú",p15),("P16","Lengua de suegra",p16),
 ("P17","Nochebuena",p17),("P18","Bugambilia morada",p18),("P19","Palma enana",p19),("P20","Yuca",p20),
 ("P21","Iris africano",p21),("P22","Duranta dorada",p22),("P23","Cempasúchil",p23)]

# ================== RONDA 2 DE AJUSTES ==================
def nursery_bag(img, state, rng):
    BAG=P("#3A3D43","#5C6069","#24262B","#0E0F11","#8A909C")
    bg=new(); d=ImageDraw.Draw(bg)
    d.polygon([(17,60),(63,60),(67,70),(68,80),(64,89),(16,89),(12,80),(13,70)], fill=BAG["mid"])
    bg=shade_blob(bg, BAG, (-3,-3), (3,3)); d=ImageDraw.Draw(bg)
    # borde enrollado y ondulado
    for x in range(15,66):
        yt=58+int(1.5*math.sin(x*0.7)); d.line([(x,yt),(x,yt+4)], fill=BAG["light"])
        px(bg,x,yt+5,BAG["dark"])
    # arrugas
    for (x0,y0,x1,y1) in [(22,66,26,80),(30,65,29,74),(50,65,53,78),(57,68,59,76),(38,80,42,86)]:
        d.line([(x0,y0),(x1,y1)], fill=BAG["dark"]); d.line([(x0+1,y0),(x1+1,y1)], fill=BAG["light"])
    for (x,y) in [(20,85),(30,87),(50,87),(60,85)]: px(bg,x,y,BAG["out"])
    soil_strip(img,17,63,57,state); img.alpha_composite(outline(bg, BAG["out"]))

def bag_bougain(state, seed, bract):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    bougain(img, rng, state, bract)
    nursery_bag(img, state, rng)
    return finish(img, state, (40,68), (66,4), (68,64), band=(17,68), leafpal=spal(BUG_G,"sedienta"), ring=hexc("#E8E8EE"))
def p04(state, seed=4): return bag_bougain(state, seed, P("#D8243A","#F25A6A","#A0142A","#540812","#FFC0C8"))
def p24(state, seed=24): return bag_bougain(state, seed, P("#F28C28","#FFB560","#C8641A","#5E2A06","#FFE0B0"))

# Begonia: solo flores blancas
_old_p05 = p05
def p05(state, seed=5):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    WIRE=P("#9AA0AA","#C9CED6","#6B717C","#33363C")
    pot_hanging(img, None, WIRE, top=46, hook_y=6)
    G=spal(P("#3F8A3A","#6DB85A","#2A6328","#153A16","#B6E59A"),state)
    lv=new()
    for k in range(11):
        a=-175+k*17+rng.uniform(-6,6); a2=a+b*((-195 if a<-90 else 15)-a)*0.6
        if rng.random()>KEEP[state]: continue
        blob_leaf(lv, ovate(40+math.cos(math.radians(a))*8, 43+math.sin(math.radians(a))*4, a2, 15, 12), G)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    fl=new(); FP=P("#FFFFFF","#FFFFFF","#DCDCE6","#7C7C96")
    for k in range(5 if state!="sedienta" else 2):
        x,y = 24+k*8+rng.uniform(-2,2), 30+rng.uniform(-3,3)+b*8
        f1=new(); d1=ImageDraw.Draw(f1)
        for (ox,oy) in ((-2,-2),(2,-2),(-2,2),(2,2)): d1.ellipse([x+ox-2.5,y+oy-2.5,x+ox+2.5,y+oy+2.5], fill=FP["mid"])
        fl.alpha_composite(outline(f1, FP["out"]))
        for dx,dy in ((0,0),(1,0),(0,1),(1,1)): px(fl,int(x)+dx,int(y)+dy,hexc("#F2C23A"))
    img.alpha_composite(fl)
    pot_hanging_body(img, P("#565C68","#7A8292","#3A3F48","#15171C","#A9B1C2"), top=46)
    return finish(img, state, (40,53), (64,2), (64,50), band=(16,54), leafpal=spal(G,"sedienta"), ring=hexc("#EDEFF3"))

# Palo de Brasil mediano: un solo tallo
def p08(state, seed=8):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,50)
    cr=new(); lp=dracaena_crown(cr, 40, 22, state, rng, scale=0.95); img.alpha_composite(cr)
    cane(img, 37, 43, 22)
    pot_round(img, P("#4C9A5A","#74BE80","#357A42","#163A1E","#A8E0B2"), rim=55, ribs=True, state=state)
    return finish(img, state, (40,66), (66,2), (70,62), band=(15,66), leafpal=lp)

# Dieffenbachia: tallo central con hojas grandes jaspeadas
def p09(state, seed=9):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,44); b=BIAS[state]
    Gb=P("#3E7A3A","#5E9E52","#2A5A28","#13301A","#A6D888"); G=spal(Gb,state); cream=mix(hexc("#EEF0B0"),YEL,SHIFT[state]*0.5)
    st=new(); d=ImageDraw.Draw(st); d.rectangle([38,16,41,58], fill=hexc("#8DB86A"))
    for y in range(20,58,5): d.line([(38,y),(41,y)], fill=hexc("#6A9450"))
    img.alpha_composite(outline(st,hexc("#2A4A1E")))
    lv=new()
    specs=[(54,-165,28),(48,-15,28),(42,-150,27),(36,-30,27),(30,-140,24),(24,-45,24),(18,-110,20)]
    for (y0,a,L) in specs:
        if rng.random()>KEEP[state]: continue
        a2=a+b*((-200 if a<-90 else 20)-a)*0.55
        x0=40+(-1 if a<-90 else 2)
        pet=new(); ImageDraw.Draw(pet).line([(x0,y0),(x0+math.cos(math.radians(a2))*4,y0+math.sin(math.radians(a2))*4)], fill=hexc("#8DB86A"))
        lv.alpha_composite(pet)
        bx,by=x0+math.cos(math.radians(a2))*3, y0+math.sin(math.radians(a2))*3
        lay=new(); blob_leaf(lay, ovate(bx,by,a2,L,14), G); l=lay.load()
        # jaspeado crema a lo largo del centro de la hoja
        for t in range(3,int(L*0.85)):
            cx,cy=bx+math.cos(math.radians(a2))*t, by+math.sin(math.radians(a2))*t
            for _ in range(2):
                xx,yy=int(cx+rng.uniform(-3.5,3.5)),int(cy+rng.uniform(-3.5,3.5))
                if 0<=xx<W and 0<=yy<H and l[xx,yy][3] and l[xx,yy][:3] in (G["mid"][:3],G["light"][:3],G["dark"][:3]): l[xx,yy]=cream
        lv.alpha_composite(lay)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    WP=P("#EEEFEA","#FFFFFF","#C9CBC2","#7A7C72")
    pot=new(); d=ImageDraw.Draw(pot); d.rounded_rectangle([18,58,62,89], radius=4, fill=WP["mid"])
    pot=shade_blob(pot, WP, (-3,-3), (3,3)); pl=pot.load()
    for x in range(21,61,4):
        for y in range(60,88):
            if pl[x,y][3] and pl[x,y][:3]==WP["mid"][:3] and not (26<x<54 and 62<y<80): pl[x,y]=WP["dark"]
    soil_strip(img,19,61,56,state); img.alpha_composite(outline(pot, WP["out"]))
    return finish(img, state, (40,64), (66,2), (64,60), band=(20,62), leafpal=spal(Gb,"sedienta"), gap=13)

# Esquejes 10 y 11: botellas hermanas tipo ramune con tapa azul
RAMUNE=[(37,44),(43,44),(43,50),(47,54),(47,58),(44,61),(44,63),(50,68),(50,89),(30,89),(30,68),(36,63),(36,61),(33,58),(33,54),(37,50)]
def ramune(img, rng, state, roots):
    glass_vessel(img, rng, state, RAMUNE, roots=roots, tint=(190,228,238,130), cap=([(36,39),(44,44)],hexc("#2F7FD6")))
    m=new(); ImageDraw.Draw(m).ellipse([37,53,43,59], fill=(220,240,250,200)); m=outline(m,hexc("#5E7E94")); img.alpha_composite(m)
    px(img,38,54,hexc("#FFFFFF"))
def p10(state, seed=10):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,26)
    cutting(img, rng, state, 40, 40, 5, spal(POTHOS_P,state), cream=hexc("#F3E7A2"), L=10)
    ramune(img, rng, state, 7)
    return finish(img, state, (40,73), (60,4), (52,66), band=(31,72), leafpal=spal(POTHOS_P,"sedienta"), gap=9)
def p11(state, seed=11):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,26)
    cutting(img, rng, state, 40, 40, 2, spal(POTHOS_P,state), spread=1.6, L=12)
    ramune(img, rng, state, 2)
    return finish(img, state, (40,73), (60,10), (52,66), band=(31,72), leafpal=spal(POTHOS_P,"sedienta"), gap=9)

# Esqueje 12: frasco de café de vidrio (chaparro, etiqueta roja sin marca)
def p12(state, seed=12):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,34)
    cutting(img, rng, state, 40, 54, 4, spal(POTHOS_P,state), spread=1.2)
    glass_vessel(img, rng, state, [(29,54),(51,54),(54,59),(54,89),(26,89),(26,59)], roots=4, tint=(215,205,175,120), label=([(27,76),(53,87)],hexc("#B8322A")))
    return finish(img, state, (40,61), (60,6), (56,58), band=(27,62), leafpal=spal(POTHOS_P,"sedienta"), gap=11)

# Liquidambar: copa triangular, el árbol más grande
def p14(state, seed=14):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,52)
    Gb=P("#4DA64F","#7CCB66","#2F7A3A","#174A22","#C2EE95"); G=spal(Gb,state)
    cp=new(); d=ImageDraw.Draw(cp)
    top,base,half = (2,50,30) if state!="sedienta" else (6,50,26)
    d.polygon([(40,top),(40+half,base),(40-half,base)], fill=G["mid"])
    for t in [i/9 for i in range(1,10)]:
        for s in (-1,1):
            x=40+s*half*t; y=top+(base-top)*t
            d.polygon(star(x+s*2,y,6,rot=rng.uniform(-20,20),inner=0.45), fill=G["mid"])
    for x in range(40-half+4,40+half-3,8): d.polygon(star(x,base+1,6,rot=rng.uniform(-20,20),inner=0.45), fill=G["mid"])
    cp=shade_blob(cp, G, (-3,-3), (3,3)); l=cp.load()
    for _ in range(12):
        sx=rng.uniform(30,50); sy=rng.uniform(top+14,base-4)
        for (x,y) in [(int(p[0]),int(p[1])) for p in star(sx,sy,3,inner=0.4)]:
            if 0<=x<W and 0<=y<H and l[x,y][3]: l[x,y]=G["dark"]
    if state=="enferma": spots(cp, rng, 4)
    trunk(img, P("#8A6E58","#B39780","#5E4838","#33251B","#D4BBA4"), top=46)
    img.alpha_composite(outline(cp, G["out"]))
    grass_line(img, rng, state)
    if state=="sedienta":
        for (x,y) in [(8,GROUND-3),(70,GROUND-2)]:
            s=new(); ImageDraw.Draw(s).polygon(star(x,y,4,inner=0.45), fill=hexc("#C99A3A")); img.alpha_composite(outline(s,hexc("#6A4A14")))
    return finish(img, state, (40,64), (66,54), (54,60), band=(29,62), gap=13, fallen=False)

# P20: planta de flor morada (por identificar): hojas en roseta + florecitas moradas diminutas
_old_p20 = p20
def p20(state, seed=20):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    pal=spal({"dark":hexc("#4A7A5A"),"mid":hexc("#6E9E7A"),"light":hexc("#9CC4A2"),"band":hexc("#6E9E7A"),"out":hexc("#22402C")},state)
    if state!="sedienta":
        fl=new(); d=ImageDraw.Draw(fl)
        for (tx,ty) in [(30,14+b*8),(42,8+b*8),(53,16+b*8)]:
            d.line([(40,62),(tx,ty+6)], fill=hexc("#6E8A5A"))
        img.alpha_composite(outline(fl,hexc("#22402C")))
        for (tx,ty) in [(30,14+b*8),(42,8+b*8),(53,16+b*8)]:
            for _ in range(9):
                x,y=int(tx+rng.uniform(-3,3)),int(ty+rng.uniform(-1,8))
                px(img,x,y,hexc("#8E5BD0")); px(img,x+1,y,hexc("#B48CF0"))
    lv=new()
    for ang,L in [(-165,30),(-15,30),(-140,34),(-40,34),(-118,38),(-62,38),(-100,40),(-80,40),(-90,34)]:
        sword(lv, 40, 64, ang, L*(1-b*0.1)*0.85, 6, pal, rng, band=False, droop=0.25+b*1.2)
    if state=="enferma": spots(lv, rng, 3)
    img.alpha_composite(lv)
    mound(img, rng, state=state)
    return _mfinish(img, state, rng, P("#6E9E7A","#9CC4A2","#4A7A5A","#22402C"))

# Iris africano: flores más pequeñas
def p21(state, seed=21):
    rng=random.Random(seed); img=new(); b=BIAS[state]
    pal=spal({"dark":hexc("#2C5E3A"),"mid":hexc("#3F7D4C"),"light":hexc("#62A36B"),"band":hexc("#3F7D4C"),"out":hexc("#14301D")},state)
    lv=new()
    for ang,L,dr in [(-150,30,0.9),(-130,36,0.7),(-112,40,0.4),(-97,44,0.2),(-83,44,0.2),(-68,40,0.4),(-50,36,0.7),(-30,30,0.9)]:
        sword(lv, 40, 70, ang, L, 3.2, pal, rng, band=False, droop=dr+b*1.4)
    if state=="enferma": spots(lv, rng, 2)
    img.alpha_composite(lv)
    if state!="sedienta":
        fl=new(); d=ImageDraw.Draw(fl)
        pts=[(52,24+b*10),(27,30+b*10),(58,36+b*10)]
        for (tx,ty) in pts: d.line([(40,70),(tx,ty+2)], fill=hexc("#4F8A4F"))
        img.alpha_composite(outline(fl,hexc("#14301D")))
        WP=P("#F4F4FA","#FFFFFF","#D8D8E4","#7C7C96")
        for (tx,ty) in pts:
            pet=new()
            for a in (-100,20,140): blob_leaf(pet, ovate(tx,ty,a,5,5), WP)
            img.alpha_composite(pet)
            px(img,tx,int(ty),hexc("#F2B33A")); px(img,tx+1,int(ty),hexc("#E07B39"))
    mound(img, rng, state=state)
    return _mfinish(img, state, rng, P("#3F7D4C","#62A36B","#2C5E3A","#14301D"))

# Cempasúchil en calabaza de Halloween: conserva los ojos triangulares
def pumpkin_face(img, cx, cy, state):
    D=hexc("#3A1606"); G1=hexc("#FFD24A")
    for ex in (cx-9, cx+3):
        tri=[(ex+3,cy),(ex+6,cy+5),(ex,cy+5)] if state!="sedienta" else [(ex,cy),(ex+6,cy),(ex+3,cy+5)]
        t=new(); ImageDraw.Draw(t).polygon(tri, fill=D); img.alpha_composite(t)
        px(img, ex+3, cy+3 if state!="sedienta" else cy+1, G1)
    ImageDraw.Draw(img).polygon([(cx,cy+7),(cx+2,cy+9),(cx-2,cy+9)], fill=D)
    my=cy+12
    if state=="feliz": mouth=[(cx-8,my),(cx-5,my+3),(cx-2,my+1),(cx+1,my+4),(cx+4,my+1),(cx+7,my+3),(cx+9,my)]
    elif state=="con_sed": mouth=[(cx-7,my+2),(cx-4,my+1),(cx-1,my+3),(cx+2,my+1),(cx+5,my+3),(cx+8,my+2)]
    elif state=="sedienta": mouth=[(cx-8,my+4),(cx-5,my+1),(cx-2,my+3),(cx+1,my),(cx+4,my+3),(cx+7,my+1),(cx+9,my+4)]
    else: mouth=[(cx-7,my+2),(cx-4,my),(cx-1,my+3),(cx+2,my),(cx+5,my+3),(cx+8,my+1)]
    d=ImageDraw.Draw(img); d.line(mouth, fill=D, width=2)
    if state=="sedienta":
        for ex in (cx-6, cx+6):
            for k in range(5): px(img, ex, cy+6+k, hexc("#7CC8F4"))
    if state=="con_sed":
        for i in range(4): px(img, cx-9+i, cy-3+(i//2), D); px(img, cx+9-i, cy-3+(i//2), D)
    if state=="enferma":
        T=hexc("#E9ECEF"); RD=hexc("#E0393E"); O=hexc("#555B66")
        for k in range(9):
            x,y=cx+1+k, my+1-k//2; px(img,x,y,T); px(img,x,y-1,O); px(img,x,y+1,O)
        px(img,cx,my+1,RD); px(img,cx+1,my+1,RD)
def p23(state, seed=23):
    rng=random.Random(seed); img=new(); ground_shadow(img,40,52); b=BIAS[state]
    LG=spal(P("#4C8A3A","#76B25A","#2F6226","#163A12"),state)
    lv=new()
    for k in range(9):
        a=-178+k*22
        if rng.random()<=KEEP[state]: blob_leaf(lv, ovate(40,50,a+b*40,17,6), LG)
    img.alpha_composite(lv)
    O=P("#F29A1F","#FFC24A","#D06A12","#6A3006","#FFE29A")
    if state=="sedienta": O={k:mix(v,hexc("#9A6A3A"),0.4) if k!="out" else v for k,v in O.items()}
    pos=[(27,42),(40,36),(53,42),(33,49),(47,49)] if state!="sedienta" else [(30,50),(42,47),(52,52)]
    for (x,y) in pos:
        f=new(); d=ImageDraw.Draw(f); y=y+b*4
        d.ellipse([x-5,y-5,x+5,y+5], fill=O["mid"])
        for k in range(10):
            a=math.radians(k*36); d.ellipse([x+math.cos(a)*5-2,y+math.sin(a)*5-2,x+math.cos(a)*5+2,y+math.sin(a)*5+2], fill=O["mid"])
        f=shade_blob(f, O, (-2,-2), (2,2)); l=f.load()
        for r in (2,4):
            for k in range(12):
                a=math.radians(k*30+r*7); xx,yy=int(round(x+math.cos(a)*r)),int(round(y+math.sin(a)*r))
                if l[xx,yy][3]: l[xx,yy]=O["dark"]
        img.alpha_composite(outline(f,O["out"]))
    PK=P("#F07A22","#FFA04A","#C25412","#5E2406","#FFC88A")
    pk=new(); d=ImageDraw.Draw(pk); d.ellipse([10,54,70,96], fill=PK["mid"]); c=pk.load()
    for y in range(GROUND,H):
        for x in range(W): c[x,y]=(0,0,0,0)
    pk=shade_blob(pk, PK, (-3,-3), (3,3)); l=pk.load()
    for x in (20,29,51,60):
        for y in range(57,GROUND-1):
            if l[x,y][3] and l[x,y][:3]!=PK["out"][:3]: l[x,y]=PK["dark"]
    img.alpha_composite(outline(pk, PK["out"]))
    pumpkin_face(img, 40, 62, state)
    if state=="enferma": bandaid(img, 14, 66)
    overlays(img, state, bpos=(66,6), sweat=(68,60), ground_leaves=True, leafpal=LG)
    return img

PLANTS = [
 ("P01","Pothos colgante (escalera)",k01),("P02","Pothos colgante (piedra)",p02),("P03","Limonero",k03),
 ("P04","Bugambilia roja (bolsa)",p04),("P05","Begonia colgante",p05),("P06","Palo de Brasil grande",p06),
 ("P07","Palo de Brasil chico",k07),("P08","Palo de Brasil mediano",p08),("P09","Dieffenbachia",p09),
 ("P10","Esqueje (botella tapa azul A)",p10),("P11","Esqueje (botella tapa azul B)",p11),("P12","Esqueje (frasco de café)",p12),
 ("P13","Esqueje neón (frasco)",p13),("P14","Liquidambar",p14),("P15","Bambú",p15),("P16","Lengua de suegra",p16),
 ("P17","Nochebuena",p17),("P18","Bugambilia grande",p18),("P19","Palma enana",p19),("P20","Flor morada (por identificar)",p20),
 ("P21","Iris africano",p21),("P22","Duranta dorada",p22),("P23","Cempasúchil (calabaza)",p23),("P24","Bugambilia naranja (bolsa)",p24)]

if __name__=="__main__":
    import os, sys
    os.makedirs("final",exist_ok=True); k=4
    only=sys.argv[1:] or None
    for pid,name,fn in [p for p in PLANTS if not only or p[0] in only]:
        for st in STATES:
            im=fn(st); im.resize((W*k,H*k),Image.NEAREST).save(f"final/{pid}_{st}.png"); im.save(f"final/{pid}_{st}_80x96.png")
    print("ok2")
