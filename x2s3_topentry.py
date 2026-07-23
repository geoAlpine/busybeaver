#!/usr/bin/env python3
"""S3 (METHODS_2026-07-24, M0/M1): structure of the EVEN topEntry  M6(g) -> descIn(K-1).

Closed form (derived from the confirmed M1(g)->entry forms minus h_low_even N(g)=267+38g):
    even:  M6(g) -> descIn(g+7)  costs  384*2^g + 15g + 117
    g=2: 1683   g=4: 6321   g=6: 24783   g=8: 98541
Windows: M6(g) = M1(g) + (267+38g) for even g.
This dumps every E-on-0 config in the g=2 and g=4 windows to expose repeated structure.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False), "INSTRUMENT CHECK FAILED (METHODS M1)"

M1s = {2: 732733, 4: 11329301}
W = {}
for g, m in M1s.items():
    lo = m + 267 + 38 * g
    W[g] = (lo, lo + 384 * 2 ** g + 15 * g + 117)
print("windows:", {g: (a, b, b - a) for g, (a, b) in W.items()})

rows = {g: [] for g in W}
def hook(step, st, pos, tape, origin):
    if st != E or tape[pos] != 0:
        return
    for g, (a, b) in W.items():
        if a <= step <= b:
            r = rle(tape, pos, maxruns=10)
            rows[g].append((step, pos - origin, comb_left(tape, pos), ones_left(tape, pos),
                            ' '.join(f"{x}^{y}" for x, y in r)))

run(max(b for _, b in W.values()) + 1, hook=hook, hook_from=min(a for a, _ in W.values()))

for g in sorted(W):
    a, b = W[g]
    print(f"\n===== g={g}: M6({g})@{a} -> descIn({g+7})@{b}  ({b-a} steps, {len(rows[g])} E-on-0 configs) =====")
    prev = None
    for step, pos, comb, ol, body in rows[g][:40]:
        gap = f"(+{step-prev})" if prev is not None else ""
        prev = step
        print(f"  {step:>9} {gap:>7} pos={pos:>6} comb={comb:<5} ones_l={ol:<5} | {body}")
    if len(rows[g]) > 40:
        print(f"  ... ({len(rows[g])-40} more)")
