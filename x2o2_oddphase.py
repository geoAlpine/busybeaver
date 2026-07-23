#!/usr/bin/env python3
"""O2 (METHODS M0/M4): phase decomposition of the ODD topEntry  M6(g) -> descIn(g+6).

Odd M6 right = 0 . (10)^4 . 1^9 . 00 . rUnits g . (10)^10 . 1^{2^{g+8}-13} . m1casc(g+6)(g+7)
(vs even: rUnits (g+1), then `1 0 0`, then 1^{2^{g+8}-3}).

Odd entry level is descIn(K-2) = descIn(g+6) and odd topEntry(g) = 6080*2^g + 53g + 105
(confirmed).  Minus h_low_odd's N(g) = 305+38g, the M6->entry span should be
  6080*2^g + 15g - 200.
PREDICTIONS recorded BEFORE the run (M4):
  g=3: 6080*8 + 45 - 200 = 48485      g=5: 6080*32 + 75 - 200 = 194435
Window: M6(g) = M1(g) + 305 + 38g.
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, check_anchors
assert check_anchors(verbose=False), "INSTRUMENT CHECK FAILED"

M1s = {3: 2852091, 5: 44986995}
for g in (3,):
    M6 = M1s[g] + 305 + 38*g
    span = 6080*2**g + 15*g - 200
    print(f"g={g}: M6({g}) = {M6}; PREDICTED M6->entry span = {span} (entry @ {M6+span})")
    rows = []
    def hook(step, st, pos, tape, origin):
        if st != E or tape[pos] != 0: return
        if M6 <= step <= M6 + 260:
            rows.append((step - M6, pos - origin, comb_left(tape, pos),
                         ' '.join(f"{b}^{l}" for b, l in rle(tape, pos, maxruns=8))))
    run(M6 + 261, hook=hook, hook_from=M6)
    print(f"\nE-on-0 configs, rel 0..260:")
    prev = None
    for rel, pos, comb, body in rows:
        gap = f"(+{rel-prev})" if prev is not None else ""
        prev = rel
        print(f"  rel={rel:<5}{gap:>6} pos={pos:>6} comb={comb:<4} | {body}")
