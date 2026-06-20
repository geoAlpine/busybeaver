#!/usr/bin/env python
"""
Word-chain extraction (the core for multi-symbol-repeater bouncers) — SOUND, verified by direct
concrete simulation. NO trace extrapolation (the v3 sin).

A period-q chain: the head, starting at a boundary of a repeated word region, crosses it copy by
copy in q steps each, NET-advancing |adv| cells per copy, returning to the SAME state at every copy
boundary, and writing the SAME transformed word per copy. If that uniform per-copy behaviour holds
across >=2 concrete copies (we check 2 vs 3 for robustness), it provably holds for ANY number of
copies (induction: each copy sees the identical local situation). That is a sound chain rule:
  enter state S at the near boundary of W^m  ->  exit state S at the far boundary, W^m -> W'^m,
  in m*q steps, head net-displaced m*adv.

extract_chain(M, state, tape, head, dir) simulates from the head sitting just before the region and
returns (q, adv, exit_state, read_word, write_word) or None.  dir = +1 (region extends right) / -1.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse


def step(M, tape, head, st):
    tr = M[st][tape.get(head, 0)]
    if tr is None:
        return None
    w, mv, nxt = tr
    tape[head] = w
    return head + (1 if mv == "R" else -1), nxt


def extract_chain(M, st0, tape0, head0, dir, qmax=8):
    """Is the head at head0 (state st0) about to cross a periodic region in direction `dir` with a
    uniform per-copy chain? Try each period q: simulate, require the head to return to st0 at copy
    boundaries having net-advanced the same nonzero `adv` (sign == dir) each copy, with identical
    per-copy read/write words, for copies 1,2,3. Return a dict or None."""
    for q in range(1, qmax + 1):
        tape = dict(tape0); head = head0; st = st0
        boundaries = [(head, st)]                       # (head, state) at copy boundaries
        reads = []; writes = []
        ok = True
        for copy in range(3):
            rd = []; wr = []
            h = head
            for _ in range(q):
                r = tape.get(h, 0); rd.append(r)
                nxt = step(M, tape, h, st)
                if nxt is None:
                    ok = False; break
                wr.append(tape.get(h, 0))
                h, st = nxt
            if not ok:
                break
            head = h
            boundaries.append((head, st))
            reads.append(tuple(rd)); writes.append(tuple(wr))
        if not ok:
            continue
        # uniform: same state at every boundary, same net advance per copy, same read/write words
        states = {b[1] for b in boundaries}
        advs = [boundaries[i + 1][0] - boundaries[i][0] for i in range(3)]
        if len(states) != 1:
            continue
        if len(set(advs)) != 1 or advs[0] == 0 or (advs[0] > 0) != (dir > 0):
            continue
        if reads[0] != reads[1] or reads[1] != reads[2]:
            continue
        if writes[0] != writes[1] or writes[1] != writes[2]:
            continue
        return {"q": q, "adv": advs[0], "state": st0,
                "read": reads[0], "write": writes[0]}
    return None


def _demo():
    # the (10)^n bouncer: at a real (R,B) record the head sweeps LEFT across the repeater, period 2.
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from bouncer_prove_sound import records
    from collections import defaultdict
    spec = "1RB0LB_1LA0RA_0LA0LZ"
    M = parse(spec)
    recs, _ = records(spec, 2000)
    buckets = defaultdict(list)
    for r in recs:
        buckets[(r[2], r[1])].append(r)
    print("spec", spec, "— extract_chain on real tape-extreme records:")
    for key, rs in buckets.items():
        t, st, side, cells, hr = rs[3]
        tape = {i: cells[i] for i in range(len(cells))}
        for d in (-1, 1):
            ch = extract_chain(M, st, dict(tape), hr, d)
            if ch:
                print(f"  {key} dir={d:+d}: {ch}")


if __name__ == "__main__":
    _demo()
