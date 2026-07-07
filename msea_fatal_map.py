#!/usr/bin/env python3
"""
Mahler-sea survey — fatal-set PARAMETER MAP (2026-07-07).
For each machine, map which standalone family members halt, by parameter residue —
the protection-statement sketch ("the blank orbit's counters never enter residue class X
at the exposure event"). [OBSERVED maps; halts are PROVEN-by-run fatal members.]
"""
from collections import defaultdict
from msea_fatal import MACHINES, capture, run_mutant, SN_

def grid(name, want, families, budget=250_000):
    spec, mstate, side = MACHINES[name]
    cap = capture(spec, mstate, side, 20_000_000, want)
    print(f"=== {name} (state {SN_[cap['state']]}, head_rel {cap['head_rel']})")
    for label, fam in families:
        rows = defaultdict(list)
        for params, blocks, gaps in fam:
            h = run_mutant(spec, blocks, gaps, cap['head_rel'], cap['state'], side, budget)
            rows[params[0]].append('H' if h is not None else '.')
        print(f"  {label}")
        for p0 in sorted(rows):
            print(f"    {p0:>3}: {''.join(rows[p0])}")
    print()

if __name__ == "__main__":
    # o11: 1^k 0 (10)^m — rows k=2..17, cols m=1..16
    fam = [((k, m), [k] + [1] * m, [1] * m) for k in range(2, 18) for m in range(1, 17)]
    grid("o11", lambda b: len(b) >= 3 and b[0] > 1 and all(x == 1 for x in b[1:]),
         [("rows k, cols m=1..16", fam)])

    # o13: 1^a 0 1^b 0 (10)^m — rows a=2..13, cols b=1..8 (m=2 fixed)
    fam = [((a, b), [a, b] + [1] * 2, [1] * 3) for a in range(2, 14) for b in range(1, 9)]
    grid("o13", lambda b: len(b) >= 3 and b[0] > 1 and b[1] == 4 and all(x == 1 for x in b[2:]),
         [("rows a, cols b=1..8 (m=2)", fam)])

    # o12: rows a=2..13, cols b=1..8 (m=2)
    fam = [((a, b), [a, b] + [1] * 2, [1] * 3) for a in range(2, 14) for b in range(1, 9)]
    grid("o12", lambda b: len(b) >= 3 and b[0] > 1 and b[1] == 4 and all(x == 1 for x in b[2:]),
         [("rows a, cols b=1..8 (m=2)", fam)])

    # o16: rows k=1..12, cols d=2..9 (sea m=2)
    fam = [((k, d), [k] + [1] * 2 + [d], [2, 1, 1]) for k in range(1, 13) for d in range(2, 10)]
    grid("o16", lambda b: len(b) >= 3 and b[0] > 1 and b[-1] == 4 and all(x == 1 for x in b[1:-1]),
         [("rows k, cols d=2..9 (m=2)", fam)])

    # o14: rows a=2..13, cols b=1..8 (m=2, tail 4,4,2)
    fam = [((a, b), [a, 1, b] + [1] * 2 + [4, 4, 2], [1] * 7) for a in range(2, 14) for b in range(1, 9)]
    grid("o14", lambda b: len(b) >= 6 and b[1] == 1 and b[-3:] == [4, 4, 2] and b[2] > 4,
         [("rows a, cols b=1..8 (m=2)", fam)])

    print("FATAL PARAMETER MAPS [OBSERVED]. H = halts (fatal, PROVEN by run), . = no halt in budget.")
    print("No machine decided. No label upgraded.")
