#!/usr/bin/env python3
"""x2bd_outer.py -- the COARSE outer trace + invariant probes.

Anchor = every arrival in state E reading a 0 (a comb/block boundary the odometer
re-visits).  At each anchor we log the whole-tape scalar candidates:
  ones   = total 1s on the tape
  val    = the integer the tape encodes, LSB-at-head weighting sum_i bit_i * 2^i
           over the RIGHT tape (blocks) -- test for the doubling invariant
  combP  = number of (01)/(10) comb pairs immediately left of the head
  blk    = length of the first 1-run to the RIGHT of the head (the block being worked)
We then extract the sequence of CHEW-STARTS (local maxima of blk at E-on-0 anchors)
= the outer round-trips, and print the (blk, comb, ones) envelope.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim, build


def total_ones(sim):
    return sum(sim.L) + sim.h + sum(sim.R)


def right_first_block(sim):
    # length of leading 1-run to the right of (and including) head
    seq = [sim.h] + sim.R[::-1]
    i = 0
    while i < len(seq) and seq[i] == 0:
        i += 1
    j = i
    while j < len(seq) and seq[j] == 1:
        j += 1
    return j - i


def left_comb_pairs(sim):
    # count leading (10)/(01) alternating pairs on the left stack (nearest-first)
    L = sim.L
    n = len(L)
    pairs = 0
    i = 0
    # comb on left after a chew looks like ...1 0 1 0 (nearest-first bits alternate)
    while i + 1 < n and L[-1 - i] != L[-1 - (i + 1)]:
        pairs += 1
        i += 2
    return pairs


def run(g, cap=200_000_000):
    sim = build(g)
    sim.step()
    miles = 0
    anchors = []      # (n, blk, combP, ones, pos)
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 5:
                pass
            elif miles == 6:
                anchors.append(('M1n', sim.n, right_first_block(sim),
                                left_comb_pairs(sim), total_ones(sim), sim.pos))
                break
        if miles >= 5:
            if sim.st == 'E' and sim.h == 0:
                anchors.append(('a', sim.n, right_first_block(sim),
                                left_comb_pairs(sim), total_ones(sim), sim.pos))
        if not sim.step():
            break
    return anchors


def chew_starts(anchors):
    """local maxima of blk among 'a' anchors = outer round-trip chew-starts."""
    pts = [(n, blk, comb, ones, pos) for k, n, blk, comb, ones, pos in anchors if k == 'a']
    outs = []
    for i in range(len(pts)):
        blk = pts[i][1]
        prev = pts[i-1][1] if i > 0 else -1
        nxt = pts[i+1][1] if i+1 < len(pts) else -1
        if blk >= 5 and blk > prev and blk >= nxt:
            outs.append(pts[i])
    return outs, pts


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    anchors = run(g)
    print(f"=== g={g}: {sum(1 for a in anchors if a[0]=='a')} E-on-0 anchors ===")
    ones0 = [a[4] for a in anchors if a[0] == 'a']
    print(f"total-ones over phase: min={min(ones0)} max={max(ones0)} "
          f"first={ones0[0]} last={ones0[-1]}")
    starts, pts = chew_starts(anchors)
    print(f"chew-starts (local maxima of block len): {len(starts)}")
    print("  n         blk    combP   ones    pos")
    for n, blk, comb, ones, pos in starts[:60]:
        print(f"  {n:<9} {blk:<6} {comb:<7} {ones:<7} {pos}")
    # final milestone
    for a in anchors:
        if a[0] == 'M1n':
            print(f"M1(g+1): n={a[1]} blk={a[2]} combP={a[3]} ones={a[4]} pos={a[5]}")
