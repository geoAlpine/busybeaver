#!/usr/bin/env python3
"""x2dg_align.py -- align descent(5) and descent(6) step-by-step to find the
divergence point (end of common prefix) and re-convergence point (start of common
suffix), and print the exact tape (Lean Cfg register runs) at those points.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

DESC = {5: (13453, 14542), 6: (33830, 37982)}

def runs(bits):
    out = []; i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b: j += 1
        out.append((b, j - i)); i = j
    return out

def sim_at(n):
    sim = build(2); sim.step()
    while sim.n < n:
        if not sim.step(): break
    return sim

def full_trace(s, e):
    sim = build(2); sim.step()
    while sim.n < s:
        if not sim.step(): break
    # record (st,h) and a snapshot fn (relative offset)
    tr = []; snaps = []
    p0 = sim.pos
    while sim.n < e:
        tr.append((sim.st, sim.h, sim.pos - p0))
        snaps.append((sim.st, sim.pos - p0, runs(sim.L[::-1])[:6], sim.h, runs([sim.h]+sim.R[::-1])[:12]))
        if not sim.step(): break
    return tr, snaps

t5, s5 = full_trace(*DESC[5])
t6, s6 = full_trace(*DESC[6])
print(f"len5={len(t5)} len6={len(t6)}")

# divergence: first i where (st,h) differ
div = 0
for i in range(min(len(t5), len(t6))):
    if t5[i][:2] == t6[i][:2]: div = i+1
    else: break
print(f"\ncommon PREFIX (st,h) = {div}")
print(f"  at prefix-end, descent5 step {div}:")
st, dp, L, h, R = s5[div]
print(f"    d5: st={st} dpos={dp} L={L} h={h} R={R}")
st, dp, L, h, R = s6[div]
print(f"    d6: st={st} dpos={dp} L={L} h={h} R={R}")
# a couple steps before divergence
print(f"  step {div-1}: d5 rel={t5[div-1]}  d6 rel={t6[div-1]}")
print(f"  step {div}:   d5 rel={t5[div]}  d6 rel={t6[div]}")

# suffix
suf = 0
for i in range(1, min(len(t5), len(t6))+1):
    if t5[-i][:2] == t6[-i][:2]: suf = i
    else: break
print(f"\ncommon SUFFIX (st,h) = {suf}")
print(f"  suffix start in d5 at step {len(t5)-suf}:")
st, dp, L, h, R = s5[len(t5)-suf]
print(f"    d5: st={st} dpos={dp} L={L} h={h} R={R}")
st, dp, L, h, R = s6[len(t6)-suf]
print(f"    d6: st={st} dpos={dp} L={L} h={h} R={R}")

# What does d6 do in the middle? print snapshots of d6 at prefix-end .. suffix-start every ~ block
print(f"\n=== d6 MIDDLE snapshots (step, st, dpos, L6, h, R12) from {div} to {len(t6)-suf} ===")
mid_start = div; mid_end = len(t6)-suf
for i in range(mid_start, mid_end+1, max(1,(mid_end-mid_start)//12)):
    st, dp, L, h, R = s6[i]
    print(f"  step {i:5d}: st={st} dpos={dp:4d} h={h} L={L} R={R}")
