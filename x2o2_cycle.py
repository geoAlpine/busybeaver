#!/usr/bin/env python3
"""O2: identify the ODD bulk's macro-cycle (period ~4000, pos advance ~170)."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
M6 = 2852091 + 305 + 38*3
LO, HI = M6 + 144, M6 + 48485
# Track configs whose right shows the big block: `1^b 0^2 1^1021 ...` with b large.
hits = []
def hook(step, st, pos, tape, origin):
    if st != E or tape[pos] != 0: return
    r = rle(tape, pos, maxruns=8)
    # look for a run of 1s with length > 300 within the first few runs
    for i,(b,l) in enumerate(r[:5]):
        if b == 1 and l > 300:
            hits.append((step - M6, pos - origin, i, l, comb_left(tape,pos), ones_left(tape,pos)))
            return
run(HI + 1, hook=hook, hook_from=LO)
print(f"configs showing a >300 block: {len(hits)}")
# report where the block VALUE changes
prev_l = None; prev_rel = None
print(f"{'rel':>8} {'d(rel)':>8} {'pos':>7} {'idx':>4} {'block':>7} {'comb':>6} {'ones_l':>7}")
for rel,pos,i,l,comb,ol in hits:
    if l != prev_l:
        d = f"{rel-prev_rel}" if prev_rel is not None else ""
        print(f"{rel:>8} {d:>8} {pos:>7} {i:>4} {l:>7} {comb:>6} {ol:>7}")
        prev_l = l; prev_rel = rel
