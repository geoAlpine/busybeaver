import X2
open X2

/-! INDEPENDENT RE-MEASUREMENT (2026-07-21).
Question: was the 2026-07-20 retraction caused by using a WRONG marker family
(`foldMarker 0 []`) in the trailing probe, rather than by a genuine off-orbit chain?
Here we test the §5be-measured trailing identity with the `depStack` marker family. -/

def depStackList (k : Nat) : List Bool :=
  (List.range (k - 6)).foldl
    (fun acc i => acc ++ (ones (2 ^ (i + 6) - 3) ++ [false, true])) []

def depStack (k : Nat) (m : List Bool) : List Bool := depStackList k ++ m

-- (1) THE CLAIMED TRAILING IDENTITY at k=7, blank marker/R.
#eval (steps (trailSteps 7)
        (cascadeReg 4 1 (0 + 2 ^ 7 - 7 - 44) (depStack 7 (regenWord 7 ++ [])) [])
      == some (cascadeReg 7 1 (0 - 2 ^ 7) [] []))

-- (2) same, NON-blank marker and R (frame-freedom check).
#eval (steps (trailSteps 7)
        (cascadeReg 4 1 (0 + 2 ^ 7 - 7 - 44)
          (depStack 7 (regenWord 7 ++ [true, false, true])) [true, true])
      == some (cascadeReg 7 1 (0 - 2 ^ 7) [true, false, true] [true, true]))

-- (3) k=6.
#eval (steps (trailSteps 6)
        (cascadeReg 4 1 (0 + 2 ^ 6 - 6 - 44) (depStack 6 (regenWord 6 ++ [])) [])
      == some (cascadeReg 6 1 (0 - 2 ^ 6) [] []))

-- (4) k=8.
#eval (steps (trailSteps 8)
        (cascadeReg 4 1 (0 + 2 ^ 8 - 8 - 44) (depStack 8 (regenWord 8 ++ [])) [])
      == some (cascadeReg 8 1 (0 - 2 ^ 8) [] []))

-- (5) THE 2026-07-20 RETRACTION PROBE, re-run verbatim: the WRONG marker family.
--     If this is false while (1) is true, the retraction was a marker error, not off-orbit.
#eval (steps (trailSteps 7) (cascadeReg 4 1 0 (foldMarker 0 []) [])
      == some (cascadeReg 7 1 (0 - 2 ^ 7) [] []))

-- (6) what the depStack marker actually is at k=7 (length), vs the wrong one.
#eval (depStackList 7).length
#eval (foldMarker 0 []).length
