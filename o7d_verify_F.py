#!/usr/bin/env python3
"""o7d_verify_F.py -- verify the b-free cascade map F against the ABSTRACT step_map orbit
(step_map itself is 0-mismatch verified against the raw TM in o7d_verify.py).
Gives >=1e5 cascade-entry transitions for F, plus odd-part census."""
import sys
from o7d_verify import step_map, F, v2, oddpart

def main(n_milestones):
    a, b, n = 2, 2, 0
    prev_even = None
    entries = []   # (a, b) at cascade entry
    min_odd = None
    while n < n_milestones:
        r = step_map(a, b)
        if r == ('HALT',):
            print(f"ABSTRACT HALT at milestone {n}, a=1"); return
        if a % 2 == 1 and a >= 5 and prev_even is True:
            entries.append((a, b))
            w = oddpart(a + 3)
            if min_odd is None or w < min_odd: min_odd = w
        prev_even = (a % 2 == 0)
        a, b = r[1], r[2]; n += 1
    print(f"milestones simulated: {n:,}; cascade entries: {len(entries):,}")
    bad_b = sum(1 for (_, bb) in entries if bb != 1)
    print(f"entries with b != 1: {bad_b}")
    mismF = 0
    for k in range(len(entries) - 1):
        u_e = entries[k][0] + 3
        got = F(u_e)
        want = entries[k + 1][0] + 3
        if got != want:
            mismF += 1
            if mismF <= 5: print("  F MISMATCH", u_e, got, want)
    print(f"F entry-to-entry checked: {len(entries)-1:,}; mismatches = {mismF}")
    print(f"min oddpart(u_e) over all entries = {min_odd}")
    print(f"final entry u_e bitlen = {entries[-1][0].bit_length()}")
    print("No machine decided.")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000)
