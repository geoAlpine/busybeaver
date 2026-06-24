import numpy as np
# Port self-consistency to o18 (base-3). Map T3(N)=floor(8N/3) = (x8 isometry on Z3) o (/3 = 3-adic shift).
# (A) Phi_3: low-trit renewal chain (state N mod 3^k, incoming high trit) -- does it contract to uniform(1/3)?
k=6; K=3**k
def step(s,ht): N=s+ht*K; return (8*N)//3 % K
def Phi3(digit_dist, T=300000):
    # incoming trit ~ digit_dist (prob of trit 0,1,2). Output = units-trit distribution of the chain.
    p=np.cumsum(digit_dist)
    s=1; x=999+int(digit_dist[0]*1e6)+int(digit_dist[2]*1e6)
    def rnd():
        nonlocal x; x=(1103515245*x+12345)&0x7fffffff; return x/0x7fffffff
    out=np.zeros(3)
    for n in range(T):
        r=rnd(); ht=0 if r<p[0] else (1 if r<p[1] else 2)
        if n>500: out[s%3]+=1
        s=step(s,ht)
    return out/out.sum()
print("Phi_3 iteration from skewed incoming trit-distributions -> converge to uniform (1/3,1/3,1/3)?")
for d0 in ([0.8,0.1,0.1],[0.1,0.1,0.8],[0.5,0.3,0.2],[0.34,0.33,0.33]):
    d=np.array(d0,float)
    for _ in range(6): d=Phi3(d)
    print(f"  start {d0} -> {np.round(d,4)}")

# (B) the hypothesis: high trit_k(N) INDEPENDENT of low-state N mod 3^k, on the actual orbit N->floor(8N/3).
from collections import Counter
N=4000  # big-int orbit
Nv=10
kk=5; KK=3**kk
pairs=[]
for n in range(N):
    s=Nv % KK; ht=(Nv//KK)%3
    pairs.append((s,ht)); Nv=(8*Nv)//3
cnt=Counter(pairs); cs=Counter(s for s,h in pairs); ch=Counter(h for s,h in pairs)
MI=sum((v/N)*np.log2((v/N)/((cs[s]/N)*(ch[h]/N))) for (s,h),v in cnt.items())
print(f"\n(B) I(high trit_k ; N mod 3^k) on orbit floor(8N/3) = {MI:.5f} bits (0=>independent; max={np.log2(3):.2f})")
# digit equidistribution
dd=Counter((Nv2:= (8*v//3) ) and 0 for v in [0])  # ignore
Nv=10; dig=Counter()
for n in range(N): dig[(Nv//KK)%3]+=1; Nv=(8*Nv)//3
print(f"    base-3 diagonal-ish digit distribution: {[round(dig[i]/N,3) for i in range(3)]} (uniform 0.333)")
print("\n=> if Phi_3 contracts to uniform AND high-trit ⊥ low-state: SAME conditional structure as Antihydra,")
print("   base-3 version. Digit equidistributes to 1/3 => o18 carry never aligns (Borel-Cantelli) => NON-HALT.")
