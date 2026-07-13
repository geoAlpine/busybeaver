#!/usr/bin/env python3
"""x2lo_trace.py -- fix window to stop at M6; trace M3->M4 growing segment to
find the repeating U-unit tile. The register M1(g)=0^22 (1 0^6)^{g-1} tail.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def run_to_M6(g, trace=False):
    sim = build(g)
    m1_pos = sim.pos
    miles = []
    minp=maxp=sim.pos
    tr=[]
    sim.step()
    while True:
        minp=min(minp,sim.pos); maxp=max(maxp,sim.pos)
        if trace: tr.append((sim.n, sim.st, sim.pos))
        if sim.is_milestone():
            miles.append(sim.n)
            if len(miles)==5: break  # M6 is 5th milestone
        sim.step()
    return miles, (minp-m1_pos, maxp-m1_pos), tr

for g in [2,3,4,5]:
    miles,win,_ = run_to_M6(g)
    print(f"g={g}: milestones(M2..M6)={miles}  low-phase head window rel M1 = {win}")

# Now trace M3->M4 for g=4 and look at the pos sawtooth (the U-unit crossings)
print("\n--- g=4 M3..M4 pos trace (looking for repeating tile) ---")
miles,win,tr = run_to_M6(4, trace=True)
M3, M4 = miles[1], miles[2]
seg = [(n,st,pos) for (n,st,pos) in tr if M3<=n<=M4]
# print positions at state changes to compress; show local maxima
print(f"M3={M3} M4={M4} segment length={M4-M3}")
# show pos every step compactly: find turning points
prev=None
for i,(n,st,pos) in enumerate(seg):
    print(f"n={n} {st} pos={pos}", end="   ")
    if (i+1)%6==0: print()
print()
