# BB(6) attack roadmap — solve the cryptids one at a time (2026-06-24)

**Strategy.** BB(6) as a whole is impregnable (its exact value is gated behind every cryptid, each a
Mahler/Collatz/Erdős-class open problem — see `antihydra_attack.md`, `CRYPTID_REDUCTIONS.md`,
`CRYPTID_CENSUS.md`). So we do NOT attack BB(6) whole. We attack the **individual cryptid problems one at a
time**, via a fixed pipeline, building toward a complete catalogue and a possible single decision.

**Two kinds of progress count (be honest which one each result is):**
- **(R) Reduction** — turn a cryptid into its *exact named number-theory problem* (the §3c method).
  Achievable, discrete, completable. Yields the catalogue "BB(6) open core = these named problems."
- **(P) Partial / decision** — unconditional progress on a reduced problem, or an actual sound decision.
  Frontier; may not crack. A *decision* requires a machine-checked certificate (`far_dfa.verify` etc.).

---

## The per-cryptid pipeline (run this for each machine)
1. **Reverse-engineer the mechanism** against the *raw TM* (`bb_sim.py`): tape invariant, the recurring
   milestone (head extreme + state), the integer parameter(s) it iterates. Hand-pick the milestone if the
   auto-extractor (`cryptid_map.py`) finds the wrong event (the slow-width machines need this).
2. **Derive the exact integer-orbit map** `v -> f(v)` and **verify it reproduces the orbit** for ≥20
   milestones against the raw TM. (Distinguish: clean scalar map / nested / odometer / no clean map.)
3. **State the exact halting criterion** as an arithmetic statement (the §3c form: `v2`/2-adic depth, a
   base-3 digit event, a balance/density condition, …). Verify it on the simulated orbit.
4. **Identify the named problem + literature check** (Mahler p/q distribution; Erdős ternary digits of
   2^n; Collatz-like; etc.). Use WebSearch; cite precisely; note unconditional vs conditional.
5. **Attack the reduced problem** with the toolkit: depth ceiling, the Φ-potential / renewal structure,
   the carry/anti-concentration framing, applicable theorems. Honestly locate the irreducible open core.
6. **Record** (one note per machine): the verified reduction, the exact open statement, the dead ends.
   SOUNDNESS GATE: no "decided" without a verified certificate; label everything PROVEN/CONDITIONAL/OPEN;
   cross-check identities against the raw TM (the SOUNDNESS_INCIDENT discipline — we caught our own §4c error).

---

## Work queue (prioritised)

### Tier 0 — DONE (5 core machines reduced)
Antihydra (Mahler 3/2, the full §4 analysis), o10 (nested Mahler-3/2 + irregular refill), o15 & o18
(Mahler 8/3 = Erdős ternary family), o17 (base-3 carrying odometer). See `CRYPTID_REDUCTIONS.md`.

### Tier 1 — REDUCE the 14 unreduced cryptids (the bulk of "one by one"; achievable, catalogue-building)
The slow-width majority — confirmed genuinely hard (all HOLDOUT under generous deciders) but **not yet
reduced to a named problem**. Do these one per session, hand-picking the milestone:
`Space Needle, o2, o3, o4, o5, o7, o8, o11, o12, o13, o14, o16` (+ re-examine `BB6 champion`, `Lucy`).
**Deliverable per machine:** its exact arithmetic halting criterion + which number-theory family it joins
(does the catalogue stay {Mahler 3/2, Erdős ternary} or grow new families?).
**Order:** start with the few-milestone ones (`o5`(18), `o7`(28), `o8`(34)) — fastest to reverse-engineer —
then the high-milestone ones.

### Tier 2 — TRIAGE for the single most attackable problem
Once all 19 are reduced, rank by literature proximity × cleanliness × problems-cleared. Current best
candidate: **o15/o18 (Erdős ternary-digits-of-2^n)** — a named 1979 problem with published partials
(Narkiewicz upper bound) and an existing BB reduction (Stérin–Woods, arXiv:2107.12475). Focus deep
unconditional effort there (or wherever Tier 1 reveals an easier family).

### Tier 3 — THE PRIZE: an unconditional resolution of ONE cryptid
= deciding a real BB(6) holdout = a genuine contribution. Requires a number-theory breakthrough on a
reduced problem (frontier). Any partial unconditional bound (e.g. `depth = o(n)` for one machine, or a
one-sided density bound) is real progress short of the full prize.

---

## Definition of "done" for the program
- **Catalogue complete (Tier 1):** all 19 cryptids reduced to explicit named open problems — a novel,
  finishable artifact even if none is solved.
- **Each reduced problem mapped (Tier 2):** for each, the precise open statement + why current tools fall
  short (the §4b/§4g-style regime analysis).
- **Stretch (Tier 3):** crack the most tractable one.

**Next concrete action:** Tier 1, machine `o5` (`1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB`) — fewest
milestones, fastest to reverse-engineer. Run the per-cryptid pipeline; produce `o5`'s exact reduction.
