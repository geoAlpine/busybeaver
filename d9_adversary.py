#!/usr/bin/env python3
"""
D9 probe, stage 3 — the decisive test of the PREMISE itself.

D9 claims: "with the first-moment budget sum D = N + O(1), a divergent second moment
forces the deep-return TIME SET to be very sparse (near-lacunary)."

Test it directly on the very adversary class D9 invokes: iid D with E[D]=2 (budget-legal
to O(sqrt N)) and E[D^2]=infinity, i.e. P(D=d) ~ c d^{-s} with 2 < s <= 3.
If T_L for THAT law is also non-lacunary, the premise is false by construction,
independently of any orbit data.

Also: what density cap does the first-moment budget actually impose?
  sum_{j<J} D_j = 2J + o(J)  and  D_j >= L on T_L  =>  |T_L| <= 2J/L.
That is a HARMONIC cap (density <= 2/L), astronomically weaker than lacunary
(density 0, count O(log J)) and weaker even than the observed 2^{-(L-1)}.
"""
import numpy as np

rng = np.random.default_rng(7)
DMAX = 10**7

def zeta(s, n=DMAX):
    """Truncated zeta; for s>1 the tail beyond n is negligible at our precision."""
    d = np.arange(1, n + 1, dtype=np.float64)
    return float((d ** (-s)).sum())

def solve_s():
    # mean = zeta(s-1)/zeta(s) = 2, with s in (2,3) => E[D^2]=zeta(s-2)/zeta(s)=inf
    f = lambda s: zeta(s - 1) / zeta(s) - 2.0
    lo, hi = 2.05, 2.999
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if f(lo)*f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

def sample_pareto_like(s, size, dmax=10**6):
    d = np.arange(1, dmax + 1, dtype=np.float64)
    p = d ** (-s); p /= p.sum()
    return rng.choice(dmax, size=size, p=p) + 1

def geom_of(D, L, J):
    t = np.nonzero(D >= L)[0].astype(np.float64)
    if len(t) < 5: return None
    tt = t[t > 0]
    r = tt[1:] / tt[:-1]
    g = np.diff(t)
    return dict(L=L, n=len(t), dens=len(t) / J, rmin=r.min(), rmed=np.median(r),
                maxgap=int(g.max()), cnt_over_log2J=len(t) / np.log2(J),
                budget_cap=2.0 / L)

def main():
    s = solve_s()
    print(f"[OBSERVED] heavy-tail adversary: P(D=d) ∝ d^-s with s = {s:.6f}")
    print(f"   E[D] = {zeta(s-1)/zeta(s):.6f} (budget-matched to Haar mean 2)")
    print(f"   E[D^2] = zeta(s-2)/zeta(s) with s-2 = {s-2:.4f} <= 1  =>  DIVERGENT ✓")
    print(f"   tail: P(D >= L) ~ c L^{{1-s}} = L^{{{1-s:.3f}}}  (polynomial, NOT lacunary)")

    J = 2_000_000
    D = sample_pareto_like(s, J)
    print(f"\n[OBSERVED] sampled J={J}: mean D = {D.mean():.4f}, "
          f"running 2nd moment = {(D.astype(float)**2).mean():.1f} (should drift up = divergent)")
    # show second moment does not stabilise
    for frac in (0.1, 0.25, 0.5, 1.0):
        k = int(J * frac)
        print(f"   first {k:>9}: E[D]={D[:k].mean():.4f}  E[D^2]={(D[:k].astype(float)**2).mean():>12.1f}")

    print(f"\n### T_L geometry under the E[D^2]=inf, budget-legal adversary [OBSERVED]")
    print(f"{'L':>3} {'|T_L|':>9} {'density':>10} {'budget cap 2/L':>15} {'min ratio':>10} "
          f"{'med ratio':>10} {'max gap':>9} {'|T|/log2 J':>11}")
    for L in list(range(3, 13)) + [20, 50, 100]:
        r = geom_of(D, L, J)
        if r is None: continue
        print(f"{r['L']:>3} {r['n']:>9} {r['dens']:>10.3e} {r['budget_cap']:>15.3e} "
              f"{r['rmin']:>10.6f} {r['rmed']:>10.6f} {r['maxgap']:>9} {r['cnt_over_log2J']:>11.1f}")

    print("\n### Same table for the Haar/geometric law P(D=d)=2^-d [OBSERVED]")
    Dg = rng.geometric(0.5, size=J)
    print(f"{'L':>3} {'|T_L|':>9} {'density':>10} {'budget cap 2/L':>15} {'min ratio':>10} "
          f"{'med ratio':>10} {'max gap':>9} {'|T|/log2 J':>11}")
    for L in range(3, 13):
        r = geom_of(Dg, L, J)
        if r is None: continue
        print(f"{r['L']:>3} {r['n']:>9} {r['dens']:>10.3e} {r['budget_cap']:>15.3e} "
              f"{r['rmin']:>10.6f} {r['rmed']:>10.6f} {r['maxgap']:>9} {r['cnt_over_log2J']:>11.1f}")

    print("\n[OBSERVED] For a genuinely lacunary set with ratio q, |T ∩ [1,J]| ≈ log J / log q.")
    print(f"           At J = {J}: q=2 -> {np.log(J)/np.log(2):.0f} elements; "
          f"q=1.01 -> {np.log(J)/np.log(1.01):.0f} elements.")

if __name__ == "__main__":
    main()
