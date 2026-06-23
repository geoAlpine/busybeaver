import numpy as np, math, cmath
# Erdos cluster (o18, x8/3=x2^3/3). Diagonal base-3 digit delta_n = (8^n // 3^n) % 3 = floor((8/3)^n) mod 3.
# Parallel to Mahler's bit_n(3^n). {(8/3)^n} = (8^n mod 3^n)/3^n.
N=3000
# 1) diagonal base-3 digit distribution over {0,1,2} -> uniform 1/3?
delta=[(pow(8,n)//pow(3,n))%3 for n in range(1,N+1)]
from collections import Counter
c=Counter(delta)
print("diagonal base-3 digit delta_n=floor((8/3)^n) mod 3 distribution:",
      {k:round(c[k]/N,4) for k in (0,1,2)}, " (uniform=0.333)")
# autocorr of [delta_n==2] (Erdos: digit 2) 
ind=[1 if d==2 else 0 for d in delta]
m=sum(ind)/N
cc=[x-m for x in ind]
ac=[sum(cc[i]*cc[i+l] for i in range(N-l))/sum(x*x for x in cc) for l in (1,2,3)]
print(f"  P(digit=2)={m:.4f} (->1/3); autocorr lags1-3 of [digit==2]: {[round(a,4) for a in ac]}")

# 2) {(8/3)^n} equidistribution
def frac83(n):
    r=pow(8,n,pow(3,n)); return r/pow(3,n) if n<40 else (pow(8,n,pow(3,n)))/pow(3,n)
fr=[ (pow(8,n,pow(3,n)))/pow(3,n) for n in range(1,1500+1)]
print(f"\n{{(8/3)^n}} in [0,1/3),[1/3,2/3),[2/3,1): ",
      [round(sum(1 for x in fr if a<=x<b)/len(fr),3) for a,b in [(0,1/3),(1/3,2/3),(2/3,1)]], "(unif 0.333)")

# 3) (b)-face: off-diagonal complete sum over <8> mod 3^M  -> Ramanujan, should be small/0
print("\n(b)-face off-diagonal |Σ_{n<ord} e(8^n/3^M)| for fixed M (complete <8>-orbit):")
for M in (6,8,10):
    q=3**M
    # ord of 8 mod 3^M = ord. 8=2^3; ord(2 mod 3^M)=2*3^(M-1); ord(8)=ord(2)/gcd(3,...). just iterate full ord.
    seen=set(); x=1%q; L=0
    while True:
        x=(x*8)%q; L+=1
        if x==8%q and L>1: break
        if L>q: break
    S=0j; x=1
    for n in range(L):
        x=(x*8)%q; S+=cmath.exp(2j*math.pi*x/q)
    print(f"  M={M} ord={L:6d}: |S|={abs(S):.3f}  |S|/sqrt(ord)={abs(S)/math.sqrt(L):.3f}")

# 4) (a)-face: 3-adic x8 isometry (|8|_3=1): fixed base-3 digit periodic in n?
print("\n(a)-face: fixed base-3 digit digit_k(8^n) periodic in n (x8 on Z_3 isometry):")
def d3(n,k): return (pow(8,n,3**(k+1))//3**k)%3
for k in (1,2,3,5):
    seq=[d3(n,k) for n in range(1,200)]
    per=next((p for p in range(1,100) if all(seq[i]==seq[i+p] for i in range(100))),None)
    print(f"  k={k}: period={per}  (predicted ord(8 mod 3^?)~2*3^(k-1)={2*3**(k-1)})")
