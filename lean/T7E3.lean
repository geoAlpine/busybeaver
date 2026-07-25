import T7E2Bridge
open X2

set_option maxRecDepth 40000

/-!
# E3 — the even doubling phase `M6(g) → M1(g+1)`-frame, in one theorem   (2026-07-24)

`topEntry ∘ evenSpine`, with BOTH tape tails freed so the two halves meet exactly.

**M7 audit, done before composing.**  Two padding seams, both measured:

* LEFT — `evenSpine`'s marker carries `zeros 11`, `topEntry` delivers `zeros 1`.
  Closed in E2 by freeing `p1t`'s inert left base (`LL := zeros 10`).
* RIGHT — `evenSpine`'s `descIn` TAIL is `zeros 25 ++ zeros 16 ++ ladderPad 5 n ++ zeros (2^{5+n}) ++ R`
  (the ladder's pads), `topEntry` delivers `[]`.  Closed here by freeing `m1casc`'s tail
  (`m1casc (h+1) (h+2) T = 0 0 · descCascade h · T`, `#eval` true at h = 0..4, proven below):
  `topEntry`'s head chews the big block and never reaches past the cascade, so that tail is inert.

And the landing is exact: `evenSpine`'s OUT right IS `M1 (g+1)`'s right followed by `zeros 9`
(`#eval` verified at g=2), its left is `zeros 10` where `M1`'s is `[]`.  So the phase lands on
`M1 (g+1)` in **realized form** — the same canonical-vs-realized situation `h_init` already
had; reconciling it is **obligation H** (`realizeM1_port` + `BlankNorm`), deliberately not done here.
-/

/-- `m1casc`'s tail is free: `m1casc (h+1) (h+2) T = 0 0 · descCascade h · T`. -/
theorem m1casc_descCascade_tail : ∀ (h : Nat) (T : List Bool),
    m1casc (h + 1) (h + 2) T = false :: false :: (descCascade h ++ T) := by
  intro h
  induction h with
  | zero => intro T; rfl
  | succ h ih =>
    intro T
    show false :: false :: (ones (2 ^ (h + 2 + 1) - 3) ++ m1casc (h + 1) (h + 1 + 1) T) = _
    rw [show h + 1 + 1 = h + 2 from rfl, ih T,
        show h + 2 + 1 = h + 3 from by omega, descCascade, List.append_assoc]
    rfl

/-! ### The `TT`-threaded boundaries (left tail `LL`, right tail `TT`) -/

/-- The big block's tail, now carrying a free right tail `TT`. -/
def teTailT (h : Nat) (TT : List Bool) : List Bool :=
  false :: false :: (descCascade (2 * h + 7) ++ TT)

def ttA (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5, ⟨[false] ++ LL, false,
    false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
      (rUnits (2 * h + 2 + 1) ++
       (true :: false :: false ::
        (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTailT h TT))))))⟩⟩

def ttB (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5 + 19, ⟨p1tL ++ LL, false,
    false :: (rUnits (2 * h + 2 + 1) ++
      (true :: false :: false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTailT h TT)))⟩⟩

def ttC (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 2 + 1 : Nat) : Int),
    ⟨rUnitsDep (2 * h + 2 + 1) (p1tL ++ LL), false,
     false :: (true :: false :: false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTailT h TT))⟩⟩

def ttD (h : Nat) (LL TT : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2 * h + 2 + 1 : Nat) : Int) + 3,
    ⟨false :: false :: true :: rUnitsDep (2 * h + 2 + 1) (p1tL ++ LL), false,
     false :: (ones (2 ^ (2 * h + 2 + 8) - 3) ++ teTailT h TT)⟩⟩

theorem ttAB (h : Nat) (LL TT : List Bool) : steps 99 (ttA h LL TT) = some (ttB h LL TT) := by
  unfold ttA ttB
  exact p1tLL (-5) LL (rUnits (2*h+2+1) ++
    (true :: false :: false :: (ones (2 ^ (2*h+2+8) - 3) ++ teTailT h TT)))

theorem ttBC (h : Nat) (LL TT : List Bool) :
    steps (15 * (2 * h + 2 + 1)) (ttB h LL TT) = some (ttC h LL TT) := by
  unfold ttB ttC
  exact rUnitsFold (2*h+2+1) (-5 + 19) (p1tL ++ LL)
    (true :: false :: false :: (ones (2 ^ (2*h+2+8) - 3) ++ teTailT h TT))

theorem ttCD (h : Nat) (LL TT : List Bool) : steps 3 (ttC h LL TT) = some (ttD h LL TT) := by
  unfold ttC ttD
  exact bridge _ (2 ^ (2*h+2+8) - 3) _ (teTailT h TT)

theorem ttDdescIn (h : Nat) (LL TT : List Bool) :
    steps (6 * 2 ^ (2 * h + 2 + 6)) (ttD h LL TT)
      = some (descIn (2 * h + 9) (teP h) (tlM h LL) TT) := by
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
  unfold ttD
  rw [hsplit,
      eChewFold (2 ^ (2*h+2+6)) _ (2 ^ (2*h+2+7) - 3)
        (false :: false :: true :: rUnitsDep (2*h+2+1) (p1tL ++ LL)) (teTailT h TT)]
  refine congrArg some ?_
  show (⟨.E, _, ⟨pow01 (2 ^ (2*h+2+6)) ++ tlM h LL, false,
      false :: (ones (2 ^ (2*h+2+7) - 3) ++ teTailT h TT)⟩⟩ : Cfg) = _
  show _ = (⟨.E, teP h, ⟨pow01 (2 ^ (2*h+9 - 1)) ++ tlM h LL, false,
      false :: (ones (2 ^ (2*h+9) - 3) ++
        (false :: false :: (descCascade (2*h+9 - 2) ++ TT)))⟩⟩ : Cfg)
  rw [show 2*h+9-1 = 2*h+2+6 from by omega, show 2*h+9 = 2*h+2+7 from by omega,
      show 2*h+2+7-2 = 2*h+7 from by omega]
  show (⟨.E, _, ⟨_, false, false :: (ones (2 ^ (2*h+2+7) - 3) ++ teTailT h TT)⟩⟩ : Cfg) = _
  unfold teTailT teP
  rfl

/-- **`topEntryEvenLT`** — `topEntry` with BOTH tails free.  With `LL := zeros 10` the marker is
the spine's; with `TT :=` the ladder pads the `descIn` TAIL is the spine's. -/
theorem topEntryEvenLT (h : Nat) (LL TT : List Bool) :
    steps (99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6)))) (ttA h LL TT)
      = some (descIn (2 * h + 9) (teP h) (tlM h LL) TT) := by
  rw [steps_add, ttAB h LL TT, someBind, steps_add, ttBC h LL TT, someBind,
      steps_add, ttCD h LL TT, someBind]
  exact ttDdescIn h LL TT

/-! ### E3 — the even doubling phase -/

/-- **`doubPhaseEven`** — the even doubling phase as ONE theorem: from `M6 (2h+2)` in realized
form (left `[false] ++ zeros 10`, right carrying the ladder pads) all the way onto the next
milestone's frame.  `= topEntryEvenLT ∘ evenSpine`, both `∀`.

The descent index is `n = 2h+5` (`descIn (n+4) = descIn (2h+9)` is `topEntry`'s OUT level) and
the frame-digit count is `j = 2h+1` (`= g−1`), forced by E2's marker identity. -/
theorem doubPhaseEven (h : Nat) (R : List Bool) :
    ∃ q : Int,
      steps ((99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6))))
             + ((descTotal (2 * h + 5) + 415)
                + (ladderSteps 5 (2 * h + 5) + exitSteps (5 + (2 * h + 5)))
                + (topGrindSteps (5 + (2 * h + 5)) + exitSteps (5 + (2 * h + 5) + 1) + 74
                   + (27 * (2 * h + 1) + 110))))
          (ttA h (zeros 10)
            (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2 * h + 5) ++
              (zeros (2 ^ (5 + (2 * h + 5))) ++ R)))))
        = some ⟨.E, q, ⟨zeros 10, false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2 * h + 1) (seamZ (5 + (2 * h + 5)) R))))⟩⟩ := by
  obtain ⟨q, hq⟩ := evenSpine (2 * h + 5) (2 * h + 1) (teP h) [] R
  refine ⟨q, ?_⟩
  rw [steps_add,
      topEntryEvenLT h (zeros 10)
        (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2 * h + 5) ++
          (zeros (2 ^ (5 + (2 * h + 5))) ++ R)))),
      someBind, tlM_spineMk h (zeros 10), zeros_1_10]
  show steps _ (descIn (2 * h + 5 + 4) (teP h) _ _) = _
  exact hq

-- ANTI-VACUITY (METHODS M4): at g=2 (h=0) the composed cost is the MEASURED
-- M6(2) @733 076 → M1(3) @2 852 091 span = 2 119 015.
example : (99 + (15 * (2 * 0 + 2 + 1) + (3 + 6 * 2 ^ (2 * 0 + 2 + 6))))
    + ((descTotal (2 * 0 + 5) + 415)
       + (ladderSteps 5 (2 * 0 + 5) + exitSteps (5 + (2 * 0 + 5)))
       + (topGrindSteps (5 + (2 * 0 + 5)) + exitSteps (5 + (2 * 0 + 5) + 1) + 74
          + (27 * (2 * 0 + 1) + 110))) = 2119015 := by decide

#print axioms m1casc_descCascade_tail
#print axioms topEntryEvenLT
#print axioms doubPhaseEven
