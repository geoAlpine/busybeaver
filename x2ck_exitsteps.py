#!/usr/bin/env python3
"""x2ck_exitsteps.py -- nail down the EXIT(j) step-count recursion & terminal law.

Extract EXIT windows at j=3,4,5,6 from build(2), confirm step counts 70/218/722/?,
and test the k-indexed recursion exitSteps(k) = TERM(k) + REGEN(k-1)-shaped sum.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def left_solid(sim):
    L = sim.L; i = 0
    while i < len(L) and L[-1 - i] == 1:
        i += 1
    return i


def anchors(n0, n1):
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    A = []
    while sim.n <= n1:
        if sim.st == 'E' and sim.h == 0:
            A.append((sim.n, left_solid(sim), sim.left_ones(), sim.right_runs(8)))
        if not sim.step():
            break
    return A


EXITS = {3: (6638, 6708), 4: (6923, 7141), 5: (8076, 8798)}

# find EXIT(6): the CORE at level-6 deposits 1^{2^6-4}=1^124 then EXIT(6) regenerates.
# Terminal g268 lays 1^125 (k=7). We know EXIT6 has a k=5 terminal (g74) at 13379.
# Scan for the level-6 EXIT window: after the sweepEF for 1^124.


def find_exit6():
    sim = build(2); sim.step()
    # Collect E-on-0 anchors and track big left-solid jumps (a CORE just doubled).
    prev = None
    hist = []
    while sim.n < 40000:
        if sim.st == 'E' and sim.h == 0:
            ls = left_solid(sim)
            hist.append((sim.n, ls))
        if not sim.step():
            break
    # EXIT(6) begins right after the level-6 CORE deposits ~1^124 (2^7-4=124).
    # find anchor where lsolid jumps to ~124
    for i, (n, ls) in enumerate(hist):
        if 118 <= ls <= 130:
            print(f"  candidate CORE-exit start: n={n} lsolid={ls}")
    return hist


for j, (n0, n1) in EXITS.items():
    A = anchors(n0, n1)
    print(f"EXIT({j}) [{n0},{n1}] = {n1-n0} steps, {len(A)} anchors")
    gaps = [A[i+1][0]-A[i][0] for i in range(len(A)-1)]
    print(f"   gaps: {gaps}")
    print(f"   last gap (terminal): {gaps[-1] if gaps else None}")

print("\nStep counts:", {j: n1-n0 for j,(n0,n1) in EXITS.items()})

# recursion hypothesis test
E = {3:70, 4:218, 5:722}
# EXIT(j) = DESCENT-FOLD(2^{j-2}-2)*6  +  REGEN(j-1)
# where REGEN(j-1) resembles a carry at scale j-1.
print("\nDescent-fold opening steps (2^{j-2}-2)*6:")
for j in (3,4,5,6):
    folds = 2**(j-2)-2
    print(f"  j={j}: folds={folds}, fold-steps={6*folds}")

print("\nTerminal TERM(k)=2^{k+1}+k+5:")
for k in (4,5,6,7):
    print(f"  k={k}: TERM={2**(k+1)+k+5}, block=1^{2**k-3}")

print("\n--- searching exitSteps recursion vs 70,218,722 ---")
# Try: exitSteps(k) where k is block level. EXIT(3)->k=4 terminal, EXIT(4)->k=5, EXIT(5)->k=6
# hypothesis: exitSteps(j) = 6*(2^{j-2}-2) + [regen at j-1] + TERM(j+1)
for j in (3,4,5):
    fold = 6*(2**(j-2)-2)
    term = 2**((j+1)+1)+(j+1)+5   # TERM(j+1)
    print(f"  j={j}: total={E[j]}, fold={fold}, TERM(j+1)={term}, residual(regen+glue)={E[j]-fold-term}")

find_exit6()
