/-! STANDALONE arithmetic probe for the §5bl doubling-phase (T7) backbone.
Local copies of `exitSteps`/`topGrindSteps`/`descentSteps` (character-identical to
X2.lean's) so every step below is checked WITHOUT the 12k-line build. -/

namespace T7Probe

def exitSteps (k : Nat) : Nat := 2 ^ (2 * k - 3) + k * 2 ^ (k - 1) + 2 ^ (k - 2) + 2
def topGrindSteps (a : Nat) : Nat := 2 ^ (2 * a) + 7 - 3 * 2 ^ a
def descentSteps (a : Nat) : Nat := 2 ^ (2 * a) + 110 - 9 * a

/-! ### the three `∀k` subtraction-free normalisations -/

theorem sq_split (k : Nat) : (2:Nat) ^ (2*k+8) = 2 ^ (k+4) * 2 ^ (k+4) := by
  rw [← Nat.pow_add]; congr 1; omega

theorem big16 (k : Nat) : (16:Nat) ≤ 2 ^ (k+4) := by
  have h : (2:Nat) ^ 4 ≤ 2 ^ (k+4) := Nat.pow_le_pow_right (by omega) (by omega)
  have e : (2:Nat) ^ 4 = 16 := by decide
  omega

theorem dom (k : Nat) : 16 * 2 ^ (k+4) ≤ 2 ^ (2*k+8) := by
  rw [sq_split k]; exact Nat.mul_le_mul_right _ (big16 k)

theorem lin (k : Nat) : k + 4 < 2 ^ (k+4) := Nat.lt_two_pow_self

theorem exit_shift (k : Nat) :
    exitSteps (k + 4) = 2 ^ (2*k+5) + (k+4) * 2 ^ (k+3) + 2 ^ (k+2) + 2 := by
  unfold exitSteps
  rw [show 2*(k+4)-3 = 2*k+5 from by omega, show (k+4)-1 = k+3 from by omega,
      show (k+4)-2 = k+2 from by omega]

theorem tg_shift (k : Nat) :
    topGrindSteps (k + 4) + 3 * 2 ^ (k+4) = 2 ^ (2*k+8) + 7 := by
  unfold topGrindSteps
  rw [show 2*(k+4) = 2*k+8 from by omega]
  have := dom k
  omega

theorem ds_shift (k : Nat) :
    descentSteps (k + 4) + 9 * (k+4) = 2 ^ (2*k+8) + 110 := by
  unfold descentSteps
  rw [show 2*(k+4) = 2*k+8 from by omega]
  have := dom k; have := big16 k; have := lin k
  omega

/-! ### the measured ladder -/

/-- `ascSteps m` = the ascending run `ASC(m+4)`: `regenIn`-exits `4..m+4` interleaved
with the topgrinds `4..m+3`. -/
def ascSteps : Nat → Nat
  | 0 => exitSteps 4
  | m + 1 => ascSteps m + topGrindSteps (m + 4) + exitSteps (m + 5)

/-- `ladderSteps m` = the descending ladder `LADDER(m+4)`. -/
def ladderSteps : Nat → Nat
  | 0 => ascSteps 0
  | m + 1 => ladderSteps m + ascSteps (m + 1) + descentSteps (m + 5)

/-- the two defining recurrences, `∀m` (definitional). -/
theorem asc_rec (m : Nat) :
    ascSteps (m+1) = ascSteps m + topGrindSteps (m+4) + exitSteps (m+5) := rfl
theorem ladder_rec (m : Nat) :
    ladderSteps (m+1) = ladderSteps m + ascSteps (m+1) + descentSteps (m+5) := rfl

/-! ### the measured closed forms (`K = g + 8`) -/

def entrySteps (K : Nat) : Nat :=
  if K % 2 = 0 then 6 * 2 ^ K + 6 * K + 91 else 26 * 2 ^ K + 6 * K - 217
def midgapSteps (K : Nat) : Nat := 4 ^ K + 2 * 2 ^ K + 554 - 8 * K
def exitPhaseSteps (K : Nat) : Nat :=
  if K % 2 = 0 then 4 * 2 ^ K + 28 * K + 306 else 4 * 2 ^ K + 28 * K + 252

def doubSteps (K : Nat) : Nat :=
  2 * 4 ^ K + 2 * K * 2 ^ K + (if K % 2 = 0 then 1 else 21) * 2 ^ K + 42 * K
    - (if K % 2 = 0 then 61 else 343)

/-- the six MEASURED doubling phases (`g = 1..6`) plus the `g = 7` value, which was
PREDICTED from `g ≤ 6` and then confirmed on the real orbit at step 2 866 093 189. -/
theorem doub_grounds :
    doubSteps  9 = 544291    ∧ doubSteps 10 = 2119015   ∧ doubSteps 11 = 8476791 ∧
    doubSteps 12 = 33657275  ∧ doubSteps 13 = 134602955 ∧ doubSteps 14 = 537346575 ∧
    doubSteps 15 = 2149155103 := by decide

theorem ladder_grounds :
    ladderSteps 4 = 132470 ∧ ladderSteps 5 = 528510 ∧ ladderSteps 6 = 2108038 ∧
    ladderSteps 7 = 8414862 ∧ ladderSteps 8 = 33615510 ∧ ladderSteps 9 = 134356638 := by
  decide

/-- the ladder's closed form `2·4^j + 2j·2^j − 9·2^j + 8j − 458` (subtraction-free),
BOUNDED grounding `m ≤ 11` (i.e. `j ≤ 15`, generations `g ≤ 7`).  NOT a `∀m` theorem. -/
theorem ladder_closed_bounded :
    ∀ m, m ≤ 11 → ladderSteps m + 9 * 2 ^ (m + 4) + 458
      = 2 * 4 ^ (m + 4) + 2 * (m + 4) * 2 ^ (m + 4) + 8 * (m + 4) := by decide

/-- **THE PHASE DECOMPOSITION**, at every measured generation.
EVEN `K`: entry ∘ ONE ladder ∘ exit.  ODD `K`: entry ∘ ladder ∘ midgap ∘ ladder ∘ exit. -/
theorem doub_decomp_grounds :
    doubSteps  9 = entrySteps  9 + 2 * ladderSteps 4 + midgapSteps  9 + exitPhaseSteps  9 ∧
    doubSteps 11 = entrySteps 11 + 2 * ladderSteps 6 + midgapSteps 11 + exitPhaseSteps 11 ∧
    doubSteps 13 = entrySteps 13 + 2 * ladderSteps 8 + midgapSteps 13 + exitPhaseSteps 13 ∧
    doubSteps 10 = entrySteps 10 +     ladderSteps 6                 + exitPhaseSteps 10 ∧
    doubSteps 12 = entrySteps 12 +     ladderSteps 8                 + exitPhaseSteps 12 ∧
    doubSteps 14 = entrySteps 14 +     ladderSteps 10                + exitPhaseSteps 14 := by
  decide

/-- CONTROL — the decomposition MUST fail if the parity split is dropped. -/
theorem doub_decomp_control :
    doubSteps 9 ≠ entrySteps 9 + ladderSteps 4 + midgapSteps 9 + exitPhaseSteps 9 ∧
    doubSteps 11 ≠ entrySteps 11 + ladderSteps 6 + midgapSteps 11 + exitPhaseSteps 11 ∧
    doubSteps 10 ≠ entrySteps 10 + 2 * ladderSteps 6 + midgapSteps 10 + exitPhaseSteps 10 := by
  decide

/-- CONTROL — the even branch with the odd constants must MISS. -/
theorem doub_even_control :
    2 * 4 ^ 10 + 2 * 10 * 2 ^ 10 + 21 * 2 ^ 10 + 42 * 10 - 343 ≠ 2119015 := by decide

#print axioms exit_shift
#print axioms tg_shift
#print axioms ds_shift
#print axioms asc_rec
#print axioms ladder_rec
#print axioms doub_grounds
#print axioms ladder_grounds
#print axioms ladder_closed_bounded
#print axioms doub_decomp_grounds
#print axioms doub_decomp_control
#print axioms doub_even_control

end T7Probe
