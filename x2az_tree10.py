#!/usr/bin/env python3
"""x2az_tree10.py -- AUDIT PROBE (2026-07-17): the FALSIFICATION TEST at k=10.

x2az_gluelaw.py fitted four ∀k glue closed forms to the k<=9 segment data and predicted,
with NO free parameters left, the ENTIRE k=10 decomposition:

  exitList 10 = [4,5,6,7,8,4,5,6,7,4,5,6,4,5,4]                      (arity 15)
  glueSegs 10 = [1558, 215, 935, 3911, 16007, 65574, 215, 935, 3911,
                 16431, 215, 935, 4152, 215, 1089, 2422]
  including two transitions that occur NOWHERE at k<=9:
      7->8 (ascend)  = 4^7 - 3*2^7 + 7 = 16007
      8->4 (descend) = descentSteps 8  = 65574

This probe extracts REGEN(10) cell-for-cell from build(2) and checks them.
Same greedy largest-block cover as x2dt_tree8.py / x2az_tree9.py; anchor lookup
bisected so the deeper scan stays tractable.
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


CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 600000
KTOP = int(sys.argv[2]) if len(sys.argv) > 2 else 10

print(f"scanning build(2) for E-at-head-0 anchors up to n={CAP} ...")
sim = build(2)
sim.step()
A = []
halted = False
while sim.n < CAP:
    if sim.st == 'E' and sim.h == 0:
        A.append(sim.n)
    if not sim.step():
        halted = True
        break
print(f"  {len(A)} anchors, last n={A[-1] if A else None}, halted={halted}")

TERM = {k: termSteps(k) for k in range(3, 13)}
REGEN = {k: exitSteps(k) for k in range(4, 13)}
Aset = set(A)

def term_windows(k):
    g = TERM[k]
    return [(A[i], A[i + 1]) for i in range(len(A) - 1) if A[i + 1] - A[i] == g]

def regen_windows(k):
    return [(e - REGEN[k], e) for (s, e) in term_windows(k)]

def tree_expr(k):
    ws = regen_windows(k)
    if not ws: return None, None
    a, b = ws[0]
    RB = [(s, e, ('R', kk)) for kk in range(4, k)
          for (s, e) in regen_windows(kk) if a <= s and e <= b and e - s < b - a]
    TB = [(s, e, ('T', kk)) for kk in range(3, k + 1)
          for (s, e) in term_windows(kk) if a <= s and e <= b and e - s < b - a]
    bystart = {}
    for x in RB + TB:
        bystart.setdefault(x[0], []).append(x)
    terms = []; pos = a; glue = 0
    while pos < b:
        cands = bystart.get(pos)
        if cands:
            x = max(cands, key=lambda x: x[1] - x[0])
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


print()
allok = True
for k in range(5, KTOP + 1):
    terms, win = tree_expr(k)
    if terms is None:
        print(f"k={k}: REGEN({k}) NOT REACHED in the scanned prefix (raise CAP)")
        allok = False
        continue
    calls = [t[1] for t in terms if t[0] == 'R']
    segs = segs_of(terms)
    total = (sum(t[1] for t in terms if t[0] == 'g')
             + sum(exitSteps(c) for c in calls)
             + sum(termSteps(t[1]) for t in terms if t[0] == 'T'))
    pl, gl = exitList(k), glueSegs_law(k)
    mc, mg, ms = calls == pl, segs == gl, total == exitSteps(k)
    allok = allok and mc and mg and ms
    print(f"k={k:<3} window={str(win):<18} arity={len(calls):<3}(pred {exitArity(k):<3}) "
          f"calls_match={str(mc):<5} glue_match={str(mg):<5} sum={str(ms):<5}")
    if k >= 9 or not (mc and mg):
        print(f"     measured calls = {calls}")
        print(f"     PREDICTED calls= {pl}")
        print(f"     measured glue  = {segs}")
        print(f"     PREDICTED glue = {gl}")

print()
if allok:
    print("VERDICT: the ∀k glue law + exitList recursion PREDICT the full REGEN(k)")
    print(f"         decomposition cell-for-cell at every measured level k=5..{KTOP},")
    print("         including transitions absent from the data they were fitted to.")
else:
    print("VERDICT: MISMATCH -- the law does NOT extend. See above.")
