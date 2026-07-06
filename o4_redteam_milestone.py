#!/usr/bin/env python
# RED TEAM: pin down the exact milestone convention M(G,a) from the REAL o4 orbit.
# Detect generation boundaries = head strictly left of all support; dump state, gap, filler.
from collections import defaultdict

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

tape=defaultdict(int); pos=0; st='A'
support=set()
N=2_000_000
best=[]
prev_boundary=False
for s in range(N):
    r=tape[pos]; a=M[(st,r)]
    if a is None: print("HALT at",s); break
    # boundary check BEFORE step: head strictly left of support
    if support:
        mn=min(support); mx=max(support)
        if pos<mn:
            gap=mn-pos
            # only record record-breaking gaps (clean milestone = max gap moment)
            if not best or gap>best[-1][2]:
                filler=''.join(str(tape[i]) for i in range(mn,mx+1))
                best.append((s,st,gap,pos,filler))
    w,d,ns=a
    if w==0:
        tape.pop(pos,None); support.discard(pos)
    else:
        tape[pos]=1; support.add(pos)
    pos+=d; st=ns

for s,stt,gap,p,f in best:
    # try to parse filler as (10)^a 1001
    a=None
    if f.endswith('1001') and len(f)>=4:
        body=f[:-4]
        if len(body)%2==0 and all(body[i:i+2]=='10' for i in range(0,len(body),2)):
            a=len(body)//2
    print(f"step={s:>8} state={stt} gap={gap} head={p} filler_len={len(f)} a={a} filler={f if len(f)<70 else f[:66]+'...'}")
