"""Relative Weyl criterion: the joint (rotation base, fiber) equidistributes iff the joint Weyl sums
   W(m,s) = |(1/N) sum_n e(2pi i m theta_n) chi_s(c_n mod 2^k)|  ->  0  for all (m,s) != (0,0),
theta_n={n*alpha}, alpha=log2(3/2), chi_s a character of Z/2^k. We map W to expose where the PROVABLE base
helps: W(m,0)=base rotation Weyl sum (provably small), W(0,s)=fiber sum (the target), W(m,s)=cross terms.
If the cross terms FACTOR ~ W(m,0)*W(0,s) or are governed by the small base sum, the base rotation provides
leverage on the joint. 0 false proofs: Weyl sums measured with the 1/sqrt(N) null; the base smallness is the
known effective rotation discrepancy.
"""
import math, cmath

N = 400000
c = 8; res = []           # c_n mod 2^K
K = 2; MOD = 1 << K
seq = []
for n in range(N):
    seq.append(c & (MOD - 1)); c = (3 * c) // 2
alpha = math.log2(1.5)
null = 1.0 / math.sqrt(N)

# precompute theta phases e(2pi i m theta_n) on the fly; fiber characters chi_s(x)=e(2pi i s x / MOD)
def W(m, s):
    acc = 0j
    for n in range(N):
        acc += cmath.exp(2j*math.pi*(m*(n*alpha))) * cmath.exp(2j*math.pi*s*seq[n]/MOD)
    return abs(acc)/N

print(f"joint Weyl sums W(m,s) = |(1/N)sum e(2pi i m theta_n) chi_s(c_n mod {MOD})|; null ~ {null:.5f}, N={N}")
msl='m s'; print(f'  {msl:>5}', end='')
for s in range(MOD): print(f"{('s='+str(s)):>10}", end="")
print()
table = {}
for m in range(0, 4):
    print(f"  {m:>5}", end="")
    for s in range(MOD):
        if m == 0 and s == 0:
            print(f"{'--':>10}", end=""); continue
        w = W(m, s); table[(m, s)] = w
        print(f"{w:>10.5f}", end="")
    print()

# factorization test: is W(m,s) ~ W(m,0)*W(0,s)? (would mean base & fiber are 'independent' in the Weyl sense)
print(f"\nfactorization check  W(m,s)  vs  W(m,0)*W(0,s):")
for m in (1,2,3):
    for s in range(1, MOD):
        prod = table.get((m,0),0)*table.get((0,s),0)
        print(f"  W({m},{s})={table[(m,s)]:.5f}   W({m},0)*W(0,{s})={prod:.5f}   ratio={table[(m,s)]/prod if prod>0 else float('inf'):.2f}")

print(f"""
READING (relative Weyl, positive):
  - W(m,0) [base only] is provably small (rotation equidistribution, effective rate). W(0,s) [fiber only,
    s>=1] is the TARGET -- the parity/fiber balance -- empirically small but the open part.
  - The cross terms W(m,s): if they FACTOR as W(m,0)*W(0,s), the base and fiber are Weyl-independent and
    the joint sum is controlled by the product -- so any bound on the (small) base sum MULTIPLIES the
    fiber sum, a genuine reduction lever. If instead W(m,s) is governed by the small W(m,0) regardless of
    s, the base rotation DIRECTLY damps the joint at every nonzero base frequency, leaving only the m=0
    fiber column W(0,s) -- which is the pure parity balance.
  - BUILD next: pin which regime holds (factorization vs base-dominated), then attack only the residual
    m=0 fiber column W(0,s) with the renewal / Korobov tools, using the base structure to have removed all
    m!=0 contributions. The provable base has organized the joint; the residue is the focused target.""")
