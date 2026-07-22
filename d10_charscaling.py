#!/usr/bin/env python3
"""D10 (2026-07-22): classify the D9 byproduct -- beyond-sqrt cancellation at ODD moduli vs
the DYADIC (mod 2^k) characters that Theorem E actually needs.

Background: D9 observed |S| = 84.9 over 1.25M induced steps at m=5 -- 12x beyond sqrt. But
Theorem E (THEORY.md B5', the sharpest (K) lever) needs cancellation for characters mod 2^k
(the dyadic cylinder deviations delta_k). If odd-moduli sums are O(1)/O(log) (a coboundary /
finite-chain artifact) while dyadic sums sit at the CLT sqrt barrier, the byproduct is
EXPLAINED-AWAY and goes to the trap list -- and the wall statement sharpens to:
"dyadic characters at the sqrt barrier; everything coprime cancels for free."

Probe: Antihydra c_0=8, c -> 3c/2 (even) / c odd contributes to the odd-restricted sums.
  S_dyadic(k,N) = sum_{i<N, c_i odd} e(2 pi i c_i / 2^k),  k=3..6
  S_odd(m,N)    = sum_{i<N, c_i odd} e(2 pi i (c_i mod m) / m),  m=5,7
at N = 1e4, 4e4, 1.6e5, 6.4e5, 2.56e6; report |S| and the growth exponent alpha
(|S| ~ N^alpha) between consecutive decades, vs the CLT line alpha=1/2.

Instrument anchor: even-density at N=2.56e6 must be ~0.50018 (recorded).
"""
import math, cmath

def run(N):
    c = 8
    Ns = [10_000, 40_000, 160_000, 640_000, 2_560_000]
    ks = [3,4,5,6]
    ms = [5,7]
    Sd = {k: 0+0j for k in ks}
    So = {m: 0+0j for m in ms}
    out = []
    evens = 0
    nodd = 0
    checkpoints = {}
    for i in range(N):
        if c & 1:
            nodd += 1
            for k in ks:
                r = c & ((1 << k) - 1)
                Sd[k] += cmath.exp(2j * math.pi * r / (1 << k))
            for m in ms:
                So[m] += cmath.exp(2j * math.pi * (c % m) / m)
            c = (3 * c - 1) >> 1
        else:
            evens += 1
            c = (3 * c) >> 1
        n = i + 1
        if n in Ns:
            checkpoints[n] = (evens / n, nodd,
                              {k: abs(Sd[k]) for k in ks},
                              {m: abs(So[m]) for m in ms})
    return checkpoints

N = 2_560_000
cp = run(N)

print("=== instrument: even-density at N=2.56e6 (recorded ~0.50018) ===")
print(f"  {cp[N][0]:.5f}")

print("\n=== |S| by N  (CLT line = sqrt(N_odd)) ===")
hdr = "N        N_odd    sqrt   | " + "  ".join(f"2^{k}" for k in (3,4,5,6)) + " |  m=5    m=7"
print(hdr)
prev = None
for n in sorted(cp):
    ed, nodd, sd, so = cp[n]
    line = f"{n:<8} {nodd:<8} {math.sqrt(nodd):6.0f} | " + \
           "  ".join(f"{sd[k]:6.1f}" for k in (3,4,5,6)) + \
           f" | {so[5]:6.1f} {so[7]:6.1f}"
    print(line)

print("\n=== growth exponents alpha between consecutive checkpoints (|S| ~ N^alpha) ===")
ns = sorted(cp)
for a, b in zip(ns, ns[1:]):
    la = math.log(b / a)
    _, _, sda, soa = cp[a]
    _, _, sdb, sob = cp[b]
    dal = {k: math.log(max(sdb[k], 1e-9) / max(sda[k], 1e-9)) / la for k in (3,4,5,6)}
    oal = {m: math.log(max(sob[m], 1e-9) / max(soa[m], 1e-9)) / la for m in (5,7)}
    print(f"  {a:>8}->{b:<8}: dyadic " +
          " ".join(f"2^{k}:{dal[k]:+.2f}" for k in (3,4,5,6)) +
          "   odd " + " ".join(f"m{m}:{oal[m]:+.2f}" for m in (5,7)) +
          "   (CLT=+0.50)")
