import T7TopRung
open X2

set_option maxRecDepth 40000

namespace X2

/-!
# ODD top rung — the doubling phase's top rung at `Lc = 6`   (2026-07-25)

MEASURED (`x2r1_lcparity.py`, `x2r1_oddpre.py`): the odd-`g` doubling top rung is a CLEAN
`cascadeReg k 6 …` — the odd branch's constant `Lc = 6` (g=1 cReg9 and g=3 cReg11 both, while
the even branch and every internal ladder rung are `Lc = 1`).  So the odd branch reuses the even
`∀`-machines verbatim, at `Lc = 6` instead of `1`, plus one distinct fixed seam episode
(`oddSeam`, the `pow10 6` left-window analogue of `seam74`).

`braid_topgrind` is already `∀ Lc` and `topGrindSteps k` is `Lc`-independent, so the topgrind
generalises to `∀ Lc` by threading `Lc` where `cascadeReg_topgrind` hard-codes `1`.
-/

/-- **`cascadeReg_topgrind_Lc`** — `cascadeReg_topgrind`, generalised to `∀ Lc`.  `topGrindSteps k`
is `Lc`-independent; the OUT left carries `pow10 Lc`. -/
theorem cascadeReg_topgrind_Lc (k : Nat) (hk : 4 ≤ k) (Lc : Nat) (p : Int) (marker R : List Bool) :
    steps (topGrindSteps k) (cascadeReg k Lc p marker R)
      = some ⟨.E, p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int),
          ⟨ones (4 * (2 ^ (k - 1) - 2) + 4) ++ (pow10 Lc ++ (true :: marker)), false,
            false :: (descCascade (k - 3) ++ (false :: false :: (zeros 7 ++ R)))⟩⟩ := by
  have hsplit : topGrindSteps k
      = 7 + braidRunSteps 0 (2 ^ (k - 1) - 2) + (4 * (2 ^ (k - 1) - 2) + 4) :=
    topGrindSteps_split k (by omega)
  have hblk : 2 * (2 ^ (k - 1) - 2) + 1 = 2 ^ k - 3 := cascadeReg_block k hk
  rw [hsplit]; unfold cascadeReg; rw [← hblk]
  exact braid_topgrind (2 ^ (k - 1) - 2) Lc p marker
    (descCascade (k - 3) ++ (false :: false :: (zeros 7 ++ R)))

#print axioms cascadeReg_topgrind_Lc

end X2

/-! ### The comb chew — the Lc law's atom  (MEASURED `x2r1_lcsweep.py`, `R1_ODDSEAM` §Lc law)

The odd exit differs from the even one only through `Lc`: the closing left-sweep of the REGEN
traverses `pow01 Lc` instead of `pow01 1`, at **4 steps and 2 right-hand zeros per comb pair**
(`span = exitSteps k + 4(Lc−1)`, `zeros = 2Lc+1`, exact for `Lc = 0..10` and at both generations).

This is that atom, `∀ p ∀ X ∀ W`: the head eats one `1 0` comb pair on the left, emits `0 0` on
the right, and advances `−2`.  The `1` that reappears at `pos+1` in the OUT is the comb's own,
uncovered by the move — which is why the tile closes with no side condition. -/
theorem combChew (p : Int) (X W : List Bool) :
    steps 4 ⟨.D, p, ⟨true :: false :: X, false, true :: W⟩⟩
      = some ⟨.D, p - 2, ⟨X, false, true :: false :: false :: W⟩⟩ := by
  have h0 : steps 4 ⟨.D, (0 : Int), ⟨true :: false :: X, false, true :: W⟩⟩
      = some ⟨.D, (-2 : Int), ⟨X, false, true :: false :: false :: W⟩⟩ := by rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

#print axioms combChew

/-- **`combChewFold`** — the `Lc` law as a `∀n` transport: `n` comb pairs are eaten in `4n` steps,
depositing `2n` zeros on the right and advancing `−2n`.  This is the exact content of the measured
law `span = exitSteps k + 4(Lc−1)`, `zeros = 2Lc+1` (`x2r1_lcsweep.py`, Lc = 0..10, both
generations); `pow10 n` is the `1 0`-comb the closing REGEN sweep traverses. -/
theorem combChewFold : ∀ (n : Nat) (p : Int) (X W : List Bool),
    steps (4 * n) ⟨.D, p, ⟨pow10 n ++ X, false, true :: W⟩⟩
      = some ⟨.D, p - 2 * (n : Int), ⟨X, false, true :: (zeros (2 * n) ++ W)⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p X W
    show steps 0 _ = _
    exact congrArg some (by rw [show p - 2 * ((0:Nat) : Int) = p from by omega]; rfl)
  | succ n ih =>
    intro p X W
    have hstep : 4 * (n + 1) = 4 + 4 * n := by omega
    show steps (4 * (n + 1)) ⟨.D, p, ⟨true :: false :: (pow10 n ++ X), false, true :: W⟩⟩ = _
    rw [hstep, steps_add, combChew p (pow10 n ++ X) W, someBind, ih (p - 2) X (false :: false :: W)]
    refine congrArg some ?_
    have hz : zeros (2 * n) ++ (false :: false :: W) = zeros (2 * (n + 1)) ++ W := by
      rw [show 2 * (n + 1) = 2 * n + 2 from by omega, zeros_add, List.append_assoc]
      rfl
    have hp : p - 2 - 2 * ((n : Nat) : Int) = p - 2 * (((n + 1 : Nat)) : Int) := by
      push_cast; omega
    rw [hz, hp]

#print axioms combChewFold

-- ANTI-VACUITY (METHODS M4): the MEASURED odd exit surplus is `4(Lc−1)` steps and `2(Lc−1)`
-- zeros at `Lc = 6`, i.e. 20 steps and 10 zeros — the on-orbit g=1 span was 136 470 =
-- `exitSteps 10 + 20`, and the g=3 span 2 122 774 = `exitSteps 12 + 20`.
example : 4 * (6 - 1) = 20 := by decide
example : 2 * (6 - 1) = 10 := by decide
example : exitSteps 10 + 4 * (6 - 1) = 136470 := by decide
example : exitSteps 12 + 4 * (6 - 1) = 2122774 := by decide
