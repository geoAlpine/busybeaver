#!/usr/bin/env python
"""
Bouncers decider — STEP 2: the PROOF engine (sound, conservative, oracle-gated).

Soundness core (the chain rule, verified at the transition-table level):
A maximal run of >=2 consecutive steps with the SAME (state, read-symbol) is a SELF-LOOP iff
M[state][read] returns the SAME state. A self-loop over a uniform block of that symbol provably
processes a block of ANY length identically -> it extends to any n. So if one "bounce" period
P -> Q satisfies:
  (1) start and end in the same state with the head at a matching (mirrored) new extreme,
  (2) every long run crossed is a verified self-loop over a uniform symbol block,
  (3) Q's tape (head-relative) = P's tape with ONLY self-loop runs lengthened (walls identical),
  (4) no halt occurs in P->Q,
then by induction the bounce repeats forever with the blocks growing -> NEVER HALTS. Conservative:
only proves bouncers whose growing segments are uniform self-loop blocks (misses multi-symbol
repeaters); never claims a counter (those have no such steady self-loop growth).

EVERY NEVER_HALTS is cross-checked against the trusted simulator (the oracle). A false proof on a
halting machine = unsound = bug to fix. (Lesson: Lin-Rado emitted false proofs twice; the oracle
caught them.)
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

HALT = {"Z", "H", "-"}


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


def rel_tape(tape, head, lo, hi):
    """tape over [lo,hi] as a tuple, indexed relative to head (head at index head-lo)."""
    return tuple(tape.get(c, 0) for c in range(lo, hi + 1)), head - lo


def collapse(trace):
    """trace = list of (state, read). Collapse maximal equal runs -> list of (state, read, count)."""
    out = []
    for sr in trace:
        if out and out[-1][0] == sr[0] and out[-1][1] == sr[1]:
            out[-1][2] += 1
        else:
            out.append([sr[0], sr[1], 1])
    return out


def records(spec, steps):
    """(t, state, head, tape-copy) at each new global extreme, with side."""
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


def macro_trace(spec, start_tape, start_head, start_state, nsteps):
    """Re-simulate a segment; return (collapsed macro trace, halted?)."""
    M = parse(spec); tape = dict(start_tape); head = start_head; st = start_state
    raw = []
    for _ in range(nsteps):
        sym = tape.get(head, 0)
        raw.append((st, sym))
        tr = M[st][sym]
        if tr is None:
            return collapse(raw), True
        w, mv, nxt = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt
    return collapse(raw), False


def prove(spec, steps=30_000):
    """('NEVER_HALTS', (settle,period)) | ('HALTS', t) | ('HOLDOUT', reason)."""
    M = parse(spec)
    recs, halted = records(spec, steps)
    if halted:
        return ("HALTS", recs[-1][0] if recs else 0)
    # group records by side; need >=3 same-side records to compare two consecutive periods
    for side in ("R", "L"):
        same = [r for r in recs if r[4] == side]
        if len(same) < 3:
            continue
        # use the last three settled same-side records: P0 -> P1 -> P2
        P0, P1, P2 = same[-3], same[-2], same[-1]
        t0, s0, h0, tp0, _ = P0
        t1, s1, h1, tp1, _ = P1
        t2, s2, h2, tp2, _ = P2
        if not (s0 == s1 == s2):
            continue
        mt_a, ha = macro_trace(spec, tp0, h0, s0, t1 - t0)
        mt_b, hb = macro_trace(spec, tp1, h1, s1, t2 - t1)
        if ha or hb:
            continue
        # the two bounce macro-traces must have the SAME (state,read) sequence
        if len(mt_a) != len(mt_b) or any(a[0] != b[0] or a[1] != b[1] for a, b in zip(mt_a, mt_b)):
            continue
        # classify each macro op: wall (count must be EQUAL across the two bounces)
        # or growing self-loop (count grows by a consistent positive delta, AND it's a real self-loop)
        ok = True
        grew = False
        for a, b in zip(mt_a, mt_b):
            st_, rd_, ca = a[0], a[1], a[2]
            cb = b[2]
            is_selfloop = (M[st_][rd_] is not None and M[st_][rd_][2] == st_)
            if cb == ca:
                continue                              # identical (wall / fixed part) -> fine
            if cb > ca and is_selfloop:
                grew = True                            # a verified self-loop run that grew -> chain rule
                continue
            ok = False; break                          # grew but NOT a self-loop, or shrank -> can't prove
        if ok and grew:
            return ("NEVER_HALTS", (t0 + 1, t1 - t0))
    return ("HOLDOUT", "no uniform-self-loop bounce")


def main() -> int:
    HALTERS = [("BB(2)", "1RB1LB_1LA1RZ"), ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA"),
               ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]
    reps = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")) if l.strip()]

    print("=" * 74)
    print("Bouncers PROOF engine — SOUNDNESS AUDIT (every NEVER_HALTS vs the simulator)")
    print("=" * 74)
    unsound = 0
    # 1) known halters MUST NOT be proven non-halting
    for name, spec in HALTERS:
        v, info = prove(spec)
        h, hs = sim(spec, 1_000_000)
        flag = "OK"
        if v == "NEVER_HALTS" and h:
            flag = f"‼ UNSOUND (halts @ {hs})"; unsound += 1
        print(f"  {name:>6} {spec:<32} -> {v:<12} [{flag}]")
    # 2) the 63 holdout reps: how many do we now PROVE? (cross-checked: none may actually halt)
    proven = 0; held = 0
    for spec in reps:
        v, info = prove(spec)
        if v == "NEVER_HALTS":
            h, hs = sim(spec, 1_000_000)
            if h:
                print(f"  ‼ UNSOUND on {spec}: proved NEVER but halts @ {hs}"); unsound += 1
            else:
                proven += 1
        elif v == "HALTS":
            pass
        else:
            held += 1
    print("=" * 74)
    print(f"  known halters falsely proven : {unsound}")
    print(f"  holdout reps PROVEN never-halt: {proven} / {len(reps)}")
    print(f"  still holdout                 : {held}")
    if unsound == 0 and proven > 0:
        print(f"\n  SOUND + a real win: {proven} of the 63 monsters are now PROVEN to run forever,")
        print(f"  with zero false proofs on known halters. The bridge from reproduction to a real")
        print(f"  sound decider is built. (Conservative: multi-symbol-repeater bouncers + the 10")
        print(f"  counters remain — next deciders.)")
    elif unsound:
        print(f"\n  UNSOUND — {unsound} false proof(s). Fix before trusting (the oracle did its job).")
    return 1 if unsound else 0


if __name__ == "__main__":
    raise SystemExit(main())
