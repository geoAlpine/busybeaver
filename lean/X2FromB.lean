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

-- Recorded as a MEASUREMENT, not a theorem: `native_decide` would add `Lean.ofReduceBool`
-- (trusting the compiler), which this development does not use.  The corresponding THEOREM will be
-- the chunked-`rfl` entry segment, exactly as `T7Entry.entryM12` is for the `A`-orbit.
#eval ((steps 2866581 initB) == some ⟨.E, -33, ⟨zeros 1, false, (MEvenB 0 (zeros 1)).tape.right⟩⟩,
       (steps 45042285 initB) == some ⟨.E, -45, ⟨zeros 1, false, (MEvenB 1 (zeros 1)).tape.right⟩⟩)

end FromB
