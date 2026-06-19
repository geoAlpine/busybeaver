#!/usr/bin/env python
"""
Decide the ENTIRE 2-state universe — the real bbchallenge method, in miniature.

Enumerate every 2-state, 2-symbol Turing machine (20,736 of them), and classify EACH with
our tools:
  1. run the simulator: does it HALT within the step cap?  (record its halt time)
  2. if not, run the SOUND deciders (exact-repeat + translated-cycles): proven NEVER_HALTS?
  3. otherwise it's a HOLDOUT (our tools couldn't settle it).

Then check the two things that matter:
  - the maximum halt time over all halting machines should be **6 = BB(2)** (we reproduce
    the first Busy Beaver value ourselves, completely), and
  - the HOLDOUT set should be empty (the simple deciders fully decide the 2-state universe).

This is the step from "tools that work on examples" to "a pipeline that closes a whole class."
"""
from __future__ import annotations

import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import run
from decider import decide                    # sound: exact-config repeat (stationary)
from translated_cyclers import decide_translated  # sound: translated cycles


def all_2state_specs():
    """Every 2-state,2-symbol machine. Transition = write(0/1)+move(L/R)+next(A/B/Z)."""
    trans = [f"{w}{m}{n}" for w in "01" for m in "LR" for n in "ABZ"]   # 12 options
    for a0, a1, b0, b1 in itertools.product(trans, repeat=4):
        yield f"{a0}{a1}_{b0}{b1}"


def classify(spec: str):
    # trivial decider (the one we forgot): no halt transition at all => can never halt. Sound & instant.
    if "Z" not in spec:
        return ("NEVER_HALTS", None)
    halted, steps, _ = run(spec, max_steps=10_000)
    if halted:
        return ("HALTS", steps)
    # stationary cyclers repeat fast & bounded -> small cap keeps the quadratic normalize cheap
    if decide(spec, max_steps=500)[0] == "NEVER_HALTS":
        return ("NEVER_HALTS", None)
    if decide_translated(spec, time_limit=2_000, space_limit=1_000)[0] == "NEVER_HALTS":
        return ("NEVER_HALTS", None)
    return ("HOLDOUT", None)


def main() -> int:
    n_halt = n_inf = n_hold = 0
    best_steps, best_spec = -1, None
    holdouts = []
    total = 0
    for spec in all_2state_specs():
        total += 1
        verdict, steps = classify(spec)
        if verdict == "HALTS":
            n_halt += 1
            if steps > best_steps:
                best_steps, best_spec = steps, spec
        elif verdict == "NEVER_HALTS":
            n_inf += 1
        else:
            n_hold += 1
            if len(holdouts) < 10:
                holdouts.append(spec)

    print("=" * 70)
    print(f"Decided the entire 2-state universe: {total} machines")
    print("=" * 70)
    print(f"  HALTS        : {n_halt}")
    print(f"  NEVER_HALTS  : {n_inf}   (proven by our sound deciders)")
    print(f"  HOLDOUT      : {n_hold}")
    print()
    print(f"  Longest halt : {best_steps} steps   ->  BB(2) = 6 ?  {'YES ✓' if best_steps == 6 else 'NO'}")
    print(f"  Champion     : {best_spec}")
    print(f"  Holdouts left: {n_hold}  {'(EMPTY — class fully decided ✓)' if n_hold == 0 else holdouts}")
    print()
    if best_steps == 6 and n_hold == 0:
        print("RESULT: we independently reproduced BB(2)=6 by deciding EVERY 2-state machine,")
        print("with zero holdouts. The pipeline closes the whole class — the real method, at scale 2.")
    else:
        print("RESULT: not fully closed — inspect holdouts / champion above.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
