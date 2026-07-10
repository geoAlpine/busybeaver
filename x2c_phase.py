#!/usr/bin/env python3
"""x2c_phase.py -- hunt for the conserved parity that forces E to meet only EVEN gaps.
At each event where E (state E) reads a 0 at the LEFT end of a maximal interior gap 0^g,
record parities of candidate conserved quantities:
  - pos (absolute head cell, relative to the fixed origin 'off')
  - number of 1s strictly left of the head (on finite support)
  - number of 1s strictly right of the head
  - total number of 1s on the tape
  - g (gap length)
Cross-tabulate g%2 against each candidate to find one that is CONSTANT whenever E meets a gap
(=> a phase invariant that forbids odd gaps)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
M = parse(SPEC)


def run(start_step, ngap, SZ=1 << 22):
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st = 0
    step = 0
    lo = hi = pos
    seen = 0
    ones_total = 0     # maintain incrementally
    from collections import Counter
    tab = Counter()    # (name, gpar, value) -> count
    while step < 10 ** 12 and seen < ngap:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"HALT step={step}")
            return
        if st == 4 and r == 0 and step >= start_step:
            g = 0
            j = pos
            while j <= hi and tape[j] == 0:
                g += 1
                j += 1
            if 2 <= g and j <= hi:
                gpar = g % 2
                ones_left = sum(tape[lo:pos])
                ones_right = ones_total - ones_left
                cands = {
                    'pos%2': (pos - off) % 2,
                    'onesL%2': ones_left % 2,
                    'onesR%2': ones_right % 2,
                    'onesTot%2': ones_total % 2,
                    'gapstart-pos%2': (pos - off) % 2,
                    'lo%2': (lo - off) % 2,
                    'hi-pos%2': (hi - pos) % 2,
                }
                for name, v in cands.items():
                    tab[(name, gpar, v)] += 1
                seen += 1
        ww, d, ns = act
        # maintain ones_total
        if tape[pos] != ww:
            ones_total += (1 if ww == 1 else -1)
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos
    # report: for each candidate, the joint distribution of (gpar, value)
    names = sorted(set(n for (n, gp, v) in tab))
    print(f"events={seen}. For each candidate parity q: table gpar x q (want q constant | E-meets-gap)")
    for name in names:
        cells = {(gp, v): tab[(name, gp, v)] for gp in (0, 1) for v in (0, 1)}
        print(f"  {name:16}  g_even&q0={cells[(0,0)]:>6} g_even&q1={cells[(0,1)]:>6} "
              f"g_odd&q0={cells[(1,0)]:>6} g_odd&q1={cells[(1,1)]:>6}")


if __name__ == "__main__":
    ss = int(sys.argv[1]) if len(sys.argv) > 1 else 500000
    ng = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    run(ss, ng)
