# BB(6) complete proof — the roadmap (2026-07-22)

**Scope: the BB(6) object itself** — `BB6 = championSteps` — NOT the x2 track (x2 has its own live
ledger, `ROADMAP_2026-07-19.md`, and sits on the carry-transparent side of the (K) wall; completing
x2 does not advance anything below). This document supersedes `ROADMAP_COMPLETE_PROOF_2026-07-10.md`
§5 as the BB6-track work ledger; that file remains the record of 経路 1/2/3 design rationale.

**Discipline.** Every load-bearing claim below was re-measured against source on 2026-07-22, not
taken from prose: the axiom inventory (`grep ^axiom`, 11 real + 1 docstring false-positive), the top
theorem, the `AllHoldoutsNonHalt` 18-conjunct shape, the `Machine` inductive (13 constructors), the
literal-vs-pinned status of every conjunct, and `O3.lean`'s partial coverage. Labels are strict:
**[PROVEN]** (Lean-green or machine-verified), **[OPEN]**, **[ENGINEERING]** (no new mathematics),
**[GATED]** (blocked on an owner decision, per the external policy). **No machine is decided and no
label is upgraded by this document.**

---

## 0. The gate — verified

```lean
theorem BB6_eq_championSteps (h : AllHoldoutsNonHalt) : BB6 = championSteps :=
  Nat.le_antisymm (enumeration_upper h) champion_lower
```

The theorem is deliberately content-free: pure `≤`-antisymmetry. Every difficulty is quarantined
into (a) the hypothesis `AllHoldoutsNonHalt` — an 18-way conjunction (17 named cryptids + the
~1087-holdout residual) — and (b) the two enumeration-bridge axioms. This is 経路 3 by design: the
regime where BB(6) is determined the instant the holdouts fall. **The roadmap to BB(6) complete is
exactly: discharge the 11 axioms of `lean/Completion.lean`.**

## 1. The 11-axiom discharge map — verified inventory

| # | axiom | class | what discharges it |
|---|---|---|---|
| 1 | `o4_ledger : o4_ledger_conjecture` | **[OPEN] math** | the ×4/3 a-ledger bound `∀n, 1 ≤ aseq n` at o4's seed — the easiest (K) rung (subcritical, margin 2.4). The ONLY axiom asserting a mathematical claim on a literal object |
| 2 | `seed : Machine → Int` | data | supply the 13 seed integers (mechanical; its logical job — keeping instances distinct — is already done by the opaque symbol) |
| 3 | `NormalityPQ : Nat → Nat → Int → Prop` | **[OPEN] math — THE WALL** | the AEV Normality Conjecture 1.6 / Mahler 3/2 floor-mirror, per (p,q,seed); 13 instances across 3 places (×3/2@ℤ₂ ×9, ×4/3@ℤ₃ ×2, ×8/3@ℤ₃ ×2) |
| 4 | `o7orbit : Nat → Nat` | data + **[OPEN]** math via `TwoPowerAvoidance` | thin-set/generalized-Collatz: o7's orbit never hits `2^k` |
| 5 | `snOrbit : Nat → Nat` | data + **[OPEN]** math via `TwoPowerAvoidance` | same schema, Space Needle (different multipliers — NOT the same conjecture as o7) |
| 6 | `o17_nonhalt : Prop` | **[OPEN] math** | gate-timing: no μ=5 gate ever branches to halting μ′=8; finite-state-ness `[OBSERVED]` non-finite (Nerode 1,2,6,19,54,132,298 — a ≥298-state lower bound is `[PROVEN]`, but a finite scan cannot refute finiteness; corrected 07-22) |
| 7 | `holdouts1087_nonhalt : Prop` | **[ENGINEERING + OPEN]**, community-scale | the un-catalogued residual; NOT reducible to the named 17 (suite: 0/300 decided) |
| 8 | `championSteps : Nat` | data | interface Nat (Kropitz-class ≈ 10↑↑15, no clean literal) |
| 9 | `BB6 : Nat` | data | interface Nat |
| 10 | `champion_lower : championSteps ≤ BB6` | **[ENGINEERING]**, internal | rigorously verify the champion's halt locally |
| 11 | `enumeration_upper : AllHoldoutsNonHalt → BB6 ≤ championSteps` | **[ENGINEERING]**, Coq-BB5-scale | formal enumeration of all 6-state machines |

Head-count: **2 engineering, 4 data/interface, 1 community sweep, and 4 slots of genuinely open
mathematics** (`o4_ledger`; `NormalityPQ`×13; `TwoPowerAvoidance` over `o7orbit`/`snOrbit`;
`o17_nonhalt`).

## 2. Formalization-fidelity ledger — measured 2026-07-22

The Lean hypothesis does not yet literally SAY "these machines never halt". Verified conjunct by
conjunct:

| conjunct | form in `Completion.lean` | fidelity |
|---|---|---|
| `o4_nonhalt` | `∀ n, Template.steps n Template.init ≠ none` | **LITERAL** — a real TM statement; `o4_reduction : o4_ledger_conjecture → o4_nonhalt` is a PROVEN theorem, `[propext, Quot.sound]` |
| `o3_nonhalt` | `Normality43 (seed .o3)` | **pinned by docstring**. `O3.lean` partially formalizes the real dynamics (generation `a ≡ 0 mod 3` class: `o3_gen0`, `o3_odometer_mod0`, blank-tape anchors) but the `mod 1/2` classes and the conjecture⇒non-halt bridge are NOT Lean; the Completion conjunct does not reference `O3.lean` |
| 12 more ×p/q conjuncts | `NormalityPQ p q (seed .m)` | **pinned by docstring** — machine⟺arithmetic identity lives in the per-machine documents, not in Lean |
| `o7`/`spaceNeedle` | `TwoPowerAvoidance o7orbit/snOrbit` | orbit symbol opaque — **pinned** |
| `o17_nonhalt`, `holdouts1087_nonhalt` | opaque `Prop` | **pinned** |

**Consequence:** as of today, discharging `NormalityPQ` would make `BB6_eq_championSteps`
unconditional *as a Lean statement about uninterpreted symbols* — the machine-level meaning would
still rest on prose for 16 of 18 conjuncts. Closing that gap is Tier E work (E3/E4 below): real,
internal, and requiring no new mathematics.

---

## 3. The tiers

### Tier E — internal engineering, actionable now, no new mathematics

Ordered by (verified) tractability:

- **E1. o17 Nerode — ✅ DONE 2026-07-22 (`O17_NERODE_VERIFIED_2026-07-22.md`), and the premise
  of this task was itself stale.** The roadmap flagged this work "verification suspended,
  uncommitted"; in fact the document and both scripts were **committed 2026-07-10 in `e59df36`**.
  What the re-verification delivered instead: a **from-scratch** gate oracle (the original uses a
  fixed `bytearray` with *no* bounds check — a negative index would silently wrap) which **PASSED**
  — all seven Lean `#eval` anchors, 0 mismatches on 780 configs, 0 of 390 861 calls hitting the cap.
  The mathematics is SOUND; four bookkeeping defects fixed: the `## Reproduce` command was missing
  `sufdig=2` (the default gives different numbers); "0/112" was the wrong count (really 882 triples,
  now extended to 5 610, still 0 deciding); **§3's "refutes finiteness" was an overclaim, retracted
  in place**; and the "ratios ≈2.5–3 ⇒ no saturation" reading is a **battery artifact** (widening
  the battery lifts `54,132` to `81,260`), so future saturation claims must vary the battery.
  **Net label change:** "any DFA computing `b` has ≥298 states" is now `[PROVEN]` as a finite
  statement; **"no finite automaton exists" stays `[OBSERVED]`** and cannot be upgraded. o17 `[OPEN]`.

- **E2. `champion_lower` → theorem. [ENGINEERING]** Verify the champion
  (`1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE`) halts, locally and rigorously. The obstacle is
  representational (≈10↑↑15 steps — needs a certified accelerated/inductive simulation, not `rfl`),
  not mathematical. Note: this is `Suffix.lean`-scale infrastructure, and the x2 track's chunked-
  transport machinery (`steps_add` chains, realized milestones) is the in-house precedent.

- **E3. Grid→Lean lifts of the reduction chain, machine by machine. [ENGINEERING, largest internal
  block]** Make more conjuncts literal, in order of existing coverage:
  1. **o3** — finish what `O3.lean` started: the `a ≡ 1, 2 (mod 3)` generation classes, then the
     bridge `Normality43(seed) → o3_nonhalt(literal)` mirroring `o4_reduction`. Closest to done.
  2. **The gap-1 mirror family** (antihydra, o10, o11, o14, o16) — one engine, five seeds;
     `Mirror.lean`'s ladder is the substrate. One lift should serve all five.
  3. o2 (negation-conjugate), then o13 (gap-7, genuinely different reload — budget separately).
  4. o15/o18 (×8/3; `O18.lean` has the sweep/gate/reset episodes), o12/o8 (catalogue-only today —
     these need their reductions *derived* before they can be lifted; hardest of the band).

  Each lift converts "docstring-pinned" → "literal" in §2 and shrinks the honesty caveat that must
  accompany any external statement of `BB6_eq_championSteps`.

- **E4. Wire `seed` values.** Trivial once E3 touches each machine; worthless before (the opaque
  symbol already does its only logical job).

### Tier C — community-scale engineering **[GATED on external policy]**

- **C1. `enumeration_upper`.** A Coq-BB5-scale formal enumeration of the 6-state space. Not buildable
  solo at reasonable cost; inherently a bbchallenge-community artifact.
- **C2. The ~1087 residual.** Catalogue and decide/classify the un-named holdouts. The certified
  suite decides 0/300 sampled; the multiplier-extractor was refused as a labeling tool (failed its
  own validation gate). Any real dent means new decider work at community scale.

Both conflict with the standing **no-community-posting decision (2026-07-07)**. They stay parked
until the owner explicitly re-opens external engagement. Do not start them "quietly".

### Tier M — the open mathematics (the wall). NOT a work queue

Ranked easiest-first, with the constraint set any attack must satisfy:

- **M1. `o4_ledger` — the easiest rung.** Subcritical instance, margin 2.4; non-halt ⟺
  `freq{3∣Wₙ} ≤ 4/5` at seed 57. Still (K)-class: no known tool crosses even this rung.
- **M2. `NormalityPQ` — the wall proper.** = AEV Conjecture 1.6 (arXiv:2510.11723), one-sided form;
  implies-side of Mahler 3/2 (1968). 13 instances, 3 places. Note the internal finding: (K) is
  strictly WEAKER than AEV on three axes (one-sided / level k=2 / single orbit) and no named
  conjecture sits at the weaker level — a proof of any single instance is already generational.
- **M3. `TwoPowerAvoidance` (o7, Space Needle).** Congruence/automaton attacks PROVEN inapplicable
  (2026-07-10, two independent sound models each fail to separate). Needs a genuinely new
  reachability idea; not (K)-shaped, so not covered by the (K) impossibility results either.
- **M4. `o17_nonhalt`.** Unbounded gate-state (E1's Nerode fact). No scalar target exists for
  tower-mod weapons.

**The no-go fence [PROVEN], which any Tier-M attempt must clear before spending effort:**
No-Structure-Only-Selection (no bounded sub-action / all-orbits / annealed certificate — scope:
Antihydra density facet), the EVEN_COUNT_FLOOR collapse (no unconditional rung between Θ(log n) and
(K)), decider-preemption (the entire regular/finite-state decider taxonomy lands in register C2),
AIU neutral-direction obstruction, ENT Ledrappier–Young collapse, EUE coisometry no-go, Coverage
No-Go (every named effective-equidistribution framework fails a hypothesis). Net spec for new
mathematics (from `NEW_MATH_PROGRAM.md`): non-spectral, non-structural, orbit-specific, excursion-
level, magnitude-reading, a-priori. Nothing in the current literature satisfies it. **Internal
attack on Tier M is exhausted with proofs of exhaustion; re-entry requires a new idea from outside
the fence, not more effort inside it.**

### Tier X — external hand-off **[GATED, owner go-ahead required per policy]**

The 07-10 roadmap's own top recommendation, still pending a decision:

- **X1.** The AEV/Eliahou letter (`OUTREACH_EMAIL_DRAFT.md` exists; **send requires explicit
  per-send go-ahead** — standing policy).
- **X2.** arXiv the two publishable partials (`PAPER_RIGIDITY_LIMITS`, `PAPER_MIRROR_LADDER`) and
  the framework package (`BB6_FRAMEWORK_PACKAGE.md`, external-share-ready since 06-30).
- **X3.** Zenodo v1.5 archive.

This is the only tier that can plausibly move Tier M, because the missing mathematics is a research
program (effective single-orbit equidistribution, rank-1 amenable, (2,3)-solenoid), not a lemma.

---

## 4. Critical path

```
BB6 = championSteps
├── champion_lower ────────────── E2                [ENGINEERING, internal, start any time]
├── enumeration_upper ─────────── C1                [GATED community]
└── AllHoldoutsNonHalt
      ├── o4 ──────────────────── M1  (reduction PROVEN; ledger [OPEN])
      ├── 13 × NormalityPQ ────── M2  (THE WALL) ← X1/X2 the only live lever
      │     └── fidelity: E3 lifts (o3 → mirror-5 → o2 → o13 → o15/o18 → o12/o8)
      ├── o7, SpaceNeedle ─────── M3  [OPEN, non-(K)]
      ├── o17 ─────────────────── M4  [OPEN]  ← E1 commits its hardness fact
      └── ~1087 residual ──────── C2  [GATED community]
```

Reading: **everything internal and unconditional lives in E1–E4**; every mathematical obligation is
behind a fence with a proof that the fence is real; the single actionable lever against the wall is
Tier X, which is an owner decision, not an engineering task.

## 5. Do-now list (this week, no gates crossed)

1. **E1** — re-verify + commit the o17 Nerode analysis (small, closes a 12-day-old dangling item).
2. **E3.1** — o3 `mod 1/2` generation classes in `O3.lean`, targeting a literal `o3_nonhalt` with
   an `o3_reduction` mirroring o4's. This is the highest-value fidelity win per unit work.
3. **E2 scoping probe** — measure what a certified champion-halt verification actually needs
   (macro-step engine? tower arithmetic representation?) before committing to the build.
4. Put the X1–X3 decision in front of the owner as a yes/no, with the package already final.

## 6. One-line status

**BB(6) `[CONDITIONAL]`:** `BB6_eq_championSteps` GREEN on 11 axioms; 2 are engineering (one
internal E2, one community-gated C1), 4 are data, 1 is the community residual, and 4 slots are open
mathematics of which 13 instances are one named generational conjecture (AEV/Mahler 3/2) — attack
on it internally exhausted **with proofs of exhaustion**; fidelity of the formal statement is
literal for 1/18 conjuncts (o4) and improvable to ~majority by internal Lean work (E3) without any
new mathematics; the only live lever on the wall is the gated external hand-off (X). No machine is
decided. No label is upgraded.
