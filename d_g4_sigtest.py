#!/usr/bin/env python3
"""Test hypothesis: M1(g) = unique E-on-0 config with leading gap exactly (0,21)
carrying a big 1-block, in a window around the milestone.
If unique at M1(2) and M1(3), then 11329301 is confirmed M1(4)."""
from x2t7_lib import run, rle_right

def scan(lo, hi, minblk):
    hits = []
    def hook(step, st, pos, tape):
        if step < lo: return
        if st == 4 and tape[pos] == 0:
            rle = rle_right(tape, pos, limit=20000)
            if rle and rle[0] == (0, 21):
                mb = max((l for b, l in rle if b == 1), default=0)
                if mb >= minblk:
                    hits.append((step, mb, tuple(rle[:4])))
    run(hi, hook=hook, hook_from=lo)
    return hits

for label, lo, hi, minblk in (
    ("M1(2)", 700_000, 780_000, 900),
    ("M1(3)", 2_800_000, 2_910_000, 1900),
    ("M1(4)", 11_250_000, 11_400_000, 4000),
):
    h = scan(lo, hi, minblk)
    print(f"{label}: {len(h)} config(s) with leading (0,21) & bigblock>={minblk}:")
    for x in h:
        print("   ", x)
