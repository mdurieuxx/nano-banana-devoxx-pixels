# Compare GIFs on the contest proxy metrics + loop seam, and write a contact sheet.
# Usage: python analysis.py [extra.gif ...]   (default: recipe of the #1 + the two black-background variants)
import sys, numpy as np
from PIL import Image

DEFAULT = ["output/RECIPE_top1_google_chomps_devoxx.gif", "output/VAR1_rocket_launch.gif", "output/VAR2_gemini_bloom.gif"]

def frames(path):
    im = Image.open(path)
    out = []
    for i in range(im.n_frames):
        im.seek(i)
        out.append(np.asarray(im.convert("RGB")).astype(int))
    return im, out

def metrics(a):
    noir = (a == 0).all(axis=2).sum() * 100 / 4096
    allume = (a > 150).any(axis=2).sum() * 100 / 4096
    hsv = np.asarray(Image.fromarray(a.astype("uint8")).convert("HSV")).astype(int)
    lit = (a > 0).any(axis=2)
    satur = (hsv[..., 1][lit] > 200).mean() * 100 if lit.any() else 0
    solo = lit.astype(int)
    iso = ((solo[:-1, :-1] + solo[1:, :-1] + solo[:-1, 1:] + solo[1:, 1:]) == 1).sum() * 100 / 4096
    return noir, allume, satur, iso

def main(paths):
    sheet = Image.new("RGB", (len(paths) * 6 * 66, 2 * 66 + 12 * 0), (30, 30, 30))
    print(f"{'file':34} {'fr':>3} {'ms':>3} {'noir%':>6} {'allume%':>8} {'satur%':>7} {'isoles%':>8} {'seam':>6}")
    for row, p in enumerate(paths):
        im, fr = frames(p)
        m = np.mean([metrics(a) for a in fr], axis=0)
        # seam = mean abs diff last->first, compared with a typical consecutive step
        seam = np.abs(fr[-1] - fr[0]).mean()
        step = np.mean([np.abs(fr[i + 1] - fr[i]).mean() for i in range(len(fr) - 1)])
        print(f"{p[-34:]:34} {im.n_frames:>3} {im.info.get('duration'):>3} {m[0]:6.1f} {m[1]:8.1f} {m[2]:7.1f} {m[3]:8.1f} {seam / max(step, 1e-9):6.2f}x")
        for j, idx in enumerate(range(0, len(fr), len(fr) // 6)[:6]):
            sheet.paste(Image.fromarray(fr[idx].astype("uint8")).resize((64 * 1, 64 * 1), Image.NEAREST),
                        (row * 6 * 66 + j * 66, 0))
    big = sheet.crop((0, 0, sheet.width, 64)).resize((sheet.width * 3, 64 * 3), Image.NEAREST)
    big.save("output/analysis_contact_sheet.png")
    print("seam = écart last->first / écart moyen entre frames consécutives (≈1x = boucle invisible)")

if __name__ == "__main__":
    main(DEFAULT + sys.argv[1:] if len(sys.argv) > 1 else DEFAULT)
