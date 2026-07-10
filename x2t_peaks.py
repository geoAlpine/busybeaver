#!/usr/bin/env python3
"""x2t_peaks.py -- capture the FULL configuration (state, head offset within structure,
tape RLE) at each maxrun-record ('super-peak') event, to read the self-similar milestone
form M(n) of the integer-x2 odometer 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def rs(rr):
    return ' '.join(f"{c}^{n}" if n > 1 else f"{c}" for c, n in rr)


def run(maxsteps, SZ=1 << 22):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    best = 0
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT step={step}"); return
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        # detect current maxrun cheaply only occasionally: when head far right in state C reading0
        if st == 2 and tape[pos] == 0 and pos > off:
            L0 = lo
            while L0 < pos and tape[L0] == 0: L0 += 1
            R0 = hi
            while R0 > pos and tape[R0] == 0: R0 -= 1
            rr = rle(tape, L0, R0)
            mx = max((n for c, n in rr if c == 1), default=0)
            if mx > best:
                best = mx
                headoff = pos - L0
                print(f"[peak maxrun={mx:>5} step={step:>10} headoff={headoff} st={STN[st]} r={tape[pos]}]")
                print(f"    {rs(rr)}")


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    run(cap)
