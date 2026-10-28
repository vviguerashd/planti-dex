import sys
from PIL import Image, ImageDraw, ImageFont
from plantitas import PLANTS, STATES, W, H
def sheet(rows, out, k=3, title=None):
    F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",18)
    TW,TH=W*k,H*k; G=12; LW=170
    S=Image.new("RGB",(LW+4*(TW+G)+G, (60 if title else 10)+len(rows)*(TH+G)+G),(246,244,236)); d=ImageDraw.Draw(S)
    if title: d.text((G,16),title,fill=(40,70,45),font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",26))
    y=(60 if title else 10)
    for pid,name,fn in rows:
        words=name.split(" "); line=""; ly=y+TH//2-30
        d.text((G,ly),pid,fill=(40,70,45),font=F); ly+=24
        for w in words:
            if len(line+w)>16: d.text((G,ly),line,fill=(30,30,30),font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",15)); ly+=19; line=""
            line+=w+" "
        d.text((G,ly),line,fill=(30,30,30),font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",15))
        for i,st in enumerate(STATES):
            x=LW+i*(TW+G)
            d.rounded_rectangle([x-3,y-3,x+TW+3,y+TH+3],radius=8,fill=(255,255,255))
            im=Image.open(f"final/{pid}_{st}_80x96.png").resize((TW,TH),Image.NEAREST)
            S.paste(im,(x,y),im)
        y+=TH+G
    S.save(out)
a,b=int(sys.argv[1]),int(sys.argv[2])
sheet(PLANTS[a:b], f"chk_{a}_{b}.png", k=2)
