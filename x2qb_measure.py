#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
def lnear_full(L):
    r=[];i=0
    while i<len(L):
        b=L[-1-i];j=i
        while j<len(L) and L[-1-j]==b:j+=1
        r.append((b,j-i));i=j
    return r
def rfull(sim):
    seq=[sim.h]+sim.R[::-1];r=[];i=0
    while i<len(seq):
        b=seq[i];j=i
        while j<len(seq) and seq[j]==b:j+=1
        r.append((b,j-i));i=j
    return r
sim=build(2);sim.step()
S,E=13453,14388
while sim.n<S:
    if not sim.step():break
hist=[]
while sim.n<=E:
    hist.append((sim.n,sim.pos,sim.st,sim.h,sim.L[:],sim.R[:]))
    if not sim.step():break
poslist=[(h[0],h[1]) for h in hist]
mins_idx=[i for i in range(1,len(poslist)-1) if poslist[i][1]<=poslist[i-1][1] and poslist[i][1]<poslist[i+1][1]]
print("RT | rel | pos | R-decomp (head-first, first ~6 tokens) | #combpairs_before_block | blocklen")
for r,i in enumerate(mins_idx):
    n,p,st,h,L,R=hist[i]
    class T:pass
    t=T();t.h=h;t.R=R
    rr=rfull(t)
    # right: 0, then (1,0)* pairs, then big 1-block
    # find first 1-run with count>1  (the shrinking block)
    combpairs=0; blocklen=None; k=1
    # rr[0]=(0,1). then alternating (1,1)(0,1)... count pairs until a 1-run>1
    idx=1
    while idx+1 < len(rr):
        if rr[idx][0]==1 and rr[idx][1]>1:
            blocklen=rr[idx][1]; break
        if rr[idx][0]==1 and rr[idx][1]==1:
            combpairs+=1; idx+=1
        else:
            idx+=1
    ln=lnear_full(L)
    # count comb pairs on left (leading (1,0) pairs) until non-comb
    lp=0; idx2=0
    while idx2+1<len(ln) and ln[idx2]==(1,1) and ln[idx2+1]==(0,1):
        lp+=1; idx2+=1  # careful
    rtxt=" ".join(f"{'1' if b else '0'}^{c}" for b,c in rr[:7])
    print(f"{r:2d} | {n-S:4d} | {p} | {rtxt} | rcombpairs={combpairs} blocklen={blocklen} | Lcombpairs~{lp}")
