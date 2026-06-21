#!/usr/bin/env python
"""
Backward-reachability ('Halting Segment') decider — SOUND.

The machine halts iff the START config (state A, blank tape) can forward-reach a HALT config. Equiv:
the halt is backward-reachable to the start. We do a bounded BACKWARD breadth-first search from the
halt transitions over partial configs (state + a finite map of constrained cells, unconstrained =
wildcard). Backward steps only ADD constraints, so the search OVER-APPROXIMATES forward-reachability.
If the over-approximate backward closure NEVER reaches a start-compatible config (state A with every
constraint = 0) and never needs a cell outside the bounded window, then the halt is UNREACHABLE =>
never halts. (If a backward step would leave the window, we cannot conclude — return None.)

Soundness: a 'never-halts' verdict means even the over-approximation can't connect a halt to the
start, so no real run can either. Verified below: returns never-halts on no halter / cryptid.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse

HALT = {"Z", "H", "-"}


def predecessors(M, cfg, lo, hi):
    """cfg = (state, head, frozenset of (pos,val)). Yield backward predecessors within [lo,hi], or
    signal a window escape with the sentinel 'ESCAPE'."""
    state, head, cons = cfg
    cd = dict(cons)
    for d in (1, -1):
        hp = head - d                                  # predecessor head; it moved by d to reach head
        if not (lo <= hp <= hi):
            yield "ESCAPE"; continue
        for s2 in M:
            for r2 in (0, 1):
                tr = M[s2][r2]
                if tr is None or tr[2] in HALT:
                    continue
                w, mv, ns = tr
                if ns != state or (1 if mv == "R" else -1) != d:
                    continue
                # the predecessor wrote w at hp; in cfg, cell hp must be w (or free)
                if hp in cd and cd[hp] != w:
                    continue
                cd2 = dict(cd)
                if hp in cd2 and cd2[hp] != r2:
                    # the predecessor READ r2 at hp; but cfg already had hp = w (just written).
                    pass
                cd2[hp] = r2                            # predecessor's cell hp held r2 (the read symbol)
                yield (s2, hp, frozenset(cd2.items()))


def is_start(cfg):
    """state A with every constrained cell = 0 (consistent with the all-blank start tape)."""
    state, head, cons = cfg
    return state == "A" and all(v == 0 for _, v in cons)


def halt_segment(spec, W=7, max_configs=60000):
    """SOUND never-halt via bounded backward search. Returns True (never halts) / None (unknown)."""
    M = parse(spec)
    lo, hi = -W, W
    # seed: every reachable-looking halt transition (s,r)->halt, head at 0 reading r
    seeds = []
    for s in M:
        for r in (0, 1):
            tr = M[s][r]
            if tr is None or tr[2] in HALT:
                seeds.append((s, 0, frozenset({(0, r)})))
    if not seeds:
        return None
    seen = set(seeds); frontier = list(seeds)
    while frontier:
        if len(seen) > max_configs:
            return None
        cfg = frontier.pop()
        if is_start(cfg):
            return None                                # the halt is backward-reachable to start
        for pre in predecessors(M, cfg, lo, hi):
            if pre == "ESCAPE":
                return None                            # backward search left the window -> can't conclude
            if pre not in seen:
                seen.add(pre); frontier.append(pre)
    return True                                        # closure exhausted, start never reached


def main():
    HALTERS = ["1RB1LB_1LA1RZ", "1RB1RZ_1LB0RC_1LC1LA", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA",
               "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA"]
    CRYPTIDS = ["1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA",
                "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"]
    print("soundness check — must NOT return 'never-halts' (True) on halters/cryptids:")
    bad = 0
    for s in HALTERS + CRYPTIDS:
        v = halt_segment(s)
        if v is True:
            bad += 1
        print(f"  {s[:34]:<34} -> {v}")
    print(f"  unsound verdicts: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
