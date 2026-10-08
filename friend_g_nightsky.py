# Night sky: big spinning Gemini star, twinkling stars, satellites on two elliptical orbits, one 2x title at the bottom.
# Black background, 60 frames @ 100 ms, everything periodic over N -> seamless loop. Layout differs from the rule/title shell.
import math, os, random
from PIL import Image, ImageDraw
from led_kit import *

CX, CY = 32, 23
rng = random.Random(7)
STARS = [(rng.randrange(1, 63), rng.randrange(1, 40), rng.randrange(1, 4), rng.randrange(0, 60), rng.choice([BLUE, RED, YEL, GRN, WHITE])) for _ in range(26)]
STARS = [s for s in STARS if math.hypot(s[0] - CX, (s[1] - CY)) > 17]

def text1x(d, s, x, y, col):
    for ch in s:
        for r, row in enumerate(LETTER[ch]):
            for c, v in enumerate(row):
                if v == "1":
                    d.point((x + c, y + r), col)
        x += 4

def frame(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    phase = 2 * math.pi * f / N
    for x, y, k, off, col in STARS:                       # twinkle: lit 1 frame in 3, per-star period k*10 frames
        if ((f + off) // (6 * k)) % 2 == 0 and (f + off) % 3 != 0:
            d.point((x, y), col)
    for k, (rx, ry, col, tilt) in enumerate([(27, 9, BLUE, 0.35), (20, 17, YEL, -0.35)]):   # two orbits, counter-rotating
        for j in range(4):
            a = (1 if k == 0 else -1) * phase + j * math.pi / 2 + k
            x = CX + rx * math.cos(a) * math.cos(tilt) - ry * math.sin(a) * math.sin(tilt)
            y = CY + rx * math.cos(a) * math.sin(tilt) + ry * math.sin(a) * math.cos(tilt)
            if 1 <= y <= 41:
                d.rectangle([round(x) - 1, round(y) - 1, round(x), round(y)], col if j else RED)
    r = 15 + round(3 * math.sin(2 * phase))
    gemini_star(d, CX, CY, r, -phase)
    d.rectangle([CX - 1, CY - 1, CX + 1, CY + 1], WHITE)
    text1x(d, "GEMINI", 20, 43, WHITE)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    out = [frame(i) for i in range(N)]
    out[0].save("output/FRIEND_G_nightsky.gif", save_all=True, append_images=out[1:], duration=100, loop=0, disposal=1)
