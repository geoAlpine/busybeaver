#!/usr/bin/env python3
"""
D9 probe, stage 4: is the REAL orbit's T_L geometry distinguishable from the
iid-geometric surrogate? Percentile of the real statistic in a surrogate ensemble.
A real value sitting at a non-extreme percentile = INDISTINGUISHABLE = premise false.
"""
import numpy as np, sys
rng = np.random.default_rng(20260722)

def stats(D, L, J):
    t = np.nonzero(D >= L)[0].astype(np.float64)
    if len(t) < 20: return None
    tt = t[t > 0]; r = tt[1:] / tt[:-1]; g = np.diff(t)
    cnt, _ = np.histogram(t, bins=np.linspace(0, J, 1001))
    return dict(count=len(t), rmin=r.min(), rmed=np.median(r),
                maxgap=g.max(), disp=cnt.var()/max(cnt.mean(), 1e-9),
                cnt_log=len(t)/np.log2(J))

KEYS = ['count', 'rmin', 'rmed', 'maxgap', 'disp']

def main(path, nsur=300):
    z = np.load(path); D = z['D'].astype(np.int32); J = len(D)
    print(f"[OBSERVED] J = {J} induced steps; real mean D = {D.mean():.6f}")
    print(f"\nPercentile of REAL statistic within {nsur} iid-geometric surrogate draws")
    print("(50 = dead centre of the null; <2.5 or >97.5 = distinguishable at ~5%)\n")
    hdr = f"{'L':>3} " + " ".join(f"{k:>10}" for k in KEYS) + "   | real values"
    print(hdr)
    for L in range(3, 14):
        real = stats(D, L, J)
        if real is None:
            print(f"{L:>3}   (real set too small: {(D>=L).sum()} elements)"); continue
        sur = []
        for _ in range(nsur):
            s = stats(rng.geometric(0.5, size=J), L, J)
            if s: sur.append(s)
        pct = {}
        for k in KEYS:
            v = np.array([x[k] for x in sur], dtype=float)
            pct[k] = 100.0 * (v < real[k]).mean()
        vals = f"count={real['count']} rmin={real['rmin']:.6f} rmed={real['rmed']:.6f} " \
               f"maxgap={int(real['maxgap'])} disp={real['disp']:.3f}"
        print(f"{L:>3} " + " ".join(f"{pct[k]:>10.1f}" for k in KEYS) + f"   | {vals}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "d9_orbit.npz",
         int(sys.argv[2]) if len(sys.argv) > 2 else 300)
