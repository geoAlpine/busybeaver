#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
def lnear(L,k=10):
    r=[];i=0
    while i<len(L) and len(r)<k:
        b=L[-1-i];j=i
        while j<len(L) and L[-1-j]==b:j+=1
        r.append((b,j-i));i=j
    return r
def rr(sim,k=12):
    seq=[sim.h]+sim.R[::-1];r=[];i=0
    while i<len(seq) and len(r)<k:
        b=seq[i];j=i
        while j<len(seq) and seq[j]==b:j+=1
        r.append((b,j-i));i=j
    return r
def fmt(x):return "".join(f"{'1' if b else '0'}^{c} " for b,c in x)
sim=build(2);sim.step()
S=13453
while sim.n<S:
    if not sim.step():break
# advance to rel=7
for _ in range(7):sim.step()
print("=== micro-trace RT0->RT2 (rel 7 to 35) ===")
for _ in range(30):
    print(f"rel={sim.n-S:3d} st={sim.st} h={sim.h} pos={sim.pos} | L: {fmt(lnear(sim.L,6))}| R: {fmt(rr(sim,8))}")
    if not sim.step():break
