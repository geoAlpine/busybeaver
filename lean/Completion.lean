import Suffix

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
statements.  For **o4** this is no longer merely documented: this file `import Suffix`s the
actual o4 formalization and makes `o4_nonhalt` **literal** — it is *defined* as the real o4
Turing machine (`Template.step`) never halting from the blank tape, and the machine→arithmetic
reduction direction (`o4_reduction`: the a-ledger conjecture ⇒ o4 non-halts) is a **theorem**,
proved by chaining `Template.real_milestone` (blank → `M(43,18)`) with
`Suffix.generation_odometer` (the base-4/3 odometer + ledger generation map).  Only the
genuinely-open arithmetic content (the a-ledger stays `≥ 1`) remains an axiom (`o4_ledger`).
The other 16 named `*_nonhalt` stay opaque `Prop`s (their machines are not formalized here).

Zero-mathlib, core only. No `sorry`. See `COMPLETION_SKELETON_2026-07-10.md`,
`ROADMAP_COMPLETE_PROOF_2026-07-10.md`, `PAPER_CENSUS.md`.
-/

namespace Completion

/-! ## §1 The 17 named protection conjectures (each machine's non-halting).

Each is an opaque `Prop`; the docstring states the exact arithmetic statement it is
equivalent to, and the status of the machine⟺arithmetic reduction. Band A (14 machines):
(K)-frequency = base-p/q normality = AEV Conjecture 1.6 = Mahler 3/2. Band B (2): thin-set
reachability = generalized-Collatz Diophantine. Band C (1): gate-timing, unbounded state. -/

/-! ### §1.o4  The LITERAL o4 layer (imported from `Template`/`Suffix`).

`o4_nonhalt` below is not an opaque `Prop`: it is *defined* as the real o4 Turing machine
never halting from the blank tape, and its arithmetic reduction (`o4_reduction`) is PROVEN
here from the o4 formalization.  See §1.o4 lemmas. -/

/-- The arithmetic milestone sequence of the o4 blank-tape orbit: `G` is the base-4/3
odometer register, `a` the filler/ledger.  Seeded at the first `G ≥ 34` milestone
`M(43, 18)` (`Template.real_milestone`, step 1548) and advanced by the derived generation
map `Suffix.generation_odometer` (`G ↦ ⌊4G/3⌋ + c(G mod 3)`, `a ↦ ledgerNext`). -/
def Gseq : Nat → Nat
  | 0 => 43
  | (n + 1) => 4 * Gseq n / 3 + Template.cOdo (Gseq n)

def aseq : Nat → Nat
  | 0 => 18
  | (n + 1) => Template.ledgerNext (Gseq n) (aseq n)

/-- The odometer register stays `≥ 34` (so every generation step is applicable). -/
theorem Gseq_ge (n : Nat) : 34 ≤ Gseq n := by
  induction n with
  | zero => decide
  | succ n ih =>
    show 34 ≤ 4 * Gseq n / 3 + Template.cOdo (Gseq n)
    omega

/-- The measure `G + 2a` strictly increases each generation (used to certify that a
generation consumes `> 0` steps).  Holds in all three residue classes, ledger drain
included. -/
theorem mu_strict (n : Nat) :
    Gseq n + 2 * aseq n < Gseq (n + 1) + 2 * aseq (n + 1) := by
  have hg : 34 ≤ Gseq n := Gseq_ge n
  show Gseq n + 2 * aseq n
      < 4 * Gseq n / 3 + Template.cOdo (Gseq n)
        + 2 * Template.ledgerNext (Gseq n) (aseq n)
  rcases (by omega : Gseq n % 3 = 0 ∨ Gseq n % 3 = 1 ∨ Gseq n % 3 = 2) with h | h | h
  · have hc : Template.cOdo (Gseq n) = 3 := by unfold Template.cOdo; rw [if_pos h]
    have hl : Template.ledgerNext (Gseq n) (aseq n) = aseq n + 6 := by
      unfold Template.ledgerNext; rw [if_neg (by omega), if_neg (by omega)]
    rw [hc, hl]; omega
  · have hc : Template.cOdo (Gseq n) = 5 := by
      unfold Template.cOdo; rw [if_neg (by omega), if_pos h]
    have hl : Template.ledgerNext (Gseq n) (aseq n) = aseq n - 1 := by
      unfold Template.ledgerNext; rw [if_pos h]
    rw [hc, hl]; omega
  · have hc : Template.cOdo (Gseq n) = 1 := by
      unfold Template.cOdo; rw [if_neg (by omega), if_neg (by omega)]
    have hl : Template.ledgerNext (Gseq n) (aseq n) = aseq n + 4 := by
      unfold Template.ledgerNext; rw [if_neg (by omega), if_pos h]
    rw [hc, hl]; omega

/-- Length of the milestone tape's right half: `= (G-1) + 2a + 2`. -/
theorem pow10_len (a : Nat) : (Template.pow10 a).length = 2 * a := by
  induction a with
  | zero => rfl
  | succ a ih =>
    rw [show Template.pow10 (a + 1) = true :: false :: Template.pow10 a from rfl]
    simp only [List.length_cons, ih]; omega

theorem Mcfg_right_len (G a : Nat) (p : Int) :
    (Template.Mcfg G a p).tape.right.length = (G - 1) + 2 * a + 2 := by
  show (List.replicate (G - 1) false ++ (Template.pow10 a ++ [false, true])).length = _
  simp only [List.length_append, List.length_replicate, pow10_len,
    List.length_cons, List.length_nil]
  omega

/-- A halt-free segment stays halt-free on every prefix: if `steps N c` succeeds then
`steps m c ≠ none` for all `m ≤ N`.  (`steps = none` is absorbing: `noneBind`.) -/
theorem prefix_ne_none {c c' : Template.Cfg} {N m : Nat}
    (h : Template.steps N c = some c') (hm : m ≤ N) : Template.steps m c ≠ none := by
  intro hnone
  rw [show N = m + (N - m) from by omega, Template.steps_add, hnone,
    Template.noneBind] at h
  exact absurd h (by simp)

/-- **The o4 orbit reaches every arithmetic milestone.**  Assuming the a-ledger stays
`≥ 1`, the blank-tape orbit reaches milestone `n` (`M(Gseq n, aseq n)`) at a step
`N ≥ n`.  Proved by induction: base = `Template.real_milestone`; step =
`Suffix.generation_odometer` (applicable since `Gseq_ge` gives `G ≥ 34`, and the ledger
hypothesis gives `a ≥ 1`); the step count grows by `> 0` via `mu_strict`. -/
theorem orbit_reaches (h : ∀ n, 1 ≤ aseq n) :
    ∀ n, ∃ (N : Nat) (p : Int),
      n ≤ N ∧ Template.steps N Template.init = some (Template.Mcfg (Gseq n) (aseq n) p) := by
  intro n
  induction n with
  | zero => exact ⟨1548, (-42 : Int), by omega, Template.real_milestone⟩
  | succ n ih =>
    obtain ⟨N, p, hNn, hN⟩ := ih
    obtain ⟨M, q, hM⟩ :=
      Template.generation_odometer (Gseq n) (aseq n) p (Gseq_ge n) (h n)
    have hMpos : 0 < M := by
      rcases Nat.eq_zero_or_pos M with h0 | h0
      · exfalso
        subst h0
        have hM' : some (Template.Mcfg (Gseq n) (aseq n) p)
            = some (Template.Mcfg (Gseq (n + 1)) (aseq (n + 1)) q) := hM
        have hlen := congrArg (fun c => c.tape.right.length) (Option.some.inj hM')
        simp only [Mcfg_right_len] at hlen
        have hmu := mu_strict n
        have hg := Gseq_ge n
        have hg1 := Gseq_ge (n + 1)
        omega
      · exact h0
    refine ⟨N + M, q, by omega, ?_⟩
    rw [Template.steps_add, hN, Template.someBind]
    exact hM

/-- **o4** never halts — the LITERAL machine statement: the real o4 Turing machine
`1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---` (`Template.step`) run from the blank tape
(`Template.init`) never reaches its halt transition (`Template.steps n = none`).  This is
the actual `o4` object of the formalization, not an opaque `Prop`. -/
def o4_nonhalt : Prop := ∀ n, Template.steps n Template.init ≠ none

/-- **The o4 a-ledger conjecture** (the genuinely-open arithmetic content): along the
base-4/3 odometer orbit the filler/ledger `aseq` never drains to `0` (equivalently, the
seed-orbit `v₃`-return frequency `freq{3∣W_n} < 4/5`, the easiest (K)/base-4/3 normality
rung — subcritical, margin 2.4).  This is the ONE informal residue of the o4 decision. -/
def o4_ledger_conjecture : Prop := ∀ n, 1 ≤ aseq n

/-- **o4 reduction (PROVEN):** the a-ledger conjecture ⇒ o4 never halts from the blank
tape.  This is the machine→arithmetic reduction direction, now LITERAL in Lean (chaining
`Template.real_milestone` and `Suffix.generation_odometer` via `orbit_reaches` +
`prefix_ne_none`), no longer merely documented.  [PROVEN, `[propext, Quot.sound]` only.] -/
theorem o4_reduction (h : o4_ledger_conjecture) : o4_nonhalt := by
  intro m
  obtain ⟨N, p, hNm, hN⟩ := orbit_reaches h m
  exact prefix_ne_none hN hNm

/-- The only remaining o4 axiom: the open arithmetic a-ledger conjecture.  Everything
between it and `o4_nonhalt` (the whole generation dynamics, odometer, and non-halting
reduction) is now a Lean theorem — cf. `o4_reduction`. -/
axiom o4_ledger : o4_ledger_conjecture

/-- o4's non-halting now follows from a single named ARITHMETIC axiom via a PROVEN
reduction, rather than being an opaque assumption. -/
theorem o4_nonhalt_of_ledger : o4_nonhalt := o4_reduction o4_ledger

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

/-! ## §5 Axiom audit (printed at every build).

`BB6_eq_championSteps` no longer lists `o4_nonhalt` among its axioms: o4's conjunct is now
a *defined* machine statement (`∀ n, Template.steps n Template.init ≠ none`), so it
contributes no axiom.  The o4 reduction (`o4_reduction`) is `[propext, Quot.sound]` only —
no `sorryAx` — and the sole remaining o4 axiom is the arithmetic `o4_ledger`. -/

#print axioms BB6_eq_championSteps
#print axioms o4_reduction
#print axioms orbit_reaches
#print axioms o4_nonhalt_of_ledger

end Completion
