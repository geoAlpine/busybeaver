#!/usr/bin/env python3
"""R2 (2026-07-23): tail(3) -- cascadeReg 12 -> M1(4).

M1(4) is near M6(3) + 8.43M ~ 11.28M (design doc's g=3 phase cost).  Scan a generous window
and report every E-on-0 config that is a cascadeReg, plus the milestone (no 1 left of head).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2t7_lib import run, E, SPAN, ORIGIN
from x2r2_tail import rle, comb_left, ones_left, label

WLO, WHI = 11_150_000, 11_500_000
rows = []


def hook(step, st, pos, tape):
    if step < WLO or st != E or tape[pos] != 0:
        return
    r = rle(tape, pos)
    lb = label(r, comb_left(tape, pos), ones_left(tape, pos))
    ms = (1 not in tape[:pos])
    if lb or ms:
        rows.append((step, pos - ORIGIN, lb, ms, r))


run(WHI, hook=hook, hook_from=WLO)
print(f"window [{WLO}, {WHI}]: {len(rows)} hits")
prev = None
for step, pos, lb, ms, r in rows:
    gap = f"(+{step - prev})" if prev is not None else ""
    prev = step
    body = ' '.join(f"{b}^{l}" for b, l in r[:8])
    mark = ('  <<< ' + lb) if lb else ''
    mark += '  *** MILESTONE (no 1 to the left) ***' if ms else ''
    print(f"{step:>9} {gap:>9} pos={pos:>6} | {body}{mark}")
