#!/usr/bin/env python3
"""Locate M1(4): scan window near 11.33M for E-on-0 configs with a big 1-block.
Record the maxblock over the window to find where it peaks (the milestone)."""
from x2t7_lib import run, rle_right

LO, HI = 11_250_000, 11_400_000
hits = []

def hook(step, st, pos, tape):
    if step < LO:
        return
    if st == 4 and tape[pos] == 0:
        rle = rle_right(tape, pos, limit=20000)
        if not rle:
            return
        mb = max((l for b, l in rle if b == 1), default=0)
        if mb >= 4000:
            lead = rle[0]
            # capture leading prefix signature
            hits.append((step, mb, lead, tuple(rle[:6])))

run(HI, hook=hook, hook_from=LO)
print(f"found {len(hits)} E-on-0 configs with maxblock>=4000 in [{LO},{HI}]")
for step, mb, lead, pref in hits[:40]:
    print(f"  step={step} maxblock={mb} lead={lead} pref={pref}")
