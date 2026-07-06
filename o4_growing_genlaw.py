# o4 growing-regime GENERATION-LAW extractor (2026-07-07)
# The probe (o4_growing_probe.py) shows all three open configs Z(k,3,0), k in {21,23,27},
# collapse to the single-segment family
#     C(m) := 0^inf [head, state A, on 0] (10)^m 0 1 0^inf
# (equivalently (10)^(m-1) 1 0 0 1 with the head one cell LEFT of the block, state A).
# This script: (1) runs standalone C(m) until it returns to the exact C(m') shape with the
# head at a new leftmost cell, recording (m -> m', left shift, steps); (2) reports the map
# on a grid of m to find the generation law; (3) re-runs the three Z configs to find the
# exact step/shape at which each first ENTERS the C-family (the concrete handoff point).
from collections import defaultdict
import sys

def parse(spec):
    M={}
    for kk,blk in enumerate(spec.split('_')):
        st="ABCDEF"[kk]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def build_C(m):
    """tape for C(m), head at -1 (on 0), state A: cells 0..2m-1=(10)^m, 2m=0, 2m+1=1."""
    t={}
    for i in range(m): t[2*i]=1
    t[2*m+1]=1
    return t

def is_C(tape, pos):
    """check tape (dict of 1-cells) is exactly (10)^m 0 1 starting at pos+1; return m or None."""
    ones=sorted(c for c,v in tape.items() if v)
    if not ones: return None
    if ones[0]!=pos+1: return None
    # ones must be pos+1, pos+3, ..., pos+2m-1, then gap, then pos+2m+2... wait last is 0 1
    # cells: pos+1..pos+2m = (10)^m -> ones at pos+1,pos+3,...,pos+2m-1 ; cell pos+2m+1=0, pos+2m+2=1
    last=ones[-1]
    body=ones[:-1]
    mm=len(body)
    for i,c in enumerate(body):
        if c!=pos+1+2*i: return None
    if last!=pos+1+2*mm+1: return None   # = pos+2m+2
    return mm

def gen_step(m, maxsteps=10**8):
    """run from C(m) (head at -1, state A) to the next exact C(m') at a new leftmost; return stats."""
    tape=defaultdict(int,build_C(m)); pos=-1; st='A'
    lo=-1; hi=2*m+1; unsafe=0
    for s in range(1,maxsteps+1):
        r=tape[pos]; tr=M[(st,r)]
        if tr is None: return dict(halt=True, steps=s)
        w,d,ns=tr
        if st=='B' and r==1 and tape.get(pos+1,0)==1: unsafe+=1
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos>hi: hi=pos
        if pos<lo:
            lo=pos
            if st=='A' and tape.get(pos,0)==0:
                mm=is_C(tape,pos)
                if mm is not None:
                    return dict(halt=False, m2=mm, shift=-1-pos, steps=s, hi=hi, unsafe=unsafe)
    return dict(halt=False, m2=None, steps=maxsteps)

def find_entry(k, horizon=200000):
    """run Z(k,3,0); return first step at which the config is exactly C(m) at a new leftmost."""
    def build_Z(k,g,a):
        t={}
        for i in range(k): t[2*i]=1
        t[2*k]=1; t[2*k+3]=1
        base=2*k+4+g
        for i in range(a): t[base+2*i]=1
        t[base+2*a]=1; t[base+2*a+3]=1
        return t
    tape=defaultdict(int,build_Z(k,3,0)); pos=0; st='E'; lo=0
    for s in range(1,horizon+1):
        r=tape[pos]; tr=M[(st,r)]
        if tr is None: return ('HALT',s)
        w,d,ns=tr
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos<lo:
            lo=pos
            if st=='A' and tape.get(pos,0)==0:
                mm=is_C(tape,pos)
                if mm is not None:
                    return ('ENTER', s, pos, mm)
    return ('NOENTRY',)

if __name__=='__main__':
    print('=== generation map on the standalone family C(m) ===')
    print('   m ->  m\'   shift  steps      hi     unsafe')
    grid=list(range(6,61,2))+list(range(6,61))  # both parities + fine sweep
    grid=sorted(set(list(range(4,40))+[50,51,100,101,200,201,500,501,1000,1001]))
    rows={}
    for m in grid:
        r=gen_step(m)
        if r.get('halt'):
            print(f'  m={m}: HALT at {r["steps"]}')
            continue
        rows[m]=r
        print(f'  m={m:>5} -> {r["m2"]:>5}  shift={r["shift"]:>3}  steps={r["steps"]:>8}  hi={r["hi"]:>6}  unsafe={r["unsafe"]}')
    print()
    print('=== entry of the three Z configs into the C-family ===')
    for k in (21,23,27):
        print(f'  Z({k},3,0):', find_entry(k))
