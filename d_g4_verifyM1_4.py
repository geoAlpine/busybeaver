#!/usr/bin/env python3
"""Verify M1(4)=11329301 has the canonical M1(g) structure (compare to M1(3))."""
from x2t7_lib import run, rle_right

for label, step in (("M1(3)", 2852091), ("M1(4)", 11329301)):
    _, st, pos, tape, _ = run(step)
    rle = rle_right(tape, pos, limit=40000)
    bigidx = max(range(len(rle)), key=lambda i: rle[i][1] if rle[i][0]==1 else -1)
    mb = rle[bigidx][1]
    print(f"\n{label} step={step} state={st} head={tape[pos]} bigblock={mb} at idx {bigidx}")
    print("  full leading+bigblock+2:", rle[:bigidx+3])
