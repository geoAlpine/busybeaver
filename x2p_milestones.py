#!/usr/bin/env python3
"""x2p_milestones.py -- dump the full RLE of the tape at each MILESTONE (head in state E,
reading 0, strictly LEFT of every 1) so the odometer's macro-evolution is visible. Also
dump the leading gap G and the maximal gap the E-scanner will hit on the coming sweep."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def rs(rr):
    return ' '.join(f"{c}{n}" if n > 1 else f"{c}" for c, n in rr)


def run(maxsteps, nmile, SZ=1 << 23):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    left1 = SZ
    count = 0
    while step < maxsteps and count < nmile:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        if st == 4 and r == 0 and pos < left1 and left1 <= hi:
            G = left1 - pos
            rr = rle(tape, left1, hi)
            print(f"m{count:>3} step={step:>9} G={G:>3}  [E]0^{G} " + rs(rr))
            count += 1
        act = M[st][r]
        ww, d, ns = act
        if ww == 1:
            if pos < left1: left1 = pos
        else:
            if pos == left1:
                k = pos + 1
                while k <= hi and tape[k] == 0: k += 1
                left1 = k if k <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    run(200_000_000, n)
