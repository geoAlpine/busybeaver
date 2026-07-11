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
and now the G2 big-block `(10)^10`-marked sweep as an arbitrary-length halt-free
lemma (`markedChew`/`markedBlock`), all with clean axioms.  The G3 accumulator-to-`2^K`
IDENTITY does NOT close as originally posed, and — the honest finding this session —
neither does the G2 ×2 doubling: the marked sweep is the block→comb CHEW, and the
doubling `2^K−3 → 2^{K+1}−3` is a COMPOUND (chew → repack → rebuild), so
`doubling_transport`'s `H_repack` is NOT discharged.  The low-phase composition, the
compound ×2, and top-level `x2_nonhalt` are not formalized.  x2 stays `[OPEN]`.  No
label upgraded. -/

end X2
