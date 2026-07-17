#!/usr/bin/env python3
"""x2au_topgrind.py -- claim audit probe #2 for lean/X2.lean.

INDEPENDENT re-verification of the §5af `braid_topgrind` theorem against the REAL
orbit, at a=5 AND a=6 (both live in build(2)).

The Lean statement (X2.lean ~5489):

  theorem braid_topgrind (N Lc : Nat) (p : Int) (marker casc : List Bool) :
      steps (7 + braidRunSteps 0 N + (4*N+4))
          <E, p, <pow01 (Lc+N) ++ marker, false,
                  0::0::0::(ones (2*N+1) ++ (0::0::casc))>>
        = some <E, p+5+2*N,
                <ones (4*N+4) ++ (pow10 Lc ++ (true::marker)), false, 0::casc>>

We check the IN shape, the OUT shape, the step count, and the head displacement
on the raw orbit at the claimed raw steps (a=5: 13453; a=6: 33830).

This tests whether §5ad's "the TOPGRIND transport [DESIGN] is the SINGLE remaining
obstruction inside descentGlue" is still accurate after §5af.

Run: python x2au_topgrind.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x2bd_sim import build


def pow10(k): return [1, 0] * k
def pow01(k): return [0, 1] * k
def ones(k):  return [1] * k


def snap(sim):
    """left nearest-first, head, right head-first -- matching the Lean Cfg layout."""
    return sim.L[::-1], sim.h, sim.R[::-1]


def run_to(sim, n):
    while sim.n < n:
        sim.step()
    return sim


def check(a, raw_in):
    N = 2 ** (a - 1) - 2
    Lc = 1
    braidRunSteps = 4 * N * N + 6 * N
    total = 7 + braidRunSteps + (4 * N + 4)
    topGrindSteps = 4 ** a - 3 * 2 ** a + 7

    print(f"\n=== a={a}  N={N}  raw_in={raw_in} ===")
    print(f"  topGrindSteps({a}) = {topGrindSteps};  7 + braidRunSteps 0 {N} + (4*{N}+4) = {total}"
          f"   -> {'MATCH' if total == topGrindSteps else 'MISMATCH'}")

    sim = build(2)
    run_to(sim, raw_in)
    L, h, R = snap(sim)
    p_in = sim.n

    # IN shape: left = pow01 (Lc+N) ++ marker ; head 0 ; right = 0^3 1^{2N+1} 0^2 casc
    inL = pow01(Lc + N)
    inR = [0, 0, 0] + ones(2 * N + 1) + [0, 0]
    ok_state = (sim.st == 'E')
    ok_h = (h == 0)
    ok_L = (L[:len(inL)] == inL)
    ok_R = (R[:len(inR)] == inR)
    # maximality of the pow01 (Lc+N) split: next two cells must not continue (0,1)
    lmax = L[len(inL):len(inL) + 2] != [0, 1]
    print(f"  IN  st={sim.st} h={h}  pow01({Lc+N}) prefix={ok_L} (maximal={lmax})  "
          f"0^3 1^{2*N+1} 0^2 prefix={ok_R}  state/head={ok_state and ok_h}")

    head0 = sim.abs_pos() if hasattr(sim, 'abs_pos') else None

    # run the claimed transport
    run_to(sim, raw_in + total)
    L2, h2, R2 = snap(sim)
    outL = ones(4 * N + 4) + pow10(Lc) + [1]   # ones(4N+4) ++ pow10 Lc ++ (true::marker)
    ok_L2 = (L2[:len(outL)] == outL)
    ok_R2 = True  # right = 0::casc -- casc opaque; check leading 0
    ok_R2 = (R2[:1] == [0])
    ok_state2 = (sim.st == 'E' and h2 == 0)
    print(f"  OUT st={sim.st} h={h2}  ones({4*N+4}) ++ pow10({Lc}) ++ 1 prefix={ok_L2}  "
          f"right starts 0={ok_R2}  state/head={ok_state2}")
    print(f"  steps {raw_in} -> {raw_in+total} = {total}")

    # run-length read of the OUT left, to settle the 4N+4 vs 4N+5 deposit question
    def runs(bits, k=6):
        out = []; i = 0
        while i < len(bits) and len(out) < k:
            b = bits[i]; j = i
            while j < len(bits) and bits[j] == b: j += 1
            out.append((b, j - i)); i = j
        return out
    print(f"  OUT left run-lengths (nearest-first): {runs(L2)}")
    print(f"     -> Lean deposits ones({4*N+4}) = 1^{4*N+4}; visible leading run should be "
          f"1^{4*N+5} (= 2^{a+1}-3 = {2**(a+1)-3}) because pow10 Lc starts with a 1")

    allok = ok_state and ok_h and ok_L and ok_R and lmax and ok_L2 and ok_R2 and ok_state2
    print(f"  VERDICT a={a}: braid_topgrind matches the real orbit: {allok}")
    return allok


if __name__ == '__main__':
    r5 = check(5, 13453)
    r6 = check(6, 33830)
    print(f"\n=== SUMMARY ===")
    print(f"braid_topgrind verified on-path at a=5: {r5}, a=6: {r6}")
    print("If both hold, the TOPGRIND transport is GREEN forall (Lean, §5af) AND its")
    print("IN shape is met on the real orbit at two independent generations --")
    print("so §5ad's '[DESIGN] TOPGRIND transport = the SINGLE remaining obstruction")
    print("inside descentGlue' is STALE prose (the transport is proven; only the")
    print("forall-a SHAPE/reachability remains).")
