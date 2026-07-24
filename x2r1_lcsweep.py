#!/usr/bin/env python3
"""R1 (2026-07-25): is the doubling-phase EXIT REGEN uniform in Lc?

The odd/even post-topgrind configs differ in exactly one parameter:
    left = ones(2^k-3) ++ pow01 Lc ++ (0 0 1 :: U)      Lc = 1 (even), 6 (odd)
and both take exactly exitSteps(k+1) to run the REGEN. This plants SYNTHETIC configs with
Lc = 0..8 (capturing the real g=1 post-topgrind tape and only editing the comb) and measures
the span to the tailLaw-IN landing (right = 0^13 1^1021 ..., state E).

If the span is affine/constant in Lc, the exit is Lc-parametric and ONE forall-Lc Lean theorem
covers both parities. If it is erratic, Lc=6 needs its own proof.

No machine decided. No label upgraded.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, TT as TRANS, A, E, rle, ones_left, check_anchors

assert check_anchors(verbose=False), "instrument FAILED"

PT = 596153          # g=1 post-topgrind  (= regenIn 10, onesL = 1021 = 2^10-3)
TAILTOP = 732623     # g=1 tailLaw IN
SPAN = 1 << 17

# ---- 1. capture the real post-topgrind tape ------------------------------------------------
cap = {}
def grab(step, st, pos, tape, origin):
    if step == PT:
        cap['tape'] = bytes(tape); cap['pos'] = pos; cap['st'] = st; cap['origin'] = origin
run(PT + 1, hook=grab, hook_from=PT)
tape0, pos0, st0, org0 = cap['tape'], cap['pos'], cap['st'], cap['origin']
ol = ones_left(tape0, pos0)
print(f"captured g=1 post-topgrind @{PT}: st={'ABCDEF'[st0]} pos={pos0-org0} onesL={ol}")
i0 = pos0 - 1 - ol           # first cell left of the ones block
past = ''.join(str(tape0[i0 - d]) for d in range(0, 16))
print(f"  past-ones (leftward): {past}   <- expect 0101010101010010.. = pow01 6 ++ 001")


def plant_and_run(Lc, maxsteps=400000):
    """Rewrite the comb past the ones block to pow01 Lc, then run to the tailLaw-IN landing."""
    t = bytearray(tape0)
    # the region past the ones block currently holds pow01 6 (12 cells) then 0 0 1 ...
    # leftward cell j (j=0,1,..) sits at index i0 - j.  pow01 Lc = (0 1) repeated Lc times.
    tail = [t[i0 - d] for d in range(12, 12 + 40)]      # the 0 0 1 :: U part, preserved
    new = []
    for _ in range(Lc):
        new += [0, 1]
    new += tail
    for d, v in enumerate(new):
        t[i0 - d] = v
    pos, st = pos0, st0
    for step in range(1, maxsteps + 1):
        e = TRANS[st][t[pos]]
        if e is None:
            return ('HALT', step)
        w, dm, st = e
        t[pos] = w
        pos += dm
        if pos < 1 or pos >= 2 * SPAN - 1:
            return ('OVERFLOW', step)
        if st == E and t[pos] == 0:
            r = rle(t, pos, maxruns=4)
            if len(r) >= 2 and r[0][0] == 0 and r[0][1] == 13 and r[1] == (1, 1021):
                return ('LAND', step, pos - org0, ''.join(str(t[pos - d]) for d in range(14, 0, -1)))
    return ('NONE', maxsteps)


print(f"\nreal g=1 span post-topgrind -> tail-top = {TAILTOP - PT}  (= exitSteps 10 + 20 = 136450 + 20)")
print(f"{'Lc':>3} {'result':>8} {'span':>8}  {'delta vs Lc=6':>13}  landing-left")
base = None
for Lc in range(0, 9):
    out = plant_and_run(Lc)
    if out[0] == 'LAND':
        span, p, L = out[1], out[2], out[3]
        if Lc == 6:
            base = span
        print(f"{Lc:>3} {'LAND':>8} {span:>8}  {'' if base is None else span-base:>13}  pos={p} L[..{L}]")
    else:
        print(f"{Lc:>3} {out[0]:>8} {out[1]:>8}")
print("\nLc=6 must reproduce 136470 exactly (control). A clean affine law in Lc => the exit is")
print("Lc-parametric and ONE forall-Lc Lean theorem covers both parities.")
