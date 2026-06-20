#!/usr/bin/env python
"""
SOUND multi-symbol-repeater bouncer prover — on the G1-validated word-block simulator (wsim.py).

Generalises bouncer_prove_sound from single-symbol runs to period-q repeaters. For a (side,state)
tape-extreme record whose growing side is periodic with period p, build the symbolic config
C(n) = [ (W)^n . wall ] (head in the wall), simulate one+ period with wsim (faithful: micro-steps +
VERIFIED word-chains), and declare NEVER_HALTS iff it closes to C(n+d), d>=1 (same seg structure,
repeater exponent bumped). Sound by the same argument as the single-symbol prover; gated on cryptids.
"""
from __future__ import annotations
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, sim
from bouncer_prove_sound import records
from wsim import step, val, exps_valid


def period_of(cells):
    """smallest p in 1..6 with cells (len>=2p) fully p-periodic; else None."""
    for p in range(1, 7):
        if len(cells) < 2 * p:
            continue
        if all(cells[i] == cells[i - p] for i in range(p, len(cells))):
            return p
    return None


def build_left_rep(cells, head, state, L):
    """repeater (word length L) on the LEFT of the head: cells[0:R] = (W)^base, W=cells[0:L]."""
    left = cells[:head]
    if len(left) < 2 * L:
        return None
    W = tuple(cells[:L])
    R = ((head - 1) // L) * L                          # largest L-multiple <= head-1 (keep head in wall)
    if R < L:
        return None
    if any(tuple(cells[i:i + L]) != W for i in range(0, R, L)):
        return None
    segs = [["r", W, (1, 0)], ["c", list(cells[R:])]]
    return (state, segs, 1, head - R), R // L


def build_right_rep(cells, head, state, L):
    """repeater (word length L) on the RIGHT of the head: cells[rep_start:] = (W)^base."""
    right = cells[head + 1:]
    if len(right) < 2 * L:
        return None
    n = len(right)
    w_len = (n // L) * L
    if w_len == n:
        w_len -= L
    if w_len < L:
        return None
    rep_start = head + 1 + (n - w_len)
    W = tuple(cells[rep_start:rep_start + L])
    if any(tuple(cells[rep_start + i:rep_start + i + L]) != W for i in range(0, w_len, L)):
        return None
    segs = [["c", list(cells[:rep_start])], ["r", W, (1, 0)]]
    return (state, segs, 0, head), w_len // L


def seg_key(segs):
    return tuple((s[0], tuple(s[1]) if s[0] == "c" else (s[1], None)) for s in segs)


def closure(start, cur):
    """cur == start with every 'r' exponent bumped by the SAME d>=1, concrete segs identical?"""
    st0, sg0, hi0, ho0 = start
    st1, sg1, hi1, ho1 = cur
    if st0 != st1 or hi0 != hi1 or ho0 != ho1 or len(sg0) != len(sg1):
        return None
    d = None
    for a, b in zip(sg0, sg1):
        if a[0] != b[0]:
            return None
        if a[0] == "c":
            if list(a[1]) != list(b[1]):
                return None
        else:
            if tuple(a[1]) != tuple(b[1]):
                return None
            dd = val(b[2], 0) - val(a[2], 0)           # const difference (a-coeff same by construction)
            if a[2][0] != b[2][0]:
                return None
            if d is None:
                d = dd
            elif dd != d:
                return None
    return d if (d and d >= 1) else None


def prove(spec, steps=20000, max_macro=4000):
    M = parse(spec)
    recs, halted = records(spec, steps)
    if halted:
        return "HALTS", recs[-1][0] if recs else 0
    buckets = defaultdict(list)
    for r in recs:
        buckets[(r[2], r[1])].append(r)
    for key, rs in buckets.items():
        if len(rs) < 3:
            continue
        r = rs[len(rs) // 2]                            # a developed record
        t, st, side, cells, hr = r
        for builder in (build_left_rep, build_right_rep):
            for L in range(1, 7):                       # word length = |adv| of the chain; try 1..6
                built = builder(cells, hr, st, L)
                if not built:
                    continue
                start, base = built
                if base < 1:
                    continue
                cfg = start
                for s in range(max_macro):
                    cfg, op = step(M, cfg)
                    if op[0] in ("HALT", "STUCK"):
                        break
                    if not exps_valid(cfg, base):     # left the n>=base valid regime
                        break
                    if s >= 1:
                        d = closure(start, cfg)
                        if d:
                            return "NEVER_HALTS", ("w-bouncer", key, f"L={L}", f"period~{s+1}", f"n>={base}", f"grow+{d}")
    return "HOLDOUT", "no word-bouncer closure"


def main():
    HALTERS = [("BB(2)", "1RB1LB_1LA1RZ"), ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA"),
               ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]
    CRYPTIDS = [("Antihydra", "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
                ("Space Needle", "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"),
                ("Lucy's Moonlight", "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA")]
    reps = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")) if l.strip()]
    print("=" * 70)
    print("word-bouncer prover — audit")
    print("=" * 70)
    bad = 0
    for name, spec in HALTERS:
        v, _ = prove(spec); h, hs = sim(spec, 1_000_000)
        if v == "NEVER_HALTS" and h:
            print(f"  ‼ {name} FALSE PROOF"); bad += 1
        else:
            print(f"  {name:>6} -> {v}")
    for name, spec in CRYPTIDS:
        v, _ = prove(spec)
        if v == "NEVER_HALTS":
            bad += 1
        print(f"  cryptid {name:<18} -> {v:<12} [{'‼ UNSOUND' if v=='NEVER_HALTS' else 'OK'}]")
    proven = 0
    for spec in reps:
        v, _ = prove(spec)
        if v == "NEVER_HALTS":
            h, hs = sim(spec, 1_000_000)
            if h:
                print(f"  ‼ FALSE PROOF {spec} halts@{hs}"); bad += 1
            else:
                proven += 1
    print("=" * 70)
    print(f"  cryptid/halter false proofs : {bad}   (MUST be 0)")
    print(f"  monsters PROVEN (word-bouncer): {proven} / {len(reps)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
