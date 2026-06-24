import numpy as np
from collections import Counter
def v3(x):
    if x==0: return 99
    r=0
    while x%3==0: x//=3; r+=1
    return r
# Port: o18 step map ~ T3(N)=floor(8N/3) = (x8 isometry on Z3) o (÷3 = 3-adic shift, MIXING).
# (I) measure-preserving 3-to-1 exact endomorphism of Z_3?
for k in (5,):
    K=3**k; pre=[0]*K
    for x in range(3*K):
        y=(8*x)//3 % K
        pre[y]+=1
    print(f"T3=floor(8N/3) on Z/3^{k}: preimage counts min={min(pre)} max={max(pre)} (exactly 3 => measure-preserving 3-to-1)")
# (II) low-3-adic-digit Markov chain: state N mod 3^k, incoming high base-3 digit (0,1,2) uniform.
def gap_and_stat(k=5, weights=(1/3,1/3,1/3)):
    K=3**k; P=np.zeros((K,K))
    for s in range(K):
        for hd in (0,1,2):
            N=s+hd*K; t=(8*N)//3 % K
            P[s,t]+=weights[hd]
    ev=sorted(np.linalg.eigvals(P.T),key=lambda z:-abs(z))
    w,v=np.linalg.eig(P.T); i=np.argmin(np.abs(w-1)); stat=np.real(v[:,i]); stat/=stat.sum()
    return 1-abs(ev[1]), stat
gap,stat=gap_and_stat()
print(f"3-adic low-digit Markov chain spectral gap = {gap:.4f} (mixing like Antihydra's 0.99?)")
print(f"stationary uniform? min={stat.min():.6f} max={stat.max():.6f} (uniform=1/{3**5}={1/3**5:.6f})")
# (III) MARGIN: o18's halt needs a base-3 carry NOT to align. The relevant digit-density vs threshold.
# digit delta_n = floor((8/3)^n) mod 3 -> uniform 1/3 each. Compare to the Antihydra margin (1/2 vs 1/3).
# For o18 the halt-relevant event is the carry/defect; measure its renewal-jump analogue.
# depth_3(N) = v3 of (relevant trap). Compute the actual o18 epoch orbit and its 3-adic depth structure.
N=10; orbit=[N]
for _ in range(60): N=(8*N)//3+2; orbit.append(N)
# 3-adic depth = v3(N - fixedpt)? find the o18 trap residue. The map fixed pt: N=8N/3+2 -> N=-6. trap N≡-6?
deps=[v3(N+6) for N in orbit]   # distance from fixed point -6 in 3-adics
print(f"\no18 orbit 3-adic depth v3(N+6) (renewal countdown?): {deps[:25]}")
# jump heights and average
jumps=[d for d in deps if d>0]
print(f"o18 nonzero 3-adic depths: mean={np.mean(deps):.3f}  max={max(deps)}")
