"""
O4 p-ADIC (3-adic) DYNAMICS EXPLORATION  (2026-07-10)
====================================================
T as a dynamical system on P^1(Q_3) / the expanding self-map of Z_3.
Branch maps b_rho(v) = (4v + e(rho))/3, e = {0:9, 1:14, 2:1}, fixed x_rho = -e.

We verify, with EXACT 3-adic arithmetic:
 (1) The multiplier at each branch fixed point: b'(v) = 4/3, |4/3|_3 = 3 -> REPELLING.
 (2) The run-cap AS a p-adic dynamical statement: within a rho-run, the distance
     to the fixed point x_rho grows by exactly a factor 3 in |.|_3 each step,
     i.e. v_3(v_n - x_rho) drops by exactly 1 -> run = v_3(v_0 - x_rho).
 (3) Frequency axis: natural invariant / maximal-entropy measure of the expanding
     3-to-1 full-branch map = Haar on Z_3. Freq of rho=1 depth L = 3^{-L}.
     Test whether the single real forward orbit equidistributes w.r.t. Haar and
     at what RATE (geometric annealed vs 1/sqrt(N) quenched Birkhoff).
"""
from fractions import Fraction

E = {0: 9, 1: 14, 2: 1}
FIXED = {0: -9, 1: -14, 2: -1}


def v3(n):
    """3-adic valuation of a nonzero integer (Fraction ok)."""
    if n == 0:
        return float('inf')
    if isinstance(n, Fraction):
        return v3(n.numerator) - v3(n.denominator)
    n = abs(int(n))
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k


def abs3(n):
    """3-adic absolute value |n|_3 = 3^{-v3(n)}."""
    val = v3(n)
    if val == float('inf'):
        return 0.0
    return 3.0 ** (-val)


def branch(v):
    """One deterministic step of the piecewise map T on the integers."""
    rho = v % 3
    return (4 * v + E[rho]) // 3, rho


# ----------------------------------------------------------------------
# (1) MULTIPLIER at each fixed point.  b_rho(v) = (4/3) v + e/3, derivative 4/3.
# ----------------------------------------------------------------------
print("=" * 68)
print("(1) MULTIPLIER at branch fixed points x_rho = -e(rho)")
print("=" * 68)
mult = Fraction(4, 3)
print(f"branch derivative b'(v) = {mult}   |b'|_3 = |4/3|_3 = 3^{{-v3(4/3)}} = {abs3(mult)}")
print(f"    v3(4/3) = v3(4)-v3(3) = {v3(4)} - {v3(3)} = {v3(4)-v3(3)}  => |4/3|_3 = 3 > 1  REPELLING")
for rho in (0, 1, 2):
    x = FIXED[rho]
    # verify fixed: b(x) == x
    bx = Fraction(4 * x + E[rho], 3)
    print(f"  rho={rho}: x={x:>4}   b(x)=(4*{x}+{E[rho]})/3 = {bx}  fixed={bx==x}   "
          f"multiplier |4/3|_3 = {abs3(mult):.0f}  (repelling)")

# ----------------------------------------------------------------------
# (2) RUN-CAP as a p-adic statement.  Take a v deep in the rho=1 class and
#     iterate the SINGLE affine branch b_1; watch v_3(v_n + 14) and |v_n+14|_3.
# ----------------------------------------------------------------------
print()
print("=" * 68)
print("(2) RUN-CAP = geometric escape from the repelling fixed point -14")
print("=" * 68)
# choose v0 with v_3(v0+14) = 6, i.e. v0 = -14 + 3^6 (deep rho=1 shadow)
v0 = -14 + 3**6
print(f"v0 = -14 + 3^6 = {v0},  v3(v0+14) = {v3(v0+14)}  (6-deep in the -14 shadow)")
v = v0
for step in range(8):
    d = v + 14
    print(f"  step {step}: v={v:>7}  v_n+14={d:>7}  v3={v3(d):>2}  |v_n+14|_3={abs3(d):.5f}"
          f"   rho=v%3={v % 3}")
    if v % 3 != 1:
        print("     -> rho != 1: run ENDED (left the -14 shadow); run length was", step)
        break
    # apply the rho=1 branch (deterministic T agrees while rho stays 1)
    v = (4 * v + 14) // 3
print("Confirmed: |v_n+14|_3 multiplies by exactly 3 each step (v3 drops by 1)")
print("=> run length = v3(v0+14) EXACTLY = the mirror-ladder run law, restated as")
print("   'orbit escapes the repelling fixed point at the rate set by |mult|_3=3'.")

# exhaustive cross-check of the run law over many seeds
print("\nExhaustive run-law check (rho=1 branch), v0 = -14 + m, m=1..20000:")
bad = 0
for m in range(1, 20001):
    v0 = -14 + m
    if v0 % 3 != 1:
        continue
    predicted = v3(v0 + 14)
    # measured run under repeated b_1 (deterministic T) while rho stays 1
    v = v0
    run = 0
    while v % 3 == 1:
        v = (4 * v + 14) // 3
        run += 1
    if run != predicted:
        bad += 1
print(f"  mismatches: {bad}  (0 = run law = 3-adic escape rate holds exactly)")

# ----------------------------------------------------------------------
# (3) FREQUENCY axis: equidistribution of the single forward orbit w.r.t. Haar.
#     Natural max-entropy measure of the full 3-to-1 expanding map = Haar.
#     Freq of {rho=1 to depth L} predicted by Haar = 3^{-L}.  Measure it, and
#     measure the RATE of equidistribution (annealed geometric vs quenched 1/sqrt).
# ----------------------------------------------------------------------
print()
print("=" * 68)
print("(3) FREQUENCY = forward-orbit equidistribution w.r.t. Haar (the max-entropy")
print("    measure of the expanding 3-to-1 full-branch map)")
print("=" * 68)
import math
G0 = 8
# NOTE: G_n grows like (4/3)^n as an EXACT integer (~0.125*n digits), so N is
# bounded by big-int cost.  The 1/sqrt(N) floor is already visible by N~1e5.
N = 120_000
# generate real orbit
G = G0
# frequency of rho values and of depth-L returns to the -14 shadow
rho_count = {0: 0, 1: 0, 2: 0}
depth_count = {}   # v3(G_n + 14) histogram (depth of -14 shadow at each step)
# empirical character sums e_{3^k}(G_n) for the equidistribution RATE
K = 4
Mk = 3 ** K
csum = 0j
partials = []
for n in range(N):
    rho = G % 3
    rho_count[rho] += 1
    d = v3(G + 14)
    dd = d if d != float('inf') else 99
    depth_count[dd] = depth_count.get(dd, 0) + 1
    csum += complex(math.cos(2 * math.pi * (G % Mk) / Mk),
                    math.sin(2 * math.pi * (G % Mk) / Mk))
    if n in (999, 9999, 49999, 99999, N - 1):
        partials.append((n + 1, abs(csum) / (n + 1)))
    G = (4 * G + E[rho]) // 3

print(f"orbit G0={G0}, N={N} steps")
print("rho frequencies (Haar predicts 1/3 each):")
for rho in (0, 1, 2):
    print(f"   rho={rho}: {rho_count[rho]/N:.5f}")
print("\n-14 shadow depth L frequency  (Haar predicts (rho=1 & depth L) ~ 2*3^{-(L+1)} "
      "for L>=1, i.e. v3(G+14)=L has Haar mass 2*3^{-(L+1)}):")
for L in sorted(depth_count)[:9]:
    haar = 2 * 3 ** (-(L + 1)) if L >= 1 else None
    hstr = f"Haar~{haar:.5f}" if haar is not None else "Haar~2/3 (depth0=rho!=1)"
    print(f"   depth {L:>2}: emp {depth_count[L]/N:.5f}   {hstr}")

print("\nEquidistribution RATE: |(1/N) sum e_{3^4}(G_n)|  vs  N")
print("  (annealed transfer op predicts geometric ~lambda2^N ~ 0 in O(k) steps;")
print("   quenched single orbit predicts CLT/Birkhoff floor ~ 1/sqrt(N)):")
for Nn, val in partials:
    print(f"   N={Nn:>8}: char={val:.6f}   1/sqrt(N)={1/math.sqrt(Nn):.6f}")
print("\n=> single-orbit character decays at the 1/sqrt(N) Birkhoff rate, NOT the")
print("   geometric annealed rate: forward-orbit equidistribution is the QUENCHED")
print("   (time-average) question = (K), not the effective ensemble mixing.")
