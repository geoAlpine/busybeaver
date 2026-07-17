#!/usr/bin/env python3
"""Exact bit-for-bit check of the Lean braidCfg shape at RT0/RT13/RT14."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def pow10(k): return [1,0]*k
def ones(k):  return [1]*k

def check(sim, r, Lc, blk, label):
    """Lean: <E, p, <pow10 Lc ++ marker, false, pow10(2r+1) ++ ones blk ++ 0::0::casc>>"""
    ok = (sim.st=='E' and sim.h==0)
    right = sim.R[::-1]          # nearest-first, after head
    left  = sim.L[::-1]          # nearest-first
    pref  = pow10(2*r+1) + ones(blk) + [0,0]
    ok_r  = right[:len(pref)] == pref
    ok_l  = left[:2*Lc] == pow10(Lc)
    # marker must NOT start with another (1,0) pair -> Lc is maximal/unambiguous
    rest_l = left[2*Lc:2*Lc+2]
    lmax   = rest_l != [1,0]
    print(f"{label}: step={sim.n} st={sim.st} h={sim.h} | E-on-0={ok} right-prefix={ok_r} left-comb={ok_l} Lc-maximal={lmax}")
    print(f"    claim braidCfg r={r} Lc={Lc} blk={blk}")
    print(f"    marker head (after (10)^{Lc}): {left[2*Lc:2*Lc+6]}")
    print(f"    casc   head (after 0,0):       {right[len(pref):len(pref)+6]}")
    return ok and ok_r and ok_l and lmax

sim = build(2); sim.step()
res = {}
for step, (r, Lc, blk), lab in [(13460,(0,15,29),'RT0 '), (14214,(13,2,3),'RT13'), (14328,(14,1,1),'RT14')]:
    while sim.n < step: sim.step()
    res[lab] = check(sim, r, Lc, blk, lab)
    print()

print("ALL EXACT:", all(res.values()), res)
print()
print("STEP ACCOUNTING (measured):")
print(f"  entry 13453->13460 = {13460-13453}")
print(f"  core  13460->14328 = {14328-13460}   vs braidRunSteps 0 14 = {4*14*14+6*14}")
print(f"  exit  14328->14388 = {14388-14328}   vs 2^(a+1)+3-7 = {2**6+3-7}")
print(f"  total = {(13460-13453)+(14328-13460)+(14388-14328)}  vs topGrindSteps 5 = {2**10+7-3*2**5}")
print(f"  braid_core_grounds: 868+(2^6+3) = {868+2**6+3}")
print()
print(f"  [RT13 alt] core 13460->14214 = {14214-13460}  vs braidRunSteps 0 13 = {4*13*13+6*13}")
