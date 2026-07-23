#!/usr/bin/env python3
"""O2: what is in the ODD topEntry's big region (rel 144 .. 48485 at g=3)?
Scan for known families (descIn / regenIn / cascadeReg, FULL shape)."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
M6 = 2852091 + 305 + 38*3
HI = M6 + 48485
def lab(tape,pos,r):
    if len(r)>=3 and r[0]==(0,1) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-2 and comb_left(tape,pos)>=(1<<(k-1)):
            return f"descIn {k}"
    if len(r)>=2 and r[0]==(0,1):
        d=cascade_at(r,1)
        if d is not None and ones_left(tape,pos)==(1<<(d+4))-3: return f"regenIn {d+4}"
    if len(r)>=4 and r[0]==(0,3) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-3: return f"cascadeReg {k}"
    return None
rows=[]
def hook(step,st,pos,tape,origin):
    if step<M6+144 or st!=E or tape[pos]!=0: return
    r=rle(tape,pos,maxruns=40)
    L=lab(tape,pos,r)
    if L: rows.append((step-M6,pos-origin,L,' '.join(f"{b}^{l}" for b,l in r[:6])))
run(HI+1,hook=hook,hook_from=M6+144)
print(f"g=3 odd topEntry, rel 144..48485: {len(rows)} known-family configs")
prev=None
for rel,pos,L,body in rows[:40]:
    gap=f"(+{rel-prev})" if prev is not None else ""
    prev=rel
    print(f"  rel={rel:<7}{gap:>9} pos={pos:>6} {L:<14} | {body}")
if len(rows)>40: print(f"  ... ({len(rows)-40} more)")
