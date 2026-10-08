# Recipe re-built from the #1 leaderboard GIF (1000024138.gif, 88.9/100):
# 64x64, 60 frames, black background (~76% pure black), exact Google palette,
# "GOOGLE" / "DEVOXX" in 2x 3x5 font framed by two blue rules, and a middle band telling a short story:
#   f0-15  a Google "G" is chased by four ghosts (bugs) along a pellet line
#   f16-23 the G eats a power-up, grows, the ghosts turn scared-blue and flee
#   f24-35 the G catches them ("FIX" tag above), eaten ghosts flash white
#   f36-47 the G leaves the screen to the right
#   f42-58 "ALL BUGS FIXED" scrolls in, cycling palette colors, then scrolls out
#   f54-59 pellets and the next ghosts slide in from the right -> seamless loop
import math, os
from PIL import Image, ImageDraw
from common import S, FONT

N = 60
BLK = (0, 0, 0)
BLUE, RED, YEL, GRN = (66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83)
WHITE, SCARED, PUPIL, PELLET, SPARK = (255, 255, 255), (30, 60, 255), (20, 20, 200), (255, 235, 170), (149, 115, 205)
LETTER = {"G": FONT["G"], "O": FONT["O"], "L": FONT["L"], "E": FONT["E"], "D": FONT["D"], "V": FONT["V"], "X": FONT["X"],
          "A": FONT["A"], "B": FONT["B"], "U": FONT["U"], "S": FONT["S"], "F": ["111", "100", "110", "100", "100"],
          "I": FONT["I"], " ": FONT[" "]}

def text2x(d, s, x, y, cols, w=1):
    for i, ch in enumerate(s):
        col = cols[i % len(cols)] if isinstance(cols, list) else cols
        for r, row in enumerate(LETTER[ch]):
            for c, v in enumerate(row):
                if v == "1":
                    d.rectangle([x + c * 2 * w, y + r * 2 * w, x + c * 2 * w + 2 * w - 1, y + r * 2 * w + 2 * w - 1], col)
        x += 8 * w

def text1x(d, s, x, y, col):
    for ch in s:
        for r, row in enumerate(LETTER[ch]):
            for c, v in enumerate(row):
                if v == "1":
                    d.point((x + c, y + r), col)
        x += 4

# ghost sprite (9 wide, 10 tall) extracted from the reference GIF
GHOST = ["...bbb...", ".bbbbbbb.", ".bbbbbbb.", "bbwwbwwbb", "bbpwbpwbb",
         "bbbbbbbbb", "bbbbbbbbb", "bbbbbbbbb", "bbbbbbbbb", "bbb..bbbb"]
SCARED_SPRITE = [".bbbbbbb.", "bbbbbbbbb", "bbwbbbwbb", "bbbbbbbbb", "bbbbbbbbb",
                 "bwbwbwbwb", "bbbbbbbbb", "bbbbbbbbb", "bbbbbbbbb", "bb.bbb.bb"]

def ghost(d, x, y, body, scared=False):
    spr = SCARED_SPRITE if scared else GHOST
    pal = {"b": body, "w": WHITE, "p": PUPIL}
    for r, row in enumerate(spr):
        for c, ch in enumerate(row):
            if ch != ".":
                d.point((x + c, y + r), pal[ch] if not scared or ch != "w" else WHITE)

def g_logo(d, cx, cy, rad, mouth):
    """Google 'G': 4-color ring + blue bar; mouth = open angle in degrees (chomp)."""
    for yy in range(-rad - 1, rad + 2):
        for xx in range(-rad - 1, rad + 2):
            dist = math.hypot(xx, yy)
            if rad - max(2, rad // 3) <= dist <= rad:
                ang = math.degrees(math.atan2(-yy, xx)) % 360          # 0 = right, ccw
                if ang < mouth / 2 or ang > 360 - mouth / 2:
                    continue
                col = BLUE if ang < 45 or ang > 315 else RED if ang < 135 else YEL if ang < 225 else GRN
                if 20 < ang < 45:                                        # lower-right of the opening stays blue
                    col = BLUE
                d.point((cx + xx, cy + yy), col)
    d.rectangle([cx, cy - 1, cx + rad - 1, cy], BLUE)                    # the G's bar

PELLET_Y = 33
def pellets(d, f):
    """Pellet line scrolls left 3 px/frame; 60 * 3 = 180 = 2 * 90 -> periodic over the loop."""
    for k in range(15):
        x = (k * 6 - f * 3) % 90 - 6
        d.rectangle([x, PELLET_Y, x + 1, PELLET_Y + 1], PELLET)
        if ((x + 6) // 6) % 3 == 1:
            d.line([(x - 2, PELLET_Y), (x + 3, PELLET_Y)], SPARK); d.line([(x, PELLET_Y - 2), (x, PELLET_Y + 3)], SPARK)

def chase(d, f, off=0):
    for i, c in enumerate([BLUE, RED, YEL, GRN]):
        ghost(d, 14 + i * 10 + off + (f % 2), 28, c)
    g_logo(d, 62 + off, 33, 6, 60 if (f // 2) % 2 else 20)

def frame(f):
    img = Image.new("RGB", (S, S), BLK)
    d = ImageDraw.Draw(img)
    text2x(d, "GOOGLE", 9, 2, [BLUE, RED, YEL, BLUE, GRN, RED])
    d.line([(0, 13), (S, 13)], BLUE); d.line([(0, 51), (S, 51)], BLUE)
    d.point((f * S // N, 13), WHITE); d.point((S - 1 - f * S // N, 51), WHITE)   # glints keep every frame distinct
    text2x(d, "DEVOXX", 9, 53, [BLUE, RED, YEL, BLUE, GRN, RED])
    ghost_cols = [BLUE, RED, YEL, GRN]
    if f < 16:                                         # chase
        pellets(d, f)
        chase(d, f)
    elif f < 24:                                       # growing G, scared ghosts flee
        t = f - 16
        g_logo(d, 11, 33, 6 + min(t, 4), 50 if t % 2 else 20)
        for i in range(4):
            ghost(d, 24 + i * 10 + t, 28, SCARED, True)
    elif f < 36:                                       # G eats ghosts
        t = f - 24
        g_logo(d, 11 + t * 2, 33, 10, 70 if t % 2 else 20)
        text1x(d, "FIX", 14 + t * 2, 15, WHITE)
        for i in range(4):
            gx = 24 + i * 10 + t * 2
            if gx > 11 + t * 2 + 11:
                ghost(d, gx, 28, WHITE if i == (t // 3) else SCARED, True)
    elif f < 42:                                       # G leaves right
        t = f - 36
        text1x(d, "FIX", 35 + t * 4, 15, WHITE)
        g_logo(d, 35 + t * 6, 33, 10, 40)
    if 42 <= f < 59:                                   # banner scroll
        off = 0 if f < 54 else -(f - 53) * 12
        cols = [YEL, GRN, BLUE, RED, WHITE, BLUE]
        col = cols[((f - 42) // 3) % len(cols)]
        text1x(d, "ALL BUGS", 18 + off, 22, col)
        text2x(d, "FIXED", 12 + off, 29, col)
        d.line([(30 + off, 42), (34 + off, 42)], SPARK); d.line([(32 + off, 40), (32 + off, 44)], SPARK)
    if f >= 54:
        pellets(d, f)
    if f >= 57:                                        # next chase slides in from the right (offset 0 at f60 == f0)
        chase(d, f, (N - f) * 10)
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    out = [frame(i) for i in range(N)]
    out[0].save("output/RECIPE_top1_google_chomps_devoxx.gif", save_all=True, append_images=out[1:],
                duration=100, loop=0, disposal=1)
