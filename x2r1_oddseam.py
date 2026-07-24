#!/usr/bin/env python3
"""R1 (2026-07-24): pin the ODD top->tail seam as an explicit fixed episode for M3'.

Goal: extract the EXACT config (cell-level, both sides, relative to head) at
  (a) the odd topRung OUT  = cReg11 + topGrindSteps 11 + exitSteps 12  (even-analogy landing)
  (b) the tailLaw IN       = where the milestone frame odometer begins
and the full head-position trace between them, so the seam can be tiled by chunked-rfl.

Compare cell-for-cell against even seam74's IN/OUT (T7TopRung.lean:412) to isolate exactly the
odd-specific prefix difference (odd U = 0 1 0 1 0 0 . frameL 1 X  vs  even 0 0 1 0 1 0 1 0 0 . X).

No machine decided. No label upgraded.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, check_anchors

assert check_anchors(verbose=False), "instrument FAILED"

# g=3 (odd) anchors from R1_ODDSEAM_2026-07-24.md, cross-checked below.
cReg11 = 5018196
topGrind11 = 4188167
exit12 = 2122754
OUT = cReg11 + topGrind11 + exit12          # even-analogy odd topRung OUT
TAILTOP = 11329137                           # milestone tail-top (0^13 1^4093 ...)
print(f"cReg11={cReg11}  topGrind11={topGrind11}  exit12={exit12}")
print(f"even-analogy topRung OUT = {OUT}   tail-top = {TAILTOP}   gap = {TAILTOP-OUT}")


def window(tape, pos, origin, L=24, R=60):
    """Explicit cell list [pos-L .. pos+R], and the head offset within it."""
    cells = [tape[pos + d] for d in range(-L, R + 1)]
    return cells, L  # head at index L


def show(step, st, pos, tape, origin):
    r = rle(tape, pos, maxruns=6)
    left = ''.join(str(tape[pos - d]) for d in range(12, 0, -1))   # 12 cells left of head
    here = tape[pos]
    right = ''.join(str(tape[pos + d]) for d in range(1, 25))       # 24 cells right of head
    rl = ' '.join(f'{b}^{l}' for b, l in r[:5])
    print(f"  @{step} st={'ABCDEF'[st]} pos={pos-origin:>6} "
          f"onesL={ones_left(tape,pos)} combL={comb_left(tape,pos)}")
    print(f"     L[{left}] ({here}) R[{right}]")
    print(f"     rle: {rl}")


CHECK = {OUT: "topRung OUT (even-analogy)", TAILTOP: "tail-top"}
# also sample a few points around the seam to see the head sweep
for s in range(OUT - 4, OUT + 1):
    CHECK.setdefault(s, "pre-OUT")
for s in range(TAILTOP - 32, TAILTOP + 1):
    CHECK.setdefault(s, "approach")

trace = []
def hook(step, st, pos, tape, origin):
    if step in CHECK:
        print(f"\n[{CHECK[step]}]")
        show(step, st, pos, tape, origin)
    if OUT - 2 <= step <= TAILTOP:
        trace.append(pos - origin)

run(TAILTOP + 2, hook=hook, hook_from=OUT - 5)

if trace:
    print(f"\nhead excursion over seam [{OUT}..{TAILTOP}]: "
          f"min={min(trace)} max={max(trace)} span={max(trace)-min(trace)} nsteps={TAILTOP-OUT}")
