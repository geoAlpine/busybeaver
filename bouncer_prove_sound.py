#!/usr/bin/env python
"""
SOUND bouncer prover — built on the G1-VALIDATED symbolic simulator (counter_prove.py).

The unsound v1/v2/v3 compared (state,read,dir) STEP-TRACES and extrapolated "forever" from one
match — and proved the OPEN Antihydra + the HALTING Lucy's Moonlight (SOUNDNESS_INCIDENT.md). This
prover does NOT look at traces. It works on the ACTUAL symbolic tape:

  1. (heuristic, soundness-irrelevant) from concrete simulation, find two consecutive same-(side,
     state) tape-extreme records that differ by GROWTH of a single-symbol run -> the repeater.
  2. build the symbolic configuration C(n) = (walls with that run made `c^n`), n the growing count.
  3. symbolically simulate one period with the FAITHFUL macro-stepper (base steps + exact self-loop
     CHAIN steps; the same one validated cell-for-cell against the trusted sim in counter_prove G1).
  4. SOUND verdict: NEVER_HALTS iff the simulation returns to the START configuration with the
     repeater exponent strictly larger (n -> n+d, d>=1) and everything else identical, with no halt
     and all exponents staying valid. That symbolic derivation IS an induction: C(n) => C(n+d) for
     all n>=base => unbounded growth => never halts.

Why this is sound where v3 was not: a CHAIN step only fires when the head genuinely faces a uniform
symbolic run and yields the faithful TM result; if the machine is a counter/cryptid (Antihydra),
the symbolic run FRAGMENTS (the head peels into non-uniform cells) and never closes back to C(n+d).
So it cannot prove Antihydra. Gated, hard, on the 3 cryptids + known halters anyway.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from counter_prove import Cfg, E, macro_step, merge, e_val
from bouncer_prove2 import parse, sim

HALT = {"Z", "H", "-"}


def records(spec, steps):
    """tape-extreme records: (t, state, side, cells[lo..hi] as int list, head_idx_in_cells)."""
    M = parse(spec); tape = {}; head = 0; st = "A"; lo = hi = 0; recs = []
    for t in range(1, steps + 1):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return recs, True
        w, mv, nxt = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt
        side = None
        if head < lo:
            lo = head; side = "L"
        elif head > hi:
            hi = head; side = "R"
        if side:
            cells = [tape.get(c, 0) for c in range(lo, hi + 1)]
            recs.append((t, st, side, cells, head - lo))
    return recs, False


def rle(x):
    out = []
    for v in x:
        if out and out[-1][0] == v:
            out[-1][1] += 1
        else:
            out.append([v, 1])
    return out


def grow_run(x0, x1):
    """x0,x1 identical except ONE maximal single-symbol run is longer in x1 -> (a,b,sym) interval
    of that run in x0's coords (base = b-a >= 1). Else None. (RLE-based, so head-adjacent runs and
    walls are handled; multi-symbol repeaters yield >1 differing run and are rejected.)"""
    r0, r1 = rle(x0), rle(x1)
    if len(r0) != len(r1):
        return None
    diff = []
    for j, ((s0, c0), (s1, c1)) in enumerate(zip(r0, r1)):
        if s0 != s1:
            return None
        if c0 != c1:
            diff.append(j)
    if len(diff) != 1:
        return None
    j = diff[0]
    if r1[j][1] <= r0[j][1]:
        return None
    a = sum(c for _, c in r0[:j]); b = a + r0[j][1]
    return a, b, r0[j][0]


def find_growth(R0, R1):
    """Align two same-(side,state) records by HEAD; if exactly one single-symbol run on one side of
    the head grew (other side identical), return (a,b,symbol) = that run's interval in R0's cells."""
    c0, h0 = R0[3], R0[4]; c1, h1 = R1[3], R1[4]
    if c0[h0] != c1[h1]:
        return None
    L0, L1 = c0[:h0], c1[:h1]                         # left of head (in order)
    Rt0, Rt1 = c0[h0 + 1:], c1[h1 + 1:]              # right of head
    if Rt0 == Rt1:                                    # left side grew
        g = grow_run(L0, L1)
        if g:
            return g
    if L0 == L1:                                      # right side grew
        g = grow_run(Rt0, Rt1)
        if g:
            a, b, sym = g
            return a + h0 + 1, b + h0 + 1, sym
    return None


def runs_blocks(cells_marks):
    """cells_marks = list of (sym, is_symbolic); -> block list in the SAME order. A contiguous
    symbolic run becomes ONE block E(1,0)=n (coefficient 1, regardless of length); concrete runs
    become E(0,count)."""
    out = []
    for sym, issym in cells_marks:
        if issym:
            if out and out[-1][0] == sym and out[-1][2]:
                pass                                 # already one symbolic block for this run
            else:
                out.append([sym, (1, 0), True])
        else:
            if out and out[-1][0] == sym and not out[-1][2]:
                out[-1][1] = (out[-1][1][0], out[-1][1][1] + 1)
            else:
                out.append([sym, (0, 1), False])
    return [[s, e] for s, e, _ in out]


def build_cfg(R, a, b):
    """build symbolic Cfg from record R with cells[a:b] (a single-symbol run) made symbolic c^n.
    Returns (cfg, base) where base = b-a = the run's length in this record = the value of n here."""
    _, st, _, cells, h = R
    marks = [(cells[i], a <= i < b) for i in range(len(cells))]
    left = runs_blocks(marks[:h])                    # far->near, last nearest head
    right_near_far = runs_blocks(marks[h + 1:])      # near->far
    right = list(reversed(right_near_far))           # far->near, last nearest head
    return Cfg(st, cells[h], left, right), b - a


def exps_valid(cfg, n):
    return all(e_val(e, n) >= 0 for _, e in cfg.left) and all(e_val(e, n) >= 0 for _, e in cfg.right)


def blocks_shift(b_start, b_now):
    """do b_now == b_start with every symbolic E(1,k) bumped by the SAME d>=1? return d or None."""
    if len(b_start) != len(b_now):
        return None
    d = None
    for (s0, e0), (s1, e1) in zip(b_start, b_now):
        if s0 != s1 or e0[0] != e1[0]:
            return None
        if e0[0] == 0:                               # concrete: must match exactly
            if e0[1] != e1[1]:
                return None
        else:                                        # symbolic: same bump d
            dd = e1[1] - e0[1]
            if d is None:
                d = dd
            elif dd != d:
                return None
    return d if d is not None else 0                  # no symbolic block on this side -> shift 0


def is_closure(start, cur):
    """cur == start with symbolic exponents bumped by a uniform d>=1? -> d or None."""
    if cur.st != start.st or cur.cur != start.cur:
        return None
    dl = blocks_shift(start.left, cur.left)
    dr = blocks_shift(start.right, cur.right)
    if dl is None or dr is None:
        return None
    ds = {x for x in (dl, dr) if x != 0}
    if len(ds) != 1:
        return None
    d = ds.pop()
    return d if d >= 1 else None


def prove(spec, steps=30_000, max_macro=4000):
    M = parse(spec)
    recs, halted = records(spec, steps)
    if halted:
        return "HALTS", recs[-1][0] if recs else 0
    # group by (side,state); try consecutive pairs for a single-symbol growth
    from collections import defaultdict
    buckets = defaultdict(list)
    for r in recs:
        buckets[(r[2], r[1])].append(r)
    for key, rs in buckets.items():
        if len(rs) < 2:
            continue
        for i in range(len(rs) - 1):
            g = find_growth(rs[i], rs[i + 1])
            if not g:
                continue
            a, b, sym = g
            start, base = build_cfg(rs[i], a, b)     # base = n at this record (the run's length)
            if base < 1:
                continue
            start.left = merge(start.left); start.right = merge(start.right)
            # symbolic-simulate from C(n); a closure C(n)=>C(n+d) proven valid for all n>=base, and
            # the real trajectory IS at C(base) (this record) -> never halts. Validity checked at base.
            cfg = start.clone(); ok_regime = True
            for step in range(max_macro):
                op = macro_step(M, cfg)
                cfg.left = merge(cfg.left); cfg.right = merge(cfg.right)
                if op[0] == "HALT":
                    ok_regime = False; break
                if not exps_valid(cfg, base):
                    ok_regime = False; break
                if step >= 1:                        # don't match the trivial start
                    d = is_closure(start, cfg)
                    if d:
                        return "NEVER_HALTS", ("sound-bouncer", key, f"n>={base}", f"period~{step+1}", f"grow+{d}")
    return "HOLDOUT", "no sound bouncer closure"


def main():
    HALTERS = [("BB(2)", "1RB1LB_1LA1RZ"), ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA"),
               ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]
    CRYPTIDS = [("Antihydra", "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
                ("Space Needle", "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"),
                ("Lucy's Moonlight", "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA")]
    reps = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")) if l.strip()]
    print("=" * 78)
    print("SOUND bouncer prover — audit")
    print("=" * 78)
    bad = 0
    for name, spec in HALTERS:
        v, _ = prove(spec); h, hs = sim(spec, 1_000_000)
        if v == "NEVER_HALTS" and h:
            print(f"  ‼ {name}: FALSE PROOF"); bad += 1
        else:
            print(f"  {name:>6} -> {v}")
    for name, spec in CRYPTIDS:
        v, info = prove(spec)
        flag = "‼ UNSOUND FALSE PROOF" if v == "NEVER_HALTS" else "OK (HOLDOUT/HALTS)"
        if v == "NEVER_HALTS":
            bad += 1
        print(f"  cryptid {name:<18} -> {v:<12} [{flag}]")
    proven = 0
    for spec in reps:
        v, _ = prove(spec)
        if v == "NEVER_HALTS":
            h, hs = sim(spec, 1_000_000)
            if h:
                print(f"  ‼ FALSE PROOF {spec} halts@{hs}"); bad += 1
            else:
                proven += 1
    print("=" * 78)
    print(f"  cryptid/halter false proofs : {bad}   (MUST be 0)")
    print(f"  monsters PROVEN (sound)      : {proven} / {len(reps)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
