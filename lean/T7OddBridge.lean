import T7OddRung
import BlankNorm
import T7E2Bridge
import T7Odd
open X2

set_option maxRecDepth 40000

/-! # The odd doubling phase: `topEntryOddFull` composed with `oddSpineFull`

`topEntryOddFull h` lands in `descIn (2h+9)` carrying the marker
`ones 20 ++ (0 0 :: (pow10 N ++ (1 :: rUnitsDep (2h+3) (p1tL ++ LL))))`, `N = 2^(2h+10) - 7`.
`oddSpineFull n` consumes `ones 20 ++ (0 0 :: (pow10 m ++ (0 1 :: frameLV j (endWord ++ zeros 11 ++ L))))`
in `descIn (n+4)`.  This file proves the two are the SAME word with

    n = 2h+5,   m = N + 1,   j = 2h+2,   LL = zeros 10 ++ L

and — independently — that `oddSpineFull`'s arithmetic side condition
`10 + m = (c+1) + (2^(5+n) - 2)` then FORCES `c = 5`, i.e. the odd top rung's measured `Lc = 6`.
-/

/-- The marker word delivered by `topEntryOddFull` IS the one `oddSpineFull` consumes. -/
theorem oddMarkerBridge (h : Nat) (L : List Bool) :
    pow10 (2^(2*h+3+7) - 7) ++ (true :: rUnitsDep (2*h+3) (p1tL ++ (zeros 10 ++ L)))
      = pow10 ((2^(2*h+3+7) - 7) + 1)
          ++ (false :: true :: frameLV ((2*h+1) + 1) (endWord ++ (zeros 11 ++ L))) := by
  rw [rUnitsDep_frameL h (zeros 10 ++ L), ← List.append_assoc (zeros 1), zeros_1_10,
      frameL_turnWord (2*h+1) (endWord ++ (zeros 11 ++ L)),
      ← oddE2Marker (2^(2*h+3+7) - 7) (2*h+1) (endWord ++ (zeros 11 ++ L))]
  rfl

/-- The side condition of `oddSpineFull` at `n = 2h+5`, `m = N+1` FORCES `c = 5` — the odd top
rung's measured `Lc = 6`, recovered here purely arithmetically. -/
theorem oddC_forced (h c : Nat)
    (hm : 10 + ((2^(2*h+3+7) - 7) + 1) = (c + 1) + (2^(5 + (2*h+5)) - 2)) : c = 5 := by
  have e : (5 + (2*h+5)) = (2*h+3+7) := by omega
  rw [e] at hm
  have hp : 2 ^ (2*h+3+7) ≥ 2 ^ 10 := Nat.pow_le_pow_right (by omega) (by omega)
  have : (2:Nat) ^ 10 = 1024 := by decide
  omega

#print axioms oddMarkerBridge
#print axioms oddC_forced

/-- **THE ODD DOUBLING PHASE** — `topEntryOddFull` composed with `oddSpineFull`, unconditional in
`h`.  From the odd A-entry `odA h` all the way to the next milestone, with `c = 5` (the measured
`Lc = 6`) and `j = 2h+2` forced, not assumed. -/
theorem doubPhaseOdd (h : Nat) (L R : List Bool) :
    ∃ q, steps (((99 + (15 * (2 * h + 3) + ((17 + 46 * (2 ^ (2 * h + 3 + 7) - 7)) + 6)))
             + 6 * 2 ^ (2 * h + 8))
          + (((descTotal (2*h+5) + 415) + (ladderSteps 5 (2*h+5) + exitSteps (5 + (2*h+5))))
             + ((topGrindSteps (5 + (2*h+5)) + exitSteps (5 + (2*h+5) + 1) + 80)
                + (topGrindSteps (5 + (2*h+5) + 1) + (exitSteps (5 + (2*h+5) + 1 + 1) + 4 * 5)
                   + (27 * (2*h+2) + 110)))))
        (odA h (zeros 10 ++ L)
          (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2*h+5) ++
            (zeros (2 ^ (5 + (2*h+5))) ++ (zeros (2 ^ (5 + (2*h+5) + 1)) ++ R))))))
      = some ⟨.E, q, ⟨zeros 10 ++ L, false,
          zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
            frameZ (2*h+2) (oddSeamZ (5 + (2*h+5) + 1) 5 R))))⟩⟩ := by
  have hm : 10 + ((2 ^ (2*h+3+7) - 7) + 1) = (5 + 1) + (2 ^ (5 + (2*h+5)) - 2) := by
    have e : (5 + (2*h+5)) = (2*h+3+7) := by omega
    rw [e]
    have hp : (2:Nat) ^ (2*h+3+7) ≥ 2 ^ 10 := Nat.pow_le_pow_right (by omega) (by omega)
    have h1024 : (2:Nat) ^ 10 = 1024 := by decide
    omega
  obtain ⟨q, hq⟩ := oddSpineFull (2*h+5) ((2 ^ (2*h+3+7) - 7) + 1) 5 (2*h+2) (by omega) (by omega)
    hm (-5 + 19 + 7 * ((2 * h + 3 : Nat) : Int) + 17
        + 2 * ((2 ^ (2 * h + 3 + 7) - 7 : Nat) : Int) + 6
        + 2 * ((2 ^ (2 * h + 8) : Nat) : Int)) L R
  refine ⟨q, ?_⟩
  have en : 2*h+5+4 = 2*h+9 := by omega
  rw [en] at hq
  rw [steps_add, topEntryOddFull h (zeros 10 ++ L) _, someBind, oddMarkerBridge h L]
  exact hq

#print axioms doubPhaseOdd

/-- **M4 anti-vacuity.**  At `h = 0` the composed cost is `8476791` — the INDEPENDENTLY MEASURED
`x2` milestone span M6(3) → M1(4).  The theorem is therefore about the real orbit, not a vacuous
or off-orbit family. -/
theorem doubPhaseOdd_cost0 :
    ((99 + (15 * (2 * 0 + 3) + ((17 + 46 * (2 ^ (2 * 0 + 3 + 7) - 7)) + 6)))
             + 6 * 2 ^ (2 * 0 + 8))
          + (((descTotal (2*0+5) + 415) + (ladderSteps 5 (2*0+5) + exitSteps (5 + (2*0+5))))
             + ((topGrindSteps (5 + (2*0+5)) + exitSteps (5 + (2*0+5) + 1) + 80)
                + (topGrindSteps (5 + (2*0+5) + 1) + (exitSteps (5 + (2*0+5) + 1 + 1) + 4 * 5)
                   + (27 * (2*0+2) + 110)))) = 8476791 := by decide

#print axioms doubPhaseOdd_cost0

/-! ## Obligation H (odd branch) — R5 dissolves

`doubPhaseOdd` is `∀ L` in the left tail.  So the low phase's surviving-blank count `j` does NOT
have to be pinned to `10`: any `j ≥ 10` feeds the phase with `L := zeros (j - 10)`.  The bracket
`hlow_j_ge`(≥10) + `steps_lpad_zeros`(≤16) is therefore already sufficient, and the "pin `j = 10`"
item (R5) is not needed for the odd branch at all. -/

/-- the doubling phase's right-hand pad register -/
def oddPadR (h : Nat) (R : List Bool) : List Bool :=
  zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2*h+5) ++
    (zeros (2 ^ (5 + (2*h+5))) ++ (zeros (2 ^ (5 + (2*h+5) + 1)) ++ R))))

/-- the low phase's free `FRAME` instantiated to what `odA` needs -/
def oddLowFrame (h : Nat) (R : List Bool) : List Bool :=
  ones (2 ^ (2*h+3+8) - 13) ++ (false :: false :: (descCascade (2*h+8) ++ oddPadR h R))

/-- `h_low_odd_core` with `FRAME` set to the doubling phase's register: the OUT is `odA h [] _`. -/
theorem hlowOdd_core' (h : Nat) (R : List Bool) :
    steps (419 + 76*h)
        ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h+2) ++
          (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R)))))⟩⟩
      = some (odA h [] (oddPadR h R)) :=
  h_low_odd_core h (oddLowFrame h R)

#print axioms hlowOdd_core'

/-- padded odd low phase: `zeros m` of left boundary blanks, `j ≤ m` survive. -/
theorem hlowOdd_padded (h : Nat) (R : List Bool) :
    ∀ m : Nat, ∃ j : Nat, j ≤ m ∧
      steps (419 + 76*h)
          ⟨.E, 0, ⟨zeros m, false, zeros 21 ++ (uUnits (2*h+2) ++
            (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R)))))⟩⟩
        = some (odA h (zeros j) (oddPadR h R)) := by
  intro m
  obtain ⟨j, hjm, hj⟩ := steps_lpad_zeros (419 + 76*h) .E 0 [] false _ (hlowOdd_core' h R) m
  exact ⟨j, hjm, by rwa [List.nil_append] at hj⟩

/-- **Obligation H (odd) — the low phase meets `doubPhaseOdd`, unconditional in `h`.**
`zeros 16` of left boundary blanks are supplied; `j ∈ [10, 16]` of them survive; the doubling
phase absorbs the surplus into its free left tail.  No exact `j` is required. -/
theorem hlowDoubOdd (h : Nat) (R : List Bool) :
    ∃ (j : Nat) (q : Int), 10 ≤ j ∧ j ≤ 16 ∧
      steps ((419 + 76*h)
          + (((99 + (15 * (2 * h + 3) + ((17 + 46 * (2 ^ (2 * h + 3 + 7) - 7)) + 6)))
               + 6 * 2 ^ (2 * h + 8))
            + (((descTotal (2*h+5) + 415) + (ladderSteps 5 (2*h+5) + exitSteps (5 + (2*h+5))))
               + ((topGrindSteps (5 + (2*h+5)) + exitSteps (5 + (2*h+5) + 1) + 80)
                  + (topGrindSteps (5 + (2*h+5) + 1) + (exitSteps (5 + (2*h+5) + 1 + 1) + 4 * 5)
                     + (27 * (2*h+2) + 110))))))
          ⟨.E, 0, ⟨zeros 16, false, zeros 21 ++ (uUnits (2*h+2) ++
            (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R)))))⟩⟩
        = some ⟨.E, q, ⟨zeros 10 ++ zeros (j - 10), false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2*h+2) (oddSeamZ (5 + (2*h+5) + 1) 5 R))))⟩⟩ := by
  obtain ⟨j, hj16, hlow⟩ := hlowOdd_padded h R 16
  have hj10 : 10 ≤ j := by
    have hm := steps_left_mono _ _ _ hlow
    simp only [odA, List.length_append, zeros_length, List.length_cons,
      List.length_nil] at hm
    push_cast at hm
    omega
  obtain ⟨q, hdb⟩ := doubPhaseOdd h (zeros (j - 10)) R
  refine ⟨j, q, hj10, hj16, ?_⟩
  have hz : zeros 10 ++ zeros (j - 10) = zeros j := by
    rw [← zeros_add, show 10 + (j - 10) = j from by omega]
  rw [hz] at hdb
  rw [steps_add, hlow, someBind, hz]
  exact hdb

#print axioms hlowOdd_padded
#print axioms hlowDoubOdd

/-! ## The even branch, made `∀ L` — and obligation H (even)

`doubPhaseEven` is stated at the FIXED left tail `zeros 10`.  Its two ingredients
(`topEntryEvenLT`, `evenSpine`) are both `∀`, so the `∀ L` restatement is immediate — and with it
the same R5-dissolving argument works on the even branch too. -/

/-- **`doubPhaseEven` with a free left tail.** -/
theorem doubPhaseEvenL (h : Nat) (L R : List Bool) :
    ∃ q : Int,
      steps ((99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6))))
             + ((descTotal (2 * h + 5) + 415)
                + (ladderSteps 5 (2 * h + 5) + exitSteps (5 + (2 * h + 5)))
                + (topGrindSteps (5 + (2 * h + 5)) + exitSteps (5 + (2 * h + 5) + 1) + 74
                   + (27 * (2 * h + 1) + 110))))
          (ttA h (zeros 10 ++ L)
            (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2 * h + 5) ++
              (zeros (2 ^ (5 + (2 * h + 5))) ++ R)))))
        = some ⟨.E, q, ⟨zeros 10 ++ L, false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2 * h + 1) (seamZ (5 + (2 * h + 5)) R))))⟩⟩ := by
  obtain ⟨q, hq⟩ := evenSpine (2 * h + 5) (2 * h + 1) (teP h) L R
  refine ⟨q, ?_⟩
  rw [steps_add,
      topEntryEvenLT h (zeros 10 ++ L)
        (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2 * h + 5) ++
          (zeros (2 ^ (5 + (2 * h + 5))) ++ R)))),
      someBind, tlM_spineMk h (zeros 10 ++ L), ← List.append_assoc, zeros_1_10]
  show steps _ (descIn (2 * h + 5 + 4) (teP h) _ _) = _
  exact hq

/-- the even doubling phase's right-hand pad register -/
def evenPadR (h : Nat) (R : List Bool) : List Bool :=
  zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2 * h + 5) ++
    (zeros (2 ^ (5 + (2 * h + 5))) ++ R)))

/-- the even low phase's free `TAIL` instantiated to what `ttA` needs -/
def evenLowFrame (h : Nat) (R : List Bool) : List Bool :=
  ones (2 ^ (2*h+2+8) - 3) ++ teTailT h (evenPadR h R)

/-- `h_low_even_core` with `TAIL` set to the doubling phase's register: the OUT is `ttA h [] _`. -/
theorem hlowEven_core' (h : Nat) (R : List Bool) :
    steps (267 + 38*(2*h+2))
        ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h+1) ++
          (true :: (zeros 10 ++ evenLowFrame h R)))⟩⟩
      = some (ttA h [] (evenPadR h R)) :=
  h_low_even_core h (evenLowFrame h R)

/-- padded even low phase. -/
theorem hlowEven_padded (h : Nat) (R : List Bool) :
    ∀ m : Nat, ∃ j : Nat, j ≤ m ∧
      steps (267 + 38*(2*h+2))
          ⟨.E, 0, ⟨zeros m, false, zeros 21 ++ (uUnits (2*h+1) ++
            (true :: (zeros 10 ++ evenLowFrame h R)))⟩⟩
        = some (ttA h (zeros j) (evenPadR h R)) := by
  intro m
  obtain ⟨j, hjm, hj⟩ := steps_lpad_zeros (267 + 38*(2*h+2)) .E 0 [] false _ (hlowEven_core' h R) m
  exact ⟨j, hjm, by rwa [List.nil_append] at hj⟩

/-- **Obligation H (even) — the low phase meets `doubPhaseEvenL`, unconditional in `h`.** -/
theorem hlowDoubEven (h : Nat) (R : List Bool) :
    ∃ (j : Nat) (q : Int), 10 ≤ j ∧ j ≤ 16 ∧
      steps ((267 + 38*(2*h+2))
          + ((99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6))))
             + ((descTotal (2 * h + 5) + 415)
                + (ladderSteps 5 (2 * h + 5) + exitSteps (5 + (2 * h + 5)))
                + (topGrindSteps (5 + (2 * h + 5)) + exitSteps (5 + (2 * h + 5) + 1) + 74
                   + (27 * (2 * h + 1) + 110)))))
          ⟨.E, 0, ⟨zeros 16, false, zeros 21 ++ (uUnits (2*h+1) ++
            (true :: (zeros 10 ++ evenLowFrame h R)))⟩⟩
        = some ⟨.E, q, ⟨zeros 10 ++ zeros (j - 10), false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2 * h + 1) (seamZ (5 + (2 * h + 5)) R))))⟩⟩ := by
  obtain ⟨j, hj16, hlow⟩ := hlowEven_padded h R 16
  have hj10 : 10 ≤ j := by
    have hm := steps_left_mono _ _ _ hlow
    simp only [ttA, List.length_append, zeros_length, List.length_cons,
      List.length_nil] at hm
    push_cast at hm
    omega
  obtain ⟨q, hdb⟩ := doubPhaseEvenL h (zeros (j - 10)) R
  refine ⟨j, q, hj10, hj16, ?_⟩
  have hz : zeros 10 ++ zeros (j - 10) = zeros j := by
    rw [← zeros_add, show 10 + (j - 10) = j from by omega]
  rw [hz] at hdb
  rw [steps_add, hlow, someBind, hz]
  exact hdb

#print axioms doubPhaseEvenL
#print axioms hlowEven_core'
#print axioms hlowDoubEven

/-! ## M4 anti-vacuity for both obligation-H compositions

MEASURED milestone steps (`x2r2_sim`, instrument anchors green): `M1(2) @732733`,
`M6(2) @733076`, `M1(3) @2852091`, `M6(3) @2852510`, `M1(4) @11329301` — each in state `E` with
right `0^21 1 0^6 …` (M1) resp. the `M6` frame.  So

    M1(2) -> M1(3) = 2 119 358      M1(3) -> M1(4) = 8 477 210

and both composed costs hit those spans exactly. -/

theorem hlowDoubEven_cost0 :
    (267 + 38*(2*0+2))
      + ((99 + (15 * (2 * 0 + 2 + 1) + (3 + 6 * 2 ^ (2 * 0 + 2 + 6))))
         + ((descTotal (2 * 0 + 5) + 415)
            + (ladderSteps 5 (2 * 0 + 5) + exitSteps (5 + (2 * 0 + 5)))
            + (topGrindSteps (5 + (2 * 0 + 5)) + exitSteps (5 + (2 * 0 + 5) + 1) + 74
               + (27 * (2 * 0 + 1) + 110)))) = 2119358 := by decide

theorem hlowDoubOdd_cost0 :
    (419 + 76*0)
      + (((99 + (15 * (2 * 0 + 3) + ((17 + 46 * (2 ^ (2 * 0 + 3 + 7) - 7)) + 6)))
           + 6 * 2 ^ (2 * 0 + 8))
        + (((descTotal (2*0+5) + 415) + (ladderSteps 5 (2*0+5) + exitSteps (5 + (2*0+5))))
           + ((topGrindSteps (5 + (2*0+5)) + exitSteps (5 + (2*0+5) + 1) + 80)
              + (topGrindSteps (5 + (2*0+5) + 1) + (exitSteps (5 + (2*0+5) + 1 + 1) + 4 * 5)
                 + (27 * (2*0+2) + 110))))) = 8477210 := by decide

#print axioms hlowDoubEven_cost0
#print axioms hlowDoubOdd_cost0

/-! ## The REVERSE left-boundary congruence (`steps_lunpad_zeros`)

`steps_lpad_zeros` lifts a run from the trimmed config to the padded one.  The F assembly needs
the OTHER direction: a milestone's OUT left carries leftover boundary blanks, and the next
generation's IN is stated on the TRIMMED (`left = []`) canonical family.  `steps_cltail` is a
genuine bisimulation, so the reverse holds — this is its iterated form.

(Belongs in `BlankNorm.lean`; kept here so the rebuild stays local.) -/
theorem steps_lunpad_zeros : ∀ (k n : Nat) (s : St) (p : Int) (L : List Bool) (hd : Bool)
    (R : List Bool) {s' : St} {p' : Int} {L'' : List Bool} {hd' : Bool} {R' : List Bool},
    steps n ⟨s, p, ⟨L ++ zeros k, hd, R⟩⟩ = some ⟨s', p', ⟨L'', hd', R'⟩⟩ →
    ∃ (L' : List Bool) (i : Nat), i ≤ k ∧ L'' = L' ++ zeros i ∧
      steps n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro n s p L hd R s' p' L'' hd' R' hrun
    refine ⟨L'', 0, Nat.le_refl 0,
      by rw [show (zeros 0 : List Bool) = [] from rfl, List.append_nil], ?_⟩
    rwa [show (zeros 0 : List Bool) = [] from rfl, List.append_nil] at hrun
  | succ k ih =>
    intro n s p L hd R s' p' L'' hd' R' hrun
    have hpad : L ++ zeros (k + 1) = (L ++ zeros k) ++ [false] := by
      rw [← zeros_snoc, List.append_assoc]
    rw [hpad] at hrun
    have hc : cltail ⟨s, p, ⟨L ++ zeros k, hd, R⟩⟩ ⟨s, p, ⟨(L ++ zeros k) ++ [false], hd, R⟩⟩ :=
      ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
    rcases steps_cltail n _ _ hc with ⟨_, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · rw [hrun] at h2; simp at h2
    · have hd2' : d2 = ⟨s', p', ⟨L'', hd', R'⟩⟩ := Option.some.inj (hd2.symm.trans hrun)
      subst hd2'
      rcases d1 with ⟨s1, p1, ⟨l1, h1, r1⟩⟩
      obtain ⟨hst, hpos, hhh, hrr, hll⟩ := hdr
      dsimp only at hst hpos hhh hrr hll
      subst hst; subst hpos; subst hhh; subst hrr
      obtain ⟨L', i, hik, hLi, hrun'⟩ := ih n s p L hd R hd1
      rcases hll with h | h
      · exact ⟨L', i, Nat.le_succ_of_le hik, by rw [← h] at hLi; exact hLi, hrun'⟩
      · refine ⟨L', i + 1, Nat.succ_le_succ hik, ?_, hrun'⟩
        rw [h, hLi, List.append_assoc, zeros_snoc]

#print axioms steps_lunpad_zeros

/-- A list that leaves a `zeros` block when a `zeros` block is appended IS a `zeros` block. -/
theorem zeros_cancel_right (a b : Nat) (X : List Bool) (h : X ++ zeros b = zeros a) :
    X = zeros (a - b) := by
  have hlen : X.length + b = a := by
    have hl := congrArg List.length h
    simpa [zeros_length] using hl
  refine List.append_cancel_right (bs := zeros b) ?_
  rw [← zeros_add, show a - b + b = a from by omega]
  exact h

/-- **Obligation H (even), TRIMMED to the canonical `left = []` form.**  This is the shape the
`M1` milestone family has, so this is the form the F assembly consumes. -/
theorem hlowDoubEven_trim (h : Nat) (R : List Bool) :
    ∃ (m : Nat) (q : Int),
      steps ((267 + 38*(2*h+2))
          + ((99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6))))
             + ((descTotal (2 * h + 5) + 415)
                + (ladderSteps 5 (2 * h + 5) + exitSteps (5 + (2 * h + 5)))
                + (topGrindSteps (5 + (2 * h + 5)) + exitSteps (5 + (2 * h + 5) + 1) + 74
                   + (27 * (2 * h + 1) + 110)))))
          ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h+1) ++
            (true :: (zeros 10 ++ evenLowFrame h R)))⟩⟩
        = some ⟨.E, q, ⟨zeros m, false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2 * h + 1) (seamZ (5 + (2 * h + 5)) R))))⟩⟩ := by
  obtain ⟨j, q, hj10, _, hrun⟩ := hlowDoubEven h R
  rw [show zeros 10 ++ zeros (j - 10) = zeros j from by
        rw [← zeros_add, show 10 + (j - 10) = j from by omega],
      show (zeros 16 : List Bool) = [] ++ zeros 16 from by rw [List.nil_append]] at hrun
  obtain ⟨L', i, _, hLi, htrim⟩ := steps_lunpad_zeros 16 _ _ _ _ _ _ hrun
  exact ⟨j - i, q, by rw [← zeros_cancel_right j i L' hLi.symm]; exact htrim⟩

/-- **Obligation H (odd), TRIMMED to the canonical `left = []` form.** -/
theorem hlowDoubOdd_trim (h : Nat) (R : List Bool) :
    ∃ (m : Nat) (q : Int),
      steps ((419 + 76*h)
          + (((99 + (15 * (2 * h + 3) + ((17 + 46 * (2 ^ (2 * h + 3 + 7) - 7)) + 6)))
               + 6 * 2 ^ (2 * h + 8))
            + (((descTotal (2*h+5) + 415) + (ladderSteps 5 (2*h+5) + exitSteps (5 + (2*h+5))))
               + ((topGrindSteps (5 + (2*h+5)) + exitSteps (5 + (2*h+5) + 1) + 80)
                  + (topGrindSteps (5 + (2*h+5) + 1) + (exitSteps (5 + (2*h+5) + 1 + 1) + 4 * 5)
                     + (27 * (2*h+2) + 110))))))
          ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h+2) ++
            (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R)))))⟩⟩
        = some ⟨.E, q, ⟨zeros m, false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2*h+2) (oddSeamZ (5 + (2*h+5) + 1) 5 R))))⟩⟩ := by
  obtain ⟨j, q, hj10, _, hrun⟩ := hlowDoubOdd h R
  rw [show zeros 10 ++ zeros (j - 10) = zeros j from by
        rw [← zeros_add, show 10 + (j - 10) = j from by omega],
      show (zeros 16 : List Bool) = [] ++ zeros 16 from by rw [List.nil_append]] at hrun
  obtain ⟨L', i, _, hLi, htrim⟩ := steps_lunpad_zeros 16 _ _ _ _ _ _ hrun
  exact ⟨j - i, q, by rw [← zeros_cancel_right j i L' hLi.symm]; exact htrim⟩

#print axioms hlowDoubEven_trim
#print axioms hlowDoubOdd_trim

/-! ## F item 2 — the CROSS-GENERATION frame identity

The OUT frame of one milestone must BE the IN frame of the next.  The key is that `uUnits`'
repetition unit `1 0^6` IS `frameZ`'s: `frameZ (j+1) Z = frameZ j (0^5 ++ 1 0 :: Z)`, and
`1 0 :: 0^5` re-associates to `1 :: 0^6`.  So the whole frame block collapses to `uUnits`. -/

theorem uUnits_snoc : ∀ k : Nat, uUnits k ++ (true :: zeros 6) = uUnits (k + 1) := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
    show ((true :: zeros 6) ++ uUnits k) ++ (true :: zeros 6) = (true :: zeros 6) ++ uUnits (k + 1)
    rw [List.append_assoc, ih]

/-- **The frame block IS a `uUnits` block.** -/
theorem uUnits_frameZ : ∀ (j : Nat) (Z : List Bool),
    true :: (zeros 6 ++ (true :: false :: frameZ j Z)) = uUnits (j + 1) ++ (true :: false :: Z) := by
  intro j
  induction j with
  | zero => intro Z; rfl
  | succ j ih =>
    intro Z
    show true :: (zeros 6 ++ (true :: false :: frameZ j (zeros 5 ++ (true :: false :: Z)))) = _
    rw [ih (zeros 5 ++ (true :: false :: Z))]
    show uUnits (j + 1) ++ (true :: (zeros 6 ++ (true :: false :: Z))) = _
    rw [show (true :: (zeros 6 ++ (true :: false :: Z)) : List Bool)
          = (true :: zeros 6) ++ (true :: false :: Z) from rfl,
        ← List.append_assoc, uUnits_snoc]

#print axioms uUnits_snoc
#print axioms uUnits_frameZ

def oddPadTail (h : Nat) (R : List Bool) : List Bool :=
  zeros 16 ++ (ladderPad 5 (2*h+5) ++
    (zeros (2 ^ (5 + (2*h+5))) ++ (zeros (2 ^ (5 + (2*h+5) + 1)) ++ R)))

theorem oddPadR_split (h : Nat) (R : List Bool) :
    oddPadR h R = zeros 25 ++ oddPadTail h R := rfl

/-- **EVEN OUT seam = ODD IN seam.**  The even milestone's `seamZ` tail, with one leading `0` from
the frame block, IS the odd low phase's `0^4 (10)^6 1^4 …` entry word. -/
theorem evenSeam_oddIn (h : Nat) (R : List Bool) :
    false :: seamZ (5 + (2*h+5)) (zeros 16 ++ oddPadTail h R)
      = zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R)) := by
  have hp : (2:Nat) ^ 11 ≤ 2 ^ (2*h+3+8) := Nat.pow_le_pow_right (by omega) (by omega)
  have h2048 : (2:Nat) ^ 11 = 2048 := by decide
  have hones : ones (2 ^ (2*h+3+8) - 9) = ones 4 ++ ones (2 ^ (2*h+3+8) - 13) := by
    rw [← ones_add, show 4 + (2 ^ (2*h+3+8) - 13) = 2 ^ (2*h+3+8) - 9 from by omega]
  have hz : (zeros 7 ++ (zeros 16 ++ oddPadTail h R) : List Bool)
      = zeros 23 ++ oddPadTail h R := by rw [← List.append_assoc, ← zeros_add]
  show false :: (_ ++ (ones (2 ^ (5 + (2*h+5) + 1) - 9) ++ (false :: false ::
      (descCascade (5 + (2*h+5) - 2) ++ (false :: false ::
        (zeros 7 ++ (zeros 16 ++ oddPadTail h R))))))) = _
  rw [show 5 + (2*h+5) + 1 = 2*h+3+8 from by omega,
      show 5 + (2*h+5) - 2 = 2*h+8 from by omega, hones, hz]
  show _ = zeros 4 ++ (pow10 6 ++ (ones 4 ++ (ones (2 ^ (2*h+3+8) - 13) ++
      (false :: false :: (descCascade (2*h+8) ++ (zeros 25 ++ oddPadTail h R))))))
  rfl

#print axioms evenSeam_oddIn

/-- **EVEN OUT frame IS the ODD IN frame** — the cross-generation milestone identity, even→odd. -/
theorem evenOut_is_oddIn (h : Nat) (R : List Bool) :
    zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
        frameZ (2*h+1) (seamZ (5 + (2*h+5)) (zeros 16 ++ oddPadTail h R)))))
      = zeros 21 ++ (uUnits (2*h+2) ++
          (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R))))) := by
  rw [uUnits_frameZ (2*h+1) _, show 2*h+1+1 = 2*h+2 from by omega]
  show zeros 21 ++ (uUnits (2*h+2) ++
    (true :: (false :: seamZ (5 + (2*h+5)) (zeros 16 ++ oddPadTail h R)))) = _
  rw [evenSeam_oddIn h R]

def evenPadTail (h : Nat) (R : List Bool) : List Bool :=
  zeros 16 ++ (ladderPad 5 (2*h+5) ++ (zeros (2 ^ (5 + (2*h+5))) ++ R))

theorem evenPadR_split (h : Nat) (R : List Bool) :
    evenPadR h R = zeros 25 ++ evenPadTail h R := rfl

/-- **ODD OUT seam = EVEN IN seam.** -/
theorem oddSeam_evenIn (h : Nat) (R : List Bool) :
    false :: oddSeamZ (5 + (2*h+5) + 1) 5 (zeros 16 ++ evenPadTail (h+1) R)
      = zeros 10 ++ evenLowFrame (h+1) R := by
  have hz : (zeros 7 ++ (zeros 16 ++ evenPadTail (h+1) R) : List Bool)
      = zeros 23 ++ evenPadTail (h+1) R := by rw [← List.append_assoc, ← zeros_add]
  show false :: (zeros (2*5-1) ++ (ones (2 ^ (5 + (2*h+5) + 1 + 1) - 3) ++ (false :: false ::
      (descCascade (5 + (2*h+5) + 1 + 1 - 3) ++ (false :: false ::
        (zeros 7 ++ (zeros 16 ++ evenPadTail (h+1) R))))))) = _
  rw [show 5 + (2*h+5) + 1 + 1 = 2*(h+1)+2+8 from by omega,
      show 2*(h+1)+2+8 - 3 = 2*(h+1)+7 from by omega, hz]
  show _ = zeros 10 ++ (ones (2 ^ (2*(h+1)+2+8) - 3) ++ (false :: false ::
      (descCascade (2*(h+1)+7) ++ (zeros 25 ++ evenPadTail (h+1) R))))
  rfl

/-- **ODD OUT frame IS the EVEN IN frame** — the cross-generation milestone identity, odd→even. -/
theorem oddOut_is_evenIn (h : Nat) (R : List Bool) :
    zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
        frameZ (2*h+2) (oddSeamZ (5 + (2*h+5) + 1) 5 (zeros 16 ++ evenPadTail (h+1) R)))))
      = zeros 21 ++ (uUnits (2*(h+1)+1) ++
          (true :: (zeros 10 ++ evenLowFrame (h+1) R))) := by
  rw [uUnits_frameZ (2*h+2) _, show 2*h+2+1 = 2*(h+1)+1 from by omega]
  show zeros 21 ++ (uUnits (2*(h+1)+1) ++
    (true :: (false :: oddSeamZ (5 + (2*h+5) + 1) 5 (zeros 16 ++ evenPadTail (h+1) R)))) = _
  rw [oddSeam_evenIn h R]

#print axioms evenOut_is_oddIn
#print axioms oddSeam_evenIn
#print axioms oddOut_is_evenIn

/-- **The REVERSE right-boundary congruence** — twin of `steps_lunpad_zeros`.  Trailing blanks on
`right` are semantically inert, so a run proven on the PADDED tape yields the run on the trimmed
one.  (Belongs in `BlankNorm.lean`.) -/
theorem steps_runpad_zeros : ∀ (k n : Nat) (s : St) (p : Int) (L : List Bool) (hd : Bool)
    (R : List Bool) {s' : St} {p' : Int} {L' : List Bool} {hd' : Bool} {R'' : List Bool},
    steps n ⟨s, p, ⟨L, hd, R ++ zeros k⟩⟩ = some ⟨s', p', ⟨L', hd', R''⟩⟩ →
    ∃ (R' : List Bool) (i : Nat), i ≤ k ∧ R'' = R' ++ zeros i ∧
      steps n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro n s p L hd R s' p' L' hd' R'' hrun
    refine ⟨R'', 0, Nat.le_refl 0,
      by rw [show (zeros 0 : List Bool) = [] from rfl, List.append_nil], ?_⟩
    rwa [show (zeros 0 : List Bool) = [] from rfl, List.append_nil] at hrun
  | succ k ih =>
    intro n s p L hd R s' p' L' hd' R'' hrun
    have hpad : R ++ zeros (k + 1) = (R ++ zeros k) ++ [false] := by
      rw [← zeros_snoc, List.append_assoc]
    rw [hpad] at hrun
    have hc : crtail ⟨s, p, ⟨L, hd, R ++ zeros k⟩⟩ ⟨s, p, ⟨L, hd, (R ++ zeros k) ++ [false]⟩⟩ :=
      ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
    rcases steps_crtail n _ _ hc with ⟨_, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · rw [hrun] at h2; simp at h2
    · have hd2' : d2 = ⟨s', p', ⟨L', hd', R''⟩⟩ := Option.some.inj (hd2.symm.trans hrun)
      subst hd2'
      rcases d1 with ⟨s1, p1, ⟨l1, h1, r1⟩⟩
      obtain ⟨hst, hpos, hll, hhh, hrr⟩ := hdr
      dsimp only at hst hpos hll hhh hrr
      subst hst; subst hpos; subst hll; subst hhh
      obtain ⟨R', i, hik, hRi, hrun'⟩ := ih n s p L hd R hd1
      rcases hrr with h | h
      · exact ⟨R', i, Nat.le_succ_of_le hik, by rw [← h] at hRi; exact hRi, hrun'⟩
      · refine ⟨R', i + 1, Nat.succ_le_succ hik, ?_, hrun'⟩
        rw [h, hRi, List.append_assoc, zeros_snoc]

#print axioms steps_runpad_zeros

/-! ## The normalized milestone family and its cycle -/

def costEven (h : Nat) : Nat :=
  (267 + 38*(2*h+2))
    + ((99 + (15 * (2 * h + 2 + 1) + (3 + 6 * 2 ^ (2 * h + 2 + 6))))
       + ((descTotal (2 * h + 5) + 415)
          + (ladderSteps 5 (2 * h + 5) + exitSteps (5 + (2 * h + 5)))
          + (topGrindSteps (5 + (2 * h + 5)) + exitSteps (5 + (2 * h + 5) + 1) + 74
             + (27 * (2 * h + 1) + 110))))

def costOdd (h : Nat) : Nat :=
  (419 + 76*h)
    + (((99 + (15 * (2 * h + 3) + ((17 + 46 * (2 ^ (2 * h + 3 + 7) - 7)) + 6)))
         + 6 * 2 ^ (2 * h + 8))
      + (((descTotal (2*h+5) + 415) + (ladderSteps 5 (2*h+5) + exitSteps (5 + (2*h+5))))
         + ((topGrindSteps (5 + (2*h+5)) + exitSteps (5 + (2*h+5) + 1) + 80)
            + (topGrindSteps (5 + (2*h+5) + 1) + (exitSteps (5 + (2*h+5) + 1 + 1) + 4 * 5)
               + (27 * (2*h+2) + 110)))))

/-- milestone `M1(2h+2)`, normalized: state `E`, pos `0`, left `[]`. -/
def MEven (h : Nat) (R : List Bool) : Cfg :=
  ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h+1) ++
    (true :: (zeros 10 ++ evenLowFrame h R)))⟩⟩

/-- milestone `M1(2h+3)`, normalized. -/
def MOdd (h : Nat) (R : List Bool) : Cfg :=
  ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h+2) ++
    (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R)))))⟩⟩

/-- **THE EVEN CYCLE** — `MEven h → MOdd h` in `costEven h` steps, right tape landing EXACTLY on
the next milestone's; only the left boundary blanks and the translation remain to normalize. -/
theorem cycleEven (h : Nat) (R : List Bool) :
    ∃ (m : Nat) (q : Int),
      steps (costEven h) (MEven h (zeros 16 ++ oddPadTail h R))
        = some ⟨.E, q, ⟨zeros m, false, zeros 21 ++ (uUnits (2*h+2) ++
            (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrame h R)))))⟩⟩ := by
  obtain ⟨m, q, hrun⟩ := hlowDoubEven_trim h (zeros 16 ++ oddPadTail h R)
  exact ⟨m, q, by rw [← evenOut_is_oddIn h R]; exact hrun⟩

/-- **THE ODD CYCLE** — `MOdd h → MEven (h+1)`. -/
theorem cycleOdd (h : Nat) (R : List Bool) :
    ∃ (m : Nat) (q : Int),
      steps (costOdd h) (MOdd h (zeros 16 ++ evenPadTail (h+1) R))
        = some ⟨.E, q, ⟨zeros m, false, zeros 21 ++ (uUnits (2*(h+1)+1) ++
            (true :: (zeros 10 ++ evenLowFrame (h+1) R)))⟩⟩ := by
  obtain ⟨m, q, hrun⟩ := hlowDoubOdd_trim h (zeros 16 ++ evenPadTail (h+1) R)
  exact ⟨m, q, by rw [← oddOut_is_evenIn h R]; exact hrun⟩

#print axioms cycleEven
#print axioms cycleOdd

/-! ## Tools for the final chain -/

/-- **Invariant non-halting** — no explicit milestone family (hence no choice) is needed: a
predicate preserved by one nonempty halt-free segment already forbids halting.  Strong induction
via a fuel bound `B`. -/
theorem nonhalt_of_invariant_aux (P : Cfg → Prop)
    (hstep : ∀ c, P c → ∃ n, 1 ≤ n ∧ ∃ c', P c' ∧ steps n c = some c') :
    ∀ (B N : Nat), N ≤ B → ∀ c, P c → steps N c ≠ none := by
  intro B
  induction B with
  | zero =>
    intro N hN c _
    rw [show N = 0 from by omega]
    intro h
    rw [show steps 0 c = some c from rfl] at h
    exact absurd h (by simp)
  | succ B ih =>
    intro N hN c hc
    obtain ⟨n, hn1, c', hc', hrun⟩ := hstep c hc
    by_cases hle : N ≤ n
    · exact steps_prefix_ne_none hrun hle
    · have e : N = n + (N - n) := by omega
      rw [e, steps_add, hrun]
      exact ih (N - n) (by omega) c' hc'

theorem nonhalt_of_invariant (P : Cfg → Prop)
    (hstep : ∀ c, P c → ∃ n, 1 ≤ n ∧ ∃ c', P c' ∧ steps n c = some c')
    (c : Cfg) (hc : P c) : ∀ N : Nat, steps N c ≠ none :=
  fun N => nonhalt_of_invariant_aux P hstep N N (Nat.le_refl N) c hc

/-- the ladder pad is one explicit block of blanks -/
def padLen (b : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => 2 ^ b + padLen (b + 1) n

theorem ladderPad_zeros : ∀ (n b : Nat), ladderPad b n = zeros (padLen b n) := by
  intro n
  induction n with
  | zero => intro b; rfl
  | succ n ih =>
    intro b
    show zeros (2 ^ b) ++ ladderPad (b + 1) n = _
    rw [ih (b + 1)]
    show _ = zeros (2 ^ b + padLen (b + 1) n)
    rw [zeros_add]

#print axioms nonhalt_of_invariant
#print axioms ladderPad_zeros
