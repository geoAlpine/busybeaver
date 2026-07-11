#!/usr/bin/env python3
"""x2cc_lowtrace.py -- CARRY CALCULUS step 1: dump the exact LOW REGION of the x2 machine
`1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` at every event where the head EXITS the low
region moving right (i.e. crosses the left edge of the leftmost BIG 1-block), deduped by
content.  The sequence of these snapshots is the register history: the raw material for
decoding the low-part update law.  Exact bytearray simulation, no approximation."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)
BIG = 15   # a 1-run of length >= BIG is "big" (cascade block); low region ends before it


def rs(rr):
    return ' '.join(f"{c}^{n}" if n > 1 else f"{c}" for c, n in rr)


def big_edge(tape, lo, hi):
    """position of the first cell of the leftmost 1-run of length >= BIG, else None"""
    i = lo
    while i <= hi:
        if tape[i] == 1:
            j = i
            while j <= hi and tape[j] == 1: j += 1
            if j - i >= BIG:
                return i
            i = j
        else:
            i += 1
    return None


def run(maxsteps, SZ=1 << 23, out=sys.stdout):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    prev_inside = False
    last_snap = None
    nsnap = 0
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}", file=out); return
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww
        oldpos = pos
        pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        # exit event: head moves right and lands ON a big-block cell while previous pos was left of it
        # cheap test: only when moving right and the new cell is 1 and previous cell (written) pattern
        # do the full scan rarely: when head moves right onto a 1 whose run extends >= BIG
        if d == 1 and tape[pos] == 1:
            j = pos
            while tape[j] == 1: j += 1
            if j - pos >= BIG:
                # head is at the left part of a big run; is it the LEFTMOST big run?
                # check nothing big strictly left of oldpos+... scan low region
                e = big_edge(tape, lo, pos - 1)
                if e is None:
                    # snapshot low region [lo..pos-1]; find leftmost 1
                    L0 = lo
                    while L0 < pos and tape[L0] == 0: L0 += 1
                    snap = bytes(tape[L0:pos])
                    if snap != last_snap:
                        last_snap = snap
                        rr = rle(tape, L0, pos - 1) if L0 < pos else []
                        print(f"s{nsnap:>4} step={step:>10} st={STN[st]} lowlen={pos-L0:>4}  {rs(rr)}",
                              file=out)
                        nsnap += 1
    print(f"[done steps={step} snaps={nsnap}]", file=out)


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    run(cap)
