#!/usr/bin/env python3
"""x2lt_probe4.py -- (1) where does regen4_transport's IN pattern occur in build(2)?
(2) what is actually at REGEN(6)+154 ?  (3) TI-trace of the genuine REGEN(4)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

N0, N1 = 33108, 33830
CAP = 60000

R4_IN_L  = [1]*12 + [1,0,1,0,0,1,0]
R4_IN_R  = [0,1,0,0,0,0,0,0,0,0,0,0,0]

def snap(sim):
    return (sim.st, sim.pos, sim.L[::-1], sim.h, sim.R[::-1])

print("=== (1) occurrences of regen4_transport IN pattern in build(2), n<%d ===" % CAP)
sim = build(2); sim.step()
occ = []
while sim.n < CAP:
    st, pos, L, h, R = snap(sim)
    if st=='E' and h==0 and L[:19]==R4_IN_L and R[:13]==R4_IN_R:
        occ.append((sim.n, sim.pos))
    if not sim.step(): break
print("   occurrences (n,pos):", occ[:20], "... total", len(occ))

print("\n=== (2) config at REGEN(6)+154 = %d ===" % (N0+154))
sim = build(2); sim.step()
while sim.n < N0+154: sim.step()
st,pos,L,h,R = snap(sim)
print(f"   st={st} pos={pos} head={h}")
print(f"   L[0:40] = {''.join(map(str,L[:40]))}")
print(f"   R[0:40] = {''.join(map(str,R[:40]))}")

print("\n=== (2b) every E-on-0 anchor inside REGEN(6) window, with offsets ===")
sim = build(2); sim.step()
while sim.n < N0: sim.step()
anch=[]
while sim.n <= N1:
    if sim.st=='E' and sim.h==0:
        anch.append((sim.n, sim.n-N0, sim.pos))
    if sim.n==N1: break
    if not sim.step(): break
print("   count", len(anch))
for n,off,pos in anch:
    print(f"      n={n} off={off:4d} pos={pos}")
