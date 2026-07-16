#!/usr/bin/env python3
"""x2dt_tree8.py -- exact tree-sum expression for REGEN(k), k=5..8, in the style of the
existing exitSteps_tree_5/6/7 Lean lemmas (landmarks REGEN(k')/TERM(k'), merged glue).
Confirms k=5,6,7 reproduce the existing lemmas, and emits the k=8 identity + arity table.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def exitSteps(k): return 2**(2*k-3)+k*2**(k-1)+2**(k-2)+2
def termSteps(k): return 2**(k+1)+k+5
REGEN={k:exitSteps(k) for k in range(4,9)}
TERM ={k:termSteps(k) for k in range(3,10)}

def anchors(cap):
    sim=build(2); sim.step(); A=[]
    while sim.n<cap:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return A
A=anchors(46000)
def term_windows(k):
    g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def regen_windows(k):
    L=REGEN[k]; return [(e-L,e) for (s,e) in term_windows(k)]

def tree_expr(k):
    a,b=regen_windows(k)[0]
    RB=[(s,e,('R',kk)) for kk in range(4,k) for (s,e) in regen_windows(kk) if a<=s and e<=b and e-s<b-a]
    TB=[(s,e,('T',kk)) for kk in range(3,k+1) for (s,e) in term_windows(kk) if a<=s and e<=b and e-s<b-a]
    landmarks=sorted(RB+TB)
    # greedy: walk pos, pick landmark starting at pos with largest length (REGEN>TERM by size)
    terms=[]; pos=a; glue=0
    while pos<b:
        cands=[x for x in landmarks if x[0]==pos]
        if cands:
            cands.sort(key=lambda x:-(x[1]-x[0])); x=cands[0]
            if glue: terms.append(('g',glue)); glue=0
            terms.append(x[2]); pos=x[1]
        else:
            na=[c for c in A if c>pos and c<=b]
            nxt=na[0] if na else b
            glue+=nxt-pos; pos=nxt
    if glue: terms.append(('g',glue))
    return terms

def render(terms):
    parts=[]; total=0
    for t in terms:
        if t[0]=='g': parts.append(str(t[1])); total+=t[1]
        elif t[0]=='T': parts.append(f"termSteps {t[1]}"); total+=termSteps(t[1])
        elif t[0]=='R': parts.append(f"exitSteps {t[1]}"); total+=exitSteps(t[1])
    return " + ".join(parts), total

for k in range(5,9):
    terms=tree_expr(k)
    expr,total=render(terms)
    arity=sum(1 for t in terms if t[0]=='R')
    calls=[t[1] for t in terms if t[0]=='R']
    print(f"REGEN({k}): exitSteps {k} = {expr}")
    print(f"   check total={total} exitSteps({k})={exitSteps(k)}  MATCH={total==exitSteps(k)}  arity={arity} calls={calls}")

print("\narity table k=5..8:",[sum(1 for t in tree_expr(k) if t[0]=='R') for k in range(5,9)])
print("closed-form (k-5)(k-4)/2:",[(k-5)*(k-4)//2 for k in range(5,9)])
