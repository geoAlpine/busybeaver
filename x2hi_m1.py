#!/usr/bin/env python3
"""x2hi_m1.py -- what IS M1(1), cell-for-cell?

Runs the VERIFIED blank-tape simulator (x2hi_sim, checked against X2.lean's
sanity50/sanity100) to raw step 188 099 and reads the tape off exactly.
Also independently RE-DERIVES the milestone index from X2.lean's own spec
("the E-milestone whose leading 0-gap is exactly 22") rather than trusting 188 099.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2hi_sim import Sim, clone


def rle(bits):
    out = []
    for b in bits:
        if out and out[-1][0] == b:
            out[-1][1] += 1
        else:
            out.append([b, 1])
    return [(b, c) for b, c in out]


def rle_str(bits, maxtok=40):
    toks = ['%d^%d' % (b, c) if c > 1 else str(b) for b, c in rle(bits)]
    if len(toks) > maxtok:
        toks = toks[:maxtok // 2] + ['...(%d more)' % (len(toks) - maxtok)] + toks[-maxtok // 2:]
    return ' '.join(toks)


def tape_row(s):
    """the FULL tape as a bit list, extent DERIVED from the tape (min/max cells)."""
    lo, hi = s.extent()
    return lo, hi, [s.cells.get(p, 0) for p in range(lo, hi + 1)]


def leading_gap(s):
    """length of the 0-run immediately right of the head (the 'leading 0-gap')."""
    n = 0
    p = s.pos
    while s.cells.get(p, 0) == 0:
        n += 1
        p += 1
        if n > 100:
            break
    return n


def main():
    N = 188099
    s = Sim()
    # --- independent milestone scan: E-configs whose leading 0-gap is exactly 22
    hits = []
    for i in range(N + 1):
        if s.st == 'E' and s.read() == 0 and leading_gap(s) == 22:
            hits.append(s.n)
        if i < N:
            if not s.step():
                print('HALTED at %d' % s.n)
                return
    print('=== independent milestone scan (X2.lean spec: E-config, leading 0-gap == 22) ===')
    print('steps <= %d with that signature: %s' % (N, hits))
    print('X2.lean records M1(1) @ 188 099 ->  %s'
          % ('CONFIRMED (and it is the FIRST such config)'
             if hits and hits[-1] == N and len(hits) == 1
             else 'hits=%s' % hits))

    lo, hi, row = tape_row(s)
    print('\n=== M1(1) @ raw step %d, cell-for-cell ===' % s.n)
    print('state      : %s' % s.st)
    print('pos        : %d' % s.pos)
    print('tape extent (DERIVED from min/max of set cells): [%d, %d]  (%d cells)'
          % (lo, hi, hi - lo + 1))
    print('head at pos %d = index %d in the row' % (s.pos, s.pos - lo))
    print('ones on tape: %d' % sum(row))
    print('\nRLE of the FULL tape (leftmost -> rightmost):')
    print('  ' + rle_str(row, maxtok=200))
    print('\nRLE from the HEAD rightwards (this is the M1 form X2.lean quotes):')
    print('  ' + rle_str(row[s.pos - lo:], maxtok=200))
    print('\nRLE left of head (nearest-first = Lean `left`):')
    print('  ' + rle_str(row[:s.pos - lo][::-1], maxtok=200))


if __name__ == '__main__':
    main()
