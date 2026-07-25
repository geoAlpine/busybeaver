import T7S3
open X2

set_option maxRecDepth 20000

/-!
# `p1t` with a FREE left tail (METHODS M6 — rename-to-generalize)  (2026-07-24)

Measured: `p1t`'s head only ever moves RIGHT (chunk boundaries at pos 0/5/10/15/19, the left
list only grows), so the left tail below `M6`'s base `[false]` is never read.  Freeing it lets
`topEntryEven` deliver a marker with any number of trailing left blanks — which is exactly what
`evenSpine`/`tailLaw` need (`zeros 11` vs the bare `zeros 1`), with NO `BlankNorm` detour.
-/

private theorem p1tLLc0 (LL REST : List Bool) :
    steps 25 ⟨.E, 0, ⟨[false] ++ LL, false, [false, true, false, true, false, true, false, true, false, true, true, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.E, 5, ⟨[false, false, true, false, true, false] ++ LL, false, [true, false, true, false, true, false, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩ := by rfl

private theorem p1tLLc1 (LL REST : List Bool) :
    steps 25 ⟨.E, 5, ⟨[false, false, true, false, true, false] ++ LL, false, [true, false, true, false, true, false, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.F, 10, ⟨[true, true, true, false, false, true, false, true, false, true, false] ++ LL, true, [false, true, false, true, true, true, true, true, false, false] ++ REST⟩⟩ := by rfl

private theorem p1tLLc2 (LL REST : List Bool) :
    steps 25 ⟨.F, 10, ⟨[true, true, true, false, false, true, false, true, false, true, false] ++ LL, true, [false, true, false, true, true, true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.E, 15, ⟨[true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false] ++ LL, false, [true, true, true, false, false] ++ REST⟩⟩ := by rfl

private theorem p1tLLc3 (LL REST : List Bool) :
    steps 24 ⟨.E, 15, ⟨[true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false] ++ LL, false, [true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.E, 19, ⟨[true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false, true, false] ++ LL, false, [false] ++ REST⟩⟩ := by rfl

/-- **`p1t`** — the fixed 99-step opening of `topEntry` (P1 ∘ T), `g`-independent, `∀ REST`. -/
theorem p1tLL (p : Int) (LL REST : List Bool) :
    steps 99 ⟨.E, p, ⟨[false] ++ LL, false,
        false :: (pow10 4 ++ (ones 9 ++ (false :: false :: REST)))⟩⟩
      = some ⟨.E, p + 19, ⟨[true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false, true, false] ++ LL, false, [false] ++ REST⟩⟩ := by
  have h0 : steps 99 ⟨.E, 0, ⟨[false] ++ LL, false, [false, true, false, true, false, true, false, true, false, true, true, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩ = some ⟨.E, 19, ⟨[true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false, true, false] ++ LL, false, [false] ++ REST⟩⟩ := by
    rw [show (99:Nat) = 25 + (25 + (25 + 24)) from by decide, steps_add, p1tLLc0 LL REST, someBind,
        steps_add, p1tLLc1 LL REST, someBind, steps_add, p1tLLc2 LL REST, someBind]
    exact p1tLLc3 LL REST
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  show steps 99 ⟨.E, p, ⟨[false] ++ LL, false, [false, true, false, true, false, true, false, true, false, true, true, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩ = _
  rw [h]
  exact congrArg some (cfgPos (by omega))


#print axioms p1tLL
