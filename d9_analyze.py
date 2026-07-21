#!/usr/bin/env python3
"""
D9 probe, stage 2: geometry of the deep-return time set T_L = {j : D_j >= L},
vs the iid-geometric surrogate P(D=d)=2^-d; plus restricted character sums.
All output is [OBSERVED].
"""
import numpy as np, sys

rng = np.random.default_rng(20260722)

def ratio_stats(t):
    """t sorted positive ints. Lacunarity ratios t_{i+1}/t_i."""
    t = t[t > 0]
    if len(t) < 3:
        return None
    r = t[1:] / t[:-1]
    return dict(n=len(t), rmin=r.min(), q01=np.quantile(r, .01), med=np.median(r),
                q99=np.quantile(r, .99), rmax=r.max(),
                frac_gt_1p01=(r > 1.01).mean(), frac_gt_1p1=(r > 1.1).mean())

def gap_stats(t):
    g = np.diff(t)
    return dict(count=len(t), mean_gap=g.mean(), med_gap=np.median(g), max_gap=g.max(),
                # index of dispersion of counts in blocks: 1.0 = Poisson/iid
                idx_disp=None)

def dispersion(t, J, nblocks=2000):
    """Variance-to-mean ratio of counts of T_L in equal blocks. iid -> ~1."""
    edges = np.linspace(0, J, nblocks + 1)
    cnt, _ = np.histogram(t, bins=edges)
    m = cnt.mean()
    return cnt.var() / m if m > 0 else np.nan

def loggrowth(t, J):
    """If T_L were lacunary, |T_L cap [1,N]| = O(log N). Report count/log2(N) at N=J,
    and count/N (density)."""
    N = J
    c = len(t)
    return c / np.log2(max(N, 2)), c / N

def analyze_set(name, D, Lmax=13, J=None):
    J = len(D) if J is None else J
    rows = []
    for L in range(3, Lmax + 1):
        t = np.nonzero(D >= L)[0].astype(np.float64)
        if len(t) < 5:
            rows.append((L, len(t), None)); continue
        rs = ratio_stats(t)
        g = np.diff(t)
        perlog, dens = loggrowth(t, J)
        rows.append(dict(L=L, count=len(t), density=dens, pred=2.0 ** (-(L - 1)),
                         mean_gap=g.mean(), max_gap=int(g.max()),
                         rmin=rs['rmin'], med_ratio=rs['med'],
                         frac_gt_1p01=rs['frac_gt_1p01'],
                         cnt_over_log2N=perlog,
                         disp=dispersion(t, J)))
    return rows

def fmt(rows, title):
    print(f"\n### {title}")
    print(f"{'L':>3} {'|T_L|':>8} {'density':>10} {'2^-(L-1)':>10} {'mean gap':>9} "
          f"{'max gap':>8} {'min ratio':>10} {'med ratio':>10} {'%r>1.01':>8} "
          f"{'|T|/log2N':>10} {'disp':>6}")
    for r in rows:
        if not isinstance(r, dict):
            print(f"{r[0]:>3} {r[1]:>8}   (too few)"); continue
        print(f"{r['L']:>3} {r['count']:>8} {r['density']:>10.3e} {r['pred']:>10.3e} "
              f"{r['mean_gap']:>9.1f} {r['max_gap']:>8} {r['rmin']:>10.6f} "
              f"{r['med_ratio']:>10.6f} {100*r['frac_gt_1p01']:>7.2f}% "
              f"{r['cnt_over_log2N']:>10.1f} {r['disp']:>6.3f}")

def char_sums(res, moduli, D, Lmax=10, shifts=(0, 1)):
    """Additive character sums e(a*o_j/m), full vs restricted to T_L, and vs a
    random subset of matched size (null: depth carries no info about o_j mod m).
    'shift' s means we use o_{j+s} (deep return at j, look at residue s steps later)."""
    J = len(D)
    out = []
    for s in shifts:
        for k, m in enumerate(moduli):
            m = int(m)
            r = res[:, k]
            for a in (1,):
                ph = np.exp(2j * np.pi * a * r / m)
                base = ph[s:J] if s else ph
                full = np.abs(base.sum()) / np.sqrt(len(base))
                for L in range(3, Lmax + 1):
                    idx = np.nonzero(D[:len(base)] >= L)[0]
                    if len(idx) < 200: break
                    S = np.abs(base[idx].sum()) / np.sqrt(len(idx))
                    # matched random subset null
                    nulls = []
                    for _ in range(20):
                        ridx = rng.choice(len(base), size=len(idx), replace=False)
                        nulls.append(np.abs(base[ridx].sum()) / np.sqrt(len(idx)))
                    out.append(dict(shift=s, m=m, a=a, L=L, n=len(idx), full=full,
                                    restr=S, null_mean=np.mean(nulls), null_sd=np.std(nulls)))
    return out

def main(path):
    z = np.load(path)
    D = z['D'].astype(np.int32); res = z['res']; moduli = z['moduli']
    J = len(D)
    print(f"[OBSERVED] induced steps J = {J}, mean D = {D.mean():.6f} (Haar mean 2), max D = {D.max()}")
    print(f"[OBSERVED] empirical P(D=d) vs 2^-d:")
    for d in range(1, 16):
        p = (D == d).mean()
        print(f"   d={d:>2} emp={p:.6f} pred={2.0**-d:.6f} ratio={p/2.0**-d:.4f}")

    fmt(analyze_set('real', D), "REAL ORBIT  T_L geometry [OBSERVED]")

    # surrogates: iid geometric P(D=d)=2^-d, same length
    print("\n### IID-GEOMETRIC SURROGATES (5 draws, same J) [OBSERVED]")
    agg = {}
    for rep in range(5):
        Ds = rng.geometric(0.5, size=J).astype(np.int32)
        rows = analyze_set('sur', Ds)
        for r in rows:
            if isinstance(r, dict):
                agg.setdefault(r['L'], []).append(r)
    print(f"{'L':>3} {'|T_L|':>8} {'density':>10} {'mean gap':>9} {'max gap':>8} "
          f"{'min ratio':>10} {'med ratio':>10} {'%r>1.01':>8} {'|T|/log2N':>10} {'disp':>6}")
    for L in sorted(agg):
        rs = agg[L]
        g = lambda key: np.mean([x[key] for x in rs])
        print(f"{L:>3} {g('count'):>8.0f} {g('density'):>10.3e} {g('mean_gap'):>9.1f} "
              f"{g('max_gap'):>8.0f} {g('rmin'):>10.6f} {g('med_ratio'):>10.6f} "
              f"{100*g('frac_gt_1p01'):>7.2f}% {g('cnt_over_log2N'):>10.1f} {g('disp'):>6.3f}")

    # gap-distribution KS-style comparison: real vs geometric
    print("\n### GAP LAW: real vs Geom(p=2^-(L-1)) [OBSERVED]")
    from math import log
    for L in range(3, 13):
        t = np.nonzero(D >= L)[0]
        if len(t) < 200: continue
        g = np.diff(t)
        p = 2.0 ** (-(L - 1))
        # theoretical mean gap 1/p; KS vs geometric cdf
        xs = np.sort(g)
        emp = np.arange(1, len(xs) + 1) / len(xs)
        th = 1 - (1 - p) ** xs
        ks = np.abs(emp - th).max()
        print(f"  L={L:>2} n={len(g):>7} mean_gap={g.mean():>9.1f} 1/p={1/p:>9.1f} "
              f"KS={ks:.4f}  KS*sqrt(n)={ks*np.sqrt(len(g)):.3f}")

    # record times (the only genuinely lacunary-candidate set)
    print("\n### RECORD-DEPTH TIMES (candidate lacunary set) [OBSERVED]")
    rec = []
    best = 0
    for j, d in enumerate(D):
        if d > best:
            best = d; rec.append((j, d))
    print("  (j, D_j):", rec)
    tt = np.array([r[0] for r in rec], dtype=float)
    rs = ratio_stats(tt)
    print("  ratio stats:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rs.items()})

    print("\n### RESTRICTED CHARACTER SUMS |S|/sqrt(n) [OBSERVED]  (random ~0.886)")
    cs = char_sums(res, moduli, D)
    print(f"{'shift':>5} {'m':>4} {'L':>3} {'n':>8} {'full':>7} {'restr':>7} "
          f"{'null_mean':>9} {'null_sd':>8} {'z':>7}")
    for r in cs:
        z_ = (r['restr'] - r['null_mean']) / (r['null_sd'] + 1e-12)
        print(f"{r['shift']:>5} {r['m']:>4} {r['L']:>3} {r['n']:>8} {r['full']:>7.3f} "
              f"{r['restr']:>7.3f} {r['null_mean']:>9.3f} {r['null_sd']:>8.3f} {z_:>7.2f}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "d9_orbit.npz")
