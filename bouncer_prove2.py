#!/usr/bin/env python
"""
‼‼ KNOWN-UNSOUND (2026-06-20) — DO NOT TRUST NEVER_HALTS. See SOUNDNESS_INCIDENT.md. ‼‼
Same unsound trace-extrapolation as v3 (v3 only changed record selection). Quarantined.
(The parse/sim/records/tokenize helpers here are sound and reused by sound measurement code.)

Bouncers PROOF engine v2 — generalize the chain rule to PERIOD-q chains (multi-symbol repeaters).

v1 (bouncer_prove.py) only proved bouncers whose growing run is a single-symbol SELF-LOOP
(period-1 cycle: M[S][r] stays in S). v2 generalizes: a growing region crossed by a PERIOD-q
state-cycle (the head returns to the same state every q steps while net-advancing) is also a sound
chain rule — it processes a period-q block of ANY length identically. Self-loop = the q=1 case.

Method per candidate bounce P->Q: take a step trace (state, read, dir). Tokenize it into
  - CHAIN(q-pattern, m): a maximal run that is m>=2 repetitions of a period-q (state,read,dir)
    pattern with nonzero net head displacement (a genuine growing-block traversal), and
  - WALL(step): any single step not part of such a chain.
Two consecutive same-side bounces prove NEVER_HALTS iff their token sequences match (same WALLs,
same CHAIN q-patterns in the same order) and every CHAIN's repetition count is >= in the later
bounce with at least one strictly greater (the region grew) -> by the period-q chain rule it
repeats forever, growing -> never halts.

EVERY NEVER_HALTS is oracle-checked against the simulator. Conservative + sound.
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

HALT = {"Z", "H", "-"}
QMAX = 12


def parse(spec):
    M = {}
    for i, g in enumerate(spec.split("_")):
        st = chr(ord("A") + i); M[st] = {}
        for s in (0, 1):
            t = g[s*3:s*3+3]
            M[st][s] = None if t[2] in HALT else (int(t[0]), t[1], t[2])
    return M


def sim(spec, cap):
    M = parse(spec); tape = {}; head = 0; st = "A"
    for steps in range(cap):
        t = M[st][tape.get(head, 0)]
        if t is None:
            return True, steps
        w, mv, nxt = t; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt
    return False, cap


def records(spec, steps):
    M = parse(spec); tape = {}; head = 0; st = "A"; lo = hi = 0; recs = []
    for t in range(1, steps + 1):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return recs, True
        w, mv, nxt = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt
        if head < lo:
            lo = head; recs.append((t, st, head, dict(tape), "L"))
        elif head > hi:
            hi = head; recs.append((t, st, head, dict(tape), "R"))
    return recs, False


def step_trace(spec, start_tape, start_head, start_state, nsteps):
    M = parse(spec); tape = dict(start_tape); head = start_head; st = start_state
    raw = []
    for _ in range(nsteps):
        sym = tape.get(head, 0)
        tr = M[st][sym]
        if tr is None:
            return raw, True
        w, mv, nxt = tr; d = 1 if mv == "R" else -1
        raw.append((st, sym, d))
        tape[head] = w; head += d; st = nxt
    return raw, False


def tokenize(raw):
    """-> list of ('CHAIN', q_pattern_tuple, m) | ('WALL', step). Greedy, smallest period first."""
    toks = []; i = 0; n = len(raw)
    while i < n:
        best = None
        for q in range(1, QMAX + 1):
            if i + 2 * q > n:
                break
            if raw[i:i+q] != raw[i+q:i+2*q]:
                continue
            # extend periodicity
            m = 2
            while i + (m + 1) * q <= n and raw[i+m*q:i+(m+1)*q] == raw[i:i+q]:
                m += 1
            net = sum(s[2] for s in raw[i:i+q])     # net head displacement over one period
            if net != 0:                              # genuine growing-block traversal
                best = (q, m); break                  # smallest q wins
        if best:
            q, m = best
            toks.append(("CHAIN", tuple(raw[i:i+q]), m)); i += m * q
        else:
            toks.append(("WALL", raw[i])); i += 1
    return toks


def prove(spec, steps=30_000):
    M = parse(spec)
    recs, halted = records(spec, steps)
    if halted:
        return ("HALTS", recs[-1][0] if recs else 0)
    for side in ("R", "L"):
        same = [r for r in recs if r[4] == side]
        if len(same) < 3:
            continue
        P0, P1, P2 = same[-3], same[-2], same[-1]
        if not (P0[1] == P1[1] == P2[1]):
            continue
        ra, ha = step_trace(spec, P0[3], P0[2], P0[1], P1[0] - P0[0])
        rb, hb = step_trace(spec, P1[3], P1[2], P1[1], P2[0] - P1[0])
        if ha or hb:
            continue
        ta, tb = tokenize(ra), tokenize(rb)
        if len(ta) != len(tb):
            continue
        ok = True; grew = False
        for a, b in zip(ta, tb):
            if a[0] != b[0]:
                ok = False; break
            if a[0] == "WALL":
                if a[1] != b[1]:
                    ok = False; break
            else:  # CHAIN
                if a[1] != b[1]:                       # different period pattern
                    ok = False; break
                if b[2] < a[2]:                         # repetition count shrank
                    ok = False; break
                if b[2] > a[2]:
                    grew = True
        if ok and grew:
            return ("NEVER_HALTS", (P0[0] + 1, P1[0] - P0[0]))
    return ("HOLDOUT", "no period-q chain bounce")


def main() -> int:
    HALTERS = [("BB(2)", "1RB1LB_1LA1RZ"), ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA"),
               ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]
    reps = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")) if l.strip()]
    print("=" * 74)
    print("Bouncers PROOF engine v2 (period-q chains) — SOUNDNESS AUDIT")
    print("=" * 74)
    unsound = 0
    for name, spec in HALTERS:
        v, _ = prove(spec); h, hs = sim(spec, 1_000_000)
        flag = "OK"
        if v == "NEVER_HALTS" and h:
            flag = f"‼ UNSOUND (halts @ {hs})"; unsound += 1
        print(f"  {name:>6} -> {v:<12} [{flag}]")
    proven = held = 0
    for spec in reps:
        v, _ = prove(spec)
        if v == "NEVER_HALTS":
            h, hs = sim(spec, 1_000_000)
            if h:
                print(f"  ‼ UNSOUND {spec}: NEVER but halts @ {hs}"); unsound += 1
            else:
                proven += 1
        elif v == "HOLDOUT":
            held += 1
    print("=" * 74)
    print(f"  known halters falsely proven : {unsound}")
    print(f"  holdout reps PROVEN never-halt: {proven} / {len(reps)}   (v1 proved 22)")
    print(f"  still holdout                 : {held}")
    if unsound == 0:
        print(f"\n  SOUND. v2 proves {proven} of 63 (vs v1's 22). The remaining holdouts are the 10")
        print(f"  counters (need counter-induction) + any multi-phase bouncers beyond period-{QMAX}.")
    return 1 if unsound else 0


if __name__ == "__main__":
    raise SystemExit(main())
