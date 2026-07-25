import T7TopRung
open X2

set_option maxRecDepth 20000

/-!
# S3 — `topEntry` (even branch): `M6(g) → descIn(g+7)`   (2026-07-24)

MEASURED phase decomposition (`x2s3_topentry.py`, `x2s3_phases.py`), g=2/4 derived and g=6
PREDICTED-THEN-CONFIRMED (METHODS M4 — all four boundaries stated before the run and all hit):

```
M6(g) --P1(88)--> · --T(11)--> · --rUnitsFold(15(g+1)+3)--> · --bigChew(6·2^{g+6})--> descIn(g+7)
```

and the phase sum reproduces the independently confirmed closed form on the nose:

```
88 + 11 + (15(g+1) + 3) + 6·2^{g+6}  =  384·2^g + 15g + 117
```

(g=2: 1683, g=4: 6321, g=6: 24783, g=8: 98541 — each = the confirmed `M1(g)→entry` form
`384·2^g + 53g + 384` minus `h_low_even`'s `267 + 38g`.)

This file builds the `Θ(2^g)` bulk: the `E`-anchored chew tile and its `∀m` fold.
-/

/-- **The `E`-anchored chew tile** (6 steps): head `E` on the `0` before a `1`-block; eats two
block cells, deposits one `01` comb pair on the left, advances `+2`.  `L` and `Y` untouched.
Read off the real orbit at g=6 (rel 207 → 213 → 219 of the `M6(6)` window). -/
theorem eChewTile (p : Int) (b : Nat) (L Y : List Bool) :
    steps 6 ⟨.E, p, ⟨L, false, false :: (ones (b + 2) ++ Y)⟩⟩
      = some ⟨.E, p + 2, ⟨false :: true :: L, false, false :: (ones b ++ Y)⟩⟩ := by
  have h0 : steps 6 (⟨.E, (0 : Int), ⟨L, false, false :: (ones (b + 2) ++ Y)⟩⟩ : Cfg)
      = some ⟨.E, (2 : Int), ⟨false :: true :: L, false, false :: (ones b ++ Y)⟩⟩ := by
    rw [show ones (b + 2) = true :: true :: ones b from by
          rw [show b + 2 = 2 + b from by omega, ones_add]; rfl]
    rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0 : Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The `E`-anchored chew FOLD, `∀m`** — `m` tiles = `6m` steps drive `1^{2m+r}` down to `1^r`,
depositing `pow01 m` on the left and advancing `+2m`.  This is `S3`'s `Θ(2^g)` bulk. -/
theorem eChewFold : ∀ (m : Nat) (p : Int) (r : Nat) (L Y : List Bool),
    steps (6 * m) ⟨.E, p, ⟨L, false, false :: (ones (2 * m + r) ++ Y)⟩⟩
      = some ⟨.E, p + 2 * (m : Int), ⟨pow01 m ++ L, false, false :: (ones r ++ Y)⟩⟩ := by
  intro m
  induction m with
  | zero =>
    intro p r L Y
    simp only [Nat.mul_zero, Nat.zero_add]
    show some (⟨.E, p, ⟨L, false, false :: (ones r ++ Y)⟩⟩ : Cfg) = _
    refine congrArg some ?_
    show (⟨.E, p, ⟨L, false, _⟩⟩ : Cfg) = ⟨.E, _, ⟨_, false, _⟩⟩
    refine cfgPos ?_
    push_cast; omega
  | succ m ih =>
    intro p r L Y
    rw [show 6 * (m + 1) = 6 + 6 * m from by omega, steps_add,
        show 2 * (m + 1) + r = (2 * m + r) + 2 from by omega,
        eChewTile p (2 * m + r) L Y, someBind,
        ih (p + 2) r (false :: true :: L) Y]
    refine congrArg some ?_
    show (⟨.E, _, ⟨pow01 m ++ (false :: true :: L), false, _⟩⟩ : Cfg) = _
    rw [show (pow01 m ++ (false :: true :: L) : List Bool) = pow01 (m + 1) ++ L from by
          rw [pow01_add, List.append_assoc]; rfl]
    exact cfgPos (by push_cast; omega)

-- ANTI-VACUITY (METHODS M4): the fold's cost at the measured phase-3 lengths.
-- g=2: 6·2^8 = 1536;  g=4: 6·2^10 = 6144;  g=6: 6·2^12 = 24576.
example : 6 * 2 ^ 8 = 1536 := by decide
example : 6 * 2 ^ 10 = 6144 := by decide
example : 6 * 2 ^ 12 = 24576 := by decide
-- and the phase sum IS the confirmed closed form, at every measured generation:
example : 88 + 11 + (15 * (2 + 1) + 3) + 6 * 2 ^ 8 = 384 * 2 ^ 2 + 15 * 2 + 117 := by decide
example : 88 + 11 + (15 * (4 + 1) + 3) + 6 * 2 ^ 10 = 384 * 2 ^ 4 + 15 * 4 + 117 := by decide
example : 88 + 11 + (15 * (6 + 1) + 3) + 6 * 2 ^ 12 = 384 * 2 ^ 6 + 15 * 6 + 117 := by decide
example : 88 + 11 + (15 * (8 + 1) + 3) + 6 * 2 ^ 14 = 384 * 2 ^ 8 + 15 * 8 + 117 := by decide

#print axioms eChewTile
#print axioms eChewFold

/-! ### S3 phase 2 — the `rUnits` fold -/

/-- **The `rUnits` chew tile** (15 steps): head `E` on the `0` before a `1^5 · 0 0` unit;
consumes the unit, deposits `0 0 1 0 1 0 1` on the left, advances `+7`.  `L` and `Y` untouched
(read window is the `1^5 0 0` block).  Read off the canonical `M6 2` orbit (steps 99 → 114). -/
theorem rUnitsTile (p : Int) (L Y : List Bool) :
    steps 15 ⟨.E, p, ⟨L, false, false :: (ones 5 ++ (false :: false :: Y))⟩⟩
      = some ⟨.E, p + 7,
          ⟨false :: false :: true :: false :: true :: false :: true :: L, false, false :: Y⟩⟩ := by
  have h0 : steps 15 (⟨.E, (0:Int), ⟨L, false,
        false :: (ones 5 ++ (false :: false :: Y))⟩⟩ : Cfg)
      = some ⟨.E, (7:Int),
          ⟨false :: false :: true :: false :: true :: false :: true :: L, false,
           false :: Y⟩⟩ := rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- The left deposit of `n` `rUnits` tiles: `n` copies of `0 0 1 0 1 0 1`. -/
def rUnitsDep : Nat → List Bool → List Bool
  | 0, L => L
  | n + 1, L => false :: false :: true :: false :: true :: false :: true :: rUnitsDep n L

/-- `rUnitsDep` absorbs one leading deposit block into its count. -/
theorem rUnitsDep_absorb : ∀ (n : Nat) (L : List Bool),
    rUnitsDep n (false :: false :: true :: false :: true :: false :: true :: L)
      = rUnitsDep (n + 1) L := by
  intro n
  induction n with
  | zero => intro L; rfl
  | succ n ih => intro L; show _ :: _ :: _ :: _ :: _ :: _ :: _ :: rUnitsDep n _ = _; rw [ih]; rfl

/-- **The `rUnits` FOLD, `∀n`** — `n` tiles = `15n` steps consume `rUnits n` from the front of
the right, deposit `rUnitsDep n` on the left, advance `+7n`.  `S3`'s parity/`g`-dependent core
(the real orbit runs `n = g+1`). -/
theorem rUnitsFold : ∀ (n : Nat) (p : Int) (L Y : List Bool),
    steps (15 * n) ⟨.E, p, ⟨L, false, false :: (rUnits n ++ Y)⟩⟩
      = some ⟨.E, p + 7 * (n : Int), ⟨rUnitsDep n L, false, false :: Y⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p L Y
    show steps (15 * 0) ⟨.E, p, ⟨L, false, false :: (rUnits 0 ++ Y)⟩⟩ = _
    show some (⟨.E, p, ⟨L, false, false :: Y⟩⟩ : Cfg) = _
    refine congrArg some ?_
    show (⟨.E, p, ⟨L, false, _⟩⟩ : Cfg) = ⟨.E, p + 7 * ((0:Nat):Int), ⟨L, false, _⟩⟩
    refine cfgPos ?_
    push_cast; omega
  | succ n ih =>
    intro p L Y
    rw [show 15 * (n + 1) = 15 + 15 * n from by omega, steps_add,
        show (rUnits (n + 1) ++ Y : List Bool)
          = ones 5 ++ (false :: false :: (rUnits n ++ Y)) from by
            show (ones 5 ++ (false :: false :: rUnits n)) ++ Y = _
            rw [List.append_assoc]; rfl,
        rUnitsTile p L (rUnits n ++ Y), someBind,
        ih (p + 7) (false :: false :: true :: false :: true :: false :: true :: L) Y,
        rUnitsDep_absorb n L]
    refine congrArg some ?_
    show (⟨.E, _, ⟨rUnitsDep (n + 1) L, false, _⟩⟩ : Cfg) = ⟨.E, _, ⟨rUnitsDep (n + 1) L, false, _⟩⟩
    refine cfgPos (by push_cast; omega)

-- ANTI-VACUITY (METHODS M4): rUF cost 15(g+1) at the measured lengths (g=2,4,6): 45/75/105.
example : 15 * (2 + 1) = 45 := by decide
example : 15 * (4 + 1) = 75 := by decide
example : 15 * (6 + 1) = 105 := by decide

#print axioms rUnitsTile
#print axioms rUnitsFold

/-! ### S3 phases 1+2 fixed prefix (P1 ∘ T) — 99 steps, g-independent -/

private theorem p1tc0 (REST : List Bool) :
    steps 25 ⟨.E, 0, ⟨[false], false, [false, true, false, true, false, true, false, true, false, true, true, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.E, 5, ⟨[false, false, true, false, true, false], false, [true, false, true, false, true, false, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩ := by rfl

private theorem p1tc1 (REST : List Bool) :
    steps 25 ⟨.E, 5, ⟨[false, false, true, false, true, false], false, [true, false, true, false, true, false, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.F, 10, ⟨[true, true, true, false, false, true, false, true, false, true, false], true, [false, true, false, true, true, true, true, true, false, false] ++ REST⟩⟩ := by rfl

private theorem p1tc2 (REST : List Bool) :
    steps 25 ⟨.F, 10, ⟨[true, true, true, false, false, true, false, true, false, true, false], true, [false, true, false, true, true, true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.E, 15, ⟨[true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false], false, [true, true, true, false, false] ++ REST⟩⟩ := by rfl

private theorem p1tc3 (REST : List Bool) :
    steps 24 ⟨.E, 15, ⟨[true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false], false, [true, true, true, false, false] ++ REST⟩⟩
      = some ⟨.E, 19, ⟨[true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false, true, false], false, [false] ++ REST⟩⟩ := by rfl

/-- **`p1t`** — the fixed 99-step opening of `topEntry` (P1 ∘ T), `g`-independent, `∀ REST`. -/
theorem p1t (p : Int) (REST : List Bool) :
    steps 99 ⟨.E, p, ⟨[false], false,
        false :: (pow10 4 ++ (ones 9 ++ (false :: false :: REST)))⟩⟩
      = some ⟨.E, p + 19, ⟨[true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false, true, false], false, [false] ++ REST⟩⟩ := by
  have h0 : steps 99 ⟨.E, 0, ⟨[false], false, [false, true, false, true, false, true, false, true, false, true, true, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩ = some ⟨.E, 19, ⟨[true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, true, false, true, false], false, [false] ++ REST⟩⟩ := by
    rw [show (99:Nat) = 25 + (25 + (25 + 24)) from by decide, steps_add, p1tc0 REST, someBind,
        steps_add, p1tc1 REST, someBind, steps_add, p1tc2 REST, someBind]
    exact p1tc3 REST
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  show steps 99 ⟨.E, p, ⟨[false], false, [false, true, false, true, false, true, false, true, false, true, true, true, true, true, true, true, true, true, false, false] ++ REST⟩⟩ = _
  rw [h]
  exact congrArg some (cfgPos (by omega))

#print axioms p1t
