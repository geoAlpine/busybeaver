#!/usr/bin/env python3
"""x2lm_middle.py -- characterize the LOW-PHASE MIDDLE (M3->M4) round-trip structure.

For g=2,3,4,5,6: build(g), step to M3, then trace M3->M4 recording the pos
trajectory. Decompose into left-comb ROUND-TRIPS (excursions between successive
left turning points) and report each round-trip's step-length and rightward reach.

Crux question: is each per-U-unit round-trip a FIXED-shape tile repeated, or does
each round-trip's length GROW with position (a genuine accumulator)?
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def milestones(g, upto=5):
    sim = build(g)
    ms = [(0, snapshot(sim))]  # M1(g) at n=0
    sim.step()
    while len(ms) <= upto:
        if sim.is_milestone():
            ms.append((sim.n, snapshot(sim)))
        if not sim.step():
            break
    return sim, ms


def snapshot(sim):
    return (sim.st, sim.pos, sim.h, list(sim.L), list(sim.R))


def trace_middle(g):
    sim = build(g)
    # advance to M3 (3rd milestone => index in collected M2,M3,...)
    sim.step()
    mcount = 0
    m3n = None
    m4n = None
    while True:
        if sim.is_milestone():
            mcount += 1
            if mcount == 2:  # M3
                m3n = sim.n
                break
        if not sim.step():
            break
    # now at M3; record trajectory to M4 (next milestone)
    traj = []
    start = sim.n
    traj.append((sim.n, sim.st, sim.pos, sim.h))
    while True:
        if not sim.step():
            break
        traj.append((sim.n, sim.st, sim.pos, sim.h))
        if sim.is_milestone():
            m4n = sim.n
            break
    return m3n, m4n, traj


def roundtrips(traj):
    """Split trajectory into round-trips by left turning points (local minima
    of pos). A round-trip = from one left-min to the next left-min."""
    poss = [p for (_, _, p, _) in traj]
    # find left turning points: indices where pos is a strict local min
    # (going down then up). Include start.
    turns = [0]
    for i in range(1, len(poss) - 1):
        if poss[i] <= poss[i - 1] and poss[i] < poss[i + 1]:
            turns.append(i)
    turns.append(len(poss) - 1)
    rts = []
    for a, b in zip(turns, turns[1:]):
        seg = traj[a:b + 1]
        length = seg[-1][0] - seg[0][0]
        minp = min(p for (_, _, p, _) in seg)
        maxp = max(p for (_, _, p, _) in seg)
        rts.append((seg[0][0], length, minp, maxp, seg[0][2], seg[-1][2]))
    return rts, turns


def main():
    for g in [2, 3, 4, 5, 6]:
        m3n, m4n, traj = trace_middle(g)
        print(f"\n=== g={g}:  M3@{m3n}  M4@{m4n}  middle length = {m4n - m3n} ===")
        rts, turns = roundtrips(traj)
        print(f"  {len(rts)} round-trips (left-min to left-min):")
        for i, (startn, length, minp, maxp, sp, ep) in enumerate(rts):
            print(f"   RT{i}: start_n={startn:5d}  len={length:4d}  "
                  f"pos[{minp:3d}..{maxp:3d}] reach={maxp - minp:3d}")


if __name__ == "__main__":
    main()
