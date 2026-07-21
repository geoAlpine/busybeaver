import Suffix

/-!
# BB(6) conditional completion theorem — the machine-checked logical frame

This file states the **complete BB(6) proof** as one conditional theorem, with all
open mathematical content isolated into explicitly-named, documented axioms. It proves
nothing about the halting of any cryptid; its value is that it makes the *logical
structure* of the complete proof machine-checked, and localizes the entire remaining
difficulty to 17 named arithmetic conjectures (each equivalent to a famous open problem)
plus the community-scale enumeration.

**Minimal distinct-conjecture structure (2026-07-10).** The 17 named conjunctions are not 17
unrelated problems: they are instances of **5 conjecture SCHEMAS** (§1.5) — base-3/2 normality
(`Normality32`, 9 seeds), base-4/3 normality (`Normality43`, 3 seeds incl. o4), base-8/3
normality (`Normality83`, 2 seeds), generalized-Collatz 2^k-avoidance (`TwoPowerAvoidance`, 2
seeds), and o17 gate-timing (its own form). The three normality schemas are one meta-schema
`NormalityPQ p q seed` at 3 genuinely-distinct p-adic places (3,2)/(4,3)/(8,3). Each `*_nonhalt`
is now *defined* as its schema at a per-machine seed, so the axiom audit exhibits the shared
conjecture FORM (one symbol `NormalityPQ`) rather than 16 opaque Props. **Honest:** sameness of
FORM transfers no bound (per-seed open content, reload doc §3.3); the collapse is of shape, not
of difficulty. See `MINIMAL_CONJECTURE_SET_2026-07-10.md`.

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

/-! ### §1.5  The conjecture SCHEMAS — the 17 named conjuncts collapse to 5 forms.

The reload-map analysis (`RELOAD_MAP_UNIFIED_2026-07-09.md`, re-verified numerically 2026-07-10:
gap-1 ×3/2 machines identical to `W ↦ ⌊3W/2⌋`, 20000/20000 exact; o2 negation-conjugate,
4000/4000; o13 gap-7 genuinely different, 2020/4000 mismatch) shows the 17 protections are
instances of a small set of parametrized schemas.  This section makes that collapse
machine-checked: each `*_nonhalt` below is *defined* as a schema at a machine-specific seed, so
the axiom audit exhibits the shared conjecture FORM (one symbol `NormalityPQ`) rather than 16
unrelated opaque Props.

**Honest scope.**  A schema is the arithmetic conjecture FORM; the seed is per-machine data.
Sameness of form does NOT transfer any bound between seeds (reload doc §3.3: two seeds of the
*same* map give statistically unrelated reload-unit sequences — the open content is per-seed).
So there remain genuinely-distinct per-seed open problems; only their SHAPE is unified.

**The machine⟺arithmetic reductions** justifying each `oX_nonhalt := schema` identity are
`[PROVEN-in-lit]` / `[PROVEN on grid]` / `[OBSERVED]` per machine (Mirror/RunStructure run-law
corollaries; catalogue for o5/o8/o12; automata for o7/SN).  Only **o4** is Lean end-to-end
(kept literal in §1.o4); for the other 16 the definitional identity ENCODES the documented
reduction, and the enumeration bridge (§3) folds those reductions into its hypothesis. -/

/-- Identifiers of the ×p/q named machines whose protection is a base-p/q normality instance.
Each machine's seed is opaque per-machine data (`seed`), so distinct machines are distinct
instances (never definitionally equal) even when they share a reload map. -/
inductive Machine where
  | antihydra | o10 | o2 | o11 | o13 | o14 | o16 | o12 | o8   -- ×3/2  (place ℤ₂)
  | o3 | o5                                                    -- ×4/3  (place ℤ₃)
  | o15 | o18                                                  -- ×8/3  (place ℤ₃)
  deriving DecidableEq

/-- The milestone seed integer of a named ×p/q machine (its initial orbit value / mirror seed
`W₀`).  Opaque: the exact value is per-machine data not needed by the frame; distinctness of the
constructors keeps the instances distinct. -/
axiom seed : Machine → Int

/-- **Base-p/q normality schema** — THE (K) open content, in one symbol.  `NormalityPQ p q s`
asserts the `ℤ_q^×`-equidistribution of the reload units of the affine ×(p/q) milestone orbit
seeded at `s` (equivalently: one-sided base-p/q digit-frequency normality of that seed orbit; the
deep-`v_q`-return frequency bound `freq{v_q(vₙ − x) ≥ ℓ}` the gate needs).  This is AEV Normality
Conjecture 1.6 / the floor-mirror of Mahler's 3/2 problem, instantiated at `(p, q, s)`.
Uninterpreted here (exactly as the 16 opaque Props were); the docstring pins its meaning.  The 14
(K)-band conjuncts are all `NormalityPQ` at 3 distinct places × their seeds. -/
axiom NormalityPQ : Nat → Nat → Int → Prop

/-- ×3/2 band (place ℤ₂).  The gap-1 machines `antihydra, o10, o11, o14, o16` are the *identical*
engine `W ↦ ⌊3W/2⌋` in mirror coordinates (SAME conjecture, different seeds); `o2` is its
negation-conjugate; `o13` (gap 7) is a genuinely different reload map — still base-3/2 normality,
a distinct instance; `o12, o8` are ×3/2 sea/nested (same fixed-point structure). -/
abbrev Normality32 (s : Int) : Prop := NormalityPQ 3 2 s
/-- ×4/3 band (place ℤ₃).  o4 (Lean-literal: `o4_ledger_conjecture` is this schema's concrete
realization at o4's seed), o3, o5. -/
abbrev Normality43 (s : Int) : Prop := NormalityPQ 4 3 s
/-- ×8/3 band (place ℤ₃).  o15, o18 (o18 = o15 mirrored/re-rooted). -/
abbrev Normality83 (s : Int) : Prop := NormalityPQ 8 3 s

/-- **Generalized-Collatz 2^k-avoidance schema** — the thin-set band (o7, Space Needle).  LITERAL:
the orbit never hits a power of two.  o7 and Space Needle share this FORM but have genuinely
different orbit maps (different multipliers: o7 two-multiplier ×3/2 & ×1/2; SN ×5/2), so they are
two distinct instances of one schema — not a normality/density statement but a reachability wall. -/
def TwoPowerAvoidance (orbit : Nat → Nat) : Prop := ∀ n k, orbit n ≠ 2 ^ k

/-- o7's milestone orbit `u_n` (opaque; halt ⟺ `u_n = 2^k`, k ≥ 2). -/
axiom o7orbit : Nat → Nat
/-- Space Needle's orbit `m_n + 1` (opaque; halt ⟺ `m_n + 1 = 2^k`). -/
axiom snOrbit : Nat → Nat

/-! #### The 16 non-o4 conjuncts as schema instances (defs, not axioms). -/

/-- **o3** ⟺ base-4/3 normality at o3's seed. [reduction `[PROVEN, Lean: O3]`: body + gen map]. -/
def o3_nonhalt : Prop := Normality43 (seed .o3)
/-- **Antihydra** ⟺ even-density ≥ 1/3 = base-3/2 normality (AEV Conj 1.6 verbatim). [PROVEN-in-lit]. -/
def antihydra_nonhalt : Prop := Normality32 (seed .antihydra)
/-- **o10** ⟺ base-3/2 normality (same reload map as Antihydra, distinct seed). [PROVEN on grid]. -/
def o10_nonhalt : Prop := Normality32 (seed .o10)
/-- **o2** ⟺ base-3/2 normality (ceiling; negation-conjugate of the canonical engine). [PROVEN on grid]. -/
def o2_nonhalt : Prop := Normality32 (seed .o2)
/-- **o11** ⟺ base-3/2 normality (gap-1 canonical engine, seeded). [PROVEN, Lean corollary]. -/
def o11_nonhalt : Prop := Normality32 (seed .o11)
/-- **o13** ⟺ base-3/2 normality (gap-7 VARIANT reload map; distinct instance). [PROVEN, Lean corollary]. -/
def o13_nonhalt : Prop := Normality32 (seed .o13)
/-- **o14** ⟺ base-3/2 normality (o11-twin, gap-1). [PROVEN, Lean corollary]. -/
def o14_nonhalt : Prop := Normality32 (seed .o14)
/-- **o16** ⟺ base-3/2 normality (gap-1). [PROVEN, Lean corollary]. -/
def o16_nonhalt : Prop := Normality32 (seed .o16)
/-- **o12** ⟺ base-3/2 normality (sea machine). [OBSERVED, catalogue]. -/
def o12_nonhalt : Prop := Normality32 (seed .o12)
/-- **o8** ⟺ base-3/2 normality (nested reset). [OBSERVED, catalogue]. -/
def o8_nonhalt : Prop := Normality32 (seed .o8)
/-- **o5** ⟺ base-4/3 normality (o4-class). [OBSERVED, catalogue]. -/
def o5_nonhalt : Prop := Normality43 (seed .o5)
/-- **o15** ⟺ base-8/3 normality. [PROVEN on grid + Lean depth]. -/
def o15_nonhalt : Prop := Normality83 (seed .o15)
/-- **o18** ⟺ base-8/3 normality (o18 = o15 mirrored). [PROVEN, Lean: O18]. -/
def o18_nonhalt : Prop := Normality83 (seed .o18)

/-- **o7** ⟺ its orbit never equals a power of two (`oddpart(u_n) ≠ 1`). Generalized-Collatz;
no finite congruence invariant, no S-unit/Baker handle. [OBSERVED milestone automaton]. -/
def o7_nonhalt : Prop := TwoPowerAvoidance o7orbit
/-- **Space Needle** ⟺ `m_n + 1` never a power of two. Thin-set reachability; `f` mixes all bits
(no congruence, no S-unit handle). [OBSERVED]. -/
def spaceNeedle_nonhalt : Prop := TwoPowerAvoidance snOrbit
/-- **o17** — the sole gate-timing form (its own schema, 1 instance): no `μ=5` gate ever branches
to the halting `μ′=8`.  Genuinely unbounded gate-state (Nerode index 1,2,6,19,54,132 — no finite
automaton), NOT a base-p/q normality statement. [Lean gate map: `O17`]. -/
axiom o17_nonhalt : Prop

/-! #### Machine-checked collapse: the conjuncts ARE their schemas at seeds (by `rfl`). -/

/-- The five ×3/2 gap-1 conjuncts are literally one schema `NormalityPQ 3 2` at five seeds. -/
example : antihydra_nonhalt = NormalityPQ 3 2 (seed .antihydra) := rfl
example : o11_nonhalt = NormalityPQ 3 2 (seed .o11) := rfl
example : o14_nonhalt = NormalityPQ 3 2 (seed .o14) := rfl
example : o16_nonhalt = NormalityPQ 3 2 (seed .o16) := rfl
example : o10_nonhalt = NormalityPQ 3 2 (seed .o10) := rfl
/-- o3/o5 are the ×4/3 schema; o15/o18 the ×8/3 schema; o7/SN the avoidance schema. -/
example : o3_nonhalt = NormalityPQ 4 3 (seed .o3) := rfl
example : o5_nonhalt = NormalityPQ 4 3 (seed .o5) := rfl
example : o15_nonhalt = NormalityPQ 8 3 (seed .o15) := rfl
example : o18_nonhalt = NormalityPQ 8 3 (seed .o18) := rfl
example : o7_nonhalt = (∀ n k, o7orbit n ≠ 2 ^ k) := rfl
example : spaceNeedle_nonhalt = (∀ n k, snOrbit n ≠ 2 ^ k) := rfl

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

/-- The champion machine's halting step count for `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE`.
Opaque: a hyperoperation-scale value, not a clean literal.

**⚠ PROVENANCE FLAGGED 2026-07-22 — this docstring contradicts the repo's own records.**  It
previously read "a Kropitz-class value ≈ 10↑↑15".  But `PROBLEM_LIST.md` and
`NEW_MATH_PROGRAM.md` BOTH record the BB(6) lower bound as `Σ(6) > 2↑↑↑5` (mxdys, 2025) —
**pentational, a whole hyperoperation level above 10↑↑15** (tetrational).  The two cannot both
be right.  The 10↑↑15/Kropitz figure is the outlier (3 sites: here, `COMPLETION_SKELETON`,
`DATA_SUMMARY`) against 2 independent internal records of `2↑↑↑5`; `10↑↑15` is plausibly the
superseded Kropitz record rather than this machine's value.  **Not resolved in-repo — the exact
value and its attribution are UNVERIFIED here and must be re-confirmed externally before being
quoted.**  Nothing depends on it: `championSteps` is opaque and `champion_lower` is an axiom, so
no theorem changes either way. -/
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
no `sorryAx` — and the sole remaining o4 axiom is the arithmetic `o4_ledger`.

**The schema collapse in the audit.**  The 16 non-o4 conjuncts are now *defs* unfolding into
schemas, so the audit of `BB6_eq_championSteps` no longer lists 16 opaque `*_nonhalt` axioms.
Instead the entire (K)-band (13 machines) contributes the SINGLE schema symbol `NormalityPQ`
(applied via `seed` at 13 constructors); the thin-set band contributes `TwoPowerAvoidance`
(a def) over the two orbit symbols `o7orbit`, `snOrbit`; o17 keeps its own `o17_nonhalt`.
That is the minimal distinct-conjecture structure made machine-visible: 5 schemas (3 of them
one meta-schema `NormalityPQ` at 3 places), 17 seed-instances. No `sorryAx` appears. -/

#print axioms BB6_eq_championSteps
#print axioms o4_reduction
#print axioms orbit_reaches
#print axioms o4_nonhalt_of_ledger
#print axioms antihydra_nonhalt
#print axioms o7_nonhalt

end Completion
