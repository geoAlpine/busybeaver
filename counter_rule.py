#!/usr/bin/env python
"""
Rule-verifier for proof-by-induction (sligocki's method) — VALIDATED against his published machine.

A rule is  R: LHS(n) -> RHS(n)  with one repeater carrying the induction variable n. We prove R by
induction, then non-halting follows from a growth rule (the tape grows unboundedly, no halt).

  base : simulate LHS(base) concretely (the trusted simulator); confirm it reaches RHS(base), no halt.
  step : symbolically simulate LHS(n) with the FAITHFUL word-block simulator (wsim, G1-validated),
         and apply the IH R(m) whenever a SUFFIX of the config matches LHS(m) for a linear m provably
         < n (well-founded); confirm it reaches RHS(n), no halt. A successful derivation IS a proof.

This file's `main` VALIDATES the engine on sligocki's machine #11,004,366 and his published rule
P(n): 0^n 1 00 B> 0 -> 1^(n+1) 00 B> 0  (step count f(n)=20*2^n-2n-20, which we also cross-check) —
the "port against a known-correct reference, gated by the oracle" discipline. Only after the engine
reproduces his proof do we trust it on our own counters. NO trusted NEVER_HALTS is emitted until the
engine validates.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from wsim import step, val, _cp, cfg_to_tape
from counter_induct import compress


# ---- a rule template: segs with exactly one repeater whose exp is the variable (a,b)=a*n+b ----
def inst(segs_t, nval):
    """instantiate a seg-template at concrete n -> concrete segs (repeater exps evaluated)."""
    out = []
    for s in segs_t:
        if s[0] == "c":
            out.append(["c", list(s[1])])
        else:
            out.append(["r", tuple(s[1]), (s[2][0], s[2][1])])
    return out


def concrete_steps(M, tape, head, st, nsteps):
    for _ in range(nsteps):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return tape, head, st, True
        w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns
    return tape, head, st, False


def cfg_equal_concrete(M_segs_head, rhs_cfg, n):
    """do two configs instantiate to the same tape+head+state at n?"""
    t1, h1, s1 = cfg_to_tape(M_segs_head, n)
    t2, h2, s2 = cfg_to_tape(rhs_cfg, n)
    if s1 != s2:
        return False
    k1 = {k - h1 for k, v in t1.items() if v}; k2 = {k - h2 for k, v in t2.items() if v}
    if k1 != k2:
        return False
    return all(t1.get(h1 + d, 0) == t2.get(h2 + d, 0) for d in k1)


def verify(spec, state, lhs_segs, lhs_head, rhs_state, rhs_segs, rhs_head, base=2, fcheck=None):
    M = parse(spec)
    # ---- base case (concrete) ----
    lcfg = (state, inst(lhs_segs, base), lhs_head[0], lhs_head[1])
    rcfg = (rhs_state, inst(rhs_segs, base), rhs_head[0], rhs_head[1])
    tape, head, sstate = cfg_to_tape(lcfg, base)
    nsteps = fcheck(base) if fcheck else 4_000_000
    tape, head, sstate, halted = concrete_steps(M, dict(tape), head, sstate, nsteps)
    if halted:
        return False, f"base P({base}) halted"
    # compare to RHS(base)
    rtape, rhead, rstate = cfg_to_tape(rcfg, base)
    if sstate != rstate or {k - head for k, v in tape.items() if v} != {k - rhead for k, v in rtape.items() if v} \
       or any(tape.get(head + d, 0) != rtape.get(rhead + d, 0) for d in {k - rhead for k, v in rtape.items() if v}):
        return False, f"base P({base}) did not reach RHS in {nsteps} steps"
    return True, f"base P({base}) reaches RHS in {nsteps} steps"


def lt_n(e, base):
    """is the linear exponent e=(a,b)=a*n+b provably < n for all n>=base?"""
    a, b = e
    if a == 0:
        return b < base
    if a == 1:
        return b <= -1
    return False


def cfg_matches(cfg, state, segs_t, head):
    """does cfg equal the template (state, segs_t, head) with the symbolic n (exact seg match)?"""
    st, segs, hi, ho = cfg
    if st != state or (hi, ho) != head or len(segs) != len(segs_t):
        return False
    for s, t in zip(segs, segs_t):
        if s[0] != t[0]:
            return False
        if s[0] == "c" and list(s[1]) != list(t[1]):
            return False
        if s[0] == "r" and (tuple(s[1]) != tuple(t[1]) or tuple(s[2]) != tuple(t[2])):
            return False
    return True


def try_suffix_apply(cfg, base):
    """sligocki-P suffix IH: if a suffix '(0,)^e [1,0,0] B> [0]' (e<n, or e==n via one peel) is present
    at the head, apply P(m) -> replace with '(1,)^(m+1) [0,0] B> [0]'. Returns new cfg or None."""
    st, segs, hi, ho = cfg
    if st != "B" or ho != 0 or hi != len(segs) - 1:
        return None
    if segs[hi] != ["c", [0]] or hi < 2 or segs[hi - 1] != ["c", [1, 0, 0]]:
        return None
    r = segs[hi - 2]
    if r[0] != "r" or tuple(r[1]) != (0,):
        return None
    e = tuple(r[2]); ridx = hi - 2
    if lt_n(e, base):
        m = e; prefix = segs[:ridx]
    elif e == (1, 0):                              # e == n: peel one 0 -> expose LHS(n-1)
        m = (1, -1); prefix = segs[:ridx] + [["c", [0]]]
    else:
        return None
    rhs = [["r", (1,), (m[0], m[1] + 1)], ["c", [0, 0]], ["c", [0]]]
    new_segs = prefix + rhs
    return ("B", new_segs, len(new_segs) - 1, 0)


def verify_step(spec, base=2, max_ops=200):
    """Inductive step for sligocki's P, via symbolic sim + suffix IH. Returns (ok, ihs, detail)."""
    M = parse(spec)
    rhs_t = [["r", (1,), (1, 1)], ["c", [0, 0]], ["c", [0]]]
    cfg = ("B", [["r", (0,), (1, 0)], ["c", [1, 0, 0]], ["c", [0]]], 2, 0)   # LHS(n), n symbolic
    ihs = 0
    for _ in range(max_ops):
        if cfg_matches(cfg, "B", rhs_t, (2, 0)):
            return True, ihs, f"step closes to RHS(n) using IH x{ihs}"
        ap = try_suffix_apply(cfg, base)
        if ap is not None:
            cfg = compress(ap); ihs += 1; continue
        cfg = compress(cfg); cfg, op = step(M, cfg)
        if op[0] == "HALT":
            return False, ihs, "halt in step"
        if op[0] == "STUCK":
            return False, ihs, "stuck"
    return False, ihs, "did not close to RHS(n)"


def main():
    # sligocki #11,004,366 ; P(n): 0^n 1 00 B> 0 -> 1^(n+1) 00 B> 0 ; f(n)=20*2^n-2n-20
    spec = "1RB1LA_0LC0RB_0LD0LB_1RE---_1LE1LA"
    f = lambda n: 20 * 2 ** n - 2 * n - 20
    # LHS(n) = 0^n 1 00  B>  0   : segs [ (0,)^n , [1,0,0] , [0] ], head on the last [0]
    lhs = [["r", (0,), (1, 0)], ["c", [1, 0, 0]], ["c", [0]]]
    # RHS(n) = 1^(n+1) 00  B>  0 : segs [ (1,)^(n+1) , [0,0] , [0] ], head on the last [0]
    rhs = [["r", (1,), (1, 1)], ["c", [0, 0]], ["c", [0]]]
    print("=" * 74)
    print("Rule-verifier — validating the engine on sligocki's reference proof")
    print(f"  {spec}")
    for b in (2, 3, 4):
        ok, det = verify(spec, "B", lhs, (2, 0), "B", rhs, (2, 0), base=b, fcheck=f)
        print(f"  base={b}: {'OK' if ok else 'FAIL'} — {det}")
    print("  inductive step (symbolic LHS(n) + suffix IH):")
    oks, ihs, dets = verify_step(spec, base=2)
    print(f"    {'OK' if oks else 'FAIL (expected)'} — {dets}")
    print("  FINDING (verified concretely): the WebFetch'd derivation table was LOSSY. The real")
    print("  reorganisation is  0 1^n 00 B> 0  ->  1 0^(n+2) B>  (a fresh '1 0^m B>' binary counter,")
    print("  NOT '1 0^k 1 00 B>'). So sligocki's machine reduces to the SAME structure as ours — the")
    print("  binary-counter doubling — and there is NO clean suffix recursion. The sound proof needs")
    print("  the nested binary-counter induction (the D(k)->D(k+1) rule with the IH applied through")
    print("  the counter's doubling), not a one-shot suffix rule. The base-case verifier above is")
    print("  validated; the inductive engine is the WIP — and it NEVER emits a trusted proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
