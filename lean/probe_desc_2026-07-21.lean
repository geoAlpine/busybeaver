import X2
open X2

/-! INDEPENDENT CHECK of the §5be STRUCTURAL claim: on the genuine orbit, does the
right register at each descend boundary sit at the floor `0^1 1^1`?
Claimed sites: k=7 offset 1833; k=8 offsets 6736, 8328. -/

def orbit7 : Cfg := regenIn 7 0 (2 ^ 6 + 9) [] []
def orbit8 : Cfg := regenIn 8 0 (2 ^ 7 + 9) [] []

-- right register at the claimed k=7 descend boundary
#eval ((steps 1833 orbit7).map (fun c => c.tape.right.take 8))
-- neighbours, in case the offset convention differs by the pad
#eval ((steps 1833 orbit7).map (fun c => c.tape.right.length))
#eval ((steps 1833 orbit7).map (fun c => c.st))

-- k=8 claimed boundaries
#eval ((steps 6736 orbit8).map (fun c => c.tape.right.take 8))
#eval ((steps 8328 orbit8).map (fun c => c.tape.right.take 8))

-- the floor for comparison: regenIn 4's right register
#eval (regenIn 4 0 1 [] []).tape.right.take 8
-- what cascadeReg 8 carries on the right, for contrast
#eval (cascadeReg 8 1 0 [] []).tape.right.take 8

-- LEAD LAW cross-check (this one IS kernel-proven at k=6,7; test the OBSERVED k=8)
#eval (steps (leadSteps 8) (regenIn 8 0 (2 ^ 7 + 9) [] [])
      == some (regenIn 4 (0 + 2 ^ 7 - 8 + 4) (2 ^ 7 + 1)
                 (ascMarker 4 (8 - 6) (regenWord 8 ++ [])) []))
