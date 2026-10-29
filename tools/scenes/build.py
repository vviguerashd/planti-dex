import json, os, shutil
from PIL import Image, ImageDraw
import estudio, escaleras, bufetera, sala, jardin
from gala import gala_stalk, gala_sleep, gala_happy, hx
import pathlib; R=str(pathlib.Path(__file__).resolve().parents[2])+'/'
os.makedirs(R+'public/scenes',exist_ok=True); os.makedirs(R+'public/gala',exist_ok=True)
scenes=[]
# escaleras
im=escaleras.base(); hx_,hy_=escaleras.stairs(im); ImageDraw.Draw(im).line([(hx_,hy_-4),(hx_,hy_+6)],fill=hx('#2f3332'),width=2)
scenes.append(('escaleras','Escaleras',im,{'P05':(14,124),'P02':(92,114),'P01':(hx_-40,hy_+6)},207,(186,160)))
im=estudio.base(); estudio.chairs(im)
scenes.append(('estudio','Estudio',im,{'P13':(146,38),'P09':(206,97)},206,(130,159)))
tv=Image.new('RGBA',(60,34),hx('#9cc8ea')); ImageDraw.Draw(tv).rectangle([0,28,60,34],fill=hx('#7db35a')); tv.alpha_composite(gala_happy(0).resize((28,34)),(16,0))
scenes.append(('sala','Sala',sala.full(None,tv),{'P06':(-2,121),'P08':(190,121),'P07':(462,121)},216,(300,168)))
scenes.append(('bufetera','Bufetera',bufetera.scene(None),{'P12':(112,30),'P10':(152,30),'P11':(186,30)},207,(120,160)))
for sid,label,fn in (('cochera','Cochera',jardin.cochera),('pasillo','Pasillo',jardin.pasillo)):
    im,pos,meta=fn(); scenes.append((sid,label,im,pos,meta['floor'],meta['sleep']))
out=[]
for sid,label,im,pos,floor,sleep in scenes:
    im.convert('RGB').save(R+f'public/scenes/{sid}.png',optimize=True)
    out.append({'id':sid,'label':label,'w':im.width,'h':im.height,'floor':floor,'sleep':list(sleep),'plants':{k:list(v) for k,v in pos.items()}})
json.dump(out,open(R+'src/lib/scenes.json','w'),ensure_ascii=False,indent=1)
gala_stalk().save(R+'public/gala/acecho.png'); gala_sleep().save(R+'public/gala/dormida.png')
for i,t in enumerate((-1,0,1)): gala_happy(t).save(R+f'public/gala/feliz{i}.png')
os.makedirs(R+'tools/scenes',exist_ok=True)
for f in ('gala.py','common.py','estudio.py','escaleras.py','bufetera.py','sala.py','jardin.py','build.py','caricia.py'): shutil.copy(f,R+'tools/scenes/'+f)
print([ (o['id'],o['w'],o['h']) for o in out])
