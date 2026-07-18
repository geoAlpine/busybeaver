import X2
open X2

/-!
# BlankNorm — a boundary-blank normalization congruence for `steps` (namespace `X2`)

A NEW REUSABLE WEAPON, axiom-clean (`propext`/`Quot.sound` only, no `sorry`,
no `native_decide`, no Mathlib).

## What it does

Reconciles a *canonical* milestone config (blank-trimmed: no redundant trailing
`false`s on `right` / leading `false`s at the far-left of `left`) with the
*actual reached* config, which carries explicit boundary blanks — because `step`
never keeps canonical trailing blanks (`mvR ⟨l,h,[]⟩ = ⟨h::l,false,[]⟩`
regenerates a blank; the tape lists do not store them).

The core structural fact (verified on the absorption boundary by `#eval`, see
`BNprobe.lean`): a trailing `false` appended to `right` is **harmless** under
`step`. It rides along cell-for-cell, and is **absorbed** exactly when the head
moves right off the end (`mvR ⟨l,h,[]⟩ = mvR ⟨l,h,[false]⟩ = ⟨h::l,false,[]⟩`).
Symmetrically a `false` appended to the far end of `left`.

So the congruence is a *disjunction* (absorbed / not), stated honestly. `pos` is
already handled by the existing `steps`/`cfgPos` machinery (`step` only shifts
`pos`, never reads it), so this file focuses purely on the blank/tape
reconciliation.

## Headline theorems

* `steps_rpad` : one trailing blank on `right` congruence (RIGHT boundary).
* `steps_lpad` : one leading blank on `left` congruence (LEFT boundary).
* `steps_rpad_zeros` / `steps_lpad_zeros` : the ITERATED versions — a whole
  block `zeros k` of boundary blanks, with `j ≤ k` surviving (the rest absorbed).
  These are the forms that lift a transport proven for the trimmed config to the
  real padded config.
-/

namespace X2

/-! ## §1 The right-pad relation and its single-cell preservation lemmas. -/

/-- `t2` is `t1` with an OPTIONAL single trailing blank on `right` (and `left`,
`head` unchanged). `t1` = trimmed/canonical, `t2` = padded/real. -/
abbrev rtail (t1 t2 : Tape) : Prop :=
  t2.left = t1.left ∧ t2.head = t1.head ∧
    (t2.right = t1.right ∨ t2.right = t1.right ++ [false])

/-- `mvR` preserves the right-pad relation (absorbs the pad when `right = []`). -/
theorem rtail_mvR (l : List Bool) (hd : Bool) (r1 r2 : List Bool)
    (hr : r2 = r1 ∨ r2 = r1 ++ [false]) :
    rtail (mvR ⟨l, hd, r1⟩) (mvR ⟨l, hd, r2⟩) := by
  rcases hr with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h
    cases r1 with
    | nil => exact ⟨rfl, rfl, Or.inl rfl⟩          -- absorbed: both land right = []
    | cons x r => exact ⟨rfl, rfl, Or.inr rfl⟩     -- rides along: right = r ++ [false]

/-- `mvL` preserves the right-pad relation (never absorbs; pad rides on `right`). -/
theorem rtail_mvL (l : List Bool) (hd : Bool) (r1 r2 : List Bool)
    (hr : r2 = r1 ∨ r2 = r1 ++ [false]) :
    rtail (mvL ⟨l, hd, r1⟩) (mvL ⟨l, hd, r2⟩) := by
  rcases hr with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h
    cases l with
    | nil => exact ⟨rfl, rfl, Or.inr rfl⟩
    | cons y ll => exact ⟨rfl, rfl, Or.inr rfl⟩

/-- Config-level right-pad relation: same state & pos, `rtail` tapes. -/
abbrev crtail (c1 c2 : Cfg) : Prop :=
  c2.st = c1.st ∧ c2.pos = c1.pos ∧ rtail c1.tape c2.tape

/-- **Single-step bisimulation for the right pad.** Either both halt, or both
step and the results stay right-pad-related. Proved by cases on `(state, head)`;
the halt case is `(B, true)`. -/
theorem step_crtail (c1 c2 : Cfg) (h : crtail c1 c2) :
    (step c1 = none ∧ step c2 = none) ∨
    (∃ d1 d2, step c1 = some d1 ∧ step c2 = some d2 ∧ crtail d1 d2) := by
  rcases c1 with ⟨s1, p1, ⟨l1, hd1, r1⟩⟩
  rcases c2 with ⟨s2, p2, ⟨l2, hd2, r2⟩⟩
  obtain ⟨hst, hpos, hll, hhh, hr⟩ := h
  dsimp only at hst hpos hll hhh hr
  -- hst : s2 = s1, hpos : p2 = p1, hll : l2 = l1, hhh : hd2 = hd1,
  -- hr : r2 = r1 ∨ r2 = r1 ++ [false]
  subst s2; subst p2; subst l2; subst hd2
  cases s1 <;> cases hd1 <;>
    first
      | (left; exact ⟨rfl, rfl⟩)
      | (right; exact ⟨_, _, rfl, rfl, ⟨rfl, rfl, rtail_mvR _ _ _ _ hr⟩⟩)
      | (right; exact ⟨_, _, rfl, rfl, ⟨rfl, rfl, rtail_mvL _ _ _ _ hr⟩⟩)

/-- **Multi-step bisimulation for the right pad** (`steps`). Lock-step: they halt
at exactly the same step, or both survive `n` steps still right-pad-related. -/
theorem steps_crtail : ∀ (n : Nat) (c1 c2 : Cfg), crtail c1 c2 →
    (steps n c1 = none ∧ steps n c2 = none) ∨
    (∃ d1 d2, steps n c1 = some d1 ∧ steps n c2 = some d2 ∧ crtail d1 d2) := by
  intro n
  induction n with
  | zero => intro c1 c2 h; right; exact ⟨c1, c2, rfl, rfl, h⟩
  | succ n ih =>
    intro c1 c2 h
    rcases step_crtail c1 c2 h with ⟨h1, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · left
      refine ⟨?_, ?_⟩
      · show (step c1).bind (steps n) = none; rw [h1]; rfl
      · show (step c2).bind (steps n) = none; rw [h2]; rfl
    · have e1 : steps (n + 1) c1 = steps n d1 := by
        show (step c1).bind (steps n) = steps n d1; rw [hd1]; rfl
      have e2 : steps (n + 1) c2 = steps n d2 := by
        show (step c2).bind (steps n) = steps n d2; rw [hd2]; rfl
      rw [e1, e2]; exact ih d1 d2 hdr

/-- **THE RIGHT-BOUNDARY BLANK CONGRUENCE (the weapon).** If a run on the
blank-trimmed config lands `some ⟨s',p',⟨L',hd',R'⟩⟩`, then the SAME run on the
config with one extra trailing blank on `right` lands the same config — with the
trailing blank either ABSORBED (`R'`) or still riding (`R' ++ [false]`). Both
disjuncts are TRUE and both occur (see the demo). `pos` and state are preserved
identically. -/
theorem steps_rpad (n : Nat) (s : St) (p : Int) (L : List Bool) (hd : Bool)
    (R : List Bool) {s' : St} {p' : Int} {L' : List Bool} {hd' : Bool}
    {R' : List Bool}
    (hrun : steps n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    steps n ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ ∨
    steps n ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩
      = some ⟨s', p', ⟨L', hd', R' ++ [false]⟩⟩ := by
  have hc : crtail ⟨s, p, ⟨L, hd, R⟩⟩ ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ :=
    ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
  rcases steps_crtail n _ _ hc with ⟨h1, _⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
  · rw [hrun] at h1; simp at h1
  · have hd1' : d1 = ⟨s', p', ⟨L', hd', R'⟩⟩ := Option.some.inj (hd1.symm.trans hrun)
    subst hd1'
    rcases d2 with ⟨s2, p2, ⟨l2, h2, r2⟩⟩
    obtain ⟨hst, hpos, hll, hhh, hrr⟩ := hdr
    dsimp only at hst hpos hll hhh hrr
    -- hst : s2 = s', hpos : p2 = p', hll : l2 = L', hhh : h2 = hd',
    -- hrr : r2 = R' ∨ r2 = R' ++ [false]
    subst s2; subst p2; subst l2; subst h2
    rcases hrr with h | h
    · left; subst h; exact hd2
    · right; subst h; exact hd2

/-! ## §2 The symmetric LEFT-pad (leading blank) development. -/

/-- `t2` is `t1` with an OPTIONAL single blank appended at the FAR end of `left`
(a leading/leftmost blank), `head`/`right` unchanged. -/
abbrev ltail (t1 t2 : Tape) : Prop :=
  t2.head = t1.head ∧ t2.right = t1.right ∧
    (t2.left = t1.left ∨ t2.left = t1.left ++ [false])

/-- `mvR` preserves the left-pad relation (never absorbs; pad rides on `left`). -/
theorem ltail_mvR (l1 l2 : List Bool) (hd : Bool) (r : List Bool)
    (hl : l2 = l1 ∨ l2 = l1 ++ [false]) :
    ltail (mvR ⟨l1, hd, r⟩) (mvR ⟨l2, hd, r⟩) := by
  rcases hl with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h
    cases r with
    | nil => exact ⟨rfl, rfl, Or.inr rfl⟩
    | cons x rr => exact ⟨rfl, rfl, Or.inr rfl⟩

/-- `mvL` preserves the left-pad relation (absorbs the pad when `left = []`). -/
theorem ltail_mvL (l1 l2 : List Bool) (hd : Bool) (r : List Bool)
    (hl : l2 = l1 ∨ l2 = l1 ++ [false]) :
    ltail (mvL ⟨l1, hd, r⟩) (mvL ⟨l2, hd, r⟩) := by
  rcases hl with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h
    cases l1 with
    | nil => exact ⟨rfl, rfl, Or.inl rfl⟩          -- absorbed: both land left = []
    | cons y ll => exact ⟨rfl, rfl, Or.inr rfl⟩    -- rides along: left = ll ++ [false]

/-- Config-level left-pad relation. -/
abbrev cltail (c1 c2 : Cfg) : Prop :=
  c2.st = c1.st ∧ c2.pos = c1.pos ∧ ltail c1.tape c2.tape

/-- **Single-step bisimulation for the left pad.** -/
theorem step_cltail (c1 c2 : Cfg) (h : cltail c1 c2) :
    (step c1 = none ∧ step c2 = none) ∨
    (∃ d1 d2, step c1 = some d1 ∧ step c2 = some d2 ∧ cltail d1 d2) := by
  rcases c1 with ⟨s1, p1, ⟨l1, hd1, r1⟩⟩
  rcases c2 with ⟨s2, p2, ⟨l2, hd2, r2⟩⟩
  obtain ⟨hst, hpos, hhh, hrr, hl⟩ := h
  dsimp only at hst hpos hhh hrr hl
  -- hst : s2 = s1, hpos : p2 = p1, hhh : hd2 = hd1, hrr : r2 = r1,
  -- hl : l2 = l1 ∨ l2 = l1 ++ [false]
  subst s2; subst p2; subst hd2; subst r2
  cases s1 <;> cases hd1 <;>
    first
      | (left; exact ⟨rfl, rfl⟩)
      | (right; exact ⟨_, _, rfl, rfl, ⟨rfl, rfl, ltail_mvR _ _ _ _ hl⟩⟩)
      | (right; exact ⟨_, _, rfl, rfl, ⟨rfl, rfl, ltail_mvL _ _ _ _ hl⟩⟩)

/-- **Multi-step bisimulation for the left pad** (`steps`). -/
theorem steps_cltail : ∀ (n : Nat) (c1 c2 : Cfg), cltail c1 c2 →
    (steps n c1 = none ∧ steps n c2 = none) ∨
    (∃ d1 d2, steps n c1 = some d1 ∧ steps n c2 = some d2 ∧ cltail d1 d2) := by
  intro n
  induction n with
  | zero => intro c1 c2 h; right; exact ⟨c1, c2, rfl, rfl, h⟩
  | succ n ih =>
    intro c1 c2 h
    rcases step_cltail c1 c2 h with ⟨h1, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · left
      refine ⟨?_, ?_⟩
      · show (step c1).bind (steps n) = none; rw [h1]; rfl
      · show (step c2).bind (steps n) = none; rw [h2]; rfl
    · have e1 : steps (n + 1) c1 = steps n d1 := by
        show (step c1).bind (steps n) = steps n d1; rw [hd1]; rfl
      have e2 : steps (n + 1) c2 = steps n d2 := by
        show (step c2).bind (steps n) = steps n d2; rw [hd2]; rfl
      rw [e1, e2]; exact ih d1 d2 hdr

/-- **THE LEFT-BOUNDARY BLANK CONGRUENCE (the weapon, symmetric).** One extra
leading blank at the far end of `left`: absorbed (`L'`) or riding (`L' ++ [false]`). -/
theorem steps_lpad (n : Nat) (s : St) (p : Int) (L : List Bool) (hd : Bool)
    (R : List Bool) {s' : St} {p' : Int} {L' : List Bool} {hd' : Bool}
    {R' : List Bool}
    (hrun : steps n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    steps n ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ ∨
    steps n ⟨s, p, ⟨L ++ [false], hd, R⟩⟩
      = some ⟨s', p', ⟨L' ++ [false], hd', R'⟩⟩ := by
  have hc : cltail ⟨s, p, ⟨L, hd, R⟩⟩ ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ :=
    ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
  rcases steps_cltail n _ _ hc with ⟨h1, _⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
  · rw [hrun] at h1; simp at h1
  · have hd1' : d1 = ⟨s', p', ⟨L', hd', R'⟩⟩ := Option.some.inj (hd1.symm.trans hrun)
    subst hd1'
    rcases d2 with ⟨s2, p2, ⟨l2, h2, r2⟩⟩
    obtain ⟨hst, hpos, hhh, hrr, hll⟩ := hdr
    dsimp only at hst hpos hhh hrr hll
    subst s2; subst p2; subst h2; subst r2
    rcases hll with h | h
    · left; subst h; exact hd2
    · right; subst h; exact hd2

/-! ## §3 The ITERATED versions — a whole block `zeros k` of boundary blanks.

The real reached config carries a run of `k` boundary blanks (`0^k`), not just
one. Iterating the single-blank congruence, `j ≤ k` of them survive on the far
side (the rest are absorbed as the head sweeps off the boundary). This is the
form that lifts a transport proven for the fully-trimmed canonical config to the
actual padded config. -/

/-- `zeros k ++ [false] = zeros (k + 1)` (append one more far blank to the block). -/
theorem zeros_snoc : ∀ k : Nat, zeros k ++ [false] = zeros (k + 1) := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih => show false :: (zeros k ++ [false]) = false :: zeros (k + 1); rw [ih]

/-- **ITERATED RIGHT-BOUNDARY CONGRUENCE.** A trailing block of `k` blanks on
`right` reconciles with the trimmed run: the padded run lands the same config
with `j ≤ k` trailing blanks surviving. -/
theorem steps_rpad_zeros (n : Nat) (s : St) (p : Int) (L : List Bool) (hd : Bool)
    (R : List Bool) {s' : St} {p' : Int} {L' : List Bool} {hd' : Bool}
    {R' : List Bool}
    (hrun : steps n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    ∀ k : Nat, ∃ j : Nat, j ≤ k ∧
      steps n ⟨s, p, ⟨L, hd, R ++ zeros k⟩⟩
        = some ⟨s', p', ⟨L', hd', R' ++ zeros j⟩⟩ := by
  intro k
  induction k with
  | zero =>
    refine ⟨0, Nat.le_refl 0, ?_⟩
    show steps n ⟨s, p, ⟨L, hd, R ++ []⟩⟩ = some ⟨s', p', ⟨L', hd', R' ++ []⟩⟩
    rw [List.append_nil, List.append_nil]; exact hrun
  | succ k ih =>
    obtain ⟨j, hjk, hj⟩ := ih
    -- add one more far blank: R ++ zeros (k+1) = (R ++ zeros k) ++ [false]
    have hpad : R ++ zeros (k + 1) = (R ++ zeros k) ++ [false] := by
      rw [← zeros_snoc, List.append_assoc]
    rw [hpad]
    rcases steps_rpad n s p L hd (R ++ zeros k) hj with h | h
    · -- absorbed: still j (and j ≤ k+1)
      exact ⟨j, Nat.le_succ_of_le hjk, h⟩
    · -- rides: j+1 blanks, R' ++ zeros j ++ [false] = R' ++ zeros (j+1)
      refine ⟨j + 1, Nat.succ_le_succ hjk, ?_⟩
      have hr' : R' ++ zeros j ++ [false] = R' ++ zeros (j + 1) := by
        rw [List.append_assoc, zeros_snoc]
      rw [hr'] at h; exact h

/-- **ITERATED LEFT-BOUNDARY CONGRUENCE** (symmetric). -/
theorem steps_lpad_zeros (n : Nat) (s : St) (p : Int) (L : List Bool) (hd : Bool)
    (R : List Bool) {s' : St} {p' : Int} {L' : List Bool} {hd' : Bool}
    {R' : List Bool}
    (hrun : steps n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    ∀ k : Nat, ∃ j : Nat, j ≤ k ∧
      steps n ⟨s, p, ⟨L ++ zeros k, hd, R⟩⟩
        = some ⟨s', p', ⟨L' ++ zeros j, hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    refine ⟨0, Nat.le_refl 0, ?_⟩
    show steps n ⟨s, p, ⟨L ++ [], hd, R⟩⟩ = some ⟨s', p', ⟨L' ++ [], hd', R'⟩⟩
    rw [List.append_nil, List.append_nil]; exact hrun
  | succ k ih =>
    obtain ⟨j, hjk, hj⟩ := ih
    have hpad : L ++ zeros (k + 1) = (L ++ zeros k) ++ [false] := by
      rw [← zeros_snoc, List.append_assoc]
    rw [hpad]
    rcases steps_lpad n s p (L ++ zeros k) hd R hj with h | h
    · exact ⟨j, Nat.le_succ_of_le hjk, h⟩
    · refine ⟨j + 1, Nat.succ_le_succ hjk, ?_⟩
      have hl' : L' ++ zeros j ++ [false] = L' ++ zeros (j + 1) := by
        rw [List.append_assoc, zeros_snoc]
      rw [hl'] at h; exact h

/-! ## §4 Concrete reconciliation demo (kernel `rfl` / weapon-derived).

Demonstrates the weapon actually reconciles trimmed vs padded, INCLUDING the
absorption boundary (the honest hard case). -/

-- (a) Absorption boundary, RIGHT: from `init`, one step, the head runs right off
--     the end.  Trimmed and one-blank-padded land the SAME config (pad absorbed).
example : steps 1 ⟨.A, 0, ⟨[], false, []⟩⟩
    = some ⟨.B, 1, ⟨[true], false, []⟩⟩ := rfl
example : steps 1 ⟨.A, 0, ⟨[], false, [] ++ [false]⟩⟩
    = some ⟨.B, 1, ⟨[true], false, []⟩⟩ := rfl                    -- absorbed

-- The weapon derives the padded run FROM the trimmed run; here the LEFT disjunct
-- (absorbed) is the true one.
example :
    steps 1 ⟨.A, 0, ⟨[], false, [] ++ [false]⟩⟩ = some ⟨.B, 1, ⟨[true], false, []⟩⟩ ∨
    steps 1 ⟨.A, 0, ⟨[], false, [] ++ [false]⟩⟩
      = some ⟨.B, 1, ⟨[true], false, [] ++ [false]⟩⟩ :=
  steps_rpad 1 .A 0 [] false [] rfl

-- (b) Non-absorption, RIGHT: the head lands before consuming the pad, so the
--     trailing blank rides along (RIGHT disjunct).
example : steps 2 ⟨.E, 0, ⟨[], false, [true, false]⟩⟩
    = some ⟨.E, 2, ⟨[true, true], false, []⟩⟩ := rfl
example : steps 2 ⟨.E, 0, ⟨[], false, [true, false] ++ [false]⟩⟩
    = some ⟨.E, 2, ⟨[true, true], false, [] ++ [false]⟩⟩ := rfl   -- rides along
example :
    steps 2 ⟨.E, 0, ⟨[], false, [true, false] ++ [false]⟩⟩
      = some ⟨.E, 2, ⟨[true, true], false, []⟩⟩ ∨
    steps 2 ⟨.E, 0, ⟨[], false, [true, false] ++ [false]⟩⟩
      = some ⟨.E, 2, ⟨[true, true], false, [] ++ [false]⟩⟩ :=
  steps_rpad 2 .E 0 [] false [true, false] rfl

-- (c) Absorption boundary, LEFT: from state C, one step, the head runs left off
--     the end.  Trimmed and one-far-blank-padded land the SAME config.
example : steps 1 ⟨.C, 0, ⟨[], false, []⟩⟩
    = some ⟨.D, -1, ⟨[], false, [false]⟩⟩ := rfl
example : steps 1 ⟨.C, 0, ⟨[] ++ [false], false, []⟩⟩
    = some ⟨.D, -1, ⟨[], false, [false]⟩⟩ := rfl                  -- absorbed

-- (d) ITERATED: a whole block `zeros 3` of trailing blanks on `init`'s run —
--     all absorbed (j = 0), reconciled by `steps_rpad_zeros`.
example : ∃ j : Nat, j ≤ 3 ∧
    steps 1 ⟨.A, 0, ⟨[], false, [] ++ zeros 3⟩⟩
      = some ⟨.B, 1, ⟨[true], false, [] ++ zeros j⟩⟩ :=
  steps_rpad_zeros 1 .A 0 [] false [] rfl 3

#print axioms steps_rpad
#print axioms steps_lpad
#print axioms steps_rpad_zeros
#print axioms steps_lpad_zeros

end X2
