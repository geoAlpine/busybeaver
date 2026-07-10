#!/usr/bin/env python3
"""x2p_ordering.py -- direct test of the ORDERING LEMMA.
The fatal event is: head=E, reading 0, at the LEFT end of a maximal 0-run of length 3.
Odd gaps (incl length 3) form TRANSIENTLY while the eraser (states A/D and the C/D/E
oscillation) grows a block 0^1->0^2->...  The ordering lemma says E always arrives at a
gap only AFTER it is finished (even) -- never mid-erasure at odd length.

This instruments the REAL orbit and, at every step, scans a window around the head for
maximal 0-runs of ODD length >= 3, and records:
  (1) the HEAD STATE whenever an odd>=3 gap is adjacent to / contains / just-left-of head,
  (2) specifically: is head ever E reading the LEFT-0 of such a gap? (the fatal ordering
      violation)  -- must be 0.
  (3) for gap-3 specifically: the multiset of head states while a gap-3 sits within radius
      W of the head, and the head's signed offset from the gap's left cell.
This shows WHICH phases coexist with a fatal-length gap and whether the E-phase is
excluded by the finite-state control (=> ordering holds) or only by counting (=> counter-
dependent)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse
from collections import Counter

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def run(maxsteps, W=6, SZ=1 << 22):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    # for gap-3 near head: head-state histogram, and head-offset-from-gapleft histogram
    st_when_gap3_near = Counter()
    off_when_gap3_near = Counter()
    st_at_gap3_left = Counter()   # head state when head sits exactly on left-0 of a gap-3
    fatal_E_left = 0
    n_gap3_steps = 0
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        # scan window [pos-W, pos+W] for maximal odd>=3 runs of 0 (need boundaries inside)
        a = max(lo, pos - W); b = min(hi, pos + W)
        i = a
        found3_near = False
        while i <= b:
            if tape[i] == 0:
                jj = i
                while jj <= hi and tape[jj] == 0: jj += 1
                # maximal run [i, jj-1]; need left boundary too (i-1 is 1 or i==0region)
                left_ok = (i - 1 >= lo and tape[i - 1] == 1)
                run_len = jj - i
                if left_ok and run_len == 3:
                    found3_near = True
                    # head state, offset of head from left cell i
                    st_when_gap3_near[STN[st]] += 1
                    off_when_gap3_near[pos - i] += 1
                    if pos == i:
                        st_at_gap3_left[STN[st]] += 1
                        if st == 4 and r == 0:
                            fatal_E_left += 1
                i = max(jj, i + 1)
            else:
                i += 1
        if found3_near:
            n_gap3_steps += 1
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    print(f"steps={step:,}   steps with a gap-3 within W={W} of head: {n_gap3_steps:,}")
    print(f"  FATAL (head=E reading left-0 of a gap-3): {fatal_E_left}")
    print(f"  head STATE while a gap-3 is near head:   {dict(st_when_gap3_near)}")
    print(f"  head state while head sits ON left-0 of a gap-3: {dict(st_at_gap3_left)}")
    print(f"  head OFFSET (pos - gap3_left) distribution: {dict(sorted(off_when_gap3_near.items()))}")


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    run(cap)
