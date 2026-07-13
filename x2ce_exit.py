#!/usr/bin/env python3
"""x2ce_exit.py -- characterize the carry EXIT (post-CORE regeneration) cell-for-cell.

The carry = ENTRY (build comb to (10)^{2^j-2}) o CORE (sweepEF repack, the m=2^j-2
culminating doubling) o EXIT (regenerate fresh 1^{2^j-3} below + re-anchor E-on-0).
CORE ends where the biggest sweepEF run ends.  We isolate the EXIT [core_end, win_end]
and decompose it: list every E-milestone-ish sub-boundary (E on 0), the sweepEF runs,
and D-sweeps, to test CLEAN-RUN-CHAIN vs RECURSIVE (nested lower carries).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def sub(g, n0, n1):
    sim = build(g); sim.step()
    while sim.n < n0: assert sim.step()
    ev = [(sim.n, sim.st, sim.pos, sim.h)]
    while sim.n < n1:
        assert sim.step(); ev.append((sim.n, sim.st, sim.pos, sim.h))
    return ev

def ef_runs(ev):
    runs=[]; i=0; n=len(ev)
    while i < n-1:
        if ev[i][1]=='E' and ev[i][3]==0:
            j=i; cnt=0
            while j+1<n and ev[j][1]=='E' and ev[j][3]==0 and ev[j+1][1]=='F' and ev[j+1][2]==ev[j][2]+1:
                if j+2<n and ev[j+2][1]=='E': j+=2; cnt+=1
                else: break
            if cnt>=1:
                runs.append((ev[i][0],ev[j][0],cnt,ev[i][2],ev[j][2])); i=j; continue
        i+=1
    return runs

def cfg_at(g, n):
    sim = build(g); sim.step()
    while sim.n < n: assert sim.step()
    return sim

def blocks_right(sim, k=14):
    return sim.right_runs(k)
def blocks_left(sim, k=10):
    return sim.left_runs_top(k)

# CORE ends: j=3 core m=6 at 6638; j=4 core m=14 at 6923.
CASES = {'j3': (6591, 6638, 6708), 'j4': (6484, 6923, 7141)}
for name,(win0,core_end,win1) in CASES.items():
    print(f"\n===== {name}: carry [{win0},{win1}]  CORE ends {core_end}  EXIT=[{core_end},{win1}] ({win1-core_end} steps) =====")
    ev = sub(2, core_end, win1)
    runs = ef_runs(ev)
    print(f"  EXIT sweepEF runs ({len(runs)}):")
    tot=0
    for (a,b,c,pa,pb) in runs:
        print(f"    n=[{a},{b}] {c} tiles (m={c}) pos {pa}->{pb}"); tot+=(b-a)
    print(f"  steps in EXIT sweepEF runs={tot}, connectors={ (win1-core_end)-tot }")
    # config at core_end and win1
    for tag,n in (('core_end',core_end),('exit_end',win1)):
        s=cfg_at(2,n)
        print(f"  cfg@{tag}(n={n}): st={s.st} pos={s.pos} h={s.h}")
        print(f"     Rruns={blocks_right(s)}")
        print(f"     Lruns={blocks_left(s)}")
