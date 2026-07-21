#!/usr/bin/env python3
"""Examine full leading structure at M1(2) and M1(3) to derive the M1(g) signature."""
from x2t7_lib import run, rle_right

for step in (732733, 2852091):
    _, st, pos, tape, _ = run(step)
    rle = rle_right(tape, pos, limit=40000)
    # show blocks up to and a bit past the big block
    print(f"\n=== step {step} state={st} head={tape[pos]} ===")
    # find index of big block
    bigidx = max(range(len(rle)), key=lambda i: rle[i][1] if rle[i][0]==1 else -1)
    print("big block at rle index", bigidx, "value", rle[bigidx])
    print("leading:", rle[:bigidx+3])
