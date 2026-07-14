#!/usr/bin/env python3
"""x2ck_exit6.py -- EXIT(6)=[12709,15239] gaps; fit exitSteps k-recursion."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def gaps_window(n0, n1):
    sim = build(2); sim.step()
    while sim.n < n0: sim.step()
    A=[]
    while sim.n <= n1:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return [A[i+1]-A[i] for i in range(len(A)-1)]

W = {3:(6638,6708),4:(6923,7141),5:(8076,8798),6:(12709,15239)}
E = {}
for j,(a,b) in W.items():
    g = gaps_window(a,b)
    E[j] = b-a
    print(f"EXIT({j}) steps={b-a} nfold(6s)={sum(1 for x in g if x==6)} terminal={g[-1]}")
print("E =", E)

# Fit E[k] = a*4^k + b*2^k + c*k + d  (4 unknowns, 4 points k=3,4,5,6)
import itertools
def solve():
    ks=[3,4,5,6]; ys=[E[k] for k in ks]
    # build matrix
    M=[[4**k,2**k,k,1] for k in ks]
    # gaussian elim (rationals via fractions)
    from fractions import Fraction as Fr
    A=[[Fr(x) for x in row]+[Fr(ys[i])] for i,row in enumerate(M)]
    n=4
    for i in range(n):
        p=A[i][i]
        if p==0:
            for r in range(i+1,n):
                if A[r][i]!=0: A[i],A[r]=A[r],A[i]; p=A[i][i]; break
        A[i]=[x/p for x in A[i]]
        for r in range(n):
            if r!=i and A[r][i]!=0:
                f=A[r][i]; A[r]=[A[r][c]-f*A[i][c] for c in range(n+1)]
    return [A[i][n] for i in range(n)]
coef = solve()
print("fit a*4^k+b*2^k+c*k+d, coef(a,b,c,d)=", coef)
# verify + predict EXIT(7)
a,b,c,d = coef
for k in [3,4,5,6,7]:
    v = a*4**k+b*2**k+c*k+d
    print(f"  k={k}: fit={v} actual={E.get(k)}")

# Also test a k-recursion: E[k] = 2*E[k-1] + FOLD-terms + TERM(k+?)
print("\nrecursion residuals E[k]-2E[k-1]:")
for k in [4,5,6]:
    print(f"  k={k}: {E[k]-2*E[k-1]}")
