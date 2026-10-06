# Image 4 : "Google chomps Devoxx" - un G façon chomper poursuit 4 fantômes aux couleurs Google
# Usage: python chomp.py  ->  output/4_google_chomps_devoxx.gif
from PIL import Image, ImageDraw
import math
from common import S, G, GC, text, tw, lerp

RED,YEL,GRN,BLU = G["red"],G["yellow"],G["green"],G["blue"]
LETTERS6 = [BLU,RED,YEL,BLU,GRN,RED]

def g_color(ang):  # ang en degrés, y vers le bas
    if -135 <= ang < -45: return RED
    if -45 <= ang < 45:   return BLU
    if 45 <= ang < 135:   return GRN
    return YEL

def draw_g(img, cx, cy, R=10, r=6, mouth=0):
    px = img.load()
    for y in range(cy-R-1, cy+R+2):
        for x in range(cx-R-1, cx+R+2):
            if not (0<=x<S and 0<=y<S): continue
            dx,dy = x-cx+0.0, y-cy+0.0
            d = math.hypot(dx,dy)
            if r <= d <= R:
                ang = math.degrees(math.atan2(dy,dx))
                if abs(ang) < mouth: continue      # bouche
                px[x,y] = g_color(ang)
    # barre du G
    for y in range(cy-1, cy+2):
        for x in range(cx, cx+R+1):
            if 0<=x<S: px[x,y] = BLU

def ghost(img, x, y, col, f):
    d = ImageDraw.Draw(img)
    d.ellipse([x,y,x+8,y+8], col); d.rectangle([x,y+4,x+8,y+9], col)
    for k in range(0,9,3):
        if (k//3 + f) % 2: d.point((x+k,y+9),(20,12,50)); d.point((x+k+1,y+9),(20,12,50))
    for ex in (x+2,x+5):
        d.rectangle([ex,y+3,ex+1,y+4],(255,255,255)); d.point((ex+1,y+4),(20,20,120))

def chomp(frame, n=24):
    img = Image.new("RGB",(S,S),(14,8,40)); d = ImageDraw.Draw(img)
    for gy in range(0,S,2):
        for gx in range(0,S,2): d.point((gx,gy),(22,16,52))
    text(img,"GOOGLE",20,3,LETTERS6)
    d.line([(0,13),(63,13)],(70,60,160)); d.line([(0,52),(63,52)],(70,60,160))
    t = frame/n
    cx = int(-14 + t*92)
    cy = 33
    # points
    for x in range(2,64,5):
        if x > cx+6: d.rectangle([x,cy,x+1,cy+1],(255,230,160))
    # fantômes (fuient devant le G)
    for i,col in enumerate([RED,YEL,GRN,BLU]):
        gx = cx + 22 + i*11
        if -9 < gx < 64: ghost(img, gx, cy-5, col, frame)
    mouth = [38,22,8,22][frame % 4]
    draw_g(img, cx, cy, mouth=mouth)
    text(img,"DEVOXX",20,56,LETTERS6)
    return img

def hearts(frame):
    img = Image.new("RGB",(S,S),(14,8,40)); d = ImageDraw.Draw(img)
    for gy in range(0,S,2):
        for gx in range(0,S,2): d.point((gx,gy),(22,16,52))
    draw_g(img, 15, 24, R=13, r=8, mouth=28)
    # D géant (traits épais) aux couleurs Devoxx-ish : dégradé
    x0,y0,x1,y1 = 41,11,57,37
    for t in range(3):
        d.line([(x0+t,y0),(x0+t,y1)],BLU)
    d.rectangle([x0,y0,x0+8,y0+2],RED); d.rectangle([x0,y1-2,x0+8,y1],GRN)
    for t in range(3):
        d.arc([x0-2,y0,x1+3,y1],270,90,fill=YEL,width=3)
    # coeur qui bat
    big = frame%2==0
    heart = ["0110110","1111111","1111111","0111110","0011100","0001000"] if big else ["000000","0110110","0111110","0011100","0001000","000000"]
    hx,hy = 29,20 if big else 21
    for r,row in enumerate(heart):
        for c,v in enumerate(row):
            if v=="1": d.point((hx+c,hy+r),(255,60,90))
    text(img,"GOOGLE",20,45,LETTERS6)
    text(img,"X",30,52,(255,255,255)); text(img,"DEVOXX",20,58,LETTERS6) if False else None
    text(img,"DEVOXX",20,58,LETTERS6)
    return img

def save_all(fn,name,n,dur):
    fr=[fn(i) for i in range(n)]
    fr[0].save(f"{name}.gif",save_all=True,append_images=fr[1:],duration=dur,loop=0)

if __name__=="__main__":
    import os; os.makedirs("output",exist_ok=True)
    save_all(lambda f: chomp(f,24),"output/4_google_chomps_devoxx",24,90)
