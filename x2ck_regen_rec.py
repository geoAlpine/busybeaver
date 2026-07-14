#!/usr/bin/env python3
"""x2ck_regen_rec.py -- the EXACT contiguous recursive decomposition of REGEN(k).

REGEN(k) = EXIT(k-1) lays top block 1^{2^k-3}, len=exitSteps(k), TI-proven.
Find, for each REGEN(k) window, which lower REGEN(k') windows and TERM(k') windows
sit CONTIGUOUSLY inside it, to reconstruct REGEN(k) = [pieces] as a Lean recursion.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

EXIT = {3:70,4:218,5:722,6:2530}         # exitSteps by j
# REGEN(k)=EXIT(k-1): REGEN(4)=70,REGEN(5)=218,REGEN(6)=722,REGEN(7)=2530
REGEN = {4:70,5:218,6:722,7:2530}
TERM = {k: 2**(k+1)+k+5 for k in range(3,9)}   # 24,41,74,139,268,...
print("TERM:", TERM)

def anchors(cap=60000):
    sim=build(2); sim.step(); A=[]
    while sim.n<cap:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return A
A = anchors()
Aset=set(A)
def gaps_between(n0,n1):
    xs=[a for a in A if n0<=a<=n1]
    return [xs[i+1]-xs[i] for i in range(len(xs)-1)]

def term_windows(k):
    g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def regen_windows(k):
    L=REGEN[k]; return [(e-L,e) for (s,e) in term_windows(k)]

# canonical REGEN(k) = the FIRST occurrence window
for k in [4,5,6,7]:
    rw = regen_windows(k)
    if not rw: continue
    a,b = rw[0]
    print(f"\n===== REGEN({k}) = [{a},{b}] len={b-a} (block 1^{2**k-3}) =====")
    # list contiguous sub-windows: lower REGENs and their positions
    inside=[]
    for k2 in range(3,k):
        for (s2,e2) in regen_windows(k2) if k2>=4 else []:
            if a<=s2 and e2<=b:
                inside.append((s2,e2,f"REGEN{k2}",e2-s2))
    for k2 in range(3,k+1):
        for (s2,e2) in term_windows(k2):
            if a<=s2 and e2<=b and e2-s2==TERM[k2]:
                inside.append((s2,e2,f"TERM{k2}",e2-s2))
    inside.sort()
    # print the segmentation of [a,b] by these landmarks
    print(" contiguous landmarks (start,end,kind,len):")
    for it in inside:
        print("   ", it)
