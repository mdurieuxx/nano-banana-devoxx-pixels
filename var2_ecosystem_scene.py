# VAR2 - "Tech Ecosystem": a Cloud hub linked to four nodes over a hilly landscape,
# data packets flow both ways, a river ripples, an equalizer pulses on the black floor.
# Every animated element is periodic over N frames -> seamless loop.
import math, os
from PIL import Image, ImageDraw
from common import S, G, text, lerp

N = 60
PINK, ORANGE, INDIGO = (233, 30, 99), (255, 152, 0), (63, 81, 181)
WHITE, CLOUD = (255, 255, 255), (240, 244, 255)
BLACK = (0, 0, 0)
GC = [G["blue"], G["red"], G["yellow"], G["green"]]
PAL = {"w": WHITE, "b": G["blue"], "r": G["red"], "y": G["yellow"], "g": G["green"], "k": BLACK}

SKY_H = 34
STOPS = [INDIGO, G["blue"], (120, 200, 255), G["yellow"], ORANGE]
FLOOR_Y = 52

SPRITES = [   # laptop, server, phone, chip - 7 px wide, 6 tall
    [".wwwww.", ".wbbbw.", ".wbrbw.", ".wwwww.", "wwwwwww", "wyyyyyw"],
    ["wwwwwww", "wgwkkkw", "wwwwwww", "wrwkkkw", "wwwwwww", "wywkkkw"],
    ["..www..", ".wbbbw.", ".wgggw.", ".wyyyw.", ".wrrrw.", "..www.."],
    ["wwwwwww", "wbwwwgw", "wbwrwgw", "wbwwwgw", "wwwwwww", "w.w.w.w"],
]
NODE_X = [8, 24, 40, 56]
NODE_Y = 39
HUB = (32, 22)

def sky_color(y):
    t = (y // 3) / (SKY_H // 3) * (len(STOPS) - 1)
    i = min(int(t), len(STOPS) - 2)
    return lerp(STOPS[i], STOPS[i + 1], t - i)

def draw_sprite(d, k, cx, top, f):
    for r, row in enumerate(SPRITES[k]):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            col = PAL[ch]
            if ch == "b" and (f // 5 + k) % 2:        # blinking screen / pins
                col = WHITE
            d.point((cx - 3 + c, top + r), col)

def frame(f):
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)
    for y in range(SKY_H):
        d.line([(0, y), (S, y)], sky_color(y))
    # sun with alternating rays
    sx, sy = 55, 9
    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], G["yellow"])
    d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], WHITE)
    rays = [(0, -5), (0, 5), (-5, 0), (5, 0)] if (f // 5) % 2 else [(-4, -4), (4, -4), (-4, 4), (4, 4)]
    for dx, dy in rays:
        d.rectangle([sx + dx, sy + dy, sx + dx + (1 if dx else 0), sy + dy + (1 if dy else 0)], ORANGE)
    # hills (far + near) down to the floor
    for x in range(S):
        far = 33 + round(2 * math.sin(2 * math.pi * 2 * x / S))
        near = 40 + round(2 * math.sin(2 * math.pi * (3 * x / S + f / N)))
        d.line([(x, far), (x, FLOOR_Y - 1)], (80, 200, 110))
        d.line([(x, near), (x, FLOOR_Y - 1)], G["green"])
    # river with moving ripples
    d.rectangle([0, 47, S, 50], G["blue"])
    for k in range(5):
        rx = (k * 13 + round(f * S / N)) % S
        d.line([(rx, 48), (min(rx + 3, S - 1), 48)], WHITE)
        d.line([((rx + 6) % S, 50), (min((rx + 8) % S + 1, S - 1), 50)], (160, 210, 255))
    # links hub <-> nodes
    for cx in NODE_X:
        d.line([(cx, NODE_Y - 1), (HUB[0] + (cx - HUB[0]) // 4, HUB[1] + 4)], WHITE)
    # nodes
    for k, cx in enumerate(NODE_X):
        d.rectangle([cx - 4, NODE_Y + 6, cx + 4, NODE_Y + 7], G["green"])
        draw_sprite(d, k, cx, NODE_Y, f)
    # hub cloud with brand text
    d.rounded_rectangle([20, 15, 44, 27], 5, CLOUD)
    d.ellipse([24, 9, 36, 21], CLOUD)
    d.ellipse([32, 12, 43, 22], CLOUD)
    text(img, "CLOUD", 23, 16, G["blue"], shadow=False)
    for k in range(4):
        d.rectangle([26 + k * 4, 22, 27 + k * 4, 23], GC[(k + f // 4) % 4])
    # packets traveling along the links (2 round trips per loop)
    for k, cx in enumerate(NODE_X):
        p = (f / 30 + k * 0.25) % 1
        p = p if k % 2 == 0 else 1 - p
        x0, y0 = cx, NODE_Y - 2
        x1, y1 = HUB[0] + (cx - HUB[0]) // 4, HUB[1] + 4
        px, py = round(x0 + (x1 - x0) * p), round(y0 + (y1 - y0) * p)
        d.rectangle([px - 1, py, px, py + 1], GC[(k + 1) % 4])
    # black floor with equalizer bars
    d.rectangle([0, FLOOR_Y, S, S], BLACK)
    for k in range(16):
        h = 1 + round(4 * (1 + math.sin(2 * math.pi * (3 * f / N + k * 0.37))))
        d.rectangle([k * 4, S - h, k * 4 + 2, S - 1], GC[k % 4])
    text(img, "DEVOXX", 3, 2, GC[:2] + GC[2:] + GC[:2])
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    out = [frame(i) for i in range(N)]
    out[0].save("output/VAR2_ecosystem_scene.gif", save_all=True, append_images=out[1:],
                duration=90, loop=0, disposal=1)
