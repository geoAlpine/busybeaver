import T7S3
open X2

set_option maxRecDepth 40000

/-!
# S3 assembly — `topEntryEven`: `M6(g) → descIn(g+7)` for even `g`  (2026-07-24)

Built under **METHODS M8 (named-config discipline)**: the four phase boundaries are given
NAMES first, each phase primitive is restated at those names, and only then are they chained.
The previous attempt composed the primitives directly over anonymous `⟨.E, p, ⟨…⟩⟩` literals
and drowned in rewrite-pattern matching; see `STRATEGY_REVIEW_2026-07-24.md` §5.

```
teA (M6's own opening)  --p1t 99-->      teB
teB                     --rUnitsFold-->  teC
teC                     --bridge 3-->    teD
teD                     --eChewFold-->   descIn (g+7)
```

Arithmetic is kept in the single spelling `2*h+2+k` throughout (M8-2); reduction happens only
in the final `cfgPos`/`omega`.
-/

/-- **The big-block tail IS `descIn`'s cascade.**  `m1casc (h+1) (h+2) [] = 0 0 · descCascade h`. -/
theorem m1casc_descCascade : ∀ (h : Nat),
    m1casc (h + 1) (h + 2) [] = false :: false :: descCascade h := by
  intro h
  induction h with
  | zero => rfl
  | succ h ih =>
    show false :: false :: (ones (2 ^ (h + 2 + 1) - 3) ++ m1casc (h + 1) (h + 1 + 1) []) = _
    rw [show h + 1 + 1 = h + 2 from rfl, ih]
    rfl

/-- **The `1 0 0` bridge** (3 steps): `E` on the `0` before `1 0 0 · 1^b`, crosses to the `0`
before `1^b`, depositing `0 0 1`, advancing `+3`.  `L` and `Y` untouched. -/
theorem bridge (p : Int) (b : Nat) (L Y : List Bool) :
    steps 3 ⟨.E, p, ⟨L, false, false :: (true :: false :: false :: (ones b ++ Y))⟩⟩
      = some ⟨.E, p + 3, ⟨false :: false :: true :: L, false, false :: (ones b ++ Y)⟩⟩ := by
  have h0 : steps 3 (⟨.E, (0:Int), ⟨L, false,
      false :: (true :: false :: false :: (ones b ++ Y))⟩⟩ : Cfg)
      = some ⟨.E, (3:Int), ⟨false :: false :: true :: L, false, false :: (ones b ++ Y)⟩⟩ := rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-! ### M8-1 — the four phase boundaries, NAMED -/

/-- `p1t`'s output left word (the 20-cell deposit), named once. -/
def p1tL : List Bool :=
  [true, true, true, true, true, true, true, true, false, false,
   true, false, true, false, true, false, true, false, true, false]

/-- The big block's tail, shared by every boundary: `descIn`'s cascade at level `2h+9`. -/
def teTail (h : Nat) : List Bool := false :: false :: descCascade (2 * h + 7)

/-- **A** — `M6 (2h+2)` itself, with the `if`s reduced and `m1casc` turned into `descCascade`. -/
def teA (h : Nat) : Cfg :=
  ⟨.E, -5, ⟨[false], false,
    false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
      (rUnits (2 * h + 2 + 1) ++
       (true :: false :: false ::
        (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h))))))⟩⟩

/-- **B** — after `p1t`: the comb deposit is down, `rUnits` at the front of the right. -/
def teB (h : Nat) : Cfg :=
  ⟨.E, -5 + 19, ⟨p1tL, false,
    false :: (rUnits (2 * h + 2 + 1) ++
      (true :: false :: false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h)))⟩⟩

/-- **C** — after `rUnitsFold`: the `rUnits` register is consumed, `1 0 0` at the front. -/
def teC (h : Nat) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 2 + 1 : Nat) : Int),
    ⟨rUnitsDep (2 * h + 2 + 1) p1tL, false,
     false :: (true :: false :: false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h))⟩⟩

/-- **D** — after `bridge`: head on the `0` before the big block. -/
def teD (h : Nat) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 2 + 1 : Nat) : Int) + 3,
    ⟨false :: false :: true :: rUnitsDep (2 * h + 2 + 1) p1tL, false,
     false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTail h)⟩⟩

/-- The marker `descIn (2h+9)` carries out of `topEntry` (everything below the comb). -/
def teM (h : Nat) : List Bool :=
  false :: false :: true :: rUnitsDep (2 * h + 2 + 1) p1tL

/-- The head position `descIn (2h+9)` is reached at. -/
def teP (h : Nat) : Int :=
  -5 + 19 + 7 * ((2 * h + 2 + 1 : Nat) : Int) + 3 + 2 * ((2 ^ (2 * h + 2 + 6) : Nat) : Int)

/-! ### M8-1 — each primitive, restated at the named boundaries -/

/-- `M6` at even `g` IS `teA`. -/
theorem M6_even (h : Nat) : M6 (2 * h + 2) = teA h := by
  have hmod : (2 * h + 2) % 2 = 0 := by omega
  show (⟨.E, -5, ⟨[false], false,
      false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
        (rUnits (if (2*h+2) % 2 = 0 then (2*h+2) + 1 else (2*h+2)) ++
         ((if (2*h+2) % 2 = 0 then true :: false :: false :: [] else pow10 10) ++
          (ones (if (2*h+2) % 2 = 0 then 2 ^ ((2*h+2) + 8) - 3 else 2 ^ ((2*h+2) + 8) - 13) ++
           m1casc ((2*h+2) + 6) ((2*h+2) + 7) []))))))⟩⟩ : Cfg) = _
  rw [if_pos hmod, if_pos hmod, if_pos hmod,
      show (2*h+2)+6 = (2*h+7)+1 from by omega,
      show (2*h+2)+7 = (2*h+7)+2 from by omega,
      m1casc_descCascade (2*h+7)]
  show (⟨.E, -5, ⟨[false], false, _⟩⟩ : Cfg) = teA h
  unfold teA teTail
  simp only [List.cons_append, List.nil_append]

/-- **A → B**: `p1t`, 99 steps. -/
theorem teAB (h : Nat) : steps 99 (teA h) = some (teB h) := by
  unfold teA teB
  exact p1t (-5) (rUnits (2*h+2+1) ++
    (true :: false :: false :: (ones (2 ^ (2*h+2+8) - 3) ++ teTail h)))

/-- **B → C**: `rUnitsFold`, `15(g+1)` steps. -/
theorem teBC (h : Nat) : steps (15 * (2 * h + 2 + 1)) (teB h) = some (teC h) := by
  unfold teB teC
  exact rUnitsFold (2*h+2+1) (-5 + 19) p1tL
    (true :: false :: false :: (ones (2 ^ (2*h+2+8) - 3) ++ teTail h))

/-- **C → D**: `bridge`, 3 steps. -/
theorem teCD (h : Nat) : steps 3 (teC h) = some (teD h) := by
  unfold teC teD
  exact bridge _ (2 ^ (2*h+2+8) - 3) _ (teTail h)

/-- **D → descIn (2h+9)**: `eChewFold`, `6·2^{g+6}` steps.  The big block `2^{g+8}−3` splits as
`2·2^{g+6} + (2^{g+7}−3)`, leaving exactly `descIn (2h+9)`'s block with comb `pow01 (2^{g+6})`. -/
theorem teDdescIn (h : Nat) :
    steps (6 * 2 ^ (2 * h + 2 + 6)) (teD h)
      = some (descIn (2 * h + 9) (teP h) (teM h) []) := by
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
  unfold teD
  rw [hsplit,
      eChewFold (2 ^ (2*h+2+6)) _ (2 ^ (2*h+2+7) - 3)
        (false :: false :: true :: rUnitsDep (2*h+2+1) p1tL) (teTail h)]
  refine congrArg some ?_
  show (⟨.E, _, ⟨pow01 (2 ^ (2*h+2+6)) ++ teM h, false,
      false :: (ones (2 ^ (2*h+2+7) - 3) ++ teTail h)⟩⟩ : Cfg) = _
  show _ = (⟨.E, teP h, ⟨pow01 (2 ^ (2*h+9 - 1)) ++ teM h, false,
      false :: (ones (2 ^ (2*h+9) - 3) ++
        (false :: false :: (descCascade (2*h+9 - 2) ++ [])))⟩⟩ : Cfg)
  rw [show 2*h+9-1 = 2*h+2+6 from by omega, show 2*h+9 = 2*h+2+7 from by omega,
      show 2*h+2+7-2 = 2*h+7 from by omega]
  show (⟨.E, _, ⟨_, false, false :: (ones (2 ^ (2*h+2+7) - 3) ++ teTail h)⟩⟩ : Cfg) = _
  unfold teTail teP
  rw [List.append_nil]

/-! ### The composition -/

/-- **`topEntryEven`** — `M6(g) → descIn(g+7)`, every even `g = 2h+2`, in
`99 + 15(g+1) + 3 + 6·2^{g+6}` steps `= 384·2^g + 15g + 117`.  Marker `teM h`, position `teP h`
both explicit; `TAIL = []` because the big block's `m1casc` tail IS `descIn`'s cascade. -/
theorem topEntryEven (h : Nat) :
    steps (99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6)))) (M6 (2 * h + 2))
      = some (descIn (2 * h + 9) (teP h) (teM h) []) := by
  rw [M6_even h, steps_add, teAB h, someBind, steps_add, teBC h, someBind,
      steps_add, teCD h, someBind]
  exact teDdescIn h

-- ANTI-VACUITY (METHODS M4): the step count IS the confirmed closed form 384·2^g + 15g + 117,
-- i.e. the MEASURED M6(g) → descIn(g+7) span (1683 / 6321 / 24783 at g = 2 / 4 / 6).
example : 99 + (15 * (2 * 0 + 2 + 1) + (3 + 6 * 2 ^ (2 * 0 + 2 + 6))) = 1683 := by decide
example : 99 + (15 * (2 * 1 + 2 + 1) + (3 + 6 * 2 ^ (2 * 1 + 2 + 6))) = 6321 := by decide
example : 99 + (15 * (2 * 2 + 2 + 1) + (3 + 6 * 2 ^ (2 * 2 + 2 + 6))) = 24783 := by decide
example : 99 + (15 * (2 * 0 + 2 + 1) + (3 + 6 * 2 ^ (2 * 0 + 2 + 6)))
    = 384 * 2 ^ 2 + 15 * 2 + 117 := by decide
example : 99 + (15 * (2 * 3 + 2 + 1) + (3 + 6 * 2 ^ (2 * 3 + 2 + 6)))
    = 384 * 2 ^ 8 + 15 * 8 + 117 := by decide

#print axioms m1casc_descCascade
#print axioms bridge
#print axioms M6_even
#print axioms teAB
#print axioms teBC
#print axioms teCD
#print axioms teDdescIn
#print axioms topEntryEven
