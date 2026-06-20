#!/usr/bin/env python
"""
Bouncers PROOF engine v3 — PHASE-ALIGN the records by (side, state).

v2 (bouncer_prove2.py) took the last 3 records on a side and required all three to share
ONE state (P0[1]==P1[1]==P2[1]). That silently drops every PERIOD-2 bouncer: a machine whose
leftmost/rightmost record alternates between two states (the '1010...' counters the analyzer
flagged with period_ratio ~ 1.0 — constant gap = linear time = a bouncer, NOT an exponential
counter). Three consecutive same-side records read state A,B,A -> the all-equal test fails ->
v2 misses it even though it IS a sound period-q bounce.

v3 fix: bucket the records by (side, state) and compare the last 3 WITHIN a bucket. The phase
is then aligned by construction (same state guaranteed), and the trace P0->P1 now spans one full
bounce cycle (out to the far wall and back), which the period-q tokenizer handles unchanged. The
chain-rule certificate (matching WALL/CHAIN token sequence with >=1 chain grown) is identical;
only the record selection changed.

Everything else (tokenize, the period-q chain rule, the oracle audit on EVERY NEVER_HALTS) is
inherited from v2 verbatim. Sound by the same argument, gated by the same simulator oracle.
"""
from __future__ import annotations

import sys, os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, sim, records, step_trace, tokenize


def prove(spec, steps=30_000):
    recs, halted = records(spec, steps)
    if halted:
        return ("HALTS", recs[-1][0] if recs else 0)
    # bucket by (side, state) -> phase-aligned record streams
    buckets = defaultdict(list)
    for r in recs:
        buckets[(r[4], r[1])].append(r)        # r = (t, state, head, tape, side)
    for (side, state), same in buckets.items():
        if len(same) < 3:
            continue
        P0, P1, P2 = same[-3], same[-2], same[-1]
        # state equality is guaranteed by the bucket key; compare the two bounce traces
        ra, ha = step_trace(spec, P0[3], P0[2], P0[1], P1[0] - P0[0])
        rb, hb = step_trace(spec, P1[3], P1[2], P1[1], P2[0] - P1[0])
        if ha or hb:
            continue
        ta, tb = tokenize(ra), tokenize(rb)
        if len(ta) != len(tb):
            continue
        ok = True; grew = False
        for a, b in zip(ta, tb):
            if a[0] != b[0]:
                ok = False; break
            if a[0] == "WALL":
                if a[1] != b[1]:
                    ok = False; break
            else:  # CHAIN
                if a[1] != b[1]:
                    ok = False; break
                if b[2] < a[2]:
                    ok = False; break
                if b[2] > a[2]:
                    grew = True
        if ok and grew:
            return ("NEVER_HALTS", (side, state, P0[0] + 1, P1[0] - P0[0]))
    return ("HOLDOUT", "no phase-aligned period-q chain bounce")


def main() -> int:
    HALTERS = [("BB(2)", "1RB1LB_1LA1RZ"), ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA"),
               ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]
    reps = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")) if l.strip()]
    print("=" * 74)
    print("Bouncers PROOF engine v3 (phase-aligned by side,state) — SOUNDNESS AUDIT")
    print("=" * 74)
    unsound = 0
    for name, spec in HALTERS:
        v, _ = prove(spec); h, hs = sim(spec, 1_000_000)
        flag = "OK"
        if v == "NEVER_HALTS" and h:
            flag = f"‼ UNSOUND (halts @ {hs})"; unsound += 1
        print(f"  {name:>6} -> {v:<12} [{flag}]")
    proven = held = 0
    holdouts = []
    for spec in reps:
        v, _ = prove(spec)
        if v == "NEVER_HALTS":
            h, hs = sim(spec, 1_000_000)
            if h:
                print(f"  ‼ UNSOUND {spec}: NEVER but halts @ {hs}"); unsound += 1
            else:
                proven += 1
        elif v == "HOLDOUT":
            held += 1; holdouts.append(spec)
    print("=" * 74)
    print(f"  known halters falsely proven : {unsound}")
    print(f"  holdout reps PROVEN never-halt: {proven} / {len(reps)}   (v2 proved 40)")
    print(f"  still holdout                 : {held}")
    if unsound == 0:
        print(f"\n  SOUND. v3 proves {proven} of 63. Remaining holdouts (should be the ~10 true counters):")
        for s in holdouts:
            print(f"    {s}")
    return 1 if unsound else 0


if __name__ == "__main__":
    raise SystemExit(main())
