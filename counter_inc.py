#!/usr/bin/env python
"""
The increment rule Inc — the first SOUNDLY-PROVEN sub-rule of the canonical counter
1RB1LA_0LA0RB_0LA0LZ. Foundation for the nested binary-counter induction (PIECE 3).

The counter keeps a binary value to the right of a fixed `1` wall (MSB next to the wall, LSB at the
head). One binary increment is the rule

    Inc(b):   0 1^b  B> 0   ->   1 0^b  B> 0          (head at the trailing blank, state B)

i.e. a `0` followed by b trailing ones becomes a `1` followed by b zeros (carry across b ones).

## Why Inc is SOUND for ALL b (not just small b)
Tracing one application (M[state][read]=(write,move,next)):
  - B,0 = 0LA : enter — step left into the run of ones, state A.
  - A,1 = 1LA : SELF-LOOP — sweep LEFT across 1^b leaving them 1. A chain rule: length-independent.
  - A,0 = 1RB : the carry — flip the leading 0 to 1, turn around right, state B.
  - B,1 = 0RB : SELF-LOOP — sweep RIGHT across the b ones turning them to 0. A chain: length-indep.
  - B,0 = ...  : arrive at the trailing blank, state B — done.
So Inc is two verified self-loop chains over 1^b plus O(1) wrap steps. It runs in exactly 2b+2 steps.

## Why Inc is HEAD-CONTAINED (=> applicable in ANY left context)
The leftmost cell the head ever touches is the leading `0` (position 0); it never steps to position
-1. So everything to the left of that `0` is untouched — Inc may be applied to a sub-window of a
larger tape with the left context frozen. (Verified below: leftmost head = 0 for every b.)

This is the load-bearing sub-rule: the full counter is 2^k applications of Inc (with b = the carry
depth, the ruler sequence), and the carry-out D(k)->D(k+1) is the OUTER doubling induction over these
— that outer induction is the remaining (WIP) part of PIECE 3.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse

SPEC = "1RB1LA_0LA0RB_0LA0LZ"


def selfloop(M, state, read):
    """is M[state][read] a self-loop (write w, move d, stay in `state`)? -> (write, move) or None."""
    tr = M[state][read]
    if tr and tr[2] == state:
        return tr[0], tr[1]
    return None


def prove_inc(spec=SPEC):
    """Return (ok, detail). Proves Inc soundly: confirms the two chains are genuine self-loops
    (=> hold for ALL b) and verifies the full rule + head-containment at several b."""
    M = parse(spec)
    # 1. structural soundness: the left and right sweeps must be self-loop chains.
    left = selfloop(M, "A", 1)        # A,1 should be 1LA (sweep left over 1s, keep)
    right = selfloop(M, "B", 1)       # B,1 should be 0RB (sweep right over 1s -> 0)
    if not (left == (1, "L") and right == (0, "R")):
        return False, f"sweeps are not the expected self-loop chains: A,1={left} B,1={right}"
    # 2. verify the full rule + head-containment at several b (the O(1) wraps + the b-independent chains)
    for b in range(1, 12):
        tape = {i: (1 if 1 <= i <= b else 0) for i in range(b + 2)}; head = b + 1; st = "B"
        leftmost = head; steps = 0
        for _ in range(4 * b + 20):
            leftmost = min(leftmost, head)
            tr = M[st][tape.get(head, 0)]
            if tr is None:
                return False, f"Inc({b}) halted"
            w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns; steps += 1
            if st == "B" and head == b + 1 and tape.get(0, 0) == 1 \
               and all(tape.get(i, 0) == 0 for i in range(1, b + 1)) and tape.get(b + 1, 0) == 0:
                break
        else:
            return False, f"Inc({b}) did not reach RHS"
        if leftmost < 0:
            return False, f"Inc({b}) NOT head-contained (head reached {leftmost})"
        if steps != 2 * b + 2:
            return False, f"Inc({b}) took {steps} steps, expected 2b+2={2 * b + 2}"
    return True, "Inc(b): 0 1^b B> 0 -> 1 0^b B> 0, two self-loop chains + O(1), 2b+2 steps, head-contained"


def main():
    print("=" * 74)
    print("Increment rule Inc — first soundly-proven sub-rule of the canonical counter")
    print(f"  {SPEC}")
    ok, detail = prove_inc()
    print(f"  {'PROVEN' if ok else 'FAIL'}: {detail}")
    print("  (the OUTER doubling induction over Inc -> D(k)->D(k+1) is the remaining WIP of PIECE 3.)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
