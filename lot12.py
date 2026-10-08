import math
from lot10 import *
LETTER.update({k: FONT[k] for k in "AKSGIEMNDTHRYOPCUBL" if k in FONT})

def bubble(d, x, y, w, h):
    d.rectangle([x+1, y, x+w-1, y+h], WHITE); d.rectangle([x, y+1, x+w, y+h-1], WHITE)

def f_duck2(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 30, 20, 99, 16)
    bob = sc(1.5*math.sin(2*ph)); dx, dy = 22, 28 + bob
    wy = lambda x: 38 + sc(1.1*math.sin(2*math.pi*(x/16 - f/30)))
    raster(d, lambda x, y: y >= wy(x), lambda x, y: (120, 200, 255) if y < wy(x)+1 else (30, 110, 230), None, (0, 33, 64, 42))
    for i in range(3):
        d.point((12+i*20 + (1 if (f//4+i) % 2 else 0), 40 - (f + i*10) % 30), (180, 230, 255))
    d.polygon([(dx-11, dy+1), (dx-15, dy-4), (dx-9, dy-1)], fill=(255, 226, 40), outline=(200, 120, 10))
    raster(d, anyof(ell(dx, dy+3, 13, 7), ell(dx+9, dy-7, 7, 7)), lambda x, y: (255, 240, 90) if (y < dy-3 or (x < dx+10 and y < dy+1 and x > dx-8)) else (255, 220, 30), (200, 100, 10), (0, 8, 64, 43))
    raster(d, ell(dx-2, dy+3, 6, 3), (240, 170, 10), (200, 100, 10))
    d.rectangle([dx+14, dy-8, dx+19, dy-6], (252, 120, 4)); d.rectangle([dx+14, dy-5, dx+18, dy-5], (200, 70, 0))
    d.rectangle([dx+8, dy-10, dx+11, dy-9], BLK); d.rectangle([dx+8, dy-10, dx+9, dy-9], WHITE) if False else d.point((dx+8, dy-10), WHITE)
    if f % 30 < 2: d.line([(dx+8, dy-9), (dx+11, dy-9)], BLK)
    d.rectangle([dx+5, dy-6, dx+6, dy-5], (255, 120, 150))
    d.line([(dx+3, dy-1), (dx+8, dy-1)], RED); d.rectangle([dx+4, dy, dx+7, dy+1], BLUE)
    by = 11 + sc(1.5*math.sin(ph))
    bubble(d, 47, by, 10, 9)
    d.rectangle([45, by+11, 46, by+12], WHITE); d.point((43, by+14), WHITE)
    gemini_star(d, 52, by+4, 3, 2*ph)
    minicloud(d, 4, 13 + sc(2*math.sin(ph+1)))
    text1x(d, "GOOGLE CLOUD", 8, 2, YEL); text1x(d, "ASK GEMINI", 12, 43, WHITE); text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

def f_cat2(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    for i in range(5):
        for side in (0, 1):
            h = 3 + sc(3*(1+math.sin(4*ph + i*1.7 + side)))
            x = 3 + i*3 if side == 0 else 60 - i*3
            d.rectangle([x, 40-h, x+1, 40], COLS[(i+side*2) % 4])
    cx, cy = 32, 18 + sc(math.sin(2*ph))
    raster(d, lambda x, y: 18 <= x <= 46 and 28 <= y <= 39, (70, 60, 120), (150, 70, 240))
    d.rectangle([15, 40, 49, 41], (150, 70, 240))
    gemini_star(d, 32, 34, 4, 2*ph)
    for k in range(5):
        d.point((20 + (k*5 + f//3) % 25, 30 if k % 2 else 38), COLS[k % 4]) if False else None
    d.polygon([(cx-11, cy-2), (cx-10, cy-12+(1 if f % 30 < 2 else 0)), (cx-4, cy-7)], fill=OR, outline=ORD)
    d.polygon([(cx+11, cy-2), (cx+10, cy-12), (cx+4, cy-7)], fill=OR, outline=ORD)
    d.point((cx-9, cy-8), (255, 150, 170)); d.point((cx+9, cy-8), (255, 150, 170))
    raster(d, ell(cx, cy, 11, 9), OR, ORD)
    for dx in (-3, 0, 3): d.line([(cx+dx, cy-8), (cx+dx, cy-5)], ORD)
    for s in (-1, 1):
        if f % 30 < 2: d.line([(cx+s*5-1, cy), (cx+s*5+1, cy)], BLK)
        else:
            d.rectangle([cx+s*5-1, cy-2, cx+s*5+1, cy+1], (110, 230, 90)); d.rectangle([cx+s*5, cy-1, cx+s*5, cy+1], BLK); d.point((cx+s*5-1, cy-2), WHITE)
        d.line([(cx+s*9, cy+3), (cx+s*12, cy+2)], WHITE); d.line([(cx+s*9, cy+5), (cx+s*12, cy+6)], WHITE)
    d.rectangle([cx-1, cy+3, cx+1, cy+4], (255, 130, 160)); d.point((cx, cy+5), BLK); d.point((cx-1, cy+6), BLK); d.point((cx+1, cy+6), BLK)
    d.line([(cx-11, cy-1), (cx-10, cy-10), (cx, cy-13), (cx+10, cy-10), (cx+11, cy-1)], CO, 2)
    d.rectangle([cx-13, cy-2, cx-11, cy+4], RED); d.rectangle([cx+11, cy-2, cx+13, cy+4], YEL)
    tap = (f // 3) % 2
    raster(d, ell(cx-7, 28+tap, 3, 2), OR, ORD, (0, 20, 64, 42)); raster(d, ell(cx+7, 29-tap, 3, 2), OR, ORD, (0, 20, 64, 42))
    gemini_star(d, 8, 16 + sc(2*math.sin(ph)), 3, -2*ph)
    minicloud(d, 52, 12 + sc(2*math.sin(ph + 2)))
    hdr(d); return img

if __name__ == "__main__":
    import sys
    M = {"DUCK2": f_duck2, "CAT2": f_cat2}
    for n, fn in M.items():
        save([fn(i) for i in range(N)], "L12_" + n)
    sh = Image.new("RGB", (256*4, 256))
    for k, (fn, fr) in enumerate(((f_duck2, 0), (f_duck2, 15), (f_cat2, 0), (f_cat2, 20))): sh.paste(fn(fr).resize((256, 256), Image.NEAREST), (256*k, 0))
    sh.save("/tmp/prev12.png")
