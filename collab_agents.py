# Three "collaboration" recipes: the Gemini star and other AI models/agents work together.
#   D TEAM UP  - four models link up with the Gemini star, packets flow both ways, a heart pulses on delivery
#   E AGENTS   - a baton is handed from agent to agent around a ring (relay), each receiver lights up
#   F ORB      - one shared orb; each orbiting model tints it as it passes (smooth, black-clamped glow)
# Logos are tiny hand-drawn pixel glyphs (simplified interpretations, not official assets).
# Black background, 60 frames @ 100 ms, everything periodic over N -> seamless loop.
import colorsys, math, os
from PIL import Image, ImageDraw
from pac_ai_variants import LOGOS, sprite
from led_kit import *

CX, CY = 32, 32
HEART = [".rr.rr.", "rrrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."]
HEART_COL = (233, 30, 99)

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def logo_at(d, i, cx, cy, flash=False, bob=0):
    cy += bob
    rows, col = LOGOS[i]
    sprite(d, rows, cx - 4, cy - len(rows) // 2, WHITE if flash else col)

def packet(d, a, b, p, col):
    x, y = round(a[0] + (b[0] - a[0]) * p), round(a[1] + (b[1] - a[1]) * p)
    d.rectangle([x - 1, y - 1, x, y], col)

# ---------------------------------------------------------------- D
POS_D = [(11, 23), (53, 23), (11, 42), (53, 42)]
def frame_d(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    frame_shell(d, f, "TEAM UP", "DEVOXX")
    for i, (x, y) in enumerate(POS_D):
        col = LOGOS[i][1]
        edge = (x + (6 if x < CX else -6), y)
        d.line([edge, (CX + (-6 if x < CX else 6), CY + (y - CY) // 3)], col)
    phase = 2 * math.pi * f / N
    gemini_star(d, CX, CY, 6 + round(2 * math.sin(2 * phase)), phase)
    for i, (x, y) in enumerate(POS_D):
        p = ((f % 30) / 30 + i * 0.25) % 1
        p = p if i % 2 == 0 else 1 - p
        a = (x + (6 if x < CX else -6), y)
        b = (CX + (-6 if x < CX else 6), CY + (y - CY) // 3)
        packet(d, a, b, p, LOGOS[i][1])
        bob = round(1.3 * math.sin(2 * math.pi * f / 30 + i * math.pi / 2))
        logo_at(d, i, x, y, flash=(f % 30) // 2 == i * 3 % 15 // 2 and (f % 30) < 8, bob=bob)
    for k, col in enumerate([BLUE, RED, YEL, GRN]):                # comets circling the star (1 turn per 30 frames)
        a = 2 * math.pi * (f % 30) / 30 + k * math.pi / 2
        x, y = CX + round(14 * math.cos(a)), CY + round(9 * math.sin(a))
        d.rectangle([x - 1, y - 1, x + 1, y + 1], col)
    if 22 <= (f % 30) <= 26:                                     # delivery heart (off at the loop seam)
        sprite(d, HEART, CX - 3, 17, HEART_COL)
    return img

# ---------------------------------------------------------------- E
RING = [(CX + round(15 * math.cos(math.radians(-90 + 72 * k))), CY + round(15 * math.sin(math.radians(-90 + 72 * k)))) for k in range(5)]
def frame_e(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    frame_shell(d, f, "AGENTS", "DEVOXX")
    for k in range(5):
        d.line([RING[k], RING[(k + 1) % 5]], BLUE if k % 2 == 0 else GRN)
    for k in range(5):                                             # running lights on every edge (1 edge per 12 frames)
        for j in range(2):
            pp = ((f % 12) / 12 + j / 2) % 1
            a, b = RING[k], RING[(k + 1) % 5]
            x, y = round(a[0] + (b[0] - a[0]) * pp), round(a[1] + (b[1] - a[1]) * pp)
            d.rectangle([x, y, x + 1, y + 1], [YEL, WHITE, GRN, RED, BLUE][k])
    seg, t = divmod(f, 12)
    recv = (seg + 1) % 5 if t > 9 else seg                         # node that just got the baton lights up
    for k in range(5):
        px, py = RING[k]
        hot = (k == seg and t < 3)
        if k == 0:
            gemini_star(d, px, py, 5 + (2 if hot else 0), 2 * math.pi * f / N)
        else:
            logo_at(d, k - 1, px, py, flash=hot, bob=round(1.3 * math.sin(2 * math.pi * f / 12 + k)))
    a, b = RING[seg], RING[(seg + 1) % 5]
    src_col = YEL
    for j, size in enumerate([3, 2, 2]):
        p = max(0, (t - j * 1.2) / 12)
        x, y = round(a[0] + (b[0] - a[0]) * p), round(a[1] + (b[1] - a[1]) * p)
        d.rectangle([x - 1, y - 1, x - 2 + size, y - 2 + size], WHITE if j == 0 else src_col)
    return img

# ---------------------------------------------------------------- F
def frame_f(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    frame_shell(d, f, "MODELS", "DEVOXX")
    phase = 2 * math.pi * f / N
    cols = [lerp(BLK, c, 1.0) for _, c in LOGOS]
    tint = [0.0] * 4
    pos = []
    for i in range(4):
        a = phase + i * math.pi / 2
        pos.append((round(CX + 24 * math.cos(a)), round(CY + 12 * math.sin(a))))
        tint[i] = max(0.0, math.cos(a)) ** 4                     # strongest when passing the right side
    w0 = 0.35                                                    # Gemini blue as the base tint
    tot = w0 + sum(tint)
    mix = [(BLUE[c] * w0 + sum(cols[i][c] * tint[i] for i in range(4))) / tot for c in range(3)]
    h, sat, _ = colorsys.rgb_to_hsv(*[v / 255 for v in mix])
    col = tuple(round(v * 255) for v in colorsys.hsv_to_rgb(h, 1.0, 1.0))   # fully saturated LED color
    px = img.load()
    R = 11
    for y in range(CY - R, CY + R + 1):
        for x in range(CX - R, CX + R + 1):
            dist = math.hypot(x - CX, (y - CY) * 1.0)
            if dist <= R:
                k = (1 - dist / R) ** 1.1
                v = tuple(round(c * (0.18 + 0.82 * k)) for c in col)
                px[x, y] = v if max(v) >= 45 else BLK          # dark-level clamp -> true black
    ring = (f % 20) / 20 * 20
    for y in range(CY - 22, CY + 23):
        for x in range(CX - 28, CX + 29):
            if abs(math.hypot(x - CX, (y - CY) * 1.2) - ring) < 0.6 and ring > R:
                px[x, y] = tuple(round(c * (1 - ring / 24)) for c in col) if ring < 17 else BLK
    for i in range(4):
        logo_at(d, i, *pos[i])
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    for name, fn in [("COLLAB_D_teamup", frame_d), ("COLLAB_E_agents", frame_e), ("COLLAB_F_orb", frame_f)]:
        out = [fn(i) for i in range(N)]
        out[0].save(f"output/{name}.gif", save_all=True, append_images=out[1:], duration=100, loop=0, disposal=1)
