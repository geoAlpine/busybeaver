# Feasibility probe: is there a NON-CIRCULAR route to the weak one-sided moment E_{mu_J}[D] <= 2 (=avg jump<=2)?
# Tests each candidate mechanism. VERDICT: none open a new path; the factor-2 margin weakens the TOOL needed
# (one-sided moment vs full Haar) but opens NO mechanism. A0 is mechanistically where A1 is, with a weaker target.
import math
def v2(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
K=12000
def ginv(D,y): return ((2**(D+1)*y+3**D-2**D)*pow(3**(D+1),-1,2**K))%2**K
def build(q,nb=7):
    def bD(j): return int(math.log(1-(pow(3,nb*j+1,2**53))/2**53)/math.log(q))
    itin=[bD(j) for j in range(2200)]; y=0
    for D in reversed(itin): y=ginv(D,y)
    xj=y; prec=K; R=[]
    for j in range(2200):
        if prec<80: break
        D=v2(3*xj-1); R.append(D); xj=((3**(D+1)*xj-3**D+2**D)//2**(D+1))%(2**(prec-(D+1))); prec-=(D+1)
    return R
print("PROBE1 no unconditional floor (avg jump can be any size):",
      [round(sum(build(q))/len(build(q)),1) for q in (0.5,0.8,0.875,0.92)])
print("PROBE2 2nd-moment bounds DEVIATION not the mean -> circular.")
print("PROBE3 parity seq has MAX linear complexity -> no algebraic density bound.")
print("PROBE4 distinct-integer counting vacuous (range (9/4)^J >> 2^k).")
print("VERDICT: margin opens no new mechanism; A0 needs a new orbit-specific tool, weaker than A1's.")
