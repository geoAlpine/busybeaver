import T7P1TLL
import T7TopEntry
import T7Spine
open X2

set_option maxRecDepth 40000

/-!
# E2 — `topEntryEven`'s OUT meets `evenSpine`'s IN   (2026-07-24)

**M7 audit result.**  `topEntryEven` lands on `descIn (2h+9)` with marker `teM h`, and
(measured + `#eval`-checked at h = 0..3)

```
teM h  =  0 0 1 · (9-cell seam) · frameL (2h+1) (turnWord ++ endWord ++ zeros 1)
```

which is EXACTLY `evenSpine`'s IN marker except that `evenSpine` carries `zeros 11 ++ L`
where `topEntry` delivers `zeros 1`.  The two are the same abstract tape (the model reads `0`
past a finite list) but different finite lists.

**The fix uses M6 (rename-to-generalize), not `BlankNorm`.**  `p1t`'s head only ever moves
right, so `M6`'s left base `[false]` is inert — `p1tLL` frees it to `[false] ++ LL`.  Threading
`LL` through the four phases makes `topEntry` deliver `… zeros 1 ++ LL`, and `LL := zeros 10`
gives `zeros 11` on the nose.  No blank-normalisation detour, no `∃ j ≤ k`.
-/

/-! ### The `LL`-threaded boundaries -/

/-- **A** — `M6 (2h+2)` with `LL` extra left blanks below its base. -/
def tlA (h : Nat) (LL : List Bool) : Cfg :=
  ⟨.E, -5, ⟨[false] ++ LL, false,
    false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
      (rUnits (2 * h + 2 + 1) ++
       (true :: false :: false ::
        (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h))))))⟩⟩

/-- **B** — after `p1tLL`. -/
def tlB (h : Nat) (LL : List Bool) : Cfg :=
  ⟨.E, -5 + 19, ⟨p1tL ++ LL, false,
    false :: (rUnits (2 * h + 2 + 1) ++
      (true :: false :: false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h)))⟩⟩

/-- **C** — after `rUnitsFold`. -/
def tlC (h : Nat) (LL : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 2 + 1 : Nat) : Int),
    ⟨rUnitsDep (2 * h + 2 + 1) (p1tL ++ LL), false,
     false :: (true :: false :: false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h))⟩⟩

/-- **D** — after `bridge`. -/
def tlD (h : Nat) (LL : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 2 + 1 : Nat) : Int) + 3,
    ⟨false :: false :: true :: rUnitsDep (2 * h + 2 + 1) (p1tL ++ LL), false,
     false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h)⟩⟩

/-- The marker `topEntry` delivers, with `LL` threaded. -/
def tlM (h : Nat) (LL : List Bool) : List Bool :=
  false :: false :: true :: rUnitsDep (2 * h + 2 + 1) (p1tL ++ LL)

/-- `M6` at even `g`, with `LL` extra left blanks, IS `tlA`. -/
theorem M6_evenL (h : Nat) (LL : List Bool) :
    (⟨.E, -5, ⟨[false] ++ LL, false, (M6 (2 * h + 2)).tape.right⟩⟩ : Cfg) = tlA h LL := by
  have e : (M6 (2 * h + 2)).tape.right = (teA h).tape.right := by rw [M6_even h]
  unfold tlA
  rw [e]
  rfl

theorem tlAB (h : Nat) (LL : List Bool) : steps 99 (tlA h LL) = some (tlB h LL) := by
  unfold tlA tlB
  exact p1tLL (-5) LL (rUnits (2*h+2+1) ++
    (true :: false :: false :: (ones (2 ^ (2*h+2+8) - 3) ++ teTail h)))

theorem tlBC (h : Nat) (LL : List Bool) :
    steps (15 * (2 * h + 2 + 1)) (tlB h LL) = some (tlC h LL) := by
  unfold tlB tlC
  exact rUnitsFold (2*h+2+1) (-5 + 19) (p1tL ++ LL)
    (true :: false :: false :: (ones (2 ^ (2*h+2+8) - 3) ++ teTail h))

theorem tlCD (h : Nat) (LL : List Bool) : steps 3 (tlC h LL) = some (tlD h LL) := by
  unfold tlC tlD
  exact bridge _ (2 ^ (2*h+2+8) - 3) _ (teTail h)

theorem tlDdescIn (h : Nat) (LL : List Bool) :
    steps (6 * 2 ^ (2 * h + 2 + 6)) (tlD h LL)
      = some (descIn (2 * h + 9) (teP h) (tlM h LL) []) := by
  have hsplit : (2 : Nat) ^ (2 * h + 2 + 8) - 3
      = 2 * 2 ^ (2 * h + 2 + 6) + (2 ^ (2 * h + 2 + 7) - 3) := by
    have e6 : (2:Nat)^(2*h+2+8) = 4 * 2^(2*h+2+6) := by
      rw [show 2*h+2+8 = (2*h+2+6)+2 from by omega, Nat.pow_add,
          show (2:Nat)^2 = 4 from rfl, Nat.mul_comm]
    have e7 : (2:Nat)^(2*h+2+7) = 2 * 2^(2*h+2+6) := by
      rw [show 2*h+2+7 = (2*h+2+6)+1 from by omega, Nat.pow_add,
          show (2:Nat)^1 = 2 from rfl, Nat.mul_comm]
    have h6 : 4 ≤ (2:Nat)^(2*h+2+6) := by
      have : (2:Nat)^2 ≤ 2^(2*h+2+6) := Nat.pow_le_pow_right (by decide) (by omega)
      omega
    omega
  unfold tlD
  rw [hsplit,
      eChewFold (2 ^ (2*h+2+6)) _ (2 ^ (2*h+2+7) - 3)
        (false :: false :: true :: rUnitsDep (2*h+2+1) (p1tL ++ LL)) (teTail h)]
  refine congrArg some ?_
  show (⟨.E, _, ⟨pow01 (2 ^ (2*h+2+6)) ++ tlM h LL, false,
      false :: (ones (2 ^ (2*h+2+7) - 3) ++ teTail h)⟩⟩ : Cfg) = _
  show _ = (⟨.E, teP h, ⟨pow01 (2 ^ (2*h+9 - 1)) ++ tlM h LL, false,
      false :: (ones (2 ^ (2*h+9) - 3) ++
        (false :: false :: (descCascade (2*h+9 - 2) ++ [])))⟩⟩ : Cfg)
  rw [show 2*h+9-1 = 2*h+2+6 from by omega, show 2*h+9 = 2*h+2+7 from by omega,
      show 2*h+2+7-2 = 2*h+7 from by omega]
  show (⟨.E, _, ⟨_, false, false :: (ones (2 ^ (2*h+2+7) - 3) ++ teTail h)⟩⟩ : Cfg) = _
  unfold teTail teP
  rw [List.append_nil]

/-- **`topEntryEvenL`** — `topEntryEven` with `LL` extra left blanks threaded through. -/
theorem topEntryEvenL (h : Nat) (LL : List Bool) :
    steps (99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6))))
        ⟨.E, -5, ⟨[false] ++ LL, false, (M6 (2 * h + 2)).tape.right⟩⟩
      = some (descIn (2 * h + 9) (teP h) (tlM h LL) []) := by
  rw [M6_evenL h LL, steps_add, tlAB h LL, someBind, steps_add, tlBC h LL, someBind,
      steps_add, tlCD h LL, someBind]
  exact tlDdescIn h LL

/-! ### The marker identity — `topEntry`'s OUT IS the spine's IN -/

/-- The spine's IN marker word, named. -/
def spineMk (j : Nat) (Z : List Bool) : List Bool :=
  false :: false :: true ::
    (false :: false :: true :: false :: true :: false :: true :: false :: false ::
      frameL j (turnWord ++ (endWord ++ Z)))

/-- **E2's core identity** — the marker `topEntry` delivers IS the spine's, with `Z = zeros 1 ++ LL`.
`rUnitsDep n` lays down `n` copies of `0 0 1 0 1 0 1`; the spine's `frameL j` lays down `j` copies
of `1 0 1 0 1 0 0`.  Offset by the fixed 9-cell seam these are the same word, with `j = 2h+1`. -/
theorem rUnitsDep_frameL : ∀ (h : Nat) (LL : List Bool),
    rUnitsDep (2 * h + 3) (p1tL ++ LL)
      = (false :: false :: true :: false :: true :: false :: true :: false :: false :: []) ++
          frameL (2 * h + 1) (turnWord ++ (endWord ++ (zeros 1 ++ LL))) := by
  intro h
  induction h with
  | zero => intro LL; rfl
  | succ h ih =>
    intro LL
    rw [show 2 * (h + 1) + 3 = (2 * h + 3) + 2 from by omega,
        show 2 * (h + 1) + 1 = (2 * h + 1) + 2 from by omega]
    show false :: false :: true :: false :: true :: false :: true ::
        (false :: false :: true :: false :: true :: false :: true ::
          rUnitsDep (2 * h + 3) (p1tL ++ LL)) = _
    rw [ih LL]
    rfl

/-- **E2's core identity** — the marker `topEntry` delivers IS the spine's IN marker,
with `Z = zeros 1 ++ LL`.  Hence `LL := zeros 10` gives the spine's `zeros 11` exactly. -/
theorem tlM_spineMk (h : Nat) (LL : List Bool) :
    tlM h LL = spineMk (2 * h + 1) (zeros 1 ++ LL) := by
  show false :: false :: true :: rUnitsDep (2 * h + 2 + 1) (p1tL ++ LL) = _
  rw [show 2 * h + 2 + 1 = 2 * h + 3 from by omega, rUnitsDep_frameL h LL]
  rfl

#print axioms M6_evenL
#print axioms tlAB
#print axioms tlBC
#print axioms tlCD
#print axioms tlDdescIn
#print axioms topEntryEvenL
#print axioms rUnitsDep_frameL
#print axioms tlM_spineMk

/-! ### E2 — `topEntry` hands the spine exactly its IN marker -/

/-- `zeros 1 ++ zeros 10 = zeros 11` — the whole content of the "BlankNorm gap". -/
theorem zeros_1_10 : (zeros 1 ++ zeros 10 : List Bool) = zeros 11 := by
  rw [← zeros_add]

/-- **E2 — CLOSED.**  With `LL := zeros 10`, `topEntry`'s OUT marker IS `evenSpine`'s IN marker
(`spineMk (2h+1) (zeros 11)`).  The apparent 10-cell mismatch was purely the finite-list spelling
of trailing left blanks, and freeing `p1t`'s inert left base closes it exactly — no `BlankNorm`
existential, no `∃ j ≤ k`. -/
theorem topEntry_meets_spine (h : Nat) :
    steps (99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6))))
        ⟨.E, -5, ⟨[false] ++ zeros 10, false, (M6 (2 * h + 2)).tape.right⟩⟩
      = some (descIn (2 * h + 9) (teP h) (spineMk (2 * h + 1) (zeros 11)) []) := by
  rw [topEntryEvenL h (zeros 10), tlM_spineMk h (zeros 10), zeros_1_10]

-- ANTI-VACUITY (METHODS M4): at g=2 (h=0) the spine's own IN marker is 54 cells and the
-- measured on-orbit descIn-9 marker is its 44-cell prefix (the rest is trailing blank).
example : (spineMk 1 (zeros 11)).length = 54 := by decide
example : (tlM 0 []).length = 44 := by decide

#print axioms zeros_1_10
#print axioms topEntry_meets_spine
