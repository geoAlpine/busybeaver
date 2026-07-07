#!/usr/bin/env python
"""ah_ledger_kernel.py — Antihydra kernel recast in the o4-ledger framework: exact verification.

Verifies (ANTIHYDRA_LEDGER_UNIFICATION_2026-07-07.md, Tasks 1 & 3 small-N):
  A. Branch maps + integer fixed points (family fixed-point theorem, (p,q)=(2,3) instance).
  B. Run closed forms  even-run = v2(c), odd-run = v2(c-1): exhaustive c <= 2*10^5 + real orbit.
  C. Ledger B_n = 3E_n - n: increment law {even:+2, odd:-1}, halt-condition equivalences,
     seed/offset convention, orbit margins (min B, worst running average, max depth vs ceiling).
  D. Ruin base eta = (sqrt5-1)/2: exact root of (eta^2 + eta^-1)/2 = 1 (golden-ratio conjugate).
  E. Multi-run decomposition identity: B before odd run i = 2*sum(e_j, j<=i) - sum(s_j, j<i).

Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
"""
from fractions import Fraction
import math

ok = True
def check(name, cond, detail=""):
    global ok
    print(("PASS  " if cond else "FAIL  ") + name + ("" if not detail else "  | " + detail))
    if not cond: ok = False

def step(c):
    return (3*c) >> 1 if c % 2 == 0 else (3*c - 1) >> 1

def v2(m):
    assert m > 0
    return (m & -m).bit_length() - 1

# ---------------------------------------------------------------- A. fixed points
# branch maps: even c -> 3c/2 ; odd c -> (3c-1)/2, i.e. c -> (3c - r)/2 with r = c mod 2.
for r in (0, 1):
    x = Fraction(r)                      # solve 2x = 3x - r  =>  x = r
    fx = (3*x - r) / 2
    check(f"fixed point branch r={r}: x={x}", fx == x and int(x) % 2 == r,
          f"x = {x} is an integer, x = r, x == r (mod 2)")
# contraction identity: c' - x = (3/2)(c - x) on the r-branch
for r, x in ((0, 0), (1, 1)):
    idok = all(Fraction(3*c - r, 2) - x == Fraction(3, 2) * (c - x)
               for c in range(r, 60, 2))
    check(f"branch r={r}: c' - {x} = (3/2)(c - {x}) identity", idok)

# ---------------------------------------------------------------- B. run closed forms, exhaustive
def parity_run(c):
    """length of the maximal constant-parity run starting at c"""
    r, n = c % 2, 0
    while c % 2 == r:
        c = step(c); n += 1
    return n

LIM = 200_000
bad = 0
for c in range(2, LIM + 1):
    pred = v2(c) if c % 2 == 0 else v2(c - 1)
    if parity_run(c) != pred:
        bad += 1
check(f"run closed forms exhaustive c=2..{LIM}", bad == 0,
      f"even-run = v2(c), odd-run = v2(c-1); mismatches = {bad}")

# ---------------------------------------------------------------- C. real orbit, N = 2*10^5
N = 200_000
c = 8
E = 0                    # evens among c_0..c_{n-1}
B = 0                    # B_n = 3E_n - n ; B_0 = 0 (seed convention)
minB, argminB = None, None            # over n >= 1
worst_avg, arg_worst = 10.0, None     # min over N>=1 of (2E_N - N)/N
runs = []                             # alternating (parity, length, v2-prediction, B at entry)
run_par, run_len, run_pred, run_B = c % 2, 0, v2(c) if c % 2 == 0 else v2(c - 1), 0
max_depth, arg_depth = 0, None        # max v2(c_n - 1) over the range (odd depth incl. all n)
inc_ok = True
run_ok = True
for n in range(N):
    par = c % 2
    if par != run_par:
        runs.append((run_par, run_len, run_pred, run_B))
        if run_len != run_pred: run_ok = False
        run_par, run_len, run_pred, run_B = par, 0, (v2(c) if par == 0 else v2(c - 1)), B
    run_len += 1
    d = v2(c - 1) if c % 2 == 1 else 0
    if d > max_depth: max_depth, arg_depth = d, n
    E += (par == 0)
    Bnew = 3*E - (n + 1)
    if Bnew - B != (2 if par == 0 else -1): inc_ok = False
    B = Bnew
    if minB is None or B < minB: minB, argminB = B, n + 1
    avg = (2*E - (n + 1)) / (n + 1)
    if avg < worst_avg: worst_avg, arg_worst = avg, n + 1
    c = step(c)
runs.append((run_par, run_len, run_pred, run_B))
if run_len > run_pred or (run_len < run_pred and False): pass  # last run truncated by horizon: only check <=
check("orbit prefix: c0=8 -> 12 -> 18 -> 27 (even-run 3 = v2(8))",
      runs[0] == (0, 3, 3, 0), f"first run record = {runs[0]}")
check(f"ledger increment law on orbit (n<{N})", inc_ok, "B_{n+1}-B_n = +2 (even) / -1 (odd), B_0 = 0")
check(f"run closed forms on the real orbit ({len(runs)-1} completed runs)", run_ok,
      "every completed maximal run = v2(c - x_r) at entry")
check("last (truncated) run <= its closed form", run_len <= run_pred,
      f"observed {run_len} <= v2-prediction {run_pred}")
print(f"      orbit N={N}: E_N={E}, even-density={E/N:.5f}, B_N={3*E-N}")
print(f"      min_(n>=1) B_n = {minB} at n={argminB}   (B_0 = 0 by seed convention)")
wa_frac = Fraction(worst_avg).limit_denominator(10**6)
print(f"      worst running avg (2E_N-N)/N = {worst_avg:.6f} = {wa_frac} at N={arg_worst}")
check("TRUE worst running avg = -2/23 at N=46 (CORRECTS memory's '-0.0407 at n=122')",
      arg_worst == 46 and abs(worst_avg + 2/23) < 1e-12,
      f"found {worst_avg:.6f} at N={arg_worst}; margin above -1/3: {worst_avg + 1/3:.4f}")
# the memory's number is the post-startup dip: worst over N >= 100
c3, E3, w100, a100 = 8, 0, 10.0, None
for n in range(1, N + 1):
    E3 += (c3 % 2 == 0); c3 = step(c3)
    a = (2*E3 - n) / n
    if n >= 100 and a < w100: w100, a100 = a, n
check("memory's -0.0407 identified: worst over N>=100 is -5/123 at N=123 (second dip)",
      a100 == 123 and abs(w100 + 5/123) < 1e-12, f"{w100:.6f} at N={a100}")
check("max_n v2(c_n - 1) at N=2*10^5 equals 20 (PROOF_TOOL_ATTEMPT)",
      max_depth == 20, f"max depth {max_depth} at n={arg_depth}; ~log2(N)={math.log2(N):.1f}")
print(f"      unconditional ceiling at that n: 0.585*n = {0.585*arg_depth:.0f}; needed (<0.5n): {0.5*arg_depth:.0f}; truth: {max_depth}")

# magnitude bounds (the ceiling's ingredient): 7*(3/2)^n <= c_n - 1 and c_n <= 8*(3/2)^n
# (2-line induction: c' <= 3c/2 always; c' - 1 >= (3/2)(c-1) with equality on odd steps)
cB, mag_ok = 8, True
lo, hi = Fraction(7), Fraction(8)
for n in range(2000):
    cB = step(cB); lo *= Fraction(3, 2); hi *= Fraction(3, 2)
    if not (lo <= cB - 1 and cB <= hi): mag_ok = False
check("magnitude bounds 7*(3/2)^n <= c_n - 1, c_n <= 8*(3/2)^n (n<=2000, exact Fractions)",
      mag_ok, "hence depth cap v2(c_n - 1) <= n*log2(3/2) + 3 = 0.585n + 3 [PROVEN]")

# halt-condition equivalences (arithmetic identities, checked pointwise on the orbit)
c2, E2, eq_ok = 8, 0, True
for n in range(1, 20001):
    E2 += (c2 % 2 == 0); c2 = step(c2)
    Bn = 3*E2 - n
    if (Bn >= 0) != (3*E2 >= n) or (Bn >= 0) != ((2*E2 - n) / n >= -1/3 - 1e-15): eq_ok = False
check("halt-condition forms agree: B_n>=0 <=> E_n/n>=1/3 <=> running avg >= -1/3", eq_ok)

# ---------------------------------------------------------------- D. ruin base eta
eta = (math.sqrt(5) - 1) / 2
check("eta = (sqrt5-1)/2 solves (eta^2 + 1/eta)/2 = 1", abs((eta*eta + 1/eta)/2 - 1) < 1e-14,
      f"eta = {eta:.6f}")
# exact: (x^2 + 1/x)/2 = 1  <=>  x^3 - 2x + 1 = 0  <=>  (x-1)(x^2+x-1) = 0 : golden conjugate.
# verify the factorization symbolically over Q[x] (coefficient comparison):
#   (x-1)(x^2+x-1) = x^3 + x^2 - x - x^2 - x + 1 = x^3 - 2x + 1
lhs = [1, 0, -2, 1]                       # x^3 - 2x + 1
prod = [0]*4
for i, a in enumerate([1, -1]):           # x - 1
    for j, b in enumerate([1, 1, -1]):    # x^2 + x - 1
        prod[i + j] += a*b
check("x^3-2x+1 = (x-1)(x^2+x-1) exactly", prod == lhs,
      "root in (0,1) is (sqrt5-1)/2 — the golden-ratio conjugate 1/phi")
check("eta is a root of x^2+x-1 (not the spurious x=1 root)",
      abs(eta*eta + eta - 1) < 1e-14)
# drift: annealed increments {+2 w.p. 1/2, -1 w.p. 1/2} -> +1/2 per step; E[eta^{-dB}] = 1:
check("eta is the exact ruin base: (eta^2 + eta^-1)/2 = 1 <=> E[eta^{-dB}]=1 for dB in {+2,-1} uniform",
      abs((eta**2 + eta**(-1)) / 2 - 1) < 1e-14, "annealed drift = (1/2)(+2)+(1/2)(-1) = +1/2")

# ---------------------------------------------------------------- E. multi-run decomposition
# runs alternate even/odd starting even (c0=8). With e_j / s_j the even/odd run lengths,
# the ledger before odd run i is  B = 2*sum_{j<=i} e_j - sum_{j<i} s_j, and the machine
# halts iff some odd run has s_i >= (that quantity) + 1.
evens = [ln for (p, ln, _, _) in runs if p == 0]
odds_ = [(ln, Bent) for (p, ln, _, Bent) in runs if p == 1]
dec_ok, worst_frac = True, 0.0
se, ss = 0, 0
oi = 0
for (p, ln, _, Bent) in runs[:-1]:
    if p == 0:
        se += ln
    else:
        pred_B = 2*se - ss
        if pred_B != Bent: dec_ok = False
        if Bent > 0: worst_frac = max(worst_frac, ln / Bent)
        ss += ln
        oi += 1
check("multi-run identity: B at odd-run entry = 2*sum(e_j) - sum(s_j)", dec_ok,
      f"{oi} odd runs checked")
print(f"      worst single-run drain fraction s_i / B(entry) observed = {worst_frac:.4f}  (fatality needs > 1)")
print(f"      run counts: {len(evens)} even runs (mean {sum(evens)/len(evens):.3f}), "
      f"{oi} odd runs (mean {ss/oi:.3f}) — annealed means are 2 and 2")

print()
print("ALL CHECKS PASSED" if ok else "*** SOME CHECKS FAILED ***")

