#!/usr/bin/env python
"""
Counter prover — STEP 2, the nested-induction engine. PIECE 1: the macro-machine substrate.

The bouncer provers build a repeater seg by hand from a record. A COUNTER's interior is a binary
counter (not one uniform run), so to accelerate it we must (a) AUTO-COMPRESS uniform runs into
repeaters and (b) cross them with wsim's verified chains. This file builds and G1-VALIDATES that
substrate. The rule-detection + proof-by-induction layers come next (PIECE 2/3).

`compress` is a SOUND re-bracketing: a run of k identical cells in a concrete segment becomes a
repeater (sym,)^k. It never touches the head's cell. With it, the counter's left/right sweeps
(self-loop chains: here state A sweeps left over 1s unchanged, state B sweeps right over 1s -> 0)
become single macro-steps, so the simulator reaches k carry-outs in ~poly(k) macro-steps with the
SAME tape as the trusted simulator (validated below).
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from wsim import step, val, cfg_to_tape, _cp, normalize


def compress(cfg, T=2):
    """fold maximal single-symbol runs (length >= T) in concrete segments into (sym,)^len repeaters.
    Never folds the head's cell. Sound re-bracketing; returns a normalized cfg."""
    state, segs, hi, ho = cfg
    out = []
    for idx, s in enumerate(_cp(segs)):
        if s[0] != "c":
            out.append(s); continue
        cells = s[1]
        head_off = ho if idx == hi else None
        i = 0; pieces = []                          # list of ('c',[..]) / ('r',(sym,),(0,k))
        while i < len(cells):
            j = i
            while j < len(cells) and cells[j] == cells[i]:
                j += 1
            run = (i, j)                              # [i,j) all equal cells[i]
            head_in = head_off is not None and i <= head_off < j
            if j - i >= T and not head_in:
                pieces.append(["r", (cells[i],), (0, j - i)])
            else:
                pieces.append(["c", list(cells[i:j])])
            i = j
        # if the head was in this seg, find which piece holds it and record (seg_index, offset)
        out.extend(pieces)
    # rebuild head index: locate the concrete piece that contains the head cell
    new_segs = out
    # recompute hi/ho by walking cells up to the original head absolute position
    cells_all, starts = cfg_to_tape(cfg, 0)[0], None
    # simpler: find head by absolute position
    abs_head = _abs_head(cfg)
    nhi, nho = _locate(new_segs, abs_head)
    return normalize((state, new_segs, nhi, nho))


def _abs_head(cfg):
    _, segs, hi, ho = cfg
    pos = 0
    for i, s in enumerate(segs):
        if i == hi:
            return pos + ho
        pos += len(s[1]) if s[0] == "c" else len(s[1]) * val(s[2], 0)
    return pos


def _locate(segs, abs_pos):
    pos = 0
    for i, s in enumerate(segs):
        ln = len(s[1]) if s[0] == "c" else len(s[1]) * val(s[2], 0)
        if s[0] == "c" and pos <= abs_pos < pos + ln:
            return i, abs_pos - pos
        pos += ln
    return 0, 0


def macro_run(spec, start, max_ops=4000, T=2):
    """accelerated macro-sim: compress then step, repeatedly. Returns list of (op, cfg)."""
    M = parse(spec); cfg = start; trace = []
    for _ in range(max_ops):
        cfg = compress(cfg, T)
        cfg, op = step(M, cfg)
        trace.append((op, cfg))
        if op[0] in ("HALT", "STUCK"):
            break
    return trace


# ---------------- G1 validation: accelerated sim vs trusted concrete sim ----------------
def concrete_run(M, tape, head, st, nsteps):
    for _ in range(nsteps):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return tape, head, st, True
        w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns
    return tape, head, st, False


def micro_cost(op, n):
    if op[0] == "MICRO":
        return 1
    if op[0] in ("CHAINR", "CHAINL"):
        return 1 + val(op[1], n) * op[2]
    return 0


def validate(spec, max_ops=300):
    """run the accelerated sim from the blank tape and the trusted sim in lockstep, cell-for-cell."""
    M = parse(spec)
    cfg = ("A", [["c", [0]]], 0, 0)
    ctape, chead, cst = {}, 0, "A"
    for i in range(max_ops):
        cfg = compress(cfg, 2)
        cfg, op = step(M, cfg)
        if op[0] in ("HALT", "STUCK"):
            break
        cost = micro_cost(op, 0)                       # exps are concrete here (n unused) -> val(,0)
        ctape, chead, cst, halted = concrete_run(M, ctape, chead, cst, cost)
        stape, shead, sst = cfg_to_tape(cfg, 0)
        if sst != cst:
            return False, f"op#{i} state {sst}!={cst} op={op}"
        allk = set(k for k, v in stape.items() if v) | set(k for k, v in ctape.items() if v)
        for k in range(min(allk, default=0) - 2, max(allk, default=0) + 3):
            if stape.get(shead - chead + k, 0) != ctape.get(k, 0):
                return False, f"op#{i} tape@{k} op={op}\n sym={cfg}"
    return True, f"validated {max_ops} accelerated macro-ops cell-for-cell"


def main():
    spec = "1RB1LA_0LA0RB_0LA0LZ"
    ok, detail = validate(spec)
    print("=" * 70)
    print("counter_induct PIECE 1 — accelerated macro-machine (compress + chains), G1")
    print(f"  {spec}")
    print(f"  {'OK' if ok else 'FAIL'}: {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
