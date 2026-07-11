/-!
# The integer-×2 base-2 odometer machine — Lean 4 formalization (namespace `X2`)

Formalizes the frontier machine

  x2 = `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`  (blank tape),

mirroring the machine-formalization template of `Template.lean` / `O3.lean`
(zipper `St`/`Tape`/`Cfg`, `step`/`steps`/`steps_add`, sweep-by-induction).
Scope: the LOCAL even-structure channel — this file does NOT decide the global
non-halt (the open core).  Zero-mathlib, self-contained.

Layers (STRICT: FORMALIZED = `lake build` green + no `sorry` + axiom-audited):

* **L1 (the machine)** — `step`/`steps`: x2 as a step function on the tape
  zipper.  `step = none` iff HALT.  Reading the TNF spec carefully, the six
  fields are `A:1RB0RE · B:1RC--- · C:0LD1LE · D:0RE1LD · E:1RF0LC · F:0RA1RE`,
  so the ONLY halt transition is `B:1` (the `---`).  Kernel-`rfl` anchors at
  N = 50, 100 vs the exact Python simulator (`x2a_eraser.py` interpreter).

* **L2 (the halt gate, `halt_gate`)** — `step c = none ↔ (c.st = B ∧ head = 1)`,
  proved by cases on `(st, head)`.

* **L3 (the EVEN sweep — the target, `sweepEF`)** — the comb-REPACK, this
  machine's genuine even-structure channel: from state `E` on the leading `0`
  of a comb `(01)^m`, the 2-cycle `E:0→1RF · F:1→1RE` marches right, rewriting
  `(01)^m → 1^{2m}` in exactly `2m` steps, for EVERY `m`, by a one-tile base
  (`sweepEF_tile`, the 2-transition unit) + length induction — exactly the
  O3-`crawlR` / Template-`sweepBF` pattern.  KEY OUTPUT: the produced block has
  length `2*m` (EVEN for all `m`), captured as `sweepEF_even`.

* **L3′ (a second genuine sweep, `dSweepTurn`)** — the leftward `D`-sweep:
  `D:1→1LD` crosses a `1`-block of length `n+1` leftward and `D:0→0RE` turns it
  around into state `E` on the block's left edge, in `n+2` steps, arbitrary `n`
  by tile + induction (a self-contained crossing+turnaround, the `crawlL`
  analogue).

## Honest scope / relation to the arithmetic notes

The lab notes (`X2_ARITHMETIC_PROOF`, `X2_TEMPLATE_PROOF`, `x2a_eraser.py`)
describe an "`A1D0` eraser" 2-cycle `A:1→0LD · D:0→0LA` producing `(01)^j →
0^{2j}`.  **That 2-cycle is o4's (`Suffix.lean`'s `sweepAD`), NOT this
machine's** — here `A:1→0RE` and `D:0→0RE` both move RIGHT, and a brute-force
search confirms x2 has NO clean cell-zeroing uniform-crossing sweep.  The
even-gap stream `[2,4,4,6,8,…]` the Python `x2a_eraser.py` reports is an
EMERGENT parity of the full compound sweep on a boundary-contaminated isolated
comb (the script itself notes "the boundary differs, so the length is not the
in-context `2j`"), not a clean single-cycle lemma.  This machine's genuine,
cleanly-formalizable EVEN channel is the DUAL: the comb-repack `(01)^m → 1^{2m}`
(the base-2 doubling engine, `X2_TEMPLATE_PROOF` §1/§3.1), whose output length
`2m` is provably even for all `m`.  That is what `sweepEF` / `sweepEF_even`
formalize.

No `sorry`, no `native_decide`.  This file decides no machine; x2 stays `[OPEN]`.
-/

namespace X2

/-! ## §1 (L1) The machine x2. -/

/-- The six states of x2. -/
inductive St where
  | A | B | C | D | E | F
deriving DecidableEq, Repr

/-- Tape zipper (as in `Template.lean`): `left` = cells left of head
(nearest first), `head` = scanned cell, `right` = cells right of head
(nearest first); off-list cells are blank (`false`). -/
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

/-- One step of x2 = `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`.
`none` = HALT, which happens exactly when `B` reads `1` (the `---` field). -/
def step (c : Cfg) : Option Cfg :=
  match c.st, c.tape.head with
  | .A, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩   -- A0 → 1RB
  | .A, true  => some ⟨.E, c.pos + 1, mvR (wr c.tape false)⟩  -- A1 → 0RE
  | .B, false => some ⟨.C, c.pos + 1, mvR (wr c.tape true)⟩   -- B0 → 1RC
  | .B, true  => none                                          -- B1 → --- HALT
  | .C, false => some ⟨.D, c.pos - 1, mvL (wr c.tape false)⟩  -- C0 → 0LD
  | .C, true  => some ⟨.E, c.pos - 1, mvL (wr c.tape true)⟩   -- C1 → 1LE
  | .D, false => some ⟨.E, c.pos + 1, mvR (wr c.tape false)⟩  -- D0 → 0RE
  | .D, true  => some ⟨.D, c.pos - 1, mvL (wr c.tape true)⟩   -- D1 → 1LD
  | .E, false => some ⟨.F, c.pos + 1, mvR (wr c.tape true)⟩   -- E0 → 1RF
  | .E, true  => some ⟨.C, c.pos - 1, mvL (wr c.tape false)⟩  -- E1 → 0LC
  | .F, false => some ⟨.A, c.pos + 1, mvR (wr c.tape false)⟩  -- F0 → 0RA
  | .F, true  => some ⟨.E, c.pos + 1, mvR (wr c.tape true)⟩   -- F1 → 1RE

/-- `n` steps; `none` iff the machine halts strictly before completing them.
Hence `steps n c = some c'` certifies a halt-free (= all-safe) segment. -/
def steps : Nat → Cfg → Option Cfg
  | 0, c => some c
  | n + 1, c => (step c).bind (steps n)

theorem someBind {α β : Type} (a : α) (f : α → Option β) :
    (some a).bind f = f a := rfl

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

/-! ### L1 sanity: kernel-checked anchors vs the Python simulator. -/

/-- x2 on the blank tape. -/
def init : Cfg := ⟨.A, 0, ⟨[], false, []⟩⟩

set_option maxRecDepth 4000 in
/-- After 50 steps from blank: state D, position 4 (Python cross-check). -/
theorem sanity50 :
    steps 50 init = some ⟨.D, 4,
      ⟨[true, true, true, false, true, false], true,
       [true, true, false, false, true, false]⟩⟩ := rfl

set_option maxRecDepth 8000 in
/-- After 100 steps from blank: state A, position −2 (Python cross-check). -/
theorem sanity100 :
    steps 100 init = some ⟨.A, -2,
      ⟨[false, true, false], true,
       [false, true, false, true, false, true, false, true, false, false,
        true, false]⟩⟩ := rfl

/-! ## §2 (L2) The halt gate. -/

/-- **The halt gate.**  `x2` halts (`step c = none`) exactly when the head is in
state `B` reading a `1` — the `---` field of the TNF spec.  Every other
`(state, read)` pair steps.  Proved by cases on `(st, head)`. -/
theorem halt_gate (c : Cfg) :
    step c = none ↔ (c.st = .B ∧ c.tape.head = true) := by
  rcases c with ⟨st, pos, ⟨l, hd, r⟩⟩
  cases st <;> cases hd <;> simp [step]

/-! ## §3 The periodic words (machine-independent, mirroring `Template`). -/

/-- `(10)^j` (`true` first). -/
def pow10 : Nat → List Bool
  | 0 => []
  | j + 1 => true :: false :: pow10 j

/-- `n` `true`s. -/
def ones : Nat → List Bool
  | 0 => []
  | n + 1 => true :: ones n

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

/-- Moving a `true` left through a `ones` block. -/
theorem ones_append_true : ∀ (n : Nat) (R : List Bool),
    ones n ++ (true :: R) = ones (n + 1) ++ R := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show true :: (ones n ++ (true :: R)) = true :: (ones (n + 1) ++ R)
    rw [ih]

/-! ## §4 (L3) The EVEN sweep — the comb-repack `(01)^m → 1^{2m}`.

The genuine even-structure channel of x2 (the base-2 doubling engine): from
state `E` on the leading `0` of a comb `(01)^m 0`, the 2-cycle `E:0→1RF ·
F:1→1RE` marches right, rewriting the comb to a solid `1`-block of length `2m`,
depositing `ones (2m)` on the left and landing on the trailing `0`.  Arbitrary
length by one-tile base + induction. -/

/-- **One repack tile** (2 steps `E:0→1RF · F:1→1RE`): reads `[E] 0 1` (the
`(01)` pair, head on the `0`, right neighbour the paired `1`), writes both to
`1`, marches `+2`, depositing `1 1` on the left; the tail `X` is untouched.
`pow10 (m+1) ++ R = 1 0 · (pow10 m ++ R)` so the head re-lands on the next `0`.
Kernel `rfl`. -/
theorem sweepEF_tile (p : Int) (L X : List Bool) :
    steps 2 ⟨.E, p, ⟨L, false, true :: false :: X⟩⟩
      = some ⟨.E, p + 2, ⟨true :: true :: L, false, X⟩⟩ := by
  have h : steps 2 (⟨.E, p, ⟨L, false, true :: false :: X⟩⟩ : Cfg)
      = some ⟨.E, p + 1 + 1, ⟨true :: true :: L, false, X⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The comb-repack, ARBITRARY length (the eraser-even TARGET).**  `m` tiles =
`2m` steps take the comb `(01)^m` (encoded as head `0` with right `pow10 m ++ R`,
i.e. `0 (10)^m R`, the comb followed by its landing `0`) to a solid `1`-block
`ones (2m)` deposited on the left, shifting `+2m`, head on the trailing `0`,
`R` untouched.  Proven for EVERY `m` by tile + length induction (the
`Template.sweepBF` / `O3.crawlR` pattern).  `some` output ⇒ HALT-FREE. -/
theorem sweepEF : ∀ (m : Nat) (p : Int) (L R : List Bool),
    steps (2 * m) ⟨.E, p, ⟨L, false, pow10 m ++ R⟩⟩
      = some ⟨.E, p + 2 * (m : Int), ⟨ones (2 * m) ++ L, false, R⟩⟩ := by
  intro m
  induction m with
  | zero =>
    intro p L R
    show steps 0 _ = _
    exact congrArg some (cfgPos (by omega))
  | succ m ih =>
    intro p L R
    have hn : 2 * (m + 1) = 2 + 2 * m := by omega
    rw [hn, steps_add]
    show (steps 2 ⟨.E, p, ⟨L, false, true :: false :: (pow10 m ++ R)⟩⟩).bind
        (steps (2 * m)) = _
    rw [sweepEF_tile, someBind, ih (p + 2) (true :: true :: L) R]
    have hL : ones (2 * m) ++ (true :: true :: L) = ones (2 * (m + 1)) ++ L := by
      rw [ones_append_true, ones_append_true,
          show 2 * m + 1 + 1 = 2 * (m + 1) from by omega]
    rw [hL, ← hn]
    exact congrArg some (cfgPos (by push_cast; omega))

/-- **The even-length output, made explicit.**  The comb `(01)^m` is repacked
into a block of length exactly `2*m` — provably EVEN (`= 2 * m`) for every `m`.
This is the local "eraser-even" fact, [PROVEN, Lean]. -/
theorem sweepEF_even (m : Nat) (p : Int) (L R : List Bool) :
    ∃ len : Nat, len = 2 * m ∧
      steps (2 * m) ⟨.E, p, ⟨L, false, pow10 m ++ R⟩⟩
        = some ⟨.E, p + 2 * (m : Int), ⟨ones len ++ L, false, R⟩⟩ :=
  ⟨2 * m, rfl, sweepEF m p L R⟩

/-! ## §5 (L3′) The leftward `D`-sweep — a `1`-block crossing + turnaround.

`D:1→1LD` crosses a `1`-block leftward; at the block's left `0` boundary
`D:0→0RE` turns around into state `E` on the block's left edge.  A self-contained
uniform crossing (the `O3.crawlL` / `Template.sweepDE` analogue), arbitrary
block length by tile + induction. -/

/-- **The `D`-sweep + turnaround, ARBITRARY length.**  From state `D` on the
rightmost `1` of a block `1^{n+1}` (head `1`, then `ones n` on the left, then a
`0` boundary `false :: L`), `n + 2` steps cross the whole block leftward and
turn into state `E` on the block's leftmost `1`, shifting `−n`; the `1`-block is
preserved (re-emitted as `ones n` on the right), `L`/`R` untouched.  `some` ⇒
HALT-FREE.  Proven for every `n` by tile + induction. -/
theorem dSweepTurn : ∀ (n : Nat) (p : Int) (L R : List Bool),
    steps (n + 2) ⟨.D, p, ⟨ones n ++ (false :: L), true, R⟩⟩
      = some ⟨.E, p - (n : Int), ⟨false :: L, true, ones n ++ R⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p L R
    have h : steps (0 + 2) (⟨.D, p, ⟨ones 0 ++ (false :: L), true, R⟩⟩ : Cfg)
        = some ⟨.E, p - 1 + 1, ⟨false :: L, true, ones 0 ++ R⟩⟩ := rfl
    rw [h]
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ n ih =>
    intro p L R
    have hn : n + 1 + 2 = 1 + (n + 2) := by omega
    rw [hn, steps_add]
    show (steps 1 ⟨.D, p, ⟨true :: (ones n ++ (false :: L)), true, R⟩⟩).bind
        (steps (n + 2)) = _
    have h1 : steps 1 (⟨.D, p, ⟨true :: (ones n ++ (false :: L)), true, R⟩⟩ : Cfg)
        = some ⟨.D, p - 1, ⟨ones n ++ (false :: L), true, true :: R⟩⟩ := rfl
    rw [h1, someBind, ih (p - 1) L (true :: R), ones_append_true]
    exact congrArg some (cfgPos (by push_cast; omega))

/-! ## §5b (L3″) The cascade CHEW tile + fold — the doubling cascade's inductive core.

The doubling phase drives the base-2 cascade `… 0^2 1^{b} 0^2 …` down by a fixed
6-step tile `chew_tile` (state `D` on the first `0` of a `0^3` marker, reading two
`1`s of the block ahead): it shrinks the block by 2, deposits one `1 0` comb pair
on the left, and re-forms the `0^3` marker.  Composed by length induction
(`chewFold`) it drives a block `1^{2m+3}` down to `1^3` in `6m` steps, depositing
`pow10 m` — the `O3.crawlR` / `Suffix.sweepAD` pattern.  This is the cascade fold's
per-block inductive core: the `x2cc` executor's certified C1 lemma (proven ∀k,r
there), re-proven here as a Lean `rfl` tile + length induction — the piece the
Python AFFINE executor could not fold for a symbolic cascade (fixed-length run lists),
now tractable in Lean exactly as o3's `crawlR`.  `some` ⇒ HALT-FREE (no `E`-met
gap-3 anywhere in the chew). -/

/-- `pow10` is additive: `(10)^{a+b} = (10)^a · (10)^b`. -/
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

/-- **One chew tile** (6 steps `D0·E0·F0·A1·E1·C0`): head `D` on the first `0` of a
`0^3` marker with block `1^{b+2}` ahead (`0 0 · 1 1 · 1^b · 0 0 · R`); shrinks the
block to `1^b`, deposits `1 0` on the left, re-forms `0^3`, advances `+2`; `ones b`
and `R` untouched (read window is the marker + two leading `1`s).  Kernel `rfl`. -/
theorem chew_tile (p : Int) (b : Nat) (L R : List Bool) :
    steps 6 ⟨.D, p, ⟨L, false,
        false :: false :: true :: true :: (ones b ++ (false :: false :: R))⟩⟩
      = some ⟨.D, p + 2, ⟨true :: false :: L, false,
          false :: false :: (ones b ++ (false :: false :: R))⟩⟩ := by
  have h : steps 6 (⟨.D, p, ⟨L, false,
        false :: false :: true :: true :: (ones b ++ (false :: false :: R))⟩⟩ : Cfg)
      = some ⟨.D, p + 1 + 1 + 1 + 1 - 1 - 1, ⟨true :: false :: L, false,
          false :: false :: (ones b ++ (false :: false :: R))⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The chew fold, ARBITRARY length.**  `m` tiles = `6m` steps drive the block
`1^{2m+3}` down to `1^3`, depositing `pow10 m` on the left, advancing `+2m`; the
`0^3`/`0^2` markers and `R` are preserved.  Proven for every `m` by tile + length
induction.  `some` ⇒ HALT-FREE. -/
theorem chewFold : ∀ (m : Nat) (p : Int) (L R : List Bool),
    steps (6 * m) ⟨.D, p, ⟨L, false,
        false :: false :: (ones (2 * m + 3) ++ (false :: false :: R))⟩⟩
      = some ⟨.D, p + 2 * (m : Int), ⟨pow10 m ++ L, false,
          false :: false :: (ones 3 ++ (false :: false :: R))⟩⟩ := by
  intro m
  induction m with
  | zero =>
    intro p L R
    show steps 0 _ = _
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ m ih =>
    intro p L R
    have hn : 6 * (m + 1) = 6 + 6 * m := by omega
    rw [hn, steps_add]
    have hb : ones (2 * (m + 1) + 3) = true :: true :: ones (2 * m + 3) := by
      rw [show 2 * (m + 1) + 3 = 2 + (2 * m + 3) from by omega, ones_add]; rfl
    rw [hb]
    show (steps 6 ⟨.D, p, ⟨L, false,
        false :: false :: true :: true :: (ones (2 * m + 3) ++ (false :: false :: R))⟩⟩).bind
        (steps (6 * m)) = _
    rw [chew_tile, someBind, ih (p + 2) (true :: false :: L) R]
    have hL : pow10 m ++ (true :: false :: L) = pow10 (m + 1) ++ L := by
      rw [show (true :: false :: L) = pow10 1 ++ L from rfl, ← List.append_assoc,
          ← pow10_add]
    rw [hL]
    exact congrArg some (cfgPos (by push_cast; omega))

/-! ## §5c (G1) The cascade SEPARATOR-CROSS tile + the cascade FOLD over a
`List Nat` of non-uniform blocks — the doubling phase's variable-length list
induction, the exact piece the affine Python executor could NOT represent.

After `chewFold` grinds a cascade block `1^{2m+3}` down to `1^3`, the machine
must CROSS the `0^2` separator into the next block.  `sepCross_tile` (15 fixed
steps `D0·E1·C0·D1·E0·F0·A0·E0·F0·A0·E0·F0·A0·E1·C0`, kernel `rfl`) reads the
fixed window `0^3 1^3 0^2 1^2` (the marker, the ground-down `1^3`, the separator,
and the first two `1`s of the NEXT block), deposits the comb pattern
`(01)^2 0^2 1` on the left, shifts `+7`, and re-forms `[D] 0^3 …` sitting on the
next block — which it trims by 2 (`1^{2s+5} → 1^{2s+3}`).  Composing
`chewFold m · sepCross_tile` gives the per-block step `blockStep`
(`= x2co_compose.py`'s certified `L1`, here a Lean tile+fold).  `cascadeFold`
then ITERATES `blockStep` over an arbitrary `List Nat bs` of block sizes by LIST
INDUCTION (the o4 `prefix_bodies` / o3 `body_iter` analogue): this is `G1` of
`X2_COMPOSITION_2026-07-11.md` — the fold the `x2cc` fixed-length-run executor
provably cannot express (block entry sizes `61,29,13,5,1` are all distinct, no
uniform `config(p)→config(p−1)` shift).  Every step lands `some` ⇒ HALT-FREE (the
`E`-met gap-3 halt gate never fires anywhere in the whole cascade). -/

/-- **The separator-cross tile** (15 steps): from state `D` on the first `0` of a
`0^3` marker, with the ground-down block `1^3`, the `0^2` separator, and the next
block's first two `1`s ahead (`0 0 · 1 1 1 · 0 0 · 1 1 · X`), the head crosses into
the next block, deposits `1 0 0 1 0 1 0` (nearest-first, `= (01)^2 0^2 1`) on the
left, advances `+7`, and re-forms `[D] 0^3 …` on the next block with its first two
`1`s consumed; `X` (the rest of the next block) is untouched.  Kernel `rfl`. -/
theorem sepCross_tile (p : Int) (L X : List Bool) :
    steps 15 ⟨.D, p, ⟨L, false,
        false :: false :: true :: true :: true :: false :: false :: true :: true :: X⟩⟩
      = some ⟨.D, p + 7,
          ⟨true :: false :: false :: true :: false :: true :: false :: L, false,
           false :: false :: X⟩⟩ := by
  have h : steps 15 (⟨.D, p, ⟨L, false,
        false :: false :: true :: true :: true :: false :: false :: true :: true :: X⟩⟩ : Cfg)
      = some ⟨.D, p + 1 + 1 + 1 + 1 - 1 - 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 - 1 - 1,
          ⟨true :: false :: false :: true :: false :: true :: false :: L, false,
           false :: false :: X⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The per-block cascade step** `blockStep m s` (`6m + 15` steps): grind the
current block `1^{2m+3}` down to `1^3` (`chewFold`, depositing `pow10 m`), then
cross the separator into the next block `1^{2s+5}` (`sepCross_tile`), leaving it
as `1^{2s+3}` with `[D] 0^3` re-formed and the deposit `(01)^2 0^2 1 · (10)^m`
grown on the left; `T` (everything past the next block's trailing `0^2`) is
untouched.  This is `x2co_compose.py`'s `L1`, mechanized as a Lean composite.
`some` ⇒ HALT-FREE. -/
theorem blockStep (m s : Nat) (p : Int) (L T : List Bool) :
    steps (6 * m + 15) ⟨.D, p, ⟨L, false,
        false :: false :: (ones (2 * m + 3)
          ++ (false :: false :: (ones (2 * s + 5) ++ (false :: false :: T))))⟩⟩
      = some ⟨.D, p + 2 * (m : Int) + 7,
          ⟨(true :: false :: false :: true :: false :: true :: false :: pow10 m) ++ L, false,
           false :: false :: (ones (2 * s + 3) ++ (false :: false :: T))⟩⟩ := by
  rw [steps_add, chewFold m p L (ones (2 * s + 5) ++ (false :: false :: T)), someBind]
  have h5 : ones (2 * s + 5) = true :: true :: ones (2 * s + 3) := by
    rw [show 2 * s + 5 = 2 + (2 * s + 3) from by omega, ones_add]; rfl
  rw [h5]
  show steps 15 ⟨.D, p + 2 * (m : Int), ⟨pow10 m ++ L, false,
      false :: false :: true :: true :: true :: false :: false :: true :: true
        :: (ones (2 * s + 3) ++ (false :: false :: T))⟩⟩ = _
  rw [sepCross_tile]
  exact congrArg some (cfgPos (by omega))

/-- The raw cascade tail as a function of a block-size list: each block `a` is
stored `1^{2a+5}` and separated by `0^2`, terminating in the opaque word `T`. -/
def casc : List Nat → List Bool → List Bool
  | [], T => T
  | a :: rest, T => ones (2 * a + 5) ++ (false :: false :: casc rest T)

/-- The size of the block the fold lands on after consuming the whole list. -/
def lastBlock (m : Nat) : List Nat → Nat
  | [] => m
  | a :: rest => lastBlock a rest

/-- Total step count of the fold: `Σ (6·(block) + 15)` down the list. -/
def foldTime (m : Nat) : List Nat → Nat
  | [] => 0
  | a :: rest => (6 * m + 15) + foldTime a rest

/-- **THE CASCADE FOLD (G1), variable-length LIST INDUCTION.**  Starting in
state `D` on the marker `0^3` of a block `1^{2m+3}` whose cascade tail is
`casc bs T` (an arbitrary, NON-UNIFORM list `bs` of further blocks), the machine
runs `foldTime m bs` steps and lands in state `D` on the final block
`1^{2·lastBlock+3}` sitting directly on the terminator `T`, with the whole cascade
folded into a comb deposited on the left.  Proven for EVERY list `bs` by List
induction on `bs` (base = 0 steps; step = `blockStep` then the IH), each step
`some` ⇒ the entire cascade traversal is HALT-FREE.  This is the fold the affine
executor could not represent; in Lean it is a routine `List` recursion whose
inductive STEP (`blockStep`) is a kernel composite. -/
theorem cascadeFold : ∀ (bs : List Nat) (m : Nat) (p : Int) (L T : List Bool),
    ∃ (comb : List Bool) (q : Int),
      steps (foldTime m bs) ⟨.D, p, ⟨L, false,
          false :: false :: (ones (2 * m + 3) ++ (false :: false :: casc bs T))⟩⟩
        = some ⟨.D, q, ⟨comb ++ L, false,
            false :: false :: (ones (2 * lastBlock m bs + 3)
              ++ (false :: false :: T))⟩⟩ := by
  intro bs
  induction bs with
  | nil =>
    intro m p L T
    exact ⟨[], p, by
      show steps 0 _ = _
      rfl⟩
  | cons a rest ih =>
    intro m p L T
    obtain ⟨comb', q', hIH⟩ := ih a (p + 2 * (m : Int) + 7)
      ((true :: false :: false :: true :: false :: true :: false :: pow10 m) ++ L) T
    refine ⟨comb' ++ (true :: false :: false :: true :: false :: true :: false :: pow10 m),
        q', ?_⟩
    show steps ((6 * m + 15) + foldTime a rest) ⟨.D, p, ⟨L, false,
        false :: false :: (ones (2 * m + 3)
          ++ (false :: false :: (ones (2 * a + 5) ++ (false :: false :: casc rest T))))⟩⟩ = _
    rw [steps_add, blockStep m a p L (casc rest T), someBind, hIH, List.append_assoc]
    rfl

/-! ## §5d (G3, arithmetic core) The big-block doubling identity in `2^K`.

The milestone big block is `B_K = 2^K − 3`; the doubling phase's register-rebuild
must equate the rebuilt block to `B_{K+1} = 2^{K+1} − 3`, i.e. prove
`2·B_K + 3 = B_{K+1}` — exponential (`2^K`) arithmetic that the affine Python
executor provably could NOT represent (`X2_COMPOSITION` §3, G3).  In Lean's `Nat`
it is a two-line fact.  This formalizes the *arithmetic core* of G3 (the
"couples-to-`2^K`" identity); it does NOT by itself close G3 — wiring it to the
`cascadeFold` output (proving the accumulated comb-total equals `B_K`, so the
repack yields exactly `B_{K+1}`) is the part that remains open (see the honest
scope note at the foot of this file). -/

/-- `4 ≤ 2^{k+2}` for every `k` (so the truncated `Nat` subtraction below is exact). -/
theorem four_le_two_pow : ∀ k, 4 ≤ 2 ^ (k + 2) := by
  intro k
  induction k with
  | zero => decide
  | succ k ih =>
    have e : 2 ^ (k + 1 + 2) = 2 ^ (k + 2) * 2 := by
      rw [show k + 1 + 2 = (k + 2) + 1 from by omega]; exact Nat.pow_succ 2 (k + 2)
    rw [e]; omega

/-- **The big-block doubling identity** `2·(2^K − 3) + 3 = 2^{K+1} − 3` (all
`K = k + 2 ≥ 2`): the register-rebuild's exponential-arithmetic obligation, the
`B → 2B + 3` doubling law of the base-2 odometer, PROVEN in Lean's `2^K` `Nat`
arithmetic — the representation the affine executor lacked. -/
theorem doubling_id (k : Nat) :
    2 * (2 ^ (k + 2) - 3) + 3 = 2 ^ (k + 2 + 1) - 3 := by
  have h := four_le_two_pow k
  have e : 2 ^ (k + 2 + 1) = 2 ^ (k + 2) * 2 := Nat.pow_succ 2 (k + 2)
  rw [e]; omega

/-! ## §5e (G3 WIRING) The milestone cascade as a concrete `List Nat`,
`cascadeFold` instantiated at it, the accumulator SUM lemma, and the
doubling-phase transport (with the still-open pieces as explicit hypotheses).

This section carries out the G3-wiring program:
1. `cascadeBlocks K` — the milestone `M(K)` cascade's WAITING-block sizes in the
   fold's `a`-convention (each waiting block is stored `1^{2a+5}`).  The milestone
   cascade is `1^{big} 0^2 1^{2^{K-1}-3} 0^2 ⋯ 0^2 1^{2^2-3}` with leading
   `big = 2^K − 3 = 2·(2^{K-1}−3) + 3`; the waiting blocks `2^j−3` map to
   `a = 2^{j-1} − 4` (representable exactly for `j ≥ 3`).
2. `cascade_traversal` — `cascadeFold` at `cascadeBlocks K`, halt-free (immediate
   from G1).
3. `cascadeBlocks_sum` — the accumulator/`Σ` closed form (`Σ = 2^{K-1} − 4K + 8`),
   proved by List/Nat induction (the "Σ blocks → closed form" step; mirrors the way
   `Suffix.lean` equates o4's accumulated filler to the odometer register).
4. `doubling_transport` — the doubling-phase transport assembled from (2), taking
   the low-phase/entry and the G2 repack as NAMED hypotheses (to be discharged
   later), so the structural G3 result stands alone.

**HONEST BOUNDARIES (the exact obstructions, see the §7 note):**
* the terminal `1^1` (`= 2^2−3`, `j=2`) block is NOT fold-representable
  (`2a+5 = 1 ⟹ a = −2`); it necessarily sits in the opaque tail `T`.  So the fold
  processes the cascade blocks `j = K-1 … 3` only.
* `cascadeFold` lands on `1^{2·lastBlock+3}` — the LAST block ground down — NOT on
  `1^{2·acc+3}` for an accumulated `acc`; the repack that would fuse the deposited
  comb into a single `1^{2·acc}` big block is a SEPARATE G2 episode, absent here.
* the cascade accumulator is `Σ ≈ 2^{K-1}`, so `2·Σ + 3 ≠ 2^{K+1} − 3` (checked by
  `#eval` below).  The genuine `2^K` doubling `2·(2^K−3)+3 = 2^{K+1}−3` is
  `doubling_id`, which applies to the BIG-BLOCK marked-sweep episode (G2), NOT to
  the cascade fold.  Hence the "accumulator = 2^K via `doubling_id`" identity as
  originally posed does NOT hold; `doubling_id` is the big-block episode's law. -/

/-- Sum of a `List Nat` (the fold accumulator's arithmetic support). -/
def natSum : List Nat → Nat
  | [] => 0
  | a :: r => a + natSum r

/-- The cascade waiting-blocks in the fold `a`-convention: `n` blocks with
descending exponents `hi, hi−1, …, hi−n+1`, block `a`-value `2^i − 4` (so the
stored block length is `2·(2^i−4)+5 = 2^{i+1}−3`). -/
def cascDesc : Nat → Nat → List Nat
  | 0, _ => []
  | n + 1, hi => (2 ^ hi - 4) :: cascDesc n (hi - 1)

/-- **The milestone `M(K)` cascade** (representable waiting blocks): exponents
`i = K−2 … 2`, i.e. block lengths `2^{i+1}−3 = 2^{K-1}−3, …, 2^3−3 = 5` — the
`K−3` blocks `j = K−1 … 3` of the milestone.  The leading big block `2^K−3` is the
fold's CURRENT block `m = 2^{K-1}−3` (not in this list), and the terminal `1^1`
(`j=2`) is in the tail `T` (not fold-representable). -/
def cascadeBlocks (K : Nat) : List Nat := cascDesc (K - 3) (K - 2)

/-- **The accumulator SUM lemma (the "Σ blocks → closed form" core).**  For every
`n ≤ hi−1`, the fold `a`-values `2^{hi}−4, …, 2^{hi−n+1}−4` sum to
`2^{hi+1} − 2^{hi−n+1} − 4n`, written additively (no `Nat` truncation) as
`Σ + 4n + 2^{hi−n+1} = 2^{hi+1}`.  Proved by induction on `n` (the geometric
telescoping); the exponent `hi−n+1` is the invariant bottom of the block range. -/
theorem cascDesc_sum : ∀ (n hi : Nat), n + 1 ≤ hi →
    natSum (cascDesc n hi) + 4 * n + 2 ^ (hi - n + 1) = 2 ^ (hi + 1) := by
  intro n
  induction n with
  | zero =>
    intro hi _
    show natSum ([] : List Nat) + 4 * 0 + 2 ^ (hi - 0 + 1) = 2 ^ (hi + 1)
    show 0 + 4 * 0 + 2 ^ (hi - 0 + 1) = 2 ^ (hi + 1)
    rw [show hi - 0 + 1 = hi + 1 from by omega]; omega
  | succ n ih =>
    intro hi h
    show (2 ^ hi - 4) + natSum (cascDesc n (hi - 1)) + 4 * (n + 1)
        + 2 ^ (hi - (n + 1) + 1) = 2 ^ (hi + 1)
    have IH := ih (hi - 1) (by omega)
    rw [show (hi - 1) - n + 1 = hi - (n + 1) + 1 from by omega,
        show (hi - 1) + 1 = hi from by omega] at IH
    have hpow : 2 ^ (hi + 1) = 2 ^ hi * 2 := Nat.pow_succ 2 hi
    have h4 : 4 ≤ 2 ^ hi := by
      have := four_le_two_pow (hi - 2)
      rwa [show hi - 2 + 2 = hi from by omega] at this
    omega

/-- **The closed form for the milestone cascade** (`K ≥ 3`):
`Σ cascadeBlocks K = 2^{K-1} − 4·(K−3) − 4 = 2^{K-1} − 4K + 8`.  The accumulated
comb sum is `Θ(2^{K-1})` — visibly NOT the big-block value `2^K−3` nor the rebuilt
`2^{K+1}−3`; this is the arithmetic witness that the cascade fold does not itself
carry the `2^K` doubling. -/
theorem cascadeBlocks_sum (K : Nat) (hK : 3 ≤ K) :
    natSum (cascadeBlocks K) + 4 * (K - 3) + 4 = 2 ^ (K - 1) := by
  unfold cascadeBlocks
  have h := cascDesc_sum (K - 3) (K - 2) (by omega)
  rw [show (K - 2) - (K - 3) + 1 = 2 from by omega,
      show (K - 2) + 1 = K - 1 from by omega,
      show (2 : Nat) ^ 2 = 4 from by decide] at h
  omega

/-- **The cascade traversal (G1 instantiated at the real milestone cascade).**
`cascadeFold` at `cascadeBlocks K`, starting from state `D` on the leading big
block `1^{2·(2^{K-1}−3)+3} = 1^{2^K−3}`, runs `foldTime (2^{K-1}−3) (cascadeBlocks K)`
steps HALT-FREE (`some`) and lands in state `D` on the ground block
`1^{2·lastBlock+3}` with the whole cascade folded into a comb on the left.
Immediate from `cascadeFold`; this is the doubling-phase's cascade sweep over the
CONCRETE milestone block list. -/
theorem cascade_traversal (K : Nat) (p : Int) (L T : List Bool) :
    ∃ (comb : List Bool) (q : Int),
      steps (foldTime (2 ^ (K - 1) - 3) (cascadeBlocks K)) ⟨.D, p, ⟨L, false,
          false :: false :: (ones (2 * (2 ^ (K - 1) - 3) + 3)
            ++ (false :: false :: casc (cascadeBlocks K) T))⟩⟩
        = some ⟨.D, q, ⟨comb ++ L, false,
            false :: false :: (ones (2 * lastBlock (2 ^ (K - 1) - 3) (cascadeBlocks K) + 3)
              ++ (false :: false :: T))⟩⟩ :=
  cascadeFold (cascadeBlocks K) (2 ^ (K - 1) - 3) p L T

/-- **The doubling-phase transport (structural G3), with the still-open pieces as
NAMED hypotheses.**  Given (`H_entry`) that the low phase + entry (`[OPEN]`,
STILL-OPEN item 1/2) reach the cascade-start config — state `D` on the leading
`1^{2^K−3}` big block with cascade tail `casc (cascadeBlocks K) T` — and
(`H_repack`) that the G2 repack episode (`[OPEN]`, STILL-OPEN item 2) carries the
ground cascade config to the next milestone `M1next`, the doubling phase reaches
`M1next` HALT-FREE.  The proof genuinely composes `H_entry`, the proven
`cascade_traversal` (G1), and `H_repack` via `steps_add`; the big-block value the
repack must target is `2^{K+1}−3 = 2·(2^K−3)+3` by `doubling_id` (its `2^K` law).
No `cascadeFold`/`doubling_id` step is assumed — only entry and repack, the pieces
this file does not yet formalize. -/
theorem doubling_transport (K : Nat) (p : Int) (L T : List Bool)
    (entryCfg : Cfg) (Nentry : Nat)
    (H_entry : steps Nentry entryCfg = some ⟨.D, p, ⟨L, false,
        false :: false :: (ones (2 * (2 ^ (K - 1) - 3) + 3)
          ++ (false :: false :: casc (cascadeBlocks K) T))⟩⟩)
    (Nrepack : Nat) (M1next : List Bool → Int → Cfg)
    (H_repack : ∀ (comb : List Bool) (q : Int),
        steps Nrepack ⟨.D, q, ⟨comb ++ L, false,
            false :: false :: (ones (2 * lastBlock (2 ^ (K - 1) - 3) (cascadeBlocks K) + 3)
              ++ (false :: false :: T))⟩⟩
          = some (M1next comb q)) :
    ∃ (N : Nat) (comb : List Bool) (q : Int),
      steps N entryCfg = some (M1next comb q) := by
  obtain ⟨comb, q, hfold⟩ := cascade_traversal K p L T
  refine ⟨Nentry + (foldTime (2 ^ (K - 1) - 3) (cascadeBlocks K) + Nrepack), comb, q, ?_⟩
  rw [steps_add, H_entry, someBind, steps_add, hfold, someBind, H_repack]

/-! ## §5f (G2) THE BIG-BLOCK `(10)^10`-MARKED SWEEP — extracted from the raw g=2..6
traces, formalized as an arbitrary-length parametric lemma.

**What the episode ACTUALLY is (extracted cell-for-cell from the raw x2 machine,
NOT from prose).**  In the doubling phase (M6→M1(g+1)) the head enters state `D` on
the first `0` of a fixed marker `0^3 (10)^10` sitting immediately left of the leading
big block `1^{2v+1}` (in M6 the big block carries the constant `(10)^10` marker; the
marker length `10` comes from the `1 0^10` even-parity tail `T_g` of the M1 template
and is `K`-INDEPENDENT — verified g=2..8).  From there the machine runs a UNIFORM
`4·10+6 = 46`-step R/L cycle that:

* sweeps RIGHT across the whole `(10)^10` marker (24 R-moves) into the block's first
  two `1`s, then sweeps back LEFT (22 L-moves), net `+2`;
* deposits one `1 0` (`pow10 1`) comb pair on the LEFT of the marker;
* shrinks the block by exactly `2` (`1^{2v+1} → 1^{2v-1}`);
* leaves the `0^3 (10)^10` marker PRESERVED and the tail untouched.

Iterated `v` times (length induction, the `chewFold` pattern) this grinds the big
block `1^{2v+1}` down to `1^1`, depositing `pow10 v` — the `markedChew` fold below.
A final fixed `29`-step `markedTurn` repacks the exhausted `(10)^10 1^1` into a solid
`1^{21} = 1^{2·10+1}` block and crosses the `0^2` separator into the next block,
trimming it by `2`.  `markedBlock` composes the two.  Every step lands `some` ⇒ the
whole marked sweep is HALT-FREE (the `E`-met gap-3 gate never fires).

**HONEST verdict on the ×2 doubling (the framing scrutinised, per the task).**  This
episode is the block→COMB CHEW, **not** the ×2 doubling.  With the milestone value
`2v+1 = B_K = 2^K − 3` (so `v = 2^{K-1} − 2`) the sweep outputs the comb `pow10 v`
(whose eventual `sweepEF` repack is `1^{2v} = 1^{2^K − 4}`) PLUS a fixed `1^{21}`
residue and a next-block trim — it does NOT emit the doubled solid block
`1^{2^{K+1}−3}`.  So `doubling_id`'s `2·(2^K−3)+3 = 2^{K+1}−3` is the milestone
ARITHMETIC law, but it is realised only by the FULL compound (this chew, THEN the
comb repack, THEN the register/cascade recombination carrying the `−4K+8` correction),
not by the marked sweep in isolation (`marked_not_doubling` below records the exact
off-by arithmetic `2·(2^{K-1}−2) = 2^K − 4 ≠ 2^{K+1}−3`).  `H_repack` of
`doubling_transport` is therefore NOT discharged by this lemma: `H_repack` is the
DISTINCT post-cascade repack episode, and even the big-block sweep only performs the
chew half of the ×2.  What IS lifted to all lengths here: the marked sweep's SAFETY
and STRUCTURAL transport (the G2 engine), halt-free ∀v. -/

set_option maxRecDepth 4000 in
/-- **One `(10)^10`-marked chew tile** (46 steps): head `D` on the first `0` of the
marker `0^3 (10)^10`, block `1^{b+2}` ahead; sweeps across the marker and back,
depositing `1 0` on the left, shrinking the block to `1^b`, marker + tail (`ones b`,
`R`) preserved, advancing `+2`.  Kernel `rfl` (the fixed 46-step window
`0^3 (10)^10 1 1`; `ones b`/`R` never read).  Extracted from the raw traces. -/
theorem markedChew_tile (p : Int) (b : Nat) (L R : List Bool) :
    steps 46 ⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (true :: true :: (ones b ++ (false :: false :: R))))⟩⟩
      = some ⟨.D, p + 2, ⟨true :: false :: L, false,
          false :: false :: (pow10 10 ++ (ones b ++ (false :: false :: R)))⟩⟩ := by
  have h : steps 46 (⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (true :: true :: (ones b ++ (false :: false :: R))))⟩⟩ : Cfg)
      = some ⟨.D, p + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1
              + 1 + 1 + 1 + 1 + 1 + 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1
              - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1,
          ⟨true :: false :: L, false,
           false :: false :: (pow10 10 ++ (ones b ++ (false :: false :: R)))⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The `(10)^10`-marked chew fold, ARBITRARY block length.**  `v` tiles = `46v`
steps grind the big block `1^{2v+1}` down to `1^1`, depositing the comb `pow10 v` on
the left, advancing `+2v`; the marker `0^3 (10)^10` and the tail `R` are preserved.
Proven for EVERY `v` by tile + length induction (the `chewFold`/`O3.crawlR` pattern).
`some` ⇒ HALT-FREE.  This is the G2 big-block marked sweep as a parametric lemma. -/
theorem markedChew : ∀ (v : Nat) (p : Int) (L R : List Bool),
    steps (46 * v) ⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (ones (2 * v + 1) ++ (false :: false :: R)))⟩⟩
      = some ⟨.D, p + 2 * (v : Int), ⟨pow10 v ++ L, false,
          false :: false :: (pow10 10 ++ (ones 1 ++ (false :: false :: R)))⟩⟩ := by
  intro v
  induction v with
  | zero =>
    intro p L R
    show steps 0 _ = _
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ v ih =>
    intro p L R
    have hn : 46 * (v + 1) = 46 + 46 * v := by omega
    rw [hn, steps_add]
    have hb : ones (2 * (v + 1) + 1) = true :: true :: ones (2 * v + 1) := by
      rw [show 2 * (v + 1) + 1 = 2 + (2 * v + 1) from by omega, ones_add]; rfl
    rw [hb]
    show (steps 46 ⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (true :: true :: (ones (2 * v + 1)
          ++ (false :: false :: R))))⟩⟩).bind (steps (46 * v)) = _
    rw [markedChew_tile, someBind, ih (p + 2) (true :: false :: L) R]
    have hL : pow10 v ++ (true :: false :: L) = pow10 (v + 1) ++ L := by
      rw [show (true :: false :: L) = pow10 1 ++ L from rfl, ← List.append_assoc, ← pow10_add]
    rw [hL]
    exact congrArg some (cfgPos (by push_cast; omega))

set_option maxRecDepth 4000 in
/-- **The marked-sweep TURN/repack tile** (29 steps): once the big block is ground to
`1^1`, the head reads the exhausted `(10)^10 1^1 0^2` marker + the next block's first
two `1`s (`1^{n+2}`) and REPACKS the marker into a solid `1^{21} = 1^{2·10+1}` block,
deposits `0^2 1 0` on the left, crosses into the next block trimming it by `2`
(`1^{n+2} → 1^n`), landing `[D]` on a fresh `0^3`, advancing `+25`; the tail
`ones n`/`T` are preserved.  Kernel `rfl` (fixed 29-step window).  Extracted raw. -/
theorem markedTurn (p : Int) (n : Nat) (L T : List Bool) :
    steps 29 ⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (true :: false :: false ::
          (true :: true :: (ones n ++ (false :: false :: T)))))⟩⟩
      = some ⟨.D, p + 25, ⟨ones 21 ++ (false :: false :: true :: false :: L), false,
          false :: false :: (ones n ++ (false :: false :: T))⟩⟩ := by
  have h : steps 29 (⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (true :: false :: false ::
          (true :: true :: (ones n ++ (false :: false :: T)))))⟩⟩ : Cfg)
      = some ⟨.D, p + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1
              + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 - 1 - 1,
          ⟨ones 21 ++ (false :: false :: true :: false :: L), false,
           false :: false :: (ones n ++ (false :: false :: T))⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **THE FULL BIG-BLOCK MARKED SWEEP** `markedBlock v s` (`46v + 29` steps):
`markedChew` (grind `1^{2v+1}` to `1^1`, deposit `pow10 v`) then `markedTurn` (repack
`(10)^10 1^1` into `1^{21}`, cross into the next block `1^{2s+3}` leaving `1^{2s+1}`).
Net: the big block `1^{2v+1}` and its marker become the comb-and-residue deposit
`1^{21} 0^2 (10) (10)^v` on the left, the head re-forms `[D] 0^3` on the trimmed next
block, `T` untouched.  Proven ∀v,s, `some` ⇒ HALT-FREE.  This is the extracted G2
episode, lifted to all block lengths. -/
theorem markedBlock (v s : Nat) (p : Int) (L T : List Bool) :
    steps (46 * v + 29) ⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (ones (2 * v + 1)
          ++ (false :: false :: (ones (2 * s + 3) ++ (false :: false :: T)))))⟩⟩
      = some ⟨.D, p + 2 * (v : Int) + 25,
          ⟨ones 21 ++ (false :: false :: true :: false :: (pow10 v ++ L)), false,
           false :: false :: (ones (2 * s + 1) ++ (false :: false :: T))⟩⟩ := by
  rw [steps_add, markedChew v p L (ones (2 * s + 3) ++ (false :: false :: T)), someBind]
  have h3 : ones (2 * s + 3) = true :: true :: ones (2 * s + 1) := by
    rw [show 2 * s + 3 = 2 + (2 * s + 1) from by omega, ones_add]; rfl
  rw [h3]
  show steps 29 ⟨.D, p + 2 * (v : Int), ⟨pow10 v ++ L, false,
      false :: false :: (pow10 10 ++ (true :: false :: false ::
        (true :: true :: (ones (2 * s + 1) ++ (false :: false :: T)))))⟩⟩ = _
  rw [markedTurn]

/-- **The exact "off-by" the marked sweep leaves (the honest doubling gap).**  With the
milestone big-block value `B_K = 2^K − 3 = 2v+1` (so `v = 2^{K-1} − 2`), the comb
`pow10 v` the marked sweep deposits repacks (via `sweepEF`) to `1^{2v} = 1^{2^K − 4}`,
which is NOT the doubled block `1^{2^{K+1}−3} = 1^{2·B_K + 3}`: the gap is
`(2^{K+1}−3) − (2^K − 4) = 2^K + 1 ≠ 0`.  So the marked sweep alone does not realise
`doubling_id`; the ×2 emerges only after the comb repack + register/cascade rebuild
(the still-open G3 wiring).  Kernel arithmetic for all `K = k+2 ≥ 2`. -/
theorem marked_not_doubling (k : Nat) :
    2 * (2 ^ (k + 1) - 2) = 2 ^ (k + 2) - 4 ∧
    2 ^ (k + 2) - 4 ≠ 2 ^ (k + 2 + 1) - 3 := by
  have e1 : 2 ^ (k + 2) = 2 ^ (k + 1) * 2 := Nat.pow_succ 2 (k + 1)
  have e2 : 2 ^ (k + 2 + 1) = 2 ^ (k + 2) * 2 := Nat.pow_succ 2 (k + 2)
  have h4 : 4 ≤ 2 ^ (k + 2) := four_le_two_pow k
  exact ⟨by omega, by omega⟩

/-! ## §5g (COMPOSITION) The doubling-phase MIDDLE — `markedBlock ∘ cascadeFold`
composed into ONE halt-free transport (`bigCascade`), with the glue proven SYMBOLIC.

**The extracted M6(k)→M1(k+1) episode sequence** (from `x2co_trace.py` g=2..6, uniform
across g; the 6 episodes of `X2_COMPOSITION_2026-07-11.md` §1):

  1. ENTRY (bounded): `M6 = 0^2 (10)^4 1^9 0^2 (1111100)^{g-1} … 1^{big} casc` → short
     `1^9` chew + hand-off into the register.
  2. REGISTER CHEW: uniform fold over the `(1111100)^{g-1}` register units.
  3. **BIG-BLOCK SWEEP**: the `(10)^10`-marked R/L loop grinds the marked big block
     `1^{2v+1} = 1^{2^K−3}` to `1^1` + a `1^{21}` residue, crosses into the first cascade
     block trimming it by 2 — **this is `markedBlock` (PROVEN ∀v,s)**.
  4. **CASCADE FOLD**: over the `K−3` UNMARKED cascade blocks `2^{K-1}−3, …, 5` — **this
     is `cascadeFold` (PROVEN ∀ list)**.
  5. REPACK: the accumulated comb is E-swept (`sweepEF`-family) toward the new big block.
  6. REGISTER-REBUILD: `U^g` + the parity tail are re-written, yielding `M1(k+1)`.

**What composes here (episodes 3+4), and the glue.**  `markedBlock v s` leaves the head
`[D]` on `0^2 1^{2s+1} 0^2 T`; `cascadeFold bs m` demands `[D]` on `0^2 1^{2m+3} 0^2 (casc
bs T')`.  The glue is the SYMBOLIC identity `2s+1 = 2m+3 ⟺ s = m+1`, together with `T =
casc bs T'`: markedBlock trims the first cascade block from `1^{2s+3} = 1^{2m+5}` to
`1^{2s+1} = 1^{2m+3}`, which is EXACTLY the block `cascadeFold` then consumes with leading
`m`.  Composing them (`steps_add`) gives `bigCascade`: the big MARKED block AND the whole
UNMARKED cascade folded into one comb-deposit, HALT-FREE, in `46v + 29 + foldTime m bs`
steps.  This CORRECTS the `cascade_traversal` framing (which mis-treated the big block as an
unmarked first fold-block): physically the big block carries the `(10)^10` marker and is
swept by `markedBlock`, the cascade blocks are plain and folded by `cascadeFold`. -/
theorem bigCascade (v m : Nat) (bs : List Nat) (p : Int) (L T : List Bool) :
    ∃ (comb : List Bool) (q : Int),
      steps (46 * v + 29 + foldTime m bs) ⟨.D, p, ⟨L, false,
          false :: false :: (pow10 10 ++ (ones (2 * v + 1)
            ++ (false :: false :: (ones (2 * (m + 1) + 3)
              ++ (false :: false :: casc bs T)))))⟩⟩
        = some ⟨.D, q, ⟨comb ++ L, false,
            false :: false :: (ones (2 * lastBlock m bs + 3)
              ++ (false :: false :: T))⟩⟩ := by
  -- glue: markedBlock's next block is `1^{2(m+1)+3} = 1^{2s+3}` (s := m+1); trimmed to
  -- `1^{2s+1} = 1^{2m+3}`, exactly `cascadeFold bs m`'s leading block; tail `T := casc bs T`.
  obtain ⟨comb, q, hfold⟩ := cascadeFold bs m (p + 2 * (v : Int) + 25)
    (ones 21 ++ (false :: false :: true :: false :: (pow10 v ++ L))) T
  refine ⟨comb ++ (ones 21 ++ (false :: false :: true :: false :: pow10 v)), q, ?_⟩
  have hb : (2 * (m + 1) + 1) = (2 * m + 3) := by omega
  have hFull : comb ++ (ones 21 ++ (false :: false :: true :: false :: (pow10 v ++ L)))
      = (comb ++ (ones 21 ++ (false :: false :: true :: false :: pow10 v))) ++ L := by
    simp only [List.append_assoc, List.cons_append]
  rw [steps_add, markedBlock v (m + 1) p L (casc bs T), someBind, hb, hfold]
  exact congrArg some (by rw [hFull])

/-- **The exact NET-DOUBLING residual of the composed middle (the honest arithmetic
obstruction).**  Even granting a *clean* repack of every comb the composed `bigCascade`
deposits, the totals do NOT sum to the doubled block `2^{K+1}−3`.  At the milestone
`K = k+3 ≥ 3`: the big-block comb repacks to `2(v+1) = 2^K−2` (`v = 2^{K-1}−2`), plus the
`1^{21}` `markedTurn` residue, plus the cascade combs whose `Σ` closed form is
`cascadeBlocks_sum = 2^{K-1}−4K+8` (with the `−4K+8` correction).  These are visibly
K-DEPENDENT and do NOT combine to a fixed `2^{K+1}−3` under any single proven repack: the
residual is `Θ(K)` (numerically `−7,−6,−3` at `K=10,11,14`; see the `#eval` below).  So the
`−4K+8` correction does NOT self-cancel to `doubling_id`'s `2^{K+1}−3` — the missing
`Θ(K)` MUST be supplied by the register-rebuild (episode 6), which couples to `2^K` and is
NOT captured by any lemma in this file.  This records the EXACT gap: the compound's chew
+fold (episodes 3+4) is proven and halt-free, but the ×2 is realised only by the
repack+rebuild that carries the K-dependent register correction. -/
theorem bigCascade_not_doubling (k : Nat) :
    -- the big-block comb repack `2^K−2` is strictly below the target `2^{K+1}−3`,
    -- so the cascade + residue must supply `2^K−1` more — but their Σ is `Θ(2^{K-1})`,
    -- carrying the `−4K+8` correction, hence no clean fixed-offset closes it.
    (2 ^ (k + 3) - 2) < (2 ^ (k + 3 + 1) - 3) ∧
    natSum (cascadeBlocks (k + 3)) + 4 * ((k + 3) - 3) + 4 = 2 ^ ((k + 3) - 1) := by
  refine ⟨?_, cascadeBlocks_sum (k + 3) (by omega)⟩
  have e : 2 ^ (k + 3 + 1) = 2 ^ (k + 3) * 2 := Nat.pow_succ 2 (k + 3)
  have h4 : 4 ≤ 2 ^ (k + 3) := by
    have := four_le_two_pow (k + 1); rwa [show k + 1 + 2 = k + 3 from by omega] at this
  omega

/-- **The doubling-phase transport with the PROVEN middle (episodes 3+4) discharged.**
This tightens `doubling_transport`: the marked big-block sweep (episode 3, `markedBlock`)
AND the cascade fold (episode 4, `cascadeFold`) are now the PROVEN composite `bigCascade`
in the middle — a genuine advance over `doubling_transport`, which covered only the cascade
fold and mis-framed the big block as an unmarked first fold-block.  What REMAINS as named
hypotheses: (`H_entry`) the low phase + entry + register chew (episodes 1,2) reaching the
MARKED-big-block-sweep start `[D] 0^2 (10)^10 1^{2v+1} 0^2 1^{2(m+1)+3} 0^2 (casc bs T)`;
and (`H_repack`) the repack + register-rebuild (episodes 5,6) carrying the ground cascade
config to `M1next`.  The proof composes `H_entry`, the PROVEN `bigCascade`, and `H_repack`
via `steps_add`, HALT-FREE.  Honest scope: episodes 3+4 are now proven; the ×2 doubling
itself still lives in the un-formalized `H_repack` (see `bigCascade_not_doubling`). -/
theorem doubling_transport_mid (v m : Nat) (bs : List Nat) (p : Int) (L T : List Bool)
    (entryCfg : Cfg) (Nentry : Nat)
    (H_entry : steps Nentry entryCfg = some ⟨.D, p, ⟨L, false,
        false :: false :: (pow10 10 ++ (ones (2 * v + 1)
          ++ (false :: false :: (ones (2 * (m + 1) + 3)
            ++ (false :: false :: casc bs T)))))⟩⟩)
    (Nrepack : Nat) (M1next : List Bool → Int → Cfg)
    (H_repack : ∀ (comb : List Bool) (q : Int),
        steps Nrepack ⟨.D, q, ⟨comb ++ L, false,
            false :: false :: (ones (2 * lastBlock m bs + 3)
              ++ (false :: false :: T))⟩⟩
          = some (M1next comb q)) :
    ∃ (N : Nat) (comb : List Bool) (q : Int),
      steps N entryCfg = some (M1next comb q) := by
  obtain ⟨comb, q, hbc⟩ := bigCascade v m bs p L T
  refine ⟨Nentry + ((46 * v + 29 + foldTime m bs) + Nrepack), comb, q, ?_⟩
  rw [steps_add, H_entry, someBind, steps_add, hbc, someBind, H_repack]

/-! ## §5h (EPISODES 5,6 — the REPACK + REGISTER-REBUILD) — extracted cell-for-cell
from the RAW machine (= this file's `step`), and the EXACT obstruction to formalizing
them as `rebuild_transport : M_mid(k) → M1(k+1)` (the piece that would discharge
`doubling_transport_mid`'s `H_repack`).

**What was extracted (all cross-checked against `step` on the real milestone tapes,
g = 2,3; see `x2co_trace.py`/`x2cc_gencheck.py` and the raw-tape harness).**  The
doubling phase M6(g)→M1(g+1) is ONE braided milestone-to-milestone segment — there are
NO intermediate `E`-on-leading-`0` milestones between M6 and M1(g+1).  Its length is
`2 119 358` steps at g=2 and `8 477 210` at g=3 (a `≈4×` jump = `Θ(2^{2K})`, `K=g+8`).
Decomposed into this file's certified macros (the executor's `try_R_cycle` = `sweepEF`,
`try_L_cycle`, `try_D_loop` = `dSweepTurn`):

* g=2: `R = 3914`, `L = 3914`, `D = 1025`;   g=3: `R = 9856`, `L = 9854`, `D = 2050`.

`R ≈ L` (equal, not off by a bounded amount) and both are `Θ(2^K)`.  The macro STREAM is a
continuous braid `…L,R,L,R,…,D,D,…,L,R,…` in which the register units `(1^5 0^2)` are
pulled in INTERMITTENTLY across the WHOLE phase — there is NO contiguous prefix that is
"the repack" followed by a suffix that is "the register-rebuild".  A single full
round-trip is: an `E`-sweep RIGHT over the live comb `(01)^n` (this is `sweepEF`, the
genuine on-path `×2` primitive, PROVEN ∀n), a turn into `C` at the next `1`-block
boundary, and a leftward RETURN sweep; the NEXT round-trip runs over a comb SHORTER by
one unit.  So the phase is a shrinking-comb ODOMETER (quadratic, `Θ(N^2)`, `N ≈ 2^K`,
matching the `4×` scaling), whose round-trips have a DIFFERENT length every trip and are
interleaved with `D`-loop register/cascade crossings at data-dependent positions.

**THE EXACT LEAN OBSTRUCTION (why `rebuild_transport` does not exist as this file's kind
of lemma), scrutinised as the FOURTH framing.**
1. **`M_mid(k)` is off-path.**  `bigCascade`'s output — the intended start of episode 5 —
   is reached from `bigCascade`'s INPUT, the `(10)^10`-MARKED big block
   `[D] 0^2 (10)^10 1^{2v+1} 0^2 …`.  That marked input occurs `0` times in the real
   doubling phase (exhaustively scanned, g=2): the real big block `1^{2^K−3}` is preceded
   by the register `(1^5 0^2)^{g-1} 1 0^2`, NOT a `(10)^10` marker, and is consumed by
   `D`-sweeps INSIDE the block (`1^{24} [D] 1^{24}`) interleaved with the comb repack.  So
   `markedBlock`/`bigCascade`, though VALID lemmas about `step`, lie OFF the trajectory —
   the machine never reaches `M_mid(k)`, and `doubling_transport_mid` is a true transport
   whose hypotheses `H_entry`/`H_repack` are jointly UNSATISFIABLE on the real path (the
   real path has no such `[D]`-marked hand-off).
2. **No fixed-length tile, no uniform-shift invariant.**  The phase is a single non-nested
   braid whose `L`/`R` round-trip lengths shrink every trip (`R = L`, `Θ(2^K)`); there is
   NO recurring sub-configuration `Cfg(p) → Cfg(p−1)` with a uniform shift, so neither a
   bounded set of `steps_add`-composed tile lemmas nor a `List`-induction fold (the
   `cascadeFold` pattern) captures it.  It is a genuine DOUBLE induction (outer: comb
   length; inner: each variable-length `sweepEF`), and the outer invariant must carry the
   ENTIRE cascade + register state simultaneously — it does not localize.
3. **The `×2` couples to `2^K` and to the FULL cascade.**  `bigCascade_not_doubling`
   already proved the deposited combs (`2^K−2` + `Σ = 2^{K-1}−4K+8` + the `1^{21}`
   residue) miss the target `2^{K+1}−3` by a `Θ(K)` residual.  The extraction shows WHY
   nothing local supplies it: the missing `Θ(K)` is realised only by the braid's
   SIMULTANEOUS processing of every cascade block and the register `U^g` — exactly the
   "register-rebuild couples to the high part" wall (`X2_COMPOSITION` §3, G3).

**VERDICT (honest, no overclaim).**  `H_repack` is NOT dischargeable as posed: episodes
5,6 do not exist as a contiguous, localizable segment.  "REPACK" and "REGISTER-REBUILD"
are abstractions of ONE interleaved shrinking-comb odometer braid spanning the whole
doubling phase, coupled to the full cascade and to `2^K`.  No `rebuild_transport` /
`M_mid(k) → M1(k+1)` lemma is added (adding one would be false-on-path or vacuous).  What
IS certified on-path: `sweepEF` (the `×2` repack primitive ∀n), `dSweepTurn` (the block
crossings ∀n), and the halt-freedom of the repack round-trip context (anchor below). -/

-- **On-path repack round-trip is HALT-FREE (small-scale anchor).**  A config in the
-- shape the braid actually runs — a grown big block `1^{20}` on the left, head `E` on the
-- leading `0` of a live comb `(01)^8`, backed by a `1^5` residue block — runs `800` steps
-- with `step` never `none` (the `E`-met gap-3 halt gate never fires).  Kernel-checked,
-- mirroring the raw-trace round-trip `1^{20} [E] (01)^8 1^5 → … C-turn … → return`:
set_option maxRecDepth 4000 in
#eval decide (steps 800 ⟨.E, 0, ⟨ones 20, false, pow10 8 ++ ones 5⟩⟩ ≠ none)   -- true

/-! ## §5i (ON-PATH, independently re-extracted 2026-07-12) THE DOUBLING PHASE'S REAL
STEADY ENGINE — the `E`-anchored comb-deposit tile + its inner comb-shrink fold, taken
CELL-FOR-CELL from a RAW simulation of the machine (matching this file's `step`) on the
real `g = 2` orbit, NOT from prose and NOT from the macro executor.

**Provenance (raw-orbit facts, all reproduced by direct `step`-simulation from the concrete
milestone tape `m1_spec(2)`, no macros):**  the doubling phase `M6(2) → M1(3)` runs from
step `343` (M6) to step `2 119 358` (M1(3)) — exactly `2 119 015` raw steps, `Θ(2^{2K})`,
`K = 10` (independent confirmation of §5h's `2 119 358`).  During its long steady region the
head sits in **state `E` on a `0`** at the boundary between a growing `(10)`-comb on the LEFT
and the big block `1^{2v+1}` on the RIGHT, and runs a UNIFORM 6-step cycle
`E:0→F:0→A:1→E:1→C:0→D:0→E:0` that consumes exactly two `1`s from the block, deposits one
`0 1` (nearest-first) comb cell-pair on the left, and re-lands `E` on the next boundary `0`,
advancing `+2`.  Verified at raw step `n = 646`: block length `969`; after exactly 6 steps
(`n = 652`) block length `967`, head again `E` on the boundary `0` — reproduced below as
`ecombChew_tile` (kernel `rfl`).  This is the SAME physical 6-loop as §5b's `chew_tile`,
phase-anchored at the on-path milestone state `E` (not `D`), with the block written directly
(no `0^3` marker) — the form the real orbit actually visits between comb repacks.

**What this is / is not.**  This is the **INNER induction** of the shrinking-comb double
induction: the block→comb chew, `1^{2v+1} → 1^1` depositing `pow01 v`, HALT-FREE ∀v.  It is
NOT the ×2 doubling and NOT the outer odometer (see the honest gap at the foot).  The genuine
`(01)^m → 1^{2m}` repack (the comb→block direction, `sweepEF`) is the OTHER half; the raw
orbit interleaves the two — e.g. at raw step `n = 6626` the head runs a `sweepEF` sweep over a
`(10)`-comb whose pair-count descends `6,5,4,3` (the repack), then chews again.  The two
directions, braided over the whole cascade with per-round-trip lengths that grow every trip,
are the quadratic odometer §5h already refuted as a single localizable lemma. -/

/-- `(01)^k` nearest-first (`false` first) — the comb cell-pair the `E`-anchored tile deposits.
This is the mirror of `pow10`; `pow01 k = (false :: true)^k`. -/
def pow01 : Nat → List Bool
  | 0 => []
  | k + 1 => false :: true :: pow01 k

/-- `pow01` is additive (mirrors `pow10_add`). -/
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

/-- **The on-path `E`-anchored comb-deposit tile** (6 steps `E:0·F:0·A:1·E:1·C:0·D:0`): head
`E` on the boundary `0`, block ahead `0 1 1 · R` (`false :: true :: true :: R`, the boundary
`0` then the two leading block `1`s); the cycle consumes the two `1`s, deposits `0 1`
(nearest-first) on the left, and re-lands `E` on the fresh boundary `0`, advancing `+2`; the
left context `L` and the tail `R` are never read.  Kernel `rfl` — reproduced from the raw
`g = 2` orbit at step `n = 646`. -/
theorem ecombChew_tile (p : Int) (L R : List Bool) :
    steps 6 ⟨.E, p, ⟨L, false, false :: true :: true :: R⟩⟩
      = some ⟨.E, p + 2, ⟨false :: true :: L, false, false :: R⟩⟩ := by
  have h : steps 6 (⟨.E, p, ⟨L, false, false :: true :: true :: R⟩⟩ : Cfg)
      = some ⟨.E, p + 1 + 1 + 1 - 1 - 1 + 1, ⟨false :: true :: L, false, false :: R⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **THE INNER COMB-SHRINK INDUCTION (block→comb chew), ARBITRARY block length.**  `v` tiles
= `6v` steps grind the on-path big block `1^{2v+1}` (encoded head-boundary `0` then
`ones (2v+1)`) down to the residue `1^1`, depositing the comb `pow01 v` on the left and
advancing `+2v`; the tail `R` is untouched.  Proven for EVERY `v` by `ecombChew_tile` + length
induction (the `chewFold` / `O3.crawlR` pattern).  Every step lands `some` ⇒ HALT-FREE (the
`E`-met gap-3 halt gate never fires anywhere in the chew).  This is the doubling phase's inner
loop, ON the real orbit (the steady chew of the `1^{2^K-3}` block, `n = 646 … ` at `g = 2`). -/
theorem ecombChewFold : ∀ (v : Nat) (p : Int) (L R : List Bool),
    steps (6 * v) ⟨.E, p, ⟨L, false, false :: (ones (2 * v + 1) ++ R)⟩⟩
      = some ⟨.E, p + 2 * (v : Int), ⟨pow01 v ++ L, false, false :: (ones 1 ++ R)⟩⟩ := by
  intro v
  induction v with
  | zero =>
    intro p L R
    show steps 0 _ = _
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ v ih =>
    intro p L R
    have hn : 6 * (v + 1) = 6 + 6 * v := by omega
    rw [hn, steps_add]
    have hb : ones (2 * (v + 1) + 1) = true :: true :: ones (2 * v + 1) := by
      rw [show 2 * (v + 1) + 1 = 2 + (2 * v + 1) from by omega, ones_add]; rfl
    rw [hb]
    show (steps 6 ⟨.E, p, ⟨L, false,
        false :: (true :: true :: (ones (2 * v + 1) ++ R))⟩⟩).bind (steps (6 * v)) = _
    rw [ecombChew_tile, someBind, ih (p + 2) (false :: true :: L) R]
    have hL : pow01 v ++ (false :: true :: L) = pow01 (v + 1) ++ L := by
      rw [show (false :: true :: L) = pow01 1 ++ L from rfl, ← List.append_assoc, ← pow01_add]
    rw [hL]
    exact congrArg some (cfgPos (by push_cast; omega))

/-- **The honest inner/outer boundary (why the inner fold does NOT close the phase).**  The
inner chew `ecombChewFold` turns the block `1^{2v+1}` into the comb `pow01 v` in `6v` steps;
with the milestone `2v+1 = 2^K − 3` (so `v = 2^{K-1} − 2`) that is `Θ(2^{K-1})` steps — but the
full doubling phase is `Θ(2^{2K})` (raw: `2 119 015` at `K=10`).  The missing quadratic factor
is the OUTER odometer: the comb `pow01 v` is then repacked by `sweepEF`-round-trips whose
length shrinks by one each trip and which are interleaved, at data-dependent positions, with the
register `(1^5 0^2)` and every cascade block — exactly §5h's non-localizable braid.  The two
`Θ(2^{K-1})` numbers (inner chew length; comb pair-count) multiplying to `Θ(2^{2K})` is the
arithmetic signature of the double induction; the inner factor is `ecombChewFold`, the outer
factor is NOT captured by any lemma here.  Kernel witness of the two scales: -/
theorem inner_is_linear_not_quadratic (k : Nat) :
    2 * (2 ^ (k + 1) - 2) + 1 = 2 ^ (k + 2) - 3 := by
  have e : 2 ^ (k + 2) = 2 ^ (k + 1) * 2 := Nat.pow_succ 2 (k + 1)
  have h4 : 4 ≤ 2 ^ (k + 2) := four_le_two_pow k
  omega

/-! ## §6 Sanity `#eval` (kernel-executed at every build) + axiom audit. -/

-- the repack really does `(01)^3 → 1^6` (E at +6), halt-free:
#eval decide (steps 6 ⟨.E, 0, ⟨[], false, pow10 3⟩⟩
      = some ⟨.E, 6, ⟨ones 6, false, []⟩⟩)                                    -- true
-- the D-sweep crosses `1^4` and turns into E at the left edge (n = 3):
#eval decide (steps 5 ⟨.D, 0, ⟨ones 3 ++ [false], true, []⟩⟩
      = some ⟨.E, -3, ⟨[false], true, ones 3⟩⟩)                               -- true
-- halt gate fires only at B reading 1:
#eval decide (step ⟨.B, 0, ⟨[], true, []⟩⟩ = none)                            -- true
#eval decide (step ⟨.B, 0, ⟨[], false, []⟩⟩ ≠ none)                           -- true
-- chew fold: block `1^7` (m=2) chewed to `1^3` in 12 steps, depositing `(10)^2`,
-- head +4, markers preserved, halt-free (cross-checks the Python x2cc C1 trace):
#eval decide (steps (6 * 2) ⟨.D, 0, ⟨[], false,
        false :: false :: (ones 7 ++ (false :: false :: []))⟩⟩
      = some ⟨.D, 4, ⟨pow10 2, false,
          false :: false :: (ones 3 ++ (false :: false :: []))⟩⟩)              -- true

-- separator-cross tile: `0^3 1^3 0^2 1^2 · X` → deposit `(01)^2 0^2 1`, `[D] 0^3 · X`,
-- head +7, `X` untouched (kernel cross-check of the 15-step crossing):
#eval decide (steps 15 ⟨.D, 0, ⟨[], false,
        false :: false :: true :: true :: true :: false :: false :: true :: true :: [true, false]⟩⟩
      = some ⟨.D, 7, ⟨[true, false, false, true, false, true, false], false,
          false :: false :: [true, false]⟩⟩)                                    -- true
-- per-block step `blockStep 2 4`: block `1^7` (m=2) chewed + separator-crossed into the
-- next block `1^{13}` (s=4), leaving it `1^{11}`, `[D] 0^3` re-formed, head +11, halt-free:
#eval decide (steps (6 * 2 + 15) ⟨.D, 0, ⟨[], false,
        false :: false :: (ones 7 ++ (false :: false :: (ones 13 ++ (false :: false :: []))))⟩⟩
      = some ⟨.D, 11, ⟨(true :: false :: false :: true :: false :: true :: false :: pow10 2), false,
          false :: false :: (ones 11 ++ (false :: false :: []))⟩⟩)              -- true

-- G2 big-block `(10)^10`-marked sweep kernel cross-checks (vs the raw x2 machine):
-- one marked chew tile (46 steps): block `1^{b+2}` (b=5) → `1^b`, marker preserved,
-- deposit `1 0`, head +2, halt-free (`ones b`/tail untouched):
#eval decide (steps 46 ⟨.D, 0, ⟨[], false,
        false :: false :: (pow10 10 ++ (true :: true :: (ones 5 ++ (false :: false :: []))))⟩⟩
      = some ⟨.D, 2, ⟨[true, false], false,
          false :: false :: (pow10 10 ++ (ones 5 ++ (false :: false :: [])))⟩⟩)     -- true
-- markedChew fold, v=8: big block `1^17` ground to `1^1` in 46·8=368 steps, deposit
-- `pow10 8`, marker `0^3 (10)^10` preserved, head +16, halt-free:
#eval decide (steps (46 * 8) ⟨.D, 0, ⟨[], false,
        false :: false :: (pow10 10 ++ (ones 17 ++ (false :: false :: [])))⟩⟩
      = some ⟨.D, 16, ⟨pow10 8, false,
          false :: false :: (pow10 10 ++ (ones 1 ++ (false :: false :: [])))⟩⟩)      -- true
-- markedTurn (29 steps): repack `(10)^10 1^1` → `1^{21}`, cross next block `1^{n+2}`
-- (n=7) → `1^7`, deposit `0^2 1 0`, head +25, halt-free:
#eval decide (steps 29 ⟨.D, 0, ⟨[], false,
        false :: false :: (pow10 10 ++ (true :: false :: false ::
          (true :: true :: (ones 7 ++ (false :: false :: [])))))⟩⟩
      = some ⟨.D, 25, ⟨ones 21 ++ (false :: false :: true :: false :: []), false,
          false :: false :: (ones 7 ++ (false :: false :: []))⟩⟩)                    -- true
-- markedBlock (46·5+29=259 steps), v=5,s=3: big block `1^11` + marker → comb-residue,
-- next block `1^9` → `1^7`, `[D] 0^3` re-formed, head +35, halt-free:
#eval decide (steps (46 * 5 + 29) ⟨.D, 0, ⟨[], false,
        false :: false :: (pow10 10 ++ (ones 11
          ++ (false :: false :: (ones 9 ++ (false :: false :: [])))))⟩⟩
      = some ⟨.D, 35, ⟨ones 21 ++ (false :: false :: true :: false :: pow10 5), false,
          false :: false :: (ones 7 ++ (false :: false :: []))⟩⟩)                    -- true
-- COMPOSITION `bigCascade` (episodes 3+4): marked big block `1^5` (v=2) chewed, then the
-- cascade fold over bs=[] (m=0, one trailing ground block) — `46·2+29+foldTime 0 [] = 121`
-- steps, lands `[D]` on `0^2 1^3 0^2`, HALT-FREE.  Kernel cross-check of the composed
-- `markedBlock ∘ cascadeFold` transport vs the raw x2 machine (`some` ⇒ no halt in 121):
#eval decide (((steps (46 * 2 + 29 + foldTime 0 []) ⟨.D, 0, ⟨[], false,
        false :: false :: (pow10 10 ++ (ones (2 * 2 + 1)
          ++ (false :: false :: (ones (2 * (0 + 1) + 3)
            ++ (false :: false :: casc [] [])))))⟩⟩).map
      (fun c => (c.st, c.tape.right)))
      = some (St.D, false :: false :: (ones 3 ++ (false :: false :: []))))          -- true

-- §5i ON-PATH (raw g=2 orbit) kernel cross-checks:
-- the `E`-anchored comb-deposit tile at the real step n=646 (block ahead `1^{40}`): 6 steps
-- consume two `1`s, deposit `0 1` on the left, re-land `E` on the boundary `0`, head +2:
#eval decide (steps 6 ⟨.E, 0, ⟨pow01 4, false, false :: ones 40⟩⟩
      = some ⟨.E, 2, ⟨false :: true :: pow01 4, false, false :: ones 38⟩⟩)           -- true
-- the inner comb-shrink fold, v=20: block `1^{41}` ground to `1^1` in 120 steps, depositing
-- `pow01 20`, head +40, HALT-FREE (mirrors the raw n=646.. chew of the `1^{1021}` big block):
#eval decide (steps (6 * 20) ⟨.E, 0, ⟨[], false, false :: (ones 41 ++ [])⟩⟩
      = some ⟨.E, 40, ⟨pow01 20, false, false :: (ones 1 ++ [])⟩⟩)                    -- true
-- the OTHER half (`sweepEF`, comb→block) also fires on the real orbit — at raw step n=6626
-- the head sweeps a `(10)`-comb of `6` pairs into `1^{12}`, halt-free (already `sweepEF`):
#eval decide (steps (2 * 6) ⟨.E, 0, ⟨[], false, pow10 6⟩⟩
      = some ⟨.E, 12, ⟨ones 12, false, []⟩⟩)                                          -- true

#print axioms steps_add
#print axioms halt_gate
#print axioms sweepEF
#print axioms sweepEF_even
#print axioms dSweepTurn
#print axioms chew_tile
#print axioms chewFold
#print axioms sepCross_tile
#print axioms blockStep
#print axioms cascadeFold
#print axioms doubling_id
#print axioms markedChew_tile
#print axioms markedChew
#print axioms markedTurn
#print axioms markedBlock
#print axioms marked_not_doubling
#print axioms bigCascade
#print axioms bigCascade_not_doubling
#print axioms doubling_transport_mid
#print axioms pow01_add
#print axioms ecombChew_tile
#print axioms ecombChewFold
#print axioms inner_is_linear_not_quadratic

-- G3 WIRING kernel cross-checks (vs the Python milestone `m1_spec`, K = g+8):
-- cascadeBlocks 10 (g=2) = fold a-params for milestone blocks 2^j−3, j=9..3:
#eval decide (cascadeBlocks 10 = [252, 124, 60, 28, 12, 4, 0])                  -- true
-- reconstructing 1^{2a+5} recovers the milestone cascade blocks 509,253,…,5:
#eval decide ((cascadeBlocks 10).map (fun a => 2 * a + 5) = [509, 253, 125, 61, 29, 13, 5]) -- true
-- leading big block: 2·(2^9−3)+3 = 2^10−3 = 1021 (the milestone `big`, g even):
#eval decide (2 * (2 ^ 9 - 3) + 3 = 1021)                                       -- true
-- the terminal 1^1 (2^2−3, j=2) is NOT fold-representable (2a+5 = 1 ⟹ a = −2):
--   it lives in the opaque tail T; cascadeBlocks stops at j=3 (block 1^5).
-- sum closed form Σ cascadeBlocks 10 = 2^9 − 4·10 + 8 = 480:
#eval decide (natSum (cascadeBlocks 10) = 480)                                  -- true
#eval decide (natSum (cascadeBlocks 10) + 4 * (10 - 3) + 4 = 2 ^ (10 - 1))      -- true
-- g=2..6 (K=10..14): reconstruction of the milestone cascade block lengths:
#eval decide ((cascadeBlocks 11).map (fun a => 2 * a + 5)
      = [1021, 509, 253, 125, 61, 29, 13, 5])                                   -- true (g=3)
#eval decide ((cascadeBlocks 14).map (fun a => 2 * a + 5)
      = [8189, 4093, 2045, 1021, 509, 253, 125, 61, 29, 13, 5])                 -- true (g=6)
-- THE OBSTRUCTION, concretely: the cascade accumulator is ≈2^{K-1}, so
-- 2·Σ+3 ≠ 2^{K+1}−3 (963 ≠ 2045) — the fold does NOT carry the 2^K doubling:
#eval decide (2 * natSum (cascadeBlocks 10) + 3 ≠ 2 ^ 11 - 3)                    -- true
-- the genuine 2^K doubling is doubling_id on the BIG block (a separate G2 episode):
#eval decide (2 * (2 ^ 10 - 3) + 3 = 2 ^ 11 - 3)                                -- true

#print axioms natSum
#print axioms cascDesc_sum
#print axioms cascadeBlocks_sum
#print axioms cascade_traversal
#print axioms doubling_transport
#print axioms sanity100

/-! ## §7 Honest scope of this file (what is FORMALIZED vs OPEN).

FORMALIZED here (`lake build` green, no `sorry`, no `native_decide`, axioms
`[propext, Quot.sound]` only):

* the x2 machine `step`/`steps` + halt gate (`step = none ↔ B reads 1`);
* the doubling-engine sweeps `sweepEF` (comb-repack `(01)^m → 1^{2m}` ∀m) and
  `dSweepTurn` (`1`-block crossing ∀n);
* the cascade CHEW `chew_tile`/`chewFold` (block `1^{2m+3} → 1^3` ∀m);
* **G1 — the cascade FOLD** (`sepCross_tile`, `blockStep`, `cascadeFold`): the
  per-block step composed over an ARBITRARY, non-uniform `List Nat` of blocks by
  List induction, halt-free (`some`) for every list.  This closes the exact
  representational gap flagged in `X2_COMPOSITION_2026-07-11.md` §3 (G1) — the
  fold the affine Python executor (fixed-length run-lists) provably could not
  express, here a routine Lean `List` recursion;
* **G3 arithmetic core** — `doubling_id`: `2·(2^K−3)+3 = 2^{K+1}−3`, the
  exponential (`2^K`) block-doubling identity the affine executor could not
  represent.
* **G3 WIRING, structural part** (§5e) — `cascadeBlocks K` (the milestone `M(K)`
  cascade as a concrete `List Nat` in the fold `a`-convention, kernel-`#eval`
  cross-checked vs the Python `m1_spec` for K = 10..14 / g = 2..6);
  `cascade_traversal` (`cascadeFold` INSTANTIATED at `cascadeBlocks K`, halt-free);
  `cascDesc_sum`/`cascadeBlocks_sum` (the accumulator `Σ = 2^{K-1} − 4K + 8` closed
  form by List/Nat induction — the "Σ blocks → closed form" step); and
  `doubling_transport`, which composes entry + `cascade_traversal` + repack into a
  halt-free transport, taking the low-phase/entry and G2-repack pieces as NAMED
  hypotheses so the structural G3 result stands alone.
* **G2 the BIG-BLOCK `(10)^10`-MARKED SWEEP** (§5f) — `markedChew_tile`/`markedChew`
  (the big block `1^{2v+1}` ground to `1^1` in `46v` steps, marker `0^3 (10)^10`
  preserved, depositing `pow10 v`, HALT-FREE ∀v — a tile+length-induction sweep
  lemma EXTRACTED cell-for-cell from the raw g=2..6 machine, mirror of `chewFold`),
  `markedTurn` (the `(10)^10 1^1 → 1^{21}` repack + separator cross), and
  `markedBlock` (the full episode ∀v,s).  This lifts the marked sweep's SAFETY and
  STRUCTURAL transport to all block lengths — the bounded g=2..6 gap of item 2 below,
  now parametric.  **But it does NOT realise the ×2 doubling** (see item 2): the
  episode is the block→COMB chew, and `marked_not_doubling` records the exact
  arithmetic gap (`2·(2^{K-1}−2) = 2^K−4 ≠ 2^{K+1}−3`).
* **COMPOSITION — the doubling-phase MIDDLE** (§5g) — `bigCascade` composes the two
  biggest proven transport episodes, the marked big-block sweep (episode 3,
  `markedBlock`) and the cascade fold (episode 4, `cascadeFold`), into ONE halt-free
  transport (`46v+29+foldTime m bs` steps), with the GLUE proven SYMBOLIC (`markedBlock`
  leaves `[D] 0^2 1^{2s+1} 0^2 T`, `cascadeFold` consumes `[D] 0^2 1^{2m+3} 0^2 casc`;
  they meet at `s = m+1`, `T = casc bs T'`).  This CORRECTS the `cascade_traversal`
  framing (the marked big block is NOT an unmarked first fold-block).  `doubling_transport_mid`
  then composes `H_entry` + `bigCascade` + `H_repack`, discharging episodes 3+4 into the
  proven middle (a strict tightening of `doubling_transport`).  `bigCascade_not_doubling`
  records the EXACT net-doubling obstruction: the deposited combs (big-block `2^K−2`,
  cascade `Σ = 2^{K-1}−4K+8`, `1^{21}` residue) are K-DEPENDENT and do NOT combine to the
  fixed `2^{K+1}−3` (residual `Θ(K)`: `−7,−6,−3` at `K=10,11,14`) — the missing `Θ(K)`
  must come from the register-rebuild (episode 6), which couples to `2^K`.
* **ON-PATH INNER COMB-SHRINK INDUCTION** (§5i, 2026-07-12, independently re-extracted by
  RAW `step`-simulation of `m1_spec(2)`, not the macro executor) — `ecombChew_tile` (the
  `E`-anchored 6-step comb-deposit tile, kernel `rfl`, reproducing the real orbit's steady
  cycle at raw step n=646) and **`ecombChewFold`** (`1^{2v+1} → 1^1` depositing `pow01 v` in
  `6v` steps, HALT-FREE ∀v).  This is the doubling phase's INNER loop, ON the real orbit (the
  steady chew of the `1^{2^K−3}` big block).  Raw-orbit facts re-confirmed here: M6(2) at raw
  step 343, M1(3) at 2 119 358 (phase = 2 119 015 = `Θ(2^{2K})`, K=10).  `inner_is_linear_not_quadratic`
  pins the honest inner/outer boundary: the inner chew is only `Θ(2^{K-1})`; the missing
  quadratic factor is the OUTER shrinking-comb odometer (`sweepEF` round-trips of a length that
  shrinks every trip, interleaved with the register + cascade), which §5h already refuted as a
  localizable lemma — NOT closed here.

STILL OPEN (NOT in this file — the exact remaining Lean gaps to a decision):

1. **Low phase M1(g)→M6(g) ∀g** — the full sweep-induction that x2's low phase
   emits only gaps `{18,10,2(g+1),6-iff-even}`, never 3 (Python-`x2cc_prove`
   PROVEN, not yet ported; it is the analogue of the entire `Template`+`Suffix`
   generation-map, ~1k lines).  Supplies `doubling_transport`'s `H_entry`.
2. **G2 — the ×2 DOUBLING itself is a COMPOUND, NOT the marked sweep** (the exact
   obstruction found this session, the framing scrutinised).  §5f DOES lift the
   `10^10`-marked big-block R/L sweep to a parametric ∀-length halt-free lemma
   (`markedChew`/`markedBlock`) — extracted from the raw traces, not prose.  But that
   episode performs the block→COMB CHEW only: `1^{2v+1}` (with `2v+1 = 2^K−3`, so
   `v = 2^{K-1}−2`) becomes the comb `pow10 v` (repacking via `sweepEF` to
   `1^{2v} = 1^{2^K−4}`) PLUS a fixed `1^{21}` residue and a next-block trim — it does
   NOT emit the doubled block `1^{2^{K+1}−3}` (`marked_not_doubling`: the `2^K+1` gap).
   The genuine ×2 `2·(2^K−3)+3 = 2^{K+1}−3` (`doubling_id`) emerges only from the FULL
   compound (this chew → comb repack → register/cascade rebuild carrying the `−4K+8`
   correction).  Hence `doubling_transport`'s `H_repack` — the DISTINCT post-cascade
   repack episode — is NOT discharged by the marked sweep; it remains a named
   hypothesis.  What §5f closes: the marked-sweep engine's safety + transport ∀length;
   what remains: the compound composition that actually doubles.
   **§5h UPDATE (episodes 5,6 extracted cell-for-cell — the FOURTH framing, refuted).**
   The `H_repack` episodes 5,6 (REPACK + REGISTER-REBUILD) were extracted from the RAW
   machine on the real milestone tapes (g=2,3).  They do NOT form a contiguous segment:
   the whole doubling phase M6→M1(g+1) is ONE braid (g=2: `2 119 358` steps, macros
   `R=L=3914`, `D=1025`; g=3: `8 477 210` steps, `R=9856,L=9854,D=2050` — `Θ(2^{2K})`), a
   shrinking-comb ODOMETER (`sweepEF` round-trips of a length that shrinks every trip,
   interleaved with register/cascade `D`-loops).  Moreover `bigCascade`'s `(10)^10`-marked
   input occurs `0` times on the real path (the big block is register-preceded, not
   marker-preceded), so `M_mid(k)` is OFF-path and `doubling_transport_mid`'s
   `H_entry`/`H_repack` are jointly unsatisfiable on the real trajectory.  `H_repack` is
   therefore NOT dischargeable as posed; the exact obstruction (no fixed tile, no
   uniform-shift invariant, `×2` couples to the full cascade + `2^K`) is recorded in §5h,
   with a kernel halt-free anchor for the on-path repack round-trip context.
3. **G3 wiring — the accumulator-to-`2^K` IDENTITY does NOT close as posed**
   (the honest obstruction found this session).  Three exact mismatches:
   (a) the terminal `1^1` (`= 2^2−3`, j=2) block is NOT fold-representable
       (`2a+5 = 1 ⟹ a = −2`); it lives in the opaque tail `T`, so `cascadeBlocks`
       covers only `j = K−1 … 3` — a genuine parity/boundary cut at the cascade
       bottom;
   (b) `cascadeFold` lands on `1^{2·lastBlock+3}` (the last block ground down), NOT
       on `1^{2·acc+3}`; the repack that fuses the deposited comb into a single big
       block is a SEPARATE G2 episode (item 2), absent here;
   (c) the cascade accumulator is `Σ ≈ 2^{K-1}`, so `2·Σ + 3 ≠ 2^{K+1}−3`
       (`#eval`: `963 ≠ 2045` at K=10).  **`doubling_id` is the BIG-BLOCK
       marked-sweep episode's law, NOT the cascade fold's** — the original
       "cascadeFold accumulator = 2^K via `doubling_id`" framing is refuted.  What
       IS wired: the cascade traversal is halt-free over the concrete milestone
       list, its `Σ` has a proven closed form, and the transport composes cleanly
       ONCE `H_entry`/`H_repack` are supplied.  The register-rebuild `2·(comb) +
       corrections = 2^{K+1}−3` (with the `−4K+8` correction the fold's `Σ` carries)
       remains OPEN — it needs the G2 big-block sweep, not further fold work.
4. **The milestone form M(g) and the composed `x2_nonhalt`** — the nested cascade
   as a concrete `Cfg`, the transport `M1(g)→M1(g+1)` ∀g, and the prefix-closed
   non-halt (`∀n, steps n init ≠ none`) — NONE assembled.

**Verdict: NO decision.**  This file advances the formalization by closing G1
(the fold engine), G3's arithmetic core, the G3-wiring STRUCTURAL part (concrete
cascade instantiation + accumulator sum + composed transport with named hypotheses),
the G2 big-block `(10)^10`-marked sweep as an arbitrary-length halt-free lemma
(`markedChew`/`markedBlock`), and now the doubling-phase MIDDLE `bigCascade`
(episodes 3+4 = marked big-block sweep ∘ cascade fold composed into one halt-free
transport with SYMBOLIC glue), all with clean axioms.  The G3 accumulator-to-`2^K`
IDENTITY does NOT close as originally posed, and — the honest finding this session —
neither does the G2 ×2 doubling even after composing episodes 3+4: `bigCascade` deposits
K-DEPENDENT combs (`2^K−2` + `Σ = 2^{K-1}−4K+8` + `1^{21}`) whose naive-repack total
misses `2^{K+1}−3` by a `Θ(K)` residual (`bigCascade_not_doubling`; `−7,−6,−3` at
`K=10,11,14`).  The doubling `2^K−3 → 2^{K+1}−3` is a COMPOUND whose CLOSING step — the
repack + register-rebuild (episodes 5,6) — couples to `2^K` and is captured by NO lemma
here, so `doubling_transport`/`doubling_transport_mid`'s `H_repack` is NOT discharged.
What §5g DOES close: episodes 3+4 as one proven halt-free transport, tightening both
`H_entry` (now → the marked-big-block start) and `H_repack` (now from the ground-cascade
config).  **§5h then EXTRACTED episodes 5,6 (`H_repack`) cell-for-cell from the raw machine
and REFUTED their formalizability as posed** (the fourth framing scrutinised): the whole
doubling phase is a single interleaved shrinking-comb odometer braid (`Θ(2^{2K})` steps,
`R=L=Θ(2^K)`, register `D`-loops braided throughout), with NO contiguous repack/rebuild
split, NO fixed-length tile, and NO uniform-shift invariant; and `bigCascade`'s
`(10)^10`-marked input is `0`-occurrence on the real path, so `M_mid(k)` is off-path and
`doubling_transport_mid`'s hypotheses are jointly unsatisfiable on the real trajectory.
`H_repack` is NOT discharged; the ×2 doubling couples to the full cascade + `2^K` and is
captured by NO lemma here.  The low-phase composition (episodes 1,2), the compound ×2
(episodes 5,6), and top-level `x2_nonhalt` remain not formalized.  x2 stays `[OPEN]`.
No label upgraded. -/

end X2
