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

/-! ### The tail's odometer — `frameDigit` and its fold -/

/-- The LEFT register the tail odometer consumes: `j` copies of the 7-cell word
`1 0 1 0 1 0 0`, measured on the real orbit (g=4, stages 44 986 804 → 831 → 858 → 885). -/
def frameL : Nat → List Bool → List Bool
  | 0, X => X
  | j + 1, X => true :: false :: true :: false :: true :: false :: false :: frameL j X

/-- The RIGHT register it builds: one `0^5 1 0` digit per stage, accumulating inward. -/
def frameZ : Nat → List Bool → List Bool
  | 0, Z => Z
  | j + 1, Z => frameZ j (zeros 5 ++ (true :: false :: Z))

/-- **`frameDigit`** — ONE stage of the tail odometer, 27 steps, `∀ p X Z`.  Consumes one
7-cell word from the left and writes one frame digit on the right; the head advances `−7`.
Head excursion is 8 cells left and 4 right against the concrete 8/4, so `X` and `Z` are
never read. -/
theorem frameDigit (p : Int) (X Z : List Bool) :
    steps 27 ⟨.E, p, ⟨false :: true :: false :: true :: false :: true :: false :: false :: X,
        false, zeros 4 ++ Z⟩⟩
      = some ⟨.E, p - 7, ⟨false :: X, false, zeros 9 ++ (true :: false :: Z)⟩⟩ := by
  have h := steps_pos_shift (d := p)
    (show steps 27 ⟨.E, (0:Int), ⟨false :: true :: false :: true :: false :: true :: false ::
        false :: X, false, zeros 4 ++ Z⟩⟩
      = some ⟨.E, (-7:Int), ⟨false :: X, false, zeros 9 ++ (true :: false :: Z)⟩⟩ from by rfl)
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **`frameFold`** — the tail odometer, `∀ j`: `j` stages in `27j` steps, building the
milestone frame one digit at a time. -/
theorem frameFold : ∀ (j : Nat) (p : Int) (X Z : List Bool),
    steps (27 * j) ⟨.E, p, ⟨false :: frameL j X, false, zeros 4 ++ Z⟩⟩
      = some ⟨.E, p - 7 * (j : Int), ⟨false :: X, false, zeros 4 ++ frameZ j Z⟩⟩ := by
  intro j
  induction j with
  | zero => intro p X Z; exact congrArg some (cfgPos (by push_cast; omega))
  | succ j ih =>
    intro p X Z
    show steps (27 * (j + 1))
        ⟨.E, p, ⟨false :: true :: false :: true :: false :: true :: false :: false :: frameL j X,
          false, zeros 4 ++ Z⟩⟩ = _
    rw [show 27 * (j + 1) = 27 + 27 * j from by omega, steps_add, frameDigit p (frameL j X) Z, someBind,
        show (zeros 9 ++ (true :: false :: Z)) = zeros 4 ++ (zeros 5 ++ (true :: false :: Z))
          from rfl,
        ih (p - 7) X (zeros 5 ++ (true :: false :: Z))]
    exact congrArg some (cfgPos (by push_cast; omega))

#print axioms frameDigit
#print axioms frameFold

/-- **`turn`** — the fixed 35-step stage between the odometer and the ending (measured at
g=4, 44 986 885 → 44 986 920).  Consumes 16 left cells, advances `−15`, and hands the
right side over in exactly `fixedEnd`'s IN shape. -/
theorem turn (p : Int) (X Z : List Bool) :
    steps 35 ⟨.E, p, ⟨false :: true :: false :: true :: false :: true :: true :: true :: true ::
        true :: true :: true :: true :: true :: false :: false :: X, false, zeros 4 ++ Z⟩⟩
      = some ⟨.E, p - 15, ⟨false :: X, false,
          false :: (ones 8 ++ (zeros 8 ++ (true :: false :: Z)))⟩⟩ := by
  have h := steps_pos_shift (d := p)
    (show steps 35 ⟨.E, (0:Int), ⟨false :: true :: false :: true :: false :: true :: true :: true ::
        true :: true :: true :: true :: true :: true :: false :: false :: X, false, zeros 4 ++ Z⟩⟩
      = some ⟨.E, (-15:Int), ⟨false :: X, false,
          false :: (ones 8 ++ (zeros 8 ++ (true :: false :: Z)))⟩⟩ from by rfl)
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- The word `turn` consumes, minus the leading `0` that `frameFold` leaves. -/
def turnWord : List Bool :=
  [true, false, true, false, true, true, true, true, true, true, true, true, true, false, false]

/-- The word `fixedEnd` consumes, minus its leading `0`. -/
def endWord : List Bool := [true, false, true, false, true, false, true, false, true]

/-- **THE TAIL, ∀g** (2026-07-23): `frameFold ∘ turn ∘ fixedEnd` — the whole exit of the
doubling phase in `27j + 110` steps, landing on the next milestone with the frame
`(0^6 1)` digits it built.  `j` is the number of frame digits (measured: `j = g − 1`). -/
theorem tailLaw (j : Nat) (p : Int) (L Z : List Bool) :
    steps (27 * j + 110)
        ⟨.E, p, ⟨false :: frameL j (turnWord ++ (endWord ++ (zeros 11 ++ L))), false,
          zeros 4 ++ Z⟩⟩
      = some ⟨.E, p - 7 * (j : Int) - 26, ⟨zeros 10 ++ L, false,
          zeros 21 ++ (true :: (zeros 6 ++ (true :: false :: frameZ j Z)))⟩⟩ := by
  rw [show 27 * j + 110 = 27 * j + (35 + 75) from by omega, steps_add,
      frameFold j p (turnWord ++ (endWord ++ (zeros 11 ++ L))) Z, someBind, steps_add,
      show (false :: (turnWord ++ (endWord ++ (zeros 11 ++ L))))
          = false :: true :: false :: true :: false :: true :: true :: true :: true :: true ::
            true :: true :: true :: true :: false :: false :: (endWord ++ (zeros 11 ++ L))
        from rfl,
      turn (p - 7 * (j : Int)) (endWord ++ (zeros 11 ++ L)) (frameZ j Z), someBind,
      show (false :: (endWord ++ (zeros 11 ++ L))) = pow01 5 ++ (zeros 11 ++ L) from rfl,
      fixedEnd (p - 7 * (j : Int) - 15) L (true :: false :: frameZ j Z)]
  exact congrArg some (cfgPos (by omega))

-- ANTI-VACUITY (METHODS M4).  Two independent controls, both against the REAL orbit:
--
-- (a) STEP COUNTS.  j = g−1 frame digits: g=1 → 110, g=3 → 164, g=4 → 191 (measured).
--
-- (b) THE IN CONFIGURATION ITSELF (x2r3_tailin.py).  `tailLaw`'s left
--       false :: frameL j (turnWord ++ endWord ++ zeros 11 ++ L)
--     was checked cell-by-cell against the odometer's entry on the real orbit and matches
--     EXACTLY at every measured generation, with j = g−1:
--       g=1 @  732 623  j=0     g=2 @  2 851 954  j=1
--       g=3 @ 11 329 137 j=2    g=4 @ 44 986 804  j=3
--     (and the intermediate g=3 stage @11 329 164 matches at j=1, as the fold requires).
--     The right is `zeros 4 ++ Z` at all of them.  So this is the machine's own register,
--     not a shape invented to make the fold close.
example : 27 * 0 + 110 = 110 := by decide
example : 27 * 2 + 110 = 164 := by decide
example : 27 * 3 + 110 = 191 := by decide

#print axioms turn
#print axioms tailLaw
