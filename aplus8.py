import math
from PIL import Image, ImageDraw
from led_kit import *
from marc_lot import sky, save
from friend_g_nightsky import text1x
CYAN, ORG, MAG, LIME = (4, 200, 232), (252, 120, 4), (200, 40, 200), (140, 220, 20)
HUES = [BLUE, CYAN, GRN, LIME, YEL, ORG, RED, MAG]
def ring8(d, cx, cy, r, th, rot):
    for dy in range(-r - 1, r + 2):
        for dx in range(-r - 1, r + 2):
            if r - th < math.hypot(dx, dy) <= r:
                ang = (math.degrees(math.atan2(dy, dx)) - math.degrees(rot)) % 360
                d.point((cx + dx, cy + dy), HUES[int(ang // 45) % 8])
def frame(f, seed=19):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, seed)
    ring8(d, cx, cy, 17, 4, ph)
    gemini_star(d, cx, cy, 7 + round(2 * math.sin(2 * ph)), -2 * ph)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], YEL)
    for k in range(6):
        a = -ph + k * math.pi / 3
        x, y = round(cx + 24 * math.cos(a)), round(cy + 5 * math.sin(a))
        if 1 <= y <= 40:
            d.rectangle([x - 1, y - 1, x, y], HUES[(2 * k + 1) % 8])
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img
if __name__ == "__main__":
    save([frame(i) for i in range(N)], "S_Aplus8")
    frame(10).resize((256, 256), Image.NEAREST).save("/tmp/s_aplus8.png")
