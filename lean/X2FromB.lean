import T7Entry
open X2

/-!
# `x2` started in state `B` — the orbit that decides holdout `C`

`C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` is `x2`'s transition graph with the states
cyclically renamed (`σ : A→F, B→A, C→B, D→C, E→D, F→E`, verified on all six rows), so

    C never halts  ⟺  x2's own `step` never halts from ⟨B, 0, blank⟩.

MEASURED (`CANDC_SPEC_2026-07-25.md`): the `B`-orbit's milestones have state `E`, `|left| = 1`,
head position stepping by a uniform `−6`, and the marker words

    even-type h : 0^21 ++ uUnits (2h+1) ++ (1 :: 0^10 ++ ones (2^(2h+11) − 3) ++ 0 0 :: descCascade (2h+8) ++ …)
    odd-type  h : 0^21 ++ uUnits (2h)   ++ (1 :: 0^4  ++ pow10 6 ++ …)

verified at `h = 0` (`uUnits 1`, `ones 2045 = 2^11−3`) and `h = 1` (`uUnits 3`,
`ones 8189 = 2^13−3`); odd-type at `h = 0` (`uUnits 0`) and `h = 1` (`uUnits 2`).

So the `B`-orbit's even-type milestone has the **even-type SHAPE at the odd-type SCALE** — the
`0^10 ++ ones` layout of `MEven h` but the exponent `2^(2h+11)` and cascade `descCascade (2h+8)` of
`MOdd h`.  That single hybrid is the whole difference from the `A`-orbit.

**No machine decided. No label upgraded.**
-/

namespace FromB

/-- the `B`-orbit's even-type low-phase tail: even SHAPE, odd SCALE -/
def lowFrameB (h : Nat) (R : List Bool) : List Bool :=
  ones (2 ^ (2*h+11) - 3) ++ (false :: false :: (descCascade (2*h+8) ++ R))

/-- the `B`-orbit's even-type milestone -/
def MEvenB (h : Nat) (R : List Bool) : Cfg :=
  ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h+1) ++ (true :: (zeros 10 ++ lowFrameB h R)))⟩⟩

/-- **the low phase applies VERBATIM** — `h_low_even_core` is `∀ TAIL`, and the `B`-orbit's
even-type milestone is exactly its IN with `TAIL := lowFrameB h R`. -/
theorem hlowB_core (h : Nat) (R : List Bool) :
    steps (267 + 38*(2*h+2)) (MEvenB h R)
      = some ⟨.E, -5, ⟨[false], false,
          false :: pow10 4 ++ ones 9 ++ false :: false ::
            (rUnits (2*h+3) ++ (true :: false :: false :: lowFrameB h R))⟩⟩ :=
  h_low_even_core h (lowFrameB h R)

#print axioms hlowB_core

-- M1 check: the measured B-orbit milestone at h = 0 has right length 4120 with the tail trimmed;
-- MEvenB 0 [] is that word with the pad register empty.
#eval ((MEvenB 0 []).tape.right.length, (MEvenB 1 []).tape.right.length)

end FromB

namespace FromB
/-! ## M4 anti-vacuity — the family IS the real orbit

`#eval` (decidable equality on `Cfg`) at the two measured milestones:

    steps 2866581  ⟨B,0,blank⟩ == some ⟨E, −33, ⟨zeros 1, false, (MEvenB 0 (zeros 1)).right⟩⟩   TRUE
    steps 45042285 ⟨B,0,blank⟩ == some ⟨E, −45, ⟨zeros 1, false, (MEvenB 1 (zeros 1)).right⟩⟩   TRUE

Not "matches the shape" — literally equal as configurations, at both `h = 0` and `h = 1`. -/

def initB : Cfg := ⟨.B, 0, ⟨[], false, []⟩⟩

/-- the `B`-orbit's ODD-type low-phase tail: `2^(2h+10)` where `x2`'s `MOdd h` has `2^(2h+11)` -/
def oddLowFrameB (h : Nat) (R : List Bool) : List Bool :=
  ones (2 ^ (2*h+10) - 13) ++ (false :: false :: (descCascade (2*h+7) ++ R))

/-- the `B`-orbit's odd-type milestone (`uUnits (2h)`, where `x2`'s `MOdd h` has `uUnits (2h+2)`) -/
def MOddB (h : Nat) (R : List Bool) : Cfg :=
  ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*h) ++
    (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrameB h R)))))⟩⟩

/-- **the ODD low phase also applies VERBATIM, for `h ≥ 1`.**  `h_low_odd_core k` needs
`uUnits (2k+2)`, and the `B`-orbit's odd-type at `h` has `uUnits (2h)` — so `k = h-1` matches, and
the lemma is `∀ FRAME`. -/
theorem hlowBodd_core (h : Nat) (R : List Bool) :
    steps (419 + 76*h) (MOddB (h+1) R)
      = some ⟨.E, -5, ⟨[false], false,
          false :: pow10 4 ++ ones 9 ++ false :: false ::
            (rUnits (2*h+3) ++ (pow10 10 ++ oddLowFrameB (h+1) R))⟩⟩ := by
  have e : 2*(h+1) = 2*h+2 := by omega
  show steps (419 + 76*h) ⟨.E, 0, ⟨[], false, zeros 21 ++ (uUnits (2*(h+1)) ++
    (true :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrameB (h+1) R)))))⟩⟩ = _
  rw [e]
  exact h_low_odd_core h (oddLowFrameB (h+1) R)

#print axioms hlowBodd_core

-- Recorded as a MEASUREMENT, not a theorem: `native_decide` would add `Lean.ofReduceBool`
-- (trusting the compiler), which this development does not use.  The corresponding THEOREM will be
-- the chunked-`rfl` entry segment, exactly as `T7Entry.entryM12` is for the `A`-orbit.
#eval ((steps 2866581 initB) == some ⟨.E, -33, ⟨zeros 1, false, (MEvenB 0 (zeros 1)).tape.right⟩⟩,
       (steps 45042285 initB) == some ⟨.E, -45, ⟨zeros 1, false, (MEvenB 1 (zeros 1)).tape.right⟩⟩,
       (steps 727067 initB) == some ⟨.E, -27, ⟨zeros 1, false, (MOddB 0 (zeros 1)).tape.right⟩⟩,
       (steps 11302995 initB) == some ⟨.E, -39, ⟨zeros 1, false, (MOddB 1 (zeros 1)).tape.right⟩⟩)
-- all four TRUE: the B-orbit's even- AND odd-type milestones are exactly MEvenB/MOddB h (zeros 1)

end FromB

namespace FromB
/-! ## The `B`-orbit doubling-phase entry

`x2`'s `ttA → ttB → ttC → ttD → descIn (2h+9)` chain is built from four lemmas that are all fully
`∀` — `p1tLL` (∀REST), `rUnitsFold` (∀n ∀Y), `bridge` (∀b ∀Y), `eChewFold` (∀m ∀r ∀Y).  So the
`B`-orbit variant, whose only difference is the exponent `2^(2h+11)` in place of `2^(2h+10)` and
the cascade `descCascade (2h+8)` in place of `(2h+7)`, is a pure RE-INSTANTIATION.  It lands one
descent level higher: **`descIn (2h+10)`**. -/

def teTailB (h : Nat) (R : List Bool) : List Bool :=
  false :: false :: (descCascade (2*h+8) ++ R)

theorem lowFrameB_split (h : Nat) (R : List Bool) :
    lowFrameB h R = ones (2 ^ (2*h+11) - 3) ++ teTailB h R := rfl

def ttA_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5, ⟨[false] ++ LL, false,
    false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
      (rUnits (2*h+3) ++ (true :: false :: false ::
        (ones (2 ^ (2*h+11) - 3) ++ teTailB h R))))))⟩⟩

def ttB_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5 + 19, ⟨p1tL ++ LL, false,
    false :: (rUnits (2*h+3) ++
      (true :: false :: false :: (ones (2 ^ (2*h+11) - 3) ++ teTailB h R)))⟩⟩

def ttC_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2*h+3 : Nat) : Int),
    ⟨rUnitsDep (2*h+3) (p1tL ++ LL), false,
     false :: (true :: false :: false :: (ones (2 ^ (2*h+11) - 3) ++ teTailB h R))⟩⟩

def ttD_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 3,
    ⟨false :: false :: true :: rUnitsDep (2*h+3) (p1tL ++ LL), false,
     false :: (ones (2 ^ (2*h+11) - 3) ++ teTailB h R)⟩⟩

theorem ttAB_B (h : Nat) (LL R : List Bool) : steps 99 (ttA_B h LL R) = some (ttB_B h LL R) := by
  unfold ttA_B ttB_B
  exact p1tLL (-5) LL (rUnits (2*h+3) ++
    (true :: false :: false :: (ones (2 ^ (2*h+11) - 3) ++ teTailB h R)))

theorem ttBC_B (h : Nat) (LL R : List Bool) :
    steps (15 * (2*h+3)) (ttB_B h LL R) = some (ttC_B h LL R) := by
  unfold ttB_B ttC_B
  exact rUnitsFold (2*h+3) (-5 + 19) (p1tL ++ LL)
    (true :: false :: false :: (ones (2 ^ (2*h+11) - 3) ++ teTailB h R))

theorem ttCD_B (h : Nat) (LL R : List Bool) : steps 3 (ttC_B h LL R) = some (ttD_B h LL R) := by
  unfold ttC_B ttD_B
  exact bridge _ (2 ^ (2*h+11) - 3) _ (teTailB h R)

#print axioms ttAB_B
#print axioms ttBC_B
#print axioms ttCD_B
end FromB

namespace FromB
def tePB (h : Nat) : Int :=
  -5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 3 + 2 * ((2 ^ (2*h+9) : Nat) : Int)

theorem ttD_BdescIn (h : Nat) (LL R : List Bool) :
    steps (6 * 2 ^ (2*h+9)) (ttD_B h LL R)
      = some (descIn (2*h+10) (tePB h) (tlM h LL) R) := by
  have hsplit : (2 : Nat) ^ (2*h+11) - 3 = 2 * 2 ^ (2*h+9) + (2 ^ (2*h+10) - 3) := by
    have e11 : (2:Nat)^(2*h+11) = 4 * 2^(2*h+9) := by
      rw [show 2*h+11 = (2*h+9)+2 from by omega, Nat.pow_add,
          show (2:Nat)^2 = 4 from rfl, Nat.mul_comm]
    have e10 : (2:Nat)^(2*h+10) = 2 * 2^(2*h+9) := by
      rw [show 2*h+10 = (2*h+9)+1 from by omega, Nat.pow_add,
          show (2:Nat)^1 = 2 from rfl, Nat.mul_comm]
    have h9 : 4 ≤ (2:Nat)^(2*h+9) := by
      have : (2:Nat)^2 ≤ 2^(2*h+9) := Nat.pow_le_pow_right (by decide) (by omega)
      omega
    omega
  unfold ttD_B
  rw [hsplit,
      eChewFold (2 ^ (2*h+9)) _ (2 ^ (2*h+10) - 3)
        (false :: false :: true :: rUnitsDep (2*h+3) (p1tL ++ LL)) (teTailB h R)]
  refine congrArg some ?_
  show (⟨.E, _, ⟨pow01 (2 ^ (2*h+9)) ++ tlM h LL, false,
      false :: (ones (2 ^ (2*h+10) - 3) ++ teTailB h R)⟩⟩ : Cfg) = _
  show _ = (⟨.E, tePB h, ⟨pow01 (2 ^ (2*h+10 - 1)) ++ tlM h LL, false,
      false :: (ones (2 ^ (2*h+10) - 3) ++
        (false :: false :: (descCascade (2*h+10 - 2) ++ R)))⟩⟩ : Cfg)
  rw [show 2*h+10-1 = 2*h+9 from by omega, show 2*h+10-2 = 2*h+8 from by omega]
  unfold teTailB tePB
  rfl

/-- **the `B`-orbit doubling-phase entry** — one descent level higher than `x2`'s -/
theorem topEntryB (h : Nat) (LL R : List Bool) :
    steps (99 + (15 * (2*h+3) + (3 + 6 * 2 ^ (2*h+9)))) (ttA_B h LL R)
      = some (descIn (2*h+10) (tePB h) (tlM h LL) R) := by
  rw [steps_add, ttAB_B h LL R, someBind, steps_add, ttBC_B h LL R, someBind,
      steps_add, ttCD_B h LL R, someBind]
  exact ttD_BdescIn h LL R

#print axioms ttD_BdescIn
#print axioms topEntryB
end FromB

namespace FromB
/-- **the `B`-orbit doubling phase** — `topEntryB ∘ evenSpine` at `n = 2h+6` (`x2`'s even phase
uses `n = 2h+5`; the `B`-orbit sits one descent level higher).  The marker bridge
`tlM_spineMk` is reused verbatim. -/
theorem doubPhaseB (h : Nat) (L R : List Bool) :
    ∃ q : Int,
      steps ((99 + (15 * (2*h+3) + (3 + 6 * 2 ^ (2*h+9))))
             + ((descTotal (2*h+6) + 415)
                + (ladderSteps 5 (2*h+6) + exitSteps (5 + (2*h+6)))
                + (topGrindSteps (5 + (2*h+6)) + exitSteps (5 + (2*h+6) + 1) + 74
                   + (27 * (2*h+1) + 110))))
          (ttA_B h (zeros 10 ++ L)
            (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2*h+6) ++
              (zeros (2 ^ (5 + (2*h+6))) ++ R)))))
        = some ⟨.E, q, ⟨zeros 10 ++ L, false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2*h+1) (seamZ (5 + (2*h+6)) R))))⟩⟩ := by
  obtain ⟨q, hq⟩ := evenSpine (2*h+6) (2*h+1) (tePB h) L R
  refine ⟨q, ?_⟩
  rw [steps_add,
      topEntryB h (zeros 10 ++ L)
        (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2*h+6) ++
          (zeros (2 ^ (5 + (2*h+6))) ++ R)))),
      someBind, tlM_spineMk h (zeros 10 ++ L), ← List.append_assoc, zeros_1_10]
  show steps _ (descIn (2*h+6+4) (tePB h) _ _) = _
  exact hq

#print axioms doubPhaseB
end FromB

namespace FromB
/-- the `B`-orbit's odd-side pad register -/
def oddPadTailB (h : Nat) (R : List Bool) : List Bool :=
  zeros 16 ++ (ladderPad 5 (2*h+6) ++
    (zeros (2 ^ (5 + (2*h+6))) ++ (zeros (2 ^ (5 + (2*h+6) + 1)) ++ R)))

/-- **`B`-orbit EVEN-OUT seam = ODD-IN seam.**  Same proof shape as `x2`'s `evenSeam_oddIn`,
re-indexed: `seamZ (2h+11)` carries `ones (2^(2h+12) − 9)` and `descCascade (2h+9)`, which is
exactly `ones 4 ++ oddLowFrameB (h+1) …`. -/
theorem evenSeamB_oddInB (h : Nat) (R : List Bool) :
    false :: seamZ (5 + (2*h+6)) (zeros 16 ++ oddPadTailB h R)
      = zeros 4 ++ (pow10 6 ++ (ones 4 ++ oddLowFrameB (h+1) (zeros 25 ++ oddPadTailB h R))) := by
  have hp : (2:Nat) ^ 12 ≤ 2 ^ (2*(h+1)+10) := Nat.pow_le_pow_right (by omega) (by omega)
  have h4096 : (2:Nat) ^ 12 = 4096 := by decide
  have hones : ones (2 ^ (2*(h+1)+10) - 9) = ones 4 ++ ones (2 ^ (2*(h+1)+10) - 13) := by
    rw [← ones_add, show 4 + (2 ^ (2*(h+1)+10) - 13) = 2 ^ (2*(h+1)+10) - 9 from by omega]
  have hz : (zeros 7 ++ (zeros 16 ++ oddPadTailB h R) : List Bool)
      = zeros 23 ++ oddPadTailB h R := by rw [← List.append_assoc, ← zeros_add]
  show false :: (_ ++ (ones (2 ^ (5 + (2*h+6) + 1) - 9) ++ (false :: false ::
      (descCascade (5 + (2*h+6) - 2) ++ (false :: false ::
        (zeros 7 ++ (zeros 16 ++ oddPadTailB h R))))))) = _
  rw [show 5 + (2*h+6) + 1 = 2*(h+1)+10 from by omega,
      show 5 + (2*h+6) - 2 = 2*(h+1)+7 from by omega, hones, hz]
  show _ = zeros 4 ++ (pow10 6 ++ (ones 4 ++ (ones (2 ^ (2*(h+1)+10) - 13) ++
      (false :: false :: (descCascade (2*(h+1)+7) ++ (zeros 25 ++ oddPadTailB h R))))))
  rfl

#print axioms evenSeamB_oddInB
end FromB

namespace FromB
/-! ## The `B`-orbit ODD entry — the same five `∀` lemmas, re-indexed

`x2`'s odd chain uses `p1tLL`, `rUnitsFold`, `crossCarry`, `odTurn`, `eChewFold`, all fully `∀`.
The `B`-orbit's odd-type `M6` is `x2`'s `odA` with the block exponent and cascade index each `+1`
and `rUnits` unchanged, so the chain re-instantiates. -/

def odA_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5, ⟨[false] ++ LL, false,
    false :: (pow10 4 ++ (ones 9 ++ (false :: false ::
      (rUnits (2*h+3) ++ (pow10 10 ++
        (ones (2 ^ (2*h+12) - 13) ++
          (false :: false :: (descCascade (2*h+9) ++ R))))))))⟩⟩

def odB_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5 + 19, ⟨p1tL ++ LL, false,
    false :: (rUnits (2*h+3) ++ (pow10 10 ++
      (ones (2 ^ (2*h+12) - 13) ++ (false :: false :: (descCascade (2*h+9) ++ R)))))⟩⟩

def odC_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2*h+3 : Nat) : Int),
    ⟨rUnitsDep (2*h+3) (p1tL ++ LL), false,
     false :: (pow10 10 ++
       (ones (2 ^ (2*h+12) - 13) ++ (false :: false :: (descCascade (2*h+9) ++ R))))⟩⟩

def odD_B (h : Nat) (LL R : List Bool) : Cfg :=
  ⟨.E, -5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 17
      + 2 * ((2 ^ (2*h+11) - 7 : Nat) : Int) + 6,
    ⟨ones 20 ++ (false :: false ::
      (pow10 (2 ^ (2*h+11) - 7) ++ (true :: rUnitsDep (2*h+3) (p1tL ++ LL)))), false,
     false :: (descCascade (2*h+9) ++ R)⟩⟩

theorem odAB_B (h : Nat) (LL R : List Bool) : steps 99 (odA_B h LL R) = some (odB_B h LL R) := by
  unfold odA_B odB_B
  exact p1tLL (-5) LL (rUnits (2*h+3) ++ (pow10 10 ++
    (ones (2 ^ (2*h+12) - 13) ++ (false :: false :: (descCascade (2*h+9) ++ R)))))

theorem odBC_B (h : Nat) (LL R : List Bool) :
    steps (15 * (2*h+3)) (odB_B h LL R) = some (odC_B h LL R) := by
  unfold odB_B odC_B
  exact rUnitsFold (2*h+3) (-5 + 19) (p1tL ++ LL)
    (pow10 10 ++ (ones (2 ^ (2*h+12) - 13) ++ (false :: false :: (descCascade (2*h+9) ++ R))))

theorem odCcarry_B (h : Nat) (LL R : List Bool) :
    steps (17 + 46 * (2 ^ (2*h+11) - 7)) (odC_B h LL R)
      = some ⟨.E, -5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 17
              + 2 * ((2 ^ (2*h+11) - 7 : Nat) : Int),
          ⟨ones 14 ++ (false :: false ::
            (pow10 (2 ^ (2*h+11) - 7) ++ (true :: rUnitsDep (2*h+3) (p1tL ++ LL)))),
           false,
           true :: false :: true :: false :: true ::
             (false :: false :: (descCascade (2*h+9) ++ R))⟩⟩ := by
  have hsplit : (2 : Nat) ^ (2*h+12) - 13 = 2 * (2 ^ (2*h+11) - 7) + 0 + 1 := by
    have e : (2:Nat)^(2*h+12) = 2 * 2^(2*h+11) := by
      rw [show 2*h+12 = (2*h+11)+1 from by omega, Nat.pow_add,
          show (2:Nat)^1 = 2 from rfl, Nat.mul_comm]
    have h7 : 8 ≤ (2:Nat)^(2*h+11) := by
      have : (2:Nat)^3 ≤ 2^(2*h+11) := Nat.pow_le_pow_right (by decide) (by omega)
      omega
    omega
  unfold odC_B
  rw [show (false :: (pow10 10 ++
        (ones (2 ^ (2*h+12) - 13) ++ (false :: false :: (descCascade (2*h+9) ++ R)))))
      = pow01 10 ++ (false ::
        (ones (2 ^ (2*h+12) - 13) ++ (false :: false :: (descCascade (2*h+9) ++ R))))
      from false_pow10_tail 10 _,
      hsplit,
      crossCarry (2 ^ (2*h+11) - 7) _ 0
        (rUnitsDep (2*h+3) (p1tL ++ LL))
        (false :: false :: (descCascade (2*h+9) ++ R))]
  rfl

theorem odCD_B (h : Nat) (LL R : List Bool) :
    steps ((17 + 46 * (2 ^ (2*h+11) - 7)) + 6) (odC_B h LL R) = some (odD_B h LL R) := by
  rw [steps_add, odCcarry_B h LL R, someBind]
  unfold odD_B
  exact odTurn _ 0 _ (descCascade (2*h+9) ++ R)

#print axioms odCcarry_B
#print axioms odCD_B
end FromB

namespace FromB
theorem odDdescIn_B (h : Nat) (LL R : List Bool) :
    steps (6 * 2 ^ (2*h+9)) (odD_B h LL R)
      = some (descIn (2*h+10)
          (-5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 17
            + 2 * ((2 ^ (2*h+11) - 7 : Nat) : Int) + 6
            + 2 * ((2 ^ (2*h+9) : Nat) : Int))
          (ones 20 ++ (false :: false ::
            (pow10 (2 ^ (2*h+11) - 7) ++ (true :: rUnitsDep (2*h+3) (p1tL ++ LL)))))
          R) := by
  have hsplit : (2 : Nat) ^ (2*h+11) - 3 = 2 * 2 ^ (2*h+9) + (2 ^ (2*h+10) - 3) := by
    have e11 : (2:Nat)^(2*h+11) = 4 * 2^(2*h+9) := by
      rw [show 2*h+11 = (2*h+9)+2 from by omega, Nat.pow_add,
          show (2:Nat)^2 = 4 from rfl, Nat.mul_comm]
    have e10 : (2:Nat)^(2*h+10) = 2 * 2^(2*h+9) := by
      rw [show 2*h+10 = (2*h+9)+1 from by omega, Nat.pow_add,
          show (2:Nat)^1 = 2 from rfl, Nat.mul_comm]
    have h9 : 4 ≤ (2:Nat)^(2*h+9) := by
      have : (2:Nat)^2 ≤ 2^(2*h+9) := Nat.pow_le_pow_right (by decide) (by omega)
      omega
    omega
  unfold odD_B
  rw [show descCascade (2*h+9)
        = ones (2 ^ (2*h+11) - 3) ++ (false :: false :: descCascade (2*h+8)) from by
          rw [show 2*h+9 = (2*h+8) + 1 from by omega, descCascade,
              show 2*h+8+3 = 2*h+11 from by omega],
      List.append_assoc, hsplit]
  show steps (6 * 2 ^ (2*h+9)) ⟨.E, _, ⟨_, false,
      false :: (ones (2 * 2 ^ (2*h+9) + (2 ^ (2*h+10) - 3)) ++
        (false :: false :: (descCascade (2*h+8) ++ R)))⟩⟩ = _
  rw [eChewFold (2 ^ (2*h+9))
        (-5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 17
          + 2 * ((2 ^ (2*h+11) - 7 : Nat) : Int) + 6)
        (2 ^ (2*h+10) - 3)
        (ones 20 ++ (false :: false ::
          (pow10 (2 ^ (2*h+11) - 7) ++ (true :: rUnitsDep (2*h+3) (p1tL ++ LL)))))
        (false :: false :: (descCascade (2*h+8) ++ R))]
  refine congrArg some ?_
  show (⟨.E, _, ⟨pow01 (2 ^ (2*h+9)) ++ _, false,
      false :: (ones (2 ^ (2*h+10) - 3) ++
        (false :: false :: (descCascade (2*h+8) ++ R)))⟩⟩ : Cfg)
    = ⟨.E, _, ⟨pow01 (2 ^ (2*h+10 - 1)) ++ _, false,
        false :: (ones (2 ^ (2*h+10) - 3) ++
          (false :: false :: (descCascade (2*h+10 - 2) ++ R)))⟩⟩
  rw [show 2*h+10-1 = 2*h+9 from by omega, show 2*h+10-2 = 2*h+8 from by omega]

/-- **the `B`-orbit ODD doubling-phase entry** — lands in the SAME `descIn (2h+10)` as the even
one, exactly as `x2`'s two entries both land in `descIn (2h+9)`. -/
theorem topEntryOddB (h : Nat) (LL R : List Bool) :
    steps ((99 + (15 * (2*h+3) + ((17 + 46 * (2 ^ (2*h+11) - 7)) + 6))) + 6 * 2 ^ (2*h+9))
        (odA_B h LL R)
      = some (descIn (2*h+10)
          (-5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 17
            + 2 * ((2 ^ (2*h+11) - 7 : Nat) : Int) + 6
            + 2 * ((2 ^ (2*h+9) : Nat) : Int))
          (ones 20 ++ (false :: false ::
            (pow10 (2 ^ (2*h+11) - 7) ++ (true :: rUnitsDep (2*h+3) (p1tL ++ LL)))))
          R) := by
  rw [steps_add, steps_add, odAB_B h LL R, someBind, steps_add, odBC_B h LL R, someBind,
      odCD_B h LL R, someBind]
  exact odDdescIn_B h LL R

#print axioms odDdescIn_B
#print axioms topEntryOddB
end FromB

namespace FromB
/-- `oddMarkerBridge` generalised in the `pow10` count — its proof only ever used `oddE2Marker`,
which is `∀ N`. -/
theorem oddMarkerBridgeN (N h : Nat) (L : List Bool) :
    pow10 N ++ (true :: rUnitsDep (2*h+3) (p1tL ++ (zeros 10 ++ L)))
      = pow10 (N + 1) ++ (false :: true :: frameLV ((2*h+1) + 1) (endWord ++ (zeros 11 ++ L))) := by
  rw [rUnitsDep_frameL h (zeros 10 ++ L), ← List.append_assoc (zeros 1), zeros_1_10,
      frameL_turnWord (2*h+1) (endWord ++ (zeros 11 ++ L)),
      ← oddE2Marker N (2*h+1) (endWord ++ (zeros 11 ++ L))]
  rfl

/-- the side condition of `oddSpineFull` at `n = 2h+6`, `m = (2^(2h+11) − 7) + 1` again FORCES
`c = 5` — the same value `x2`'s odd branch has. -/
theorem oddC_forcedB (h c : Nat)
    (hm : 10 + ((2 ^ (2*h+11) - 7) + 1) = (c + 1) + (2 ^ (5 + (2*h+6)) - 2)) : c = 5 := by
  have e : (5 + (2*h+6)) = (2*h+11) := by omega
  rw [e] at hm
  have hp : (2:Nat) ^ (2*h+11) ≥ 2 ^ 11 := Nat.pow_le_pow_right (by omega) (by omega)
  have h2048 : (2:Nat) ^ 11 = 2048 := by decide
  omega

/-- **the `B`-orbit ODD doubling phase** — `topEntryOddB ∘ oddSpineFull` at `n = 2h+6`, `c = 5`,
`j = 2h+2`, all forced. -/
theorem doubPhaseOddB (h : Nat) (L R : List Bool) :
    ∃ q, steps (((99 + (15 * (2*h+3) + ((17 + 46 * (2 ^ (2*h+11) - 7)) + 6))) + 6 * 2 ^ (2*h+9))
          + (((descTotal (2*h+6) + 415) + (ladderSteps 5 (2*h+6) + exitSteps (5 + (2*h+6))))
             + ((topGrindSteps (5 + (2*h+6)) + exitSteps (5 + (2*h+6) + 1) + 80)
                + (topGrindSteps (5 + (2*h+6) + 1) + (exitSteps (5 + (2*h+6) + 1 + 1) + 4 * 5)
                   + (27 * (2*h+2) + 110)))))
        (odA_B h (zeros 10 ++ L)
          (zeros 25 ++ (zeros 16 ++ (ladderPad 5 (2*h+6) ++
            (zeros (2 ^ (5 + (2*h+6))) ++ (zeros (2 ^ (5 + (2*h+6) + 1)) ++ R))))))
      = some ⟨.E, q, ⟨zeros 10 ++ L, false,
          zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
            frameZ (2*h+2) (oddSeamZ (5 + (2*h+6) + 1) 5 R))))⟩⟩ := by
  have hm : 10 + ((2 ^ (2*h+11) - 7) + 1) = (5 + 1) + (2 ^ (5 + (2*h+6)) - 2) := by
    have e : (5 + (2*h+6)) = (2*h+11) := by omega
    rw [e]
    have hp : (2:Nat) ^ (2*h+11) ≥ 2 ^ 11 := Nat.pow_le_pow_right (by omega) (by omega)
    have h2048 : (2:Nat) ^ 11 = 2048 := by decide
    omega
  obtain ⟨q, hq⟩ := oddSpineFull (2*h+6) ((2 ^ (2*h+11) - 7) + 1) 5 (2*h+2) (by omega) (by omega)
    hm (-5 + 19 + 7 * ((2*h+3 : Nat) : Int) + 17
        + 2 * ((2 ^ (2*h+11) - 7 : Nat) : Int) + 6
        + 2 * ((2 ^ (2*h+9) : Nat) : Int)) L R
  refine ⟨q, ?_⟩
  have en : 2*h+6+4 = 2*h+10 := by omega
  rw [en] at hq
  rw [steps_add, topEntryOddB h (zeros 10 ++ L) _, someBind,
      oddMarkerBridgeN (2 ^ (2*h+11) - 7) h L]
  exact hq

#print axioms oddMarkerBridgeN
#print axioms oddC_forcedB
#print axioms doubPhaseOddB
end FromB

namespace FromB
/-- the `B`-orbit's even-side pad register -/
def evenPadTailB (h : Nat) (R : List Bool) : List Bool :=
  zeros 16 ++ (ladderPad 5 (2*h+6) ++ (zeros (2 ^ (5 + (2*h+6))) ++ R))

/-- **`B`-orbit ODD-OUT seam = EVEN-IN seam.** -/
theorem oddSeamB_evenInB (h : Nat) (R : List Bool) :
    false :: oddSeamZ (5 + (2*h+6) + 1) 5 (zeros 16 ++ evenPadTailB (h+1) R)
      = zeros 10 ++ lowFrameB (h+1) (zeros 25 ++ evenPadTailB (h+1) R) := by
  have hz : (zeros 7 ++ (zeros 16 ++ evenPadTailB (h+1) R) : List Bool)
      = zeros 23 ++ evenPadTailB (h+1) R := by rw [← List.append_assoc, ← zeros_add]
  show false :: (zeros (2*5-1) ++ (ones (2 ^ (5 + (2*h+6) + 1 + 1) - 3) ++ (false :: false ::
      (descCascade (5 + (2*h+6) + 1 + 1 - 3) ++ (false :: false ::
        (zeros 7 ++ (zeros 16 ++ evenPadTailB (h+1) R))))))) = _
  rw [show 5 + (2*h+6) + 1 + 1 = 2*(h+1)+11 from by omega,
      show 2*(h+1)+11 - 3 = 2*(h+1)+8 from by omega, hz]
  show _ = zeros 10 ++ (ones (2 ^ (2*(h+1)+11) - 3) ++ (false :: false ::
      (descCascade (2*(h+1)+8) ++ (zeros 25 ++ evenPadTailB (h+1) R))))
  rfl

#print axioms oddSeamB_evenInB
end FromB

namespace FromB
/-! ## Obligation H for the `B`-orbit -/

theorem hlowB_core' (h : Nat) (R : List Bool) :
    steps (267 + 38*(2*h+2)) (MEvenB h R) = some (ttA_B h [] R) := hlowB_core h R

theorem hlowB_padded (h : Nat) (R : List Bool) :
    ∀ m : Nat, ∃ j : Nat, j ≤ m ∧
      steps (267 + 38*(2*h+2))
          ⟨.E, 0, ⟨zeros m, false, (MEvenB h R).tape.right⟩⟩
        = some (ttA_B h (zeros j) R) := by
  intro m
  obtain ⟨j, hjm, hj⟩ :=
    steps_lpad_zeros (267 + 38*(2*h+2)) .E 0 [] false _ (hlowB_core' h R) m
  exact ⟨j, hjm, by rwa [List.nil_append] at hj⟩

/-- **obligation H (even), `B`-orbit** — the padded low phase meets `doubPhaseB`. -/
theorem hlowDoubB (h : Nat) (R : List Bool) :
    ∃ (j : Nat) (q : Int), 10 ≤ j ∧ j ≤ 16 ∧
      steps ((267 + 38*(2*h+2))
          + ((99 + (15 * (2*h+3) + (3 + 6 * 2 ^ (2*h+9))))
             + ((descTotal (2*h+6) + 415)
                + (ladderSteps 5 (2*h+6) + exitSteps (5 + (2*h+6)))
                + (topGrindSteps (5 + (2*h+6)) + exitSteps (5 + (2*h+6) + 1) + 74
                   + (27 * (2*h+1) + 110)))))
          ⟨.E, 0, ⟨zeros 16, false,
            (MEvenB h (zeros 25 ++ evenPadTailB h R)).tape.right⟩⟩
        = some ⟨.E, q, ⟨zeros 10 ++ zeros (j - 10), false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2*h+1) (seamZ (5 + (2*h+6)) R))))⟩⟩ := by
  obtain ⟨j, hj16, hlow⟩ := hlowB_padded h (zeros 25 ++ evenPadTailB h R) 16
  have hj10 : 10 ≤ j := by
    have hm := steps_left_mono _ _ _ hlow
    simp only [ttA_B, MEvenB, List.length_append, zeros_length, List.length_cons,
      List.length_nil] at hm
    push_cast at hm
    omega
  obtain ⟨q, hdb⟩ := doubPhaseB h (zeros (j - 10)) R
  refine ⟨j, q, hj10, hj16, ?_⟩
  have hz : zeros 10 ++ zeros (j - 10) = zeros j := by
    rw [← zeros_add, show 10 + (j - 10) = j from by omega]
  rw [hz] at hdb
  rw [steps_add, hlow, someBind, hz]
  exact hdb

#print axioms hlowB_padded
#print axioms hlowDoubB
end FromB

namespace FromB
def oddPadRB (h : Nat) (R : List Bool) : List Bool := zeros 25 ++ oddPadTailB h R

theorem hlowBodd_core' (h : Nat) (R : List Bool) :
    steps (419 + 76*h) (MOddB (h+1) R) = some (odA_B h [] R) := hlowBodd_core h R

theorem hlowBodd_padded (h : Nat) (R : List Bool) :
    ∀ m : Nat, ∃ j : Nat, j ≤ m ∧
      steps (419 + 76*h) ⟨.E, 0, ⟨zeros m, false, (MOddB (h+1) R).tape.right⟩⟩
        = some (odA_B h (zeros j) R) := by
  intro m
  obtain ⟨j, hjm, hj⟩ :=
    steps_lpad_zeros (419 + 76*h) .E 0 [] false _ (hlowBodd_core' h R) m
  exact ⟨j, hjm, by rwa [List.nil_append] at hj⟩

/-- **obligation H (odd), `B`-orbit** -/
theorem hlowDoubOddB (h : Nat) (R : List Bool) :
    ∃ (j : Nat) (q : Int), 10 ≤ j ∧ j ≤ 16 ∧
      steps ((419 + 76*h)
          + (((99 + (15 * (2*h+3) + ((17 + 46 * (2 ^ (2*h+11) - 7)) + 6))) + 6 * 2 ^ (2*h+9))
            + (((descTotal (2*h+6) + 415) + (ladderSteps 5 (2*h+6) + exitSteps (5 + (2*h+6))))
               + ((topGrindSteps (5 + (2*h+6)) + exitSteps (5 + (2*h+6) + 1) + 80)
                  + (topGrindSteps (5 + (2*h+6) + 1) + (exitSteps (5 + (2*h+6) + 1 + 1) + 4 * 5)
                     + (27 * (2*h+2) + 110))))))
          ⟨.E, 0, ⟨zeros 16, false, (MOddB (h+1) (oddPadRB h R)).tape.right⟩⟩
        = some ⟨.E, q, ⟨zeros 10 ++ zeros (j - 10), false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ (2*h+2) (oddSeamZ (5 + (2*h+6) + 1) 5 R))))⟩⟩ := by
  obtain ⟨j, hj16, hlow⟩ := hlowBodd_padded h (oddPadRB h R) 16
  have hj10 : 10 ≤ j := by
    have hm := steps_left_mono _ _ _ hlow
    simp only [odA_B, MOddB, List.length_append, zeros_length, List.length_cons,
      List.length_nil] at hm
    push_cast at hm
    omega
  obtain ⟨q, hdb⟩ := doubPhaseOddB h (zeros (j - 10)) R
  refine ⟨j, q, hj10, hj16, ?_⟩
  have hz : zeros 10 ++ zeros (j - 10) = zeros j := by
    rw [← zeros_add, show 10 + (j - 10) = j from by omega]
  rw [hz] at hdb
  rw [steps_add, hlow, someBind, hz]
  exact hdb

#print axioms hlowDoubOddB
end FromB

namespace FromB
/-! ## The cross-generation frame identities and the cycles -/

theorem evenOutB_is_oddInB (h : Nat) (R : List Bool) :
    zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
        frameZ (2*h+1) (seamZ (5 + (2*h+6)) (zeros 16 ++ oddPadTailB h R)))))
      = (MOddB (h+1) (oddPadRB h R)).tape.right := by
  rw [uUnits_frameZ (2*h+1) _, show 2*h+1+1 = 2*(h+1) from by omega]
  show zeros 21 ++ (uUnits (2*(h+1)) ++
    (true :: (false :: seamZ (5 + (2*h+6)) (zeros 16 ++ oddPadTailB h R)))) = _
  rw [evenSeamB_oddInB h R]
  rfl

theorem oddOutB_is_evenInB (h : Nat) (R : List Bool) :
    zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
        frameZ (2*h+2) (oddSeamZ (5 + (2*h+6) + 1) 5 (zeros 16 ++ evenPadTailB (h+1) R)))))
      = (MEvenB (h+1) (zeros 25 ++ evenPadTailB (h+1) R)).tape.right := by
  rw [uUnits_frameZ (2*h+2) _, show 2*h+2+1 = 2*(h+1)+1 from by omega]
  show zeros 21 ++ (uUnits (2*(h+1)+1) ++
    (true :: (false :: oddSeamZ (5 + (2*h+6) + 1) 5 (zeros 16 ++ evenPadTailB (h+1) R)))) = _
  rw [oddSeamB_evenInB h R]
  rfl

#print axioms evenOutB_is_oddInB
#print axioms oddOutB_is_evenInB
end FromB

namespace FromB
def costBEven (h : Nat) : Nat :=
  (267 + 38*(2*h+2))
    + ((99 + (15 * (2*h+3) + (3 + 6 * 2 ^ (2*h+9))))
       + ((descTotal (2*h+6) + 415)
          + (ladderSteps 5 (2*h+6) + exitSteps (5 + (2*h+6)))
          + (topGrindSteps (5 + (2*h+6)) + exitSteps (5 + (2*h+6) + 1) + 74
             + (27 * (2*h+1) + 110))))

def costBOdd (h : Nat) : Nat :=
  (419 + 76*h)
    + (((99 + (15 * (2*h+3) + ((17 + 46 * (2 ^ (2*h+11) - 7)) + 6))) + 6 * 2 ^ (2*h+9))
      + (((descTotal (2*h+6) + 415) + (ladderSteps 5 (2*h+6) + exitSteps (5 + (2*h+6))))
         + ((topGrindSteps (5 + (2*h+6)) + exitSteps (5 + (2*h+6) + 1) + 80)
            + (topGrindSteps (5 + (2*h+6) + 1) + (exitSteps (5 + (2*h+6) + 1 + 1) + 4 * 5)
               + (27 * (2*h+2) + 110)))))

/-- **THE `B`-ORBIT EVEN CYCLE** — `MEvenB h → MOddB (h+1)`, trimmed to `left = []`. -/
theorem cycleBEven (h : Nat) (R : List Bool) :
    ∃ (m : Nat) (q : Int),
      steps (costBEven h)
          ⟨.E, 0, ⟨[], false,
            (MEvenB h (zeros 25 ++ evenPadTailB h (zeros 16 ++ oddPadTailB h R))).tape.right⟩⟩
        = some ⟨.E, q, ⟨zeros m, false, (MOddB (h+1) (oddPadRB h R)).tape.right⟩⟩ := by
  obtain ⟨j, q, _, _, hrun⟩ := hlowDoubB h (zeros 16 ++ oddPadTailB h R)
  rw [show zeros 10 ++ zeros (j - 10) = zeros j from by
        rw [← zeros_add, show 10 + (j - 10) = j from by omega],
      evenOutB_is_oddInB h R] at hrun
  obtain ⟨L', i, _, hLi, htrim⟩ := steps_lunpad_zeros 16 _ _ _ [] _ _ hrun
  exact ⟨j - i, q, by rw [← zeros_cancel_right j i L' hLi.symm]; exact htrim⟩

/-- **THE `B`-ORBIT ODD CYCLE** — `MOddB (h+1) → MEvenB (h+1)`. -/
theorem cycleBOdd (h : Nat) (R : List Bool) :
    ∃ (m : Nat) (q : Int),
      steps (costBOdd h)
          ⟨.E, 0, ⟨[], false,
            (MOddB (h+1) (oddPadRB h (zeros 16 ++ evenPadTailB (h+1) R))).tape.right⟩⟩
        = some ⟨.E, q, ⟨zeros m, false,
            (MEvenB (h+1) (zeros 25 ++ evenPadTailB (h+1) R)).tape.right⟩⟩ := by
  obtain ⟨j, q, _, _, hrun⟩ := hlowDoubOddB h (zeros 16 ++ evenPadTailB (h+1) R)
  rw [show zeros 10 ++ zeros (j - 10) = zeros j from by
        rw [← zeros_add, show 10 + (j - 10) = j from by omega],
      oddOutB_is_evenInB h R] at hrun
  obtain ⟨L', i, _, hLi, htrim⟩ := steps_lunpad_zeros 16 _ _ _ [] _ _ hrun
  exact ⟨j - i, q, by rw [← zeros_cancel_right j i L' hLi.symm]; exact htrim⟩

#print axioms cycleBEven
#print axioms cycleBOdd
end FromB


namespace FromB
/-! ## The chain

The recursion is on the INNER argument, so that each cycle's OUT is literally the next cycle's IN:

    argInner h 0     = []
    argInner h (d+1) = 0^16 ++ oddPadTailB h (0^16 ++ evenPadTailB (h+1) (argInner (h+1) d))
    argB h d         = 0^25 ++ evenPadTailB h (argInner h d)

even cycle at `h` : MEvenB h (argB h (d+1))  →  MOddB (h+1) (oddPadRB h …)
odd  cycle at `h` : that very config          →  MEvenB (h+1) (argB (h+1) d)
-/

def argInner : Nat → Nat → List Bool
  | _, 0 => []
  | h, d + 1 => zeros 16 ++ oddPadTailB h (zeros 16 ++ evenPadTailB (h+1) (argInner (h+1) d))

def argB (h d : Nat) : List Bool := zeros 25 ++ evenPadTailB h (argInner h d)

theorem liftB {n : Nat} {R Rout : List Bool} {q : Int} {m1 : Nat}
    (h : steps n ⟨.E, 0, ⟨[], false, R⟩⟩ = some ⟨.E, q, ⟨zeros m1, false, Rout⟩⟩)
    (p : Int) (m : Nat) :
    ∃ m2 : Nat, steps n ⟨.E, p, ⟨zeros m, false, R⟩⟩
      = some ⟨.E, q + p, ⟨zeros m2, false, Rout⟩⟩ := by
  obtain ⟨j, _, hp⟩ := steps_lpad_zeros n .E 0 [] false R h m
  rw [List.nil_append] at hp
  have hs := steps_pos_shift (d := p) hp
  rw [show (0:Int) + p = p from by omega] at hs
  exact ⟨m1 + j, by rw [zeros_add]; exact hs⟩

set_option maxHeartbeats 4000000 in
/-- **THE `B`-ORBIT CHAIN** — depth `d`, `2d` cycles, cost `≥ d`. -/
theorem chainB : ∀ (d h : Nat) (p : Int) (m : Nat),
    ∃ (n m' : Nat) (q : Int), d ≤ n ∧
      steps n ⟨.E, p, ⟨zeros m, false, (MEvenB h (argB h d)).tape.right⟩⟩
        = some ⟨.E, q, ⟨zeros m', false, (MEvenB (h + d) (argB (h + d) 0)).tape.right⟩⟩ := by
  intro d
  induction d with
  | zero => intro h p m; exact ⟨0, m, p, Nat.le_refl 0, rfl⟩
  | succ d ih =>
    intro h p m
    obtain ⟨m1, q1, hc1⟩ := cycleBEven h (zeros 16 ++ evenPadTailB (h+1) (argInner (h+1) d))
    obtain ⟨m2, hE⟩ := liftB hc1 p m
    obtain ⟨m3, q2, hc2⟩ := cycleBOdd h (argInner (h+1) d)
    obtain ⟨m4, hO⟩ := liftB hc2 (q1 + p) m2
    obtain ⟨n5, m5, q5, hn5, h5⟩ := ih (h+1) (q2 + (q1 + p)) m4
    refine ⟨costBEven h + (costBOdd h + n5), m5, q5, ?_, ?_⟩
    · simp only [costBEven, costBOdd]; omega
    · have hE' : steps (costBEven h)
          ⟨.E, p, ⟨zeros m, false, (MEvenB h (argB h (d+1))).tape.right⟩⟩
        = some ⟨.E, q1 + p, ⟨zeros m2, false,
            (MOddB (h+1) (oddPadRB h
              (zeros 16 ++ evenPadTailB (h+1) (argInner (h+1) d)))).tape.right⟩⟩ := hE
      have hO' : steps (costBOdd h)
          ⟨.E, q1 + p, ⟨zeros m2, false,
            (MOddB (h+1) (oddPadRB h
              (zeros 16 ++ evenPadTailB (h+1) (argInner (h+1) d)))).tape.right⟩⟩
        = some ⟨.E, q2 + (q1 + p), ⟨zeros m4, false,
            (MEvenB (h+1) (argB (h+1) d)).tape.right⟩⟩ := hO
      rw [show h + (d+1) = h + 1 + d from by omega,
          steps_add, hE', someBind, steps_add, hO', someBind]
      exact h5

#print axioms liftB
#print axioms chainB
end FromB

namespace FromB
/-! ## From the chain to non-halting -/

theorem evenPadTailB_app (h : Nat) (X : List Bool) :
    evenPadTailB h X = evenPadTailB h [] ++ X := by
  simp [evenPadTailB, List.append_assoc]

theorem oddPadTailB_app (h : Nat) (X : List Bool) :
    oddPadTailB h X = oddPadTailB h [] ++ X := by
  simp [oddPadTailB, List.append_assoc]

theorem lowFrameB_app (h : Nat) (X : List Bool) :
    lowFrameB h X = lowFrameB h [] ++ X := by
  simp [lowFrameB, teTailB, List.append_assoc]

theorem MEvenB_right_app (h : Nat) (X : List Bool) :
    (MEvenB h X).tape.right = (MEvenB h []).tape.right ++ X := by
  show zeros 21 ++ (uUnits (2*h+1) ++ (true :: (zeros 10 ++ lowFrameB h X))) = _
  simp [MEvenB, lowFrameB_app h X, List.append_assoc]

theorem evenPadTailB_zeros (h : Nat) :
    evenPadTailB h [] = zeros (16 + (padLen 5 (2*h+6) + 2 ^ (5 + (2*h+6)))) := by
  show zeros 16 ++ (ladderPad 5 (2*h+6) ++ (zeros (2 ^ (5 + (2*h+6))) ++ [])) = _
  rw [List.append_nil, ladderPad_zeros, ← zeros_add, ← zeros_add]

theorem oddPadTailB_zeros (h : Nat) :
    oddPadTailB h [] = zeros (16 + (padLen 5 (2*h+6)
      + (2 ^ (5 + (2*h+6)) + 2 ^ (5 + (2*h+6) + 1)))) := by
  show zeros 16 ++ (ladderPad 5 (2*h+6) ++
    (zeros (2 ^ (5 + (2*h+6))) ++ (zeros (2 ^ (5 + (2*h+6) + 1)) ++ []))) = _
  rw [List.append_nil, ladderPad_zeros, ← zeros_add, ← zeros_add, ← zeros_add]

theorem argInner_zeros : ∀ (d h : Nat), ∃ t : Nat, argInner h d = zeros t := by
  intro d
  induction d with
  | zero => intro h; exact ⟨0, rfl⟩
  | succ d ih =>
    intro h
    obtain ⟨t, ht⟩ := ih (h+1)
    refine ⟨16 + ((16 + (padLen 5 (2*h+6) + (2 ^ (5 + (2*h+6)) + 2 ^ (5 + (2*h+6) + 1))))
        + (16 + ((16 + (padLen 5 (2*(h+1)+6) + 2 ^ (5 + (2*(h+1)+6)))) + t))), ?_⟩
    show zeros 16 ++ oddPadTailB h (zeros 16 ++ evenPadTailB (h+1) (argInner (h+1) d)) = _
    rw [oddPadTailB_app h, evenPadTailB_app (h+1), ht,
        oddPadTailB_zeros h, evenPadTailB_zeros (h+1),
        ← zeros_add, ← zeros_add, ← zeros_add, ← zeros_add]

/-- `argB h d` is a blank block of size at least `25` -- the `25` matters for the entry seam. -/
theorem argB_zeros (h d : Nat) : ∃ t : Nat, argB h d = zeros (25 + t) := by
  obtain ⟨t, ht⟩ := argInner_zeros d h
  refine ⟨(16 + (padLen 5 (2*h+6) + 2 ^ (5 + (2*h+6)))) + t, ?_⟩
  show zeros 25 ++ evenPadTailB h (argInner h d) = _
  rw [evenPadTailB_app h, ht, evenPadTailB_zeros h, ← zeros_add, ← zeros_add]

/-- **`C` NEVER HALTS, given only the entry segment** — `C`'s non-halting is `x2`'s `step` never
halting from `⟨B, 0, blank⟩`, and this reduces it to one finite concrete run.  `hsplit` says the
reached right tape is the canonical milestone word plus `k ≤ 25` blanks. -/
theorem C_nonhalt_of_entry (n0 : Nat) (p0 : Int) (tl k : Nat) (Rreal : List Bool)
    (hk : k ≤ 25)
    (hsplit : (MEvenB 0 ([]:List Bool)).tape.right ++ zeros k = Rreal)
    (hentry : steps n0 initB = some ⟨.E, p0, ⟨zeros tl, false, Rreal⟩⟩) :
    ∀ N : Nat, steps N initB ≠ none := by
  intro N
  obtain ⟨t, ht⟩ := argB_zeros 0 N
  obtain ⟨n, m', q, hn, hrun⟩ := chainB N 0 p0 tl
  have hrun' : steps n ⟨.E, p0, ⟨zeros tl, false, Rreal ++ zeros (25 + t - k)⟩⟩
      = some ⟨.E, q, ⟨zeros m', false, (MEvenB (0 + N) (argB (0 + N) 0)).tape.right⟩⟩ := by
    rw [← hsplit, List.append_assoc, ← zeros_add,
        show k + (25 + t - k) = 25 + t from by omega,
        ← ht, ← MEvenB_right_app 0 (argB 0 N)]
    exact hrun
  obtain ⟨R', i, _, _, htrim⟩ :=
    steps_runpad_zeros (25 + t - k) n .E p0 (zeros tl) false Rreal hrun'
  have hfull : steps (n0 + n) initB = some ⟨.E, q, ⟨zeros m', false, R'⟩⟩ := by
    rw [steps_add, hentry, someBind]; exact htrim
  exact steps_prefix_ne_none hfull (by omega)

#print axioms argB_zeros
#print axioms C_nonhalt_of_entry
end FromB
