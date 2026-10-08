# Contest-score simulator. Calibrated on the scorer's own public output (/api/public/scores?limit=100).
#
#   python simulator.py score a.gif b.gif ...    pillars, warnings, duplicate check, FESTIVAL_SHUFFLE estimate
#   python simulator.py rank a.gif ...           same, plus the position it would take in the stored leaderboard
#   python simulator.py validate                 leave-one-out error, per pillar and end to end
#   python simulator.py add NAME file.gif LED PAL SPAT MOT HW AES SCORE [penalty]
#
# Two scoring systems alternate (rev 11 FESTIVAL_SHUFFLE, rev 16 PIXOO_CLASSIC). The six pillar bars are IDENTICAL
# in both (0 difference on the 46 entries present in both snapshots); only the bars -> note mapping changes.
# Rev 16 (current): note = old PIXOO_CLASSIC note + theme bonus - duplicate penalty, exact to 0.05 on 43/43 matched
# entries (the two gaps of 15.6 and 18.0 are the published penalties). `score`/`rank` follow the system stored in
# calibration/local/leaderboard_now.json (CL@ columns for classic, FS@ for festival); both pipelines stay in the file.
# Classic, pixels only, leave-one-out on the 47 entries still on the board: rmse 5.4 on the base, Spearman +0.59
# [0.32, 0.78] against the final note; the simulator over-reads the top 12 by about 2.6 points.
#
# Pillar mechanisms (50 entries). Honest leave-one-out error in brackets; each set was kept because nested
# re-selection over a 75-feature pool did not beat it.
#   black%   = pixels that are strictly #000000 (max channel == 0). The scorer quotes its own figure as
#              "True-Black (#000000) usage (0.32%)", and max==0 reproduces it to 0.001 over the 20 native
#              entries that disclose one; the max<=7 definition used until now is off by 2.51 and cost the
#              LED pillar 0.64 -> 0.49 of leave-one-out error.
#   LED      ~ 55 + 0.45 black% + 18 sat - 0.36 leak (only when black% >= 20) - 0.7 max(black%-70, 0)   [0.64]
#   PAL      ~ 98 - 49 max(0.8 - sat, 0) - 0.19 soft-edge% - 0.04 leak (when black% < 20)               [1.79]
#   SPAT     two modes: "Static Edge Crispness" when motion is ~nil (mean frame diff < 1.1), else
#            "Morph Coherence"; one regression per mode                                      [6.80 / 7.75]
#   MOT      rule below                                                                                 [9.07]
#   HW       100 if <= 60 frames, else 82                                                      [exact 50/50]
#   overall  = ridge on the 6 bars + theme bonus - duplicate penalty, fitted on FESTIVAL_SHUFFLE    [5.83]
#
# Known limits, measured not assumed:
#   - "AI Craft & Originality" is Gemini Vision: unpredictable from pixels (LOO 6.10 vs 6.17 for the mean).
#     It carries the largest mapping weight (0.26), so score() substitutes the field median and says so.
#   - themeBonusPts is semantic (0 to 6.4, half the field at 0) and likewise unpredictable; score() brackets it.
#   - ping-pong stays undetectable: palin/hard overlap fully with seamless-cycle.
#   - end to end, with both unknowns substituted, the overall note carries about +/- 7 points.

import csv, glob, json, os, sys
import numpy as np
from PIL import Image

ORDER = ["led", "pal", "spat", "mot"]
SIG = "calibration/local/signatures.json"
FS_CSV = "calibration/local/festival_scores.csv"
FLAG_NAMES = "calibration/local/flag_names.json"
# Pixel features the flag classifiers see. The scorer's own detectors are not single-threshold on these
# (only the near-black leak separates cleanly), so each flag is fitted rather than hard-coded.
FLAG_FEATS = ["black7", "leak", "sat", "mid", "soft48", "ncol_f", "grad", "jitter", "seam_ratio", "iso", "n", "dur"]
LB_NOW = "calibration/local/leaderboard_now.json"
BARS = ["led", "pal", "spat", "mot", "hw", "aes"]
FS_COLS = BARS + ["theme", "dupflag"]
# The scorer narrates itself. strengths/warnings carry 16 reusable binary detector flags, and several
# messages quote the scorer's own measurements, which pins mechanisms down exactly:
#   "Near-black leak detected (10.45% pixels between RGB 1..18)" matches this file's leak feature to 0.01
#     on native entries; non-native ones read ~2.1x higher because the scorer measures before downscaling.
#   "Perceptual near-duplicate (-15.6 pts originality penalty)" gives the duplicate penalty outright
#     (-9.6, -15.6, -18.0 observed), so it no longer has to be inferred from 80*similarity-62.
#   "Conference & Ecosystem Theme Bonus (+4.4 pts: Devoxx, Google Cloud)" gives the theme rule (see THEME_PTS).
#   "Seamless animation loop (ping-pong)" discloses the loop style, so ping-pong is observable from the API
#     even though it stays undetectable from pixels.
# Thresholds bracketed from the flagged/unflagged boundary, native entries only:
#   near-black leak warning   leak > 7.17..8.16        frame buffer warning   frames > 60..96
#   high framerate warning    duration < 40..50        full-frame churn       jitter > 20.9..22.7
# The frame-buffer cap is 60, now corroborated outside the data: the contest's own recommended library
# (glaforge/jixoo, SPECIFICATION.md) states "The internal memory buffer for HTTP GIF animations on the
# Pixoo 64 is capped at ~60 frames". Device is a Divoom Pixoo 64, 64x64, 24-bit colour, so no palette cap.
# Contest rules: up to 3 visuals per entry, 5MB each, square ratio mandatory, PNG/JPG/GIF/WebP/SVG/MP4/WebM.
# submissionCount carries nothing usable (48 entries at 1, 2 at 0).
# Non-64x64 sources: the scorer downscales them BILINEAR, not nearest-neighbour. That reproduces its own
# quoted leak figure to 0.003 on the six non-native entries that disclose one. It is NOT used as the feature
# basis here: swapping it in degrades every pillar (SPAT crisp 10.4 -> 20.9), because five locally stored
# "native" files are re-encoded copies that are not 64x64, so the emulation no longer matches its input.
# Practical consequence: submit native 64x64. For a non-native source, downscale it BILINEAR yourself first
# and feed that, otherwise the pillar numbers below are measured on something the scorer never saw.
# The other detectors overlap on every single feature tried, so they are multi-criteria.
# colorLed.dominant_palette is the scorer's own colour analysis, top 10 colours. Four exact mechanisms, over
# all 497 published colours: channels are quantised to multiples of 4 (6 bits each); luminance is Rec.601
# (0.299R + 0.587G + 0.114B, max error 0.048); saturation is HSV S, (max-min)/max, max error 0.0005;
# is_black_or_near_black trips at max channel <= 16 (bracketed ]12, 20]) -- a different, looser notion than
# the True-Black figure above, which is why the two disagree by about 3 points.
# Reproducing the palette itself still misses: rounding to the nearest multiple of 4 gets the percentages to
# ~1.4 but individual channels land +/-4 off, so pixel decoding differs somewhere. Nine features derived from
# the published palette were tried on the pillars and all hurt (LED 0.72 -> 1.60, PAL 1.89 -> 5.15): closed.
# Fitting the note EXCLUDING the exact duplicate penalty and adding the pixel-predicted flags takes the
# end-to-end LOO from 7.01 to 6.45 (max 15.7 -> 13.8), and the mapping-with-true-bars from 5.43 to 4.80.
# Pixel-only ranking goes 0.45 -> 0.52 Spearman, but the bootstrap CI of that gap is [-0.03, +0.20]:
# not significant, so the ordering claim stays at "detects the top, cannot order the rest".
FS_SIGMA = 7.0          # end-to-end LOO spread, theme and AES substituted
# Empirical LOO coverage of the calibrated note, measured on the 44 live entries, not assumed Gaussian:
#   +/-5 pts 55% | +/-7 pts 73% | +/-9 pts 84% | +/-12 pts 91%
FS_BAND = (9.0, 84)
CL_BAND = 8.0
# Ranking ability, measured the only honest way: inputs are the pixels and nothing else. No real bar, no real
# theme bonus, no real duplicate flag, no leaderboard position anywhere in the model. Each entry is scored by
# models refitted without it, then all are ordered and compared with the live table. All 50 stored media files
# are usable (31 gif + 10 png + 9 jpeg; an earlier run globbed only *.gif and so measured on 26):
#   theme unknown   Spearman +0.53, bootstrap 95% CI [+0.25, +0.74], mean rank error 9.3 of 44, note RMSE 6.57
#   theme known     Spearman +0.61, mean rank error 8.7 of 44, note RMSE 6.34
# The CI no longer straddles zero, so the ordering signal is established, but a 9-place mean error over 44
# entries still means this detects the top of the table rather than a position.
# Two findings that cost v5 its claimed edge:
#   - fitting the mapping to the FESTIVAL_SHUFFLE note orders WORSE than fitting it to the retired note
#     (+0.21 vs +0.43): the new note is the noisier target, so the weights absorb noise.
#   - feeding it a constant for a heavily weighted unpredictable input (AES, weight 0.32) dilutes the signal
#     from the bars that ARE predictable. Plain sum of the 5 predicted bars scores +0.45, statistically
#     indistinguishable from the fitted blend (bootstrap CI of the gap [-0.13, +0.17]).
# So: order with the retired-note blend, read the FESTIVAL_SHUFFLE note as the magnitude. Earlier runs of this
# file quoted Spearman 0.57; that number used the real theme bonus and the real duplicate flag as inputs.
# The raw ridge compresses the scale: it overshoots the lower half (mean bias +1.9) and undershoots the
# leaders by 8 to 11 pts. calibrate() quantile-maps it back onto the real score distribution, which removes
# the bias (+0.12) and lifts mid-range coverage. It is monotone, so the ranking is untouched by design.
THEME_HI = 4.4          # theme bonus of the current leader; score() shows 0 and this
# Conference & Ecosystem Theme Bonus, recovered exactly from the scorer's own strengths text
# ("Theme Bonus (+4.4 pts: Devoxx, Google Cloud)"): purely additive, max error 0.0000 over the 25 entries
# that carry one. It enters the overall note with coefficient 1.0. Pass --theme=Devoxx,Gemini to apply it.
# Highest seen in the table is 3 keywords (6.4). Nobody has stacked 4 or 5, so the cap is untested, not absent.
THEME_PTS = {"devoxx": 2.2, "google cloud": 2.2, "gemini": 2.2, "antigravity": 2.0, "mascots/devtech": 1.8}


def theme_bonus(names):
    """Sum of the recognised keywords. Unknown names are reported, not silently dropped."""
    pts, bad = 0.0, []
    for n in names:
        k = n.strip().lower()
        if k in THEME_PTS: pts += THEME_PTS[k]
        elif k: bad.append(n.strip())
    return pts, bad
LED_COLS = ["black0", "leak_hb", "sat", "bh"]
PAL_COLS = ["satlo", "mid", "leak_nb"]
SPAT_COLS = {"crisp": ["logcol", "sat_logcol", "loggrad"], "morph": ["soft48", "sat", "grad_nb"]}
FEATS = ("n", "dur", "black0", "black7", "leak", "sat", "mid", "soft48", "ncol_f", "grad", "jitter", "seam_ratio", "iso")

def frames(path):
    im = Image.open(path); out = []
    for i in range(getattr(im, "n_frames", 1)):
        im.seek(i); f = im.convert("RGBA"); bg = Image.new("RGBA", f.size, (0, 0, 0, 255)); bg.alpha_composite(f); f = bg.convert("RGB")
        out.append(np.asarray(f.resize((64, 64), Image.NEAREST) if f.size != (64, 64) else f).astype(int))
    return np.array(out), im.info.get("duration", 100)

def features(path):
    fr, dur = frames(path); mx, mn = fr.max(axis=3), fr.min(axis=3); lit = mx > 0
    sat = np.where(lit, (mx - mn) / np.maximum(mx, 1), 0)
    gx = np.abs(np.diff(fr, axis=2)).sum(axis=3); gy = np.abs(np.diff(fr, axis=1)).sum(axis=3); pairs = gx.size + gy.size
    step = np.abs(np.diff(fr, axis=0)).mean() if len(fr) > 1 else 0.0
    nb = np.zeros(lit.shape, int)
    nb[:, 1:, :] += lit[:, :-1, :]; nb[:, :-1, :] += lit[:, 1:, :]; nb[:, :, 1:] += lit[:, :, :-1]; nb[:, :, :-1] += lit[:, :, 1:]
    return dict(n=len(fr), dur=dur, black0=(mx == 0).mean() * 100, black7=(mx <= 7).mean() * 100,
                leak=((mx >= 1) & (mx <= 18)).mean() * 100,
                sat=sat[lit].mean() if lit.any() else 0.0,
                mid=(((gx > 24) & (gx < 150)).sum() + ((gy > 24) & (gy < 150)).sum()) / pairs * 100,
                soft48=(((gx > 0) & (gx <= 48)).sum() + ((gy > 0) & (gy <= 48)).sum()) / pairs * 100,
                ncol_f=np.mean([len(np.unique(f.reshape(-1, 3), axis=0)) for f in fr]),
                grad=(gx.mean() + gy.mean()) / 2, jitter=step, iso=(lit & (nb == 0)).sum() / max(lit.sum(), 1) * 100,
                seam_ratio=(np.abs(fr[-1] - fr[0]).mean() / max(step, 1e-6)) if len(fr) > 1 else 0.0)

def engineer(d):
    # Two black measures, each where it was measured to belong: the LED level keys off strict #000000, the
    # leak gate keys off the looser max<=7. Mixing them the other way costs PAL 1.79 -> 1.91.
    hb = 1.0 if d["black7"] >= 20 else 0.0
    d["logcol"] = np.log10(d["ncol_f"]); d["loggrad"] = np.log10(1 + d["grad"]); d["bh"] = max(d["black0"] - 70, 0)
    d["leak_hb"] = d["leak"] * hb; d["leak_nb"] = d["leak"] * (1 - hb); d["grad_nb"] = d["grad"] * (1 - hb)
    d["satlo"] = max(0.8 - d["sat"], 0); d["sat_logcol"] = d["sat"] * d["logcol"]
    d["mode"] = "crisp" if d["n"] == 1 or d["jitter"] < 1.1 else "morph"
    return d

TB_CSV = "calibration/local/true_black.csv"


def rows():
    """The shipped CSV stores black% under the old max-channel<=7 definition; override it where we have the
    corrected strict-#000000 value, which is what the scorer actually reports."""
    tb = {}
    if os.path.exists(TB_CSV):
        tb = {r["entry"]: float(r["black0"]) for r in csv.DictReader(open(TB_CSV))}
    out = []
    for p in sorted(glob.glob("calibration/*.csv")) + sorted(glob.glob("calibration/local/extra_*.csv")):
        for r in csv.DictReader(open(p)):
            d = {k: float(v) for k, v in r.items() if k not in ("entry", "mode", "loop")}; d["entry"] = r["entry"]; d["loop"] = r["loop"]
            d["black0"] = tb.get(r["entry"], d["black7"])    # strict #000000 where recomputed
            engineer(d); d["mode"] = "crisp" if r["mode"].startswith("Static") else "morph"; out.append(d)
    return out

def ridge(A, y, lam=1e-2):
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ y)

def design(data, cols):
    return np.array([[d[c] for c in cols] + [1.0] for d in data])

def fit_all(data):
    nat = [d for d in data if d["native"]]
    m = {"led": ridge(design(nat, LED_COLS), np.array([d["led"] for d in nat])), "pal": ridge(design(nat, PAL_COLS), np.array([d["pal"] for d in nat]))}
    for k, cols in SPAT_COLS.items():
        g = [d for d in nat if d["mode"] == k]; m["spat_" + k] = ridge(design(g, cols), np.array([d["spat"] for d in g]), 1e-1)
    B = np.array([[d[p] / 100 for p in ORDER] for d in data])
    m["blend"] = ridge(B, np.array([d["score"] for d in data]), 1e-6)         # score stored without the duplicate penalty
    sty = {}
    for d in data:
        if d["n"] > 1: sty.setdefault(d["loop"], []).append(d["mot"])
    m["mot_seamless"] = float(np.mean(sty.get("seamless-cycle", [92.0]))); m["mot_hard"] = float(np.mean(sty.get("hard-cut", [67.0])))
    m["mot_negl"] = 82.0
    return m

def motion(f, m):
    if f["n"] == 1: return 68.0
    if f["jitter"] < 1.1: return m["mot_negl"]
    if f["seam_ratio"] > 2.9: return m["mot_hard"]
    if 40 <= f["n"] <= 60 and 90 <= f["dur"] <= 110 and f["jitter"] >= 1.4: return 98.0   # holds for 4 of 5, but the 9 real
    return m["mot_seamless"]            # 98s span n=10..55 and dur=15..140, so this is a partial rule, not the mechanism

def estimate(f, m):
    f = engineer(dict(f)); ap = lambda w, c: float(np.dot(w[:-1], [f[x] for x in c]) + w[-1])
    pil = {"led": float(np.clip(ap(m["led"], LED_COLS), 0, 100)), "pal": float(np.clip(ap(m["pal"], PAL_COLS), 0, 100)),
           "spat": float(np.clip(ap(m["spat_" + f["mode"]], SPAT_COLS[f["mode"]]), 0, 100)), "mot": motion(f, m),
           "hw": 100.0 if f["n"] <= 60 else 82.0}
    return pil, float(np.array([pil[p] / 100 for p in ORDER]) @ m["blend"]), f["mode"]

def warnings(f):
    w = []
    if f["black0"] < 10.5: w.append(f"very low true-black ({f['black0']:.1f}%): full-lit backgrounds cap LED near 68")
    if f["leak"] > 7.5: w.append(f"near-black leak ({f['leak']:.1f}% of pixels at RGB 1..18): snap them to #000000")
    if f["n"] > 60: w.append("more than 60 frames (Pixoo frame buffer): Hardware 82")
    if f["n"] > 1 and f["jitter"] < 0.75: w.append("negligible motion")
    elif f["n"] > 1 and f["jitter"] < 1.1: w.append(f"motion at the limit of the 'negligible' flag ({f['jitter']:.2f}; <=0.74 flagged, >=1.09 safe)")
    if f["n"] > 1 and f["dur"] < 50: w.append("frame duration too short for the LED refresh cadence")
    if f["n"] > 1 and f["seam_ratio"] > 2.9: w.append("loop boundary likely flagged as a jump")
    return w


def source_note(path):
    """The scorer measures a non-64x64 source after a BILINEAR downscale; this file samples NEAREST."""
    from PIL import Image as _I
    w, h = _I.open(path).size
    if (w, h) == (64, 64): return None
    if w != h: return f"source is {w}x{h}: non-square entries are rejected outright"
    return (f"source is {w}x{h}, not native 64x64: the scorer BILINEAR-downscales it, this file samples "
            f"nearest-neighbour, so the pillars below are less reliable here")

def thumb(path, size=32, maxf=12):
    im = Image.open(path); n = getattr(im, "n_frames", 1); out = []
    for i in sorted(set(np.linspace(0, n - 1, min(n, maxf)).astype(int))):
        im.seek(i); f = im.convert("RGBA"); bg = Image.new("RGBA", f.size, (0, 0, 0, 255)); bg.alpha_composite(f)
        out.append(np.asarray(bg.convert("L").resize((size, size), Image.BILINEAR), float))
    return np.array(out)

def _norm(a):
    a = a - a.mean(); s = np.sqrt((a ** 2).sum()); return a / s if s > 0 else a

SELF = 0.9995     # above this the signature IS this file, already scored in the table: not a duplicate


def duplicates(path, drop_self=True):
    """Closest stored signature. Self-matches are dropped so re-scoring a table entry is not penalised."""
    if not os.path.exists(SIG): return None
    sigs = json.load(open(SIG)); t = thumb(path); best = ("", 0.0); mine = ""
    for name, v in sigs.items():
        v = np.array(v); s = max(float((_norm(a.ravel()) * _norm(b.ravel())).sum()) for a in t for b in v)
        if drop_self and s >= SELF: mine = name; continue
        if s > best[1]: best = (name, s)
    return best + (mine,)

def dup_penalty(sim):
    return max(0.0, 80 * sim - 62) if sim >= 0.965 else 0.0


def flag_cols():
    if not os.path.exists(FLAG_NAMES): return []
    return ["f%02d" % k for k in range(len(json.load(open(FLAG_NAMES))))]


def fs_rows(data):
    """Calibration rows still in the live table, with their note, theme, exact duplicate penalty and flags."""
    if not os.path.exists(FS_CSV): return []
    fs = {r["entry"]: r for r in csv.DictReader(open(FS_CSV))}
    fc = flag_cols(); out = []
    for d in data:
        r = fs.get(d["entry"])
        if not r: continue
        d = dict(d)
        d["score_fs"] = float(r["score_fs"]); d["theme"] = float(r["theme"])
        d["pen"] = float(r.get("pen", 0.0)); d["dupflag"] = 1.0 if d["pen"] else 0.0
        d["clean"] = d["score_fs"] + d["pen"]            # note before the originality penalty
        for c in fc: d[c] = float(r[c])
        out.append(d)
    return out


def fit_flags(fsd):
    """One logistic classifier per detector flag, predicting it from the pixel features."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    X = np.array([[d[c] for c in FLAG_FEATS] for d in fsd]); out = {}
    for c in flag_cols():
        y = np.array([d[c] for d in fsd])
        if y.std() == 0: out[c] = float(y.mean()); continue
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=4000)); m.fit(X, y); out[c] = m
    return out


def flag_probs(fm, f):
    x = np.array([[f[c] for c in FLAG_FEATS]])
    return {c: (m if isinstance(m, float) else float(m.predict_proba(x)[0, 1])) for c, m in fm.items()}


NOTE_COLS = ["led", "pal", "spat", "mot", "hw", "theme"]


def fit_fs(fsd):
    """Fit the note EXCLUDING the originality penalty: that penalty is quoted exactly, so it is not modelled."""
    cols = NOTE_COLS + flag_cols()
    return ridge(design(fsd, cols), np.array([d["clean"] for d in fsd]), 1e-3)


def estimate_fs(w, pil, theme, probs, penalty=0.0):
    cols = NOTE_COLS + sorted(probs)
    vals = {**pil, "theme": theme, **probs}
    return float(np.dot(w[:-1], [vals[c] for c in cols]) + w[-1]) - penalty


def fit_cal(fsd, m, w, fm):
    """Quantile map from this model's own in-fold predictions onto the real score distribution."""
    p = [estimate_fs(w, estimate({k: d[k] for k in FEATS}, m)[0], d["theme"],
                     flag_probs(fm, engineer(dict(d)))) for d in fsd]
    return np.sort(np.array(p)), np.sort(np.array([d["clean"] for d in fsd]))


def calibrate(cal, s):
    """Quantile map, with linear extrapolation past the ends: plain interp clips, which silently flattened
    everything above the best entry in the table to its exact score."""
    if not cal: return s
    x, y = cal
    if s > x[-1]: k = (y[-1] - y[-2]) / max(x[-1] - x[-2], 1e-9); return float(y[-1] + (s - x[-1]) * k)
    if s < x[0]:  k = (y[1] - y[0]) / max(x[1] - x[0], 1e-9);      return float(y[0] + (s - x[0]) * k)
    return float(np.interp(s, x, y))


def leaderboard():
    return json.load(open(LB_NOW)) if os.path.exists(LB_NOW) else None


def validate():
    data = rows(); err = []
    for i, d in enumerate(data):
        m = fit_all([x for j, x in enumerate(data) if j != i]); _, s, _ = estimate({k: d[k] for k in FEATS}, m)
        err.append(s - d["score"])
    print(f"PIXOO_CLASSIC (in force since rev 16)   leave-one-out on {len(data)} entries: rmse {np.sqrt(np.mean(np.square(err))):.2f} "
          f"(mean-only baseline {np.std([d['score'] for d in data]):.2f})")
    for bar, cols, lam, grp in (("LED", LED_COLS, 1e-2, None), ("PAL", PAL_COLS, 1e-2, None),
                                ("SPAT crisp", SPAT_COLS["crisp"], 1e-1, "crisp"), ("SPAT morph", SPAT_COLS["morph"], 1e-1, "morph")):
        g = [d for d in data if d["native"] and (grp is None or d["mode"] == grp)]
        key = "spat" if bar.startswith("SPAT") else bar.lower(); e = []
        for i, d in enumerate(g):
            tr = [x for j, x in enumerate(g) if j != i]
            w = ridge(design(tr, cols), np.array([x[key] for x in tr]), lam)
            e.append(float(np.clip(np.dot(w[:-1], [d[c] for c in cols]) + w[-1], 0, 100)) - d[key])
        print(f"  pillar {bar:<11} n={len(g):<3} loo rmse {np.sqrt(np.mean(np.square(e))):5.2f}")
    e = [motion(d, fit_all(data)) - d["mot"] for d in data]
    print(f"  pillar {'MOT':<11} n={len(data):<3} loo rmse {np.sqrt(np.mean(np.square(e))):5.2f}  (rule, not fitted)")
    fsd = fs_rows(data)
    if not fsd:
        print("FESTIVAL_SHUFFLE         no calibration file, skipped"); return
    y = np.array([d["clean"] for d in fsd]); true_bars = np.empty(len(y)); end2end = np.empty(len(y))
    for i, d in enumerate(fsd):
        tr = [x for j, x in enumerate(fsd) if j != i]
        w = fit_fs(tr); fm = fit_flags(tr); fl = {c: d[c] for c in flag_cols()}
        true_bars[i] = estimate_fs(w, {k: d[k] for k in BARS[:5]}, d["theme"], fl)
        pil, _, _ = estimate({k: d[k] for k in FEATS}, fit_all(tr))
        end2end[i] = estimate_fs(w, pil, float(np.mean([x["theme"] for x in tr])),
                                 flag_probs(fm, engineer(dict(d))))
    withaes = np.empty(len(y))
    for i, d in enumerate(fsd):
        tr = [x for j, x in enumerate(fsd) if j != i]; cols = NOTE_COLS + ["aes"] + flag_cols()
        w = ridge(design(tr, cols), np.array([x["clean"] for x in tr]), 1e-3)
        withaes[i] = float(np.dot(w[:-1], [d[c] for c in cols]) + w[-1])
    for lbl, p in (("ceiling: true bars, flags and AES", withaes), ("mapping, true bars and true flags", true_bars),
                   ("end to end, theme/flags predicted", end2end)):
        r = p - y
        print(f"FESTIVAL_SHUFFLE  {lbl:<34} n={len(y)}  loo rmse {np.sqrt((r ** 2).mean()):5.2f}  max {np.abs(r).max():5.2f}")
    print(f"  mean-only baseline {y.std():.2f}; feature sets were fixed before this run, the bar->note ridge is refitted per fold")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "score"
    if cmd == "validate":
        validate()
    elif cmd == "add":
        name, path, led, pal, spat, mot, hw, aes, score, *opt = sys.argv[2:]
        pen = float((opt + ["0"])[0]); f = features(path); path_csv = "calibration/own_results.csv"; new = not os.path.exists(path_csv)
        header = open(sorted(glob.glob("calibration/leaderboard*.csv"))[0]).readline().strip().split(",")
        mode = "Static Edge Crispness" if engineer(dict(f))["mode"] == "crisp" else "Morph Coherence"
        vals = {"entry": name, "score": float(score) + pen, "penalty": pen, "led": led, "pal": pal, "spat": spat, "mot": mot, "hw": hw, "aes": aes, "mode": mode,
                "loop": "seamless-cycle", "native": 1}; vals.update({k: round(v, 4) for k, v in f.items()})
        with open(path_csv, "a", newline="") as fh:
            w = csv.writer(fh)
            if new: w.writerow(header)
            w.writerow([vals.get(h, 0) for h in header])
        print("added", name); validate()
    else:
        data = rows(); m = fit_all(data); fsd = fs_rows(data)
        w_fs = fit_fs(fsd) if fsd else None; fm = fit_flags(fsd) if fsd else None
        cal = fit_cal(fsd, m, w_fs, fm) if fsd else None
        lb = leaderboard()
        args = [a for a in (sys.argv[2:] if cmd in ("score", "rank") else sys.argv[1:])]
        want = [a.split("=", 1)[1] for a in args if a.startswith("--theme=")]
        args = [a for a in args if not a.startswith("--theme=")]
        th_pts, th_bad = theme_bonus(want[0].split(",")) if want else (None, [])
        if th_bad: print(f"! unknown theme keyword(s): {', '.join(th_bad)}; known: {', '.join(sorted(THEME_PTS))}")
        classic = bool(lb) and lb["scoringSystem"] == "PIXOO_CLASSIC"
        tag = "CL" if classic else "FS"
        hi_lbl = f"{tag}@{th_pts:g}" if th_pts is not None else f"{tag}@{THEME_HI:g}"
        print(f"{'file':30} {'fr':>3} {'blk0%':>6} {'LED':>5} {'PAL':>5} {'SPAT':>5} {'MOT':>5} {'HW':>4}"
              f" {tag + '@0':>6} {hi_lbl:>7}  Spatial mode")
        for p in args:
            f = features(p); pil, old_sc, mode = estimate(f, m)
            dup = duplicates(p); sim_ = dup[1] if dup else 0.0; pen = dup_penalty(sim_)
            mine = dup[2] if dup else ""
            lo = hi = None
            if classic:
                lo = old_sc - pen; hi = old_sc + (THEME_HI if th_pts is None else th_pts) - pen
            elif w_fs is not None:
                probs = flag_probs(fm, f)
                lo = calibrate(cal, estimate_fs(w_fs, pil, 0.0, probs)) - pen
                hi = calibrate(cal, estimate_fs(w_fs, pil, THEME_HI if th_pts is None else th_pts, probs)) - pen
            print(f"{p[-30:]:30} {f['n']:>3} {f['black0']:6.1f} {pil['led']:5.1f} {pil['pal']:5.1f} {pil['spat']:5.1f}"
                  f" {pil['mot']:5.1f} {pil['hw']:4.0f} {lo if lo is None else f'{lo:6.1f}'} {hi if hi is None else f'{hi:7.1f}'}  {mode}")
            for wmsg in warnings(f): print(f"{'':30} ! {wmsg}")
            sn = source_note(p)
            if sn: print(f"{'':30} ! {sn}")
            if mine: print(f"{'':30} . already in the table as {mine}: self-match ignored")
            if dup and sim_ >= 0.9:
                print(f"{'':30} ! similarity {sim_:.3f} with {dup[0]}: " + (f"DUPLICATE PENALTY about -{pen:.1f}" if pen else "below the duplicate threshold (~0.965), but close"))
            band, cover, spear = ((CL_BAND, 84, 0.59) if classic else (FS_BAND[0], FS_BAND[1], 0.53))
            if cmd == "rank" and lb and lo is not None:
                pos = lambda s: sum(1 for e in lb["entries"] if e["score"] > s) + 1
                print(f"{'':30} = rank {pos(hi)} with a {THEME_HI if th_pts is None else th_pts:g} theme bonus, {pos(lo)} without "
                      f"(leaderboard rev {lb['revision']}, {lb['scoringSystem']}, {len(lb['entries'])} entries)")
                print(f"{'':30} = plus/minus {band:.0f} pts covers {cover}% of entries, so rank "
                      f"{pos(hi + band)}..{pos(lo - band)}; pixel-only order agreement is Spearman {spear:.2f},"
                      f" so treat this as top-of-table detection, not a position")
            if not classic:
                print(f"{'':30} . AES left out of the mapping on purpose: unpredictable from pixels and heavily "
                      f"weighted, so a constant for it diluted the usable bars. Retired-system note was {old_sc - pen:.1f}")
