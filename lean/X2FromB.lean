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
