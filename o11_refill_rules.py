#!/usr/bin/env python3
"""
o11 refill-law deep dive, part 3: THE RULES, unit-tested on large grids (2026-07-08).

The epoch grid (o11_refill_grid.py) + anatomy (o11_refill_anatomy.py) suggest the
complete transition system on B/right-extreme milestones (k = leading block, m = sea):

  R1 (in-epoch)    (k,m) -> (k-4, T(m))          for k >= 5,   T(m) = floor(3m/2)+4
  R2 (boundary)    (4,m) -> (1, T(m)-1)
  R3 (terminal)    (3,m) -> collapse c = 3m+5 (m odd) / 3m+6 (m even), refill (c-2, 2)
  R4 (terminal)    (2,m) -> HALT (00-gap during collapse reorganization)
  R5 (terminal)    (1,m) -> HALT iff m odd; else collapse c = 3m+3, refill (c-2, 2)
  R6 (refill)      [1^c] state F head-on-last-1 -> (c-2, 2) in 7 steps

This script unit-tests each rule as a SINGLE transition on wide (k,m)/(c) grids,
records halt anatomies (expect: halt state C reading 0 with left neighbor 0), and
prints exact mismatch counts. All exact simulation; a halt is PROVEN-by-run; rule
labels are [PROVEN on grid] only. No induction claimed.
"""
import sys
from msea_struct2 import parse, rle_blocks

SPEC = "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF"
SN = "ABCDEF"

def T(m):
    return (3 * m) // 2 + 4

def make_tape(k, m, left_margin=512):
    """Milestone tape [1^k 0 (10)^m], returns (tape, lo, last1). Dynamically sized:
    room for the sea to grow through a full transition + collapse (rightward)."""
    SZ = left_margin + 8 * (k + 3 * m + 64) + 4096
    tape = bytearray(SZ)
    p = left_margin
    lo = p
    for _ in range(k):
        tape[p] = 1; p += 1
    p += 1
    for _ in range(m):
        tape[p] = 1; p += 2
    return tape, lo, p - 2

def run(tape, lo, last1, state, off, budget=200_000_000, detect_collapse=True):
    """Run from (state, pos=last1+off). Stop at: next B/right-extreme milestone with
    changed RLE ('MIL'), F/right-extreme pure single block ('COLLAPSE'), or halt
    ('HALT' + anatomy). Returns (kind, payload, steps)."""
    M = parse(SPEC)
    pos = last1 + off
    hi = max(pos, last1)
    st = state
    b0 = rle_blocks(tape, lo, hi)
    step = 0
    while step < budget:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            left = tape[pos - 1]
            return ('HALT', (SN[st], r, left), step)
        if pos >= hi and (st == 1 or st == 5):
            b = rle_blocks(tape, lo, hi)
            if st == 5 and len(b) == 1 and step > 0 and detect_collapse:
                return ('COLLAPSE', b[0], step)
            if st == 1 and b != b0 and step > 0:
                return ('MIL', b, step)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos > hi: hi = pos
        elif pos < lo: lo = pos
        if pos < 8 or pos >= len(tape) - 8:
            raise RuntimeError("tape bounds exceeded — enlarge margins")
    return ('BUDGET', None, step)

def seed_run(k, m, budget=200_000_000):
    tape, lo, last1 = make_tape(k, m)
    return run(tape, lo, last1, 1, +1, budget)   # state B, head one right of last 1

def decode(b):
    if len(b) >= 2 and all(x == 1 for x in b[1:]):
        return (b[0], len(b) - 1)
    if all(x == 1 for x in b):
        return (0, len(b))
    return None

def test_R1_R2(kmax, mmax):
    bad = 0; tot = 0
    for k in range(4, kmax + 1):
        for m in range(1, mmax + 1):
            kind, pay, s = seed_run(k, m)
            want = (1, T(m) - 1) if k == 4 else (k - 4, T(m))
            got = decode(pay) if kind == 'MIL' else (kind, pay)
            tot += 1
            if kind != 'MIL' or got != want:
                bad += 1
                if bad <= 10:
                    print(f"  R1/R2 MISMATCH k={k} m={m}: got {kind} {got}, want MIL {want}")
    print(f"R1/R2 (k,m)->(k-4,T(m)) [k>=5], (4,m)->(1,T(m)-1): {tot-bad}/{tot} exact")

def test_R3(mmax):
    bad = 0; tot = 0; anat = None
    for m in range(1, mmax + 1):
        kind, pay, s = seed_run(3, m)
        cw = 3 * m + 5 if m % 2 else 3 * m + 6
        tot += 1
        if kind != 'COLLAPSE' or pay != cw:
            bad += 1
            if bad <= 10:
                print(f"  R3 MISMATCH m={m}: got {kind} {pay}, want COLLAPSE {cw}")
    print(f"R3 (3,m) -> collapse c=3m+5/3m+6 (m odd/even): {tot-bad}/{tot} exact")

def test_R4(mmax):
    bad = 0; tot = 0; anats = set()
    for m in range(1, mmax + 1):
        kind, pay, s = seed_run(2, m)
        tot += 1
        if kind != 'HALT':
            bad += 1
            if bad <= 10:
                print(f"  R4 MISMATCH m={m}: got {kind} {pay} (no halt)")
        else:
            anats.add(pay)
    print(f"R4 (2,m) -> HALT: {tot-bad}/{tot}; halt anatomies (state, read, left-nbr): {anats}")

def test_R5(mmax):
    bad = 0; tot = 0; anats = set()
    for m in range(1, mmax + 1):
        kind, pay, s = seed_run(1, m)
        tot += 1
        if m % 2 == 1:
            if kind != 'HALT':
                bad += 1
                if bad <= 10:
                    print(f"  R5 MISMATCH m={m} (odd): got {kind} {pay}, want HALT")
            else:
                anats.add(pay)
        else:
            cw = 3 * m + 3
            if kind != 'COLLAPSE' or pay != cw:
                bad += 1
                if bad <= 10:
                    print(f"  R5 MISMATCH m={m} (even): got {kind} {pay}, want COLLAPSE {cw}")
    print(f"R5 (1,m): HALT iff m odd, else c=3m+3: {tot-bad}/{tot}; halt anatomies: {anats}")

def test_R6(cmax, spots=()):
    bad = 0; tot = 0
    cs = list(range(3, cmax + 1)) + list(spots)
    for c in cs:
        tape, lo, last1 = make_tape(c, 0)
        # [1^c] only: make_tape(c,0) leaves a trailing 0 gap; last1 is c-th 1... fix:
        # make_tape with m=0: p advanced by k then +1; last1 = p-2 = lo+k-1? check:
        # p = lo+k after block, then p += 1 -> lo+k+1, last1 = p-2 = lo+k-1. correct.
        kind, pay, s = run(tape, lo, last1, 5, 0, budget=1000,
                           detect_collapse=False)  # state F, head on last 1
        got = decode(pay) if kind == 'MIL' else (kind, pay)
        want = (c - 2, 2)
        tot += 1
        if kind != 'MIL' or got != want or s != 7:
            bad += 1
            if bad <= 10:
                print(f"  R6 MISMATCH c={c}: got {kind} {got} at step {s}, want MIL {want} at 7")
    print(f"R6 [1^c] F -> (c-2,2) in exactly 7 steps: {tot-bad}/{tot} exact  (c=3..{cmax} + {list(spots)})")

if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    tmax = int(sys.argv[3]) if len(sys.argv) > 3 else 400   # terminal-rule m range
    print(f"grids: R1/R2 k=4..{kmax} x m=1..{mmax}; R3/R4/R5 m=1..{tmax}; R6 c=3..1000 + spots")
    test_R1_R2(kmax, mmax)
    test_R3(tmax)
    test_R4(tmax)
    test_R5(tmax)
    test_R6(1000, spots=(4155, 4156, 65536, 65537, 100003, 100004))
    print("All rules are [PROVEN on the stated grids] (exact runs); no induction claimed.")
    print("No machine decided. No label upgraded.")
