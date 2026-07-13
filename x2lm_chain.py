#!/usr/bin/env python3
"""x2lm_chain.py -- find the maximal chain of identical 29-step/+7 forward tiles in the
low-phase middle, extract its exact register encoding, and confirm chain length = u = g-1.
Also verify the tile is the SAME frame-independent transport at every link."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def to_M3(g):
    s=build(g); s.step(); mc=0
    while True:
        if s.is_milestone():
            mc+=1
            if mc==2: return s
        if not s.step(): return s

def snap(s): return (s.st,s.pos,s.h,list(s.L),list(s.R),s.n)
def restore(s,z): s.st,s.pos,s.h,s.L,s.R,s.n=z[0],z[1],z[2],z[3],z[4],z[5]

TILE_R_IN=[1,0,1,0,0,1,0,0,0,0,0]   # nearest-first right ctx (from head+1)
def tile_ctx(s):
    right=(s.R[::-1])[:11]
    return right==TILE_R_IN and s.st=='E' and s.h==0

for g in (2,4,6):
    s=to_M3(g)
    # collect all n in middle (until M4) where a 29-step +7 E-h0 tile with the SAME ctx begins
    # step through, at each config test if next 29 steps = +7 E-h0 tile AND ctx matches TILE_R_IN
    m4=False
    hits=[]
    while True:
        z=snap(s)
        ctx_ok = tile_ctx(s)
        moved=all(s.step() for _ in range(29))
        tile_ok = moved and s.st=='E' and s.h==0 and s.pos==z[1]+7
        if tile_ok and ctx_ok:
            hits.append(z[5])   # start n
        restore(s,z)
        if not s.step(): break
        if s.is_milestone():
            break
    # maximal consecutive run (step 29 apart)
    runs=[]
    cur=[hits[0]] if hits else []
    for a,b in zip(hits,hits[1:]):
        if b-a==29: cur.append(b)
        else: runs.append(cur); cur=[b]
    if cur: runs.append(cur)
    best=max(runs,key=len) if runs else []
    print(f"g={g} (u={g-1}): {len(hits)} ctx-matching tiles; maximal consecutive chain length = {len(best)}"
          f"  start n={best[0] if best else None}")

# extract exact register at the chain start for g=6 to see the periodic word
s=to_M3(6)
while True:
    z=snap(s)
    if tile_ctx(s):
        moved=all(s.step() for _ in range(29))
        ok=moved and s.st=='E' and s.h==0 and s.pos==z[1]+7
        restore(s,z)
        if ok:
            break
    if not s.step(): break
right=[s.h]+s.R[::-1]
print(f"\ng=6 chain start: n={s.n} pos={s.pos}")
print(f"  register nearest-first, first 45: {right[:45]}")
# show period-7: 1-positions
ones=[i for i,b in enumerate(right[:45]) if b==1]
print(f"  1-positions in first 45: {ones}")
