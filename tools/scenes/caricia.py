from PIL import Image, ImageDraw
from gala import gala_sleep, gala_happy, heart_big, hx
import estudio
bg=estudio.scene(False, nogala=True)
frames=[]; durs=[]
sl=gala_sleep()
for i in range(6):
    f=bg.copy(); f.alpha_composite(sl,(130,205-46)); d=ImageDraw.Draw(f)
    for j,(x,y,s) in enumerate(((212,150,4),(220,142,5),(229,133,6))):
        if j<=i%3: d.line([(x,y),(x+s,y),(x,y+s),(x+s,y+s)],fill=hx('#4a554c'))
    frames.append(f); durs.append(350)
# toque
for r in (4,9,14):
    f=bg.copy(); f.alpha_composite(sl,(130,205-46)); d=ImageDraw.Draw(f)
    d.ellipse([196-r,176-r,196+r,176+r],outline=hx('#1d5fd1'),width=2); frames.append(f); durs.append(90)
# feliz con corazones
hearts=[(150,118,0),(176,108,4),(196,120,8),(164,104,12)]
for t in range(18):
    f=bg.copy(); g=gala_happy([-1,0,1,0][t%4]); f.alpha_composite(g,(140,205-80))
    for hx0,hy0,start in hearts:
        k=t-start
        if 0<=k<10:
            a=255 if k<6 else int(255*(10-k)/4)
            heart_big(f,hx0+(k%2),hy0-k*4,a)
    frames.append(f); durs.append(110)
frames=[fr.resize((fr.width*3,fr.height*3),Image.NEAREST).convert('P',palette=Image.ADAPTIVE,colors=128) for fr in frames]
frames[0].save('caricia_gala.gif',save_all=True,append_images=frames[1:],duration=durs,loop=0,optimize=True)
