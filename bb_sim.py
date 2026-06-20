#!/usr/bin/env python
"""
Busy Beaver / Turing-machine simulator — the foundational tool.

Runs an n-state, 2-symbol Turing machine from a blank tape and reports steps-to-halt
and the number of 1s left on the tape. Parses the standard bbchallenge text format:

    "1RB1LB_1LA1RZ"   (BB(2) champion)

Each underscore-separated group is one state's two transitions (for read symbol 0, then 1).
Each transition is 3 chars:  <write 0/1><move L/R><next state A.. or Z=halt>.

Usage:
    python3 bb_sim.py
"""
from __future__ import annotations


def parse(spec: str) -> dict:
    """spec -> machine[state_letter][read_symbol] = (write, move, next_state)."""
    machine = {}
    for i, group in enumerate(spec.split("_")):
        state = chr(ord("A") + i)
        machine[state] = {}
        for sym in (0, 1):
            w, m, nxt = group[sym * 3 : sym * 3 + 3]
            # halt transitions are written "---" in the standard format; write is irrelevant then.
            machine[state][sym] = (int(w) if w in "01" else 0, m, nxt)
    return machine


def run(spec: str, max_steps: int = 200_000_000):
    """Return (halted, steps, ones). 'Z' (or '-','H') in next-state means HALT."""
    machine = parse(spec)
    tape: dict[int, int] = {}
    head = 0
    state = "A"
    steps = 0
    HALT = {"Z", "H", "-"}
    while steps < max_steps:
        sym = tape.get(head, 0)
        write, move, nxt = machine[state][sym]
        tape[head] = write
        head += 1 if move == "R" else -1
        steps += 1
        if nxt in HALT:
            ones = sum(tape.values())
            return True, steps, ones
        state = nxt
    return False, steps, sum(tape.values())


# Known champions, with their KNOWN step counts as a self-check.
CHAMPIONS = [
    ("BB(2)", "1RB1LB_1LA1RZ", 6, 4),
    ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA", 21, 5),
    ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA", 107, 13),
]


def main() -> int:
    print("=" * 64)
    print("Verifying the simulator on small KNOWN champions (hand-checkable):")
    print("=" * 64)
    print(f"{'name':>7}  {'steps':>12}  {'ones':>6}  {'expected':>14}  ok?")
    for name, spec, exp_steps, exp_ones in CHAMPIONS:
        halted, steps, ones = run(spec)
        ok = "OK" if (halted and steps == exp_steps) else "MISMATCH"
        print(f"{name:>7}  {steps:>12}  {ones:>6}  {exp_steps:>7}st/{exp_ones}one  {ok}")
    print("\n(If any MISMATCH: the table in CHAMPIONS is what's wrong, not necessarily")
    print(" the simulator — small ones are hand-traceable. We debug before trusting it.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
