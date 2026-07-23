#!/usr/bin/env python3
"""R3: g=6 (even, 3rd even point) and g=7 (odd, 4th odd point -- TESTS a closed-form FIT).

PREDICTIONS, stated BEFORE measuring (METHODS M4):
  odd topEntry(g) = 6080*2^g + 53g + 105   -- FIT to g=1,3,5 (12318 / 48904 / 194930);
      3 points, 3 parameters, so it has NO predictive content yet.  g=7 tests it:
      PREDICT topEntry(7) = 6080*128 + 371 + 105 = 778 716.
  g=6 entry level = descIn 13 (even rule K-1, K=14), marker head with NO leading 1-run.
  g=7 entry level = descIn 13 (odd rule K-2, K=15), marker head leading 1-run = 20.
"""
import sys, time
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, comb_left, check_anchors
assert check_anchors(verbose=False)
M1_6 = 179_590_445
Z200 = bytearray(200)

def descIn_raw(tape,pos,r):
    if len(r)>=3 and r[0]==(0,1) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-2: return k,comb_left(tape,pos),1<<(k-1)
    return None

def entry_scan(m1, span, tag):
    hits=[]
    def hook(step,st,pos,tape,origin):
        if st!=E or tape[pos]!=0 or len(hits)>=2: return
        r=rle(tape,pos,maxruns=48)
        d=descIn_raw(tape,pos,r)
        if d is not None and d[1]>=d[2]:
            hits.append((step,pos-origin,d,bytes(tape[max(0,pos-9000):pos])))
    t=time.time(); run(m1+span, hook=hook, hook_from=m1+1)
    print(f"\n{tag}: scan [{m1+1}, {m1+span}]  ({round(time.time()-t,1)}s)")
    for step,pos,(k,comb,want),lw in hits:
        left=lw[::-1]; i=0
        while i+1<len(left) and left[i]==0 and left[i+1]==1: i+=2
        head=''.join(map(str,left[i:i+40])); ones=len(head)-len(head.lstrip('1'))
        print(f"  {step:>11} (+{step-m1:>8}) descIn {k:<3} pos={pos:<7} comb={comb} (want {want})"
              f"  leading 1-run = {ones}")
    return hits

entry_scan(M1_6, 900_000, "g=6 (EVEN; predict descIn 13, no 1-run)")

# find M1(7): expected near 4 * M1(6) ~ 718.4M
ms=[]
def hookm(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0 or pos>=origin: return
    if tape[pos-200:pos]==Z200 and 1 not in tape[:pos]: ms.append(step)
t=time.time(); run(730_000_000, hook=hookm, hook_from=700_000_000)
print(f"\nmilestone-signature steps in [700M,730M]: {ms[:6]}  ({round(time.time()-t,1)}s)")
if ms:
    M1_7 = ms[0]
    print(f"M1(7) = {M1_7}")
    entry_scan(M1_7, 1_200_000, "g=7 (ODD; predict descIn 13, 1-run 20, cost 778716)")
