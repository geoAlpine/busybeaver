/-
**WIP — NOT GREEN. NOT a build target.** (2026-07-23)

R1's last mile per `METHODS_2026-07-23.md`: the `descIn` arithmetic framing that
instantiates `descLevel` at the `descIn` block sizes.  `descIn_right_split` below
currently FAILS to elaborate (`pow_add` is a Mathlib name; this project is
Mathlib-free) and therefore `#print axioms` reports `sorryAx`.  Nothing in this
file may be cited until it is green and in `defaultTargets`.
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
  have e2 : (2:Nat)^(n+6) = 4 * 2^(n+4) := by rw [show n+6 = (n+4)+2 from by omega, pow_add]; ring
  have e5 : (2:Nat)^(n+5) = 2 * 2^(n+4) := by rw [show n+5 = (n+4)+1 from by omega, pow_add]; ring
  have h4 : 4 ≤ 2^(n+4) := by
    calc (4:Nat) = 2^2 := by norm_num
    _ ≤ 2^(n+4) := Nat.pow_le_pow_right (by norm_num) (by omega)
  -- block1: ones(2^{n+6}-3) = ones(2m) ++ ones 3
  rw [show 2^(n+6)-3 = 2*(2^(n+5)-3) + 3 from by omega, ones_add,
      show n+6-2 = (n+3)+1 from by omega, descCascade]
  -- descCascade top block: ones(2^{(n+3)+3}-3) = ones(2^{n+6}-3); split as 1 1 ones(2(m'+1)) ones(2^{n+5}-3)
  rw [show 2^((n+3)+3)-3 = 2 + (2*((2^(n+4)-1-1)+1) + (2^(n+5)-3)) from by omega,
      ones_add, ones_add]
  simp only [List.append_assoc, List.cons_append, ones]
  rfl

#print axioms descIn_right_split
