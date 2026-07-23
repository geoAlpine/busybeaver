#!/usr/bin/env python3
"""R3: g=1 (ODD) -- a second cheap odd data point.  Entry level, cost, marker head, tail."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, comb_left, check_anchors
M1 = {1: 188099, 2: 732733, 3: 2852091, 4: 11329301, 5: 44986995}

def descIn_raw(tape, pos, r):
    if len(r) >= 3 and r[0] == (0, 1) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]; k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 2:
            return k, comb_left(tape, pos), 1 << (k - 1)
    return None

def cascadeReg_raw(tape, pos, r):
    if len(r) >= 4 and r[0] == (0, 3) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]; k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 3:
            return k
    return None
assert check_anchors(verbose=False)
g=1
hits=[]; lastc=None; finals=[]
def hook(step,st,pos,tape,origin):
    global lastc
    if st!=E or tape[pos]!=0: return
    r=rle(tape,pos,maxruns=48)
    d=descIn_raw(tape,pos,r)
    if d is not None and len(hits)<8: hits.append((step,pos-origin,d,bytes(tape[max(0,pos-3000):pos])))
    k=cascadeReg_raw(tape,pos,r)
    if k is not None and k>=7: lastc=(step,pos-origin,k)
    if step>=M1[2]-300: finals.append((step,pos-origin,' '.join(f"{b}^{l}" for b,l in r[:8])))
run(M1[2]+1, hook=hook, hook_from=M1[1]+1)
print(f"g=1  M1(1)@{M1[1]} -> M1(2)@{M1[2]}   (K(1) would be 9, entry expected descIn 8)")
for step,pos,(k,comb,want),lw in hits:
    left=lw[::-1]; i=0
    while i+1<len(left) and left[i]==0 and left[i+1]==1: i+=2
    tag='COMB-OK' if comb>=want else f'comb {comb}<{want}'
    print(f"  {step:>9} (+{step-M1[1]:>7}) descIn {k:<3} pos={pos:<7} comb={comb:<5} {tag}")
    if comb>=want:
        print(f"        marker head: {''.join(map(str,left[i:i+48]))}")
print(f"\n  last cascadeReg k>=7 before M1(2): {lastc}"
      + (f"  -> tail(1) = {M1[2]-lastc[0]}" if lastc else ""))
print("  final E-on-0 configs:")
prev=None
for step,pos,body in finals:
    gap=f"(+{step-prev})" if prev is not None else ""
    prev=step
    print(f"    {step:>9} {gap:>7} pos={pos:>6} | {body}")
