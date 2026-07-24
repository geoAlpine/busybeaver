#!/usr/bin/env python3
"""R1 oddPre (2026-07-25): pin the exact `cascadeReg 11` (topRung IN) in the g=3 orbit and
measure the reconciliation from the milestone-defined odd cReg11 to it.

topRung consumes `cascadeReg 11 1 p (0 0 1 :: U) (zeros 2048 ++ R)` with right side
`0^3 1^2045 0^2 descCascade 8 ...`.  We (1) confirm whether 5018196 is that exact config,
(2) find the precise step where label()=='cascadeReg 11', (3) dump its left marker so it can
be matched to Lean `pow01 1023 ++ (0 0 1 :: U_odd)`.  No machine decided. No label upgraded.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, ones_left, label, check_anchors

assert check_anchors(verbose=False), "instrument FAILED"

CREG11 = 5018196

def dump(step, st, pos, tape, origin, nleft=30):
    r = rle(tape, pos, maxruns=6)
    lab = label(tape, pos)
    left = ''.join(str(tape[pos - d]) for d in range(nleft, 0, -1))
    here = tape[pos]
    right = ''.join(str(tape[pos + d]) for d in range(1, 20))
    rl = ' '.join(f'{b}^{l}' for b, l in r[:5])
    print(f"  @{step} st={'ABCDEF'[st]} pos={pos-origin} label={lab} "
          f"onesL={ones_left(tape,pos)} combL={comb_left(tape,pos)}")
    print(f"     L[..{left}] ({here}) R[{right}]  rle: {rl}")

# 1) what is at the milestone-defined cReg11?
seen = {}
def hook(step, st, pos, tape, origin):
    lab = label(tape, pos)
    if step == CREG11:
        print(f"[milestone cReg11 @{CREG11}]")
        dump(step, st, pos, tape, origin)
    # 2) record every step whose label is cascadeReg 11 in a window around it
    if lab == 'cascadeReg 11' and step not in seen:
        seen[step] = (st, pos - origin)

run(CREG11 + 400, hook=hook, hook_from=CREG11 - 400)

print(f"\nsteps labelled 'cascadeReg 11' in [{CREG11-400},{CREG11+400}]: "
      f"{sorted(seen)[:8]}{' ...' if len(seen)>8 else ''}  (total {len(seen)})")
if seen:
    first = sorted(seen)[0]
    print(f"first cascadeReg-11 step = {first}  (rel to milestone cReg11: {first-CREG11})")
    # dump the exact topRung-IN config with its full left marker
    def hook2(step, st, pos, tape, origin):
        if step == first:
            print(f"\n[topRung IN = cascadeReg 11 @{first}]")
            dump(step, st, pos, tape, origin, nleft=40)
    run(first + 1, hook=hook2, hook_from=first)
