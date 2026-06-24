import numpy as np, math, cmath
N=100000
c=8; cs=[]
for n in range(N): cs.append(c); c=3*c//2
def v2(x):
    if x==0: return 99
    r=0
    while x&1==0: x>>=1; r+=1
    return r
dep=np.array([v2(cs[n]-1) if cs[n]>1 else 0 for n in range(N)])

# ===== (1) LARGE SIEVE: separation of linear form vs nonlinear orbit =====
print("(1) SEPARATION (large-sieve viability): min gap of points in [0,1)")
# nonlinear orbit points {(3/2)^n}
frac32=[(pow(3,n,1<<n)>>(n-52))/(1<<52) if n>52 else pow(3,n,1<<n)/(1<<n) for n in range(1,3000)]
g_nl=min(np.diff(sorted(frac32)))
# linear form S_n mod 2^M / 2^M  (the x3-coset, fixed M)
M=20; S=0; Sm=[]
for n in range(3000):
    Sm.append((S%(1<<M))/(1<<M)); S=3*S+(1<<n)*(cs[n]&1) if n<60 else 3*S
g_lin=min(d for d in np.diff(sorted(Sm)) if d>0)
print(f"   nonlinear (3/2)^n : min gap = {g_nl:.2e}  (~1/N^2 = {1/3000**2:.2e}, CLUSTERED -> sieve dies)")
print(f"   linear S_n mod 2^M: min gap = {g_lin:.2e}  (uniform ~1/N = {1/3000:.2e}? => well-separated -> sieve lives)")

# 2nd moment of the linear form over t (large-sieve quantity): sum_t |sum_n e(t S_n/2^M)|^2 / (#t * N)
M=14; S=0; Sm=[]
for n in range(N):
    Sm.append(S%(1<<M)); S=3*S+(1<<n)*(cs[n]&1) if n<60 else 3*S
Sm=np.array(Sm)
mom=0
for t in range(1,1<<M):
    val=abs(np.sum(np.exp(2j*math.pi*t*Sm/(1<<M))))**2
    mom+=val
print(f"   2nd moment (1/(2^M-1)) sum_t |sum_n e(t S_n/2^M)|^2 = {mom/((1<<M)-1):.1f}  (N={N}; ~N if well-separated)")

# ===== (2) STEWART: does depth correlate with the binary-digit-count of 3^n (Baker-accessible)? =====
print("\n(2) STEWART/BAKER: is depth_n bounded by a Baker-accessible quantity?")
# number of nonzero binary digits of 3^n (Stewart: -> infinity, unconditional lower bound)
ndig=[bin(pow(3,n)).count('1') for n in range(2,400)]
deps=dep[2:400]
corr=np.corrcoef(ndig, deps)[0,1]
print(f"   corr(depth_n, #nonzero-binary-digits(3^n)) = {corr:+.4f}")
# Stewart bounds the DIGIT COUNT (archimedean/global); depth is TRAILING zeros of c_n-1 (2-adic). Different.
print(f"   #nonzero digits of 3^n grows ~ {np.mean([ndig[i] for i in range(len(ndig))]):.0f} avg (Stewart: ->inf)")
print(f"   depth_n ~ O(log n), max={dep.max()}; these are uncorrelated ({corr:+.3f}) => Stewart (archimedean")
print(f"   digit-count) does NOT see the 2-adic trailing-zero depth. Disconnected.")
