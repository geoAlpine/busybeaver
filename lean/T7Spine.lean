import T7S3
open X2

set_option maxRecDepth 20000

/-!
# THE EVEN SPINE — S1 closed, and the whole `descIn → M1`-frame composed  (2026-07-24)

The "composition glue" (METHODS_2026-07-24 S1) turns out to be **fully generic**: one pure
`List` identity with no condition on the marker at all.

The descent deposits one marker block per rung (`descMarkStep`), and the ladder consumes one
nested layer per rung (`ladderMarker`).  These are THE SAME WORDS:

```
descMarkStep j M = 0 0 1 · (01)^{1+(2^{j+3}−3)+2^{j+3}} · M = 0 0 1 · (01)^{2^{j+4}−2} · M
                 = layer (j+4) ++ M
ladderMarker 5 n = layer 5 ++ … ++ layer (n+4)
```

so `descMarkInner n M = ladderMarker 5 n ++ M` — the descent hands the ladder EXACTLY its
nested marker, with the descent's own entry marker `M` as the ladder's base.  (And `E2` had
already consumed `layer 4`: the deposit indices run 4..n+4, `E2` eats the bottom one, the
ladder eats 5..n+4.  Nothing is left over and nothing is missing.)

The pad seam is `headLaw`'s free `R` instantiated at `zeros 16 ++ …` plus `regenIn_pad`
(9 + 16 = 2^4 + 9).

With S1 closed, `headLaw ∘ ladderToCascade ∘ topRungToMilestone` composes into **one theorem**
covering the whole even doubling phase from the descent's entry to the next milestone's frame.
-/

/-- One descent deposit IS one ladder layer: `descMarkStep j M = layer (j+4) ++ M`. -/
theorem descMarkStep_layer (j : Nat) (M : List Bool) :
    descMarkStep j M = (false :: false :: true :: pow01 (2 ^ (j + 4) - 2)) ++ M := by
  have ha : (3 : Nat) ≤ 2 ^ (j + 3) := by
    have h : (2 : Nat) ^ 3 ≤ 2 ^ (j + 3) := Nat.pow_le_pow_right (by omega) (by omega)
    omega
  have hp : (2 : Nat) ^ (j + 4) = 2 * 2 ^ (j + 3) := by
    rw [Nat.pow_succ]; omega
  show false :: false :: true :: false :: true ::
      (pow01 (2 ^ (j + 3) - 3) ++ (pow01 (2 ^ (j + 3)) ++ M)) = _
  rw [show (2 : Nat) ^ (j + 4) - 2 = 1 + ((2 ^ (j + 3) - 3) + 2 ^ (j + 3)) from by omega,
      pow01_add, pow01_add]
  simp only [List.cons_append, List.append_assoc]
  rfl

/-- `ladderMarker` snoc: extending the climb appends the TOP layer. -/
theorem ladderMarker_snoc : ∀ (n b : Nat),
    ladderMarker b (n + 1)
      = ladderMarker b n ++ (false :: false :: true :: pow01 (2 ^ (b + n) - 2)) := by
  intro n
  induction n with
  | zero =>
    intro b
    show (false :: false :: true :: pow01 (2 ^ b - 2)) ++ ladderMarker (b + 1) 0 = _
    rw [show ladderMarker (b + 1) 0 = [] from rfl, List.append_nil]
    rfl
  | succ n ih =>
    intro b
    show (false :: false :: true :: pow01 (2 ^ b - 2)) ++ ladderMarker (b + 1) (n + 1) = _
    rw [ih (b + 1),
        show (ladderMarker b (n + 1) : List Bool)
          = (false :: false :: true :: pow01 (2 ^ b - 2)) ++ ladderMarker (b + 1) n from rfl,
        List.append_assoc, show b + 1 + n = b + (n + 1) from by omega]

/-- **S1 (the marker glue) — CLOSED, generically.**  The descent's accumulated deposits ARE
the ladder's nested marker, over ANY base `M`.  No condition on `M` whatsoever: the descent's
entry marker becomes the ladder's base marker unchanged. -/
theorem descMarkInner_eq_ladderMarker : ∀ (n : Nat) (M : List Bool),
    descMarkInner n M = ladderMarker 5 n ++ M := by
  intro n
  induction n with
  | zero => intro M; rfl
  | succ n ih =>
    intro M
    show descMarkInner n (descMarkStep (n + 1) M) = _
    rw [ih (descMarkStep (n + 1) M), descMarkStep_layer (n + 1) M,
        ladderMarker_snoc n 5,
        show (5 : Nat) + n = n + 5 from by omega,
        show n + 1 + 4 = n + 5 from by omega,
        List.append_assoc]

/-- **S1 (complete) — head-to-ladder, composed.**  `headLaw ∘ [marker glue] ∘ [pad glue] ∘
`ladderToCascade`: from the descent's entry `descIn (n+4)` with base marker `marker'` all the
way up to the last canonical `cascadeReg (5+n)`.  The pad glue is `headLaw`'s free `R`
instantiated at `zeros 16 ++ (ladderPad 5 n ++ R'')` plus `regenIn_pad` (9+16 = 2^4+9). -/
theorem headToLadder (n : Nat) (p : Int) (marker' R'' : List Bool) :
    ∃ q, steps ((descTotal n + 415) + (ladderSteps 5 n + exitSteps (5 + n)))
        (descIn (n + 4) p marker' (zeros 25 ++ (zeros 16 ++ (ladderPad 5 n ++ R''))))
      = some (cascadeReg (5 + n) 1 q marker' R'') := by
  obtain ⟨q', hlad⟩ := ladderToCascade 5 (by omega) n (descPosF n p + 23) marker' R''
  refine ⟨q', ?_⟩
  rw [steps_add, headLaw n p marker' (zeros 16 ++ (ladderPad 5 n ++ R'')), someBind,
      descMarkInner_eq_ladderMarker n marker',
      regenIn_pad 5 (descPosF n p + 23) 9 16 (ladderMarker 5 n ++ marker')
        (ladderPad 5 n ++ R'')]
  exact hlad

/-- **THE EVEN SPINE** — `headToLadder ∘ topRungToMilestone`, `∀ n ∀ j`.  The ENTIRE even
doubling phase below `topEntry`, as one theorem: from the descent's entry `descIn (n+4)`
(marker = the top-rung word over the frame odometer's register, tail = the ladder pads) all
the way onto the next milestone's frame.

On the real orbit `n = g+3` and `j = g−1`; both are left free here — S3/S4 instantiate. -/
theorem evenSpine (n j : Nat) (p : Int) (L R : List Bool) :
    ∃ q, steps ((descTotal n + 415) + (ladderSteps 5 n + exitSteps (5 + n))
          + (topGrindSteps (5 + n) + exitSteps (5 + n + 1) + 74 + (27 * j + 110)))
        (descIn (n + 4) p
          (false :: false :: true ::
            (false :: false :: true :: false :: true :: false :: true :: false :: false ::
              frameL j (turnWord ++ (endWord ++ (zeros 11 ++ L)))))
          (zeros 25 ++ (zeros 16 ++ (ladderPad 5 n ++ (zeros (2 ^ (5 + n)) ++ R)))))
      = some ⟨.E, q, ⟨zeros 10 ++ L, false,
          zeros 21 ++ (true :: (zeros 6 ++ (true :: false :: frameZ j (seamZ (5 + n) R))))⟩⟩ := by
  obtain ⟨q1, h1⟩ := headToLadder n p
    (false :: false :: true ::
      (false :: false :: true :: false :: true :: false :: true :: false :: false ::
        frameL j (turnWord ++ (endWord ++ (zeros 11 ++ L)))))
    (zeros (2 ^ (5 + n)) ++ R)
  refine ⟨q1 + 5 + 2 * ((2 ^ (5 + n - 1) - 2 : Nat) : Int) - 2 ^ (5 + n + 1) - 10
      - 7 * (j : Int) - 26, ?_⟩
  rw [steps_add, h1, someBind]
  exact topRungToMilestone (5 + n) j (by omega) q1 L R

-- ANTI-VACUITY (METHODS M4): the spine's total cost, instantiated at the orbit's own
-- parameters, must reproduce the MEASURED spans.
-- g=2 (n = g+3 = 5, j = g−1 = 1): descIn 9 @734 759 → M1(3) @2 852 091 = 2 117 332.
example : (descTotal 5 + 415) + (ladderSteps 5 5 + exitSteps 10)
    + (topGrindSteps 10 + exitSteps 11 + 74 + (27 * 1 + 110)) = 2117332 := by decide
example : 734759 + 2117332 = 2852091 := by decide
-- g=4 (n = 7, j = 3): descIn 11 @11 336 041 → M1(5) @44 986 995 = 33 650 954.
example : (descTotal 7 + 415) + (ladderSteps 5 7 + exitSteps 12)
    + (topGrindSteps 12 + exitSteps 13 + 74 + (27 * 3 + 110)) = 33650954 := by decide
example : 11336041 + 33650954 = 44986995 := by decide

#print axioms descMarkStep_layer
#print axioms ladderMarker_snoc
#print axioms descMarkInner_eq_ladderMarker
#print axioms headToLadder
#print axioms evenSpine
