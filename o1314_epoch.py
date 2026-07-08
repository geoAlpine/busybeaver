#!/usr/bin/env python3
"""
o13/o14 fixed-point deep dive, part 2: EPOCH STRUCTURE + a-start x3/2 recursion (2026-07-08).
Extract, from the blank orbit, the milestone chain decoded as counters; fit
  (i)   in-epoch counter law (a,b) -> (a-2, b+3)
  (ii)  the a-start recursion  a' = floor(3a/2) + c  and report c BY PARITY of a
  (iii) collapse values + refill sea growth.
All [OBSERVED on the orbit]. Decides nothing.
"""
import sys
from collections import Counter
from msea_struct2 import parse, rle_blocks

MACH = {
    "o13": ("1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 2, 'L'),
    "o14": ("1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 4, 'L'),
}

def milestones(spec, mstate, side, N, maxsnap=100000):
    M = parse(spec)
    SZ = 1 << 24
    tape = bytearray(SZ)
    pos = SZ // 2
    st = 0
    lo = hi = pos
    snaps = []
    last = None
    step = 0
    while step < N and len(snaps) < maxsnap:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            snaps.append((step, 'HALT'))
            break
        at_ext = (pos <= lo) if side == 'L' else (pos >= hi)
        if st == mstate and at_ext:
            b = rle_blocks(tape, lo, hi)
            if b != last:
                snaps.append((step, list(b)))
                last = list(b)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return snaps

def analyze_o13(snaps):
    print("=== o13 epoch analysis ===")
    # decode each milestone as (a, b, m) where blocks = [a, b, 1*m]  (b may be any)
    # In-epoch: blocks length>=2, blocks[2:] all ones.
    dec = []
    for s, b in snaps:
        if b == 'HALT':
            dec.append((s, 'HALT', b)); continue
        if len(b) >= 2 and all(x == 1 for x in b[2:]):
            dec.append((s, (b[0], b[1], len(b) - 2), b))
        elif len(b) == 1:
            dec.append((s, ('COLLAPSE', b[0]), b))
        else:
            dec.append((s, ('OTHER', tuple(b[:6])), b))
    # in-epoch (a,b) deltas where both consecutive are (a,b,m) triples with same m
    da = Counter()
    for i in range(len(dec) - 1):
        x, y = dec[i][1], dec[i + 1][1]
        if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == 3 and len(y) == 3 and x[2] == y[2]:
            da[(y[0] - x[0], y[1] - x[1])] += 1
    print(f"  in-epoch (da,db) census: {dict(da.most_common(6))}")
    # collapse events
    cols = [(s, d[1]) for s, d, b in dec if isinstance(d, tuple) and d[0] == 'COLLAPSE']
    print(f"  collapse [1^c] events (t,c): {cols[:12]}")
    # collapse c vs preceding (2,b,m): c = b+3 ?
    for i in range(1, len(dec)):
        d = dec[i][1]
        if isinstance(d, tuple) and d and d[0] == 'COLLAPSE':
            p = dec[i - 1][1]
            if isinstance(p, tuple) and len(p) == 3:
                print(f"    collapse c={d[1]} from (a,b,m)={p}: b+3={p[1]+3}, a+b+1={p[0]+p[1]+1}")
    # a-start recursion: sub-cycle starts where b-block == 4 (2nd block ==4)
    astarts = [(s, d[0], d[2]) for s, d, b in dec if isinstance(d, tuple) and len(d) == 3 and d[1] == 4]
    print(f"  a-starts [a,4,1^m] (t,a,m): {[(a) for _, a, _ in astarts][:20]}")
    fit_x32(astarts, "o13 a-start")

def analyze_o14(snaps):
    print("=== o14 epoch analysis ===")
    # blocks = [a, 1, b, <single-1 field>, 4, 4, 2] early; later [a,1,b,2] pure two-counter
    # counters at RLE blocks (0,2): a=block0, b=block2
    dec = []
    for s, b in snaps:
        if b == 'HALT':
            dec.append((s, 'HALT', b)); continue
        if len(b) >= 3 and b[1] == 1:
            dec.append((s, (b[0], b[2], tuple(b[3:])), b))
        else:
            dec.append((s, ('OTHER', tuple(b[:8])), b))
    da = Counter()
    for i in range(len(dec) - 1):
        x, y = dec[i][1], dec[i + 1][1]
        if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == 3 and x[0] != 'OTHER' and len(y) == 3 and y[0] != 'OTHER' and x[2] == y[2]:
            da[(y[0] - x[0], y[1] - x[1])] += 1
    print(f"  in-epoch (da,db) census (same tail): {dict(da.most_common(6))}")
    # a-start: sub-cycle where inner b == 7
    astarts = [(s, d[0], d[2]) for s, d, b in dec if isinstance(d, tuple) and len(d) == 3 and d[0] != 'OTHER' and d[1] == 7]
    print(f"  a-starts [a,1,7,...] (t,a): {[a for _, a, _ in astarts][:20]}")
    fit_x32(astarts, "o14 a-start")
    # marker tail census
    tails = Counter(d[2] for s, d, b in dec if isinstance(d, tuple) and len(d) == 3 and d[0] != 'OTHER')
    print(f"  tail (blocks after b) census top: {dict(tails.most_common(5))}")

def fit_x32(astarts, label):
    aser = [a for _, a, _ in astarts]
    print(f"  {label}: sequence {aser[:24]}")
    # fit a' = floor(3a/2)+c, report c by parity of a
    byp = {0: Counter(), 1: Counter()}
    for i in range(len(aser) - 1):
        a0, a1 = aser[i], aser[i + 1]
        if a1 > a0:  # forward step (skip refill resets which drop)
            c = a1 - (3 * a0) // 2
            byp[a0 & 1][c] += 1
    print(f"    c = a' - floor(3a/2) by parity: even-a {dict(byp[0])}, odd-a {dict(byp[1])}")

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000_000
    for name in ("o13", "o14"):
        spec, ms, side = MACH[name]
        snaps = milestones(spec, ms, side, N)
        print(f"[{name}] {len(snaps)} milestones over N={N}")
        (analyze_o13 if name == "o13" else analyze_o14)(snaps)
        print()
