#!/usr/bin/env python3
"""x2ca_find.py -- locate the larger-j CARRY events on the real g orbit.

A carry = the leading working block regenerates UP (1^{d_j} -> 1^{d_{j+1}}),
d_j = 2^j-3: 5->13 (j=3, = carry_event_5to13), 13->29 (j=4), 29->61 (j=5), ...

We log every E-on-0 anchor with (n, blk, comb, pos, st).  The carry window is
bracketed by the E-on-0 anchor where the block LEAVES value d_j (start of the
repack) and the next E-on-0 anchor where the leading block has become d_{j+1}
with a fresh d_j below.  We report candidate [n0,n1] windows for j=4 and j=5.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs, total_ones


def right_block_vector(sim, k=6):
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


def anchors(g):
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


def find_carries(seq, dj):
    """A carry to level d_{j+1}=2*dj+3: leading block transitions from dj to 2*dj+3.
    Find anchor index i where blk[i]==dj (last time at dj before the jump) and a
    later anchor j0 where blk==2*dj+3 for the first time (regenerated)."""
    up = 2 * dj + 3
    hits = []
    n = len(seq)
    for i in range(n):
        if seq[i][1] == dj:
            # look ahead for the block to become `up` (regenerated) within a window
            for j in range(i + 1, min(i + 4000, n)):
                if seq[j][1] == up:
                    hits.append((seq[i][0], seq[j][0], i, j))
                    break
    return hits


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    seq = anchors(g)
    print(f"g={g}: {len(seq)} E-on-0 anchors")
    # sanity: show the block-vector around the known j=3 carry (n~6591..6708)
    for dj, name in ((5, 'j=3'), (13, 'j=4'), (29, 'j=5'), (61, 'j=6')):
        hits = find_carries(seq, dj)
        print(f"\n=== carries {name}: block {dj}->{2*dj+3}  ({len(hits)} found) ===")
        for (n0, n1, i, j) in hits[:4]:
            print(f"  window n=[{n0},{n1}] ({n1-n0} steps)  anchors[{i}->{j}]")
            # print block vectors at start and end
            print(f"    start blk-vec={seq[i][4]} comb={seq[i][2]} pos={seq[i][3]}")
            print(f"    end   blk-vec={seq[j][4]} comb={seq[j][2]} pos={seq[j][3]}")
