#!/usr/bin/env python3
"""
o13/o14 fixed-point deep dive, part 1: INSTRUMENT the milestone dynamics (2026-07-08).
Run the blank-tape orbit; dump the milestone (extreme + designated state) RLE chain,
decoded into counters, to reverse-engineer the exact rule system to o11-depth.

o13  1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA  milestone: state C, L-extreme
o14  1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE  milestone: state E, L-extreme
"""
import sys
from msea_struct2 import parse, rle_blocks

MACH = {
    "o13": ("1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 2, 'L'),
    "o14": ("1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 4, 'L'),
}
SN = "ABCDEF"

def milestones(spec, mstate, side, N, maxsnap=200):
    M = parse(spec)
    SZ = 1 << 23
    tape = bytearray(SZ)
    pos = SZ // 2
    st = 0
    lo = hi = pos
    snaps = []
    last = None
    step = 0
    while step < N and len(snaps) < maxsnap:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            snaps.append((step, 'HALT'))
            break
        at_ext = (pos <= lo) if side == 'L' else (pos >= hi)
        if st == mstate and at_ext:
            b = rle_blocks(tape, lo, hi)
            if b != last:
                snaps.append((step, b))
                last = list(b)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return snaps

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    for name in ("o13", "o14"):
        spec, ms, side = MACH[name]
        snaps = milestones(spec, ms, side, N, maxsnap=120)
        print(f"===== {name}: milestone chain (state {SN[ms]}, {side}-extreme), N={N}")
        for s, b in snaps:
            print(f"  t={s:>10}  {b}")
        print()
