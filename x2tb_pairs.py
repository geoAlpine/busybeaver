#!/usr/bin/env python3
"""x2tb_pairs.py -- re-derive the island COUNT by testing the pairing claims (2026-07-17).

The roadmap's island count "5 firm candidates ~= 3 distinct structural problems
(B1/B2, B3/B4, B5)" rests entirely on two asserted PEAK-IDENTICAL PAIRS.  59749fb's
count is known to be wrong (B5 merged into B1's class), so the count must be re-derived
rather than patched -- and that means re-testing the pairings themselves, not inheriting
them.

Test: are the two machines' register peak sequences AND the step-times at which those
peaks fire literally the same?  "Peak-identical" is a claim about the peak VALUES; if
the values differ, the machines are not peak-identical, whatever else they share.  A
shared FIT SHAPE (e.g. both fitting v'=2v-28.5) is a much weaker statement and must not
be reported as identity.

All observables from x2tb_sim.feats (tape-derived extent).  Decides NO halting.
"""

import sys
from x2tb_sim import MACHINES, run, OBS_IDX
from x2tb_braid import record_curve

PAIRS = [('B1', 'B2', 'maxrun'), ('B3', 'B4', 'maxrun'), ('B3', 'B4', 'total1')]


def curve_of(name, ob, cap):
    outc, step, S = run(MACHINES[name], cap)
    return record_curve(S, OBS_IDX[ob])


if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    for a, b, ob in PAIRS:
        ca, cb = curve_of(a, ob, cap), curve_of(b, ob, cap)
        va = [v for _, v in ca][-8:]
        vb = [v for _, v in cb][-8:]
        ta = [t for t, _ in ca][-4:]
        tb = [t for t, _ in cb][-4:]
        same_vals = va == vb
        same_times = ta == tb
        print(f"\n=== {a} vs {b}   observable={ob}")
        print(f"  {a} record values : {va}")
        print(f"  {b} record values : {vb}")
        print(f"  {a} record steps  : {ta}")
        print(f"  {b} record steps  : {tb}")
        print(f"  peak-identical VALUES: {same_vals};  identical TIMES: {same_times}")
        if same_vals and same_times:
            print("  ==> INDISTINGUISHABLE on this observable (consistent with one structure)")
        elif same_vals:
            print("  ==> same peak values, DIFFERENT timings")
        else:
            print("  ==> NOT peak-identical: the peak values differ.")
    print("\nNo machine decided. No label upgraded.")
