#!/usr/bin/env python3
"""x2az_tree9.py -- AUDIT PROBE (2026-07-17): does the REGEN tree structure that
lean/X2.lean grounds only at k=5..8 (exitSteps_tree_5/6/7/8, exitArity_grounds,
exitList_grounds) actually CONTINUE at k=9 -- the first level BEYOND the grounded range?

Why it matters.  §5aa's `exitArity_exceeds_four` cites `exitArity 9 = 10`, and §5ab's
`exitList` is a total Nat/List recursion whose k=9 value is PREDICTED but never measured:
    exitList 9 = List.range' 4 4 ++ exitList 8 = [4,5,6,7] ++ [4,5,6,4,5,4]   (length 10)
This probe extracts REGEN(9) cell-for-cell from the faithful build(2) orbit with the SAME
greedy largest-block cover as x2dt_tree8.py and compares.

Reuses x2dt_tree8.py's method verbatim (re-derived here so the probe is self-contained).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def exitSteps(k):
    return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2


def termSteps(k):
    return 2 ** (k + 1) + k + 5


def exitArity(k):
    return (k - 5) * (k - 4) // 2 if k >= 5 else 0


def exitList(k):
    # the Lean def: exitList (k+6) = range' 4 (k+1) ++ exitList (k+5); base <=5 -> []
    if k <= 5:
        return []
    return list(range(4, k - 1)) + exitList(k - 1)


CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 200000

print(f"scanning build(2) for E-at-head-0 anchors up to n={CAP} ...")
sim = build(2)
sim.step()
A = []
while sim.n < CAP:
    if sim.st == 'E' and sim.h == 0:
        A.append(sim.n)
    if not sim.step():
        print("  !! HALT during scan")
        break
print(f"  {len(A)} anchors, last n={A[-1] if A else None}")

TERM = {k: termSteps(k) for k in range(3, 12)}
REGEN = {k: exitSteps(k) for k in range(4, 12)}


def term_windows(k):
    g = TERM[k]
    return [(A[i], A[i + 1]) for i in range(len(A) - 1) if A[i + 1] - A[i] == g]


def regen_windows(k):
    return [(e - REGEN[k], e) for (s, e) in term_windows(k)]


def tree_expr(k):
    ws = regen_windows(k)
    if not ws:
        return None, None
    a, b = ws[0]
    RB = [(s, e, ('R', kk)) for kk in range(4, k)
          for (s, e) in regen_windows(kk) if a <= s and e <= b and e - s < b - a]
    TB = [(s, e, ('T', kk)) for kk in range(3, k + 1)
          for (s, e) in term_windows(kk) if a <= s and e <= b and e - s < b - a]
    landmarks = sorted(RB + TB)
    terms = []
    pos = a
    glue = 0
    while pos < b:
        cands = [x for x in landmarks if x[0] == pos]
        if cands:
            cands.sort(key=lambda x: -(x[1] - x[0]))
            x = cands[0]
            if glue:
                terms.append(('g', glue))
                glue = 0
            terms.append(x[2])
            pos = x[1]
        else:
            na = [c for c in A if c > pos and c <= b]
            nxt = na[0] if na else b
            glue += nxt - pos
            pos = nxt
    if glue:
        terms.append(('g', glue))
    return terms, (a, b)


print()
print(f"{'k':>3} {'window':>20} {'arity':>6} {'exitArity':>10} {'call list':>28} "
      f"{'exitList k':>28} {'match':>6} {'sum ok':>7}")
allok = True
for k in range(5, 10):
    terms, win = tree_expr(k)
    if terms is None:
        print(f"{k:>3} {'NOT REACHED in orbit prefix':>20}")
        allok = False
        continue
    calls = [t[1] for t in terms if t[0] == 'R']
    glues = [t[1] for t in terms if t[0] == 'g']
    total = (sum(glues) + sum(exitSteps(c) for c in calls)
             + sum(termSteps(t[1]) for t in terms if t[0] == 'T'))
    pred = exitList(k)
    m = (calls == pred) and (len(calls) == exitArity(k))
    s = (total == exitSteps(k))
    allok = allok and m and s
    print(f"{k:>3} {str(win):>20} {len(calls):>6} {exitArity(k):>10} {str(calls):>28} "
          f"{str(pred):>28} {str(m):>6} {str(s):>7}")

print()
print("GLUE SEGMENTS (the lead/between/trailing segments, as Lean `glueSegs`):")
for k in range(5, 10):
    terms, win = tree_expr(k)
    if terms is None:
        continue
    # merge: a glue segment = the run of ('g',_) and ('T',_) terms between REGEN calls
    segs = []
    cur = 0
    for t in terms:
        if t[0] == 'R':
            segs.append(cur)
            cur = 0
        elif t[0] == 'g':
            cur += t[1]
        elif t[0] == 'T':
            cur += termSteps(t[1])
    segs.append(cur)
    print(f"  glueSegs {k} = {segs}   (n={len(segs)} = arity+1; sum={sum(segs)})")

print()
print("TRANSITION-TYPED GLUE (segment keyed by the (from -> to) REGEN levels it joins):")
trans = {}
for k in range(5, 10):
    terms, win = tree_expr(k)
    if terms is None:
        continue
    segs = []
    cur = 0
    for t in terms:
        if t[0] == 'R':
            segs.append(cur)
            cur = 0
        elif t[0] == 'g':
            cur += t[1]
        elif t[0] == 'T':
            cur += termSteps(t[1])
    segs.append(cur)
    calls = [t[1] for t in terms if t[0] == 'R']
    labels = (['START'] + [str(c) for c in calls])
    rights = ([str(c) for c in calls] + ['END'])
    for i, s in enumerate(segs):
        key = f"{labels[i]}->{rights[i]}"
        trans.setdefault(key, []).append((k, s))
for key in sorted(trans, key=lambda x: (len(x), x)):
    vals = trans[key]
    lens = sorted({v[1] for v in vals})
    const = "CONST" if len(lens) == 1 else "VARIES-BY-k"
    print(f"  {key:>10}: {const:>12}  {[(k, s) for k, s in vals]}")

print()
print("VERDICT:", "exitList/exitArity CONTINUE at k=9 (prediction confirmed)" if allok
      else "MISMATCH -- see table")
