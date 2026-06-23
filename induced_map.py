import numpy as np
from collections import Counter, defaultdict
def v2(x):
    if x==0: return 99
    r=0
    while x&1==0: x>>=1; r+=1
    return r
# Derived induced first-return-to-even map on c' (where even orbit value = 2c'):
#   D=v2(3c'-1), u=(3c'-1)/2^D (odd),  F(c') = (3^D*u + 1)//2 ;  jump height = D.
def F(cp):
    x=3*cp-1; D=v2(x); u=x>>D
    return (pow(3,D)*u + 1)//2, D
# 1) VERIFY F reproduces the even-subsequence of the real orbit (c_n even -> c'=c_n/2)
c=8; evens=[]
for n in range(2000):
    if c%2==0: evens.append(c//2)
    c=3*c//2
cp=evens[0]; ok=True
for j in range(len(evens)-1):
    nxt,D=F(cp)
    if nxt!=evens[j+1]: ok=False; break
    cp=nxt
print("induced map F reproduces real even-subsequence:", ok)

# 2) jump-height statistics along the REAL induced orbit
cp=evens[0]; Ds=[]
for _ in range(300000):
    cp,D=F(cp); Ds.append(D)
Ds=np.array(Ds)
print(f"\nreal jump heights D_j: mean={Ds.mean():.4f} (need <2; geometric mean=1)  max={Ds.max()}")
print(f"  P(D>=k): {[round(np.mean(Ds>=k),4) for k in range(0,8)]} (geometric 2^-k: {[round(2.0**-k,4) for k in range(8)]})")

# 3) Is F measure-preserving on Z/2^k? (each target exactly 2^? preimages)
for k in (6,8):
    K=1<<k; cnt=Counter()
    for cp in range(1,4*K,2):  # odd c' representatives (c' parity matters); sample residues
        nxt,_=F(cp); cnt[nxt%K]+=1
    vals=list(cnt.values())
    print(f"F on Z/2^{k}: target-hit counts min={min(vals)} max={max(vals)} (uniform => measure-preserving)")

# 4) DRIFT / Lyapunov hunt: is there negative drift in log2(c') or a supermartingale bounding jumps?
cp=evens[0]; lg=[]; 
import math
for _ in range(100000):
    lg.append(math.log2(cp)); cp,D=F(cp)
lg=np.array(lg); dl=np.diff(lg)
print(f"\nlog2(c') drift per induced step: mean={dl.mean():+.4f} (growth rate of even-subsequence)")
# correlation between jump height D_j and next: is D_j predictable / bounded by a function of c' mod small?
cp=evens[0]; pairs=[]
for _ in range(200000):
    Dprev=v2(3*cp-1); cp,_=F(cp); pairs.append((Dprev, v2(3*cp-1)))
import numpy as np
a=np.array(pairs)
print(f"autocorr of consecutive jump heights D_j,D_{{j+1}}: {np.corrcoef(a[:,0],a[:,1])[0,1]:+.4f} (0 => independent)")
