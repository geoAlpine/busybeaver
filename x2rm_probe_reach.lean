/-
x2rm_probe_reach.lean -- AUDIT PROBE (2026-07-17), NOT part of the lake build.
Lives in the repo ROOT deliberately: lean/lakefile.toml declares only named libs
under lean/, so this file is inert and cannot affect the X2 build.

FINDING: `regen4_transport` / `regen5_transport`'s OUT IS *literally* `descent_glue`'s
IN at a=4 / a=5 -- no connector, just instantiation of their already-forall-quantified
L / R tails (that is `regen_TI_generic`, the translation-invariance principle).
The proofs are `rw` + `rfl`.  Stronger than X2.lean §5ah's `descent_reach_4/5`, which
fix Lc = 1: these are forall Lc, for free.

Verified against the PINNED snapshot e1dfbc7 (lean/X2.lean, 5982 lines,
md5 c0c20d5a4848d22111b278fcfe72cd7e) -- which PREDATES §5ah, so this is an
independent replication.  All four theorems: [propext, Quot.sound] only.

REPRODUCE:
  SNAP=<scratch>/snap
  git archive e1dfbc7 lean/ | tar -x -C $SNAP && cp -R lean/.lake $SNAP/lean/.lake
  cp x2rm_probe_reach.lean $SNAP/lean/Probe.lean
  cd $SNAP/lean && lake build X2 && lake env lean Probe.lean
-/
import X2
open X2

/-- CHECK 1: regen4_transport's OUT is LITERALLY descent_glue's IN at (N=6, d=0, p=-7),
    under the instantiations L := true :: (pow01 (Lc+4) ++ marker), R := zeros 6 ++ R'. -/
theorem regen4_lands_descent_IN (Lc : Nat) (marker R' : List Bool) :
    steps (exitSteps 4) ⟨.E, 9, ⟨
        ones 12 ++ (true :: false :: true :: false :: false :: true :: false ::
          (true :: (pow01 (Lc + 4) ++ marker))),
        false,
        (false :: true :: false :: false :: false :: false :: false :: false ::
         false :: false :: false :: false :: false :: (zeros 6 ++ R'))⟩⟩
      = some ⟨.E, -7, ⟨pow01 (Lc + 6) ++ marker, false,
          false :: false :: false :: (ones (2 * 6 + 1) ++ (false :: false ::
            (descCascade (0 + 1) ++ (false :: false :: (zeros 7 ++ R')))))⟩⟩ := by
  rw [regen4_transport]; rfl

/-- CHECK 2: regen5_transport's OUT is LITERALLY descent_glue's IN at (N=14, d=1, p=-22),
    under L := true :: (pow01 (Lc+13) ++ marker), R := zeros 8 ++ R'. -/
theorem regen5_lands_descent_IN (Lc : Nat) (marker R' : List Bool) :
    steps (exitSteps 5) ⟨.E, 10, ⟨
        ones 28 ++ (true :: false :: true :: false :: false ::
          (true :: (pow01 (Lc + 13) ++ marker))),
        false,
        false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: (zeros 8 ++ R')⟩⟩
      = some ⟨.E, -22, ⟨pow01 (Lc + 14) ++ marker, false,
          false :: false :: false :: (ones (2 * 14 + 1) ++ (false :: false ::
            (descCascade (1 + 1) ++ (false :: false :: (zeros 7 ++ R')))))⟩⟩ := by
  rw [regen5_transport]; rfl

#print axioms regen4_lands_descent_IN
#print axioms regen5_lands_descent_IN

/-- CHECK 3 (END-TO-END, a=4): REGEN(4) ∘ descentGlue as ONE transport.  The carry exit's
    OUT feeds descent_glue with NO connector: `steps_add` + the two ∀-lemmas, instantiated. -/
theorem regen4_then_descent (Lc : Nat) (marker R' : List Bool) :
    ∃ dep : List Bool,
      steps (exitSteps 4 + ((7 + braidRunSteps 0 6 + (4 * 6 + 4)) + lowerFoldSteps (0 + 1) + 100))
          ⟨.E, 9, ⟨ones 12 ++ (true :: false :: true :: false :: false :: true :: false ::
              (true :: (pow01 (Lc + 4) ++ marker))), false,
            (false :: true :: false :: false :: false :: false :: false :: false ::
             false :: false :: false :: false :: false :: (zeros 6 ++ R'))⟩⟩
        = some ⟨.E, (-7 : Int) + 13 + 2 * ((6 : Nat) : Int) + (lowerFoldShiftN (0 + 1) : Nat),
            ⟨ones 12 ++ dep, false, false :: true :: false :: R'⟩⟩ := by
  obtain ⟨dep, hdep⟩ := descent_glue 6 0 Lc (-7) marker R'
  exact ⟨dep, by rw [steps_add, regen4_lands_descent_IN, someBind, hdep]⟩

/-- CHECK 4 (END-TO-END, a=5). -/
theorem regen5_then_descent (Lc : Nat) (marker R' : List Bool) :
    ∃ dep : List Bool,
      steps (exitSteps 5 + ((7 + braidRunSteps 0 14 + (4 * 14 + 4)) + lowerFoldSteps (1 + 1) + 100))
          ⟨.E, 10, ⟨ones 28 ++ (true :: false :: true :: false :: false ::
              (true :: (pow01 (Lc + 13) ++ marker))), false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: (zeros 8 ++ R')⟩⟩
        = some ⟨.E, (-22 : Int) + 13 + 2 * ((14 : Nat) : Int) + (lowerFoldShiftN (1 + 1) : Nat),
            ⟨ones 12 ++ dep, false, false :: true :: false :: R'⟩⟩ := by
  obtain ⟨dep, hdep⟩ := descent_glue 14 1 Lc (-22) marker R'
  exact ⟨dep, by rw [steps_add, regen5_lands_descent_IN, someBind, hdep]⟩

#print axioms regen4_then_descent
#print axioms regen5_then_descent
