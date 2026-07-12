#!/usr/bin/env python3
"""x2fr_decode.py -- decode the full tape at each chew-start into a structured
register and TEST purity: is the next register state a deterministic function of
the current one (bounded-vocabulary, tape-free)?

Register decode:
  LEFT (nearest-first) is split at 0^2 separators into left-digit-blocks; each
  block is classified: solid '1^k' (a BUILT doubled digit, value k) or comb
  '(1 0)^m' / leading teeth (the pending COUNTER).  We record the compact tuple
  of left blocks (kind,val) nearest-first.
  RIGHT is the 1-run vector head-first: working block = RIGHT[0], todo = RIGHT[1:].

Full register = (left_blocks_tuple, right_vec_tuple).  This is literally the whole
tape (modulo head pos), so determinism is trivial; the POINT is to inspect the
*local* transition (top-of-left + working + top-of-todo) and confirm a small
bounded rule, i.e. a genuine odometer.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2fr_state import collect, chew_start_states, right_run_vector, left_full


def decode_left(lf):
    """lf = tuple of (bit,len) nearest-first. Split at 0-runs of len>=2 into
    digit-blocks; classify each maximal 1/0-alternating chunk."""
    # Represent left as a flat token stream then group.
    # We'll just return a compact signature: list of tokens, capping length.
    return lf


import pickle
SP = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'

if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    with open(f'{SP}/css_g{g}.pkl','rb') as f:
        css = pickle.load(f)
    print(f"g={g} K={g+8}: {len(css)} chew-starts")
    # focus on the ACTIVE window: leading left run (built 1^k), then comb depth,
    # then working block b and next todo digit.
    print("idx  built  combDepth  work  todo[:4]")
    for i in range(min(N, len(css))):
        n, blk, comb, rv, lf = css[i]
        # built = leading 1-run length on left (nearest-first)
        built = lf[0][1] if lf and lf[0][0] == 1 else 0
        # comb depth = count leading alternating single teeth after built, until 0^2
        # walk tokens after the built block
        idx0 = 1 if (lf and lf[0][0] == 1) else 0
        teeth = 0
        j = idx0
        while j < len(lf) and lf[j][1] == 1:
            teeth += 1
            j += 1
        work = rv[0] if rv else 0
        todo = rv[1:5]
        print(f"{i:<4} {built:<6} {teeth:<10} {work:<5} {todo}")
