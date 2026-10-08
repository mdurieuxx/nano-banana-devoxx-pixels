from led_kit import BLUE, RED, YEL, GRN
from aplus8 import CYAN, ORG, MAG, LIME
BASE = (BLUE, RED, YEL, GRN)
TOP = {YEL: ORG, RED: MAG, GRN: LIME}
def dark(c): return tuple(round(v * 0.6) // 4 * 4 for v in c)
def enrich(img, top=11, low=31, bot=40):
    px = img.load()
    for y in range(2, bot + 1):
        for x in range(img.width):
            c = px[x, y]
            if c in BASE:
                if y <= top and c in TOP: px[x, y] = TOP[c]
                elif y >= low: px[x, y] = dark(c)
    return img
