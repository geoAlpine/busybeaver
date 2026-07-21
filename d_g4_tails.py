#!/usr/bin/env python3
"""Consolidate tails + coverage. Probe g=3 top-rung-12 exit near predicted landing."""
import x2t7_lib
x2t7_lib.SPAN = 1 << 18
x2t7_lib.ORIGIN = x2t7_lib.SPAN
from x2t7_lib import run, rle_right, ones_run_left

def exitSteps(k): return 2**(2*k-3) + k*2**(k-1) + 2**(k-2) + 2

def show(label, step):
    _, st, pos, tape, _ = run(step)
    rle = rle_right(tape, pos, limit=40000)
    print(f"{label} step={step} state={st} head={tape[pos]} left_ones={ones_run_left(tape,pos)} rle={rle[:5]}")

# g=3 top rung 12: regenIn @9206363, predicted landing +exitSteps(12)=2122754 -> 11329117
print("### g=3 top-rung-12 exit region (predicted landing 11329117) ###")
for off in (-80, 0, 80, 160, 184):
    show(f"  +{off:>4}", 9206363 + 2122754 + off)
print("  M1(4) = 11329301")

# g=4 top rung 13: regenIn @36542824, predicted 36542824+exitSteps(13)=44986730
print("\n### g=4 top-rung-13 exit (predicted landing 44986730) ###")
show("  land ", 36542824 + exitSteps(13))
print("  M1(5) = 44986995  -> tail =", 44986995 - (36542824 + exitSteps(13)))

# coverage summary
def cov(kmax, plen):
    s = sum(exitSteps(k) for k in range(5, kmax+1))
    return s, plen, s/plen
print("\n### coverage (sum exitSteps / phase length) ###")
for g,(kmax,plen) in {2:(11,2119015),3:(12,8476791),4:(13,33657275)}.items():
    s,pl,f = cov(kmax,plen)
    print(f"  g={g}: sumExit={s} phaselen={pl} coverage={f:.4%}")
