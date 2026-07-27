import TapeCalc

/-!
# Right-extension transport — the lemma the seam induction needs

`TapeCalc` can pad a right context with **zeros** (`steps_rpad_dich`, `steps_rpad_zeros`,
`steps_rpad_zeros_absorb`; the underlying `rtail` relation is literally
`t2.right = t1.right ∨ t2.right = t1.right ++ [false]`).  What `D`'s epoch argument needs is the
**arbitrary** extension: a run that stays inside a known right prefix behaves the same however
that prefix is continued.

That is not a convenience.  The measured structure of `D`'s epoch is that the run from `M1(j)` is
a function of the cascade word's *prefix* — two epochs of the same parity are step-for-step
identical until the head first reaches a cell where their words differ — so every piece of the
seam induction has the form "this run is prefix-local, hence tail-uniform".

Proving such a run directly with a symbolic tail is not an option: measured, a 2000-step `rfl`
with a free `X : List Bool` in the right context does not finish in ten minutes (and with a
symbolic `p` the kernel additionally accumulates one `± 1` per step in the position, so a
13000-step run would build a 13000-term `Int`).  The working route is: run it on a **concrete**
tape, transport with `steps_rext` below, and move the position with `TapeCalc.steps_pos_shift`.

## The frontier condition

`F c := c.tape.right.length + c.pos` is the position just past the end of the represented right
list.  `TapeCalc.step_right_mono` shows `F` never decreases, and inspecting `mvR`/`mvL` shows it
increases *exactly* when the head steps right off the end of the list.  So `F c' = F c` says
precisely "the run never left the given right context", which is the hypothesis below.

Zero-Mathlib, core only.  No `sorry`, and **no `Classical.choice`** — which needed care: running
the branch tactics inside a `cases R` whose motive mentions the frontier hypothesis pulls
`Classical.choice` in, while delegating each branch to its own lemma does not.  Hence the three
auxiliary lemmas.
-/

namespace TapeCalc

/-- Left move: the extension is inert. -/
theorem step_rext_L {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (s : S) (p : Int) (L : List Bool) (hd : Bool) (R Y : List Bool) (b : Bool) (s' : S)
    (hT : T s hd = some (b, .L, s'))
    {s1 : S} {p1 : Int} {L1 : List Bool} {hd1 : Bool} {R1 : List Bool}
    (h : step T ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s1, p1, ⟨L1, hd1, R1⟩⟩) :
    step T ⟨s, p, ⟨L, hd, R ++ Y⟩⟩ = some ⟨s1, p1, ⟨L1, hd1, R1 ++ Y⟩⟩ := by
  simp only [step, hT] at h ⊢
  cases L with
  | nil =>
    simp only [wr, mvL] at h ⊢
    injection h with e
    injection e with e1 e2 e3
    injection e3 with f1 f2 f3
    subst e1; subst e2; subst f1; subst f2; subst f3
    rfl
  | cons x L' =>
    simp only [wr, mvL] at h ⊢
    injection h with e
    injection e with e1 e2 e3
    injection e3 with f1 f2 f3
    subst e1; subst e2; subst f1; subst f2; subst f3
    rfl

/-- Right move with a non-empty right list: the head stays inside `R`, so the extension rides
along untouched. -/
theorem step_rext_Rcons {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (s : S) (p : Int) (L : List Bool) (hd : Bool) (r : Bool) (R' Y : List Bool)
    (b : Bool) (s' : S) (hT : T s hd = some (b, .R, s'))
    {s1 : S} {p1 : Int} {L1 : List Bool} {hd1 : Bool} {R1 : List Bool}
    (h : step T ⟨s, p, ⟨L, hd, r :: R'⟩⟩ = some ⟨s1, p1, ⟨L1, hd1, R1⟩⟩) :
    step T ⟨s, p, ⟨L, hd, (r :: R') ++ Y⟩⟩ = some ⟨s1, p1, ⟨L1, hd1, R1 ++ Y⟩⟩ := by
  simp only [step, hT, wr, mvR] at h ⊢
  injection h with e
  injection e with e1 e2 e3
  injection e3 with f1 f2 f3
  subst e1; subst e2; subst f1; subst f2; subst f3
  rfl

/-- Right move off the end of the right list: this is exactly the case the frontier hypothesis
excludes, since `F` strictly increases here. -/
theorem step_rext_Rnil {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (s : S) (p : Int) (L : List Bool) (hd : Bool) (b : Bool) (s' : S)
    (hT : T s hd = some (b, .R, s'))
    {s1 : S} {p1 : Int} {L1 : List Bool} {hd1 : Bool} {R1 : List Bool}
    (h : step T ⟨s, p, ⟨L, hd, []⟩⟩ = some ⟨s1, p1, ⟨L1, hd1, R1⟩⟩)
    (hf : (R1.length : Int) + p1 = (([] : List Bool).length : Int) + p) : False := by
  simp only [step, hT, wr, mvR] at h
  injection h with e
  injection e with e1 e2 e3
  injection e3 with f1 f2 f3
  subst e2; subst f3
  simp only [List.length_nil] at hf
  omega

/-- One step, transported across an arbitrary right extension, given that the step did not
advance the right frontier. -/
theorem step_rext {S : Type} (T : S → Bool → Option (Bool × Dir × S))
    (s : S) (p : Int) (L : List Bool) (hd : Bool) (R Y : List Bool)
    {s1 : S} {p1 : Int} {L1 : List Bool} {hd1 : Bool} {R1 : List Bool}
    (h : step T ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s1, p1, ⟨L1, hd1, R1⟩⟩)
    (hf : (R1.length : Int) + p1 = (R.length : Int) + p) :
    step T ⟨s, p, ⟨L, hd, R ++ Y⟩⟩ = some ⟨s1, p1, ⟨L1, hd1, R1 ++ Y⟩⟩ := by
  cases hT : T s hd with
  | none => simp only [step, hT] at h; exact absurd h (by simp)
  | some v =>
    rcases v with ⟨b, dir, s'⟩
    cases dir with
    | L => exact step_rext_L T s p L hd R Y b s' hT h
    | R =>
      cases R with
      | nil => exact absurd h (fun hh => step_rext_Rnil T s p L hd b s' hT hh hf)
      | cons r R' => exact step_rext_Rcons T s p L hd r R' Y b s' hT h

/-- **Right-extension transport.**  A run whose right frontier never advances — i.e. which never
reads past the given right context — behaves identically when that context is extended by an
arbitrary `Y`, and carries `Y` along untouched. -/
theorem steps_rext {S : Type} (T : S → Bool → Option (Bool × Dir × S)) :
    ∀ (n : Nat) (s : S) (p : Int) (L : List Bool) (hd : Bool) (R Y : List Bool)
      {s' : S} {p' : Int} {L' : List Bool} {hd' : Bool} {R' : List Bool},
    steps T n ⟨s, p, ⟨L, hd, R⟩⟩ = some ⟨s', p', ⟨L', hd', R'⟩⟩ →
    (R'.length : Int) + p' = (R.length : Int) + p →
    steps T n ⟨s, p, ⟨L, hd, R ++ Y⟩⟩ = some ⟨s', p', ⟨L', hd', R' ++ Y⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro s p L hd R Y s' p' L' hd' R' hrun _
    injection hrun with e
    injection e with e1 e2 e3
    injection e3 with f1 f2 f3
    subst e1; subst e2; subst f1; subst f2; subst f3
    rfl
  | succ n ih =>
    intro s p L hd R Y s' p' L' hd' R' hrun hf
    have hru : ((step T ⟨s, p, ⟨L, hd, R⟩⟩).bind (steps T n)) = some ⟨s', p', ⟨L', hd', R'⟩⟩ := hrun
    cases hc : step T (⟨s, p, ⟨L, hd, R⟩⟩ : Cfg S) with
    | none => rw [hc] at hru; simp at hru
    | some d =>
      rw [hc] at hru
      have hd2 : steps T n d = some ⟨s', p', ⟨L', hd', R'⟩⟩ := hru
      rcases d with ⟨s1, p1, ⟨L1, hd1, R1⟩⟩
      -- the frontier is squeezed: it never decreases and ends where it started
      have m1 := step_right_mono T _ _ hc
      have m2 := steps_right_mono T n _ _ hd2
      simp only at m1 m2
      have hf1 : (R1.length : Int) + p1 = (R.length : Int) + p := by omega
      have hf2 : (R'.length : Int) + p' = (R1.length : Int) + p1 := by omega
      show ((step T ⟨s, p, ⟨L, hd, R ++ Y⟩⟩).bind (steps T n)) = _
      rw [step_rext T s p L hd R Y hc hf1]
      exact ih s1 p1 L1 hd1 R1 Y hd2 hf2

#print axioms step_rext
#print axioms steps_rext

end TapeCalc
