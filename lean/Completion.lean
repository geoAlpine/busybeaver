/-!
# BB(6) conditional completion theorem — the machine-checked logical frame

This file states the **complete BB(6) proof** as one conditional theorem, with all
open mathematical content isolated into explicitly-named, documented axioms. It proves
nothing about the halting of any cryptid; its value is that it makes the *logical
structure* of the complete proof machine-checked, and localizes the entire remaining
difficulty to 17 named arithmetic conjectures (each equivalent to a famous open problem)
plus the community-scale enumeration.

**What is PROVEN here:** the assembly `BB6 = championSteps` from the named hypotheses,
by antisymmetry of `≤`. **What is ASSUMED (the isolated hard content):** the 17 named
protection conjectures (`*_nonhalt`), the 1087-holdout residual, and the enumeration
bridge (`enumeration_upper`, `champion_lower`) — the [C]+[D] Coq-BB5-scale engineering.

The `reduction *` docstrings record where the machine⟺arithmetic equivalence is already
Lean-proven elsewhere in this project (o4 end-to-end via `Mirror`/`Template`/`Suffix`),
so that the `*_nonhalt` Props below are known to be *equivalent* to the stated arithmetic
statements — this file keeps them opaque only to stay self-contained (no imports).

Zero-mathlib, core only. No `sorry`. See `COMPLETION_SKELETON_2026-07-10.md`,
`ROADMAP_COMPLETE_PROOF_2026-07-10.md`, `PAPER_CENSUS.md`.
-/

namespace Completion

/-! ## §1 The 17 named protection conjectures (each machine's non-halting).

Each is an opaque `Prop`; the docstring states the exact arithmetic statement it is
equivalent to, and the status of the machine⟺arithmetic reduction. Band A (14 machines):
(K)-frequency = base-p/q normality = AEV Conjecture 1.6 = Mahler 3/2. Band B (2): thin-set
reachability = generalized-Collatz Diophantine. Band C (1): gate-timing, unbounded state. -/

/-- **o4** never halts ⟺ `freq{3∣W_n} < 4/5` for the seed-57 odometer orbit `W`.
Reduction machine⟺arithmetic: [PROVEN, Lean END-TO-END] (`Mirror`+`Template`+`Suffix`).
The easiest (K)-rung: subcritical, margin 2.4. Equivalent to a one-orbit base-4/3 normality. -/
axiom o4_nonhalt : Prop
/-- **o3** never halts ⟺ its ×4/3 odometer never triggers the ledger gate. [Lean: body+gen map]. -/
axiom o3_nonhalt : Prop
/-- **Antihydra** never halts ⟺ even-density ≥ 1/3 — verbatim the AEV Normality Conjecture. -/
axiom antihydra_nonhalt : Prop
/-- **o10** never halts ⟺ the balance never drops (×3/2 density, an AEV-relative seed). -/
axiom o10_nonhalt : Prop
/-- **o2** never halts ⟺ the ceiling-×3/2 orbit's even-density bound holds (+ mod-4 hatch). -/
axiom o2_nonhalt : Prop
/-- **o11** never halts ⟺ a seeded ×3/2 return-frequency bound at doubly-exp refills. -/
axiom o11_nonhalt : Prop
/-- **o13** never halts ⟺ its ×3/2 parity/gap draw avoids the fatal congruence. -/
axiom o13_nonhalt : Prop
/-- **o14** never halts ⟺ the o11-twin ×3/2 return bound (fixed points −12,−11). -/
axiom o14_nonhalt : Prop
/-- **o16** never halts ⟺ a seeded ×3/2 bound at a tower-sparse gate. -/
axiom o16_nonhalt : Prop
/-- **o12** never halts ⟺ its ×3/2 sea-machine return bound. -/
axiom o12_nonhalt : Prop
/-- **o8** never halts ⟺ its nested-×3/2 orbit bound. -/
axiom o8_nonhalt : Prop
/-- **o5** never halts ⟺ its ×4/3 orbit frequency bound (o4-flavored). -/
axiom o5_nonhalt : Prop
/-- **o15** never halts ⟺ the ×8/3 epoch-hit congruence is avoided. [Lean: machine+sweeps]. -/
axiom o15_nonhalt : Prop
/-- **o18** never halts ⟺ the same ×8/3 congruence (o18 = o15 mirrored/re-rooted). -/
axiom o18_nonhalt : Prop

/-- **o7** never halts ⟺ its orbit `u_n = a+3` never equals a power of two
(`oddpart(u_n) ≠ 1` for all n). Generalized-Collatz Diophantine; no finite congruence
invariant and no S-unit/Baker handle (2026-07-10 attacks). [OBSERVED milestone automaton]. -/
axiom o7_nonhalt : Prop
/-- **Space Needle** never halts ⟺ `m_n + 1` never equals a power of two. Thin-set
reachability, `f` mixes all bits (no congruence, no S-unit handle). [OBSERVED]. -/
axiom spaceNeedle_nonhalt : Prop
/-- **o17** never halts ⟺ no `μ=5` gate ever branches to the halting `μ′=8`. The gate-state
is genuinely unbounded (Nerode index 1,2,6,19,54,132 — no finite automaton). [Lean gate map: `O17`]. -/
axiom o17_nonhalt : Prop

/-- The ~1087 un-catalogued 6-state holdouts (bbchallenge April-2026 residual) are all
non-halting. Community-scale [OPEN]: our certified suite is a subset of the community
decider class (0/300 decided), so this is not internally reducible to the named 17. -/
axiom holdouts1087_nonhalt : Prop

/-! ## §2 The aggregate hypothesis and the busy-beaver interface. -/

/-- All 1104 BB(6) holdouts are non-halting: the 17 named protections ∧ the 1087 residual. -/
def AllHoldoutsNonHalt : Prop :=
  o4_nonhalt ∧ o3_nonhalt ∧ antihydra_nonhalt ∧ o10_nonhalt ∧ o2_nonhalt ∧
  o11_nonhalt ∧ o13_nonhalt ∧ o14_nonhalt ∧ o16_nonhalt ∧ o12_nonhalt ∧
  o8_nonhalt ∧ o5_nonhalt ∧ o15_nonhalt ∧ o18_nonhalt ∧
  o7_nonhalt ∧ spaceNeedle_nonhalt ∧ o17_nonhalt ∧
  holdouts1087_nonhalt

/-- The champion machine's halting step count: `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE`
halts at a Kropitz-class value ≈ 10↑↑15. Opaque: the exact tower is the current record
(machine-verified halting; the integer is not a clean literal). -/
axiom championSteps : Nat

/-- `BB6` = the maximal halting step-count over all 6-state 2-symbol Turing machines.
Modeled here as an abstract `Nat` with its two defining inequalities supplied by §3. -/
axiom BB6 : Nat

/-! ## §3 The two enumeration bridges (the [C]+[D] engineering, isolated as axioms). -/

/-- **Lower bound.** The champion is an explicit halting 6-state machine realizing
`championSteps`, so `BB6 ≥ championSteps`. [Checkable engineering: the champion's halt +
step count; not new mathematics.] -/
axiom champion_lower : championSteps ≤ BB6

/-- **Upper bound.** IF all 1104 holdouts are non-halting, THEN no halting 6-state machine
exceeds the champion, i.e. `BB6 ≤ championSteps`. This is the [C]+[D] content: a
Coq-BB5-scale enumeration of every 6-state machine in which each is either decided
(halts ≤ champion, or proven non-halting) or is one of the 1104 holdouts — so once the
holdouts are non-halting, the champion is maximal. [Community-scale engineering, no new
mathematics beyond the holdout resolutions.] -/
axiom enumeration_upper : AllHoldoutsNonHalt → BB6 ≤ championSteps

/-! ## §4 The conditional completion theorem. -/

/-- **BB(6) conditional completion.** The complete value of BB(6) equals the champion's
step count, PROVIDED all 1104 holdouts are non-halting (the 17 named protection conjectures
∧ the 1087-holdout residual). The proof is pure assembly (antisymmetry of `≤`): the champion
gives `BB6 ≥ N`, and the holdout hypotheses + enumeration give `BB6 ≤ N`.

All remaining difficulty is isolated into the hypothesis `AllHoldoutsNonHalt`, whose 17
named conjuncts are each equivalent to a famous open problem (AEV normality / Mahler 3/2
for 14; generalized-Collatz for o7/Space Needle; unbounded gate-timing for o17), and the
1087-holdout community sweep. Resolving any one named conjunct upgrades the corresponding
axiom to a theorem and decides that machine. -/
theorem BB6_eq_championSteps (h : AllHoldoutsNonHalt) : BB6 = championSteps :=
  Nat.le_antisymm (enumeration_upper h) champion_lower

/-- Equivalent packaging: BB(6) is determined (equals a known value) once the holdouts fall. -/
theorem BB6_determined (h : AllHoldoutsNonHalt) : ∃ N, BB6 = N :=
  ⟨championSteps, BB6_eq_championSteps h⟩

end Completion
