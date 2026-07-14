#!/usr/bin/env python3
"""x2cu_gen.py -- emit the exact on-path config at the MIDDLE-run boundaries in
Odo.toCfg form (head pos 0, arbitrary far tails M' R), so §5v can ground the
outer_tick_noCarry_run reuse cell-for-cell against build(2).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def cfg_at(n):
    sim = build(2); sim.step()
    while sim.n < n:
        assert sim.step()
    L = [sim.L[-1 - i] for i in range(len(sim.L))]
    R = [sim.R[-1 - i] for i in range(len(sim.R))]
    return sim.st, sim.pos, sim.h, L, R


def lean(bits):
    return ''.join('true :: ' if b else 'false :: ' for b in bits)


def decode(n, tag):
    st, pos, h, L, R = cfg_at(n)
    # leading ones on left
    i = 0
    while i < len(L) and L[i] == 1:
        i += 1
    print(f"# {tag} n={n}: st={st} h={h} pos={pos}")
    print(f"#   L leading ones = {i}; next 20 = {L[i:i+20]}")
    j = 0
    while j < len(R) and R[j] == 1:
        j += 1
    print(f"#   R leading ones = {j}; next 20 = {R[j:j+20]}")
    return st, h, L, R, i, j


# C4 MIDDLE run in: 6717   out: 6821
decode(6717, "C4 MIDDLE IN")
decode(6821, "C4 MIDDLE OUT")
# C5 MIDDLE run in: 7150   out: 7846
decode(7150, "C5 MIDDLE IN")
decode(7846, "C5 MIDDLE OUT")
