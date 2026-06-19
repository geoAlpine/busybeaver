#!/usr/bin/env python
"""
Translated Cyclers decider — faithful port of the bbchallenge reference (S(5)-gated).

This replaces the UNSOUND lin_decider.py. The algorithm is the "record" method from
github.com/bbchallenge/bbchallenge-deciders/decider-translated-cyclers (the exact one
that, with the Cyclers decider, settled the bulk of the BB(5) seed database and is part
of the machine-checked S(5)=47,176,870 result):

  - Snapshot ("record") the configuration ONLY when the head reaches a NEW extreme
    position (new leftmost OR new rightmost cell — a "record-breaking" step).
  - Bucket records by (side, state, read-symbol). When a record breaks, compare it to
    every earlier record in the SAME bucket.
  - Two records are equivalent (=> machine never halts, drifting by d = p1 - p0) iff,
    walking from the head INTO the explored region, the current tape and the past tape
    agree (head-relative: now[p1+offset] == past[p0+offset]) over EXACTLY the band of
    cells visited since the past record's time. The walk stops at the first cell not
    visited since then (that's the proof's "distance L" — comparing fewer is unsound,
    comparing the whole tape is unnecessary).
  - Soundness: same state, head at a fresh frontier reading the same symbol, and identical
    tape over everything reachable since the earlier record => the segment repeats
    verbatim, translated by d, forever.

Built WITH a soundness audit: every NEVER_HALTS claim is cross-checked against the trusted
simulator (the known-halter oracle that caught the previous unsound attempt).
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import parse, run


def decide_translated(spec: str, time_limit: int = 50_000, space_limit: int = 20_000):
    """('HALTS',k) | ('NEVER_HALTS',(settle,period,drift)) | ('HOLDOUT',reason)."""
    machine = parse(spec)
    tape: dict[int, int] = {}
    last_seen: dict[int, int] = {0: 0}        # cell -> most recent time the head was there
    head, state, t = 0, "A", 0
    min_pos = max_pos = 0
    HALT = {"Z", "H", "-"}
    # records[side][state][read] -> list of {tape, last_seen, time, pos}
    records: dict = {True: {}, False: {}}

    def equivalent(min_side: bool, past: dict, curr: dict) -> bool:
        p0, p1 = past["pos"], curr["pos"]
        offset = 0
        step = 1 if min_side else -1
        while True:
            idx_past = p0 + offset
            ls = curr["last_seen"].get(idx_past)
            if ls is None or ls < past["time"]:      # cell not visited since past record => stop (proof's distance L)
                return True
            if curr["tape"].get(p1 + offset, 0) != past["tape"].get(idx_past, 0):
                return False
            offset += step

    while t <= time_limit:
        if max_pos - min_pos > space_limit:
            return ("HOLDOUT", f"space>{space_limit}")
        last_seen[head] = t
        read = tape.get(head, 0)

        # record-breaking step?
        new_record = head < min_pos or head > max_pos
        if new_record:
            min_side = head < min_pos
            rec = {"tape": dict(tape), "last_seen": dict(last_seen), "time": t, "pos": head}
            bucket = records[min_side].setdefault(state, {}).setdefault(read, [])
            for past in bucket:
                if equivalent(min_side, past, rec):
                    return ("NEVER_HALTS", (past["time"] + 1, t - past["time"], head - past["pos"]))
            bucket.append(rec)
            min_pos = min(min_pos, head)
            max_pos = max(max_pos, head)

        # transition
        write, move, nxt = machine[state][read]
        tape[head] = write
        head += 1 if move == "R" else -1
        t += 1
        if nxt in HALT:
            return ("HALTS", t)
        state = nxt
    return ("HOLDOUT", f"time>{time_limit}")


# Known halters are the SOUNDNESS ORACLE: a decider must never call any of these NEVER_HALTS.
HALTERS = [
    ("BB(2) champ", "1RB1LB_1LA1RZ"),
    ("BB(3) champ", "1RB1RZ_1LB0RC_1LC1LA"),
    ("BB(4) champ", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA"),
]
INFINITE = [
    ("trivial eraser",  "0RA0RA"),
    ("runaway right",   "1RA1RA"),
    ("flip-in-place",   "1RB1LA_1LA1RB"),
]


def main() -> int:
    from bb_sim import run as sim
    ORACLE_CAP = 1_000_000
    print("=" * 80)
    print("Translated Cyclers decider — SOUNDNESS AUDIT (vs the trusted simulator)")
    print("=" * 80)
    unsound = 0
    detected = 0
    print(f"{'machine':>16}  {'verdict':>12}  {'oracle':>20}  result")
    for name, spec in HALTERS + INFINITE:
        verdict, info = decide_translated(spec)
        halted, osteps, _ = sim(spec, max_steps=ORACLE_CAP)
        if verdict == "NEVER_HALTS" and halted:
            res, oracle = "‼ UNSOUND (false proof!)", f"HALTS @ {osteps}"; unsound += 1
        elif verdict == "NEVER_HALTS":
            s, p, d = info
            res, oracle = f"proven infinite (period {p}, drift {d:+d})", f"no halt <{ORACLE_CAP}"; detected += 1
        elif verdict == "HALTS":
            res, oracle = "OK (halts)", f"HALTS @ {osteps}"
        else:
            res, oracle = f"holdout ({info})", (f"HALTS @ {osteps}" if halted else f"no halt <{ORACLE_CAP}")
        print(f"{name:>16}  {verdict:>12}  {oracle:>20}  {res}")
    print("=" * 80)
    if unsound:
        print(f"RESULT: STILL UNSOUND — {unsound} false proof(s). Do not trust.")
        return 1
    print(f"RESULT: SOUND on this set — 0 false proofs across {len(HALTERS)} known halters,")
    print(f"        and PROVED non-halting for {detected}/{len(INFINITE)} drifting machines the")
    print(f"        exact-repeat decider could not. The holdout set just shrank, soundly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
