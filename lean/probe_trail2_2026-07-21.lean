import X2
open X2

/-! INDEPENDENT RE-MEASUREMENT #2 (2026-07-21) of the trailing law, now with the
claimed `zeros 16` right pad.  Family built ONLY from definitions -- never lifted
off the orbit (that was the defect in the first, retracted report). -/

def depStack (k : Nat) (m : List Bool) : List Bool :=
  ((List.range (k - 6)).map (fun i => ones (2 ^ (i + 6) - 3) ++ [false, true])).foldr (· ++ ·) m

/-- the claimed identity, parametric in the pad `z` and the anchor shift `s` -/
def trailTest (k z : Nat) (s : Int) (marker R : List Bool) : Bool :=
  steps (trailSteps k)
      (cascadeReg 4 1 (0 + 2 ^ k - k + s) (depStack k (regenWord k ++ marker)) (zeros z ++ R))
    == some (cascadeReg k 1 (0 - 2 ^ k) marker R)

-- non-blank marker AND non-blank R throughout
def mk : List Bool := [true, false, true]
def RR : List Bool := [true, true, false]

-- (1) THE CLAIM: pad 16, anchor -44
#eval (trailTest 6 16 (-44) mk RR, trailTest 7 16 (-44) mk RR, trailTest 8 16 (-44) mk RR)

-- (2) CONTROL: no pad (the original, retracted form) -- must be false
#eval (trailTest 6 0 (-44) mk RR, trailTest 7 0 (-44) mk RR, trailTest 8 0 (-44) mk RR)

-- (3) CONTROL: wrong anchor -43 -- must be false
#eval (trailTest 6 16 (-43) mk RR, trailTest 7 16 (-43) mk RR)

-- (4) CONTROL: pad 15 and 17 -- must both be false
#eval (trailTest 7 15 (-44) mk RR, trailTest 7 17 (-44) mk RR)

-- (5) PAD SWEEP at k=7: which z work?  Should be exactly {16}.
#eval ((List.range 40).filter (fun z => trailTest 7 z (-44) mk RR))

-- (6) blank marker/R too
#eval (trailTest 7 16 (-44) [] [])

-- (7) REAL-ORBIT CROSS-CHECK: does the genuine orbit reach this fitted family?
def realTrailIn (k : Nat) (marker R : List Bool) : Option Cfg :=
  steps (exitSteps k - trailSteps k) (regenIn k 0 (2 ^ (k - 1) + 9) marker R)
#eval (realTrailIn 7 mk RR
      == some (cascadeReg 4 1 (0 + 2 ^ 7 - 7 - 44)
                 (depStack 7 (regenWord 7 ++ mk)) (zeros 16 ++ RR)))
#eval (realTrailIn 8 mk RR
      == some (cascadeReg 4 1 (0 + 2 ^ 8 - 8 - 44)
                 (depStack 8 (regenWord 8 ++ mk)) (zeros 16 ++ RR)))
