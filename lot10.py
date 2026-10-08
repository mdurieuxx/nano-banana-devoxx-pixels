import math
from PIL import Image, ImageDraw
from newchar import *

WH, GR = (240, 244, 250), (150, 160, 200)
def hdr(d, word="GEMINI"):
    text1x(d, "GOOGLE CLOUD", 8, 2, YEL)
    kw_bottom(d, 0, word)
    text2x(d, "DEVOXX", 9, 53, BRAND)
def raster(d, inside, col, out=None, box=(0, 8, 64, 43)):
    pts = {(x, y) for x in range(box[0], box[2]) for y in range(box[1], box[3]) if inside(x, y)}
    for p in pts: d.point(p, col(*p) if callable(col) else col)
    if out:
        for x, y in pts:
            for n in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if n not in pts: d.point(n, out)
def ell(cx, cy, rx, ry): return lambda x, y: ((x-cx)/(rx+.4))**2 + ((y-cy)/(ry+.4))**2 <= 1
def anyof(*fs): return lambda x, y: any(f(x, y) for f in fs)
def new(): return Image.new("RGB", (S, S), BLK)
def sc(r): return round(r)

CW, CS, CO = (130, 195, 255), (70, 130, 240), (20, 70, 200)
def f_cloud(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 22, 61, 22)
    cx, cy = 32, 21 + sc(math.sin(2*ph))
    shp = anyof(ell(cx-11, cy+2, 7, 7), ell(cx, cy-3, 9, 9), ell(cx+11, cy+2, 7, 7), ell(cx-5, cy+5, 7, 7), ell(cx+5, cy+5, 7, 7))
    for i in range(5):
        y = 35 + (f + i*2) % 6
        if y <= 40: d.rectangle([cx-12+i*6, y, cx-12+i*6, y+1], COLS[i % 4])
    raster(d, shp, lambda x, y: CW if y < cy+6 else CS, CO)
    wave = sc(2*math.sin(4*ph))
    raster(d, ell(cx-17, cy+3+wave, 2, 2), CW, CO)
    sy = cy-11 + sc(math.sin(2*ph+1))
    raster(d, ell(cx+16, cy+3, 2, 2), CW, CO)
    d.line([(cx+16, cy+1), (cx+16, sy+4)], CO)
    gemini_star(d, cx+16, sy, 4, 2*ph)
    ex = 4
    if f % 30 < 2:
        for s in (-1, 1): d.line([(cx+s*ex-1, cy+2), (cx+s*ex+1, cy+2)], BLK)
    else:
        for s in (-1, 1):
            d.rectangle([cx+s*ex-1, cy, cx+s*ex, cy+3], BLK); d.point((cx+s*ex-1, cy), WHITE)
    for s in (-1, 1): d.rectangle([cx+s*8-1, cy+4, cx+s*8, cy+4], (255, 130, 160))
    for dx, dy in ((-2, 5), (-1, 6), (0, 6), (1, 6), (2, 5)): d.point((cx+dx, cy+dy), (200, 40, 80))
    minicloud(d, 5 + (f*0), 14 + sc(2*math.sin(ph)))
    hdr(d); return img

SU, SG = (255, 190, 90), (190, 105, 20)
def f_astro(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 30, 22, 77, 14)
    raster(d, ell(8, 44, 12, 12), lambda x, y: (40, 160, 70) if (x*7 + y*13 + x*y) % 11 < 3 else (30, 100, 220), (140, 210, 255), (0, 30, 64, 42))
    bob = sc(1.5*math.sin(ph*2))
    ax, ay = 28, 12 + bob
    raster(d, ell(ax+7, ay+17, 3, 2), (150, 150, 170))
    d.rectangle([ax-3, ay+9, ax-1, ay+19], (150, 150, 170)); d.rectangle([ax+15, ay+9, ax+17, ay+19], (150, 150, 170))
    raster(d, lambda x, y: ax <= x <= ax+14 and ay+9 <= y <= ay+19, SU, SG)
    for i, c in enumerate((RED, YEL, GRN, BLUE)): d.point((ax+4+i*2 - (1 if i > 1 else 0), ay+13), c)
    d.rectangle([ax+4, ay+15, ax+10, ay+16], (120, 130, 170))
    lk = sc(2.5*math.sin(ph*2 + 1))
    for lx in (ax+2, ax+9):
        s = lk if lx == ax+2 else -lk
        raster(d, lambda x, y, lx=lx, s=s: lx+s <= x <= lx+s+3 and ay+20 <= y <= ay+27, SU, SG)
    raster(d, ell(ax+7, ay+4, 7, 7), SU, SG)
    raster(d, ell(ax+8, ay+4, 5, 4), (20, 30, 100))
    for p in ((ax+6, ay+2), (ax+7, ay+2), (ax+6, ay+3)): d.point(p, (120, 220, 255))
    d.point((ax+10, ay+6), (60, 90, 200))
    wv = sc(2*math.sin(4*ph))
    d.line([(ax-2, ay+11), (ax-6, ay+7+wv)], SU); d.rectangle([ax-8, ay+5+wv, ax-6, ay+7+wv], SU)
    ly = 24 + sc(2*math.sin(2*ph + 3))
    d.line([(ax+16, ay+12), (47, ly+4)], SU)
    d.rectangle([46, ly-6, 58, ly+1], (150, 70, 240)); d.rectangle([47, ly-5, 57, ly], BLK)
    d.line([(44, ly+2), (60, ly+2)], (240, 70, 200))
    gemini_star(d, 52, ly-3, 3, 2*ph)
    for k in range(3): d.line([(48, ly-4+k*2), (48+2+(f//2+k*3) % 3, ly-4+k*2)], COLS[k])
    hdr(d); return img

OR, ORD = (236, 140, 40), (150, 70, 10)
def f_cat(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    for i in range(5):
        for side in (0, 1):
            h = 3 + sc(3*(1+math.sin(2*ph*2 + i*1.7 + side))/1.0)
            x = 3 + i*3 if side == 0 else 61 - i*3 - 1
            d.rectangle([x, 40-h, x+1, 40], COLS[(i+side*2) % 4])
    cx, cy = 32, 22 + sc(math.sin(2*ph))
    tw = sc(2*math.sin(2*ph))
    d.line([(42, 38), (48, 36), (51+tw, 31), (50+tw, 27)], OR, 2); d.point((50+tw, 26), WH)
    raster(d, ell(cx, 36, 11, 5), OR, ORD)
    d.polygon([(cx-11, cy-2), (cx-10, cy-12+ (1 if f % 30 < 2 else 0)), (cx-4, cy-7)], fill=OR, outline=ORD)
    d.polygon([(cx+11, cy-2), (cx+10, cy-12), (cx+4, cy-7)], fill=OR, outline=ORD)
    d.point((cx-9, cy-8), (255, 150, 170)); d.point((cx+9, cy-8), (255, 150, 170))
    raster(d, ell(cx, cy, 11, 9), OR, ORD)
    for dx in (-3, 0, 3): d.line([(cx+dx, cy-8), (cx+dx, cy-5)], ORD)
    for s in (-1, 1):
        if f % 30 < 2: d.line([(cx+s*5-1, cy), (cx+s*5+1, cy)], BLK)
        else:
            d.rectangle([cx+s*5-1, cy-2, cx+s*5+1, cy+1], (110, 230, 90)); d.rectangle([cx+s*5, cy-2, cx+s*5, cy+1], BLK); d.point((cx+s*5-1, cy-2), WH)
        d.line([(cx+s*9, cy+3), (cx+s*13 if False else cx+s*12, cy+2)], WH); d.line([(cx+s*9, cy+5), (cx+s*12, cy+6)], WH)
    d.rectangle([cx-1, cy+3, cx+1, cy+4], (255, 130, 160)); d.point((cx, cy+5), BLK); d.point((cx-1, cy+6), BLK); d.point((cx+1, cy+6), BLK)
    d.arc([cx-12, cy-15, cx+12, cy+4], 200, 340, CO, 2) if False else d.line([(cx-11, cy-1), (cx-10, cy-10), (cx, cy-13), (cx+10, cy-10), (cx+11, cy-1)], CO, 2)
    for s, c in ((-1, RED), (1, YEL)): d.rectangle([cx+s*12-1+(0 if s > 0 else -1), cy-2, cx+s*12+1+(1 if s > 0 else 0), cy+4], c)
    d.rectangle([cx-9, 38, cx-6, 40], WH); d.rectangle([cx+6, 38, cx+9, 40], WH)
    gemini_star(d, 11, 18 + sc(2*math.sin(ph)), 3, 2*ph)
    minicloud(d, 52, 12 + sc(2*math.sin(ph + 2)))
    hdr(d); return img

def f_duck(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 30, 20, 99, 16)
    bob = sc(1.5*math.sin(2*ph)); dx, dy = 28, 28 + bob
    raster(d, lambda x, y: y >= 38 + sc(1.1*math.sin(2*math.pi*(x/16 - f/30))), lambda x, y: (120, 200, 255) if y < 39 + sc(1.1*math.sin(2*math.pi*(x/16 - f/30))) else (30, 110, 230), None, (0, 33, 64, 42))
    for i in range(3):
        by = 40 - (f + i*10) % 30
        d.point((12+i*20 + (1 if (f//4+i) % 2 else 0), by), (180, 230, 255))
    d.polygon([(dx-11, dy+1), (dx-15, dy-4), (dx-9, dy-1)], fill=(255, 226, 40), outline=(200, 120, 10))
    raster(d, anyof(ell(dx, dy+3, 13, 7), ell(dx+9, dy-7, 7, 7)), (255, 226, 40), (200, 120, 10), (0, 8, 64, 43))
    raster(d, ell(dx-1, dy+3, 6, 3), (240, 190, 20), (200, 120, 10))
    d.rectangle([dx+14, dy-8, dx+19, dy-6], (252, 120, 4)); d.rectangle([dx+14, dy-5, dx+18, dy-5], (200, 80, 0))
    d.rectangle([dx+9, dy-10, dx+10, dy-9], BLK); d.point((dx+9, dy-10), WH)
    d.point((dx+7, dy-6), (255, 140, 160))
    d.line([(dx+3, dy-1), (dx+8, dy-1)], RED); d.rectangle([dx+4, dy, dx+7, dy+1], BLUE)
    gemini_star(d, dx+9, dy-18 if False else 12, 3, 2*ph) if False else gemini_star(d, 52, 17 + sc(2*math.sin(ph)), 4, 2*ph)
    minicloud(d, 5, 13 + sc(2*math.sin(ph + 1)))
    hdr(d); return img

OP = {"b": (252, 150, 20), "d": (180, 90, 0), "w": WHITE, "k": BLK, "c": (255, 230, 150), "r": RED}
def f_twins(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 24, 123, 14)
    hy = 12 + sc(math.sin(2*ph))
    mir = [row[::-1] for row in ROBO]
    sprite(d, ROBO, 6, hy, RP); sprite(d, mir, 44, hy, OP)
    if (f // 6) % 2: d.point((12, hy), BLK); d.point((51, hy), BLK)
    t = (f % 30) / 30.0
    hx = 23 + sc(4*max(0, math.sin(2*math.pi*t)))
    for sd, pal, base in ((0, RB, 6), (1, OP["b"], 44)):
        by = hy + 14
        d.rectangle([base+3, by, base+10, by+7], pal); d.rectangle([base+5, by+2, base+8, by+4], WH if sd == 0 else (255, 230, 150))
        d.rectangle([base+3, by+8, base+5, by+10], pal); d.rectangle([base+8, by+8, base+10, by+10], pal)
        d.rectangle([base+2, by+11, base+5, by+11], WH); d.rectangle([base+8, by+11, base+11, by+11], WH)
    ay = hy + 14
    d.line([(17, ay+2), (hx, ay-4)], RB, 2); d.rectangle([hx, ay-6, hx+2, ay-3], WH)
    d.line([(46, ay+2), (63-hx, ay-4)], OP["b"], 2); d.rectangle([63-hx-2, ay-6, 63-hx, ay-3], WH)
    pulse = 1 + sc(3*max(0, math.sin(2*math.pi*t)))
    gemini_star(d, 32, ay-5, 2+pulse, 2*ph)
    if pulse >= 3:
        for k in range(4):
            a = k*math.pi/2 + math.pi/4
            d.point((32+sc(8*math.cos(a)), ay-5+sc(8*math.sin(a))), COLS[k])
    d.line([(4, 40), (60, 40)], (60, 60, 140))
    minicloud(d, 28, 12 + sc(math.sin(ph)))
    hdr(d); return img

CR = (255, 205, 130)
def f_dog(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    cx, cy = 32, 21 + sc(math.sin(2*ph))
    for k in range(3):
        a = ph + k*2*math.pi/3
        x, y = 32 + 25*math.cos(a), 24 + 11*math.sin(a)
        if k == 0: minicloud(d, sc(x)-3, sc(y)-2)
        else: gemini_star(d, sc(x), sc(y), 3, 2*ph)
    raster(d, ell(cx, 37, 9, 3), CR, GR, (0, 8, 64, 42))
    ew = sc(math.sin(4*ph))
    d.polygon([(cx-11, cy-1), (cx-10, cy-12+ew), (cx-3, cy-8)], fill=OR, outline=ORD)
    d.polygon([(cx+11, cy-1), (cx+10, cy-12-ew), (cx+3, cy-8)], fill=OR, outline=ORD)
    d.point((cx-9, cy-8+ew), (255, 150, 170)); d.point((cx+9, cy-8-ew), (255, 150, 170))
    raster(d, ell(cx, cy, 11, 9), OR, ORD)
    raster(d, anyof(ell(cx, cy+5, 7, 5), ell(cx-6, cy+3, 3, 4), ell(cx+6, cy+3, 3, 4)), CR, None)
    for s in (-1, 1):
        if f % 30 < 2: d.line([(cx+s*5-1, cy-1), (cx+s*5+1, cy-1)], BLK)
        else: d.rectangle([cx+s*5-1, cy-3, cx+s*5, cy], BLK); d.point((cx+s*5-1, cy-3), CR)
        d.point((cx+s*5, cy-6), (255, 210, 150)); d.point((cx+s*5+s, cy-6), (255, 210, 150))
    d.rectangle([cx-2, cy+2, cx+1, cy+3], BLK)
    d.line([(cx-1, cy+4), (cx-1, cy+5)], BLK); d.line([(cx-4, cy+6), (cx-2, cy+6)], BLK); d.line([(cx+1, cy+6), (cx+3, cy+6)], BLK)
    if (f // 5) % 2 == 0: d.rectangle([cx-1, cy+7, cx+1, cy+9], (255, 90, 130)); d.point((cx, cy+8), (200, 40, 80))
    d.rectangle([cx-8, 31 + (cy-21), cx+8, 32 + (cy-21)], CO)
    gemini_star(d, cx, 34 + (cy-21), 2, 0) if False else d.rectangle([cx-1, 33+(cy-21), cx+1, 35+(cy-21)], YEL)
    hdr(d); return img

def f_peng(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    for i in range(16):
        x = 3 + (i*37) % 58; y = 10 + (2*f + i*7) % 30
        if abs(x-32) > 12 or y < 12: d.point((x + (1 if (f//5+i) % 2 else 0), y), YEL if i % 2 else (120, 220, 255))
    bob = sc(2*math.sin(2*ph))
    cx, cy = 32, 26+bob
    raster(d, lambda x, y: y >= 39 and abs(x-32) < 22 - (y-39)*3, (90, 205, 255), (40, 140, 230), (0, 38, 64, 42))
    raster(d, ell(cx, cy, 10, 13), (35, 35, 75), None)
    raster(d, ell(cx, cy+3, 7, 10), (255, 236, 170), None)
    fl = sc(3*math.sin(4*ph))
    d.line([(cx-10, cy-3), (cx-14, cy+4-fl)], (35, 35, 75), 3); d.line([(cx+10, cy-3), (cx+14, cy+4+fl)], (35, 35, 75), 3)
    for s in (-1, 1):
        d.rectangle([cx+s*4-2, cy-9, cx+s*4+1, cy-6], WH)
        if f % 30 >= 2: d.rectangle([cx+s*4-1+(0 if s < 0 else 0), cy-8, cx+s*4, cy-7], BLK)
    d.polygon([(cx-2, cy-5), (cx+2, cy-5), (cx, cy-2)], fill=(252, 130, 10))
    d.polygon([(cx-6, cy-12), (cx+6, cy-12), (cx, cy-22)], fill=RED, outline=None) if False else d.polygon([(cx-4, cy-12), (cx+4, cy-12), (cx, cy-19)], fill=RED)
    d.point((cx, cy-20), YEL)
    for i, c in enumerate((RED, YEL, GRN, BLUE)): d.rectangle([cx-8+i*4, cy+0, cx-6+i*4, cy+1], c)
    d.rectangle([cx-8, cy+0, cx-6, cy+3], RED) if False else None
    d.rectangle([cx-6, 38, cx-2, 39], (252, 130, 10)); d.rectangle([cx+2, 38, cx+6, 39], (252, 130, 10))
    sy = 11 + sc(2*math.sin(ph))
    gemini_star(d, 50, sy+4, 4, 2*ph); minicloud(d, 6, sy+3)
    hdr(d); return img

def f_rocket(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 24, 5, 14)
    for i, x in enumerate((7, 49, 14, 53)):
        y = 10 + (f + i*8) % 30
        if y < 36: minicloud(d, x, y)
    rx, ry = 32 + sc(math.sin(2*ph)), 17
    ln = 9 + (f % 3) * 2
    for i, c in enumerate((YEL, ORG, RED)):
        d.rectangle([rx-3+i, ry+13+i*3, rx+3-i, ry+13+i*3+ln//3], c)
    d.polygon([(rx-6, ry+3), (rx-11, ry+14), (rx-5, ry+10)], fill=RED); d.polygon([(rx+6, ry+3), (rx+11, ry+14), (rx+5, ry+10)], fill=RED)
    raster(d, ell(rx, ry+2, 6, 12), WH, GR, (0, 4, 64, 42))
    d.polygon([(rx-6, ry-5), (rx+6, ry-5), (rx, ry-13)], fill=RED)
    d.rectangle([rx-6, ry+9, rx+6, ry+10], CO)
    raster(d, ell(rx, ry+1, 3, 3), (20, 30, 100), (140, 210, 255))
    gemini_star(d, rx, ry+1, 2, 2*ph)
    a = ph
    gemini_star(d, 32+sc(24*math.cos(a)), 26+sc(8*math.sin(a)), 3, -2*ph)
    hdr(d, "GEMINI"); return img

if __name__ == "__main__":
    S8 = {"CLOUD": f_cloud, "ASTRO": f_astro, "CAT": f_cat, "DUCK": f_duck, "TWINS": f_twins, "DOG": f_dog, "PENG": f_peng, "ROCKET": f_rocket}
    import sys
    sel = sys.argv[1:] or list(S8)
    for n in sel:
        save([S8[n](i) for i in range(N)], "L10_" + n)
        sheet = Image.new("RGB", (192*4, 192))
        for k, fr in enumerate((0, 7, 15, 22)): sheet.paste(S8[n](fr).resize((192, 192), Image.NEAREST), (192*k, 0))
        sheet.save(f"/tmp/prev_{n}.png")
