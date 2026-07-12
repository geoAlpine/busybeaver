#!/usr/bin/env python3
"""x2la_ecfold.py -- pin the E/C leftward block->comb fold tile + fold, and the
2-step entry, so the full non-carry tick factors as
  entry(2) o ECfold(m) o sweepEF(m),  m = (built+3)/2   [built odd].
Emit Lean-ready configs and verify by direct simulation.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim


def run_cfg(st, pos, Lnf, head, Rnf, nsteps):
    """Lnf nearest-first, Rnf head-first-after-head. Return final cfg."""
    rstr = str(head) + ''.join(str(b) for b in Rnf)
    sim = Sim(rstr, state=st, pos=pos)
    sim.L = list(Lnf)[::-1]
    for _ in range(nsteps):
        if not sim.step():
            return ('HALT', sim.n)
    Lout = [sim.L[-1-k] for k in range(len(sim.L))]
    Rout = [sim.R[-1-k] for k in range(len(sim.R))]
    return (sim.st, sim.pos, Lout, sim.h, Rout)


# --- ECfold tile: E on 1, block 1^{2}::Lrest to the left? actually consume 2 ones
#     from the left going left, emit (10) to the right. Test candidate:
#   steps 2 <E, p, [1,1]++L (nearest), head=1, R>  -> <E, p-2, L, head=1, [1,0]++R>?
# From the trace the head is E ON a 1 with more 1s to the LEFT. Let me test the
# leftward consumption directly.
print("=== ECfold tile candidates (E on 1, ones to the LEFT) ===")
# candidate A: head=1, left = 1::1::L, right = R
for L, R in [([1,1,1,0], [0,0]), ([1,1,1,1,1,0], [1,1,0])]:
    print("  A in: head=1 left=1,1,"+str(L)+" right="+str(R), "->",
          run_cfg('E', 0, [1,1]+L, 1, R, 2))

# The real tick's ECfold segment for built=3 is n=2..8 (E pos2 -> E pos-4, 6 steps).
# Reconstruct n=2 config exactly and confirm 6 steps -> the comb, then sweepEF(3).
print("\n=== built=3 full-tick segmentation ===")
# start of tick (n=0): E,0, left = 1,1,1,0, comb..., head 0, right 1,1,R
L0 = [1,1,1,0,1,0,1,0,1,0]         # 1^3 0 (10)^...
R0 = [1]*10 + [0,0] + [1]*5 + [0,0,1,0]  # after head 0: the 1^13 block etc
print("  entry(2):", run_cfg('E', 0, L0, 0, R0, 2))
print("  after 8 (entry+ECfold):", run_cfg('E', 0, L0, 0, R0, 8))
print("  after 14 (full tick):", run_cfg('E', 0, L0, 0, R0, 14))
# at n=8 we claim: E on 0, right = (10)^3 :: 1^rest ; sweepEF(3)=6 steps -> 1^6
seg = run_cfg('E', 0, L0, 0, R0, 8)
print("  n=8 head/right:", seg[3], seg[4][:12])
