# A0 [PROVEN, negative]: NO universal one-sided certificate proves avg jump <= 2.
# Any V>=0 on Z_2 with V(F(c')) <= V(c') - v2(3c'-1) + b (all c'), telescoped along the constructed
# avg-jump=3.1 orbit, forces b >= 3.1 > 2. So drift/Lyapunov/sub-additive/potential routes are closed;
# any proof of avg jump<=2 must inject SEED-SPECIFIC genericity. The margin only weakens the STRENGTH of
# genericity needed (one-sided moment E_mu[D]<=2 vs mu=Haar), not the requirement of orbit-specific input.
import math
def v2(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
K=9000
def ginv(D,y): return ((2**(D+1)*y+3**D-2**D)*pow(3**(D+1),-1,2**K))%2**K
def bD(j): return int(math.log(1-(pow(3,7*j+1,2**53))/2**53)/math.log(0.75))
itin=[bD(j) for j in range(1800)]; y=0
for D in reversed(itin): y=ginv(D,y)
xj=y; prec=K; Ds=[]
for j in range(1800):
    if prec<80: break
    D=v2(3*xj-1); Ds.append(D); xj=((3**(D+1)*xj-3**D+2**D)//2**(D+1))%(2**(prec-(D+1))); prec-=(D+1)
J=len(Ds)
print(f"witness Z_2 orbit: avg jump = {sum(Ds)/J:.3f} > 2  => any universal drift needs b >= {sum(Ds)/J:.2f} > 2.")
print("LEMMA: no universal one-sided (drift/Lyapunov/sub-additive) certificate proves avg jump<=2.")
print("Refined A0 question: is the WEAK one-sided moment bound E_{mu_J}[D]<=2 provable for seed 8")
print("when full equidistribution mu_J->Haar is not?  (Both need orbit-specific input; margin only weakens it.)")
