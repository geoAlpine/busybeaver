import EntryB
open X2

/-!
# `C` decided — the state-relabelling isomorphism, in Lean

`C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` and `x2 = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`
are the SAME transition graph under the cyclic relabelling `σ : A→F, B→A, C→B, D→C, E→D, F→E`.
`EntryB.C_nonhalt_blank` says `x2`'s own `step` never halts from `⟨B, 0, blank⟩`.  This file builds
the relabelling in Lean and transfers that to the machine `C` started on the blank tape.
**No machine decided until the audit passes.**
-/

namespace CIso

/-- `σ`: x2's state ↦ C's state -/
def sg : St → St
  | .A => .F | .B => .A | .C => .B | .D => .C | .E => .D | .F => .E

/-- `σ⁻¹`: C's state ↦ x2's state -/
def sgi : St → St
  | .A => .B | .B => .C | .C => .D | .D => .E | .E => .F | .F => .A

theorem sgi_sg : ∀ s, sgi (sg s) = s := by intro s; cases s <;> rfl
theorem sg_sgi : ∀ s, sg (sgi s) = s := by intro s; cases s <;> rfl

/-- `C`'s one-step function, written directly against `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` -/
def stepC (c : Cfg) : Option Cfg :=
  match c.st, c.tape.head with
  | .A, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩    -- 1RB
  | .A, true  => none                                           -- ---
  | .B, false => some ⟨.C, c.pos - 1, mvL (wr c.tape false)⟩   -- 0LC
  | .B, true  => some ⟨.D, c.pos - 1, mvL (wr c.tape true)⟩    -- 1LD
  | .C, false => some ⟨.D, c.pos + 1, mvR (wr c.tape false)⟩   -- 0RD
  | .C, true  => some ⟨.C, c.pos - 1, mvL (wr c.tape true)⟩    -- 1LC
  | .D, false => some ⟨.E, c.pos + 1, mvR (wr c.tape true)⟩    -- 1RE
  | .D, true  => some ⟨.B, c.pos - 1, mvL (wr c.tape false)⟩   -- 0LB
  | .E, false => some ⟨.F, c.pos + 1, mvR (wr c.tape false)⟩   -- 0RF
  | .E, true  => some ⟨.D, c.pos + 1, mvR (wr c.tape true)⟩    -- 1RD
  | .F, false => some ⟨.A, c.pos + 1, mvR (wr c.tape true)⟩    -- 1RA
  | .F, true  => some ⟨.D, c.pos + 1, mvR (wr c.tape false)⟩   -- 0RD

def stepsC : Nat → Cfg → Option Cfg
  | 0, c => some c
  | n + 1, c => (stepC c).bind (stepsC n)

/-- relabel a configuration from `x2`'s naming into `C`'s -/
def rl (c : Cfg) : Cfg := ⟨sg c.st, c.pos, c.tape⟩

/-- **the one-step correspondence** — `C` IS `x2` relabelled -/
theorem stepC_rl (c : Cfg) : stepC (rl c) = (step c).map rl := by
  rcases c with ⟨s, p, ⟨l, hd, r⟩⟩
  cases s <;> cases hd <;> rfl

theorem stepsC_rl : ∀ (n : Nat) (c : Cfg), stepsC n (rl c) = (steps n c).map rl := by
  intro n
  induction n with
  | zero => intro c; rfl
  | succ n ih =>
    intro c
    show (stepC (rl c)).bind (stepsC n) = ((step c).bind (steps n)).map rl
    rw [stepC_rl]
    cases step c with
    | none => rfl
    | some d => show stepsC n (rl d) = _; exact ih d

/-- `C` on the blank tape is `x2`'s `⟨B, 0, blank⟩` relabelled -/
theorem initC_rl : (⟨.A, 0, ⟨[], false, []⟩⟩ : Cfg) = rl FromB.initB := rfl

/-- **`C` NEVER HALTS FROM THE BLANK TAPE.** -/
theorem C_machine_nonhalt : ∀ N : Nat, stepsC N ⟨.A, 0, ⟨[], false, []⟩⟩ ≠ none := by
  intro N
  rw [initC_rl, stepsC_rl]
  intro h
  exact FromB.C_nonhalt_blank N (by
    cases hs : steps N FromB.initB with
    | none => rfl
    | some d => rw [hs] at h; exact absurd h (by simp))

#print axioms stepC_rl
#print axioms stepsC_rl
#print axioms C_machine_nonhalt

end CIso
