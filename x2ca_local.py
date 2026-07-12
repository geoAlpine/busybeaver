#!/usr/bin/env python3
"""x2ca_local.py -- inspect the LOCAL anchor structure around a known carry and
find tightly-localized single carries at each level j.

Reference: carry_event_5to13 is n=6591->6708 (117 steps), a j=3 carry:
  start right = 000 1^5 00 1  (blk-vec (5,1)),  small comb
  end   right = 000 1^13 00 1^5 00 1  (blk-vec (13,5,1))
We look for the analogous j=4 (13->29) and j=5 (29->61) LOCAL carries: an E-on-0
anchor whose leading block = dj with a SHORT trailing cascade, jumping to 2dj+3
within a few hundred steps, ending E-on-0 with leading block 2dj+3 and a fresh
dj planted below.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


def right_block_vector(sim, k=8):
    bits = [sim.h] + sim.R[::-1]
    runs = []
    i = 0
    while i < len(bits) and len(runs) < k:
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b:
            j += 1
        if b == 1:
            runs.append(j - i)
        i = j
    return runs


def all_anchors(g):
    sim = build(g); sim.step()
    miles = 0
    seq = []
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6:
                break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            seq.append((sim.n, right_first_block(sim), left_comb_pairs(sim),
                        sim.pos, tuple(right_block_vector(sim))))
        if not sim.step():
            break
    return seq


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    seq = all_anchors(g)
    idx = {n: i for i, (n, *_) in enumerate(seq)}
    # 1. show anchors bracketing the reference j=3 carry
    print("=== anchors near reference j=3 carry n=6591..6708 ===")
    for (n, blk, comb, pos, bv) in seq:
        if 6560 <= n <= 6720:
            print(f"  n={n} blk={blk} comb={comb} pos={pos} bv={bv}")
    # 2. localized single carries: consecutive anchors (i, i+1) where leading
    #    block jumps dj -> 2dj+3 and the trailing cascade is short (bv len small)
    print("\n=== localized single carries (leading block dj -> 2dj+3, adjacent-ish) ===")
    for dj in (5, 13, 29, 61, 125):
        up = 2 * dj + 3
        found = []
        for i in range(len(seq) - 1):
            n0, b0, c0, p0, bv0 = seq[i]
            # find nearest later anchor (within 6 anchors) whose leading block = up
            for k in range(1, 7):
                if i + k >= len(seq):
                    break
                n1, b1, c1, p1, bv1 = seq[i + k]
                if b0 == dj and b1 == up and len(bv1) <= len(bv0) + 1:
                    found.append((n0, n1, n1 - n0, c0, c1, bv0, bv1))
                    break
        print(f" dj={dj}->{up}: {len(found)} localized")
        for f in found[:3]:
            print(f"   n=[{f[0]},{f[1]}] {f[2]}st comb {f[3]}->{f[4]} bv {f[5]}->{f[6]}")
