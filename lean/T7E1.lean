import T7DLaw
open X2

set_option maxRecDepth 20000

/-!
# R2 / E1 — the first fixed episode of the doubling phase  (2026-07-23)

`descIn 3 → cascadeReg 4` in **200 steps**.  MEASURED on the real orbit at g=2 (step
739 241 → 739 441) and g=3 (2 905 477 → 2 905 677); at both endpoints the tape is
bit-identical over ±64 cells at the two generations, only the absolute position differs
(`x2r2_ep.py`) — the episode is genuinely level-free, which is why it can be stated
with `∀ M R` and lifted to `∀ p` by `steps_pos_shift`.

Proved by eight 25-step `rfl` chunks at position 0.  Chunking is forced: a single
200-step `rfl` blows the elaborator (measured 0.28 s at 25 steps, 4.3 s at 50, >39 s
and failing at 100).  The head's excursion over the episode is `0 ≤ pos ≤ 33` and the
concrete right padding is 41 cells, so neither `M` nor `R` is ever read — which is
exactly what makes the `∀ M R` statement provable rather than merely true at `[]`.
-/

private theorem e1c0 (M R : List Bool) :
    steps 25 ⟨.E, 0, ⟨[false, true, false, true, false, true, false, true] ++ M, false, [false, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.C, 11, ⟨[false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e1c1 (M R : List Bool) :
    steps 25 ⟨.C, 11, ⟨[false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.A, 18, ⟨[false, true, false, true, false, false, true, false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e1c2 (M R : List Bool) :
    steps 25 ⟨.A, 18, ⟨[false, true, false, true, false, false, true, false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.D, 15, ⟨[true, false, false, true, false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [true, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e1c3 (M R : List Bool) :
    steps 25 ⟨.D, 15, ⟨[true, false, false, true, false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [true, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.E, 12, ⟨[true, false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [true, false, true, false, true, false, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e1c4 (M R : List Bool) :
    steps 25 ⟨.E, 12, ⟨[true, false, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [true, false, true, false, true, false, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.F, 17, ⟨[true, true, true, true, true, true, true, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, true, [false, true, false, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e1c5 (M R : List Bool) :
    steps 25 ⟨.F, 17, ⟨[true, true, true, true, true, true, true, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, true, [false, true, false, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.A, 26, ⟨[false, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, true, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e1c6 (M R : List Bool) :
    steps 25 ⟨.A, 26, ⟨[false, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, true, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.D, 23, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [true, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

private theorem e1c7 (M R : List Bool) :
    steps 25 ⟨.D, 23, ⟨[true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [true, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩
      = some ⟨.E, 6, ⟨[false, true, false, true, false, true, false, true, false, true, false, true, false, true] ++ M, false, [false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ := by rfl

/-- `E1` at position 0: eight chunks chained by `steps_add`. -/
theorem E1_zero (M R : List Bool) :
    steps 200 (descIn 3 0 M (zeros 25 ++ R)) = some (cascadeReg 4 1 6 M R) := by
  show steps 200 ⟨.E, 0, ⟨[false, true, false, true, false, true, false, true] ++ M, false, [false, true, true, true, true, true, false, false, true, true, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false] ++ R⟩⟩ = _
  rw [
      show (200:Nat) = 25 + 175 from rfl, steps_add, e1c0 M R, someBind,
      show (175:Nat) = 25 + 150 from rfl, steps_add, e1c1 M R, someBind,
      show (150:Nat) = 25 + 125 from rfl, steps_add, e1c2 M R, someBind,
      show (125:Nat) = 25 + 100 from rfl, steps_add, e1c3 M R, someBind,
      show (100:Nat) = 25 + 75 from rfl, steps_add, e1c4 M R, someBind,
      show (75:Nat) = 25 + 50 from rfl, steps_add, e1c5 M R, someBind,
      show (50:Nat) = 25 + 25 from rfl, steps_add, e1c6 M R, someBind]
  exact e1c7 M R

/-- **R2 / E1 — `descIn 3 → cascadeReg 4`, ∀ position, ∀ marker, ∀ tail.**  200 steps. -/
theorem E1 (p : Int) (M R : List Bool) :
    steps 200 (descIn 3 p M (zeros 25 ++ R)) = some (cascadeReg 4 1 (p + 6) M R) := by
  have h := steps_pos_shift (d := p) (E1_zero M R)
  rw [show (0:Int) + p = p from by omega] at h
  show steps 200 ⟨.E, p, ⟨pow01 (2 ^ (3 - 1)) ++ M, false,
      false :: (ones (2 ^ 3 - 3) ++
        (false :: false :: (descCascade (3 - 2) ++ (zeros 25 ++ R))))⟩⟩ = _
  rw [h]
  exact congrArg some (cfgPos (by omega))

#print axioms E1_zero
#print axioms E1
