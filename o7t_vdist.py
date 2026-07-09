import sys
from collections import Counter
from o7d_verify import F, v2, oddpart
from o7d_verify import step_map
a,b,n=2,2,0; prev_even=None; first=None
while first is None:
    if a%2==1 and a>=5 and prev_even is True: first=a+3
    r=step_map(a,b); prev_even=(a%2==0); a,b=r[1],r[2]; n+=1
u=first; N=20000; vs=Counter(); ds=Counter()
for i in range(N):
    if oddpart(u)==1: print("HALT"); break
    d=v2(u); w=oddpart(u); x=u+(w+3)//2+d; vv=v2(x); vs[vv]+=1; ds[d]+=1
    u=3**vv*oddpart(x)-1
print("v_n (=v2(x_n), the S-unit exponent per step) distribution, N=20000:")
for k in sorted(vs)[:12]: print(f"  v={k}: {vs[k]:6d}  ({vs[k]/N:.4f})  geom 2^-(k+1)={2**-(k+1):.4f}")
print(f"  max v = {max(vs)}")
print("d_n (=v2(u_n)) distribution:")
for k in sorted(ds)[:8]: print(f"  d={k}: {ds[k]:6d}  ({ds[k]/N:.4f})")
print(f"  max d = {max(ds)}")
