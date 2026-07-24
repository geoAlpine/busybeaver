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
