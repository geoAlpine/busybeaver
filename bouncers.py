#!/usr/bin/env python
"""
Bouncers decider — STEP 1: sound DETECTION (no halting claim yet).

A bouncer reaches its growth configuration C(n) after a + b*n + c*n^2 steps (quadratic time)
while its tape grows linearly. Operationally: each time the head reaches a NEW extreme position
(a "record"), the TIME since the previous record grows ~linearly, so successive record-times have
~constant SECOND difference (the signature of quadratic growth), and the span grows ~linearly per
record. This module DETECTS that structure and extracts the per-record growth — soundly, because
detection only MEASURES; it makes no non-halting claim.

The PROOF step (build the wall/repeater rule list, chain-rule the repeaters, close the induction
C(n)->C(n+1) — Iijil1/Bouncers, arXiv 2504.20563 Sec.7) is the NEXT, careful, oracle-gated build.
We deliberately do NOT ship an unsound proof here (lesson of the night).
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


def records(spec, steps):
    """Return list of (time, extreme_position, side, span) at each new leftmost/rightmost record."""
    M = parse(spec)
    tape = {}; head = 0; st = "A"; lo = hi = 0
    recs = []
    for t in range(1, steps + 1):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return recs, "HALT", t
        w, mv, nxt = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt
        if head < lo:
            lo = head; recs.append((t, head, "L", hi - lo))
        elif head > hi:
            hi = head; recs.append((t, head, "R", hi - lo))
    return recs, "RUN", steps


def detect_bouncer(spec, steps=30_000):
    """Sound detection: does the record structure look quadratic-time / linear-space?"""
    recs, status, n = records(spec, steps)
    if status == "HALT":
        return ("HALTS", n, {})
    # use same-side records (say the side with more records); times should have ~const 2nd diff
    for side in ("R", "L"):
        ts = [r[0] for r in recs if r[2] == side]
        if len(ts) < 6:
            continue
        ts = ts[-12:] if len(ts) > 12 else ts          # later records = settled growth
        d1 = [ts[i+1] - ts[i] for i in range(len(ts)-1)]          # gaps between records
        d2 = [d1[i+1] - d1[i] for i in range(len(d1)-1)]          # 2nd differences
        if not d2:
            continue
        avg = sum(d2) / len(d2)
        if avg == 0:
            continue
        spread = max(d2) - min(d2)
        # quadratic time  <=>  gaps grow by a ~constant amount each record (2nd diff ~ const)
        if avg > 0 and spread <= 0.5 * abs(avg) * len(d2) ** 0:    # tolerant constancy check
            consistent = max(abs(x - avg) for x in d2) <= max(2.0, 0.30 * abs(avg))
            if consistent:
                return ("BOUNCER-STRUCTURE", side, {"period_growth_per_record": round(avg, 2),
                                                    "records": len(recs)})
    return ("NO-CLEAR-STRUCTURE", None, {"records": len(recs)})


def main() -> int:
    path = os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")
    specs = [l.strip() for l in open(path) if l.strip()]
    # the 53 bouncers are the ones our classifier flagged; here just run detection on all 63 reps
    det = 0; noclear = 0; halted = 0
    rows = []
    for s in specs:
        verdict, info, extra = detect_bouncer(s)
        if verdict == "BOUNCER-STRUCTURE":
            det += 1
        elif verdict == "HALTS":
            halted += 1
        else:
            noclear += 1
        rows.append((s, verdict, info, extra))
    print("=" * 78)
    print("Bouncers decider — STEP 1: DETECTION (sound; no halting proof yet)")
    print("=" * 78)
    for s, v, info, extra in rows:
        tag = f"{v}" + (f" [{info} side]" if v == "BOUNCER-STRUCTURE" else "")
        print(f"  {s:>22}  {tag:<26}  {extra}")
    print("=" * 78)
    print(f"  bouncer-structure detected : {det}")
    print(f"  no clear structure          : {noclear}  (counters / multi-phase — different decider)")
    print(f"  halted                      : {halted}")
    print("\nSOUND so far: this only MEASURES structure (no non-halt claim). NEXT (clear head,")
    print("oracle-gated): build the wall/repeater rule list + chain rules + induction closing to")
    print("turn 'bouncer-structure' into a PROVEN 'never halts'. That is the real decider.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
