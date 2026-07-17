#!/usr/bin/env python3
"""x2fg_law.py -- the candidate FRAMING GLUE law, its parameter count, its DERIVATION,
and its out-of-sample test.

Data source: x2fg_frame.py, which measures lead/trailing BY TRANSPORT (never by length).

THE DISCIPLINE (ROADMAP §1.3.2 / §1.5):
  * a fit on <=3 points with >=3 free parameters is meaningless.  So: fit on k=6,7,8 ONLY
    (3 points, 3 parameters -- exactly determined, ZERO residual degrees of freedom, i.e.
    it explains nothing yet), then test at k=9,10,11 which the fit never saw.
  * `[OBSERVED]` != `[PROVEN]`.  A derivation beats any fit; §2 below finds one for
    `trailing` and reduces `lead` to a single measured constant.
"""
import json, sys

# ---- the transport-measured table (x2fg_frame.py) ----------------------------------
MEASURED = {
    6:  (154, 498),
    7:  (241, 627),
    8:  (424, 884),
    9:  (799, 1397),
    10: (1558, 2422),
    11: (3085, 4471),      # measured AFTER §5's prediction was written & committed
}
try:
    D = json.load(open('/tmp/x2fg_data.json'))
    for k, v in D.items():
        if int(k) in MEASURED:
            assert MEASURED[int(k)] == (v[0], v[1]), f"k={k}: probe disagrees with hard-coded table"
    print("[0] hard-coded table agrees with the live x2fg_frame.py run\n")
except FileNotFoundError:
    print("[0] /tmp/x2fg_data.json absent -- run x2fg_frame.py first (using hard-coded table)\n")

def exitSteps(k):  return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k):  return 2 ** (k + 1) + k + 5

# ---- [1] the fit, on k=6,7,8 ONLY --------------------------------------------------
# ansatz: f(k) = A*2^k + B*k + C   (3 free parameters).  Solve exactly on k=6,7,8.
from fractions import Fraction

def solve(pts):
    (k1, y1), (k2, y2), (k3, y3) = pts
    # Gaussian elimination over Q on [[2^k, k, 1]]
    import itertools
    M = [[Fraction(2 ** k), Fraction(k), Fraction(1), Fraction(y)] for k, y in pts]
    for c in range(3):
        p = next(r for r in range(c, 3) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(3):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return M[0][3], M[1][3], M[2][3]

FITK = [6, 7, 8]
A_l, B_l, C_l = solve([(k, MEASURED[k][0]) for k in FITK])
A_t, B_t, C_t = solve([(k, MEASURED[k][1]) for k in FITK])
print("[1] FIT on k=6,7,8 ONLY -- 3 data points, 3 free parameters (exactly determined;")
print("    at this stage the fit has ZERO explanatory content).  Ansatz A*2^k + B*k + C:\n")
print(f"    lead(k)     = {A_l}*2^k + {B_l}*k + {C_l}   =  3*2^(k-1) - 9k + 112")
print(f"    trailing(k) = {A_t}*2^k + {B_t}*k + {C_t}   =  2^(k+1) + k + 364\n")

def lead_law(k):     return 3 * 2 ** (k - 1) - 9 * k + 112
def trailing_law(k): return 2 ** (k + 1) + k + 364

assert (A_l, B_l, C_l) == (Fraction(3, 2), Fraction(-9), Fraction(112))
assert (A_t, B_t, C_t) == (Fraction(2), Fraction(1), Fraction(364))
for k in FITK:
    assert (lead_law(k), trailing_law(k)) == MEASURED[k]

# ---- [2] DERIVATION of `trailing` --------------------------------------------------
print("[2] DERIVATION of `trailing` (this one is NOT a fit)\n")
print("    The transport parse of every REGEN(k) tail, k=6..10, is the SAME fixed word:")
print("        trailing(k) = 113 + TERM(3) + 122 + TERM(3) + 76 + TERM(k)")
print("    i.e. a k-INDEPENDENT 359-step tail glue (113+24+122+24+76) followed by the")
print("    single k-dependent closing block TERM(k).  Hence")
print("        trailing(k) = 359 + termSteps(k) = 359 + 2^(k+1) + k + 5 = 2^(k+1) + k + 364.")
print("    The 2^(k+1) is termSteps(k)'s -- the closing TERM block's sweep of the 1^(2^k-3)")
print("    block.  Nothing is fitted: the '2' and the '1' and the '364' are FORCED.\n")
print("    check against the fit's coefficients (independently derived):")
print(f"      derived  A,B,C = 2, 1, 364")
print(f"      fitted   A,B,C = {A_t}, {B_t}, {C_t}   "
      f"{'IDENTICAL' if (A_t,B_t,C_t)==(2,1,364) else '*** DIFFER ***'}\n")
for k in sorted(MEASURED):
    d = 359 + termSteps(k)
    print(f"      k={k:<3} 359 + termSteps({k})={termSteps(k):<5} = {d:<6} "
          f"measured {MEASURED[k][1]:<6} {'OK' if d==MEASURED[k][1] else '*** NO ***'}")

# ---- [3] `lead` -- reduced, but a fit at its core -----------------------------------
print("\n[3] `lead` -- partially derived, ONE constant still measured\n")
print("    The transport parse of every REGEN(k) head, k=6..10, is")
print("        lead(k) = headGlue(k) + TERM(3) + 47")
print("    with the k-independent 71 = TERM(3)+47 = 24+47, and headGlue(k) measured:")
for k in sorted(MEASURED):
    print(f"      k={k:<3} headGlue = {MEASURED[k][0] - 71}")
print("\n    x2fg_geom.py §3(c) upgrades this from a fit to a WORD IDENTITY -- the NESTING LAW:")
print("        leadword(k+1) = P_(k+1) ++ leadword(k)      EXACTLY, verified k=6..11")
print("        |P_(k+1)| = 3*2^(k-1) - 9                   verified k=6..11")
print("    i.e. level k's ENTIRE lead is a literal suffix of level k+1's; each level")
print("    prepends ONE new block.  Hence the RECURSION")
print("        lead(6) = 154 ;  lead(k+1) = lead(k) + 3*2^(k-1) - 9")
print("    is structural, and 3*2^(k-1) - 9k + 112 is merely its closed-form solution.")
print("    The 3*2^(k-1) = 1.5*2^k is one-and-a-half sweeps of the 1^(2^k-3) block")
print("    (x2fg_geom.py §3(d): lead/2^k -> 1.500 monotonically).")
print("    NOT derived: the base constant lead(6) = 154, and the per-level -9.")
print("    Both are [OBSERVED] -- measured, and stable across 6 levels.\n")

# ---- [4] OUT-OF-SAMPLE ---------------------------------------------------------------
print("[4] OUT-OF-SAMPLE TEST -- the fit saw k=6,7,8 ONLY\n")
print(f"    {'k':<4} {'lead pred':>10} {'lead meas':>10}  {'trail pred':>11} {'trail meas':>11}   verdict")
ok = True
for k in (9, 10, 11):
    lp, tp = lead_law(k), trailing_law(k)
    lm, tm = MEASURED[k]
    v = "EXACT" if (lp, tp) == (lm, tm) else "*** MISS ***"
    ok = ok and (lp, tp) == (lm, tm)
    note = "  <- PREDICTED BEFORE MEASURING" if k == 11 else ""
    print(f"    {k:<4} {lp:>10} {lm:>10}  {tp:>11} {tm:>11}   {v}{note}")
print(f"\n    3 out-of-sample levels, 6 out-of-sample numbers, "
      f"{'all EXACT' if ok else 'FAILURE'}.")
print("""
    HONEST PROTOCOL NOTE -- the three levels are NOT equally strong evidence:
      k=9,10 : already measured when the ansatz A*2^k+Bk+C was chosen.  The PARAMETERS
               were fitted on k=6,7,8 alone, but the ANSATZ was picked with k=9,10
               visible, so these are weakly out-of-sample at best.  Discount them.
      k=11   : genuinely unseen.  lead(11)=3085 / trailing(11)=4471 were written into
               this file before the k=11 numbers were ever read.  (The k=11 run had been
               LAUNCHED in the background beforehand -- but its output was not read until
               after the prediction was written.  Not a git-commit-sealed prediction;
               stated here exactly as it happened, take it for what it is.)
               Both hit exactly.
    The load-bearing evidence is NOT the fit at all -- it is the WORD IDENTITY of §2 and
    §3 (x2fg_geom.py), which holds at every level and needs no extrapolation.""")
assert ok

print("\n[5] the law, in the exact form a Lean `def` + `theorem` would take\n")
print("""    def leadSteps : Nat -> Nat
      | 6       => 154
      | (k+1)   => leadSteps k + 3 * 2^(k-1) - 9      -- k >= 6
      | _       => 0

    def trailSteps (k : Nat) : Nat := 359 + termSteps k

    -- closed forms (both `decide`-checkable at any concrete k):
    theorem leadSteps_closed  (k : Nat) (h : 6 <= k) :
        leadSteps k = 3 * 2^(k-1) - 9*k + 112
    theorem trailSteps_closed (k : Nat) :
        trailSteps k = 2^(k+1) + k + 364

    -- THE FRAMING GLUE LAW the sibling's `FramingGlueLaw -> forall k, RegenLaw k` consumes:
    theorem framingGlue (k : Nat) (h : 6 <= k) :
        exitSteps k = leadSteps k + interSteps k + trailSteps k""")
print("\n    STATUS: [OBSERVED] at k=6..11 by transport.  NOT [PROVEN].")
print(f"\n    exitSteps(11) = {exitSteps(11)} (the k=11 window is 536066 steps long).")
