import numpy as np, math, cmath
# Evaluate the linear-form exponential sum sum_n e(t * S_n / 2^M). Does the linearity give cancellation,
# or does it inherit the moving-modulus / x3-isometry wall?
N=200000
c=8; S=0; Smod={}
Ms=[10,16,20]
for M in Ms: Smod[M]=[]
for n in range(N):
    for M in Ms: Smod[M].append(S % (1<<M))
    S=3*S+(1<<n)*(c&1) if n<60 else 3*S  # for n>=M the 2^n term vanishes mod 2^M; keep exact low part
    c=3*c//2
# NOTE: for n>=M, S_n mod 2^M = 3^{n-M} S_M mod 2^M (x3 isometry). Verify + measure cancellation.
print("(1) fixed-modulus linear form  sum_{n<=N} e(t S_n/2^M):  cancellation vs sqrt(N)?")
for M in Ms:
    sm=np.array(Smod[M],float)/(1<<M)
    for t in (1,3):
        Ssum=sum(cmath.exp(2j*math.pi*t*x) for x in sm)
        print(f"   M={M} t={t}: |sum|={abs(Ssum):9.1f}  /sqrt(N)={abs(Ssum)/math.sqrt(N):.2f}  /N={abs(Ssum)/N:.4f}")
# (2) is S_n mod 2^M eventually the x3-isometry orbit (periodic => no cancellation)?
M=16
seq=Smod[M][100:100+200]
# period of the x3 orbit of S_100 mod 2^16
x=seq[0]; per=None
for p in range(1,2*(1<<(M-2))):
    if (pow(3,p,1<<M)*seq[0])%(1<<M)==seq[0] and p>0: per=p; break
print(f"\n(2) S_n mod 2^{M} for n>=M equals 3^(n-M) S_M mod 2^M (x3 ISOMETRY). period ~ {per} (=ord(3 mod 2^M)=2^(M-2)={1<<(M-2)})")
print("=> fixed-modulus linear form = sum over a PERIODIC x3-isometry orbit => NO cancellation beyond 1 period.")
print("   The MOVING modulus 2^(n+L) (what the depth needs) re-introduces the original problem.")
print("   => the affine/linear structure inherits the x3-isometry + moving-modulus walls. Honest check pending t-scan.")
