#!/usr/bin/env python3
"""x2dg_tile.py -- extract the descent glue a->4 cell-for-cell as a sequence of
E-anchor register snapshots, to identify the per-depth TILE structure.

Lean Cfg convention (matching x2bd_sim / lean X2.step):
  lean.left  (nearest-first) = sim.L[::-1]
  lean.head                  = sim.h
  lean.right (nearest-first) = sim.R[::-1]
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

DESC = {5: (13453, 14542), 6: (33830, 37982), 7: (114703, 131134)}

def runs(bits):
    out = []; i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b: j += 1
        out.append((b, j - i)); i = j
    return out

def lean_cfg(sim):
    return (sim.st, sim.pos, sim.L[::-1], sim.h, sim.R[::-1])

def right_reading(sim):
    # full right region from head inclusive, nearest-first
    return [sim.h] + sim.R[::-1]

def snap_at(n):
    sim = build(2); sim.step()
    while sim.n < n:
        if not sim.step(): break
    return sim

def anchors_in(s, e):
    """E-milestone anchors (E on 0, no 1 to left) strictly inside (s,e]."""
    sim = build(2); sim.step()
    out = []
    while sim.n <= e:
        if sim.n >= s and sim.st == 'E' and sim.h == 0 and (1 not in sim.L):
            out.append(sim.n)
        if sim.n >= e: break
        if not sim.step(): break
    return out

for a in (5, 6):
    s, e = DESC[a]
    print(f"\n===================== descent a={a}  [{s},{e}] len={e-s} =====================")
    sim0 = snap_at(s); sim1 = snap_at(e)
    print(f"START st={sim0.st} pos={sim0.pos} h={sim0.h}")
    print(f"   L(near-first,top12)={runs(sim0.L[::-1])[:12]}")
    print(f"   R-from-head runs   ={runs(right_reading(sim0))[:14]}")
    print(f"END   st={sim1.st} pos={sim1.pos} h={sim1.h}  dpos={sim1.pos-sim0.pos}")
    print(f"   L(near-first,top12)={runs(sim1.L[::-1])[:12]}")
    print(f"   R-from-head runs   ={runs(right_reading(sim1))[:14]}")
    A = anchors_in(s, e)
    print(f"   #E-anchors in window: {len(A)}  (first few gaps: {[A[i+1]-A[i] for i in range(min(6,len(A)-1))]})")
