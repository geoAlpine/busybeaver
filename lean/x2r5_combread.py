#!/usr/bin/env python3
"""Is the comb READ during the REGEN transport, or merely carried?

If merely carried, RegenLaw generalises to a free comb count `a` and topRung follows
(a = 0), closing the largest unproven span of the doubling phase.

Segments:
  g=2 TOP      regenIn-11-with-comb-0 @2 315 814 -> cascadeReg-11-shape @2 851 880  (536 066)
  g=4 CANONICAL the same levels, canonical, inside g=4's phase
For each: the head's minimum position vs where the comb sits in the left.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, check_anchors
assert check_anchors(verbose=False)
A,B = 2_315_814, 2_851_880
tr=[]; start=[None]
def hook(step,st,pos,tape,origin):
    if step==A:
        start[0]=(pos-origin, bytes(tape[max(0,pos-3000):pos]))
    if A<=step<=B: tr.append(pos-origin)
run(B+1,hook=hook,hook_from=A)
p0,l = start[0]; L=list(l[::-1])
n=0
while n<len(L) and L[n]==1: n+=1
print(f"g=2 TOP REGEN segment [{A},{B}] = {B-A} steps  (exitSteps 11 = 536066)")
print(f"  start pos {p0};  head range {min(tr)} .. {max(tr)}")
print(f"  left: ones-run = {n}, then {''.join(map(str,L[n:n+12]))}")
print(f"  the ones-run + separator occupy left indices 0..{n+4}")
print(f"  head descends {p0-min(tr)} cells into the left"
      f"  ->  {'STAYS INSIDE the ones-run+separator' if p0-min(tr)<=n+5 else 'GOES PAST the separator by '+str(p0-min(tr)-(n+5))+' cells'}")
