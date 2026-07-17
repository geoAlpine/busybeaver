#!/usr/bin/env python3
"""Config signature at each round-trip minimum of TOPGRIND a=5."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def lnear_runs(L,k=8):
    r=[];i=0
    while i<len(L) and len(r)<k:
        b=L[-1-i];j=i
        while j<len(L) and L[-1-j]==b:j+=1
        r.append((b,j-i));i=j
    return r
def rruns(sim,k=10):
    seq=[sim.h]+sim.R[::-1];r=[];i=0
    while i<len(seq) and len(r)<k:
        b=seq[i];j=i
        while j<len(seq) and seq[j]==b:j+=1
        r.append((b,j-i));i=j
    return r
def fmt(rr):
    return "".join(f"{'1' if b else '0'}^{c} " for b,c in rr)

sim=build(2); sim.step()
S,E=13453,14388
while sim.n<S:
    if not sim.step(): break
hist=[]
while sim.n<=E:
    hist.append((sim.n,sim.pos,sim.st,sim.h,sim.L[:],sim.R[:]))
    if not sim.step(): break

# reconstruct minima
poslist=[(h[0],h[1]) for h in hist]
mins_idx=[i for i in range(1,len(poslist)-1) if poslist[i][1]<=poslist[i-1][1] and poslist[i][1]<poslist[i+1][1]]
print("=== config at each round-trip minimum (leftmost turn) ===")
for r,i in enumerate(mins_idx):
    n,p,st,h,L,R=hist[i]
    class T: pass
    t=T(); t.h=h; t.R=R
    lr=lnear_runs(L)
    rr=rruns(t)
    print(f"\nRT {r}: rel={n-S} pos={p} st={st}")
    print(f"   L(near): {fmt(lr)}")
    print(f"   R(head): {fmt(rr)}")
