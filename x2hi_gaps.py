#!/usr/bin/env python3
"""x2hi_gaps.py -- characterize the UNCOVERED residue of the blank -> M1(1) cover.

Groups the gaps by the (st,h) WORD of the gap window.  Method invariant 2: every
transition is a total function of (state,bit), so the (st,h) word over a window
DETERMINES every write, every move and the whole trace -- so two gaps with the same
word are the SAME motif, and gaps with different words are genuinely different, no
matter what their lengths are.  Lengths are reported but NEVER used to identify.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2hi_sim import Sim, clone
from x2hi_cover import cover
from x2hi_m1 import rle_str


def word_at(s, n):
    t = clone(s)
    w = []
    for _ in range(n):
        w.append((t.st, t.read()))
        t.step()
    return tuple(w)


def ctx(s, lo=-14, hi=26):
    bits = [s.cells.get(s.pos + k, 0) for k in range(lo, hi)]
    i = -lo
    return ''.join(str(b) for b in bits[:i]) + '[' + str(bits[i]) + ']' + \
           ''.join(str(b) for b in bits[i + 1:])


def main():
    s, inst, gaps = cover()
    print('=== the uncovered residue, grouped BY WORD (not by length) ===')
    print('%d gaps, %d steps (%.1f%% of 188 099)\n'
          % (len(gaps), sum(L for _, L in gaps),
             100.0 * sum(L for _, L in gaps) / 188099))

    # replay to collect each gap's word + entry config
    fam = {}
    t = Sim()
    for start, L in gaps:
        while t.n < start:
            t.step()
        w = word_at(t, L)
        f = fam.setdefault(w, {'len': L, 'starts': [], 'ctx': ctx(t), 'st': t.st})
        f['starts'].append(start)

    rows = sorted(fam.values(), key=lambda f: -f['len'] * len(f['starts']))
    print('%-6s %-6s %-9s  %s' % ('len', 'count', 'steps', 'entry context (head in [])'))
    tot = 0
    for f in rows:
        n = len(f['starts'])
        tot += f['len'] * n
        print('%-6d %-6d %-9d  %s  st=%s  first@%d'
              % (f['len'], n, f['len'] * n, f['ctx'], f['st'], f['starts'][0]))
    print('\ndistinct motifs (by word): %d   total steps: %d' % (len(rows), tot))

    print('\n=== the 5 largest single gaps, in detail ===')
    t = Sim()
    for start, L in sorted(gaps, key=lambda g: -g[1])[:5]:
        t2 = Sim()
        while t2.n < start:
            t2.step()
        lo, hi = t2.extent()
        row = [t2.cells.get(p, 0) for p in range(lo, hi + 1)]
        print('\n-- gap @%d, length %d, st=%s pos=%d' % (start, L, t2.st, t2.pos))
        print('   tape from head: %s' % rle_str(row[t2.pos - lo:], maxtok=24))
        print('   left of head  : %s' % (rle_str(row[:t2.pos - lo][::-1], maxtok=24) or '(blank)'))


if __name__ == '__main__':
    main()
