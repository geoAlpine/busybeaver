#!/usr/bin/env python3
"""x2qb_extract.py -- extract the TOPGRIND (a=5) cell-for-cell from build(2).
Window [13453, 14388] (935 steps), consumes top block 1^29, deposits doubled 1^126 0 1^61.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def runs(bits):
    out = []; i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b: j += 1
        out.append((b, j - i)); i = j
    return out

def snap(sim):
    lr = runs(sim.L[::-1])          # left, far-to-near? L is nearest-first (top=nearest)
    # left nearest-first: sim.L[-1] is nearest. Show nearest-first:
    lnear = []
    i=0; L=sim.L
    while i < len(L):
        b=L[-1-i]; j=i
        while j<len(L) and L[-1-j]==b: j+=1
        lnear.append((b,j-i)); i=j
    rr = runs([sim.h]+sim.R[::-1])
    return lnear, rr

def fmt(rr):
    return " ".join(f"{'1' if b else '0'}^{c}" for b,c in rr)

sim = build(2); sim.step()
S,E = 13453, 14388
while sim.n < S:
    if not sim.step(): break

print(f"=== TOPGRIND a=5 window [{S},{E}] ===")
ln, rr = snap(sim)
print(f"step {sim.n}: st={sim.st} h={sim.h} pos={sim.pos}")
print(f"  LEFT (nearest-first): {fmt(ln)}")
print(f"  RIGHT (head-first):   {fmt(rr)}")

# Trace to end
while sim.n < E:
    if not sim.step(): break
print(f"\nstep {sim.n}: st={sim.st} h={sim.h} pos={sim.pos}")
ln, rr = snap(sim)
print(f"  LEFT (nearest-first): {fmt(ln)}")
print(f"  RIGHT (head-first):   {fmt(rr)}")
