#!/usr/bin/env python3
"""x2p_invariant.py -- test the PARITY-separation hypothesis at every milestone.
At each milestone (E reading 0, left of all 1s) verify structural invariants and evaluate
candidate CONSERVED parities to find one that (a) is constant across milestones and
(b) forces the leading gap G even. Also test the eraser-parity-count law:
  G(new gap) is even  <=>  the region the eraser consumed contained an EVEN number of
  odd-length 1-runs.  All 1-runs being odd => G even iff #1-runs-consumed even.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
from collections import Counter

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
M = parse(SPEC)


def run(maxsteps, SZ=1 << 24):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    left1 = SZ
    ones_total = 0
    n_mile = 0
    bad_1run = 0        # milestones with an EVEN-length 1-run
    bad_gap = 0         # milestones with an odd>=3 gap
    Ghist = Counter()
    # candidate parity tallies: name -> Counter of value
    cand = {k: Counter() for k in
            ['n_blocks', 'n_gaps', 'ones_tot', 'n_even_gaps', 'n_odd_blocks', 'G']}
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        if st == 4 and r == 0 and pos < left1 and left1 <= hi:
            G = left1 - pos
            Ghist[G] += 1
            rr = rle(tape, left1, hi)   # starts with a 1-run
            blocks = [n for c, n in rr if c == 1]
            gaps = [n for c, n in rr if c == 0]   # interior gaps (between blocks)
            if any(b % 2 == 0 for b in blocks):
                bad_1run += 1
            if any(g >= 3 and g % 2 for g in gaps) or (G >= 3 and G % 2):
                bad_gap += 1
            cand['n_blocks'][len(blocks) % 2] += 1
            cand['n_gaps'][(len(gaps) + 1) % 2] += 1   # +1 for leading gap
            cand['ones_tot'][ones_total % 2] += 1
            cand['n_even_gaps'][(sum(1 for g in [G] + gaps if g % 2 == 0)) % 2] += 1
            cand['n_odd_blocks'][(sum(1 for b in blocks if b % 2)) % 2] += 1
            cand['G'][G % 2] += 1
            n_mile += 1
        act = M[st][r]
        ww, d, ns = act
        if tape[pos] != ww:
            ones_total += (1 if ww == 1 else -1)
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
    print(f"milestones = {n_mile}  (to step {step:,})")
    print(f"  milestones with an EVEN-length 1-run:  {bad_1run}")
    print(f"  milestones with an odd>=3 gap (incl G): {bad_gap}")
    print(f"  leading-gap G histogram: {dict(sorted(Ghist.items()))}")
    print("  candidate conserved parities (value:count) -- CONSTANT means it never varies:")
    for k, c in cand.items():
        const = "CONSTANT" if len(c) == 1 else "splits"
        print(f"    {k:14} {dict(c)}   {const}")


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    run(cap)
