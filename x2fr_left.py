#!/usr/bin/env python3
"""x2fr_left.py -- dump the FULL left+right tape structure at the first N
chew-starts so we can design the faithful (todo, built, comb) register."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2fr_state import right_run_vector, left_full, collect, chew_start_states

if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    states = collect(g)
    css = chew_start_states(states)
    print(f"g={g} K={g+8}: {len(css)} chew-starts")
    print("idx  n         LEFT(nearest-first runs)                     | RIGHT(1-run vec head-first)")
    for i in range(min(N, len(css))):
        n, blk, comb, rv, lf = css[i]
        # compact left: show as run tokens
        lft = ' '.join(f'{b}^{l}' for b,l in lf[:14])
        print(f"{i:<4} {n:<9} {lft:<52}| {rv[:12]}")
