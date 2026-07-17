#!/usr/bin/env python3
"""Detect outer round-trip structure of TOPGRIND a=5 window [13453,14388]."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def runs(bits):
    out=[];i=0
    while i<len(bits):
        b=bits[i];j=i
        while j<len(bits) and bits[j]==b:j+=1
        out.append((b,j-i));i=j
    return out
def lnear_runs(L,k=6):
    runs=[];i=0
    while i<len(L) and len(runs)<k:
        b=L[-1-i];j=i
        while j<len(L) and L[-1-j]==b:j+=1
        runs.append((b,j-i));i=j
    return runs
def fmt(rr):
    return "".join(f"{'1' if b else '0'}^{c} " for b,c in rr)

sim=build(2); sim.step()
S,E=13453,14388
while sim.n<S:
    if not sim.step(): break

# Track turning points in pos
poss=[]
prev_pos=sim.pos
recs=[(sim.n,sim.pos,sim.st,sim.h)]
minmax=[]
last=sim.pos; direction=0
turns=[]
prevp=sim.pos
history=[(sim.n,sim.pos)]
while sim.n<E:
    if not sim.step(): break
    history.append((sim.n,sim.pos))

# find local minima (leftmost points = start of each rightward sweep / bottom of round trip)
mins=[]
for i in range(1,len(history)-1):
    n,p=history[i]
    if p<=history[i-1][1] and p<history[i+1][1]:
        mins.append((n,p))
maxs=[]
for i in range(1,len(history)-1):
    n,p=history[i]
    if p>=history[i-1][1] and p>history[i+1][1]:
        maxs.append((n,p))
print(f"window {S}-{E}, {len(history)} configs")
print(f"pos range: {min(p for _,p in history)} .. {max(p for _,p in history)}")
print(f"# local minima (turnarounds left): {len(mins)}")
print(f"# local maxima (turnarounds right): {len(maxs)}")
# print the minima positions and step gaps
print("\nLocal minima (n_rel, pos):")
for (n,p) in mins[:60]:
    print(f"  rel={n-S:5d} pos={p}")
