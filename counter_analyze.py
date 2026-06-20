#!/usr/bin/env python
"""
Counter analysis engine — STEP 1 for the 10 counters (sound: measurement, no halting claim).

The bouncer prover (v2) cleared the 40 bouncers; the remaining holdouts include ~10 COUNTERS
(width ~ log steps; the period between growth events DOUBLES — exponential time). This analyzer
extracts each counter's structure so the PROOF engine (sligocki nested counter-induction — the
hard NEXT build) has precise targets. We deliberately do NOT ship an unsound counter proof here.

For each counter it reports:
  - the growing-block signature at the same-state records (e.g. tape '0 1^k 0', k += const),
  - the period-doubling ratio (gap_{i+1} / gap_i ~ 2 => exponential time => true counter),
  - whether the bouncer prover already proves it (so we count only the genuine residual counters).
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, prove as bouncer_prove

HALT = {"Z", "H", "-"}


def records(spec, steps):
    M = parse(spec); tape = {}; head = 0; st = "A"; lo = hi = 0; recs = []
    for t in range(1, steps + 1):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return recs, True
        w, mv, nxt = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt
        if head < lo or head > hi:
            lo = min(lo, head); hi = max(hi, head)
            bits = "".join(str(tape.get(c, 0)) for c in range(lo, hi + 1))
            recs.append((t, st, head - lo, bits))
    return recs, False


def analyze(spec, steps=200_000):
    recs, halted = records(spec, steps)
    if halted:
        return "HALTS", {}
    # same-state records (the natural growth checkpoints)
    from collections import Counter
    states = Counter(r[1] for r in recs)
    if not states:
        return "no-records", {}
    S = states.most_common(1)[0][0]
    same = [r for r in recs if r[1] == S]
    if len(same) < 5:
        return "few-records", {}
    times = [r[0] for r in same]
    gaps = [times[i+1] - times[i] for i in range(len(times)-1)]
    ratios = [gaps[i+1] / gaps[i] for i in range(len(gaps)-1) if gaps[i] > 0]
    avg_ratio = sum(ratios[-5:]) / len(ratios[-5:]) if ratios else 0
    # block growth: look at the bit strings' length growth
    lens = [len(r[3]) for r in same]
    dlen = [lens[i+1] - lens[i] for i in range(len(lens)-1)]
    block_growth = max(set(dlen[-5:]), key=dlen[-5:].count) if len(dlen) >= 5 else None
    return "COUNTER", {"state": S, "period_ratio": round(avg_ratio, 2),
                       "block_growth_per_record": block_growth,
                       "example_tape": same[min(8, len(same)-1)][3]}


def main() -> int:
    reps = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")) if l.strip()]
    print("=" * 84)
    print("Counter analysis — the residual monsters the bouncer prover can't reach")
    print("=" * 84)
    counters = []
    for spec in reps:
        if bouncer_prove(spec)[0] == "NEVER_HALTS":
            continue                                  # already proven (a bouncer)
        status, info = analyze(spec)
        if status == "COUNTER" and info.get("period_ratio", 0) >= 1.7:
            counters.append((spec, info))
            print(f"  {spec:<22} ratio~{info['period_ratio']:<4} blockΔ={info['block_growth_per_record']}"
                  f"  e.g. tape '{info['example_tape']}'")
        else:
            print(f"  {spec:<22} [{status}] {info}")
    print("=" * 84)
    print(f"  genuine COUNTERS (period doubling, residual): {len(counters)}")
    print("\n  These need the PROOF engine = sligocki nested counter-induction (the carry/doubling")
    print("  cascade is a chain-of-chains). That is the next careful, oracle-gated build. NOT shipped")
    print("  unsound here. Structure extracted above = the targets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
