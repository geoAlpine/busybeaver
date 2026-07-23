#!/usr/bin/env python3
"""R2: locate M1(4), M1(5) and the cascadeReg(g+9) before each -- tail(3), tail(4)."""
import sys, time
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, label, check_anchors
HI = int(sys.argv[1]) if len(sys.argv)>1 else 60_000_000
LO = int(sys.argv[2]) if len(sys.argv)>2 else 2_900_000
assert check_anchors(verbose=False), "instrument check failed"
Z = bytearray(40)
hits=[]
def hook(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    if tape[pos-40:pos]==Z and 1 not in tape[:pos]:
        hits.append((step,pos-origin,'*** M1 MILESTONE ***','')); return
    r=rle(tape,pos)
    if len(r)>=4 and r[0]==(0,3) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and k>=11 and cascade_at(r,3)==k-3:
            hits.append((step,pos-origin,f'cascadeReg {k}',' '.join(f"{b}^{l}" for b,l in r[:4])))
t=time.time(); res=run(HI,hook=hook,hook_from=LO)
print(f"scanned [{LO},{HI}] halted={res[4]} reach={res[6][0]-res[5]}..{res[6][1]-res[5]} elapsed={round(time.time()-t,1)}s")
prev=None
for step,pos,lb,body in hits:
    gap=f"(+{step-prev})" if prev is not None else ""
    prev=step
    print(f"{step:>11} {gap:>12} pos={pos:>7} {lb}   {body}")
