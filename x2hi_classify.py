#!/usr/bin/env python3
"""x2hi_classify.py -- classify the residue motifs for the h_init blueprint.

For each maximal gap:
  * its WORD (identity, method inv. 2), and thus its motif class;
  * head-excursion SPAN over the window (max |pos - pos_start|) -> is the window
    BOUNDED (a fixed reusable tile) or GROWING (a per-level carry landing);
  * the covered lemma IMMEDIATELY BEFORE and AFTER (method inv. 3: pin by BOTH
    endpoints, not by length).

Then split the residue into:
  (A) REPEATED fixed-window motifs  -> each is ONE new bounded (∀L∀R) tile lemma;
  (B) SINGLETON motifs              -> each a bounded concrete kernel run.
Neither needs a ∀k law: blank->M1(1) is a SINGLE finite trajectory.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2hi_sim import Sim, clone
from x2hi_cover import cover
from x2hi_gaps import word_at


def span(s, n):
    t = clone(s)
    p0 = t.pos
    lo = hi = 0
    for _ in range(n):
        t.step()
        lo = min(lo, t.pos - p0)
        hi = max(hi, t.pos - p0)
    return lo, hi, t.pos - p0


def main():
    s, inst, gaps = cover()
    # index instances by start for before/after lookup
    starts = {st: (name, cnt) for st, name, _, cnt in inst}
    ends = {}
    for st, name, _, cnt in inst:
        ends[st + cnt] = (name, cnt)

    gapset = {st: L for st, L in gaps}
    # replay, collecting per-gap info
    t = Sim()
    recs = []
    covend = {}  # step where a covered inst ends
    for st, L in gaps:
        while t.n < st:
            t.step()
        w = word_at(t, L)
        lo, hi, dp = span(t, L)
        before = ends.get(st, ('<start>', 0))[0]
        after = starts.get(st + L, ('<end:M1(1)>', 0))[0]
        recs.append({'st': st, 'L': L, 'w': w, 'span': hi - lo,
                     'lo': lo, 'hi': hi, 'before': before, 'after': after})

    # group by word
    fam = {}
    for r in recs:
        f = fam.setdefault(r['w'], {'L': r['L'], 'span': r['span'],
                                    'n': 0, 'before': set(), 'after': set(),
                                    'first': r['st']})
        f['n'] += 1
        f['before'].add(r['before'])
        f['after'].add(r['after'])

    rows = sorted(fam.values(), key=lambda f: -f['L'] * f['n'])
    print('=== residue motifs: role + bounded/growing ===')
    print('%-5s %-5s %-7s %-6s  %-22s -> %-22s' %
          ('len', 'cnt', 'steps', 'span', 'preceded by', 'followed by'))
    A_lemmas = 0
    A_steps = 0
    B_count = 0
    B_steps = 0
    for f in rows:
        bef = ','.join(sorted(f['before']))
        aft = ','.join(sorted(f['after']))
        tag = 'REPEAT' if f['n'] > 1 else 'single'
        print('%-5d %-5d %-7d span%-3d  %-22s -> %-22s  [%s]' %
              (f['L'], f['n'], f['L'] * f['n'], f['span'], bef[:22], aft[:22], tag))
        if f['n'] > 1:
            A_lemmas += 1
            A_steps += f['L'] * f['n']
        else:
            B_count += 1
            B_steps += f['L']

    print('\n=== blueprint split of the %d-step residue ===' % sum(r['L'] for r in recs))
    print('(A) REPEATED fixed-window motifs : %d distinct words, %d steps' % (A_lemmas, A_steps))
    print('    -> %d new bounded (∀L∀R) tile lemmas (kernel rfl), each reused' % A_lemmas)
    print('(B) SINGLETON motifs             : %d gaps, %d steps' % (B_count, B_steps))
    print('    -> each a bounded concrete kernel run (max window %d steps)'
          % max((r['L'] for r in recs if fam[r['w']]['n'] == 1), default=0))
    mx = max(r['span'] for r in recs)
    print('\nmax head-excursion span over ANY residue gap: %d cells' % mx)
    print('longest residue gap: %d steps (kernel-feasible; cf. regen6_transport = 722 brute)'
          % max(r['L'] for r in recs))


if __name__ == '__main__':
    main()
