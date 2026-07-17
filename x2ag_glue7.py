#!/usr/bin/env python3
"""x2ag_glue7.py -- TEST BY TRANSPORT (not by length) the two claims of the
`glueSegs 7` docstring, at REGEN(7)'s TI-genuine window [12709,15239) found by
x2ag_regen7.py:

  glueSegs 7 idx 1 = 215  =?=  braid_topgrind N=6  (topGrindSteps 4)   raw [13020,13235)
  glueSegs 7 idx 2 = 1089 =?=  descent_glue N=14 d+1=2 (descentSteps 5) raw [13453,14542)

Method (x2lt_ti.py's, i.e. the project's own TI criterion): build each Lean
statement's IN config, replay it in the simulator, take its relative
(state, head, dpos) trace, and search build(2) for THAT trace.  A `forall marker casc`
theorem cannot branch on marker/casc, so the trace is determined by (N, Lc)
alone and any concrete filler is faithful.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, Sim

W0, W1 = 12709, 15239            # REGEN(7) TI-genuine window (x2ag_regen7.py)

def pow10(j):  return [1, 0] * j
def pow01(j):  return [0, 1] * j
def ones(n):   return [1] * n
def zeros(n):  return [0] * n
def descCascade(d):
    # Lean: | 0 => ones 1 ; | (d+1) => ones (2^(d+3)-3) ++ 0::0::descCascade d
    # i.e. for argument m >= 1 the exponent is m+2 (NOT m+3).
    return ones(1) if d == 0 else ones(2**(d+2)-3) + [0, 0] + descCascade(d-1)
def braidRunSteps(r, n):
    return 0 if n == 0 else (8*r+10) + braidRunSteps(r+1, n-1)
def lowerFoldSteps(d):
    return 0 if d == 0 else (6*(2**(d+1)-2)+3) + lowerFoldSteps(d-1)

def mk(st, pos, L, h, R):
    s = Sim('0'); s.st=st; s.pos=pos; s.h=h
    s.L=list(L)[::-1]; s.R=list(R)[::-1]; s.n=0
    return s

def own_trace(st, pos, L, h, R, nsteps):
    s = mk(st, pos, L, h, R); tr=[]
    for _ in range(nsteps):
        tr.append((s.st, s.h, s.pos-pos)); s.step()
    return tr, s

# ---------- collect build(2) ----------
sim = build(2); sim.step()
hist=[]; ns=[]
while sim.n < 20000:
    hist.append((sim.st, sim.h, sim.pos)); ns.append(sim.n)
    if not sim.step(): break
N2I = {n:i for i,n in enumerate(ns)}

def match_at(tr, n):
    i = N2I.get(n)
    if i is None or i+len(tr) > len(hist): return False
    p0 = hist[i][2]
    return all(hist[i+j][0]==tr[j][0] and hist[i+j][1]==tr[j][1]
               and hist[i+j][2]-p0==tr[j][2] for j in range(len(tr)))

def find(tr, lo, hi):
    return [n for n in range(lo, hi) if match_at(tr, n)]

PAD = 400   # concrete filler for the `forall marker casc` tails

# ================= 1. braid_topgrind N=6 (topGrindSteps 4 = 215) =================
print("="*72)
N = 6
steps215 = 7 + braidRunSteps(0, N) + (4*N+4)
print("braid_topgrind N=%d : step count = 7 + %d + %d = %d   (topGrindSteps 4 = %d)"
      % (N, braidRunSteps(0,N), 4*N+4, steps215, 2**(2*4)+7-3*2**4))
for Lc in range(0, 5):
    marker = zeros(PAD); casc = zeros(PAD)
    L = pow01(Lc+N) + marker
    R = [0,0,0] + ones(2*N+1) + [0,0] + casc
    tr, s = own_trace('E', 0, L, 0, R, steps215)
    hits = find(tr, W0, W1)
    print("   Lc=%d -> TI-hits inside REGEN(7) window: %s   (offsets %s)"
          % (Lc, hits, [h-W0 for h in hits]))

# ================= 2. descent_glue N=14 d+1=2 (descentSteps 5 = 1089) ============
print("="*72)
N, d1 = 14, 2
steps1089 = (7 + braidRunSteps(0,N) + (4*N+4)) + lowerFoldSteps(d1) + 100
print("descent_glue N=%d d+1=%d : step count = %d + %d + 100 = %d   (descentSteps 5 = %d)"
      % (N, d1, 7+braidRunSteps(0,N)+(4*N+4), lowerFoldSteps(d1), steps1089,
         2**(2*5)+110-9*5))
for Lc in range(0, 5):
    marker = zeros(PAD); R_ = zeros(PAD)
    L = pow01(Lc+N) + marker
    R = [0,0,0] + ones(2*N+1) + [0,0] + descCascade(d1) + [0,0] + zeros(7) + R_
    tr, s = own_trace('E', 0, L, 0, R, steps1089)
    hits = find(tr, W0, W1)
    print("   Lc=%d -> TI-hits inside REGEN(7) window: %s   (offsets %s)"
          % (Lc, hits, [h-W0 for h in hits]))
