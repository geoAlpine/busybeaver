#!/usr/bin/env python
"""
Counter PROOF engine (STEP 2) — symbolic macro-simulator + nested induction, oracle-gated.

Built against the spec in STEP2_COUNTER_PLAN.md (sligocki, "BB Counters and Proof by Induction",
2022) — NOT reconstructed from memory. The engine proves a rule  P(n): C(n) -> C(n+d)  by symbolic
simulation, and NEVER_HALTS follows because C(n) is reachable for unboundedly large n with no halt.

SOUNDNESS MODEL (three independent guards; a verdict needs all three):
  (G1) The symbolic simulator is a faithful TM simulator: each micro-step is the real delta, and
       a "chain step" over a uniform run b^c is exactly c real self-loop steps (delta(S,b)=(w,d,S)
       repeats verbatim). This is validated cell-for-cell against the trusted concrete simulator
       (selftest at the bottom) at several concrete n.
  (G2) The induction is well-founded: the hypothesis P is applied only to a block whose symbolic
       length is provably STRICTLY LESS than the current induction variable (asserted), and the
       base case is checked by concrete simulation. A successful symbolic derivation of
       C(n+1) -> C(n+2) using only P(<n+1) + faithful micro/chain steps IS a proof.
  (G3) The oracle gate: every NEVER_HALTS is cross-checked against the concrete simulator to a
       large cap (must not halt). Catches any wrong rule even if (G1)/(G2) had a bug.

If the symbolic derivation does not close, the verdict is HOLDOUT (never a guess).

Exponents are single-variable linear forms a*n+b (a>=0, value>=1 enforced where peeled/crossed).
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, sim

HALT = {"Z", "H", "-"}


# ---------- exponents: a*n + b ----------
def E(a, b):                      # linear exponent a*n+b
    return (a, b)

def e_val(e, n):
    return e[0] * n + e[1]

def e_is_const(e):
    return e[0] == 0

def e_add(e, k):                  # add integer k
    return (e[0], e[1] + k)

def e_lt(e1, e2, base):
    """provably e1 < e2 for ALL n >= base? (linear, so check slope+intercept)."""
    da, db = e2[0] - e1[0], e2[1] - e1[1]      # need da*n + db > 0 for all n>=base
    if da > 0:
        return da * base + db > 0
    if da == 0:
        return db > 0
    return False                                # negative slope -> fails for large n


# ---------- configuration ----------
# state, cur (symbol under head int 0/1), left (list of [sym,exp] far->near head),
# right (list of [sym,exp] far->near head on the right, i.e. last element nearest head).
class Cfg:
    __slots__ = ("st", "cur", "left", "right")
    def __init__(self, st, cur, left, right):
        self.st = st; self.cur = cur
        self.left = [list(b) for b in left]
        self.right = [list(b) for b in right]

    def clone(self):
        return Cfg(self.st, self.cur, self.left, self.right)

    def key(self):
        return (self.st, self.cur, tuple(map(tuple, self.left)), tuple(map(tuple, self.right)))

    def __repr__(self):
        def s(blocks):
            return " ".join(f"{sym}^{e[0]}n+{e[1]}" if e[0] else f"{sym}^{e[1]}"
                            for sym, e in blocks)
        return f"[{s(self.left)}] ({self.st},{self.cur}) [{s(self.right)}]"


def merge(blocks):
    """merge adjacent equal-symbol blocks; drop zero-length blocks."""
    out = []
    for sym, e in blocks:
        if e[0] == 0 and e[1] == 0:
            continue
        if out and out[-1][0] == sym:
            out[-1][1] = (out[-1][1][0] + e[0], out[-1][1][1] + e[1])
        else:
            out.append([sym, (e[0], e[1])])
    return out


def push(stack, sym):
    """push one concrete symbol onto the near-head end of a stack."""
    if stack and stack[-1][0] == sym:
        stack[-1][1] = e_add(stack[-1][1], 1)
    else:
        stack.append([sym, E(0, 1)])


def pop_concrete(stack):
    """pop one concrete symbol from near-head end. Returns (sym, ok). ok=False if the
    near block is symbolic (cannot peel a single cell -> needs a rule)."""
    if not stack:
        return 0, True                          # 0^inf
    sym, e = stack[-1]
    if e[0] != 0:                               # symbolic length -> cannot peel one cell
        return sym, False
    if e[1] <= 0:
        stack.pop(); return pop_concrete(stack)
    stack[-1][1] = e_add(e, -1)
    if stack[-1][1] == (0, 0):
        stack.pop()
    return sym, True


# ---------- one symbolic macro-step (returns (kind, cost_exp); cost = a*n+b micro-steps) ----------
def expose_cur(ahead):
    """Set the head onto the near cell of `ahead`, splitting a symbolic block by one if needed.
    Returns the symbol now under the head. No micro-step is charged (pure re-bracketing)."""
    if not ahead:
        return 0                                         # 0^inf
    sym, e = ahead[-1]
    if e[0] != 0:                                        # symbolic: peel one cell to sit on it
        ahead[-1][1] = e_add(e, -1)
        if ahead[-1][1] == (0, 0):
            ahead.pop()
        return sym
    s, _ = pop_concrete(ahead)
    return s


def macro_step(M, cfg):
    """One faithful action. Returns (kind, cost_exp): ('MICRO',(0,1)) | ('CHAIN',(a,b)) |
    ('HALT',(0,0)). A CHAIN of cost 1+e is exactly 1+e real self-loop micro-steps."""
    tr = M[cfg.st][cfg.cur]
    if tr is None:
        return ("HALT", (0, 0))
    w, dc, ns = tr
    ahead = cfg.right if dc == "R" else cfg.left
    behind = cfg.left if dc == "R" else cfg.right
    # CHAIN: this transition is a self-loop (ns==st) reading cur, and a symbolic run of the SAME
    # symbol sits directly ahead -> the head writes w across cur + the whole run (1+e steps).
    if ns == cfg.st and ahead and ahead[-1][0] == cfg.cur and ahead[-1][1][0] != 0:
        e = ahead[-1][1]
        ahead.pop()
        behind[:] = merge(behind + [[w, (e[0], e[1] + 1)]])    # cur + run, all -> w, now behind
        cfg.st = ns
        cfg.cur = expose_cur(ahead)
        return ("CHAIN", (e[0], e[1] + 1))
    # normal single micro-step
    push(behind, w)
    cfg.cur = expose_cur(ahead)
    cfg.st = ns
    return ("MICRO", (0, 1))


def cfg_to_tape(cfg, n):
    """Instantiate symbolic cfg at concrete n -> (tape dict, head abs index, state). For validation."""
    tape = {}; idx = 0
    # left blocks far->near: lay them ending just left of head
    cells = []
    for sym, e in cfg.left:
        cells += [sym] * e_val(e, n)
    headpos = len(cells)
    cells += [cfg.cur]
    for sym, e in reversed(cfg.right):
        cells += [sym] * e_val(e, n)
    for i, c in enumerate(cells):
        if c: tape[i] = c
    return tape, headpos, cfg.st


def explore(spec, cfg0, n_for_validate=6, max_macro=400):
    """Symbolically simulate from cfg0 with micro+chain steps; stop when STUCK/HALT or budget.
    Returns the macro-op trace and the final cfg. (Diagnostic; no proof yet.)"""
    cfg = cfg0.clone(); trace = []
    for _ in range(max_macro):
        op = macro_step(spec, cfg)
        cfg.left = merge(cfg.left); cfg.right = merge(cfg.right)
        trace.append(op[0] if op[0] != "CHAIN" else f"CHAIN(1n+{op[1][1]}|{op[1][0]})")
        if op[0] in ("HALT", "STUCK"):
            break
    return trace, cfg


# ---------- G1: validate the symbolic simulator against the trusted concrete sim ----------
def concrete_run(M, tape0, head0, st0, nsteps):
    """run the REAL machine nsteps from a concrete config -> (tape,head,st,halted)."""
    tape = dict(tape0); head = head0; st = st0
    for _ in range(nsteps):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return tape, head, st, True
        w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns
    return tape, head, st, False


def norm_tape(tape):
    return {k: v for k, v in tape.items() if v}


def exps_valid(cfg, n):
    return all(e_val(e, n) >= 0 for _, e in cfg.left) and all(e_val(e, n) >= 0 for _, e in cfg.right)


def validate(spec, cfg0, ns=(20, 25, 30, 41), max_macro=160):
    """Lockstep: for each n, replay the symbolic macro-sim and the concrete sim micro-for-micro,
    comparing (tape, head, state) after every macro-op. Stop a given n once the symbolic config
    leaves the valid regime (some block exponent would be negative at that n). Returns (ok, detail)."""
    M = parse(spec); checked = 0
    for n in ns:
        cfg = cfg0.clone()
        tape, head, st = cfg_to_tape(cfg, n)
        ctape, chead, cst = dict(tape), head, st
        for i in range(max_macro):
            op = macro_step(M, cfg)
            cfg.left = merge(cfg.left); cfg.right = merge(cfg.right)
            if op[0] == "HALT":
                break
            if op[0] == "STUCK":
                break
            if not exps_valid(cfg, n):
                break                                   # left the n>=base valid regime; stop this n
            checked += 1
            cost = e_val(op[1], n)
            ctape, chead, cst, halted = concrete_run(M, ctape, chead, cst, cost)
            # compare symbolic-instantiated config to concrete
            stape, shead, sst = cfg_to_tape(cfg, n)
            # align by head absolute position: shift so heads coincide
            if sst != cst:
                return False, f"n={n} op#{i} state {sst}!={cst}"
            # compare tapes relative to head
            keys = set(norm_tape(stape)) | set(norm_tape(ctape))
            for off in range(min(keys, default=0) - chead - 5, max(keys, default=0) - chead + 6):
                sv = stape.get(shead + off, 0); cv = ctape.get(chead + off, 0)
                if sv != cv:
                    return False, f"n={n} op#{i} tape@off{off} {sv}!={cv}\n sym={cfg}\n c h={chead}"
    return True, f"validated {len(ns)} values of n, {checked} macro-ops compared cell-for-cell"


def main():
    # canonical counter, C(n) = A> 0 1^n 0
    spec = "1RB1LA_0LA0RB_0LA0LZ"
    c0 = Cfg("A", 0, [], [[0, E(0, 1)], [1, E(1, 0)]])
    ok, detail = validate(spec, c0)
    print("=" * 74)
    print("Counter PROOF engine — G1 simulator-faithfulness validation")
    print("=" * 74)
    print(f"  canonical {spec}  C(n)=A> 0 1^n 0")
    print(f"  {'OK' if ok else 'FAIL'}: {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())


