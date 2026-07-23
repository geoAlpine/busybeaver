#!/usr/bin/env python3
"""O2 discovery: coarse map of the ODD topEntry's unmapped bulk (g=3, rel 144..48485).

METHODS M0: measure the shape before inventing a story.  Sample E-on-0 configs and report
their RLE signature, so repeated structure (a fold) becomes visible.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
M6 = 2852091 + 305 + 38*3
LO, HI = M6 + 144, M6 + 48485
rows = []
def hook(step, st, pos, tape, origin):
    if st != E or tape[pos] != 0: return
    r = rle(tape, pos, maxruns=7)
    rows.append((step - M6, pos - origin, comb_left(tape, pos), ones_left(tape, pos),
                 ' '.join(f"{b}^{l}" for b, l in r)))
run(HI + 1, hook=hook, hook_from=LO)
print(f"E-on-0 configs in rel 144..48485: {len(rows)}")
# print a sample: first 15, then every ~1/12 of the range, then last 10
idx = list(range(min(15, len(rows)))) + \
      [i*len(rows)//12 for i in range(1, 12)] + \
      list(range(max(0, len(rows)-10), len(rows)))
seen = set()
prev = None
for i in idx:
    if i in seen or i >= len(rows): continue
    seen.add(i)
    rel, pos, comb, ol, body = rows[i]
    gap = f"(+{rel-prev})" if prev is not None else ""
    prev = rel
    print(f"  [{i:>5}] rel={rel:<7}{gap:>9} pos={pos:>6} comb={comb:<5} ones_l={ol:<5} | {body}")
