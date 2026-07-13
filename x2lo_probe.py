#!/usr/bin/env python3
"""x2lo_probe.py -- instrument the LOW phase M1(g)->M6(g) for g=2,3,4,5.
Extract length, config shapes at M1(g) and M6(g), head excursion window,
and the sequence of milestones. Reports whether the low phase is a clean
fixed parametric transport or grows with g."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, Sim

def right_run_str(sim, k=30):
    return sim.right_runs(k)

def probe(g):
    sim = build(g)
    # snapshot M1(g)
    m1_pos = sim.pos
    m1_left_runs = sim.left_runs_top(12)
    m1_right_runs = sim.right_runs(40)
    miles = []
    minpos = maxpos = sim.pos
    sim.step()
    cap = 20_000_000
    n_at_mile = []
    while sim.n < cap:
        minpos = min(minpos, sim.pos); maxpos = max(maxpos, sim.pos)
        if sim.is_milestone():
            miles.append((sim.n, sim.pos, sim.left_runs_top(6), sim.right_runs(40)))
            if len(miles) == 6:
                break
        if not sim.step():
            print(f"  g={g}: HALT at {sim.n}"); return
    print(f"=== g={g} ===")
    print(f" M1({g}) pos={m1_pos} leftruns={m1_left_runs}")
    print(f"   M1 rightruns(40)={m1_right_runs[:20]}")
    for i,(n,pos,lr,rr) in enumerate(miles):
        label = f"M{i+2}" if i<4 else ("M6" if i==4 else f"M1({g+1})")
        print(f"  {label}: n={n} pos={pos} leftruns={lr}")
        print(f"       rightruns={rr[:16]}")
    m6 = miles[4]
    print(f" LOW PHASE M1({g})->M6({g}): length={m6[0]} steps")
    print(f"   head window relative to M1 head: [{minpos-m1_pos}, {maxpos-m1_pos}] (abs [{minpos},{maxpos}])")
    print(f"   M6 shift = {m6[1]-m1_pos}")
    return m1_pos, m1_right_runs, m6

for g in [2,3,4,5,6]:
    probe(g)
