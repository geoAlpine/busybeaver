# 2-adic valuation budget identity: sum_{odd i<n} v2(3c_i-1) = n + v2(c_n) - v2(c_0). Verified to n=1e5.
# => odd-density = 1/avgD_odd (asymp); non-halt <=> avgD_odd >= 3/2 (Haar 2). Unconditional range [n,1.585n].
import math
def v2(x):
    x=int(x); r=0
    if x==0: return 10**9
    while x&1==0: x>>=1; r+=1
    return r
c0=8; c=c0; S_odd=0; E=0; O=0; ok=True
for n in range(1,100001):
    if c&1==0: E+=1
    else: O+=1; S_odd += v2(3*c-1)
    c=(3*c)//2
    if n in (10,100,1000,10000,100000):
        rhs=v2(c)-v2(c0)+n; ok&=(S_odd==rhs)
        print(f"n={n:>6}  sum_odd D={S_odd:>6}  =n+v2(cn)-v2(c0)={rhs:>6}  ok={S_odd==rhs}  "
              f"avgD_odd={S_odd/O:.4f}  even-dens={E/n:.4f}  (non-halt <=> avgD_odd>=1.5)")
print(f"identity verified: {ok};  unconditional range  n-v2(c0) <= sum_odd D <= {1+math.log2(1.5):.4f}n-v2(c0)")
