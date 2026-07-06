# o15 fatal-set hunt (o3/o18-ledger style): does ANY standalone milestone vector halt?
# Milestone M(D,V): digit vector D + big block V, head state A right of the last block.
# The halt needs an F-reads-1 with right neighbour 1 DURING a generation; every milestone
# itself is safe by construction (separators present). Hunt over a broad vector grid,
# including the anomalous small-leading-digit region and digit values 1..9 in all slots.
import sys, itertools
from o15_template_scan import run_gen

def hunt(grids, label):
    halts, buds = [], []
    n = 0
    anomalies = {}
    for blocks in grids:
        status, land, steps, unsafe, mg, toks, bad0 = run_gen(blocks, record=False)
        n += 1
        if status == 'HALT':
            halts.append((tuple(blocks), steps))
            print(f"  *** HALT: {blocks} at step {steps}")
        elif status == 'BUDGET':
            buds.append(tuple(blocks))
            print(f"  budget: {blocks} steps={steps}")
        else:
            if unsafe:
                print(f"  *** UNSAFE landing: {blocks} unsafe={unsafe}")
            if bad0:
                anomalies[tuple(blocks)] = ('double0', bad0)
    print(f"[{label}] {n} configs: {len(halts)} HALT, {len(buds)} budget-out, anomalies={len(anomalies)}")
    return halts

allh = []
# 1) two-block [d, V]: d=1..9, V=30..75 (all residues, incl. anomalous d=1,2 at V==1 mod 3)
g1 = [[d, v] for d in range(1, 10) for v in range(30, 76)]
allh += hunt(g1, "two-block d=1..9 x V=30..75")

# 2) three-block [d1, d2, V]: d1,d2 in 1..6, V in {50,51,52,100}
g2 = [[a, b, v] for a in range(1, 7) for b in range(1, 7) for v in (50, 51, 52, 100)]
allh += hunt(g2, "three-block 1..6 x 1..6 x V")

# 3) deep queues: all-ones queues of length 1..8 + V; and mixed
g3 = [[1] * k + [v] for k in range(1, 9) for v in (49, 50, 51, 52, 53, 54)]
g3 += [[2] * k + [v] for k in range(1, 6) for v in (50, 51, 52)]
g3 += [[3, 1, 1, v] for v in (49, 50, 51, 52, 53, 54)]
g3 += [[1, 1, 2, 1, v] for v in (50, 51, 52)]
g3 += [[6, 6, 6, v] for v in (50, 51, 52)]
g3 += [[9, 9, v] for v in (50, 51, 52)]
allh += hunt(g3, "deep queues")

# 4) big block small (V=1..29) with and without digits — the small-V floor (o3's fatal floor analogue)
g4 = [[v] for v in range(1, 30)]
g4 += [[d, v] for d in range(1, 7) for v in range(1, 20)]
allh += hunt(g4, "small-V floor")

# 5) big block ODD phases / degenerate: single digits only (no big block distinction), pairs of small
g5 = [[a, b] for a in range(1, 12) for b in range(1, 12)]
allh += hunt(g5, "small pairs")

print("\nTOTAL halting configs found:", len(allh))
for h in allh:
    print("  ", h)
