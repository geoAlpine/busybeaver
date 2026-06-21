#!/usr/bin/env python
"""
SOUND sliding-window forward-closure decider (a finite CTL over-approximation).

Abstract state = (TM state, a fixed-width window of 2k+1 tape cells centered on the head).
We compute the FORWARD closure under one TM step. When the head moves, the newly exposed FAR
edge cell is UNKNOWN -> we branch it over {0,1} (a wildcard) and drop the opposite far cell.
Dropping a cell only ADDS configurations; branching a wildcard covers both real possibilities.
So the reachable abstract set OVER-approximates every reachable real config's window.

Therefore: if no reachable abstract state has the head reading a HALT (state,symbol), the real
machine never halts. SOUND by construction (over-approximation never misses a reachable halt).
Inconclusive if the over-approximation reaches a halt-window (too coarse -> raise k).
"""
from __future__ import annotations
import sys, os
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse


def decide(spec, k=3, cap=2_000_000):
    M = parse(spec)
    W = 2 * k + 1
    start = ("A", (0,) * W)                      # blank tape, head centered, state A
    seen = {start}
    dq = deque([start])
    while dq:
        if len(seen) > cap:
            return None, f"blew cap {cap} at k={k}"
        st, cells = dq.popleft()
        r = cells[k]
        tr = M[st].get(r)
        if tr is None:
            return None, f"halt-window REACHABLE (state {st} reads {r}) at k={k}"
        w, d, ns = tr
        base = list(cells); base[k] = w
        if d == "R":
            kept = base[1:W]                     # drop far-left, head moves to center from k+1
            news = [tuple(kept) + (b,) for b in (0, 1)]   # wildcard far-right
        else:
            kept = base[0:W - 1]                 # drop far-right
            news = [(b,) + tuple(kept) for b in (0, 1)]   # wildcard far-left
        for nc in news:
            s2 = (ns, nc)
            if s2 not in seen:
                seen.add(s2); dq.append(s2)
    return True, f"never halts (closure {len(seen)} abstract states, k={k})"


def main():
    targets = ["1RB0LZ_1LC1RA_0RA0LC", "1RB1LC_0LA0RB_1LA0LZ"]
    gates = [("Antihydra", "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
             ("Lucy", "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"),
             ("BB4-halter", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]
    for spec in targets:
        print("TARGET", spec)
        for k in range(2, 13):
            v, msg = decide(spec, k=k)
            print(f"   k={k:2d} -> {v}  {msg}")
            if v is True:
                break
    for n, s in gates:
        print("GATE", n)
        for k in range(2, 9):
            v, msg = decide(s, k=k, cap=500_000)
            print(f"   k={k:2d} -> {v}  {msg}")
            if v is True:
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
