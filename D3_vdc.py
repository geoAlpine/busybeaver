import numpy as np, math
# Test van der Corput on the parity sum Sigma_n (-1)^{e_n}. vdC: |S|^2 <= N + 2 sum_k |A_k|,
# A_k = sum_n (-1)^{e_n + e_{n+k}} = the lag-k autocorrelation (x N). Does differencing DECAY, or reduce
# to the autocorrelation wall? Also test the linear depth-congruence object.
N=300000
c=8; e=np.zeros(N,dtype=np.int8)
for n in range(N): e[n]=c&1; c=3*c//2
chi=1-2*e.astype(float)   # (-1)^{e_n}
S=chi.sum()
print(f"raw parity sum |Sigma (-1)^e_n| = {abs(S):.1f}  /sqrt(N)={abs(S)/math.sqrt(N):.2f}  (sqrt-cancellation already!)")
print("\nvdC differenced terms A_k/N = lag-k autocorrelation (these must be o(1) for vdC to close):")
for k in [1,2,3,5,10,20,50]:
    Ak=np.mean(chi[:-k]*chi[k:])
    print(f"  k={k:3d}: A_k/N = {Ak:+.5f}")
print("\n=> the parity ALREADY has sqrt-cancellation; vdC needs the autocorrelations A_k to be provably o(1).")
print("   They ARE ~0 empirically, but proving sum_k A_k = o(N) IS the equidistribution (the wall).")

# KEY NEW TEST: is there a LINEAR identity making A_k computable from the coefficient structure?
# e_n e_{n+k} correlation -- e_n is nonlinear (bit extraction), so A_k is NOT a clean linear object.
# Test the genuinely-linear surrogate: the depth-indicator correlation, which IS a linear congruence event.
def v2(x):
    if x==0: return 99
    r=0
    while x&1==0: x>>=1; r+=1
    return r
c=8; cs=[]
for n in range(50000): cs.append(c); c=3*c//2
dep=np.array([v2(cs[n]-1) if cs[n]>1 else 0 for n in range(len(cs))])
print("\ndepth-indicator [depth>=L] density (should be ~2^-L if geometric/equidistributed):")
for L in range(1,9):
    d=np.mean(dep>=L)
    print(f"  L={L}: P(depth>=L)={d:.4f}  2^-L={2.0**-L:.4f}  ratio={d/2.0**-L:.3f}")
print("=> depth tail is geometric to high precision; PROVING P(depth>=L)<=C 2^-L unconditionally = M2 target.")
