/-!
# The o4 body lemma — Lean 4 formalization (template-layer pilot)

Formalizes the BODY LEMMA of the certified trace-template method
(`PAPER_TEMPLATE_METHOD.md` §2–3, `O4_TEMPLATE_CLOSURE_2026-07-06.md` §2,
computational content `o4_body_proof.py`) for the BB(6) cryptid

  o4 = `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`.

Layers:

* **L1 (the machine)** — `step`/`steps`: o4 as a step function on
  configurations `(state, position, tape-zipper)`; `step = none` iff the
  machine halts (state `F` reads `1` — the halt gate of
  `O4_WINDOW_SATURATION`).  `#eval`/`rfl` sanity against the Python
  cross-check (`template_crosscheck.py`) at N = 100, 1000.
* **L2 (the sweep lemmas)** — `sweepBF`, `sweepDE`: the two o4 sweeps,
  `B1F0` read-only rightward over `(01)^j` and `D1E0` leftward invert
  (`(01)^j` on the left becomes `(10)^j` on the right), proven for
  **arbitrary length** `j` by 2-transition induction — the
  "proven for arbitrary length" ingredients of the method.
* **L3 (the body lemma)** — `body_step`:
  `B(k) = 0^∞ [E] (10)^k 1001 0^∞  →  B(k+2)` shifted one cell left,
  in exactly `4k + 15` steps, for **every** `k` (the lab note's grid
  certifies odd `k ≥ 19`; the formal composition — 2 fixed episode steps ·
  sweep `2k` · 8 fixed episode steps · sweep `2(k+2)` · 1 fixed episode
  step — holds for all `k ≥ 0`, both parities, strictly extending the
  red-team's `k ≥ 13` cone check).  Since `steps` returns `some`, the
  segment is halt-free, which by the halt gate *is* the safety claim
  (a B-reads-1 with right neighbour 1 would halt on the next step).
* **Corollaries** — `body_iter` (r-fold body application,
  `B(k) → B(k+2r)` shifted `-r`) and `body_nonhalt`: the **standalone**
  configuration `B(k)` (blank tape left of the zone) never halts — a fully
  formal translated-bouncer non-halting certificate for this family.
* **L4 (the prefix, parametric window)** — `prefix471`: the fixed
  471-step prefix word from the real milestone form
  `M(G,a) = 0^∞ [E] 0^G (10)^a 01 0^∞`, with span `[-11, 30]` and an
  ARBITRARY untouched suffix beyond 30 gap zeros — hence
  (G, a)-uniformity for ALL `G ≥ 31`, all `a` (`prefix_milestone`).
  Plus `steps_shift` (translation equivariance), `body_step_ctx` /
  `body_iter_ctx` (body with explicit right context: exactly 3 gap zeros
  consumed per application), and the composition **`prefix_bodies`**:
  `M(G,a) → prefix · body^r →` the suffix-entry zone `(10)^(19+2r) 1001`,
  for every `r` with `31 + 3r ≤ G`.  Real-orbit anchors: `real_milestone`
  (blank tape reaches exactly `M(43,18)` at step 1548, kernel-checked) and
  `real_generation` (blank tape → step 2431 = the suffix-entry
  configuration of the real generation).

Honest scope: the SUFFIX lemmas (3 classes, small-`a` per-parameter
templates) are NOT formalized, so the full generation map `M(G,a) →
M(G',a')`, the derived odometer, and the a-ledger remain on the lab-note
record (`RunStructure.lean` has the arithmetic layer).
**This file decides no machine; o4 remains `[OPEN]`.**

Dependency-free: core Lean only (no mathlib), matching `RunStructure.lean`.
No `sorry`, no `native_decide`; sanity checks are `rfl`/`decide`-free
kernel-checked equalities plus `#eval` mirrors.
-/

namespace Template

/-! ## §1 (L1) The machine o4. -/

/-- The six states of o4. -/
inductive St where
  | A | B | C | D | E | F
deriving DecidableEq, Repr

/-- Tape zipper: `left` lists the cells left of the head (nearest first),
`head` the scanned cell, `right` the cells right of the head (nearest
first).  Cells beyond either list are blank (`false`): both `mv` functions
materialize `false` when they pop an empty list, so the zipper represents a
two-way-infinite tape with finite support. -/
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

/-- One step of o4 = `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`.
`none` = HALT, which happens exactly when `F` reads `1` (the halt gate:
`F` is entered only by `B:1→1RF`, so non-halting ⟺ every 1 that `B` reads
has right neighbour 0, `O4_WINDOW_SATURATION`). -/
def step (c : Cfg) : Option Cfg :=
  match c.st, c.tape.head with
  | .A, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩
  | .A, true  => some ⟨.D, c.pos - 1, mvL (wr c.tape false)⟩
  | .B, false => some ⟨.C, c.pos + 1, mvR (wr c.tape true)⟩
  | .B, true  => some ⟨.F, c.pos + 1, mvR (wr c.tape true)⟩
  | .C, false => some ⟨.A, c.pos - 1, mvL (wr c.tape true)⟩
  | .C, true  => some ⟨.A, c.pos + 1, mvR (wr c.tape false)⟩
  | .D, false => some ⟨.A, c.pos - 1, mvL (wr c.tape false)⟩
  | .D, true  => some ⟨.E, c.pos - 1, mvL (wr c.tape false)⟩
  | .E, false => some ⟨.D, c.pos - 1, mvL (wr c.tape true)⟩
  | .E, true  => some ⟨.A, c.pos - 1, mvL (wr c.tape true)⟩
  | .F, false => some ⟨.B, c.pos + 1, mvR (wr c.tape false)⟩
  | .F, true  => none

/-- `n` steps; `none` iff the machine halts strictly before completing
them.  Hence `steps n c = some c'` certifies a halt-free (= all-safe)
segment. -/
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
  | zero =>
    rw [Nat.zero_add]
    rfl
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

/-! ### L1 sanity: kernel-checked anchors against the Python cross-check
(`template_crosscheck.py`, zipper AND independent dict-tape semantics). -/

/-- o4 on the blank tape. -/
def init : Cfg := ⟨.A, 0, ⟨[], false, []⟩⟩

set_option maxRecDepth 4000 in
/-- After 100 steps from blank: state D, position 2 (Python cross-check). -/
theorem sanity100 :
    steps 100 init = some ⟨.D, 2,
      ⟨[false, true, true, true, true, false, true, true], true,
       [true, false, true, false, true, false, true, false, true, false,
        false, true]⟩⟩ := rfl

set_option maxRecDepth 40000 in
/-- After 1000 steps from blank: state F, position −16 (Python cross-check). -/
theorem sanity1000 :
    steps 1000 init = some ⟨.F, -16,
      ⟨[true, false, true, false, true, false, true, false, true, false,
        true, false, true, false, true, false, true, false, true, false,
        true, true], false,
       [true, false, true, false, true, false, false, true, false, false,
        false, false, false, false, false, false, true, false, true, false,
        true, false, true, false, true, false, true, false, true, false,
        true, false, true, false, true, false, true, false, true, false,
        false, true]⟩⟩ := rfl

/-! ## §2 The periodic words. -/

/-- `(01)^j` as a list (`false` first). -/
def pow01 : Nat → List Bool
  | 0 => []
  | j + 1 => false :: true :: pow01 j

/-- `(10)^j` as a list (`true` first). -/
def pow10 : Nat → List Bool
  | 0 => []
  | j + 1 => true :: false :: pow10 j

/-- A `(01)` pair commutes past `(01)^j`. -/
theorem pow01_mid : ∀ (j : Nat) (X : List Bool),
    pow01 j ++ (false :: true :: X) = pow01 (j + 1) ++ X := by
  intro j
  induction j with
  | zero => intro X; rfl
  | succ j ih =>
    intro X
    show false :: true :: (pow01 j ++ (false :: true :: X))
        = false :: true :: (pow01 (j + 1) ++ X)
    rw [ih]

/-- A `(10)` pair commutes past `(10)^j`. -/
theorem pow10_mid : ∀ (j : Nat) (X : List Bool),
    pow10 j ++ (true :: false :: X) = pow10 (j + 1) ++ X := by
  intro j
  induction j with
  | zero => intro X; rfl
  | succ j ih =>
    intro X
    show true :: false :: (pow10 j ++ (true :: false :: X))
        = true :: false :: (pow10 (j + 1) ++ X)
    rw [ih]

theorem pow10_snoc (j : Nat) : pow10 (j + 1) = pow10 j ++ [true, false] := by
  have h := pow10_mid j []
  rw [List.append_nil] at h
  exact h.symm

/-- Reading `(10)^j 1` shifted one cell: `0 · (10)^j · 1 X = (01)^(j+1) X`. -/
theorem pow01_of_pow10 : ∀ (j : Nat) (X : List Bool),
    false :: (pow10 j ++ (true :: X)) = pow01 (j + 1) ++ X := by
  intro j
  induction j with
  | zero => intro X; rfl
  | succ j ih =>
    intro X
    show false :: true :: (false :: (pow10 j ++ (true :: X)))
        = false :: true :: (pow01 (j + 1) ++ X)
    rw [ih]

/-! ## §3 (L2) The sweep lemmas, for ARBITRARY length by 2-transition
induction (`PAPER_TEMPLATE_METHOD.md` §2.1). -/

/-- **Sweep lemma `B1F0`** (read-only rightward): from state `B` on a `1`
whose right context starts with `(01)^j`, the 2-cycle `B:1→1RF · F:0→0RB`
traverses the region in exactly `2j` steps, translating the head by `+2j`
and leaving the tape unchanged (the `(01)^j` block moves from the right
list to the left list intact).  Proven for every `j` by induction. -/
theorem sweepBF : ∀ (j : Nat) (p : Int) (L R : List Bool),
    steps (2 * j) ⟨.B, p, ⟨L, true, pow01 j ++ R⟩⟩
      = some ⟨.B, p + 2 * (j : Int), ⟨pow01 j ++ L, true, R⟩⟩ := by
  intro j
  induction j with
  | zero =>
    intro p L R
    exact congrArg some (cfgPos (by omega))
  | succ j ih =>
    intro p L R
    have hn : 2 * (j + 1) = 2 * j + 2 := by omega
    rw [hn]
    have h2 : steps (2 * j + 2) (⟨.B, p, ⟨L, true, pow01 (j + 1) ++ R⟩⟩ : Cfg)
        = steps (2 * j) ⟨.B, p + 1 + 1, ⟨false :: true :: L, true, pow01 j ++ R⟩⟩ := rfl
    rw [h2, ih (p + 1 + 1) (false :: true :: L) R, pow01_mid]
    exact congrArg some (cfgPos (by omega))

/-- **Sweep lemma `D1E0`** (leftward invert): from state `D` on a `1` whose
left context starts with `(01)^j` (reading leftward), the 2-cycle
`D:1→0LE · E:0→1LD` traverses it in exactly `2j` steps, translating the
head by `−2j` and INVERTING the block: `(01)^j` on the left becomes
`(10)^j` on the right.  Proven for every `j` by induction. -/
theorem sweepDE : ∀ (j : Nat) (p : Int) (L R : List Bool),
    steps (2 * j) ⟨.D, p, ⟨pow01 j ++ L, true, R⟩⟩
      = some ⟨.D, p - 2 * (j : Int), ⟨L, true, pow10 j ++ R⟩⟩ := by
  intro j
  induction j with
  | zero =>
    intro p L R
    exact congrArg some (cfgPos (by omega))
  | succ j ih =>
    intro p L R
    have hn : 2 * (j + 1) = 2 * j + 2 := by omega
    rw [hn]
    have h2 : steps (2 * j + 2) (⟨.D, p, ⟨pow01 (j + 1) ++ L, true, R⟩⟩ : Cfg)
        = steps (2 * j) ⟨.D, p - 1 - 1, ⟨pow01 j ++ L, true, true :: false :: R⟩⟩ := rfl
    rw [h2, ih (p - 1 - 1) L (true :: false :: R), pow10_mid]
    exact congrArg some (cfgPos (by omega))

/-! ## §4 (L3) The body lemma. -/

/-- The standalone body configuration
`B(k) = 0^∞ [E] (10)^k 1001 0^∞`, head (state `E`) on the leading `1`,
at absolute position `p`.  (`1·(01)^k·001 = (10)^k·1001`.) -/
def Bcfg (k : Nat) (p : Int) : Cfg :=
  ⟨.E, p, ⟨[], true, pow01 k ++ [false, false, true]⟩⟩

theorem Bcfg_congr {k l : Nat} {p q : Int} (hk : k = l) (hp : p = q) :
    Bcfg k p = Bcfg l q := by rw [hk, hp]

/-- Episode 1 (2 fixed steps): `E1 · A0` — turn at the left zone edge. -/
theorem intro2 (k : Nat) (p : Int) :
    steps 2 (Bcfg k p)
      = some ⟨.B, p - 1 + 1, ⟨[true], true, pow01 k ++ [false, false, true]⟩⟩ := rfl

/-- Episode 2 (8 fixed steps): `B1·F0·B0·C1·A0·B0·C0·A1` — the cap
crossing/rebuild at the right zone edge (crosses the old `1001` cap, writes
the two new zone cells, turns).  Parameter-independent: the left context
`L` is untouched (the landmark-pinning of the method, made literal). -/
theorem seam8 (p : Int) (L : List Bool) :
    steps 8 ⟨.B, p, ⟨L, true, [false, false, true]⟩⟩
      = some ⟨.D, p + 4,
          ⟨false :: true :: false :: true :: L, true, [false, true]⟩⟩ := by
  have h : steps 8 (⟨.B, p, ⟨L, true, [false, false, true]⟩⟩ : Cfg)
      = some ⟨.D, p + 1 + 1 + 1 + 1 + 1 + 1 - 1 - 1,
          ⟨false :: true :: false :: true :: L, true, [false, true]⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- Episode 3 (1 fixed step): `D1` — landing back on the (shifted) zone
start, re-entering state `E`. -/
theorem outro1 (p : Int) (R : List Bool) :
    steps 1 ⟨.D, p, ⟨[true], true, R⟩⟩
      = some ⟨.E, p - 1, ⟨[], true, false :: R⟩⟩ := rfl

/-- **The BODY LEMMA (L3), fully formal.**
`B(k) → B(k+2)` shifted one cell left, in exactly `4k + 15` steps, for
EVERY `k` — the composition prefix-episode(2) · `B1F0`-sweep(`2k`) ·
cap-episode(8) · `D1E0`-sweep(`2k+4`) · landing-episode(1) of
`o4_body_proof.py`, with the grid verification replaced by the sweep
inductions.  `some` output = halt-free = every B-reads-1 safe (halt gate).
The lab note claims odd `k ≥ 19`; the formal statement covers all
`k ≥ 0`. -/
theorem body_step (k : Nat) (p : Int) :
    steps (4 * k + 15) (Bcfg k p) = some (Bcfg (k + 2) (p - 1)) := by
  have hsplit : 4 * k + 15 = 2 + (2 * k + (8 + (2 * (k + 2) + 1))) := by omega
  rw [hsplit, steps_add, intro2, someBind, steps_add, sweepBF, someBind,
      steps_add, seam8, someBind]
  have hL : false :: true :: false :: true :: (pow01 k ++ [true])
      = pow01 (k + 2) ++ [true] := rfl
  rw [hL, steps_add, sweepDE, someBind, outro1]
  have hR : false :: (pow10 (k + 2) ++ [false, true])
      = pow01 (k + 2) ++ [false, false, true] := by
    have h1 : pow10 (k + 2) = pow10 (k + 1) ++ [true, false] := pow10_snoc (k + 1)
    rw [h1, List.append_assoc]
    exact pow01_of_pow10 (k + 1) [false, false, true]
  rw [hR]
  exact congrArg some (Bcfg_congr rfl (by omega))

/-- The paper's instance: at `k = 19` the body takes exactly 91 steps
(cross-check anchor of `o4_body_proof.py`). -/
example : steps 91 (Bcfg 19 0) = some (Bcfg 21 (-1)) := body_step 19 0

/-! ## §5 Corollaries: iterated body and standalone non-halting. -/

/-- Total step count of `r` body applications starting at zone size `k`. -/
def bodyTime : Nat → Nat → Nat
  | 0, _ => 0
  | r + 1, k => (4 * k + 15) + bodyTime r (k + 2)

/-- `r`-fold body application: `B(k) → B(k + 2r)` shifted `−r`, in exactly
`bodyTime r k` steps. -/
theorem body_iter : ∀ (r k : Nat) (p : Int),
    steps (bodyTime r k) (Bcfg k p) = some (Bcfg (k + 2 * r) (p - (r : Int))) := by
  intro r
  induction r with
  | zero =>
    intro k p
    exact congrArg some (Bcfg_congr (by omega) (by omega))
  | succ r ih =>
    intro k p
    have h1 : steps (bodyTime (r + 1) k) (Bcfg k p)
        = (steps (4 * k + 15) (Bcfg k p)).bind (steps (bodyTime r (k + 2))) :=
      steps_add (4 * k + 15) (bodyTime r (k + 2)) (Bcfg k p)
    rw [h1, body_step, someBind, ih (k + 2) (p - 1)]
    exact congrArg some (Bcfg_congr (by omega) (by omega))

/-- Strong induction on `Nat` (self-contained, no mathlib). -/
theorem strong_ind (P : Nat → Prop) (h : ∀ n, (∀ m, m < n → P m) → P n) :
    ∀ n, P n := by
  have key : ∀ N n, n < N → P n := by
    intro N
    induction N with
    | zero => intro n hn; exact absurd hn (Nat.not_lt_zero n)
    | succ N ihN =>
      intro n hn
      exact h n (fun m hm => ihN m (by omega))
  intro n
  exact key (n + 1) n (by omega)

/-- **Non-halting of the standalone body family (translated bouncer):**
from `B(k)` with blank left half-tape, o4 never halts — for every `n`,
`n` steps complete without reaching the halt transition.  (This decides
NOTHING about o4 from the blank tape: inside the real orbit the zone has a
non-blank left context, and reachability/the a-ledger stay open.) -/
theorem body_nonhalt : ∀ (n k : Nat) (p : Int), steps n (Bcfg k p) ≠ none := by
  apply strong_ind (fun n => ∀ (k : Nat) (p : Int), steps n (Bcfg k p) ≠ none)
  intro n ih k p
  by_cases hle : n ≤ 4 * k + 15
  · -- n is a prefix of one body pass, which completes: no halt inside it
    have hbody : steps (n + (4 * k + 15 - n)) (Bcfg k p) = some (Bcfg (k + 2) (p - 1)) := by
      have hs : n + (4 * k + 15 - n) = 4 * k + 15 := by omega
      rw [hs]
      exact body_step k p
    rw [steps_add] at hbody
    intro hnone
    rw [hnone, noneBind] at hbody
    cases hbody
  · -- peel one full body pass and recurse
    have hsplit : n = (4 * k + 15) + (n - (4 * k + 15)) := by omega
    rw [hsplit, steps_add, body_step, someBind]
    exact ih (n - (4 * k + 15)) (by omega) (k + 2) (p - 1)

/-! ## §6 (L4) The prefix lemma (parametric window) and the
`prefix · body^r` composition.

The real o4 milestone (observed on the blank-tape orbit at steps 731,
1548, … — the same orbit whose later milestones carry the ledger anchors
G = 275, 367, 494 …, a = 34, 38, 37 … of `O4_TEMPLATE_CLOSURE` §4) is

  `M(G, a) = 0^∞ [E] 0^G (10)^a 0 1 0^∞`   (head on the gap-left 0).

The PREFIX is a fixed 471-step word with span `[-11, 30]`, formalized in
parametric-window form: 30 explicit gap zeros suffice and everything
beyond is an arbitrary untouched suffix `Y`, which proves
(G, a)-uniformity for ALL `G ≥ 31`, all `a`, at once (the lab note claims
G ≥ 37; the window argument needs only `G ≥ 31`).  Then the body lemma
with explicit right context composes: `prefix · body^r` reaches the
suffix-entry configuration — everything of the generation except the
suffix itself. -/

/-- Position-shift equivariance, one step. -/
theorem step_shift (d : Int) (s : St) (p : Int) (l : List Bool) (hd : Bool)
    (r : List Bool) :
    step ⟨s, p + d, ⟨l, hd, r⟩⟩
      = (step ⟨s, p, ⟨l, hd, r⟩⟩).map (fun x => ⟨x.st, x.pos + d, x.tape⟩) := by
  cases s <;> cases hd <;> simp only [step, Option.map] <;>
    exact congrArg some (cfgPos (by omega))

/-- Position-shift equivariance: the dynamics is translation-invariant. -/
theorem steps_shift (d : Int) : ∀ (n : Nat) (s : St) (p : Int) (t : Tape),
    steps n ⟨s, p + d, t⟩
      = (steps n ⟨s, p, t⟩).map (fun x => ⟨x.st, x.pos + d, x.tape⟩) := by
  intro n
  induction n with
  | zero => intro s p t; rfl
  | succ n ih =>
    intro s p t
    obtain ⟨l, hd, r⟩ := t
    show (step ⟨s, p + d, ⟨l, hd, r⟩⟩).bind (steps n)
        = ((step ⟨s, p, ⟨l, hd, r⟩⟩).bind (steps n)).map
            (fun x => ⟨x.st, x.pos + d, x.tape⟩)
    rw [step_shift]
    cases step ⟨s, p, ⟨l, hd, r⟩⟩ with
    | none => rfl
    | some c' =>
      show steps n ⟨c'.st, c'.pos + d, c'.tape⟩
          = (steps n c').map (fun x => ⟨x.st, x.pos + d, x.tape⟩)
      obtain ⟨s', p', t'⟩ := c'
      exact ih s' p' t'

theorem replicate_split (m n : Nat) (b : Bool) :
    List.replicate (m + n) b = List.replicate m b ++ List.replicate n b := by
  induction m with
  | zero => rw [Nat.zero_add]; rfl
  | succ m ih =>
    have h : m + 1 + n = (m + n) + 1 := by omega
    rw [h]
    show b :: List.replicate (m + n) b
        = b :: (List.replicate m b ++ List.replicate n b)
    rw [ih]

/-- The body configuration with an explicit right context: `B(k)` followed
by an arbitrary word `Y` beyond its cap. -/
def BcfgCtx (k : Nat) (p : Int) (Y : List Bool) : Cfg :=
  ⟨.E, p, ⟨[], true, pow01 k ++ ([false, false, true] ++ Y)⟩⟩

theorem BcfgCtx_congr {k l : Nat} {p q : Int} {Y Z : List Bool}
    (hk : k = l) (hp : p = q) (hY : Y = Z) : BcfgCtx k p Y = BcfgCtx l q Z := by
  rw [hk, hp, hY]

/-- The real milestone `M(G, a)` at position `p` (head on the gap-left 0). -/
def Mcfg (G a : Nat) (p : Int) : Cfg :=
  ⟨.E, p, ⟨[], false, List.replicate (G - 1) false ++ (pow10 a ++ [false, true])⟩⟩

/-! ### The 471-step prefix word, kernel-checked in sixteen 30-step
symbolic chunks (a monolithic symbolic-tail `rfl` exceeds the elaborator's
`whnf` budget already at ~60 steps; 30-step chunks are cheap).  Each chunk
is a fixed step word over the concrete window content with the untouched
symbolic suffix `Y`, composed by `steps_add`; chunk statements generated
from the trace, every one checked by `rfl`. -/

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk0 (Y : List Bool) :
    steps 30 (⟨.E, 0, ⟨[], false, List.replicate 30 false ++ Y⟩⟩ : Cfg)
      = some ⟨.D, (-2 : Int), ⟨true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk1 (Y : List Bool) :
    steps 30 (⟨.D, (-2 : Int), ⟨true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.B, (-4 : Int), ⟨true :: ([] : List Bool), true, false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk2 (Y : List Bool) :
    steps 30 (⟨.B, (-4 : Int), ⟨true :: ([] : List Bool), true, false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.D, (-2 : Int), ⟨false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk3 (Y : List Bool) :
    steps 30 (⟨.D, (-2 : Int), ⟨false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.E, 10, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk4 (Y : List Bool) :
    steps 30 (⟨.E, 10, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.B, 6, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk5 (Y : List Bool) :
    steps 30 (⟨.B, 6, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.D, 0, ⟨false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk6 (Y : List Bool) :
    steps 30 (⟨.D, 0, ⟨false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.F, 14, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk7 (Y : List Bool) :
    steps 30 (⟨.F, 14, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.E, (-2 : Int), ⟨true :: false :: true :: false :: true :: true :: ([] : List Bool), false, false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk8 (Y : List Bool) :
    steps 30 (⟨.E, (-2 : Int), ⟨true :: false :: true :: false :: true :: true :: ([] : List Bool), false, false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.B, 14, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk9 (Y : List Bool) :
    steps 30 (⟨.B, 14, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.D, 4, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk10 (Y : List Bool) :
    steps 30 (⟨.D, 4, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.F, 6, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk11 (Y : List Bool) :
    steps 30 (⟨.F, 6, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.E, 18, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk12 (Y : List Bool) :
    steps 30 (⟨.E, 18, ⟨true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), false, false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.B, (-10 : Int), ⟨true :: ([] : List Bool), true, false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk13 (Y : List Bool) :
    steps 30 (⟨.B, (-10 : Int), ⟨true :: ([] : List Bool), true, false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.B, 20, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk14 (Y : List Bool) :
    steps 30 (⟨.B, 20, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, false :: true :: false :: true :: false :: false :: true :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.D, 10, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: Y⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem prefix_chunk15 (Y : List Bool) :
    steps 21 (⟨.D, 10, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: true :: ([] : List Bool), true, true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: Y⟩⟩ : Cfg)
      = some ⟨.E, (-11 : Int), ⟨([] : List Bool), true, false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: true :: Y⟩⟩ := rfl


/-- **The PREFIX LEMMA (L4), parametric-window form, base position.**
A fixed 471-step word: from the milestone head with >= 30 gap zeros ahead
and blank tape behind, o4 builds the fresh zone `(10)^19 1001` spanning
`[-11, 30]` and lands on its leading 1 in state `E` — with an ARBITRARY
suffix `Y` beyond cell 30 left untouched (the head reach is exactly 30:
no chunk ever pops `Y`).  Kernel-checked symbolic computation in 16
chunks; `Y` is never inspected, which is the formal (G, a)-uniformity. -/
theorem prefix471 (Y : List Bool) :
    steps 471 ⟨.E, 0, ⟨[], false, List.replicate 30 false ++ Y⟩⟩
      = some (BcfgCtx 19 (-11) Y) := by
  have hs : (471 : Nat) = 30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (30 + (21))))))))))))))) := rfl
  rw [hs, steps_add, prefix_chunk0, someBind, steps_add, prefix_chunk1, someBind, steps_add, prefix_chunk2, someBind, steps_add, prefix_chunk3, someBind, steps_add, prefix_chunk4, someBind, steps_add, prefix_chunk5, someBind, steps_add, prefix_chunk6, someBind, steps_add, prefix_chunk7, someBind, steps_add, prefix_chunk8, someBind, steps_add, prefix_chunk9, someBind, steps_add, prefix_chunk10, someBind, steps_add, prefix_chunk11, someBind, steps_add, prefix_chunk12, someBind, steps_add, prefix_chunk13, someBind, steps_add, prefix_chunk14, someBind, prefix_chunk15]
  rfl

/-- The prefix lemma at an arbitrary position (by shift equivariance). -/
theorem prefix471_at (p : Int) (Y : List Bool) :
    steps 471 ⟨.E, p, ⟨[], false, List.replicate 30 false ++ Y⟩⟩
      = some (BcfgCtx 19 (p - 11) Y) := by
  have h0 : (⟨.E, p, ⟨[], false, List.replicate 30 false ++ Y⟩⟩ : Cfg)
      = ⟨.E, 0 + p, ⟨[], false, List.replicate 30 false ++ Y⟩⟩ := cfgPos (by omega)
  rw [h0, steps_shift p 471 .E 0 ⟨[], false, List.replicate 30 false ++ Y⟩,
      prefix471 Y]
  have hmap : (some (BcfgCtx 19 (-11) Y)).map
        (fun x => (⟨x.st, x.pos + p, x.tape⟩ : Cfg))
      = some ⟨.E, -11 + p, ⟨[], true, pow01 19 ++ ([false, false, true] ++ Y)⟩⟩ := rfl
  rw [hmap]
  exact congrArg some (BcfgCtx_congr rfl (by omega) rfl)

/-- **Prefix from the milestone, for ALL `G ≥ 31`, all `a`, all positions.**
`M(G, a) → B(19)`-with-context in 471 steps; the remaining gap
(`G - 31` zeros), the filler `(10)^a` and the `01` cap are untouched. -/
theorem prefix_milestone (G a : Nat) (p : Int) (hG : 31 ≤ G) :
    steps 471 (Mcfg G a p)
      = some (BcfgCtx 19 (p - 11)
          (List.replicate (G - 31) false ++ (pow10 a ++ [false, true]))) := by
  have hrep : List.replicate (G - 1) false
      = List.replicate 30 false ++ List.replicate (G - 31) false := by
    rw [← replicate_split]
    congr 1
    omega
  show steps 471 ⟨.E, p, ⟨[], false,
      List.replicate (G - 1) false ++ (pow10 a ++ [false, true])⟩⟩ = _
  rw [hrep, List.append_assoc]
  exact prefix471_at p _







/-- Episode 2 with explicit right context (the three zeros the body
consumes from the gap): same 8 fixed steps, same landing. -/
theorem seam8_ctx (p : Int) (L Y : List Bool) :
    steps 8 ⟨.B, p, ⟨L, true, false :: false :: true :: false :: false :: false :: Y⟩⟩
      = some ⟨.D, p + 4,
          ⟨false :: true :: false :: true :: L, true, false :: true :: Y⟩⟩ := by
  have h : steps 8 (⟨.B, p, ⟨L, true,
        false :: false :: true :: false :: false :: false :: Y⟩⟩ : Cfg)
      = some ⟨.D, p + 1 + 1 + 1 + 1 + 1 + 1 - 1 - 1,
          ⟨false :: true :: false :: true :: L, true, false :: true :: Y⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- Episode 1 for an arbitrary right word (the 2 fixed steps never look
right of the head). -/
theorem intro2W (p : Int) (W : List Bool) :
    steps 2 ⟨.E, p, ⟨[], true, W⟩⟩
      = some ⟨.B, p - 1 + 1, ⟨[true], true, W⟩⟩ := rfl

/-- **The body lemma with context**: `B(k)` followed by three gap zeros and
an arbitrary untouched suffix `Y` — "the body consumes exactly 3 gap
cells per application" made literal. -/
theorem body_step_ctx (k : Nat) (p : Int) (Y : List Bool) :
    steps (4 * k + 15) (BcfgCtx k p (false :: false :: false :: Y))
      = some (BcfgCtx (k + 2) (p - 1) Y) := by
  have hsplit : 4 * k + 15 = 2 + (2 * k + (8 + (2 * (k + 2) + 1))) := by omega
  show steps (4 * k + 15) ⟨.E, p, ⟨[], true,
      pow01 k ++ ([false, false, true] ++ (false :: false :: false :: Y))⟩⟩ = _
  rw [hsplit, steps_add, intro2W, someBind, steps_add, sweepBF, someBind, steps_add]
  have hc : ([false, false, true] ++ (false :: false :: false :: Y) : List Bool)
      = false :: false :: true :: false :: false :: false :: Y := rfl
  rw [hc, seam8_ctx, someBind]
  have hL : false :: true :: false :: true :: (pow01 k ++ [true])
      = pow01 (k + 2) ++ [true] := rfl
  rw [hL, steps_add, sweepDE, someBind, outro1]
  have hR : false :: (pow10 (k + 2) ++ (false :: true :: Y))
      = pow01 (k + 2) ++ ([false, false, true] ++ Y) := by
    have h1 : pow10 (k + 2) = pow10 (k + 1) ++ [true, false] := pow10_snoc (k + 1)
    rw [h1, List.append_assoc]
    exact pow01_of_pow10 (k + 1) (false :: false :: true :: Y)
  rw [hR]
  exact congrArg some (BcfgCtx_congr rfl (by omega) rfl)

/-- Iterated body with context: `r` applications eat `3r` gap zeros. -/
theorem body_iter_ctx : ∀ (r k : Nat) (p : Int) (Y : List Bool),
    steps (bodyTime r k) (BcfgCtx k p (List.replicate (3 * r) false ++ Y))
      = some (BcfgCtx (k + 2 * r) (p - (r : Int)) Y) := by
  intro r
  induction r with
  | zero =>
    intro k p Y
    exact congrArg some (BcfgCtx_congr (by omega) (by omega) rfl)
  | succ r ih =>
    intro k p Y
    have h3 : 3 * (r + 1) = 3 + 3 * r := by omega
    rw [h3, replicate_split, List.append_assoc]
    have hc : List.replicate 3 false ++ (List.replicate (3 * r) false ++ Y)
        = false :: false :: false :: (List.replicate (3 * r) false ++ Y) := rfl
    rw [hc]
    have h1 : steps (bodyTime (r + 1) k)
          (BcfgCtx k p (false :: false :: false :: (List.replicate (3 * r) false ++ Y)))
        = (steps (4 * k + 15)
            (BcfgCtx k p (false :: false :: false :: (List.replicate (3 * r) false ++ Y)))).bind
            (steps (bodyTime r (k + 2))) :=
      steps_add (4 * k + 15) (bodyTime r (k + 2)) _
    rw [h1, body_step_ctx, someBind, ih (k + 2) (p - 1) Y]
    exact congrArg some (BcfgCtx_congr (by omega) (by omega) rfl)

/-- **The composition `prefix · body^r` (the generation, minus its
suffix):** from the milestone `M(G, a)`, for any `r` with `31 + 3r ≤ G`,
o4 reaches the zone `(10)^(19+2r) 1001` (head on its leading 1, state `E`)
with `G - 31 - 3r` gap zeros, the filler `(10)^a` and the `01` cap intact —
in exactly `471 + bodyTime r 19` steps, uniformly in `G`, `a`, `p`. -/
theorem prefix_bodies (G a r : Nat) (p : Int) (hG : 31 + 3 * r ≤ G) :
    steps (471 + bodyTime r 19) (Mcfg G a p)
      = some (BcfgCtx (19 + 2 * r) (p - 11 - (r : Int))
          (List.replicate (G - 31 - 3 * r) false ++ (pow10 a ++ [false, true]))) := by
  rw [steps_add, prefix_milestone G a p (by omega), someBind]
  have hY : List.replicate (G - 31) false
      = List.replicate (3 * r) false ++ List.replicate (G - 31 - 3 * r) false := by
    rw [← replicate_split]
    congr 1
    omega
  rw [hY, List.append_assoc]
  exact body_iter_ctx r 19 (p - 11) _



/-! ### The real-orbit anchor: o4 from blank reaches the exact milestone
form `M(43, 18)` at step 1548 (kernel-checked; the second milestone —
the first, `M(30, 12)` at step 731, has `G < 31`). -/

set_option maxRecDepth 62000 in
/-- o4 from blank is at `M(43, 18)` (position −42) at step 1548. -/
theorem real_milestone : steps 1548 init = some (Mcfg 43 18 (-42)) := rfl

/-- The real generation: blank tape → step 2431 = `M(43,18)` + prefix +
4 bodies = zone `(10)^27 1001` at −57, gap exhausted, filler `(10)^18`
and cap intact — the suffix-entry configuration, on the real orbit. -/
theorem real_generation :
    steps (1548 + (471 + bodyTime 4 19)) init
      = some (BcfgCtx 27 (-57) (pow10 18 ++ [false, true])) := by
  rw [steps_add, real_milestone, someBind,
      prefix_bodies 43 18 4 (-42) (by omega)]
  exact congrArg some (BcfgCtx_congr rfl (by omega) rfl)

/-! ## §7 Axiom audit (printed at every build) and `#eval` mirrors. -/

#print axioms sweepBF
#print axioms sweepDE
#print axioms body_step
#print axioms body_iter
#print axioms body_nonhalt
#print axioms body_step_ctx
#print axioms body_iter_ctx
#print axioms steps_shift
#print axioms prefix471
#print axioms prefix_milestone
#print axioms prefix_bodies
#print axioms real_milestone
#print axioms real_generation

#eval steps 100 init  -- cross-check vs template_crosscheck.py (N=100)
#eval decide (steps (4 * 251 + 15) (Bcfg 251 0) = some (Bcfg 253 (-1)))
  -- the k=251 red-team grid point, executed: expect true

end Template
