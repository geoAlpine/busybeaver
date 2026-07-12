#!/usr/bin/env python3
"""x2fr_cache.py -- run the raw sim once per g and pickle the chew-start states
(n, blk, comb, right_run_vector, left_full) so downstream analysis is fast."""
import sys, pickle, os
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2fr_state import collect, chew_start_states

SP = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'

if __name__ == "__main__":
    g = int(sys.argv[1])
    path = f'{SP}/css_g{g}.pkl'
    states = collect(g)
    css = chew_start_states(states)
    with open(path, 'wb') as f:
        pickle.dump(css, f)
    print(f"g={g} K={g+8}: {len(css)} chew-starts cached to {path}")
