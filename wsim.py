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
    segs = [list(s) for s in segs]
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
    segs = [list(s) for s in segs]
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
    """head in `state` is about to enter repeater segs[rep_seg]=(W,exp) from direction d (d=+1 means
    moving right into it, so entering its left/W[0]; d=-1 entering its right/W[-1]). Cross via a
    verified word-chain. Returns (cfg, (kind,cost)) or STUCK."""
    _, W, exp = segs[rep_seg]
    q = len(W)
    # build a concrete window of K copies of W in tape order, head at the entry boundary
    K = 4
    cells = list(W) * K
    if d > 0:
        head0 = 0; tdir = 1
    else:
        head0 = len(cells) - 1; tdir = -1
    tape = {i: cells[i] for i in range(len(cells))}
    ch = extract_chain(M, state, dict(tape), head0, tdir, qmax=max(2, q + 2))
    if ch is None or abs(ch["adv"]) != q or ch["state"] != state:
        return (state, segs, from_seg, (0 if d > 0 else len(segs[from_seg][1]) - 1)), ("STUCK", 0)
    # transformed word in tape order
    write = ch["write"]
    Wp = tuple(write) if d > 0 else tuple(reversed(write))
    segs[rep_seg] = ["r", Wp, exp]
    cost = ("CHAIN", None)                     # symbolic cost; filled by val at validation time
    # head exits the far side of the repeater
    far = rep_seg + d
    if d > 0:
        if far >= len(segs):
            segs.append(["c", [0]]); return (state, segs, far, 0), ("CHAINR", exp)
        if segs[far][0] == "c":
            return (state, segs, far, 0), ("CHAINR", exp)
        # far is another repeater -> recurse cross from boundary (rare); stuck for now
        return (state, segs, rep_seg, 0), ("STUCK", 0)
    else:
        if far < 0:
            segs.insert(0, ["c", [0]]); return (state, segs, rep_seg, 0), ("CHAINL", exp)
        if segs[far][0] == "c":
            return (state, segs, far, len(segs[far][1]) - 1), ("CHAINL", exp)
        return (state, segs, rep_seg, 0), ("STUCK", 0)


def step(M, cfg):
    cfg2, op = micro(M, cfg)
    if op[0] in ("HALT", "STUCK"):
        return cfg2, op
    cfg2 = normalize(cfg2)
    return cfg2, op


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
            else:                                # CHAIN: 1 entry micro-step + (copies * q) chain steps
                q = None
                for s in prev[1]:
                    if s[0] == "r" and s[2] == op[1]:
                        q = len(s[1]); break
                cost = 1 + val(op[1], n) * (q or 1)
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
