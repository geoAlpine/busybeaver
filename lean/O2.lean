/-!
# The o2 cryptid — Lean 4 formalization (candidate THIRD machine, after o4, o3)

Formalizes the BB(6) cryptid "the second Antihydra" (ceiling ×3/2)

  o2 = `1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA`  (blank tape),

mirroring the machine-formalization architecture of `Template.lean` (o4) and
`O3.lean` (o3): tape-zipper, `step`/`steps`, `steps_add`, sweep-by-induction,
fixed episodes, generation-map composition.  The exact spec and the certified
Link-0 decomposition come from `o2_link0_certify.py` /
`O2_LINK0_CERTIFIED_2026-07-08.md`.

Layers (labels: FORMALIZED = `lake build O2` green + `sorry`-free):

* **L1 (the machine)** — `step`/`steps`: o2 as a step function on the tape
  zipper.  `step = none` iff HALT, which for o2 is the gate `F` reads `0`
  (`F` is entered only by `D:0→0RF`, so HALT ⟺ that `D`-read-`0` has right
  neighbour `0`).  Kernel-`rfl` anchors vs the Python simulator at N = 44
  (the blank tape reaches milestone `D(2,1)`), 100, 200.
* **L2 (the two sweeps)** — `sweepBE` (the `B1E1` leftward invert,
  `1^{2n} → (01)^n`, head `−2n`) and `sweepCA` (the `C0A1` rightward invert,
  `(01)^n → 1^{2n}`, head `+2n`), each an ARBITRARY-length uniform lemma by
  2-transition tile + length induction.  Both period-2 (o4-grade), the exact
  content of §2 of the certificate.
* **L3 (the certified generation branch, FORMALIZED)** — the milestone
  `Mcfg a b` (`D(a,b) = 0^∞ [A] 0 11 (01)^a 0 11 (01)^b 0^∞`), the fixed
  10-step `prefix10` (`D(a,b) → cut 1`), and the **canonical unit**
  `unit`: from a cut `V(t) = 0^∞ 1^{6t+5} 0 [F:1] (01)^m S` (`k = t+1` the
  cut index), one unit is EXACTLY `12t+32 = 12k+20` steps and lands on the
  next cut with the 1-block grown by 6, `m ↦ m−2`, and the right suffix `S`
  UNTOUCHED — the composition
  `ep_pre(11) · sweepBE(3t+3) · ep_bnd(3) · sweepCA(3t+4) · ep_tail(4)`
  gluing the two arbitrary-length sweeps with three landmark-pinned fixed
  episodes.  `unit_iter` iterates it (`J` units, phase-1 drain of the
  odometer), and `phase1` composes `prefix10 · unit^J`: the FULL phase-1
  loop of a generation, Lean-checked, `D(a+1,b) → V(J)` with `m = a−2J`.

Honest scope: only PHASE 1 of the generation (prefix + the unit loop) is
formalized.  The 7 exit templates (SUF_EVEN/ODD/MID/ESC/TERMINAL, the
cut → next-milestone step), the phase-2 drain, and hence the full milestone
automaton `D(a,b) → D(a',b')`, the (y,b) conjugacy, and the mod-4
halt/escape hatch stay on the lab record (`O2_LINK0_CERTIFIED` §2–5), as does
the ceiling-(K) ledger conjecture.  **This file decides no machine; o2 stays
`[OPEN]`.**

Dependency-free (core Lean only, no mathlib), self-contained in namespace
`O2`.  No `sorry`, no `native_decide`.
-/

namespace O2

/-! ## §1 (L1) The machine o2. -/

/-- The six states of o2. -/
inductive St where
  | A | B | C | D | E | F
deriving DecidableEq, Repr

/-- Tape zipper (as in `Template.lean`/`O3.lean`): `left` = cells left of head
(nearest first), `head` = scanned cell, `right` = cells right of head (nearest
first); off-list cells are blank (`false`). -/
structure Tape where
  left : List Bool
  head : Bool
  right : List Bool
deriving DecidableEq, Repr

/-- A configuration: state, absolute head position, tape. -/
structure Cfg where
  st : St
  pos : Int
  tape : Tape
deriving DecidableEq, Repr

/-- Write `b` at the head. -/
def wr (t : Tape) (b : Bool) : Tape := ⟨t.left, b, t.right⟩

/-- Move the head one cell right. -/
def mvR : Tape → Tape
  | ⟨l, h, []⟩ => ⟨h :: l, false, []⟩
  | ⟨l, h, b :: r⟩ => ⟨h :: l, b, r⟩

/-- Move the head one cell left. -/
def mvL : Tape → Tape
  | ⟨[], h, r⟩ => ⟨[], false, h :: r⟩
  | ⟨b :: l, h, r⟩ => ⟨l, b, h :: r⟩

/-- One step of o2 = `1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA`.
`none` = HALT, which happens exactly when `F` reads `0` (the halt gate:
`F` is entered only by `D:0→0RF`, so non-halting ⟺ every `0` that `D`
reads has right neighbour `1`). -/
def step (c : Cfg) : Option Cfg :=
  match c.st, c.tape.head with
  | .A, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩   -- A0 → 1RB
  | .A, true  => some ⟨.C, c.pos + 1, mvR (wr c.tape true)⟩   -- A1 → 1RC
  | .B, false => some ⟨.C, c.pos - 1, mvL (wr c.tape true)⟩   -- B0 → 1LC
  | .B, true  => some ⟨.E, c.pos - 1, mvL (wr c.tape true)⟩   -- B1 → 1LE
  | .C, false => some ⟨.A, c.pos + 1, mvR (wr c.tape true)⟩   -- C0 → 1RA
  | .C, true  => some ⟨.D, c.pos + 1, mvR (wr c.tape true)⟩   -- C1 → 1RD
  | .D, false => some ⟨.F, c.pos + 1, mvR (wr c.tape false)⟩  -- D0 → 0RF
  | .D, true  => some ⟨.E, c.pos + 1, mvR (wr c.tape false)⟩  -- D1 → 0RE
  | .E, false => some ⟨.A, c.pos - 1, mvL (wr c.tape true)⟩   -- E0 → 1LA
  | .E, true  => some ⟨.B, c.pos - 1, mvL (wr c.tape false)⟩  -- E1 → 0LB
  | .F, false => none                                          -- F0 → HALT
  | .F, true  => some ⟨.A, c.pos + 1, mvR (wr c.tape true)⟩   -- F1 → 1RA

/-- `n` steps; `none` iff the machine halts strictly before completing them.
Hence `steps n c = some c'` certifies a halt-free (= all-safe) segment. -/
def steps : Nat → Cfg → Option Cfg
  | 0, c => some c
  | n + 1, c => (step c).bind (steps n)

theorem someBind {α β : Type} (a : α) (f : α → Option β) :
    (some a).bind f = f a := rfl

theorem noneBind {α β : Type} (f : α → Option β) :
    (none : Option α).bind f = none := rfl

/-- Run-splitting: `m + n` steps = `m` steps, then `n` more. -/
theorem steps_add (m n : Nat) (c : Cfg) :
    steps (m + n) c = (steps m c).bind (steps n) := by
  induction m generalizing c with
  | zero => rw [Nat.zero_add]; rfl
  | succ m ih =>
    have h : m + 1 + n = (m + n) + 1 := by omega
    rw [h]
    show (step c).bind (steps (m + n)) = ((step c).bind (steps m)).bind (steps n)
    cases step c with
    | none => rfl
    | some c' => exact ih c'

/-- Position-congruence helper. -/
theorem cfgPos {s : St} {p q : Int} {t : Tape} (h : p = q) :
    (⟨s, p, t⟩ : Cfg) = ⟨s, q, t⟩ := by rw [h]

/-! ### L1 sanity: kernel-checked anchors vs the Python simulator
(`o2_link0_certify.py`). -/

/-- o2 on the blank tape. -/
def init : Cfg := ⟨.A, 0, ⟨[], false, []⟩⟩

set_option maxRecDepth 4000 in
/-- After 44 steps from blank: state A, position −6, tape
`0 [A] 11 (01)^2 0 11 (01)^1` — i.e. the milestone `D(2,1)` (Python
cross-check; the blank orbit joins the milestone automaton here). -/
theorem sanity44 :
    steps 44 init = some ⟨.A, -6,
      ⟨[], false,
       [true, true, false, true, false, true, false, true, true, false, true]⟩⟩ := rfl

set_option maxRecDepth 4000 in
/-- After 100 steps from blank: state E, position 6 (Python cross-check). -/
theorem sanity100 :
    steps 100 init = some ⟨.E, 6,
      ⟨[true, true, true, true, false, true, true, true, true, true, true,
        true, true, true, true, true], true,
       [true, false, true]⟩⟩ := rfl

set_option maxRecDepth 8000 in
/-- After 200 steps from blank: state C, position −10 (Python cross-check). -/
theorem sanity200 :
    steps 200 init = some ⟨.C, -10,
      ⟨[true, true, true, true, true, true, true, true], false,
       [true, false, true, false, true, false, true, true, false, true, false,
        true, true, false, true, false, true, false, true]⟩⟩ := rfl

/-! ## §2 The periodic words (machine-independent, mirroring `Template`). -/

/-- `(01)^j` (`false` first). -/
def pow01 : Nat → List Bool
  | 0 => []
  | j + 1 => false :: true :: pow01 j

/-- `(10)^j` (`true` first). -/
def pow10 : Nat → List Bool
  | 0 => []
  | j + 1 => true :: false :: pow10 j

/-- `j` `true`s. -/
def ones : Nat → List Bool
  | 0 => []
  | j + 1 => true :: ones j

theorem pow01_add : ∀ (a b : Nat), pow01 (a + b) = pow01 a ++ pow01 b := by
  intro a
  induction a with
  | zero => intro b; rw [Nat.zero_add]; rfl
  | succ a ih =>
    intro b
    have h : a + 1 + b = (a + b) + 1 := by omega
    rw [h]
    show false :: true :: pow01 (a + b) = false :: true :: (pow01 a ++ pow01 b)
    rw [ih]

theorem pow10_add : ∀ (a b : Nat), pow10 (a + b) = pow10 a ++ pow10 b := by
  intro a
  induction a with
  | zero => intro b; rw [Nat.zero_add]; rfl
  | succ a ih =>
    intro b
    have h : a + 1 + b = (a + b) + 1 := by omega
    rw [h]
    show true :: false :: pow10 (a + b) = true :: false :: (pow10 a ++ pow10 b)
    rw [ih]

theorem ones_add : ∀ (a b : Nat), ones (a + b) = ones a ++ ones b := by
  intro a
  induction a with
  | zero => intro b; rw [Nat.zero_add]; rfl
  | succ a ih =>
    intro b
    have h : a + 1 + b = (a + b) + 1 := by omega
    rw [h]
    show true :: ones (a + b) = true :: (ones a ++ ones b)
    rw [ih]

/-- The pivotal config-identity (o2 analogue of o4's `pow01_of_pow10`):
`1 · (01)^n = (10)^n · 1`.  Turns the leftward sweep's `(01)` fabric into the
`(10)` marker the rightward sweep reads. -/
theorem cons_pow01 : ∀ (n : Nat), true :: pow01 n = pow10 n ++ [true] := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    show true :: false :: true :: pow01 n = true :: false :: (pow10 n ++ [true])
    rw [ih]

/-! ## §3 (L2) The two sweep lemmas — o2's period-2 inverting cycles, each an
arbitrary-length uniform lemma by 2-transition tile + length induction
(`O2_LINK0_CERTIFIED` §2, "PROVEN, 2-transition induction from the table"). -/

/-- **Sweep lemma `B1E1`** (leftward invert): from state `B` on the top `1` of
a block `1^{2n}` (`ones (2n)` on the left, head a `1`), the 2-cycle
`B:1→1LE · E:1→0LB` marches `−2n`, consuming the block and depositing `(01)^n`
on the right; the head stays a `1` (a carry) and the deep left context `L` is
untouched.  Proven for every `n` by induction. -/
theorem sweepBE : ∀ (n : Nat) (p : Int) (L R : List Bool),
    steps (2 * n) ⟨.B, p, ⟨ones (2 * n) ++ L, true, R⟩⟩
      = some ⟨.B, p - 2 * (n : Int), ⟨L, true, pow01 n ++ R⟩⟩ := by
  intro n
  induction n with
  | zero => intro p L R; exact congrArg some (cfgPos (by omega))
  | succ n ih =>
    intro p L R
    have hn : 2 * (n + 1) = 2 * n + 2 := by omega
    rw [hn]
    have hones : ones (2 * n + 2) = true :: true :: ones (2 * n) := by
      rw [show 2 * n + 2 = 2 + 2 * n from by omega, ones_add]; rfl
    rw [hones]
    have h2 : steps (2 * n + 2)
          (⟨.B, p, ⟨true :: true :: ones (2 * n) ++ L, true, R⟩⟩ : Cfg)
        = steps (2 * n) ⟨.B, p - 1 - 1, ⟨ones (2 * n) ++ L, true, false :: true :: R⟩⟩ := rfl
    rw [h2, ih (p - 1 - 1) L (false :: true :: R)]
    have hr : pow01 n ++ (false :: true :: R) = pow01 (n + 1) ++ R := by
      rw [show pow01 (n + 1) = pow01 n ++ pow01 1 from pow01_add n 1, List.append_assoc]; rfl
    rw [hr]
    exact congrArg some (cfgPos (by push_cast; omega))

/-- **Sweep lemma `C0A1`** (rightward invert): from state `C` on the leading
`0` of `(01)^n` (`head` a `0`, right starting with `(10)^n`), the 2-cycle
`C:0→1RA · A:1→1RC` marches `+2n`, consuming `(10)^n` and depositing `1^{2n}`
on the left; the head stays a `0` and the deep right context `R` is untouched.
Proven for every `n` by induction. -/
theorem sweepCA : ∀ (n : Nat) (p : Int) (L R : List Bool),
    steps (2 * n) ⟨.C, p, ⟨L, false, pow10 n ++ R⟩⟩
      = some ⟨.C, p + 2 * (n : Int), ⟨ones (2 * n) ++ L, false, R⟩⟩ := by
  intro n
  induction n with
  | zero => intro p L R; exact congrArg some (cfgPos (by omega))
  | succ n ih =>
    intro p L R
    have hn : 2 * (n + 1) = 2 * n + 2 := by omega
    rw [hn]
    have h2 : steps (2 * n + 2)
          (⟨.C, p, ⟨L, false, pow10 (n + 1) ++ R⟩⟩ : Cfg)
        = steps (2 * n) ⟨.C, p + 1 + 1, ⟨true :: true :: L, false, pow10 n ++ R⟩⟩ := rfl
    rw [h2, ih (p + 1 + 1) (true :: true :: L) R]
    have hl : ones (2 * n) ++ (true :: true :: L) = ones (2 * n + 2) ++ L := by
      rw [show 2 * n + 2 = 2 * n + 2 from rfl, ones_add, List.append_assoc]; rfl
    rw [hl, show 2 * n + 2 = 2 * (n + 1) from by omega]
    exact congrArg some (cfgPos (by push_cast; omega))

/-! ## §4 (L3) The certified generation branch (phase 1). -/

/-- The o2 milestone `D(a,b) = 0^∞ [A] 0 11 (01)^a 0 11 (01)^b 0^∞`, head
(state `A`) on the leading `0`, all cells strictly left blank, at position `p`.
Matches `o2_link0_certify.py`'s milestone form; blank tape → `Mcfg 2 1 (-6)`
at step 44 (see `sanity44`). -/
def Mcfg (a b : Nat) (p : Int) : Cfg :=
  ⟨.A, p, ⟨[], false,
    true :: true :: (pow01 a ++ (false :: true :: true :: pow01 b))⟩⟩

/-- A cut configuration `V(t) = 0^∞ 1^{6t+5} 0 [F:1] (01)^m S 0^∞` (head, state
`F`, on the `1` just right of the `0`-terminated `1`-block), cut index
`k = t+1`, with an arbitrary untouched right suffix `S`.  (For a bare
phase-2 cut `S = []`; for a phase-1 cut `S = 0 11 (01)^q`.) -/
def Vcfg (t m : Nat) (p : Int) (S : List Bool) : Cfg :=
  ⟨.F, p, ⟨false :: ones (6 * t + 5), true, pow01 m ++ S⟩⟩

/-! ### The fixed episodes (kernel `rfl` with symbolic tails, landmark-pinned
— max offset 3, the certificate's pinning bound met exactly). -/

set_option maxRecDepth 8000 in
/-- Episode `ep_pre` (11 fixed steps `F1 A0 B1 E1 B1 E0 A1 C1 D1 E0 A0`): the
cut → block turnaround.  Reads only the window `[−2,+2]`; the tails `LT`
(left) and `RT` (right) are untouched. -/
theorem ep_pre (p : Int) (LT RT : List Bool) :
    steps 11 ⟨.F, p, ⟨false :: true :: LT, true, false :: true :: RT⟩⟩
      = some ⟨.B, p + 1, ⟨true :: true :: true :: LT, true, true :: RT⟩⟩ := by
  have h : steps 11 (⟨.F, p, ⟨false :: true :: LT, true, false :: true :: RT⟩⟩ : Cfg)
      = some ⟨.B, p + 1 + 1 - 1 - 1 - 1 - 1 + 1 + 1 + 1 - 1 + 1,
          ⟨true :: true :: true :: LT, true, true :: RT⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- Episode `ep_bnd` (3 fixed steps `B1 E1 B0`): the left boundary turn, from
the last carry `1` onto the blank, re-entering state `C`; `W` untouched. -/
theorem ep_bnd (p : Int) (W : List Bool) :
    steps 3 ⟨.B, p, ⟨[true], true, W⟩⟩
      = some ⟨.C, p - 3, ⟨[], false, true :: false :: true :: W⟩⟩ := by
  have h : steps 3 (⟨.B, p, ⟨[true], true, W⟩⟩ : Cfg)
      = some ⟨.C, p - 1 - 1 - 1, ⟨[], false, true :: false :: true :: W⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- Episode `ep_tail` (4 fixed steps `C0 A1 C1 D0`): the right boundary rebuild
and next-cut re-entry (into state `F`, the halt-gate cell now reading `1`);
`LL` and `TL` untouched. -/
theorem ep_tail (p : Int) (LL TL : List Bool) :
    steps 4 ⟨.C, p, ⟨LL, false, true :: true :: false :: true :: TL⟩⟩
      = some ⟨.F, p + 4, ⟨false :: true :: true :: true :: LL, true, TL⟩⟩ := by
  have h : steps 4 (⟨.C, p, ⟨LL, false, true :: true :: false :: true :: TL⟩⟩ : Cfg)
      = some ⟨.F, p + 1 + 1 + 1 + 1, ⟨false :: true :: true :: true :: LL, true, TL⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- **The fixed 10-step PREFIX (`certified`, `O2_LINK0_CERTIFIED` §2):**
`A0 B1 E1 B0 C0 A1 C0 A1 C1 D0`, window `[−2,4]`.  From the milestone head
`[A] 0 1 1 0 1 Z` it builds the cut-1 block `1^5 0 [F:1]` and lands, with the
tail `Z` (all of `(01)^{a−1} 0 11 (01)^b …`) untouched. -/
theorem prefix10 (p : Int) (Z : List Bool) :
    steps 10 ⟨.A, p, ⟨[], false, true :: true :: false :: true :: Z⟩⟩
      = some ⟨.F, p + 4, ⟨false :: ones 5, true, Z⟩⟩ := by
  have h : steps 10 (⟨.A, p, ⟨[], false, true :: true :: false :: true :: Z⟩⟩ : Cfg)
      = some ⟨.F, p + 1 - 1 - 1 - 1 + 1 + 1 + 1 + 1 + 1 + 1,
          ⟨false :: ones 5, true, Z⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- **The prefix from a milestone.**  `D(a+1,b) → V(0)` (cut 1) in 10 steps:
the odometer count `m = a` (`= (a+1)−1`), the remaining milestone
`0 11 (01)^b` becoming the untouched suffix `S`. -/
theorem prefix_mil (a b : Nat) (p : Int) :
    steps 10 (Mcfg (a + 1) b p)
      = some (Vcfg 0 a (p + 4) (false :: true :: true :: pow01 b)) := by
  show steps 10 (⟨.A, p, ⟨[], false,
      true :: true :: (pow01 (a + 1) ++ (false :: true :: true :: pow01 b))⟩⟩ : Cfg) = _
  show steps 10 (⟨.A, p, ⟨[], false,
      true :: true :: false :: true :: (pow01 a ++ (false :: true :: true :: pow01 b))⟩⟩ : Cfg) = _
  rw [prefix10]
  rfl

/-- **THE o2 CANONICAL UNIT (L3), fully formal.**  For every `t` (cut index
`k = t+1`) and `m''` (so `m = m''+2 ≥ 2`), one canonical unit takes the cut
`V(t)` with `m = m''+2` to the next cut `V(t+1)` with `m'' = m−2`, in exactly
`12t+32 = 12k+20` steps, the `1`-block grown by 6 and the right suffix `S`
UNTOUCHED.  `some` output ⇒ HALT-FREE over the whole unit (the halt gate never
fires).  Composition:
`ep_pre(11) · sweepBE(3t+3) · ep_bnd(3) · sweepCA(3t+4) · ep_tail(4)`. -/
theorem unit (t m'' : Nat) (p : Int) (S : List Bool) :
    steps (12 * t + 32) (Vcfg t (m'' + 2) p S)
      = some (Vcfg (t + 1) m'' (p + 4) S) := by
  have hsplit : 12 * t + 32
      = 11 + (2 * (3 * t + 3) + (3 + (2 * (3 * t + 4) + 4))) := by omega
  -- reshape the cut into the `ep_pre` input (defeq peeling)
  show steps (12 * t + 32) (⟨.F, p, ⟨false :: true :: ones (6 * t + 4), true,
      false :: true :: (pow01 (m'' + 1) ++ S)⟩⟩ : Cfg) = _
  rw [hsplit, steps_add, ep_pre, someBind]
  -- phase 2: sweepBE with n = 3t+3.  left = ones(6t+7) = ones(6t+6) ++ [true]
  have hL1 : (true :: true :: true :: ones (6 * t + 4) : List Bool)
      = ones (2 * (3 * t + 3)) ++ [true] := by
    have e1 : (true :: true :: true :: ones (6 * t + 4) : List Bool)
        = ones ((6 * t + 4) + 3) := rfl
    rw [e1, show (6 * t + 4) + 3 = 2 * (3 * t + 3) + 1 from by omega, ones_add]; rfl
  rw [hL1, steps_add, sweepBE, someBind]
  -- phase 3: ep_bnd (boundary).  right after sweepBE = pow01(3t+3) ++ (true :: (pow01(m''+1) ++ S))
  rw [steps_add, ep_bnd, someBind]
  -- phase 4: sweepCA with n = 3t+4.  reshape the boundary word into pow10(3t+4) ++ R'
  have hR : (true :: false :: true :: (pow01 (3 * t + 3) ++ (true :: (pow01 (m'' + 1) ++ S))) : List Bool)
      = pow10 (2 * (3 * t + 4) / 2) ++ (true :: true :: (pow01 (m'' + 1) ++ S)) := by
    rw [show 2 * (3 * t + 4) / 2 = 3 * t + 4 from by omega]
    have e2 : (true :: false :: true :: (pow01 (3 * t + 3) ++ (true :: (pow01 (m'' + 1) ++ S))) : List Bool)
        = (true :: pow01 (3 * t + 4)) ++ (true :: (pow01 (m'' + 1) ++ S)) := rfl
    rw [e2, cons_pow01, List.append_assoc]; rfl
  rw [hR]
  have hn4 : (2 * (3 * t + 4) / 2 : Nat) = 3 * t + 4 := by omega
  rw [hn4, show (2 * (3 * t + 4)) = 2 * (3 * t + 4) from rfl, steps_add, sweepCA, someBind]
  -- phase 5: ep_tail.  right = true::true::(pow01(m''+1) ++ S) = true::true::false::true::(pow01 m'' ++ S)
  have hR2 : (true :: true :: (pow01 (m'' + 1) ++ S) : List Bool)
      = true :: true :: false :: true :: (pow01 m'' ++ S) := rfl
  rw [hR2, ep_tail]
  -- assemble the next cut (defeq): left false::true^3::ones(6t+8) = false::ones(6t+11)
  apply congrArg some
  show (⟨.F, _, ⟨false :: true :: true :: true :: (ones (2 * (3 * t + 4)) ++ []), true,
      pow01 m'' ++ S⟩⟩ : Cfg) = Vcfg (t + 1) m'' (p + 4) S
  show (⟨.F, _, ⟨false :: true :: true :: true :: (ones (2 * (3 * t + 4)) ++ []), true,
      pow01 m'' ++ S⟩⟩ : Cfg)
    = ⟨.F, p + 4, ⟨false :: ones (6 * (t + 1) + 5), true, pow01 m'' ++ S⟩⟩
  have hLfin : (false :: true :: true :: true :: (ones (2 * (3 * t + 4)) ++ []) : List Bool)
      = false :: ones (6 * (t + 1) + 5) := by
    rw [List.append_nil]
    have e3 : (true :: true :: true :: ones (2 * (3 * t + 4)) : List Bool)
        = ones (2 * (3 * t + 4) + 3) := rfl
    rw [show (false :: true :: true :: true :: ones (2 * (3 * t + 4)) : List Bool)
          = false :: (true :: true :: true :: ones (2 * (3 * t + 4))) from rfl, e3,
        show 2 * (3 * t + 4) + 3 = 6 * (t + 1) + 5 from by omega]
  rw [hLfin]
  exact cfgPos (by push_cast; omega)

/-! ### §4a Iterating the unit — the phase-1 odometer drain. -/

/-- Total steps of `J` consecutive units starting at cut index `t+1`
(each unit at cut `t+i+1` costs `12(t+i)+32`). -/
def unitTime : Nat → Nat → Nat
  | 0, _ => 0
  | J + 1, t => (12 * t + 32) + unitTime J (t + 1)

/-- **Iterated unit (halt-free phase-1 drain):** `J` units take the cut `V(t)`
with `m = 2J + r` to `V(t+J)` with `m = r`, shifting `+4J`, suffix `S`
untouched, in exactly `unitTime J t` steps — all halt-free. -/
theorem unit_iter : ∀ (J t r : Nat) (p : Int) (S : List Bool),
    steps (unitTime J t) (Vcfg t (2 * J + r) p S)
      = some (Vcfg (t + J) r (p + 4 * (J : Int)) S) := by
  intro J
  induction J with
  | zero =>
    intro t r p S
    show steps 0 _ = _
    apply congrArg some
    show Vcfg t (2 * 0 + r) p S = Vcfg (t + 0) r (p + 4 * ((0 : Nat) : Int)) S
    rw [show 2 * 0 + r = r from by omega, Nat.add_zero]
    exact cfgPos (by push_cast; omega)
  | succ J ih =>
    intro t r p S
    have h1 : steps (unitTime (J + 1) t) (Vcfg t (2 * (J + 1) + r) p S)
        = (steps (12 * t + 32) (Vcfg t ((2 * J + r) + 2) p S)).bind
            (steps (unitTime J (t + 1))) := by
      have he : (2 * (J + 1) + r : Nat) = (2 * J + r) + 2 := by omega
      rw [he]
      exact steps_add (12 * t + 32) (unitTime J (t + 1)) _
    rw [h1, unit, someBind, ih (t + 1) r (p + 4) S]
    apply congrArg some
    show Vcfg (t + 1 + J) r ((p + 4) + 4 * (J : Int)) S
      = Vcfg (t + (J + 1)) r (p + 4 * ((J + 1 : Nat) : Int)) S
    have ht : t + 1 + J = t + (J + 1) := by omega
    rw [ht]
    exact cfgPos (by push_cast; omega)

/-- **THE o2 PHASE-1 GENERATION BRANCH (L3), fully formal.**  For every `a`,
`b`, `J`, `r` with `a = 2J + r`, the milestone `D(a+1,b)` reaches the phase-1
cut `V(J)` with odometer remainder `m = r` in exactly `10 + unitTime J 0`
steps — the fixed prefix then `J` canonical units.  `some` output ⇒ HALT-FREE
over the whole phase.  This is the certified `prefix · unit^J` composition of
`O2_LINK0_CERTIFIED` §2, Lean-checked; the exit template that turns the last
cut into the next milestone (and the mod-4 hatch) stays on the lab record. -/
theorem phase1 (a b J r : Nat) (p : Int) (ha : a = 2 * J + r) :
    steps (10 + unitTime J 0) (Mcfg (a + 1) b p)
      = some (Vcfg J r (p + 4 + 4 * (J : Int)) (false :: true :: true :: pow01 b)) := by
  rw [steps_add, prefix_mil, someBind]
  subst ha
  have h := unit_iter J 0 r (p + 4) (false :: true :: true :: pow01 b)
  rw [h]
  apply congrArg some
  show Vcfg (0 + J) r ((p + 4) + 4 * (J : Int)) (false :: true :: true :: pow01 b)
    = Vcfg J r (p + 4 + 4 * (J : Int)) (false :: true :: true :: pow01 b)
  rw [Nat.zero_add]

/-! ### §4b real-orbit anchor: the blank tape → milestone `D(2,1)` → phase 1. -/

set_option maxRecDepth 4000 in
/-- Blank tape → milestone `D(2,1)` at position `−6` in 44 steps (the blank
orbit's entry to the milestone automaton; kernel `rfl` vs Python). -/
theorem blank_to_D21 : steps 44 init = some (Mcfg 2 1 (-6)) := rfl

/-- Blank → the phase-1 cut of `D(2,1)`: `D(2,1) = D(1+1,1)`, `a = 1 = 2·0+1`,
so `J = 0`, `r = 1` — the prefix alone reaches cut 1 `V(0)` with `m = 1`
(the odometer's last unit is the exit, not a canonical unit).  Composed from
`blank_to_D21` and `phase1`. -/
theorem blank_to_cut1 :
    steps (44 + (10 + unitTime 0 0)) init
      = some (Vcfg 0 1 (-6 + 4 + 4 * (0 : Int)) (false :: true :: true :: pow01 1)) := by
  rw [steps_add, blank_to_D21, someBind]
  exact phase1 1 1 0 1 (-6) (by omega)

/-! ## §5 Axiom audit (printed at every build). -/

#print axioms steps_add
#print axioms sanity44
#print axioms sanity100
#print axioms sanity200
#print axioms sweepBE
#print axioms sweepCA
#print axioms cons_pow01
#print axioms ep_pre
#print axioms ep_bnd
#print axioms ep_tail
#print axioms prefix10
#print axioms prefix_mil
#print axioms unit
#print axioms unit_iter
#print axioms phase1
#print axioms blank_to_D21
#print axioms blank_to_cut1

/-! ### §5a sanity: the sweeps and the unit, kernel-executed on real configs. -/

-- the two sweeps at concrete lengths (vs o2_link0_certify.py):
#eval decide (steps (2 * 7) ⟨.B, 0, ⟨ones 14 ++ [false], true, [false, true]⟩⟩
      = some ⟨.B, -14, ⟨[false], true, pow01 7 ++ [false, true]⟩⟩)   -- sweepBE n=7: true
#eval decide (steps (2 * 5) ⟨.C, 0, ⟨[true], false, pow10 5 ++ [true]⟩⟩
      = some ⟨.C, 10, ⟨ones 10 ++ [true], false, [true]⟩⟩)            -- sweepCA n=5: true

-- the canonical unit at concrete cut indices (vs the standalone-unit grid):
#eval decide (steps (12 * 1 + 32) (Vcfg 1 7 0 [])
      = some (Vcfg 2 5 4 []))                                          -- unit t=1,m=7: true
#eval decide (steps (12 * 2 + 32) (Vcfg 2 7 0 [false, true, true])
      = some (Vcfg 3 5 4 [false, true, true]))                        -- unit t=2 with suffix: true

-- phase-1 branch on a real milestone D(9,3) = D(8+1,3), a=8=2*4+0, J=4:
#eval decide ((steps (10 + unitTime 4 0) (Mcfg 9 3 0)).map (fun c => (c.st, c.pos))
      = some (St.F, (20 : Int)))                                       -- phase1 J=4: true

#eval steps 44 init  -- cross-check vs Python (blank → D(2,1))

end O2
