#!/usr/bin/env python3
"""x2wf_counter.py -- confirm the phase is a BINARY ODOMETER and find the clean
well-founded measure.

Hypotheses tested on the real g=2,3 orbit:
  H1  the leading cascade is [2^K-3, 2^{K-1}-3, ..., 2^2-3, 1] at M6 and
      [2^{K+1}-3, 2^K-3, ..., 2^2-3, 1] at M1(K+1)  (a full doubling / shift-up).
  H2  carries fire at comb = 2^j - 1 and regenerate block 2^j-3 -> 2^{j+1}-3.
  H3  the number of level-j carries is 2^{K-1-j} (binary-counter bit j), summing
      to Theta(2^K) total carries.
  H4  MEASURE CANDIDATE (mu): the odometer counts DOWN a well-founded rank.
      Test mu = (blocks-left-to-double, block-remaining-to-chew) lexicographic,
      strictly decreasing every E-on-0 tick.  Also test a single Nat
      mu2 = 2*(sum over descending original digits not yet doubled) + block-remaining.
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


def full_stats(g):
    sim = build(g); sim.step()
    K = g + 8
    miles = 0
    start_vec = None
    end_vec = None
    carry_levels = {}       # 2^{j+1}-3 -> count of carries producing it
    n_e0 = 0
    prev_blk = -1
    # candidate measure: mu_ticks = decreasing count of E-on-0 anchors to the end.
    # We simply record the sequence of (comb, blk) at chew-starts to inspect monotone rank.
    chew_seq = []
    csprev = -1
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 5:
                start_vec = tuple(right_block_vector(sim))
            if miles == 6:
                end_vec = tuple(right_block_vector(sim))
                break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            n_e0 += 1
            blk = right_first_block(sim)
            comb = left_comb_pairs(sim)
            # chew-start = local max
            if blk >= 5 and blk > csprev:
                # a carry if blk larger than previous chew-start's blk
                pass
            # detect carry: block regenerates upward
            if blk > prev_blk and prev_blk != -1 and prev_blk <= 5 and blk >= 13:
                carry_levels[blk] = carry_levels.get(blk, 0) + 1
            prev_blk = blk
        if not sim.step():
            break
    return K, start_vec, end_vec, carry_levels, n_e0


if __name__ == "__main__":
    for g in (2, 3):
        K, sv, ev, cl, n_e0 = full_stats(g)
        print(f"=== g={g} K={K} ===")
        print(f" M6 cascade start : {sv}")
        print(f"   expected [2^j-3]: {tuple(2**j - 3 for j in range(K, 1, -1))} (+trailing 1)")
        print(f" M1(K+1) cascade  : {ev}")
        print(f"   expected doubled: {tuple(2**j - 3 for j in range(K+1, 1, -1))} (+trailing 1)")
        print(f" carry levels (block->count): {dict(sorted(cl.items()))}")
        tot = sum(cl.values())
        print(f"   total carries={tot}  E-on-0 anchors={n_e0}  2^K={2**K} 2^(K-1)={2**(K-1)}")
        # H3: level-(2^{j+1}-3) count should be ~2^{K-1-j}
        for blk in sorted(cl):
            # blk = 2^{j+1}-3  => j+1 = log2(blk+3)
            import math
            jp1 = round(math.log2(blk + 3))
            print(f"   block {blk} (=2^{jp1}-3): {cl[blk]} carries, 2^(K-1-({jp1-1}))=2^{K-jp1}={2**(K-jp1) if K-jp1>=0 else 0}")
