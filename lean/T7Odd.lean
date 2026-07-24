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

/-! ### M8 — the odd `topEntry`, assembled at named boundaries

Odd `M6 g` right = `0 · (10)^4 · 1^9 · 00 · rUnits g · (10)^10 · 1^{2^{g+8}−13} · m1casc(g+6)(g+7)`.

The one seam needing an identity is `rUnitsFold` → `cross17`: the former leaves
`false :: pow10 10 ++ …`, the latter wants `pow01 10 ++ (false :: …)`, and those are equal
(`false_pow10`, the general `0 :: (10)^n = (01)^n :: 0`). -/

/-- `0 :: (10)^n · X = (01)^n · 0 · X` — `false_pow10` with a tail. -/
theorem false_pow10_tail (n : Nat) (X : List Bool) :
    false :: (pow10 n ++ X) = pow01 n ++ (false :: X) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    show false :: (true :: false :: (pow10 n ++ X)) = false :: true :: (pow01 n ++ (false :: X))
    rw [← ih]

/-- **A** — odd `M6 (2h+3)` with the `if`s reduced and `m1casc` turned into `descCascade`. -/
def odA (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5, ⟨[false] ++ LL, false,
    false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
      (rUnits (2 * h + 3) ++
       (pow10 10 ++
        (ones (2 ^ (2 * h + 3 + 8) - 13) ++
          (false :: false :: (descCascade (2 * h + 8) ++ TT))))))))⟩⟩

/-- **B** — after `p1t`. -/
def odB (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5 + 19, ⟨p1tL ++ LL, false,
    false :: (rUnits (2 * h + 3) ++
      (pow10 10 ++
       (ones (2 ^ (2 * h + 3 + 8) - 13) ++
         (false :: false :: (descCascade (2 * h + 8) ++ TT)))))⟩⟩

/-- **C** — after `rUnitsFold`: head on the `0` before `(10)^10`. -/
def odC (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 3 : Nat) : Int),
    ⟨rUnitsDep (2 * h + 3) (p1tL ++ LL), false,
     false :: (pow10 10 ++
       (ones (2 ^ (2 * h + 3 + 8) - 13) ++
         (false :: false :: (descCascade (2 * h + 8) ++ TT))))⟩⟩

/-- `M6` at odd `g = 2h+3` IS `odA`. -/
theorem M6_odd (h : Nat) (LL : List Bool) :
    (⟨.E, -5, ⟨[false] ++ LL, false, (M6 (2 * h + 3)).tape.right⟩⟩ : Cfg) = odA h LL [] := by
  have hmod : (2 * h + 3) % 2 = 1 := by omega
  have hne : ¬ ((2 * h + 3) % 2 = 0) := by omega
  have e : (M6 (2 * h + 3)).tape.right
      = false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
          (rUnits (2 * h + 3) ++
           (pow10 10 ++
            (ones (2 ^ (2 * h + 3 + 8) - 13) ++
              (false :: false :: (descCascade (2 * h + 8) ++ [])))))))) := by
    show false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
        (rUnits (if (2*h+3) % 2 = 0 then (2*h+3) + 1 else (2*h+3)) ++
         ((if (2*h+3) % 2 = 0 then true :: false :: false :: [] else pow10 10) ++
          (ones (if (2*h+3) % 2 = 0 then 2 ^ ((2*h+3) + 8) - 3 else 2 ^ ((2*h+3) + 8) - 13) ++
           m1casc ((2*h+3) + 6) ((2*h+3) + 7) [])))))) = _
    rw [if_neg hne, if_neg hne, if_neg hne,
        show (2*h+3)+6 = (2*h+8)+1 from by omega,
        show (2*h+3)+7 = (2*h+8)+2 from by omega,
        m1casc_descCascade_tail (2*h+8) []]
  unfold odA
  rw [e]

theorem odAB (h : Nat) (LL TT : List Bool) : steps 99 (odA h LL TT) = some (odB h LL TT) := by
  unfold odA odB
  exact p1tLL (-5) LL (rUnits (2*h+3) ++
    (pow10 10 ++ (ones (2 ^ (2*h+3+8) - 13) ++
      (false :: false :: (descCascade (2*h+8) ++ TT)))))

theorem odBC (h : Nat) (LL TT : List Bool) :
    steps (15 * (2 * h + 3)) (odB h LL TT) = some (odC h LL TT) := by
  unfold odB odC
  exact rUnitsFold (2*h+3) (-5 + 19) (p1tL ++ LL)
    (pow10 10 ++ (ones (2 ^ (2*h+3+8) - 13) ++
      (false :: false :: (descCascade (2*h+8) ++ TT))))

#print axioms false_pow10_tail
#print axioms M6_odd
#print axioms odAB
#print axioms odBC

/-- **C → the carry register exhausted** — `crossCarry` at the odd block.  `cross17` eats one
cell and the fold eats `2n` with `n = 2^{g+7}−7`, and `1 + 2n = 2^{g+8}−13` exactly: the big
block is consumed to the last cell, leaving `b = 0`. -/
theorem odCcarry (h : Nat) (LL TT : List Bool) :
    steps (17 + 46 * (2 ^ (2 * h + 3 + 7) - 7)) (odC h LL TT)
      = some ⟨.E, -5 + 19 + 7 * ((2 * h + 3 : Nat) : Int) + 17
              + 2 * ((2 ^ (2 * h + 3 + 7) - 7 : Nat) : Int),
          ⟨ones 14 ++ (false :: false ::
            (pow10 (2 ^ (2 * h + 3 + 7) - 7) ++ (true :: rUnitsDep (2 * h + 3) (p1tL ++ LL)))),
           false,
           true :: false :: true :: false :: true ::
             (false :: false :: (descCascade (2 * h + 8) ++ TT))⟩⟩ := by
  have hsplit : (2 : Nat) ^ (2 * h + 3 + 8) - 13
      = 2 * (2 ^ (2 * h + 3 + 7) - 7) + 0 + 1 := by
    have e7 : (2:Nat)^(2*h+3+8) = 2 * 2^(2*h+3+7) := by
      rw [show 2*h+3+8 = (2*h+3+7)+1 from by omega, Nat.pow_add,
          show (2:Nat)^1 = 2 from rfl, Nat.mul_comm]
    have h7 : 8 ≤ (2:Nat)^(2*h+3+7) := by
      have : (2:Nat)^3 ≤ 2^(2*h+3+7) := Nat.pow_le_pow_right (by decide) (by omega)
      omega
    omega
  unfold odC
  rw [show (false :: (pow10 10 ++
        (ones (2 ^ (2*h+3+8) - 13) ++ (false :: false :: (descCascade (2*h+8) ++ TT)))))
      = pow01 10 ++ (false ::
        (ones (2 ^ (2*h+3+8) - 13) ++ (false :: false :: (descCascade (2*h+8) ++ TT))))
      from false_pow10_tail 10 _,
      hsplit,
      crossCarry (2 ^ (2*h+3+7) - 7) _ 0
        (rUnitsDep (2*h+3) (p1tL ++ LL))
        (false :: false :: (descCascade (2*h+8) ++ TT))]
  rfl

#print axioms odCcarry

/-- **`odTurn`** — the fixed 6-step turn between the exhausted carry register and the final
`eChewFold`: absorbs the `1 0 1 0 1 · 0 0` seam into the register (`ones 14 → ones 20`) and
leaves the head on the `0` before the next block.  `D` and `Y` untouched. -/
theorem odTurn (p : Int) (b : Nat) (D Y : List Bool) :
    steps 6 ⟨.E, p, ⟨ones 14 ++ (false :: false :: D), false,
        true :: false :: true :: false :: true :: (false :: false :: (ones b ++ Y))⟩⟩
      = some ⟨.E, p + 6, ⟨ones 20 ++ (false :: false :: D), false,
          false :: (ones b ++ Y)⟩⟩ := by
  have h0 : steps 6 (⟨.E, (0:Int), ⟨ones 14 ++ (false :: false :: D), false,
      true :: false :: true :: false :: true :: (false :: false :: (ones b ++ Y))⟩⟩ : Cfg)
      = some ⟨.E, (6:Int), ⟨ones 20 ++ (false :: false :: D), false,
          false :: (ones b ++ Y)⟩⟩ := rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **D** — after `odCcarry ∘ odTurn`: the register is `ones 20`, head on the `0` before
`descCascade (2h+8)`'s leading block, ready for the final `eChewFold`. -/
def odD (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 3 : Nat) : Int) + 17
      + 2 * ((2 ^ (2 * h + 3 + 7) - 7 : Nat) : Int) + 6,
    ⟨ones 20 ++ (false :: false ::
      (pow10 (2 ^ (2 * h + 3 + 7) - 7) ++ (true :: rUnitsDep (2 * h + 3) (p1tL ++ LL)))), false,
     false :: (descCascade (2 * h + 8) ++ TT)⟩⟩

theorem odCD (h : Nat) (LL TT : List Bool) :
    steps ((17 + 46 * (2 ^ (2 * h + 3 + 7) - 7)) + 6) (odC h LL TT) = some (odD h LL TT) := by
  rw [steps_add, odCcarry h LL TT, someBind]
  unfold odD
  exact odTurn _ 0 _ (descCascade (2 * h + 8) ++ TT)

#print axioms odTurn
#print axioms odCD


/-- **`topEntryOdd`** — `M6(g) → (the eChew-ready config)` for every odd `g = 2h+3`, in
`99 + 15g + (17 + 46(2^{g+7}−7)) + 6` steps.

`= p1t ∘ rUnitsFold ∘ crossCarry ∘ odTurn` — every factor proven, two of them (`p1t`,
`rUnitsFold`) reused VERBATIM from the even branch.  The remaining `eChewFold` then chews
`descCascade (2h+8)`'s leading block down to the `descIn (g+6)` block. -/
theorem topEntryOdd (h : Nat) (LL TT : List Bool) :
    steps (99 + (15 * (2 * h + 3) + ((17 + 46 * (2 ^ (2 * h + 3 + 7) - 7)) + 6)))
        (odA h LL TT)
      = some (odD h LL TT) := by
  rw [steps_add, odAB h LL TT, someBind, steps_add, odBC h LL TT, someBind]
  exact odCD h LL TT

-- ANTI-VACUITY (METHODS M4): at g=3 (h=0) the measured phase boundaries are
--   P1+T 99 | rUF 144 | cross 161 | carry-end 46 943 | turn 46 949 | descIn 9 @ 48 485.
example : 99 + (15 * (2 * 0 + 3) + ((17 + 46 * (2 ^ (2 * 0 + 3 + 7) - 7)) + 6)) = 46949 := by decide
example : 46949 + 6 * 2 ^ (2 * 0 + 8) = 48485 := by decide
-- and that IS the confirmed odd closed form at g=3:
example : 46949 + 6 * 2 ^ 8 = 6080 * 2 ^ 3 + 15 * 3 - 200 := by decide
-- general shape: the eChew phase is 6·2^{g+5} tiles (g = 2h+3, so 2^{2h+8}).
example : 6 * 2 ^ (3 + 5) = 6 * 2 ^ 8 := by decide

#print axioms topEntryOdd
