#!/usr/bin/env python3
"""x2az_gluelaw.py -- AUDIT PROBE (2026-07-17): the ∀k GLUE LAW.

x2az_tree9.py showed every glue segment of REGEN(k) is a fixed constant keyed by the
(from -> to) transition it joins, and that exitList/exitArity continue exactly at k=9.
This probe fits closed forms to the four transition families and tests whether the
resulting ∀k law reproduces exitSteps(k)'s closed form as an EXACT ARITHMETIC IDENTITY --
i.e. whether the digit-tree fold closes ∀k, or only at the measured levels.

Measured segment data (x2az_tree9.py, build(2), k=5..9):
  START->4 :  154, 241, 424, 799        (k=6,7,8,9)
  4->END   :  498, 627, 884, 1397       (k=6,7,8,9)
  a->a+1   :  215 (4->5), 935 (5->6), 3911 (6->7)
  a->4     : 1089 (5->4), 4152 (6->4), 16431 (7->4)   [= descentSteps a, §5ac/§5ag]
"""

# ---- the Lean defs, verbatim -------------------------------------------------
def exitSteps(k):    return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k):    return 2 ** (k + 1) + k + 5
def descentSteps(a): return 2 ** (2 * a) + 110 - 9 * a
def exitArity(k):    return (k - 5) * (k - 4) // 2 if k >= 5 else 0
def exitList(k):
    if k <= 5: return []
    return list(range(4, k - 1)) + exitList(k - 1)

# ---- the FITTED ∀k glue law (candidates) ------------------------------------
def g_start(k):  return 3 * 2 ** (k - 1) - 9 * k + 112      # START -> 4
def g_end(k):    return termSteps(k) + 359                   # 4 -> END  (= 2^{k+1}+k+364)
def g_asc(a):    return 4 ** a - 3 * 2 ** a + 7              # a -> a+1
def g_desc(a):   return descentSteps(a)                      # a -> 4  (a>4), §5ag-proven

MEAS_START = {6: 154, 7: 241, 8: 424, 9: 799}
MEAS_END   = {6: 498, 7: 627, 8: 884, 9: 1397}
MEAS_ASC   = {4: 215, 5: 935, 6: 3911}
MEAS_DESC  = {5: 1089, 6: 4152, 7: 16431}

print("=== (1) the four glue closed forms vs the MEASURED segments ===")
ok = True
for name, f, m in (("START->4  3*2^{k-1}-9k+112", g_start, MEAS_START),
                   ("4->END    termSteps k + 359", g_end, MEAS_END),
                   ("a->a+1    4^a - 3*2^a + 7  ", g_asc, MEAS_ASC),
                   ("a->4      descentSteps a   ", g_desc, MEAS_DESC)):
    rows = []
    for x, v in sorted(m.items()):
        good = (f(x) == v)
        ok = ok and good
        rows.append(f"{x}:{f(x)}{'==' if good else ' != '}{v}")
    print(f"  {name}  " + "  ".join(rows) + ("   OK" if all(f(x) == v for x, v in m.items()) else "   MISMATCH"))
print("  all four closed forms reproduce every measured segment:", ok)

# ---- (2) the ∀k glueSegs law -------------------------------------------------
def glueSegs_law(k):
    """The predicted glue segment list of REGEN(k): one segment per gap in
    [START] ++ exitList k ++ [END]."""
    cl = exitList(k)
    if not cl:
        return [exitSteps(k)]          # k<=5: the base, no lower REGEN, one segment
    seq = ['S'] + cl + ['E']
    segs = []
    for i in range(len(seq) - 1):
        a, b = seq[i], seq[i + 1]
        if a == 'S':   segs.append(g_start(k))
        elif b == 'E': segs.append(g_end(k))
        elif b == a + 1: segs.append(g_asc(a))
        elif b == 4:   segs.append(g_desc(a))
        else: raise AssertionError(f"unexpected transition {a}->{b} in exitList {k}")
    return segs

MEAS_SEGS = {
    5: [218],
    6: [154, 498],
    7: [241, 215, 1089, 627],
    8: [424, 215, 935, 4152, 215, 1089, 884],
    9: [799, 215, 935, 3911, 16431, 215, 935, 4152, 215, 1089, 1397],
}
print()
print("=== (2) the ∀k glueSegs LAW vs the MEASURED glueSegs (x2az_tree9.py) ===")
for k in range(5, 10):
    pred = glueSegs_law(k)
    print(f"  k={k}: law == measured: {pred == MEAS_SEGS[k]}")
    if pred != MEAS_SEGS[k]:
        print(f"        law     ={pred}\n        measured={MEAS_SEGS[k]}")

# ---- (3) THE DECISIVE TEST: does the fold close ∀k, arithmetically? ---------
def foldRegenSteps(k):
    return sum(exitSteps(kk) for kk in exitList(k))

print()
print("=== (3) DOES THE DIGIT-TREE FOLD CLOSE ∀k?  ===")
print("    test:  exitSteps k  ==  sum(glueSegs_law k) + foldRegenSteps k")
print(f"{'k':>4} {'exitSteps k':>22} {'glue sum + fold':>22} {'arity':>6} {'closes':>7}")
allclose = True
for k in list(range(5, 41)):
    lhs = exitSteps(k)
    rhs = sum(glueSegs_law(k)) + foldRegenSteps(k)
    c = (lhs == rhs)
    allclose = allclose and c
    if k <= 12 or not c or k in (20, 30, 40):
        print(f"{k:>4} {lhs:>22} {rhs:>22} {exitArity(k):>6} {str(c):>7}")
print()
print("  fold closes for EVERY k in 5..40 (arity up to "
      f"{exitArity(40)}):", allclose)
print()
print("  NOTE: k=5..9 are MEASURED (cell-for-cell, x2az_tree9.py). k=10..40 is the")
print("  ARITHMETIC identity of the four closed forms -- it shows the law is not a")
print("  coincidence of the measured levels, but it is NOT orbit evidence for k>=10.")

# ---- (4) the prediction to falsify at k=10 ----------------------------------
print()
print("=== (4) FALSIFIABLE PREDICTIONS AT k=10 (outside all measured data) ===")
print(f"  exitList 10 = {exitList(10)}   (arity {exitArity(10)} = {len(exitList(10))})")
print(f"  glueSegs 10 = {glueSegs_law(10)}")
print(f"  in particular the NEW transitions:  7->8 (ascend) = {g_asc(7)},  "
      f"8->4 (descend) = {g_desc(8)}")
print(f"  REGEN(10) length = exitSteps 10 = {exitSteps(10)}")
