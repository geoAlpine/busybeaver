# o17 — the one live BB(6) decision target (attack foundation, 2026-06-22)

`o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt = state F reads 0).

Selected as **the candidate closest to an actual answer** (deciding a real BB(6) holdout) after the
5-machine Collatz-core comparison (`CRYPTID_REDUCTIONS.md`): four of five are Mahler-hard, but **o17 is
a carrying odometer**, structurally nearest our already-defeated counter class. This note records the
self-verified structure that upgrades o17 from "lottery" to "concrete FAR target".

## Mechanism (self-derived, verified vs the raw TM)
Transition table: `A:0→1RB 1→1LD | B:0→1RC 1→0LE | C:0→1LA 1→1RE | D:0→0LF 1→1LA | E:0→1RB 1→0RB |
F:0→HALT 1→0LB`. The tape is a string of 1-blocks separated by single 0s; it runs as a **base-3-ish
carrying odometer**: the rightmost ("active") block increments through `2,4,5,7,8,10,11,13,…` (steps
alternate +2,+1) and on overflow a carry propagates leftward, resetting via a transient `1` marker.

## The invariant (verified over 1.5–3M steps, 1711 milestones)
1. **Every interior 0-separator has length exactly 1** — a `00` gap NEVER forms. (max separator = 1.)
2. **Every settled (non-rightmost) 1-block has length ≡ 2 (mod 3)** — 346 575 samples, all ≡2; no
   block of any length is ≡0 (mod 3). The active rightmost block is ≡1 or 2 (mod 3), transiently.

## Why this is THE decision route (and conjecture-free, if it closes)
- **Halt ⟺ a `00` gap is read by D** (D:0→0LF then F reads the left cell; F reads 0 ⟺ left cell is 0 ⟺
  the separator was `00`). So **non-halt ⟸ "no `00` gap ever forms" = invariant (1).**
- Invariant (1)+(2) describe a **regular language**: "single 0-separators + 1-runs of length ≡2 (mod 3)"
  is recognised by a DFA tracking run-length mod 3 (3 phases) + separator state. This is **inside FAR's
  sound expressive class** — `far_dfa.py`'s `Invariant` base supports an arbitrary `step(state,sym)`
  DFA, not just m-grams, so mod-3 counting is expressible.
- Therefore a **sound FAR certificate may exist**: a regular over-approximation `L ⊇ reachable`, step-
  closed, halt-free (no `00` ⇒ no halt). If `far_dfa.verify(L)` passes (start∈L, succ(L)⊆L, no halt in
  L), **o17 is DECIDED, soundly** — a genuine BB(6) holdout settled (route i).

## Why FAR auto-search (`far_finder`/`far_cegar`) held out, and the plan
The k-tails / CEGAR auto-builders held out on o17 — but that is a *construction* failure, not evidence
no certificate exists. The auto-builders sample reachable configs and merge; they did not discover the
**mod-3 run-length phase** (a non-local, counting invariant — the same gap that defeated k-tails on the
parity counter, where CEGAR with the verifier's counterexamples succeeded). The plan:
1. Hand-build a DFA invariant `L` over configs encoding: 1-run phase mod 3 (settled runs must reach
   phase 2 before a separator), single 0-separators, plus the transient carry/head patterns the step
   produces (the over-approximation must include the in-flight `1`-marker and head-sweep configs).
2. Run the SOUND `far_dfa.verify(L)`. Iterate CEGAR-style on its `Invariant.witness` counterexamples
   until (S)(C)(H) all pass — or until a counterexample reveals a genuine non-regular obstruction
   (which would honestly downgrade o17 toward Mahler-hard).

## Status
- **[PROVEN, this session]** mechanism + invariants (1),(2) hold over 3M steps / 1711 milestones, cross-
  checked vs the raw TM. The reachable structure's *core* is regular.
- **[OPEN]** whether the regular core extends to a **step-closed, halt-free** DFA certificate (the carry
  transients are the risk). This is the concrete next build. **Not yet decided; no non-halt claim.**
- Soundness: any certificate must pass `far_dfa.verify` (decider-agnostic; a wrong DFA fails, never a
  false proof). Discipline per `SOUNDNESS_INCIDENT.md` — no claim before verify() passes.
