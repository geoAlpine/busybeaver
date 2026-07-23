#!/usr/bin/env python3
"""R2: locate M1(4) and the cascadeReg 12 immediately before it (the tail(3) episode)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2t7_lib import run, E, SPAN, ORIGIN
from x2r2_tail import rle, comb_left, ones_left, label

LO, HI = 11_500_000, 14_500_000
hits = []
def hook(step, st, pos, tape):
    if st != E or tape[pos] != 0:
        return
    # cheap pre-filter for the milestone: a long run of 0s immediately left
    if tape[pos-40:pos] == bytearray(40):
        if 1 not in tape[:pos]:
            hits.append((step, pos - ORIGIN, 'MILESTONE', None))
            return
    r = rle(tape, pos)
    lb = label(r, comb_left(tape, pos), ones_left(tape, pos))
    if lb and lb.startswith('cascadeReg 1'):
        hits.append((step, pos - ORIGIN, lb, ' '.join(f"{b}^{l}" for b,l in r[:6])))

n, st, pos, tape, halted = run(HI, hook=hook, hook_from=LO)
print(f"scanned [{LO},{HI}] halted={halted}; hits={len(hits)}")
prev=None
for step, pos, lb, body in hits:
    gap = f"(+{step-prev})" if prev is not None else ""
    prev = step
    print(f"{step:>10} {gap:>10} pos={pos:>7} {lb}   {body or ''}")
