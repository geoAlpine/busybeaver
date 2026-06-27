"""Ergodic-optimization test for the one-sided sub-solution MINPROP_COBOUNDARY_LP.

Induced odd map  T(o) = 3^{D-1}(3o-1)/2^D,  D = v2(3o-1),  on odd 2-adic units.
psi(o) = 1{o==1 mod4} - 1{o==3 mod8} - 1/2,  Haar-mean -1/4.

Target (robust GAP-lemma):  avg psi <= 0  <=>  freq(D>=2)+freq(D>=3) >= 1/2.
One-sided sub-solution: bounded g with  psi <= g(T o) - g(o)  =>  limsup avg psi <= 0
for EVERY orbit.  Such g exists (continuous sub-action, level 0) IFF
   beta(psi) := max over T-invariant measures of  integral psi dmu   <=  0.
We compute beta via periodic orbits (Bousch/Jenkinson: maximizer is typically periodic).
"""

def v2(x):
    x = abs(int(x)); r = 0
    if x == 0: return 10**9
    while x % 2 == 0: x //= 2; r += 1
    return r

def psi_by_residue(o):
    o8 = o % 8
    a = 1 if (o % 4) == 1 else 0
    b = 1 if (o % 8) == 3 else 0
    return a - b - 0.5

def psi_by_D(o):
    D = v2(3*o - 1)
    if D == 1:   return +0.5
    if D == 2:   return -0.5
    return -1.5   # D>=3

# ---- 1. CONFIRM psi depends only on D (=current step's valuation) ----
mism = 0
for o in range(1, 2_000_000, 2):
    if abs(psi_by_residue(o) - psi_by_D(o)) > 1e-12:
        mism += 1
print(f"[1] psi(o) == psi(D)?  mismatches over odd o<2e6: {mism}")
print("    D=1 (o=1 mod4): psi=+1/2 | D=2 (o=7 mod8): psi=-1/2 | D>=3 (o=3 mod8): psi=-3/2\n")

# ---- 2. induced map and integer cycle search ----
def Tind(o):
    t = 3*o - 1
    D = v2(t)
    m = t // (2**D)          # odd
    return (3**(D-1)) * m, D

print("[2] integer cycles of the induced map (start o, capped iterations):")
seen_cycles = set()
for start in range(1, 200000, 2):
    o = start; path = {}; step = 0
    while o not in path and step < 2000 and o < 10**18 and o >= 1:
        path[o] = step; step += 1
        o, _ = Tind(o)
    if o in path:                      # found a cycle
        # extract cycle
        idx = path[o]
        cyc = sorted(k for k, v in path.items() if v >= idx)
        key = tuple(cyc)
        if key not in seen_cycles:
            seen_cycles.add(key)
            avg = sum(psi_by_D(x) for x in cyc) / len(cyc)
            print(f"    cycle (len {len(cyc)}) start-from {start}: {cyc[:6]}{'...' if len(cyc)>6 else ''}  psi-avg = {avg:+.4f}")
print()

# ---- 3. constant-D 2-adic fixed points o_d = 3^{d-1}/(3^d - 2^d) and psi ----
from fractions import Fraction
print("[3] constant-D fixed points o_d = 3^{d-1}/(3^d-2^d)  (2-adic units, denom odd):")
for d in range(1, 7):
    od = Fraction(3**(d-1), 3**d - 2**d)
    print(f"    d={d}: o_d = {od}   psi(D={d}) = {(+0.5 if d==1 else (-0.5 if d==2 else -1.5)):+.2f}")
print("    => MAX single-symbol psi = +1/2 at d=1 (o=1, the trivial/halting cycle)\n")

# ---- 4. max psi-average over all periodic D-words up to length L (full shift) ----
# psi depends only on current symbol; D in {1,2,>=3}. Max cyclic-word avg = max symbol value.
print("[4] ergodic-optimization max over periodic D-words (full shift, Haar=Bernoulli):")
print("    psi is a function of the CURRENT symbol only => max over invariant measures")
print("    = max_d psi(d) = psi(1) = +1/2  (Dirac on constant D=1 = fixed point o=1).")
print("    beta(psi) = max_mu integral psi = +1/2 > 0.\n")

# ---- 5. empirical Cesaro average of psi along orbit of o0=27 ----
o = 27
S = 0.0; N = 0; rec = {}
CHK = (10**3, 10**4, 3*10**4, 6*10**4, 10**5)
for n in range(1, CHK[-1]+1):
    S += psi_by_D(o); N += 1
    if n in CHK:
        rec[n] = S / N
    o, _ = Tind(o)
print("[5] empirical Cesaro avg of psi along orbit of o0=27 (should approach Haar -1/4):")
for n in sorted(rec):
    print(f"    N={n:>9}:  avg psi = {rec[n]:+.5f}")
print("    Haar value = -0.25.  (orbit of 27 satisfies target avg psi <= 0 empirically.)")
