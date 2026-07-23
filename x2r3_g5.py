#!/usr/bin/env python3
"""R3: g=5 (ODD) -- third odd data point.  Entry level + marker head; then M1(6) and tail(5).
PREDICTIONS to test (stated BEFORE measuring, METHODS M4):
  entry level = K-2 = 11   (odd rule from g=1,3)
  marker head = exactly twenty 1s
  tail(5) frameDigit stages = g-1 = 4
"""
import sys, time
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, comb_left, check_anchors
assert check_anchors(verbose=False)
M1_5 = 44_986_995

def descIn_raw(tape,pos,r):
    if len(r)>=3 and r[0]==(0,1) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-2: return k,comb_left(tape,pos),1<<(k-1)
    return None

# --- pass 1: entry ---
hits=[]
def hook1(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0 or len(hits)>=4: return
    r=rle(tape,pos,maxruns=48)
    d=descIn_raw(tape,pos,r)
    if d is not None and d[1]>=d[2]:
        hits.append((step,pos-origin,d,bytes(tape[max(0,pos-6000):pos])))
t=time.time(); run(M1_5+600_000, hook=hook1, hook_from=M1_5+1)
print(f"g=5 entry scan [{M1_5+1}, {M1_5+600000}]  ({round(time.time()-t,1)}s)")
print("  K(5)=13 -> even rule would give descIn 12, odd rule (K-2) gives descIn 11")
for step,pos,(k,comb,want),lw in hits:
    left=lw[::-1]; i=0
    while i+1<len(left) and left[i]==0 and left[i+1]==1: i+=2
    head=''.join(map(str,left[i:i+40]))
    ones=len(head)-len(head.lstrip('1'))
    print(f"  {step:>10} (+{step-M1_5:>7}) descIn {k:<3} pos={pos:<7} comb={comb} (want {want})")
    print(f"        marker head: {head}   leading 1-run = {ones}")

# --- pass 2: M1(6) and tail(5) ---
Z=bytearray(40); ms=[]
def hook2(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    if tape[pos-40:pos]==Z and 1 not in tape[:pos]: ms.append(step)
t=time.time(); run(220_000_000, hook=hook2, hook_from=M1_5+1000)
print(f"\nmilestone-signature steps after M1(5): {ms[:8]}  ({round(time.time()-t,1)}s)")
