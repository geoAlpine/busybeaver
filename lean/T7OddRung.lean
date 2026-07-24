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
