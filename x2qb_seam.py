#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
def full_tape(sim, w=14):
    # window around head: w cells each side
    left = [sim.L[-1-i] if i < len(sim.L) else 0 for i in range(w)][::-1]
    right = [sim.R[-1-i] if i < len(sim.R) else 0 for i in range(w)]
    ls = "".join(str(b) for b in left)
    rs = "".join(str(b) for b in right)
    return f"{ls}[{sim.h}]{rs}"
sim=build(2);sim.step()
S=13453
while sim.n<S: 
    if not sim.step(): break
# advance to rel 15
for _ in range(15): sim.step()
print("rel : st h pos | ...L[h]R...")
for _ in range(24):
    print(f"{sim.n-S:3d} : {sim.st} {sim.h} {sim.pos} | {full_tape(sim)}")
    if not sim.step(): break
