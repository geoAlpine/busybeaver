/-!
# Run structure of base-4/3 odometer itineraries — Lean 4 formalization

Formalizes the crown lemmas of `PAPER_RUN_STRUCTURE.md` (BB(6) machine o4):

* **Theorem 1 (itinerary bijection, injectivity form)** — `itinerary_inj`:
  seeds with equal length-`L` residue itineraries are congruent mod `3^L`.
  (Surjectivity onto `{0,1,2}^L` then follows by counting; checked by
  enumeration in the `#eval` block and in `crosscheck.py`.)
* **Theorem 2 (run closed form)** — `run_closed_form`: the branch fixed
  points are `x_ρ = -e(ρ)` (`fixedpoint_e`), the conjugation identity is
  `3·(T G - x_ρ) = 4·(G - x_ρ)` (`fixedpoint_conj`), and the maximal run
  of the starting residue is exactly `v₃(G - x_ρ) = v₃(G + e G)`.
* **Corollary 2.1 (run cap)** — `run_cap`, `run_cap_orbit`:
  `3^(v₃ n) ≤ |n|`, hence run `≤ log₃(G + 14)`.
* **Stretch (o15/o18 mirror)** — `o15_conj`, `o15_val_drop`,
  `o15_queued`, `o15_queued_val_drop`: the `×8/3` analogues.

Dependency-free: core Lean only (no mathlib); `Int`/`Nat` arithmetic,
`omega`, and a from-scratch 3-adic valuation `v3`.
-/

namespace RunStructure

/-! ## §1 The odometer.  `3·T(G) = 4·G + e(G mod 3)`, `e = {0↦9, 1↦14, 2↦1}`. -/

/-- Branch constant `e(ρ)` read off the residue of the argument. -/
def e (G : Int) : Int :=
  if G % 3 = 0 then 9 else if G % 3 = 1 then 14 else 1

/-- The base-4/3 odometer (generation counter of the BB(6) cryptid o4). -/
def T (G : Int) : Int := (4 * G + e G) / 3

/-- The orbit `G, T G, T² G, …`. -/
def orbit (G : Int) : Nat → Int
  | 0 => G
  | n + 1 => T (orbit G n)

theorem e_cases (G : Int) : e G = 9 ∨ e G = 14 ∨ e G = 1 := by
  unfold e
  by_cases h0 : G % 3 = 0
  · simp [h0]
  · by_cases h1 : G % 3 = 1
    · simp [h1]
    · simp [h0, h1]

theorem e_pos (G : Int) : 1 ≤ e G := by
  rcases e_cases G with h | h | h <;> omega

theorem e_le (G : Int) : e G ≤ 14 := by
  rcases e_cases G with h | h | h <;> omega

/-- `e` depends only on the residue mod 3. -/
theorem e_congr {G H : Int} (h : G % 3 = H % 3) : e G = e H := by
  unfold e; rw [h]

/-- `3 ∣ 4G + e(G mod 3)` — the odometer is integral. -/
theorem T_key (G : Int) : (4 * G + e G) % 3 = 0 := by
  unfold e
  have h : G % 3 = 0 ∨ G % 3 = 1 ∨ G % 3 = 2 := by omega
  rcases h with h | h | h <;> simp [h] <;> omega

/-- The defining identity `(1)` of the paper: `3·T(G) = 4·G + e(ρ)`. -/
theorem T_eq (G : Int) : 3 * T G = 4 * G + e G := by
  have h := T_key G
  have hdvd : (3 : Int) ∣ 4 * G + e G := by omega
  exact Int.mul_ediv_cancel' hdvd

/-- The fixed point of each branch sits in its own residue class:
`3 ∣ G + e G`, i.e. `G ≡ x_ρ (mod 3)` with `x_ρ = -e(ρ)`. -/
theorem e_resid (G : Int) : (G + e G) % 3 = 0 := by
  unfold e
  have h : G % 3 = 0 ∨ G % 3 = 1 ∨ G % 3 = 2 := by omega
  rcases h with h | h | h <;> simp [h] <;> omega

theorem T_pos {G : Int} (h : 1 ≤ G) : 1 ≤ T G := by
  have h1 := T_eq G
  have h2 := e_pos G
  omega

theorem orbit_pos {G : Int} (h : 1 ≤ G) : ∀ i, 1 ≤ orbit G i := by
  intro i
  induction i with
  | zero => exact h
  | succ i ih => exact T_pos ih

theorem orbit_shift (G : Int) (i : Nat) : orbit (T G) i = orbit G (i + 1) := by
  induction i with
  | zero => rfl
  | succ i ih => show T (orbit (T G) i) = T (orbit G (i + 1)); rw [ih]

/-! ## §2 Theorem 1: the itinerary bijection (injectivity form).

For `L ≥ 1`, seeds mod `3^L` map injectively (hence, by counting,
bijectively) to residue itineraries `(ρ₀, …, ρ_{L-1}) ∈ {0,1,2}^L`. -/

/-- `4` is a unit mod every power of 3: `3^L ∣ 4n → 3^L ∣ n`. -/
theorem pow3_dvd_of_dvd_four_mul :
    ∀ (L : Nat) (n : Int), (3 : Int) ^ L ∣ 4 * n → (3 : Int) ^ L ∣ n := by
  intro L
  induction L with
  | zero =>
    intro n _
    exact ⟨n, by rw [Int.pow_zero, Int.one_mul]⟩
  | succ L ih =>
    intro n h
    obtain ⟨k, hk⟩ := h
    rw [Int.pow_succ] at hk
    -- hk : 4 * n = 3 ^ L * 3 * k
    have hk' : 4 * n = 3 * ((3 : Int) ^ L * k) := by
      rw [hk, Int.mul_comm ((3 : Int) ^ L) 3, Int.mul_assoc]
    have h3 : (3 : Int) ∣ n := by
      have h4 : (3 : Int) ∣ 4 * n := ⟨(3 : Int) ^ L * k, hk'⟩
      omega
    obtain ⟨m, hm⟩ := h3
    have hmk : 4 * m = (3 : Int) ^ L * k := by
      have hlin : (3 : Int) * (4 * m) = 3 * ((3 : Int) ^ L * k) := by
        rw [← hk', hm]; omega
      generalize (3 : Int) ^ L * k = q at hlin ⊢
      omega
    obtain ⟨j, hj⟩ := ih m ⟨k, hmk⟩
    refine ⟨j, ?_⟩
    rw [hm, hj, Int.pow_succ, Int.mul_comm ((3 : Int) ^ L) 3, Int.mul_assoc]

/-- Induction step of Theorem 1 (the paper's `G = 3H + ρ`, `T(G) = 4H + s(ρ)`
argument in congruence form): equal first residues plus `T`-images congruent
mod `3^L` forces congruence mod `3^(L+1)`. -/
theorem step_inj {L : Nat} {G G' : Int} (hρ : G % 3 = G' % 3)
    (h : (3 : Int) ^ L ∣ T G - T G') : (3 : Int) ^ (L + 1) ∣ G - G' := by
  apply pow3_dvd_of_dvd_four_mul
  obtain ⟨k, hk⟩ := h
  refine ⟨k, ?_⟩
  have h1 := T_eq G
  have h2 := T_eq G'
  have he : e G = e G' := e_congr hρ
  rw [Int.pow_succ, Int.mul_comm ((3 : Int) ^ L) 3, Int.mul_assoc, ← hk]
  omega

/-- **Theorem 1** (seed–itinerary bijection, injectivity form): if two seeds
have the same residue itinerary for `L` steps, they agree mod `3^L`.
Since both sides have exactly `3^L` classes, the map is a bijection. -/
theorem itinerary_inj :
    ∀ (L : Nat) (G G' : Int),
      (∀ i, i < L → orbit G i % 3 = orbit G' i % 3) →
      (3 : Int) ^ L ∣ G - G' := by
  intro L
  induction L with
  | zero =>
    intro G G' _
    exact ⟨G - G', by rw [Int.pow_zero, Int.one_mul]⟩
  | succ L ih =>
    intro G G' h
    have h0 : G % 3 = G' % 3 := h 0 (Nat.succ_pos L)
    apply step_inj h0
    apply ih
    intro i hi
    have hnext := h (i + 1) (by omega)
    rw [orbit_shift G i, orbit_shift G' i]
    exact hnext

/-! ## §3 The 3-adic valuation, from scratch. -/

/-- Strong induction on `Nat` (self-contained, no mathlib). -/
theorem strong_ind (P : Nat → Prop) (h : ∀ n, (∀ m, m < n → P m) → P n) :
    ∀ n, P n := by
  have key : ∀ N n, n < N → P n := by
    intro N
    induction N with
    | zero => intro n hn; exact absurd hn (Nat.not_lt_zero n)
    | succ N ihN =>
      intro n hn
      exact h n (fun m hm => ihN m (by omega))
  intro n
  exact key (n + 1) n (by omega)

/-- 3-adic valuation on `Nat` (`v3n 0 = 0` by convention). -/
def v3n (n : Nat) : Nat :=
  if n = 0 then 0
  else if n % 3 = 0 then v3n (n / 3) + 1
  else 0
termination_by n
decreasing_by omega

/-- 3-adic valuation on `Int` (`v3 0 = 0` by convention). -/
def v3 (n : Int) : Nat := v3n n.natAbs

theorem v3n_of_not_dvd {n : Nat} (h : n % 3 ≠ 0) : v3n n = 0 := by
  rw [v3n.eq_def]
  by_cases h0 : n = 0
  · subst h0; simp at h
  · simp [h0, h]

theorem v3n_of_dvd {n : Nat} (h0 : n ≠ 0) (h : n % 3 = 0) :
    v3n n = v3n (n / 3) + 1 := by
  rw [v3n.eq_def]; simp [h0, h]

theorem v3n_three_mul {n : Nat} (h : n ≠ 0) : v3n (3 * n) = v3n n + 1 := by
  have h1 : 3 * n ≠ 0 := by omega
  have h2 : (3 * n) % 3 = 0 := by omega
  have h3 : (3 * n) / 3 = n := by omega
  rw [v3n_of_dvd h1 h2, h3]

/-- Units (numbers prime to 3) do not move the valuation. -/
theorem v3n_unit_mul {u : Nat} (hu : u % 3 ≠ 0) :
    ∀ n, v3n (u * n) = v3n n := by
  apply strong_ind (fun n => v3n (u * n) = v3n n)
  intro n ih
  by_cases h0 : n = 0
  · subst h0; rw [Nat.mul_zero]
  · by_cases h3 : n % 3 = 0
    · obtain ⟨k, hk⟩ : ∃ k, n = 3 * k := ⟨n / 3, by omega⟩
      subst hk
      have hk0 : k ≠ 0 := by omega
      have hu0 : u ≠ 0 := fun h => hu (by subst h; rfl)
      have huk : u * k ≠ 0 := Nat.mul_ne_zero hu0 hk0
      have hassoc : u * (3 * k) = 3 * (u * k) := by
        rw [← Nat.mul_assoc, Nat.mul_comm u 3, Nat.mul_assoc]
      rw [hassoc, v3n_three_mul huk, v3n_three_mul hk0, ih k (by omega)]
    · have hun : (u * n) % 3 ≠ 0 := by
        rw [Nat.mul_mod]
        have h1 : u % 3 = 1 ∨ u % 3 = 2 := by omega
        have h2 : n % 3 = 1 ∨ n % 3 = 2 := by omega
        rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2 <;>
          rw [h1, h2] <;> decide
      rw [v3n_of_not_dvd hun, v3n_of_not_dvd h3]

theorem v3_three_mul {n : Int} (h : n ≠ 0) : v3 (3 * n) = v3 n + 1 := by
  unfold v3
  rw [Int.natAbs_mul]
  exact v3n_three_mul (by omega)

theorem v3_four_mul (n : Int) : v3 (4 * n) = v3 n := by
  unfold v3
  rw [Int.natAbs_mul]
  exact v3n_unit_mul (by decide) n.natAbs

theorem v3_eight_mul (n : Int) : v3 (8 * n) = v3 n := by
  unfold v3
  rw [Int.natAbs_mul]
  exact v3n_unit_mul (by decide) n.natAbs

theorem v3_of_not_dvd {n : Int} (h : n % 3 ≠ 0) : v3 n = 0 := by
  unfold v3
  apply v3n_of_not_dvd
  omega

theorem v3_step {n : Int} (h0 : n ≠ 0) (h3 : n % 3 = 0) :
    v3 n = v3 (n / 3) + 1 := by
  obtain ⟨m, hm⟩ : ∃ m, n = 3 * m := ⟨n / 3, by omega⟩
  subst hm
  have hm0 : m ≠ 0 := by omega
  have hdiv : (3 * m) / 3 = m := by omega
  rw [hdiv, v3_three_mul hm0]

theorem v3_pos {n : Int} (h0 : n ≠ 0) (h3 : n % 3 = 0) : 1 ≤ v3 n := by
  rw [v3_step h0 h3]; omega

theorem v3_pos_mod {n : Int} (_h0 : n ≠ 0) (h : 1 ≤ v3 n) : n % 3 = 0 := by
  by_cases hc : n % 3 = 0
  · exact hc
  · rw [v3_of_not_dvd hc] at h
    omega

/-! ## §4 Theorem 2: exact run structure.

Branch fixed points `x_ρ = -e(ρ)` (`x₀ = -9, x₁ = -14, x₂ = -1`), conjugation
`T(G) - x_ρ = (4/3)(G - x_ρ)`, and the run closed form
`run(G) = v₃(G - x_ρ) = v₃(G + e G)`. -/

/-- The fixed-point identity `e(ρ) = -x_ρ`: `x = -(e G)` satisfies `3x = 4x + e`. -/
theorem fixedpoint_e (G : Int) : 3 * (-(e G)) = 4 * (-(e G)) + e G := by omega

/-- The conjugation identity: `3·(T G - x_ρ) = 4·(G - x_ρ)` with `x_ρ = -(e G)`,
written additively as `3·(T G + e G) = 4·(G + e G)`.  (One `ρ`-branch step
multiplies the distance to the branch fixed point by exactly `4/3`.) -/
theorem fixedpoint_conj (G : Int) : 3 * (T G + e G) = 4 * (G + e G) := by
  have h := T_eq G
  omega

/-- Valuation drop: `3a = 4b`, `3 ∣ b`, `b ≠ 0` force `v₃ a = v₃ b - 1`
(stated additively to avoid truncated subtraction).  Uses that 4 is a 3-adic
unit. -/
theorem v3_step_down {a b : Int} (h : 3 * a = 4 * b) (hb : b ≠ 0)
    (h3 : b % 3 = 0) : v3 a + 1 = v3 b := by
  obtain ⟨c, hc⟩ : ∃ c, b = 3 * c := ⟨b / 3, by omega⟩
  subst hc
  have hc0 : c ≠ 0 := by omega
  have ha : a = 4 * c := by omega
  rw [ha, v3_four_mul, v3_three_mul hc0]

/-- The run invariant: inside the run, `v₃(orbit G i + e G) = v₃(G + e G) - i`. -/
theorem run_invariant {G : Int} (hG : 1 ≤ G) :
    ∀ i, i ≤ v3 (G + e G) →
      v3 (orbit G i + e G) = v3 (G + e G) - i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    have hv := ih (by omega)
    have hΩ : 1 ≤ orbit G i := orbit_pos hG i
    have hE : 1 ≤ e G := e_pos G
    have hne : orbit G i + e G ≠ 0 := by omega
    have h1 : 1 ≤ v3 (orbit G i + e G) := by omega
    have hmod : (orbit G i + e G) % 3 = 0 := v3_pos_mod hne h1
    have hres : orbit G i % 3 = G % 3 := by
      have h2 := e_resid G
      omega
    have heq : e (orbit G i) = e G := e_congr hres
    have hTe := T_eq (orbit G i)
    have horb : orbit G (i + 1) = T (orbit G i) := rfl
    have hstep : 3 * (orbit G (i + 1) + e G) = 4 * (orbit G i + e G) := by
      omega
    have hdrop := v3_step_down hstep hne hmod
    omega

/-- Theorem 2, lower half: the starting residue persists for
`v₃(G + e G)` steps. -/
theorem run_length_lower {G : Int} (hG : 1 ≤ G) {i : Nat}
    (hi : i < v3 (G + e G)) : orbit G i % 3 = G % 3 := by
  have hv := run_invariant hG i (by omega)
  have hΩ : 1 ≤ orbit G i := orbit_pos hG i
  have hE : 1 ≤ e G := e_pos G
  have hne : orbit G i + e G ≠ 0 := by omega
  have h1 : 1 ≤ v3 (orbit G i + e G) := by omega
  have hmod : (orbit G i + e G) % 3 = 0 := v3_pos_mod hne h1
  have h2 := e_resid G
  omega

/-- Theorem 2, upper half: the run ends at exactly step `v₃(G + e G)`. -/
theorem run_length_exact {G : Int} (hG : 1 ≤ G) :
    orbit G (v3 (G + e G)) % 3 ≠ G % 3 := by
  have hv := run_invariant hG (v3 (G + e G)) (Nat.le_refl _)
  have hΩ : 1 ≤ orbit G (v3 (G + e G)) := orbit_pos hG _
  have hE : 1 ≤ e G := e_pos G
  have hne : orbit G (v3 (G + e G)) + e G ≠ 0 := by omega
  have hmod : (orbit G (v3 (G + e G)) + e G) % 3 ≠ 0 := by
    intro hc
    have hp := v3_pos hne hc
    omega
  have h2 := e_resid G
  omega

/-- **Theorem 2 (run closed form).**  For `G ≥ 1` with `ρ = G % 3`, the maximal
run of the residue `ρ` starting at `G` is exactly `v₃(G - x_ρ) = v₃(G + e G)`:
the residue persists for all `i < v₃(G + e G)` and changes at `i = v₃(G + e G)`. -/
theorem run_closed_form {G : Int} (hG : 1 ≤ G) :
    (∀ i, i < v3 (G + e G) → orbit G i % 3 = G % 3) ∧
      orbit G (v3 (G + e G)) % 3 ≠ G % 3 :=
  ⟨fun _ hi => run_length_lower hG hi, run_length_exact hG⟩

/-! ## §5 Corollary 2.1: the unconditional run cap. -/

theorem v3n_pow_le : ∀ n, n ≠ 0 → 3 ^ v3n n ≤ n := by
  apply strong_ind (fun n => n ≠ 0 → 3 ^ v3n n ≤ n)
  intro n ih h0
  by_cases h3 : n % 3 = 0
  · obtain ⟨k, hk⟩ : ∃ k, n = 3 * k := ⟨n / 3, by omega⟩
    subst hk
    have hk0 : k ≠ 0 := by omega
    have hle : 3 ^ v3n k ≤ k := ih k (by omega) hk0
    rw [v3n_three_mul hk0, Nat.pow_succ]
    generalize 3 ^ v3n k = P at hle ⊢
    omega
  · rw [v3n_of_not_dvd h3]
    omega

/-- **Corollary (run cap, valuation form):** `3^(v₃ n) ≤ |n|` for `n ≠ 0`. -/
theorem run_cap {n : Int} (h : n ≠ 0) : 3 ^ v3 n ≤ n.natAbs := by
  unfold v3
  exact v3n_pow_le n.natAbs (by omega)

/-- **Corollary 2.1:** the run starting at `G ≥ 1` satisfies
`3^run ≤ G + 14`, i.e. `run ≤ log₃(G + 14)`. -/
theorem run_cap_orbit {G : Int} (hG : 1 ≤ G) :
    (3 : Int) ^ v3 (G + e G) ≤ G + 14 := by
  have hE1 : 1 ≤ e G := e_pos G
  have hE2 : e G ≤ 14 := e_le G
  have h1 : 3 ^ v3 (G + e G) ≤ (G + e G).natAbs := run_cap (by omega)
  have h2 : ((3 ^ v3 (G + e G) : Nat) : Int) = (3 : Int) ^ v3 (G + e G) := by
    rw [Int.natCast_pow]
    rfl
  omega

/-! ## §6 Stretch: the o15/o18 `×8/3` mirror analogues.

o15's branch maps are `V ↦ (8V + c)/3` (`c ∈ {9, 11, -17, -5}`); the same
fixed-point argument conjugates to `3·(5·V' + c) = 8·(5·V + c)`, so
`v₃(5V + c)` drops by exactly 1 per same-branch step (8 is a 3-adic unit) —
the run laws `run = v₃(5V + 9)`, `v₃(5V + 11)`, `v₃(2V - 5)`, `v₃(V - 1)` of
`O15_FIXEDPOINT_2026-07-07.md`.  The queued branch `c = -5` has the *integer*
fixed point `x = 1`; the identity `3·(V' - 1) = 8·(V - 1)` is simultaneously
o18's depth push law `m' - 1 = (8/3)(m - 1)` (`O18_DEPTH_UNIFORM`). -/

/-- The o15 branch map `V ↦ (8V + c)/3`. -/
def T8 (c V : Int) : Int := (8 * V + c) / 3

theorem T8_eq {c V : Int} (h : (8 * V + c) % 3 = 0) :
    3 * T8 c V = 8 * V + c := by
  have hdvd : (3 : Int) ∣ 8 * V + c := by omega
  exact Int.mul_ediv_cancel' hdvd

/-- o15 conjugation identity: `3·(5·T₈ V + c) = 8·(5·V + c)`
(the fixed point `x = -c/5 ∈ ℤ₃` cleared of denominators). -/
theorem o15_conj {c V : Int} (h : (8 * V + c) % 3 = 0) :
    3 * (5 * T8 c V + c) = 8 * (5 * V + c) := by
  have h1 := T8_eq h
  omega

/-- Valuation drop under `×8/3` (8 a 3-adic unit). -/
theorem v3_step_down8 {a b : Int} (h : 3 * a = 8 * b) (hb : b ≠ 0)
    (h3 : b % 3 = 0) : v3 a + 1 = v3 b := by
  obtain ⟨c, hc⟩ : ∃ c, b = 3 * c := ⟨b / 3, by omega⟩
  subst hc
  have hc0 : c ≠ 0 := by omega
  have ha : a = 8 * c := by omega
  rw [ha, v3_eight_mul, v3_three_mul hc0]

/-- o15 run law, one step: on a same-branch step `v₃(5V + c)` drops by
exactly 1. -/
theorem o15_val_drop {c V : Int} (h8 : (8 * V + c) % 3 = 0)
    (h5 : (5 * V + c) % 3 = 0) (h0 : 5 * V + c ≠ 0) :
    v3 (5 * T8 c V + c) + 1 = v3 (5 * V + c) :=
  v3_step_down8 (o15_conj h8) h0 h5

/-- o15 queued branch (`c = -5`, integer fixed point `x = 1`) = o18 depth
push law: `3·(V' - 1) = 8·(V - 1)`. -/
theorem o15_queued {V : Int} (h : (8 * V - 5) % 3 = 0) :
    3 * (T8 (-5) V - 1) = 8 * (V - 1) := by
  have h1 : (8 * V + (-5)) % 3 = 0 := by omega
  have h2 := T8_eq h1
  omega

/-- o15 queued-branch / o18 depth run law: `v₃(V - 1)` drops by exactly 1 per
split step (hence `run = v₃(V - 1)`, mirroring Theorem 2). -/
theorem o15_queued_val_drop {V : Int} (hV : V % 3 = 1) (hne : V ≠ 1) :
    v3 (T8 (-5) V - 1) + 1 = v3 (V - 1) :=
  v3_step_down8 (o15_queued (by omega)) (by omega) (by omega)

/-! ## §7 Numeric sanity mirrors (`#eval`; cross-checked in `crosscheck.py`). -/

/-- Length-`L` residue itinerary. -/
def itin (G : Int) (L : Nat) : List Int :=
  (List.range L).map (fun i => orbit G i % 3)

/-- Theorem 1 check: all `3^L` seeds give pairwise-distinct itineraries
(injectivity + counting = bijectivity). -/
def bijCheck (L : Nat) : Bool :=
  let its := (List.range (3 ^ L)).map (fun g => itin (Int.ofNat g) L)
  its.eraseDups.length == 3 ^ L

/-- Simulated maximal run of the starting residue (fuel-bounded). -/
def runSimAux (ρ : Int) : Nat → Int → Nat
  | 0, _ => 0
  | fuel + 1, H => if H % 3 = ρ then runSimAux ρ fuel (T H) + 1 else 0

def runSim (G : Int) : Nat := runSimAux (G % 3) 64 G

/-- Theorem 2 check on a range: simulated run = `v₃(G + e G)`. -/
def runCheck (lo hi : Nat) : Bool :=
  (List.range (hi - lo)).all
    (fun k => runSim (Int.ofNat (lo + k)) == v3 (Int.ofNat (lo + k) + e (Int.ofNat (lo + k))))

#eval [bijCheck 1, bijCheck 2, bijCheck 3, bijCheck 4, bijCheck 5]
  -- expect [true, true, true, true, true]
#eval runCheck 1 2000        -- expect true
#eval [orbit 3 5, orbit 3 9, orbit 3 12, orbit 3 20]
  -- o4 real-orbit anchors from O4_LEDGER_ANALYSIS §5: expect [43, 151, 367, 3727]
#eval [v3 (43 + 14), v3 (7 + 14), v3 (14 + 1), v3 (30 + 9)]
  -- runs at G=43 (ρ=1), 7 (ρ=1), 14 (ρ=2), 30 (ρ=0)
#eval (List.range 20).all (fun k =>
  let V : Int := 3 * Int.ofNat k + 1
  V == 1 || decide (3 * (T8 (-5) V - 1) = 8 * (V - 1)))  -- o15/o18 identity, expect true

end RunStructure
