#!/usr/bin/env python
"""
Antihydra — meet the BB(6) cryptid. A 6-state machine whose halting is open (Collatz-hard).

Machine (bbchallenge): 1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA   ('---' = halt)

Its abstract soul: iterate the Hydra map  h <- floor(3h/2)  from h=8, keeping a counter c that
gets +2 on each EVEN h and -1 on each ODD h. The machine HALTS iff c ever reaches -1 (i.e. odds
ever exceed twice the evens). Whether that happens is equivalent to an open parity question about
floor(x*(3/2)^n) (Mahler's 3/2 problem) — currently UNDECIDED. Heuristics say it (almost surely)
runs forever, but no one can prove it.

Two views:
  (A) run the actual Turing machine and confirm it doesn't halt early (it really is doing the arithmetic);
  (B) simulate the abstract Hydra process for millions of iterations and WATCH the counter — see it
      drift upward and never return to -1 (the visceral 'why it probviously runs forever').
"""
from __future__ import annotations

SPEC = "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"


def run_tm(spec, max_steps):
    """Robust runner: a transition is HALT if its 3 chars aren't a normal write/move/state."""
    groups = spec.split("_")
    M = {}
    for i, g in enumerate(groups):
        st = chr(ord("A") + i)
        M[st] = {}
        for sym in (0, 1):
            t = g[sym * 3: sym * 3 + 3]
            M[st][sym] = None if (t[0] not in "01") else (int(t[0]), t[1], t[2])
    tape, head, state, steps = {}, 0, "A", 0
    lo = hi = 0
    while steps < max_steps:
        lo, hi = min(lo, head), max(hi, head)
        t = M[state][tape.get(head, 0)]
        if t is None:
            return ("HALTS", steps, hi - lo)
        w, mv, nxt = t
        tape[head] = w
        head += 1 if mv == "R" else -1
        steps += 1
        state = nxt
    return ("RUN", steps, hi - lo)


def run_hydra(max_iters, checkpoints=()):
    """The abstract soul: h<-floor(3h/2) from 8; c +=2 if h even, -=1 if h odd; halt iff c==-1.
    (h is tracked as an exact bigint — only its parity matters, but parity needs the full number.)"""
    h, c = 8, 0
    evens = odds = 0
    min_c = c
    traj = {}
    cps = set(checkpoints)
    for k in range(1, max_iters + 1):
        if h % 2 == 0:
            c += 2; evens += 1
        else:
            c -= 1; odds += 1
        min_c = min(min_c, c)
        if c == -1:
            return ("HALTS", k, c, min_c, evens, odds, h, traj)
        if k in cps:
            digits = int(h.bit_length() * 0.30103) + 1   # avoid str(h) (huge-int guard)
            traj[k] = (c, digits)
        h = h + h // 2                       # floor(3h/2)
    return ("RUN", max_iters, c, min_c, evens, odds, h, traj)


def main() -> int:
    print("=" * 74)
    print("ANTIHYDRA — the BB(6) cryptid (halting OPEN, Collatz-hard)")
    print("=" * 74)

    print("\n(A) The actual Turing machine, run 1,000,000 steps:")
    status, steps, width = run_tm(SPEC, 1_000_000)
    print(f"    -> {status} after {steps:,} steps, tape width {width}")
    print(f"    (it's grinding through the arithmetic; no halt — as expected)")

    N = 100_000
    cps = [1_000, 10_000, 50_000, 100_000]
    print(f"\n(B) The abstract Hydra soul, {N:,} iterations of h<-floor(3h/2):")
    status, k, c, min_c, ev, od, h, traj = run_hydra(N, cps)
    print(f"    counter c trajectory (halt would need c to ever touch -1):")
    for cp in cps:
        if cp in traj:
            cc, dig = traj[cp]
            print(f"        after {cp:>7,} iters:  c = {cc:>8,}   (h is a {dig:,}-digit number)")
    print(f"    -> {status} after {k:,} iterations")
    print(f"    lowest c EVER reached = {min_c}   (started 0; needs to hit -1 to halt)")
    print(f"    evens {ev:,}  odds {od:,}   ratio odd/even = {od/ev:.4f}  (halt needs > 2.0)")

    print("\n" + "=" * 74)
    print("Reading: each EVEN gives c+2, each ODD c-1. Parity is ~50/50, so c drifts UP by ~+0.5")
    print("per step and marches away from -1. To halt, odds must outrun evens 2-to-1 for a sustained")
    print("stretch — a random-walk excursion whose probability is astronomically tiny (the wiki:")
    print("< ((sqrt5-1)/2)^237 from the current state). So it 'probviously' runs forever — but that")
    print("is a HEURISTIC. Proving it is equivalent to an open problem (Mahler's 3/2). No one has.")
    print("THIS is a BB(6) cryptid: a 6-state toy whose fate hides behind unsolved number theory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
