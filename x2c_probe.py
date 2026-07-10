#!/usr/bin/env python3
"""x2c_probe.py -- discover the REAL in-context local situations the head encounters.

Run the raw TM from blank tape. At every step, classify the head's *local situation*:
(state, direction-of-last-move, symbol-under-head, and the run it is about to enter:
 its symbol + length). We are especially interested in E-scanner (rightward) events that
enter a maximal 0-run: record every maximal 0-run length that any rightmoving head enters,
and flag odd runs >=3 (the halt-relevant pattern).

Also: collect the SET of distinct (state, under, right-neighbor-run-symbol) transitions to
gauge whether a finite-state RLE abstraction exists, and the distribution of 0-run and
1-run lengths actually realized on the tape over the whole run (global, at rest AND transient)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def run(maxsteps, SZ=1 << 25):
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st = 0
    step = 0
    lo = hi = pos
    # halt-gate instrumentation: whenever we are in state E about to move right into a 0,
    # measure the maximal 0-run starting at pos.
    odd0_ge3 = 0            # count of odd 0-runs length>=3 *entered by a rightmoving scanner*
    worst = {}             # run-length -> count of times a rightward head sat at its left edge in E
    # global run-length census sampled periodically (both symbols)
    zero_runs_seen = {}    # maximal 0-run length -> times a head's read cell began such a run moving right
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return ('HALT', step, pos, st, odd0_ge3, worst)
        # Detect: state E reading 0 (start of the E->F->A->B halt chain) -- measure run to the right
        if st == 4 and r == 0:
            L = 0
            j = pos
            while j < SZ and tape[j] == 0:
                L += 1
                j += 1
            worst[L] = worst.get(L, 0) + 1
            if L >= 3 and (L % 2 == 1):
                odd0_ge3 += 1
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos
    return ('MAX', step, pos, st, odd0_ge3, worst)


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    out, step, pos, st, odd0, worst = run(cap)
    print(f"outcome={out} step={step} state={STN[st]}")
    print(f"odd 0-runs (>=3) entered by E-scanner: {odd0}")
    print("E-scanner 0-run-length histogram (L : count):")
    for L in sorted(worst):
        flag = "  <== ODD>=3 (HALT-relevant)" if (L >= 3 and L % 2 == 1) else ""
        print(f"  L={L:>4}: {worst[L]}{flag}")
