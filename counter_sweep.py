#!/usr/bin/env python
"""
PIECE 3 core — prove the SWEEP rule by nested induction (the outer doubling), soundly.

Canonical counter 1RB1LA_0LA0RB_0LA0LZ. The load-bearing OUTER rule above Inc (see counter_inc.py):

    Sweep(m):   0^(m+1) B> 0   ->   1 0^m B> 0          (set bit m: 2^m increments, in 2^(m+2)-2 steps)

VERIFIED so far (sound, by the trusted simulator): Sweep(m) reaches RHS in f(m)=2^(m+2)-2 steps with
f(m+1)=2f(m)+2 (the DOUBLING) and is HEAD-CONTAINED (leftmost head = 0, never -1).

‼ WHAT IS NOT YET DONE: the inductive STEP. A NAIVE 'apply Sweep(j) to any suffix 0^j B>' does NOT
work — verified concretely on Sweep(3)=0^4 B>: the doubling is NOT two identical Sweep(2)'s via a
clean suffix. The first half 0000->0100 IS Sweep(2) on the suffix (f(2)=14 steps), but the second
half 0100->1000 is f(2)+2 steps starting from 0100 (NOT from 0^3) — so the second IH use is on a
DIFFERENT, non-suffix configuration. Like sligocki's machine (whose rule carries an auxiliary '1 00'
suffix), our counter needs an auxiliary-structure rule, not a bare 0^j suffix. So prove_sweep below
greedily cascades the IH onto wrong suffixes and does NOT close — it is a documented WIP that NEVER
emits a trusted proof (returns WIP-CLOSED-UNTRUSTED even if it reached RHS). The exact auxiliary rule
is the next careful step.

Soundness model (all checked):
  base : simulate Sweep(base) concretely (trusted simulator), reach RHS(base), no halt, head-contained.
  step : symbolically simulate LHS(m) with the G1-VALIDATED faithful simulator + apply Sweep(j) (the
         IH) to a suffix only when j < m (well-founded, asserted); reach RHS(m), no halt. A successful
         derivation IS a proof. (Head-containment of Sweep(j), verified in the base sims, makes the
         suffix application sound.)
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from wsim import step, val, _cp
from counter_induct import compress

SPEC = "1RB1LA_0LA0RB_0LA0LZ"


def lt_m(e, base):
    """is exp e=(a,b) provably < m (the induction var) for all m>=base?"""
    a, b = e
    if a == 0:
        return b < base
    if a == 1:
        return b <= -1
    return False


def rhs_cfg(mexp):
    """RHS(m) = '1 0^m B> 0' : segs [ [1], (0,)^m, [0] ], head on the trailing [0], state B."""
    return ("B", [["c", [1]], ["r", (0,), mexp], ["c", [0]]], 2, 0)


def is_rhs(cfg, mexp):
    st, segs, hi, ho = cfg
    return (st, hi, ho) == ("B", 2, 0) and len(segs) == 3 and segs[0] == ["c", [1]] \
        and segs[1][0] == "r" and tuple(segs[1][1]) == (0,) and tuple(segs[1][2]) == tuple(mexp) \
        and segs[2] == ["c", [0]]


def try_suffix_sweep(cfg, base, mexp):
    """If a suffix '0^e B> 0' (repeater (0,)^e then head on a trailing [0], state B) is present with
    j=e-1 provably < m, apply Sweep(j): replace that suffix with '1 0^j B> 0'. Peel one 0 if e==m+1
    (the whole LHS) to expose Sweep(m-1). Returns new cfg or None."""
    st, segs, hi, ho = cfg
    if st != "B" or ho != 0 or hi != len(segs) - 1 or segs[hi] != ["c", [0]]:
        return None
    if hi < 1 or segs[hi - 1][0] != "r" or tuple(segs[hi - 1][1]) != (0,):
        return None
    e = tuple(segs[hi - 1][2]); ridx = hi - 1
    je = (e[0], e[1] - 1)                          # j = e-1
    if lt_m(je, base):
        j = je; prefix = segs[:ridx]
    elif e == (1, 1):                              # e == m+1 (the whole LHS): peel one 0 -> Sweep(m-1)
        j = (1, -1); prefix = segs[:ridx] + [["c", [0]]]
    else:
        return None
    # RHS(j) = '1 0^j B> 0'
    rhs = [["c", [1]], ["r", (0,), j], ["c", [0]]]
    new_segs = prefix + rhs
    return ("B", new_segs, len(new_segs) - 1, 0)


def prove_sweep(spec=SPEC, base=3, max_ops=400):
    M = parse(spec)
    mexp = (1, 0)                                  # m, symbolic
    # LHS(m) = '0^(m+1) B> 0' : segs [ (0,)^(m+1), [0] ], head on trailing [0]
    cfg = ("B", [["r", (0,), (1, 1)], ["c", [0]]], 1, 0)
    ihs = 0
    for _ in range(max_ops):
        if is_rhs(cfg, mexp):
            return "WIP-CLOSED-UNTRUSTED", ihs       # IH logic not validated -> never a trusted proof
        ap = try_suffix_sweep(cfg, base, mexp)
        if ap is not None:
            cfg = compress(ap); ihs += 1; continue
        cfg = compress(cfg); cfg, op = step(M, cfg)
        if op[0] == "HALT":
            return "halt-in-step", ihs
        if op[0] == "STUCK":
            return "stuck", ihs
    return "no-close", ihs


def verify_sweep_facts(spec=SPEC, ms=range(1, 10)):
    """SOUND verified facts about Sweep(m) (by the trusted simulator): reaches RHS, f(m)=2^(m+2)-2,
    f(m+1)=2f(m)+2 (doubling), head-contained (leftmost head = 0). Returns (ok, detail)."""
    M = parse(spec); fs = []
    for m in ms:
        n = m + 1; tape = {i: 0 for i in range(n)}; head = n; st = "B"; leftmost = head; steps = 0
        for _ in range(2 ** (m + 2) + 10):
            leftmost = min(leftmost, head)
            tr = M[st][tape.get(head, 0)]
            if tr is None:
                return False, f"Sweep({m}) halted"
            w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns; steps += 1
            if st == "B" and head == n and tape.get(0, 0) == 1 and all(tape.get(i, 0) == 0 for i in range(1, n)):
                break
        else:
            return False, f"Sweep({m}) no RHS"
        if leftmost < 0 or steps != 2 ** (m + 2) - 2:
            return False, f"Sweep({m}) leftmost={leftmost} steps={steps}"
        fs.append(steps)
    dbl = all(fs[i + 1] == 2 * fs[i] + 2 for i in range(len(fs) - 1))
    return dbl, f"f(m)=2^(m+2)-2 {fs[:6]}..., doubling f(m+1)=2f(m)+2={dbl}, head-contained (leftmost=0)"


def main():
    print("=" * 74)
    print("SWEEP rule — toward the outer-doubling nested induction")
    print(f"  {SPEC}   Sweep(m): 0^(m+1) B> 0 -> 1 0^m B> 0")
    ok, det = verify_sweep_facts()
    print(f"  VERIFIED (sound): {det}")
    r, ihs = prove_sweep()
    print(f"  inductive step (WIP, naive suffix IH): {r}  (applied {ihs}x — does NOT close; see docstring)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
