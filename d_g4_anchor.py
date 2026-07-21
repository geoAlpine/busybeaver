#!/usr/bin/env python3
"""Anchor check: reproduce M1(1)@188099/1^503, M1(2)@732733/1^1021, M1(3)@2852091/1^2039."""
from x2t7_lib import run, classify, E, rle_right, ones_run_left

anchors = [(188099, 503), (732733, 1021), (2852091, 2039)]

def check(step, expect_ones):
    _, st, pos, tape, halted = run(step)
    # after `step` steps, state/pos/tape are the configuration
    left = ones_run_left(tape, pos)
    rle = rle_right(tape, pos, limit=6000)
    print(f"step={step}: state={st} tape[pos]={tape[pos]} left_ones={left} expect={expect_ones}")
    print(f"   rle_right head: {rle[:6]}")
    return st, left

for step, ones in anchors:
    check(step, ones)
