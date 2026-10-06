# Génère des visuels 64x64 pour la matrice LED Devoxx Belgium 2026 (Anvers)
# Usage: pip install pillow && python make_pixel_art.py
from PIL import Image, ImageDraw
import math, random

S = 64
G = {"blue": (66,133,244), "red": (234,67,53), "yellow": (251,188,5), "green": (52,168,83)}
GC = list(G.values())

FONT = {
"A":["010","101","111","101","101"],"B":["110","101","110","101","110"],"D":["110","101","101","101","110"],
"E":["111","100","110","100","111"],"N":["111","101","101","101","101"],"O":["111","101","101","101","111"],
"P":["110","101","110","100","100"],"R":["110","101","110","101","101"],"T":["111","010","010","010","010"],
"V":["101","101","101","101","010"],"W":["101","101","101","111","101"],"X":["101","101","010","101","101"],
"G":["011","100","101","101","011"],"L":["100","100","100","100","111"],"C":["011","100","100","100","011"],
"U":["101","101","101","101","111"],"2":["110","001","010","100","111"],"0":["111","101","101","101","111"],
"6":["011","100","111","101","111"],"-":["000","000","111","000","000"]," ":["000"]*5,
"I":["111","010","010","010","111"],"M":["101","111","111","101","101"],"S":["011","100","010","001","110"],
"H":["101","101","111","101","101"],"J":["001","001","001","101","111"],"Y":["101","101","010","010","010"],"K":["101","101","110","101","101"],
}
def text(img, s, x, y, colors, shadow=True):
    d = ImageDraw.Draw(img)
    for i, ch in enumerate(s):
        col = colors[i % len(colors)] if isinstance(colors, list) else colors
        for r, row in enumerate(FONT[ch]):
            for c, v in enumerate(row):
                if v == "1":
                    if shadow: d.point((x+c+1, y+r+1), (0,0,0))
                    d.point((x+c, y+r), col)
        x += 4
def tw(s): return len(s)*4-1

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

# ---------- 1. Antwerp sunset ----------
def antwerp(frame=0):
    img = Image.new("RGB",(S,S)); d = ImageDraw.Draw(img)
    stops=[(25,10,70),(90,30,120),(220,70,100),(255,150,60),(255,210,90)]
    for y in range(44):
        t=y/43*(len(stops)-1); i=min(int(t),len(stops)-2)
        band=round((t-i)*5)/5  # banding = look pixel art
        d.line([(0,y),(S,y)], lerp(stops[i],stops[i+1],band))
    random.seed(4)
    for k in range(14):
        x,y=random.randrange(S),random.randrange(0,22)
        if (k+frame)%3: d.point((x,y),(255,255,230))
    # soleil
    d.ellipse([40,30,54,44],(255,235,120)); d.ellipse([43,33,51,41],(255,250,190))
    sil=(12,8,30)
    # maisons à pignons flamands
    houses=[(0,40,7,5),(7,38,7,8),(14,42,6,6)]
    # cathédrale : tour haute
    d.rectangle([22,32,30,64],sil)
    d.polygon([(22,32),(26,14),(30,32)],sil)   # flèche
    d.line([(26,10),(26,15)],sil)
    d.rectangle([32,38,40,64],sil); d.polygon([(32,38),(36,26),(40,38)],sil)
    d.rectangle([41,40,64,64],sil)
    # pignons en escalier
    for i,(x,w) in enumerate([(42,6),(49,6),(56,7)]):
        h=38-(i%2)*3
        for s in range(3):
            d.rectangle([x+s,h+s*2-2,x+w-s,h+s*2],sil)
    d.rectangle([0,44,21,64],sil)
    for i,(x,w) in enumerate([(1,6),(8,6),(15,6)]):
        for s in range(3):
            d.rectangle([x+s,38+s*2+(i%2)*2,x+w-s,40+s*2+(i%2)*2],sil)
    # fenêtres allumées
    random.seed(9)
    for _ in range(26):
        x,y=random.randrange(0,64),random.randrange(48,63)
        if img.getpixel((x,y))==sil and (x+y+frame)%4: d.point((x,y),(255,200,80))
    text(img,"DEVOXX",3,2,[G["blue"],G["red"],G["yellow"],G["blue"],G["green"],G["red"]])
    text(img,"ANTWERP",2,57,(255,255,255))
    return img

# ---------- 2. Matrice LED Google ----------
def matrix():
    img = Image.new("RGB",(S,S),(8,8,16)); d=ImageDraw.Draw(img)
    for gy in range(0,S,2):
        for gx in range(0,S,2):
            d.point((gx,gy),(25,25,40))
    # chevrons </>
    def thick(pts,col):
        for a,b in zip(pts,pts[1:]):
            d.line([a,b],col,width=3)
    thick([(18,10),(6,22),(18,34)],G["blue"])
    thick([(46,10),(58,22),(46,34)],G["green"])
    thick([(36,8),(28,36)],G["red"])
    # points Google
    for i,c in enumerate(GC):
        d.rectangle([20+i*6,41,23+i*6,44],c)
    text(img,"DEVOXX",20-1,48,[G["blue"],G["red"],G["yellow"],G["blue"],G["green"],G["red"]])
    text(img,"BE 2026",16,56,(255,255,255))
    return img

# ---------- 3. Nano Banana ----------
def banana(frame=0):
    img=Image.new("RGB",(S,S),(20,12,50)); d=ImageDraw.Draw(img)
    for y in range(S):
        d.line([(0,y),(S,y)],lerp((20,12,50),(60,25,110),y/S))
    random.seed(2)
    for k in range(18):
        x,y=random.randrange(S),random.randrange(S-14)
        if (k+frame)%2: d.point((x,y),GC[k%4])
    off = -1 if frame%2 else 0
    # corps banane (croissant)
    body=Image.new("L",(S,S),0); bd=ImageDraw.Draw(body)
    bd.ellipse([14,8+off,52,50+off],255); bd.ellipse([24,4+off,62,44+off],0)
    d.bitmap((0,0),body,fill=(255,225,53))
    edge=Image.new("L",(S,S),0); ed=ImageDraw.Draw(edge)
    ed.ellipse([14,8+off,52,50+off],255); ed.ellipse([20,10+off,58,46+off],0); ed.ellipse([24,4+off,62,44+off],0)
    d.bitmap((0,0),edge,fill=(222,170,20))
    d.rectangle([29,5+off,32,9+off],(110,80,30)); d.rectangle([29,5+off,32,6+off],(70,50,20))  # tige
    # lunettes
    d.rectangle([20,26+off,26,29+off],(10,10,10)); d.rectangle([29,26+off,35,29+off],(10,10,10))
    d.line([(26,27+off),(29,27+off)],(10,10,10)); d.point((21,26+off),(255,255,255)); d.point((30,26+off),(255,255,255))
    d.line([(22,34+off),(26,35+off)],(120,70,10))
    # étincelles
    for (x,y) in [(10,12),(56,50),(8,44)]:
        c=GC[(x+frame)%4]; d.point((x,y),c); d.point((x-1,y),c); d.point((x+1,y),c); d.point((x,y-1),c); d.point((x,y+1),c)
    text(img,"NANO",10,56,G["yellow"]); text(img,"BANANA",30,56,(255,255,255))
    return img

def save(img,name,scale=8):
    img.save(f"{name}.png")
    img.resize((S*scale,S*scale),Image.NEAREST).save(f"{name}_preview.png")

if __name__=="__main__":
    save(antwerp(),"1_antwerp_sunset")
    save(matrix(),"2_google_led_matrix")
    save(banana(),"3_nano_banana")
    for name,fn in [("1_antwerp_sunset",antwerp),("3_nano_banana",banana)]:
        fr=[fn(i) for i in range(4)]
        fr[0].save(f"{name}.gif",save_all=True,append_images=fr[1:],duration=350,loop=0)
