#!/usr/bin/env python3
"""x2ex_gen.py -- emit Lean-ready cell-exact configs for the EXIT's recurring
translation-invariant motifs, extracted at the MINIMAL excursion window so the
lemma is reusable at every occurrence (tail-parametric, forall L R).

Since the (st,h,dpos) local trace is IDENTICAL across occurrences, every visited
cell is forced identical, so the minimal-window config is the reusable transport.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def cell_at(sim, abspos):
    d = abspos - sim.pos
    if d == 0:
        return sim.h
    if d < 0:
        idx = -d - 1
        return sim.L[-1 - idx] if idx < len(sim.L) else 0
    idx = d - 1
    return sim.R[-1 - idx] if idx < len(sim.R) else 0


def bit(b):
    return "true" if b else "false"


def cons(cells, tail):
    return "".join(bit(c) + " :: " for c in cells) + tail


def run_window(n0, n1):
    """Return start/end windowed configs over the MINIMAL excursion [dmin,dmax]
    relative to the start head position."""
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    base = sim.pos
    dmin = dmax = 0
    # first pass: excursion
    s2 = build(2); s2.step()
    while s2.n < n0:
        assert s2.step()
    while s2.n < n1:
        assert s2.step()
        dmin = min(dmin, s2.pos - base)
        dmax = max(dmax, s2.pos - base)
    # start config windowed to [base+dmin, base+dmax]
    def windowed(sim):
        pos = sim.pos
        # left cells: from pos-1 down to base+dmin
        left = [cell_at(sim, k) for k in range(pos - 1, base + dmin - 1, -1)]
        right = [cell_at(sim, k) for k in range(pos + 1, base + dmax + 1)]
        return sim.st, sim.pos - base, sim.h, left, right
    st0, rel0, h0, l0, r0 = windowed(sim)
    while sim.n < n1:
        assert sim.step()
    st1, rel1, h1, l1, r1 = windowed(sim)
    return (dmin, dmax, n1 - n0,
            (st0, rel0, h0, l0, r0), (st1, rel1, h1, l1, r1))


def emit(name, n0, n1, doc):
    dmin, dmax, k, A, B = run_window(n0, n1)
    st0, rel0, h0, l0, r0 = A
    st1, rel1, h1, l1, r1 = B
    ci = f"⟨.{st0}, {rel0}, ⟨{cons(l0,'L')}, {bit(h0)}, {cons(r0,'R')}⟩⟩"
    co = f"⟨.{st1}, {rel1}, ⟨{cons(l1,'L')}, {bit(h1)}, {cons(r1,'R')}⟩⟩"
    print(f"-- {doc}")
    print(f"-- excursion rel [{dmin},{dmax}], {k} steps, window {len(l0)}L+1+{len(r0)}R")
    print(f"set_option maxRecDepth 8000 in")
    print(f"set_option maxHeartbeats 2000000 in")
    print(f"theorem {name} (L R : List Bool) :")
    print(f"    steps {k} {ci}")
    print(f"      = some {co} :=")
    print(f"  rfl\n")


if __name__ == "__main__":
    emit("exit_anchor_motif", 6638, 6667,
         "EXIT anchor motif g3 g15 g7 sweepEF2 -- translation-invariant (EXIT3/4/5)")
