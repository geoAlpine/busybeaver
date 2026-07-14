#!/usr/bin/env python3
"""x2ck_regen_seg.py -- TOP-LEVEL segmentation of REGEN(k): the maximal non-overlapping
sub-blocks (lower REGENs + TERM(k)), to test for a ∀k-uniform recursive pattern.

REGEN(k) window = [e-exitSteps(k), e] where e ends a TERM(k) terminal.
Top-level decomposition: greedily take the LARGEST known sub-block at each position.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

REGEN = {4:70,5:218,6:722,7:2530}
TERM = {k: 2**(k+1)+k+5 for k in range(3,9)}

def anchors(cap=60000):
    sim=build(2); sim.step(); A=[]
    while sim.n<cap:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return A
A=anchors()
def term_windows(k):
    g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def regen_windows(k):
    L=REGEN[k]; return [(e-L,e) for (s,e) in term_windows(k)]

# all known blocks by size (largest first): REGEN5,REGEN4=REGEN via len, TERMk
def all_blocks():
    B=[]
    for k in REGEN:
        for (s,e) in regen_windows(k): B.append((s,e,f"REGEN{k}",e-s))
    for k in TERM:
        for (s,e) in term_windows(k): B.append((s,e,f"TERM{k}",e-s))
    return B
BLK=all_blocks()

def top_segment(a,b):
    """greedy left-to-right largest-block cover of [a,b] by anchors."""
    # candidate blocks fully inside [a,b], sorted by start then -len
    cand=[x for x in BLK if a<=x[0] and x[1]<=b]
    seg=[]; pos=a
    while pos<b:
        # largest block starting exactly at pos (that isn't the whole window)
        here=[x for x in cand if x[0]==pos and (x[1]-x[0])<(b-a)]
        if here:
            here.sort(key=lambda x:-(x[1]-x[0]))
            x=here[0]; seg.append(("BLOCK",)+x); pos=x[1]
        else:
            # advance to next anchor; accumulate as "glue"
            nxt=[c for c in A if c>pos]
            np_=min([c for c in cand if c[0]>pos] and [x[0] for x in cand if x[0]>pos] or [b], default=b)
            # find next anchor after pos
            na=[c for c in A if c>pos]
            step_to = na[0] if na and na[0]<b else b
            # but if a block starts before next anchor... just go anchor by anchor
            seg.append(("GLUE",pos,step_to,step_to-pos)); pos=step_to
    return seg

for k in [4,5,6,7]:
    a,b=regen_windows(k)[0]
    print(f"\n===== REGEN({k})=[{a},{b}] len={b-a} block 1^{2**k-3} =====")
    seg=top_segment(a,b)
    # merge consecutive GLUE
    merged=[]
    for s in seg:
        if s[0]=="GLUE" and merged and merged[-1][0]=="GLUE":
            merged[-1]=("GLUE",merged[-1][1],s[2],s[2]-merged[-1][1])
        else: merged.append(list(s) if s[0]=="GLUE" else s)
    tot=0
    for s in merged:
        if s[0]=="BLOCK":
            print(f"   BLOCK {s[3]:>8} len={s[4]}"); tot+=s[4]
        else:
            print(f"   glue  [{s[1]},{s[2]}] len={s[3]}"); tot+=s[3]
    print(f"   sum={tot}")
