#!/usr/bin/env python3
"""R2: locate cascadeReg 12 and M1(4) (tail(3)).  g=3's ladder tops at cascadeReg(3+9)=12."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2t7_lib import run, E, SPAN, ORIGIN

LO, HI = 19_000_000, 22_000_000
def rle(tape,pos,limit=60000,maxruns=12):
    out,i=[],pos+1; end=min(pos+1+limit,2*SPAN)
    while i<end and len(out)<maxruns:
        b=tape[i]; j=i
        while j<end and tape[j]==b: j+=1
        out.append((b,j-i)); i=j
    return out
def casc(d): return [(1<<(j+2))-3 for j in range(d,0,-1)]+[1]
def cascade_at(r,s):
    for d in range(11,0,-1):
        want,ok,i=casc(d),True,s
        for bi,bl in enumerate(want):
            if i>=len(r) or r[i][0]!=1 or r[i][1]!=bl: ok=False;break
            i+=1
            if bi<len(want)-1:
                if i>=len(r) or r[i]!=(0,2): ok=False;break
                i+=1
        if ok: return d
    return None
hits=[]
def hook(step,st,pos,tape):
    if st!=E or tape[pos]!=0: return
    if tape[pos-40:pos]==bytearray(40) and 1 not in tape[:pos]:
        hits.append((step,pos-ORIGIN,'*** M1 MILESTONE ***','')); return
    r=rle(tape,pos)
    if len(r)>=4 and r[0]==(0,3) and r[1][0]==1 and r[2]==(0,2):
        blk=r[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and cascade_at(r,3)==k-3 and k>=11:
            hits.append((step,pos-ORIGIN,f'cascadeReg {k}',' '.join(f"{b}^{l}" for b,l in r[:5])))
run(HI,hook=hook,hook_from=LO)
print(f"scanned [{LO},{HI}] hits={len(hits)}")
prev=None
for step,pos,lb,body in hits:
    gap=f"(+{step-prev})" if prev is not None else ""
    prev=step
    print(f"{step:>10} {gap:>10} pos={pos:>7} {lb}   {body}")
