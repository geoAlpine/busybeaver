# Effective top-digit equidistribution of c_n=floor(8(3/2)^n), quantified by the CF of alpha=log2(3/2).
# (a) discrepancy at convergent denominators q_m ~ 1/q_m => top log2(N)-O(loglogN) bits equidistribute.
# (b) direct top-k-bit histogram of c_n is uniform up to k ~ log2 N. (c) barrier: parity bit = bit_{n+3}(3^n),
# the diagonal, Theta(n) from both the top (Weyl) and bottom (x3 coset) footholds.
import mpmath as mp, math
from collections import Counter
mp.mp.dps=200
alpha=mp.log(3,2)-1
A=[]; x=alpha
for _ in range(30):
    ai=int(mp.floor(x)); A.append(ai)
    if x==ai: break
    x=1/(x-ai)
p,q=[0,1],[1,0]
for ai in A: p.append(ai*p[-1]+p[-2]); q.append(ai*q[-1]+q[-2])
qs=[v for v in q[2:] if v>1]
af=alpha
def disc(N):
    pts=sorted(float((n*af)%1) for n in range(1,N+1)); D=0.0
    for i,xp in enumerate(pts): D=max(D,abs((i+1)/N-xp),abs(i/N-xp))
    return D
print("discrepancy at CF convergents N=q_m (should be ~1/N => -log2 D ~ log2 N):")
for N in qs:
    if N>40000: break
    if N<5: continue
    D=disc(N); print(f"  q_m={N:>6}: -log2 D*={-math.log2(D):6.3f}  log2 N={math.log2(N):6.3f}  k/log2N={-math.log2(D)/math.log2(N):.3f}")
N=20000; l32=mp.log(3,2)
mant=[float((mp.mpf(3)+n*(l32-1))%1) for n in range(1,N+1)]
print("top-k-bit histogram of c_n (n<=20000), max|freq-2^-k|/2^-k:")
for k in (4,8,12,14):
    cnt=Counter(int(m*2**k)%2**k for m in mant)
    md=max(abs(cnt.get(r,0)/N-2.0**-k) for r in range(2**k))
    print(f"  k={k:2d}: {md/2.0**-k:.3f}")
print("barrier: parity bit = bit_{n+3}(3^n) = diagonal of ~1.585n-bit 3^n; both footholds reach Theta(log N) only.")
