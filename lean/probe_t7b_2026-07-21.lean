import X2
open X2

/-! §5bl PROBE — the UNCONDITIONAL harvest of `regenLaw_closed` (§5bk).

Seven theorems in this file take `RegenLaw` as a hypothesis.  `regenLaw_closed`
(new today) discharges ALL of them `∀k ≥ 4`.  Every one of these is the FIRST
unconditional form of its statement. -/

namespace T7B

/-- `CascadeRegReached k` `∀k ≥ 4` — §5ah's reachability invariant, unconditional. -/
theorem cascadeRegReached_all (k : Nat) (hk : 4 ≤ k) : CascadeRegReached k :=
  cascadeRegReached_of_regenLaw k (regenLaw_closed k hk)

/-- `regenLaw_pos` `∀k ≥ 4` — the level-`k` REGEN exit at ANY anchor `q`. -/
theorem regenLaw_pos_all (k : Nat) (hk : 4 ≤ k) (q : Int) (marker R : List Bool) :
    steps (exitSteps k) (regenIn k q (2 ^ (k - 1) + 9) marker R)
      = some (cascadeReg k 1 (q - 2 ^ k) marker R) :=
  regenLaw_pos (regenLaw_closed k hk) q marker R

/-- **THE `∀k` CARRY, UNCONDITIONAL** — `carry_descends_of_regenLaw` discharged. -/
theorem carry_descends_all (k : Nat) (hk : 4 ≤ k) :
    ∃ p : Int, ∀ marker R, ∃ (dep : List Bool) (p' : Int),
      steps (exitSteps k + descentSteps k) (regenIn k p (2 ^ (k - 1) + 9) marker R)
        = some ⟨.E, p', ⟨ones 12 ++ dep, false, false :: true :: false :: R⟩⟩ :=
  carry_descends_of_regenLaw k hk (regenLaw_closed k hk)

/-- The ascend leg `a → a+1`, `∀a ≥ 4`, unconditional. -/
theorem regenAscend_all (a : Nat) (ha : 4 ≤ a) (q : Int) (m R : List Bool) :
    steps (exitSteps a + topGrindSteps a)
        (regenIn a q (2 ^ (a - 1) + 9)
          (false :: false :: true :: (pow01 (2 ^ a - 2) ++ m))
          (zeros (2 ^ a) ++ R))
      = some (regenIn (a + 1) (q - 2 ^ a + 5 + 2 * ((2 ^ (a - 1) - 2 : Nat) : Int))
          (2 ^ (a + 1 - 1) + 9) m R) :=
  regenAscend a ha (regenLaw_closed a ha) q m R

/-- The descend leg `a → 4`, `∀a ≥ 5`, unconditional. -/
theorem regenDescend_all (a : Nat) (ha : 5 ≤ a) (q : Int) (m R : List Bool) :
    steps (exitSteps a + descentSteps a) (regenIn a q (2 ^ (a - 1) + 9) m R)
      = some (regenIn 4
          (q - 2 ^ a + 13 + 2 * ((2 ^ (a - 1) - 2 : Nat) : Int)
            + ((lowerFoldShiftN (a - 3) : Nat) : Int))
          1
          (foldDepTail (a - 5)
            ++ (ones (4 * (2 ^ (a - 1) - 2) + 4) ++ (pow10 1 ++ (true :: m))))
          R) :=
  regenDescend a ha (regenLaw_closed a (by omega)) q m R

/-- **THE ASCENDING SPINE, UNCONDITIONAL `∀ n b ≥ 4`.** -/
theorem ascSpine_all (n b : Nat) (hb : 4 ≤ b) (q : Int) (m R : List Bool) :
    ∃ q' : Int, steps (ascSteps b n)
        (regenIn b q (2 ^ (b - 1) + 9) (ascMarker b n m) (ascR b n R))
      = some (regenIn (b + n) q' (2 ^ (b + n - 1) + 9) m R) :=
  ascSpine n b hb (fun i _ => regenLaw_closed (b + i) (by omega)) q m R

/-- **THE ODOMETER SUPER-DIGIT, UNCONDITIONAL `∀ b ≥ 4, n ≥ 1`** — an ascending ramp
`b → b+n` then its terminal descend to the floor level 4, as ONE halt-free transport of
length `ascSteps b n + (exitSteps (b+n) + descentSteps (b+n))`.  This is EXACTLY the
measured ladder rung of the doubling phase (§5bl). -/
theorem rampDescend_all (b n : Nat) (hb : 4 ≤ b) (hn : 1 ≤ n) (q : Int) (m R : List Bool) :
    ∃ q' : Int, steps (ascSteps b n + (exitSteps (b + n) + descentSteps (b + n)))
        (regenIn b q (2 ^ (b - 1) + 9) (ascMarker b n m) (ascR b n R))
      = some (regenIn 4 q' 1
          (foldDepTail (b + n - 5)
            ++ (ones (4 * (2 ^ (b + n - 1) - 2) + 4) ++ (pow10 1 ++ (true :: m)))) R) :=
  rampDescend b n hb hn (fun i _ => regenLaw_closed (b + i) (by omega)) q m R

/-- The super-digit reaches levels no `rfl` could: `b = 4, n = 10` is a ramp to level 14. -/
theorem rampDescend_all_14 (q : Int) (m R : List Bool) :
    ∃ q' : Int, steps (ascSteps 4 10 + (exitSteps 14 + descentSteps 14))
        (regenIn 4 q (2 ^ (4 - 1) + 9) (ascMarker 4 10 m) (ascR 4 10 R))
      = some (regenIn 4 q' 1
          (foldDepTail (4 + 10 - 5)
            ++ (ones (4 * (2 ^ (4 + 10 - 1) - 2) + 4) ++ (pow10 1 ++ (true :: m)))) R) :=
  rampDescend_all 4 10 (by decide) (by decide) q m R

#print axioms cascadeRegReached_all
#print axioms regenLaw_pos_all
#print axioms carry_descends_all
#print axioms regenAscend_all
#print axioms regenDescend_all
#print axioms ascSpine_all
#print axioms rampDescend_all
#print axioms rampDescend_all_14

end T7B
