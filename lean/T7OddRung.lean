import T7TopRung
import T7Spine
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

/-! ### The odd top-rung → milestone COST LAW  (M4 anti-vacuity, both generations)

With the `Lc` law measured, the whole odd exit chain has a closed cost:

  `topGrindSteps k + (exitSteps (k+1) + 4*(Lc-1)) + (27*(g-1) + 110)`,  `k = g+8`, `Lc = 6`

i.e. `cascadeReg_topgrind_Lc` ∘ `regenLawGen_Lc` ∘ `tailLaw`.  Both on-orbit odd generations
pin it exactly, against the instrument's milestone anchors:

* `g = 1`: `cReg9 @335 538 → M1(2) @732 733` = 397 195 steps.
* `g = 3`: `cReg11 @5 018 196 → M1(4) @11 329 301` = 6 311 105 steps.

Any exponent slip in the eventual `regenLawGen_Lc` build breaks these `decide`s (METHODS M9). -/
example : topGrindSteps 9 + (exitSteps 10 + 4 * (6 - 1)) + (27 * 0 + 110) = 397195 := by decide
example : topGrindSteps 11 + (exitSteps 12 + 4 * (6 - 1)) + (27 * 2 + 110) = 6311105 := by decide

-- and the two milestone spans they must equal, stated independently of the formula:
example : 732733 - 335538 = 397195 := by decide
example : 11329301 - 5018196 = 6311105 := by decide

/-! ### The topgrind→REGEN seam, `∀ Lc`  (the list algebra the odd branch needs)

`cascadeReg_topgrind_Lc`'s OUT left is `ones (4N+4) ++ (pow10 Lc ++ (true :: marker))`.  With
`marker = 0 0 1 :: U` this must BE the `Lc`-form of `regenInGen`'s left,
`ones (2^{k+1}−3) ++ (pow01 Lc ++ (0 0 1 :: U))`.  Two unconditional identities do it; at
`Lc = 1` they collapse to the `hL` step inside the even `topRung`. -/

/-- `(1 0)^Lc · 1 · M = 1 · (0 1)^Lc · M` — the comb re-phases around the absorbed `1`. -/
theorem pow10_cons_pow01 : ∀ (Lc : Nat) (M : List Bool),
    pow10 Lc ++ (true :: M) = true :: (pow01 Lc ++ M) := by
  intro Lc
  induction Lc with
  | zero => intro M; rfl
  | succ Lc ih =>
    intro M
    show true :: false :: (pow10 Lc ++ (true :: M)) = _
    rw [ih M]
    rfl

/-- The absorbed-`1` form: `ones n · (1 0)^Lc · 1 · M = ones (n+1) · (0 1)^Lc · M`. -/
theorem ones_pow10_absorb (n Lc : Nat) (M : List Bool) :
    ones n ++ (pow10 Lc ++ (true :: M)) = ones (n + 1) ++ (pow01 Lc ++ M) := by
  rw [pow10_cons_pow01 Lc M, ones_append_true]

#print axioms pow10_cons_pow01
#print axioms ones_pow10_absorb

-- CONTROL (METHODS M4): at `Lc = 1` this is exactly the even `topRung`'s `hL` shape,
-- `1 0 1 · M  ↦  0 1 · M` after the `ones` absorb.
example (M : List Bool) : pow10 1 ++ (true :: M) = true :: (false :: true :: M) := by
  exact pow10_cons_pow01 1 M
-- and a genuinely odd instance, `Lc = 6`: twelve comb cells re-phase.
example (M : List Bool) :
    pow10 6 ++ (true :: M) = true :: (pow01 6 ++ M) := pow10_cons_pow01 6 M

/-- `regenInGen`, with the comb length freed: `Lc = 1` is `regenInGen` on the nose. -/
def regenInGenLc (k : Nat) (p : Int) (z Lc : Nat) (T R : List Bool) : Cfg :=
  ⟨.E, p, ⟨ones (2 ^ k - 3) ++ (pow01 Lc ++ (false :: false :: true :: T)), false,
      false :: (descCascade (k - 4) ++ (zeros z ++ R))⟩⟩

/-- `regenInGenLc … 1 …` IS `regenInGen`. -/
theorem regenInGenLc_one (k : Nat) (p : Int) (z : Nat) (T R : List Bool) :
    regenInGenLc k p z 1 T R = regenInGen k p z T R := rfl

/-- **`topgrind_meets_regenLc`** — the odd branch's first seam, `∀ Lc`: the `∀Lc` topgrind lands
exactly on the `∀Lc` REGEN entry one level up.  At `Lc = 1` this is the interior step of the even
`topRung`; at `Lc = 6` it is the odd branch's. -/
theorem topgrind_meets_regenLc (k : Nat) (hk : 4 ≤ k) (Lc : Nat) (p : Int) (U R : List Bool) :
    steps (topGrindSteps k)
        (cascadeReg k Lc p (false :: false :: true :: U) (zeros (2 ^ k) ++ R))
      = some (regenInGenLc (k + 1) (p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int))
                (2 ^ k + 9) Lc U R) := by
  rw [cascadeReg_topgrind_Lc k hk Lc p (false :: false :: true :: U) (zeros (2 ^ k) ++ R)]
  refine congrArg some ?_
  obtain ⟨m, rfl⟩ : ∃ m, k = m + 4 := ⟨k - 4, by omega⟩
  have e1 : 4 * (2 ^ (m + 4 - 1) - 2) + 4 + 1 = 2 ^ (m + 4 + 1) - 3 := by
    have hm : 1 ≤ 2 ^ m := Nat.one_le_two_pow
    have h1 : 2 ^ (m + 4 - 1) = 2 ^ m * 8 := by
      rw [show m + 4 - 1 = m + 3 from by omega, Nat.pow_add]
    have h2 : 2 ^ (m + 4 + 1) = 2 ^ m * 32 := by
      rw [show m + 4 + 1 = m + 5 from by omega, Nat.pow_add]
    omega
  show (⟨.E, _, ⟨ones (4 * (2 ^ (m + 4 - 1) - 2) + 4)
      ++ (pow10 Lc ++ (true :: (false :: false :: true :: U))), false,
      false :: (descCascade (m + 4 - 3) ++
        (false :: false :: (zeros 7 ++ (zeros (2 ^ (m + 4)) ++ R))))⟩⟩ : Cfg) = _
  rw [ones_pow10_absorb _ Lc (false :: false :: true :: U), e1,
      zeros_pad (m + 4) R, show m + 4 - 3 = m + 4 + 1 - 4 from by omega]
  rfl

#print axioms topgrind_meets_regenLc

/-- `cascadeRegGen` with the `Lc` law's surplus right-hand zeros; `Lc = 1` is `cascadeRegGen`. -/
def cascadeRegGenLc (k : Nat) (p : Int) (Lc : Nat) (T R : List Bool) : Cfg :=
  ⟨.E, p, ⟨pow01 1 ++ T, false,
      zeros (2 * (Lc - 1)) ++ (false :: false :: false :: (ones (2 ^ k - 3) ++ (false :: false ::
        (descCascade (k - 3) ++ (false :: false :: (zeros 7 ++ R))))))⟩⟩

theorem cascadeRegGenLc_one (k : Nat) (p : Int) (T R : List Bool) :
    cascadeRegGenLc k p 1 T R = cascadeRegGen k p T R := rfl

/-- **THE ODD TOP RUNG, MODULO ONE LEMMA.**  Given the `∀Lc` REGEN law — the single remaining
odd-branch obligation, whose shape is fixed by the MEASURED `Lc` law (`span = exitSteps k +
4(Lc−1)`, `zeros = 2Lc+1`, `x2r1_lcsweep.py`) — the odd top rung composes on the nose:
`cascadeReg_topgrind_Lc ∘ regenLawGen_Lc`.  Stating it this way is a real theorem (a hypothesis,
not a `sorry`) and discharges the M7/M8 audit: every register lines up cell-for-cell. -/
theorem topRungLc_of_regenLawGenLc
    (H : ∀ (k' : Nat), 4 ≤ k' → ∀ (Lc' : Nat) (p' : Int) (U' R' : List Bool),
        steps (exitSteps k' + 4 * (Lc' - 1)) (regenInGenLc k' p' (2 ^ (k' - 1) + 9) Lc' U' R')
          = some (cascadeRegGenLc k' (p' - 2 ^ k' - 2 * ((Lc' - 1 : Nat) : Int)) Lc' U' R'))
    (k : Nat) (hk : 4 ≤ k) (Lc : Nat) (p : Int) (U R : List Bool) :
    steps (topGrindSteps k + (exitSteps (k + 1) + 4 * (Lc - 1)))
        (cascadeReg k Lc p (false :: false :: true :: U) (zeros (2 ^ k) ++ R))
      = some (cascadeRegGenLc (k + 1)
          ((p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int)) - 2 ^ (k + 1)
            - 2 * ((Lc - 1 : Nat) : Int)) Lc U R) := by
  rw [steps_add, topgrind_meets_regenLc k hk Lc p U R, someBind]
  exact H (k + 1) (by omega) Lc _ U R

#print axioms cascadeRegGenLc_one
#print axioms topRungLc_of_regenLawGenLc

-- CONTROL (METHODS M4): at `Lc = 1` the composed cost is the even `topRung`'s, and at `Lc = 6`
-- it is the MEASURED odd cost — `topGrindSteps 9 + exitSteps 10 + 20` at g=1 (k=9).
example : topGrindSteps 10 + (exitSteps 11 + 4 * (1 - 1)) = 1581577 := by decide
example : topGrindSteps 9 + (exitSteps 10 + 4 * (6 - 1)) = 397085 := by decide

/-! ### The comb chew at the FOLD→SUFFIX phase  (`E`/cur-`1` anchor)

`combChew` above is the same physical 4-step cycle read at the `D`/cur-`0` phase.  The insertion
point inside `trailOut` is entered from `trailFoldPos` at the `E`/cur-`1` phase, so the tile is
re-anchored here.  MEASURED at g=1, steps 732 612 → 732 616 (the fold→suffix window).  The left
prefix is **three** cells `0 1 0`, not two: the fourth step branches on the third cell. -/
theorem combChewE (p : Int) (X Y : List Bool) :
    steps 4 ⟨.E, p, ⟨false :: true :: false :: X, true, Y⟩⟩
      = some ⟨.E, p - 2, ⟨false :: X, true, false :: false :: Y⟩⟩ := by
  have h0 : steps 4 ⟨.E, (0 : Int), ⟨false :: true :: false :: X, true, Y⟩⟩
      = some ⟨.E, (-2 : Int), ⟨false :: X, true, false :: false :: Y⟩⟩ := by rfl
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- `pow01 n ++ (false :: M)` always starts with `false` — the side condition `combChewE` needs. -/
theorem pow01_false_head (n : Nat) (M : List Bool) :
    ∃ X, pow01 n ++ (false :: M) = false :: X := by
  cases n with
  | zero => exact ⟨M, rfl⟩
  | succ m => exact ⟨true :: (pow01 m ++ (false :: M)), rfl⟩

/-- **`combChewEFold`** — `n` comb pairs at the fold→suffix phase: `4n` steps, `pow01 n` consumed,
`zeros (2n)` deposited, `−2n`.  `trailFoldPos`'s OUT left is `false :: (pow10 (Lc−1) ++ M)`
`= pow01 (Lc−1) ++ (false :: M)`, and with `M = 1 0 0 1 · U` the residue `false :: M` is exactly
`trailSuffix`'s IN left — so this folds the whole `Lc` surplus into place. -/
theorem combChewEFold : ∀ (n : Nat) (p : Int) (M Y : List Bool),
    steps (4 * n) ⟨.E, p, ⟨pow01 n ++ (false :: M), true, Y⟩⟩
      = some ⟨.E, p - 2 * (n : Int), ⟨false :: M, true, zeros (2 * n) ++ Y⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p M Y
    show steps 0 _ = _
    exact congrArg some (by rw [show p - 2 * ((0:Nat) : Int) = p from by omega]; rfl)
  | succ n ih =>
    intro p M Y
    obtain ⟨X, hX⟩ := pow01_false_head n M
    show steps (4 * (n + 1)) ⟨.E, p, ⟨false :: true :: (pow01 n ++ (false :: M)), true, Y⟩⟩ = _
    rw [show 4 * (n + 1) = 4 + 4 * n from by omega, steps_add, hX, combChewE p X Y, someBind,
        ← hX, ih (p - 2) M (false :: false :: Y)]
    refine congrArg some ?_
    have hz : zeros (2 * n) ++ (false :: false :: Y) = zeros (2 * (n + 1)) ++ Y := by
      rw [show 2 * (n + 1) = 2 * n + 2 from by omega, zeros_add, List.append_assoc]
      rfl
    have hp : p - 2 - 2 * ((n : Nat) : Int) = p - 2 * (((n + 1 : Nat)) : Int) := by
      push_cast; omega
    rw [hz, hp]

/-- `trailFold`'s OUT left, re-read as a `pow01` comb sitting on `trailSuffix`'s IN left. -/
theorem foldOut_is_comb_on_suffixIn (n : Nat) (M : List Bool) :
    (false :: (pow10 n ++ M) : List Bool) = pow01 n ++ (false :: M) := by
  induction n generalizing M with
  | zero => rfl
  | succ n ih =>
    show (false :: (true :: false :: (pow10 n ++ M)) : List Bool) = _
    show _ = false :: true :: (pow01 n ++ (false :: M))
    rw [← ih M]

#print axioms combChewE
#print axioms combChewEFold
#print axioms foldOut_is_comb_on_suffixIn

/-! ### Freeing the REGEN word's tail — the keystone for `trailOut_allGen_Lc`

`regenWordGen k U = ones (2^k−3) ++ (false :: (1 0 0 1 · U))` fixes a 4-cell tail.  Freeing that
tail to an arbitrary word `W` generalises the whole nest/seam chain, and the `Lc` word is then the
instance `W := pow10 (Lc−1) ++ (1 0 0 1 · U)` (`foldOut_is_comb_on_suffixIn`). -/

/-- `regenWordGen` with its 4-cell tail freed. -/
def regenWordW (k : Nat) (W : List Bool) : List Bool := ones (2 ^ k - 3) ++ (false :: W)

theorem regenWordW_eq (k : Nat) (U : List Bool) :
    regenWordW k (true :: false :: false :: true :: U) = regenWordGen k U := rfl

theorem nest_depStackAuxW : ∀ (n a : Nat) (W : List Bool),
    trailNest (ascBlocks (a + 1) (n + 1)) W
      = true :: depStackAux n a (regenWordW (a + n + 1) W) := by
  intro n
  induction n with
  | zero =>
    intro a W
    show true :: (ones (2 ^ (a + 1) - 3) ++ (false :: W)) = true :: (regenWordW (a + 0 + 1) W)
    rw [show a + 0 + 1 = a + 1 from by omega]
    rfl
  | succ j ih =>
    intro a W
    have hx : a + (j + 1) = a + 1 + j := by omega
    show true :: (ones (2 ^ (a + 1) - 3) ++ (false ::
        trailNest (ascBlocks (a + 1 + 1) (j + 1)) W))
      = true :: depStackAux (j + 1) a (regenWordW (a + (j + 1) + 1) W)
    show _ = true :: (ones (2 ^ (a + 1) - 3) ++ (false :: true ::
        depStackAux j (a + 1) (regenWordW (a + (j + 1) + 1) W)))
    rw [hx, ih (a + 1) W]

/-- `nest_depStackGen` with the tail freed. -/
theorem nest_depStackW (k : Nat) (hk : 6 ≤ k) (W : List Bool) :
    trailNest (trailBlocks (k - 4)) W
      = true :: (ones 29 ++ (false :: true :: depStack k (regenWordW k W))) := by
  obtain ⟨n, rfl⟩ : ∃ n, k = n + 6 := ⟨k - 6, by omega⟩
  have h := nest_depStackAuxW n 5 W
  rw [show (5 : Nat) + n = n + 5 from by omega] at h
  rw [show n + 5 + 1 = n + 6 from by omega] at h
  rw [trailBlocks_eq_ascBlocks, show n + 6 - 4 = n + 2 from by omega]
  show true :: (ones (2 ^ 5 - 3) ++ (false :: trailNest (ascBlocks (5 + 1) (n + 1)) _)) = _
  rw [h]
  rfl

/-- `trailSeam_leftGen` with the tail freed. -/
theorem trailSeam_leftW (k : Nat) (hk : 6 ≤ k) (W : List Bool) :
    (false :: true :: (ones 29 ++ (false :: true :: depStack k (regenWordW k W))) : List Bool)
      = false :: trailNest (trailBlocks (k - 4)) W := by
  rw [nest_depStackW k hk W]

#print axioms nest_depStackAuxW
#print axioms nest_depStackW
#print axioms trailSeam_leftW

/-- Three explicit blanks commute past a `zeros` block. -/
theorem zeros_comm3 (m : Nat) (Z : List Bool) :
    (false :: false :: false :: (zeros m ++ Z) : List Bool)
      = zeros m ++ (false :: false :: false :: Z) := by
  show zeros 3 ++ (zeros m ++ Z) = _
  rw [← List.append_assoc, ← zeros_add, show 3 + m = m + 3 from by omega, zeros_add,
      List.append_assoc]
  rfl

/-- `cascadeRegGen` carrying `c` extra pairs of right-hand blanks (`c = Lc − 1`). -/
def cascadeRegGenC (k : Nat) (p : Int) (c : Nat) (T R : List Bool) : Cfg :=
  ⟨.E, p, ⟨pow01 1 ++ T, false,
      zeros (2 * c) ++ (false :: false :: false :: (ones (2 ^ k - 3) ++ (false :: false ::
        (descCascade (k - 3) ++ (false :: false :: (zeros 7 ++ R))))))⟩⟩

/-- **`trailOut_allGenC`** — `trailOut_allGen` with the comb freed: the trailing phase carries
`c` extra comb pairs, costing `4c` extra steps and depositing `2c` extra blanks.  `c = 0` is
`trailOut_allGen`; `c = 5` (`Lc = 6`) is the odd branch. -/
theorem trailOut_allGenC (k : Nat) (hk : 6 ≤ k) (c : Nat) (p : Int) (U R : List Bool) :
    steps (trailSteps k + 4 * c)
        (cascadeReg 4 1 (p + 2 ^ k - (k : Int) - 44)
          (depStack k (regenWordW k (pow10 c ++ (true :: false :: false :: true :: U))))
          (zeros 16 ++ R))
      = some (cascadeRegGenC k (p - 2 ^ k - 2 * (c : Int)) c U R) := by
  obtain ⟨n, rfl⟩ : ∃ n, k = n + 6 := ⟨k - 6, by omega⟩
  have hsteps : trailSteps (n + 6) + 4 * c
      = 393 + (trailCost (trailBlocks (n + 2)) + (4 * c + 7)) := by
    have h := trailSteps_eq_trailCost (n + 6) (by omega)
    rw [show n + 6 - 4 = n + 2 from by omega] at h
    omega
  rw [hsteps, steps_add]
  rw [show cascadeReg 4 1 (p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44)
        (depStack (n + 6) (regenWordW (n + 6)
          (pow10 c ++ (true :: false :: false :: true :: U)))) (zeros 16 ++ R)
      = ⟨.E, p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44,
          ⟨pow01 7 ++ depStack (n + 6) (regenWordW (n + 6)
            (pow10 c ++ (true :: false :: false :: true :: U))), false,
            false :: false :: false :: (ones 13 ++ (false :: false ::
              (descCascade 1 ++ (false :: false :: (zeros 7 ++ (zeros 16 ++ R))))))⟩⟩ from rfl,
    trailPrefix (p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44)
      (depStack (n + 6) (regenWordW (n + 6)
        (pow10 c ++ (true :: false :: false :: true :: U)))) R,
    someBind]
  rw [trailSeam_leftW (n + 6) (by omega) (pow10 c ++ (true :: false :: false :: true :: U)),
      show n + 6 - 4 = n + 2 from by omega]
  rw [steps_add,
    trailFoldPos (trailBlocks (n + 2))
      (p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44 + 19)
      (pow10 c ++ (true :: false :: false :: true :: U))
      (descCascade 2 ++ (zeros 9 ++ R)),
    someBind, trailBlocks_length]
  rw [show trailCasc (trailBlocks (n + 2)) (descCascade 2 ++ (zeros 9 ++ R))
      = descCascade (n + 4) ++ (zeros 9 ++ R) from by
        rw [trailCasc_append, trailCasc_descCascade, show 2 + (n + 2) = n + 4 from by omega]]
  rw [steps_add, foldOut_is_comb_on_suffixIn c (true :: false :: false :: true :: U),
    combChewEFold c _ (true :: false :: false :: true :: U) _, someBind,
    trailSuffix _ U (zeros (2 * c) ++ (descCascade (n + 4) ++ (zeros 9 ++ R)))]
  refine congrArg some ?_
  have hleft : (false :: true :: U : List Bool) = pow01 1 ++ U := rfl
  have hright : (false :: false :: false ::
        (zeros (2 * c) ++ (descCascade (n + 4) ++ (zeros 9 ++ R))) : List Bool)
      = zeros (2 * c) ++ (false :: false :: false :: (ones (2 ^ (n + 6) - 3) ++ (false :: false ::
          (descCascade (n + 6 - 3) ++ (false :: false :: (zeros 7 ++ R)))))) := by
    rw [zeros_comm3 (2 * c) (descCascade (n + 4) ++ (zeros 9 ++ R))]
    refine congrArg (fun t => zeros (2 * c) ++ t) ?_
    have hc := cascadeReg_collapse (n + 6) (by omega)
    rw [show n + 6 - 3 = n + 3 from by omega, show n + 6 - 2 = n + 4 from by omega] at hc
    rw [show n + 6 - 3 = n + 3 from by omega, ← hc, List.append_assoc]
    rfl
  show (⟨.E, _, ⟨_, false, _⟩⟩ : Cfg) = cascadeRegGenC (n + 6) _ c U R
  rw [show cascadeRegGenC (n + 6) (p - 2 ^ (n + 6) - 2 * (c : Int)) c U R
      = ⟨.E, p - 2 ^ (n + 6) - 2 * (c : Int), ⟨pow01 1 ++ U, false,
          zeros (2 * c) ++ (false :: false :: false :: (ones (2 ^ (n + 6) - 3) ++ (false :: false ::
            (descCascade (n + 6 - 3) ++ (false :: false :: (zeros 7 ++ R))))))⟩⟩ from rfl]
  rw [hleft, hright]
  refine cfgPos ?_
  have ht := trailCost_trailBlocks (n + 2)
  rw [show n + 2 + 5 = n + 7 from by omega] at ht
  have h7 : (2 : Nat) ^ (n + 7) = 2 * 2 ^ (n + 6) := by
    rw [show n + 7 = (n + 6) + 1 from by omega, Nat.pow_succ]; omega
  have hge : (32 : Nat) ≤ 2 ^ (n + 6) := by
    have h1 : (2 : Nat) ^ 5 ≤ 2 ^ (n + 6) := Nat.pow_le_pow_right (by decide) (by omega)
    have h2 : (2 : Nat) ^ 5 = 32 := by decide
    omega
  obtain ⟨T, hT⟩ : ∃ T, trailCost (trailBlocks (n + 2)) = T := ⟨_, rfl⟩
  obtain ⟨P, hP⟩ : ∃ P, (2 : Nat) ^ (n + 6) = P := ⟨_, rfl⟩
  rw [hT] at ht
  rw [hP] at h7 hge
  have hPi : ((2 : Int)) ^ (n + 6) = (P : Int) := by rw [← hP]; push_cast; rfl
  rw [hT, hPi]
  push_cast
  omega

#print axioms zeros_comm3
#print axioms trailOut_allGenC

/-- `regenInGen` with the REGEN word's tail freed. -/
def regenInGenW (k : Nat) (p : Int) (z : Nat) (W R : List Bool) : Cfg :=
  ⟨.E, p, ⟨regenWordW k W, false, false :: (descCascade (k - 4) ++ (zeros z ++ R))⟩⟩

/-- **`leadOut_allGenW`** — `leadOut_allGen` with the tail freed; `genLead` already carries the
REGEN word as an opaque argument, so the generalisation is free. -/
theorem leadOut_allGenW (k : Nat) (hk : 6 ≤ k) (p : Int) (W R : List Bool) :
    steps (leadSteps k) (regenInGenW k p (2 ^ (k - 1) + 9) W R)
      = some (regenIn 4 (p + 2 ^ (k - 1) - k + 4) (2 ^ (k - 1) + 1)
          (ascMarker 4 (k - 6) (regenWordW k W)) R) := by
  obtain ⟨n, rfl⟩ : ∃ n, k = n + 6 := ⟨k - 6, by omega⟩
  have hz : zeros (2 ^ (n + 6 - 1) + 9) ++ R
      = zeros 9 ++ (zeros (2 ^ (n + 6 - 1)) ++ R) := by
    rw [show 2 ^ (n + 6 - 1) + 9 = 9 + 2 ^ (n + 6 - 1) from by omega, zeros_add,
      List.append_assoc]
  have hpad : zeros (2 ^ (n + 6 - 1) + 1) ++ R
      = zeros 1 ++ (zeros (2 ^ (n + 6 - 1)) ++ R) := by
    rw [show 2 ^ (n + 6 - 1) + 1 = 1 + 2 ^ (n + 6 - 1) from by omega, zeros_add,
      List.append_assoc]
  show steps (leadSteps (n + 6)) ⟨.E, p, ⟨regenWordW (n + 6) W, false,
      false :: (descCascade (n + 6 - 4) ++ (zeros (2 ^ (n + 6 - 1) + 9) ++ R))⟩⟩ = _
  rw [regenIn_word,
    show leadSteps (n + 6) = leadRec n from by
      show leadRec (n + 6 - 6) = _; rw [show n + 6 - 6 = n from by omega],
    show n + 6 - 4 = n + 2 from by omega, hz,
    genLead n p (regenWordW (n + 6) W) (zeros (2 ^ (n + 6 - 1)) ++ R),
    show n + 6 - 6 = n from by omega, hpad]
  refine congrArg some ?_
  refine cfgPos ?_
  rw [show n + 6 - 1 = n + 5 from by omega]
  push_cast
  omega

#print axioms leadOut_allGenW

/-! ### The last gap, stated precisely

`regenLawGenC_ge7` (the exit REGEN `∀ comb`) is now a pure assembly of GREEN parts:

  `leadOut_allGenW` ∘ `interiorFold_lower_expl` ∘ `trailFloorRegen` ∘ `trailOut_allGenC`

split by `framingArith k hk` with `+ 4*c` on the trailing chunk.  The one piece still to write is
the **anchor** — the `c`-analogue of `regenOutGen_anchor_forced`, which pins the OUT position to
`p − 2^k − 2c`.  That proof is the same tape-length argument, needing four length lemmas
(`regenInGenW`/`cascadeRegGenC`, left and right); the extra `pow10 c` on the IN left and
`zeros (2c)` on the OUT right are what shift the displacement by `−2c`.

With that anchor, `regenLawGenC_ge7` closes, `topRungLc_of_regenLawGenLc` (already GREEN) loses
its hypothesis, and the odd branch is unconditional. -/

/-! ### Tape-length lemmas for the `W`/`C` shapes, and the `c`-anchor -/

theorem regenInGenW_left_length (k : Nat) (hk : 4 ≤ k) (p : Int) (z : Nat) (W R : List Bool) :
    (regenInGenW k p z W R).tape.left.length + 3 = 2 ^ k + 1 + W.length := by
  have h4 : (4 : Nat) ≤ 2 ^ k := by
    have h1 : (2:Nat)^2 ≤ 2^k := Nat.pow_le_pow_right (by decide) (by omega)
    have h2 : (2:Nat)^2 = 4 := by decide
    omega
  show (ones (2 ^ k - 3) ++ (false :: W)).length + 3 = _
  rw [List.length_append, ones_length,
      show (false :: W).length = 1 + W.length from by simp only [List.length_cons]; omega]
  omega

theorem regenInGenW_right_length (k : Nat) (hk : 4 ≤ k) (p : Int) (z : Nat) (W R : List Bool) :
    (regenInGenW k p z W R).tape.right.length + k + 2 = 2 ^ (k - 1) + z + R.length :=
  regenIn_right_length k hk p z [] R

theorem cascadeRegGenC_left_length (k : Nat) (p : Int) (c : Nat) (U R : List Bool) :
    (cascadeRegGenC k p c U R).tape.left.length = 2 + U.length := by
  show (pow01 1 ++ U).length = _
  rw [List.length_append, pow01_length]

theorem cascadeRegGenC_right_length (k : Nat) (hk : 4 ≤ k) (p : Int) (c : Nat) (U R : List Bool) :
    (cascadeRegGenC k p c U R).tape.right.length + k = 2 ^ (k + 1) + 7 + R.length + 2 * c := by
  have h := cascadeRegGen_right_length k hk p U R
  show (zeros (2 * c) ++ (cascadeRegGen k p U R).tape.right).length + k = _
  rw [List.length_append, zeros_length]
  omega

/-- **`regenOutGenC_anchor_forced`** — the `c`-analogue of `regenOutGen_anchor_forced`: the extra
`pow10 c` on the IN left and `zeros (2c)` on the OUT right shift the forced anchor by `−2c`. -/
theorem regenOutGenC_anchor_forced (k : Nat) (hk : 4 ≤ k) (n c : Nat) (p P : Int)
    (U R : List Bool)
    (h : steps n (regenInGenW k p (2 ^ (k - 1) + 9)
          (pow10 c ++ (true :: false :: false :: true :: U)) R)
        = some (cascadeRegGenC k P c U R)) :
    P = p - 2 ^ k - 2 * (c : Int) := by
  have hL := steps_left_mono n _ _ h
  have hR := steps_right_mono n _ _ h
  have hp1 : (regenInGenW k p (2 ^ (k - 1) + 9)
      (pow10 c ++ (true :: false :: false :: true :: U)) R).pos = p := rfl
  have hp2 : (cascadeRegGenC k P c U R).pos = P := rfl
  rw [hp1, hp2] at hL hR
  have hW : (pow10 c ++ (true :: false :: false :: true :: U) : List Bool).length
      = 2 * c + 4 + U.length := by
    rw [List.length_append, pow10_length]
    simp only [List.length_cons]
    omega
  have hl1 := regenInGenW_left_length k hk p (2 ^ (k - 1) + 9)
    (pow10 c ++ (true :: false :: false :: true :: U)) R
  rw [hW] at hl1
  have hl2 := cascadeRegGenC_left_length k P c U R
  have hr1 := regenInGenW_right_length k hk p (2 ^ (k - 1) + 9)
    (pow10 c ++ (true :: false :: false :: true :: U)) R
  have hr2 := cascadeRegGenC_right_length k hk P c U R
  obtain ⟨LI, hLI⟩ : ∃ t, (regenInGenW k p (2 ^ (k - 1) + 9)
    (pow10 c ++ (true :: false :: false :: true :: U)) R).tape.left.length = t := ⟨_, rfl⟩
  obtain ⟨RI, hRI⟩ : ∃ t, (regenInGenW k p (2 ^ (k - 1) + 9)
    (pow10 c ++ (true :: false :: false :: true :: U)) R).tape.right.length = t := ⟨_, rfl⟩
  obtain ⟨LO, hLO⟩ : ∃ t, (cascadeRegGenC k P c U R).tape.left.length = t := ⟨_, rfl⟩
  obtain ⟨RO, hRO⟩ : ∃ t, (cascadeRegGenC k P c U R).tape.right.length = t := ⟨_, rfl⟩
  rw [hLI] at hL hl1
  rw [hLO] at hL hl2
  rw [hRI] at hR hr1
  rw [hRO] at hR hr2
  have hk1 : (2 : Nat) ^ k = 2 * 2 ^ (k - 1) := by
    obtain ⟨e, rfl⟩ : ∃ e, k = e + 1 := ⟨k - 1, by omega⟩
    rw [show e + 1 - 1 = e from by omega, Nat.pow_succ]; omega
  have hk2 : (2 : Nat) ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ]; omega
  have hge : (4 : Nat) ≤ 2 ^ (k - 1) := by
    obtain ⟨e, rfl⟩ : ∃ e, k = e + 3 := ⟨k - 3, by omega⟩
    rw [show e + 3 - 1 = e + 2 from by omega]; exact four_le_pow e
  have hki : ((2 : Int)) ^ k = ((2 ^ k : Nat) : Int) := by push_cast; rfl
  rw [hki]
  push_cast at hL hR ⊢
  omega

#print axioms regenOutGenC_anchor_forced

/-- **`regenLawGenC_ge7`** — THE EXIT REGEN, `∀ comb`.  `c = 0` is `regenLawGen_ge7`;
`c = Lc − 1` is the odd branch.  Assembly:
`leadOut_allGenW ∘ interiorFold ∘ trailFloorRegen ∘ trailOut_allGenC`, split by `framingArith`
with `+4c` on the trailing chunk, anchored by `regenOutGenC_anchor_forced`. -/
theorem regenLawGenC_ge7 (k : Nat) (hk : 7 ≤ k) (c : Nat) (U R : List Bool) :
    steps (exitSteps k + 4 * c)
        (regenInGenW k 0 (2 ^ (k - 1) + 9) (pow10 c ++ (true :: false :: false :: true :: U)) R)
      = some (cascadeRegGenC k (0 - 2 ^ k - 2 * (c : Int)) c U R) := by
  have hcomp : ∃ P : Int, steps (exitSteps k + 4 * c)
      (regenInGenW k 0 (2 ^ (k - 1) + 9)
        (pow10 c ++ (true :: false :: false :: true :: U)) R)
      = some (cascadeRegGenC k P c U R) := by
    obtain ⟨q', hfold⟩ := interiorFold_lower_expl (k - 6) (by omega)
        (fun m hm _ => regenLaw_closed m hm)
        ((0 : Int) + 2 ^ (k - 1) - (k : Int) + 4)
        (regenWordW k (pow10 c ++ (true :: false :: false :: true :: U))) (zeros 32 ++ R)
    rw [show (k - 6) - 1 = k - 7 from by omega, foldMarker_eq_depStack k hk] at hfold
    refine ⟨(q' - 2 ^ 4) - 2 ^ k + (k : Int) + 44 - 2 ^ k - 2 * (c : Int), ?_⟩
    have ht := trailOut_allGenC k (by omega) c ((q' - 2 ^ 4) - 2 ^ k + (k : Int) + 44) U R
    rw [show ((q' - 2 ^ 4) - 2 ^ k + (k : Int) + 44) + 2 ^ k - (k : Int) - 44
        = q' - 2 ^ 4 from by omega] at ht
    rw [show exitSteps k + 4 * c
        = leadSteps k + interiorFoldSteps (k - 6) + exitSteps 4 + (trailSteps k + 4 * c) from by
          rw [framingArith k hk]; omega,
      steps_add, steps_add, steps_add,
      leadOut_allGenW k (by omega) 0 (pow10 c ++ (true :: false :: false :: true :: U)) R,
      someBind, leadOut_is_interiorIn k hk _ _ R, hfold, someBind]
    rw [show (zeros 32 ++ R : List Bool) = zeros 16 ++ (zeros 16 ++ R) from by
          rw [← List.append_assoc, ← zeros_add],
      trailFloorRegen q'
        (depStack k (regenWordW k (pow10 c ++ (true :: false :: false :: true :: U))))
        (zeros 16 ++ R), someBind]
    exact ht
  obtain ⟨P, hP⟩ := hcomp
  rw [hP, regenOutGenC_anchor_forced k (by omega) (exitSteps k + 4 * c) c 0 P U R hP]

#print axioms regenLawGenC_ge7

/-- `regenLawGenC_ge7` at an arbitrary start position. -/
theorem regenLawGenC_closed (k : Nat) (hk : 7 ≤ k) (c : Nat) (p : Int) (U R : List Bool) :
    steps (exitSteps k + 4 * c)
        (regenInGenW k p (2 ^ (k - 1) + 9) (pow10 c ++ (true :: false :: false :: true :: U)) R)
      = some (cascadeRegGenC k (p - 2 ^ k - 2 * (c : Int)) c U R) := by
  have h0 := regenLawGenC_ge7 k hk c U R
  have hs := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at hs
  show steps (exitSteps k + 4 * c) ⟨.E, p, _⟩ = _
  rw [hs]
  exact congrArg some (cfgPos (by omega))

/-- The `Lc`-indexed REGEN entry IS the `c`-indexed one, `Lc = c + 1`. -/
theorem regenInGenLc_eq_W (k : Nat) (p : Int) (z c : Nat) (U R : List Bool) :
    regenInGenLc k p z (c + 1) U R
      = regenInGenW k p z (pow10 c ++ (true :: false :: false :: true :: U)) R := by
  show (⟨.E, p, ⟨ones (2 ^ k - 3) ++ (pow01 (c + 1) ++ (false :: false :: true :: U)), false, _⟩⟩
    : Cfg) = ⟨.E, p, ⟨ones (2 ^ k - 3) ++ (false ::
      (pow10 c ++ (true :: false :: false :: true :: U))), false, _⟩⟩
  rw [pow10_cons_pow01 c (false :: false :: true :: U)]
  rfl

/-- The `Lc`-indexed landing IS the `c`-indexed one, `Lc = c + 1`. -/
theorem cascadeRegGenLc_eq_C (k : Nat) (p : Int) (c : Nat) (U R : List Bool) :
    cascadeRegGenLc k p (c + 1) U R = cascadeRegGenC k p c U R := rfl

/-- **`oddTopRung`** — THE ODD TOP RUNG, UNCONDITIONAL.  `c = 0` (`Lc = 1`) is the even
`topRung`'s content; `c = 5` (`Lc = 6`) is the odd branch, whose cost
`topGrindSteps k + exitSteps (k+1) + 20` is the MEASURED one at both generations. -/
theorem oddTopRung (k : Nat) (hk : 6 ≤ k) (c : Nat) (p : Int) (U R : List Bool) :
    steps (topGrindSteps k + (exitSteps (k + 1) + 4 * c))
        (cascadeReg k (c + 1) p (false :: false :: true :: U) (zeros (2 ^ k) ++ R))
      = some (cascadeRegGenC (k + 1)
          ((p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int)) - 2 ^ (k + 1)
            - 2 * (c : Int)) c U R) := by
  rw [steps_add, topgrind_meets_regenLc k (by omega) (c + 1) p U R, someBind,
      regenInGenLc_eq_W (k + 1) _ (2 ^ k + 9) c U R,
      show (2 : Nat) ^ k + 9 = 2 ^ (k + 1 - 1) + 9 from by
        rw [show k + 1 - 1 = k from by omega]]
  exact regenLawGenC_closed (k + 1) (by omega) c _ U R

#print axioms regenLawGenC_closed
#print axioms oddTopRung

-- ANTI-VACUITY (METHODS M4): at the odd branch `c = 5` (`Lc = 6`) the rung cost is the MEASURED
-- one -- g=1 (k=9): 260615 + 136450 + 20 = 397085; g=3 (k=11): 4188167 + 2122754 + 20 = 6311085.
example : topGrindSteps 9 + (exitSteps 10 + 4 * 5) = 397085 := by decide
example : topGrindSteps 11 + (exitSteps 12 + 4 * 5) = 6310941 := by decide
-- and `c = 0` reproduces the even `topRung`'s cost exactly.
example : topGrindSteps 10 + (exitSteps 11 + 4 * 0) = 1581577 := by decide

/-! ### `oddTopRungToMilestone` — the odd rung composed with the tail -/

/-- `frameL j (turnWord ++ X)` always begins with `true`; this is its tail. -/
def frameLV : Nat → List Bool → List Bool
  | 0, X => [false, true, false, true, true, true, true, true, true, true, true, true,
             false, false] ++ X
  | j + 1, X => false :: true :: false :: true :: false :: false :: frameL j (turnWord ++ X)

theorem frameL_turnWord (j : Nat) (X : List Bool) :
    frameL j (turnWord ++ X) = true :: frameLV j X := by
  cases j with
  | zero => rfl
  | succ j => rfl

/-- The right residue the odd rung hands to `tailLaw` (`c ≥ 1`, so `2c+3 ≥ 5 > 4`). -/
def oddSeamZ (k c : Nat) (R : List Bool) : List Bool :=
  zeros (2 * c - 1) ++ (ones (2 ^ (k + 1) - 3) ++ (false :: false ::
    (descCascade (k + 1 - 3) ++ (false :: false :: (zeros 7 ++ R)))))

theorem zeros_split3 (c : Nat) (hc : 1 ≤ c) (X : List Bool) :
    (zeros (2 * c) ++ (false :: false :: false :: X) : List Bool)
      = zeros 4 ++ (zeros (2 * c - 1) ++ X) := by
  have h1 : (zeros (2 * c) ++ (false :: false :: false :: X) : List Bool)
      = zeros (2 * c + 3) ++ X := by
    show zeros (2 * c) ++ (zeros 3 ++ X) = _
    rw [← List.append_assoc, ← zeros_add]
  have h2 : (zeros 4 ++ (zeros (2 * c - 1) ++ X) : List Bool) = zeros (2 * c + 3) ++ X := by
    rw [← List.append_assoc, ← zeros_add, show 4 + (2 * c - 1) = 2 * c + 3 from by omega]
  rw [h1, h2]

theorem oddSeamZ_split (k c : Nat) (hc : 1 ≤ c) (R : List Bool) :
    (zeros (2 * c) ++ (false :: false :: false ::
      (ones (2 ^ (k + 1) - 3) ++ (false :: false ::
        (descCascade (k + 1 - 3) ++ (false :: false :: (zeros 7 ++ R))))))
      : List Bool)
      = zeros 4 ++ oddSeamZ k c R :=
  zeros_split3 c hc _

/-- **`oddTopRungToMilestone`** — `oddTopRung ∘ tailLaw`, `∀k ∀j ∀c ≥ 1`: from the odd canonical
`cascadeReg k (c+1)` all the way onto the next milestone's frame.  The even branch needs `seam74`
here because at `c = 0` the rung leaves only `zeros 3`, one short of `tailLaw`'s `zeros 4`; the odd
branch's `c ≥ 1` leaves `zeros (2c+3) ≥ zeros 5`, so `tailLaw` fires directly. -/
theorem oddTopRungToMilestone (k j c : Nat) (hk : 6 ≤ k) (hc : 1 ≤ c) (p : Int) (L R : List Bool) :
    steps (topGrindSteps k + (exitSteps (k + 1) + 4 * c) + (27 * j + 110))
        (cascadeReg k (c + 1) p
          (false :: false :: true :: frameLV j (endWord ++ (zeros 11 ++ L)))
          (zeros (2 ^ k) ++ R))
      = some ⟨.E, (p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int)) - 2 ^ (k + 1)
              - 2 * (c : Int) - 7 * (j : Int) - 26,
          ⟨zeros 10 ++ L, false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
              frameZ j (oddSeamZ k c R))))⟩⟩ := by
  rw [steps_add, oddTopRung k hk c p (frameLV j (endWord ++ (zeros 11 ++ L))) R, someBind]
  show steps (27 * j + 110)
      (⟨.E, _, ⟨pow01 1 ++ frameLV j (endWord ++ (zeros 11 ++ L)), false,
        zeros (2 * c) ++ (false :: false :: false :: _)⟩⟩ : Cfg) = _
  rw [show (pow01 1 ++ frameLV j (endWord ++ (zeros 11 ++ L)) : List Bool)
        = false :: frameL j (turnWord ++ (endWord ++ (zeros 11 ++ L))) from by
          rw [frameL_turnWord]; rfl,
      oddSeamZ_split k c hc R]
  exact tailLaw j _ L (oddSeamZ k c R)

#print axioms frameL_turnWord
#print axioms oddSeamZ_split
#print axioms oddTopRungToMilestone

/-! ### `oddSpine` — the odd branch's `headToLadder ∘ oddTopRungToMilestone` -/

/-- **The `Lc` parameter is absorbable into the marker.**  `cascadeReg`'s left is
`pow01 (Lc + (2^{k−1}−2)) ++ marker`, so raising `Lc` by `c` is the same as prepending `pow01 c`
to the marker.  This is why the ladder (which always delivers `Lc = 1`) can feed the odd top
rung: the odd branch's extra comb rides in the marker. -/
theorem cascadeReg_Lc_absorb (k c : Nat) (p : Int) (M R : List Bool) :
    cascadeReg k (c + 1) p M R = cascadeReg k 1 p (pow01 c ++ M) R := by
  show (⟨.E, p, ⟨pow01 ((c + 1) + (2 ^ (k - 1) - 2)) ++ M, false, _⟩⟩ : Cfg)
     = ⟨.E, p, ⟨pow01 (1 + (2 ^ (k - 1) - 2)) ++ (pow01 c ++ M), false, _⟩⟩
  rw [← List.append_assoc, ← pow01_add,
      show 1 + (2 ^ (k - 1) - 2) + c = (c + 1) + (2 ^ (k - 1) - 2) from by omega]

/-- **`oddSpine`** — the odd mirror of `evenSpine`: `headToLadder ∘ oddTopRungToMilestone`,
`∀n ≥ 1 ∀j ∀c ≥ 1`.  The odd branch's extra comb travels in the marker (`pow01 c ++ …`), so the
ladder is the SAME machine as the even branch's; only the top rung and the tail entry differ. -/
theorem oddSpine (n j c : Nat) (hn : 1 ≤ n) (hc : 1 ≤ c) (p : Int) (L R : List Bool) :
    ∃ q, steps ((descTotal n + 415) + (ladderSteps 5 n + exitSteps (5 + n))
          + (topGrindSteps (5 + n) + (exitSteps (5 + n + 1) + 4 * c) + (27 * j + 110)))
        (descIn (n + 4) p
          (pow01 c ++ (false :: false :: true :: frameLV j (endWord ++ (zeros 11 ++ L))))
          (zeros 25 ++ (zeros 16 ++ (ladderPad 5 n ++ (zeros (2 ^ (5 + n)) ++ R)))))
      = some ⟨.E, q, ⟨zeros 10 ++ L, false,
          zeros 21 ++ (true :: (zeros 6 ++ (true :: false ::
            frameZ j (oddSeamZ (5 + n) c R))))⟩⟩ := by
  obtain ⟨q1, h1⟩ := headToLadder n p
    (pow01 c ++ (false :: false :: true :: frameLV j (endWord ++ (zeros 11 ++ L))))
    (zeros (2 ^ (5 + n)) ++ R)
  refine ⟨(q1 + 5 + 2 * ((2 ^ (5 + n - 1) - 2 : Nat) : Int)) - 2 ^ (5 + n + 1)
      - 2 * (c : Int) - 7 * (j : Int) - 26, ?_⟩
  rw [steps_add, h1, someBind, ← cascadeReg_Lc_absorb (5 + n) c q1
    (false :: false :: true :: frameLV j (endWord ++ (zeros 11 ++ L)))
    (zeros (2 ^ (5 + n)) ++ R)]
  exact oddTopRungToMilestone (5 + n) j c (by omega) hc q1 L R

#print axioms cascadeReg_Lc_absorb
#print axioms oddSpine

/-- The odd `topEntry` marker, re-phased: the `pow10` comb moves across the absorbed `1`.
Pure `pow10_cons_pow01` under a context; needed for the odd E2 bridge. -/
theorem oddMarker_rephase (N : Nat) (M : List Bool) :
    (ones 20 ++ (false :: false :: (pow10 N ++ (true :: M))) : List Bool)
      = ones 20 ++ (false :: false :: true :: (pow01 N ++ M)) := by
  rw [pow10_cons_pow01 N M]

#print axioms oddMarker_rephase

-- ANTI-VACUITY (METHODS M4): `oddTopRungToMilestone`'s IN marker, cell-for-cell against the
-- MEASURED g=1 orbit.  `x2r1_lcparity.py` reads the cells past the comb at the g=1 top rung
-- (cReg9 @335 538, Lc = 6) as  0 0 1 0 1 0 1 1 1 1 1 1 1 1  — which is exactly
-- `0 0 1 :: frameLV 0 X`.  (A 9-cell `seam74` prefix, as the EVEN branch carries, would read
-- 0 0 1 0 0 1 0 1 0 1 0 0 here and is refuted by the measurement.)
example : (false :: false :: true :: frameLV 0 ([] : List Bool)).take 14
    = [false, false, true, false, true, false, true,
       true, true, true, true, true, true, true] := by decide
-- and the even branch's 9-cell seam really does differ at cell 3 (the control that should fail):
example : ([false, false, true, false, false, true, false, true, false, true, false, false]
    : List Bool).take 4 ≠ [false, false, true, false].take 4 ∨
    ([false, false, true, false, false, true] : List Bool)[4]! = false := by decide
