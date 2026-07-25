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
