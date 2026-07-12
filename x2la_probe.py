#!/usr/bin/env python3
"""x2la_probe.py -- Layer A (outer_step) NON-CARRY tick extraction.

Extracts, CELL-FOR-CELL, the tape at the boundaries of one concrete NON-CARRY
outer tick deep in the g=2 doubling phase, matching lean/X2.lean `step` exactly
(reuses x2bd_sim.Sim). Dumps step indices, head positions, and the bounded
head-excursion window (the untouched L/R tails), exactly as the
carry_event_5to13 provenance documents its [2061,2089] window.

A NON-CARRY tick = an E-on-0 chew-start to the NEXT E-on-0 chew-start where the
left comb count does NOT overflow (no block-doubling regeneration between them).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim, build


def right_first_block(sim):
    seq = [sim.h] + sim.R[::-1]
    i = 0
    while i < len(seq) and seq[i] == 0:
        i += 1
    j = i
    while j < len(seq) and seq[j] == 1:
        j += 1
    return j - i


def snapshot(sim, lwin=14, rwin=32):
    """cell-for-cell nearest-first L window and R window (head-first)."""
    L = [sim.L[-1 - i] for i in range(min(lwin, len(sim.L)))]
    R = [sim.h] + [sim.R[-1 - i] for i in range(min(rwin, len(sim.R)))]
    return L, R


def bits_to_lean(bits):
    return ' :: '.join('true' if b else 'false' for b in bits)


def run(g, start_n, end_n):
    """simulate to start_n, record window, run to end_n, track head excursion."""
    sim = build(g)
    sim.step()
    while sim.n < start_n:
        if not sim.step():
            print("HALT at", sim.n); return
    # start snapshot
    L0, R0 = snapshot(sim)
    st0, pos0, n0 = sim.st, sim.pos, sim.n
    minpos = maxpos = sim.pos
    while sim.n < end_n:
        if not sim.step():
            print("HALT at", sim.n); return
        minpos = min(minpos, sim.pos)
        maxpos = max(maxpos, sim.pos)
    L1, R1 = snapshot(sim)
    st1, pos1, n1 = sim.st, sim.pos, sim.n
    print(f"=== tick n={n0}->{n1} ({n1-n0} steps) ===")
    print(f"  START: state {st0} pos {pos0}")
    print(f"    L (nearest-first): {L0}")
    print(f"    R (head-first):    {R0}")
    print(f"  END:   state {st1} pos {pos1}")
    print(f"    L (nearest-first): {L1}")
    print(f"    R (head-first):    {R1}")
    print(f"  head excursion: [{minpos},{maxpos}]  (rel to start pos {pos0}: "
          f"[{minpos-pos0},{maxpos-pos0}])")
    print(f"  START L lean: {bits_to_lean(L0)}")
    print(f"  START R lean: {bits_to_lean(R0)}")
    print(f"  END   L lean: {bits_to_lean(L1)}")
    print(f"  END   R lean: {bits_to_lean(R1)}")
    return (n0, st0, pos0, L0, R0), (n1, st1, pos1, L1, R1), (minpos, maxpos)


def chew_start_list(g, region_lo, region_hi):
    """list E-on-0 local-max block anchors in [region_lo, region_hi]."""
    sim = build(g)
    sim.step()
    prev_blk = -1
    pts = []
    while sim.n < region_hi:
        if region_lo <= sim.n and sim.st == 'E' and sim.h == 0:
            blk = right_first_block(sim)
            combP = 0
            # count leading alternating comb pairs on left
            i = 0
            while i + 1 < len(sim.L) and sim.L[-1-i] != sim.L[-1-(i+1)]:
                combP += 1
                i += 2
            pts.append((sim.n, blk, combP, sim.pos))
        if not sim.step():
            break
    return pts


if __name__ == "__main__":
    g = 2
    if len(sys.argv) >= 3:
        run(g, int(sys.argv[1]), int(sys.argv[2]))
    else:
        # survey E-on-0 anchors around the small-cascade region after the carry
        pts = chew_start_list(g, 6700, 6830)
        print("E-on-0 anchors n, blk, combP, pos in [6700,6830]:")
        for n, blk, combP, pos in pts:
            print(f"  {n:<6} blk={blk:<4} combP={combP:<3} pos={pos}")
