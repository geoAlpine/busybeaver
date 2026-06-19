#!/usr/bin/env python
"""
Unmask the 3-state holdouts — how many DISTINCT hard behaviours, and what do they DO?

The 684 holdouts share prefixes (state C often unreached), so most are the SAME behaviour
replicated across irrelevant transitions. This:
  1. re-finds the holdouts,
  2. dedupes them by their REACHED-transition signature (two machines that only ever use the
     same (state,symbol)->transition entries behave identically — collapses the C-variants),
  3. for each distinct behaviour: probes with GENEROUS limits (cap-limited vs genuinely hard)
     and characterises the dynamics (does the head spread two-sided & unboundedly? that's the
     classic non-cycler the simple deciders can't catch).
"""
from __future__ import annotations

import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import run, parse
from decider import decide
from translated_cyclers import decide_translated


def specs():
    trans = [f"{w}{m}{n}" for w in "01" for m in "LR" for n in "ABCZ"]
    for a1, b0, b1, c0, c1 in itertools.product(trans, repeat=5):
        yield f"1RB{a1}_{b0}{b1}_{c0}{c1}"


def is_holdout(spec):
    if "Z" not in spec:
        return False
    if run(spec, max_steps=2_000)[0]:
        return False
    if decide(spec, max_steps=400)[0] == "NEVER_HALTS":
        return False
    if decide_translated(spec, time_limit=3_000, space_limit=1_500)[0] == "NEVER_HALTS":
        return False
    return True


def reached_signature(spec, steps=3_000):
    """Frozenset of the (state,sym)->transition entries the machine actually uses."""
    machine = parse(spec)
    tape, head, state = {}, 0, "A"
    used = set()
    HALT = {"Z", "H", "-"}
    for _ in range(steps):
        sym = tape.get(head, 0)
        w, m, n = machine[state][sym]
        used.add((state, sym, w, m, n))
        tape[head] = w
        head += 1 if m == "R" else -1
        if n in HALT:
            break
        state = n
    return frozenset(used)


def characterize(spec, steps=30_000):
    """Run long; report head-span growth (two-sided?), ones, and whether it stays a holdout."""
    machine = parse(spec)
    tape, head, state = {}, 0, "A"
    lo = hi = 0
    HALT = {"Z", "H", "-"}
    for i in range(steps):
        lo, hi = min(lo, head), max(hi, head)
        sym = tape.get(head, 0)
        w, m, n = machine[state][sym]
        tape[head] = w
        head += 1 if m == "R" else -1
        if n in HALT:
            return f"HALTS @ {i+1}"
        state = n
    ones = sum(tape.values())
    return f"span [{lo},{hi}] width {hi-lo}, ones {ones} after {steps} steps (no halt)"


def main() -> int:
    print("Re-finding the 3-state holdouts (this takes a few minutes)...", flush=True)
    holds = []
    for k, s in enumerate(specs()):
        if k % 200_000 == 0 and k:
            print(f"  scanned {k:,} ...", flush=True)
        if is_holdout(s):
            holds.append(s)
    print(f"\nHoldouts found: {len(holds)}", flush=True)

    # dedupe by reached-transition signature
    by_sig = {}
    for s in holds:
        by_sig.setdefault(reached_signature(s), []).append(s)
    print(f"Distinct hard BEHAVIOURS (after collapsing irrelevant-transition replicas): {len(by_sig)}\n")

    print(f"{'representative spec':>22}  {'#replicas':>9}  generous-limit probe / dynamics")
    for sig, group in sorted(by_sig.items(), key=lambda kv: -len(kv[1])):
        rep = min(group)                                   # canonical-ish representative
        # cap-limited or genuinely hard?
        big = ("HALTS" if run(rep, max_steps=500_000)[0]
               else "NEVER" if (decide(rep, 5_000)[0] == "NEVER_HALTS"
                                or decide_translated(rep, 50_000, 20_000)[0] == "NEVER_HALTS")
               else "STILL-HOLDOUT")
        dyn = characterize(rep)
        print(f"{rep:>22}  {len(group):>9}  {big:>12} | {dyn}")
    print("\nReading: a 'STILL-HOLDOUT' with two-sided growing span is the classic non-cycler the")
    print("trivial/exact-repeat/translated deciders cannot settle — the next decider's target.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
