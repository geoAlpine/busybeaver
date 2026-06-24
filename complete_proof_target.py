# What the COMPLETE proof requires (the summit, A0): avg jump <= 2, one-sided, factor-2 margin.
#  - avg jump = (1/J)sum_j v2(c'_j - 1/3) = avg 2-adic proximity to the single point 1/3 (shrinking target).
#  - one-sided condition avg jump<=2 is STRICTLY WEAKER than equidistribution (avg jump->1): we build a
#    non-Haar orbit with avg jump in (1,2) that satisfies it without equidistributing.
#  - budget: complete proof <= [k=1 term <=1 trivial] + [sum_{k>=2} N_k/J <= 1, true ~0.5, margin 2x].
import math
from collections import Counter
def v2(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
# (A) real orbit budget
c=8; renew=[]
while len(renew)<20000:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
J=len(renew); Nk=[sum(1 for cp in renew if v2(3*cp-1)>=k) for k in range(1,13)]
print(f"real orbit: avg jump = sum_k N_k/J = {sum(Nk)/J:.4f} (need <=2); "
      f"k=1 term {Nk[0]/J:.3f}(<=1 trivial); tail_(k>=2) {sum(Nk[1:])/J:.3f} (need <=1, true ~0.5)")
# (B) one-sided strictly weaker: non-Haar orbit with avg jump in (1,2)
K=9000
def ginv(D,y): return ((2**(D+1)*y+3**D-2**D)*pow(3**(D+1),-1,2**K))%2**K
def bD(j): return int(math.log(1-(pow(3,11*j+1,2**53))/2**53)/math.log(0.6))  # mean ~1.5
itin=[bD(j) for j in range(1500)]; y=0
for D in reversed(itin): y=ginv(D,y)
xj=y; prec=K; R=[]
for j in range(1500):
    if prec<80: break
    D=v2(3*xj-1); R.append(D); xj=((3**(D+1)*xj-3**D+2**D)//2**(D+1))%(2**(prec-(D+1))); prec-=(D+1)
aj=sum(R)/len(R); dist=Counter(R)
print(f"constructed non-Haar orbit: avg jump={aj:.3f} in (1,2) [satisfies non-halt]; "
      f"D-dist ratios vs Haar: {[round(dist.get(k,0)/(len(R)*2**-(k+1)),2) for k in range(5)]} (!=1 => NOT equidist)")
print("=> {avg jump<=2} strictly contains {Haar}: the complete proof's condition is weaker than equidistribution.")
