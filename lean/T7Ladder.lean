import X2

namespace X2

/-- **GAP RAIL** — `braid_topgrind` fires from `cascadeReg k` in `topGrindSteps k` steps. -/
theorem cascadeReg_topgrind (k : Nat) (hk : 4 ≤ k) (p : Int) (marker R : List Bool) :
    steps (topGrindSteps k) (cascadeReg k 1 p marker R)
      = some ⟨.E, p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int),
          ⟨ones (4 * (2 ^ (k - 1) - 2) + 4) ++ (pow10 1 ++ (true :: marker)), false,
            false :: (descCascade (k - 3) ++ (false :: false :: (zeros 7 ++ R)))⟩⟩ := by
  have hsplit : topGrindSteps k
      = 7 + braidRunSteps 0 (2 ^ (k - 1) - 2) + (4 * (2 ^ (k - 1) - 2) + 4) :=
    topGrindSteps_split k (by omega)
  have hblk : 2 * (2 ^ (k - 1) - 2) + 1 = 2 ^ k - 3 := cascadeReg_block k hk
  rw [hsplit]; unfold cascadeReg; rw [← hblk]
  exact braid_topgrind (2 ^ (k - 1) - 2) 1 p marker
    (descCascade (k - 3) ++ (false :: false :: (zeros 7 ++ R)))

/-- **THE LADDER STEP, ∀-position** — `regenIn k → regenIn (k+1)` in `exitSteps k + topGrindSteps k`
steps (RegenLaw ∘ braid_topgrind), for ANY start position `q`.  Marker carries one `ascMarker`
layer, tail carries the `2^k` pad; the seam (`ones_append_true` + `zeros_pad`) is discharged. -/
theorem ladderStep (k : Nat) (hk : 4 ≤ k) (q : Int) (marker' R'' : List Bool) :
    steps (exitSteps k + topGrindSteps k)
        (regenIn k q (2 ^ (k - 1) + 9)
          (false :: false :: true :: (pow01 (2 ^ k - 2) ++ marker'))
          (zeros (2 ^ k) ++ R''))
      = some (regenIn (k + 1)
              ((q - 2 ^ k) + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int))
              (2 ^ k + 9) marker' R'') := by
  rw [steps_add, regenLaw_pos (regenLaw_closed k hk) q _ _, someBind,
      cascadeReg_topgrind k hk (q - 2 ^ k) _ _]
  obtain ⟨m, rfl⟩ : ∃ m, k = m + 4 := ⟨k - 4, by omega⟩
  refine congrArg some ?_
  unfold regenIn
  rw [show m + 4 + 1 - 1 = m + 4 from by omega, show m + 4 + 1 - 4 = m + 1 from by omega,
      show m + 4 - 3 = m + 1 from by omega]
  have e1 : 4 * (2 ^ (m + 4 - 1) - 2) + 4 + 1 = 2 ^ (m + 4 + 1) - 3 := by
    have hm : 1 ≤ 2 ^ m := Nat.one_le_two_pow
    have h1 : 2 ^ (m + 4 - 1) = 2 ^ m * 8 := by rw [show m + 4 - 1 = m + 3 from by omega, Nat.pow_add]
    have h2 : 2 ^ (m + 4 + 1) = 2 ^ m * 32 := by rw [show m + 4 + 1 = m + 5 from by omega, Nat.pow_add]
    omega
  have hL : ones (4 * (2 ^ (m + 4 - 1) - 2) + 4)
        ++ (pow10 1 ++ (true :: false :: false :: true :: (pow01 (2 ^ (m + 4) - 2) ++ marker')))
      = ones (2 ^ (m + 4 + 1) - 3)
        ++ (false :: true :: false :: false :: true :: (pow01 (2 ^ (m + 4) - 2) ++ marker')) := by
    show ones (4 * (2 ^ (m + 4 - 1) - 2) + 4)
        ++ (true :: false :: true :: false :: false :: true :: (pow01 (2 ^ (m + 4) - 2) ++ marker'))
      = ones (2 ^ (m + 4 + 1) - 3)
        ++ (false :: true :: false :: false :: true :: (pow01 (2 ^ (m + 4) - 2) ++ marker'))
    rw [ones_append_true, e1]
  rw [hL, zeros_pad (m + 4) R'']

/-- Nested marker / pad / step-count consumed by an `n`-rung ascent from level `b`. -/
def ladderMarker (b : Nat) : Nat → List Bool
  | 0 => []
  | (n + 1) => (false :: false :: true :: pow01 (2 ^ b - 2)) ++ ladderMarker (b + 1) n
def ladderPad (b : Nat) : Nat → List Bool
  | 0 => []
  | (n + 1) => zeros (2 ^ b) ++ ladderPad (b + 1) n
def ladderSteps (b : Nat) : Nat → Nat
  | 0 => 0
  | (n + 1) => (exitSteps b + topGrindSteps b) + ladderSteps (b + 1) n

/-- **THE LADDER FOLD** (T7, 2026-07-22): the whole doubling-phase interior as ONE `∀n` induction.
`n` rungs from `regenIn b` — each an already-`∀`-proven `RegenLaw ∘ braid_topgrind` pair — climb to
`regenIn (b+n)`.  The two banked rails, assembled `∀n`, position-threaded. -/
theorem ladderFold : ∀ (n b : Nat), 4 ≤ b → ∀ (q : Int) (marker' R'' : List Bool),
    ∃ q', steps (ladderSteps b n)
        (regenIn b q (2 ^ (b - 1) + 9) (ladderMarker b n ++ marker') (ladderPad b n ++ R''))
      = some (regenIn (b + n) q' (2 ^ (b + n - 1) + 9) marker' R'') := by
  intro n
  induction n with
  | zero =>
    intro b hb q marker' R''
    exact ⟨q, by simp only [ladderSteps, ladderMarker, ladderPad, List.nil_append, Nat.add_zero]; rfl⟩
  | succ n ih =>
    intro b hb q marker' R''
    have hstep := ladderStep b hb q (ladderMarker (b + 1) n ++ marker') (ladderPad (b + 1) n ++ R'')
    obtain ⟨q', hq'⟩ := ih (b + 1) (by omega)
      ((q - 2 ^ b) + 5 + 2 * ((2 ^ (b - 1) - 2 : Nat) : Int)) marker' R''
    refine ⟨q', ?_⟩
    rw [ladderSteps, steps_add]
    simp only [ladderMarker, ladderPad, List.cons_append, List.append_assoc]
    rw [hstep, someBind, show b + 1 + n = b + (n + 1) from by omega] at *
    exact hq'

end X2

namespace X2

/-- **THE PROVEN MIDDLE, packaged** (T7, 2026-07-22): interior ladder + the top REGEN rung, as ONE
theorem.  From `regenIn b` with the nested marker/pad, `n` rungs climb to `regenIn (b+n)`
(`ladderFold`), then one more `RegenLaw` transport lands `cascadeReg (b+n)` — the config the tail
episode carries into `M1(g+1)`.  This is the maximal already-proven span of the doubling phase:
everything between the head's `regenIn 5` and the tail's `cascadeReg (g+9)`. -/
theorem ladderToCascade (b : Nat) (hb : 4 ≤ b) (n : Nat) (q : Int) (marker' R'' : List Bool) :
    ∃ q', steps (ladderSteps b n + exitSteps (b + n))
        (regenIn b q (2 ^ (b - 1) + 9) (ladderMarker b n ++ marker') (ladderPad b n ++ R''))
      = some (cascadeReg (b + n) 1 q' marker' R'') := by
  obtain ⟨q', hq'⟩ := ladderFold n b hb q marker' R''
  refine ⟨q' - 2 ^ (b + n), ?_⟩
  rw [steps_add, hq', someBind,
      regenLaw_pos (regenLaw_closed (b + n) (by omega)) q' marker' R'']

end X2

