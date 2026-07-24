#!/usr/bin/env python3
"""R1 (2026-07-25): measure the top-rung `cascadeReg k` Lc across generations to test whether
odd-g Lc is a g-independent constant (needed for a forall-odd oddSeam).

Scan to ~12M (covers g=1 cReg9, g=2 cReg10, g=3 cReg11). For each k, report the FIRST clean
`cascadeReg k` config (label()-confirmed, state E) with its Lc = combL - (2^{k-1}-2) and marker.
No machine decided. No label upgraded.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, label, check_anchors

assert check_anchors(verbose=False), "instrument FAILED"

seen = {}
def hook(step, st, pos, tape, origin):
    lab = label(tape, pos)
    if lab and lab.startswith('cascadeReg '):
        k = int(lab.split()[1])
        if k not in seen and 9 <= k <= 11:
            cb = comb_left(tape, pos)
            base = (1 << (k - 1)) - 2
            i = pos - 1; n = 0
            while i - 1 >= 0 and tape[i] == 0 and tape[i - 1] == 1:
                n += 1; i -= 2
            mk = ''.join(str(tape[i - d]) for d in range(0, 14))
            seen[k] = (step, st, cb, base, cb - base, mk)

run(12_000_000, hook=hook)

print(f"{'k':>3} {'g(par)':>7} {'step':>10} {'combL':>6} {'2^(k-1)-2':>10} {'Lc':>4}  marker")
gpar = {9: 'g=1 odd', 10: 'g=2 even', 11: 'g=3 odd'}
for k in sorted(seen):
    step, st, cb, base, lc, mk = seen[k]
    print(f"{k:>3} {gpar.get(k,'?'):>7} {step:>10} {cb:>6} {base:>10} {lc:>4}  {mk}")
print("\nPattern: even Lc should be 1 (proven via doubPhaseEven); odd Lc constant => forall-odd oddSeam.")
