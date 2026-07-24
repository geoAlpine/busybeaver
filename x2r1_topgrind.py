#!/usr/bin/env python3
"""R1: the odd top rung split.  cReg11 @5018196.  Even analogy: topGrindSteps 11 = 4 188 167
lands regenIn 12 (comb-free); exitSteps 12 = 2 122 754 lands the top.  Sample both predicted
points to see the odd register structure and pin the actual seam."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
cReg11=5018196
pts={cReg11+4188167:'topgrind OUT (pred)', cReg11+4188167+2122754:'exit OUT (pred)',
     11329108:'4093 built'}
snap={}
def hook(step,st,pos,tape,origin):
    if step in pts: snap[step]=(st,pos-origin,comb_left(tape,pos),ones_left(tape,pos),
                                ' '.join(f'{b}^{l}' for b,l in rle(tape,pos,maxruns=7)))
run(max(pts)+1,hook=hook,hook_from=cReg11)
for s in sorted(pts):
    if s in snap:
        st,pos,comb,ol,body=snap[s]
        print(f"{s} [{pts[s]}] st={'ABCDEF'[st]} pos={pos} comb={comb} ones_l={ol}")
        print(f"  | {body}")
