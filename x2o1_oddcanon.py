#!/usr/bin/env python3
"""O1 (METHODS M1, full-shape): is the ladder CANONICAL at ODD g?

At even g the rule is: cascadeReg k canonical for k <= g+8, the top k = g+9 NOT canonical
(the climb exhausts the comb).  Odd g has no canonical cascadeReg at the TOP (0^13 vs 0^3),
but the MID-ladder was never checked.  If mid-ladder is canonical at odd g too, then
ladderToCascade/topRung apply verbatim and the odd branch is only topEntry + the tail entry.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, cascade_at, ones_left, check_anchors
assert check_anchors(verbose=False), "INSTRUMENT CHECK FAILED"

M1 = {1: 188099, 2: 732733, 3: 2852091, 4: 11329301, 5: 44986995}

def creg(tape, pos, r):
    if len(r) >= 4 and r[0] == (0, 3) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]; k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 3: return k
    return None

def regin(tape, pos, r):
    if len(r) >= 2 and r[0] == (0, 1):
        d = cascade_at(r, 1)
        if d is not None and ones_left(tape, pos) == (1 << (d + 4)) - 3: return d + 4
    return None

for g in (3,):
    LO, HI = M1[g], M1[g+1]
    rows = []
    def hook(step, st, pos, tape, origin):
        if st != E or tape[pos] != 0: return
        r = rle(tape, pos, maxruns=48)
        k = creg(tape, pos, r)
        if k is not None and k >= 9:
            want = (1 << (k-1)) - 2
            L = [tape[pos-1-i] for i in range(min(2*want+8, pos))]
            c = 0; i = 0
            while c < want+2 and i+1 < len(L) and L[i] == 0 and L[i+1] == 1:
                c += 1; i += 2
            rows.append(('cascadeReg', k, step, c, want))
            return
        j = regin(tape, pos, r)
        if j is not None and j >= 9:
            blk = (1 << j) - 3; want = (1 << (j-1)) - 2
            N = blk + 8 + 2*want + 4
            L = [tape[pos-1-i] for i in range(min(N, pos))]
            sep = L[blk:blk+5] == [0,1,0,0,1]
            c = 0; i = blk+5
            while c < want+1 and i+1 < len(L) and L[i] == 0 and L[i+1] == 1:
                c += 1; i += 2
            rows.append(('regenIn', j, step, c if sep else -1, want))
    run(HI, hook=hook, hook_from=LO)
    print(f"\n=== g={g} (ODD): every regenIn/cascadeReg with k>=9 in [M1({g}), M1({g+1})] ===")
    print(f"  ladder should be canonical through k = g+8 = {g+8}; top = g+9 = {g+9}")
    for what, k, step, c, want in rows:
        verdict = 'CANONICAL' if c >= want else '*** NOT CANONICAL ***'
        print(f"  {what:<11} {k:<3} @{step:>10}  comb={c:<6} need={want:<6}  {verdict}")
