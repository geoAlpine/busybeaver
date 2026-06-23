import numpy as np
from collections import Counter
# Verify the mixing model against the REAL Antihydra orbit, and test if the incoming-bit assumption
# is robust (the bits the orbit reads in are actually ~uniform/decorrelated => bootstrapping is real).
N=400000
c=8
cmodk={k:[] for k in (4,6,8)}
incoming=[]   # the bit shifted in each step = bit that becomes relevant; track bit at position 8
parity=[]
for n in range(N):
    parity.append(c&1)
    for k in cmodk: cmodk[k].append(c & ((1<<k)-1))
    incoming.append((c>>8)&1)   # a 'high' bit that will shift down
    c=3*c//2

# 1) real c_n mod 2^k equidistribution (chi-square vs uniform)
print("real orbit c_n mod 2^k vs uniform:")
for k in (4,6,8):
    cnt=Counter(cmodk[k]); K=1<<k
    exp=N/K
    chi=sum((cnt[r]-exp)**2/exp for r in range(K))
    print(f"  k={k}: chi^2/dof = {chi/(K-1):.3f} (->1 if uniform); distinct states {len(cnt)}/{K}")

# 2) the incoming high-bit sequence: is it balanced & decorrelated (=> 'uniform incoming' justified)?
m=sum(incoming)/N
cc=[x-m for x in incoming]
den=sum(x*x for x in cc)
print(f"\nincoming high-bit: balance={m:.4f} (->0.5)")
for lag in (1,2,3,5,10):
    ac=sum(cc[i]*cc[i+lag] for i in range(N-lag))/den
    print(f"  autocorr lag {lag}: {ac:+.4f}")

# 3) does even-density of the REAL orbit match the model's stationary 1/2, with fast convergence?
ev=np.cumsum([1-p for p in parity])/np.arange(1,N+1)
print(f"\nreal even-density at n=1e3,1e4,1e5,4e5: {[round(ev[j],4) for j in (1000,10000,100000,N-1)]}")

# 4) KEY robustness check: depth_n = v2(c_n - 1) = current odd-run; does max grow like log2(n) (=o(n))?
c=8; depth=[]; 
def v2(x):
    if x==0: return 99
    r=0
    while x&1==0: x>>=1; r+=1
    return r
maxd=[]; cur=0
c=8
for n in range(N):
    d=v2(c-1) if c>1 else 0
    cur=max(cur,d); 
    if n in (1000,10000,100000,N-1): maxd.append((n,cur))
    c=3*c//2
print(f"max depth_n up to n: {maxd}  (log2(n): {[round(np.log2(x[0]),1) for x in maxd]})")
print("=> if max-depth ~ log2(n), depth=o(n) => Antihydra NON-HALTS (the exact condition).")
