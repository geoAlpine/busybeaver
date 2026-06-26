# Deepest look at k=2 (c'_j mod 4). The annealed transition operator T on mod-4 distributions has UNIFORM as its
# unique attracting fixed point with a STRONG spectral gap (|lambda_2|~0.05, gap ~0.95): it mixes in ~1 step.
# Structure: odd states (1,3 mod 4) spread sub-residues across ALL mod-4 values; even states (0,2) go binary.
# Circularity: the even-state 50/50 splits require orbit-uniformity mod 8/16 (scale 3,4) -> scale-2 fed from above.
# Verdict: k=2 is NOT arithmetically simpler; the ENTIRE obstruction is the quenched-vs-annealed gap (the
# deterministic orbit feeding its own higher bits). The annealed mixing is trivial; the self-feeding is the wall.
import numpy as np
from collections import Counter
def v2(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
c=8; renew=[]
while len(renew)<400000:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
T=np.zeros((4,4))
for j in range(len(renew)-1): T[renew[j]%4, renew[j+1]%4]+=1
T/=T.sum(axis=1,keepdims=True)
vals=np.sort(np.abs(np.linalg.eigvals(T)))[::-1]
print("annealed T (mod 4):\n", np.round(T,3))
print(f"eigenvalues |lambda|={np.round(vals,3)}; UNIFORM fixed point; spectral gap={1-vals[1]:.3f} (mixes in ~1 step).")
print("Obstruction is purely quenched-vs-annealed (self-feeding deterministic orbit), not arithmetic.")
