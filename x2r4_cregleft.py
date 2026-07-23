#!/usr/bin/env python3
"""CRITICAL CHECK (METHODS M1): does the real orbit present cascadeReg's LEFT?

cascadeReg k Lc p marker R  has  left = pow01 (Lc + (2^{k-1} - 2)) ++ marker,
i.e. AT LEAST 2^{k-1} - 2 comb pairs.  Every cascadeReg identification so far in this
session checked the RIGHT side only.  This measures the left comb at each hit.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
def creg(tape,pos,r):
    if len(r)>=4 and r[0]==(0,3) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-3: return k
    return None
def regin(tape,pos,r):
    if len(r)>=2 and r[0]==(0,1):
        d=cascade_at(r,1)
        if d is not None and ones_left(tape,pos)==(1<<(d+4))-3: return d+4
    return None
rows=[]
def hook(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    r=rle(tape,pos,maxruns=48)
    k=creg(tape,pos,r)
    if k is not None:
        rows.append(('cascadeReg',k,step,comb_left(tape,pos),(1<<(k-1))-2))
    else:
        j=regin(tape,pos,r)
        if j is not None:
            # regenIn k left = ones(2^k-3) ++ [0,1,0,0,1] ++ pow01(2^{k-1}-2) ++ marker
            rows.append(('regenIn',j,step,None,None))
run(2852092, hook=hook, hook_from=733076)
print("g=2 doubling phase: every cascadeReg / regenIn hit, with the LEFT comb measured")
print(f"{'what':<12}{'k':<4}{'step':>10}  {'comb_left':>10}  {'needed':>10}   verdict")
for what,k,step,comb,need in rows:
    if what=='cascadeReg':
        v = 'LEFT OK' if comb>=need else '*** LEFT FAILS ***'
        print(f"{what:<12}{k:<4}{step:>10}  {comb:>10}  {need:>10}   {v}")
    else:
        print(f"{what:<12}{k:<4}{step:>10}  {'(left verified: ones(2^k-3))':>40}")
