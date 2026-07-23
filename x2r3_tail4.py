#!/usr/bin/env python3
"""tail(4): control for the '+27 frame-digit stage' reading.
Measured tails:  g=1 -> 0 stages (110 steps from the 0^13 top)
                 g=2 -> 1 stage
                 g=3 -> 2 stages (164 = 110 + 2*27)
PREDICTION (count = g-1):  g=4 -> 3 stages, i.e. 110 + 3*27 = 191 from its top config.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, check_anchors
assert check_anchors(verbose=False)
T = 44_986_995
rows=[]
def hook(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    rows.append((step,pos-origin,' '.join(f"{b}^{l}" for b,l in rle(tape,pos,maxruns=10)),comb_left(tape,pos)))
run(T+1, hook=hook, hook_from=T-4000)
print(f"g=4 tail: E-on-0 configs in [{T-4000}, {T}]  ({len(rows)} hits)")
prev=None
for step,pos,body,comb in rows:
    gap=f"(+{step-prev})" if prev is not None else ""
    prev=step
    print(f"  {step:>10} {gap:>7} pos={pos:>6} comb={comb:<4} | {body}")
