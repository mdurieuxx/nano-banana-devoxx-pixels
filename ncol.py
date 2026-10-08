import sys, numpy as np
from PIL import Image
def ncol(p, k=10):
    im = Image.open(p); fr = []
    for i in range(im.n_frames):
        im.seek(i); fr.append(np.asarray(im.convert("RGB")))
    a = np.concatenate(fr, 0)
    big = Image.fromarray(a)
    q = big.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = np.array(q.getpalette()).reshape(-1, 3); pal = pal[:int(np.asarray(q).max()) + 1]; k = len(pal); cnt = np.bincount(np.asarray(q).ravel(), minlength=k) / a.shape[0] / 64
    nb = [(tuple(pal[i]), round(100 * cnt[i], 1)) for i in range(k) if pal[i].sum() > 60 and cnt[i] > 0.003]
    return len(nb)
if __name__ == "__main__":
    for p in sys.argv[1:]: print(ncol(p), p.split("/")[-1])
