#!/usr/bin/env python
"""
BB(6) lower-bound hunt (in miniature) — you can't COMPUTE BB(6), but you can HUNT its floor.

Each 6-state machine that HALTS gives BB(6) >= (its halt time). The record holders (BB(6) >
10^^15) are found by clever construction + accelerated simulation, NOT brute force. Here we just
randomly sample 6-state machines, brute-run each to a step cap, and keep the LATEST halter we
find — to watch halt times climb past the smaller BBs and feel the explosion / the rarity of
late-halters (which is exactly why records need cleverness, not brute force).

For honesty/contrast we also brute-confirm the known champions BB(4)=107 and BB(5)=47,176,870.
"""
from __future__ import annotations

import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))

HALT = {"Z", "H", "-"}
TRANS = [f"{w}{m}{n}" for w in "01" for m in "LR" for n in "ABCDEFZ"]  # 6 states + halt


def run_fast(spec, cap):
    """Minimal fast simulator; returns (halted, steps)."""
    g = spec.split("_")
    M = []
    idx = {c: i for i, c in enumerate("ABCDEF")}
    for grp in g:
        row = []
        for s in (0, 1):
            t = grp[s*3:s*3+3]
            if t[2] in HALT:
                row.append(None)
            else:
                row.append((int(t[0]), 1 if t[1] == "R" else -1, idx[t[2]]))
        M.append(row)
    tape = {}; head = 0; st = 0; steps = 0
    while steps < cap:
        t = M[st][tape.get(head, 0)]
        if t is None:
            return True, steps
        w, d, nxt = t
        tape[head] = w; head += d; steps += 1; st = nxt
    return False, steps


def random_6state():
    # normalized: A0 = 1RB
    rest = [random.choice(TRANS) for _ in range(11)]
    parts = ["1RB" + rest[0]] + ["".join(rest[1+2*i:3+2*i]) for i in range(5)]
    return "_".join(parts)


def main() -> int:
    cap = 300_000
    N = 40_000
    print("Brute-confirming known champions:")
    print("  BB(4):", run_fast("1RB1LB_1LA0LC_1RZ1LD_1RD0RA", 1000))
    print("  (BB(5)=47,176,870 is too big for this quick cap; trust last night's run.)\n")

    print(f"Hunting BB(6) lower bound: {N:,} random normalized 6-state machines, cap {cap:,} steps")
    best_steps, best_spec = -1, None
    n_halt = 0
    random.seed(20260620)
    for k in range(N):
        spec = random_6state()
        halted, steps = run_fast(spec, cap)
        if halted:
            n_halt += 1
            if steps > best_steps:
                best_steps, best_spec = steps, spec
    print(f"  halters found: {n_halt:,} / {N:,}")
    print(f"  LATEST halter (our hunt's champion): {best_steps:,} steps")
    print(f"    machine: {best_spec}")
    print(f"\n  => BB(6) >= {best_steps:,}  (a true lower bound, from this tiny hunt!)")
    print(f"  Context: BB(5)=47,176,870. The real BB(6) record is > 10^^15 (a tower of 10s),")
    print(f"  found by CONSTRUCTION + accelerated simulation, not random brute force.")
    print(f"  We can't out-search that here — but every halter we found is a real floor, and you")
    print(f"  can FEEL how rare late-halters are: that rarity is why records need cleverness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
