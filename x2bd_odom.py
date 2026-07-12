#!/usr/bin/env python3
"""x2bd_odom.py -- is the outer loop a binary odometer on the cascade block-vector,
and is there a scalar VALUE linear in the round-trip index?

At each chew-start anchor we record the FULL vector of right-tape 1-run lengths
(the cascade "digits") and several scalar candidates, then test:
  * round-trip count scaling vs g  (Theta(2^K)?)
  * a base-2 VALUE = sum over 1-runs of len_i placed by its 0^2-gap position,
    read as the odometer register -- check first-differences per round-trip.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim, build
from x2bd_outer import run, chew_starts, total_ones


def right_block_vector(bits):
    runs = []
    i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b:
            j += 1
        if b == 1:
            runs.append(j - i)
        i = j
    return runs


def count_roundtrips(g):
    sim = build(g); sim.step()
    miles = 0; rt = 0; prevblk = -1
    from x2bd_outer import right_first_block
    lastE0 = -1
    seq = []
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6: break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            blk = right_first_block(sim)
            seq.append(blk)
        if not sim.step():
            break
    # count local maxima >=5
    rt = 0
    for i in range(len(seq)):
        if seq[i] >= 5 and (i == 0 or seq[i] > seq[i-1]) and (i+1 >= len(seq) or seq[i] >= seq[i+1]):
            rt += 1
    return rt, len(seq)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'scale'
    if mode == 'scale':
        for g in (2, 3, 4):
            rt, anch = count_roundtrips(g)
            K = g + 8
            print(f"g={g} K={K} 2^K={2**K}: round-trips={rt}  E0-anchors={anch}  "
                  f"rt/2^K={rt/2**K:.3f}")
    elif mode == 'digits':
        g = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        sim = build(g); sim.step()
        miles = 0
        from x2bd_outer import right_first_block, left_comb_pairs
        rows = []
        prevblk = -1
        while True:
            if sim.is_milestone():
                miles += 1
                if miles == 6: break
            if miles >= 5 and sim.st == 'E' and sim.h == 0:
                blk = right_first_block(sim)
                if blk >= 5 and blk > prevblk:
                    bits = [sim.h] + sim.R[::-1]
                    vec = right_block_vector(bits)
                    rows.append((sim.n, tuple(vec[:12]), total_ones(sim)))
                prevblk = blk
            else:
                prevblk = -1 if sim.st != 'E' else prevblk
            if not sim.step():
                break
        print(f"g={g}: {len(rows)} chew-starts; cascade digit-vectors (first 40):")
        for n, vec, ones in rows[:40]:
            print(f"  n={n:<8} ones={ones:<6} blocks={vec}")
