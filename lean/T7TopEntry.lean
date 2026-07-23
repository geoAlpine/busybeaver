import T7S3
open X2

set_option maxRecDepth 40000

/-!
# S3 assembly — `topEntryEven`: `M6(g) → descIn(g+7)` for even `g`  (2026-07-24)

Composes the four measured phase primitives against `M6 g`'s actual register:

```
M6(g).right = 0 · pow10 4 · 1^9 · 00 · rUnits(g+1) · 1 0 0 · 1^{2^{g+8}−3} · m1casc(g+6)(g+7)
              └────── p1t (99) ──────┘└ rUnitsFold ┘└ bridge ┘└──── eChewFold ────┘
```

with two glue lemmas measured on the orbit: the `1 0 0` **bridge** (3 steps) and the
`m1casc = descCascade` **landing** identity (the big block's tail IS `descIn`'s cascade).

Writing `A = 2h+8` (`= g+6`, the `eChewFold` deposit exponent): the big block is `2^{A+2}−3`,
`eChewFold` chews `2·2^A` cells leaving `2^{A+1}−3` = `descIn (A+1)`'s block, with comb
`pow01 (2^A)`; and `descIn (A+1)` is `descIn (2h+9) = descIn (g+7)`.
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

/-! ### `topEntryEven` — the four phases composed over the even-`g` opening -/

/-- `M6` at even `g = 2h+2`, with the three `if`s reduced and the big-block/cascade exponents
normalised: block `2^{A+2}−3` (`A = 2h+8`), cascade `descCascade (2h+7)` via `m1casc_descCascade`. -/
theorem M6_even (h : Nat) :
    M6 (2 * h + 2)
      = ⟨.E, -5, ⟨[false], false,
          false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
            (rUnits (2 * h + 2 + 1) ++
             (true :: false :: false ::
              (ones (2 ^ (2 * h + 2 + 8) - 3) ++
               (false :: false :: descCascade (2 * h + 7))))))))⟩⟩ := by
  have hmod : (2 * h + 2) % 2 = 0 := by omega
  unfold M6
  rw [if_pos hmod, if_pos hmod, if_pos hmod,
      show (2*h+2)+6 = (2*h+7)+1 from by omega,
      show (2*h+2)+7 = (2*h+7)+2 from by omega,
      m1casc_descCascade (2*h+7)]
  simp only [List.cons_append, List.nil_append]

/-- **`topEntryEven` — WIP (pure Lean rewrite plumbing remaining).**  `M6(g) → descIn(g+7)`,
every even `g = 2h+2`, in `99 + 15(g+1) + 3 + 6·2^{g+6}` steps.

The mathematical assembly is COMPLETE and `#eval`-verified (M6 2 reaches the descIn 9 form in
exactly 1683 steps; the four phase primitives `p1t`/`rUnitsFold`/`bridge`/`eChewFold` are green;
`m1casc_descCascade` and `M6_even` reduce the endpoints).  What remains is only the `steps_add`
threading of the four phases against `M6_even`'s register — finicky rewrite-pattern matching,
not new content.  Marked `sorry` until that plumbing is done; NOT cited as proven. -/
theorem topEntryEven (h : Nat) :
    ∃ (p : Int) (M : List Bool),
      steps (99 + (15 * (2 * h + 3) + (3 + 6 * 2 ^ (2 * h + 2 + 6)))) (M6 (2 * h + 2))
        = some (descIn (2 * h + 9) p M []) := by
  sorry

-- ANTI-VACUITY (METHODS M4): the step count IS the confirmed closed form 384·2^g + 15g + 117.
example : 99 + (15 * (2 * 0 + 3) + (3 + 6 * 2 ^ (2 * 0 + 8))) = 384 * 2 ^ 2 + 15 * 2 + 117 := by decide
example : 99 + (15 * (2 * 1 + 3) + (3 + 6 * 2 ^ (2 * 1 + 8))) = 384 * 2 ^ 4 + 15 * 4 + 117 := by decide
example : 99 + (15 * (2 * 2 + 3) + (3 + 6 * 2 ^ (2 * 2 + 8))) = 384 * 2 ^ 6 + 15 * 6 + 117 := by decide

#print axioms m1casc_descCascade
#print axioms bridge
#print axioms M6_even
