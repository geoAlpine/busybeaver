#!/usr/bin/env python3
"""R2: tail(3) = cascadeReg 12 -> M1(4) @ 11 329 301.  Dump the window, full-width RLE."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, label, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
M1_4 = 11_329_301
LO = M1_4 - 60000
rows=[]
def hook(step,st,pos,tape,origin):
    if step<LO or st!=E or tape[pos]!=0: return
    r = rle(tape,pos,maxruns=40)
    rows.append((step,pos-origin,label(tape,pos,r),comb_left(tape,pos),ones_left(tape,pos),r))
run(M1_4+1, hook=hook, hook_from=LO)
print(f"E-on-0 configs in [{LO},{M1_4}]: {len(rows)}")
prev=None
for step,pos,lb,comb,ol,r in rows:
    gap=f"(+{step-prev})" if prev is not None else ""
    prev=step
    body=' '.join(f"{b}^{l}" for b,l in r[:9])
    print(f"{step:>10} {gap:>7} pos={pos:>6} comb={comb:<4} ones_l={ol:<5} | {body}{'   <<< '+lb if lb else ''}")
