#!/usr/bin/env python3
"""Find the largest g-independent PREFIX of the low phase (fixed entry tile)
that is provable forall g as a tail-parametric transport, and pin the exact
step where g-dependence begins (head first reads a cell that differs across g)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def trace(g, N):
    sim=build(g)
    out=[]
    for _ in range(N):
        out.append((sim.n, sim.st, sim.pos, sim.h))
        if not sim.step(): break
    out.append((sim.n, sim.st, sim.pos, sim.h))
    return out

# M1(g) register prefixes: all share 0^22, then (1 0^6)^{g-1}.
# g=2: 0^22 1 0^6 [1 0^10]      -> divergence at the token AFTER first 1 0^6
# g>=3: 0^22 1 0^6 [1 0^6] ...
# Compare full step-by-step state/pos across g to find first divergence.
Tg = {g: trace(g, 120) for g in [2,3,4,5]}
maxlen = min(len(Tg[g]) for g in Tg)
div = None
for i in range(maxlen):
    vals = set((Tg[g][i][1], Tg[g][i][2]) for g in Tg)  # (state,pos)
    if len(vals) != 1:
        div = i; break
print("first (state,pos) divergence across g=2..5 at index", div)
if div is not None:
    for g in Tg:
        print(f"  g={g}: n={Tg[g][div][0]} st={Tg[g][div][1]} pos={Tg[g][div][2]} head={Tg[g][div][3]}")
    print("  step before divergence:")
    for g in Tg:
        print(f"  g={g}: n={Tg[g][div-1][0]} st={Tg[g][div-1][1]} pos={Tg[g][div-1][2]} head={Tg[g][div-1][3]}")

# also: rightmost reach vs step, and which register position first differs
# max pos reached in first K steps for each g
for K in [15,46,60,80,100]:
    reach = {g: max(p for (_,_,p,_) in Tg[g][:K]) for g in Tg}
    print(f"first {K} steps rightmost reach: {reach}")
