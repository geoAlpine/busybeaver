#!/usr/bin/env python3
"""x2rm_preg_ladder.py -- the POSITION ladder p(k) and comb-excess Lc(k) at the REAL
descent starts.  Any forall-k form of `cascadeReg k Lc p` must supply BOTH p(k) and
Lc(k) as closed forms; the Lean file currently has them only as the bespoke constants
p(4) = -7, p(5) = -22 (from carry_exit_j3/j4) and Lc = 1 (simulator, k=4..7).

Measured on x2bd_sim.build(2) at the descent starts raw n = 13453/33830/114703
(a=5,6,7; the anchors lean/X2.lean §5ag/§5ah records).  MAXIMAL run-length parse.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

ANCH = {5: 13453, 6: 33830, 7: 114703}

def left_comb_pairs_maximal(sim):
    """count maximal leading (0,1) pairs of the left stack, nearest-first."""
    L = sim.L; m = 0; i = 0
    while i + 1 < len(L) and L[-1-i] == 0 and L[-1-(i+1)] == 1:
        m += 1; i += 2
    return m

sim = build(2); rows = []
target = sorted(ANCH.values())
seen = {}
while sim.n <= target[-1]:
    if sim.n in target:
        seen[sim.n] = (sim.st, sim.h, sim.pos, left_comb_pairs_maximal(sim))
    if not sim.step():
        break

print(f"{'k':>2} {'raw n':>8} {'st':>3} {'head':>4} {'pos p(k)':>9} "
      f"{'comb (01)^m':>12} {'N=2^(k-1)-2':>12} {'Lc = m - N':>10}")
for k in (5, 6, 7):
    n = ANCH[k]
    if n not in seen:
        print(f"{k:>2} {n:>8}  -- not reached"); continue
    st, h, pos, m = seen[n]
    N = 2**(k-1) - 2
    print(f"{k:>2} {n:>8} {st:>3} {h:>4} {pos:>9} {m:>12} {N:>12} {m-N:>10}")
print()
print("Lean's bespoke constants (from carry_exit_j3/j4, NOT measured here):")
print("  p(4) = -7   (regen4_transport OUT pos)")
print("  p(5) = -22  (regen5_transport OUT pos)")
