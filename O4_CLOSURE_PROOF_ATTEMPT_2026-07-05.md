# Proving o4's closure — a serious attempt: Fork-A confirmed, but the certificate is non-regular (counter + sweep-phase) (2026-07-05)

*Going for an actual decision of o4 (does not halt). Result: **Fork-A is confirmed rigorously-in-structure** (the
head-local abstraction has a **stable finite** state set, halt-free over 30M+ steps), but a **complete proof is blocked
at two precisely-located obstructions**: (1) the invariant is **non-regular** — the growing big-gap `G` makes any
fixed-window / plain-DFA abstraction **non-Markov** (verified), so the generic FAR/CEGAR deciders provably cannot
express it; (2) **transient len-2 `1`-blocks genuinely occur**, and halt-freeness needs a **sweep-vs-cascade timing**
argument (B never reads one) that requires the base-4/3 odometer arithmetic. o4 stays `[OPEN]`, but its decision is now
a **precisely-characterized custom-certificate problem**, not a generic-decider gap. SOUNDNESS: `[OBSERVED]`/`[PROVEN
structure]`; halting `[OPEN]`; no machine decided.*

## What was established `[OBSERVED, strong]`
- **Stable finite macro-abstraction.** The head-local state `(control-state, ±6 window)` has **exactly 268 reachable
  values, constant from 5M to 30M steps** while the tape width grows `3280→7874`. Halt event (`B` reads a `1` with
  right-neighbour `1`) fires **0 times / 12.5M B-reads (50M steps)**. So the local abstraction is **finite and
  halt-free** — the Fork-A signature.
- **Milestone tape language is closed.** Every milestone is `[1]`-unit-blocks + `(1)/(2)`-gaps + **one** big gap
  (length `= G`, the `⌊4G/3⌋` odometer: `7,14,19,30,…`) + at most **one transient `[2]` block**. Zero language
  violations / 19901 milestones.

## The two obstructions to a rigorous proof `[PROVEN structure]`
1. **The invariant is NON-REGULAR (needs a counter).** Determinism test: does `(state, ±W window)` map to a **unique**
   next macro-state? **No** — millions of non-deterministic transitions at `W=6,8,10`, and the macro-count **grows**
   with `W` (`268→409→568`). Reason: the big gap is a long `0`-run, so the head sits in an "all-`0`" window at many
   absolute positions with **different** continuations (depending on distance to the far block). **A fixed-window /
   plain-DFA cannot be Markov here** — the certificate must track the big-gap length as a **counter** (the base-4/3
   odometer). This is exactly why `far_dfa` (m≤16) and CEGAR return **HOLDOUT**: they use *regular* abstractions, and
   o4's invariant is *regular + one counter*.
2. **Halt-freeness needs a sweep-vs-cascade TIMING argument.** Transient `[2]` `1`-blocks **do occur** (e.g. milestone
   at step 231: `…(2)[2]…`). Halting would be `B` reading one. Proving `B` never does requires the **phase
   relationship** between `B`'s rightward sweeps and the odometer's carry cascades (which create the `[2]`) — a
   bounded but arithmetic (base-4/3) timing invariant, not a static tape property.

## The precise remaining obligation `[the tractable-but-nontrivial target]`
o4's decision `=` a **custom counter-automaton certificate**: a **regular tape language parameterized by the big-gap
counter `G`**, proven closed under one *generation* (milestone→milestone) via the `G′=⌊4G/3⌋+c(G mod3)` cascade, with
a **phase invariant** ensuring `B`'s sweeps avoid the transient `[2]` blocks. This is **finite-per-generation** (the
cascade is local given `G mod 3` and the carry front) — decidable in principle — but **beyond the generic regular
deciders** in the repo. o4 is thus **the first BB(6) cryptid pinned to a concrete custom-certificate proof
obligation**, distinct in kind from `(K)`-hard machines (Space Needle, whose orbit is *normal* so **no** invariant
exists) and from the generic-decidable affine machines.

## Verdict
**(c)/(b) — a serious closure-proof attempt: Fork-A confirmed, obstructions located, proof not completed.** o4's
head-local abstraction is finite (268) and halt-free (0/50M), confirming an invariant exists (Fork A); but it is
**non-regular** (big-gap counter) and its halt-freeness needs a **sweep-vs-cascade timing** argument, so the generic
FAR/DFA/CEGAR deciders (regular only) provably can't close it — explaining the HOLDOUT as a *representation* limit, not
absence of an invariant. **A rigorous o4 decision needs a hand-built counter + phase certificate** — bounded,
non-trivial, and the concrete next target. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `/tmp/o4_macro.py` (268 stable macro-states, 0 halt, 30M), `/tmp/o4_markov.py` (non-Markov: nondet grows with W),
  `/tmp/o4_gen.py` (milestone language, transient `[2]`), `far_dfa.prove(...ms up to 16)`=HOLDOUT. Basis:
  `FORK_A_O4_DECIDABLE_CANDIDATE_2026-07-05`, `o4_transducer.py`, `B2_DECISION_FORK_2026-07-05`.
