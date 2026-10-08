# Low-risk probes for the friend's account (all expected well below the top of the table).
#   TEST_spiral_60 / TEST_spiral_96: same black-background dot spiral, 60 vs 96 frames (frame-count effect on the SPAT bar), no text
#   TEST_theme: navy background (low LED on purpose), "ANTIGRAVITY AGENTS" readable on every frame, nothing else thematic
import math, os
from PIL import Image, ImageDraw
from led_kit import *
from friend_g_nightsky import text1x

COLS = [BLUE, RED, YEL, GRN]

def spiral(f, n):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / n
    for arm in range(4):
        for k in range(26):
            a = ph + arm * math.pi / 2 + k * 0.28
            r = 3 + k * 1.15
            x, y = round(32 + r * math.cos(a)), round(32 + r * math.sin(a))
            sz = 2 if k > 14 else 1
            d.rectangle([x, y, x + sz - 1, y + sz - 1], COLS[arm] if k % 5 else WHITE)
    return img

def theme(f):
    img = Image.new("RGB", (S, S), (0, 40, 90)); d = ImageDraw.Draw(img)
    text1x(d, "ANTIGRAVITY", 10, 12, WHITE)
    text2x(d, "AGENTS", 8, 24, YEL)
    x = round(6 + 50 * (0.5 - 0.5 * math.cos(2 * math.pi * f / N)))
    d.rectangle([x, 46, x + 3, 49], RED)
    return img

def save(frames, name):
    frames[0].save(f"output/{name}.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, disposal=1)

if __name__ == "__main__":
    save([spiral(i, 60) for i in range(60)], "TEST_spiral_60")
    save([spiral(i, 96) for i in range(96)], "TEST_spiral_96")
    save([theme(i) for i in range(N)], "TEST_theme")
