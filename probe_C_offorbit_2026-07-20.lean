import X2
open X2
-- The real intermediate config: trailFloorRegen's OUT for k=7 (j=0): cascadeReg 4 1 p (foldMarker 0 []) []
-- C claims: this reaches cascadeReg 7 in trailSteps 7 = 627 steps. Test the STATE/POS at step 627.
#eval ((steps 627 (cascadeReg 4 1 0 (foldMarker 0 []) [])).map (fun c => (c.st, c.pos)))
-- cascadeReg 7's canonical (st=E). Is the step-627 config EQUAL to any cascadeReg 7? Check state=E and pos.
-- Also: how far to a clean cascadeReg-7-like state? sample pos at 2530 (exitSteps 7) and 10069:
#eval ((steps 2530 (cascadeReg 4 1 0 (foldMarker 0 []) [])).map (fun c => (c.st, c.pos)))
#eval ((steps 10069 (cascadeReg 4 1 0 (foldMarker 0 []) [])).map (fun c => (c.st, c.pos)))
-- direct: does step-627 equal cascadeReg 7 with the trailing-anchor p' = 0 - 2^7 ? (decide on structure)
#eval decide (steps 627 (cascadeReg 4 1 0 (foldMarker 0 []) []) = some (cascadeReg 7 1 (0 - 2^7) [] []))
