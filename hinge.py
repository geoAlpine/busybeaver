import numpy as np
from collections import Counter
# THE HINGE: the adversary breaks even-density>1/3 by correlating the incoming bit bit_k(c_n) with the
# low-bit STATE c_n mod 2^k. If the REAL orbit has bit_k(c_n) INDEPENDENT of (c_n mod 2^k), the renewal
# contraction forces even-density 1/2 unconditionally. Measure mutual information I(bit_k ; low-state).
N=800000
for k in (6,8,10):
    c=8; pairs=[]
    K=1<<k
    for n in range(N):
        state=c & (K-1)         # c_n mod 2^k
        hib=(c>>k)&1            # incoming high bit bit_k(c_n)
        pairs.append((state,hib))
        c=3*c//2
    # mutual information I(state ; high bit). state has k bits; reduce to: does high bit depend on state?
    # MI between hib and state: I = sum p(s,h) log( p(s,h)/(p(s)p(h)) )
    cnt=Counter(pairs); cs=Counter(s for s,h in pairs); ch=Counter(h for s,h in pairs)
    MI=0.0
    for (s,h),v in cnt.items():
        p=v/N; ps=cs[s]/N; ph=ch[h]/N
        MI+=p*np.log2(p/(ps*ph))
    # also: the MORE RELEVANT correlation -- does hib correlate with the PARITY (low bit, s&1)?
    par=np.array([s&1 for s,h in pairs],float); hb=np.array([h for s,h in pairs],float)
    corr=np.corrcoef(par,hb)[0,1]
    print(f"k={k:2d}: I(bit_k ; c_n mod 2^k) = {MI:.5f} bits (0=>independent; max={k})   corr(bit_k,parity)={corr:+.5f}")
print("\n=> if MI~0: incoming high bit is INDEPENDENT of the low-bit state => adversary's correlated-attack")
print("   is NOT realized by the real orbit => renewal contraction (gap 0.99) forces even-density 1/2.")
print("   THE remaining gap, in its sharpest form: PROVE bit_k(c_n) ⊥ (c_n mod 2^k) unconditionally.")
