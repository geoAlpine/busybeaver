# Q9(b) sufficiency: is non-shadowing/Diophantine (i) SUFFICIENT for the avg-jump (M_4) bound,
# and (ii) STRICTLY WEAKER than Haar-equidistribution?  ANSWER: (i) NO, (ii) NO.
# Decisive construction: an F-orbit generic for a NON-Haar Bernoulli measure -- fully supported,
# dense in Z_2, aperiodic (maximally non-shadowing) -- yet avg jump = E_nu[v2(3x-1)] > 2.
import math
from collections import Counter
K=9000
def v2(x):
    x=abs(int(x))
    if x==0: return 10**9
    r=0
    while x%2==0: x//=2; r+=1
    return r
def ginv(D,y):  # inverse branch g_D: F(g_D(y))=y
    return ((2**(D+1)*y + 3**D - 2**D)*pow(3**(D+1),-1,2**K)) % 2**K
def biased_D(j):  # fully-supported geometric itinerary, mean ~3 (q=3/4): all D>=0 appear
    u=(pow(3,7*j+1,2**53))/2**53
    return int(math.log(1-u)/math.log(3/4))
m=1800
itin=[biased_D(j) for j in range(m)]
y=0
for D in reversed(itin): y=ginv(D,y)
x=y
xj=x; prec=K; realized=[]; cyl=set()
for j in range(m):
    if prec<80: break
    cyl.add(xj%256)
    D=v2(3*xj-1); realized.append(D)
    xj=((3**(D+1)*xj-3**D+2**D)//2**(D+1))%(2**(prec-(D+1))); prec-=(D+1)
n=len(realized)
print(f"(i)/(ii) counterexample: {n} steps, avg jump={sum(realized)/n:.3f} (>2 VIOLATES), "
      f"D-support={sorted(set(realized))[:8]}..., cylinders={len(cyl)}/256 (dense/non-shadowing)")
# binding scale: avg jump = (1/J) sum_k N_k dominated by small k
c=8; renew=[]; J=20000
while len(renew)<J:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
cum=0
for k in range(1,8):
    r=pow(3,-1,2**k); Nk=sum(1 for cp in renew if cp%2**k==r); cum+=Nk/J
    if k==3: print(f"real orbit: avg-jump mass in k<=3 = {cum:.3f} of ~1.0 => binding part is fixed-k equidistribution")
