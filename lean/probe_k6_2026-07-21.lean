import X2
open X2
def mk : List Bool := [true, false, true]
def RR : List Bool := [true, true, false]
-- does the REAL orbit reach TrailLaw 6's IN family?
#eval (steps (exitSteps 6 - trailSteps 6) (regenIn 6 0 (2 ^ 5 + 9) mk RR)
      == some (cascadeReg 4 1 (0 + 2 ^ 6 - 6 - 44) (depStack 6 (regenWord 6 ++ mk)) (zeros 16 ++ RR)))
-- control: wrong pad must fail
#eval (steps (exitSteps 6 - trailSteps 6) (regenIn 6 0 (2 ^ 5 + 9) mk RR)
      == some (cascadeReg 4 1 (0 + 2 ^ 6 - 6 - 44) (depStack 6 (regenWord 6 ++ mk)) (zeros 15 ++ RR)))
