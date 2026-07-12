#!/usr/bin/env python3
"""x2bd_value.py -- does a clean scalar VALUE telescope across the real round-trips?

Sample the FULL tape (as a big integer, MSB-first over all cells) at the true
round-trip anchors (local maxima of the leading-block length among E-on-0 arrivals).
Report the per-round-trip first-difference of the value, and of a structured
'odometer value' V = sum_j 2^(position of the j-th 0^2 gap) style reading, to see
if either increments by a constant.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, total_ones


def full_value(sim):
    """the whole tape as an integer: LSB at the head, going right (blocks), plus
    the left deposits above the head as higher bits.  Absolute positional weight."""
    # left cells are at positions pos-1, pos-2, ... ; right at pos, pos+1, ...
    # use head as bit 0 baseline; weight 2^(offset from a fixed origin = leftmost)
    v = 0
    # right side incl head: offsets 0,1,2,...
    seq = [sim.h] + sim.R[::-1]
    for i, b in enumerate(seq):
        if b:
            v += 1 << i
    # left side: offsets -1,-2,... -> negative; shift everything up by len(L)
    # instead build absolute integer with left as low bits:
    return v  # right-only value (blocks/cascade); left comb tracked separately


def cascade_value(sim):
    """base-2 odometer reading of the cascade: blocks separated by 0^2 gaps;
    read block lengths as digits weighted by 2^(cumulative)."""
    bits = [sim.h] + sim.R[::-1]
    # collect (runbit,len)
    runs = []
    i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b:
            j += 1
        runs.append((b, j - i)); i = j
    return tuple(l for b, l in runs if b == 1)


def run(g):
    sim = build(g); sim.step()
    miles = 0
    seq = []      # (n, blk, value, ones, pos, leftones)
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6: break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            seq.append((sim.n, right_first_block(sim), full_value(sim),
                        total_ones(sim), sim.pos, sum(sim.L)))
        if not sim.step():
            break
    # real round-trip maxima
    maxima = []
    for i in range(len(seq)):
        blk = seq[i][1]
        if blk >= 5 and (i == 0 or blk > seq[i-1][1]) and (i+1 >= len(seq) or blk >= seq[i+1][1]):
            maxima.append(seq[i])
    return maxima


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    M = run(g)
    print(f"g={g}: {len(M)} real round-trips. (n, blk, right-value v2(delta), ones, pos, Lones)")
    prev = None
    for k in range(min(len(M), 50)):
        n, blk, val, ones, pos, lones = M[k]
        if prev is None:
            d = '-'
        else:
            dv = val - prev
            # factor sign and 2-adic valuation
            if dv == 0:
                d = '0'
            else:
                s = '+' if dv > 0 else '-'
                a = abs(dv); v2 = (a & -a).bit_length() - 1
                d = f"{s}2^{v2}*{a>>v2}" if a>>v2 < 10**6 else f"{s}~2^{a.bit_length()}"
        print(f"  n={n:<8} blk={blk:<5} d(val)={d:<16} ones={ones:<6} pos={pos:<6} Lones={lones}")
        prev = val
