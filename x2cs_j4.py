#!/usr/bin/env python3
"""x2cs_j4.py -- extract the j=4 carry window [6484,7141] cell-for-cell,
in the RELATIVE frame anchored so that n=6591 (start of the embedded j=3
carry = carry_event_5to13) has head pos 0.  Emits Lean-format zipper configs
(left nearest-first, head, right nearest-first) at the chunk boundaries, and
measures the global head excursion to place the tail variables L,R.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

TARGETS = [6484, 6591, 6708, 7141]

def leanbits(bs):
    return [1 if b else 0 for b in bs]

def snap(sim):
    # Lean zipper: left = reverse(python L), right = reverse(python R)
    left = sim.L[::-1]
    right = sim.R[::-1]
    return (sim.st, sim.pos, left[:], sim.h, right[:])

def main():
    g = 2
    sim = build(g); sim.step()
    # advance to first target
    snaps = {}
    minpos = None; maxpos = None
    # anchor pos at 6591
    while sim.n < TARGETS[0]:
        assert sim.step()
    # record from 6484 onward, tracking head excursion
    minpos = maxpos = sim.pos
    if sim.n in TARGETS:
        snaps[sim.n] = snap(sim)
    while sim.n < TARGETS[-1]:
        assert sim.step()
        minpos = min(minpos, sim.pos)
        maxpos = max(maxpos, sim.pos)
        if sim.n in TARGETS:
            snaps[sim.n] = snap(sim)
    anchor = snaps[6591][1]  # abs pos at 6591
    print(f"# anchor (abs pos @6591) = {anchor}")
    print(f"# global head excursion abs [{minpos},{maxpos}] "
          f"rel [{minpos-anchor},{maxpos-anchor}]")
    for n in TARGETS:
        st, pos, left, h, right = snaps[n]
        rel = pos - anchor
        print(f"\n=== n={n}  state={st}  abs_pos={pos}  rel_pos={rel} ===")
        print(f"  left (nearest-first, {len(left)} cells):")
        print("   ", leanbits(left))
        print(f"  head = {1 if h else 0}")
        print(f"  right (nearest-first, {len(right)} cells):")
        print("   ", leanbits(right))

if __name__ == "__main__":
    main()
