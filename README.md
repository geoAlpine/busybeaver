# Busy Beaver — a high mountain that also gives clean wins

**Yosuke Aoki** — GeoAlpine LLC — started 2026-06-19 (evening, one shochu in)

> **Current state → `STATUS.md`** (this README is the early-days log). The sound decider suite proves
> **46/63** of the three-state monsters (0 false proofs); run it with `python suite.py`. Soundness
> argument: `SOUNDNESS.md`. NOTE: the `bouncer_prove v1/v2/v3` engines described later were later found
> **UNSOUND and are quarantined** (`SOUNDNESS_INCIDENT.md`) — the real sound provers are
> `bouncer_prove_sound.py` + `wbounce.py` on the G1-validated `wsim.py`.

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

## Unmasking the 3-state holdouts (`holdout3_analyze.py`)
- The 684 holdouts collapse to **63 distinct hard behaviours** (deduped by reached-transition
  signature; the rest are replicas across irrelevant/unreached transitions). The genuinely-hard
  core is ~10% of the apparent count.
- **All 63 stay holdouts even at generous limits — they are genuinely hard, not cap-limited.**
  (Tested the hypothesis "the small-width ones are just long-period cyclers": FALSED by direct
  measurement — see below — the 6th self-correction.)
- **Two monster types** defeat the simple deciders:
  1. **Two-sided unbounded growth** — symmetric spans (e.g. [-172,173]), width grows ~linearly;
     escapes the same-side translated-cycle test.
  2. **Counters** — width ≈ log(steps): one machine measured 5→12→15→18→19 at
     10²→10³→10⁴→10⁶→2·10⁶ steps. Each carry takes ~2× the last, so the inter-record period
     keeps growing and no fixed-period cycle exists. (These look "bounded" at 30k steps but creep.)
- **This is the precise target of the next decider** (Closed Tape Language / acceleration /
  counter-aware) — and the road toward BB(6).

## Targeting the monsters: BOUNCER vs COUNTER split (`classify_monsters.py`)
Before building the (complex, must-be-sound) next decider, we measured each of the 63 distinct
monsters' width-vs-steps growth law (sound measurement, not a proof) and binned them:
- **53 BOUNCERS** — width ∝ √steps (ratio r = width(1e5)/width(1e4) clustered tightly at
  **3.16–3.19 ≈ √10**, the exact quadratic-time bouncer signature: time ∝ n², space ∝ n).
  Target of the **Bouncers decider** (Iijil1/Bouncers; arXiv 2504.20563 §7 — spec fetched).
- **10 COUNTERS** — width ∝ log(steps) (carry takes ~2× the last; exponential time).
  Target of a **counter-induction decider** (sligocki 2022).
- 0 MID, 0 cap-limited (all genuinely infinite).
So a Bouncers decider cracks 53/63 (84%); counter-induction the remaining 10. Precise targets,
zero unsound-decider risk. `holdouts3_reps.txt` holds the 63 representatives (the test set:
each must become NEVER_HALTS once the matching decider is built, gated by the known-halter oracle).

## Meeting the BB(6) cryptid: Antihydra (`antihydra.py`)
Ran the actual BB(6) cryptid `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` (halting OPEN,
Collatz-hard) on our simulator, plus its abstract "soul": iterate h←⌊3h/2⌋ from 8, counter
c +=2 (even) / −1 (odd), halt iff c=−1.
- TM: 1,000,000 steps, no halt, tape width 1383 (grinding huge-int arithmetic).
- Abstract: c climbs 497→4,862→24,961→**50,477** over 100k iters; **lowest c ever = 0** (never
  near −1); evens 50,159 / odds 49,841 (ratio 0.994; halt needs >2.0); h reaches a
  **17,610-digit** number. So c drifts ~+0.5/step away from −1 → "probviously" runs forever —
  but proving it ≡ Mahler's 3/2 problem (open). A 6-state toy whose fate hides behind unsolved
  number theory: the wall that makes BB(6) astronomically (perhaps unprovably) hard.

## "Computing BB(6)" — the two walls, and a real (tiny) lower bound (`hunt6.py`)
You can't COMPUTE BB(6): (wall 1, math) deciding it needs every 6-state machine settled,
incl. cryptids like Antihydra ≡ open problems; (wall 2, time) the known record-holders halt
after ~10↑↑15 steps — unrunnable by brute force in any physical time. But you can HUNT its
lower bound. A quick hunt of 40,000 random normalized 6-state machines (cap 300k steps):
**16,530 halted — and the LATEST halter stopped at just 67 steps**, giving the true (laughable)
bound **BB(6) ≥ 67**. The lesson is the chasm 67 vs >10↑↑15: late-halters are so rare that
random search never finds them — **records come from clever CONSTRUCTION (counter/Collatz
structure), not brute force.** (Our fast counter omits the final halt transition, so +1 vs the
standard convention; BB(4) read 106 here vs the true 107.)

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
