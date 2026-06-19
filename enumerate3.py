#!/usr/bin/env python
"""
Scale to the 3-state universe — reproduce BB(3) = 21, the real method at scale 3.

3-state,2-symbol machines: 16^6 = 16.7M. We use the standard BB enumeration normalization
(WLOG the start transition (A,0) = "1RB": writes 1, moves Right, goes to B — the accepted
canonical first move; the BB(3) champion is in this class), reducing to 16^5 = 1,048,576.
Plus the trivial no-halt-state filter. Classify each with the sound deciders.

Check: max halt time should be 21 = BB(3), with 0 holdouts (the 3-state class is fully
decided by trivial + exact-repeat + translated-cycle deciders).
"""
from __future__ import annotations

import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import run
from decider import decide
from translated_cyclers import decide_translated


def specs():
    trans = [f"{w}{m}{n}" for w in "01" for m in "LR" for n in "ABCZ"]   # 16 options
    a0 = "1RB"                                                            # WLOG normalization
    for a1, b0, b1, c0, c1 in itertools.product(trans, repeat=5):
        yield f"{a0}{a1}_{b0}{b1}_{c0}{c1}"


def classify(spec: str):
    if "Z" not in spec:
        return ("NEVER_HALTS", None)                 # no halt transition => trivially infinite
    halted, steps, _ = run(spec, max_steps=2_000)
    if halted:
        return ("HALTS", steps)
    if decide(spec, max_steps=400)[0] == "NEVER_HALTS":
        return ("NEVER_HALTS", None)
    if decide_translated(spec, time_limit=3_000, space_limit=1_500)[0] == "NEVER_HALTS":
        return ("NEVER_HALTS", None)
    return ("HOLDOUT", None)


def main() -> int:
    n_halt = n_inf = n_hold = 0
    best_steps, best_spec = -1, None
    holdouts = []
    total = 0
    for spec in specs():
        total += 1
        if total % 100_000 == 0:
            print(f"  ... {total:,} done | halt {n_halt} inf {n_inf} hold {n_hold} | best {best_steps}", flush=True)
        verdict, steps = classify(spec)
        if verdict == "HALTS":
            n_halt += 1
            if steps > best_steps:
                best_steps, best_spec = steps, spec
        elif verdict == "NEVER_HALTS":
            n_inf += 1
        else:
            n_hold += 1
            if len(holdouts) < 20:
                holdouts.append(spec)

    print("=" * 70)
    print(f"Decided the (normalized) 3-state universe: {total:,} machines")
    print("=" * 70)
    print(f"  HALTS       : {n_halt:,}")
    print(f"  NEVER_HALTS : {n_inf:,}")
    print(f"  HOLDOUT     : {n_hold}")
    print(f"  Longest halt: {best_steps} steps  ->  BB(3) = 21 ?  {'YES ✓' if best_steps == 21 else 'NO'}")
    print(f"  Champion    : {best_spec}")
    if best_steps == 21 and n_hold == 0:
        print("\nRESULT: reproduced BB(3)=21 by deciding the whole (normalized) class, 0 holdouts.")
    else:
        print(f"\nRESULT: not fully closed. holdouts(sample)={holdouts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
