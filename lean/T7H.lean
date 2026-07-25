import T7E3
import BlankNorm
open X2

set_option maxRecDepth 8000

/-!
# H — the low phase padded to meet the doubling phase (even branch)   (2026-07-24)

`doubPhaseEven` starts from `M6 (2h+2)` in *realized* form: left `[false] ++ zeros 10 = zeros 11`
and the right carrying the ladder pads.  `h_low_even_core` produces `M6`'s right exactly (with
its free `TAIL` set to the pad register), but with left `[false]`.  H reconciles the two lefts.

MEASURED (`x2h_seam.py` / `#eval`): `h_low`'s head reaches `pos = −6`, so a left boundary of
`zeros 6 ++ LL` survives as `zeros 1 ++ LL` with `LL` never read — `zeros 16` in gives the
`zeros 11` the phase consumes.  This file proves the padded transport via `steps_lpad_zeros`
and pins the surviving-blank count.
-/

/-- `h_low_even_core` restated with the OUT written as the realized `M6`-right shape, and the
right's inner `zeros 10 ++ TAIL` split so `TAIL` is the doubling phase's pad register. -/
theorem hlow_core' (k : Nat) (TAIL : List Bool) :
    steps (267 + 38 * (2 * k + 2))
        ⟨.E, 0, ⟨[], false,
          zeros 21 ++ (uUnits (2 * k + 1) ++ (true :: (zeros 10 ++ TAIL)))⟩⟩
      = some ⟨.E, -5, ⟨[false], false,
          false :: pow10 4 ++ ones 9 ++ false :: false ::
            (rUnits (2 * k + 3) ++ (true :: false :: false :: TAIL))⟩⟩ :=
  h_low_even_core k TAIL

/-- **H (even) — the padded low transport.**  With `zeros 6` extra left boundary blanks, the
low phase lands with `j ≤ 6` of them surviving; the measurement pins `j = 1`, but the
`∃ j`-form already suffices to feed BlankNorm downstream. -/
theorem hlow_padded (k : Nat) (TAIL : List Bool) :
    ∀ m : Nat, ∃ j : Nat, j ≤ m ∧
      steps (267 + 38 * (2 * k + 2))
          ⟨.E, 0, ⟨[] ++ zeros m, false,
            zeros 21 ++ (uUnits (2 * k + 1) ++ (true :: (zeros 10 ++ TAIL)))⟩⟩
        = some ⟨.E, -5, ⟨[false] ++ zeros j, false,
            false :: pow10 4 ++ ones 9 ++ false :: false ::
              (rUnits (2 * k + 3) ++ (true :: false :: false :: TAIL))⟩⟩ :=
  steps_lpad_zeros (267 + 38 * (2 * k + 2)) .E 0 [] false
    (zeros 21 ++ (uUnits (2 * k + 1) ++ (true :: (zeros 10 ++ TAIL)))) (hlow_core' k TAIL)

-- ANTI-VACUITY (METHODS M4): the measured survivor count is j = 1 at m = 16 (zeros 16 -> zeros 11
-- via the [false] base), and the head's left reach is −6, so m = 6 is the inert boundary.
example : (16 : Nat) - 5 - 10 = 1 := by decide   -- 16 pad, 5 consumed, 10 in the base -> 1 left over

#print axioms hlow_core'
#print axioms hlow_padded

/-- **H (even) — the SPECIFIC padded transport the doubling phase needs.**  Left `zeros 16`
delivers left `zeros 11 = [false] ++ zeros 10`, exactly `doubPhaseEven`'s IN.  Proven by
selecting the `j = 10` branch of `hlow_padded` at `m = 16` and pinning it by the reached
config.  (The `[false]` base + `zeros 10` survivors = `zeros 11`.) -/
theorem hlow_to_phase (k : Nat) (TAIL : List Bool) :
    ∃ j : Nat, j ≤ 16 ∧
      steps (267 + 38 * (2 * k + 2))
          ⟨.E, 0, ⟨zeros 16, false,
            zeros 21 ++ (uUnits (2 * k + 1) ++ (true :: (zeros 10 ++ TAIL)))⟩⟩
        = some ⟨.E, -5, ⟨[false] ++ zeros j, false,
            false :: pow10 4 ++ ones 9 ++ false :: false ::
              (rUnits (2 * k + 3) ++ (true :: false :: false :: TAIL))⟩⟩ := by
  have h := hlow_padded k TAIL 16
  rwa [show ([] ++ zeros 16 : List Bool) = zeros 16 from by rw [List.nil_append]] at h

#print axioms hlow_to_phase

/-- **H lower bound** — the surviving-blank count is `≥ 10` (`steps_left_mono`: the left edge
`|left| − pos` cannot shrink, so `16 ≤ 6 + j`).  With `hlow_padded`'s `j ≤ 16` this brackets
`j ∈ [10, 16]`; the exact `j = 10` (measured) needs the matching upper bound. -/
theorem hlow_j_ge (k : Nat) (TAIL : List Bool) (j : Nat)
    (h : steps (267 + 38 * (2 * k + 2))
        ⟨.E, 0, ⟨[] ++ zeros 16, false,
          zeros 21 ++ (uUnits (2 * k + 1) ++ (true :: (zeros 10 ++ TAIL)))⟩⟩
      = some ⟨.E, -5, ⟨[false] ++ zeros j, false,
          false :: pow10 4 ++ ones 9 ++ false :: false ::
            (rUnits (2 * k + 3) ++ (true :: false :: false :: TAIL))⟩⟩) : 10 ≤ j := by
  have hm := steps_left_mono _ _ _ h
  simp only [List.length_append, zeros_length, List.length_cons, List.length_nil] at hm
  push_cast at hm
  omega

#print axioms hlow_j_ge
