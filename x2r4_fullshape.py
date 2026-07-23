#!/usr/bin/env python3
"""FULL-SHAPE verification (METHODS M1) of regenIn / cascadeReg on the real g=2 orbit.

Earlier checks in this session were PARTIAL:
  cascadeReg -- right side only (the left comb was never checked)
  regenIn    -- the leading ones-run only (the [0,1,0,0,1] + pow01(2^{k-1}-2) was not)

Lean definitions (lean/X2.lean):
  regenIn k p z marker R = <E,p, <ones(2^k-3) ++ [0,1,0,0,1] ++ pow01(2^{k-1}-2) ++ marker,
                                  false, 0 :: descCascade(k-4) ++ zeros z ++ R>>
  cascadeReg k Lc p marker R = <E,p, <pow01(Lc + 2^{k-1}-2) ++ marker, false,
                                  0 0 0 :: ones(2^k-3) ++ 0 0 :: descCascade(k-3) ++ 0 0 :: zeros 7 ++ R>>
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)

def left_bits(tape,pos,n):
    return [tape[pos-1-i] for i in range(min(n,pos))]

def comb_from(L,i,want):
    """count (0,1) pairs in L starting at index i, capped at want; return (count, next_i)"""
    c=0
    while c<want and i+1<len(L) and L[i]==0 and L[i+1]==1:
        c+=1; i+=2
    return c,i

def check_regenIn(tape,pos,k):
    blk=(1<<k)-3; want=(1<<(k-1))-2
    L=left_bits(tape,pos,blk+8+2*want+4)
    if L[:blk]!=[1]*blk: return ('ones-run',0)
    i=blk
    if L[i:i+5]!=[0,1,0,0,1]: return ('separator',0)
    c,_=comb_from(L,i+5,want)
    return ('OK' if c>=want else 'comb', c)

def check_cascadeReg(tape,pos,k):
    want=(1<<(k-1))-2   # with Lc=1 the requirement is 1+want pairs
    L=left_bits(tape,pos,2*(want+2)+4)
    c,_=comb_from(L,0,want+1)
    return ('OK' if c>=want else 'comb', c)

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

bad=[]; tot={'regenIn':0,'cascadeReg':0}
def hook(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    r=rle(tape,pos,maxruns=48)
    k=creg(tape,pos,r)
    if k is not None:
        tot['cascadeReg']+=1
        v,c=check_cascadeReg(tape,pos,k)
        if v!='OK': bad.append(('cascadeReg',k,step,v,c,(1<<(k-1))-2))
        return
    j=regin(tape,pos,r)
    if j is not None:
        tot['regenIn']+=1
        v,c=check_regenIn(tape,pos,j)
        if v!='OK': bad.append(('regenIn',j,step,v,c,(1<<(j-1))-2))

run(2852092, hook=hook, hook_from=733076)
print(f"g=2 phase: {tot['regenIn']} regenIn hits, {tot['cascadeReg']} cascadeReg hits (right-side signature)")
print(f"FULL-SHAPE FAILURES: {len(bad)}")
for what,k,step,why,c,need in bad:
    print(f"  {what} {k} @{step}: {why} -- got {c}, need {need}")
