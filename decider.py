#!/usr/bin/env python
"""
A first "decider" — the real tool of the Busy Beaver frontier.

The frontier game is: take a machine and PROVE its fate. Every machine is one of:
  - HALTS              (run it; it stops — easy)
  - NEVER HALTS        (PROVEN infinite — the interesting proofs)
  - HOLDOUT            (this decider couldn't settle it — the battle)

This module ships the simplest sound non-halting proof: **cycle detection**. If the
*normalized configuration* (state + head position relative to the written region +
the trimmed tape contents) ever EXACTLY repeats, the machine is in a deterministic
loop and provably never halts. That is a rigorous proof, from finite observation, of
infinite behavior — exactly the "certify a property you can't reach by just running"
move. It catches *stationary* cyclers; *translated* cyclers (that drift while
repeating a pattern) slip through and need a smarter decider — which is precisely how
the real frontier escalates: better deciders shrink the holdout set.

Usage:  python3 decider.py
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import parse


def normalize(tape: dict[int, int], head: int, state: str):
    """A hashable, position-independent snapshot: trim blanks, make head relative."""
    nz = [k for k, v in tape.items() if v != 0]
    if not nz:
        return (state, 0, ())          # blank tape, head "at the void"
    lo, hi = min(nz), max(nz)
    cells = tuple(tape.get(i, 0) for i in range(lo, hi + 1))
    return (state, head - lo, cells)


def decide(spec: str, max_steps: int = 100_000):
    """Return ('HALTS', steps) | ('NEVER_HALTS', steps_to_proof) | ('HOLDOUT', max_steps)."""
    machine = parse(spec)
    tape: dict[int, int] = {}
    head, state, steps = 0, "A", 0
    HALT = {"Z", "H", "-"}
    seen = {normalize(tape, head, state)}
    while steps < max_steps:
        sym = tape.get(head, 0)
        write, move, nxt = machine[state][sym]
        tape[head] = write
        head += 1 if move == "R" else -1
        steps += 1
        if nxt in HALT:
            return ("HALTS", steps)
        state = nxt
        config = normalize(tape, head, state)
        if config in seen:                       # exact repeat => deterministic loop
            return ("NEVER_HALTS", steps)
        seen.add(config)
    return ("HOLDOUT", max_steps)


CASES = [
    ("BB(4) champion",      "1RB1LB_1LA0LC_1RZ1LD_1RD0RA"),  # halts at 107
    ("trivial eraser loop", "0RA0RA"),                        # never halts (blank recurs)
    ("flip-in-place loop",  "1RB1LA_1LA1RB"),                 # bounded oscillator
    ("runaway right",       "1RA1RA"),                        # infinite, but DRIFTS -> holdout here
]


def main() -> int:
    print("=" * 70)
    print("Decider — sorting machines into HALTS / NEVER_HALTS / HOLDOUT")
    print("=" * 70)
    print(f"{'machine':>20}  {'verdict':>12}  {'@step':>8}")
    # NOTE: this naive decider's normalize() copies the whole tape each step, so it is
    # QUADRATIC on drifting machines (caught it the hard way — the 'runaway right' case
    # hung at 100k). A real decider keeps an incremental/relative config. For tonight we
    # cap at 3000 steps: enough to halt the halters, catch the loopers, and flag the drifter.
    for name, spec in CASES:
        verdict, k = decide(spec, max_steps=3000)
        print(f"{name:>20}  {verdict:>12}  {k:>8}")
    print("\nReading:")
    print("  HALTS       -> ran to a stop (e.g. BB(4) at 107).")
    print("  NEVER_HALTS -> PROVEN infinite: its configuration exactly repeated.")
    print("  HOLDOUT     -> this simple cycle-decider couldn't settle it. 'runaway right'")
    print("                 IS infinite, but it DRIFTS (never exactly repeats), so it slips")
    print("                 through. Catching it needs a smarter decider (detect the drift).")
    print("                 THAT escalation — building deciders that shrink the holdout set —")
    print("                 is the actual frontier work, machine by machine, toward BB(6).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
