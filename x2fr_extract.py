#!/usr/bin/env python3
"""x2fr_extract.py -- FAITHFUL extraction of the odometer event sequence.

Dump the exact sequence of chew-starts (local maxima of the leading right block
at E-on-0 anchors) with (blk, comb, ones) across the doubling phase M6(K)->M1(K+1),
for g=2 and g=3.  This is the raw event stream the abstract register must reproduce.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import run, chew_starts


def extract(g):
    anchors = run(g)
    starts, pts = chew_starts(anchors)
    seq = [(blk, comb) for (n, blk, comb, ones, pos) in starts]
    return seq, len(pts)


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    seq, npts = extract(g)
    print(f"=== g={g} K={g+8}: {len(seq)} chew-starts, {npts} E-on-0 anchors ===")
    print("FIRST 80 (blk,comb):")
    for i in range(0, min(80, len(seq)), 8):
        print("  ", seq[i:i+8])
    print("LAST 40 (blk,comb):")
    for i in range(max(0, len(seq)-40), len(seq), 8):
        print("  ", seq[i:i+8])
    # distribution of blk values
    from collections import Counter
    c = Counter(b for b, _ in seq)
    print("blk distribution (blk: count):", dict(sorted(c.items())))
