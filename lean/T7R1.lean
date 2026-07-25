/-
**SCRATCH PROBE — NOT a build target.** (2026-07-23)
`#eval` reconnaissance for R1's link-1 (does `descChew` apply to `descIn 6`'s block).
`descIn` is DEFINED in `T7Head.lean`; the copy below is the probe's local restatement.
-/
import T7Head
open X2

/-- **`descIn k`** (T7 head, 2026-07-23): the descent milestone at level `k`, EXACTLY as measured.
Comb `(01)^{2^{k-1}}` then marker `M`; right `0 · 1^{2^k-3} · 0^2 · descCascade(k-2) · TAIL`. -/
def descIn (k : Nat) (p : Int) (M TAIL : List Bool) : Cfg :=
  ⟨.E, p, ⟨pow01 (2 ^ (k - 1)) ++ M, false,
      false :: (ones (2 ^ k - 3) ++ (false :: false :: (descCascade (k - 2) ++ TAIL)))⟩⟩

-- R1 link 1 check: does descChew apply to descIn 6's block? Need
--   ones(2^k-3) = ones(2m) ++ [1,1,1]  (m = 2^{k-1}-3), then 0 0, then descCascade(k-2) = 1 1 X.
-- At k=6: 2^6-3=61 = ones(58)++[1,1,1] (m=29), descCascade(4) = ones(61)++... = 1 1 ones(59)++...
example : (2:Nat)^6 - 3 = 2 * 29 + 3 := by decide
#eval descCascade 4  -- to confirm it starts 1 1 1... (ones 61)
#eval (List.take 5 (descCascade 4))
