#!/usr/bin/env python3
"""Where does the ladder stop being CANONICAL?  Find every cascadeReg k (k>=9) in g=4's
phase [M1(4), M1(5)] and full-shape check the left comb."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, check_anchors
assert check_anchors(verbose=False)
LO,HI=11_329_301,44_986_995
def creg(tape,pos,r):
    if len(r)>=4 and r[0]==(0,3) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-3: return k
    return None
rows=[]
def hook(step,st,pos,tape,origin):
    if st!=E or tape[pos]!=0: return
    r=rle(tape,pos,maxruns=48)
    k=creg(tape,pos,r)
    if k is None or k<9: return
    want=(1<<(k-1))-2
    L=[tape[pos-1-i] for i in range(min(2*want+8,pos))]
    c=0;i=0
    while c<want+2 and i+1<len(L) and L[i]==0 and L[i+1]==1: c+=1;i+=2
    rows.append((step,k,c,want))
run(HI+1,hook=hook,hook_from=LO)
print("g=4 phase, cascadeReg k>=9 (ladder top should be k = g+9 = 13):")
for step,k,c,want in rows:
    print(f"  cascadeReg {k:<3} @{step:>10}  comb={c:<6} need={want:<6}  "
          f"{'CANONICAL' if c>=want else '*** NOT CANONICAL ***'}")
