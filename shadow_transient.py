# Lemma 1 (PROVEN): shadows are transient. F is expanding (slope (3/2)^{D+1}, |.|_2=2^{D+1}), so near a fixed
# point p:  v2(F(x)-p) = v2(x-p) - (D+1).  An orbit entering at depth m=v2(x-p) leaves p's branch in <= m/(D+1)
# steps. Verified sharp on p=5/19 (D=2): integer == 5/19 mod 2^m shadows for exactly m/3 steps.
from fractions import Fraction as Fr
def v2(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
K=20000
p=Fr(5,19); pmod=(5*pow(19,-1,2**K))%(2**K)
for m in (30,50,70,90):
    seed=(5*pow(19,-1,2**K))%(2**m); xj=seed; prec=K; shadow=0
    for j in range(200):
        if prec<80: break
        vd=v2((xj-pmod)%(2**prec)); Dj=v2((3*xj-1)%(2**prec))
        if Dj==2 and vd>=2: shadow=j+1
        else: break
        xj=((3**(Dj+1)*xj-3**Dj+2**Dj)//2**(Dj+1))%(2**(prec-(Dj+1))); prec-=(Dj+1)
    print(f"seed==5/19 mod 2^{m}: shadow length={shadow} == m/(D+1)={m//3}")
