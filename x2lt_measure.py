#!/usr/bin/env python3
"""x2lt_measure.py -- MEASURE FIRST: locate the REGEN(4) sub-transport INSIDE
REGEN(6)'s window [33108,33830] of build(2) as an actual `steps` segment.

Prints Lean-order configs (L nearest-first, head, R nearest-first) at the
candidate split points, and checks them against regen4_transport's IN/OUT
patterns from lean/X2.lean.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

N0, N1 = 33108, 33830

def snap(sim):
    """Lean-order (st, pos, L_nearest_first, head, R_nearest_first)."""
    return (sim.st, sim.pos, sim.L[::-1], sim.h, sim.R[::-1])

def run_to(n):
    sim = build(2); sim.step()
    while sim.n < n:
        if not sim.step(): raise RuntimeError("halt")
    return sim

def show(sim, label, nl=30, nr=30):
    st, pos, L, h, R = snap(sim)
    print(f"{label}  n={sim.n} st={st} pos={pos}")
    print(f"   L[0:{nl}] (nearest-first) = {''.join(str(b) for b in L[:nl])}")
    print(f"   head = {h}")
    print(f"   R[0:{nr}] (nearest-first) = {''.join(str(b) for b in R[:nr])}")

sim = run_to(N0)
show(sim, "REGEN(6) IN   @33108")
print()

# window length check
sim2 = run_to(N1)
show(sim2, "REGEN(6) OUT  @33830")
print(f"\nwindow length = {N1-N0} (exitSteps 6 = 722? {N1-N0==722})")
print("="*70)

# ---- regen4_transport IN pattern (from lean/X2.lean:4206) ----
# st E, pos 9, L = ones 12 ++ [1,0,1,0,0,1,0] ++ free
#                head = false
#                R = [0,1,0,0,0,0,0,0,0,0,0,0,0] ++ free
R4_IN_L  = [1]*12 + [1,0,1,0,0,1,0]
R4_IN_H  = 0
R4_IN_R  = [0,1,0,0,0,0,0,0,0,0,0,0,0]
R4_IN_ST = 'E'

def matches_r4_in(sim):
    st, pos, L, h, R = snap(sim)
    return (st == R4_IN_ST and h == R4_IN_H
            and L[:len(R4_IN_L)] == R4_IN_L
            and R[:len(R4_IN_R)] == R4_IN_R)

print("Scanning [33108,33830] for the regen4_transport IN pattern (tape-shape match):")
sim = run_to(N0)
hits = []
while sim.n <= N1:
    if matches_r4_in(sim):
        hits.append((sim.n, sim.n - N0, sim.pos))
    if sim.n == N1: break
    if not sim.step(): break
for n, off, pos in hits:
    print(f"   HIT n={n}  offset-from-REGEN(6)-IN = {off}  pos={pos}")
if not hits:
    print("   *** NO HIT ***")
