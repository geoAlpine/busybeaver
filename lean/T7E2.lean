import T7E1
open X2

set_option maxRecDepth 20000

/-!
# R2 / E2 — the second fixed episode of the doubling phase  (2026-07-23)

`cascadeReg 4 → regenIn 5` in **215 steps**.  MEASURED at g=2 (739 441 → 739 656) and
g=3 (2 905 677 → 2 905 892), bit-identical over ±64 cells at both generations.

Head excursion over the episode: `−11 ≤ pos ≤ 17`, against a concrete left prefix of 14
cells (`pow01 7`) and right of 35 — so neither `M` nor `R` is ever read, and the episode
is a genuine `∀ M R` transport.  Nine `rfl` chunks (8×25 + 15) at position 0, lifted to
`∀ p` by `steps_pos_shift`.

The OUT is `regenIn 5` exactly when the incoming marker has the shape
`0 0 1 · (01)^14 · marker` — which is what the real orbit presents (`x2r2_ep.py`).
`E2_raw` states the transport with no condition on `M`; `E2` specialises it.
-/

private theorem e2c0 (M R : List Bool) :
    steps 25 ⟨.E, 0, ⟨[false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.E, 7, ⟨[true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, true, [true, true, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c1 (M R : List Bool) :
    steps 25 ⟨.E, 7, ⟨[true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, true, [true, true, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.C, 6, ⟨[true, true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, true, false, true] ++ M, true, [false, true, false, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c2 (M R : List Bool) :
    steps 25 ⟨.C, 6, ⟨[true, true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, true, false, true] ++ M, true, [false, true, false, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.E, 9, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, true] ++ M, false, [true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c3 (M R : List Bool) :
    steps 25 ⟨.E, 9, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, true] ++ M, false, [true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.F, -2, ⟨[true, true, true, true, true, true, false, true, false, true, false, true] ++ M, true, [false, true, false, true, false, true, false, true, false, true, false, true, false, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c4 (M R : List Bool) :
    steps 25 ⟨.F, -2, ⟨[true, true, true, true, true, true, false, true, false, true, false, true] ++ M, true, [false, true, false, true, false, true, false, true, false, true, false, true, false, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.E, 3, ⟨[true, true, true, true, true, true, true, true, true, true, true, false, true, false, true, false, true] ++ M, true, [true, false, true, false, true, false, true, false, true, false, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c5 (M R : List Bool) :
    steps 25 ⟨.E, 3, ⟨[true, true, true, true, true, true, true, true, true, true, true, false, true, false, true, false, true] ++ M, true, [true, false, true, false, true, false, true, false, true, false, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.F, 4, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, true] ++ M, true, [false, true, false, true, false, true, false, true, false, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c6 (M R : List Bool) :
    steps 25 ⟨.F, 4, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, true] ++ M, true, [false, true, false, true, false, true, false, true, false, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.E, 1, ⟨[true, true, true, true, true, true, true, true, true, true, true, false, true, false, true] ++ M, true, [true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c7 (M R : List Bool) :
    steps 25 ⟨.E, 1, ⟨[true, true, true, true, true, true, true, true, true, true, true, false, true, false, true] ++ M, true, [true, false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.F, 2, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true] ++ M, true, [false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e2c8 (M R : List Bool) :
    steps 15 ⟨.F, 2, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true] ++ M, true, [false, true, false, true, false, true, false, true, false, true, false, true, false, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.E, 17, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true] ++ M, false, [false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

/-- `E2` at position 0, no condition on the marker. -/
theorem E2_zero (M R : List Bool) :
    steps 215 (cascadeReg 4 1 0 M R) = some ⟨.E, 17, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true] ++ M, false, [false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by
  show steps 215 ⟨.E, 0, ⟨[false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ = _
  rw [
      show (215:Nat) = 25 + 190 from rfl, steps_add, e2c0 M R, someBind,
      show (190:Nat) = 25 + 165 from rfl, steps_add, e2c1 M R, someBind,
      show (165:Nat) = 25 + 140 from rfl, steps_add, e2c2 M R, someBind,
      show (140:Nat) = 25 + 115 from rfl, steps_add, e2c3 M R, someBind,
      show (115:Nat) = 25 + 90 from rfl, steps_add, e2c4 M R, someBind,
      show (90:Nat) = 25 + 65 from rfl, steps_add, e2c5 M R, someBind,
      show (65:Nat) = 25 + 40 from rfl, steps_add, e2c6 M R, someBind,
      show (40:Nat) = 25 + 15 from rfl, steps_add, e2c7 M R, someBind]
  exact e2c8 M R

/-- **R2 / E2 (raw) — the 215-step transport, ∀ position, ∀ marker, ∀ tail.** -/
theorem E2_raw (p : Int) (M R : List Bool) :
    steps 215 (cascadeReg 4 1 p M R)
      = some ⟨.E, p + 17, ((⟨.E, 17, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true] ++ M, false, [false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ : Cfg).tape)⟩ := by
  have h := steps_pos_shift (d := p) (E2_zero M R)
  rw [show (0:Int) + p = p from by omega] at h
  show steps 215 ⟨.E, p, ⟨pow01 (1 + (2 ^ (4 - 1) - 2)) ++ M, false,
      false :: false :: false :: (ones (2 ^ 4 - 3) ++ (false :: false ::
        (descCascade (4 - 3) ++ (false :: false :: (zeros 7 ++ R)))))⟩⟩ = _
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **R2 / E2 — `cascadeReg 4 → regenIn 5`**, for the marker shape the real orbit presents. -/
theorem E2 (p : Int) (marker R : List Bool) :
    steps 215 (cascadeReg 4 1 p (false :: false :: true :: (pow01 14 ++ marker)) R)
      = some (regenIn 5 (p + 17) 9 marker R) := by
  rw [E2_raw p (false :: false :: true :: (pow01 14 ++ marker)) R]
  rfl

#print axioms E2_zero
#print axioms E2_raw
#print axioms E2

/-! ### Composition — `regenEntry`, and then the WHOLE head -/

/-- The descent's accumulated marker, minus the fixed `0 0 1 · (01)^14` head that `regenIn 5`
consumes.  `descMarkStep 0 X = 0 0 1 · (01)^1 (01)^5 (01)^8 · X` and `1 + 5 + 8 = 14` exactly —
the descent hands the ladder precisely the comb `regenIn 5` asks for. -/
def descMarkInner : Nat → List Bool → List Bool
  | 0, M => M
  | n + 1, M => descMarkInner n (descMarkStep (n + 1) M)

theorem descMark_shape : ∀ (n : Nat) (M : List Bool),
    descMark n M = false :: false :: true :: (pow01 14 ++ descMarkInner n M) := by
  intro n
  induction n with
  | zero => intro M; rfl
  | succ n ih => intro M; exact ih (descMarkStep (n + 1) M)

/-- **R2 / `regenEntry` — `descIn 3 → regenIn 5` in 415 steps** = `E1 ∘ E2`.
The design doc booked this as one opaque ~615-step episode; measurement showed 613, of which
135 + 63 are two more `descLaw` rungs and only these 415 steps are genuinely new. -/
theorem regenEntry (p : Int) (marker R : List Bool) :
    steps 415 (descIn 3 p (false :: false :: true :: (pow01 14 ++ marker)) (zeros 25 ++ R))
      = some (regenIn 5 (p + 23) 9 marker R) := by
  rw [show (415:Nat) = 200 + 215 from rfl, steps_add,
      E1 p (false :: false :: true :: (pow01 14 ++ marker)) R, someBind, E2 (p + 6) marker R]
  exact congrArg some (cfgPos (by omega))

/-- **THE WHOLE HEAD OF THE DOUBLING PHASE, ∀k** (2026-07-23): from the descent's entry
milestone `descIn (n+4)` all the way to `regenIn 5`, where the PROVEN ladder
(`T7Ladder.ladderToCascade`) takes over.  `descTotal n + 415` steps.

This is `DescFold` (R1) ∘ `E1` ∘ `E2` (R2) — every factor `∀`, `R` untouched throughout. -/
theorem headLaw (n : Nat) (p : Int) (M R : List Bool) :
    steps (descTotal n + 415) (descIn (n + 4) p M (zeros 25 ++ R))
      = some (regenIn 5 (descPosF n p + 23) 9 (descMarkInner n M) R) := by
  rw [steps_add, descFold_all n p M (zeros 25 ++ R), someBind, descMark_shape n M,
      regenEntry (descPosF n p) (descMarkInner n M) R]

-- ANTI-VACUITY (METHODS M4): the composed head cost against the MEASURED g=2 head.
-- descIn 9 @734759 -> regenIn 5 @739656 is 4897 steps = descTotal 5 + 415 = 4482 + 415.
example : descTotal 5 + 415 = 4897 := by decide
-- and the design doc's own total: 1683 (topEntry) + 4897 = 6580, the measured head.
example : 1683 + 4897 = 6580 := by decide

#print axioms descMark_shape
#print axioms regenEntry
#print axioms headLaw
