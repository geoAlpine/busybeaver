#!/usr/bin/env python3
"""x2lt_ti.py -- TI-filter: compute regen4_transport's OWN (state,head,dpos) trace by
running its Lean IN config in the simulator, then search build(2) for that trace.
This is the project's own TI criterion (x2ck_regen_ti.py), applied to the LEAN statement."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, Sim, TT

def mk(st, pos, L, h, R):
    s = Sim('0'); s.st=st; s.pos=pos; s.h=h
    s.L = list(L)[::-1]      # Sim.L: top-of-stack = nearest -> reverse of nearest-first
    s.R = list(R)[::-1]      # Sim.R stored reversed
    s.n = 0
    return s

def snapL(s):  # Lean-order
    return (s.st, s.pos, s.L[::-1], s.h, s.R[::-1])

# ---- regen4_transport, lean/X2.lean:4206 ----
IN_L  = [1]*12 + [1,0,1,0,0,1,0]
IN_R  = [0,1,0,0,0,0,0,0,0,0,0,0,0]
OUT_L = [0,1,0]
OUT_R = [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,0,0,0]

s = mk('E', 9, IN_L, 0, IN_R)
trace = []
for _ in range(70):
    trace.append((s.st, s.h, s.pos - 9))
    s.step()
st,pos,L,h,R = snapL(s)
print("regen4_transport replay OUT: st=%s pos=%s" % (st,pos))
print("   L[0:6] =", ''.join(map(str,L[:6])), " expected", ''.join(map(str,OUT_L)))
print("   head =", h)
print("   R[0:29] =", ''.join(map(str,R[:29])))
print("   expected", ''.join(map(str,OUT_R)))
ok = (st=='E' and pos==-7 and L[:3]==OUT_L and h==0 and R[:29]==OUT_R)
print("   *** regen4_transport reproduced in simulator:", ok, "***")
print("="*72)

# ---- search build(2) for this 70-step rel trace ----
CAP = 60000
sim = build(2); sim.step()
hist = []   # (st,h,pos)
ns = []
while sim.n < CAP:
    hist.append((sim.st, sim.h, sim.pos)); ns.append(sim.n)
    if not sim.step(): break
print("collected", len(hist), "steps of build(2)")

key = trace
hits=[]
for i in range(len(hist)-70):
    if hist[i][0]!='E' or hist[i][1]!=0: continue
    p0 = hist[i][2]
    good=True
    for j in range(70):
        a=hist[i+j]; b=key[j]
        if a[0]!=b[0] or a[1]!=b[1] or a[2]-p0!=b[2]:
            good=False; break
    if good: hits.append(ns[i])
print("\nREGEN(4) TI-trace occurrences in build(2) (n<%d): %d" % (CAP, len(hits)))
print("  ", hits)
N0,N1 = 33108, 33830
inside = [h for h in hits if N0 <= h < N1]
print("\n  inside REGEN(6) window [33108,33830):", inside)
for h in inside:
    print("     offset from REGEN(6) IN =", h-N0)
