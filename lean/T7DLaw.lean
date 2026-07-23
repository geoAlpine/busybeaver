/-
**T7 / R1 — `DescLaw` ∀k.**  (2026-07-23, GREEN)

R1's last mile per `METHODS_2026-07-23.md`: the `descIn` arithmetic framing that
instantiates `T7Head.descLevel` at the `descIn` block sizes.  Two pure `List`
split lemmas (right = the cascade block, left = the settled comb) turn the rung
MECHANISM into the rung LAW `descIn k → descIn (k−1)` for all `k = n+6`.

Mathlib-free throughout: core `Nat` lemmas + `omega`, with `2^(n+4)` as the single
atom the power facts are linear in.
-/
import T7Head
open X2

-- DescLaw: descIn k -> descIn (k-1). Work with k = n+6. Set m = 2^{n+5}-3, and the phase-2 count.
-- RIGHT-side split lemma: descIn (n+6)'s right = descLevel's IN right, with
--   m = 2^{n+5}-3, m'+1 = 2^{n+4}-1, Y = ones(2^{n+5}-3) ++ 0 0 descCascade(n+3) ++ TAIL.
-- Uses: ones(a+b)=ones a++ones b, descCascade unfold.
theorem descIn_right_split (n : Nat) (TAIL : List Bool) :
    ones (2 ^ (n + 6) - 3) ++ (false :: false :: (descCascade (n + 6 - 2) ++ TAIL))
      = ones (2 * (2 ^ (n + 5) - 3)) ++
          (true :: true :: true :: false :: false :: true :: true ::
            (ones (2 * ((2 ^ (n + 4) - 1 - 1) + 1)) ++
              (ones (2 ^ (n + 5) - 3) ++ (false :: false :: (descCascade (n + 3) ++ TAIL))))) := by
  -- Mathlib-free power arithmetic: everything below is core `Nat` + `omega`,
  -- with `2^(n+4)` as the single atom the three facts are linear in.
  have e5 : (2:Nat)^(n+5) = 2 * 2^(n+4) := by rw [Nat.pow_succ]; exact Nat.mul_comm _ _
  have e2 : (2:Nat)^(n+6) = 4 * 2^(n+4) := by rw [Nat.pow_succ, e5]; omega
  -- the same power under the `descCascade`-unfolded spelling `n+3+3` (defeq to `n+6`)
  have e6 : (2:Nat)^(n+3+3) = 4 * 2^(n+4) := e2
  have h4 : 4 ≤ 2^(n+4) := by
    have h : (2:Nat)^2 ≤ 2^(n+4) := Nat.pow_le_pow_right (by omega) (by omega)
    omega
  -- block1: ones(2^{n+6}-3) = ones(2m) ++ ones 3
  rw [show 2^(n+6)-3 = 2*(2^(n+5)-3) + 3 from by omega, ones_add,
      show n+6-2 = (n+3)+1 from by omega, descCascade]
  -- descCascade top block: ones(2^{(n+3)+3}-3) = ones(2^{n+6}-3); split as 1 1 ones(2(m'+1)) ones(2^{n+5}-3)
  rw [show 2^((n+3)+3)-3 = 2 + (2*((2^(n+4)-1-1)+1) + (2^(n+5)-3)) from by omega,
      ones_add, ones_add]
  simp only [List.append_assoc, List.cons_append, ones]
  rfl

/-- **LEFT framing**: `descLevel`'s OUT left is `descIn (k−1)`'s left.  The settle's fresh `0 1`,
the phase-2 comb `(10)^a` and the crossing residue `1 0` reassemble into `(01)^{a+2}` followed by a
bounded marker.  Pure `List` identity (`false_pow10` + `pow01_add`). -/
theorem descIn_left_split (a m : Nat) (L : List Bool) :
    false :: true :: (false :: (pow10 a ++
        (true :: false :: false :: true :: false :: true :: (pow01 m ++ L))))
      = pow01 (a + 2) ++
          (false :: false :: true :: false :: true :: (pow01 m ++ L)) := by
  rw [show a + 2 = 1 + (a + 1) from by omega, pow01_add, pow01_add]
  show false :: true :: (false :: pow10 a ++ _) = _
  rw [false_pow10]
  simp only [List.append_assoc, List.cons_append, List.nil_append, pow01]

/-- **`DescLaw` — ONE DESCENT RUNG, `∀k`** (T7 head, 2026-07-23).  `descIn k → descIn (k−1)` in
`9·(2^{k−1}−1)` steps (here `k = n+6`), the machine content supplied by `descLevel` and the framing
by the two split lemmas above.  The marker `M` grows by a bounded prefix plus two combs. -/
theorem descLaw (n : Nat) (p : Int) (M TAIL : List Bool) :
    steps (9 * (2 ^ (n + 5) - 1)) (descIn (n + 6) p M TAIL)
      = some (descIn (n + 5)
          (p + 2 * ((2 ^ (n + 5) - 3 : Nat) : Int) + 8
             + 2 * (((2 ^ (n + 4) - 1 - 1 : Nat) : Int) + 1) - 1)
          (false :: false :: true :: false :: true ::
            (pow01 (2 ^ (n + 5) - 3) ++ (pow01 (2 ^ (n + 5)) ++ M)))
          TAIL) := by
  have e5 : (2:Nat)^(n+5) = 2 * 2^(n+4) := by rw [Nat.pow_succ]; exact Nat.mul_comm _ _
  have h4 : 4 ≤ 2^(n+4) := by
    have h : (2:Nat)^2 ≤ 2^(n+4) := Nat.pow_le_pow_right (by omega) (by omega)
    omega
  show steps _ ⟨.E, p, ⟨pow01 (2 ^ (n + 6 - 1)) ++ M, false,
      false :: (ones (2 ^ (n + 6) - 3) ++
        (false :: false :: (descCascade (n + 6 - 2) ++ TAIL)))⟩⟩ = _
  rw [descIn_right_split n TAIL,
      show 9 * (2 ^ (n+5) - 1)
          = 6 * (2 ^ (n+5) - 3) + 12 + 6 * ((2 ^ (n+4) - 1 - 1) + 1) + 3 from by omega,
      descLevel (2 ^ (n+5) - 3) (2 ^ (n+4) - 1 - 1) p (pow01 (2 ^ (n + 6 - 1)) ++ M) _]
  show some (_ : Cfg) = some (_ : Cfg)
  refine congrArg some ?_
  show (⟨.E, _, ⟨_, false, _⟩⟩ : Cfg) = ⟨.E, _, ⟨_, false, _⟩⟩
  rw [descIn_left_split (2 ^ (n+4) - 1 - 1) (2 ^ (n+5) - 3) (pow01 (2 ^ (n + 6 - 1)) ++ M),
      show 2 ^ (n+4) - 1 - 1 + 2 = 2 ^ (n+4) from by omega]
  -- residual differences are all definitional: `n+6-1 = n+5`, `n+5-2 = n+3`, `2^(n+4) = 2^(n+5-1)`
  rfl

/-! ### `DescFold` — the whole head descent, `∀k` -/

/-- the marker deposited by ONE rung at level `k = n+6`. -/
def descMarkStep (n : Nat) (M : List Bool) : List Bool :=
  false :: false :: true :: false :: true ::
    (pow01 (2 ^ (n + 5) - 3) ++ (pow01 (2 ^ (n + 5)) ++ M))

/-- the head position after ONE rung at level `k = n+6`. -/
def descPosStep (n : Nat) (p : Int) : Int :=
  p + 2 * ((2 ^ (n + 5) - 3 : Nat) : Int) + 8
    + 2 * (((2 ^ (n + 4) - 1 - 1 : Nat) : Int) + 1) - 1

/-- total step count of the descent `descIn (n+6) → descIn 5`. -/
def descTotal : Nat → Nat
  | 0 => 9 * (2 ^ 5 - 1)
  | n + 1 => 9 * (2 ^ (n + 6) - 1) + descTotal n

/-- the marker accumulated over the whole descent (outermost rung applied first). -/
def descMark : Nat → List Bool → List Bool
  | 0, M => descMarkStep 0 M
  | n + 1, M => descMark n (descMarkStep (n + 1) M)

/-- the position after the whole descent. -/
def descPosF : Nat → Int → Int
  | 0, p => descPosStep 0 p
  | n + 1, p => descPosF n (descPosStep (n + 1) p)

/-- **`DescFold` ∀k**: the ENTIRE head descent, `descIn (n+6)` → `descIn 5`, in `descTotal n`
steps.  Induction over the level, each rung discharged by `descLaw`; `TAIL` untouched throughout. -/
theorem descFold_all : ∀ (n : Nat) (p : Int) (M TAIL : List Bool),
    steps (descTotal n) (descIn (n + 6) p M TAIL)
      = some (descIn 5 (descPosF n p) (descMark n M) TAIL) := by
  intro n
  induction n with
  | zero => intro p M TAIL; exact descLaw 0 p M TAIL
  | succ n ih =>
    intro p M TAIL
    show steps (9 * (2 ^ (n + 6) - 1) + descTotal n) _ = _
    rw [steps_add, descLaw (n + 1) p M TAIL, someBind]
    -- `n+1+5 ≡ n+6`, `descPosF (n+1) p ≡ descPosF n (descPosStep (n+1) p)`, likewise the marker:
    -- all definitional, so `exact` (not `rw`, which would have to unify syntactically).
    exact ih (descPosStep (n + 1) p) (descMarkStep (n + 1) M) TAIL

set_option maxRecDepth 8000 in
/-- Closed form of the descent's total cost, stated subtraction-free:
`descTotal n = 9·(2^{n+6} − n − 33)`, i.e. `Σ_{j≤n} 9(2^{j+5}−1)`. -/
theorem descTotal_closed : ∀ n : Nat, descTotal n + 9 * (n + 33) = 9 * 2 ^ (n + 6) := by
  intro n
  induction n with
  | zero => decide
  | succ n ih =>
    have h1 : 1 ≤ (2:Nat) ^ (n + 6) := Nat.one_le_two_pow
    have h2 : (2:Nat) ^ (n + 1 + 6) = 2 * 2 ^ (n + 6) := by
      rw [Nat.pow_succ]; exact Nat.mul_comm _ _
    show 9 * (2 ^ (n + 6) - 1) + descTotal n + 9 * (n + 1 + 33) = 9 * 2 ^ (n + 1 + 6)
    rw [h2]
    -- abstract both atoms so `omega` sees a purely linear problem (it otherwise tries to
    -- normalise the `2^_` terms itself and blows the recursion depth)
    revert ih h1
    generalize (2:Nat) ^ (n + 6) = A
    generalize descTotal n = T
    intro h1 ih
    omega

-- ANTI-VACUITY (METHODS M4): the ∀k step count must reproduce the MEASURED rung totals.
-- k=6 (n=0): 279;  k=7 (n=1): 567;  k=8 (n=2): 1143;  k=9 (n=3): 2295.
example : 9 * (2 ^ (0 + 5) - 1) = 279 := by decide
example : 9 * (2 ^ (1 + 5) - 1) = 567 := by decide
example : 9 * (2 ^ (2 + 5) - 1) = 1143 := by decide
example : 9 * (2 ^ (3 + 5) - 1) = 2295 := by decide
-- and it must be the descLevel decomposition 6m + 12 + 6(m'+1) + 3 at k=6, not a coincidence:
example : 6 * (2 ^ 5 - 3) + 12 + 6 * ((2 ^ 4 - 1 - 1) + 1) + 3 = 279 := by decide
-- the FOLD's totals (descIn (n+6) -> descIn 5), i.e. the partial sums of the above:
example : descTotal 0 = 279 := by decide
example : descTotal 1 = 846 := by decide
example : descTotal 2 = 1989 := by decide
example : descTotal 3 = 4284 := by decide

#print axioms descIn_right_split
#print axioms descIn_left_split
#print axioms descLaw
#print axioms descFold_all
#print axioms descTotal_closed
