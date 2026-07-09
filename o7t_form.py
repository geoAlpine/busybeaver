#!/usr/bin/env python3
"""o7t_form.py -- re-derive & VERIFY the exact S-integer recursion for o7's cascade-entry
values, and measure the S-unit-vs-additive decomposition.

Clean recursion (to be verified 0-mismatch against F):
    x_n   = u_n + (w_n+3)/2 + d_n         (w_n=oddpart(u_n), d_n=v2(u_n))
    v_n   = v2(x_n)
    u_{n+1}+1 = (3/2)^{v_n} * x_n         (== 3^{v_n} * oddpart(x_n))
HALT iff w_n==1 (u_n a power of 2).
"""
import sys
from o7d_verify import F, v2, oddpart

def step_clean(u):
    d = v2(u); w = oddpart(u)
    if w == 1: return 'HALT'
    x = u + (w+3)//2 + d
    v = v2(x)
    return 3**v * oddpart(x) - 1   # = (3/2)^v * x - 1

def main(n_entries):
    # seed: first real cascade entry.  From o7d_verify_F the orbit starts a,b=2,2.
    # Reproduce entries by iterating F from the first entry.  Get first entry:
    from o7d_verify import step_map
    a,b,n = 2,2,0; prev_even=None; first=None
    while first is None:
        if a%2==1 and a>=5 and prev_even is True: first=a+3
        r=step_map(a,b); prev_even=(a%2==0); a,b=r[1],r[2]; n+=1
    u=first
    mism=0; V=0; A=0  # V=sum v_n (power of 3 & 2 exponent), A=sum d... 
    recs=[]
    for i in range(n_entries):
        sc=step_clean(u); sf=F(u)
        if sc!=sf:
            mism+=1
            if mism<=5: print("CLEAN vs F MISMATCH",u,sc,sf)
        if sf=='HALT':
            print("HALT at entry",i,"u=",u); return
        d=v2(u); w=oddpart(u); x=u+(w+3)//2+d; v=v2(x)
        V+=v
        # decomposition sizes (bits)
        recs.append((i,u.bit_length(),d,w.bit_length(),v))
        u=sf
    print(f"entries checked: {n_entries}; clean-vs-F mismatches: {mism}")
    print(f"final u bitlen: {u.bit_length()}; sum v_n (V) = {V}")
    # sample records
    print("i, bitlen(u), d=v2(u), bitlen(oddpart), v=v2(x):")
    for r in recs[:8]: print("  ",r)
    print("  ...")
    for r in recs[-5:]: print("  ",r)
    # correction ratio: c_n=(w+3)/2+d vs u_n.  measure log2(x/u)=log2(1+c/u).
    import math
    ratios=[]
    u2=first
    for i in range(min(n_entries,20000)):
        if oddpart(u2)==1: break
        d=v2(u2); w=oddpart(u2); c=(w+3)//2+d; x=u2+c
        ratios.append(x/u2)
        u2=F(u2)
    ratios.sort()
    print(f"correction multiplier x/u over {len(ratios)} entries: min={ratios[0]:.6f} "
          f"median={ratios[len(ratios)//2]:.6f} max={ratios[-1]:.6f}")
    print(f"  #entries with x/u>1.05: {sum(1 for r in ratios if r>1.05)} "
          f"({100*sum(1 for r in ratios if r>1.05)/len(ratios):.1f}%)")

if __name__=="__main__":
    main(int(sys.argv[1]) if len(sys.argv)>1 else 5000)
