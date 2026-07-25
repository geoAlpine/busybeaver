#!/usr/bin/env python3
"""S3 phase decomposition of the EVEN topEntry  M6(g) -> descIn(g+7).

DERIVED from the g=2 and g=4 dumps (x2s3_topentry.py):

  topEntryEven(g) = P1(88) o T(11) o rUnitsFold(15(g+1)+3) o bigChew(6*2^{g+6})
                  = 88 + 11 + 15g + 18 + 384*2^g
                  = 384*2^g + 15g + 117            <- the closed form, reproduced exactly

  P1  : 4 cycles of 22 steps (3,2,2,2,13) chewing `ones 9` -> comb; block 9,7,5,3,1   FIXED
  T   : an 11-step transition                                                          FIXED
  rUF : (g+1) rUnits blocks, 15 steps each (6,6,3), then a final 3
  bigC: the 2^{g+8}-3 block chewed 6 steps per tile, 2^{g+6} tiles

PREDICTIONS for g=6, recorded BEFORE the run (METHODS M4):
  M6(6) = M1(6) + 267 + 38*6 = 179 590 445 + 495 = 179 590 940
  P1 ends   @ +88     = 179 591 028   (block 1^9 -> 1^1, comb 0 -> 4)
  T  ends   @ +99     = 179 591 039
  rUF ends  @ +207    = 179 591 147   (7 blocks of 1^5, i.e. g+1 = 7)
  descIn 13 @ +24 783 = 179 615 723   (independently measured earlier: MATCH expected)
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, check_anchors
assert check_anchors(verbose=False), "INSTRUMENT CHECK FAILED (METHODS M1)"

g = 6
M6 = 179590445 + 267 + 38 * g
PRED = {'P1 end': M6 + 88, 'T end': M6 + 99, 'rUF end': M6 + 207,
        'descIn 13': M6 + 384 * 2 ** g + 15 * g + 117}
LO, HI = M6, M6 + 300
rows = []
def hook(step, st, pos, tape, origin):
    if LO <= step <= HI and st == E and tape[pos] == 0:
        rows.append((step, pos - origin, comb_left(tape, pos),
                     ' '.join(f"{b}^{l}" for b, l in rle(tape, pos, maxruns=8))))
run(HI + 1, hook=hook, hook_from=LO)
print(f"g={g}  M6({g}) = {M6}   predictions: " +
      ", ".join(f"{k}@{v}" for k, v in PRED.items()))
print(f"\nE-on-0 configs in [{LO}, {HI}]:")
prev = None
for step, pos, comb, body in rows:
    gap = f"(+{step-prev})" if prev is not None else ""
    prev = step
    tag = "  <<< " + ", ".join(k for k, v in PRED.items() if v == step)
    print(f"  {step:>10} {gap:>6} rel={step-M6:<5} pos={pos:>6} comb={comb:<4} | {body}"
          + (tag if tag.strip() != "<<<" else ""))
