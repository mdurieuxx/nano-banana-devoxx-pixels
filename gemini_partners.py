# 11: "Gemini powers the partners" - étoile Gemini au centre, logos des partenaires Devoxx qui s'allument
# Logos = interprétations pixel art maison (JetBrains, Docker, Red Hat, Oracle)
# Usage: python gemini_partners.py  ->  output/11_gemini_powers_partners.gif
from PIL import Image, ImageDraw
import math, random
from common import S, GC, FONT, text, lerp

N = 60
STOPS = [(66,133,244),(155,114,203),(217,101,121)]
def grad(t):
    t = max(0,min(.999,t)); t = round(t*7)/7; i = int(t*2); return lerp(STOPS[i],STOPS[i+1],(t*2)-i)

PAL = {"b":(36,150,237),"w":(245,245,245),"k":(20,20,30),"o":(255,110,0),"y":(255,200,100),"r":(210,30,40),"d":(130,15,25)}
WHALE = ["....bb.....",".bb.bb.bb..","bbbbbbbbbb.","bwkbbbbbbbb","bbbbbbbbbb.",".bbbbbbbbb.","..bbbbbbb..","....www...."]
HAT  = ["...rrrrr...","..rrrrrrr..","..rrrrrrr..","..kkkkkkk..",".rrrrrrrrr.","rrrrrrrrrrr","dddddddddddd"[:11]]

def draw_sprite(d, rows, x, y):
    for r,row in enumerate(rows):
        for c,ch in enumerate(row):
            if ch!=".": d.point((x+c,y+r),PAL[ch])

def draw_jb(d, x, y):
    d.rectangle([x-1,y-1,x+11,y+10],(150,150,175)); d.rectangle([x,y,x+10,y+9],(8,8,12))
    for p,c in [((0,0),(255,49,140)),((1,0),(255,140,0)),((0,1),(255,60,200)),((10,9),(40,150,255)),((9,9),(60,220,120))]:
        d.point((x+p[0],y+p[1]),c)
    for ch,ox in (("J",1),("B",6)):
        for r,row in enumerate(FONT[ch]):
            for c,v in enumerate(row):
                if v=="1": d.point((x+ox+c,y+1+r),(255,255,255))
    d.rectangle([x+2,y+7,x+5,y+7],(255,255,255))

def draw_oracle(d, x, y):
    d.rounded_rectangle([x,y,x+26,y+8],3,(210,30,40)) if hasattr(d,"rounded_rectangle") else d.rectangle([x,y,x+26,y+8],(210,30,40))
    text_img = d._image
    text(text_img,"ORACLE",x+2,y+2,(255,255,255),shadow=False)

# (nom, dessin, x, y, centre du logo)
LOGOS = [("jb",5,13,(10,18)),("docker",49,13,(54,17)),("hat",5,39,(10,42)),("ora",35,43,(48,47))]
T0 = [6,16,26,36]
CX,CY = 32,29

def radius(f):
    if f < 46: return 11 + 1.1*math.sin(f*0.45)
    if f < 54: return 11 + 2.5*math.sin((f-46)/8*math.pi) + 1.1
    return 11 + 1.1*math.sin(f*0.45)

def bright(f,i):
    t0 = T0[i]+6
    if f < t0: k = .30
    else: k = 1.0
    if f >= 54: k = 1.0-.7*((f-54)/6)
    return k

def frame(f):
    img = Image.new("RGB",(S,S),(8,6,22)); d = ImageDraw.Draw(img); d._image = img; px = img.load()
    rg = random.Random(f//2)
    for _ in range(16): px[rg.randrange(S),rg.randrange(S)] = (45,45,95)
    text(img,"GOOGLE AI",14,3,[GC[i%4] for i in range(9)])
    # logos sur calque + luminosité
    layer = Image.new("RGB",(S,S),(0,0,0)); ld = ImageDraw.Draw(layer); ld._image = layer
    for i,(nm,x,y,c) in enumerate(LOGOS):
        k = f - (T0[i]+6)
        by = -2 if 0 <= k < 2 else (-1 if 2 <= k < 4 else 0)
        yy = y + by
        if nm=="jb": draw_jb(ld,x,yy)
        elif nm=="docker": draw_sprite(ld,WHALE,x,yy)
        elif nm=="hat": draw_sprite(ld,HAT,x,yy)
        else: draw_oracle(ld,x,yy)
    lp = layer.load()
    for y in range(S):
        for x in range(S):
            c = lp[x,y]
            if c!=(0,0,0):
                # luminosité propre à chaque logo selon sa zone
                i = min(range(4), key=lambda j: (x-LOGOS[j][3][0])**2+(y-LOGOS[j][3][1])**2)
                k = bright(f,i)
                fl = 1.0 if 0 <= f-(T0[i]+6) < 2 else 0
                c = tuple(int(v*k) for v in c)
                if fl: c = lerp(c,(255,255,255),.7)
                px[x,y] = c
    # faisceaux
    for i,(nm,x,y,c) in enumerate(LOGOS):
        p = (f-T0[i])/6
        if 0 <= p <= 1:
            for s in range(5):
                q = max(0,p-s*.07)
                bx,by_ = int(CX+(c[0]-CX)*q), int(CY+(c[1]-CY)*q)
                if 0<=bx<S and 0<=by_<S:
                    d.rectangle([bx,by_,bx+1,by_+1],(255,255,255) if s==0 else lerp(STOPS[1],(8,6,22),s/5))
    # étoile Gemini
    r = radius(f); phase = .22*math.sin(f*.35)
    for y in range(S):
        for x in range(S):
            dx,dy = abs(x-CX+.5)/r, abs(y-CY+.5)/r
            m = dx**.62 + dy**.62
            if m <= 1:
                t = ((x-CX)-(y-CY))/(2*r)*.5+.5+phase
                px[x,y] = lerp(grad(t),(255,255,255),max(0,1-m*1.4)*.7)
            elif m <= 1.3:
                k = (1.3-m)/.3*.22; bg = px[x,y]
                px[x,y] = tuple(int(bg[j]+(STOPS[1][j]-bg[j])*k) for j in range(3))
    # étincelles finales
    if 46 <= f < 56:
        for k in range(10):
            a = math.radians(k*36+f*9); rad = 14+(f-46)*2.5
            x,y = int(CX+rad*math.cos(a)), int(CY+rad*math.sin(a)*.8)
            if 0<=x<S and 0<=y<S: px[x,y] = (255,255,255) if k%2 else GC[k%4]
    # texte du bas
    text(img,"GEMINI X DEVOXX",2,57,[(255,255,255)]*7+[(120,120,160)]+[GC[i%4] for i in range(6)])
    return img

import os; os.makedirs("output",exist_ok=True)
frames = [frame(i) for i in range(N)]
frames[0].save("output/11_gemini_powers_partners.gif",save_all=True,append_images=frames[1:],duration=90,loop=0)
