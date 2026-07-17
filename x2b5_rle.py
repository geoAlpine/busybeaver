"""x2b5_rle.py -- B5's tape in run-length coordinates.

The tape is (empirically) a sequence of 1-runs separated by single 0s.
We RLE the 1-run lengths at successive left-record milestones in state C and
watch how the run-length WORD evolves -- this is where any register/rewrite
rule would live, if one exists.
"""
import sys
from collections import Counter
from x2b5_sim import RULES

def rle(cells, lo, hi):
    runs = []; cur = 0; gaps = []
    g = 0
    for p in range(lo, hi + 1):
        if cells.get(p, 0):
            if g: gaps.append(g); g = 0
            cur += 1
        else:
            if cur: runs.append(cur); cur = 0
            g += 1
    if cur: runs.append(cur)
    return runs, gaps

def run(max_steps, want='C'):
    cells = {}; pos = 0; state = 'A'; lo = hi = 0
    snaps = []
    for step in range(max_steps):
        sym = cells.get(pos, 0)
        rule = RULES[state][sym]
        if rule is None:
            print("HALT", step); break
        w, mv, nxt = rule
        if w != sym:
            if w: cells[pos] = 1
            else: del cells[pos]
        pos += mv; state = nxt
        if pos < lo:
            lo = pos
            if state == want:
                snaps.append((step, lo, hi) + rle(cells, lo, hi))
    return snaps

if __name__ == '__main__':
    snaps = run(400000)
    print("snapshots:", len(snaps))
    for step, lo, hi, runs, gaps in snaps[-5:]:
        print(f"\nstep={step} lo={lo} hi={hi} nruns={len(runs)}")
        print("  run lengths:", runs)
        print("  gap lengths (0-blocks) multiset:", dict(Counter(gaps)))
    print("\n# run-length value distribution over last snapshot")
    print(" ", dict(sorted(Counter(snaps[-1][3]).items())))
    print("\n# run lengths mod 3 over last snapshot")
    print(" ", dict(sorted(Counter(r % 3 for r in snaps[-1][3]).items())))
