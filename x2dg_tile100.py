#!/usr/bin/env python3
"""x2dg_tile100.py -- pin the descent FINAL-100 tile's EXACT cell window.

The FINAL touches only [-4, +11] (x2dg_final.py).  Dump the absolute tape cells in
[-8, +16] at IN and OUT for a=5,6,7 so the Lean tile can be stated cell-exactly, and
confirm the window content is IDENTICAL across a (=> a fixed `rfl` tile with parametric
tails, NOT a growing object).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

DESC = {5: 13453, 6: 33830, 7: 114703}


def topGrindSteps(a):
    return 2 ** (2 * a) + 7 - 3 * 2 ** a


def lowerFoldSteps(d):
    return 0 if d == 0 else (6 * (2 ** (d + 1) - 2) + 3) + lowerFoldSteps(d - 1)


def goto(sim, n):
    while sim.n < n:
        if not sim.step():
            raise SystemExit(f"HALT at {sim.n}")


def cell(sim, p0, k):
    """tape cell at absolute offset k relative to p0 (p0 = the head at RESID)."""
    d = sim.pos - p0          # current head offset
    if k == d:
        return sim.h
    if k > d:
        idx = k - d - 1
        return sim.R[len(sim.R) - 1 - idx] if idx < len(sim.R) else 0
    idx = d - k - 1
    return sim.L[len(sim.L) - 1 - idx] if idx < len(sim.L) else 0


for a in (5, 6, 7):
    resid = DESC[a] + topGrindSteps(a) + lowerFoldSteps(a - 3)
    sim = build(2)
    sim.step()
    goto(sim, resid)
    p0 = sim.pos
    win = range(-8, 17)
    IN = [cell(sim, p0, k) for k in win]
    print(f"\n=== a={a}   RESID raw {resid}   head at offset 0")
    print(f"  IN  [-8..+16] = {IN}   st={sim.st}")
    for _ in range(100):
        sim.step()
    OUT = [cell(sim, p0, k) for k in win]
    print(f"  OUT [-8..+16] = {OUT}   st={sim.st}  head offset={sim.pos-p0}")
    print(f"  IN  offsets -4..+11 = {[cell(sim,p0,k) for k in range(-4,12)]}  (post; see OUT)")
