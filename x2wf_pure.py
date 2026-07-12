#!/usr/bin/env python3
"""x2wf_pure.py -- the PURE odometer model, and the clean well-founded measure.

Model the phase abstractly as a binary counter and check it reproduces the real
carry statistics, and that mu = T - t is the clean decreasing measure.  Also
detect COMPOUND (multi-digit ripple) carries on the real orbit -- does a single
carry ever propagate through >1 cascade digit (the inner carry-recursion depth)?
"""
import sys, math
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


def ripple_probe(g):
    """track consecutive chew-starts; a carry regenerates the leading block UP.
    Measure how many carries happen 'back to back' (ripple depth) by watching the
    comb reset pattern and whether two regenerations occur without a full chew
    between them."""
    sim = build(g); sim.step()
    miles = 0
    starts = []      # (n, blk, comb)
    prev = -1
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6: break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            blk = right_first_block(sim)
            comb = left_comb_pairs(sim)
            nxt = None
            starts.append((sim.n, blk, comb))
        if not sim.step():
            break
    # reduce to chew-starts (local maxima of blk)
    cs = []
    for i in range(len(starts)):
        blk = starts[i][1]
        p = starts[i-1][1] if i > 0 else -1
        nx = starts[i+1][1] if i+1 < len(starts) else -1
        if blk >= 5 and blk > p and blk >= nx:
            cs.append(starts[i])
    # a carry = chew-start whose blk > previous chew-start's blk (regeneration up).
    # ripple depth = run-length of consecutive carries with STRICTLY increasing blk
    depths = {}
    i = 0
    ncarry = 0
    while i < len(cs):
        if i > 0 and cs[i][1] > cs[i-1][1]:
            # start of a possible ripple
            d = 1
            j = i
            while j+1 < len(cs) and cs[j+1][1] > cs[j][1]:
                d += 1; j += 1
            depths[d] = depths.get(d, 0) + 1
            ncarry += d
            i = j + 1
        else:
            i += 1
    return len(cs), ncarry, depths


if __name__ == "__main__":
    for g in (2, 3):
        K = g + 8
        ncs, ncarry, depths = ripple_probe(g)
        print(f"=== g={g} K={K} ===")
        print(f" chew-starts={ncs} (~Theta(2^K)={2**K}), carries={ncarry}")
        print(f" ripple-depth histogram (consecutive up-regenerations): {dict(sorted(depths.items()))}")
        print(f"   max ripple depth = {max(depths) if depths else 0}  (bounded by K-2={K-2}?)")
