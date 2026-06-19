#!/usr/bin/env python
"""
Classify the 63 hard 3-state holdouts into BOUNCER vs COUNTER (sound measurement, no proof).

Rationale (from the Bouncers spec): the next-level deciders are type-specific —
  - BOUNCER  (Iijil1/Bouncers; arXiv 2504.20563 §7): time ~ c*n^2, space ~ linear in n,
             so tape WIDTH grows ~ sqrt(steps). Head bounces between walls, region grows
             by a constant each bounce.
  - COUNTER  (sligocki counter-induction): time ~ exponential, so WIDTH grows ~ log(steps)
             (a carry takes ~2x the previous; width creeps).
This pass MEASURES each monster's width-vs-steps growth and bins it, so we know how many each
future decider must target. Pure measurement => sound; it does NOT prove non-halting.

Diagnostic: r = width(1e5) / width(1e4)   (one decade of steps)
  r ~ sqrt(10) ~ 3.16  -> BOUNCER (width ~ sqrt steps)
  r ~ 1 (additive, small)            -> COUNTER (width ~ log steps)
  r ~ 10                             -> LINEAR-TIME grower (width ~ steps) [rare]
"""
from __future__ import annotations

import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import parse

CHECKS = [10_000, 100_000, 300_000]
MAXS = 300_000


def width_profile(spec):
    m = parse(spec); tape = {}; head = 0; st = "A"; lo = hi = 0
    HALT = {"Z", "H", "-"}
    prof = {}
    for i in range(1, MAXS + 1):
        lo, hi = min(lo, head), max(hi, head)
        s = tape.get(head, 0); w, mv, n = m[st][s]; tape[head] = w
        head += 1 if mv == "R" else -1
        if n in HALT:
            return ("HALTS", i, {})
        st = n
        if i in CHECKS:
            prof[i] = hi - lo
    return ("RUN", MAXS, prof)


def diagnose(prof):
    w1, w2 = prof.get(10_000, 0), prof.get(100_000, 0)
    if w1 <= 0:
        return "flat?"
    r = w2 / w1
    if r >= 2.4:
        return "BOUNCER"          # ~sqrt growth (or faster but sub-linear)
    if r <= 1.6:
        return "COUNTER"          # ~log growth
    return "MID"                  # in-between / multi-phase


def main() -> int:
    path = os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")
    specs = [l.strip() for l in open(path) if l.strip()]
    bins = {"BOUNCER": 0, "COUNTER": 0, "MID": 0, "HALTS": 0, "flat?": 0}
    rows = []
    for s in specs:
        status, steps, prof = width_profile(s)
        if status == "HALTS":
            bins["HALTS"] += 1
            rows.append((s, "HALTS", steps, None))
            continue
        d = diagnose(prof)
        bins[d] += 1
        r = prof.get(100_000, 0) / prof.get(10_000, 1)
        rows.append((s, d, prof, round(r, 2)))

    print("=" * 78)
    print("Classifying the 63 hard 3-state monsters by growth law (BOUNCER vs COUNTER)")
    print("=" * 78)
    for s, d, prof, r in rows:
        if d == "HALTS":
            print(f"  {s:>22}  HALTS @ {prof}")
        else:
            print(f"  {s:>22}  {d:>8}  r={r:<5}  widths {prof}")
    print("=" * 78)
    print(f"  BOUNCER (next: Bouncers decider)        : {bins['BOUNCER']}")
    print(f"  COUNTER (next: counter-induction decider): {bins['COUNTER']}")
    print(f"  MID / multi-phase (harder)              : {bins['MID']}")
    print(f"  HALTS within {MAXS} (were cap-limited!)  : {bins['HALTS']}")
    print(f"  flat?                                   : {bins['flat?']}")
    print("\nThis is sound measurement, not a proof. It sets the precise targets for the two")
    print("type-specific deciders to build next (Bouncers / counter-induction).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
