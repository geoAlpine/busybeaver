#!/usr/bin/env python3
"""x2lf_cfg.py -- extract the exact Lean Cfg (state, head-rel-pos, L, h, R) at the start and
end of the CONSTANT byte-identical transition glues (4->5 = 215 steps, 5->4 = 1089 steps) so
we can assess whether they are cleanly provable as `∀ L R` Lean transports, and confirm the
ascending-CORE-height arithmetic law maxpeak(a,b) = 2^h - 4."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def exitSteps(k): return 2**(2*k-3)+k*2**(k-1)+2**(k-2)+2
def termSteps(k): return 2**(k+1)+k+5
REGEN={k:exitSteps(k) for k in range(4,10)}
TERM ={k:termSteps(k) for k in range(3,11)}
CAP=45000
def anchors():
    sim=build(2); sim.step(); A=[]
    while sim.n<CAP:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return A
A=anchors()

def snap_at(n):
    sim=build(2); sim.step()
    while sim.n<n:
        if not sim.step(): break
    # left runs nearest-first, right bits from head
    Lb=sim.L[::-1]  # innermost (nearest head) first? sim.L top-of-stack = nearest; L[-1] nearest
    return sim

def cfg_desc(sim, ref_pos):
    # emulate Lean Cfg: state, head-pos relative to ref, and local tape window
    L=sim.L[:]   # nearest-first is L[-1]; Lean List L is nearest-first => reversed(sim.L)?
    # Lean tape.left is nearest-first list; sim.L has nearest at end (append). So Lean L = sim.L reversed.
    leanL=sim.L[::-1]
    R=sim.R[::-1]  # sim.R has nearest at end(pop); Lean R nearest-first = sim.R reversed? sim.R stored reversed so pop=nearest => nearest at end => reversed gives nearest first
    return sim.st, sim.pos-ref_pos, leanL, sim.h, R

# 4->5 window: find first, at REGEN(7) [12709..]; the 4->5 glue is [13020,13235]
for (label, s,e) in [("4->5 @k7",13020,13235), ("5->4 @k7",13453,14542)]:
    ss=snap_at(s); es=snap_at(e)
    st0,p0,L0,h0,R0=cfg_desc(ss, ss.pos)
    st1,p1,L1,h1,R1=cfg_desc(es, ss.pos)
    print(f"\n=== {label}: {s}->{e}  ({e-s} steps) ===")
    print(f"  START state={st0} head-rel=0  h={h0}")
    print(f"     L(nearest-first, top {min(40,len(L0))})={L0[:40]}")
    print(f"     R(nearest-first, top {min(40,len(R0))})={R0[:40]}")
    print(f"  END   state={st1} head-rel={p1}  h={h1}")
    print(f"     L(nearest-first, top {min(50,len(L1))})={L1[:50]}")
    print(f"     R(nearest-first, top {min(50,len(R1))})={R1[:50]}")
    print(f"     |L| {len(L0)}->{len(L1)}  |R| {len(R0)}->{len(R1)}")

# confirm maxpeak(a,b) = 2^h-4 law
print("\n=== ascending CORE height law: maxpeak = 2^h - 4 ===")
for (lbl,mp) in [("4->5",28),("5->4",60),("5->6",60),("6->4",124)]:
    h=(mp+4)
    import math
    print(f"  {lbl}: maxpeak={mp}, maxpeak+4={h}, log2={math.log2(h):.3f}  (power of two => single top block)")
