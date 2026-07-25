import TapeCalc
open TapeCalc

/-!
# Candidate C — the first Phase-B machine

`C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD`, a member of the 1104-holdout residual, found by
the pre-flight screen (`PREFLIGHT_2026-07-25.md`) to be a `(2, 4)` doubler whose milestone marker
words are drawn from the SAME family as `x2`'s.

This file sets it up on the machine-independent `TapeCalc` and audits the instrument.
**No machine decided. No label upgraded.**
-/

namespace CandC

inductive S6 | A | B | C | D | E | F
deriving DecidableEq, Repr

open S6

/-- the transition table of `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` -/
def TC : S6 → Bool → Option (Bool × Dir × S6)
  | A, false => some (true,  .R, B)   -- 1RB
  | A, true  => none                  -- ---   HALT
  | B, false => some (false, .L, C)   -- 0LC
  | B, true  => some (true,  .L, D)   -- 1LD
  | C, false => some (false, .R, D)   -- 0RD
  | C, true  => some (true,  .L, C)   -- 1LC
  | D, false => some (true,  .R, E)   -- 1RE
  | D, true  => some (false, .L, B)   -- 0LB
  | E, false => some (false, .R, F)   -- 0RF
  | E, true  => some (true,  .R, D)   -- 1RD
  | F, false => some (true,  .R, A)   -- 1RA
  | F, true  => some (false, .R, D)   -- 0RD

/-- blank tape, state A, position 0 -/
def initC : Cfg S6 := ⟨.A, 0, ⟨[], false, []⟩⟩

/-! ## Instrument audit -/

def stn : S6 → String
  | A => "A" | B => "B" | C => "C" | D => "D" | E => "E" | F => "F"

def rd (s : S6) (b : Bool) : String :=
  match step TC ⟨s, 0, ⟨[], b, []⟩⟩ with
  | none => "---"
  | some c =>
    let w := if c.pos = 1 then c.tape.left.headD false else c.tape.right.headD false
    (if w then "1" else "0") ++ (if c.pos = 1 then "R" else "L") ++ stn c.st

-- read the table back cell by cell; must equal the spec string
#eval String.intercalate "_" ([A,B,C,D,E,F].map (fun s => rd s false ++ rd s true))
#eval "spec :  1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD"
#eval (initC.pos, initC.tape.left, initC.tape.head, initC.tape.right)
#eval ([A,B,C,D,E,F].flatMap (fun s => [false,true].filterMap (fun b =>
    if (step TC ⟨s, 0, ⟨[], b, []⟩⟩).isNone then some (stn s, b) else none)))
#eval ((steps TC 1 ⟨A, 0, ⟨[], true, []⟩⟩).isNone, (steps TC 400 ⟨A, 0, ⟨[], true, []⟩⟩).isNone)

-- the four MEASURED milestones (python: 49469 / 192508 / 727066 / 2866580)
#eval [49469, 192508, 727066, 2866580].map (fun n =>
  (steps TC n initC).map (fun c => (stn c.st, c.pos, c.tape.left.length, c.tape.right.length)))

end CandC

/-! ## Milestone marker words (M0) -/

namespace CandC
def rle : List Bool → List (Bool × Nat)
  | [] => []
  | b :: r =>
    let rec go (b : Bool) (n : Nat) : List Bool → List (Bool × Nat)
      | [] => [(b, n)]
      | c :: t => if c == b then go b (n+1) t else (b, n) :: go c 1 t
    go b 1 r
end CandC

open CandC in
#eval [49469, 192508, 727066, 2866580].map (fun n =>
  (steps TC n initC).map (fun c => (rle c.tape.right).take 12))
