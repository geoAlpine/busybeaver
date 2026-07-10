#!/usr/bin/env python3
"""x2p_entry.py -- prove-by-enumeration the ENTRY MECHANISM: every time the head is in
state E reading a 0 at the LEFT end of a maximal 0-run (tape[i-1]=1), by which transition
did it ARRIVE at cell i?  Claim: ONLY via F:1->1RE (the repack sweep stepping off the
right edge of a 1-block).  If so, 'E meets a maximal gap' == 'the E/F repack sweep exits a
block', and the gap it faces is the pre-existing settled gap to the right of that block
(untouched, since the head moved right to reach it).  Also re-confirm ordering: 0 fatal
E-at-gap-3 to a larger horizon, and log the length histogram of every E-met maximal gap."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse
from collections import Counter

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def run(maxsteps, SZ=1 << 23):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    prev_state = None; prev_read = None
    entry_trans = Counter()     # (prevstate, prevread) that delivered E to a maximal-gap-left
    emet = Counter()            # length histogram of E-met maximal gaps
    fatal = 0
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        if st == 4 and r == 0 and pos > lo and tape[pos - 1] == 1:
            # E at left of a maximal gap
            j = pos
            while j <= hi and tape[j] == 0: j += 1
            g = j - pos
            emet[g] += 1
            if g == 3:
                fatal += 1
            entry_trans[(STN[prev_state], prev_read)] += 1
        act = M[st][r]
        ww, d, ns = act
        prev_state = st; prev_read = r
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    print(f"steps={step:,}")
    print(f"  E-met maximal-gap length histogram: {dict(sorted(emet.items()))}")
    print(f"  FATAL (E met a gap of exactly 3): {fatal}")
    print(f"  transitions that DELIVERED E to a maximal-gap-left (prevstate,prevread)->count:")
    for k, v in entry_trans.most_common():
        print(f"      {k} -> {v}")


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
    run(cap)
