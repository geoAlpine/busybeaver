import T7E2
open X2

set_option maxRecDepth 20000

/-!
# The TAIL's fixed ending  (2026-07-23)

`fixedEnd`: the last **75** steps of the doubling phase, landing on the next milestone.
MEASURED bit-identical at g=1,2,3,4 (`x2r3_tailrle.py`); the milestone FRAME that the
tail has been building is never read, so it is universally quantified here.

Head excursion over the episode is 12 cells left and 12 right, against a concrete left
of 21 (`pow01 5 ++ zeros 11`) and right of 17 — so neither `L` nor `FRAME` is touched.

CALIBRATION: this was first stated as a 110-step episode.  It is 75; the extra 35 is a
separate preceding `turn` stage which I had mis-attributed.  Lean refused the 110-step
statement outright.  The tail's TOTALS are unaffected:
  tail(g) = <entry> ∘ (g−1)×frameDigit(27) ∘ turn(35) ∘ fixedEnd(75)
  g=1: 0·27+35+75 = 110 ✓   g=3: 2·27+110 = 164 ✓   g=4: 3·27+110 = 191 ✓
-/

private theorem fec0 (L FRAME : List Bool) :
    steps 25 ⟨.E, 0, ⟨[false, true, false, true, false, true, false, true, false, true, false, false, false, false, false, false, false, false, false, false, false] ++ L, false, [false, true, true, true, true, true, true, true, true, false, false, false, false, false, false, false, false] ++ FRAME⟩⟩
      = some ⟨.F, 9, ⟨[true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, false, false, false, false, false, false, false, false, false, false] ++ L, false, [false, false, false, false, false, false, false, false] ++ FRAME⟩⟩ := by rfl

private theorem fec1 (L FRAME : List Bool) :
    steps 25 ⟨.F, 9, ⟨[true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, false, false, false, false, false, false, false, false, false, false] ++ L, false, [false, false, false, false, false, false, false, false] ++ FRAME⟩⟩
      = some ⟨.D, 0, ⟨[false, true, false, true, false, true, false, true, false, true, false, false, false, false, false, false, false, false, false, false, false] ++ L, true, [false, false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ FRAME⟩⟩ := by rfl

private theorem fec2 (L FRAME : List Bool) :
    steps 25 ⟨.D, 0, ⟨[false, true, false, true, false, true, false, true, false, true, false, false, false, false, false, false, false, false, false, false, false] ++ L, true, [false, false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ FRAME⟩⟩
      = some ⟨.E, -11, ⟨[false, false, false, false, false, false, false, false, false, false] ++ L, false, [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ FRAME⟩⟩ := by rfl

/-- `fixedEnd` at position 0. -/
theorem fixedEnd_zero (L FRAME : List Bool) :
    steps 75 ⟨.E, 0, ⟨pow01 5 ++ (zeros 11 ++ L), false,
        false :: (ones 8 ++ (zeros 8 ++ FRAME))⟩⟩
      = some ⟨.E, -11, ⟨[false, false, false, false, false, false, false, false, false, false] ++ L, false, [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ FRAME⟩⟩ := by
  show steps 75 ⟨.E, 0, ⟨[false, true, false, true, false, true, false, true, false, true, false, false, false, false, false, false, false, false, false, false, false] ++ L, false, [false, true, true, true, true, true, true, true, true, false, false, false, false, false, false, false, false] ++ FRAME⟩⟩ = _
  rw [show (75:Nat) = 25 + 50 from rfl, steps_add, fec0 L FRAME, someBind,
      show (50:Nat) = 25 + 25 from rfl, steps_add, fec1 L FRAME, someBind]
  exact fec2 L FRAME

/-- **THE TAIL'S FIXED ENDING, ∀ position, ∀ left, ∀ frame** — 75 steps onto the milestone.
The frame `(0^6 1)^g` the tail has been building is untouched; the episode only prepends
one more `1 0^6` digit and blanks the left. -/
theorem fixedEnd (p : Int) (L FRAME : List Bool) :
    steps 75 ⟨.E, p, ⟨pow01 5 ++ (zeros 11 ++ L), false,
        false :: (ones 8 ++ (zeros 8 ++ FRAME))⟩⟩
      = some ⟨.E, p - 11, ⟨zeros 10 ++ L, false, zeros 21 ++ (true :: (zeros 6 ++ FRAME))⟩⟩ := by
  have h := steps_pos_shift (d := p) (fixedEnd_zero L FRAME)
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

#print axioms fixedEnd_zero
#print axioms fixedEnd
