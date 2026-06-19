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
  (proven, by exact configuration repeat) / HOLDOUT**. **SOUND but weak**: only catches
  *stationary* cyclers (exact config repeat). Honest limitation: the naive `normalize()` is
  quadratic on drifting machines (hit it the hard way — a runaway machine hung).
- `lin_decider.py` — an ATTEMPT at a Lin-Rado *translated*-cycle decider (to catch drifters
  like `1RA1RA`). **KNOWN-UNSOUND — DO NOT TRUST its NEVER_HALTS verdicts.** Two reconstructed
  formulations of the tape-comparison condition BOTH falsely "proved" non-halting for machines
  that demonstrably halt (BB(4)@107, BB(5)@47M). Caught by the built-in **soundness audit**
  that cross-checks every NEVER_HALTS claim against the trusted simulator (the known-halter
  oracle). Kept as a documented failed attempt + a self-auditing harness. The correct Lin
  recurrence condition is subtler than reconstructable from memory — it must be implemented
  against the published spec / a Coq-verified reference and gated by this oracle.
  **Lesson (the 5th and sharpest self-correction of the day): a decider that emits a false
  proof is the cardinal sin; we refused to trust a "win" that the oracle flagged — which is
  exactly why the 2024 BB(5) result is a *machine-checked* proof, not a hand-wave.**
- `translated_cyclers.py` — **the SOUND translated-cycle decider** (supersedes the unsound
  `lin_decider.py`). A faithful port of the bbchallenge S(5)-gated reference
  (`bbchallenge-deciders/decider-translated-cyclers`): the **record method** — snapshot only
  at new leftmost/rightmost positions; bucket by (side, state, read); two records are
  equivalent iff, walking from the head into the explored region, the tapes agree
  head-relative (`now[p1+offset] == past[p0+offset]`) over exactly the cells visited since the
  past record's time (the proof's "distance L"). **Verified SOUND by the built-in audit: 0
  false proofs across the known halters (BB(2)/BB(3)/BB(4)), and it PROVES non-halting for the
  drifters the exact-repeat decider couldn't — including `1RA1RA`, the very machine we falsely
  "proved" then caught.** This is the earned win: failed twice from memory → caught it with the
  oracle → fetched the authoritative spec → implemented faithfully → gated until sound. The
  holdout set genuinely shrank. (`flip-in-place` remains a holdout: neither stationary nor
  translated cycling — the next escalation rung.)

Run (no dependencies; Python 3.11):
```
/opt/homebrew/bin/python3.11 busybeaver/bb_sim.py
/opt/homebrew/bin/python3.11 busybeaver/decider.py
```

## Closing a whole class: the 2-state universe (the real method, at scale 2)
- `enumerate2.py` — enumerate ALL 20,736 two-state machines and classify each with the sound
  tools (trivial no-halt-state check → simulator → exact-repeat → translated-cycle).
  **Result: HALTS 9,784 (max = 6 = BB(2), reproduced from scratch by deciding every machine),
  NEVER_HALTS 10,952, HOLDOUT 0 — the class is fully closed.**
- `holdout_probe.py` — the frontier move that got us there. A first pass left **12 holdouts**;
  probing showed all 12 share one trait: **no halt transition at all** (`Z` absent), and they
  resist exact-repeat AND translated-cycle even at generous limits (their infinite behaviour is
  neither). The missing decider was the *simplest* one — "no halt state ⇒ never halts" — not a
  fancier one. Lesson: enumerate the trivial cases; a holdout can be a forgotten triviality, not
  a hard problem. Adding it closed the universe (0 holdouts).

## Scaling up: the 3-state universe (the difficulty wall, seen firsthand)
- `enumerate3.py` — all 16^5 = 1,048,576 normalized (A0=1RB) three-state machines, classified.
  **Result: HALTS 471,236 (max = 21 = BB(3), reproduced), NEVER_HALTS 576,656, HOLDOUT 684.**
  Champion `1RB0LZ_1LB0RC_1LC1LA`.
- **The key observation (the difficulty wall):** at n=2 the simple deciders close the class
  (0 holdouts); at n=3 they leave **684 holdouts** — a small but nonzero stubborn residual the
  trivial + exact-repeat + translated-cycle deciders cannot settle. This is, in miniature, why
  BB(5) took until 2024 and BB(6) is open: each added state spawns behaviours that resist simple
  cycle arguments. The holdout sample all share the prefix `1RB0LB_1LA0RA_…` (state C never
  reached) — i.e. the 684 are a handful of distinct hard behaviours replicated across irrelevant
  C-transitions. The genuinely-hard core is small; that's where stronger deciders / hand-analysis
  go next.

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
