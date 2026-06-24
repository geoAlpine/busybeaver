# Q9(b): can the Gibbs-Markov spectral gap (a property of (F,Haar) ALONE) imply the
# single-orbit visit-count / M_4 bound?  ANSWER: NO -- provable obstruction.
#  (1) The transfer operator L and its spectral gap depend only on (F,Haar): orbit-blind.
#  (2) F has a fixed point x_D=(3^D-2^D)/(3^{D+1}-2^{D+1}) in Z_2 on EVERY branch D (exact).
#      A constant orbit visits 1 cylinder => M_4=J^4 >> J^4/2^{3k}=random: the bound FAILS.
#  (3) Integer seeds that 2-adically shadow a fixed point over-concentrate for a whole
#      window (verified ~7000x below). So the M_4 bound is orbit-specific; an orbit-blind
#      gap cannot imply it. Residual input needed = a non-shadowing/Diophantine property
#      of the seed (seed 6 non-exceptional) -- the single-orbit wall, precisely relocated.
from fractions import Fraction as Fr
from collections import Counter
def v2(x):
    x=abs(int(x))
    if x==0: return 999
    r=0
    while x%2==0: x//=2; r+=1
    return r
def F(x):
    D=v2(3*x-1); num=3**(D+1)*x-3**D+2**D
    assert num%2**(D+1)==0; return num//2**(D+1)
# (2) fixed points, exact
def v2f(q):
    return v2(q.numerator)-v2(q.denominator)
print("Fixed points of F (one per branch), exact:")
for D in range(6):
    x=(Fr(3)**D-Fr(2)**D)/(Fr(3)**(D+1)-Fr(2)**(D+1))
    Fx=(Fr(3)**(D+1)*x-Fr(3)**D+Fr(2)**D)/Fr(2)**(D+1)
    print(f"  D={D}: x={str(x):>10} in Z2={x.denominator%2==1} v2(3x-1)={v2f(3*x-1)}(={D}) F(x)=x:{Fx==x}")
# (3) shadowing integer seed over-concentrates
x=pow(5,-1,2**60); orbit=[x]
for _ in range(200): x=F(x); orbit.append(x)
print("\nInteger seed (1/5 mod 2^60) shadows the fixed point; M_4 on the shadow window:")
for W in (20,40,80):
    cnt=Counter(o%2**10 for o in orbit[:W]); M4=sum(v**4 for v in cnt.values())
    rand=W+7*W*(W-1)/2**10+6*W*(W-1)*(W-2)/2**20+W*(W-1)*(W-2)*(W-3)/2**30
    print(f"  W={W:3d} k=10: cylinders={len(cnt):3d} M4/rand={M4/rand:8.0f}x")
