#!/usr/bin/env python3
"""odd topRung seam: track the odd register from cReg11 (g+8) to tail-IN.
The even topRung threads U through topgrind+RegenLawGen; measure the odd analogue's
register at a few points so the seam identity can be pinned."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
# odd g=3: cReg11 @5018196, tail-top @11329137.  Sample E-on-0 configs with a big block.
M6c=5018196; TOP=11329137
rows=[]
def hook(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    r=rle(tape,pos,maxruns=6)
    # big block present?
    if any(b==1 and l>1000 for b,l in r[:4]):
        rows.append((step, pos-origin, comb_left(tape,pos), ' '.join(f"{b}^{l}" for b,l in r[:5])))
run(TOP+1,hook=hook,hook_from=M6c)
print(f"odd big-block configs cReg11->tail-top: {len(rows)}")
# sample
idx=[0,1,2]+[i*len(rows)//8 for i in range(1,8)]+[len(rows)-2,len(rows)-1]
for i in sorted(set(x for x in idx if 0<=x<len(rows))):
    step,pos,comb,body=rows[i]
    print(f"  [{i}] {step} (+{step-M6c}) pos={pos} comb={comb} | {body}")
