#!/usr/bin/env python3
"""R4 seam: ladder top (cascadeReg g+9) -> tailLaw's IN.  Fixed episode, or block-dependent?
Measured tail-IN steps: g=2 @2851954, g=4 @44986804.  Find the cascadeReg before each."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, check_anchors
assert check_anchors(verbose=False)
TARGETS={2851954:('g=2',11), 44986804:('g=4',13)}
def creg(tape,pos,r):
    if len(r)>=4 and r[0]==(0,3) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-3: return k
    return None
best={}
def hook(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    for t in TARGETS:
        if t-3000<=step<=t:
            r=rle(tape,pos,maxruns=48)
            k=creg(tape,pos,r)
            if k is not None: best[t]=(step,pos-origin,k)
run(max(TARGETS)+1,hook=hook,hook_from=min(TARGETS)-3000)
for t,(tag,wantk) in sorted(TARGETS.items()):
    if t in best:
        s,pos,k=best[t]
        print(f"{tag}: cascadeReg {k} @{s} pos={pos}  ->  tail IN @{t}   SEAM = {t-s} steps"
              f"   (expected level {wantk}: {'OK' if k==wantk else 'MISMATCH'})")
    else:
        print(f"{tag}: no cascadeReg found within 3000 steps before {t}")
