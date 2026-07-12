#!/usr/bin/env python3
"""x2ca_trace.py -- trace INSIDE a carry window and locate sweepEF-repack runs.

sweepEF = the E/F 2-cycle (E:0->1RF, F:1->1RE) marching RIGHT, repacking (01)^m
-> 1^{2m}.  Signature: a maximal run of steps cycling states E,F,E,F,... with pos
strictly increasing.  We find all such runs >= 4 steps in [n0,n1], report their
length (= 2m, so m pairs repacked) and where they sit, plus the residual
'connector' step-counts between runs (to test bounded vs growing).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def trace(g, n0, n1):
    sim = build(g); sim.step()
    while sim.n < n0:
        assert sim.step()
    events = []  # (n, st, pos, h)
    events.append((sim.n, sim.st, sim.pos, sim.h))
    while sim.n < n1:
        assert sim.step()
        events.append((sim.n, sim.st, sim.pos, sim.h))
    return events


def find_ef_runs(events):
    """maximal runs where states alternate in {E,F} with pos increasing."""
    runs = []
    i = 0
    n = len(events)
    while i < n - 1:
        # a sweepEF tile is E(on 0) then F then back to E; detect runs of E,F pattern
        if events[i][1] == 'E' and events[i][3] == 0:
            j = i
            cnt = 0
            while j + 1 < n and events[j][1] == 'E' and events[j][3] == 0 \
                    and events[j + 1][1] == 'F' and events[j + 1][2] == events[j][2] + 1:
                # this is a tile start; advance 2
                if j + 2 < n and events[j + 2][1] == 'E':
                    j += 2; cnt += 1
                else:
                    break
            if cnt >= 2:
                runs.append((events[i][0], events[j][0], cnt, events[i][2], events[j][2]))
                i = j
                continue
        i += 1
    return runs


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    windows = {
        'j3': (6591, 6708),
        'j4': (6484, 7141),
    }
    if len(sys.argv) >= 4:
        windows = {'custom': (int(sys.argv[2]), int(sys.argv[3]))}
    for name, (n0, n1) in windows.items():
        ev = trace(g, n0, n1)
        runs = find_ef_runs(ev)
        print(f"=== {name}: n=[{n0},{n1}] {n1-n0} steps ===")
        print(f"  sweepEF-style runs (>=2 tiles): {len(runs)}")
        for (a, b, cnt, p0, p1) in runs:
            print(f"    n=[{a},{b}] {cnt} tiles (repack m={cnt}, 2m={2*cnt} block) pos {p0}->{p1}")
        # count total steps in runs vs connectors
        in_runs = sum(b - a for (a, b, c, p0, p1) in runs)
        print(f"  steps in sweepEF runs = {in_runs}, connector steps = {(n1-n0)-in_runs}")
