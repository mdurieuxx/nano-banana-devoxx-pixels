import math
from PIL import Image, ImageDraw
from led_kit import *
from marc_lot import sky, ring, COLS, save
from friend_g_nightsky import text1x
SEED = 19
def frame_aplus(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, SEED)
    ring(d, cx, cy, 17, 4, ph)
    gemini_star(d, cx, cy, 7 + round(2 * math.sin(2 * ph)), -2 * ph)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], YEL)
    for k in range(6):
        a = -ph + k * math.pi / 3
        x, y = round(cx + 24 * math.cos(a)), round(cy + 5 * math.sin(a))
        if 1 <= y <= 40:
            d.rectangle([x - 1, y - 1, x, y], COLS[k % 4])
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img
if __name__ == "__main__":
    save([frame_aplus(i) for i in range(N)], "MARC_Aplus_gemini")
