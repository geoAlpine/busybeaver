import X2
open X2

/-! INDEPENDENT CHECK (2026-07-21) of the STRENGTHENED descend claim:
are the sub-call sites genuine `regenIn a` instances?  If yes, the already-proven
`regenDescend` (∀a≥5, antecedent `RegenLaw a`) APPLIES there, and the floor landing
is a consequence rather than an observation. -/

def orbit7 : Cfg := regenIn 7 0 (2 ^ 6 + 9) [] []
def orbit8 : Cfg := regenIn 8 0 (2 ^ 7 + 9) [] []

/-- Is `c` literally `regenIn a` at its own position, with marker/tail read off at the
canonical offsets? -/
def isSite (a : Nat) (c : Cfg) : Bool :=
  let m := c.tape.left.drop (regenWord a).length
  let R := c.tape.right.drop (1 + (descCascade (a - 4)).length + (2 ^ (a - 1) + 9))
  c == regenIn a c.pos (2 ^ (a - 1) + 9) m R

/-- Does the descend from that site land EXACTLY on `regenDescend`'s proven OUT? -/
def descendMatches (a : Nat) (c : Cfg) : Bool :=
  let m := c.tape.left.drop (regenWord a).length
  let R := c.tape.right.drop (1 + (descCascade (a - 4)).length + (2 ^ (a - 1) + 9))
  steps (exitSteps a + descentSteps a) c
    == some (regenIn 4
        (c.pos - 2 ^ a + 13 + 2 * ((2 ^ (a - 1) - 2 : Nat) : Int)
          + ((lowerFoldShiftN (a - 3) : Nat) : Int))
        1
        (foldDepTail (a - 5)
          ++ (ones (4 * (2 ^ (a - 1) - 2) + 4) ++ (pow10 1 ++ (true :: m))))
        R)

def check (a off : Nat) (start : Cfg) : String :=
  match steps off start with
  | none => "HALT"
  | some c => s!"site regenIn {a}? {isSite a c} | descend == regenDescend OUT? {descendMatches a c}"

-- k=7 claimed site
#eval check 5 526 orbit7
-- k=8 claimed sites
#eval check 6 1862 orbit8
#eval check 5 7021 orbit8

-- control: an arbitrary nearby offset should NOT be a site
#eval check 5 527 orbit7
