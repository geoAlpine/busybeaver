#!/usr/bin/env python3
"""T7 COVERAGE (2026-07-22): how much of the doubling phase does RegenLaw ∀k actually cover?

Follow-up to x2t7_recon.py (instrument-validated against M1(1)/M1(2)/M1(3) at steps
188099/732733/2852091 carrying 1^503/1^1021/1^2039).

Question (a): does each `regenIn k` config on the real doubling-phase orbit land on
`cascadeReg k` after EXACTLY `exitSteps k` steps?  That is RegenLaw's transport, and if it
holds on-orbit here then the crux closure applies INSIDE the doubling phase.
Question (b): what fraction of the phase's 2 119 015 raw steps do those transports cover?

`exitSteps k = 2^(2k-3) + k*2^(k-1) + 2^(k-2) + 2`  (lean/X2.lean:4316)
"""
from x2t7_lib import run, classify, E

LO, HI = 732733 + 343, 2852091          # M6(2) .. M1(3)
PHASE = HI - LO


def exitSteps(k):
    return (1 << (2 * k - 3)) + k * (1 << (k - 1)) + (1 << (k - 2)) + 2


hits = []


def hook(step, st, pos, tape):
    if st == E and tape[pos] == 0:
        r = classify(st, pos, tape)
        if r is not None:
            hits.append((step, r[0], r[1]))


print(f"simulating to {HI} and collecting shape hits ...", flush=True)
run(HI, hook=hook)
inside = [h for h in hits if LO <= h[0] <= HI]
print(f"  hits over whole run: {len(hits)};  inside the doubling phase: {len(inside)}")

casc = {}
regen = {}
for step, kind, k in hits:
    (casc if kind == "cascadeReg" else regen).setdefault(k, set()).add(step)

# ---------------------------------------------------------------- (a) exact transport test
print("\n=== (a) does regenIn k --(exitSteps k)--> cascadeReg k hold ON-ORBIT? ===")
print(f"{'k':>3} {'exitSteps k':>12} {'regenIn hits':>13} {'exact lands':>12}  verdict")
paired = {}
for k in sorted(regen):
    es = exitSteps(k)
    rs = sorted(regen[k])
    cs = casc.get(k, set())
    good = [s for s in rs if (s + es) in cs]
    paired[k] = good
    print(f"{k:>3} {es:>12} {len(rs):>13} {len(good):>12}  "
          f"{'ALL' if len(good)==len(rs) else f'{len(good)}/{len(rs)}'}")

print("\n  closed form vs the 5 recorded groundings (exitSteps_grounds, k=4..8):")
for k, want in ((4, 70), (5, 218), (6, 722), (7, 2530), (8, 9282)):
    print(f"    exitSteps({k}) = {exitSteps(k):>6}  recorded {want:>6}  "
          f"{'MATCH' if exitSteps(k)==want else 'MISMATCH'}")

# ---------------------------------------------------------------- (b) coverage
print(f"\n=== (b) coverage of the doubling phase ({PHASE} raw steps) ===")
iv = []
for k, starts in paired.items():
    es = exitSteps(k)
    for s in starts:
        a, b = s, s + es
        if b > LO and a < HI:                      # overlaps the phase
            iv.append((max(a, LO), min(b, HI), k))
iv.sort()
merged = []
for a, b, k in iv:
    if merged and a <= merged[-1][1]:
        merged[-1] = (merged[-1][0], max(merged[-1][1], b))
    else:
        merged.append((a, b))
cov = sum(b - a for a, b in merged)
print(f"  verified transports overlapping the phase: {len(iv)}")
print(f"  merged covered steps: {cov} / {PHASE} = {100.0*cov/PHASE:.2f}%")
print(f"  uncovered: {PHASE-cov} = {100.0*(PHASE-cov)/PHASE:.2f}%")
by_k = {}
for a, b, k in iv:
    by_k[k] = by_k.get(k, 0) + (b - a)
print("  per-level contribution (unmerged):")
for k in sorted(by_k):
    print(f"    k={k:>2}: {by_k[k]:>9} steps  ({100.0*by_k[k]/PHASE:5.2f}%)")

# ---------------------------------------------------------------- structure
print("\n=== nesting structure (are the transports nested or disjoint?) ===")
iv2 = sorted(iv, key=lambda t: (t[0], -(t[1] - t[0])))
top = []
for a, b, k in iv2:
    if top and a >= top[-1][0] and b <= top[-1][1]:
        continue                                    # strictly inside a bigger one
    top.append((a, b, k))
print(f"  maximal (non-nested) transports: {len(top)}")
print(f"  levels present at top: {sorted({k for _,_,k in top})}")
print(f"  => the deep transports CONTAIN the shallow ones (self-similar), so the covered "
      f"mass is carried by the few deepest levels.")
