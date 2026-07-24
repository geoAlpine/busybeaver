#!/usr/bin/env python3
"""R1: find the odd top rung OUT -- the config where the 1^4093 block (2^{g+9}-3) first appears,
i.e. where the top rung finished building it.  cReg11 @5018196, tail-top @11329137."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
cReg11=5018196; TOP=11329137
first=None
def hook(step,st,pos,tape,origin):
    global first
    if first: return
    r=rle(tape,pos,maxruns=6)
    if any(b==1 and l==4093 for b,l in r[:4]):
        first=(step, st, pos-origin, comb_left(tape,pos), ' '.join(f'{b}^{l}' for b,l in r[:5]))
run(TOP+1,hook=hook,hook_from=cReg11+1)
print(f"first 1^4093 @ {first[0] if first else None}")
if first:
    print(f"  st={'ABCDEF'[first[1]]} pos={first[2]} comb={first[3]} | {first[4]}")
    print(f"  rel to cReg11: +{first[0]-cReg11}  rel to tail-top: {first[0]-TOP}")
    print(f"  even topGrind 11 + exit 12 = 6310921; measured = {first[0]-cReg11}")
