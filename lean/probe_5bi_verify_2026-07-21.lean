import X2
open X2

/-! VERIFICATION of §5bi (`trailLaw_all`) — problem C closed `∀k`.
Confirms (a) the `∀k` theorem really inhabits `TrailLaw k` as DEFINED in §5bf,
(b) it specialises on the nose to the independently kernel-proven `trailLaw_6`/`trailLaw_7`,
(c) its axiom footprint, and (d) the phase-split arithmetic it rests on. -/

-- (a) the ∀k theorem inhabits the §5bf `Prop`
example (k : Nat) (hk : 6 ≤ k) : TrailLaw k := trailLaw_all k hk
#check @trailLaw_all

-- (b) ANTI-VACUITY: agrees with the two independently proven levels
example : TrailLaw 6 := trailLaw_all 6 (by decide)
example : TrailLaw 7 := trailLaw_all 7 (by decide)
example : TrailLaw 6 := trailLaw_6
example : TrailLaw 7 := trailLaw_7
-- reaches levels chunked `rfl` cannot
example : TrailLaw 8 := trailLaw_all 8 (by decide)
example : TrailLaw 12 := trailLaw_all 12 (by decide)
example : TrailLaw 100 := trailLaw_all 100 (by decide)

-- (c) axiom footprint
#print axioms trailLaw_all
#print axioms trailOut_all
#print axioms nest_depStack
#print axioms trailFoldPos
#print axioms trailPrefix
#print axioms trailSuffix

-- (d) the measured phase split, as arithmetic
example (k : Nat) (hk : 4 ≤ k) :
    trailSteps k = 393 + (trailCost (trailBlocks (k - 4)) + 7) := by
  have h := trailSteps_eq_trailCost k hk
  omega
