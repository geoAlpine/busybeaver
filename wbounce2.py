#!/usr/bin/env python
"""
Multi-symbol bouncer prover v2 — find the period-q repeater BETWEEN walls via a two-record diff.

wbounce.py builds a repeater only when a whole side of a record is periodic (period_of). That misses
bouncers whose growing repeater sits between fixed walls (e.g. a trailing '00' wall), so it never even
builds a candidate. Here we head-align two consecutive same-(side,state) records and locate the
growing periodic block by diff (common prefix/suffix -> the middle grew by k copies of a word W). Then
we build C(n)=[outer-wall (W)^n inner-wall] and run the G1-validated word-block simulator (wsim) for
one period, declaring NEVER_HALTS only on a structural closure C(n)=>C(n+d). Sound by the same
argument as wbounce; gated on the cryptids + cross-checked.
"""
from __future__ import annotations
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, sim
from bouncer_prove_sound import records
from wsim import step, val, exps_valid, cfg_to_tape


def _strip_copies(x, W):
    """strip leading copies of tuple W from list x; return (count, remainder)."""
    q = len(W); k = 0
    while len(x) - k * q >= q and tuple(x[k * q:k * q + q]) == W:
        k += 1
    return k, x[k * q:]


def find_periodic_growth(R0, R1):
    """head-align R0,R1; if one side grew by m copies of a word W that is INSERTED adjacent to the
    head (the repeater grows at the head end; a fixed wall sits at the far end), return
    (side, W, base_copies, wall) with side in {'L','R'} = which side of the head the repeater is on.
    Sound detection only: build+closure does the actual proving."""
    c0, h0 = R0[3], R0[4]; c1, h1 = R1[3], R1[4]
    if c0[h0] != c1[h1]:
        return None
    for side in ("L", "R"):
        if side == "R":
            x0, x1 = c0[h0 + 1:], c1[h1 + 1:]              # right of head: head-end = left end of x
            other0, other1 = c0[:h0], c1[:h1]
        else:
            x0, x1 = c0[:h0], c1[:h1]                      # left of head: head-end = right end of x
            other0, other1 = c0[h0 + 1:], c1[h1 + 1:]
        if other0 != other1 or len(x1) <= len(x0):
            continue
        d = len(x1) - len(x0)
        for q in range(1, 7):
            if d % q:
                continue
            m = d // q
            if side == "R":
                ins = x1[:d]                               # inserted block at head end (left of x)
                if x1[d:] != x0:
                    continue
                W = tuple(ins[:q])
                if any(tuple(ins[i:i + q]) != W for i in range(0, d, q)):
                    continue
                k, wall = _strip_copies(x0, W)            # x0 = (W)^k + wall(far end)
                if k < 1:
                    continue
                return side, W, k, wall
            else:
                ins = x1[len(x0):]                         # inserted block at head end (right of x)
                if x1[:len(x0)] != x0:
                    continue
                W = tuple(ins[:q])
                if any(tuple(ins[i:i + q]) != W for i in range(0, d, q)):
                    continue
                # left side: repeater adjacent to head is the SUFFIX of x; strip from the right
                rx0 = list(reversed(x0)); rW = tuple(reversed(W))
                k, rwall = _strip_copies(rx0, rW)
                if k < 1:
                    continue
                wall = list(reversed(rwall))
                return side, W, k, wall
    return None


def build(R0, g):
    side, W, base, wall = g
    _, st, _, cells, h = R0
    rep = ["r", list(W), (1, 0)]                       # (W)^n, n=base at this record
    head_cell = ["c", [cells[h]]]
    if side == "R":
        other = list(cells[:h])                        # cells left of head (fixed wall, opposite side)
        segs = [["c", other], head_cell, rep, ["c", list(wall)]]
        segs = [s for s in segs if s[0] != "c" or s[1]]
        hi = segs.index(head_cell); ho = 0
        return (st, segs, hi, ho), base
    else:
        other = list(cells[h + 1:])                    # cells right of head (fixed wall, opposite side)
        segs = [["c", list(wall)], rep, head_cell, ["c", other]]
        segs = [s for s in segs if s[0] != "c" or s[1]]
        hi = segs.index(head_cell); ho = 0
        return (st, segs, hi, ho), base


def closure(start, cur):
    st0, sg0, hi0, ho0 = start; st1, sg1, hi1, ho1 = cur
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
            if tuple(a[1]) != tuple(b[1]) or a[2][0] != b[2][0]:
                return None
            dd = b[2][1] - a[2][1]
            if d is None:
                d = dd
            elif dd != d:
                return None
    return d if (d and d >= 1) else None


def faithful(cfg, base, rec):
    """SOUNDNESS GATE: the built config at n=base must equal the real machine tape at this record.
    If it does not, a closure on cfg proves nothing about THIS machine (cfg may be unreachable)."""
    t, rst, side, cells, hd = rec
    tape, head_abs, state = cfg_to_tape(cfg, base)
    if state != rst:
        return False
    # head-relative comparison, ignoring blank (0) cells beyond the written region on both ends
    lo = min([head_abs] + list(tape)); hi = max([head_abs] + list(tape))
    built = [tape.get(j, 0) for j in range(lo, hi + 1)]
    bh = head_abs - lo
    bl = ''.join(map(str, built[:bh])).lstrip('0')
    br = ''.join(map(str, built[bh + 1:])).rstrip('0')
    bc = built[bh]
    rl = ''.join(map(str, cells[:hd])).lstrip('0')
    rr = ''.join(map(str, cells[hd + 1:])).rstrip('0')
    rc = cells[hd]
    return bl == rl and br == rr and bc == rc


def _canon(state, tape, head):
    keys = [k for k, v in tape.items() if v]
    lo = min(keys + [head]); hi = max(keys + [head])
    while lo < head and tape.get(lo, 0) == 0:
        lo += 1
    while hi > head and tape.get(hi, 0) == 0:
        hi -= 1
    return (state, tuple(tape.get(j, 0) for j in range(lo, hi + 1)), head - lo)


def _canon_cfg(start, n):
    tape, head, state = cfg_to_tape(start, n)
    return _canon(state, dict(tape), head)


def concrete_closure_ok(M, start, base, d, cap=2_000_000, checks=3):
    """SOUNDNESS GATE 2 (concrete-induction): the symbolic wsim closure C(n)=>C(n+d) is only trusted
    if the REAL machine actually maps C(base+j) -> C(base+j+d), exactly and without halting, for
    several consecutive j. This catches wsim chain-extrapolation that is unfaithful at small n
    (e.g. it 'proved' a real BB(6) bouncer mapping C(1)->C(2) when the machine does C(1)->C(6))."""
    for j in range(checks):
        ns = base + j
        tgt = _canon_cfg(start, ns + d)
        tape, head, state = cfg_to_tape(start, ns); tape = dict(tape)
        reached = False
        for _ in range(cap):
            r = tape.get(head, 0); tr = M[state].get(r)
            if tr is None:
                return False                          # halts -> closure is false
            w, dd, nx = tr; tape[head] = w; state = nx; head += 1 if dd == "R" else -1
            if state == tgt[0] and _canon(state, tape, head) == tgt:
                reached = True; break
        if not reached:
            return False
    return True


def prove(spec, steps=20000, max_macro=6000):
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
        for i in range(len(rs) - 2):
            g = find_periodic_growth(rs[i], rs[i + 1])
            if not g:
                continue
            built = build(rs[i], g)
            if not built:
                continue
            start, base = built
            if base < 1:
                continue
            if not faithful(start, base, rs[i]):     # soundness gate: C(base) must be the real config
                continue
            cfg = start
            for s in range(max_macro):
                cfg, op = step(M, cfg)
                if op[0] in ("HALT", "STUCK"):
                    break
                if not exps_valid(cfg, base):
                    break
                if s >= 1:
                    d = closure(start, cfg)
                    if d:
                        if not concrete_closure_ok(M, start, base, d):
                            break                     # symbolic closure not confirmed concretely -> reject
                        return "NEVER_HALTS", ("wbounce2", key, f"W={g[1]}", f"period~{s+1}", f"n>={base}", f"grow+{d}")
    return "HOLDOUT", "no closure"


def main():
    spec = "1RB0LC_0LA0RA_1LA0LZ"
    print("target bouncer:", prove(spec))
    print("other bouncer :", prove("1RB0LZ_1LC0RA_0RB0LB"))
    for n, s in [("BB4", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA"),
                 ("Antihydra", "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
                 ("Lucy", "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA")]:
        print(f"  gate {n}: {prove(s)[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
