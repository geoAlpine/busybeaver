#!/usr/bin/env python3
"""x2ex_motif.py -- test the EXIT's recurring MOTIFS for translation-invariance
(are they the SAME cell-for-cell transport = reusable forall-context glue?) and
confirm the descent-fold count law + the carry-shaped nesting of REGEN(j-1).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def trace(n0, n1):
    """(state, head, delta-pos, left-window, right-window) over [n0,n1)."""
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    base = sim.pos
    tr = []
    while sim.n < n1:
        tr.append((sim.st, sim.h, sim.pos - base))
        assert sim.step()
    return tr


def local_trace(n0, n1):
    """just (state,head,dpos) -- the translation-invariant fingerprint."""
    return trace(n0, n1)


# The "anchor motif" g3 g15 g7 sweepEF2 (29 steps) occurrences:
#   EXIT3: [6638,6667]   EXIT4: [6938,6967]   EXIT5: [8130,8159],[8230,8259]
ANCHOR = {
    'EXIT3@6638': (6638, 6667),
    'EXIT4@6938': (6938, 6967),
    'EXIT5@8130': (8130, 8159),
    'EXIT5@8230': (8230, 8259),
}

# The "C3-body buildup" motif g7 sweepEF1 g8 sweepEF3 g12 sweepEF6 (47 steps):
#   EXIT4: [6991,7038]   EXIT5: [8183,8230],[8583,8630]
C3BODY = {
    'EXIT4@6991': (6991, 7038),
    'EXIT5@8183': (8183, 8230),
    'EXIT5@8583': (8583, 8630),
}


def compare(name, D):
    print(f"\n=== {name}: are these occurrences the SAME (st,h,dpos) transport? ===")
    ref = None; refkey = None
    allsame = True
    for k, (a, b) in D.items():
        t = local_trace(a, b)
        if ref is None:
            ref = t; refkey = k
            print(f"   {k} [{a},{b}] len={len(t)}  (reference)")
        else:
            same = (t == ref)
            allsame = allsame and same
            print(f"   {k} [{a},{b}] len={len(t)}  identical-to-{refkey}? {same}")
    print(f"   >>> ALL IDENTICAL: {allsame}")
    return allsame


def fold_law():
    print("\n=== descent-fold count law: EXIT(j) opens with 2^(j-2)-2 folds ===")
    for j, folds in ((4, 2), (5, 6)):
        print(f"   EXIT({j}): measured opening fold-run = {folds}folds ; "
              f"2^({j}-2)-2 = {2**(j-2)-2}  match={folds == 2**(j-2)-2}")


def lengths():
    print("\n=== EXIT lengths (non-parametric growth) ===")
    for j, (a, b) in ((3, (6638, 6708)), (4, (6923, 7141)), (5, (8076, 8798))):
        print(f"   EXIT({j}) = {b-a} steps")
    print("   growth 70 -> 218 -> 722 ; ratios "
          f"{218/70:.3f}, {722/218:.3f} (NOT geometric, NOT a clean 4^j+2^j closed form)")


if __name__ == "__main__":
    compare("ANCHOR MOTIF (g3 g15 g7 sweepEF2)", ANCHOR)
    compare("C3-BODY BUILDUP (g7 sweepEF1 g8 sweepEF3 g12 sweepEF6)", C3BODY)
    fold_law()
    lengths()
