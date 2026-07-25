/-!
# TapeCalc — the machine-INDEPENDENT tape calculus

Everything in the `x2` closure that does not mention `x2`, restated for an ARBITRARY transition
table.  `x2`'s own (audited) development is untouched; this file is what a NEW machine imports.

Contents
* `step` / `steps` over a table `T : S → Bool → Option (Bool × Dir × S)`
* `steps_add`, `steps_pos_shift`, `steps_left_mono`, `steps_right_mono`, `steps_prefix_ne_none`
* the four boundary congruences: `steps_{l,r}pad_zeros` (forward) and `steps_{l,r}unpad_zeros`
  (reverse)
* the EXACT congruences: `steps_rpad_dich` / `steps_rpad_zeros_absorb` and their left twins
* `nonhalt_of_invariant`
-/

namespace TapeCalc

inductive Dir | L | R
deriving DecidableEq

structure Tape where
  left : List Bool
  head : Bool
  right : List Bool
deriving DecidableEq

structure Cfg (S : Type) where
  st : S
  pos : Int
  tape : Tape

def zeros : Nat → List Bool
  | 0 => []
  | n + 1 => false :: zeros n

theorem zeros_length : ∀ n, (zeros n).length = n := by
  intro n; induction n with
  | zero => rfl
  | succ n ih => show (zeros n).length + 1 = n + 1; rw [ih]

theorem zeros_add : ∀ a b : Nat, zeros (a + b) = zeros a ++ zeros b := by
  intro a
  induction a with
  | zero => intro b; rw [Nat.zero_add]; rfl
  | succ a ih =>
    intro b
    rw [show a + 1 + b = (a + b) + 1 from by omega]
    show false :: zeros (a + b) = false :: (zeros a ++ zeros b)
    rw [ih]

theorem zeros_snoc : ∀ k : Nat, zeros k ++ [false] = zeros (k + 1) := by
  intro k; induction k with
  | zero => rfl
  | succ k ih => show false :: (zeros k ++ [false]) = false :: zeros (k + 1); rw [ih]

def wr (t : Tape) (b : Bool) : Tape := ⟨t.left, b, t.right⟩

def mvR : Tape → Tape
  | ⟨l, h, []⟩ => ⟨h :: l, false, []⟩
  | ⟨l, h, b :: r⟩ => ⟨h :: l, b, r⟩

def mvL : Tape → Tape
  | ⟨[], h, r⟩ => ⟨[], false, h :: r⟩
  | ⟨b :: l, h, r⟩ => ⟨l, b, h :: r⟩

/-- one step of the machine given by `T`; `none` = HALT -/
def step {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (c : Cfg S) : Option (Cfg S) :=
  match T c.st c.tape.head with
  | none => none
  | some (b, .R, s') => some ⟨s', c.pos + 1, mvR (wr c.tape b)⟩
  | some (b, .L, s') => some ⟨s', c.pos - 1, mvL (wr c.tape b)⟩

def steps {S : Type} (T : S → Bool → Option (Bool × Dir × S)) : Nat → Cfg S → Option (Cfg S)
  | 0, c => some c
  | n + 1, c => (step T c).bind (steps T n)

theorem someBind {α β : Type} (a : α) (f : α → Option β) : (some a).bind f = f a := rfl

theorem steps_add {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (a b : Nat) (c : Cfg S), steps T (a + b) c = (steps T a c).bind (steps T b) := by
  intro a
  induction a with
  | zero => intro b c; rw [Nat.zero_add]; rfl
  | succ a ih =>
    intro b c
    rw [show a + 1 + b = (a + b) + 1 from by omega]
    show (step T c).bind (steps T (a + b)) = ((step T c).bind (steps T a)).bind (steps T b)
    cases step T c with
    | none => rfl
    | some d => show steps T (a + b) d = (steps T a d).bind (steps T b); exact ih b d

theorem steps_prefix_ne_none {S : Type} {T : S → Bool → Option (Bool × Dir × S)}
    {N k : Nat} {c c' : Cfg S} (h : steps T N c = some c') (hk : k ≤ N) :
    steps T k c ≠ none := by
  intro hnone
  have hz : steps T N c = none := by
    rw [show N = k + (N - k) from by omega, steps_add, hnone]; rfl
  rw [hz] at h; exact absurd h (by simp)

#print axioms steps_add
#print axioms steps_prefix_ne_none

/-! ## Translation and the two monotonicities -/

def shiftPos {S : Type} (d : Int) (c : Cfg S) : Cfg S := ⟨c.st, c.pos + d, c.tape⟩

theorem step_shiftPos {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (d : Int) (c : Cfg S) :
    step T (shiftPos d c) = (step T c).map (shiftPos d) := by
  cases hT : T c.st c.tape.head with
  | none => simp [step, shiftPos, hT]
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir <;>
      · simp only [step, shiftPos, hT, Option.map_some]
        refine congrArg some ?_
        congr 1
        omega

theorem steps_shiftPos {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (d : Int) :
    ∀ (n : Nat) (c : Cfg S), steps T n (shiftPos d c) = (steps T n c).map (shiftPos d) := by
  intro n
  induction n with
  | zero => intro c; rfl
  | succ n ih =>
    intro c
    show (step T (shiftPos d c)).bind (steps T n) = ((step T c).bind (steps T n)).map (shiftPos d)
    rw [step_shiftPos]
    cases step T c with
    | none => rfl
    | some e => show steps T n (shiftPos d e) = _; exact ih e

theorem steps_pos_shift {S : Type} {T : S → Bool → Option (Bool × Dir × S)}
    {n : Nat} {st st' : S} {p p' d : Int} {t t' : Tape}
    (h : steps T n ⟨st, p, t⟩ = some ⟨st', p', t'⟩) :
    steps T n ⟨st, p + d, t⟩ = some ⟨st', p' + d, t'⟩ := by
  have hs := steps_shiftPos T d n ⟨st, p, t⟩
  rw [h] at hs
  exact hs

#print axioms step_shiftPos
#print axioms steps_pos_shift

theorem step_left_mono {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (c d : Cfg S)
    (h : step T c = some d) :
    (c.tape.left.length : Int) - c.pos ≤ (d.tape.left.length : Int) - d.pos := by
  rcases c with ⟨s, p, ⟨l, hd, r⟩⟩
  cases hT : T s hd with
  | none => simp only [step, hT] at h; exact absurd h (by simp)
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir <;>
      · simp only [step, hT] at h
        injection h with h3
        subst h3
        cases l <;> cases r <;>
          simp only [mvL, mvR, wr, List.length_cons, List.length_nil] <;> push_cast <;> omega

theorem step_right_mono {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (c d : Cfg S)
    (h : step T c = some d) :
    (c.tape.right.length : Int) + c.pos ≤ (d.tape.right.length : Int) + d.pos := by
  rcases c with ⟨s, p, ⟨l, hd, r⟩⟩
  cases hT : T s hd with
  | none => simp only [step, hT] at h; exact absurd h (by simp)
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir <;>
      · simp only [step, hT] at h
        injection h with h3
        subst h3
        cases l <;> cases r <;>
          simp only [mvL, mvR, wr, List.length_cons, List.length_nil] <;> push_cast <;> omega

theorem steps_left_mono {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (n : Nat) (c c' : Cfg S), steps T n c = some c' →
    (c.tape.left.length : Int) - c.pos ≤ (c'.tape.left.length : Int) - c'.pos := by
  intro n
  induction n with
  | zero => intro c c' h; injection h with h; subst h; omega
  | succ n ih =>
    intro c c' h
    have h : ((step T c).bind (steps T n)) = some c' := h
    cases hc : step T c with
    | none => rw [hc] at h; simp at h
    | some d =>
      rw [hc] at h
      have h1 := step_left_mono T c d hc
      have h2 := ih d c' h
      omega

theorem steps_right_mono {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (n : Nat) (c c' : Cfg S), steps T n c = some c' →
    (c.tape.right.length : Int) + c.pos ≤ (c'.tape.right.length : Int) + c'.pos := by
  intro n
  induction n with
  | zero => intro c c' h; injection h with h; subst h; omega
  | succ n ih =>
    intro c c' h
    have h : ((step T c).bind (steps T n)) = some c' := h
    cases hc : step T c with
    | none => rw [hc] at h; simp at h
    | some d =>
      rw [hc] at h
      have h1 := step_right_mono T c d hc
      have h2 := ih d c' h
      omega

#print axioms steps_left_mono
#print axioms steps_right_mono

/-! ## The right boundary: forward, reverse, and exact congruences -/

abbrev rtail (t1 t2 : Tape) : Prop :=
  t2.left = t1.left ∧ t2.head = t1.head ∧
    (t2.right = t1.right ∨ t2.right = t1.right ++ [false])

abbrev crtail {S : Type} (c1 c2 : Cfg S) : Prop :=
  c2.st = c1.st ∧ c2.pos = c1.pos ∧ rtail c1.tape c2.tape

theorem rtail_mvR (l : List Bool) (hd : Bool) (r1 r2 : List Bool)
    (hr : r2 = r1 ∨ r2 = r1 ++ [false]) : rtail (mvR ⟨l, hd, r1⟩) (mvR ⟨l, hd, r2⟩) := by
  rcases hr with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h
    cases r1 with
    | nil => exact ⟨rfl, rfl, Or.inl rfl⟩
    | cons x r => exact ⟨rfl, rfl, Or.inr rfl⟩

theorem rtail_mvL (l : List Bool) (hd : Bool) (r1 r2 : List Bool)
    (hr : r2 = r1 ∨ r2 = r1 ++ [false]) : rtail (mvL ⟨l, hd, r1⟩) (mvL ⟨l, hd, r2⟩) := by
  rcases hr with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h; cases l <;> exact ⟨rfl, rfl, Or.inr rfl⟩

theorem step_crtail {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (c1 c2 : Cfg S)
    (h : crtail c1 c2) :
    (step T c1 = none ∧ step T c2 = none) ∨
    (∃ d1 d2, step T c1 = some d1 ∧ step T c2 = some d2 ∧ crtail d1 d2) := by
  rcases c1 with ⟨s1, p1, ⟨l1, hd1, r1⟩⟩
  rcases c2 with ⟨s2, p2, ⟨l2, hd2, r2⟩⟩
  obtain ⟨hst, hpos, hll, hhh, hr⟩ := h
  dsimp only at hst hpos hll hhh hr
  subst hst; subst hpos; subst hll; subst hhh
  cases hT : T s2 hd2 with
  | none => left; exact ⟨by simp [step, hT], by simp [step, hT]⟩
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir
    · right
      refine ⟨⟨s', p2 - 1, mvL ⟨l2, b, r1⟩⟩, ⟨s', p2 - 1, mvL ⟨l2, b, r2⟩⟩, ?_, ?_,
        ⟨rfl, rfl, rtail_mvL l2 b r1 r2 hr⟩⟩ <;> simp [step, hT, wr]
    · right
      refine ⟨⟨s', p2 + 1, mvR ⟨l2, b, r1⟩⟩, ⟨s', p2 + 1, mvR ⟨l2, b, r2⟩⟩, ?_, ?_,
        ⟨rfl, rfl, rtail_mvR l2 b r1 r2 hr⟩⟩ <;> simp [step, hT, wr]

theorem steps_crtail {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (n : Nat) (c1 c2 : Cfg S), crtail c1 c2 →
    (steps T n c1 = none ∧ steps T n c2 = none) ∨
    (∃ d1 d2, steps T n c1 = some d1 ∧ steps T n c2 = some d2 ∧ crtail d1 d2) := by
  intro n
  induction n with
  | zero => intro c1 c2 h; right; exact ⟨c1, c2, rfl, rfl, h⟩
  | succ n ih =>
    intro c1 c2 h
    rcases step_crtail T c1 c2 h with ⟨h1, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · left
      exact ⟨by show (step T c1).bind (steps T n) = none; rw [h1]; rfl,
             by show (step T c2).bind (steps T n) = none; rw [h2]; rfl⟩
    · have e1 : steps T (n + 1) c1 = steps T n d1 := by
        show (step T c1).bind (steps T n) = steps T n d1; rw [hd1]; rfl
      have e2 : steps T (n + 1) c2 = steps T n d2 := by
        show (step T c2).bind (steps T n) = steps T n d2; rw [hd2]; rfl
      rw [e1, e2]; exact ih d1 d2 hdr

#print axioms step_crtail
#print axioms steps_crtail

theorem steps_rpad {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool}
    (hrun : steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    steps T n ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ ∨
    steps T n ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = some ⟨s', p', ⟨L', hd', R' ++ [false]⟩⟩ := by
  have hc : crtail (⟨s, p, ⟨L, hd, R⟩⟩ : Cfg S) ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ :=
    ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
  rcases steps_crtail T n _ _ hc with ⟨h1, _⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
  · rw [hrun] at h1; simp at h1
  · have hd1' : d1 = ⟨s', p', ⟨L', hd', R'⟩⟩ := Option.some.inj (hd1.symm.trans hrun)
    subst hd1'
    rcases d2 with ⟨s2, p2, ⟨l2, h2, r2⟩⟩
    obtain ⟨hst, hpos, hll, hhh, hrr⟩ := hdr
    dsimp only at hst hpos hll hhh hrr
    subst hst; subst hpos; subst hll; subst hhh
    rcases hrr with h | h
    · left; subst h; exact hd2
    · right; subst h; exact hd2

theorem steps_rpad_zeros {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool}
    (hrun : steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    ∀ k : Nat, ∃ j : Nat, j ≤ k ∧
      steps T n ⟨s, p, ⟨L, hd, R ++ zeros k⟩⟩ = some ⟨s', p', ⟨L', hd', R' ++ zeros j⟩⟩ := by
  intro k
  induction k with
  | zero =>
    refine ⟨0, Nat.le_refl 0, ?_⟩
    show steps T n ⟨s, p, ⟨L, hd, R ++ []⟩⟩ = some ⟨s', p', ⟨L', hd', R' ++ []⟩⟩
    rw [List.append_nil, List.append_nil]; exact hrun
  | succ k ih =>
    obtain ⟨j, hjk, hj⟩ := ih
    have hpad : R ++ zeros (k + 1) = (R ++ zeros k) ++ [false] := by
      rw [← zeros_snoc, List.append_assoc]
    rw [hpad]
    rcases steps_rpad T n s p L hd (R ++ zeros k) hj with h | h
    · exact ⟨j, Nat.le_succ_of_le hjk, h⟩
    · refine ⟨j + 1, Nat.succ_le_succ hjk, ?_⟩
      rwa [List.append_assoc R' (zeros j) [false], zeros_snoc] at h

/-- **reverse**: a run proven on the PADDED tape yields the run on the trimmed one -/
theorem steps_runpad_zeros {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (k n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R'' : List Bool},
    steps T n ⟨s, p, ⟨L, hd, R ++ zeros k⟩⟩ = some ⟨s', p', ⟨L', hd', R''⟩⟩ →
    ∃ (R' : List Bool) (i : Nat), i ≤ k ∧ R'' = R' ++ zeros i ∧
      steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro n s p L hd R s' p' L' hd' R'' hrun
    refine ⟨R'', 0, Nat.le_refl 0, by rw [show (zeros 0 : List Bool) = [] from rfl,
      List.append_nil], ?_⟩
    rwa [show (zeros 0 : List Bool) = [] from rfl, List.append_nil] at hrun
  | succ k ih =>
    intro n s p L hd R s' p' L' hd' R'' hrun
    rw [show R ++ zeros (k + 1) = (R ++ zeros k) ++ [false] from by
          rw [← zeros_snoc, List.append_assoc]] at hrun
    have hc : crtail (⟨s, p, ⟨L, hd, R ++ zeros k⟩⟩ : Cfg S)
        ⟨s, p, ⟨L, hd, (R ++ zeros k) ++ [false]⟩⟩ := ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
    rcases steps_crtail T n _ _ hc with ⟨_, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · rw [hrun] at h2; simp at h2
    · have hd2' : d2 = ⟨s', p', ⟨L', hd', R''⟩⟩ := Option.some.inj (hd2.symm.trans hrun)
      subst hd2'
      rcases d1 with ⟨s1, p1, ⟨l1, h1, r1⟩⟩
      obtain ⟨hst, hpos, hll, hhh, hrr⟩ := hdr
      dsimp only at hst hpos hll hhh hrr
      subst hst; subst hpos; subst hll; subst hhh
      obtain ⟨R', i, hik, hRi, hrun'⟩ := ih n s p L hd R hd1
      rcases hrr with h | h
      · exact ⟨R', i, Nat.le_succ_of_le hik, by rw [← h] at hRi; exact hRi, hrun'⟩
      · exact ⟨R', i + 1, Nat.succ_le_succ hik,
          by rw [h, hRi, List.append_assoc, zeros_snoc], hrun'⟩

#print axioms steps_rpad_zeros
#print axioms steps_runpad_zeros

/-! ## The EXACT right congruence — pad absorbed ⟺ right frontier advanced -/

theorem rpadR (L : List Bool) (b : Bool) (R : List Bool) (p : Int) :
    ( mvR ⟨L, b, R ++ [false]⟩
        = ⟨(mvR ⟨L, b, R⟩).left, (mvR ⟨L, b, R⟩).head, (mvR ⟨L, b, R⟩).right ++ [false]⟩
      ∧ (((mvR ⟨L, b, R⟩).right.length : Int) + (p + 1) = (R.length : Int) + p) )
    ∨ mvR ⟨L, b, R ++ [false]⟩ = mvR ⟨L, b, R⟩ := by
  cases R with
  | nil => exact Or.inr rfl
  | cons x r =>
    refine Or.inl ⟨rfl, ?_⟩
    show ((r.length : Int)) + (p + 1) = (((x :: r).length : Int)) + p
    simp only [List.length_cons]; push_cast; omega

theorem rpadL (L : List Bool) (b : Bool) (R : List Bool) (p : Int) :
    mvL ⟨L, b, R ++ [false]⟩
        = ⟨(mvL ⟨L, b, R⟩).left, (mvL ⟨L, b, R⟩).head, (mvL ⟨L, b, R⟩).right ++ [false]⟩
      ∧ (((mvL ⟨L, b, R⟩).right.length : Int) + (p - 1) = (R.length : Int) + p) := by
  cases L with
  | nil =>
    refine ⟨rfl, ?_⟩
    show (((b :: R).length : Int)) + (p - 1) = ((R.length : Int)) + p
    simp only [List.length_cons]; push_cast; omega
  | cons y l =>
    refine ⟨rfl, ?_⟩
    show (((b :: R).length : Int)) + (p - 1) = ((R.length : Int)) + p
    simp only [List.length_cons]; push_cast; omega

theorem step_rpad_dich {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool) :
    (step T ⟨s, p, ⟨L, hd, R⟩⟩ = none ∧ step T ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = none) ∨
    (∃ (s' : S) (p' : Int) (t : Tape),
        step T ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', t⟩ ∧
        ( (step T ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩
              = some ⟨s', p', ⟨t.left, t.head, t.right ++ [false]⟩⟩
             ∧ ((t.right.length : Int) + p' = (R.length : Int) + p))
        ∨ step T ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = some ⟨s', p', t⟩ )) := by
  cases hT : T s hd with
  | none => left; exact ⟨by simp [step, hT], by simp [step, hT]⟩
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir
    · obtain ⟨h1, h2⟩ := rpadL L b R p
      refine Or.inr ⟨s', p - 1, mvL ⟨L, b, R⟩, by simp [step, hT, wr], Or.inl ⟨?_, h2⟩⟩
      simp only [step, hT, wr]
      rw [h1]
    · rcases rpadR L b R p with ⟨h1, h2⟩ | h1
      · refine Or.inr ⟨s', p + 1, mvR ⟨L, b, R⟩, by simp [step, hT, wr], Or.inl ⟨?_, h2⟩⟩
        simp only [step, hT, wr]
        rw [h1]
      · refine Or.inr ⟨s', p + 1, mvR ⟨L, b, R⟩, by simp [step, hT, wr], Or.inr ?_⟩
        simp only [step, hT, wr]
        rw [h1]

#print axioms step_rpad_dich

theorem steps_rpad_dich {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool},
    steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ →
    (steps T n ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = some ⟨s', p', ⟨L', hd', R' ++ [false]⟩⟩
       ∧ ((R'.length : Int) + p' = (R.length : Int) + p))
    ∨ steps T n ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro s p L hd R s' p' L' hd' R' hrun
    have e : (⟨s, p, ⟨L, hd, R⟩⟩ : Cfg S) = ⟨s', p', ⟨L', hd', R'⟩⟩ := Option.some.inj hrun
    injection e with e1 e2 e3
    subst e1; subst e2
    injection e3 with f1 f2 f3
    subst f1; subst f2; subst f3
    exact Or.inl ⟨rfl, rfl⟩
  | succ n ih =>
    intro s p L hd R s' p' L' hd' R' hrun
    have hru : ((step T ⟨s, p, ⟨L, hd, R⟩⟩).bind (steps T n)) = some ⟨s', p', ⟨L', hd', R'⟩⟩ := hrun
    rcases step_rpad_dich T s p L hd R with ⟨hn, _⟩ | ⟨s1, p1, t, hst, hcase⟩
    · rw [hn] at hru; simp at hru
    · rw [hst] at hru
      have hru' : steps T n ⟨s1, p1, t⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := hru
      rcases t with ⟨tl, th, tr⟩
      rcases hcase with ⟨hpad, hfr⟩ | hpad
      · rcases ih s1 p1 tl th tr hru' with ⟨hp1, hf1⟩ | hp1
        · refine Or.inl ⟨?_, hf1.trans hfr⟩
          show ((step T ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩).bind (steps T n)) = _
          rw [hpad]; exact hp1
        · refine Or.inr ?_
          show ((step T ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩).bind (steps T n)) = _
          rw [hpad]; exact hp1
      · refine Or.inr ?_
        show ((step T ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩).bind (steps T n)) = _
        rw [hpad]; exact hru'

theorem steps_rpad_absorb {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool}
    (hrun : steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩)
    (hf : (R.length : Int) + p < (R'.length : Int) + p') :
    steps T n ⟨s, p, ⟨L, hd, R ++ [false]⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  rcases steps_rpad_dich T n s p L hd R hrun with ⟨_, he⟩ | h
  · exact absurd he (by omega)
  · exact h

theorem steps_rpad_zeros_absorb {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (k n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool},
    steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ →
    (R.length : Int) + p + (k : Int) ≤ (R'.length : Int) + p' →
    steps T n ⟨s, p, ⟨L, hd, R ++ zeros k⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro n s p L hd R s' p' L' hd' R' hrun _
    rwa [show (zeros 0 : List Bool) = [] from rfl, List.append_nil]
  | succ k ih =>
    intro n s p L hd R s' p' L' hd' R' hrun hf
    have hk : (R.length : Int) + p + (k : Int) ≤ (R'.length : Int) + p' := by omega
    have hstep := ih n s p L hd R hrun hk
    have hlen : ((R ++ zeros k).length : Int) + p < (R'.length : Int) + p' := by
      rw [List.length_append, zeros_length]; omega
    have habs := steps_rpad_absorb T n s p L hd (R ++ zeros k) hstep hlen
    rwa [List.append_assoc, zeros_snoc] at habs

/-- **Invariant non-halting** — no explicit milestone family and no choice. -/
theorem nonhalt_of_invariant_aux {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (P : Cfg S → Prop)
    (hstep : ∀ c, P c → ∃ n, 1 ≤ n ∧ ∃ c', P c' ∧ steps T n c = some c') :
    ∀ (B N : Nat), N ≤ B → ∀ c, P c → steps T N c ≠ none := by
  intro B
  induction B with
  | zero =>
    intro N hN c _
    rw [show N = 0 from by omega]
    intro h
    rw [show steps T 0 c = some c from rfl] at h
    exact absurd h (by simp)
  | succ B ih =>
    intro N hN c hc
    obtain ⟨n, hn1, c', hc', hrun⟩ := hstep c hc
    by_cases hle : N ≤ n
    · exact steps_prefix_ne_none hrun hle
    · rw [show N = n + (N - n) from by omega, steps_add, hrun]
      exact ih (N - n) (by omega) c' hc'

theorem nonhalt_of_invariant {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (P : Cfg S → Prop)
    (hstep : ∀ c, P c → ∃ n, 1 ≤ n ∧ ∃ c', P c' ∧ steps T n c = some c')
    (c : Cfg S) (hc : P c) : ∀ N : Nat, steps T N c ≠ none :=
  fun N => nonhalt_of_invariant_aux T P hstep N N (Nat.le_refl N) c hc

#print axioms steps_rpad_dich
#print axioms steps_rpad_zeros_absorb
#print axioms nonhalt_of_invariant

/-! ## The left boundary (mirror) -/

abbrev ltail (t1 t2 : Tape) : Prop :=
  t2.head = t1.head ∧ t2.right = t1.right ∧
    (t2.left = t1.left ∨ t2.left = t1.left ++ [false])

abbrev cltail {S : Type} (c1 c2 : Cfg S) : Prop :=
  c2.st = c1.st ∧ c2.pos = c1.pos ∧ ltail c1.tape c2.tape

theorem ltail_mvL (l1 l2 : List Bool) (hd : Bool) (r : List Bool)
    (hl : l2 = l1 ∨ l2 = l1 ++ [false]) : ltail (mvL ⟨l1, hd, r⟩) (mvL ⟨l2, hd, r⟩) := by
  rcases hl with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h
    cases l1 with
    | nil => exact ⟨rfl, rfl, Or.inl rfl⟩
    | cons x l => exact ⟨rfl, rfl, Or.inr rfl⟩

theorem ltail_mvR (l1 l2 : List Bool) (hd : Bool) (r : List Bool)
    (hl : l2 = l1 ∨ l2 = l1 ++ [false]) : ltail (mvR ⟨l1, hd, r⟩) (mvR ⟨l2, hd, r⟩) := by
  rcases hl with h | h
  · subst h; exact ⟨rfl, rfl, Or.inl rfl⟩
  · subst h; cases r <;> exact ⟨rfl, rfl, Or.inr rfl⟩

theorem step_cltail {S : Type} (T : S → Bool → Option (Bool × Dir × S)) (c1 c2 : Cfg S)
    (h : cltail c1 c2) :
    (step T c1 = none ∧ step T c2 = none) ∨
    (∃ d1 d2, step T c1 = some d1 ∧ step T c2 = some d2 ∧ cltail d1 d2) := by
  rcases c1 with ⟨s1, p1, ⟨l1, hd1, r1⟩⟩
  rcases c2 with ⟨s2, p2, ⟨l2, hd2, r2⟩⟩
  obtain ⟨hst, hpos, hhh, hrr, hl⟩ := h
  dsimp only at hst hpos hhh hrr hl
  subst hst; subst hpos; subst hhh; subst hrr
  cases hT : T s2 hd2 with
  | none => left; exact ⟨by simp [step, hT], by simp [step, hT]⟩
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir
    · right
      refine ⟨⟨s', p2 - 1, mvL ⟨l1, b, r2⟩⟩, ⟨s', p2 - 1, mvL ⟨l2, b, r2⟩⟩, ?_, ?_,
        ⟨rfl, rfl, ltail_mvL l1 l2 b r2 hl⟩⟩ <;> simp [step, hT, wr]
    · right
      refine ⟨⟨s', p2 + 1, mvR ⟨l1, b, r2⟩⟩, ⟨s', p2 + 1, mvR ⟨l2, b, r2⟩⟩, ?_, ?_,
        ⟨rfl, rfl, ltail_mvR l1 l2 b r2 hl⟩⟩ <;> simp [step, hT, wr]

theorem steps_cltail {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (n : Nat) (c1 c2 : Cfg S), cltail c1 c2 →
    (steps T n c1 = none ∧ steps T n c2 = none) ∨
    (∃ d1 d2, steps T n c1 = some d1 ∧ steps T n c2 = some d2 ∧ cltail d1 d2) := by
  intro n
  induction n with
  | zero => intro c1 c2 h; right; exact ⟨c1, c2, rfl, rfl, h⟩
  | succ n ih =>
    intro c1 c2 h
    rcases step_cltail T c1 c2 h with ⟨h1, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · left
      exact ⟨by show (step T c1).bind (steps T n) = none; rw [h1]; rfl,
             by show (step T c2).bind (steps T n) = none; rw [h2]; rfl⟩
    · have e1 : steps T (n + 1) c1 = steps T n d1 := by
        show (step T c1).bind (steps T n) = steps T n d1; rw [hd1]; rfl
      have e2 : steps T (n + 1) c2 = steps T n d2 := by
        show (step T c2).bind (steps T n) = steps T n d2; rw [hd2]; rfl
      rw [e1, e2]; exact ih d1 d2 hdr

theorem steps_lpad {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool}
    (hrun : steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    steps T n ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ ∨
    steps T n ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = some ⟨s', p', ⟨L' ++ [false], hd', R'⟩⟩ := by
  have hc : cltail (⟨s, p, ⟨L, hd, R⟩⟩ : Cfg S) ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ :=
    ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
  rcases steps_cltail T n _ _ hc with ⟨h1, _⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
  · rw [hrun] at h1; simp at h1
  · have hd1' : d1 = ⟨s', p', ⟨L', hd', R'⟩⟩ := Option.some.inj (hd1.symm.trans hrun)
    subst hd1'
    rcases d2 with ⟨s2, p2, ⟨l2, h2, r2⟩⟩
    obtain ⟨hst, hpos, hhh, hrr, hll⟩ := hdr
    dsimp only at hst hpos hhh hrr hll
    subst hst; subst hpos; subst hhh; subst hrr
    rcases hll with h | h
    · left; subst h; exact hd2
    · right; subst h; exact hd2

theorem steps_lpad_zeros {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool}
    (hrun : steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩) :
    ∀ k : Nat, ∃ j : Nat, j ≤ k ∧
      steps T n ⟨s, p, ⟨L ++ zeros k, hd, R⟩⟩ = some ⟨s', p', ⟨L' ++ zeros j, hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    refine ⟨0, Nat.le_refl 0, ?_⟩
    show steps T n ⟨s, p, ⟨L ++ [], hd, R⟩⟩ = some ⟨s', p', ⟨L' ++ [], hd', R'⟩⟩
    rw [List.append_nil, List.append_nil]; exact hrun
  | succ k ih =>
    obtain ⟨j, hjk, hj⟩ := ih
    have hpad : L ++ zeros (k + 1) = (L ++ zeros k) ++ [false] := by
      rw [← zeros_snoc, List.append_assoc]
    rw [hpad]
    rcases steps_lpad T n s p (L ++ zeros k) hd R hj with h | h
    · exact ⟨j, Nat.le_succ_of_le hjk, h⟩
    · refine ⟨j + 1, Nat.succ_le_succ hjk, ?_⟩
      rwa [List.append_assoc L' (zeros j) [false], zeros_snoc] at h

theorem steps_lunpad_zeros {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (k n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L'' : List Bool} {hd' : Bool} {R' : List Bool},
    steps T n ⟨s, p, ⟨L ++ zeros k, hd, R⟩⟩ = some ⟨s', p', ⟨L'', hd', R'⟩⟩ →
    ∃ (L' : List Bool) (i : Nat), i ≤ k ∧ L'' = L' ++ zeros i ∧
      steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro n s p L hd R s' p' L'' hd' R' hrun
    refine ⟨L'', 0, Nat.le_refl 0, by rw [show (zeros 0 : List Bool) = [] from rfl,
      List.append_nil], ?_⟩
    rwa [show (zeros 0 : List Bool) = [] from rfl, List.append_nil] at hrun
  | succ k ih =>
    intro n s p L hd R s' p' L'' hd' R' hrun
    have hpad : L ++ zeros (k + 1) = (L ++ zeros k) ++ [false] := by
      rw [← zeros_snoc, List.append_assoc]
    rw [hpad] at hrun
    have hc : cltail (⟨s, p, ⟨L ++ zeros k, hd, R⟩⟩ : Cfg S)
        ⟨s, p, ⟨(L ++ zeros k) ++ [false], hd, R⟩⟩ := ⟨rfl, rfl, rfl, rfl, Or.inr rfl⟩
    rcases steps_cltail T n _ _ hc with ⟨_, h2⟩ | ⟨d1, d2, hd1, hd2, hdr⟩
    · rw [hrun] at h2; simp at h2
    · have hd2' : d2 = ⟨s', p', ⟨L'', hd', R'⟩⟩ := Option.some.inj (hd2.symm.trans hrun)
      subst hd2'
      rcases d1 with ⟨s1, p1, ⟨l1, h1, r1⟩⟩
      obtain ⟨hst, hpos, hhh, hrr, hll⟩ := hdr
      dsimp only at hst hpos hhh hrr hll
      subst hst; subst hpos; subst hhh; subst hrr
      obtain ⟨L', i, hik, hLi, hrun'⟩ := ih n s p L hd R hd1
      rcases hll with h | h
      · exact ⟨L', i, Nat.le_succ_of_le hik, by rw [← h] at hLi; exact hLi, hrun'⟩
      · exact ⟨L', i + 1, Nat.succ_le_succ hik,
          by rw [h, hLi, List.append_assoc, zeros_snoc], hrun'⟩

#print axioms steps_lpad_zeros
#print axioms steps_lunpad_zeros

/-! ## The EXACT left congruence — pad absorbed ⟺ left frontier `|left| − pos` advanced -/

theorem lpadL (L : List Bool) (b : Bool) (R : List Bool) (p : Int) :
    ( mvL ⟨L ++ [false], b, R⟩
        = ⟨(mvL ⟨L, b, R⟩).left ++ [false], (mvL ⟨L, b, R⟩).head, (mvL ⟨L, b, R⟩).right⟩
      ∧ (((mvL ⟨L, b, R⟩).left.length : Int) - (p - 1) = (L.length : Int) - p) )
    ∨ mvL ⟨L ++ [false], b, R⟩ = mvL ⟨L, b, R⟩ := by
  cases L with
  | nil => exact Or.inr rfl
  | cons x l =>
    refine Or.inl ⟨rfl, ?_⟩
    show ((l.length : Int)) - (p - 1) = (((x :: l).length : Int)) - p
    simp only [List.length_cons]; push_cast; omega

theorem lpadR (L : List Bool) (b : Bool) (R : List Bool) (p : Int) :
    mvR ⟨L ++ [false], b, R⟩
        = ⟨(mvR ⟨L, b, R⟩).left ++ [false], (mvR ⟨L, b, R⟩).head, (mvR ⟨L, b, R⟩).right⟩
      ∧ (((mvR ⟨L, b, R⟩).left.length : Int) - (p + 1) = (L.length : Int) - p) := by
  cases R with
  | nil =>
    refine ⟨rfl, ?_⟩
    show (((b :: L).length : Int)) - (p + 1) = ((L.length : Int)) - p
    simp only [List.length_cons]; push_cast; omega
  | cons y r =>
    refine ⟨rfl, ?_⟩
    show (((b :: L).length : Int)) - (p + 1) = ((L.length : Int)) - p
    simp only [List.length_cons]; push_cast; omega

theorem step_lpad_dich {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool) :
    (step T ⟨s, p, ⟨L, hd, R⟩⟩ = none ∧ step T ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = none) ∨
    (∃ (s' : S) (p' : Int) (t : Tape),
        step T ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', t⟩ ∧
        ( (step T ⟨s, p, ⟨L ++ [false], hd, R⟩⟩
              = some ⟨s', p', ⟨t.left ++ [false], t.head, t.right⟩⟩
             ∧ ((t.left.length : Int) - p' = (L.length : Int) - p))
        ∨ step T ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = some ⟨s', p', t⟩ )) := by
  cases hT : T s hd with
  | none => left; exact ⟨by simp [step, hT], by simp [step, hT]⟩
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir
    · rcases lpadL L b R p with ⟨h1, h2⟩ | h1
      · refine Or.inr ⟨s', p - 1, mvL ⟨L, b, R⟩, by simp [step, hT, wr], Or.inl ⟨?_, h2⟩⟩
        simp only [step, hT, wr]; rw [h1]
      · refine Or.inr ⟨s', p - 1, mvL ⟨L, b, R⟩, by simp [step, hT, wr], Or.inr ?_⟩
        simp only [step, hT, wr]; rw [h1]
    · obtain ⟨h1, h2⟩ := lpadR L b R p
      refine Or.inr ⟨s', p + 1, mvR ⟨L, b, R⟩, by simp [step, hT, wr], Or.inl ⟨?_, h2⟩⟩
      simp only [step, hT, wr]; rw [h1]

theorem steps_lpad_dich {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool},
    steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ →
    (steps T n ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = some ⟨s', p', ⟨L' ++ [false], hd', R'⟩⟩
       ∧ ((L'.length : Int) - p' = (L.length : Int) - p))
    ∨ steps T n ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro s p L hd R s' p' L' hd' R' hrun
    have e : (⟨s, p, ⟨L, hd, R⟩⟩ : Cfg S) = ⟨s', p', ⟨L', hd', R'⟩⟩ := Option.some.inj hrun
    injection e with e1 e2 e3
    subst e1; subst e2
    injection e3 with f1 f2 f3
    subst f1; subst f2; subst f3
    exact Or.inl ⟨rfl, rfl⟩
  | succ n ih =>
    intro s p L hd R s' p' L' hd' R' hrun
    have hru : ((step T ⟨s, p, ⟨L, hd, R⟩⟩).bind (steps T n)) = some ⟨s', p', ⟨L', hd', R'⟩⟩ := hrun
    rcases step_lpad_dich T s p L hd R with ⟨hn, _⟩ | ⟨s1, p1, t, hst, hcase⟩
    · rw [hn] at hru; simp at hru
    · rw [hst] at hru
      have hru' : steps T n ⟨s1, p1, t⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := hru
      rcases t with ⟨tl, th, tr⟩
      rcases hcase with ⟨hpad, hfr⟩ | hpad
      · rcases ih s1 p1 tl th tr hru' with ⟨hp1, hf1⟩ | hp1
        · refine Or.inl ⟨?_, hf1.trans hfr⟩
          show ((step T ⟨s, p, ⟨L ++ [false], hd, R⟩⟩).bind (steps T n)) = _
          rw [hpad]; exact hp1
        · refine Or.inr ?_
          show ((step T ⟨s, p, ⟨L ++ [false], hd, R⟩⟩).bind (steps T n)) = _
          rw [hpad]; exact hp1
      · refine Or.inr ?_
        show ((step T ⟨s, p, ⟨L ++ [false], hd, R⟩⟩).bind (steps T n)) = _
        rw [hpad]; exact hru'

theorem steps_lpad_absorb {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool}
    (hrun : steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩)
    (hf : (L.length : Int) - p < (L'.length : Int) - p') :
    steps T n ⟨s, p, ⟨L ++ [false], hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  rcases steps_lpad_dich T n s p L hd R hrun with ⟨_, he⟩ | h
  · exact absurd he (by omega)
  · exact h

theorem steps_lpad_zeros_absorb {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (k n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R : List Bool)
    {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool},
    steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ →
    (L.length : Int) - p + (k : Int) ≤ (L'.length : Int) - p' →
    steps T n ⟨s, p, ⟨L ++ zeros k, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro n s p L hd R s' p' L' hd' R' hrun _
    rwa [show (zeros 0 : List Bool) = [] from rfl, List.append_nil]
  | succ k ih =>
    intro n s p L hd R s' p' L' hd' R' hrun hf
    have hk : (L.length : Int) - p + (k : Int) ≤ (L'.length : Int) - p' := by omega
    have hstep := ih n s p L hd R hrun hk
    have hlen : ((L ++ zeros k).length : Int) - p < (L'.length : Int) - p' := by
      rw [List.length_append, zeros_length]; omega
    have habs := steps_lpad_absorb T n s p (L ++ zeros k) hd R hstep hlen
    rwa [List.append_assoc, zeros_snoc] at habs

#print axioms steps_lpad_dich
#print axioms steps_lpad_zeros_absorb
