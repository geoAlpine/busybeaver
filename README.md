# Busy Beaver — a high mountain that also gives clean wins

**Yosuke Aoki** — GeoAlpine LLC — started 2026-06-19 (evening, one shochu in)

## Why this mountain

The criteria, after a day of searching for the right "high mountain":
- **Grand** (the kind that keeps you up at night): BB(n) is the halting problem / Gödel made
  into a number — it grows faster than any computable function. The edge of the knowable.
- **Solvable solo, zero budget**: needs only a clever head and an ordinary computer.
- **Clean, verifiable wins** (the "解けた！" we actually want): each stubborn machine you
  prove halts-or-runs-forever is a definitive, machine-checkable result.
- **Uncrowded frontier**: the *concept* is famous (Aaronson's "Who Can Name the Bigger
  Number?"; the 2024 BB(5) proof made the news), but the working frontier (deciding BB(6)
  holdouts) is a small, collaborative, *under-staffed* community (bbchallenge.org).
- **Fits this exact mind**: big numbers (loved), discrete math (crypto/lattice muscle),
  and — crucially — "certify an infinite property from finite observation" is the SAME
  instinct as the quantum genuineness limit theorem. Deciding halting *is* a verification
  problem.

## The state of the art (why now is a good time)
- BB(1)=1, BB(2)=6, BB(3)=21, BB(4)=107.
- **BB(5) = 47,176,870** — conjectured since ~1989, **PROVEN in July 2024** by the
  bbchallenge community (Coq-verified).
- **BB(6) is open** and astronomically large; some 6-state holdouts are tied to Collatz-like
  problems. Far enough out, BB(n) becomes independent of ZFC (math itself can't prove it).

## What's here (built & verified tonight)
- `bb_sim.py` — Turing-machine simulator, standard bbchallenge text format. **Verified**:
  reproduces BB(2)=6, BB(3)=21, BB(4)=107, and the **BB(5) champion to the exact step:
  47,176,870 steps / 4098 ones** (matches the 2024 world result — double-checks both the
  simulator and the table).
- `decider.py` — a first non-halting prover. Sorts machines into **HALTS / NEVER_HALTS
  (proven, by exact configuration repeat) / HOLDOUT**. Honest known limitation: the naive
  `normalize()` is quadratic on drifting machines (hit it the hard way — a runaway machine
  hung), and it only catches *stationary* cyclers; *translated* cyclers (that drift while
  repeating) are holdouts here.

Run (no dependencies; Python 3.11):
```
/opt/homebrew/bin/python3.11 busybeaver/bb_sim.py
/opt/homebrew/bin/python3.11 busybeaver/decider.py
```

## The actual frontier work (next steps)
The game is: **shrink the holdout set, one decider at a time, toward BB(6).**
1. **Incremental config / faster sim** — kill the quadratic normalize; use a relative,
   O(1)-per-step configuration so deciders run on real machine counts.
2. **A translated-cycle decider** — catch drifters like `1RA1RA` (the most common holdout
   class after stationary cyclers). This alone settles a large fraction of machines.
3. **Plug into bbchallenge** — get the BB(5)/BB(6) machine database and the standard format,
   run our deciders against the real holdout lists, and see what's actually open.
4. **Adopt the strong deciders** the community uses (Closed Tape Language, etc.), then look
   for an individual BB(6) holdout to attack by hand — the "crack a stubborn machine" win.

The through-line: this is the same "what can be certified from finite observation" muscle as
the quantum genuineness framework — pointed at the limits of computation itself.
