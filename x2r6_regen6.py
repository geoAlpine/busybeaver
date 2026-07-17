#!/usr/bin/env python3
"""x2r6_regen6.py -- REGEN(6): the FIRST RECURSIVE level of the EXIT tree.

exitSteps 6 = 722, and `exitSteps_tree_6` says REGEN(6) makes exactly ONE recursive
call -- to REGEN(4) (= exitSteps 4 = 70), an arity-0 leaf already discharged in Lean
as `regen4_transport`/`descent_reach_4`.  So REGEN(6) is the cleanest test of whether
the k-recursion COMPOSES.

This probe, on the REAL orbit (x2bd_sim.build(2), a=5 and a=6 in ONE generation run):

  1. locates the REGEN(6) window [33830-722, 33830] = [33108, 33830] -- 33830 is the
     measured a=6 descent start recorded by §5ag/`x2rc_regen_shape.py`;
  2. measures the head EXCURSION over the window, so the far tails can be abstracted
     as Lean's `∀ L R` (a cell never visited is a legitimate parameter);
  3. emits the exact Lean IN / OUT tapes (nearest-first, maximal run parse);
  4. checks the OUT is *literally* `cascadeReg 6 1 p` for the measured p;
  5. compares the IN's SHAPE against REGEN(4)/REGEN(5)'s INs (carry_exit_j3/j4) to
     test for a k-uniform IN family -- the inductive-step question.

Run-length parses are MAXIMAL (greedy to exhaustion), technique per x2qb_exact.py.
SIMULATOR EVIDENCE -- the Lean theorems it feeds are proved independently by `rfl`.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

# The measured descent (TOPGRIND) starts = REGEN(k) exits, per §5ag / x2rc_regen_shape.py.
EXITSITE = {4: 6708, 5: 13453, 6: 33830, 7: 114703}


def exitSteps(k):
    """lean/X2.lean §5z: 2^(2k-3) + k*2^(k-1) + 2^(k-2) + 2."""
    return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2


def termSteps(k):
    return 2 ** (k + 1) + k + 5


def snap(n):
    sim = build(2)
    sim.step()
    while sim.n < n:
        assert sim.step(), f"HALT before {n}"
    return sim


def lean_view(sim):
    """(state, pos, left, head, right) in LEAN orientation (nearest-first)."""
    return (sim.st, sim.pos, sim.L[::-1], sim.h, sim.R[::-1])


def runs(bits, cap=None):
    out, i = [], 0
    while i < len(bits):
        j = i
        while j < len(bits) and bits[j] == bits[i]:
            j += 1
        out.append((bits[i], j - i))
        i = j
        if cap and len(out) >= cap:
            break
    return out


def descCascade(d):
    if d == 0:
        return [1]
    return [1] * (2 ** (d + 2) - 3) + [0, 0] + descCascade(d - 1)


def cascadeReg(k, Lc):
    """lean/X2.lean §5ah `cascadeReg k Lc p marker R`, as (left_prefix, head, right_prefix).
    left  = pow01 (Lc + 2^(k-1) - 2) ++ marker
    right = 0^3 1^(2^k-3) 0^2 descCascade (k-3) 0^2 0^7 R"""
    N = 2 ** (k - 1) - 2
    left = [0, 1] * (Lc + N)
    right = ([0, 0, 0] + [1] * (2 ** k - 3) + [0, 0] + descCascade(k - 3)
             + [0, 0] + [0] * 7)
    return left, 0, right


def excursion(n0, n1):
    """min/max ABSOLUTE head position visited over raw [n0, n1] inclusive."""
    sim = snap(n0)
    lo = hi = sim.pos
    while sim.n < n1:
        assert sim.step()
        lo = min(lo, sim.pos)
        hi = max(hi, sim.pos)
    return lo, hi


def report(k):
    e = EXITSITE[k]
    L = exitSteps(k)
    s = e - L
    print(f"\n{'='*72}\n=== REGEN({k}):  exitSteps {k} = {L}   window raw [{s}, {e}]\n{'='*72}")

    sim_in = snap(s)
    sim_out = snap(e)
    st_i, pos_i, left_i, h_i, right_i = lean_view(sim_in)
    st_o, pos_o, left_o, h_o, right_o = lean_view(sim_out)

    lo, hi = excursion(s, e)
    print(f"  IN : state={st_i} pos={pos_i} head={h_i}")
    print(f"       left  runs: {runs(left_i, 10)}")
    print(f"       right runs: {runs(right_i, 10)}")
    print(f"  OUT: state={st_o} pos={pos_o} head={h_o}")
    print(f"       left  runs: {runs(left_o, 10)}")
    print(f"       right runs: {runs(right_o, 12)}")
    print(f"  head EXCURSION over the window: abs pos [{lo}, {hi}]  (IN pos {pos_i})")
    print(f"       cells left  of IN head touched: {pos_i - lo}")
    print(f"       cells right of IN head touched: {hi - pos_i}")

    # --- the ∀ L R abstraction points, measured (a cell never visited is a parameter)
    nL = pos_i - lo          # depth into `left` actually read/written
    nR = hi - pos_i          # depth into `right` actually read/written
    print(f"  => Lean `∀ L R`: left  may be abstracted after {nL} cells "
          f"(stored {len(left_i)})")
    print(f"     Lean `∀ L R`: right may be abstracted after {nR} cells "
          f"(stored {len(right_i)})")

    # --- OUT vs cascadeReg(k, Lc=1)
    cl, ch, cr = cascadeReg(k, 1)
    okL = left_o[:len(cl)] == cl
    okR = (right_o + [0] * 200)[:len(cr)] == cr
    okH = (h_o == ch and st_o == 'E')
    print(f"  [OUT == cascadeReg({k}, Lc=1)?]  state/head:{okH}  left:{okL}  right:{okR}")
    return dict(k=k, s=s, e=e, L=L, pos_i=pos_i, pos_o=pos_o, nL=nL, nR=nR,
                left_i=left_i, right_i=right_i, left_o=left_o, right_o=right_o,
                ok=(okH and okL and okR))


def in_family_compare(D):
    """THE INDUCTIVE-STEP QUESTION: is there a k-uniform REGEN(k) IN family?"""
    print(f"\n{'='*72}\n=== IN-FAMILY CROSS-LEVEL COMPARISON (the inductive step)\n{'='*72}")
    print(f"{'k':>3} {'exitSteps':>10} {'IN left runs (first 6)':>46} {'touchL':>7} {'touchR':>7}")
    for k in sorted(D):
        d = D[k]
        print(f"{k:>3} {d['L']:>10} {str(runs(d['left_i'], 6)):>46} "
              f"{d['nL']:>7} {d['nR']:>7}")
    print("\n  candidate IN laws (leading 1-block of `left`, i.e. `ones m ++ ...`):")
    for k in sorted(D):
        r = runs(D[k]['left_i'], 1)
        m = r[0][1] if r and r[0][0] == 1 else 0
        print(f"    k={k}: leading ones = {m:>5}   2^k-4 = {2**k-4:>5}   "
              f"match={m == 2**k-4}")
    print("\n  OUT left comb (01)^m  [cascadeReg needs m = Lc + 2^(k-1)-2]:")
    for k in sorted(D):
        lo_ = D[k]['left_o']
        m = 0
        while 2 * m + 1 < len(lo_) and lo_[2*m] == 0 and lo_[2*m+1] == 1:
            m += 1
        print(f"    k={k}: m = {m:>5}   2^(k-1)-1 = {2**(k-1)-1:>5}   "
              f"=> Lc = {m - (2**(k-1)-2)}")
    print("\n  OUT anchor `pos` (relative to the IN pos) -- the `p` of cascadeReg:")
    for k in sorted(D):
        print(f"    k={k}: pos_in={D[k]['pos_i']:>6} pos_out={D[k]['pos_o']:>6} "
              f"delta={D[k]['pos_o']-D[k]['pos_i']:>6}")


def tree_check():
    print(f"\n{'='*72}\n=== exitSteps_tree_6 ARITHMETIC (lean: exitSteps_tree_6)\n{'='*72}")
    lhs = exitSteps(6)
    rhs = (83 + termSteps(3) + 47 + exitSteps(4) + 113 + termSteps(3)
           + 122 + termSteps(3) + 76 + termSteps(6))
    print(f"  exitSteps 6 = {lhs};  tree sum = {rhs};  match = {lhs == rhs}")
    print(f"  arity(6) = 1 recursive call: exitSteps 4 = {exitSteps(4)} "
          f"(an arity-0 LEAF, already discharged)")


if __name__ == "__main__":
    tree_check()
    D = {k: report(k) for k in (4, 5, 6)}
    in_family_compare(D)
    print(f"\n=== VERDICT ===")
    for k in sorted(D):
        print(f"  REGEN({k}) OUT == cascadeReg({k},1) on the real orbit: {D[k]['ok']}")
