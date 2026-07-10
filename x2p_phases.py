#!/usr/bin/env python3
"""x2p_phases.py -- segment the orbit into macro-SWEEPS (maximal same-direction head
motions) and label each by (start state, end state, span, net tape change). Goal: see
the true macro-phase alternation -- where the ERASER runs, where the E-SCANNER runs, and
in what ORDER, so the ordering lemma ('eraser completes a block before E traverses it')
can be examined as a phase property, not a radius-local window."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def rs(rr, lo):
    return ' '.join(f"{c}{n}" if n > 1 else f"{c}" for c, n in rr)


def run(maxsteps, dumpfrom, dumpto, SZ=1 << 22):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    # a "sweep" = maximal run of constant direction.
    cur_dir = 0
    sweep_start_step = 0
    sweep_start_pos = pos
    sweep_start_st = st
    def emit(endstep, endpos, endst, d):
        if dumpfrom <= sweep_start_step <= dumpto:
            span = endpos - sweep_start_pos
            print(f"  step{sweep_start_step:>8}..{endstep:<8} "
                  f"{'R' if d>0 else 'L' if d<0 else '.'} span={span:>5} "
                  f"{STN[sweep_start_st]}->{STN[endst]}")
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT step={step}"); return
        act = M[st][r]
        ww, d, ns = act
        if d != cur_dir and cur_dir != 0:
            emit(step, pos, st, cur_dir)
            sweep_start_step = step; sweep_start_pos = pos; sweep_start_st = st
        cur_dir = d
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    run(b + 100000, a, b)
