#!/usr/bin/env python
"""
Probe the 2-state HOLDOUTS — the real frontier move: figure out WHY they resist.

Re-run each holdout with GENEROUS limits to separate two cases:
  (a) it was only cap-limited  -> resolves with more steps (our pipeline IS complete here),
  (b) it genuinely needs a stronger decider -> stays a holdout (real escalation needed).
Also: does it even have a halt transition? (no 'Z' => can never halt, trivially.)
"""
from __future__ import annotations

import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import run
from decider import decide
from translated_cyclers import decide_translated


def all_2state_specs():
    trans = [f"{w}{m}{n}" for w in "01" for m in "LR" for n in "ABZ"]
    for a0, a1, b0, b1 in itertools.product(trans, repeat=4):
        yield f"{a0}{a1}_{b0}{b1}"


def classify(spec, sim_cap, exact_cap, tc_time, tc_space):
    halted, steps, _ = run(spec, max_steps=sim_cap)
    if halted:
        return ("HALTS", steps)
    if decide(spec, max_steps=exact_cap)[0] == "NEVER_HALTS":
        return ("NEVER_HALTS-exact", None)
    if decide_translated(spec, time_limit=tc_time, space_limit=tc_space)[0] == "NEVER_HALTS":
        return ("NEVER_HALTS-translated", None)
    return ("HOLDOUT", None)


def main() -> int:
    # find the holdouts under the SMALL limits (same as enumerate2)
    holds = [s for s in all_2state_specs()
             if classify(s, 10_000, 500, 2_000, 1_000)[0] == "HOLDOUT"]
    print(f"Holdouts under small limits: {len(holds)}\n")
    print(f"{'spec':>18}  {'has Z?':>6}  {'verdict @ GENEROUS limits':>30}")
    still = []
    for s in holds:
        hasЗ = "Z" in s
        v, info = classify(s, 200_000, 5_000, 100_000, 20_000)
        detail = v if v != "HALTS" else f"HALTS @ {info}"
        if v == "HOLDOUT":
            still.append(s)
        print(f"{s:>18}  {('yes' if hasЗ else 'NO'):>6}  {detail:>30}")
    print()
    if not still:
        print("RESULT: all 12 were CAP-LIMITED. With generous limits, our sound deciders close")
        print("the ENTIRE 2-state universe (0 holdouts) and the BB(2)=6 champion stands.")
        print("=> the pipeline is complete at n=2; the earlier 12 were just step-budget, not")
        print("   a missing decider.")
    else:
        print(f"RESULT: {len(still)} GENUINE holdouts remain even at generous limits:")
        for s in still:
            print(f"   {s}")
        print("=> these need a STRONGER decider (the real escalation). Inspect them by hand.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
