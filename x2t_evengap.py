#!/usr/bin/env python3
"""x2t_evengap.py -- for every RIGHTWARD E-scanner entry into a maximal 0-run of length>=3,
dump the LOCAL context (state, the run length, and the RLE of a window around the entry point)
to see what creates these runs and whether the length is locally determined (finite-state) or
counter-dependent. Also separately: track the length-3 gap 0^3 that sits right of the current
top block, and log the (state,direction) of EVERY head crossing of that specific cell triple."""
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
    big_events = []
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT step={step}"); break
        if st == 4 and r == 0 and pos > lo and tape[pos - 1] == 1:
            j = pos
            while j < SZ and tape[j] == 0: j += 1
            L = j - pos
            if 3 <= L <= 40:   # skip the run-into-background (~2M) and the trivial 1,2
                w0 = max(lo, pos - 12); w1 = min(hi, pos + L + 12)
                rr = rle(tape, w0, w1)
                big_events.append((step, L, pos - w0, rs(rr)))
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    for step, L, hoff, ctx in big_events:
        print(f"step={step:>9} runlen={L:>3} E@off{hoff}:  {ctx}")
    print(f"total non-background E-entries with L>=3: {len(big_events)}  (all should be even, none==3)")
    from collections import Counter
    print("length histogram:", dict(sorted(Counter(L for _,L,_,_ in big_events).items())))


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 700000
    run(cap)
