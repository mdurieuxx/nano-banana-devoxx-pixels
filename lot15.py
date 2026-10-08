import math
from lot10 import *

def f_owl(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 24, 71, 22)
    d.rectangle([6, 38, 58, 40], (150, 90, 30)); d.line([(6, 41), (58, 41)], (90, 50, 10))
    for x in (10, 50): d.rectangle([x, 35, x+3, 37], (60, 200, 70))
    cx, cy = 32, 25 + sc(math.sin(2*ph))
    PU, PD = (140, 90, 235), (70, 30, 150)
    fl = sc(1.5*math.sin(4*ph))
    raster(d, ell(cx-12+fl, cy+2, 3, 8), (100, 60, 200), PD); raster(d, ell(cx+12-fl, cy+2, 3, 8), (100, 60, 200), PD)
    d.polygon([(cx-10, cy-9), (cx-9, cy-16), (cx-4, cy-11)], fill=PU, outline=PD); d.polygon([(cx+10, cy-9), (cx+9, cy-16), (cx+4, cy-11)], fill=PU, outline=PD)
    raster(d, ell(cx, cy, 11, 12), PU, PD, (0, 6, 64, 42))
    raster(d, ell(cx, cy+5, 7, 7), (255, 205, 80), (200, 120, 20))
    for k in range(3): d.point((cx-3+k*3, cy+4+ (k % 2)*3), (200, 120, 20)); d.point((cx-2+k*3, cy+7), (200, 120, 20))
    lk = sc(1.5*math.sin(ph))
    for s in (-1, 1):
        raster(d, ell(cx+s*5, cy-4, 4, 4), (255, 245, 150), PD)
        if f % 30 < 2: d.line([(cx+s*5-2, cy-4), (cx+s*5+2, cy-4)], BLK)
        else: d.rectangle([cx+s*5-1+lk, cy-5, cx+s*5+lk, cy-3], BLK); d.point((cx+s*5-1+lk, cy-5), WHITE)
    d.polygon([(cx-2, cy), (cx+2, cy), (cx, cy+4)], fill=(252, 130, 10))
    d.polygon([(cx-9, cy-12), (cx+9, cy-12), (cx, cy-9)], fill=BLK); d.rectangle([cx-4, cy-15, cx+4, cy-13], BLK)
    d.line([(cx+9, cy-12), (cx+11, cy-8 + (f//5) % 2)], YEL)
    d.rectangle([cx-6, 37, cx-3, 38], (252, 130, 10)); d.rectangle([cx+3, 37, cx+6, 38], (252, 130, 10))
    gemini_star(d, 53, 18 + sc(2*math.sin(ph)), 4, 2*ph); minicloud(d, 4, 16 + sc(2*math.sin(ph+1)))
    hdr(d); return img

def f_bee(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 22, 83, 20)
    for i, (x, c) in enumerate(((10, RED), (26, YEL), (44, (255, 90, 200)), (56, (150, 90, 255)))):
        sw = sc(math.sin(2*ph + i))
        d.line([(x, 41), (x+sw, 36)], (50, 190, 70), 1)
        for dx, dy in ((0, -1), (2, 0), (-2, 0), (0, 1)): d.point((x+sw+dx, 35+dy), c)
        d.point((x+sw, 35), YEL if c != YEL else RED)
    bx, by = 30 + sc(3*math.sin(ph)), 22 + sc(2*math.sin(2*ph))
    for k in range(1, 7):
        t = ph - k*0.18
        d.point((30 + sc(3*math.sin(t)) - 12 - k*0 , 22 + sc(2*math.sin(2*t)) + 8), BLK) if False else None
    wl = 3 if f % 2 == 0 else 1
    raster(d, ell(bx-2, by-9, 5, wl+1), (170, 235, 255), (60, 150, 230)); raster(d, ell(bx+5, by-9, 5, wl+1), (170, 235, 255), (60, 150, 230))
    d.polygon([(bx+10, by-1), (bx+16, by+1), (bx+10, by+3)], fill=BLK)
    raster(d, ell(bx, by+1, 11, 8), lambda x, y: BLK if (x-bx) % 6 in (0, 1) and x > bx-6 else (255, 215, 20), BLK, (0, 8, 64, 43))
    raster(d, ell(bx-9, by+2, 5, 5), (255, 215, 20), BLK)
    for s in ((bx-12, by-8), (bx-8, by-8)): d.line([s, (s[0]-1, s[1]-3)], BLK); d.point((s[0]-1, s[1]-4), RED)
    d.rectangle([bx-11, by, bx-10, by+2], BLK) if f % 30 >= 2 else d.line([(bx-12, by+1), (bx-9, by+1)], BLK); d.point((bx-11, by), WHITE) if f % 30 >= 2 else None
    for dx, dy in ((-11, 5), (-10, 6), (-9, 6), (-8, 5)): d.point((bx+dx, by+dy), BLK)
    d.point((bx-12, by+4), (255, 120, 150))
    gemini_star(d, 52, 15 + sc(2*math.sin(ph)), 4, 2*ph); minicloud(d, 4, 14 + sc(2*math.sin(ph+1)))
    hdr(d); return img

def f_uni(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 24, 91, 20)
    cx, cy = 32, 25 + sc(math.sin(2*ph))
    for side in (-1, 1):
        for b in range(4):
            pts = []
            for k in range(16):
                t = k/15.0
                x = cx + side*(9 + b*2.2 + 5*t + 2*math.sin(2*math.pi*(t*1.2 - f/30.0 + b*0.1)))
                pts.append((sc(x), sc(cy - 6 + k*1.5)))
            for (x, y) in pts:
                if y <= 40: d.point((x, y), COLS[b]); d.point((x, y+1), COLS[b])
    for s in (-1, 1): d.polygon([(cx+s*5, cy-8), (cx+s*8, cy-14), (cx+s*2, cy-10)], fill=(255, 150, 215), outline=(190, 60, 140))
    raster(d, ell(cx, cy, 8, 10), (255, 150, 215), (190, 60, 140), (0, 6, 64, 42))
    raster(d, ell(cx, cy+6, 5, 4), (255, 200, 235), (190, 60, 140))
    d.polygon([(cx, cy-20), (cx-3, cy-9), (cx+3, cy-9)], fill=YEL, outline=ORG)
    d.line([(cx-1, cy-14), (cx+1, cy-15)], ORG); d.line([(cx-2, cy-11), (cx+2, cy-12)], ORG)
    for s in (-1, 1):
        if f % 30 < 2: d.line([(cx+s*4-1, cy-1), (cx+s*4+1, cy-1)], BLK)
        else: d.rectangle([cx+s*4-1, cy-3, cx+s*4, cy+1], BLK); d.point((cx+s*4-1, cy-3), WHITE); d.point((cx+s*4, cy-1), (150, 100, 255))
        d.point((cx+s*7, cy+2), (255, 90, 130)); d.point((cx+s*2, cy+6), (190, 60, 140))
    for dx, dy in ((-2, 8), (-1, 9), (0, 9), (1, 9), (2, 8)): d.point((cx+dx, cy+dy-1), (190, 60, 140))
    gemini_star(d, cx, cy-21 if False else 7, 1, 0) if False else None
    gemini_star(d, 8, 22 + sc(2*math.sin(ph)), 4, 2*ph); gemini_star(d, 55, 16 + sc(2*math.sin(ph+2)), 3, -2*ph)
    hdr(d); return img

def f_panda(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 24, 13, 22)
    cx, cy = 28, 20 + sc(math.sin(2*ph))
    bx = 50 + sc(math.sin(ph)); 
    d.line([(bx, 12), (bx, 41)], (60, 200, 80), 3)
    for yy in (18, 26, 34): d.line([(bx-1, yy), (bx+1, yy)], (20, 120, 40))
    raster(d, ell(bx-4, 14, 4, 2), (90, 220, 90), (20, 120, 40)); raster(d, ell(bx+5, 21, 4, 2), (90, 220, 90), (20, 120, 40))
    raster(d, ell(cx, 34, 13, 9), (250, 250, 250), BLK, (0, 8, 64, 42))
    raster(d, ell(cx-13, 33, 3, 6), BLK, None); 
    arm = sc(2*math.sin(2*ph))
    raster(d, ell(cx+13, 30 + arm, 3, 5), BLK, None)
    d.line([(cx+14, 28+arm), (bx-1, 24)], BLK, 2)
    for s in (-1, 1): raster(d, ell(cx+s*7, 41, 3, 2), BLK, None)
    d.line([(cx-9, 28), (cx+9, 28)], RED, 2); d.rectangle([cx-1, 29, cx+1, 32], RED)
    for s in (-1, 1): raster(d, ell(cx+s*9, cy-8, 3, 3), BLK, None)
    raster(d, ell(cx, cy, 11, 9), (250, 250, 250), BLK)
    for s in (-1, 1):
        raster(d, ell(cx+s*5, cy-1, 3, 4), BLK, None)
        if f % 30 >= 2: d.rectangle([cx+s*5-1, cy-2, cx+s*5, cy-1], WHITE)
    d.rectangle([cx-1, cy+2, cx+1, cy+3], BLK)
    if (f // 5) % 2 == 0: d.line([(cx-2, cy+5), (cx+2, cy+5)], BLK)
    else: d.rectangle([cx-1, cy+5, cx+1, cy+6], (255, 90, 130))
    gemini_star(d, 10, 22 + sc(2*math.sin(ph)), 4, 2*ph); minicloud(d, 52, 8 + sc(2*math.sin(ph+1)) + 0) if False else minicloud(d, 4, 12 + sc(2*math.sin(ph+1)))
    hdr(d); return img

def f_cactus(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    GRN2, GD2 = (60, 205, 80), (20, 110, 40)
    sky(d, f, 32, 24, 37, 22)
    raster(d, ell(32, 41, 22, 3), (245, 160, 50), (200, 100, 20), (0, 36, 64, 42))
    cx, cy = 32, 26 + sc(2*math.sin(2*ph))
    w = sc(3*math.sin(4*ph))
    raster(d, lambda x, y: 18 <= x <= 24 and cy-4 <= y <= cy+4, GRN2, GD2); raster(d, lambda x, y: 18 <= x <= 21 and cy-12-w <= y <= cy-3, GRN2, GD2)
    raster(d, lambda x, y: 40 <= x <= 46 and cy-6 <= y <= cy+2, GRN2, GD2); raster(d, lambda x, y: 43 <= x <= 46 and cy-14+w <= y <= cy-5, GRN2, GD2)
    raster(d, lambda x, y: ((x-cx)/(7.4))**2 + ((y-cy)/(14.4))**2 <= 1, lambda x, y: (110, 235, 120) if x < cx-2 else GRN2, GD2, (0, 8, 64, 42))
    for k, (dx, dy) in enumerate(((-3, -6), (3, -2), (-3, 3), (3, 7), (0, -10))): d.point((cx+dx, cy+dy), (240, 255, 200))
    d.rectangle([cx-6, cy-5, cx-1, cy-2], BLK); d.rectangle([cx+1, cy-5, cx+6, cy-2], BLK); d.line([(cx-1, cy-4), (cx+1, cy-4)], BLK)
    d.point((cx-5, cy-5), WHITE); d.point((cx+2, cy-5), WHITE)
    for dx, dy in ((-3, 1), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 1)): d.point((cx+dx, cy+dy), BLK)
    for s in (-1, 1): d.point((cx+s*6, cy+1), (255, 120, 160))
    fy = cy-15
    if (f//3) % 2: d.point((cx, fy-4), (255, 90, 190)); d.point((cx-4, fy), (255, 90, 190))
    for dx, dy in ((0, -2), (2, 0), (-2, 0), (0, 2)): raster(d, ell(cx+dx, fy+dy, 1, 1), (255, 90, 190), None)
    d.rectangle([cx-1, fy-1, cx, fy], YEL)
    gemini_star(d, 54, 14 + sc(2*math.sin(ph)), 4, 2*ph); minicloud(d, 4, 14 + sc(2*math.sin(ph+1)))
    hdr(d); return img

def f_crab(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    RDc, RDd = (235, 50, 50), (130, 10, 20)
    sky(d, f, 32, 24, 47, 22)
    wy = lambda x: 39 + sc(1*math.sin(2*math.pi*(x/16 - f/30)))
    raster(d, lambda x, y: y >= wy(x), lambda x, y: (120, 200, 255) if y < wy(x)+1 else (30, 110, 230), None, (0, 36, 64, 42))
    cx, cy = 32, 29 + sc(math.sin(4*ph))
    for s in (-1, 1):
        for k in range(3):
            lx = cx + s*(9 + k*2); wig = (f//2 + k) % 2
            d.line([(cx+s*(7+k*2), cy+5), (lx+s*3, cy+9+wig)], RDd)
            d.line([(lx+s*3, cy+9+wig), (lx+s*4, 37)], RDd)
    for s, off in ((-1, 0), (1, 1)):
        cw = sc(3*math.sin(2*ph + off*math.pi))
        d.line([(cx+s*10, cy), (cx+s*15, cy-4+cw)], RDd, 2)
        raster(d, ell(cx+s*17, cy-9+cw, 5, 5), RDc, RDd)
        d.polygon([(cx+s*17, cy-9+cw), (cx+s*21, cy-14+cw), (cx+s*15, cy-14+cw)], fill=BLK)
    for s in (-1, 1):
        d.line([(cx+s*5, cy-6), (cx+s*5, cy-10)], RDd)
        raster(d, ell(cx+s*5, cy-12, 2, 2), WHITE, RDd)
        d.rectangle([cx+s*5, cy-12, cx+s*5, cy-11], BLK)
    raster(d, ell(cx, cy, 12, 7), lambda x, y: (255, 110, 90) if y < cy-2 else RDc, RDd)
    for dx, dy in ((-3, 2), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 2)): d.point((cx+dx, cy+dy), BLK)
    for s in (-1, 1): d.point((cx+s*7, cy+1), (255, 170, 190))
    gemini_star(d, 32, 12 + sc(2*math.sin(ph)), 3, 2*ph) if False else gemini_star(d, 32, 14 + sc(2*math.sin(ph)), 3, 2*ph)
    minicloud(d, 4, 20 + sc(2*math.sin(ph+1))); minicloud(d, 53, 20 + sc(2*math.sin(ph+2)))
    hdr(d); return img

if __name__ == "__main__":
    M = {"OWL": f_owl, "BEE": f_bee, "UNI": f_uni, "PANDA": f_panda, "CACTUS": f_cactus, "CRAB": f_crab}
    for n, fn in M.items(): save([fn(i) for i in range(N)], "L15_" + n)
    sh = Image.new("RGB", (256*3, 256*2))
    for k, (n, fn) in enumerate(M.items()): sh.paste(fn(8).resize((256, 256), Image.NEAREST), (256*(k % 3), 256*(k//3)))
    sh.save("/tmp/prev15.png")
