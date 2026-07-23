#!/usr/bin/env python3
"""topRung endpoints (2026-07-23).

g=2: cascadeReg 10 @1 270 303 (LAST CANONICAL)  --1 581 577-->  top @2 851 880  --74--> tail IN
Measure both ends cell-exactly, and the head excursion, and compare with the analogous
g=4 pair once its last canonical level is known.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, check_anchors
assert check_anchors(verbose=False)

def rl(bits,n=16):
    out,i=[],0
    while i<len(bits) and len(out)<n:
        b=bits[i]; j=i
        while j<len(bits) and bits[j]==b: j+=1
        out.append(f"{b}^{j-i}"); i=j
    return ' '.join(out)

PTS={1270303:'g=2 cascadeReg 10  (topRung IN, canonical)',
     2851880:'g=2 top            (topRung OUT, NOT canonical)',
     2851954:'g=2 tail IN'}
snap={}; tr=[]
def hook(step,st,pos,tape,origin):
    if step in PTS:
        snap[step]=(st,pos-origin,bytes(tape[max(0,pos-4200):pos]),tape[pos],bytes(tape[pos+1:pos+4200]))
    if 1270303<=step<=2851880: tr.append(pos-origin)
run(2851955,hook=hook,hook_from=1270303)
print(f"topRung head excursion (g=2): min={min(tr)} max={max(tr)}  start={snap[1270303][1]}")
for s in sorted(PTS):
    st,pos,l,h,r=snap[s]
    L=list(l[::-1])
    print(f"\n--- {PTS[s]}  step={s} st={'ABCDEF'[st]} pos={pos} head={h}")
    print(f"    L RLE: {rl(L)}")
    print(f"    R RLE: {rl(list(r))}")
    print(f"    L first 40 bits: {''.join(map(str,L[:40]))}")
