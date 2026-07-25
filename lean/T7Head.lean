import X2

namespace X2

theorem descTile (p : Int) (L X : List Bool) :
    steps 6 ⟨.E, p, ⟨L, false, false :: true :: true :: X⟩⟩
      = some ⟨.E, p + 2, ⟨false :: true :: L, false, false :: X⟩⟩ := by
  have h : steps 6 (⟨.E, p, ⟨L, false, false :: true :: true :: X⟩⟩ : Cfg)
      = some ⟨.E, p + 1 + 1 + 1 - 1 - 1 + 1, ⟨false :: true :: L, false, false :: X⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- **THE DESCENT CHEW FOLD, ARBITRARY length** (T7 head, 2026-07-22): `m` tiles = `6m` steps chew a
`1^{2m}` block (behind its leading `0`) into the comb `pow01 m = (01)^m` deposited on the left,
advancing `+2m`, leading `0` and tail `Y` preserved.  The head-descent analogue of `sweepEF`
(comb↔block), built tile + length induction.  `some` ⇒ HALT-FREE. -/
theorem descFold : ∀ (m : Nat) (p : Int) (L Y : List Bool),
    steps (6 * m) ⟨.E, p, ⟨L, false, false :: (ones (2 * m) ++ Y)⟩⟩
      = some ⟨.E, p + 2 * (m : Int), ⟨pow01 m ++ L, false, false :: Y⟩⟩ := by
  intro m
  induction m with
  | zero =>
    intro p L Y
    show steps 0 _ = _
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ m ih =>
    intro p L Y
    have hn : 6 * (m + 1) = 6 + 6 * m := by omega
    rw [hn, steps_add]
    have hb : ones (2 * (m + 1)) = true :: true :: ones (2 * m) := by
      rw [show 2 * (m + 1) = 2 + 2 * m from by omega, ones_add]; rfl
    rw [hb]
    show (steps 6 ⟨.E, p, ⟨L, false, false :: true :: true :: (ones (2 * m) ++ Y)⟩⟩).bind
        (steps (6 * m)) = _
    rw [descTile, someBind, ih (p + 2) (false :: true :: L) Y]
    have hL : pow01 m ++ (false :: true :: L) = pow01 (m + 1) ++ L := by
      rw [show (false :: true :: L) = pow01 1 ++ L from rfl, ← List.append_assoc, ← pow01_add]
    rw [hL]
    exact congrArg some (cfgPos (by push_cast; omega))


theorem descTile2 (p : Int) (L Y : List Bool) :
    steps 6 ⟨.E, p, ⟨false :: false :: L, true, true :: true :: Y⟩⟩
      = some ⟨.E, p + 2, ⟨false :: false :: true :: false :: L, true, Y⟩⟩ := by
  have h : steps 6 (⟨.E, p, ⟨false :: false :: L, true, true :: true :: Y⟩⟩ : Cfg)
      = some ⟨.E, p - 1 - 1 + 1 + 1 + 1 + 1, ⟨false :: false :: true :: false :: L, true, Y⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- **THE PHASE-2 DESCENT FOLD, ∀m** (T7 head): `m` `descTile2`s = `6m` steps chew `1^{2m}` (head on
the block) into `pow10 m` deposited after the `0 0` separator, `+2m`, tail `Y` preserved. -/
theorem descFold2 : ∀ (m : Nat) (p : Int) (L Y : List Bool),
    steps (6 * m) ⟨.E, p, ⟨false :: false :: L, true, ones (2 * m) ++ Y⟩⟩
      = some ⟨.E, p + 2 * (m : Int), ⟨false :: false :: (pow10 m ++ L), true, Y⟩⟩ := by
  intro m
  induction m with
  | zero =>
    intro p L Y
    show steps 0 _ = _
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ m ih =>
    intro p L Y
    have hn : 6 * (m + 1) = 6 + 6 * m := by omega
    rw [hn, steps_add]
    have hb : ones (2 * (m + 1)) = true :: true :: ones (2 * m) := by
      rw [show 2 * (m + 1) = 2 + 2 * m from by omega, ones_add]; rfl
    rw [hb]
    show (steps 6 ⟨.E, p, ⟨false :: false :: L, true, true :: true :: (ones (2 * m) ++ Y)⟩⟩).bind
        (steps (6 * m)) = _
    rw [descTile2, someBind, ih (p + 2) (true :: false :: L) Y]
    have hL : pow10 m ++ (true :: false :: L) = pow10 (m + 1) ++ L := by
      rw [show (true :: false :: L) = pow10 1 ++ L from rfl, ← List.append_assoc, ← pow10_add]
    rw [hL]
    exact congrArg some (cfgPos (by push_cast; omega))


/-- **THE PHASE-1→PHASE-2 TRANSITION** (T7 head, 2026-07-22): the fixed 12-step episode at a block
boundary that bridges the head-on-0 chew (phase 1) to the head-on-1 chew (phase 2): it consumes the
leftover `1 1 1`, the `0 0` separator and the first `1 1` of the next block, depositing a fixed
8-cell comb layer and landing head-on-1.  Level-independent (a local boundary crossing). -/
theorem descTrans (p : Int) (L X : List Bool) :
    steps 12 ⟨.E, p, ⟨L, false,
        false :: true :: true :: true :: false :: false :: true :: true :: X⟩⟩
      = some ⟨.E, p + 8,
          ⟨false :: false :: true :: false :: false :: true :: false :: true :: L, true, X⟩⟩ := by
  have h : steps 12 (⟨.E, p, ⟨L, false,
        false :: true :: true :: true :: false :: false :: true :: true :: X⟩⟩ : Cfg)
      = some ⟨.E, p + 1 + 1 + 1 - 1 - 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1,
          ⟨false :: false :: true :: false :: false :: true :: false :: true :: L, true, X⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))


/-- **PHASE 1 + TRANSITION composed** (T7 head, 2026-07-23): `descFold` (chew `2m` block cells) then
`descTrans` (cross the `1 1 1 0 0 1 1` boundary), in `6m + 12` steps.  Takes a block
`1^{2m} 1 1 1 0 0 1 1` (with tail `X`) to the phase-2 start (head-on-1 on `X`). -/
theorem descChew (m : Nat) (p : Int) (L X : List Bool) :
    steps (6 * m + 12)
        ⟨.E, p, ⟨L, false,
          false :: (ones (2 * m) ++
            (true :: true :: true :: false :: false :: true :: true :: X))⟩⟩
      = some ⟨.E, p + 2 * (m : Int) + 8,
          ⟨false :: false :: true :: false :: false :: true :: false :: true :: (pow01 m ++ L),
           true, X⟩⟩ := by
  rw [steps_add,
      descFold m p L (true :: true :: true :: false :: false :: true :: true :: X), someBind,
      descTrans (p + 2 * (m : Int)) (pow01 m ++ L) X]

/-- **FULL DESCENT RUNG** (T7 head, 2026-07-23): `descChew ∘ descFold2` — chew the top block, cross
the boundary, then phase-2 rebuild the comb on the next block `1^{2m'}`, in `6m+12+6m'` steps.  The
machine shape of one `descIn k → descIn (k−1)` rung (modulo the descIn framing). -/
theorem descRung (m m' : Nat) (p : Int) (L Y : List Bool) :
    steps (6 * m + 12 + 6 * m')
        ⟨.E, p, ⟨L, false,
          false :: (ones (2 * m) ++
            (true :: true :: true :: false :: false :: true :: true ::
              (ones (2 * m') ++ Y)))⟩⟩
      = some ⟨.E, p + 2 * (m : Int) + 8 + 2 * (m' : Int),
          ⟨false :: false :: (pow10 m' ++
            (true :: false :: false :: true :: false :: true :: (pow01 m ++ L))),
           true, Y⟩⟩ := by
  rw [steps_add, descChew m p L (ones (2 * m') ++ Y), someBind,
      descFold2 m' (p + 2 * (m : Int) + 8)
        (true :: false :: false :: true :: false :: true :: (pow01 m ++ L)) Y]


/-- **THE SETTLE** (T7 head, 2026-07-23): the fixed 3-step episode ending a descent rung — from
phase-2's head-on-`1` (`0 0 1 · comb C · [1]block`) to `descIn (k−1)`'s head-on-`0` on the fresh
leading `0` (`0 1 · comb C · [0]0 block`), advancing `−1`.  Level-free. -/
theorem settle (p : Int) (C block : List Bool) :
    steps 3 ⟨.E, p, ⟨false :: false :: true :: C, true, block⟩⟩
      = some ⟨.E, p - 1, ⟨false :: true :: C, false, false :: block⟩⟩ := by
  have h : steps 3 (⟨.E, p, ⟨false :: false :: true :: C, true, block⟩⟩ : Cfg)
      = some ⟨.E, p - 1 - 1 + 1, ⟨false :: true :: C, false, false :: block⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))


/-- **THE FULL DESCENT LEVEL** (T7 head, 2026-07-23): `descRung ∘ settle` — the complete
`descIn`-to-`descIn` rung mechanism ending head-on-`0` on the fresh leading `0`.  In
`6m + 12 + 6(m'+1) + 3` steps: chew block `1^{2m}`, cross, phase-2 rebuild `1^{2(m'+1)}`, settle.
This is the machine content of `DescLaw` (modulo the descIn arithmetic framing). -/
theorem descLevel (m m' : Nat) (p : Int) (L Y : List Bool) :
    steps (6 * m + 12 + 6 * (m' + 1) + 3)
        ⟨.E, p, ⟨L, false,
          false :: (ones (2 * m) ++
            (true :: true :: true :: false :: false :: true :: true ::
              (ones (2 * (m' + 1)) ++ Y)))⟩⟩
      = some ⟨.E, p + 2 * (m : Int) + 8 + 2 * ((m' : Int) + 1) - 1,
          ⟨false :: true ::
            (false :: (pow10 m' ++
              (true :: false :: false :: true :: false :: true :: (pow01 m ++ L)))),
           false, false :: Y⟩⟩ := by
  rw [steps_add, descRung m (m' + 1) p L Y, someBind]
  have hp : pow10 (m' + 1) ++
      (true :: false :: false :: true :: false :: true :: (pow01 m ++ L))
      = true :: false :: (pow10 m' ++
          (true :: false :: false :: true :: false :: true :: (pow01 m ++ L))) := rfl
  rw [hp, settle]
  exact congrArg some (cfgPos (by push_cast; omega))


/-- `0 :: (10)^n = (01)^n :: 0`. -/
theorem false_pow10 (n : Nat) : false :: pow10 n = pow01 n ++ [false] := by
  induction n with
  | zero => rfl
  | succ n ih =>
    show false :: (true :: false :: pow10 n) = (false :: true :: pow01 n) ++ [false]
    rw [show (false :: true :: pow01 n) ++ [false] = false :: true :: (pow01 n ++ [false]) from rfl,
        ← ih]

def descIn (k : Nat) (p : Int) (M TAIL : List Bool) : Cfg :=
  ⟨.E, p, ⟨pow01 (2 ^ (k - 1)) ++ M, false,
      false :: (ones (2 ^ k - 3) ++ (false :: false :: (descCascade (k - 2) ++ TAIL)))⟩⟩

#check @false_pow10
#check @descIn

end X2
