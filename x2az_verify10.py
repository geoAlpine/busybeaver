#!/usr/bin/env python3
"""x2az_verify10.py -- AUDIT PROBE (2026-07-17): is the DISPUTED k=10 window a GENUINE
REGEN(7) call, or a false positive of the step-count cover?

x2az_tree10.py found REGEN(10)'s call list is [4,5,6,7,8,7,4,5,6,7,4,5,6,4,5,4] (arity 16),
NOT the exitList/exitArity prediction [4,5,6,7,8,4,5,6,7,4,5,6,4,5,4] (arity 15): an EXTRA
REGEN(7) appears inside what the law modelled as the single 8->4 descent glue (65574).
Note 15297 + exitSteps(7) + 47747 = 65574 exactly -- the step SUM is preserved either way,
so arithmetic alone cannot decide it.

THE METHOD ISSUE THIS EXPOSES.  x2dt_tree8.py / x2ck_regen_seg.py -- the probes grounding
lean/X2.lean's exitSteps_tree_5/6/7/8, exitArity_grounds and exitList_grounds -- identify a
"REGEN(k') call" purely by STEP COUNT (a TERM(k')-length anchor gap, minus exitSteps(k')).
They never check the window is actually the REGEN(k') TRANSPORT.  So a window can be a false
positive.  This probe applies the x2ck_regen_ti.py criterion instead: a genuine REGEN(k') is
TRANSLATION-INVARIANT -- byte-identical relative (state, head, dpos) trace at every site.

If the disputed window's trace == a known-good REGEN(7) trace  -> arity 16 is REAL and
   exitList / exitArity are FALSIFIED at k=10 (4-point overfits).
If it differs -> the step-count cover produces false positives, and the k<=9 arities
   (0,1,3,6,10) that lean/X2.lean grounds are themselves not established by that method.
Either way exitArity/exitList are not established forall-k.
"""
import sys
from bisect import bisect_right
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def exitSteps(k): return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k): return 2 ** (k + 1) + k + 5

CAP = 620000
print(f"scanning build(2) up to n={CAP} ...")
sim = build(2)
sim.step()
A = []
while sim.n < CAP:
    if sim.st == 'E' and sim.h == 0:
        A.append(sim.n)
    if not sim.step():
        break
print(f"  {len(A)} anchors")

def term_windows(k):
    g = termSteps(k)
    return [(A[i], A[i + 1]) for i in range(len(A) - 1) if A[i + 1] - A[i] == g]

def regen_windows(k):
    return [(e - exitSteps(k), e) for (s, e) in term_windows(k)]

# --- all REGEN(7)-length candidate windows, in orbit order -------------------
w7 = sorted(regen_windows(7))
print(f"\nREGEN(7)-length candidate windows found (len={exitSteps(7)}): {len(w7)}")
for i, w in enumerate(w7):
    print(f"  [{i}] {w}")

# --- the disputed one lives inside REGEN(10)'s 8->4 descent ------------------
# REGEN(10) window = (401120, 537570); the extra call sits after the REGEN(8) sub-call.
R10 = (401120, 537570)
inside10 = [w for w in w7 if R10[0] <= w[0] and w[1] <= R10[1]]
print(f"\nREGEN(7)-length windows inside REGEN(10) {R10}: {len(inside10)}")
for w in inside10:
    print(f"  {w}")


def rel_trace(start, length):
    """The relative (state, head, dpos) trace of the window [start, start+length),
    exactly the x2ck_regen_ti.py translation-invariance criterion."""
    s = build(2)
    s.step()
    while s.n < start:
        if not s.step():
            raise RuntimeError("halt before window")
    p0 = s.pos
    tr = []
    while s.n < start + length:
        tr.append((s.st, s.h, s.pos - p0))
        if not s.step():
            raise RuntimeError("halt inside window")
    return tr


print("\n=== translation-invariance test (x2ck_regen_ti.py criterion) ===")
ref = None
L7 = exitSteps(7)
results = []
for w in w7:
    try:
        t = rel_trace(w[0], L7)
    except RuntimeError as e:
        print(f"  {w}: {e}")
        continue
    if ref is None:
        ref = t
        results.append((w, True))
        print(f"  {w}: REFERENCE (the standalone REGEN(7), {L7} steps)")
    else:
        same = (t == ref)
        results.append((w, same))
        tag = "IDENTICAL to reference" if same else "*** DIFFERS from reference ***"
        loc = "inside REGEN(10)" if (R10[0] <= w[0] and w[1] <= R10[1]) else ""
        print(f"  {w}: {tag}  {loc}")

print("\n=== VERDICT ===")
ok = [w for w, s in results if s]
bad = [w for w, s in results if not s]
print(f"  {len(ok)}/{len(results)} REGEN(7)-length windows are byte-identical transports.")
if bad:
    print(f"  FALSE POSITIVES (same length, different transport): {bad}")
    print("  => the step-count cover used to ground exitSteps_tree_* / exitArity_grounds /")
    print("     exitList_grounds admits false positives; those arities are not established")
    print("     by that method.")
else:
    print("  ALL REGEN(7)-length windows -- including the disputed one inside REGEN(10)'s")
    print("  8->4 descent -- are the SAME translation-invariant transport.")
    print("  => the extra call is REAL: REGEN(10) has arity 16, and")
    print("     exitArity 10 = 15 / exitList 10 are FALSIFIED (4-point overfits).")
