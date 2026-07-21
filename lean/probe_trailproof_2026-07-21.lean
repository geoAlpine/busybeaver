import X2
open X2

/-! VERIFICATION of §5bg (`trailLaw_6`, `trailLaw_7`).
Confirms (a) the proved theorems really inhabit `TrailLaw 6` / `TrailLaw 7` as
DEFINED in §5bf, (b) their axiom footprint, and (c) that the statement is NOT
vacuous -- the same shape with a wrong pad or wrong anchor is kernel-FALSE. -/

-- (a) the theorems inhabit the §5bf `Prop` verbatim
example : TrailLaw 6 := trailLaw_6
example : TrailLaw 7 := trailLaw_7
#check @trailLaw_6
#check @trailLaw_7

-- (b) axiom footprint
#print axioms trailOut_6
#print axioms trailLaw_6
#print axioms trailOut_7
#print axioms trailLaw_7

-- (c) NON-VACUITY CONTROLS.  `trailLaw_6` instantiated at a non-blank marker/R and a
-- non-zero anchor must be `true`; the pad-15 / pad-17 / anchor-43 variants must be `false`.
def mk : List Bool := [true, false, true]
def RR : List Bool := [true, true, false]

def trailTest (k z : Nat) (s : Int) (p : Int) (marker R : List Bool) : Bool :=
  steps (trailSteps k)
      (cascadeReg 4 1 (p + 2 ^ k - k + s) (depStack k (regenWord k ++ marker)) (zeros z ++ R))
    == some (cascadeReg k 1 (p - 2 ^ k) marker R)

-- must be (true, true) -- the proved law, at p = 7 and p = -3
#eval (trailTest 6 16 (-44) 7 mk RR, trailTest 6 16 (-44) (-3) mk RR)
#eval (trailTest 7 16 (-44) 7 mk RR, trailTest 7 16 (-44) (-3) mk RR)

-- must be (false, false, false) -- wrong pad / wrong anchor
#eval (trailTest 6 15 (-44) 7 mk RR, trailTest 6 17 (-44) 7 mk RR, trailTest 6 16 (-43) 7 mk RR)
#eval (trailTest 7 15 (-44) 7 mk RR, trailTest 7 17 (-44) 7 mk RR, trailTest 7 16 (-43) 7 mk RR)
