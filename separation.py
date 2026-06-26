"""Phase 2 PIVOT (non-circular, Diophantine): the orbit's self-separation v2(c'_i - c'_j).
The margin needs one-sided control of deep-branch frequency N_k = #{j: c'_j == 1/3 mod 2^k}. Two
renewal terms in the same deep cylinder collide: c'_i == c'_j mod 2^k <=> v2(c'_i - c'_j) >= k. So
N_k large <=> many deep self-collisions. EXPERT_ASK Q2 asks whether p-adic Baker (linear forms in
2-adic logs) gives an UNCONDITIONAL lower bound on v2(c'_i - c'_j) (=> separation => N_k bound).
This is the one route to an UNCONDITIONAL partial (everything else is conditional/characterization).

Two concrete questions, both computable:
 (Q-sep) Does the orbit separate BETTER than random? Count pairs with v2(c'_i-c'_j) >= k vs the
         random/Haar expectation ~ C(J,2)*2^-k. Max collision depth vs log2(J) (birthday scale).
 (Q-baker) Does Baker even APPLY? Baker bounds v2 of linear forms in FIXED S-units (2^a 3^b). The
         orbit c'_j = floor(A (3/2)^{2j}) -- the FLOOR makes it NOT a pure S-unit. Test how close
         c'_i - c'_j is to an S-unit combination 2^a 3^b - 2^c 3^d, i.e. whether the floor error
         destroys the algebraic structure Baker needs. If destroyed -> Baker inapplicable (the
         precise gap); if preserved -> a real unconditional handle.
Honest: empirical reconnaissance to locate the gap, not a theorem.
"""
import numpy as np
from math import log2, gcd

# generate renewal subsequence low bits (mod 2^K) cheaply, AND keep small exact c'_j for S-unit test
K=40
MASK=(1<<(K+1))-1
N_REN=4000
c=8; low=[]; exact=[]
while len(low)<N_REN:
    if c&1==0:
        low.append((c & MASK)>>1)        # c'=c//2 mod 2^K
        if len(exact)<400: exact.append(c>>1)   # first 400 exact c'_j (big ints) for structure test
    c=(3*c)//2
low=np.array(low, dtype=object)
J=len(low)

def v2(x):
    x=int(x)
    if x==0: return K+1
    r=0
    while x&1==0 and r<=K: x>>=1; r+=1
    return r

print("="*78)
print(f"Orbit self-separation v2(c'_i - c'_j)   (Antihydra, J={J} renewal terms, residues mod 2^{K})")
print("="*78)

# (Q-sep) collision-depth histogram vs random expectation
# sample pairs (full J^2 too big; sample many random pairs)
rng=np.random.default_rng(0)
NP=400000
ii=rng.integers(0,J,NP); jj=rng.integers(0,J,NP)
mask=ii!=jj; ii=ii[mask]; jj=jj[mask]
depths=np.array([v2((low[a]-low[b]) & MASK) for a,b in zip(ii,jj)])
print(f"\nPair collision depth v2(c'_i-c'_j) over {len(depths)} random pairs:")
print(f"{'k':>3} {'P(depth>=k) obs':>16} {'random 2^-k':>12} {'ratio':>7}")
for k in range(1,12):
    obs=(depths>=k).mean()
    print(f"{k:>3} {obs:16.5f} {2.0**-k:12.5f} {obs/2.0**-k:7.2f}")
print(f"max collision depth in sample = {depths.max()}  (random birthday scale ~ log2(#pairs) = {log2(len(depths)):.1f};")
print(f" full-orbit max expected ~ log2(C(J,2)) = {log2(J*(J-1)/2):.1f})")

# (Q-baker) RIGOROUS structure: the DIRECT orbit c_n=floor(3c_{n-1}/2) satisfies, with parity bits
# r_i = (3 c_i) mod 2 in {0,1},   c_n = (3^n c_0 - T_n)/2^n,   T_n = sum_{i<n} 3^{n-1-i} 2^i r_i.
# T_n is the dual carry (Prop 4); it depends on the WHOLE parity history. Verify the identity, then
# show height(T_n) ~ n*log2(3) grows LINEARLY -> c_n is NOT a bounded-height S-unit -> Baker (which
# bounds v2 of linear forms in a FIXED finite set of algebraic numbers) cannot apply to c_i - c_j.
print("\n(Q-baker) RIGOROUS: c_n = (3^n c_0 - T_n)/2^n, T_n = sum_{i<n} 3^{n-1-i} 2^i r_i (dual carry).")
c0=8; cc=c0; T=0; ok=True
print(f"{'n':>4} {'c_n bits':>9} {'T_n bits':>9} {'identity holds':>15} {'height(T_n)/n':>14}")
for n in range(1,601):
    r=(3*cc)%2
    T=3*T+ (2**(n-1))*r           # T_n = 3*T_{n-1} + 2^{n-1} r_{n-1}
    cc=(3*cc)//2
    if n in (1,5,10,50,100,300,600):
        lhs=cc*(2**n); rhs=3**n*c0 - T
        holds=(lhs==rhs); ok&=holds
        print(f"{n:>4} {cc.bit_length():>9} {T.bit_length():>9} {str(holds):>15} {T.bit_length()/n:14.3f}")
print(f"identity verified on all checkpoints: {ok}")
print("height(T_n) ~ n*log2(3) = 1.585n : LINEARLY GROWING, unbounded.")
print("=> c_n (hence c_i - c_j) is a nested-floor value of UNBOUNDED height, NOT a 2^a 3^b S-unit of")
print("   bounded height. p-adic Baker / linear-forms-in-logs bounds v2(2^a 3^b - 2^c 3^d) only for a")
print("   FIXED finite set of algebraic numbers; here the 'numbers' are the T_n, whose height grows")
print("   with n. Baker is therefore INAPPLICABLE at the source -- structurally, not for lack of effort.")

print("\n--- reading ---")
print("Q-sep: if obs ratio ~1 at all k and max depth ~ birthday scale, the orbit separates exactly")
print("  like random -- NO better-than-random separation to exploit (consistent w/ i.i.d.-likeness).")
print("Q-baker: p-adic Baker bounds v2(2^a 3^b - 2^c 3^d) for FIXED exponent S-units. The orbit's")
print("  nested floors make c'_i - c'_j NOT such a form -> Baker does not apply directly. THIS is the")
print("  precise gap: the unconditional Diophantine tool needs algebraic (S-unit) inputs, but the")
print("  floor map destroys the S-unit structure each step. So Q2's 'unconditional separation via")
print("  Baker' is blocked at the source -- the orbit is arithmetic but not algebraic-of-bounded-height.")
