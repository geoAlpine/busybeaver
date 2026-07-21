#!/usr/bin/env python3
"""Verify max 1-block on tape at each anchor step, and full leading structure."""
from x2t7_lib import run, rle_right, ones_run_left

anchors = [(188099, 503), (732733, 1021), (2852091, 2039)]

for step, ones in anchors:
    _, st, pos, tape, _ = run(step)
    rle = rle_right(tape, pos, limit=40000)
    maxblk = max((l for b, l in rle if b == 1), default=0)
    lead0 = rle[0] if rle else None
    print(f"step={step} state={st} head={tape[pos]} lead={lead0} maxblock(1)={maxblk} expect={ones}  match={maxblk==ones}")
