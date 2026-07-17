#!/usr/bin/env python3
"""x2hi_cover.py -- greedy-maximal TRANSPORT cover of the blank -> M1(1) run.

At every on-path step we ask: does some PROVEN `∀`-parametric Lean theorem apply to
THIS config (IN pattern matched cell-for-cell), and does the machine really produce
the OUT it asserts (verified by simulation)?  If several do, take the longest.
Otherwise advance one raw step and count it as UNCOVERED.

Output: the covered fraction, the per-lemma step/instance budget, and the uncovered
residue broken into maximal contiguous gaps (the NAMED GAPS = the new work).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2hi_sim import Sim
from x2hi_transport import MATCHERS, verify

N_TARGET = 188099


def cover(limit=N_TARGET, verbose_gaps=12):
    s = Sim()
    inst = []          # (start, name, params, count)
    gaps = []          # (start, length)
    gap_start = None
    while s.n < limit:
        cands = []
        for m in MATCHERS:
            c = m(s)
            if c is not None and c[2] >= 1 and s.n + c[2] <= limit:
                cands.append(c)
        cands.sort(key=lambda c: -c[2])
        hit = None
        for c in cands:
            if verify(s, c):
                hit = c
                break
        if hit is None:
            if gap_start is None:
                gap_start = s.n
            if not s.step():
                raise RuntimeError('HALT at %d' % s.n)
            continue
        if gap_start is not None:
            gaps.append((gap_start, s.n - gap_start))
            gap_start = None
        inst.append((s.n, hit[0], hit[1], hit[2]))
        for _ in range(hit[2]):
            s.step()
    if gap_start is not None:
        gaps.append((gap_start, s.n - gap_start))
    return s, inst, gaps


def main():
    s, inst, gaps = cover()
    covered = sum(c for _, _, _, c in inst)
    total = s.n
    print('=== TRANSPORT COVER of blank -> M1(1) ===')
    print('raw steps           : %d' % total)
    print('covered by proven ∀ : %d  (%.1f%%)' % (covered, 100.0 * covered / total))
    print('uncovered           : %d  (%.1f%%)  in %d maximal gaps'
          % (total - covered, 100.0 * (total - covered) / total, len(gaps)))
    print('theorem instances   : %d' % len(inst))

    print('\n--- per-lemma budget (steps, instances) ---')
    agg = {}
    for _, name, _, c in inst:
        a = agg.setdefault(name, [0, 0])
        a[0] += c
        a[1] += 1
    for name, (st, k) in sorted(agg.items(), key=lambda x: -x[1][0]):
        print('  %-24s %8d steps (%5.1f%%)  %6d instances'
              % (name, st, 100.0 * st / total, k))

    print('\n--- the uncovered residue: %d gaps, %d steps ---'
          % (len(gaps), total - covered))
    glen = {}
    for st, L in gaps:
        glen[L] = glen.get(L, 0) + 1
    print('  gap-length histogram (length: count):')
    for L in sorted(glen):
        print('     %4d : %5d   (= %d steps)' % (L, glen[L], L * glen[L]))
    print('  largest gaps (start, length):')
    for st, L in sorted(gaps, key=lambda g: -g[1])[:12]:
        print('     @%7d  len %d' % (st, L))
    return s, inst, gaps


if __name__ == '__main__':
    main()
