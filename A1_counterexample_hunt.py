# A1 counterexample hunt: refine the target theorem (rank-1 single-orbit equidistribution) by breaking it.
# Seeds in Z_2; iterate the renewal map F (exact affine branches); D_j=v2(3x-1). Haar: avg jump=1, P(D=0)=1/2.
# Finding: the ONLY biased seeds are eventually-periodic or singularity(1/3)-preimages; integers always -> Haar.
import math
def v2i(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
K=14000
def run(x0_mod):
    xj=x0_mod%(2**K); prec=K; R=[]
    for j in range(5000):
        if prec<80: break
        t=(3*xj-1)%(2**prec)
        if t==0: return R,"SINGULARITY"
        D=v2i(t)
        if D+1>=prec: break
        R.append(D); xj=((3**(D+1)*xj-3**D+2**D)//2**(D+1))%(2**(prec-(D+1))); prec-=(D+1)
    return R,"ok"
def period(R,maxP=40):
    if len(R)<2*maxP+50: return None
    tail=R[-(2*maxP+30):]
    for P in range(1,maxP+1):
        if all(tail[i]==tail[i+P] for i in range(len(tail)-P)): return P
    return None
if __name__=="__main__":
    nH=nP=nS=nAB=0
    for a in range(1,16):
        for b in [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33]:
            if math.gcd(a,b)!=1: continue
            R,st=run((a*pow(b,-1,2**K))%2**K)
            if st=="SINGULARITY": nS+=1; continue
            if not R: continue
            aj=sum(R)/len(R); p0=R.count(0)/len(R); P=period(R)
            isH=abs(aj-1)<0.12 and abs(p0-0.5)<0.12
            if isH and P is None: nH+=1
            elif P is not None: nP+=1
            else: nAB+=1
    print(f"rationals: ->Haar(aperiodic)={nH}  biased&periodic={nP}  singularity={nS}  APERIODIC-BIASED={nAB}")
    for s in [8,12345,7**13,10**18+7]:
        R,_=run(s%2**K); print(f"  integer {s}: avg jump={sum(R)/len(R):.3f} P(D=0)={R.count(0)/len(R):.3f}")
