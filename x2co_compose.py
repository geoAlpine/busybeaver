#!/usr/bin/env python3
"""x2co_compose.py -- the doubling-phase COMPOSITION suite (reproducible).

Runs, in the certified symbolic executor (x2cc_symb + x2cc_faith), the parametric
episode lemmas that the doubling phase M6(g)->M1(g+1) is built from, and prints the
honest closure ledger.  See X2_COMPOSITION_2026-07-11.md.

  L0  within-block CHEW FOLD (uniform in r):
        (01)^(k+1) [D] 0^3 1^(2r+5) 0^2 T  ->*  (01)^(k+r+2) [D] 0^3 1^3 0^2 T
      -- PROVEN all k,r by certified loop induction, 0 gap events.
  L1  PER-BLOCK cascade step (chew-fold + C2), symbolic (r,s,k), opaque tail:
        (01)^(k+1) [D] 0^3 1^(2r+5) 0^2 1^(2s+5) 0^2 T
          ->*  (01)^(k+r+4) 0^2 1 [D] 0^3 1^(2s+3) 0^2 T
      -- PROVEN all k,r,s, 0 gap>=3.  This is the inductive STEP of the cascade fold.
  (C1,C2,low-phase: see x2cc_prove.py, 4/4 obligations.)

NOT closed here (the honest gaps -- see report): the cascade FOLD over the g+6
non-uniform (2^j-3) blocks; the big-block marked R/L sweep / entry / repack episodes
as parametric lemmas; the register-rebuild + doubling-arithmetic reconstruction of the
exact M1(g+1) template (couples the exponential accumulated comb-total ~2^K to the new
big block -- not representable in the affine executor)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, E
from x2cc_faith import T, Prover, GoalConfig


def prove(name, start, goal, maxops=20000):
    P = Prover(name, verbose=False)
    P.prove(start, GoalConfig(goal), max_ops=maxops)
    ok = len(P.results) >= 1
    safe = all(not [e for e in ev if e[1] == 'gap'
                    and not (e[2].is_const() and e[2].c < 3)]
               for _, _, ev in P.results)
    branches = [(case or '(base)',
                 [str(e[2]) for e in ev if e[1] == 'gap'],
                 [e[2] for e in ev if e[1] == 'loop'])
                for case, _, ev in P.results]
    return ok and safe, branches


def main():
    print("=== x2 doubling-phase composition: parametric episode lemmas ===\n")

    print("L0  within-block CHEW FOLD (uniform in r), all k,r:")
    kr = E.var('k', 1, 0) + E.var('r', 1, 0) + E(2)
    ok0, b0 = prove("L0",
                    Config(T("01^k+1"), 'D', T("0^3 1^2r+5 0^2 1^99 0^2")),
                    Config([('01', kr)], 'D', T("0^3 1^3 0^2 1^99 0^2")))
    for c, g, l in b0:
        print(f"     branch {c}: gaps {g} loops {l}")
    print(f"   -> {'PROVEN (0 gap>=3)' if ok0 else 'INCOMPLETE'}\n")

    print("L1  PER-BLOCK cascade step (chew-fold + C2), all k,r,s:")
    kf = E.var('k', 1, 0) + E.var('r', 1, 0) + E(4)
    ok1, b1 = prove("L1",
                    Config(T("01^k+1"), 'D', T("0^3 1^2r+5 0^2 1^2s+5 0^2 1^97 0^2")),
                    Config([('01', kf), ('0', E(2)), ('1', E(1))], 'D',
                           T("0^3 1^2s+3 0^2 1^97 0^2")))
    for c, g, l in b1:
        print(f"     branch {c}: gaps {g} loops {l}")
    print(f"   -> {'PROVEN (0 gap>=3)' if ok1 else 'INCOMPLETE'}\n")

    print("SUMMARY")
    print(f"  L0 chew-fold        : {'PROVEN' if ok0 else 'FAIL'}")
    print(f"  L1 per-block step   : {'PROVEN' if ok1 else 'FAIL'}  (= cascade-fold inductive step)")
    print("  cascade FOLD (g+6 non-uniform 2^j-3 blocks) : OPEN (not representable in affine")
    print("    fixed-length executor; needs Lean-style list induction or executor extension)")
    print("  big-block marked sweep / entry / repack     : per-g only (g=2..6), not parametric")
    print("  register-rebuild + doubling reconstruction  : OPEN (couples ~2^K comb-total to")
    print("    new big block; affine executor cannot represent 2^K)")
    print("\nNO DECISION.  See X2_COMPOSITION_2026-07-11.md for the exact gap.")


if __name__ == "__main__":
    main()
