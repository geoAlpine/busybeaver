"""x2b5_mod3.py -- is ANY bounded mod-3 run-length invariant true on the FULL tape?

The first (buggy, left-half-only) probe claimed: every run == 2 mod 3 bar exactly
2 boundary runs. On the FULL tape that is FALSE. This probe asks the weaker
question: is the NUMBER of runs !=2 (mod 3) BOUNDED as the orbit grows, and are
the exceptions confined to the tape boundary?
"""
import sys
from collections import Counter
from x2b5_sim import RULES, extent

def run(max_steps):
    cells = {}; pos = 0; state = 'A'; lo = 0
    rows = []
    for step in range(max_steps):
        sym = cells.get(pos, 0)
        rule = RULES[state][sym]
        if rule is None:
            print("*** HALT", step); break
        w, mv, nxt = rule
        if w != sym:
            if w: cells[pos] = 1
            else: del cells[pos]
        pos += mv; state = nxt
        if pos < lo:
            lo = pos
            if state == 'C':
                elo, ehi = extent(cells)
                runs = []; cur = 0
                for p in range(elo, ehi + 1):
                    if cells.get(p, 0): cur += 1
                    else:
                        if cur: runs.append(cur)
                        cur = 0
                if cur: runs.append(cur)
                bad = [i for i, r in enumerate(runs) if r % 3 != 2]
                # interior = not among the first/last 2 runs
                interior = [i for i in bad if 2 <= i < len(runs) - 2]
                rows.append((len(rows), step, len(runs), len(bad), len(interior)))
    return rows

if __name__ == '__main__':
    rows = run(int(sys.argv[1]) if len(sys.argv) > 1 else 6_000_000)
    print(f"milestones: {len(rows)}")
    print(f"{'window':>14} {'#bad max':>9} {'#interior-bad max':>18}")
    n = len(rows)
    for a in range(0, n, max(1, n // 8)):
        w = rows[a:a + max(1, n // 8)]
        print(f"{w[0][0]:>6}..{w[-1][0]:<6} {max(x[3] for x in w):>9} {max(x[4] for x in w):>18}")
    print("\n#bad histogram overall:", dict(sorted(Counter(x[3] for x in rows).items())))
    print("#INTERIOR-bad histogram:", dict(sorted(Counter(x[4] for x in rows).items())))
    print("\nIf #bad grows with the window, NO bounded mod-3 invariant of this shape exists.")
