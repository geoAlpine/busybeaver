#!/usr/bin/env python3
"""x2lb_trace.py -- extract the ABSTRACT ODOMETER trace at chew-starts, to design
and cross-check the pure Layer-B register `OdoB` in lean/X2.lean.

At each chew-start (local max of leading right block among E-on-0 anchors) log the
full right cascade digit vector + comb pairs.  Print the first N chew-starts and a
clean decomposition (no-carry ticks vs genuine 2^j-3 -> 2^{j+1}-3 carries, ripple
depth).  Also report the TOTAL chew-start count T per g (must match 3852/9729/19470)
and the digit-doubling chain (must be 1,5,13,29,61,... = carryDigit).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


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


def collect_chewstarts(g, limit=None):
    sim = build(g); sim.step()
    miles = 0
    pts = []   # (n, blk, comb, vec)
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6:
                break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            pts.append((sim.n, right_first_block(sim), left_comb_pairs(sim),
                        tuple(right_block_vector(sim))))
        if not sim.step():
            break
    # local maxima of blk
    outs = []
    for i in range(len(pts)):
        blk = pts[i][1]
        prev = pts[i-1][1] if i > 0 else -1
        nxt = pts[i+1][1] if i+1 < len(pts) else -1
        if blk >= 5 and blk > prev and blk >= nxt:
            outs.append(pts[i])
    return outs


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    K = g + 8
    cs = collect_chewstarts(g)
    print(f"=== g={g} K={K}: {len(cs)} chew-starts ===")
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    for i, (n, blk, comb, vec) in enumerate(cs[:N]):
        print(f" {i:<4} n={n:<8} blk={blk:<6} comb={comb:<4} vec={vec}")
