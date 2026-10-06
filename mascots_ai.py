# Les mascottes des partenaires Platinum de Devoxx BE 2026 "nourrissent" un robot IA
# Gopher (Google), cube JB (JetBrains), lion (ING), Duke (Oracle)  -- interprétations pixel art maison
# Image 7 : "AI Builders"
# Usage: python mascots_ai.py  ->  output/7_mascots_ai.gif
from PIL import Image, ImageDraw
import random, math
from common import S, G, FONT, text

PAL = {"k":(20,20,30),"w":(245,245,245),"r":(230,50,50),"o":(255,140,0),"y":(255,205,110),
       "b":(100,200,230),"n":(120,70,30),"g":(150,155,170)}
GOPHER = ["..bb...bb..",".bbbbbbbbb.","bbwwbbbwwbb","bbwkbbbwkbb","bbbbbnbbbbb","bbbbwkwbbbb",
          ".bbbbbbbbb.",".bbbbbbbbb.","b.bbbbbbb.b","..bbbbbbb..","..bb...bb..","..nn...nn.."]
LION   = ["..ooooooo..",".ooyyyyyoo.","ooyyyyyyyoo","ooykyyykyoo","ooyyyrryyoo","ooyykkkyyoo",
          ".ooyyyyyoo.","..ooooooo..",".ooooooooo.",".oo.ooo.oo.",".oo.ooo.oo.","..oo...oo.."]
DUKE   = ["...kkkkk...","..kwwwwwk..",".kwwkwkwwk.",".kwwwrwwwk.","..kwwrrwk..","...kwwwk...",
          "k.kwwwwwk.k","kwkwwwwwkwk",".k.kwwwk.k.","...kwwwk...","...kk.kk...","..kkk.kkk.."]
CHAR_COL = {"gopher":(66,133,244),"jb":(255,49,140),"lion":(255,120,0),"duke":(234,67,53)}

def blit(img, rows, x, y):
    px = img.load()
    for r,row in enumerate(rows):
        for c,ch in enumerate(row):
            if ch!="." and 0<=x+c<S and 0<=y+r<S: px[x+c,y+r] = PAL[ch]

def jb(img, x, y):
    d = ImageDraw.Draw(img)
    d.rectangle([x-1,y-1,x+11,y+10],(150,150,175)); d.rectangle([x,y,x+10,y+9],(8,8,12))
    for i,c in enumerate([(255,49,140),(255,140,0),(255,230,60),(60,220,120),(40,150,255)]):
        d.point((x+1+i,y+9),c) if False else None
    d.point((x,y),(255,49,140)); d.point((x+1,y),(255,140,0)); d.point((x,y+1),(255,60,200)); d.point((x+10,y+9),(40,150,255)); d.point((x+9,y+9),(60,220,120))
    for ch,ox in (("J",2),("B",6)):
        for r,row in enumerate(FONT[ch]):
            for c,v in enumerate(row):
                if v=="1": d.point((x+ox+c-1+(1 if ch=="B" else 0),y+1+r),(255,255,255))
    d.rectangle([x+2,y+7,x+5,y+7],(255,255,255))
    d.point((x+2,y+10),(10,10,14)); d.point((x+8,y+10),(150,150,175))      # pieds
    d.point((x+2,y+11),(10,10,14)); d.point((x+8,y+11),(10,10,14))
    d.point((x-2,y+4),(150,150,175)); d.point((x+12,y+4),(150,150,175))      # bras

CHARS = [("gopher",2),("jb",15),("lion",38),("duke",51)]
FLOOR = 50
N = 56
rnd = random.Random(5)
STARS = [(rnd.randrange(S),rnd.randrange(8,34)) for _ in range(14)]

def jump_h(f, t0):
    k = f - t0
    return [1,3,4,3,1,0][k] if 0 <= k < 6 else 0

def frame(f):
    img = Image.new("RGB",(S,S),(10,8,32)); d = ImageDraw.Draw(img)
    for gy in range(0,S,4):
        for gx in range(0,S,4): d.point((gx,gy),(20,18,52))
    for i,(x,y) in enumerate(STARS):
        if (i+f//2)%3: d.point((x,y),(120,120,200))
    text(img,"AI BUILDERS",10,2,[(66,133,244),(234,67,53),(255,255,255),(251,188,5),(66,133,244),(52,168,83),(234,67,53),(251,188,5),(66,133,244),(52,168,83),(234,67,53)])
    final = f >= 42
    # robot au centre
    flash, fcol = 0, (255,255,255)
    for i,(nm,x) in enumerate(CHARS):
        t0 = i*10
        if t0+8 <= f < t0+11: flash, fcol = 1, CHAR_COL[nm]
    rx,ry = 24,13
    d.rectangle([rx+7,ry-4,rx+8,ry-1],(150,155,170))                       # antenne
    tip = fcol if flash or final else ((255,60,60) if f%4<2 else (120,30,30))
    d.rectangle([rx+6,ry-6,rx+9,ry-4],tip)
    d.rectangle([rx,ry,rx+15,ry+11],(160,165,185)); d.rectangle([rx+1,ry+1,rx+14,ry+10],(30,36,70))
    d.rectangle([rx-2,ry+3,rx-1,ry+7],(110,115,135)); d.rectangle([rx+16,ry+3,rx+17,ry+7],(110,115,135))
    d.rectangle([rx+3,ry+12,rx+12,ry+14],(110,115,135))
    if final:
        cols = [(66,133,244),(234,67,53),(251,188,5),(52,168,83)]
        txtcol = cols[(f//2)%4]
    else:
        txtcol = fcol if flash else (170,200,255)
    text(img,"AI",rx+4,ry+3,txtcol,shadow=False)
    if flash or final:
        d.line([(rx+3,ry+9),(rx+12,ry+9)],txtcol)
    # sol
    for x in range(0,S,2): d.point((x,FLOOR),(60,60,120))
    # personnages
    for i,(nm,x) in enumerate(CHARS):
        t0 = i*10
        h = jump_h(f,t0)
        if final: h = [0,3,4,3,0,2,3,0][(f-42)%8 if (f%2==0 or True) else 0] if False else [1,3,4,3,1,0][(f//1)%6] if False else [0,3,4,3,0,0][(f-42+ i%2*3)%6]
        elif h==0 and (f//4+i)%2==0 and not (t0<=f<t0+11): h = 0
        top = FLOOR-12-h
        if nm=="jb": jb(img,x,top+1)
        else: blit(img,{"gopher":GOPHER,"lion":LION,"duke":DUKE}[nm],x,top)
        # impulsion vers le robot
        p = (f-(t0+2))/6
        if 0 <= p <= 1:
            sx,sy = x+5, top
            ex,ey = 32, ry+15
            for k in range(4):
                q = max(0,p-k*0.08)
                px_,py_ = int(sx+(ex-sx)*q), int(sy+(ey-sy)*q)
                c = tuple(int(v*(1-k*0.22)) for v in CHAR_COL[nm])
                if 0<=px_<S and 0<=py_<S:
                    cc = c if k else (255,255,255)
                    d.rectangle([px_,py_,px_+1,py_+1],cc)
    # confettis
    if final:
        rc = random.Random(f)
        for _ in range(16):
            cx = 32+rc.randint(-20,20); cy = ry-2+rc.randint(-8,22)
            if 0<=cx<S and 0<=cy<S: img.putpixel((cx,cy),rc.choice([(66,133,244),(234,67,53),(251,188,5),(52,168,83),(255,255,255)]))
    text(img,"DEVOXX 26",14,56,(255,255,255))
    return img

import os; os.makedirs("output",exist_ok=True)
frames = [frame(i) for i in range(N)]
frames[0].save("output/7_mascots_ai.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
