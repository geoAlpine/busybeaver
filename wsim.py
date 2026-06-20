#!/usr/bin/env python
"""
Word-block symbolic simulator (segment model) — for multi-symbol-repeater bouncers.

Tape = list of segments around an implicit 0^inf on both ends:
  ['c', [cells...]]            concrete run of single cells
  ['r', (W tuple), (a, b)]     a repeater: word W repeated (a*n + b) times  (n the growth variable)
head = (seg index into a 'c' segment, offset); state = letter.

Stepping: ordinary TM micro-step inside concrete segments. When the head would walk INTO a repeater
segment, it is crossed atomically by a VERIFIED word-chain (wchain.extract_chain: q steps/copy,
uniform across 3 concrete copies => sound for any count). No trace extrapolation (the v3 sin).

G1 validation (bottom): instantiate at concrete n, run the macro-sim and the trusted concrete sim
in lockstep, compare cell-for-cell. Same discipline that validated counter_prove.py.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from wchain import extract_chain


def val(exp, n):
    return exp[0] * n + exp[1]


def _cp(segs):
    """deep-copy segments (the 'c' cell lists are mutable and must not be shared)."""
    return [[x[0], list(x[1])] if x[0] == "c" else [x[0], x[1], x[2]] for x in segs]


def expand(segs, n):
    """-> (cells list, seg_start_index list)."""
    cells = []; starts = []
    for s in segs:
        starts.append(len(cells))
        if s[0] == "c":
            cells += list(s[1])
        else:
            cells += list(s[1]) * val(s[2], n)
    return cells, starts


def cfg_to_tape(cfg, n):
    state, segs, hi, ho = cfg
    cells, starts = expand(segs, n)
    head_abs = starts[hi] + ho
    tape = {i: c for i, c in enumerate(cells) if c}
    return tape, head_abs, state


def normalize(cfg):
    """merge adjacent 'c' segs, drop empty/zero-count segs, keep head valid. Returns new cfg."""
    state, segs, hi, ho = cfg
    # map old head to an absolute marker so we can re-find it
    # tag the head cell with a sentinel object inside the concrete seg
    segs = _cp(segs)
    # drop zero-count repeaters and empty concrete segs (but not the head seg) by rebuilding
    out = []; head_marker = ("HEAD", hi, ho)
    for idx, s in enumerate(segs):
        if s[0] == "r" and s[2] == (0, 0):
            continue
        if s[0] == "c" and len(s[1]) == 0 and idx != hi:
            continue
        out.append((idx, s))
    # merge adjacent concrete
    merged = []
    for idx, s in out:
        if s[0] == "c" and merged and merged[-1][1][0] == "c":
            # record offset shift for head if needed
            merged[-1] = (merged[-1][0] + [idx], ["c", merged[-1][1][1] + s[1]])
        else:
            merged.append(([idx], list(s)))
    # find new head seg/off
    new_segs = [m[1] for m in merged]
    new_hi = new_ho = None
    for ni, (idxs, s) in enumerate(merged):
        if hi in idxs and s[0] == "c":
            # offset = cells before in the merged seg + ho
            off = 0
            for j in idxs:
                if j == hi:
                    off += ho; break
                off += len(segs[j][1])
            new_hi, new_ho = ni, off
            break
    if new_hi is None:                       # head seg vanished (shouldn't); fallback
        return state, new_segs, hi, ho
    return state, new_segs, new_hi, new_ho


def micro(M, cfg):
    """One macro action. Returns (kind, cost_in_micro_steps) or ('HALT',0)/('STUCK',0)."""
    state, segs, hi, ho = cfg
    segs = _cp(segs)
    cur = segs[hi][1][ho]
    tr = M[state][cur]
    if tr is None:
        return cfg, ("HALT", 0)
    w, mv, ns = tr
    segs[hi][1][ho] = w
    d = 1 if mv == "R" else -1
    nho = ho + d
    if 0 <= nho < len(segs[hi][1]):
        return (ns, segs, hi, nho), ("MICRO", 1)
    # stepped off this concrete seg
    nbr = hi + d                              # neighbor index in travel direction
    if d > 0:
        if nbr >= len(segs):                  # blank to the right
            segs.append(["c", [0]]); return (ns, segs, nbr, 0), ("MICRO", 1)
        if segs[nbr][0] == "c":
            return (ns, segs, nbr, 0), ("MICRO", 1)
        return cross(M, ns, segs, hi, nbr, +1)
    else:
        if nbr < 0:                           # blank to the left
            segs.insert(0, ["c", [0]]); return (ns, segs, 0, 0), ("MICRO", 1)
        if segs[nbr][0] == "c":
            return (ns, segs, nbr, len(segs[nbr][1]) - 1), ("MICRO", 1)
        return cross(M, ns, segs, hi, nbr, -1)


def cross(M, state, segs, from_seg, rep_seg, d):
    """head in `state` is about to enter repeater segs[rep_seg]=(W,exp) from direction d. Cross via a
    verified word-chain (q steps/copy, advancing |W| cells/copy; the transformed word W' is read from
    the NET result of crossing concrete copies, so q != |W| 'wiggling' chains are handled). The chain
    op carries (exp, q) so the cost is exp*q micro-steps (+1 entry, in validate)."""
    _, W, exp = segs[rep_seg]
    qc = len(W)                                   # cells per copy
    K, BUF = 4, 4                                 # K copies to cross, BUF buffer copies each side
    total = K + 2 * BUF
    cells = list(W) * total
    tape = {i: cells[i] for i in range(len(cells))}
    if d > 0:
        head0 = BUF * qc; tdir = 1
    else:
        head0 = len(cells) - 1 - BUF * qc; tdir = -1
    ch = extract_chain(M, state, dict(tape), head0, tdir, qmax=max(2, 2 * qc + 4))
    if ch is None or abs(ch["adv"]) != qc or ch["state"] != state:
        return (state, segs, from_seg, (0 if d > 0 else len(segs[from_seg][1]) - 1)), ("STUCK", 0)
    qstep = ch["q"]
    # simulate K cycles concretely to read the NET transformed word W'
    t2 = dict(tape); h = head0; s = state
    for _ in range(K * qstep):
        tr = M[s][t2.get(h, 0)]
        if tr is None:
            return (state, segs, from_seg, 0), ("STUCK", 0)
        w, mv, ns = tr; t2[h] = w; h += 1 if mv == "R" else -1; s = ns
    if s != state or h != head0 + d * K * qc:    # must end at the far boundary, same state
        return (state, segs, from_seg, 0), ("STUCK", 0)
    # the K copies just crossed are now behind the head; read W' (period qc), require uniform
    if d > 0:
        region = [t2.get(head0 + i, 0) for i in range(K * qc)]
    else:
        region = [t2.get(head0 - K * qc + 1 + i, 0) for i in range(K * qc)]
    Wp = tuple(region[:qc])
    if any(tuple(region[i:i + qc]) != Wp for i in range(0, K * qc, qc)):
        return (state, segs, from_seg, 0), ("STUCK", 0)
    segs[rep_seg] = ["r", Wp, exp]
    far = rep_seg + d
    if d > 0:
        if far >= len(segs):
            segs.append(["c", [0]]); return (state, segs, far, 0), ("CHAINR", exp, qstep)
        if segs[far][0] == "c":
            return (state, segs, far, 0), ("CHAINR", exp, qstep)
        return (state, segs, rep_seg, 0), ("STUCK", 0)
    else:
        if far < 0:
            segs.insert(0, ["c", [0]]); return (state, segs, rep_seg, 0), ("CHAINL", exp, qstep)
        if segs[far][0] == "c":
            return (state, segs, far, len(segs[far][1]) - 1), ("CHAINL", exp, qstep)
        return (state, segs, rep_seg, 0), ("STUCK", 0)


def absorb(cfg):
    """canonicalize: fold concrete W-copies that sit against a repeater into its exponent (sound
    re-bracketing: 'c'[..W] 'r'W^e == 'r'W^(e+1) with 'c'[..]). Never absorbs the head's cell."""
    state, segs, hi, ho = cfg
    segs = _cp(segs)
    changed = True
    while changed:
        changed = False
        for i, s in enumerate(segs):
            if s[0] != "r":
                continue
            W = s[1]; q = len(W)
            # left neighbor: absorb trailing copies of W
            if i - 1 >= 0 and segs[i - 1][0] == "c":
                c = segs[i - 1][1]; j = 0
                while len(c) >= (j + 1) * q and tuple(c[len(c) - (j + 1) * q: len(c) - j * q]) == W:
                    j += 1
                if i - 1 == hi:                      # don't absorb the head's cell
                    while j > 0 and ho >= len(c) - j * q:
                        j -= 1
                if j > 0:
                    segs[i][2] = (s[2][0], s[2][1] + j)
                    segs[i - 1][1] = c[:len(c) - j * q]; changed = True
            # right neighbor: absorb leading copies of W
            if i + 1 < len(segs) and segs[i + 1][0] == "c":
                c = segs[i + 1][1]; j = 0
                while len(c) >= (j + 1) * q and tuple(c[j * q:(j + 1) * q]) == W:
                    j += 1
                if i + 1 == hi:
                    while j > 0 and ho < j * q:
                        j -= 1
                if j > 0:
                    segs[i][2] = (s[2][0], s[2][1] + j)
                    segs[i + 1][1] = c[j * q:]
                    if i + 1 == hi:
                        ho -= j * q
                    changed = True
    return normalize((state, segs, hi, ho))


def step(M, cfg):
    cfg2, op = micro(M, cfg)
    if op[0] in ("HALT", "STUCK"):
        return cfg2, op
    return absorb(normalize(cfg2)), op


def cost_micro(op, exp_or_word, q, n):
    if op[0] == "MICRO":
        return 1
    if op[0] in ("CHAINR", "CHAINL"):
        return val(op[1], n) * q
    return 0


# ---------------- G1 validation ----------------
def concrete_run(M, tape, head, st, nsteps):
    for _ in range(nsteps):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return tape, head, st, True
        w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns
    return tape, head, st, False


def validate(spec, cfg0, ns=(3, 4, 5, 7), max_macro=200):
    M = parse(spec); checked = 0
    for n in ns:
        cfg = cfg0
        tape, head, st = cfg_to_tape(cfg, n)
        ctape, chead, cst = dict(tape), head, st
        for i in range(max_macro):
            # cost needs q of the repeater being crossed; recompute inside
            prev = cfg
            cfg, op = step(M, cfg)
            if op[0] == "HALT":
                break
            if op[0] == "STUCK":
                break
            if op[0] == "MICRO":
                cost = 1
            else:                                # CHAIN ('CHAINR'/'CHAINL', exp, qstep): 1 entry + copies*qstep
                cost = 1 + val(op[1], n) * op[2]
            ctape, chead, cst, halted = concrete_run(M, ctape, chead, cst, cost)
            stape, shead, sst = cfg_to_tape(cfg, n)
            if sst != cst:
                return False, f"n={n} op#{i} state {sst}!={cst} op={op}"
            keys = set(k for k, v in stape.items() if v) | set(k for k, v in ctape.items() if v)
            for off in range(-3, 4):
                for base in (shead, chead):
                    pass
            # compare relative to head
            allk = set(stape) | set(ctape)
            for k in range(min(allk, default=0) - 2, max(allk, default=0) + 3):
                if stape.get(shead - chead + k, 0) != ctape.get(k, 0):
                    return False, f"n={n} op#{i} tape mismatch @{k} op={op}\n  sym head={shead} {cfg}\n  con head={chead}"
            checked += 1
    return True, f"validated {len(ns)} n-values, {checked} macro-ops cell-for-cell"


def main():
    # (10)^n bouncer; C(n) = (10)^n . "10", head on the trailing 0, state B (matches the (R,B) record).
    spec = "1RB0LB_1LA0RA_0LA0LZ"
    cfg0 = ("B", [["r", (1, 0), (1, 0)], ["c", [1, 0]]], 1, 1)
    ok, detail = validate(spec, cfg0, ns=(6, 7, 8, 10), max_macro=400)
    print("=" * 70)
    print("wsim — G1 word-block simulator validation")
    print(f"  {spec}  C(n) = (10)^n 10, head on trailing 0, state B")
    print(f"  {'OK' if ok else 'FAIL'}: {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
