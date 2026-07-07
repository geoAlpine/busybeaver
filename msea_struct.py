#!/usr/bin/env python3
"""
Mahler-sea survey — STRUCTURE stage (2026-07-07).
For each machine: milestone snapshots (RLE of the 1-blocks at every gate-trigger event),
then post-process:
  (1) shape-class census (blocks > T abstracted to '*'): rigid template vs unbounded growth
      (o17-style refutation test). RLE-based, so NOT period-capped (Space Needle's x5/2
      sweeps are captured; the old period<=8 sweep-detector cap does not apply here).
  (2) counter-law fit over consecutive same-shape milestones: which m' = floor(p*m/q)+c
      (p/q in {3/2, 5/2, 4/3, 8/3, 2}) fits which block exactly, over how many generations.
  (3) margin censuses: interior 00-count near the trigger (o11/o12/o14/o16 protection =
      "no 00 in the field"); o13 sweep-start run-length parity (halt iff EVEN run).
All [OBSERVED]/[VERIFIED-numeric]. Decides nothing.
"""
import sys
from collections import defaultdict, Counter

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

SN = "ABCDEF"

MACHINES = [
    ("o11", "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", 1, 0, -1),
    ("o12", "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB", 4, 0, +1),
    ("o13", "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 3, 1, -1),
    ("o14", "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 2, 0, -1),
    ("o16", "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", 4, 0, +1),
    ("SN",  "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD", 2, 0, -1),
]

def rle_blocks(tape, lo, hi):
    """List of (start,len) of 1-runs in tape[lo..hi]."""
    blocks = []
    i = lo
    while i <= hi:
        if tape[i]:
            j = i
            while j <= hi and tape[j]:
                j += 1
            blocks.append(j - i)
            i = j
        else:
            i += 1
    return blocks

def gaps_profile(tape, lo, hi):
    """Count 00 (two adjacent interior zeros strictly between first and last 1)."""
    # find first/last 1
    a = lo
    while a <= hi and not tape[a]:
        a += 1
    b = hi
    while b >= lo and not tape[b]:
        b -= 1
    if a >= b:
        return 0
    cnt = 0
    run = 0
    for i in range(a, b + 1):
        if tape[i]:
            run = 0
        else:
            run += 1
            if run == 2:
                cnt += 1
    return cnt

def run_struct(spec, tstate, tread, N, max_snap=4000, o13_parity=False):
    M = parse(spec)
    SZ = 1 << 23
    tape = bytearray(SZ)
    pos = SZ // 2
    st = 0
    lo = hi = pos
    snaps = []           # (step, blocks, zz_count)
    parities = Counter() # o13: run parity at sweep starts
    prev_st = -1
    step = 0
    while step < N:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            break
        if st == tstate and r == tread and len(snaps) < max_snap:
            blocks = rle_blocks(tape, lo, hi)
            zz = gaps_profile(tape, lo, hi)
            snaps.append((step, blocks, zz))
        if o13_parity and st == 3 and r == 1 and prev_st != 4:  # D,1 sweep-start, prev not E
            L = 0
            i = pos
            while tape[i]:
                L += 1
                i -= 1
            parities[L & 1] += 1
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        prev_st = st
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return snaps, parities

LAWS = [(3, 2), (5, 2), (4, 3), (8, 3), (2, 1)]

def shape(blocks, T=4):
    return tuple(b if b <= T else '*' for b in blocks)

def analyze(name, snaps, parities):
    print(f"=== {name}: {len(snaps)} milestone snapshots (gate-trigger events)")
    if not snaps:
        return
    # (1) shape census
    shapes = [shape(b) for _, b, _ in snaps]
    seen, firsts = set(), []
    for i, sh in enumerate(shapes):
        if sh not in seen:
            seen.add(sh)
            firsts.append(i)
    half = len(shapes) // 2
    new_late = sum(1 for i in firsts if i >= half)
    print(f"  shape classes: {len(seen)} distinct / {len(shapes)} gens; "
          f"new in 2nd half: {new_late}  -> {'RIGID-template-compatible' if new_late == 0 else 'shapes still appearing (o17-style?)'}")
    top = Counter(shapes).most_common(4)
    for sh, ct in top:
        s = ','.join(str(x) for x in sh[:14]) + ('...' if len(sh) > 14 else '')
        print(f"    x{ct:<6} [{s}]  ({len(sh)} blocks)")
    # (2) counter laws: candidate scalar series = largest block; #blocks (sea size proxy)
    big = [max(b) for _, b, _ in snaps]
    nb = [len(b) for _, b, _ in snaps]
    lead = [b[0] for _, b, _ in snaps]
    tailb = [b[-1] for _, b, _ in snaps]
    for label, series in (("max-block", big), ("#blocks(sea)", nb), ("first-block", lead), ("last-block", tailb)):
        best = None
        for p, q in LAWS:
            for c in range(-8, 9):
                hits = sum(1 for i in range(len(series) - 1)
                           if series[i] >= 2 and series[i + 1] == (p * series[i]) // q + c)
                tries = sum(1 for i in range(len(series) - 1) if series[i] >= 2)
                if tries and (best is None or hits > best[0]):
                    best = (hits, tries, p, q, c)
        if best and best[0] > 0:
            h, t, p, q, c = best
            print(f"  law fit [{label:>12}]: m'=floor({p}m/{q})+{c:+d}  exact {h}/{t} consecutive gens "
                  f"({100*h/t:.0f}%)  series head: {series[:8]} ... tail: {series[-4:]}")
    # monotone-increasing subseries ratio check on max-block (growth events only)
    inc = [v for i, v in enumerate(big) if i == 0 or v > big[i - 1]]
    if len(inc) > 3:
        rt = [f"{inc[i+1]/inc[i]:.3f}" for i in range(max(0, len(inc) - 6), len(inc) - 1)]
        print(f"  max-block growth-event ratios (last): {rt}")
    # (3) margins
    zz = [z for _, _, z in snaps]
    print(f"  interior-00 census at milestones: min={min(zz)} max={max(zz)} "
          f"(protection field: {'NO interior 00 ever' if max(zz)==0 else '00s present'})")
    if parities:
        print(f"  o13 sweep-start run parity: odd(safe)={parities[1]}, even(FATAL)={parities[0]}")
    print()

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    for name, spec, ts, tr, nd in MACHINES:
        snaps, par = run_struct(spec, ts, tr, N, o13_parity=(name == "o13"))
        analyze(name, snaps, par)
    print("STRUCTURE STAGE [OBSERVED/numeric-exact on stated gens]. No machine decided. No label upgraded.")
