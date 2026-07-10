#!/usr/bin/env python3
"""x2c_milestone.py -- dump the FULL tape RLE (finite support) each time the head reaches a
new rightward record while in a rightward growth state, to read the exact cascade grammar
of the reachable 'rest' configurations. Also dump the RLE just before/after the head turns
around at the right frontier (where new structure is created)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def rs(rr):
    return ' '.join(f"{c}^{n}" if n > 1 else f"{c}" for c, n in rr)


def run(maxsteps, SZ=1 << 22):
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st = 0
    step = 0
    lo = hi = pos
    # record the config each time the tape's rightmost 1 advances (a growth milestone):
    # i.e. when we are about to turn around at the far right. We detect a right-turn as
    # a move R followed by ... simpler: sample when state is C reading 0 far right (turnaround
    # C:0->0LD moves left). Dump the RLE of the whole finite structure.
    last_dump_hi = 0
    dumps = 0
    while step < maxsteps and dumps < 25:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"HALT step={step}")
            return
        ww, d, ns = act
        # detect right frontier turnaround: currently moving into background 0 and will go left
        # Turnaround happens at state C reading 0 (C:0->0LD) which is the rightmost point.
        if st == 2 and r == 0 and pos > last_dump_hi + 3:
            # full finite support: leftmost..rightmost nonzero
            L0 = lo
            while L0 < pos and tape[L0] == 0:
                L0 += 1
            rr = rle(tape, L0, pos - 1)
            print(f"[turn @ step={step:>9} width={pos-L0:>7}]  {rs(rr)} [C]0")
            last_dump_hi = pos
            dumps += 1
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    run(cap)
