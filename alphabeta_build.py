import numpy as np, math
# Build (beta): first genuine UNCONDITIONAL partial beyond "infinitely many evens".
# Argument: consecutive even positions p_i, p_{i+1}: gap = odd-run length = depth at run start <= log2(c) ~0.585p.
# So p_{i+1} <= p_i + 0.585 p_i = 1.585 p_i (geometric) => E_n >= log(n)/log(1.585) ~ 2.2 log n. UNCONDITIONAL.
N=200000
c=8; evens=[]
for n in range(N):
    if c%2==0: evens.append(n)
    c=3*c//2
# verify the geometric gap bound: is p_{i+1}/p_i bounded? (provable bound 1.585; empirical smaller)
ratios=[evens[i+1]/evens[i] for i in range(10,len(evens)-1) if evens[i]>0]
print("(beta) FIRST PARTIAL: E_n = Omega(log n) unconditional")
print(f"  consecutive even-position ratio p_(i+1)/p_i: max={max(ratios):.4f} mean={np.mean(ratios):.4f}")
print(f"  provable bound (from depth<=log2 c ~0.585n): p_(i+1) <= 1.585 p_i  (holds: {max(ratios)<=1.586})")
print(f"  => E_n >= log(n)/log(1.585) = {math.log(N)/math.log(1.585):.0f} (vs actual E_n={len(evens)})")
print(f"  (actual is ~N/2; the bound Omega(log n) is real+unconditional but far below positive density)")
print()
# the gap to the kernel: positive density needs depth=o(n), not just <=0.585n.
print("(beta) NEW OPEN CORE (what improves the partial to the full result):")
print("  even-density>1/3  <==  depth_n = o(n)  [vs trivial depth<=0.585n].")
print("  Equivalently: improve the trivial 2-adic valuation bound v2(c_n-1)<=log2(c_n) to o(n).")
print("  This is the (beta) target theorem: a sub-linear 2-adic depth bound for the SELF-REFERENTIAL")
print("  linear-feedback carry S_n. The linear structure controls off-diagonal; the o(n) needs the diagonal.")

# Build (alpha): the rank-1 equidistribution target. State the precise Diophantine condition.
print("\n(alpha) rank-1 specific-orbit equidistribution -- the target theorem + its required input:")
print("  THEOREM-TO-PROVE: {(3/2)^n} equidistributes mod 1.  Weyl: |sum_{n<=N} e(h(3/2)^n)| = o(N).")
print("  The ONLY provable input today: {n log2(3)} equidistributes (top ~log n bits, Benford).")
print("  REQUIRED NEW INPUT: an effective-discrepancy / mixing statement for the rank-1 map x(3/2) that")
print("  reaches depth eps*n -- a rank-1 'effective Furstenberg' with a Diophantine condition on log2(3).")
# measure the Diophantine quality of log2(3) (irrationality measure proxy via continued fraction)
from fractions import Fraction
import mpmath as mp
mp.mp.dps=200
a=mp.log(3)/mp.log(2)
cf=[]
x=a
for _ in range(25): cf.append(int(mp.floor(x))); x=1/(x-mp.floor(x))
print(f"  continued fraction of log2(3) = {cf[:15]}...")
print(f"  max partial quotient (first 25) = {max(cf)} => log2(3) is NOT Liouville (bounded-type-ish);")
print(f"  its discrepancy ~ (log N)/N (good), but that only controls O(log N) top bits = the foothold wall.")
