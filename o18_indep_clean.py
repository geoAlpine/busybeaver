import numpy as np
from collections import Counter
# Confirm high-trit ⊥ low-state for o18 with controlled finite-size. Use smaller k, compare to shuffle baseline.
for kk in (2,3):
    KK=3**kk
    for Nsteps in (8000,):
        Nv=10; pairs=[]
        for n in range(Nsteps):
            s=Nv % KK; ht=(Nv//KK)%3; pairs.append((s,ht)); Nv=(8*Nv)//3
        N=len(pairs)
        cnt=Counter(pairs); cs=Counter(s for s,h in pairs); ch=Counter(h for s,h in pairs)
        MI=sum((v/N)*np.log2((v/N)/((cs[s]/N)*(ch[h]/N))) for (s,h),v in cnt.items())
        # shuffle baseline: independent re-pairing
        ss=[s for s,h in pairs]; hs=[h for s,h in pairs]
        # deterministic shuffle of hs
        idx=list(range(N)); 
        x=7
        for i in range(N-1,0,-1):
            x=(1103515245*x+12345)&0x7fffffff; j=x%(i+1); idx[i],idx[j]=idx[j],idx[i]
        hs2=[hs[idx[i]] for i in range(N)]
        cnt2=Counter(zip(ss,hs2)); ch2=Counter(hs2)
        MI_sh=sum((v/N)*np.log2((v/N)/((cs[s]/N)*(ch2[h]/N))) for (s,h),v in cnt2.items())
        print(f"k={kk} (3^{kk}={KK} states), N={N}: MI(trit_k;low)={MI:.4f}  shuffle-baseline={MI_sh:.4f}  excess={MI-MI_sh:+.4f}")
print("\n(excess MI over shuffle ~0 => the dependence is finite-size noise => high-trit ⊥ low-state holds,")
print(" SAME as Antihydra. excess significantly >0 => o18 has genuine residual correlation.)")
