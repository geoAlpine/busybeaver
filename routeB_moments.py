import numpy as np
from collections import Counter
# THE LEAD: bound #{c'_j ≡ 3^-1 mod 2^k} via MOMENTS of the c'_j-distribution mod 2^k (additive energy),
# which Markov (1st moment) cannot. Cauchy-Schwarz: count_r <= sqrt(2nd moment). Higher moments -> tighter.
Nsteps=8000
c=8; cps=[]
for n in range(Nsteps):
    if c%2==0: cps.append(c//2)
    c=3*c//2
J=len(cps)
# even-density bound from m-th moment: count_r <= (M_{2m})^{1/2m}; avg D <= sum_k (count bound)/J.
print(f"J={J}.  Implied even-density lower bound from moment method (IF the moment is ~random):")
for m in (1,2,3,4):  # use 2m-th moment
    # 2m-th moment M = sum_r count_r^{2m}; bound count_r <= M^{1/2m}; need M ~ J^{2m}/2^{(2m-1)k} (random)
    # avg D <= sum_{k>=1} (M_k)^{1/2m}/J ; with random M_k => sum_k 2^{-k(2m-1)/2m}
    avgD_bound=sum(2.0**(-k*(2*m-1)/(2*m)) for k in range(1,200))
    ed=1/(1+avgD_bound)
    print(f"  moment 2m={2*m}: avg-jump bound = sum_k 2^(-k*(2m-1)/2m) = {avgD_bound:.4f} => even-density >= {ed:.4f}  {'> 1/3 !!' if ed>1/3 else '(< 1/3)'}")
print()
# VERIFY the moments ARE ~random empirically (so the bound is achievable IF provable):
print("empirical 2m-th moments M_k=sum_r count_r^{2m} vs random, mod 2^k:")
for k in (8,10):
    mod=1<<k; res=[cp%mod for cp in cps]; h=Counter(res)
    counts=np.array(list(h.values())+[0]*(mod-len(h)))
    for m in (1,2,3):
        M=np.sum(counts.astype(float)**(2*m))
        # random model: count_r ~ Binom(J,1/2^k); E[count^{2m}] ~ (J/2^k)^{2m} for J/2^k>1, sum over 2^k residues
        lam=J/mod
        import math
        # crude: for Poisson(lam), E[X^{2m}] ~ Bell-ish; just report ratio to (lam^{2m})*2^k for large lam
        print(f"    k={k} 2m={2*m}: M={M:.3e}  (J/2^k={lam:.2f}; max count={counts.max()}, count^{2*m} bound -> count<=M^(1/2m)={M**(1/(2*m)):.1f}, vs J/2^k={lam:.1f})")
print("\n=> THE ROUTE: prove the additive energy / higher moments of (c'_j mod 2^k) are ~random (O(J^{2m}/2^{(2m-1)k}))")
print("   unconditionally. Then moment method => even-density > 1/3 (needs ~4th moment) => NON-HALT.")
print("   2nd moment alone gives ~0.293 (near-miss); 4th+ moment crosses 1/3. This is ADDITIVE COMBINATORICS")
print("   on the induced orbit (S-unit-like differences c'_i - c'_j; p-adic Baker may bound v2 of differences).")
