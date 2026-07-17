#!/usr/bin/env python3
"""x2ag_regen7.py -- MEASURE FIRST, BY TRANSPORT (not by length).

Locate REGEN(7)'s genuine window in build(2), then locate its exitList 7 = [4,5,4]
sub-calls INSIDE it by the project's TI criterion (byte-identical relative
(state, head, dpos) trace), and MEASURE the four real glue segments.

Then test the two claims of the glueSegs 7 docstring, BY TRANSPORT:
  glueSegs 7 idx 1 = 215  ==  topGrindSteps 4   (braid_topgrind at a=4, N=6)
  glueSegs 7 idx 2 = 1089 ==  descentSteps  5   (descent_glue  at a=5, N=14, d+1=2)
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, Sim

CAP = 200_000

# ---------- collect build(2) ----------
sim = build(2); sim.step()
hist = []          # (st, h, pos) at step n = sim.n
ns = []
while sim.n < CAP:
    hist.append((sim.st, sim.h, sim.pos)); ns.append(sim.n)
    if not sim.step(): break
N2I = {n: i for i, n in enumerate(ns)}
print("collected %d steps of build(2) (n up to %d)" % (len(hist), ns[-1]))

def rel(i, L):
    """relative (st,h,dpos) trace of length L starting at index i."""
    p0 = hist[i][2]
    return tuple((hist[i+j][0], hist[i+j][1], hist[i+j][2]-p0) for j in range(L))

# ---------- REGEN(k) candidate windows: length exitSteps(k), ending at a TERM(k) anchor ----------
def exitSteps(k):  return 2**(2*k-3) + k*2**(k-1) + 2**(k-2) + 2
def termSteps(k):  return 2**(k+1) + k + 5

anchors = [ns[i] for i in range(len(hist)) if hist[i][0] == 'E' and hist[i][1] == 0]
ASET = set(anchors)
def term_windows(k):
    """TERM(k) = a gap of exactly termSteps(k) between CONSECUTIVE E-on-0 anchors
    (x2ck_regen_seg.py's criterion; NOT any two anchors that far apart)."""
    g = termSteps(k)
    return [(anchors[i], anchors[i+1]) for i in range(len(anchors)-1)
            if anchors[i+1] - anchors[i] == g]
def cand_windows(k):
    L = exitSteps(k)
    return [(e-L, e) for (s, e) in term_windows(k) if e-L >= ns[0]]

print("\nexitSteps 7 = %d, termSteps 7 = %d" % (exitSteps(7), termSteps(7)))
cw7 = cand_windows(7)
print("REGEN(7)-LENGTH candidate windows in n<%d: %d" % (CAP, len(cw7)))
for w in cw7: print("   ", w)

# ---------- TI-group them: genuine ones share a relative trace ----------
groups = {}
for (a, b) in cw7:
    if a not in N2I or b not in N2I: continue
    t = rel(N2I[a], exitSteps(7))
    groups.setdefault(hash(t), []).append((a, b))
print("\nTI trace-classes among REGEN(7)-length windows:")
for h, ws in groups.items():
    print("   class size %d : %s" % (len(ws), ws))
print("  --> a length match is NOT a transport match; classes above prove it.")

# ---------- reference sub-transport traces from the LEAN statements ----------
def mk(st, pos, L, h, R):
    s = Sim('0'); s.st = st; s.pos = pos; s.h = h
    s.L = list(L)[::-1]; s.R = list(R)[::-1]; s.n = 0
    return s

def own_trace(st, pos, L, h, R, nsteps):
    s = mk(st, pos, L, h, R)
    tr = []
    for _ in range(nsteps):
        tr.append((s.st, s.h, s.pos - pos)); s.step()
    return tr, (s.st, s.pos, s.L[::-1], s.h, s.R[::-1])

# regen4_transport (lean/X2.lean:4219): E, pos 9, 70 steps
R4_tr, R4_out = own_trace('E', 9, [1]*12 + [1,0,1,0,0,1,0], 0,
                          [0,1,0,0,0,0,0,0,0,0,0,0,0], 70)
print("\nregen4_transport replay OUT st=%s pos=%s (Lean: E, -7) -> %s"
      % (R4_out[0], R4_out[1], R4_out[0] == 'E' and R4_out[1] == -7))

# regen5_transport (lean/X2.lean:4236): E, pos 10, 218 steps
R5_tr, R5_out = own_trace('E', 10, [1]*28 + [1,0,1,0,0], 0,
                          [0,1,1,1,1,1,0,0,1,0] + [0]*15, 218)
print("regen5_transport replay OUT st=%s pos=%s (Lean: E, -22) -> %s"
      % (R5_out[0], R5_out[1], R5_out[0] == 'E' and R5_out[1] == -22))

def find_trace(tr, lo, hi):
    """all n in [lo,hi) where build(2) matches the relative trace tr."""
    L = len(tr); out = []
    for n in range(lo, min(hi, ns[-1]-L)):
        i = N2I.get(n)
        if i is None: continue
        if hist[i][0] != tr[0][0] or hist[i][1] != tr[0][1]: continue
        p0 = hist[i][2]; ok = True
        for j in range(L):
            a = hist[i+j]; b = tr[j]
            if a[0] != b[0] or a[1] != b[1] or a[2]-p0 != b[2]: ok = False; break
        if ok: out.append(n)
    return out

# ---------- pick the genuine REGEN(7): the one whose class is largest AND which
# contains TI-genuine REGEN(4)/REGEN(5) sub-calls ----------
print("\n" + "="*72)
for (a, b) in cw7:
    h4 = find_trace(R4_tr, a, b)
    h5 = find_trace(R5_tr, a, b)
    cls = [len(ws) for hh, ws in groups.items() if (a, b) in ws]
    print("window [%d,%d) class=%s : REGEN(4) TI-hits at offsets %s ; REGEN(5) TI-hits at %s"
          % (a, b, cls, [x-a for x in h4], [x-a for x in h5]))

# ---------- FINDING 2 (coordinator, 2026-07-17): canonicity by the DEFINITION, not by
# "earliest". The REGEN(k) window must carry the block 1^{2^k-3} on the tape at its IN.
print("\n" + "="*72)
print("DEFINITIONAL criterion: REGEN(7) IN must show the block 1^{2^7-3} = 1^125.")
def left_runs(i, n=3):
    """first n run tokens of the left tape (nearest-first) at index i."""
    return None
sim2 = build(2); sim2.step()
want = {a for (a, b) in cw7}
found = {}
while sim2.n <= max(b for _, b in cw7):
    if sim2.n in want:
        L = sim2.L[::-1]
        j = 0
        while j < len(L) and L[j] == 1: j += 1
        found[sim2.n] = j
    if not sim2.step(): break
for (a, b) in cw7:
    j = found[a]
    cls = [len(ws) for hh, ws in groups.items() if (a, b) in ws]
    print("   window [%d,%d) class=%s : leading 1-block at IN = 1^%d %s"
          % (a, b, cls, j, "<-- 1^125 = 2^7-3, GENUINE by definition" if j == 125 else ""))
