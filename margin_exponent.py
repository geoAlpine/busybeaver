"""Phase 2: where does the factor-2 margin live? Decompose the avg-jump EXCESS by cylinder depth k.
avg jump = (1/J) sum_j v2(3c'_j - 1) = sum_{k>=1} N_k/J,  N_k = #{j: v2(3c'_j-1) >= k} = #{j: c'_j == 1/3 mod 2^k}.
Haar: N_k/J -> 2^-k, avg jump -> 1. Non-halt criterion: avg jump <= 2, i.e. EXCESS := avg jump - 1 = sum_k D_k <= 1,
where D_k = N_k/J - 2^-k is cylinder k's signed discrepancy. The factor-2 margin = budget 1 on sum_k D_k.

QUESTION (quantitative, tool-independent): is the margin (sum_k D_k <= 1) controlled by a FINITE set of small-k
cylinders (=> a weaker, finite-scale equidistribution input suffices, the genuine cash-out of the margin), or does
the budget draw on all scales (=> needs full equidistribution)? We measure:
 (a) per-k discrepancy D_k(J) and its decay rate in J (exponent),
 (b) the excess decomposition: how much of sum_k D_k each k contributes, and the partial sum vs tail split,
 (c) the tail sum_{k>K} N_k/J = (1/J) sum_j (v2_j - K)^+  -- the 'deep excursions' (large-k separation / Baker),
     and whether it is small WITHOUT equidistribution (a Haar-type one-sided bound) or itself needs genericity.
Honest: empirical, single orbit (seed 8); the n->inf limit is the open problem. We report localization, not a proof.
"""
import numpy as np

KMAX=24
N_REN=200000
MASK=(1<<(KMAX+2))-1     # low bits of c needed to get v2(3c'-1) up to KMAX
def v2_capped(x, cap):
    if x==0: return cap
    r=0
    while x&1==0 and r<cap: x>>=1; r+=1
    return r

c=8; vlist=[]
while len(vlist)<N_REN:
    if c&1==0:
        cp_low=(c & MASK)>>1            # c'=c//2 low bits
        vlist.append(v2_capped((3*cp_low-1) & MASK, KMAX))   # v2(3c'-1) capped
    c=(3*c)//2
v=np.array(vlist)
J=len(v)
print("="*78)
print(f"Avg-jump excess decomposition by cylinder depth  (Antihydra seed 8, J={J} renewals)")
print("="*78)
avgjump=v.mean()
print(f"avg jump = {avgjump:.5f}  (Haar 1; non-halt needs <=2; excess = {avgjump-1:+.5f}, budget 1)")

# N_k/J and D_k
Nk=np.array([ (v>=k).mean() for k in range(1,KMAX+1) ])
haar=np.array([2.0**-k for k in range(1,KMAX+1)])
Dk=Nk-haar
print(f"\n{'k':>3} {'N_k/J':>10} {'2^-k':>11} {'D_k=disc':>11} {'cum excess':>11}")
cum=0.0
for i,k in enumerate(range(1,13)):
    cum+=Dk[i]
    print(f"{k:>3} {Nk[i]:10.5f} {haar[i]:11.5f} {Dk[i]:+11.5f} {cum:+11.5f}")
print(f"... (k=13..{KMAX}): sum D_k = {Dk[12:].sum():+.6f}")
print(f"total excess sum_k D_k = {Dk.sum():+.5f}  (== avg jump - 1 = {avgjump-1:+.5f}; check)")

# tail: deep excursions sum_{k>K} N_k/J = mean of (v-K)^+
print(f"\nDeep-excursion tail  sum_{{k>K}} N_k/J = mean_j (v2_j - K)^+   (Haar value 2^-K):")
print(f"{'K':>3} {'tail (measured)':>16} {'Haar 2^-K':>11} {'ratio':>7}")
for K in (2,3,4,6,8,12):
    tail=np.maximum(v-K,0).mean()
    print(f"{K:>3} {tail:16.6f} {2.0**-K:11.6f} {tail/2.0**-K:7.2f}")

# decay of D_k in J: split J into chunks, see if D_k shrinks (equidistribution) per k
print(f"\nPer-k discrepancy |D_k| at growing prefixes J/4, J/2, J  (does it -> 0? rate):")
print(f"{'k':>3} {'|D_k|@J/4':>11} {'|D_k|@J/2':>11} {'|D_k|@J':>11} {'~exponent':>10}")
for k in (1,2,3,4,6,8):
    ds=[]
    for frac in (4,2,1):
        Jp=J//frac
        ds.append(abs((v[:Jp]>=k).mean()-2.0**-k))
    beta = (np.log(ds[0]+1e-12)-np.log(ds[2]+1e-12))/np.log(4) if ds[2]>0 else float('nan')
    print(f"{k:>3} {ds[0]:11.6f} {ds[1]:11.6f} {ds[2]:11.6f} {beta:10.3f}")

# ADVERSARIAL decomposition: where does an orbit with avg jump > 2 put its excess? i.i.d. geometric
# branch model P(D=d)=(1-q)q^d, N_k/J=q^k, excess D_k=q^k-2^-k. Real orbit=Haar q=1/2.
print(f"\nAdversarial excess decomposition (i.i.d. geometric, q=avgjump/(1+avgjump)):")
print(f"{'avgjump':>8} {'q':>6} | " + " ".join(f"k{k}" for k in range(1,7)) + " | tail k>8 | excess")
for aj in (1.0,1.5,2.0,3.1):
    q=aj/(1+aj); Dk2=[q**k-0.5**k for k in range(1,25)]
    head=" ".join(f"{Dk2[k-1]:+.2f}" for k in range(1,7))
    print(f"{aj:>8} {q:6.3f} | {head} | {sum(Dk2[8:]):+.3f}  | {sum(Dk2):+.3f}")

print("\n--- reading (VERDICT) ---")
print("REAL orbit (seed 8): avg jump 1.0036, excess +0.0036 -- localized to small k (k<=5), deep tail")
print("~Haar (ratio<=1). The D_k are at the CLT noise floor (~1/sqrt J), no extractable decay exponent.")
print("BUT the MARGIN proof must rule out ADVERSARIES: an orbit with q>1/2 has excess q^k-2^-k POSITIVE")
print("at EVERY k, decaying only like q^k, with the deep tail (k>8) contributing materially once")
print("avg jump>2. So preventing budget overflow requires controlling cylinder frequencies at ALL k,")
print("NOT just small k. VERDICT: the factor-2 margin relaxes the THRESHOLD (sum<=1 vs ->0) but the")
print("CONTROL still spans every scale -> SAME discrepancy class as equidistribution, NO weaker exponent.")
print("The real orbit's small-k-localized excess is a property of the GENERIC orbit, not of the margin")
print("requirement. (Sharpens #2 quantitatively; corrects the naive 'margin localizes to small k' hope.)")
print("Honest: single-orbit empirical + i.i.d.-adversary model; the n->inf limit is the open problem.")
