#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
def lnear_full(L,cap=40):
    r=[];i=0
    while i<len(L) and len(r)<cap:
        b=L[-1-i];j=i
        while j<len(L) and L[-1-j]==b:j+=1
        r.append((b,j-i));i=j
    return r
sim=build(2);sim.step()
S,E=13453,14388
while sim.n<S:
    if not sim.step():break
hist=[]
while sim.n<=E:
    hist.append((sim.n,sim.pos,sim.st,sim.h,sim.L[:]))
    if not sim.step():break
poslist=[(h[0],h[1]) for h in hist]
mins_idx=[i for i in range(1,len(poslist)-1) if poslist[i][1]<=poslist[i-1][1] and poslist[i][1]<poslist[i+1][1]]
for r,i in enumerate(mins_idx):
    n,p,st,h,L=hist[i]
    ln=lnear_full(L)
    # count leading comb (1,1)(0,1) pairs before hitting 1^126 or other
    lp=0;idx=0
    while idx+1<len(ln) and ln[idx]==(1,1) and ln[idx+1]==(0,1):
        lp+=1; idx+=1  # each pair uses 2 tokens
    # actually properly step by 2
    lp=0;idx=0
    while idx+1<len(ln) and ln[idx]==(1,1) and ln[idx+1]==(0,1):
        lp+=1; idx+=2
    txt=" ".join(f"{'1' if b else '0'}^{c}" for b,c in ln[:12])
    print(f"RT{r:2d} pos={p}: Lcombpairs={lp} | {txt}")
