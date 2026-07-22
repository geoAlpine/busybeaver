#!/usr/bin/env python3
"""D11 (2026-07-22): apply the re-examined √-scaling method to the EASIEST rung, o4.

D10 established that Antihydra's quenched character sums (dyadic + coprime) sit at the CLT √ tier.
The sharpest LEVER (D3) is o4-first: DECIDE o4 <=> prove Re(S1(n)) < 0.7·n for the seed orbit,
where S1 = Σ e(2πi W_n / 3) (a mod-3 character), and freq{3|W_n} = 1/3 + (2/3)·Re(S1)/N.
Fatal iff freq ≥ 4/5 iff Re(S1)/n ≥ 0.7. The target has a 0.30 absolute slack -- unlike
Antihydra's zero-margin ½-density.

This measures Re(S1(N))/N and |S1(N)| across N-decades to confirm the √-tier scaling on o4
(the analogue of D10 for the easy rung), banking D3's numerical support:
 - if |S1| ~ √N (exponent +½), then Re(S1)/N ~ N^{-1/2} → 0 ≪ 0.7 (huge margin, √-tier),
   and the o4 wall is confirmed as the SAME √-barrier as Antihydra but with slack 0.30.

o4 dynamics (O4_LEDGER_ANALYSIS / D8): odometer 3·G' = 4·G + e(ρ), ρ = G mod 3,
e = {0:9, 1:14, 2:1}; W_n = G_n + 14. Seed G_0 = 43 (W_0 = 57).
Instrument anchor: the fatal count uses #1 = #{i : 3 | W_i}; freq{ρ=1} should be ≈ 0.334
(D8: 0.334033), and the ledger a_n ≈ a_0 + 3n (drift +3).
"""
import math, cmath

def run(N):
    G = 43
    Ns = [10_000, 40_000, 160_000, 640_000, 2_560_000, 10_240_000]
    e = {0: 9, 1: 14, 2: 1}
    S1 = 0 + 0j
    cnt1 = 0            # #{i : 3 | W_i}  (W = G+14, 3|W <=> G ≡ 1 mod 3, i.e. ρ=1)
    cp = {}
    for i in range(N):
        W = G + 14
        S1 += cmath.exp(2j * math.pi * (W % 3) / 3)
        rho = G % 3
        if rho == 1:
            cnt1 += 1
        G = (4 * G + e[rho]) // 3
        n = i + 1
        if n in Ns:
            cp[n] = (S1.real, abs(S1), cnt1 / n)
    return cp

N = 10_240_000
cp = run(N)

print("=== instrument: freq{ρ=1} = freq{3|W} (D8 recorded ≈ 0.334) ===")
print(f"  at N={N}: {cp[N][2]:.4f}")

print("\n=== the o4 target scalar Re(S1)/N  (fatal threshold 0.7; slack 0.30) ===")
print(f"{'N':>10} {'Re(S1)':>12} {'Re(S1)/N':>11} {'|S1|':>10} {'sqrt(N)':>9} {'|S1|/sqrt(N)':>12}")
for n in sorted(cp):
    re, ab, f = cp[n]
    print(f"{n:>10} {re:>12.1f} {re/n:>11.6f} {ab:>10.1f} {math.sqrt(n):>9.0f} {ab/math.sqrt(n):>12.3f}")

print("\n=== |S1| growth exponent α (|S1| ~ N^α; CLT = 0.50) ===")
ns = sorted(cp)
for a, b in zip(ns, ns[1:]):
    aa = math.log(cp[b][1] / cp[a][1]) / math.log(b / a)
    print(f"  {a:>10}->{b:<10}: α = {aa:+.3f}")

re, ab, f = cp[N]
print(f"\n=== verdict at N={N} ===")
print(f"  Re(S1)/N = {re/N:.6f}   (target < 0.7; margin to fatal = {0.7 - re/N:.4f})")
print(f"  = {0.7 / (abs(re/N) if re else 1e-9):.0f}x inside the 0.7 threshold" if re else "")
print(f"  |S1|/√N = {ab/math.sqrt(N):.3f}  -> {'√-TIER (Re(S1)/N ~ N^{-1/2} -> 0)' if 0.2 < ab/math.sqrt(N) < 5 else 'NOT √'}")
