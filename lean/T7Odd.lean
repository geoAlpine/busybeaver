import T7E3
open X2

set_option maxRecDepth 20000

/-!
# O2 — the ODD branch's macro-tile and its fold   (2026-07-24)

The odd `topEntry`'s bulk — 99.7 % of its steps — is ONE 46-step macro-tile, repeated.
Measured at g=3 (`x2o2_cycle.py`): `block = 2035 − 2n` at `rel = 161 + 46n`, uniform from
`n = 0` to `n ≈ 867`, and the whole odd decomposition

```
M6(g) --P1(88)--> --T(11)--> --rUnitsFold(15g)--> --cross(17)-->
      --carry46 × (2^{g+7}−7)--> --eChewFold × (2^{g+5}+1)--> descIn(g+6)
```

sums to `6080·2^g + 15g − 200`, the **independently confirmed** odd closed form, exactly at
g = 1, 3, 5, 7 (see the `decide`s at the end).  That closed form was confirmed out-of-sample at
g=7 BEFORE this structure was measured, so the agreement is a cross-check, not a fit.

The tile walks 16 cells left into the `ones 14` register and 6 right, restores `ones 14 · 0 0`
on top, deposits one `1 0` pair below it, and takes two cells off the block — a carry step.
-/

/-- **The odd branch's 46-step carry tile.**  `E` on the `0` above `ones 14 · 0 0 · D`, with
`1 0 1 0 1 · 1^b` to the right: consumes two block cells, deposits `1 0` under the register,
advances `+2`.  `D` and `R` untouched (the head reaches 16 left / 6 right, exactly the
concrete window). -/
theorem carry46 (p : Int) (b : Nat) (D R : List Bool) :
    steps 46 ⟨.E, p, ⟨ones 14 ++ (false :: false :: D), false,
        true :: false :: true :: false :: true :: (ones (b + 2) ++ R)⟩⟩
      = some ⟨.E, p + 2, ⟨ones 14 ++ (false :: false :: (true :: false :: D)), false,
          true :: false :: true :: false :: true :: (ones b ++ R)⟩⟩ := by
  have h0 : steps 46 (⟨.E, (0:Int), ⟨ones 14 ++ (false :: false :: D), false,
      true :: false :: true :: false :: true :: (ones (b + 2) ++ R)⟩⟩ : Cfg)
      = some ⟨.E, (2:Int), ⟨ones 14 ++ (false :: false :: (true :: false :: D)), false,
          true :: false :: true :: false :: true :: (ones b ++ R)⟩⟩ := by
    rw [show ones (b + 2) = true :: true :: ones b from by
          rw [show b + 2 = 2 + b from by omega, ones_add]; rfl]
    rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The odd carry FOLD, `∀n`** — `n` tiles = `46n` steps take `2n` cells off the block and
lay down `pow10 n` under the `ones 14` register, advancing `+2n`.  This is the odd branch's
`Θ(2^g)` bulk. -/
theorem carryFold46 : ∀ (n : Nat) (p : Int) (b : Nat) (D R : List Bool),
    steps (46 * n) ⟨.E, p, ⟨ones 14 ++ (false :: false :: D), false,
        true :: false :: true :: false :: true :: (ones (2 * n + b) ++ R)⟩⟩
      = some ⟨.E, p + 2 * (n : Int),
          ⟨ones 14 ++ (false :: false :: (pow10 n ++ D)), false,
           true :: false :: true :: false :: true :: (ones b ++ R)⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p b D R
    show some (⟨.E, p, ⟨ones 14 ++ (false :: false :: D), false,
        true :: false :: true :: false :: true :: (ones (2 * 0 + b) ++ R)⟩⟩ : Cfg) = _
    simp only [Nat.mul_zero, Nat.zero_add]
    refine congrArg some ?_
    show (⟨.E, p, ⟨_, false, _⟩⟩ : Cfg) = ⟨.E, _, ⟨_, false, _⟩⟩
    refine cfgPos ?_
    push_cast; omega
  | succ n ih =>
    intro p b D R
    rw [show 46 * (n + 1) = 46 + 46 * n from by omega, steps_add,
        show 2 * (n + 1) + b = (2 * n + b) + 2 from by omega,
        carry46 p (2 * n + b) D R, someBind,
        ih (p + 2) b (true :: false :: D) R]
    refine congrArg some ?_
    show (⟨.E, _, ⟨ones 14 ++ (false :: false :: (pow10 n ++ (true :: false :: D))), false, _⟩⟩ : Cfg)
      = ⟨.E, _, ⟨ones 14 ++ (false :: false :: (pow10 (n + 1) ++ D)), false, _⟩⟩
    rw [show (pow10 n ++ (true :: false :: D) : List Bool) = pow10 (n + 1) ++ D from by
          rw [show n + 1 = n + 1 from rfl, pow10_add, List.append_assoc]; rfl]
    exact cfgPos (by push_cast; omega)

-- ANTI-VACUITY (METHODS M4).  The odd decomposition's total IS the confirmed closed form
--   88 + 11 + 15g + 17 + 46·(2^{g+7}−7) + 6·(2^{g+5}+1)  =  6080·2^g + 15g − 200
-- at every odd g measured (the closed form was confirmed out-of-sample at g=7 first).
example : 88 + 11 + 15*1 + 17 + 46*(2^(1+7)-7) + 6*(2^(1+5)+1) = 6080*2^1 + 15*1 - 200 := by decide
example : 88 + 11 + 15*3 + 17 + 46*(2^(3+7)-7) + 6*(2^(3+5)+1) = 6080*2^3 + 15*3 - 200 := by decide
example : 88 + 11 + 15*5 + 17 + 46*(2^(5+7)-7) + 6*(2^(5+5)+1) = 6080*2^5 + 15*5 - 200 := by decide
example : 88 + 11 + 15*7 + 17 + 46*(2^(7+7)-7) + 6*(2^(7+5)+1) = 6080*2^7 + 15*7 - 200 := by decide
-- and the measured g=3 tile count and phase boundary
example : 46 * (2^(3+7) - 7) = 46782 := by decide
example : 161 + 46782 = 46943 := by decide

#print axioms carry46
#print axioms carryFold46

/-! ### The `(10)^10` crossing — the odd branch's one remaining fixed episode -/

/-- **`cross17`** — the 17-step episode between `rUnitsFold` and the carry fold: crosses the
odd `M6`'s `(10)^10` block, builds the `ones 14 · 0 0 · 1` register the carry tile runs on,
and hands over `1 0 1 0 1 · 1^b`.  Consumes ONE block cell.  The head only moves RIGHT
(excursion 0 left / 17 right), so `L` is genuinely free. -/
theorem cross17 (p : Int) (b : Nat) (L R : List Bool) :
    steps 17 ⟨.E, p, ⟨L, false, pow01 10 ++ (false :: (ones (b + 1) ++ R))⟩⟩
      = some ⟨.E, p + 17, ⟨ones 14 ++ (false :: false :: true :: L), false,
          true :: false :: true :: false :: true :: (ones b ++ R)⟩⟩ := by
  have h0 : steps 17 (⟨.E, (0:Int), ⟨L, false,
      pow01 10 ++ (false :: (ones (b + 1) ++ R))⟩⟩ : Cfg)
      = some ⟨.E, (17:Int), ⟨ones 14 ++ (false :: false :: true :: L), false,
          true :: false :: true :: false :: true :: (ones b ++ R)⟩⟩ := by
    rw [show ones (b + 1) = true :: ones b from by
          rw [show b + 1 = 1 + b from by omega, ones_add]; rfl]
    rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **`crossCarry`** — `cross17 ∘ carryFold46`: the odd branch's whole `Θ(2^g)` middle, from
the `(10)^10` block to the exhausted carry register. -/
theorem crossCarry (n : Nat) (p : Int) (b : Nat) (L R : List Bool) :
    steps (17 + 46 * n) ⟨.E, p, ⟨L, false, pow01 10 ++ (false :: (ones (2 * n + b + 1) ++ R))⟩⟩
      = some ⟨.E, p + 17 + 2 * (n : Int),
          ⟨ones 14 ++ (false :: false :: (pow10 n ++ (true :: L))), false,
           true :: false :: true :: false :: true :: (ones b ++ R)⟩⟩ := by
  rw [steps_add, cross17 p (2 * n + b) L R, someBind,
      carryFold46 n (p + 17) b (true :: L) R]

#print axioms cross17
#print axioms crossCarry
