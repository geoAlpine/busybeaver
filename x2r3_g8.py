#!/usr/bin/env python3
"""R3: g=8 -- tests the EVEN closed form (3 points, 3 params -> no predictive content yet).

  even topEntry(g) = 384*2^g + 53g + 384   (fits g=2,4,6 = 2026 / 6740 / 25278 exactly)
  PREDICT topEntry(8) = 384*256 + 424 + 384 = 99 112, entry level descIn 15 (K-1, K=16),
          marker head with NO leading 1-run.

(The ODD form 6080*2^g + 53g + 105 is already CONFIRMED: fitted on g=1,3,5 and predicted
 g=7 = 778 716 before measuring; measured 778 716.)
"""
import sys, time
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, comb_left, check_anchors
assert check_anchors(verbose=False)
SPAN = 1 << 18
Z200 = bytearray(200)
def descIn_raw(tape,pos,r):
    if len(r)>=3 and r[0]==(0,1) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-2: return k,comb_left(tape,pos),1<<(k-1)
    return None
ms=[]
def hookm(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0 or pos>=origin: return
    if tape[pos-200:pos]==Z200 and 1 not in tape[:pos]: ms.append(step)
t=time.time(); run(2_950_000_000, hook=hookm, hook_from=2_820_000_000, span=SPAN)
print(f"milestones in [2.82G,2.95G]: {ms[:4]}  ({round(time.time()-t,1)}s)")
if ms:
    M=ms[0]; print(f"M1(8) = {M}")
    hits=[]
    def hook(step,st,pos,tape,origin):
        if st!=E or tape[pos]!=0 or hits: return
        r=rle(tape,pos,maxruns=48)
        d=descIn_raw(tape,pos,r)
        if d is not None and d[1]>=d[2]:
            hits.append((step,pos-origin,d,bytes(tape[max(0,pos-40000):pos])))
    t=time.time(); run(M+400_000, hook=hook, hook_from=M+1, span=SPAN)
    for step,pos,(k,comb,want),lw in hits:
        left=lw[::-1]; i=0
        while i+1<len(left) and left[i]==0 and left[i+1]==1: i+=2
        head=''.join(map(str,left[i:i+40])); ones=len(head)-len(head.lstrip('1'))
        print(f"  {step:>12} (+{step-M:>8}) descIn {k} pos={pos} comb={comb} (want {want}) 1-run={ones}")
        print(f"  PREDICTED cost 99112 -> {'MATCH' if step-M==99112 else 'MISS'};"
              f" predicted level 15 -> {'MATCH' if k==15 else 'MISS'}")
