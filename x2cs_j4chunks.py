#!/usr/bin/env python3
"""x2cs_j4chunks.py -- emit fixed-window Lean configs at the j=4 carry chunk
boundaries, in the relative frame anchored at n=6591 -> pos 0.

Fixed abs window [LO,HI] = [2046,2105] (rel [-23,+36]); cells outside are the
safe tails L (left of LO) / R (right of HI).  For each boundary snapshot we
emit the left list (nearest-first, from head-1 down to LO, padded false) and the
right list (from head+1 up to HI, padded false), ready as `bits ++ L` / `bits ++ R`.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

ANCHOR = 2069          # abs pos at n=6591 -> rel 0
LO, HI = 2046, 2105    # fixed abs window (global head excursion)

BOUNDS = [6484, 6523, 6562, 6591,        # ENTRY A (reuse j3 carry begins at 6591)
          6708,                          # j3 carry end
          6747, 6786, 6825, 6864, 6895,  # MIDDLE C (repack at 6895)
          6923,                          # repack end
          6962, 7001, 7040, 7079, 7118, 7141]  # EXIT E

def cell_at(sim, abspos):
    """value of the tape cell at absolute position abspos (0 if blank)."""
    # sim.pos is head; sim.h head bit; sim.L nearest-first-reversed; sim.R reversed
    d = abspos - sim.pos
    if d == 0:
        return sim.h
    if d < 0:
        # left: distance |d|; nearest is sim.L[-1]
        idx = -d - 1
        return sim.L[-1 - idx] if idx < len(sim.L) else 0
    else:
        idx = d - 1
        return sim.R[-1 - idx] if idx < len(sim.R) else 0

def leanlist(bits, tailvar):
    inner = " :: ".join(("true" if b else "false") for b in bits)
    if inner:
        return inner + " :: " + tailvar
    return tailvar

def emit(sim):
    n = sim.n
    rel = sim.pos - ANCHOR
    st = sim.st
    h = sim.h
    left = [cell_at(sim, sim.pos - k) for k in range(1, sim.pos - LO + 1)]   # head-1..LO
    right = [cell_at(sim, sim.pos + k) for k in range(1, HI - sim.pos + 1)]  # head+1..HI
    print(f"-- n={n} state={st} rel_pos={rel} head={1 if h else 0} "
          f"(left {len(left)} cells to LO, right {len(right)} cells to HI)")
    print(f"   LEFT:  {leanlist(left,'L')}")
    print(f"   RIGHT: {leanlist(right,'R')}")

def main():
    sim = build(2); sim.step()
    bset = set(BOUNDS)
    while sim.n < BOUNDS[-1]:
        if sim.n in bset:
            emit(sim)
            print()
        assert sim.step()
    if sim.n in bset:
        emit(sim)

if __name__ == "__main__":
    main()
