import T7RegenGen
import T7Ladder
open X2

set_option maxRecDepth 20000

/-!
# `RegenLawGen` ∀k and the ladder's TOP RUNG  (2026-07-23)

`regenIn k`'s left is `ones(2^k−3) ++ [0,1,0,0,1] ++ pow01(2^{k−1}−2) ++ marker`.  On the real
orbit the ladder's LAST rung presents that shape with the comb `pow01(2^{k−1}−2)` **absent** —
the climb exhausts it — so `regenLaw_closed` does not apply there and ≈75 % of the doubling
phase had no theorem (`LADDER_TOP_NOT_CANONICAL_2026-07-23.md`).

Measurement (`x2r5_combread.py`) showed the head never enters the comb during the transport;
the comb is carried, +1 pair.  This file frees it:

  `regenInGen k p z U R`   — `regenIn` with `pow01(2^{k−1}−2) ++ marker` replaced by a free `U`
  `cascadeRegGen k p U R`  — `cascadeReg k 1` with its comb replaced by `pow01 1 ++ U`

Every step of `regenLaw_closed`'s chain is ported with `U` free, each with a `_specialises`
CONTROL proving the canonical statement is the instance `U := pow01(2^{k−1}−2) ++ marker`:

  `nest_depStackAuxGen` → `nest_depStackGen` → `trailSeam_leftGen` → `trailOut_allGen`   (trailing)
  `genLead` (already ∀-left) → `leadOut_allGen`                                          (lead)
  `regenOutGen_anchor_forced`                                                            (anchor)
  → `regenLawGen_ge7` → `regenLawGen_closed`

The `k ≥ 7` assembly needs the CANONICAL `RegenLaw` only at strictly lower levels, which
`regenLaw_closed` already supplies — so it is a direct theorem, not a nested induction.
Levels 4, 5, 6 come from `T7RegenGen`'s chunked proofs.

`topRung` then = `cascadeReg_topgrind` (∀ marker, already proven) ∘ `regenLawGen_closed (k+1)`.
-/

/-- `regenWord k` with its comb `pow01 (2^{k-1}-2)` replaced by a free tail `U`. -/
def regenWordGen (k : Nat) (U : List Bool) : List Bool :=
  ones (2 ^ k - 3) ++ (false :: true :: false :: false :: true :: U)

theorem regenWordGen_spec (k : Nat) (marker : List Bool) :
    regenWordGen k (pow01 (2 ^ (k - 1) - 2) ++ marker) = regenWord k ++ marker := by
  show ones (2 ^ k - 3) ++ (false :: true :: false :: false :: true ::
      (pow01 (2 ^ (k - 1) - 2) ++ marker)) = _
  show _ = (ones (2 ^ k - 3) ++ (false :: true :: false :: false :: true ::
      pow01 (2 ^ (k - 1) - 2))) ++ marker
  rw [List.append_assoc]
  rfl

/-- `nest_depStackAux` with the comb freed. -/
theorem nest_depStackAuxGen : ∀ (n a : Nat) (U : List Bool),
    trailNest (ascBlocks (a + 1) (n + 1)) (true :: false :: false :: true :: U)
      = true :: depStackAux n a (regenWordGen (a + n + 1) U) := by
  intro n
  induction n with
  | zero =>
    intro a U
    show true :: (ones (2 ^ (a + 1) - 3) ++ (false ::
        (true :: false :: false :: true :: U)))
      = true :: (regenWordGen (a + 0 + 1) U)
    rw [show a + 0 + 1 = a + 1 from by omega]
    rfl
  | succ j ih =>
    intro a U
    have hx : a + (j + 1) = a + 1 + j := by omega
    show true :: (ones (2 ^ (a + 1) - 3) ++ (false ::
        trailNest (ascBlocks (a + 1 + 1) (j + 1)) (true :: false :: false :: true :: U)))
      = true :: depStackAux (j + 1) a (regenWordGen (a + (j + 1) + 1) U)
    show _ = true :: (ones (2 ^ (a + 1) - 3) ++ (false :: true ::
        depStackAux j (a + 1) (regenWordGen (a + (j + 1) + 1) U)))
    rw [hx, ih (a + 1) U]

#print axioms nest_depStackAuxGen
#print axioms regenWordGen_spec

/-- `nest_depStack` with the comb freed. -/
theorem nest_depStackGen (k : Nat) (hk : 6 ≤ k) (U : List Bool) :
    trailNest (trailBlocks (k - 4)) (true :: false :: false :: true :: U)
      = true :: (ones 29 ++ (false :: true :: depStack k (regenWordGen k U))) := by
  obtain ⟨n, rfl⟩ : ∃ n, k = n + 6 := ⟨k - 6, by omega⟩
  have h := nest_depStackAuxGen n 5 U
  rw [show (5 : Nat) + n = n + 5 from by omega] at h
  rw [show n + 5 + 1 = n + 6 from by omega] at h
  rw [trailBlocks_eq_ascBlocks, show n + 6 - 4 = n + 2 from by omega]
  show true :: (ones (2 ^ 5 - 3) ++ (false :: trailNest (ascBlocks (5 + 1) (n + 1)) _)) = _
  rw [h]
  rfl

/-- `trailSeam_left` with the comb freed. -/
theorem trailSeam_leftGen (k : Nat) (hk : 6 ≤ k) (U : List Bool) :
    (false :: true :: (ones 29 ++ (false :: true :: depStack k (regenWordGen k U)))
      : List Bool)
      = false :: trailNest (trailBlocks (k - 4)) (true :: false :: false :: true :: U) := by
  rw [nest_depStackGen k hk U]

#print axioms nest_depStackGen
#print axioms trailSeam_leftGen

theorem trailOut_allGen (k : Nat) (hk : 6 ≤ k) (p : Int) (U R : List Bool) :
    steps (trailSteps k)
        (cascadeReg 4 1 (p + 2 ^ k - (k : Int) - 44) (depStack k (regenWordGen k U))
          (zeros 16 ++ R))
      = some (cascadeRegGen k (p - 2 ^ k) U R) := by
  obtain ⟨n, rfl⟩ : ∃ n, k = n + 6 := ⟨k - 6, by omega⟩
  -- COUNT: trailSteps = 393 (prefix) + trailCost (fold) + 7 (suffix)
  have hsteps : trailSteps (n + 6) = 393 + (trailCost (trailBlocks (n + 2)) + 7) := by
    have h := trailSteps_eq_trailCost (n + 6) (by omega)
    rw [show n + 6 - 4 = n + 2 from by omega] at h
    omega
  rw [hsteps, steps_add]
  -- PHASE 1 : the k-INDEPENDENT 393-step prefix
  rw [show cascadeReg 4 1 (p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44)
        (depStack (n + 6) (regenWordGen (n + 6) U)) (zeros 16 ++ R)
      = ⟨.E, p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44,
          ⟨pow01 7 ++ depStack (n + 6) (regenWordGen (n + 6) U), false,
            false :: false :: false :: (ones 13 ++ (false :: false ::
              (descCascade 1 ++ (false :: false :: (zeros 7 ++ (zeros 16 ++ R))))))⟩⟩ from rfl,
    trailPrefix (p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44)
      (depStack (n + 6) (regenWordGen (n + 6) U)) R,
    someBind]
  -- SEAM : the machine's left word IS trailFold's nest
  rw [trailSeam_leftGen (n + 6) (by omega) U, show n + 6 - 4 = n + 2 from by omega]
  -- PHASE 2 : the fold, with its exact anchor
  rw [steps_add,
    trailFoldPos (trailBlocks (n + 2))
      (p + 2 ^ (n + 6) - ((n + 6 : Nat) : Int) - 44 + 19)
      (true :: false :: false :: true :: (U))
      (descCascade 2 ++ (zeros 9 ++ R)),
    someBind, trailBlocks_length]
  -- RIGHT structure-match : the fold's cascade IS descCascade (k−2)
  rw [show trailCasc (trailBlocks (n + 2)) (descCascade 2 ++ (zeros 9 ++ R))
      = descCascade (n + 4) ++ (zeros 9 ++ R) from by
        rw [trailCasc_append, trailCasc_descCascade, show 2 + (n + 2) = n + 4 from by omega]]
  -- PHASE 3 : the k-INDEPENDENT 7-step suffix
  rw [trailSuffix _ (U) (descCascade (n + 4) ++ (zeros 9 ++ R))]
  -- LAND on cascadeReg k
  refine congrArg some ?_
  have hleft : (false :: true :: (U) : List Bool) = pow01 1 ++ U := rfl
  have hright : (false :: false :: false :: (descCascade (n + 4) ++ (zeros 9 ++ R)) : List Bool)
      = false :: false :: false :: (ones (2 ^ (n + 6) - 3) ++ (false :: false ::
          (descCascade (n + 6 - 3) ++ (false :: false :: (zeros 7 ++ R))))) := by
    have hc := cascadeReg_collapse (n + 6) (by omega)
    rw [show n + 6 - 3 = n + 3 from by omega, show n + 6 - 2 = n + 4 from by omega] at hc
    rw [show n + 6 - 3 = n + 3 from by omega, ← hc, List.append_assoc]
    rfl
  show (⟨.E, _, ⟨_, false, _⟩⟩ : Cfg) = cascadeRegGen (n + 6) (p - 2 ^ (n + 6)) U R
  rw [show cascadeRegGen (n + 6) (p - 2 ^ (n + 6)) U R
      = ⟨.E, p - 2 ^ (n + 6), ⟨pow01 1 ++ U, false,
          false :: false :: false :: (ones (2 ^ (n + 6) - 3) ++ (false :: false ::
            (descCascade (n + 6 - 3) ++ (false :: false :: (zeros 7 ++ R)))))⟩⟩ from rfl]
  rw [hleft, hright]
  refine cfgPos ?_
  -- ANCHOR : the four displacements close on the nose
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

/-- CONTROL: the canonical `TrailLaw k` is exactly the instance `U := pow01 (2^{k-1}-2) ++ marker`. -/
theorem trailOut_allGen_specialises (k : Nat) (hk : 6 ≤ k) (p : Int) (marker R : List Bool) :
    steps (trailSteps k)
        (cascadeReg 4 1 (p + 2 ^ k - (k : Int) - 44) (depStack k (regenWord k ++ marker))
          (zeros 16 ++ R))
      = some (cascadeReg k 1 (p - 2 ^ k) marker R) := by
  rw [← regenWordGen_spec k marker, trailOut_allGen k hk p _ R]
  refine congrArg some ?_
  show (⟨.E, _, ⟨pow01 1 ++ (pow01 (2 ^ (k-1) - 2) ++ marker), false, _⟩⟩ : Cfg) = _
  rw [← List.append_assoc, ← pow01_add]
  rfl

#print axioms trailOut_allGen
#print axioms trailOut_allGen_specialises

theorem regenInGen_word (k : Nat) (p : Int) (z : Nat) (U R : List Bool) :
    regenInGen k p z U R
      = ⟨.E, p, ⟨regenWordGen k U, false,
          false :: (descCascade (k - 4) ++ (zeros z ++ R))⟩⟩ := rfl

/-- `leadOut_all` with the comb freed. -/
theorem leadOut_allGen (k : Nat) (hk : 6 ≤ k) (p : Int) (U R : List Bool) :
    steps (leadSteps k) (regenInGen k p (2 ^ (k - 1) + 9) U R)
      = some (regenIn 4 (p + 2 ^ (k - 1) - k + 4) (2 ^ (k - 1) + 1)
          (ascMarker 4 (k - 6) (regenWordGen k U)) R) := by
  obtain ⟨n, rfl⟩ : ∃ n, k = n + 6 := ⟨k - 6, by omega⟩
  have hz : zeros (2 ^ (n + 6 - 1) + 9) ++ R
      = zeros 9 ++ (zeros (2 ^ (n + 6 - 1)) ++ R) := by
    rw [show 2 ^ (n + 6 - 1) + 9 = 9 + 2 ^ (n + 6 - 1) from by omega, zeros_add,
      List.append_assoc]
  have hpad : zeros (2 ^ (n + 6 - 1) + 1) ++ R
      = zeros 1 ++ (zeros (2 ^ (n + 6 - 1)) ++ R) := by
    rw [show 2 ^ (n + 6 - 1) + 1 = 1 + 2 ^ (n + 6 - 1) from by omega, zeros_add,
      List.append_assoc]
  rw [regenInGen_word, regenIn_word,
    show leadSteps (n + 6) = leadRec n from by
      show leadRec (n + 6 - 6) = _; rw [show n + 6 - 6 = n from by omega],
    show n + 6 - 4 = n + 2 from by omega, hz,
    genLead n p (regenWordGen (n + 6) U) (zeros (2 ^ (n + 6 - 1)) ++ R),
    show n + 6 - 6 = n from by omega, hpad]
  refine congrArg some ?_
  refine cfgPos ?_
  rw [show n + 6 - 1 = n + 5 from by omega]
  push_cast
  omega

/-- CONTROL: `leadOut_all` is the instance `U := pow01 (2^{k-1}-2) ++ marker`. -/
theorem leadOut_allGen_specialises (k : Nat) (hk : 6 ≤ k) (p : Int) (marker R : List Bool) :
    steps (leadSteps k) (regenIn k p (2 ^ (k - 1) + 9) marker R)
      = some (regenIn 4 (p + 2 ^ (k - 1) - k + 4) (2 ^ (k - 1) + 1)
          (ascMarker 4 (k - 6) (regenWord k ++ marker)) R) := by
  rw [← regenWordGen_spec k marker]
  exact leadOut_allGen k hk p (pow01 (2 ^ (k - 1) - 2) ++ marker) R

#print axioms leadOut_allGen
#print axioms leadOut_allGen_specialises

theorem regenInGen_left_length (k : Nat) (hk : 4 ≤ k) (p : Int) (z : Nat) (U R : List Bool) :
    (regenInGen k p z U R).tape.left.length + 3 = 2 ^ k + 5 + U.length := by
  have h4 : (4 : Nat) ≤ 2 ^ k := by
    have : (2:Nat)^2 ≤ 2^k := Nat.pow_le_pow_right (by decide) (by omega)
    have : (2:Nat)^2 = 4 := by decide
    omega
  show (ones (2 ^ k - 3) ++ (false :: true :: false :: false :: true :: U)).length + 3 = _
  rw [List.length_append, ones_length,
      show (false :: true :: false :: false :: true :: U).length = 5 + U.length from by
        simp only [List.length_cons]; omega]
  omega

theorem cascadeRegGen_left_length (k : Nat) (p : Int) (U R : List Bool) :
    (cascadeRegGen k p U R).tape.left.length = 2 + U.length := by
  show (pow01 1 ++ U).length = _
  rw [List.length_append, pow01_length]

theorem regenInGen_right_length (k : Nat) (hk : 4 ≤ k) (p : Int) (z : Nat) (U R : List Bool) :
    (regenInGen k p z U R).tape.right.length + k + 2 = 2 ^ (k - 1) + z + R.length :=
  regenIn_right_length k hk p z [] R

theorem cascadeRegGen_right_length (k : Nat) (hk : 4 ≤ k) (p : Int) (U R : List Bool) :
    (cascadeRegGen k p U R).tape.right.length + k = 2 ^ (k + 1) + 7 + R.length :=
  cascadeReg_right_length k 1 hk p [] R

/-- `regenOut_anchor_forced` with the comb freed: the anchor is the SAME `p − 2^k`. -/
theorem regenOutGen_anchor_forced (k : Nat) (hk : 4 ≤ k) (n : Nat) (p P : Int)
    (U R : List Bool)
    (h : steps n (regenInGen k p (2 ^ (k - 1) + 9) U R) = some (cascadeRegGen k P U R)) :
    P = p - 2 ^ k := by
  have hL := steps_left_mono n _ _ h
  have hR := steps_right_mono n _ _ h
  have hp1 : (regenInGen k p (2 ^ (k - 1) + 9) U R).pos = p := rfl
  have hp2 : (cascadeRegGen k P U R).pos = P := rfl
  rw [hp1, hp2] at hL hR
  have hl1 := regenInGen_left_length k hk p (2 ^ (k - 1) + 9) U R
  have hl2 := cascadeRegGen_left_length k P U R
  have hr1 := regenInGen_right_length k hk p (2 ^ (k - 1) + 9) U R
  have hr2 := cascadeRegGen_right_length k hk P U R
  obtain ⟨LI, hLI⟩ : ∃ t, (regenInGen k p (2 ^ (k - 1) + 9) U R).tape.left.length = t := ⟨_, rfl⟩
  obtain ⟨RI, hRI⟩ : ∃ t, (regenInGen k p (2 ^ (k - 1) + 9) U R).tape.right.length = t := ⟨_, rfl⟩
  obtain ⟨LO, hLO⟩ : ∃ t, (cascadeRegGen k P U R).tape.left.length = t := ⟨_, rfl⟩
  obtain ⟨RO, hRO⟩ : ∃ t, (cascadeRegGen k P U R).tape.right.length = t := ⟨_, rfl⟩
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

#print axioms regenOutGen_anchor_forced

/-- **`RegenLawGen ∀k ≥ 7`** — the ported assembly.  Note it needs the CANONICAL `RegenLaw`
only at the strictly lower levels (`m ≤ k−2`), which `regenLaw_closed` already supplies —
so this is a direct theorem, not a nested induction. -/
theorem regenLawGen_ge7 (k : Nat) (hk : 7 ≤ k) (U R : List Bool) :
    steps (exitSteps k) (regenInGen k 0 (2 ^ (k - 1) + 9) U R)
      = some (cascadeRegGen k (0 - 2 ^ k) U R) := by
  have hcomp : ∃ P : Int, steps (exitSteps k) (regenInGen k 0 (2 ^ (k - 1) + 9) U R)
      = some (cascadeRegGen k P U R) := by
    obtain ⟨q', hfold⟩ := interiorFold_lower_expl (k - 6) (by omega)
        (fun m hm hmle => regenLaw_closed m hm)
        ((0 : Int) + 2 ^ (k - 1) - (k : Int) + 4) (regenWordGen k U) (zeros 32 ++ R)
    rw [show (k - 6) - 1 = k - 7 from by omega, foldMarker_eq_depStack k hk] at hfold
    refine ⟨(q' - 2 ^ 4) - 2 ^ k + (k : Int) + 44 - 2 ^ k, ?_⟩
    have ht := trailOut_allGen k (by omega)
      ((q' - 2 ^ 4) - 2 ^ k + (k : Int) + 44) U R
    rw [show ((q' - 2 ^ 4) - 2 ^ k + (k : Int) + 44) + 2 ^ k - (k : Int) - 44
        = q' - 2 ^ 4 from by omega] at ht
    rw [framingArith k hk, steps_add, steps_add, steps_add,
        leadOut_allGen k (by omega) 0 U R, someBind,
        leadOut_is_interiorIn k hk _ _ R, hfold, someBind]
    rw [show (zeros 32 ++ R : List Bool) = zeros 16 ++ (zeros 16 ++ R) from by
          rw [← List.append_assoc, ← zeros_add],
        trailFloorRegen q' (depStack k (regenWordGen k U)) (zeros 16 ++ R), someBind]
    exact ht
  obtain ⟨P, hP⟩ := hcomp
  rw [hP, regenOutGen_anchor_forced k (by omega) (exitSteps k) 0 P U R hP]

#print axioms regenLawGen_ge7

/-- **`RegenLawGen` — CLOSED `∀ k ≥ 4`, `∀ p`, `∀ U`, `∀ R`.** -/
theorem regenLawGen_closed (k : Nat) (hk : 4 ≤ k) (p : Int) (U R : List Bool) :
    steps (exitSteps k) (regenInGen k p (2 ^ (k - 1) + 9) U R)
      = some (cascadeRegGen k (p - 2 ^ k) U R) := by
  have hcases : k = 4 ∨ k = 5 ∨ k = 6 ∨ 7 ≤ k := by omega
  rcases hcases with h | h | h | h
  · subst h; exact regenLawGen_4 p U R
  · subst h; exact regenLawGen_5 p U R
  · subst h; exact regenLawGen_6 p U R
  · have h0 := regenLawGen_ge7 k h U R
    have hs := steps_pos_shift (d := p) h0
    rw [show (0:Int) + p = p from by omega] at hs
    show steps (exitSteps k) ⟨.E, p, _⟩ = _
    rw [hs]
    exact congrArg some (cfgPos (by omega))

/-- CONTROL: `regenLaw_closed`'s content is the instance `U := pow01 (2^{k−1}−2) ++ marker`. -/
theorem regenLawGen_closed_specialises (k : Nat) (hk : 4 ≤ k) (p : Int) (marker R : List Bool) :
    steps (exitSteps k) (regenIn k p (2 ^ (k - 1) + 9) marker R)
      = some (cascadeReg k 1 (p - 2 ^ k) marker R) := by
  have h := regenLawGen_closed k hk p (pow01 (2 ^ (k - 1) - 2) ++ marker) R
  show steps (exitSteps k) (regenInGen k p (2 ^ (k - 1) + 9)
      (pow01 (2 ^ (k - 1) - 2) ++ marker) R) = _
  rw [h]
  refine congrArg some ?_
  show (⟨.E, _, ⟨pow01 1 ++ (pow01 (2 ^ (k-1) - 2) ++ marker), false, _⟩⟩ : Cfg) = _
  rw [← List.append_assoc, ← pow01_add]
  rfl

#print axioms regenLawGen_closed
#print axioms regenLawGen_closed_specialises

/-- **`topRung` — THE LADDER'S LAST RUNG, `∀ k ≥ 4`.**
`cascadeReg_topgrind` (∀ marker, already proven) then `RegenLawGen (k+1)`.  The incoming
marker carries only the DEGENERATE ladder layer `0 0 1` — no comb — which is exactly what the
real orbit presents at the ladder top (`LADDER_TOP_NOT_CANONICAL_2026-07-23.md`), and the OUT
is `cascadeReg (k+1)`'s right with the collapsed left `pow01 1 ++ U`. -/
theorem topRung (k : Nat) (hk : 4 ≤ k) (p : Int) (U R : List Bool) :
    steps (topGrindSteps k + exitSteps (k + 1))
        (cascadeReg k 1 p (false :: false :: true :: U) (zeros (2 ^ k) ++ R))
      = some (cascadeRegGen (k + 1)
          ((p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int)) - 2 ^ (k + 1)) U R) := by
  rw [steps_add,
      cascadeReg_topgrind k hk p (false :: false :: true :: U) (zeros (2 ^ k) ++ R), someBind]
  obtain ⟨m, rfl⟩ : ∃ m, k = m + 4 := ⟨k - 4, by omega⟩
  have e1 : 4 * (2 ^ (m + 4 - 1) - 2) + 4 + 1 = 2 ^ (m + 4 + 1) - 3 := by
    have hm : 1 ≤ 2 ^ m := Nat.one_le_two_pow
    have h1 : 2 ^ (m + 4 - 1) = 2 ^ m * 8 := by rw [show m + 4 - 1 = m + 3 from by omega, Nat.pow_add]
    have h2 : 2 ^ (m + 4 + 1) = 2 ^ m * 32 := by rw [show m + 4 + 1 = m + 5 from by omega, Nat.pow_add]
    omega
  have hL : ones (4 * (2 ^ (m + 4 - 1) - 2) + 4)
        ++ (pow10 1 ++ (true :: false :: false :: true :: U))
      = ones (2 ^ (m + 4 + 1) - 3) ++ (false :: true :: false :: false :: true :: U) := by
    show ones (4 * (2 ^ (m + 4 - 1) - 2) + 4)
        ++ (true :: false :: true :: false :: false :: true :: U)
      = ones (2 ^ (m + 4 + 1) - 3) ++ (false :: true :: false :: false :: true :: U)
    rw [ones_append_true, e1]
  show steps (exitSteps (m + 4 + 1))
      ⟨.E, _, ⟨ones (4 * (2 ^ (m + 4 - 1) - 2) + 4)
        ++ (pow10 1 ++ (true :: false :: false :: true :: U)), false,
        false :: (descCascade (m + 4 - 3) ++
          (false :: false :: (zeros 7 ++ (zeros (2 ^ (m + 4)) ++ R))))⟩⟩ = _
  rw [hL, zeros_pad (m + 4) R, show m + 4 - 3 = m + 4 + 1 - 4 from by omega]
  exact regenLawGen_closed (m + 4 + 1) (by omega) _ U R

#print axioms topRung

-- ANTI-VACUITY (METHODS M4): the ∀k rung cost must reproduce the MEASURED top rung.
-- g=2: cascadeReg 10 @1 270 303 → the top @2 851 880 = 1 581 577 steps, split by the orbit at
-- @2 315 814 into 1 045 511 (topgrind) + 536 066 (REGEN) — both exact library constants.
example : topGrindSteps 10 = 1045511 := by decide
example : exitSteps 11 = 536066 := by decide
example : topGrindSteps 10 + exitSteps 11 = 1581577 := by decide

/-! ### S2 — the 74-step seam `topRung` OUT → `tailLaw` IN

MEASURED (`x2s2_seam.py`) at g=2 (2 851 880 → 2 851 954) and g=4 (44 986 730 → 44 986 804):
74 steps at both, endpoints agreeing across generations well beyond the head's reach, so the
episode is level-free.  Head excursion is 11 cells left and 9 right, against exactly that much
concrete tape — so `X` and `Z` are never read and the `∀ X Z` statement is provable, not merely
true at `[]` (METHODS M3′ step 2). -/

private theorem s2c0 (X Z : List Bool) :
    steps 25 ⟨.E, 0, ⟨[false, true, false, false, true, false, true, false, true, false, false] ++ X, false, [false, false, false, true, true, true, true, true, true] ++ Z⟩⟩
      = some ⟨.E, 7, ⟨[true, true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, false] ++ X, true, [true, true] ++ Z⟩⟩ := by rfl

private theorem s2c1 (X Z : List Bool) :
    steps 25 ⟨.E, 7, ⟨[true, true, true, true, true, true, true, true, true, false, false, true, false, true, false, true, false, false] ++ X, true, [true, true] ++ Z⟩⟩
      = some ⟨.C, 6, ⟨[true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, false] ++ X, true, [false, true, false] ++ Z⟩⟩ := by rfl

private theorem s2c2 (X Z : List Bool) :
    steps 24 ⟨.C, 6, ⟨[true, true, true, true, true, true, true, true, true, false, true, false, true, false, true, false, false] ++ X, true, [false, true, false] ++ Z⟩⟩
      = some ⟨.E, -10, ⟨[false] ++ X, false, [false, false, false, false, false, false, false, true, false, true, false, true, false, true, false, true, false, true, false] ++ Z⟩⟩ := by rfl

/-- **S2 — the ladder-top → tail seam, ∀ position, ∀ left tail, ∀ right tail.**  74 steps. -/
theorem seam74 (p : Int) (X Z : List Bool) :
    steps 74 ⟨.E, p, ⟨[false, true, false, false, true, false, true, false, true, false, false]
        ++ X, false, [false, false, false, true, true, true, true, true, true] ++ Z⟩⟩
      = some ⟨.E, p - 10, ⟨[false] ++ X, false, [false, false, false, false, false, false, false, true, false, true, false, true, false, true, false, true, false, true, false] ++ Z⟩⟩ := by
  have h0 : steps 74 ⟨.E, 0, ⟨[false, true, false, false, true, false, true, false, true, false, false] ++ X, false, [false, false, false, true, true, true, true, true, true] ++ Z⟩⟩ = some ⟨.E, -10, ⟨[false] ++ X, false, [false, false, false, false, false, false, false, true, false, true, false, true, false, true, false, true, false, true, false] ++ Z⟩⟩ := by
    rw [show (74:Nat) = 25 + (25 + 24) from by decide, steps_add, s2c0 X Z, someBind,
        steps_add, s2c1 X Z, someBind]
    exact s2c2 X Z
  have h := steps_pos_shift (d := p) h0
  rw [show (0:Int) + p = p from by omega] at h
  rw [h]
  exact congrArg some (cfgPos (by omega))

#print axioms seam74

/-- **`topRungSeam`** — `topRung ∘ seam74`.  The ladder's last rung and the 74-step seam, composed:
from the canonical `cascadeReg k` (with the degenerate layer `0 0 1` and the seam's fixed 9-cell
marker prefix) to exactly `tailLaw`'s IN shape. -/
theorem topRungSeam (k : Nat) (hk : 4 ≤ k) (p : Int) (X R : List Bool) :
    steps (topGrindSteps k + exitSteps (k + 1) + 74)
        (cascadeReg k 1 p
          (false :: false :: true ::
            (false :: false :: true :: false :: true :: false :: true :: false :: false :: X))
          (zeros (2 ^ k) ++ R))
      = some ⟨.E, p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int) - 2 ^ (k + 1) - 10,
          ⟨false :: X, false,
            [false, false, false, false, false, false, false, true, false, true, false, true,
             false, true, false, true, false, true, false]
            ++ (ones (2 ^ (k + 1) - 9) ++ (false :: false ::
                  (descCascade (k - 2) ++ (false :: false :: (zeros 7 ++ R)))))⟩⟩ := by
  have h9 : (9 : Nat) ≤ 2 ^ (k + 1) := by
    have h : (2:Nat) ^ 4 ≤ 2 ^ (k + 1) := Nat.pow_le_pow_right (by decide) (by omega)
    have : (2:Nat) ^ 4 = 16 := by decide
    omega
  rw [steps_add,
      topRung k hk p
        (false :: false :: true :: false :: true :: false :: true :: false :: false :: X) R,
      someBind]
  show steps 74 ⟨.E, _, ⟨pow01 1 ++ _, false,
      false :: false :: false :: (ones (2 ^ (k + 1) - 3) ++ (false :: false ::
        (descCascade (k + 1 - 3) ++ (false :: false :: (zeros 7 ++ R)))))⟩⟩ = _
  rw [show (2:Nat) ^ (k + 1) - 3 = 6 + (2 ^ (k + 1) - 9) from by omega, ones_add,
      show k + 1 - 3 = k - 2 from by omega]
  exact seam74 _ X
    (ones (2 ^ (k + 1) - 9) ++ (false :: false ::
      (descCascade (k - 2) ++ (false :: false :: (zeros 7 ++ R)))))

#print axioms topRungSeam

/-- The right tail `seam74` hands to `tailLaw`, as a function of the level and the outer tail. -/
def seamZ (k : Nat) (R : List Bool) : List Bool :=
  [false, false, false, true, false, true, false, true, false, true, false, true, false, true,
   false] ++ (ones (2 ^ (k + 1) - 9) ++ (false :: false ::
      (descCascade (k - 2) ++ (false :: false :: (zeros 7 ++ R)))))

/-- **`topRungToMilestone`** — `topRung ∘ seam74 ∘ tailLaw`, `∀k ∀j`.  From the ladder's last
canonical `cascadeReg k` all the way onto the next milestone's frame: the whole exit of the
doubling phase, in `topGrindSteps k + exitSteps (k+1) + 74 + (27j + 110)` steps. -/
theorem topRungToMilestone (k j : Nat) (hk : 4 ≤ k) (p : Int) (L R : List Bool) :
    steps (topGrindSteps k + exitSteps (k + 1) + 74 + (27 * j + 110))
        (cascadeReg k 1 p
          (false :: false :: true ::
            (false :: false :: true :: false :: true :: false :: true :: false :: false ::
              frameL j (turnWord ++ (endWord ++ (zeros 11 ++ L)))))
          (zeros (2 ^ k) ++ R))
      = some ⟨.E, p + 5 + 2 * ((2 ^ (k - 1) - 2 : Nat) : Int) - 2 ^ (k + 1) - 10
              - 7 * (j : Int) - 26,
          ⟨zeros 10 ++ L, false,
            zeros 21 ++ (true :: (zeros 6 ++ (true :: false :: frameZ j (seamZ k R))))⟩⟩ := by
  rw [steps_add,
      topRungSeam k hk p (frameL j (turnWord ++ (endWord ++ (zeros 11 ++ L)))) R, someBind]
  exact tailLaw j _ L (seamZ k R)

-- ANTI-VACUITY (METHODS M4): the composed exit cost at g=2 (k = g+8 = 10, j = g−1 = 1) must be
-- the MEASURED cascadeReg 10 @1 270 303 → M1(3) @2 852 091 = 1 581 788 steps.
example : topGrindSteps 10 + exitSteps 11 + 74 + (27 * 1 + 110) = 1581788 := by decide
-- and at g=4 (k = 12, j = 3): cascadeReg 12 @44 986 730 is 74 steps before the tail odometer,
-- whose own start was measured at 44 986 804; the tail then costs 27·3 + 110 = 191.
example : 74 + (27 * 3 + 110) = 265 := by decide

#print axioms seamZ
#print axioms topRungToMilestone
