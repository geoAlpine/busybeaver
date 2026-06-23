import numpy as np
from collections import defaultdict
# depth d_n = v2(c_n - 1). Re-analysis: is there a NEGATIVE DRIFT E[d_{n+1}-d_n | d_n=d] < 0 for d>=1?
# A uniform negative drift => supermartingale => exponential tail on d => max d = O(log n) = o(n) => PROOF.
def v2(x):
    if x==0: return 60
    r=0
    while x&1==0: x>>=1; r+=1
    return r
N=2_000_000
c=8
ds=[]
for n in range(N):
    ds.append(v2(c-1) if c!=1 else 60)
    c=3*c//2
ds=np.array(ds)
# drift by current depth
drift=defaultdict(list)
for n in range(N-1):
    drift[ds[n]].append(ds[n+1]-ds[n])
print("depth d -> E[delta depth], count, P(stay/increase):")
for d in range(0,12):
    if d in drift and len(drift[d])>50:
        a=np.array(drift[d])
        print(f"  d={d:2d}: E[Δd]={a.mean():+.4f}  n={len(a):8d}  P(Δd>=0)={np.mean(a>=0):.3f}")
# Also: the TAIL of d. P(d>=k) -- geometric?
print("\nP(depth >= k):")
for k in range(0,15):
    print(f"  k={k:2d}: P(d>=k)={np.mean(ds>=k):.5f}  (geometric 2^-k={2.0**-k:.5f})")
# KEY: is the depth a supermartingale (drift<0) ONLY in aggregate, or conditionally for each d?
# If E[Δd|d]<0 for all d>=1 with a uniform bound, Foster-Lyapunov gives the result.
overall=np.mean(ds[1:]-ds[:-1])
print(f"\noverall mean drift (should be ~0 since d bounded): {overall:+.5f}")
# conditional drift for d>=1:
mask=ds[:-1]>=1
print(f"conditional drift E[Δd | d>=1] = {np.mean((ds[1:]-ds[:-1])[mask]):+.4f}  (negative => mean-reverting)")
