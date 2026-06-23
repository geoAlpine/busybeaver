import math
from collections import Counter
# The unified kernel as a (x2,x3) / solenoid object. We need (for Antihydra) only ONE-SIDED density>1/3,
# not full equidistribution. Test what the (x2,x3) structure could give.
#
# Furstenberg topological: a closed S-invariant (S=<x2,x3>) infinite subset of R/Z is all of R/Z.
# Our orbit point: t_n = {(3/2)^n}. Is {t_n} contained in / generating a x2,x3-structure?
# (3/2)^n = 3^n 2^{-n}: applying x2 -> 3^n 2^{-(n-1)} = (3/2)^n * 2 ; x3 -> (3/2)^n*3. So the orbit
# {(3/2)^n} sits inside the x2,x3 ORBIT of any single t_m. Check density of the x2,x3 orbit of t_1.

# 1) the x2,x3 orbit closure of a point: numerically, is {2^a 3^b t mod 1} dense? (Furstenberg => yes if t irrational)
import random
t=( (3*3*3)/(2*2*2) )%1.0  # (3/2)^3
pts=set()
# BFS apply x2,x3
frontier=[t]; allp=[t]
for _ in range(18):
    nf=[]
    for x in frontier:
        for m in (2,3):
            y=(m*x)%1.0
            allp.append(y); nf.append(y)
    frontier=nf[:400]
allp=[round(x,4) for x in allp]
binc=Counter(int(x*20) for x in allp)
print("x2,x3 orbit of (3/2)^3: occupancy of 20 bins:", sorted(binc.keys()))
print(f"  => fills {len(binc)}/20 bins (Furstenberg: dense; but DENSE != equidistributed)")

# 2) the ACTUAL need: even-density of c_{n+1}=floor(3c/2). Can a one-sided bound come from a CONSERVED
# quantity? Test: is there any modular invariant making density provable? Check parity-run structure.
c=8; runs=[]; cur=None; ln=0
parity=[]
for n in range(200000):
    p=c%2; parity.append(p); c=3*c//2
# distribution of run-lengths of consecutive ODD (the depth that must stay o(n))
oddruns=[]; k=0
for p in parity:
    if p==1: k+=1
    else:
        if k>0: oddruns.append(k)
        k=0
print(f"\nAntihydra parity: even-density={1-sum(parity)/len(parity):.4f}")
print(f"  odd-run lengths: max={max(oddruns)} mean={sum(oddruns)/len(oddruns):.3f} (depth=o(n) needs max-run=o(n))")
rc=Counter(oddruns)
print(f"  odd-run length distribution (geometric? P(len=k)~2^-k): {[(k,rc[k]) for k in range(1,8)]}")
# if odd-runs are geometric with ratio 1/2, max run ~ log2(n) = o(n) -> non-halt. Check ratio.
for k in range(1,6):
    if rc[k+1]>0: print(f"    ratio P(k={k+1})/P(k={k}) = {rc[k+1]/rc[k]:.3f} (geometric->0.5)")
