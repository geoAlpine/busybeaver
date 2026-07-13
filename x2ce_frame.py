#!/usr/bin/env python3
"""x2ce_frame.py -- extract carry sub-windows in ONE common relative frame
(the carry START at pos 0), blanks defaulted to 0, with per-subwindow head
excursion so the parametric tail split is exact.  Emits Lean-syntax lists.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def sim_to(n0):
    sim = build(2); sim.step()
    while sim.n < n0: assert sim.step()
    return sim

def abs_tape(sim):
    d = {sim.pos: sim.h}
    for k in range(len(sim.L)): d[sim.pos-1-k]=sim.L[-1-k]
    for k in range(len(sim.R)): d[sim.pos+1+k]=sim.R[-1-k]
    return d

def excursion(n0,n1):
    sim=sim_to(n0); lo=hi=sim.pos
    while sim.n<n1:
        assert sim.step(); lo=min(lo,sim.pos); hi=max(hi,sim.pos)
    return lo,hi

def L(bits): return ''.join('true :: ' if b else 'false :: ' for b in bits)

def dump(n, base_pos, name):
    """emit config at abs step n, in frame where base_pos->0, over full known tape."""
    s=sim_to(n); d=abs_tape(s)
    rel = s.pos - base_pos
    lo=min(d); hi=max(d)
    left=[d.get(s.pos-1-k,0) for k in range(s.pos-lo)]   # nearest-first
    right=[d.get(s.pos+1+k,0) for k in range(hi-s.pos)]
    # trim trailing zeros on far ends (parametric)
    print(f"  {name} n={n}: st={s.st} relpos={rel} head={'true' if d[s.pos] else 'false'}")
    print(f"    L = {L(left)}(...)")
    print(f"    R = {L(right)}(...)")
    return s.st, rel, d[s.pos]

# j=3 carry
BASE=sim_to(6591).pos   # 2069
print(f"j=3 carry base_pos(6591)={BASE}")
for n,name in [(6591,'START'),(6626,'CORE_in'),(6638,'CORE_out/EXIT_in'),(6708,'EXIT_out')]:
    dump(n,BASE,name)
print("  sub-excursions (abs):")
for a,b,nm in [(6591,6626,'ENTRY'),(6626,6638,'CORE'),(6638,6708,'EXIT'),(6591,6708,'FULL')]:
    lo,hi=excursion(a,b); print(f"    {nm} [{a},{b}] excursion abs[{lo},{hi}] rel[{lo-BASE},{hi-BASE}]")
