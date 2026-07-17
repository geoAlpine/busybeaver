#!/usr/bin/env python3
"""x2az_tree_ti.py -- AUDIT PROBE (2026-07-17): the REGEN tree decomposition with every
candidate sub-call VERIFIED as a genuine translation-invariant transport, not merely
matched by step count.

WHY.  x2dt_tree8.py / x2ck_regen_seg.py -- the probes grounding lean/X2.lean's
exitSteps_tree_5/6/7/8, exitArity_grounds, exitList_grounds -- identify a "REGEN(k') call"
by STEP COUNT alone (a TERM(k')-length anchor gap, minus exitSteps(k')).  x2az_verify10.py
showed that criterion admits FALSE POSITIVES: of the 8 REGEN(7)-length windows in the first
620k steps, only 4 are the REGEN(7) transport.  One false positive lands inside REGEN(10)
and inflates its measured arity from 15 to 16.

THIS PROBE re-runs the cover, but accepts a window as REGEN(k') only if its relative
(state, head, dpos) trace is byte-identical to the standalone REGEN(k') -- the
x2ck_regen_ti.py translation-invariance criterion, which is what "is the same transport"
actually means (and is the Lean content of the `∀ L R` statements).

Compares the result against the Lean defs exitList / exitArity at k=5..10 -- i.e. two
levels beyond their grounding range (k<=8).
"""
import sys
from bisect import bisect_right
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def exitSteps(k):    return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k):    return 2 ** (k + 1) + k + 5
def descentSteps(a): return 2 ** (2 * a) + 110 - 9 * a
def exitArity(k):    return (k - 5) * (k - 4) // 2 if k >= 5 else 0
def exitList(k):
    if k <= 5: return []
    return list(range(4, k - 1)) + exitList(k - 1)

def g_start(k): return 3 * 2 ** (k - 1) - 9 * k + 112
def g_end(k):   return termSteps(k) + 359
def g_asc(a):   return 4 ** a - 3 * 2 ** a + 7
def g_desc(a):  return descentSteps(a)

def glueSegs_law(k):
    cl = exitList(k)
    if not cl: return [exitSteps(k)]
    seq = ['S'] + cl + ['E']
    segs = []
    for i in range(len(seq) - 1):
        a, b = seq[i], seq[i + 1]
        if a == 'S': segs.append(g_start(k))
        elif b == 'E': segs.append(g_end(k))
        elif b == a + 1: segs.append(g_asc(a))
        elif b == 4: segs.append(g_desc(a))
        else: raise AssertionError(f"{a}->{b}")
    return segs


CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 620000
KTOP = int(sys.argv[2]) if len(sys.argv) > 2 else 10

print(f"scanning build(2) up to n={CAP} ...")
sim = build(2); sim.step()
A = []
while sim.n < CAP:
    if sim.st == 'E' and sim.h == 0:
        A.append(sim.n)
    if not sim.step():
        break
print(f"  {len(A)} anchors\n")

def term_windows(k):
    g = termSteps(k)
    return [(A[i], A[i + 1]) for i in range(len(A) - 1) if A[i + 1] - A[i] == g]

def regen_windows_bylen(k):
    return sorted((e - exitSteps(k), e) for (s, e) in term_windows(k))

# ---- trace cache -------------------------------------------------------------
_snap = []
def _prep(cap):
    s = build(2); s.step()
    while s.n < cap:
        _snap.append((s.n, s.st, s.h, s.pos))
        if not s.step(): break
_prep(CAP)
_ns = [x[0] for x in _snap]

def rel_trace(n0, length):
    i = bisect_right(_ns, n0) - 1
    if i < 0 or _snap[i][0] != n0: return None
    j = bisect_right(_ns, n0 + length) - 1
    if j >= len(_snap) or _snap[j][0] != n0 + length - 0: pass
    p0 = _snap[i][3]
    out = []
    for t in range(i, min(i + length, len(_snap))):
        n, st, h, pos = _snap[t]
        out.append((st, h, pos - p0))
    return out if len(out) == length else None

# ---- TI-verified REGEN windows ----------------------------------------------
print("=== TI verification of every step-count-matched REGEN(k') window ===")
REF = {}
GOOD = {}
for k in range(4, KTOP):
    ws = regen_windows_bylen(k)
    if not ws:
        GOOD[k] = []
        continue
    ref = rel_trace(ws[0][0], exitSteps(k))
    REF[k] = ref
    good, bad = [], []
    for w in ws:
        t = rel_trace(w[0], exitSteps(k))
        (good if t is not None and t == ref else bad).append(w)
    GOOD[k] = good
    print(f"  REGEN({k}): {len(good):>3}/{len(ws):<3} windows are the genuine transport"
          + (f"   FALSE POSITIVES: {len(bad)}" if bad else ""))

goodset = {k: set(GOOD[k]) for k in GOOD}

def tree_expr(k):
    ws = [w for w in regen_windows_bylen(k)]
    if not ws: return None, None
    a, b = ws[0]
    RB = [(s, e, ('R', kk)) for kk in range(4, k)
          for (s, e) in GOOD[kk] if a <= s and e <= b and e - s < b - a]
    TB = [(s, e, ('T', kk)) for kk in range(3, k + 1)
          for (s, e) in term_windows(kk) if a <= s and e <= b and e - s < b - a]
    bystart = {}
    for x in RB + TB:
        bystart.setdefault(x[0], []).append(x)
    terms = []; pos = a; glue = 0
    while pos < b:
        c = bystart.get(pos)
        if c:
            x = max(c, key=lambda x: x[1] - x[0])
            if glue: terms.append(('g', glue)); glue = 0
            terms.append(x[2]); pos = x[1]
        else:
            i = bisect_right(A, pos)
            nxt = A[i] if i < len(A) and A[i] <= b else b
            glue += nxt - pos; pos = nxt
    if glue: terms.append(('g', glue))
    return terms, (a, b)

def segs_of(terms):
    segs = []; cur = 0
    for t in terms:
        if t[0] == 'R': segs.append(cur); cur = 0
        elif t[0] == 'g': cur += t[1]
        elif t[0] == 'T': cur += termSteps(t[1])
    segs.append(cur)
    return segs

print("\n=== TI-FILTERED tree decomposition vs the Lean defs ===")
allok = True
for k in range(5, KTOP + 1):
    terms, win = tree_expr(k)
    if terms is None:
        print(f"k={k}: not reached"); allok = False; continue
    calls = [t[1] for t in terms if t[0] == 'R']
    segs = segs_of(terms)
    total = (sum(t[1] for t in terms if t[0] == 'g')
             + sum(exitSteps(c) for c in calls)
             + sum(termSteps(t[1]) for t in terms if t[0] == 'T'))
    pl, gl = exitList(k), glueSegs_law(k)
    mc, mg, ms = calls == pl, segs == gl, total == exitSteps(k)
    allok = allok and mc and mg and ms
    star = "  <-- BEYOND the Lean grounding range (k<=8)" if k >= 9 else ""
    print(f"k={k:<3} arity={len(calls):<3}(exitArity {exitArity(k):<3}) calls={str(mc):<5} "
          f"glue={str(mg):<5} sum={str(ms):<5}{star}")
    if not (mc and mg):
        print(f"     measured calls={calls}\n     exitList  {k} ={pl}")
        print(f"     measured glue ={segs}\n     glue law  {k} ={gl}")

print()
print("VERDICT:", "exitList / exitArity / the ∀k glue law reproduce the TI-verified tree"
      f" cell-for-cell at k=5..{KTOP}" if allok else "MISMATCH -- see above")
