import math, cmath
# Weyl sum S_N(c) = sum_{n<=N} e(c*(3/2)^n). Van der Corput: differencing with lag k gives
# inner sum I_k = sum_n e(c*((3/2)^{n+k}-(3/2)^n)) = sum_n e(c*((3/2)^k -1)*(3/2)^n)
#             = S_N( c*((3/2)^k -1) )  -- SAME family, new coefficient. Test if it gains cancellation.
def frac_mul(coef, n):
    # need {coef*(3/2)^n} accurately. (3/2)^n=3^n/2^n. coef*(3/2)^n mod 1.
    # use exact: 3^n mod 2^n gives (3/2)^n frac; but coef*frac mod1 with coef real -> do via high-prec.
    r=pow(3,n,1<<n)              # 3^n mod 2^n  (exact low n bits)
    # (3/2)^n = integer + r/2^n ; fractional part = r/2^n
    # we want frac(coef * (3/2)^n). Only the fractional part of (3/2)^n matters mod 1 if coef integer;
    # but coef=(3/2)^k-1 is NOT integer -> need integer part of (3/2)^n too. Use full high precision.
    return None
# Simpler: directly compute (3/2)^n in high precision via Fraction for moderate n, take e(c*x).
from fractions import Fraction
def pow32(n): return Fraction(3,2)**n
N=8000
# precompute fractional parts as floats of (3/2)^n via exact frac r/2^n (this is {(3/2)^n})
def frac32(n):
    r=pow(3,n,1<<n)
    return (r>>(n-52))/(1<<52) if n>52 else r/(1<<n)
vals=[frac32(n) for n in range(1,N+1)]
def weyl(coef_list_phase):  # given list of phases theta_n (=coef*(3/2)^n mod1) compute |sum e|
    S=sum(cmath.exp(2j*math.pi*t) for t in coef_list_phase)
    return abs(S)
# base sum c=1
base=weyl(vals)
print(f"base |S_N(1)|={base:.2f}  /sqrt(N)={base/math.sqrt(N):.3f}")
# differenced inner sums for lags k=1..6: phase = ((3/2)^k -1)*(3/2)^n mod 1
print("van der Corput differenced inner sums I_k (should be SMALL if differencing helps):")
for k in range(1,7):
    ck=float((Fraction(3,2)**k)-1)   # coefficient
    # phase_n = frac( ck * (3/2)^n ) ; need ck*(3/2)^n mod1. ck*(3/2)^n = ck*int + ck*frac.
    # compute (3/2)^n as exact Fraction is too big; use: (3/2)^n = q_n + vals[n], q_n integer.
    # ck*(3/2)^n mod1 = frac( ck*q_n + ck*vals[n] ). ck*q_n mod1 needs q_n... q_n huge.
    # Instead compute ck*(3/2)^n mod 1 directly in float for n where (3/2)^n < 2^52 (n<~90) -- too few.
    # Use exact 2-adic: ck=(3^k-2^k)/2^k. ck*(3/2)^n = (3^k-2^k)*3^n / 2^{n+k}. frac = ((3^k-2^k)*3^n mod 2^{n+k})/2^{n+k}
    a=(3**k-2**k)
    phases=[]
    for n in range(1,N+1):
        m=n+k
        num=(a*pow(3,n,1<<m))% (1<<m)
        phases.append((num>>(m-52))/(1<<52) if m>52 else num/(1<<m))
    Ik=weyl(phases)
    print(f"  k={k}: coef=(3/2)^{k}-1={ck:.4f}  |I_k|={Ik:8.2f}  /sqrt(N)={Ik/math.sqrt(N):.3f}")
print("\n=> if |I_k|/sqrt(N) ~ O(1) like the base, differencing yields NO gain (family is closed).")
