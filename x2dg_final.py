#!/usr/bin/env python3
"""x2dg_final.py -- is the descent's FINAL 100 a BOUNDED tile (a `rfl` candidate), or does it
read the GROWING left comb?

From RESID (= descent IN + topGrindSteps(a) + lowerFoldSteps(a-3)) run 100 steps and record
the MINIMUM position reached relative to RESID (how deep LEFT it goes) and the MAXIMUM
(how deep RIGHT).  If the left excursion is bounded and identical across a=5,6,7, the FINAL
is a fixed tile in a bounded neighbourhood -> provable `∀` by kernel `rfl` with parametric
tails.  If the excursion grows with a, the FINAL depends on the accumulated comb.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

DESC = {5: 13453, 6: 33830, 7: 114703}


def topGrindSteps(a):
    return 2 ** (2 * a) + 7 - 3 * 2 ** a


def lowerFoldSteps(d):
    return 0 if d == 0 else (6 * (2 ** (d + 1) - 2) + 3) + lowerFoldSteps(d - 1)


def goto(sim, n):
    while sim.n < n:
        if not sim.step():
            raise SystemExit(f"HALT at {sim.n}")


for a in (5, 6, 7):
    s = DESC[a]
    resid = s + topGrindSteps(a) + lowerFoldSteps(a - 3)
    sim = build(2)
    sim.step()
    goto(sim, resid)
    p0 = sim.pos
    L0 = list(sim.L)
    print(f"\n=== a={a}  RESID @ raw {resid}")
    print(f"  IN  st={sim.st} left(nearest-first 12) = {[sim.L[-1-i] for i in range(min(12,len(sim.L)))]}")
    print(f"      right(12) = {sim.right_bits()[:12]}")
    lo = hi = 0
    trace = []
    for t in range(100):
        sim.step()
        d = sim.pos - p0
        lo = min(lo, d)
        hi = max(hi, d)
        trace.append((sim.st, d))
    print(f"  100 steps: pos excursion  lo={lo}  hi={hi}  net={sim.pos-p0}")
    print(f"  OUT st={sim.st} left(nearest-first 20) = {[sim.L[-1-i] for i in range(min(20,len(sim.L)))]}")
    print(f"      right(12) = {sim.right_bits()[:12]}")
    # how much of the ORIGINAL left stack was consumed / is unchanged?
    # left cells beyond depth `-lo` from the boundary can never have been touched.
    print(f"  deepest LEFT cell touched (rel to RESID head) = {lo}")
    print(f"  state word = {''.join(st for st, _ in trace)}")
