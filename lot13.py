import math
from lot10 import *

def f_octo(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 24, 17, 18)
    cx, cy = 32, 17 + sc(1.5*math.sin(2*ph))
    PU, PD, PL = (235, 60, 175), (140, 20, 110), (255, 150, 215)
    for i in range(8):
        off = (i - 3.5) * 3.2
        pts = []
        for k in range(15):
            t = k / 14.0
            x = cx + off * (1 + 0.5*t) + 3*t*math.sin(2*math.pi*(t*1.2 - f/30.0 + i*0.15))
            pts.append((sc(x), cy + 6 + k*1.6))
        for (x, y) in pts:
            if y <= 40: d.rectangle([x, sc(y), x+1, sc(y)+1], PU)
        for k in range(3, 15, 3):
            x, y = pts[k]
            if y <= 41: d.point((x, sc(y)), PL)
    raster(d, ell(cx, cy, 11, 9), lambda x, y: PL if (y < cy-5 and x < cx-1) else PU, PD, (0, 4, 64, 43))
    for s in (-1, 1):
        if f % 30 < 2: d.line([(cx+s*5-1, cy), (cx+s*5+1, cy)], BLK)
        else:
            d.rectangle([cx+s*5-2, cy-3, cx+s*5+1, cy+1], WHITE); d.rectangle([cx+s*5-1+(0 if s < 0 else 0), cy-2, cx+s*5, cy], BLK)
        d.rectangle([cx+s*8-1, cy+3, cx+s*8, cy+3], (255, 220, 235))
    for dx, dy in ((-3, 4), (-2, 5), (-1, 5), (0, 5), (1, 5), (2, 5), (3, 4)): d.point((cx+dx, cy+dy), BLK)
    gemini_star(d, 10, 18 + sc(2*math.sin(ph)), 4, 2*ph)
    minicloud(d, 50, 12 + sc(2*math.sin(ph+1)))
    for i in range(3): d.point((46 + i*5, 40 - (f + i*10) % 30), (120, 220, 255))
    hdr(d); return img

def f_ufo(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 26, 29, 20)
    ux = 32 + sc(3*math.sin(ph)); uy = 17
    for y in range(uy+4, 42):
        hw = 3 + (y-uy-4)*0.55
        for x in range(sc(ux-hw), sc(ux+hw)+1):
            if (x + y + f//2) % 2 == 0: d.point((x, y), (255, 240, 110))
    ay = 36 + sc(2*math.sin(2*ph))
    minicloud(d, ux-4, ay-8 + 4)
    gemini_star(d, ux+7, ay-3, 3, 2*ph); gemini_star(d, ux-8, ay-9, 2, -2*ph)
    raster(d, ell(ux, uy-3, 6, 5), (110, 235, 255), (40, 150, 200), (0, 4, 64, 30))
    raster(d, ell(ux, uy-3, 3, 3), (90, 220, 90), (30, 120, 30), (0, 4, 64, 30))
    d.rectangle([ux-2, uy-4, ux-1, uy-3], BLK); d.rectangle([ux+1, uy-4, ux+2, uy-3], BLK)
    raster(d, ell(ux, uy+1, 15, 4), (160, 90, 245), (90, 30, 170), (0, 4, 64, 30))
    for k in range(5):
        d.point((ux-10+k*5, uy+1), COLS[(k + f//5) % 4])
    minicloud(d, 5, 22 + sc(2*math.sin(ph+2)))
    hdr(d); return img

def f_jelly(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 20, 41, 16)
    cx, cy = 32, 18 + sc(2*math.sin(ph))
    sq = sc(1*math.sin(2*ph))
    for i in range(7):
        off = (i-3)*3.6
        for k in range(16):
            t = k / 15.0
            x = cx + off*(1 - 0.2*t) + 2.5*t*math.sin(2*math.pi*(t - f/30.0 + i*0.2))
            y = cy + 8 + k*1.2
            if y <= 40: d.rectangle([sc(x), sc(y), sc(x), sc(y)+1], COLS[(i + k//5) % 4])
    raster(d, lambda x, y: ((x-cx)/(12.4+sq))**2 + ((y-cy)/(10.4-sq))**2 <= 1 and y <= cy+3, lambda x, y: (90, 230, 255) if y < cy-3 else ((200, 90, 255) if y < cy+1 else (255, 70, 190)), (30, 60, 200), (0, 4, 64, 30))
    for s in (-1, 1):
        if f % 30 < 2: d.line([(cx+s*5-1, cy-2), (cx+s*5+1, cy-2)], BLK)
        else:
            d.rectangle([cx+s*5-1, cy-4, cx+s*5, cy-1], BLK); d.point((cx+s*5-1, cy-4), WHITE)
    for dx, dy in ((-2, 0), (-1, 1), (0, 1), (1, 1), (2, 0)): d.point((cx+dx, cy+dy-1), BLK)
    for i in range(4): d.point((cx-8+i*5, cy-8+(i % 2)*2), WHITE)
    gemini_star(d, 8, 20 + sc(2*math.sin(ph)), 3, 2*ph); minicloud(d, 52, 14 + sc(2*math.sin(ph+1)))
    hdr(d); return img

GR_, GD, GL = (60, 205, 70), (20, 110, 40), (190, 245, 110)
def f_frog(f):
    img = new(); d = ImageDraw.Draw(img); ph = 2*math.pi*f/N
    sky(d, f, 32, 24, 57, 20)
    wy = lambda x: 39 + sc(1*math.sin(2*math.pi*(x/16 - f/30)))
    raster(d, lambda x, y: y >= wy(x), lambda x, y: (120, 200, 255) if y < wy(x)+1 else (30, 110, 230), None, (0, 36, 64, 42))
    raster(d, ell(30, 37, 16, 2), (30, 150, 60), (10, 90, 30), (0, 30, 64, 42))
    cx, cy = 30, 26 + sc(math.sin(2*ph))
    raster(d, ell(cx-9, cy+7, 4, 3), GR_, GD); raster(d, ell(cx+9, cy+7, 4, 3), GR_, GD)
    raster(d, ell(cx, cy+4, 9, 7), lambda x, y: GL if y > cy+4 else GR_, GD)
    raster(d, ell(cx, cy-3, 9, 6), GR_, GD)
    for s in (-1, 1):
        raster(d, ell(cx+s*6, cy-9, 3, 3), WHITE, GD)
        d.rectangle([cx+s*6, cy-9, cx+s*6+1, cy-8], BLK) if f % 30 >= 2 else d.line([(cx+s*6-1, cy-8), (cx+s*6+1, cy-8)], BLK)
        d.point((cx+s*7, cy-3), (255, 130, 150))
    d.line([(cx-5, cy-1), (cx+5, cy-1)], GD); d.point((cx-6, cy-2), GD); d.point((cx+6, cy-2), GD)
    sx, sy = 48, 13 + sc(2*math.sin(ph))
    t = f % 30
    if 12 <= t <= 17:
        L = min(t-11, 17-t+1)/3.0
        ex, ey = cx + (sx-cx)*L, (cy-1) + (sy-(cy-1))*L
        d.line([(cx+2, cy-1), (sc(ex), sc(ey))], (255, 90, 130), 2)
    gemini_star(d, sx, sy, 3, 2*ph)
    minicloud(d, 5, 12 + sc(2*math.sin(ph+1)))
    text1x(d, "GOOGLE CLOUD", 8, 2, YEL); text1x(d, "CATCH GEMINI", 8, 43, WHITE) if False else kw_bottom(d, f); text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    M = {"OCTO": f_octo, "UFO": f_ufo, "JELLY": f_jelly, "FROG": f_frog}
    for n, fn in M.items(): save([fn(i) for i in range(N)], "L13_" + n)
    sh = Image.new("RGB", (256*4, 256*2))
    for k, (n, fn) in enumerate(M.items()):
        for r, fr in enumerate((0, 14)): sh.paste(fn(fr).resize((256, 256), Image.NEAREST), (256*k, 256*r))
    sh.save("/tmp/prev13.png")
