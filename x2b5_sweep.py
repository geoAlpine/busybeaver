"""x2b5_sweep.py -- is B5 a uniform sweep with a shift rule?

Milestone = the step at which the head sets a NEW LEFTMOST record while the
tape's left end is extended. We dump the full tape at successive milestones of
the same (state, pos-lo) phase and look for a "prefix + BLOCK^n + suffix"
skeleton whose n grows by a fixed amount per milestone.
"""
import sys
from x2b5_sim import RULES, extent

def tapestr(cells, lo=None, hi=None):
    lo, hi = extent(cells)          # FULL written extent -- never truncate
    return ''.join('1' if cells.get(p, 0) else '0' for p in range(lo, hi + 1))

def run(max_steps, want):
    cells = {}; pos = 0; state = 'A'; lo = 0
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
                snaps.append((step, state, pos) + extent(cells) + (tapestr(cells),))
    return snaps

if __name__ == '__main__':
    snaps = run(600000, 'C')
    print("left-record snapshots in state C:", len(snaps))
    sel = snaps[-6:]
    for step, st, pos, lo, hi, s in sel:
        print(f"\nstep={step} state={st} lo={lo} hi={hi} width={len(s)}")
        print("  L40:", s[:40], " ...  R60:", s[-60:])
    # look for a periodic core: longest p in 1..12 s.t. a long stretch is p-periodic
    print("\n# periodicity scan of the last snapshot")
    s = sel[-1][5]
    for p in range(1, 13):
        best = cur = 0
        for i in range(p, len(s)):
            if s[i] == s[i - p]:
                cur += 1
                best = max(best, cur)
            else:
                cur = 0
        print(f"  period {p:>2}: longest {p}-periodic stretch = {best + p if best else 0} / {len(s)}")
