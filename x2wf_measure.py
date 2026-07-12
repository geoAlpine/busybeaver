#!/usr/bin/env python3
"""x2wf_measure.py -- WELL-FOUNDED MEASURE probe for the doubling-phase odometer.

At each CHEW-START (true local maximum of the leading right block among E-on-0
arrivals) we log the full cascade digit vector + the left comb-pair count, mark
carry events (block regenerates UP), and test candidate well-founded measures for
strict monotone decrease to the base case (= M1(K+1)).

Candidate measures tested:
  M_ones      : total ones on tape           (known to double, NOT monotone)
  M_biglen    : leading-block length          (resets up at carries, NOT monotone)
  M_remcasc   : sum of the *un-consumed* descending cascade digits (>= current chew
                position), i.e. how much of the original [2^K-3,..] is still to the
                RIGHT and not yet doubled -- candidate primary key
  M_lex       : (remaining descending-cascade blocks to process, comb pairs left to
                deposit in current block) -- lexicographic pair
  M_odo       : 2^{K+1}-3 - (accumulated odometer value) -- counts UP toward target
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, total_ones, left_comb_pairs


def right_block_vector(sim):
    bits = [sim.h] + sim.R[::-1]
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


def collect(g):
    """all E-on-0 anchors in the doubling phase: (n, blk, combP, ones, pos, vec)."""
    sim = build(g); sim.step()
    miles = 0
    anchors = []
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6:
                anchors.append(('M1', sim.n, right_first_block(sim),
                                left_comb_pairs(sim), total_ones(sim), sim.pos,
                                tuple(right_block_vector(sim))))
                break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            anchors.append(('a', sim.n, right_first_block(sim),
                            left_comb_pairs(sim), total_ones(sim), sim.pos,
                            tuple(right_block_vector(sim))))
        if not sim.step():
            break
    return anchors


def chew_starts(anchors):
    pts = [t for t in anchors if t[0] == 'a']
    outs = []
    for i in range(len(pts)):
        blk = pts[i][2]
        prev = pts[i-1][2] if i > 0 else -1
        nxt = pts[i+1][2] if i+1 < len(pts) else -1
        if blk >= 5 and blk > prev and blk >= nxt:
            outs.append(pts[i])
    return outs


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    K = g + 8
    anchors = collect(g)
    starts = chew_starts(anchors)
    print(f"=== g={g} K={K}: {len(starts)} chew-starts, target leading = 2^(K+1)-3 = {2**(K+1)-3} ===")
    print("Marking carries (blk regenerates UP vs previous chew-start).")
    print(" idx  n        blk    comb   ones   pos     tag   remcasc_sum")
    prevblk = -1
    carries = 0
    for i, (_, n, blk, comb, ones, pos, vec) in enumerate(starts):
        tag = ""
        if blk > prevblk and prevblk != -1:
            tag = "<<CARRY"
            carries += 1
        prevblk = blk
        # remcasc = sum of descending cascade digits strictly to the right that are
        # still in original (un-doubled) descending order form -- approximate by the
        # tail of vec that is strictly increasing downward? Use sum of vec beyond head.
        remcasc = sum(vec[1:]) if len(vec) > 1 else 0
        if i < 40 or blk > 100 or tag:
            print(f" {i:<4} {n:<8} {blk:<6} {comb:<6} {ones:<6} {pos:<7} {tag:<7} {remcasc}")
    print(f"total carries = {carries}, total chew-starts = {len(starts)}")
    M = anchors[-1]
    print(f"M1(K+1): n={M[1]} blk={M[2]} comb={M[3]} ones={M[4]} vec[:14]={M[6][:14]}")
