#!/usr/bin/env python3
"""S2 (METHODS_2026-07-24, M3' steps 1-2): the 74-step seam  topRung OUT -> tailLaw IN.

topRung's OUT is `cascadeRegGen (k+1) p U R`  = <E,p, <pow01 1 ++ U, false, cascadeReg(k+1) right>>
tailLaw's IN  is <E,p, <false :: frameL j (turnWord ++ endWord ++ zeros 11 ++ L), false, zeros 4 ++ Z>>

Measured pairs:  g=2  2 851 880 -> 2 851 954      g=4  44 986 730 -> 44 986 804
Both 74 steps.  This dumps the endpoints with enough depth to read off the forall-form and
confirms the head excursion (which bounds the concrete window).
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, check_anchors
assert check_anchors(verbose=False), "INSTRUMENT CHECK FAILED (METHODS M1)"

W = {'g=2': (2851880, 2851954), 'g=4': (44986730, 44986804)}
PTS = {s for v in W.values() for s in v}
snap = {}; tr = {k: [] for k in W}

def hook(step, st, pos, tape, origin):
    if step in PTS:
        snap[step] = (st, pos - origin, bytes(tape[pos-40:pos]), tape[pos], bytes(tape[pos+1:pos+40]))
    for k, (a, b) in W.items():
        if a <= step <= b:
            tr[k].append(pos - origin)

run(max(PTS) + 1, hook=hook, hook_from=min(PTS))

for k, (a, b) in W.items():
    st0, p0, _, _, _ = snap[a]
    lo, hi = min(tr[k]), max(tr[k])
    print(f"\n=== {k}: {a} -> {b}  ({b-a} steps) ===")
    print(f"  head excursion {lo}..{hi} from start {p0}  ->  LEFT {p0-lo} cells, RIGHT {hi-p0} cells")
    for s in (a, b):
        st, pos, l, h, r = snap[s]
        L = list(l[::-1])
        print(f"  step {s}: st={'ABCDEF'[st]} pos={pos} head={h}")
        print(f"    L(head-adj first,40): {''.join(map(str,L))}")
        print(f"    R(strictly right,39): {''.join(map(str,r))}")

print("\n=== DIFF g=2 vs g=4 (the seam must be LEVEL-FREE) ===")
for a, b, tag in ((2851880, 44986730, 'IN'), (2851954, 44986804, 'OUT')):
    la, ra = snap[a][2][::-1], snap[a][4]
    lb, rb = snap[b][2][::-1], snap[b][4]
    nl = next((i for i in range(40) if la[i] != lb[i]), 40)
    nr = next((i for i in range(39) if ra[i] != rb[i]), 39)
    print(f"  {tag}: left agrees {nl}/40, right agrees {nr}/39, pos {snap[a][1]} / {snap[b][1]}")
