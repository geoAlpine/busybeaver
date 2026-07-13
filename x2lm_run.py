#!/usr/bin/env python3
"""x2lm_run.py -- extract the exact per-tile RUN invariant for the forward pass:
config at chain start (n=157) and after each tile (+29k) for g=6, read off L-deposit
and R-consumption so the Lean run-induction lemma can be stated exactly."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaux'.replace('aokiyousuke','aokiyousuke') and '/Users/aokiyousuke/busybeaver')
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def to_M3(g):
    s=build(g); s.step(); mc=0
    while True:
        if s.is_milestone():
            mc+=1
            if mc==2: return s
        if not s.step(): return s

s=to_M3(6)
# advance to n=157 (chain start)
while s.n<157:
    if not s.step(): break
print(f"chain start: n={s.n} st={s.st} pos={s.pos} h={s.h}")
def near(s,kL=16,kR=20):
    left=s.L[::-1][:kL]         # nearest-first
    right=[s.h]+s.R[::-1][:kR]  # head + nearest-first
    return left,right
for k in range(7):
    L,R=near(s)
    print(f" after {k} tiles: pos={s.pos} |L|={len(s.L)} |R|={len(s.R)}")
    print(f"    L nearest-first[:16]={L}")
    print(f"    R head+near[:21]  ={R}")
    # step one tile
    if not all(s.step() for _ in range(29)):
        print("   (halt/short)"); break
