import math
from PIL import Image, ImageDraw
from led_kit import *
from marc_lot import sky, ring, COLS, save
from friend_g_nightsky import text1x
from aplus8 import CYAN, ORG, MAG
def dark(c): return tuple(round(v * 0.6) // 4 * 4 for v in c)
EXTRA = [CYAN, ORG, MAG, CYAN, ORG, MAG]
def frame(f, seed=19):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, seed)
    ring(d, cx, cy, 17, 4, ph)
    gemini_star(d, cx, cy, 7 + round(2 * math.sin(2 * ph)), -2 * ph)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], YEL)
    for k in range(6):
        a = -ph + k * math.pi / 3
        x, y = round(cx + 24 * math.cos(a)), round(cy + 5 * math.sin(a))
        if 1 <= y <= 40:
            d.rectangle([x - 2, y - 1, x + 1, y], EXTRA[k])
    px = img.load()
    for y in range(31, 41):
        for x in range(S):
            if px[x, y] in (BLUE, RED, YEL, GRN): px[x, y] = dark(px[x, y])
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img
if __name__ == "__main__":
    save([frame(i) for i in range(N)], "S_AplusG")
    frame(10).resize((256, 256), Image.NEAREST).save("/tmp/s_aplusg.png")
