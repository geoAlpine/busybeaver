#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Route #19 -- periodic-orbit shadowing of the (K)-kernel orbit (2026-07-25).

Kernel: induced odd map T(o) = 3^(D-1)(3o-1)/2^D, D = v2(3o-1), seed 27.
Periodic points = fixed points of branch words w = (d1..dq):
    x*(w) = B_w * 2^S / (2^S - 3^S),  S = sum d_i   (rational, odd denominator,
    the p/(3^q - 2^q) family for the all-1 words).

Measurements (all exact big-int / Fraction; floats only for real statistics):

 M1. Periodic-point family verified: x*(w) is a genuine period-q point whose
     branch itinerary equals w (checked for every word used below).
 M2. Ensemble equidistribution [check of the prompt's claim]: with natural
     (Gibbs) weights 2^-S, the periodic points of period q equidistribute in
     residues mod 2^k (TV distance -> 0 as q grows) and the ensemble depth-mean
     -> 2 (the Haar value).  [MEASURED, truncation d_i <= 9 quantified]
 M3. The SAME ensemble carries (K)-VIOLATING mass at every period:
     P(S_q < 3q/2) computed exactly (negative-binomial), e.g. 29/128 at q=5.
     Violating periodic orbits (e.g. word (1,1,2), depth-mean 4/3) are
     themselves shadowed with error 0.  ==> summable shadowing cannot separate.
 M4. Shadowing decay for the true orbit: at sample times n, canonical shadow of
     period q is x*(D_n..D_{n+q-1}); measure v = v2(o_n - x*).  Prediction from
     the cylinder structure: v = S + 1 + (geometric excess).  [MEASURED]
     Consequence: the per-period shadowing exponent v/q = (window depth-mean)
     + O(1/q) -- the shadowing rate IS the (K)-statistic.
 M5. Random-model control: same measurement for the orbit of a random odd
     64-bit seed; distributions of the excess v-(S+1) compared.
 M6. Agreement with FIXED low-period orbits (period <= 3, d <= 4): distribution
     of the maximal agreement length along the orbit vs the same for the
     control (geometric tails; no anomalous shadowing structure).
"""

from fractions import Fraction as F
from itertools import product
import math, random

# ---------------------------------------------------------------- utilities
def v2int(n):
    n = abs(n)
    if n == 0:
        return None
    return (n & -n).bit_length() - 1

def orbit(o0, N):
    o = o0; os_ = [o]; Ds = []
    for _ in range(N):
        t = 3 * o - 1
        d = (t & -t).bit_length() - 1
        o = (3 ** (d - 1) * t) >> d
        Ds.append(d); os_.append(o)
    return os_, Ds

def fixed_point(word):
    """Exact fixed point of T_{dq} o ... o T_{d1}."""
    A, B = F(1), F(0)
    for d in word:
        mu = F(3 ** d, 2 ** d)
        A, B = mu * A, mu * B - F(3 ** (d - 1), 2 ** d)
    return B / (1 - A)

def branch_of(p):
    """D = v2(3p - 1) for rational p in Z2^x (odd denominator)."""
    t = 3 * p - 1
    if t == 0:
        return None
    return v2int(t.numerator) - v2int(t.denominator)

def step(p):
    d = branch_of(p)
    return d, (F(3) ** (d - 1)) * (3 * p - 1) / (F(2) ** d)

def verify_word(word):
    p0 = fixed_point(word)
    assert p0.denominator % 2 == 1 and p0.numerator % 2 == 1, (word, p0)
    p = p0
    for d in word:
        dd, p = step(p)
        if dd != d:
            return p0, False
    return p0, (p == p0)

def v2diff(o_int, p_frac):
    a, b = p_frac.numerator, p_frac.denominator
    diff = o_int * b - a
    if diff == 0:
        return None  # infinite
    return v2int(diff)  # b odd => v2 of difference

# ---------------------------------------------------------------- orbits
N = 20000
os_t, Ds_t = orbit(27, N)                       # true orbit
rng = random.Random(2026)
seed_c = rng.getrandbits(63) | 1
os_c, Ds_c = orbit(seed_c, N)                   # random-model control
mean_t = sum(Ds_t) / N
mean_c = sum(Ds_c) / N
print(f"true orbit  : seed 27, N={N}, depth-mean = {mean_t:.6f}")
print(f"control     : seed {seed_c} (random odd), depth-mean = {mean_c:.6f}")
print(f"(Haar/Bernoulli mean = 2; (K) threshold = 3/2)")

# ================================================================ M1
print()
print("=" * 78)
print("M1: periodic-point family verification [EXACT]")
print("=" * 78)
nver = 0
for q in (1, 2, 3):
    for w in product(range(1, 7), repeat=q):
        p0, ok = verify_word(w)
        assert ok, w
        nver += 1
print(f"  all words q<=3, d<=6: {nver} fixed points verified (itinerary = word,")
print(f"  T^q returns exactly).  Examples: x*(1)=1, x*(2)=3/5, "
      f"x*(1,2)={fixed_point((1,2))}, x*(1,1,2)={fixed_point((1,1,2))}")

# ================================================================ M2
print()
print("=" * 78)
print("M2: ensemble equidistribution with weights 2^-S [MEASURED]")
print("=" * 78)
DMAX = 9
for q in range(1, 6):
    hists = {k: {} for k in (4, 6, 8)}
    wtot = 0.0; wS = 0.0
    for w in product(range(1, DMAX + 1), repeat=q):
        S = sum(w)
        wt = 2.0 ** (-S)
        p = fixed_point(w)
        a, b = p.numerator, p.denominator
        wtot += wt; wS += wt * S
        for k in hists:
            mod = 1 << k
            r = (a * pow(b, -1, mod)) % mod
            hists[k][r] = hists[k].get(r, 0.0) + wt
    line = f"  q={q}: captured weight {wtot:.4f}, depth-mean {wS/(q*wtot):.4f}, TV(mod 2^k) ="
    for k in (4, 6, 8):
        ncl = 1 << (k - 1)
        tv = 0.5 * sum(abs(hists[k].get(r, 0.0) / wtot - 1.0 / ncl)
                       for r in range(1, 1 << k, 2))
        line += f"  k={k}: {tv:.4f}"
    print(line)
print(f"  (truncation d<=9 loses 1-(1-2^-9)^q of weight; TV -> 0 with q: the")
print(f"   ensemble equidistributes toward Haar and its depth-mean -> 2.)")

# ================================================================ M3
print()
print("=" * 78)
print("M3: exact (K)-violating mass of the SAME ensemble [EXACT]")
print("=" * 78)
def comb(n, r):
    return math.comb(n, r)
for q in (2, 5, 10, 20, 40):
    # S ~ sum of q iid Geometric(1/2) (support >=1); P(S=s)=C(s-1,q-1) 2^-s
    smax = (3 * q - 1) // 2  # S <= smax  <=>  S < 3q/2 (S integer)
    mass = sum(F(comb(s - 1, q - 1), 2 ** s) for s in range(q, smax + 1))
    print(f"  q={q:3d}: P(depth-mean of periodic word < 3/2) = {mass} = {float(mass):.6f}")
pv = fixed_point((1, 1, 2))
print(f"  explicit violator: word (1,1,2), depth-mean 4/3 < 3/2, "
      f"periodic point {pv};")
print(f"  it shadows ITSELF with 2-adic error 0 (exactly summable), so")
print(f"  'summable shadowing by equidistributed periodic orbits' holds for")
print(f"  (K)-violating orbits too -- shadowing cannot separate.")

# ================================================================ M4 + M5
print()
print("=" * 78)
print("M4/M5: canonical-shadow decay, true orbit vs random control [MEASURED]")
print("=" * 78)
QMAX = 40
samples = list(range(0, N - QMAX - 1, 500))

def shadow_stats(os_, Ds):
    excesses = []           # v - (S+1)
    slope_pts = []          # (S, v)
    exp_ratio = []          # v/q at q=QMAX vs window depth-mean
    for n in samples:
        for q in range(1, QMAX + 1):
            w = tuple(Ds[n:n + q])
            p = fixed_point(w)
            v = v2diff(os_[n], p)
            S = sum(w)
            assert v is not None and v >= S + 1, (n, q, v, S)
            excesses.append(v - (S + 1))
            slope_pts.append((S, v))
            if q == QMAX:
                exp_ratio.append((v / q, S / q))
    return excesses, slope_pts, exp_ratio

def summarize(tag, excesses, slope_pts, exp_ratio):
    import statistics
    xs = [s for s, _ in slope_pts]; ys = [v for _, v in slope_pts]
    mx = statistics.mean(xs); my = statistics.mean(ys)
    slope = (sum((x - mx) * (y - my) for x, y in slope_pts)
             / sum((x - mx) ** 2 for x in xs))
    hist = {}
    for e in excesses:
        hist[e] = hist.get(e, 0) + 1
    tot = len(excesses)
    hs = "  ".join(f"e={e}:{hist[e]/tot:.3f}" for e in sorted(hist)[:6])
    mean_vq = statistics.mean(r[0] for r in exp_ratio)
    mean_Sq = statistics.mean(r[1] for r in exp_ratio)
    print(f"  {tag}:")
    print(f"    v vs S regression slope = {slope:.5f} (predict 1);  "
          f"excess v-(S+1): mean = {statistics.mean(excesses):.4f}, "
          f"max = {max(excesses)}")
    print(f"    excess distribution: {hs}  (predict geometric(1/2): .5 .25 ...)")
    print(f"    at q={QMAX}: mean v/q = {mean_vq:.4f} vs window depth-mean "
          f"{mean_Sq:.4f} (+1/q offset {1/QMAX + 0.0:.3f})")

et, st_, rt = shadow_stats(os_t, Ds_t)
summarize("TRUE orbit (seed 27)", et, st_, rt)
ec, sc, rc = shadow_stats(os_c, Ds_c)
summarize("CONTROL (random seed)", ec, sc, rc)
print(f"  summability: error(q) = 2^-v <= 2^-(S_q+1) <= 2^-(q+1), so")
print(f"  sum_q error(q) < 1 for EVERY orbit -- including all-1 (o=1, depth-mean")
print(f"  1) and (1,1,2)-type violators.  Summable 2-adic shadowing is FREE.")

# ================================================================ M6
print()
print("=" * 78)
print("M6: max agreement length with FIXED periodic orbits (period<=3, d<=4)")
print("=" * 78)
W = []
for q in (1, 2, 3):
    W.extend(product(range(1, 5), repeat=q))
CAP = 60
def agree_stats(Ds):
    hist = {}
    for n in range(0, N - CAP):
        best = 0
        for w in W:
            L = len(w); i = 0
            while i < CAP and Ds[n + i] == w[i % L]:
                i += 1
            if i > best:
                best = i
        hist[best] = hist.get(best, 0) + 1
    return hist
ht = agree_stats(Ds_t); hc = agree_stats(Ds_c)
tot_t = sum(ht.values()); tot_c = sum(hc.values())
print("  L : P(true)   P(control)")
for L in range(0, 15):
    print(f"  {L:2d}: {ht.get(L,0)/tot_t:8.5f}  {hc.get(L,0)/tot_c:8.5f}")
mt = sum(k * v for k, v in ht.items()) / tot_t
mc = sum(k * v for k, v in hc.items()) / tot_c
print(f"  mean max-agreement: true {mt:.4f}, control {mc:.4f}, "
      f"max: true {max(ht)}, control {max(hc)}")
print(f"  ==> geometric tails, statistically indistinguishable from the random")
print(f"      model: no anomalous shadowing structure to exploit.")
print()
print("No machine decided. No label upgraded.")
