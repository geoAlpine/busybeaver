#!/usr/bin/env python3
"""x2ca_bottom.py -- find the BOTTOM-of-cascade carry macro-events at each level.

The reference carry_event_5to13 is the E-on-0 anchor with bv=(5,1) [n=6591]
transporting to the next E-on-0 anchor with bv=(13,5,1) [n=6708], 117 steps.

General pattern for level j (dj=2^j-3): an E-on-0 anchor whose block-vector is
exactly (dj, dj-1, ..., 5, 1) [the descending cascade bottom, leading block dj]
transporting to the E-on-0 anchor with bv=(2dj+3, dj, dj-1, ..., 5, 1).  We scan
for the FIRST such macro-event at each j and report [n0,n1], step-count, and the
comb at both ends (to see the window/step growth with j).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


def right_block_vector(sim, k=12):
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


def cascade_bottom(j):
    # descending [dj, d_{j-1}, ..., 5, 1] where d_i = 2^i - 3, i from j down to 2
    return tuple(2 ** i - 3 for i in range(j, 1, -1))


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    seq = all_anchors(g)
    print(f"g={g}: {len(seq)} anchors")
    for j in range(3, 8):
        dj = 2 ** j - 3
        start_bv = cascade_bottom(j)
        end_bv = (2 * dj + 3,) + cascade_bottom(j)
        # find first anchor with bv == start_bv, then next anchor with bv == end_bv
        starts = [i for i, a in enumerate(seq) if a[4] == start_bv]
        if not starts:
            print(f" j={j} dj={dj}: start bv={start_bv} NOT FOUND")
            continue
        i0 = starts[0]
        # find next anchor after i0 with bv == end_bv
        i1 = None
        for k in range(i0 + 1, min(i0 + 400, len(seq))):
            if seq[k][4] == end_bv:
                i1 = k; break
        if i1 is None:
            print(f" j={j} dj={dj}: start@n={seq[i0][0]} bv={start_bv}; end bv={end_bv} NOT FOUND within 400 anchors")
            # show what bv's appear
            print(f"    nearby end bv candidates: {[seq[k][4][:3] for k in range(i0+1,i0+8)]}")
            continue
        n0, n1 = seq[i0][0], seq[i1][0]
        print(f" j={j} dj={dj}->{2*dj+3}: n=[{n0},{n1}] {n1-n0} steps  "
              f"comb {seq[i0][2]}->{seq[i1][2]}  pos {seq[i0][3]}->{seq[i1][3]}  "
              f"({i1-i0} sub-anchors)")
