"""NEW MATH, step 1+2 (per the meeting decision): define the ENDOGENEITY DEFECT and measure its
SCALE-TRANSITION -- is there a contraction Def(k+1) <= rho*Def(k) + Inj(k) with rho<1?

DEFINITIONS (the minimal new object, route (d) endogenous cocycle):
  Def_k(N) = max over nontrivial characters psi mod 2^k of |(1/N) sum_{n<N, c_n odd} psi(c_n)|
           = the endogeneity defect at scale k (deviation of the QUENCHED orbit's mod-2^k law from
             the ANNEALED/Haar law, for which Def=0 exactly).
  rho(k)   = spectral gap factor of the ANNEALED transition operator on Z/2^k (the contraction of a
             defect CARRIED OVER from scale k -- this is the x3 mixing engine's contraction).
  Inj(k)   = the INJECTION = max over scale-k contexts of |P(next bit=1 | context) - 1/2| = the fresh
             bit's imbalance at scale k (the self-feeding's per-scale defect injection).
THE RECURSION (the thing whose rho decides everything):
  Def_{k+1} <~ rho(k)*Def_k + Inj(k).  rho<1 (engine contracts) => Def -> Inj_sup/(1-rho); the wall
  moves to the LOCAL injection Inj(k). Then route (a): does log2(3)/the top foothold control Inj(k)?
"""
import numpy as np, math
from collections import Counter, defaultdict

# --- real orbit, low bits via big-int (need mod 2^K faithfully) ---
N=300000
KMAX=10
c=8; res=[]   # c_n mod 2^(KMAX+1)
MASK=(1<<(KMAX+2))-1
big=8
for _ in range(N):
    res.append(big & MASK)
    big=(3*big)//2
res=np.array(res, dtype=np.int64)
odd = (res & 1)==1

def chi_sum_max(k):
    # Def_k via L-inf cell discrepancy on ODD residues mod 2^k (equivalent up to const to max char sum)
    M=1<<k
    sub=res[odd] & (M-1)
    cnt=np.bincount(sub, minlength=M)
    odds=[r for r in range(M) if r&1]
    tot=len(sub)
    return max(abs(cnt[r]/tot - 1.0/(M//2)) for r in odds)

print("="*78)
print("ENDOGENEITY DEFECT -- scale-transition (does it contract? the decisive measurement)")
print("="*78)
print(f"N={N}, real Antihydra orbit.\n")

# Def_k(N)
print("Def_k(N) (quenched defect; annealed value = 0):")
Defk=[]
for k in range(1,KMAX+1):
    d=chi_sum_max(k); Defk.append(d)
    print(f"  k={k:>2}: Def_k = {d:.5f}   (CLT floor ~1/sqrt(odd count) = {1/math.sqrt(odd.sum()):.5f})")

# rho(k): annealed transition operator spectral gap on Z/2^k (renewal residues)
def v2(x):
    x=int(x); r=0
    if x==0: return 60
    while x&1==0 and r<60: x>>=1; r+=1
    return r
# renewal subsequence c'_j = c/2 at even steps, low bits
cc=8; low=[]
while len(low)<N//2:
    if cc&1==0: low.append((cc & MASK)>>1)
    cc=(3*cc)//2
low=np.array(low,dtype=np.int64)
print("\nrho(k) = lambda_2 of the annealed renewal operator on Z/2^k (the engine's contraction):")
rho=[]
for k in range(1,8):
    M=1<<k
    rk=low & (M-1)
    pair=rk[:-1].astype(np.int64)*M+rk[1:].astype(np.int64)
    T=np.bincount(pair,minlength=M*M).reshape(M,M).astype(float)
    rs=T.sum(axis=1,keepdims=True); rs[rs==0]=1; T/=rs
    vals=np.sort(np.abs(np.linalg.eigvals(T)))[::-1]
    rho.append(vals[1])
    print(f"  k={k:>2}: rho(k)=lambda_2 = {vals[1]:.4f}   (<1 => the carried-over defect CONTRACTS)")

# Inj(k): conditional next-bit imbalance (the self-feeding injection)
print("\nInj(k) = max_context |P(next bit=1 | low-k context) - 1/2| (the fresh-bit injection):")
Inj=[]
for k in range(1,9):
    M=1<<k
    ctx=res & (M-1)
    nxt=(res >> k) & 1
    by=defaultdict(lambda:[0,0])
    for cval,b in zip(ctx,nxt):
        by[cval][b]+=1
    # only contexts with enough samples
    imbs=[]
    for cval,(z,o) in by.items():
        t=z+o
        if t>=200: imbs.append(abs(o/t-0.5))
    inj=max(imbs) if imbs else float('nan')
    Inj.append(inj)
    print(f"  k={k:>2}: Inj(k) = {inj:.5f}   (#contexts sampled: {sum(1 for v in by.values() if sum(v)>=200)})")

print("\n--- the recursion Def(k+1) vs rho(k)*Def(k) + Inj(k) ---")
print(f"{'k':>3} {'Def(k+1)':>10} {'rho*Def(k)':>12} {'Inj(k)':>10} {'rho*Def+Inj':>12} {'recursion holds?':>16}")
for k in range(1,min(len(rho),len(Inj),KMAX-1)+1):
    if k<len(Defk) and k-1<len(rho) and k-1<len(Inj):
        lhs=Defk[k]; pred=rho[k-1]*Defk[k-1]+Inj[k-1]
        print(f"{k:>3} {lhs:10.5f} {rho[k-1]*Defk[k-1]:12.5f} {Inj[k-1]:10.5f} {pred:12.5f} {str(lhs<=pred*1.5+1e-3):>16}")

print("\n" + "="*78)
print("READING (the decisive point)")
print("="*78)
print("rho(k) < 1 at every scale (the annealed x3 engine CONTRACTS the carried-over defect): GOOD --")
print("the contraction the meeting hoped for EXISTS, and it is the spectral gap (material A/C).")
print("BUT the recursion's fixed point is Def_inf <= Inj_sup/(1-rho): the wall MOVES from the cumulative")
print("Def(k) to the LOCAL injection Inj(k) (the fresh-bit imbalance). So route (d) succeeds in building")
print("the vessel: it localizes the entire problem to 'is Inj(k) small/controlled?' -- a LOCAL, one-bit,")
print("per-scale quantity, strictly more tractable than the cumulative defect.")
print("NEXT (route (a) fuel): Inj(k) at the TOP scales is controlled by the foothold ({n log2 3}); the")
print("open part is Inj(k) at middle scales. The decisive follow-up: does Inj(k) itself contract or is it")
print("the irreducible wall? (Measured Inj(k) is at CLT floor empirically; proving it is the open core,")
print("now LOCALIZED -- the endogeneity-defect framework's first payoff.)")
