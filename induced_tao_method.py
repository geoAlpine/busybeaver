#!/usr/bin/env python
"""
Tao-method / Syracuse-random-model angle on the Antihydra induced odd map.

Setup (GAP LEMMA, this repo):
  Base map  h <- floor(3h/2),  h0 = 8.  Counter c = 2*evens - odds = 3*evens - n >= 0 forever
  <=> even-density E_n/n >= 1/3 forever.
  Induced odd map: from odd o, D = v2(3o-1); next odd o' = 3^{D-1}(3o-1)/2^D, and the GAP to the
  next odd in the base map is exactly D (1 odd step + (D-1) even steps per renewal).
  => over R renewals covering n = sum D_j base-steps:  even-density = 1 - R/sum D_j = 1 - 1/mean(D).
  => non-halt target  even-density >= 1/3  <=>  mean(D) >= 3/2   (liminf of running mean of D).

Syracuse heuristic: for "random" odd o, D = v2(3o-1) is Geometric(1/2): P(D=k)=2^{-k}, mean 2.
  2 > 3/2 with margin 1/2.  Question: does the REAL single orbit keep liminf mean(D) >= 3/2?

This script:
  (1) computes the real induced D-sequence from the base orbit (exact bigint parity),
  (2) builds the Syracuse iid Geometric(1/2) model, compares the D-distributions,
  (3) tracks the running mean of D and its minimum (liminf proxy) for both,
  (4) stress: how far below 3/2 does the running mean ever dip; how big a deficit run is needed.
"""
import math
from collections import Counter


def v2(x):
    return (x & -x).bit_length() - 1


def real_induced_D(n_steps):
    """Run base map floor(3h/2) from 8 for n_steps; return list of gaps D between successive odds
       (each D = v2(3*odd-1)), plus realized even-density of the base orbit."""
    h = 8
    evens = odds = 0
    Ds = []
    last_odd_step = None
    for step in range(1, n_steps + 1):
        if h & 1:  # odd
            odds += 1
            D = v2(3 * h - 1)
            Ds.append(D)
        else:
            evens += 1
        h = h + (h >> 1)  # floor(3h/2)
    even_density = evens / n_steps
    return Ds, even_density, evens, odds


def running_mean_min(Ds, warmup=10):
    """running mean of D and the minimum running-mean after a warmup (liminf proxy)."""
    s = 0
    run_min = float("inf")
    means = []
    for i, d in enumerate(Ds, 1):
        s += d
        m = s / i
        means.append(m)
        if i >= warmup:
            run_min = min(run_min, m)
    return means, run_min


def syracuse_model(R, seed=12345):
    """iid Geometric(1/2): P(D=k)=2^{-k}, k>=1.  Sample R values."""
    import random
    rng = random.Random(seed)
    Ds = []
    for _ in range(R):
        k = 1
        while rng.random() < 0.5:
            k += 1
        Ds.append(k)
    return Ds


def dist(Ds, kmax=10):
    c = Counter(Ds)
    n = len(Ds)
    return {k: c.get(k, 0) / n for k in range(1, kmax + 1)}


def main():
    N = 300_000  # base-map steps (exact bigint; h ~ 1.585*N bits)
    print("=" * 78)
    print("TAO-METHOD / SYRACUSE-MODEL ANGLE on the induced odd map  o' = 3^{D-1}(3o-1)/2^D")
    print("Target (non-halt):  even-density >= 1/3  <=>  liminf running-mean(D) >= 3/2")
    print("=" * 78)

    print(f"\n[REAL ORBIT] base map floor(3h/2) from 8, {N:,} steps ...")
    Ds, ed, ev, od = real_induced_D(N)
    R = len(Ds)
    print(f"  renewals (odds) R = {R:,}   evens = {ev:,}   even-density = {ed:.6f}  (need >=1/3=0.3333)")
    mean_D = sum(Ds) / R
    print(f"  mean(D) over orbit = {mean_D:.6f}   (need liminf >= 1.5)   1-1/mean(D) = {1-1/mean_D:.6f}")
    # consistency check: even-density vs 1-1/mean(D) (renewal identity, up to boundary)
    print(f"  renewal-identity check: even-density {ed:.5f} vs 1-1/mean(D) {1-1/mean_D:.5f}")

    means, run_min = running_mean_min(Ds, warmup=20)
    print(f"  running-mean(D): final = {means[-1]:.5f}   MIN after warmup = {run_min:.5f}")
    print(f"  margin of running-mean MIN above 3/2 = {run_min - 1.5:+.5f}")
    # earliest index where running mean dips below thresholds
    for thr in (1.5, 1.6, 1.7):
        idx = [i for i, m in enumerate(means, 1) if i >= 20 and m < thr]
        print(f"    running-mean < {thr}: {'never' if not idx else f'at {len(idx)} of {R} renewals (min {min(means[19:]):.4f})'}")

    print(f"\n[REAL ORBIT] D-distribution vs Geometric(1/2):")
    dr = dist(Ds)
    print(f"  {'k':>3} {'real P(D=k)':>13} {'geom 2^-k':>11} {'real cum>=k':>12}")
    cum = 1.0
    for k in range(1, 9):
        geom = 2.0 ** (-k)
        print(f"  {k:>3} {dr[k]:>13.5f} {geom:>11.5f} {cum:>12.5f}")
        cum -= dr[k]

    print(f"\n[SYRACUSE MODEL] iid Geometric(1/2), R = {R:,} samples (3 seeds):")
    for seed in (1, 2, 3):
        Dm = syracuse_model(R, seed)
        mm, rmin = running_mean_min(Dm, warmup=20)
        print(f"  seed {seed}: mean(D) = {sum(Dm)/R:.5f}   running-mean final = {mm[-1]:.5f}   MIN(after warmup) = {rmin:.5f}  (margin {rmin-1.5:+.4f})")

    print(f"\n[ROBUSTNESS] How robust is liminf mean(D) >= 3/2 to a localized deficit?")
    print(f"  To drag the running mean of R={R:,} below 3/2 you need the partial sum of D to fall")
    print(f"  below 1.5*R. Real partial-sum slack at the end = sum(D) - 1.5*R = {sum(Ds) - 1.5*R:,.0f}")
    # worst suffix deficit: min over j of (sum_{i<=j} D_i) - 1.5*j  (how close to crossing 0)
    s = 0
    worst = float("inf")
    worst_at = 0
    for j, d in enumerate(Ds, 1):
        s += d
        slack = s - 1.5 * j
        if slack < worst:
            worst, worst_at = slack, j
    print(f"  worst prefix slack  min_j [ sum_{{i<=j}}D_i - 1.5 j ] = {worst:.1f} at renewal {worst_at:,}")
    print(f"    (>0 means running mean NEVER dipped below 3/2 over the whole orbit)")

    print("\n" + "=" * 78)
    print("READING:")
    print("  - Real D-dist tracks Geometric(1/2) closely; mean ~ 2, liminf running-mean stays > 1.5")
    print("    with a large absolute slack -> the >= 3/2 target holds with ~+0.5 margin EMPIRICALLY.")
    print("  - This is OBSERVED, not proven: it is exactly the single-orbit equidistribution (Mahler 3/2)")
    print("    that neither Tao (almost-all STARTS, log density) nor Krasikov-Lagarias (counting STARTS)")
    print("    delivers for one fixed orbit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
