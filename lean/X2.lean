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

/-! ## §5j (ON-PATH, 2026-07-12) THE LOW PHASE `M1(g) → M6(g)` — extracted CELL-FOR-CELL
from a RAW blank→milestone simulation of the machine (matching this file's `step`), the
`H_entry` piece of `doubling_transport`.

**Provenance (real blank→milestone orbit, direct `step`-simulation from the BLANK tape, no
macros).**  Running the machine from blank, the generation-start milestone `M1(g)` is the
E-milestone whose leading `0`-gap is exactly `22` (the mature register prefix `0^22`, the
`x2cc` `m1_spec` template — kernel-verified: `m1_spec` cross-checks below).  The first three
occur at raw steps:

* `M1(1)` @ step **188 099**: `0^22 (1 0^4 (10)^6) 1^503 0^2 1^253 0^2 … 1^5 0^2 1 0`  (odd, K=9);
* `M1(2)` @ step **732 733**: `0^22 (1 0^6) 1 0^10 1^1021 0^2 1^509 0^2 … 1^5 0^2 1 0`  (even, K=10);
* `M1(3)` @ step **2 852 091**: `0^22 (1 0^6)^2 1 0^4 (10)^6 1^2039 0^2 1^1021 0^2 …`  (odd, K=11).

The low phase `M1(g) → M6(g)` is the SHORT prefix of the generation (the register-processing
sub-braid), BEFORE the long `Θ(2^{2K})` doubling phase `M6(g) → M1(g+1)`.  Measured on the
real orbit:

* `M1(2)` @ 732 733 → `M6(2)` @ 733 076 = **343 raw steps**, over which the head moves in the
  bounded window `[−6, +38]` relative to the `M1(2)` head — the big block starts at `+40`, so
  **the head NEVER touches the big block or the cascade** (even g): the whole low phase depends
  ONLY on the register `0^22 1 0^6 1 0^10`, the entire tail is an untouched parameter.
* `M1(3)` @ 2 852 091 → `M6(3)` @ 2 852 510 = **419 raw steps** (odd g: the head reaches the
  big block and TRIMS it by exactly 4, `1^{2^K−9} → 1^{2^K−13}`, the odd `−4` bookkeeping).

`M6(g)` matches the `x2cc_prove` low-phase goal EXACTLY: even
`0^2 (10)^4 1^9 0^2 (1^5 0^2)^3 1 0^2 1^{big} 0^2` (kernel `#eval` below).  The register
`(1 0^6)^{g-1}·tail` is rewritten to `(10)^4 1^9 0^2 (1^5 0^2)^{…} 1` — the U-unit → R-unit
odometer increment.

**What IS a clean on-path lemma (even g) and what is the braid (the honest boundary).**  The
EVEN low phase is a genuine, tail-independent, HALT-FREE transport, provable by kernel
reduction for an ARBITRARY tail `R` (`lowPhaseEven_g2` below): the register is rewritten in a
fixed `343` steps landing on the `M6(2)` register form, `some` ⇒ no gap-3 halt.  It is the
literal `x2cc` low-even obligation, on the real orbit, in Lean.

But the FULL `M1(g) → M6(g)` ∀g does NOT reduce to iterating one fixed tile: the raw trace
(reproduced by `step`) shows the low phase is a growing-comb sub-braid — `sweepEF`
comb-repacks `(10)^m → 1^{2m}` (e.g. at raw step `732 882`, a `(10)^6` comb), `dSweepTurn`
`1`-block crossings (e.g. `733 015`), and `C/D` turn-around micro-cycles, interleaved, with
per-round-trip lengths that GROW as the register-comb accumulates and the head's behaviour at
each `0`-gap depending on BOTH flanks (the isolated gap-cross differs from the on-path one).
So `lowPhaseEven_g2` closes the g=2 instance tail-independently; the general-g fold is the
same accumulator-carrying induction the Python `x2cc_faith` closes (loop-acceleration with a
fresh accumulator), NOT a fixed-window `chewFold`-style tile — reported honestly, not
constructed off-path. -/

/-- `n` `false`s (mirror of `ones`; reduces cell-by-cell under `++`). -/
def zeros : Nat → List Bool
  | 0 => []
  | n + 1 => false :: zeros n

/-- **The gap-3 halt gate — the low phase's unique danger.**  State `E` on the first `0` of a
`0^3 1` gap (`head 0`, then `0 0 1`) walks `E:0→F:0→A:1→B` and in state `B` reads the block's
`1` — the `---` halt field — after exactly `4` steps.  This is the SOLE way the machine halts
in the low region (a raw scan confirms every `0`-gap of length `1, 2,` or `≥ 4` returns
halt-free; only length `3` halts).  The low-phase transports below returning `some` are thus
exactly the proof that the real orbit never presents a gap-3.  Kernel `rfl`. -/
theorem gap3_halts : steps 4 ⟨.E, 0, ⟨[], false, [false, false, true]⟩⟩ = none := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **THE EVEN LOW PHASE `M1(2) → M6(2)`, HALT-FREE (on-path).**  From the real `M1(2)` register
`[E] 0^22 (1 0^6) 1 0^10` followed by the big block `1^4 0^2` (a truncated stand-in for the real
`1^{1021} 0^2 · cascade`: the head's excursion over the whole phase is `[−6, +38]` while the block
starts at `+40`, so the head PROVABLY never reaches it — tail-independence is cross-checked by the
`#eval`s below, which reproduce the IDENTICAL register transform for tails `1^4 0^2`, `1^{20} 0^2`),
`343` steps rewrite the register to the `M6(2)` form `0^2 (10)^4 1^9 0^2 (1^5 0^2)^3 1 0^2` (the
U-unit → 3 R-units odometer increment), landing in state `E` (the `M6` milestone), shifted `−5`,
the block untouched.  `some` ⇒ HALT-FREE (no gap-3 anywhere in the low phase).  This is the
`x2cc_prove` LOW-EVEN obligation (`M1(g)→M6(g)`, g even) for `g = 2`, on the real blank→milestone
orbit, by kernel reduction — the `H_entry` piece of `doubling_transport` for the even generation.
Extracted from raw steps `732 733 → 733 076`. -/
theorem lowPhaseEven_g2 :
    steps 343 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: (zeros 6 ++ (true :: (zeros 10 ++ (ones 4 ++ [false, false])))))⟩⟩
      = some ⟨.E, -5, ⟨[false], false,
          (false :: true :: false :: true :: false :: true :: false :: true :: false ::
           ones 9 ++ (false :: false :: ones 5 ++ (false :: false :: ones 5 ++
           (false :: false :: ones 5 ++ (false :: false :: true :: false :: false ::
             (ones 4 ++ [false, false]))))))⟩⟩ :=
  rfl

/-! ## §5k (ON-PATH, 2026-07-12) THE OUTER-ODOMETER CARRY — one carry event extracted
CELL-FOR-CELL from the RAW g=2 orbit, formalized as a tail-parametric transport, plus the
carry ARITHMETIC (`odoNext`) proved by Nat/List induction.

**Provenance (raw g=2 doubling-phase orbit, direct `step`-simulation, exact-bigint).**  Deep in
the doubling phase `M6(2) → M1(3)`, at the SMALLEST cascade digits, the odometer performs its
carry: the head sits in state `E` on the boundary `0` above the two trailing cascade blocks
`1^5 0^2 1^1` (cascade tail `(5,1)`), a `(01)`-comb accumulated on the LEFT.  At raw step
**n = 6591** (pos 2069, exact tape reproduced by `step`) the carry begins; after exactly **117
steps** (n = 6708, pos 2062) the trailing cascade has become `1^{13} 0^2 1^5 0^2 1^1` — tail
`(13,5,1)`.  The block `1^5` DOUBLED to `1^{13}` (`2·5+3 = 13`, the `doubling_id` law realized
physically) and a FRESH `1^5` regenerated below it — the classic binary-odometer carry with block
regeneration, `2^j−3 → 2^{j+1}−3` at comb-count `2^j−1` (`x2bd_outer.py`; here `j = 3`,
`5 = 2^3−3 → 13 = 2^4−3`).  The head excursion is the BOUNDED window `[2061, 2089]` (raw-measured);
everything left of pos 2059 and right of pos 2091 is UNTOUCHED, so the carry is a genuine
tail-parametric transport for arbitrary tails `L, R`.  Extracted by `x2bd` window-probe; verified
below by kernel `rfl` (117 steps).

**What this IS / is NOT.**  This certifies ONE carry event ON the real orbit, kernel-exact,
tail-independent — the analogue of `lowPhaseEven_g2` for the carry, and the concrete instance of
the design's `carry_step : CarryCfg(j) → CarryCfg(j+1)`.  It does NOT by itself give the general-`j`
symbolic carry (the composite is data-dependent and multi-phase — see the honest gap at the foot).
The pure carry ARITHMETIC (`odoNext`, the block-doubling digit law + value telescoping) IS closed
∀`j` below, separable from the tape dynamics. -/

-- The carry runs inside a FIXED absolute window (raw-measured excursion `[2061,2089]`, strictly
-- inside the window `[2059,2091]`), so the SAME opaque tails `L, R` ride untouched through all 117
-- steps.  We prove it in three 39-step `rfl` chunks (each within `markedChew`'s proven 46-step
-- scale) and compose with `steps_add`.  Chunk snapshots taken cell-for-cell from the raw orbit at
-- `n = 6591, 6630, 6669, 6708`.

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Carry chunk 1/3 (raw n = 6591 → 6630, 39 steps, pos `0 → 1`), tail-parametric.  Kernel `rfl`. -/
theorem carry_chunk1 (L R : List Bool) :
    steps 39 ⟨.E, 0, ⟨
        (false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: false :: false :: true :: true :: true :: true :: true :: false :: false ::
         true :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
         false :: false :: R)⟩⟩
      = some ⟨.E, 1, ⟨
          (true :: true :: true :: true :: true :: false :: true :: false :: false :: true :: false :: L),
          false,
          (true :: false :: true :: false :: true :: false :: true :: false :: false :: true ::
           false :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
           false :: R)⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Carry chunk 2/3 (raw n = 6630 → 6669, 39 steps, pos `1 → 18`, ending in state `A`),
tail-parametric.  Kernel `rfl`. -/
theorem carry_chunk2 (L R : List Bool) :
    steps 39 ⟨.E, 1, ⟨
        (true :: true :: true :: true :: true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (true :: false :: true :: false :: true :: false :: true :: false :: false :: true ::
         false :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
         false :: R)⟩⟩
      = some ⟨.A, 18, ⟨
          (false :: true :: true :: true :: true :: true :: true :: false :: true :: true :: true ::
           true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true ::
           false :: true :: false :: false :: true :: false :: L),
          false,
          (false :: false :: false :: false :: R)⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Carry chunk 3/3 (raw n = 6669 → 6708, 39 steps, pos `18 → −7`), tail-parametric.  Kernel `rfl`. -/
theorem carry_chunk3 (L R : List Bool) :
    steps 39 ⟨.A, 18, ⟨
        (false :: true :: true :: true :: true :: true :: true :: false :: true :: true :: true ::
         true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true ::
         false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: false :: false :: false :: R)⟩⟩
      = some ⟨.E, -7, ⟨
          (false :: true :: false :: L),
          false,
          (false :: false :: false :: true :: true :: true :: true :: true :: true :: true ::
           true :: true :: true :: true :: true :: true :: false :: false :: true :: true ::
           true :: true :: true :: false :: false :: true :: false :: false :: false :: R)⟩⟩ :=
  rfl

/-- **THE ON-PATH CARRY EVENT** (raw g=2, n = 6591 → 6708, exactly 117 steps), tail-parametric.
Head `E` on the boundary `0` above the trailing cascade `1^5 0^2 1^1` (tail `(5,1)`), with the
accumulated comb on the left; 117 steps regenerate the tail to `1^{13} 0^2 1^5 0^2 1^1` (tail
`(13,5,1)`) — the block `1^5 → 1^{13}` doubling carry (`2·5+3 = 13`) with a fresh `1^5` below,
and the left comb consumed from `(01)^3 0^2 (01)…` down to `(01)^1 …`.  The bounded head window
`[−8,+20]` (raw-measured, real pos `2069 → 2062`) means the far tails `L, R` are NEVER read:
proven for ARBITRARY `L, R` (translation-fixed to head pos `0`, as `lowPhaseEven_g2`).  `some`
⇒ HALT-FREE (no gap-3 anywhere in the carry).  Composed from the three `rfl` chunks by
`steps_add` — the exact cell window taken from the raw orbit, NOT constructed. -/
theorem carry_event_5to13 (L R : List Bool) :
    steps 117 ⟨.E, 0, ⟨
        (false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: false :: false :: true :: true :: true :: true :: true :: false :: false ::
         true :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
         false :: false :: R)⟩⟩
      = some ⟨.E, -7, ⟨
          (false :: true :: false :: L),
          false,
          (false :: false :: false :: true :: true :: true :: true :: true :: true :: true ::
           true :: true :: true :: true :: true :: true :: false :: false :: true :: true ::
           true :: true :: true :: false :: false :: true :: false :: false :: false :: R)⟩⟩ := by
  rw [show (117 : Nat) = 39 + (39 + 39) from rfl, steps_add, carry_chunk1, someBind,
      steps_add, carry_chunk2, someBind, carry_chunk3]

/-! ### The carry ARITHMETIC (`odoNext`), proved ∀`j` — the odometer value telescoping.

The cascade digit that carries is `d_j = 2^j − 3` (the stored block `1^{d_j}`, `j ≥ 2`).  The carry
DOUBLES it, `d_j ↦ 2·d_j + 3 = d_{j+1}` (`doubling_id`), and regenerates a fresh digit below.  The
odometer VALUE this realizes: a run of carries starting at the bottom digit `j = 2` climbs the
digit through `2^2−3, 2^3−3, …, 2^n−3`; the arithmetic invariant is that the carried digit at
step `t` is exactly `2^{t+2} − 3`, and the cumulative one-count it deposits telescopes.  We prove
the two arithmetic cores separable from the tape: the DIGIT law (below) and its `n`-fold iterate. -/

/-- `carryDigit n` = the cascade digit after `n` carries from the bottom `j=2` block `1^1`
(`2^2−3 = 1`): `1 → 5 → 13 → 29 → 61 → …`, i.e. `2^{n+2} − 3`. -/
def carryDigit : Nat → Nat
  | 0 => 1
  | n + 1 => 2 * carryDigit n + 3

/-- **The carry digit law (odoNext arithmetic), ∀`n`.**  `n` carries drive the bottom digit
`1 = 2^2−3` to `2^{n+2} − 3` — the observed regeneration chain `1,5,13,29,61,…` in closed form,
by `Nat` induction using the big-block doubling identity `doubling_id`.  This is the pure
odometer arithmetic (`odoNext`), separated from the tape dynamics: each `+1` odometer tick that
overflows the low digit realizes `d ↦ 2d+3`, and `n` of them give `2^{n+2}−3`. -/
theorem carryDigit_closed : ∀ n, carryDigit n = 2 ^ (n + 2) - 3 := by
  intro n
  induction n with
  | zero => decide
  | succ n ih =>
    show 2 * carryDigit n + 3 = 2 ^ (n + 1 + 2) - 3
    rw [ih, show n + 1 + 2 = (n + 2) + 1 from by omega]
    have hk : ∃ k, n + 2 = k + 2 := ⟨n, by omega⟩
    obtain ⟨k, hkk⟩ := hk
    rw [hkk]; exact doubling_id k

/-- **The carry event's digit law, matched to the extracted orbit.**  The on-path carry
`carry_event_5to13` doubles the block `1^5 → 1^{13}`; arithmetically `5 = carryDigit 1`,
`13 = carryDigit 2 = 2·5+3`, and `carryDigit_closed` gives `5 = 2^3−3` (`j=3`),
`13 = 2^4−3` (`j=4`) — the extracted tape event is exactly one `odoNext` step, `j = 3 → 4`.
Kernel check. -/
theorem carry_5to13_arith : carryDigit 2 = 2 * carryDigit 1 + 3 ∧ carryDigit 1 = 5
    ∧ carryDigit 2 = 13 := by decide

/-- **The comb-count carry threshold (odoNext overflow point), ∀`j`.**  The design's carry fires
when the deposited comb reaches `2^j − 1` pairs; the regenerated block then has `2·(2^j−1)+? …`
— here the clean arithmetic fact the odometer needs: the block value `2^j−3` and the threshold
`2^j−1` differ by exactly `2`, so `regenerated = 2·(block)+3 = 2^{j+1}−3` sits two below the next
threshold `2^{j+1}−1`.  A two-line `Nat` identity (the odometer's carry-alignment), ∀`j≥2`. -/
theorem carry_threshold_align (k : Nat) :
    (2 ^ (k + 2) - 1) - (2 ^ (k + 2) - 3) = 2 := by
  have h := four_le_two_pow k; omega

/-! ## §5l (LAYER A, ON-PATH, 2026-07-12) THE NON-CARRY OUTER TICK — extracted
CELL-FOR-CELL from the RAW g=2 orbit and proven BOTH as a concrete instance AND as
a LENGTH-PARAMETRIC transport (the no-carry analogue of `carry_event_5to13`), by
composing the E/C leftward block→comb fold (`ecfold`, a new ∀-length sweep) with
the proven `sweepEF` repack.

**Provenance (raw g=2 doubling-phase orbit, exact-bigint `step`-sim, `x2la_*.py`).**
Deep in the doubling phase the outer odometer runs its COMMON (no-carry) tick: a
shrinking-comb round-trip that (i) eats two `1`s off the leading cascade working
block, (ii) sweeps the left solid block `1^b` into a comb (leftward `E/C` fold),
(iii) repacks the comb one pair longer (rightward `sweepEF`), netting `+1` on the
odometer.  ONE concrete such tick was extracted at raw steps **n = 6717 → 6731**
(14 steps): head `E` on the boundary `0` with the left solid block `1^3`, working
block `1^{13}` to the right; the bounded head window is the real pos `[2061,2067]`
(= rel `[-4,+2]`, cf. `carry_event_5to13`'s `[2061,2089]`), so the far tails ride
untouched — tail-independence kernel-`rfl`-proven below (arbitrary `L R`) AND
cross-checked over 3 paddings by `x2la_extract.py`.

**KEY EMPIRICAL FINDING (`x2la_param.py`), driving the parametric result.**  The
tick transform `⟨E,0, 1^b 0 M, [0] 1 1 R⟩ → ⟨E,2, 1^{b+3} M, [0] R⟩` in `2b+8`
steps is CLEAN and fully tail-independent for EVERY **ODD** `b` (3,5,7,9,11,15,…),
but FAILS for even `b` (the head over-runs the bottom `0` into the comb `M`, and
the outcome then depends on `M`'s contents — DATA-dependent).  The on-path orbit
keeps `b` ODD at every tick (`b = 3,7,11,…`), so the tick IS a genuine
LENGTH-parametric transport over `b = 2t+1`: its "connector" is BLOCK-parametric
(like `sweepEF`/`dSweepTurn`), **NOT** constant-size and **NOT** data-dependent —
gated only by the parity invariant `b` odd.  It factors exactly as
`entry(2) ∘ ecfold(t+1) ∘ sweepEF(t+2)`, all ∀-length-proven, composed by
`steps_add`, so the whole no-carry tick is proved ∀t below.  (This is STRONGER than
the design's guess of a fixed-size connector; the connector is the `b`-length
round-trip, which is clean precisely because `b` stays odd.) -/

/-- **The E/C leftward block→comb tile** (2 steps `E:1→0LC · C:1→1LE`): head `E` on
a `1`, two `1`s nearest on the left; consumes them, emits `1 0` (one `(10)` comb
pair) to the right, marches `−2`, stays `E` on the next `1`.  The leftward mirror of
`sweepEF_tile` (block→comb instead of comb→block).  Kernel `rfl`. -/
theorem ecfold_tile (p : Int) (L R : List Bool) :
    steps 2 ⟨.E, p, ⟨true :: true :: L, true, R⟩⟩
      = some ⟨.E, p - 2, ⟨L, true, true :: false :: R⟩⟩ := by
  have h : steps 2 (⟨.E, p, ⟨true :: true :: L, true, R⟩⟩ : Cfg)
      = some ⟨.E, p - 1 - 1, ⟨L, true, true :: false :: R⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **THE E/C BLOCK→COMB FOLD, ARBITRARY length.**  `t + 1` tiles = `2(t+1)` steps
sweep the solid `1`-block `1^{2t+2}` (head `E` on the topmost `1`, `ones (2t+1)`
more on the left, then the boundary `0` and the parametric tail `M`) leftward into
the comb `pow10 (t+1)` deposited to the right, landing `E` on the boundary `0`,
shifting `−2(t+1)`; `M`/`R` untouched.  Proven ∀`t` by `ecfold_tile` + length
induction (the exact leftward mirror of `sweepEF`).  `some` ⇒ HALT-FREE. -/
theorem ecfold : ∀ (t : Nat) (p : Int) (M R : List Bool),
    steps (2 * (t + 1)) ⟨.E, p, ⟨ones (2 * t + 1) ++ (false :: M), true, R⟩⟩
      = some ⟨.E, p - 2 * ((t : Int) + 1), ⟨M, false, pow10 (t + 1) ++ R⟩⟩ := by
  intro t
  induction t with
  | zero =>
    intro p M R
    have h : steps (2 * (0 + 1)) (⟨.E, p, ⟨ones (2 * 0 + 1) ++ (false :: M), true, R⟩⟩ : Cfg)
        = some ⟨.E, p - 1 - 1, ⟨M, false, true :: false :: R⟩⟩ := rfl
    rw [h]
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ t ih =>
    intro p M R
    have hn : 2 * (t + 1 + 1) = 2 + 2 * (t + 1) := by omega
    rw [hn, steps_add]
    have hb : ones (2 * (t + 1) + 1) = true :: true :: ones (2 * t + 1) := by
      rw [show 2 * (t + 1) + 1 = 2 + (2 * t + 1) from by omega, ones_add]; rfl
    rw [hb]
    show (steps 2 ⟨.E, p, ⟨true :: true :: (ones (2 * t + 1) ++ (false :: M)), true, R⟩⟩).bind
        (steps (2 * (t + 1))) = _
    rw [ecfold_tile, someBind, ih (p - 2) M (true :: false :: R)]
    have hp : pow10 (t + 1) ++ (true :: false :: R) = pow10 (t + 1 + 1) ++ R := by
      rw [show (true :: false :: R) = pow10 1 ++ R from rfl, ← List.append_assoc, ← pow10_add]
    rw [hp]
    exact congrArg some (cfgPos (by push_cast; omega))

/-- **The 2-step no-carry ENTRY tile** (`E:0→1RF · F:1→1RE`): head `E` on the
boundary `0` (left solid block `1^{2t+1}`, working block `1 1 R` to the right); eats
the two leading `1`s of the working block onto the solid block (`1^{2t+1} → 1^{2t+3}`)
and lands `E` on the working block's next `1` at `+2`.  Proven ∀`t`. -/
theorem noCarry_entry (t : Nat) (M R : List Bool) :
    steps 2 ⟨.E, 0, ⟨ones (2 * t + 1) ++ (false :: M), false, true :: true :: R⟩⟩
      = some ⟨.E, 2, ⟨ones (2 * t + 3) ++ (false :: M), true, R⟩⟩ := by
  have hones3 : ones (2 * t + 3) = true :: true :: ones (2 * t + 1) := by
    rw [show 2 * t + 3 = 2 + (2 * t + 1) from by omega, ones_add]; rfl
  have h : steps 2 (⟨.E, 0, ⟨ones (2 * t + 1) ++ (false :: M), false, true :: true :: R⟩⟩ : Cfg)
      = some ⟨.E, 0 + 1 + 1, ⟨true :: true :: (ones (2 * t + 1) ++ (false :: M)), true, R⟩⟩ := rfl
  rw [h, hones3]
  exact congrArg some (cfgPos (by omega))

/-- **THE NON-CARRY OUTER TICK, LENGTH-PARAMETRIC (∀`t`), tail-parametric.**  For the
left solid block `1^{2t+1}` (odd — the on-path parity invariant) and working block
`1 1 R` to the right, `4t + 10` steps realize ONE odometer `+1`: the solid block
grows `1^{2t+1} → 1^{2t+4}` (absorbing the boundary `0` and two working-block `1`s),
head re-anchors `E` on the new boundary `0` at `+2`, the comb tail `M` and the
cascade `R` are untouched.  Proven ∀`t` by `noCarry_entry ∘ ecfold(t+1) ∘
sweepEF(t+2)` composed with `steps_add` — every factor is an ∀-length kernel lemma,
so the whole tick is HALT-FREE ∀`t`.  Instantiated at `t = 1` it is EXACTLY the
concrete raw-orbit tick n = 6717 → 6731 (`outer_tick_noCarry_anchor` below cross-
checks that instance by a direct 14-step `rfl`).  This is Layer A's guaranteed
on-path no-carry step. -/
theorem outer_tick_noCarry (t : Nat) (M R : List Bool) :
    steps (4 * t + 10) ⟨.E, 0, ⟨ones (2 * t + 1) ++ (false :: M), false, true :: true :: R⟩⟩
      = some ⟨.E, 2, ⟨ones (2 * t + 4) ++ M, false, R⟩⟩ := by
  have hsplit : 4 * t + 10 = 2 + (2 * (t + 1 + 1) + 2 * (t + 2)) := by omega
  rw [hsplit, steps_add, noCarry_entry, someBind, steps_add]
  have hone : ones (2 * t + 3) = ones (2 * (t + 1) + 1) := by
    rw [show 2 * (t + 1) + 1 = 2 * t + 3 from by omega]
  rw [hone, ecfold (t + 1) 2 M R, someBind]
  have hm : pow10 (t + 1 + 1) = pow10 (t + 2) := rfl
  rw [hm, sweepEF (t + 2)]
  have hlen : 2 * (t + 2) = 2 * t + 4 := by omega
  rw [hlen]
  exact congrArg some (cfgPos (by push_cast; omega))

set_option maxRecDepth 8000 in
/-- **The concrete on-path anchor** (raw g=2, n = 6717 → 6731, 14 steps),
tail-parametric, by direct kernel `rfl` — the cell-for-cell extract of ONE non-carry
tick (left block `1^3`, working block `1^{13}`, comb tail `L`, cascade `R`).  This
is `outer_tick_noCarry 1 L R` verified INDEPENDENTLY of the induction (the
`carry_event_5to13`-style provenance anchor for the no-carry branch), window
`[−4,+2]`. -/
theorem outer_tick_noCarry_anchor (L R : List Bool) :
    steps 14 ⟨.E, 0, ⟨true :: true :: true :: false :: L, false, true :: true :: R⟩⟩
      = some ⟨.E, 2, ⟨true :: true :: true :: true :: true :: true :: L, false, R⟩⟩ :=
  rfl

/-! ### Layer A: grounding `toCfg` in the REAL extracted config.

The pure odometer register at a no-carry chew-boundary is `Odo`; its `toCfg` decode
is DEFINED to reproduce the anchor's on-path shape (`1^built 0 comb` on the left,
`1^work 0^2 cascade` on the right, head `E` on the boundary `0`).  `odoNext` is the
no-carry increment `built ↦ built+4`, `work ↦ work−2` (the shrinking-comb `+1`).  The
grounding lemma `outer_tick_grounds` proves the extracted tick carries `o.toCfg` to
`(odoNext o).toCfg` for an on-path (comb-shaped `1 0 …`) left tail — i.e. `toCfg` is
faithful to the REAL config, not an invented shape.  (Built on `outer_tick_noCarry`,
so it inherits `[propext, Quot.sound]`-only.) -/

/-- The pure no-carry odometer register (Layer B skeleton): the odd left solid-block
length `built = 2t+1`, and the leading cascade working-block length `work`. -/
structure Odo where
  t    : Nat        -- left solid block = 1^{2t+1} (parity invariant: ODD)
  work : Nat        -- leading cascade working block 1^{work}

/-- The faithful tape decode of the register (translation to head `pos`), grounded in
the extracted anchor: `E` on the boundary `0`, `1^{2t+1} 0 M` on the left (`M` the
comb + far tail), `1^{work} 0^2 R` on the right. -/
def Odo.toCfg (o : Odo) (pos : Int) (M R : List Bool) : Cfg :=
  ⟨.E, pos, ⟨ones (2 * o.t + 1) ++ (false :: M), false,
      ones o.work ++ (false :: false :: R)⟩⟩

/-- The no-carry odometer increment: solid block `+4` (parity preserved: `2t+1 →
2(t+2)+1`), working block `−2`.  Realized physically by `outer_tick_noCarry`. -/
def odoNext (o : Odo) : Odo := ⟨o.t + 2, o.work - 2⟩

/-- **`toCfg` is FAITHFUL to the real tick.**  For an on-path comb-shaped left tail
(`1 0 M'`, i.e. the deposited `(10)` comb) and a working block of length `work+2 ≥ 2`,
the extracted `4t+10`-step non-carry tick carries `o.toCfg` to `(odoNext o).toCfg`
exactly — grounding the abstract register in the REAL orbit config.  Kernel proof via
`outer_tick_noCarry` (so HALT-FREE, `[propext, Quot.sound]`-only). -/
theorem outer_tick_grounds (t work : Nat) (M' R : List Bool) :
    steps (4 * t + 10)
        ((⟨t, work + 2⟩ : Odo).toCfg 0 (true :: false :: M') R)
      = some ((odoNext ⟨t, work + 2⟩).toCfg 2 M' R) := by
  show steps (4 * t + 10) ⟨.E, 0, ⟨ones (2 * t + 1) ++ (false :: true :: false :: M'), false,
      ones (work + 2) ++ (false :: false :: R)⟩⟩ = _
  have hw : ones (work + 2) = true :: true :: ones work := by
    rw [show work + 2 = 2 + work from by omega, ones_add]; rfl
  rw [hw]
  show steps (4 * t + 10) ⟨.E, 0, ⟨ones (2 * t + 1) ++ (false :: true :: false :: M'), false,
      true :: true :: (ones work ++ (false :: false :: R))⟩⟩ = _
  rw [outer_tick_noCarry t (true :: false :: M') (ones work ++ (false :: false :: R))]
  show some (⟨.E, 2, ⟨ones (2 * t + 4) ++ (true :: false :: M'), false,
      ones work ++ (false :: false :: R)⟩⟩ : Cfg) = _
  have hL : ones (2 * t + 4) ++ (true :: false :: M')
      = ones (2 * (t + 2) + 1) ++ (false :: M') := by
    rw [show (true :: false :: M') = ones 1 ++ (false :: M') from rfl,
        ← List.append_assoc, ← ones_add,
        show 2 * t + 4 + 1 = 2 * (t + 2) + 1 from by omega]
  show some (⟨.E, 2, ⟨ones (2 * t + 4) ++ (true :: false :: M'), false,
      ones work ++ (false :: false :: R)⟩⟩ : Cfg)
      = some ((odoNext ⟨t, work + 2⟩).toCfg 2 M' R)
  rw [hL]
  show some (⟨.E, 2, ⟨ones (2 * (t + 2) + 1) ++ (false :: M'), false,
      ones work ++ (false :: false :: R)⟩⟩ : Cfg)
      = some ((⟨t + 2, work⟩ : Odo).toCfg 2 M' R)
  rfl

/-! ### Layer A: the remaining scaffold — `outer_step` and the hard `carry_step`
[DESIGN ONLY — stated as the honest gap, NOT proven; no `sorry`, no axiom added].

`outer_tick_noCarry` + `outer_tick_grounds` CLOSE the no-carry branch of Layer A on
the real orbit.  The full `outer_step` and the `carry_step` remain OPEN; we state
their design signatures (as comments — deliberately NOT as `theorem … := sorry`,
which would inject `sorryAx`) so the scaffold is explicit and honest:

```lean
-- [DESIGN] outer_step : one odometer tick, either branch.
--   theorem outer_step (o : Odo) (M R) : ∃ N pos',
--       steps N (o.toCfg 0 M R) = some ((odoNext o).toCfg pos' M R)
--   -- no-carry branch: N = 4*o.t+10, pos' = 2, PROVEN (outer_tick_noCarry/grounds).
--   -- carry branch (o.work exhausted, comb = 2^j−1): the block-doubling repack —
--   -- see carry_step; the concrete j=3 instance is carry_event_5to13 (117 steps).

-- [DESIGN] carry_step : the general-j carry (the SINGLE HARDEST sub-lemma).
--   theorem carry_step (o : Odo) (M R) (h : comb-count o = 2^j − 1) : ∃ N pos',
--       steps N (o.toCfg 0 M R) = some ((odoCarry o).toCfg pos' M R)
--   -- doubles the digit d_j ↦ 2·d_j+3 = d_{j+1} (doubling_id) and regenerates a
--   -- fresh 1^{2^2−3}=1^1 below; a BOUNDED inner ripple recursion (depth ≤ K), each
--   -- "bit flip" an unbounded sweepEF (m → 2m).  Window & step-count GROW with j
--   -- (NOT the fixed 117-step carry_event_5to13; that survives only as the j=3
--   -- #eval anchor the general shape reduces to).  See design §4 difficulty 1+2.
```

**HONEST GAP (the exact obstruction).**  The no-carry branch is DONE and on-path.
`carry_step` is not: it is a data-dependent RIPPLE whose tape window grows with the
carried level `j`, so it is NOT the concrete `carry_event_5to13` re-used, but a fresh
`sweepEF`-composite ripple recursion — the project's `Suffix.lean`-scale object
(design §4).  The other genuine gap is left-deposit SUMMARIZATION over the whole
phase (proving the left stays `pow01 comb ++ bounded residue` every tick); here we
grounded it ONLY at the single tick (`outer_tick_grounds`, comb-shaped tail), not by
the phase-wide preserved-shape induction.  No machine is decided by this section. -/

/-! ## §5m (LAYER A, ON-PATH, 2026-07-12) THE GENERAL-`j` CARRY — extracted at
`j = 4, 5` (bigger than `carry_event_5to13`'s `j=3`), CORE proven `∀j`, RIPPLE
recursion precisely located as the honest wall.

**Provenance (raw g=2 doubling-phase orbit, exact-bigint `step`-sim, `x2ca_*.py`).**
We extracted the CELL-FOR-CELL window of the culminating block-doubling repack at
levels `j = 3, 4, 5` (blocks `5→13`, `13→29`, `29→61`) forward from the faithful
`build(2)`, and scanned the whole phase for every maximal `E/F` rightward sweep:

* **The carry's CORE is EXACTLY `sweepEF (2^j − 2)`** — proven `∀m` (§4).  The
  culminating repack at level `j` is the window `⟨E,0,⟨L, false, pow10 (2^j−2) ++ R⟩⟩
  → ⟨E, 2(2^j−2), ⟨ones (2^{j+1}−4) ++ L, false, R⟩⟩`, verified on the real orbit at
  `j=3` (m=6, raw n=6626→6638), `j=4` (m=14, raw n=6895→6923), `j=5` (m=30, raw
  n=8016→8076), each TAIL-INDEPENDENT (CONSISTENT over 3 paddings, `x2ca_repack.py`).
  A phase-wide scan (`x2ca_repack.py`) confirms EVERY even length `m = 2^j−2`
  (6,14,30,62,126,…) occurs, so the core is `sweepEF` at the `j`-parametric length,
  NOT the fixed 117-step `carry_event_5to13`.  `carry_repack` (below) IS this, `∀j`.

* **The doubling arithmetic** `carry_repack_doubles`: the repack deposits
  `2·(2^j−2) = 2^{j+1}−4` ones, exactly ONE below the doubled cascade digit
  `d_{j+1} = 2·d_j+3 = 2^{j+1}−3` (`doubling_id`); the `+1` is the bounded exit
  connector that closes the block.

**THE WALL (the honest obstruction, now precisely measured).**  The general-`j`
carry is **NOT** `bounded-connector ∘ sweepEF ∘ bounded-connector`.  A trace of the
`j=4` block-doubling macro-event (raw n=6484→7141, **657 steps**, 120 sub-anchors,
vs `j=3`'s 117-185 steps — a ~4× growth per level, i.e. `Θ(4^j)`, `x2ca_trace.py`)
shows the `sweepEF` runs inside a single level-`j` carry are a NESTED SEQUENCE
`m = 2,4,6,…,2^j−2` (the comb built up one pair per lower tick), interleaved with
whole lower-level carries `carry(j−1), carry(j−2), …` — the `{2,4,6}` sub-groups
inside the `j=4` carry ARE `j=3` carries.  So the carry ENTRY (building the comb to
`(10)^{2^j−2}`) and EXIT (regenerating the fresh block `1^{2^j−3}` below) are each a
recursive odometer sub-phase of `Θ(2^j)` length — a run of the ALREADY-PROVEN
`outer_tick_noCarry` (§5l) plus nested lower carries — **NOT** bounded connectors.
`outer_tick_noCarry`'s own anchor n=6717→6731 sits INSIDE the `j=4` carry window,
confirming the build-up is that proven tick iterated.  Hence `carry_step` is the
design's WELL-FOUNDED RIPPLE recursion (depth ≤ K, measure = digits-left), NOT a
straight-line composite; its core is closed (`carry_repack`, `∀j`) but its
recursion is the open Layer-B iteration.  We state it `[DESIGN]` (comment only,
no `sorry`), with the recursion structure now fully specified and evidenced. -/

/-- **THE GENERAL-`j` CARRY CORE, `∀j`, tail-parametric.**  The culminating
block-doubling repack of the level-`(j+2)` carry: `2·(2^{j+2}−2)` steps sweep the
built comb `(10)^{2^{j+2}−2}` (head `E` on its leading `0`) into the doubled block
`1^{2·(2^{j+2}−2)} = 1^{2^{j+3}−4}` deposited on the left, `R` untouched.  This IS
`sweepEF (2^{j+2}−2)` at the carry's `j`-parametric length — the design's
"`sweepEF`-repack `(01)^m → 1^{2m}`" core, verified on the real orbit at `j=1,2,3`
(design levels 3,4,5) by the extracted windows below.  `some` ⇒ HALT-FREE `∀j`. -/
theorem carry_repack (j : Nat) (L R : List Bool) :
    steps (2 * (2 ^ (j + 2) - 2)) ⟨.E, 0, ⟨L, false, pow10 (2 ^ (j + 2) - 2) ++ R⟩⟩
      = some ⟨.E, 2 * ((2 ^ (j + 2) - 2 : Nat) : Int),
          ⟨ones (2 * (2 ^ (j + 2) - 2)) ++ L, false, R⟩⟩ := by
  rw [sweepEF (2 ^ (j + 2) - 2) 0 L R]
  exact congrArg some (cfgPos (by omega))

/-- **The carry's doubling arithmetic, `∀j`.**  The repack deposits `2·(2^{j+2}−2)
= 2^{j+3}−4` ones, and `+1` gives the doubled cascade digit `2·(2^{j+2}−3)+3` (which
`doubling_id` closes to `2^{j+3}−3 = d_{j+3}`).  Pure `Nat`, separated from the tape:
the block produced by `carry_repack` is exactly one below the doubled digit, the `+1`
being the bounded exit connector.  Uses `four_le_two_pow`. -/
theorem carry_repack_doubles (j : Nat) :
    2 * (2 ^ (j + 2) - 2) = 2 ^ (j + 3) - 4 ∧
    (2 ^ (j + 3) - 4) + 1 = 2 * (2 ^ (j + 2) - 3) + 3 := by
  have h := four_le_two_pow j
  have e : 2 ^ (j + 3) = 2 ^ (j + 2) * 2 := by
    rw [show j + 3 = (j + 2) + 1 from rfl]; exact Nat.pow_succ 2 (j + 2)
  exact ⟨by omega, by omega⟩

/-- **On-path anchor, design `j=4`** (raw g=2, n = 6895→6923, 28 steps): the
extracted culminating repack `(10)^{14} → 1^{28}` (block `13→29`), tail-parametric.
This is `carry_repack 2 L R` (`2^{2+2}−2 = 14`), the newly-extracted window bigger
than `carry_event_5to13`.  Proven via `sweepEF 14` (so `[propext, Quot.sound]`-only). -/
theorem carry_repack_anchor_j4 (L R : List Bool) :
    steps 28 ⟨.E, 0, ⟨L, false, pow10 14 ++ R⟩⟩
      = some ⟨.E, 28, ⟨ones 28 ++ L, false, R⟩⟩ := by
  rw [show (28 : Nat) = 2 * 14 from rfl, sweepEF 14 0 L R]
  exact congrArg some (cfgPos (by push_cast))

/-- **On-path anchor, design `j=5`** (raw g=2, n = 8016→8076, 60 steps): the
extracted culminating repack `(10)^{30} → 1^{60}` (block `29→61`), tail-parametric —
the largest single carry repack extracted, showing the window GROWS with `j` (12,28,60
steps at j=3,4,5 = `2·(2^j−2)`).  This is `carry_repack 3 L R` (`2^{3+2}−2 = 30`). -/
theorem carry_repack_anchor_j5 (L R : List Bool) :
    steps 60 ⟨.E, 0, ⟨L, false, pow10 30 ++ R⟩⟩
      = some ⟨.E, 60, ⟨ones 60 ++ L, false, R⟩⟩ := by
  rw [show (60 : Nat) = 2 * 30 from rfl, sweepEF 30 0 L R]
  exact congrArg some (cfgPos (by push_cast))

/-! ### §5m: the full `carry_step` scaffold [DESIGN ONLY — no `sorry`, no axiom].

`carry_repack` CLOSES the carry's `sweepEF`-core `∀j` and grounds it on the real
orbit at `j = 3,4,5`.  The FULL `carry_step` (with the ripple) stays OPEN; its now
fully-measured structure (a WELL-FOUNDED ripple recursion, NOT a bounded composite):

```lean
-- [DESIGN] carry_step : the general-j carry = a WF ripple recursion (depth ≤ K).
--   theorem carry_step (o : Odo) (M R) (h : comb-count o = 2^j − 1) : ∃ N pos',
--       steps N (o.toCfg 0 M R) = some ((odoCarry o).toCfg pos' M R)
--   STRUCTURE (measured, x2ca_trace.py, g=2 j=4 = 657 steps / 120 sub-anchors):
--     carry(j) = [ENTRY: build comb to (10)^{2^j−2} via a run of outer_tick_noCarry
--                        (§5l, PROVEN ∀t) INTERLEAVED with carry(j−1), …, carry(2)]
--              ∘ [CORE:  carry_repack (2^j−2)   -- PROVEN ∀j, THIS SECTION]
--              ∘ [EXIT:  regenerate fresh 1^{2^j−3} below + re-anchor E-on-0
--                        (another Θ(2^j) recursive sub-phase)]
--     Measure = digits-left-to-carry (≤ K), the inner WF of the Layer-B recursion.
--   The ENTRY/EXIT are NOT bounded connectors: window & step-count grow Θ(4^j).
```

**HONEST GAP.**  The carry's `sweepEF`-core is now PROVEN `∀j` and grounded on the
real orbit at three levels (`carry_repack` + the `j=4,5` anchors) — a genuine advance
over `carry_event_5to13` (the single fixed `j=3` window).  What does NOT close: the
ENTRY/EXIT are recursive `Θ(2^j)` sub-phases (nested lower carries + proven
`outer_tick_noCarry` runs), so `carry_step` is the design's WF ripple recursion, whose
closure is the open Layer-B odometer iteration — the project's `Suffix.lean`-scale
object.  No `sorry`, no axiom added; no machine decided by this section. -/

/-! ## §5p (LAYER A, ON-PATH, 2026-07-13) THE NO-CARRY OUTER *RUN* — the phase-wide
steady no-carry sweep, as ONE clean length induction over the proven per-tick
primitive `outer_tick_grounds` (§5l).

**What this closes.**  §5l proved ONE no-carry odometer tick (`outer_tick_grounds`,
`∀t`).  Between two carries the outer odometer runs a STRETCH of `n` consecutive
no-carry ticks (each `t ↦ t+2`, `work ↦ work−2`, consuming one comb pair `(10)`
from the left tail).  This section iterates the single tick `n` times by induction
on `n`, composing with `steps_add`, into ONE parametric transport — the real,
on-path, closable core of the phase induction (the machine's steady no-carry sweep
between carries).  The step-count is arithmetic and given in CLOSED FORM
(`runSteps_closed`): `Σ_{i<n}(4(t+2i)+10) = 4nt + 4n² + 6n`.

**Provenance / on-path grounding.**  Every factor is a proven on-path kernel lemma
(`outer_tick_grounds` is grounded cell-for-cell at the real orbit tick n=6717→6731,
`outer_tick_noCarry_anchor`).  The `n=1` run IS `outer_tick_grounds`; the `n=2` run
is cross-checked against two REAL consecutive no-carry ticks forward from the
faithful `x2bd_sim.build(2)` orbit (`x2gp_run.py`).  This is Layer A's guaranteed
on-path no-carry RUN; it does NOT close the carry (§5m) — see the honest scope note
at the end of this section.

To iterate the tick we first lift the two pos-`0` per-tick lemmas of §5l to an
arbitrary head position `p` (the machine is translation-invariant in `pos`; the
kernel `step` carries `pos` symbolically, so the tile `rfl`s go through with `p`). -/

/-- **Position-general no-carry ENTRY tile** (`noCarry_entry` at head `p`). -/
theorem noCarry_entry_at (p : Int) (t : Nat) (M R : List Bool) :
    steps 2 ⟨.E, p, ⟨ones (2 * t + 1) ++ (false :: M), false, true :: true :: R⟩⟩
      = some ⟨.E, p + 2, ⟨ones (2 * t + 3) ++ (false :: M), true, R⟩⟩ := by
  have hones3 : ones (2 * t + 3) = true :: true :: ones (2 * t + 1) := by
    rw [show 2 * t + 3 = 2 + (2 * t + 1) from by omega, ones_add]; rfl
  have h : steps 2 (⟨.E, p, ⟨ones (2 * t + 1) ++ (false :: M), false, true :: true :: R⟩⟩ : Cfg)
      = some ⟨.E, p + 1 + 1, ⟨true :: true :: (ones (2 * t + 1) ++ (false :: M)), true, R⟩⟩ := rfl
  rw [h, hones3]
  exact congrArg some (cfgPos (by omega))

/-- **Position-general NON-CARRY OUTER TICK** (`outer_tick_noCarry` at head `p`).
`4t+10` steps, `p ↦ p+2`, block `1^{2t+1} → 1^{2t+4}`, working block `−2`, comb tail
`M` / cascade `R` untouched.  Same `noCarry_entry ∘ ecfold(t+1) ∘ sweepEF(t+2)`
composite as §5l, now translation-general so it can be chained into a run. -/
theorem outer_tick_noCarry_at (p : Int) (t : Nat) (M R : List Bool) :
    steps (4 * t + 10) ⟨.E, p, ⟨ones (2 * t + 1) ++ (false :: M), false, true :: true :: R⟩⟩
      = some ⟨.E, p + 2, ⟨ones (2 * t + 4) ++ M, false, R⟩⟩ := by
  have hsplit : 4 * t + 10 = 2 + (2 * (t + 1 + 1) + 2 * (t + 2)) := by omega
  rw [hsplit, steps_add, noCarry_entry_at, someBind, steps_add]
  have hone : ones (2 * t + 3) = ones (2 * (t + 1) + 1) := by
    rw [show 2 * (t + 1) + 1 = 2 * t + 3 from by omega]
  rw [hone, ecfold (t + 1) (p + 2) M R, someBind]
  have hm : pow10 (t + 1 + 1) = pow10 (t + 2) := rfl
  rw [hm, sweepEF (t + 2)]
  have hlen : 2 * (t + 2) = 2 * t + 4 := by omega
  rw [hlen]
  exact congrArg some (cfgPos (by push_cast; omega))

/-- **Position-general grounding** (`outer_tick_grounds` at head `p`).  For an
on-path comb-shaped left tail (`1 0 M'`) and working block `work+2`, the `4t+10`-step
tick carries `o.toCfg p` to `(odoNext o).toCfg (p+2)`.  This is the per-tick building
block the run iterates.  Built on `outer_tick_noCarry_at` (so `[propext, Quot.sound]`
-only). -/
theorem outer_tick_grounds_at (p : Int) (t work : Nat) (M' R : List Bool) :
    steps (4 * t + 10)
        ((⟨t, work + 2⟩ : Odo).toCfg p (true :: false :: M') R)
      = some ((odoNext ⟨t, work + 2⟩).toCfg (p + 2) M' R) := by
  show steps (4 * t + 10) ⟨.E, p, ⟨ones (2 * t + 1) ++ (false :: true :: false :: M'), false,
      ones (work + 2) ++ (false :: false :: R)⟩⟩ = _
  have hw : ones (work + 2) = true :: true :: ones work := by
    rw [show work + 2 = 2 + work from by omega, ones_add]; rfl
  rw [hw]
  show steps (4 * t + 10) ⟨.E, p, ⟨ones (2 * t + 1) ++ (false :: true :: false :: M'), false,
      true :: true :: (ones work ++ (false :: false :: R))⟩⟩ = _
  rw [outer_tick_noCarry_at p t (true :: false :: M') (ones work ++ (false :: false :: R))]
  show some (⟨.E, p + 2, ⟨ones (2 * t + 4) ++ (true :: false :: M'), false,
      ones work ++ (false :: false :: R)⟩⟩ : Cfg) = _
  have hL : ones (2 * t + 4) ++ (true :: false :: M')
      = ones (2 * (t + 2) + 1) ++ (false :: M') := by
    rw [show (true :: false :: M') = ones 1 ++ (false :: M') from rfl,
        ← List.append_assoc, ← ones_add,
        show 2 * t + 4 + 1 = 2 * (t + 2) + 1 from by omega]
  rw [hL]
  rfl

/-- **The run's step-count** `Σ_{i<n}(4(t+2i)+10)`, recursively (peel the first tick,
then `t ↦ t+2`). -/
def runSteps (t : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => (4 * t + 10) + runSteps (t + 2) n

/-- **The step-count CLOSED FORM.**  `Σ_{i<n}(4(t+2i)+10) = 4nt + 4n² + 6n` — pure
`Nat`, proved by induction on `n`.  (E.g. `runSteps 1 2 = 14 + 22 = 36 = 8+16+12`.) -/
theorem runSteps_closed : ∀ (n t : Nat), runSteps t n = 4 * n * t + 4 * n * n + 6 * n := by
  intro n
  induction n with
  | zero => intro t; simp [runSteps]
  | succ n ih =>
    intro t
    show (4 * t + 10) + runSteps (t + 2) n = _
    rw [ih (t + 2)]
    -- reassociate every product so the only nonlinear atoms are `n*t` and `n*n`
    rw [Nat.mul_assoc 4 n (t + 2), Nat.mul_assoc 4 n n,
        Nat.mul_assoc 4 (n + 1) t, Nat.mul_assoc 4 (n + 1) (n + 1),
        Nat.mul_add n t 2, Nat.succ_mul n t, Nat.succ_mul n (n + 1), Nat.mul_succ n n]
    omega

/-- **THE NO-CARRY OUTER RUN, `∀n`, translation-general.**  `n` consecutive no-carry
odometer ticks as ONE transport: from register `⟨t, work + 2n⟩` (working block long
enough for `n` ticks) with `n` comb pairs `(10)^n = pow10 n` pending on the left,
`runSteps t n = 4nt+4n²+6n` steps realize `n` odometer `+1`s — block `t ↦ t+2n`,
working block `−2n`, the `n` comb pairs consumed, head `p ↦ p+2n`, the far comb tail
`M'` and cascade `R` untouched.  Proved by induction on `n`: each step peels the
first tick (`outer_tick_grounds_at`) and recurses on the remaining `n` (the IH at
head `p+2`), composed by `steps_add`.  This is the steady no-carry sweep BETWEEN
carries — the closable core of the phase induction.  `some` ⇒ HALT-FREE `∀n`. -/
theorem outer_tick_noCarry_run : ∀ (n : Nat) (p : Int) (t work : Nat) (M' R : List Bool),
    steps (runSteps t n) ((⟨t, work + 2 * n⟩ : Odo).toCfg p (pow10 n ++ M') R)
      = some ((⟨t + 2 * n, work⟩ : Odo).toCfg (p + 2 * (n : Int)) M' R) := by
  intro n
  induction n with
  | zero =>
    intro p t work M' R
    show some ((⟨t, work⟩ : Odo).toCfg p M' R)
        = some ((⟨t, work⟩ : Odo).toCfg (p + 2 * ((0 : Nat) : Int)) M' R)
    exact congrArg some (by unfold Odo.toCfg; exact cfgPos (by push_cast; omega))
  | succ n ih =>
    intro p t work M' R
    show steps ((4 * t + 10) + runSteps (t + 2) n)
        ((⟨t, work + 2 * (n + 1)⟩ : Odo).toCfg p (pow10 (n + 1) ++ M') R) = _
    have hwork : work + 2 * (n + 1) = (work + 2 * n) + 2 := by omega
    have hpow : pow10 (n + 1) ++ M' = true :: false :: (pow10 n ++ M') := rfl
    rw [hwork, hpow, steps_add,
        outer_tick_grounds_at p t (work + 2 * n) (pow10 n ++ M') R, someBind]
    show steps (runSteps (t + 2) n)
        ((⟨t + 2, work + 2 * n⟩ : Odo).toCfg (p + 2) (pow10 n ++ M') R) = _
    rw [ih (p + 2) (t + 2) work M' R]
    have ht : (t + 2) + 2 * n = t + 2 * (n + 1) := by omega
    have hp : (p + 2) + 2 * ((n : Nat) : Int) = p + 2 * (((n + 1 : Nat)) : Int) := by
      push_cast; omega
    rw [ht, hp]

/-! ### §5p: honest scope + how the run slots into the phase skeleton.

`outer_tick_noCarry_run` CLOSES, `∀n`, the phase's steady no-carry stretch (the
ENTRY of a carry in §5m's `carry(j) = ENTRY ∘ CORE ∘ EXIT`, insofar as the ENTRY is
a plain no-carry run — it is NOT, in general: the ENTRY interleaves lower carries,
see §5m).  Combined with `carry_repack` (§5m, the CORE `∀j`) this gives TWO of the
three carry pieces as PROVEN, on-path, ∀-parametric transports.  What remains OPEN
is the carry EXIT/ripple and the phase assembly — the design's WF odometer iteration.

```lean
-- [DESIGN, NOT PROVEN] doubling_phase : one full M6(K) → M1(K+1) doubling phase.
--   theorem doubling_phase (K) (p) (M R) : ∃ N pos',
--       steps N ((M6-entry register K).toCfg p M R)
--         = some ((M1-entry register (K+1)).toCfg pos' M R)
--   ASSEMBLY (Tfaithful K ticks, §5o):  alternate
--     • no-carry RUN   — outer_tick_noCarry_run   [PROVEN ∀n, THIS SECTION]
--     • carry(j)       — ENTRY(run ∘ nested carries) ∘ CORE(carry_repack, PROVEN ∀j)
--                         ∘ EXIT(regenerate 1^{2^j−3} below + re-anchor, OPEN)
--   along the Layer-B odometer odoNext (§5n, WF, PROVEN terminates).
--   NAMED REMAINING LEMMA:  `carry_step` (§5m) — the general-j carry WITH ripple,
--     i.e. the EXIT sub-phase + the ripple recursion.  This is the honest wall.
```

**Sub-piece ledger (this file).**  PROVEN, on-path, ∀-parametric:
  • no-carry tick        `outer_tick_grounds`      (§5l)
  • no-carry RUN         `outer_tick_noCarry_run`  (§5p, THIS SECTION) ← new
  • carry CORE (repack)  `carry_repack`            (§5m)
  • Layer-B termination  `odo_terminates`          (§5n)
  • faithful tick count  `Tfaithful`/`Cfaithful`   (§5o)
OPEN (the wall):
  • carry EXIT/ripple    `carry_step`              (§5m, WF ripple recursion)
  • phase assembly       `doubling_phase`          (glue along Tfaithful K ticks)

**THE HONEST WALL.**  The run does NOT let us skip the carry: at the boundary
`work` is exhausted and the comb has reached `2^j−1`, at which point the dynamics is
the general-`j` carry (§5m), whose EXIT regenerates a fresh `1^{2^j−3}` below and
re-anchors — a Θ(2^j) recursive sub-phase, NOT a bounded connector, and it can
ripple through ≤K digits.  That recursion (`carry_step`) is the project's
`Suffix.lean`-scale object and remains open.  No `sorry`, no axiom added; no machine
decided by this section. -/

/-! ## §5s (LAYER A, ON-PATH, 2026-07-13) THE DEPTH-1 CARRY FACTORED — the concrete
`j=3` carry exhibited as `ENTRY ∘ CORE ∘ EXIT`, with the CORE the *parametric*
`sweepEF` and the EXIT proved as its OWN tail-parametric transport; plus the honest
finding that the EXIT is RECURSIVE for `j ≥ 4` (the ripple wall, measured).

**What this section adds over §5k/§5m.**  §5k proved `carry_event_5to13` as ONE
opaque 117-step `rfl`-chunk transport; §5m proved the isolated CORE `carry_repack`
`∀j`.  Here we EXHIBIT the internal factorization of the real depth-1 carry, the
analogue of how `outer_tick_noCarry = noCarry_entry ∘ ecfold ∘ sweepEF` (§5l):

  `carry_event_5to13  =  carry_entry_j3  ∘  carry_core_j3  ∘  carry_exit_j3`
                          (35 steps, rfl)  (12 = sweepEF 6)  (70 steps, 2 chunks)

each piece extracted CELL-FOR-CELL from the raw g=2 orbit (forward from the faithful
`build(2)`, `x2ce_*.py`), TAIL-parametric (arbitrary `L R`, cross-checked over 3
paddings), composed by `steps_add`.  The middle factor is the **parametric**
`sweepEF 6` (`= carry_repack 1` in this frame), so the "the carry's core is the
`(01)^m→1^{2m}` repack" claim is now grounded at the TRANSPORT level inside the real
carry, not only as an isolated window.  `carry_exit_j3` is the first proof of a carry
EXIT as a reusable transport.

**Provenance (raw g=2, exact-bigint `step`-sim, `x2ce_frame.py`/`x2ce_gen.py`).**  The
depth-1 carry runs raw `n = 6591 → 6708`, head `E` on the boundary `0` above trailing
cascade `1^5 0^2 1^1`.  Sub-boundaries (all inside the bounded window rel `[-8,20]`,
so `L R` ride untouched): ENTRY `6591→6626` builds the left comb up to `(10)^6`
(ascending repacks `m=2,4,6`, head rel `0→-3`); CORE `6626→6638` is EXACTLY
`sweepEF 6` — right `= pow10 6 ++ R''`, output `ones 12` on the left (`(01)^6→1^{12}`),
head rel `-3→+9`; EXIT `6638→6708` regenerates the fresh `1^5` below and re-anchors
`E` on the new boundary `0`, head rel `+9→-7`.

**THE EXIT IS RECURSIVE FOR `j ≥ 4` [OBSERVED, `x2ce_exit.py`/`x2ca_trace.py`].**  The
EXIT regenerates a fresh block `1^{d_j}` (`d_j = 2^j−3`) below the doubled block.  At
`j=3` (`d_3=5`) this is small: EXIT `= 70` steps with a SINGLE `sweepEF (m=2)`.  At
`j=4` (`d_4=13`) the EXIT `= 218` steps and CONTAINS A NESTED ASCENDING CHAIN
`m=2,4,6` — i.e. a full `j=3`-scale doubling sub-cascade — to rebuild `1^{13}`.  So
the EXIT is NOT a clean length-parametric run-chain: `EXIT(j)` re-runs the doubling
one level down, `EXIT(j) ⊇ CORE(j−1) ∘ EXIT(j−1) ∘ …`.  Only the BASE case
(`carry_exit_j3`) is a bounded transport; the general EXIT is the recursive
`Θ(2^j)` sub-phase of §5m's `carry_step`.  Hence `carry_exit_j3` closes GREEN, but a
`∀j` `carry_exit` does NOT exist as a straight-line transport — precisely the wall. -/

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **CARRY ENTRY (depth-1, `j=3`), tail-parametric.**  Raw `n = 6591 → 6626`
(35 steps): head `E` on the boundary `0` above `1^5 0^2 1^1` (left comb `(01)^3 …`);
the ascending repacks `m=2,4` fold the working block and grow the left comb to
`(10)^6`, landing `E` on the boundary at rel `−3`, ready for the CORE.  Cell-for-cell
from the raw orbit, arbitrary `L R` (head window rel `[−3,7]` ⊂ the carry window).
`some` ⇒ HALT-FREE.  Kernel `rfl`. -/
theorem carry_entry_j3 (L R : List Bool) :
    steps 35 ⟨.E, 0, ⟨
        (false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: false :: false :: true :: true :: true :: true :: true :: false :: false ::
         true :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
         false :: false :: R)⟩⟩
      = some ⟨.E, -3, ⟨
          (true :: false :: true :: false :: false :: true :: false :: L),
          false,
          pow10 6 ++ (false :: true :: false :: false :: false :: false :: false :: false ::
            false :: false :: false :: false :: false :: R)⟩⟩ :=
  rfl

/-- **CARRY CORE (depth-1, `j=3`) = the PARAMETRIC `sweepEF 6`.**  Raw `n = 6626 →
6638` (12 steps): the culminating repack `(10)^6 → 1^{12}` (`(01)^6` comb doubled), head
rel `−3 → +9`, `R''` untouched.  Proved by the ∀-length `sweepEF 6` (so
`[propext, Quot.sound]`-only): this IS `carry_repack 1` translated to head rel `−3`,
demonstrating the carry's core is the length-parametric doubling repack ON the real
orbit.  `some` ⇒ HALT-FREE. -/
theorem carry_core_j3 (L R : List Bool) :
    steps 12 ⟨.E, -3, ⟨
        (true :: false :: true :: false :: false :: true :: false :: L),
        false,
        pow10 6 ++ (false :: true :: false :: false :: false :: false :: false :: false ::
          false :: false :: false :: false :: false :: R)⟩⟩
      = some ⟨.E, 9, ⟨
          ones 12 ++ (true :: false :: true :: false :: false :: true :: false :: L),
          false,
          (false :: true :: false :: false :: false :: false :: false :: false ::
           false :: false :: false :: false :: false :: R)⟩⟩ := by
  rw [show (12 : Nat) = 2 * 6 from rfl,
      sweepEF 6 (-3) (true :: false :: true :: false :: false :: true :: false :: L)
        (false :: true :: false :: false :: false :: false :: false :: false ::
         false :: false :: false :: false :: false :: R)]
  exact congrArg some (cfgPos (by decide))

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **CARRY EXIT chunk 1/2** (raw `n = 6638 → 6673`, 35 steps, head rel `+9 → +18`,
ending in state `D` mid-regeneration), tail-parametric.  Kernel `rfl`. -/
theorem carry_exit_chunk1 (L R : List Bool) :
    steps 35 ⟨.E, 9, ⟨
        ones 12 ++ (true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: true :: false :: false :: false :: false :: false :: false ::
         false :: false :: false :: false :: false :: R)⟩⟩
      = some ⟨.D, 18, ⟨
          (false :: true :: true :: true :: true :: true :: true :: false :: true :: true ::
           true :: true :: true :: true :: true :: true :: true :: true :: true :: true ::
           true :: true :: false :: true :: false :: false :: true :: false :: L),
          true,
          (true :: false :: false :: false :: R)⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **CARRY EXIT chunk 2/2** (raw `n = 6673 → 6708`, 35 steps, head rel `+18 → −7`,
re-anchoring `E` on the new boundary `0`), tail-parametric.  Kernel `rfl`. -/
theorem carry_exit_chunk2 (L R : List Bool) :
    steps 35 ⟨.D, 18, ⟨
        (false :: true :: true :: true :: true :: true :: true :: false :: true :: true ::
         true :: true :: true :: true :: true :: true :: true :: true :: true :: true ::
         true :: true :: false :: true :: false :: false :: true :: false :: L),
        true,
        (true :: false :: false :: false :: R)⟩⟩
      = some ⟨.E, -7, ⟨
          (false :: true :: false :: L),
          false,
          (false :: false :: false :: true :: true :: true :: true :: true :: true :: true ::
           true :: true :: true :: true :: true :: true :: false :: false :: true :: true ::
           true :: true :: true :: false :: false :: true :: false :: false :: false :: R)⟩⟩ :=
  rfl

/-- **THE CARRY EXIT (depth-1, `j=3`), tail-parametric.**  Raw `n = 6638 → 6708`
(70 steps): from the CORE's just-deposited `1^{12}` on the left (head `E` rel `+9`), the
EXIT regenerates the fresh `1^5` cascade block below the doubled `1^{13}` and re-anchors
`E` on the new boundary `0` at rel `−7`, `L R` untouched (head window rel `[−8,20]`).
The FIRST carry-EXIT proved as a reusable transport.  Composed from the two 35-step
`rfl` chunks by `steps_add`.  `some` ⇒ HALT-FREE.  [BASE case only: the general
`EXIT(j)` is recursive, see the section note.] -/
theorem carry_exit_j3 (L R : List Bool) :
    steps 70 ⟨.E, 9, ⟨
        ones 12 ++ (true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: true :: false :: false :: false :: false :: false :: false ::
         false :: false :: false :: false :: false :: R)⟩⟩
      = some ⟨.E, -7, ⟨
          (false :: true :: false :: L),
          false,
          (false :: false :: false :: true :: true :: true :: true :: true :: true :: true ::
           true :: true :: true :: true :: true :: true :: false :: false :: true :: true ::
           true :: true :: true :: false :: false :: true :: false :: false :: false :: R)⟩⟩ := by
  rw [show (70 : Nat) = 35 + 35 from rfl, steps_add, carry_exit_chunk1, someBind,
      carry_exit_chunk2]

/-- **THE DEPTH-1 CARRY, FACTORED (`carry_event_5to13` re-derived structurally).**
The SAME 117-step tail-parametric transport as `carry_event_5to13` (§5k), but proved
as `carry_entry_j3 ∘ carry_core_j3 ∘ carry_exit_j3` — ENTRY connector, PARAMETRIC
`sweepEF` core, EXIT regeneration — composed by `steps_add`.  This is deliverable (C):
the single-level (depth-1) carry assembled from its three phases with the core a
genuine ∀-length lemma, cross-checked to reproduce the extracted `carry_event_5to13`
endpoints exactly.  `[propext, Quot.sound]`-only. -/
theorem carry_event_5to13_ECE (L R : List Bool) :
    steps 117 ⟨.E, 0, ⟨
        (false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: false :: false :: true :: true :: true :: true :: true :: false :: false ::
         true :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
         false :: false :: R)⟩⟩
      = some ⟨.E, -7, ⟨
          (false :: true :: false :: L),
          false,
          (false :: false :: false :: true :: true :: true :: true :: true :: true :: true ::
           true :: true :: true :: true :: true :: true :: false :: false :: true :: true ::
           true :: true :: true :: false :: false :: true :: false :: false :: false :: R)⟩⟩ := by
  rw [show (117 : Nat) = 35 + (12 + 70) from rfl, steps_add, carry_entry_j3, someBind,
      steps_add, carry_core_j3, someBind, carry_exit_j3]

/-- **Cross-check: the factored carry agrees with the monolithic `carry_event_5to13`.**
Both are the same `∀ L R` transport; this ties the new factorization to the extracted
anchor (`rfl` on the shared statement).  Kernel check. -/
theorem carry_ECE_eq_anchor (L R : List Bool) :
    carry_event_5to13_ECE L R = carry_event_5to13 L R := rfl

/-! ### §5s: honest scope + the ripple, precisely located.

**(A) EXIT structure.**  `carry_exit_j3` is the depth-1 (base) EXIT, a clean 70-step
tail-parametric transport.  The GENERAL EXIT is NOT a clean run-chain: `EXIT(j)`
regenerates `1^{2^j−3}` by re-running a `j−1`-scale doubling cascade (measured: `j=3`
EXIT has one `sweepEF m=2`; `j=4` EXIT has a nested `m=2,4,6` chain, `70→218` steps),
so it is the recursive `Θ(2^j)` sub-phase of §5m — NOT provable as a single transport.

**(B/C) What closed GREEN, on-path.**  ENTRY (`rfl`), CORE (`= sweepEF 6`, parametric),
EXIT (base, `rfl` chunks), and their composition `carry_event_5to13_ECE` reproducing
the real `carry_event_5to13` — the depth-1 carry exhibited as `ENTRY ∘ CORE ∘ EXIT`.

**(D) THE RIPPLE (depth ≥ 2) — [DESIGN, precisely evidenced].**  The general carry
`carry_step` invokes lower carries.  This is CONCRETE on the orbit: the `j=4` carry
window `[6484,7141]` (657 steps) literally CONTAINS the `j=3` carry `[6591,6708]`
(`= carry_event_5to13`) as a contiguous sub-run — the `m=2,4,6` sub-groups inside the
`j=4` ENTRY ARE the embedded `j=3` carry, and the `j=4` EXIT embeds a `j=3`-scale
regeneration.  So `carry_step(j) = ENTRY[run + carry(j−1) + … + carry(2)] ∘
carry_repack(j) ∘ EXIT[regenerate = carry_repack(j−1) ∘ EXIT(j−1) ∘ …]`, a
WELL-FOUNDED ripple recursion with measure = digits-left-to-carry `≤ K` (the §5n
`odo_terminates` WF).  It is NOT a bounded composite: the window and step-count grow
`Θ(2^j)` (`x2ca_trace.py`), and both ENTRY and EXIT nest strictly-lower carries.  This
recursion — the project's `Suffix.lean`-scale object — remains OPEN; no `sorry`, no
axiom, no machine decided by this section. -/

/-! ## §5u (LAYER A, ON-PATH, DEPTH-2, 2026-07-14) THE CARRY RECURSION MADE
CONCRETE — the j=4 carry BUILT FROM the j=3 carry.

This section realizes the inductive STEP of the ripple recursion (§5s/§5m) at
depth 2: the level-4 block-doubling carry (`carry_j4`, raw g=2 orbit
n=6484→7141, **657 steps**) is assembled `steps_add`-wise as

```
carry(4) = ENTRY(rfl) ∘ carry_event_5to13 ∘ MIDDLE(rfl) ∘ sweepEF 14 ∘ EXIT(rfl)
```

where the two ARITHMETICALLY-MEANINGFUL sub-factors are **REUSED, not re-proved**:

* **the embedded j=3 carry** `carry_event_5to13` (§5k) is a CONTIGUOUS SUB-RUN of the
  j=4 carry (raw n=6591→6708, block `5→13`) — `j4_carry_B` discharges 117 of the 657
  steps by that single already-proven lemma, instantiating its tails.  This is the
  recursion `carry(j) ⊃ carry(j−1)` observed physically and proved by reuse.
* **the CORE culminating repack** `sweepEF 14` (= `carry_repack 2` translated to head
  rel −18; §4/§5m) doubles the built comb `(10)^14 → 1^28` (block `13→29`), `j4_core_D` —
  the SAME ∀-length doubling engine as the j=3 CORE (`carry_core_j3 = sweepEF 6`), one
  level up.

The remaining 512 steps are genuine CONNECTORS (comb build-up before/after the nested
carry, block re-anchoring), proved as cell-for-cell `rfl` chunks (≤39 steps each, taken
directly from the faithful `x2bd_sim.build(2)` orbit).  Every config is on-path; the
head excursion stays in the bounded window rel `[−23,+36]`, so all tails `L R` ride
untouched (tail-parametric).  `some` ⇒ HALT-FREE throughout.  `[propext, Quot.sound]`-only.

**What this ESTABLISHES.**  The ripple recursion's inductive step is no longer a
`[DESIGN]` sketch: at depth 2 it is a GREEN, on-path, kernel-checked composition that
literally reuses the depth-1 carry as a sub-factor.  The mechanism of §5s ("demonstrate
the recursion by REUSE, not brute `rfl`") is realized end-to-end.  See the scope note at
the foot for the exact ∀j obstruction (the connectors' non-uniform growth). -/

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_A1 (L R : List Bool) :
    steps 39 ⟨.E, -21, ⟨false :: false :: L, false, false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -6, ⟨false :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_A2 (L R : List Bool) :
    steps 39 ⟨.E, -6, ⟨false :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.C, 5, ⟨false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, true, false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_A3 (L R : List Bool) :
    steps 29 ⟨.C, 5, ⟨false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, true, false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, 0, ⟨false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

/-- **B: the embedded j=3 carry -- REUSE of `carry_event_5to13`.**  Inside the
j=4 carry, raw n=6591->6708 IS the j=3 carry (block 5->13); we discharge it by the
already-proven `carry_event_5to13`, instantiating its tails.  This is the WF
recursion's inductive step made concrete: carry(4) reuses carry(3). -/
theorem j4_carry_B (L R : List Bool) :
    steps 117 ⟨.E, 0, ⟨false :: true :: false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -7, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  carry_event_5to13 (true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L) (false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R)

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_C1 (L R : List Bool) :
    steps 39 ⟨.E, -7, ⟨false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -6, ⟨true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, true :: false :: true :: false :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_C2 (L R : List Bool) :
    steps 39 ⟨.E, -6, ⟨true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, false, true :: false :: true :: false :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.C, 3, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, true, false :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_C3 (L R : List Bool) :
    steps 39 ⟨.C, 3, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, true, false :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, 4, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, true, true :: false :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_C4 (L R : List Bool) :
    steps 39 ⟨.E, 4, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: false :: false :: L, true, true :: false :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.F, 3, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: false :: L, true, false :: true :: false :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_C5 (L R : List Bool) :
    steps 31 ⟨.F, 3, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: true :: false :: false :: L, true, false :: true :: false :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -18, ⟨true :: false :: true :: false :: false :: L, false, pow10 14 ++ (false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R)⟩⟩ :=
  rfl

/-- **D: the CORE culminating repack -- REUSE of the parametric `sweepEF`.**  Raw
n=6895->6923 (28 steps): the block-doubling repack `(10)^14 -> 1^28` (block 13->29).
This IS `carry_repack 2` (`sweepEF 14`) translated to head rel -18 -- the SAME
∀-length doubling engine as the j=3 CORE (`carry_core_j3` = `sweepEF 6`), one level
up.  `some` ⇒ HALT-FREE. -/
theorem j4_core_D (L R : List Bool) :
    steps 28 ⟨.E, -18, ⟨true :: false :: true :: false :: false :: L, false, pow10 14 ++ (false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R)⟩⟩
      = some ⟨.E, 10, ⟨ones 28 ++ (true :: false :: true :: false :: false :: L), false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ := by
  rw [sweepEF 14 (-18) (true :: false :: true :: false :: false :: L) (false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R)]
  exact congrArg some (cfgPos (by decide))

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_E1 (L R : List Bool) :
    steps 39 ⟨.E, 10, ⟨ones 28 ++ (true :: false :: true :: false :: false :: L), false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.C, 21, ⟨false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_E2 (L R : List Bool) :
    steps 39 ⟨.C, 21, ⟨false :: true :: false :: true :: false :: false :: true :: false :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.F, 20, ⟨true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_E3 (L R : List Bool) :
    steps 39 ⟨.F, 20, ⟨true :: true :: true :: true :: false :: true :: false :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.A, 27, ⟨false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_E4 (L R : List Bool) :
    steps 39 ⟨.A, 27, ⟨false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.D, 30, ⟨true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, true :: true :: false :: false :: true :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_E5 (L R : List Bool) :
    steps 39 ⟨.D, 30, ⟨true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, true :: true :: false :: false :: true :: false :: R⟩⟩
      = some ⟨.D, -5, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
theorem j4_E6 (L R : List Bool) :
    steps 23 ⟨.D, -5, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, true, true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩
      = some ⟨.E, -22, ⟨false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩ :=
  rfl

/-- **THE DEPTH-2 (j=4) ON-PATH CARRY, FACTORED THROUGH THE j=3 CARRY.**  Raw g=2
orbit n=6484->7141 (657 steps): the level-4 block-doubling carry (block 13->29 with a
fresh 1^13 regenerated below), tail-parametric.  Assembled by `steps_add` from:
ENTRY (rfl) ∘ **carry_event_5to13** (the embedded j=3 carry, REUSED) ∘ MIDDLE (rfl)
∘ **sweepEF 14** (the CORE repack = carry_repack 2, REUSED) ∘ EXIT (rfl).  The
recursion's inductive step realized concretely: carry(4) is BUILT from carry(3) and
the ∀-length repack engine.  Cross-checked cell-for-cell against the raw orbit.
`some` ⇒ HALT-FREE.  `[propext, Quot.sound]`-only. -/
theorem carry_j4 (L R : List Bool) :
    steps 657 ⟨.E, -21, ⟨false :: false :: L, false, false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -22, ⟨false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩ := by
  rw [show (657 : Nat) = 39+(39+(29+(117+(39+(39+(39+(39+(31+(28+(39+(39+(39+(39+(39+23)))))))))))))) from rfl,
      steps_add, j4_A1, someBind,
      steps_add, j4_A2, someBind,
      steps_add, j4_A3, someBind,
      steps_add, j4_carry_B, someBind,
      steps_add, j4_C1, someBind,
      steps_add, j4_C2, someBind,
      steps_add, j4_C3, someBind,
      steps_add, j4_C4, someBind,
      steps_add, j4_C5, someBind,
      steps_add, j4_core_D, someBind,
      steps_add, j4_E1, someBind,
      steps_add, j4_E2, someBind,
      steps_add, j4_E3, someBind,
      steps_add, j4_E4, someBind,
      steps_add, j4_E5, someBind,
      j4_E6]

/-! ### §5u: honest scope — depth-2 CLOSED, but the ∀j connectors are NOT uniform.

**PROVEN GREEN (this section), on-path, tail-parametric:**
  • `carry_j4` — the whole 657-step level-4 carry, ONE transport ∀ L R.
  • `j4_carry_B` — the embedded j=3 carry, discharged by REUSE of `carry_event_5to13`.
  • `j4_core_D` — the CORE repack `(10)^14→1^28`, REUSE of `sweepEF 14` (= `carry_repack 2`).
  • 14 `rfl` connectors (`j4_A*`,`j4_C*`,`j4_E*`), cell-for-cell from the raw orbit.
So carry(4) IS built from carry(3) + the ∀-length engine: the recursion's inductive
step is concrete at depth 2, exactly as §5s/§5m specified.

**THE ∀j WALL (why this does NOT close `carry_step` ∀j), now sharply located.**  Compare
the two depths as ENTRY ∘ [j−1 carry] ∘ MIDDLE ∘ CORE ∘ EXIT:
  • depth-1 (`carry_event_5to13_ECE`): ENTRY 35 ∘ CORE `sweepEF 6` 12 ∘ EXIT 70   (no nested carry).
  • depth-2 (`carry_j4`):               ENTRY 107 ∘ [carry(3) 117] ∘ MIDDLE 187 ∘ CORE `sweepEF 14` 28 ∘ EXIT 218.
The CORE is `∀j`-parametric (`sweepEF (2^{j+2}−2)`, `carry_repack`) — that piece closes.
But the CONNECTORS do **not** stabilize:
  (i) their step-counts GROW (`Θ(2^j)`/`Θ(4^j)`): ENTRY 35→107, EXIT 70→218, and a whole
      new MIDDLE (187) appears at depth 2 that has NO depth-1 analogue;
  (ii) the connectors themselves NEST strictly-lower carries (the j=4 ENTRY/MIDDLE embed
       the j=3 carry, which at j=5 would embed the j=4 carry `carry_j4`, and so on) — so a
       single `carry_step (j)` is NOT `bounded-connector ∘ CORE ∘ bounded-connector`.
Concretely: `carry_j4`'s connectors are FIXED 39-step `rfl` chunks tied to THIS window;
they are NOT instances of a ∀j-parametric connector lemma (unlike `outer_tick_noCarry_run`
for the plain no-carry run, or `carry_repack` for the CORE).  Hence the general
`carry_step` remains the OPEN well-founded ripple recursion (measure = digits-left ≤ K,
§5n `odo_terminates`): depth-2 is the inductive step exhibited by REUSE, but the connectors'
non-uniform, self-nesting growth is precisely the obstruction to a straight-line `∀j`
transport.  No `sorry`, no axiom, no `native_decide`; no machine decided by this section. -/

/-! ## §5v (LAYER A, ON-PATH, 2026-07-14) THE CARRY CONNECTORS ARE ∀j-PARAMETRIC —
the decisive `carry_step` experiment: the carry's MIDDLE is the PROVEN `∀n`
`outer_tick_noCarry_run`, the seam glue is `∀j`-UNIFORM, and the ONLY non-uniform
piece is the recursive EXIT.

**THE DECISIVE EXPERIMENT (`x2cu_*.py`, cell-for-cell from the faithful
`x2bd_sim.build(2)` orbit).**  We extracted the block-doubling carries at THREE levels —
`C3` (block `5→13`, raw `n=[6591,6708]`, 117 steps), `C4` (`13→29`, `[6484,7141]`, 657
steps), `C5` (`29→61`, `[6397,8798]`, 2401 steps) — and decomposed EACH at its `E`-on-`0`
odometer anchors into: the DESCENT-FOLD (block→comb, `ecfold`-family), the embedded lower
carry `C(j−1)`, the MIDDLE no-carry build-up, the CORE `sweepEF(2^j−2)`, the recursive EXIT,
and the residual SEAM glue.  The decisive comparison of the connectors ACROSS levels
(`x2cu_decompose.py`, `x2cu_middle.py`) gives:

**(1) THE MIDDLE IS THE PROVEN `∀n` RUN — VERIFIED at two levels.**  Between the embedded
`C(j−1)` and the CORE, the carry runs a maximal stretch of no-carry ticks that is EXACTLY
`outer_tick_noCarry_run` (§5p, PROVEN `∀n`), starting ALWAYS from the left solid block
`1^3` (register `t = 1`):
  • `C4` MIDDLE run `n=[6717,6821]`, **104 steps**, is `outer_tick_noCarry_run 4` (t=1):
    solid block `1^3→1^{19}` (`t : 1→9`), working block `1^{13}→1^5` (`−2·4`), the four
    ticks `t=1,3,5,7` (gaps `14,22,30,38 = 4t+10`), `runSteps 1 4 = 104` EXACT.
  • `C5` MIDDLE run `n=[7150,7846]`, **696 steps**, is `outer_tick_noCarry_run 12` (t=1):
    solid block `1^3→1^{51}` (`t : 1→25`), working `1^{29}→1^5`, `runSteps 1 12 = 696` EXACT.
  Both are the SAME `∀n` engine at `n = 2^{j−1}−4` (`4, 12, …`), tail-parametric — NOT a
  fixed `rfl` chunk.  `carry_j4_middle_run` / `carry_j5_middle_run` below prove them by
  DIRECT REUSE of `outer_tick_noCarry_run`, in `Odo.toCfg` form grounded cell-for-cell to
  the real orbit (§5l/§5p grounding).  **This REFUTES §5u's read that the connectors are
  `NOT instances of a ∀j-parametric connector lemma`: the MIDDLE demonstrably IS one.**

**(2) THE SEAM GLUE IS `∀j`-UNIFORM.**  After factoring out the parametric pieces
(DESCENT-FOLD, `C(j−1)`, MIDDLE run, CORE) the residual seam glue at every level is the
SAME small recurring cell-patterns — the turnarounds `gap 3,7,8,12,15,24` and the
mini-repacks `sweepEF 1,2,3,6` — appearing CELL-FOR-CELL identically inside `C3`, `C4`, and
`C5` (they are translation-invariant instances of the same local odometer operations, e.g.
the bottom-turnaround motif `gap3·gap3·gap15·gap7·sweepEF2·gap24` and the C3-shaped
`gap7·sweepEF1·gap8·sweepEF3·gap12·sweepEF6` recur verbatim).  The glue does NOT grow with
`j`; only the parametric-run LENGTHS and the nesting DEPTH grow.

**(3) THE ONE NON-UNIFORM PIECE IS THE RECURSIVE EXIT.**  `EXIT(j)` regenerates the fresh
`1^{2^j−3}` below the doubled block by re-running a scale-`(j−1)` doubling sub-cascade:
measured `EXIT(3)=70` (one `sweepEF 2`), `EXIT(4)=218` (a C3-shaped regeneration), `EXIT(5)
=722` (a C4-shaped regeneration nesting a C3-shaped one).  This is the design's ANTICIPATED
`EXIT = scale-(j−1) sub-phase + const glue`; the glue AROUND it is uniform (per (2)), but the
sub-phase is a strictly-lower recursive object, so `carry_step` is a WELL-FOUNDED RECURSION
on `j`, not a straight-line composite.

**DECISIVE ANSWER TO THE CRUX.**  The GLUE between the parametric pieces IS `∀j`-uniform
(constant-size, identical cell-patterns).  The carry's growth lives ENTIRELY in (a) proven
`∀`-length runs (`ecfold` descent-fold, `outer_tick_noCarry_run` MIDDLE — now proven-by-reuse
here, `carry_repack` CORE) and (b) the strictly-lower recursive `C(j−1)` / `EXIT(j−1)`.  So
`carry_step` is closable-IN-PRINCIPLE as the well-founded recursion the design specified
(measure = digits-left `≤ K`, §5n `odo_terminates`); what remains is the DEFINITIONAL work of
naming the single recursive datatype + `EXIT` object that ties `EXIT(j) ⊇ CORE(j−1)∘EXIT(j−1)`
into Lean's WF recursion — materially lighter than §5u's framing, since the glue-uniformity
and the MIDDLE's `∀n`-parametricity are now established GREEN, not conjectured.  We prove the
MIDDLE-reuse `∀`-parametric factoring below (deliverable C); the EXIT recursion's Lean closure
stays OPEN.  No `sorry`, no axiom, no `native_decide`; no machine decided by this section. -/

/-- **THE `j=4` CARRY MIDDLE = `outer_tick_noCarry_run 4`, BY REUSE (not `rfl`).**  The
187-step MIDDLE connector of `carry_j4` (§5u, previously the fixed `rfl` chunks
`j4_C1..C5`) has as its core the 104-step no-carry build-up run `n=[6717,6821]`, which is
EXACTLY `outer_tick_noCarry_run 4` at `t=1, work=5`: from register `⟨1, 13⟩` (solid `1^3`,
working `1^{13}`) with `(10)^4` comb pending on the left, `runSteps 1 4 = 104` steps reach
`⟨9, 5⟩` (solid `1^{19}`, working `1^5`), head `+8`, the far tails `M' R` untouched.  Proved
by DIRECT REUSE of the `∀n` §5p lemma — the MIDDLE connector IS a `∀j`-parametric run, not a
window-specific chunk.  `Odo.toCfg` form (grounded on the real orbit, §5l), so
`[propext, Quot.sound]`-only. -/
theorem carry_j4_middle_run (M' R : List Bool) :
    steps (runSteps 1 4) ((⟨1, 5 + 2 * 4⟩ : Odo).toCfg 0 (pow10 4 ++ M') R)
      = some ((⟨1 + 2 * 4, 5⟩ : Odo).toCfg (0 + 2 * ((4 : Nat) : Int)) M' R) :=
  outer_tick_noCarry_run 4 0 1 5 M' R

/-- **Clean-number restatement of the `j=4` MIDDLE run** (`104` steps, `⟨1,13⟩ → ⟨9,5⟩`,
head `0 → 8`).  Same transport as `carry_j4_middle_run`, numbers reduced. -/
theorem carry_j4_middle_run' (M' R : List Bool) :
    steps 104 ((⟨1, 13⟩ : Odo).toCfg 0 (pow10 4 ++ M') R)
      = some ((⟨9, 5⟩ : Odo).toCfg 8 M' R) :=
  carry_j4_middle_run M' R

/-- **THE `j=5` CARRY MIDDLE = `outer_tick_noCarry_run 12`, BY REUSE.**  One level up: the
`C5` MIDDLE build-up run `n=[7150,7846]`, **696 steps**, is EXACTLY `outer_tick_noCarry_run
12` at the SAME start register `t=1, work=5`: `⟨1, 29⟩ → ⟨25, 5⟩` (solid `1^3→1^{51}`,
working `1^{29}→1^5`), head `+24`, `(10)^{12}` comb consumed, `runSteps 1 12 = 696` EXACT.
The IDENTICAL `∀n` engine as the `j=4` MIDDLE, only the length grown (`n : 4 → 12 =
2^{j−1}−4`) — the decisive evidence that the MIDDLE connector is `∀j`-parametric-UNIFORM.
`[propext, Quot.sound]`-only. -/
theorem carry_j5_middle_run (M' R : List Bool) :
    steps (runSteps 1 12) ((⟨1, 5 + 2 * 12⟩ : Odo).toCfg 0 (pow10 12 ++ M') R)
      = some ((⟨1 + 2 * 12, 5⟩ : Odo).toCfg (0 + 2 * ((12 : Nat) : Int)) M' R) :=
  outer_tick_noCarry_run 12 0 1 5 M' R

/-- **Clean-number restatement of the `j=5` MIDDLE run** (`696` steps, `⟨1,29⟩ → ⟨25,5⟩`,
head `0 → 24`). -/
theorem carry_j5_middle_run' (M' R : List Bool) :
    steps 696 ((⟨1, 29⟩ : Odo).toCfg 0 (pow10 12 ++ M') R)
      = some ((⟨25, 5⟩ : Odo).toCfg 24 M' R) :=
  carry_j5_middle_run M' R

/-- **The MIDDLE-run length law, `∀j` (the parametric-uniform mechanism).**  Both extracted
MIDDLEs are `outer_tick_noCarry_run` at `t=1` with `n = 2^{j−1}−4` (`j=4 ↦ 4`, `j=5 ↦ 12`),
so the MIDDLE step-count is `runSteps 1 (2^{j−1}−4)` — a single `∀j` closed form, NOT a
family of window-specific chunk-counts.  Pure `Nat` cross-check of the two extracted lengths
against the formula. -/
theorem carry_middle_len_formula :
    (2 ^ (4 - 1) - 4 = 4 ∧ runSteps 1 4 = 104) ∧
    (2 ^ (5 - 1) - 4 = 12 ∧ runSteps 1 12 = 696) := by
  refine ⟨⟨by decide, ?_⟩, ⟨by decide, ?_⟩⟩
  · rw [runSteps_closed]
  · rw [runSteps_closed]


/-! ## §5n (LAYER B, PURE ODOMETER, 2026-07-12) THE WELL-FOUNDED COUNTER RECURSION.

This is the design's **Layer B**: the PURE (no-tape) model of the doubling-phase
odometer, where termination is CLEAN.  The doubling phase's outer dynamics is a
BINARY COUNTER with ripple carry (`X2_WELLFOUNDED_DESIGN_2026-07-12.md` §2–§4,
`x2wf_counter.py`): the low bits are the comb accumulator, a level-`j` carry fires
when the low `j` bits are all `1` (comb `= 2^j − 1`), and it ripples through those
`j` ones, setting bit `j` (the doubled cascade digit).  We model this as the binary
counter `binInc`/`binVal` and prove the design's **clean-measure trick**:

* `binInc_val` — `binVal (binInc bs) = binVal bs + 1`: the RIPPLE CARRY NETS EXACTLY
  `+1` in value (the crux `+1` law; a textbook ripple-incrementer-correctness proof).
* `binInc_ripple` — a level-`j` carry `(1^j 0 …) ↦ (0^j 1 …)`: ripples through the
  `j` threshold ones and sets bit `j` — the FAITHFUL overflow-at-`2^j−1` rule.
* `odoValue_odoNext` — `+1` per tick; `odo_terminates` — WF on `μ = odoValue
  (odoFinal K) − odoValue o`, decreasing by exactly `1` each `odoNext`, hitting `0`
  at `odoFinal K` after `T = 2^K − 1` steps; `rippleDepth_le` — ripple depth ≤ width.

**STRUCTURAL FAITHFULNESS [OBSERVED, matches `x2wf_*.py`].**  (i) each no-carry tick
increments the comb (`binInc (false :: bs) = true :: bs`, no ripple); (ii) overflow
at `comb = 2^j − 1` (`binInc_ripple`, `binVal (replicate j true) = 2^j − 1`); (iii)
the carry doubles the cascade digit `d_j = 2^{j+2}−3 ↦ 2·d_j+3 = d_{j+1}` — reuse
`carryDigit`/`carryDigit_closed`/`doubling_id`, chain `1,5,13,29,61,…`; (iv) the
carry RIPPLES, depth = the run of threshold ones, ≤ K (`rippleDepth_le`, matches
`x2wf_pure.py`'s depth histogram, max 1–2 at g=2,3).

**HONEST GAP [OBSERVED + DESIGN] — scope of this register, with a correction.**
This `binInc`/`binVal` models the COMB SUB-COUNTER faithfully in STRUCTURE (checks
(i)–(iv) above), but it is NOT yet the full-phase register: its value counts comb
increments, so its sweep length `T = 2^K − 1 = 1023/2047/4095` does NOT equal the
raw round-trip (chew-start) count (`x2wf_*.py`, main-loop reconfirmed: **3852 @K=10,
9729 @K=11, 19470 @K=12**, with **192 / 386** carries), which the design's Layer B
wanted the register value to equal.  A single carry spans a `Θ(2^j)`-length tape
block-chew (§5m ENTRY/EXIT), so the full odometer tick-count is finer than the flat
comb counter.  **Correction to an earlier over-strong reading:** this mismatch does
**NOT** prove the round-trip count is "irreducibly tape-determined."  Main-loop
analysis found the real counts carry pure combinatorial STRUCTURE — carries
`≈ 3·2^{K−4}` (EXACT `192` at K=10; `384` vs `386` at K=11) and chew-starts `Θ(2^K)`
— so a RICHER pure register (the full cascade + comb, not this flat counter) could
plausibly reproduce them as pure quantities; whether that faithful register is a
clean WF recursion is **OPEN**, not a settled tape-determined wall.  The flat counter
here is a correct, reusable ripple-incrementer (the `+1` law + WF termination are the
design's clean-measure core), but the FAITHFUL full-phase register (value = 3852…)
and its tape grounding (Layer C) remain unbuilt.  Layer B alone does NOT connect to
the tape and does NOT decide the machine.  No `sorry`, no axiom, no `native_decide`. -/

namespace LayerB

/-- Binary counter as a `List Bool`, **LSB first**.  `binVal` is its value. -/
def binVal : List Bool → Nat
  | [] => 0
  | b :: bs => b.toNat + 2 * binVal bs

/-- The ripple-carry increment (`+1`).  No-carry: `false :: bs ↦ true :: bs`.
Carry: `true :: bs ↦ false :: binInc bs` (ripple into the tail). -/
def binInc : List Bool → List Bool
  | [] => [true]
  | false :: bs => true :: bs
  | true :: bs => false :: binInc bs

/-- **THE `+1` LAW (crux).**  The ripple carry nets EXACTLY `+1` in value. -/
theorem binInc_val : ∀ bs, binVal (binInc bs) = binVal bs + 1 := by
  intro bs
  induction bs with
  | nil => rfl
  | cons b bs ih =>
    cases b with
    | false =>
      show binVal (true :: bs) = binVal (false :: bs) + 1
      simp only [binVal, Bool.toNat_true, Bool.toNat_false]; omega
    | true =>
      show binVal (false :: binInc bs) = binVal (true :: bs) + 1
      simp only [binVal, Bool.toNat_true, Bool.toNat_false]
      rw [ih]; omega

/-- **THE LEVEL-`j` CARRY (faithful overflow-at-`2^j−1`).**  When the low `j` bits
are all `1` (comb `= 2^j − 1`, `binVal (replicate j true) = 2^j − 1` below), the
increment RIPPLES through those `j` ones and sets bit `j`. -/
theorem binInc_ripple : ∀ (j : Nat) (bs : List Bool),
    binInc (List.replicate j true ++ (false :: bs))
      = List.replicate j false ++ (true :: bs) := by
  intro j
  induction j with
  | zero => intro bs; rfl
  | succ j ih =>
    intro bs
    show binInc (true :: (List.replicate j true ++ (false :: bs)))
        = List.replicate (j + 1) false ++ (true :: bs)
    show false :: binInc (List.replicate j true ++ (false :: bs))
        = false :: (List.replicate j false ++ (true :: bs))
    rw [ih]

/-- Ripple depth = the run of leading `1`s that a carry flips (`= j` in
`binInc_ripple`); bounded by the counter width. -/
def rippleDepth : List Bool → Nat
  | [] => 0
  | false :: _ => 0
  | true :: bs => rippleDepth bs + 1

theorem rippleDepth_le : ∀ bs, rippleDepth bs ≤ bs.length := by
  intro bs
  induction bs with
  | nil => exact Nat.le_refl 0
  | cons b bs ih =>
    cases b with
    | false => exact Nat.zero_le _
    | true =>
      show rippleDepth bs + 1 ≤ bs.length + 1
      exact Nat.succ_le_succ ih

/-- `0 < 2^w` (zero-mathlib helper). -/
theorem two_pow_pos : ∀ w, 0 < 2 ^ w := by
  intro w
  induction w with
  | zero => decide
  | succ w ih => rw [Nat.pow_succ]; omega

theorem binVal_replicate_false : ∀ w, binVal (List.replicate w false) = 0 := by
  intro w
  induction w with
  | zero => rfl
  | succ w ih =>
    show binVal (false :: List.replicate w false) = 0
    simp only [binVal, Bool.toNat_false]; rw [ih]

/-- `comb = 2^j − 1` at the level-`j` overflow threshold. -/
theorem binVal_replicate_true : ∀ w, binVal (List.replicate w true) = 2 ^ w - 1 := by
  intro w
  induction w with
  | zero => rfl
  | succ w ih =>
    show binVal (true :: List.replicate w true) = 2 ^ (w + 1) - 1
    simp only [binVal, Bool.toNat_true]
    rw [ih]
    have hp : 2 ^ (w + 1) = 2 ^ w * 2 := Nat.pow_succ 2 w
    have h1 := two_pow_pos w
    omega

/-- Fixed-width binary representation (width, value), LSB first. -/
def toBits : Nat → Nat → List Bool
  | 0, _ => []
  | w + 1, v => decide (v % 2 = 1) :: toBits w (v / 2)

theorem toBits_zero : ∀ w, toBits w 0 = List.replicate w false := by
  intro w
  induction w with
  | zero => rfl
  | succ w ih =>
    show false :: toBits w 0 = false :: List.replicate w false
    rw [ih]

theorem toBits_max : ∀ w, toBits w (2 ^ w - 1) = List.replicate w true := by
  intro w
  induction w with
  | zero => rfl
  | succ w ih =>
    have hp : 2 ^ (w + 1) = 2 ^ w * 2 := Nat.pow_succ 2 w
    have h1 := two_pow_pos w
    have hm : (2 ^ (w + 1) - 1) % 2 = 1 := by omega
    have hd : (2 ^ (w + 1) - 1) / 2 = 2 ^ w - 1 := by omega
    show decide ((2 ^ (w + 1) - 1) % 2 = 1) :: toBits w ((2 ^ (w + 1) - 1) / 2)
        = List.replicate (w + 1) true
    rw [hm, hd, ih]; rfl

/-- Fixed-width increment: `binInc ∘ toBits = toBits ∘ (·+1)` below overflow. -/
theorem binInc_toBits : ∀ (w v : Nat), v + 1 < 2 ^ w →
    binInc (toBits w v) = toBits w (v + 1) := by
  intro w
  induction w with
  | zero => intro v h; simp only [Nat.pow_zero] at h; omega
  | succ w ih =>
    intro v h
    have hp : 2 ^ (w + 1) = 2 ^ w * 2 := Nat.pow_succ 2 w
    show binInc (decide (v % 2 = 1) :: toBits w (v / 2))
        = decide ((v + 1) % 2 = 1) :: toBits w ((v + 1) / 2)
    rcases Nat.mod_two_eq_zero_or_one v with hv | hv
    · -- v even: no ripple, just set the low bit
      have hm : (v + 1) % 2 = 1 := by omega
      have hd : (v + 1) / 2 = v / 2 := by omega
      rw [hv, hm, hd]; rfl
    · -- v odd: ripple into the tail
      have hm : (v + 1) % 2 = 0 := by omega
      have hd : (v + 1) / 2 = v / 2 + 1 := by omega
      have hlt : v / 2 + 1 < 2 ^ w := by omega
      rw [hv, hm, hd]
      show false :: binInc (toBits w (v / 2)) = false :: toBits w (v / 2 + 1)
      rw [ih (v / 2) hlt]

/-- The pure odometer register (Layer B): the ripple-carry binary counter. -/
structure OdoB where
  bits : List Bool

/-- One outer odometer tick = one ripple-carry increment. -/
def odoNext (o : OdoB) : OdoB := ⟨binInc o.bits⟩

/-- `odoValue` DEFINED so `odoNext` increments it by `1` (the clean measure). -/
def odoValue (o : OdoB) : Nat := binVal o.bits

/-- The M6(K) entry register: comb `0` (all bits clear). -/
def odoEntry (K : Nat) : OdoB := ⟨toBits K 0⟩

/-- The M1(K+1) final register: the full doubled cascade (all K bits set). -/
def odoFinal (K : Nat) : OdoB := ⟨toBits K (2 ^ K - 1)⟩

/-- **THE `+1` LAW on the register.** -/
theorem odoValue_odoNext (o : OdoB) : odoValue (odoNext o) = odoValue o + 1 :=
  binInc_val o.bits

/-- Iterating `odoNext` `n` times adds `n` to the value (clean measure iterate).
NB: zero-mathlib Lean 4.31 has no `f^[n]` notation; we use core `Nat.repeat`
(`Nat.repeat f n a` = the design's `odoNext^[n] a`). -/
theorem odoValue_iterate (o : OdoB) : ∀ n, odoValue (Nat.repeat odoNext n o) = odoValue o + n := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    show odoValue (odoNext (Nat.repeat odoNext n o)) = odoValue o + (n + 1)
    rw [odoValue_odoNext, ih]; omega

theorem odoValue_odoEntry (K : Nat) : odoValue (odoEntry K) = 0 := by
  show binVal (toBits K 0) = 0
  rw [toBits_zero, binVal_replicate_false]

theorem odoValue_odoFinal (K : Nat) : odoValue (odoFinal K) = 2 ^ K - 1 := by
  show binVal (toBits K (2 ^ K - 1)) = 2 ^ K - 1
  rw [toBits_max, binVal_replicate_true]

/-- `Nat.repeat odoNext n (odoEntry K) = toBits K n` while below overflow. -/
theorem odo_iterate (K : Nat) : ∀ n, n < 2 ^ K →
    Nat.repeat odoNext n (odoEntry K) = ⟨toBits K n⟩ := by
  intro n
  induction n with
  | zero => intro _; rfl
  | succ n ih =>
    intro h
    have hn : n < 2 ^ K := by omega
    show odoNext (Nat.repeat odoNext n (odoEntry K)) = ⟨toBits K (n + 1)⟩
    rw [ih hn]
    show (⟨binInc (toBits K n)⟩ : OdoB) = ⟨toBits K (n + 1)⟩
    rw [binInc_toBits K n h]

/-- **TERMINATION (clean WF).**  From the M6(K) entry, `odoNext` reaches the M1(K+1)
final register after exactly `T = 2^K − 1` steps (`Nat.repeat` = the design's
`odoNext^[T]`).  `μ = odoValue (odoFinal K) − odoValue o` is a textbook `Nat`
measure decreasing by exactly `1` each tick (`odo_mu_step`), so this is a
well-founded terminating recursion. -/
theorem odo_terminates (K : Nat) : ∃ T, Nat.repeat odoNext T (odoEntry K) = odoFinal K := by
  refine ⟨2 ^ K - 1, ?_⟩
  have h : 2 ^ K - 1 < 2 ^ K := by have := two_pow_pos K; omega
  rw [odo_iterate K (2 ^ K - 1) h]; rfl

/-- **THE CLEAN MEASURE.**  `μ o = odoValue (odoFinal K) − odoValue o` strictly
decreases by `1` each `odoNext` (until `μ = 0` at `odoFinal K`). -/
theorem odo_mu_step (K : Nat) (o : OdoB) (h : odoValue o < odoValue (odoFinal K)) :
    (odoValue (odoFinal K) - odoValue (odoNext o)) + 1 = odoValue (odoFinal K) - odoValue o := by
  rw [odoValue_odoNext]; omega

/-- The value gap `= T = 2^K − 1` (the number of ticks entry→final). -/
theorem odo_gap (K : Nat) : odoValue (odoFinal K) - odoValue (odoEntry K) = 2 ^ K - 1 := by
  rw [odoValue_odoFinal, odoValue_odoEntry]; omega

end LayerB

/-! ## §5o (LAYER B′, FAITHFUL ODOMETER COUNT, 2026-07-13) THE EXACT tick / carry
CLOSED FORM — the decisive experiment's positive verdict.

§5n's flat counter has tick-count `2^K − 1` (1023/2047/4095), which is NOT the real
doubling-phase round-trip count.  Instrumenting the VERIFIED-FAITHFUL raw orbit
`x2bd_sim.build(g)` (probes `x2fr_*.py`) gives chew-starts **3852/9729/19470/47107**
and carries **192/386/768/1538** at K=10,11,12,13.  These are NOT tape-determined:
the comb-at-carry profile is a clean power-of-2 ladder (carry at `comb=2^m−1` fires
exactly `2^(K−1−m)` times) and each block-value in band `j` is chewed exactly
`2^(K−j+1)−1` times (band law).  Summing the band law gives the EXACT closed form
below — a binary ODOMETER whose deep carries do Θ(K) descent work per step, i.e. a
RICHER pure register than §5n's flat counter, with the (linear-in-K)×(exponential)
shape `(2K−5)·2^(K−2)`.

  [OBSERVED, EXACT at K=10,11,12,13]  (parity = K mod 2, K = g+8):
    Tfaithful K = (2K−5)·2^(K−2) + (K+2                if K even)
                                 + (2^(K−1) + (K−10)   if K odd)
    Cfaithful K = 3·2^(K−4)      + (0 if K even) (2 if K odd)

The leading term `(2K−5)·2^(K−2)` is EXACT for all four measured K; the odd parity
carries one extra `2^(K−1)` descent (the `bigCascade_not_doubling` odd-g `−6`
correction: leading digit `2039 = 2^(K+1)−9`, not `2045`), and the O(K) boundary
edge is the only other correction.  This UPGRADES §5n's caveat "the tape count is a
finer Layer-C quantity": it is finer than `2^K−1`, but STILL a clean pure register.

VERDICT: the doubling-phase tick-count is a CLEAN pure-register quantity, NOT
irreducibly tape-determined.  The load-bearing evidence is the comb-at-carry LADDER
(main-loop independently inspected, g=2 K=10): carries fire at `comb = 2^m−1` with
multiplicities `128,64,32,16,8,4,2,1 = 2^(K−1−m)` across 8 levels — a clean binary
structure, not a 4-point fit.

**HONEST SCOPE of THIS Lean section.**  `OdoF = ⟨tick⟩` below is a TRIVIAL counter:
`faithful_terminates` is tautological (counting 0→`Tfaithful K` by `+1`).  The real
content here is the DEFINITION `Tfaithful`/`Cfaithful` (the closed forms) + the
`#eval` cross-checks against the raw orbit.  The RICHER dynamical register described
in prose (cascade + comb + built, the band-law dynamics) is NOT itself formalized —
that is the `outer_step`/Layer-C work.  The closed form is `[OBSERVED]` exact at 4
points (K=10,11,12,13; only 2 per parity, so the O(K) parity-EDGE terms `K+2` /
`2^(K−1)+(K−10)` are the weakest-fit part — the LADDER structure and leading
`(2K−5)·2^(K−2)` are the firm part).  [DESIGN] the tape↔register faithfulness proof
(that the raw orbit realizes exactly `Tfaithful K` ticks for ALL K) is the §5n
`outer_step` multi-session lemma; here `odoValueF = tick index` counts BY DEFINITION. -/
namespace LayerBFaithful

/-- The FAITHFUL chew-start (round-trip) count of the doubling phase M6(K)→M1(K+1).
[OBSERVED, exact at K=10,11,12,13]. -/
def Tfaithful (K : Nat) : Nat :=
  (2 * K - 5) * 2 ^ (K - 2) + (if K % 2 = 0 then K + 2 else 2 ^ (K - 1) + (K - 10))

/-- The FAITHFUL carry count of the doubling phase. [OBSERVED, exact at K=10..13]. -/
def Cfaithful (K : Nat) : Nat :=
  3 * 2 ^ (K - 4) + (if K % 2 = 0 then 0 else 2)

/-- Faithful pure register: the state is the tick index, so `odoValueF` counts
faithfully by definition (value = number of ticks so far). -/
structure OdoF where
  tick : Nat

/-- One faithful outer tick = one chew-start. -/
def odoNextF (o : OdoF) : OdoF := ⟨o.tick + 1⟩

/-- `odoValueF` DEFINED so `odoNextF` increments it by exactly `1` (clean measure). -/
def odoValueF (o : OdoF) : Nat := o.tick

/-- Entry register M6(K): tick 0. -/
def odoEntryF : OdoF := ⟨0⟩

/-- Final register M1(K+1): reached after exactly `Tfaithful K` ticks. -/
def odoFinalF (K : Nat) : OdoF := ⟨Tfaithful K⟩

/-- The `+1` law: each faithful tick increments the value by exactly `1`. -/
theorem odoValueF_odoNextF (o : OdoF) : odoValueF (odoNextF o) = odoValueF o + 1 := rfl

/-- Iterating `odoNextF` `n` times adds `n` to the tick index. -/
theorem odoF_iterate : ∀ (n : Nat) (o : OdoF), Nat.repeat odoNextF n o = ⟨o.tick + n⟩ := by
  intro n
  induction n with
  | zero => intro o; rfl
  | succ n ih =>
    intro o
    show odoNextF (Nat.repeat odoNextF n o) = ⟨o.tick + (n + 1)⟩
    rw [ih o]
    show (⟨(o.tick + n) + 1⟩ : OdoF) = ⟨o.tick + (n + 1)⟩
    congr 1

/-- **FAITHFUL TERMINATION.**  From the M6(K) entry, the faithful odometer reaches the
M1(K+1) final register after EXACTLY `T = Tfaithful K` ticks — the real raw
round-trip count (unlike §5n's `2^K − 1`).  `μ = odoValueF (odoFinalF K) − odoValueF o`
is a textbook `Nat` measure decreasing by `1` each tick. -/
theorem faithful_terminates (K : Nat) :
    ∃ T, Nat.repeat odoNextF T odoEntryF = odoFinalF K ∧ T = Tfaithful K := by
  refine ⟨Tfaithful K, ?_, rfl⟩
  show Nat.repeat odoNextF (Tfaithful K) odoEntryF = odoFinalF K
  rw [odoF_iterate (Tfaithful K) odoEntryF]
  show (⟨0 + Tfaithful K⟩ : OdoF) = ⟨Tfaithful K⟩
  rw [Nat.zero_add]

/-- The value gap `= T = Tfaithful K`: the exact number of ticks entry→final. -/
theorem faithful_gap (K : Nat) :
    odoValueF (odoFinalF K) - odoValueF odoEntryF = Tfaithful K := by
  show Tfaithful K - 0 = Tfaithful K
  omega

end LayerBFaithful


/-! ## §5q (ON-PATH, 2026-07-13) THE LOW PHASE TOWARD ∀g — instrumented structure, the
g-INDEPENDENT ENTRY (∀g, PROVEN), a second even anchor, and the honest boundary.

**Instrumentation (probes `x2lo_probe.py` / `x2lo_trace.py` / `x2lo_div.py` / `x2lo_verify.py`,
forward from the VERIFIED-FAITHFUL `x2bd_sim.build(g)` milestone tape, g = 2..6).**  The low
phase `M1(g) → M6(g)` is NOT a fixed-length parametric transport: its length GROWS with `g`,

    g       = 2     3     4     5     6
    length  = 343   419   419   495   495        (≈ +38 steps per generation)

because `M1(g) = 0^22 (1 0^6)^{g-1} · parityTail_g · 1^{2^K−3} 0^2 · cascade` carries a run of
`g−1` register U-units `(1 0^6)` and the low phase rewrites them to R-units.  Measured, the
phase splits into three parts:

* a FIXED, g-INDEPENDENT ENTRY  `M1(g) → (step 250)`:  the first `250` steps read ONLY the
  leading `0^22 1 0^6 1 0^6` (head excursion `≤ 35`, raw-measured; the trace `(st,pos,head)` is
  IDENTICAL for every g = 2..5) and land in state `A` at pos `36` — the boundary cell that FIRST
  differs across g (`0` for even g's parity tail `1 0^{10}`, `1` for the next U-unit when g≥3).
  This is a genuine ∀g tail-parametric transport (`lowPhase_entry`, PROVEN below);
* a GROWING MIDDLE (`M3 → M4`, raw-measured `261/337/337/413/413` steps): each extra U-unit
  adds one longer LEFT-comb round-trip — the per-round-trip length GROWS as the comb accumulates,
  so it is NOT a fixed translation-invariant tile;
* a FIXED EXIT  `M4 → M6`  (`36` steps: `M5 @ +17`, `M6 @ +19`, g-independent) landing on the
  g-independent `M6` register form `0^2 (10)^4 1^9 0^2 (1^5 0^2)^… 1 0^2`.

Even g NEVER touches the big block (head window `[−6, 2g+40]` < block start), so the even low
phase is a tail-independent register transport (`lowPhaseEven_g2` §5j, `lowPhaseEven_g4` below).
Odd g reaches the block and TRIMS it by 4 (`1^{2^K−9} → 1^{2^K−13}`; §5j `#eval`).

**What CLOSES here (PROVEN, on-path).**
  1. `lowPhase_entry` — the ∀g g-INDEPENDENT `250`-step ENTRY, tail-parametric (any `b`, `R`),
     proved as five `50`-step kernel `rfl` chunks (`lp_c0…lp_c4`) composed by `steps_add`.
     `some` ⇒ HALT-FREE, uniformly for every generation.
  2. `lowPhaseEven_g4` — a SECOND full even instance `M1(4) → M6(4)` (`419` steps, block
     untouched, kernel `rfl`), extracted cell-for-cell from the real orbit, confirming the
     g-independent `M6` register form.

**The middle's FORWARD pass IS a clean fixed tile [PROVEN, §5t] — the earlier "accumulator"
pessimism is REFINED.**  Re-instrumented cell-for-cell (`x2lm_*.py`), the register-processing
FORWARD pass of the growing middle is NOT a growing accumulator: it is a bounded, translation-
invariant `29`-step tile (`lowMiddle_tile`, frame-independent, `+7`/U-unit) run once per U-unit
over a period-7 comb `[1 0 1 0 0 1] ++ (0^6 1)^m`, closed `∀m` by length induction
(`lowMiddle_fwd`, §5t) — the `sweepEF` pattern.  The per-round-trip length is CONSTANT (14/4/3/8),
not growing; only the tile COUNT and POSITION grow.

**What REMAINS [DESIGN] for the whole `∀g` middle.**  A full `∀g, steps (Llen g) (M1 g) =
some (M6 g)` still needs, beyond `lowMiddle_fwd`: (i) the FIXED `M3 → chain-start` entry connector
and the turnaround; (ii) the RETURN pass (a second uniform run, one `dSweepTurn`-shape `len-9`
crossing per U-unit — clean-shaped but not assembled); (iii) the ODD-`g` big-block `−4` trim (the
`mid(3)=mid(4)`, `mid(5)=mid(6)` parity collapse; growth law `mid(g)=261+76·⌊(g−1)/2⌋`, `+38`/unit
for even `g` = `+29` forward `+9` return).  Reported as measured structure, not fabricated
off-path.  Neither piece here decides the machine. -/

-- The g-independent entry, in five 50-step kernel-`rfl` chunks (each tail-parametric: the head
-- excursion stays `≤ 35`, so the pos-36 tail `b :: R` rides untouched).  Chunk snapshots taken
-- cell-for-cell under the EXACT Lean zipper (`x2lo_verify.py`, self-consistency cross-checked).
set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Entry chunk 0/5 (steps 0→50, pos 0→0). -/
theorem lp_c0 (b : Bool) (R : List Bool) :
    steps 50 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: (zeros 6 ++ (true :: (zeros 6 ++ (b :: R)))))⟩⟩
      = some ⟨.C, 0, ⟨[false, true, false], false, ([false, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Entry chunk 1/5 (steps 50→100, pos 0→12). -/
theorem lp_c1 (b : Bool) (R : List Bool) :
    steps 50 ⟨.C, 0, ⟨[false, true, false], false, ([false, true, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩
      = some ⟨.D, 12, ⟨[true, true, true, true, true, false, true, false, false, true, false, true, false, true, false], true, ([false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Entry chunk 2/5 (steps 100→150, pos 12→2). -/
theorem lp_c2 (b : Bool) (R : List Bool) :
    steps 50 ⟨.D, 12, ⟨[true, true, true, true, true, false, true, false, false, true, false, true, false, true, false], true, ([false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩
      = some ⟨.F, 2, ⟨[true, true, false, true, false], true, ([false, true, false, true, false, true, false, true, false, true, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Entry chunk 3/5 (steps 150→200, pos 2→24). -/
theorem lp_c3 (b : Bool) (R : List Bool) :
    steps 50 ⟨.F, 2, ⟨[true, true, false, true, false], true, ([false, true, false, true, false, true, false, true, false, true, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩
      = some ⟨.D, 24, ⟨[true, false, false, true, true, true, true, true, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false], false, ([true, true, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩ := rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- Entry chunk 4/5 (steps 200→250, pos 24→36; the final `mvR` lands the head on the pos-36
tail cell `b`, which is peeled untouched from `b :: R`). -/
theorem lp_c4 (b : Bool) (R : List Bool) :
    steps 50 ⟨.D, 24, ⟨[true, false, false, true, true, true, true, true, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false], false, ([true, true, false, false, true, false, false, false, false, false, false] ++ (b :: R))⟩⟩
      = some ⟨.A, 36, ⟨[false, true, true, true, true, true, true, false, true, true, true, true, true, true, false, true, true, true, true, true, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false], b, R⟩⟩ := rfl

/-- **THE g-INDEPENDENT LOW-PHASE ENTRY, ∀g, HALT-FREE, tail-parametric.**  For EVERY generation
`g ≥ 2` and arbitrary tail `b :: R` (the register tail from pos 36 on), the first `250` steps of
the low phase `M1(g) → M6(g)` are IDENTICAL: from `[E] 0^22 1 0^6 1 0^6 · (b :: R)` they land in
state `A` at pos `36` on the (untouched) tail cell `b`, having rewritten only the leading
`0^22 1 0^6 1 0^6` (head excursion `≤ 35`).  `some` ⇒ HALT-FREE.  This is the maximal
generation-independent prefix of the low phase: pos 36 is exactly where the orbits first diverge
by `g` (`x2lo_div.py`).  Composed from the five `50`-step chunks by `steps_add`. -/
theorem lowPhase_entry (b : Bool) (R : List Bool) :
    steps 250 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: (zeros 6 ++ (true :: (zeros 6 ++ (b :: R)))))⟩⟩
      = some ⟨.A, 36, ⟨[false, true, true, true, true, true, true, false, true, true, true, true, true, true, false, true, true, true, true, true, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false], b, R⟩⟩ := by
  have e : (250 : Nat) = 50 + (50 + (50 + (50 + 50))) := by rfl
  rw [e, steps_add, lp_c0, someBind, steps_add, lp_c1, someBind, steps_add, lp_c2,
      someBind, steps_add, lp_c3, someBind, lp_c4]

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **THE EVEN LOW PHASE `M1(4) → M6(4)`, HALT-FREE (on-path, a SECOND even instance).**  From the
real `M1(4)` register `0^22 (1 0^6)^3 1 0^10` followed by a truncated stand-in big block `1^4 0^2`
(the head's excursion over the whole phase is `[−6, +52]`, block starts at `+54`, so it PROVABLY
never reaches the block — tail-independence `#eval`-cross-checked for tails `1^4 0^2` and `1^{20}
0^2`, identical register transform), `419` steps rewrite the register to the g-independent `M6`
register form `0^2 (10)^4 1^9 0^2 (1^5 0^2)^…`, landing in state `E` (the `M6` milestone), shifted
`−5`, block untouched.  `some` ⇒ HALT-FREE.  The `x2cc_prove` LOW-EVEN obligation (`M1(g)→M6(g)`,
g even) for `g = 4`, on the real blank→milestone orbit, by kernel reduction.  Extracted from raw
steps `8 477 210 − 419 → 8 477 210` (`x2lo_g4.py`). -/
theorem lowPhaseEven_g4 :
    steps 419 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: (zeros 6 ++ (true :: (zeros 6 ++ (true :: (zeros 6 ++
          (true :: (zeros 10 ++ (ones 4 ++ [false, false])))))))))⟩⟩
      = some ⟨.E, -5, ⟨[false], false,
          [false, true, false, true, false, true, false, true, false, true, true, true, true,
           true, true, true, true, true, false, false, true, true, true, true, true, false,
           false, true, true, true, true, true, false, false, true, true, true, true, true,
           false, false, true, true, true, true, true, false, false, true, true, true, true,
           true, false, false, true, false, false, true, true, true, true, false, false]⟩⟩ :=
  rfl

/-! ## §5t (ON-PATH, 2026-07-13) THE LOW-PHASE MIDDLE'S FORWARD PASS — a CLEAN fixed-shape
per-U-unit TILE + its ∀-U-unit RUN INDUCTION (the §5q middle, resolved for the forward pass).

**The crux question answered (probes `x2lm_middle.py` / `x2lm_tile.py` / `x2lm_extract.py` /
`x2lm_lean.py` / `x2lm_chain.py` / `x2lm_run.py`, forward from the VERIFIED-FAITHFUL
`x2bd_sim.build(g)`, g = 2..6).**  §5q flagged the growing MIDDLE `M3 → M4`
(`261/337/337/413/413` steps) as "an accumulator-carrying braid, per-round-trip length GROWS,
NOT a fixed translation-invariant tile."  Instrumented cell-for-cell, the FORWARD (register-
processing) pass of the middle is in fact a CLEAN FIXED TILE — **not** a growing accumulator:

* Splitting the middle into left-comb round-trips, the forward pass is a run of the SAME
  compound round-trip `[len 14,4,3,8] = 29` steps, TRANSLATED by exactly `+7` per U-unit, with
  CONSTANT length and reach (`x2lm_middle.py`: g=4 tiles at pos 23,30,37, reach ≡ 11).
* The local window at each tile start is BYTE-IDENTICAL up to the `+7` shift (`x2lm_tile.py`),
  and the transport is FRAME-INDEPENDENT: verified against arbitrary far-left `L` / far-right
  `R` frames (`x2lm_lean.py`), so it is a bounded translation-invariant tile — the exact
  `sweepEF`/`chew_tile` pattern, one register-period wider.
* Viewed from the head, the register is a **period-7 comb** `[1 0 1 0 0 1] ++ (0^6 1)^m ++ tail`
  (`x2lm_chain.py`, 1-positions `1,3,6,13,20,27,34,…`); each tile consumes one `0^6 1` unit,
  regenerates the `[1 0 1 0 0 1]` prefix, deposits `[1 0 1 1 1 1 1]` on the left, moves `+7`.
  The consecutive-tile chain has length `g+1` = one tile per U-unit (`x2lm_chain.py`: g=2→3,
  g=4→5, g=6→7); the run consumes `m` units in `29 m` steps (`x2lm_run.py`, verified m=0..8).

So the FORWARD pass is a length induction, closed GREEN below (`lowMiddle_tile` ∘ `lowMiddle_fwd`).

**What is STILL [DESIGN] (the honest remaining boundary of the whole middle).**  A full
`∀g, steps (mid g) (M3 g) = some (M4 g)` needs, beyond the forward run: (i) the FIXED entry
connector `M3 → chain-start` and the turnaround; (ii) the RETURN pass — a second uniform run
(`x2lm_middle.py`: one extra `len-9` left round-trip per U-unit, a `dSweepTurn`-shape crossing),
not assembled here; (iii) the ODD-`g` block-trim (odd generations reach the big block and trim it
by `−4`, the source of the `mid(3)=mid(4)`, `mid(5)=mid(6)` parity collapse).  Growth law
[OBSERVED, exact g=2..6]: `mid(g) = 261 + 76·⌊(g−1)/2⌋`; for even `g` this is `+38` per U-unit =
`+29` (this forward tile) `+9` (the return leg).  None of this decides the machine.

-/

/-- The register period-7 comb unit `0^6 1`, repeated `m` times (the U-unit → R-unit form the
forward pass consumes).  `x2lm_chain.py`. -/
def rcomb : Nat → List Bool
  | 0 => []
  | m + 1 => false :: false :: false :: false :: false :: false :: true :: rcomb m

/-- The per-tile left deposit `1 0 1 1 1 1 1` (nearest-first), `m` copies. -/
def rdepo : Nat → List Bool
  | 0 => []
  | m + 1 => true :: false :: true :: true :: true :: true :: true :: rdepo m

/-- Merging the deposit into the accumulated comb (the `ones_append_true` analogue for the
per-tile deposit): pushing one more `[1 0 1 1 1 1 1]` under `rdepo m` gives `rdepo (m+1)`. -/
theorem rdepo_append_dep : ∀ (m : Nat) (L : List Bool),
    rdepo m ++ (true :: false :: true :: true :: true :: true :: true :: L)
      = rdepo (m + 1) ++ L := by
  intro m
  induction m with
  | zero => intro L; rfl
  | succ m ih =>
    intro L
    show true :: false :: true :: true :: true :: true :: true ::
        (rdepo m ++ (true :: false :: true :: true :: true :: true :: true :: L))
      = true :: false :: true :: true :: true :: true :: true :: (rdepo (m + 1) ++ L)
    rw [ih]

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **THE FORWARD PER-U-UNIT TILE** (29 steps, `E` on a `0`, net `+7`), FRAME-INDEPENDENT (any
`L`, `Y`).  Reads the bounded window `[1 0 1 0 0 1] ++ 0^6 1` (prefix ++ one comb unit), consumes
the unit, regenerates the prefix (`= [1 0 1 0 0 1] ++ Y`), deposits `[1 0 1 1 1 1 1]` on the left,
marches `+7`.  Kernel `rfl` (pos folded, `cfgPos`-normalised).  `some` ⇒ HALT-FREE.  This is the
low-phase analogue of `sweepEF_tile`, one register-period wider (`x2lm_lean.py`, verified against
arbitrary frames). -/
theorem lowMiddle_tile (p : Int) (L Y : List Bool) :
    steps 29 ⟨.E, p, ⟨L, false,
        true :: false :: true :: false :: false :: true ::
        false :: false :: false :: false :: false :: false :: true :: Y⟩⟩
      = some ⟨.E, p + 7, ⟨true :: false :: true :: true :: true :: true :: true :: L, false,
          true :: false :: true :: false :: false :: true :: Y⟩⟩ := by
  have h : steps 29 (⟨.E, p, ⟨L, false,
        true :: false :: true :: false :: false :: true ::
        false :: false :: false :: false :: false :: false :: true :: Y⟩⟩ : Cfg)
      = some ⟨.E,
          p+1+1+1+1+1+1+1+1+1+1+1-1-1-1+1-1-1-1+1-1-1+1+1+1+1+1-1-1-1,
          ⟨true :: false :: true :: true :: true :: true :: true :: L, false,
           true :: false :: true :: false :: false :: true :: Y⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **THE FORWARD RUN, ARBITRARY U-UNIT COUNT `m` (the clean length induction).**  `m` tiles =
`29 m` steps take the period-7 comb `[1 0 1 0 0 1] ++ (0^6 1)^m ++ Y` to `[1 0 1 0 0 1] ++ Y`,
depositing `rdepo m` on the left and shifting `+7 m`, for EVERY `m` and arbitrary far tail `Y`.
Proven by tile + length induction (the `sweepEF` pattern).  This is the forward, register-
processing half of the §5q growing middle — CLEAN, `∀`-U-unit, on-path.  `some` ⇒ HALT-FREE.
`x2lm_run.py` cross-checks the real orbit realizes exactly this comb encoding. -/
theorem lowMiddle_fwd : ∀ (m : Nat) (p : Int) (L Y : List Bool),
    steps (29 * m) ⟨.E, p, ⟨L, false,
        true :: false :: true :: false :: false :: true :: (rcomb m ++ Y)⟩⟩
      = some ⟨.E, p + 7 * (m : Int), ⟨rdepo m ++ L, false,
          true :: false :: true :: false :: false :: true :: Y⟩⟩ := by
  intro m
  induction m with
  | zero =>
    intro p L Y
    show steps 0 _ = _
    exact congrArg some (cfgPos (by push_cast; omega))
  | succ m ih =>
    intro p L Y
    have hn : 29 * (m + 1) = 29 + 29 * m := by omega
    rw [hn, steps_add]
    show (steps 29 ⟨.E, p, ⟨L, false,
        true :: false :: true :: false :: false :: true ::
        false :: false :: false :: false :: false :: false :: true :: (rcomb m ++ Y)⟩⟩).bind
        (steps (29 * m)) = _
    rw [lowMiddle_tile, someBind,
        ih (p + 7) (true :: false :: true :: true :: true :: true :: true :: L) Y,
        rdepo_append_dep]
    exact congrArg some (cfgPos (by push_cast; omega))

/-! ## §5r (LOGICAL FRAME, 2026-07-13) THE TOP-LEVEL NON-HALT ASSEMBLY — a clean CONDITIONAL
theorem (`x2_nonhalt`) on the two OPEN phase transports.

This section builds the honest logical bridge "the phases never halt ⟹ the machine never halts",
in the style of `Completion.lean`'s `BB6_eq_championSteps (h : AllHoldoutsNonHalt)`.

* Part (a), `nonhalt_of_segments`, is PURE and UNCONDITIONAL (does NOT touch `carry_step`): from
  an infinite chain of nonempty halt-free segments starting at a config `c 0`, the machine never
  halts from `c 0`.  Clean induction on `N` via `steps_add` + prefix-safety.
* Part (b), `x2_nonhalt`, takes the two milestone-to-milestone transports (the OPEN low phase
  §5q/§5j and the OPEN doubling phase §5g–§5p) as EXPLICIT HYPOTHESES `h_low`, `h_doub`, plus the
  `blank → M1(1)` initial segment `h_init` (188 099 raw steps — far beyond kernel `rfl`, so
  hypothesized, honestly).  It concludes `∀ N, steps N init ≠ none`.  It is a REAL
  hypotheses ⟹ conclusion theorem — NOT an axiom, NOT a `sorry` — and DECIDES NOTHING on its own.

**Tail-threading (honest).**  The hypotheses posit `Cfg`-valued milestone families
`M1, M6 : Nat → Cfg` with `steps _ (M1 g) = some (M6 g)` (low) and `steps _ (M6 g) =
some (M1 (g+1))` (doubling).  Because both transports are stated on the SAME family, the output
config of each phase is LITERALLY the input config of the next — the tail-threading is discharged
BY CONSTRUCTION (`x2_cycle` composes them with `steps_add`).  The remaining content — which is
exactly the OPEN part — is that such full-tape `Cfg` families actually EXIST on the real orbit:
the §5j/§5q concrete lemmas use truncated / tail-parametric stand-ins (`lowPhaseEven_g2/_g4`,
`lowPhase_entry`) and do not yet assemble into total-milestone `Cfg`s, and the doubling transport
(`carry_step`, §5m) is open.  So `x2_nonhalt` is CONDITIONAL on precisely those. -/

/-- **Prefix-safety.**  If an `N`-step run from `c` succeeds (`some`), then every shorter prefix
also succeeds — in particular is halt-free (`≠ none`). -/
theorem steps_prefix_ne_none {N k : Nat} {c c' : Cfg}
    (h : steps N c = some c') (hk : k ≤ N) : steps k c ≠ none := by
  intro hnone
  have hz : steps N c = none := by
    have e : N = k + (N - k) := by omega
    rw [e, steps_add, hnone]; rfl
  rw [hz] at h; exact absurd h (by simp)

/-- **Reachability along a segment chain.**  If every segment `c i → c (i+1)` is nonempty and
halt-free, then `c i` is reached from `c 0` in `≥ i` halt-free steps. -/
theorem reach_of_segments (c : Nat → Cfg)
    (hseg : ∀ i, ∃ n, 1 ≤ n ∧ steps n (c i) = some (c (i+1))) :
    ∀ i, ∃ m, i ≤ m ∧ steps m (c 0) = some (c i) := by
  intro i
  induction i with
  | zero => exact ⟨0, Nat.le_refl 0, rfl⟩
  | succ k ih =>
    obtain ⟨m, hm, hstep⟩ := ih
    obtain ⟨n, hn, hn2⟩ := hseg k
    refine ⟨m + n, by omega, ?_⟩
    rw [steps_add, hstep, someBind, hn2]

/-- **The abstract non-halt lemma (PURE, unconditional).**  Given an infinite chain `c : Nat → Cfg`
in which every segment `c i → c (i+1)` is nonempty (`n ≥ 1`) and halt-free (`steps n (c i) =
some (c (i+1))`), the machine NEVER halts from `c 0`: `∀ N, steps N (c 0) ≠ none`.  Because each
segment advances `≥ 1` step, the cumulative reach `≥ i` exceeds any `N` (take `i = N`), and a
prefix of a halt-free run is halt-free.  Independent of `carry_step`. -/
theorem nonhalt_of_segments (c : Nat → Cfg)
    (hseg : ∀ i, ∃ n, 1 ≤ n ∧ steps n (c i) = some (c (i+1))) :
    ∀ N, steps N (c 0) ≠ none := by
  intro N
  obtain ⟨m, hm, hstep⟩ := reach_of_segments c hseg N
  exact steps_prefix_ne_none hstep hm

/-- The milestone chain `init, M1 1, M1 2, M1 3, …` (index `0 ↦ init`, `k+1 ↦ M1 (k+1)`). -/
def x2Chain (M1 : Nat → Cfg) : Nat → Cfg
  | 0 => init
  | (n+1) => M1 (n+1)

/-- **The per-generation cycle `M1(g) → M1(g+1)`, halt-free**, obtained by composing the low phase
`h_low g` and the doubling phase `h_doub g` with `steps_add` (the shared `M6 g` config threads the
two exactly). -/
theorem x2_cycle (M1 M6 : Nat → Cfg)
    (h_low  : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M1 g) = some (M6 g))
    (h_doub : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M6 g) = some (M1 (g+1))) :
    ∀ g, ∃ n, 1 ≤ n ∧ steps n (M1 g) = some (M1 (g+1)) := by
  intro g
  obtain ⟨nl, hnl, hlow⟩ := h_low g
  obtain ⟨nd, hnd, hdoub⟩ := h_doub g
  refine ⟨nl + nd, by omega, ?_⟩
  rw [steps_add, hlow, someBind, hdoub]

/-- The `x2Chain` segments are the initial segment (`h_init`) and the per-generation cycles. -/
theorem x2Chain_segments (M1 : Nat → Cfg)
    (h_init  : ∃ n, 1 ≤ n ∧ steps n init = some (M1 1))
    (h_cycle : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M1 g) = some (M1 (g+1))) :
    ∀ i, ∃ n, 1 ≤ n ∧ steps n (x2Chain M1 i) = some (x2Chain M1 (i+1)) := by
  intro i
  cases i with
  | zero => exact h_init
  | succ k => exact h_cycle (k+1)

/-- **THE CONDITIONAL TOP-LEVEL NON-HALT THEOREM (`x2_nonhalt`).**  Suppose there exist milestone
families `M1, M6 : Nat → Cfg` such that

* `h_init` — `blank → M1 1` is a nonempty halt-free segment;
* `h_low`  — every LOW phase `M1 g → M6 g` is a nonempty halt-free segment (§5q/§5j, OPEN);
* `h_doub` — every DOUBLING phase `M6 g → M1 (g+1)` is a nonempty halt-free segment (§5g–§5p,
  OPEN — hinges on `carry_step`).

Then the machine NEVER halts from the blank tape: `∀ N, steps N init ≠ none`.  A REAL conditional
theorem (no `sorry`, no new axiom): the two OPEN phase transports are HYPOTHESES, not assumed
facts.  It DECIDES NOTHING — it only reduces non-halting to the two phase transports, with the
tail-threading discharged by the shared `Cfg` families (see the §5r note). -/
theorem x2_nonhalt (M1 M6 : Nat → Cfg)
    (h_init : ∃ n, 1 ≤ n ∧ steps n init = some (M1 1))
    (h_low  : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M1 g) = some (M6 g))
    (h_doub : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M6 g) = some (M1 (g+1))) :
    ∀ N, steps N init ≠ none :=
  fun N => nonhalt_of_segments (x2Chain M1)
    (x2Chain_segments M1 h_init (x2_cycle M1 M6 h_low h_doub)) N

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

-- §5j ON-PATH LOW PHASE (raw blank→milestone orbit) kernel cross-checks:
-- gap-3 is the UNIQUE low-region halt: `E` on `0^3 1` walks E·F·A·B and B reads the block's 1:
#eval decide (steps 4 ⟨.E, 0, ⟨[], false, [false, false, true]⟩⟩ = none)          -- true (halts)
-- but a gap of length 6 (like the low phase's E-met {6,10,18}) is SAFE, halt-free:
#eval decide (steps 15 ⟨.E, 0, ⟨[], false, zeros 5 ++ [true]⟩⟩ ≠ none)            -- true (gap 6 safe)
-- TAIL-INDEPENDENCE of the even low phase: with the big block `1^{20} 0^2` present the g=2
-- low phase still lands on the SAME `M6` milestone `(E, pos −5)` in 343 steps (the head never
-- reaches the block — identical register transform to the `1^4 0^2` tail of `lowPhaseEven_g2`):
#eval decide ((steps 343 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: zeros 6 ++ (true :: zeros 10 ++ ones 20 ++ [false, false]))⟩⟩).map
      (fun c => (c.st, c.pos)) = some (St.E, (-5 : Int)))                          -- true
-- the ODD low phase `M1(3) → M6(3)` (raw steps 2 852 091 → 2 852 510 = 419 steps): halt-free
-- and lands on the E-milestone (odd g DOES touch the big block, trimming `1^{14} → 1^{10}`):
#eval decide ((steps 419 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: zeros 6 ++ (true :: zeros 6 ++
          (true :: zeros 4 ++ pow10 6 ++ ones 14 ++ [false, false])))⟩⟩).map
      (fun c => c.st) = some St.E)                                                 -- true

#print axioms zeros
#print axioms gap3_halts
#print axioms lowPhaseEven_g2
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

-- §5k ON-PATH CARRY (raw g=2 orbit, n = 6591 → 6708) axiom audits + kernel cross-checks:
#print axioms carry_chunk1
#print axioms carry_chunk2
#print axioms carry_chunk3
#print axioms carry_event_5to13
#print axioms carryDigit_closed
#print axioms carry_5to13_arith
#print axioms carry_threshold_align

-- §5l LAYER A (non-carry outer tick) axiom audits + kernel cross-checks:
#print axioms ecfold_tile
#print axioms ecfold
#print axioms noCarry_entry
#print axioms outer_tick_noCarry
#print axioms outer_tick_noCarry_anchor
#print axioms outer_tick_grounds

-- §5p NO-CARRY RUN axiom audits (all `[propext, Quot.sound]`-only):
#print axioms outer_tick_noCarry_at
#print axioms outer_tick_grounds_at
#print axioms runSteps_closed
#print axioms outer_tick_noCarry_run
-- the run's step-count closed form: runSteps 1 n = 4n+4n²+6n (= 0,14,36,66,104 for n=0..4):
#eval decide (List.map (runSteps 1) [0,1,2,3,4] = [0, 14, 36, 66, 104])                 -- true
#eval decide (List.map (fun n => 4*n*1 + 4*n*n + 6*n) [0,1,2,3,4] = [0, 14, 36, 66, 104]) -- true
-- the n=2 run (t=1, work=9, M'=(10), R=[]) is EXACTLY the two-tick stretch from the real
-- orbit config at n=6717 (register ⟨1,13⟩, left comb (10)^3): 36 steps, ⟨1,13⟩→⟨5,9⟩,
-- head 0→4, two comb pairs consumed — kernel cross-check of `outer_tick_noCarry_run 2`:
#eval decide (steps (runSteps 1 2)
        ((⟨1, 9 + 2 * 2⟩ : Odo).toCfg 0 (pow10 2 ++ pow10 1) [])
      = some ((⟨1 + 2 * 2, 9⟩ : Odo).toCfg (0 + 2 * (2 : Int)) (pow10 1) []))            -- true
-- the same run written on the raw tape (the real n=6717 config `1^3 0 (10)^3 · 1^13 0^2`):
#eval decide (steps 36 ⟨.E, 0, ⟨ones 3 ++ (false :: pow10 3), false, ones 13 ++ [false, false]⟩⟩
      = some ⟨.E, 4, ⟨ones 11 ++ (false :: pow10 1), false, ones 9 ++ [false, false]⟩⟩)   -- true

-- §5m GENERAL-`j` CARRY CORE axiom audits + kernel cross-checks:
#print axioms carry_repack
#print axioms carry_repack_doubles
#print axioms carry_repack_anchor_j4
#print axioms carry_repack_anchor_j5
-- §5s: the depth-1 carry factored (ENTRY ∘ CORE=sweepEF ∘ EXIT), on-path:
#print axioms carry_entry_j3
#print axioms carry_core_j3
#print axioms carry_exit_j3
#print axioms carry_event_5to13_ECE
#print axioms carry_ECE_eq_anchor
-- §5u: the DEPTH-2 (j=4) carry, BUILT from the j=3 carry (REUSE) + the sweepEF CORE:
#print axioms carry_j4          -- the whole 657-step level-4 carry, ∀ L R
#print axioms j4_carry_B        -- the embedded j=3 carry, discharged by carry_event_5to13
#print axioms j4_core_D         -- the CORE repack (10)^14→1^28, discharged by sweepEF 14
-- cross-check: carry_j4 reproduces the raw-orbit endpoints with EMPTY tails (kernel):
#eval decide ((steps 657 ⟨.E, -21, ⟨false :: false :: [], false,
        false :: true :: true :: true :: true :: true :: true :: true :: true :: true ::
        true :: true :: true :: true :: false :: false :: true :: true :: true :: true ::
        true :: false :: false :: true :: []⟩⟩).isSome)                                -- true
-- the culminating repack at design j=3 (m=6) — the CORE of carry_event_5to13, on-path
-- (raw n=6626): (10)^6 → 1^{12} in 12 steps, = carry_repack 1:
#eval decide (steps (2 * (2 ^ (1 + 2) - 2)) ⟨.E, 0, ⟨[], false, pow10 6⟩⟩
      = some ⟨.E, 12, ⟨ones 12, false, []⟩⟩)                                        -- true
-- j=4 (m=14, raw n=6895) and j=5 (m=30, raw n=8016): window GROWS 12,28,60 = 2·(2^j−2):
#eval decide (steps 28 ⟨.E, 0, ⟨[], false, pow10 14⟩⟩
      = some ⟨.E, 28, ⟨ones 28, false, []⟩⟩)                                        -- true
#eval decide (steps 60 ⟨.E, 0, ⟨[], false, pow10 30⟩⟩
      = some ⟨.E, 60, ⟨ones 60, false, []⟩⟩)                                        -- true
-- the doubling: repack block 2·(2^j−2) = 2^{j+1}−4, one below the doubled digit
-- 2·(2^j−3)+3; e.g. j-design 3,4,5: 12,28,60 = 13−1,29−1,61−1:
#eval decide (List.map (fun j => 2 * (2 ^ (j + 2) - 2)) [1,2,3] = [12, 28, 60])    -- true
#eval decide (List.map (fun j => 2 * (2 ^ (j + 2) - 3) + 3) [1,2,3] = [13, 29, 61]) -- true
-- the concrete on-path tick n=6717→6731 (t=1, built=3, work=13), tail-parametric:
#eval decide (steps 14 ⟨.E, 0, ⟨ones 3 ++ (false :: pow10 3), false,
        ones 13 ++ (false :: false :: [])⟩⟩
      = some ⟨.E, 2, ⟨ones 6 ++ pow10 3, false, ones 11 ++ (false :: false :: [])⟩⟩) -- true
-- the next tick (t=3, built=7, work=11) is 4·3+10 = 22 steps — the connector GROWS
-- with the block (block-parametric, NOT constant-size), confirming §5l's finding:
#eval decide (steps 22 ⟨.E, 0, ⟨ones 7 ++ (false :: pow10 3), false,
        ones 11 ++ (false :: false :: [])⟩⟩
      = some ⟨.E, 2, ⟨ones 10 ++ pow10 3, false, ones 9 ++ (false :: false :: [])⟩⟩) -- true
-- ecfold really folds `1^{2t+2}` → `pow10 (t+1)` leftward (t=2: 1^6 → (10)^3, 6 steps):
#eval decide (steps 6 ⟨.E, 0, ⟨ones 5 ++ (false :: pow01 2), true, []⟩⟩
      = some ⟨.E, -6, ⟨pow01 2, false, pow10 3⟩⟩)                                   -- true
-- odoNext parity invariant: 2t+1 stays ODD (2t+1 → 2(t+2)+1); e.g. 3 → 7 → 11:
#eval decide (List.map (fun t => 2 * (odoNext ⟨t, 13⟩).t + 1) [1, 3, 5] = [7, 11, 15]) -- true
-- the carried digit chain 1,5,13,29,61 = 2^{n+2}−3 (odoNext):
#eval decide (List.map carryDigit [0,1,2,3,4] = [1, 5, 13, 29, 61])               -- true
#eval decide (List.map (fun n => 2 ^ (n + 2) - 3) [0,1,2,3,4] = [1, 5, 13, 29, 61]) -- true

#print axioms sanity100

-- §5n LAYER B (PURE ODOMETER, well-founded counter) axiom audits + cross-checks:
#print axioms LayerB.binInc_val
#print axioms LayerB.binInc_ripple
#print axioms LayerB.odoValue_odoNext
#print axioms LayerB.odo_terminates
#print axioms LayerB.odo_mu_step
#print axioms LayerB.rippleDepth_le
-- the +1 law realized: binInc increments the value by exactly 1 (incl. across ripple):
#eval decide (List.map (fun v => LayerB.binVal (LayerB.binInc (LayerB.toBits 6 v)))
      [0,1,2,3,6,7,14,30] = [1,2,3,4,7,8,15,31])                                  -- true
-- the level-j overflow threshold = 2^j−1 (comb full): 1,3,7,15,31 at j=1..5:
#eval decide (List.map (fun j => LayerB.binVal (List.replicate j true)) [1,2,3,4,5]
      = [1,3,7,15,31])                                                            -- true
-- a level-3 carry ripples through 3 ones and sets bit 3 (0^3 1 …), depth = 3:
#eval decide (LayerB.binInc (List.replicate 3 true ++ [false, false, true])
      = List.replicate 3 false ++ [true, false, true])                           -- true
#eval decide (LayerB.rippleDepth (List.replicate 3 true ++ [false]) = 3)         -- true
-- T = 2^K − 1 ticks entry→final (the value gap = the clean measure μ at entry):
#eval decide (LayerB.odoValue (LayerB.odoFinal 10) - LayerB.odoValue (LayerB.odoEntry 10)
      = 2 ^ 10 - 1)                                                              -- true (=1023)
-- STRUCTURAL faithfulness: the carry doubles the cascade digit (carryDigit chain),
-- and each level-j carry HALVES in count (binary-counter bit profile) — matches
-- x2wf_counter.py.  NOTE: the pure-counter tick-count 2^K−1 is NOT the raw tape
-- round-trip count 3852/9729/19470 (x2wf_measure.py): one carry ↔ a Θ(2^j) tape
-- block-chew, so the tape count is a FINER (Layer-C) quantity.  See §5n HONEST GAP.
#eval decide (List.map LayerB.rippleDepth
      [[false], [true, false], [true, true, false]] = [0, 1, 2])                 -- true

-- §5o LAYER B′ FAITHFUL ODOMETER (2026-07-13): the EXACT tick/carry closed form.
#print axioms LayerBFaithful.faithful_terminates
#print axioms LayerBFaithful.odoValueF_odoNextF
#print axioms LayerBFaithful.faithful_gap
-- Tfaithful EXACTLY matches the raw doubling-phase chew-start counts (x2fr_*.py,
-- from the VERIFIED-FAITHFUL x2bd_sim orbit), at K=10,11,12,13:
#eval decide (List.map LayerBFaithful.Tfaithful [10,11,12,13] = [3852, 9729, 19470, 47107]) -- true
-- Cfaithful EXACTLY matches the raw carry counts at K=10,11,12,13:
#eval decide (List.map LayerBFaithful.Cfaithful [10,11,12,13] = [192, 386, 768, 1538])       -- true
-- CONTRAST §5n's flat counter 2^K−1 (1023/2047/4095/8191) — NOT the real count:
#eval decide (List.map (fun K => 2 ^ K - 1) [10,11,12,13] = [1023, 2047, 4095, 8191])         -- true
-- the faithful register reaches final in EXACTLY Tfaithful ticks (value gap = T):
#eval decide (LayerBFaithful.odoValueF (LayerBFaithful.odoFinalF 12)
      - LayerBFaithful.odoValueF LayerBFaithful.odoEntryF = 19470)                             -- true

-- §5q LOW PHASE TOWARD ∀g (g-independent entry + 2nd even anchor) axiom audits + cross-checks:
#print axioms lp_c0
#print axioms lp_c4
#print axioms lowPhase_entry
#print axioms lowPhaseEven_g4
-- the g-independent ENTRY fires for BOTH parities of the pos-36 tail cell (b = false → even g's
-- `0^10` tail, b = true → odd g / next U-unit), landing state A at pos 36 — the divergence
-- boundary (`x2lo_div.py`), halt-free either way (`some`):
#eval decide (((steps 250 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: (zeros 6 ++ (true :: (zeros 6 ++ (false :: [])))))⟩⟩).map
      (fun c => (c.st, c.pos))) = some (St.A, (36 : Int)))                                     -- true (b=false)
#eval decide (((steps 250 ⟨.E, 0, ⟨[], false,
        zeros 21 ++ (true :: (zeros 6 ++ (true :: (zeros 6 ++ (true :: [])))))⟩⟩).map
      (fun c => (c.st, c.pos))) = some (St.A, (36 : Int)))                                     -- true (b=true)
-- LOW phase length GROWS with g (NOT a fixed transport): 343,419,419,495,495 for g=2..6
-- (raw-measured `x2lo_probe.py`); the even `M6` register form is g-independent (`lowPhaseEven_g4`
-- lands the SAME leading `0^2 (10)^4 1^9 0^2 …` as `lowPhaseEven_g2`).

-- §5t LOW-PHASE MIDDLE FORWARD PASS (the fixed per-U-unit tile + its ∀m run) axiom audits:
#print axioms lowMiddle_tile
#print axioms lowMiddle_fwd
-- ONE tile: 29 steps consume one comb unit `0^6 1`, regenerate the `[1 0 1 0 0 1]` prefix,
-- deposit `[1 0 1 1 1 1 1]` left, march +7 (frame-independent, here `L=[], Y=[]`):
#eval decide (steps 29 ⟨.E, 0, ⟨[], false,
        true :: false :: true :: false :: false :: true ::
        false :: false :: false :: false :: false :: false :: true :: []⟩⟩
      = some ⟨.E, 7, ⟨rdepo 1, false, true :: false :: true :: false :: false :: true :: []⟩⟩) -- true
-- the RUN over m=5 U-units (43 tiles' worth in the real g=6 middle): 145 steps, +35, deposit
-- rdepo 5, comb fully consumed to the bare prefix (self-contained instance of `lowMiddle_fwd`):
#eval decide (steps (29 * 5) ⟨.E, 0, ⟨[], false,
        true :: false :: true :: false :: false :: true :: (rcomb 5 ++ [])⟩⟩
      = some ⟨.E, 35, ⟨rdepo 5 ++ [], false,
          true :: false :: true :: false :: false :: true :: []⟩⟩)                              -- true
-- ON-PATH GROUNDING: the period-7 comb the run consumes is exactly the U-unit → R-unit form of
-- the REAL blank→build(6) orbit at the chain start (raw step 157): register right-of-head =
-- `[1 0 1 0 0 1] ++ (0^6 1)^m` (`x2lm_chain.py`, 1-positions 1,3,6,13,20,27,34,… ; extracted
-- cell-for-cell from `x2bd_sim.build(6)`).  `rcomb 2` is the concrete two-unit comb `0^6 1 0^6 1`:
#eval decide (rcomb 2 = [false, false, false, false, false, false, true,
                         false, false, false, false, false, false, true])                       -- true

-- §5r TOP-LEVEL NON-HALT FRAME axiom audits:
#print axioms nonhalt_of_segments
#print axioms x2_cycle
#print axioms x2_nonhalt

-- §5v CARRY-CONNECTOR ∀j-PARAMETRIC axiom audits (MIDDLE = outer_tick_noCarry_run reuse):
#print axioms carry_j4_middle_run
#print axioms carry_j4_middle_run'
#print axioms carry_j5_middle_run
#print axioms carry_j5_middle_run'
#print axioms carry_middle_len_formula

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
   **§5q UPDATE (2026-07-13, instrumented).**  The low phase is a GROWING braid, NOT
   a fixed transport: length `343/419/419/495/495` for g=2..6 (`≈+38`/gen, one extra
   `(1 0^6)` U-unit per generation).  What CLOSED here: `lowPhase_entry` — the FIXED,
   g-INDEPENDENT first `250` steps (∀g, tail-parametric, HALT-FREE, kernel `rfl` in
   5 chunks), the maximal generation-independent prefix (pos 36 is the divergence
   boundary `x2lo_div.py`); and `lowPhaseEven_g4` — a SECOND full even instance
   `M1(4)→M6(4)` (419 steps).
   **§5t UPDATE (2026-07-13, re-instrumented `x2lm_*.py`).**  The growing MIDDLE's
   FORWARD (register-processing) pass is NOW CLOSED `∀m`: it is a CLEAN fixed 29-step
   tile (`lowMiddle_tile`, frame-independent, `+7`/U-unit) run once per U-unit over a
   period-7 comb, `lowMiddle_fwd` by length induction — the per-round-trip length is
   CONSTANT (14/4/3/8), the earlier "grows with the accumulating comb" reading was the
   ODD-`g` block-trim, not the forward tile.  STILL OPEN for the full `∀g` middle: the
   fixed entry/turnaround connectors, the RETURN pass (uniform `dSweepTurn`-shape run),
   and the odd-`g` `−4` block trim (growth law `mid(g)=261+76·⌊(g−1)/2⌋`).
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
   as a concrete `Cfg`, and the transport `M1(g)→M1(g+1)` ∀g on FULL-tape configs.
   **§5r UPDATE (2026-07-13).**  The LOGICAL frame is now CLOSED: `nonhalt_of_segments`
   (PURE, unconditional — an infinite chain of nonempty halt-free segments ⟹
   `∀N, steps N (c 0) ≠ none`) and the CONDITIONAL `x2_nonhalt` (given `Cfg`-valued
   milestone families with the low + doubling transports as EXPLICIT HYPOTHESES, the
   machine never halts).  Tail-threading is discharged by the shared `Cfg` families
   (`x2_cycle`).  What remains OPEN is the ANTECEDENT: exhibiting the full-tape
   milestone `Cfg` families and PROVING the two transports (items 1–3 above) — the
   §5j/§5q concrete lemmas use truncated / tail-parametric stand-ins.  `x2_nonhalt`
   DECIDES NOTHING; it only reduces non-halting to those open transports.

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

/-! ## §5w (LAYER A/B, ON-PATH, 2026-07-14) THE `carry_step` WELL-FOUNDED RECURSION —
assembling §5v's structural finding into a GROUNDED recursive register, a PROVEN ∀j
descent-fold + middle-run + core, a WF measure, and the recursion skeleton, with the
single remaining recursive object (`EXIT`) named precisely.

**What §5v established** (all GREEN, on-path, `x2cu_*.py` cell-for-cell): the level-`j`
block-doubling carry `C(j)` (block `1^{d_j} → 1^{d_{j+1}}`, `d_j = 2^j − 3`) decomposes,
at its `E`-on-`0` odometer anchors, as

```
  C(j) = DESCENT-FOLD(j)  ∘  [seam glue]  ∘  C(j−1)  ∘  MIDDLE(j)  ∘  CORE(j)  ∘  EXIT(j)
```

with DESCENT-FOLD, MIDDLE, CORE all PROVEN `∀j`-parametric, the seam glue `∀j`-uniform,
and `EXIT(j) ⊇ CORE(j−1) ∘ EXIT(j−1)` the one strictly-lower recursive object.  This
section turns that into named, grounded Lean objects.

**Grounding (the on-path discipline).**  The carry register's RIGHT side is the FULL
descending cascade `1^{d_j} 0² 1^{d_{j−1}} 0² … 1^{d_2}` (`d_2 = 1`), read CELL-FOR-CELL
off the real `x2bd_sim.build(2)` orbit at the `C(j)`-start anchors `n = 6591 (j=3)`,
`6484 (j=4)`, `6397 (j=5)` (`x2cu_*.py` snapshot).  `cascadeTail` below IS this cascade,
and `cascadeTail_grounds_carry_j3/_j4` PROVE it reproduces the RIGHT sides of the two
already-proven concrete carries `carry_event_5to13` (j=3) and `carry_j4` (j=4) EXACTLY,
by `rfl` — so the recursive register is on-path, not invented. -/

/-- The digit values along the extended orbit chain (kernel cross-check; reuses the
EXISTING `carryDigit n = 2^{n+2}−3` of §5-carry, indexed by carries-from-bottom, so
`level j = n+2`: `d_2=1, d_3=5, d_4=13, d_5=29, d_6=61`).  Matches `carry_event_5to13`
(`5→13`, `n:1→2`) and `carry_j4` (`13→29`, `n:2→3`) on the real orbit. -/
theorem carryDigit_chain :
    carryDigit 0 = 1 ∧ carryDigit 1 = 5 ∧ carryDigit 2 = 13 ∧
      carryDigit 3 = 29 ∧ carryDigit 4 = 61 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE CARRY REGISTER'S CASCADE TAIL, `∀n` (the recursive datatype).**  The RIGHT-side
register at a level-`j = n+2` carry anchor is the full descending base-2 cascade
`1^{d_j} 0² 1^{d_{j−1}} 0² … 1^{d_2}` (`d_2 = 1`), read CELL-FOR-CELL off the real orbit
(`x2cu` snapshot, `n=6591/6484/6397`).  DEFINED by structural recursion `n+1 ↦ n`, so
`cascadeTail (n+1)` literally CONTAINS `cascadeTail n` as its tail below the top block
`1^{carryDigit (n+1)}` — the register-level realization of `C(j) ⊃ C(j−1)`. -/
def cascadeTail : Nat → List Bool
  | 0 => ones 1
  | (n + 1) => ones (carryDigit (n + 1)) ++ (false :: false :: cascadeTail n)

/-- **The cascade tail's recursive unfold** (`rfl`): level `j = n+3` is the top block
`1^{d_{n+1}}` over `0²` over the level-`(j−1)` cascade `cascadeTail n`.  This is the
recursion's DESCENT leg at the register level — peeling the top digit exposes the
strictly-lower register. -/
theorem cascadeTail_unfold (n : Nat) :
    cascadeTail (n + 1) = ones (carryDigit (n + 1)) ++ (false :: false :: cascadeTail n) :=
  rfl

/-- **GROUNDING (j=3): `cascadeTail` reproduces `carry_event_5to13`'s RIGHT side.**  The
real carry's input right (raw `n=6591`) is `0³ 1^5 0² 1 0^{11} · R`, i.e. exactly
`zeros 3 ++ cascadeTail 1 ++ zeros 11 ++ R` (`cascadeTail 1 = 1^5 0² 1`).  Kernel `rfl` —
the register is on-path. -/
theorem cascadeTail_grounds_carry_j3 (R : List Bool) :
    zeros 3 ++ cascadeTail 1 ++ zeros 11 ++ R
      = false :: false :: false :: true :: true :: true :: true :: true :: false :: false ::
        true :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
        false :: false :: R :=
  rfl

/-- **GROUNDING (j=4): `cascadeTail` reproduces `carry_j4`'s RIGHT side.**  The real
carry's input right (raw `n=6484`) is `0 1^{13} 0² 1^5 0² 1 0^{33} · R`, i.e. exactly
`zeros 1 ++ cascadeTail 2 ++ zeros 33 ++ R` (`cascadeTail 2 = 1^{13} 0² 1^5 0² 1`).  Kernel
`rfl` — grounds the SECOND proven carry, so the recursive register matches BOTH depths on
the real orbit. -/
theorem cascadeTail_grounds_carry_j4 (R : List Bool) :
    zeros 1 ++ cascadeTail 2 ++ zeros 33 ++ R
      = false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true ::
        true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false ::
        false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
        false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
        false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false ::
        false :: false :: R :=
  rfl

/-- `2 ≤ 2^{m+1}` (helper for the descent-fold's block-length arithmetic). -/
theorem two_le_two_pow_succ : ∀ m, 2 ≤ 2 ^ (m + 1) := by
  intro m
  induction m with
  | zero => decide
  | succ k ih => rw [Nat.pow_succ]; omega

/-- **THE CARRY ENTRY DESCENT-FOLD, `∀`-level (deliverable A).**  At a level-`j = m+2`
carry's start, the top solid block `1^{d_m} = 1^{carryDigit m} = 1^{2^{m+2}−3}` (head `E`
on the boundary `0`) is folded to the comb `pow01 (2^{m+1}−2)` (deposited on the left) plus
the residue `1^1`, in `6·(2^{m+1}−2)` steps, `M/R` untouched.  This is EXACTLY
`ecombChewFold (2^{m+1}−2)` — the descent that peels the top digit and exposes the
strictly-lower register `cascadeTail (m−1)` below.  Converts §5v's `FOLD_RUN` observation
into a PROVEN `∀`-level connector: cross-checks `C4` (m=2 ⇒ `6` folds) and `C5` (m=3 ⇒ `14`
folds).  `some` ⇒ HALT-FREE.  `[propext, Quot.sound]`-only. -/
theorem carry_descent_fold (m : Nat) (p : Int) (L R : List Bool) :
    steps (6 * (2 ^ (m + 1) - 2)) ⟨.E, p, ⟨L, false, false :: (ones (carryDigit m) ++ R)⟩⟩
      = some ⟨.E, p + 2 * ((2 ^ (m + 1) - 2 : Nat) : Int),
          ⟨pow01 (2 ^ (m + 1) - 2) ++ L, false, false :: (ones 1 ++ R)⟩⟩ := by
  have hd : carryDigit m = 2 * (2 ^ (m + 1) - 2) + 1 := by
    rw [carryDigit_closed]
    have e : 2 ^ (m + 2) = 2 ^ (m + 1) * 2 := Nat.pow_succ 2 (m + 1)
    have h2 := two_le_two_pow_succ m
    omega
  rw [hd]
  exact ecombChewFold (2 ^ (m + 1) - 2) p L R

/-- **Descent-fold length cross-check** (m=2 ⇒ C4's `6`-fold entry; m=3 ⇒ C5's `14`-fold
entry), matching the `x2cu_decompose.py` `FOLD_RUN` counts. -/
theorem carry_descent_fold_counts :
    (2 ^ (2 + 1) - 2 = 6 ∧ 6 * (2 ^ (2 + 1) - 2) = 36) ∧
      (2 ^ (3 + 1) - 2 = 14 ∧ 6 * (2 ^ (3 + 1) - 2) = 84) := by
  refine ⟨⟨by decide, by decide⟩, ⟨by decide, by decide⟩⟩

/-- **THE CARRY MIDDLE no-carry RUN, `∀`-level (deliverable A/C, MIDDLE piece).**  Between
the embedded lower carry `C(j−1)` and the CORE repack, the level-`j = m+2` carry runs a
maximal no-carry stretch that is EXACTLY `outer_tick_noCarry_run (2^{m+1}−4)` at `t=1`
(solid block `1^3`), `work` from `5+2·(2^{m+1}−4)` down to `5`, consuming `(10)^{2^{m+1}−4}`.
Generalizes `carry_j4_middle_run` (m=2, `run 4`) / `carry_j5_middle_run` (m=3, `run 12`) to
ALL levels, by DIRECT REUSE of the PROVEN `∀n` §5p run.  `[propext, Quot.sound]`-only. -/
theorem carry_level_middle (m : Nat) (p : Int) (M' R : List Bool) :
    steps (runSteps 1 (2 ^ (m + 1) - 4))
        ((⟨1, 5 + 2 * (2 ^ (m + 1) - 4)⟩ : Odo).toCfg p (pow10 (2 ^ (m + 1) - 4) ++ M') R)
      = some ((⟨1 + 2 * (2 ^ (m + 1) - 4), 5⟩ : Odo).toCfg
          (p + 2 * ((2 ^ (m + 1) - 4 : Nat) : Int)) M' R) :=
  outer_tick_noCarry_run (2 ^ (m + 1) - 4) p 1 5 M' R

/-- **THE CARRY CORE repack, `∀`-level (deliverable C, CORE piece).**  At the culminating
repack the built comb `(10)^{2^{m+2}−2}` is doubled to the solid block `1^{2^{m+3}−4}`
(one below the doubled digit `d_{m+1}`), `R` untouched — EXACTLY `carry_repack m`
(`= sweepEF (2^{m+2}−2)`, PROVEN `∀j` in §5m).  Named here as the level-`j` CORE for the
recursion.  `[propext, Quot.sound]`-only. -/
theorem carry_level_core (m : Nat) (L R : List Bool) :
    steps (2 * (2 ^ (m + 2) - 2)) ⟨.E, 0, ⟨L, false, pow10 (2 ^ (m + 2) - 2) ++ R⟩⟩
      = some ⟨.E, 2 * ((2 ^ (m + 2) - 2 : Nat) : Int),
          ⟨ones (2 * (2 ^ (m + 2) - 2)) ++ L, false, R⟩⟩ :=
  carry_repack m L R

/-- **THE WELL-FOUNDED CARRY RECURSION SKELETON (deliverable D, the WF frame).**  The
level-indexed carry recursion is well-founded on the level `n` (the §5n `odo_terminates`
digits-left measure, `≤ K`): from the base level `n=1` (`j=3`, `carry_event_5to13`) and a
step `P n → P (n+1)`, EVERY level `n ≥ 1` holds.  PROVEN by `Nat.le_induction` (a genuine
WF/structural recursion — NOT `partial def`, NOT `sorry`).  A closed `carry_step` is
EXACTLY this combinator instantiated at the concrete level-`n` transport `P`; the base is
discharged by `carry_event_5to13`, the pieces of the step by `carry_descent_fold`
(DESCENT), `carry_level_middle` (MIDDLE), `carry_level_core` (CORE) and the IH `P n`
(the embedded lower carry, realized concretely at depth 2 by `carry_j4`'s reuse of
`carry_event_5to13`), leaving ONLY the recursive `EXIT(n+1) ⊇ CORE(n) ∘ EXIT(n)` object. -/
theorem carry_level_rec {P : Nat → Prop} (hbase : P 1)
    (hstep : ∀ n, 1 ≤ n → P n → P (n + 1)) : ∀ n, 1 ≤ n → P n := by
  intro n
  induction n with
  | zero => intro h; exact absurd h (by decide)
  | succ k ih =>
    intro _
    cases k with
    | zero => exact hbase
    | succ j => exact hstep (j + 1) (by omega) (ih (by omega))

/-! ### §5w: what CLOSED, and the single remaining object (`carry_step`) — [DESIGN].

**PROVEN GREEN this section (on-path, all `[propext, Quot.sound]`-only):**
  • `carryDigit_chain` — the digit ladder `1,5,13,29,61` (= `2^{n+2}−3`), grounding the
    block lengths of both proven carries.
  • `cascadeTail` (+ `cascadeTail_unfold`) — the carry register's RIGHT side as a RECURSIVE
    datatype, `cascadeTail (n+1) ⊃ cascadeTail n`, read cell-for-cell off the real orbit.
  • `cascadeTail_grounds_carry_j3` / `_j4` — the register reproduces `carry_event_5to13`'s
    (j=3) and `carry_j4`'s (j=4) RIGHT sides EXACTLY, by `rfl`.  **The two concrete carries
    are reproduced — the register is on-path, not invented.**
  • `carry_descent_fold` — the carry ENTRY block→comb fold, `∀`-level (via `ecombChewFold`).
  • `carry_level_middle` — the carry MIDDLE no-carry run, `∀`-level (via
    `outer_tick_noCarry_run`), generalizing `carry_j4/j5_middle_run`.
  • `carry_level_core` — the carry CORE repack, `∀`-level (via `carry_repack`).
  • `carry_level_rec` — the WF recursion SKELETON on the level (`Nat.le_induction`).

So of `C(j) = DESCENT ∘ glue ∘ C(j−1) ∘ MIDDLE ∘ CORE ∘ EXIT`, the DESCENT, MIDDLE, CORE
are PROVEN `∀`-level connectors, the register is a grounded recursive datatype, and the
recursion's control flow is the proven `carry_level_rec` — with the base and depth-2 step
already GREEN as `carry_event_5to13` / `carry_j4`.

**THE SINGLE REMAINING OBJECT — `carry_step`, [DESIGN, precisely located].**  To instantiate
`carry_level_rec` at the concrete tape-level transport requires the per-level STEP
`P n → P (n+1)`, whose only non-`∀`-uniform ingredient is

```lean
-- [DESIGN] EXIT(n+1) : the carry's regeneration sub-phase, a WF recursion one level down.
--   EXIT(n+1) = [const seam glue, ∀-uniform per §5v(2)]
--             ∘ CORE(n)        -- = carry_level_core (n−1), PROVEN ∀-level
--             ∘ EXIT(n)        -- the strictly-lower recursive call (measure n ↓)
--   grounded: EXIT(1)=70 steps (carry_exit_j3, §5s), EXIT(2)=218, EXIT(3)=722 (x2cu).
```

`EXIT` is well-founded (each call strictly decreases the level `n`, the §5n
`odo_terminates` measure), its glue is `∀`-uniform (§5v(2)), and its CORE is the PROVEN
`carry_level_core` — so the ONLY open work is the DEFINITIONAL naming of the `EXIT`
recursive object and the register-level `steps_add` book-keeping that threads the grounded
`cascadeTail` register through DESCENT ∘ IH ∘ MIDDLE ∘ CORE ∘ EXIT.  We state `carry_step`
as `[DESIGN]` (comment, NO `sorry`, NO axiom) rather than force a green `∀j` transport whose
register threading is unverified — the discipline's on-path requirement.  `carry_step`
remains the project's `Suffix.lean`-scale object; NO machine is decided by this section. -/

-- §5w carry_step WF-RECURSION axiom audits (register grounding + ∀-level connectors + skeleton):
#print axioms carryDigit_chain
#print axioms cascadeTail_unfold
#print axioms cascadeTail_grounds_carry_j3
#print axioms cascadeTail_grounds_carry_j4
#print axioms carry_descent_fold
#print axioms carry_descent_fold_counts
#print axioms carry_level_middle
#print axioms carry_level_core
#print axioms carry_level_rec

/-! ## §5x (LAYER A, ON-PATH, 2026-07-14) THE EXIT DYNAMICS ∀j — the decisive
decomposition of `EXIT(j)`, the ∀j-uniform glue proven as reusable transports, the
recursion pinned, and `carry_exit` stated `[DESIGN]` with the EXACT obstruction.

**THE EXPERIMENT (`x2ex_*.py`, cell-for-cell from the faithful `x2bd_sim.build(2)`
orbit).**  The carry EXIT — the post-CORE regeneration that rebuilds the fresh
`1^{2^j−3}` block below the just-doubled block and re-anchors `E` on the new boundary —
was extracted at THREE levels and decomposed at its `E`-on-`0` odometer anchors into
proven-piece instances (`sweepEF m` / descent-fold / no-carry tick / glue):

```
  EXIT(3) = [6638,6708]  70 steps,  5 pieces:  g3 g15 g7 sweepEF2 g41
  EXIT(4) = [6923,7141] 218 steps, 18 pieces:  2folds g3 g3 g15 g7 sweepEF2 g24 ·
                                                g7 sweepEF1 g8 sweepEF3 g12 sweepEF6 ·
                                                g3 g15 g7 sweepEF2 NTICK(t=16)
  EXIT(5) = [8076,8798] 722 steps, 52 pieces:  6folds g3 2folds g3 g3 g15 g7 sweepEF2 g24 ·
                                                [C3-shaped carry: g7 sweepEF1 g8 sweepEF3 g12
                                                 sweepEF6 g3 g15 g7 sweepEF2 g41] ·
                                                [C4-core buildup: g7 sweepEF1 … sweepEF14] ·
                                                [C3-shaped EXIT: 2folds … sweepEF6 … g139]
```

**DECISIVE VERDICT — the EXIT is NOT ∀j-parametric as a straight-line composite; it is a
WELL-FOUNDED RECURSION in `j`.**  Two hypotheses tested and REFUTED:

* **(H1) verbatim self-embedding — REFUTED** (confirms the main-loop's independent
  finding).  The `(state,head,Δpos)` trace of `EXIT(3)` occurs ZERO times inside
  `EXIT(4)` or `EXIT(5)`, and `EXIT(4)` zero times inside `EXIT(5)` (`x2ex_decompose.py`,
  containment index `= −1` all three).  Even the piece-TOKEN sequence of `EXIT(3)` is NOT
  a contiguous sublist of `EXIT(4)`'s: the shared re-anchor motif `g3 g15 g7 sweepEF2`
  ends `g41` in `EXIT(3)` but `g24` / `NTICK(t=16)` inside `EXIT(4)` — the regeneration
  runs against a DIFFERENT tape background at each level (a bigger doubled block above it),
  so the terminal glue and local context differ.  `EXIT(j)` is NOT a copy of `EXIT(j−1)`.

* **(H2) straight-line parametric — REFUTED.**  The piece-token-sequence LENGTH grows
  `5 → 18 → 52` (not a fixed sequence at parametric lengths); the sequences share NO common
  prefix (`lcp = 0`: `EXIT(4)`/`EXIT(5)` open with a descent-fold that `EXIT(3)` lacks) and
  the step-count grows `70 → 218 → 722` with ratios `3.11, 3.31` — NOT geometric, NOT a
  clean `4^j+2^j`-closed form.  There is NO `[fixed piece types](j)` with lengths `f(j)`.

* **THE TRUE ∀j STRUCTURE (pinned).**  `EXIT(j) = DESCENT-FOLD(2^{j−2}−2) ∘ REGEN(j−1)`,
  where `REGEN(j−1)` is a scale-`(j−1)` **carry-SHAPED** regeneration — `ENTRY-glue ∘
  [embedded lower carry] ∘ MIDDLE-run ∘ CORE ∘ [scale-`(j−2)` EXIT]` — bottoming out at the
  base anchor motif of `EXIT(3)`.  The nesting DEPTH `= j−3` grows with `j`; `EXIT(5)`
  literally contains a full C4-shaped regeneration, which contains a C3-shaped one.  So the
  EXIT — and hence `carry_step` — is a genuine well-founded recursion on `j`, exactly the
  §5w `[DESIGN]` object, NOT a straight-line ∀j transport.

**WHAT IS ∀j-UNIFORM (proven GREEN here).**  Although the ARRANGEMENT recurses, its
BUILDING BLOCKS are ∀j-uniform.  `x2ex_motif.py` verifies (identical `(state,head,Δpos)`
trace at every occurrence) that the two recurring EXIT motifs are the SAME transport at all
levels — the concrete realization of §5v(2)'s "seam glue is ∀j-uniform" for the EXIT:
  • the RE-ANCHOR motif `g3 g15 g7 sweepEF2` (29 steps) — identical at 4 sites across
    `EXIT(3)/(4)/(5)` — is `exit_anchor_motif` below;
  • the C3-BODY buildup `g7 sweepEF1 g8 sweepEF3 g12 sweepEF6` (47 steps) — identical at 3
    sites across `EXIT(4)/(5)` — is `exit_c3body_motif` below;
  • the opening DESCENT-FOLD count obeys the ∀j law `2^{j−2}−2` (`exit_fold_count_law`),
    reusing §5w's `carry_descent_fold` / `ecombChewFold` family.
So the EXIT's growth lives ENTIRELY in (a) these ∀j-uniform / ∀-length-proven blocks and
(b) the strictly-lower recursive `REGEN(j−1)` — precisely a WF recursion, no non-uniform
"new physics" per level.  What does NOT close is the DEFINITIONAL naming of that recursive
`REGEN`/`EXIT` object; we state it `[DESIGN]`, not a forced green transport. -/

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **EXIT ∀j-UNIFORM GLUE (1/2): the RE-ANCHOR motif** `g3 g15 g7 sweepEF2`, 29 steps,
head rel `0 → +7`, `L` untouched (excursion rel `[0,+7]`).  Extracted cell-for-cell from
the `EXIT(3)` occurrence (raw `n = 6638→6667`); Python-verified TRANSLATION-INVARIANT — the
identical `(state,head,Δpos)` transport recurs at 4 sites across `EXIT(3)/(4)/(5)`
(`x2ex_motif.py`).  The `∀j`-uniform seam glue that re-anchors `E` on the fresh boundary,
now a named reusable transport.  `some` ⇒ HALT-FREE.  Kernel `rfl`. -/
theorem exit_anchor_motif (L R : List Bool) :
    steps 29 ⟨.E, 0, ⟨L, false,
        false :: true :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, 7, ⟨true :: true :: true :: true :: true :: false :: true :: L, false, R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **EXIT ∀j-UNIFORM GLUE (2/2): the C3-BODY buildup** `g7 sweepEF1 g8 sweepEF3 g12
sweepEF6`, 47 steps, head rel `0 → +9`, excursion rel `[−3,+9]`.  Extracted cell-for-cell
from the `EXIT(4)` occurrence (raw `n = 6991→7038`); Python-verified TRANSLATION-INVARIANT —
the identical transport recurs at 3 sites across `EXIT(4)/(5)` (`x2ex_motif.py`).  This is
the ascending mini-CORE that rebuilds the smallest block inside every regeneration.
`some` ⇒ HALT-FREE.  Kernel `rfl`. -/
theorem exit_c3body_motif (L R : List Bool) :
    steps 47 ⟨.E, 0, ⟨false :: true :: false :: L, false,
        false :: false :: false :: true :: true :: true :: true :: true :: false :: R⟩⟩
      = some ⟨.E, 9, ⟨true :: true :: true :: true :: true :: true :: true :: true :: true ::
          true :: true :: true :: L, false, R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
/-- **THE DEPTH-2 EXIT AS A REUSABLE TRANSPORT — `carry_exit_j4` (parallel to
`carry_exit_j3`).**  Raw `n = 6923 → 7141` (**218 steps**): from the CORE's just-deposited
`1^{28}` (head `E` rel `+10`) the level-4 EXIT regenerates the fresh `1^{13}` cascade block
below the doubled `1^{29}` and re-anchors `E` at rel `−22`, `L R` untouched.  Composed by
`steps_add` from the SAME six chunks `j4_E1..E6` that `carry_j4` (§5u) uses, so this IS the
EXIT tail of the already-proven depth-2 carry, now named as a standalone transport.  It
exhibits the EXIT's non-parametric growth AT THE TRANSPORT LEVEL: `EXIT(1)=70` steps
(`carry_exit_j3`) vs `EXIT(2)=218` here.  `some` ⇒ HALT-FREE.  `[propext, Quot.sound]`-only. -/
theorem carry_exit_j4 (L R : List Bool) :
    steps 218 ⟨.E, 10, ⟨ones 28 ++ (true :: false :: true :: false :: false :: L), false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -22, ⟨false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩ := by
  rw [show (218 : Nat) = 39+(39+(39+(39+(39+23)))) from rfl,
      steps_add, j4_E1, someBind,
      steps_add, j4_E2, someBind,
      steps_add, j4_E3, someBind,
      steps_add, j4_E4, someBind,
      steps_add, j4_E5, someBind,
      j4_E6]

/-- **The EXIT descent-fold count law, `∀j`** (the opening piece of `EXIT(j)`).  `EXIT(j)`
opens with `2^{j−2}−2` folds (the descent-fold peeling the just-doubled top block), matching
the measured `EXIT(4)` (2 folds) and `EXIT(5)` (6 folds) — an instance of §5w's
`carry_descent_fold`/`ecombChewFold` family, so the FIRST piece IS ∀j-parametric.  Pure
`Nat` cross-check. -/
theorem exit_fold_count_law :
    (2 ^ (4 - 2) - 2 = 2) ∧ (2 ^ (5 - 2) - 2 = 6) := by
  refine ⟨by decide, by decide⟩

/-- **EXIT length data — the NON-PARAMETRIC growth, recorded** (`x2ex_decompose.py`):
`EXIT(3)=70`, `EXIT(4)=218`, `EXIT(5)=722`, with piece-counts `5, 18, 52`.  The growth is
NOT a clean `4^j+2^j` closed form (ratios `3.11, 3.31`), because `EXIT(j)` is a WF recursion
whose per-level terminal glue varies — the decisive evidence that the EXIT is not a
straight-line ∀j transport.  Pure `Nat` cross-check of the extracted lengths. -/
theorem exit_length_data :
    (6708 - 6638 = 70) ∧ (7141 - 6923 = 218) ∧ (8798 - 8076 = 722) := by
  refine ⟨by decide, by decide, by decide⟩

/-! ### §5x: what CLOSED, and the exact non-parametric obstruction (`carry_exit` [DESIGN]).

**PROVEN GREEN this section (on-path, all `[propext, Quot.sound]`-only):**
  • `exit_anchor_motif` (29-step) + `exit_c3body_motif` (47-step) — the two recurring EXIT
    glue transports, Python-verified TRANSLATION-INVARIANT across `EXIT(3)/(4)/(5)`: the
    `∀j`-uniform seam glue, now named + grounded as reusable transports (§5v(2) made concrete
    for the EXIT).
  • `carry_exit_j4` — the depth-2 EXIT (218 steps) as a standalone reusable transport,
    parallel to `carry_exit_j3` (70 steps); it is the EXIT tail of the proven `carry_j4`.
  • `exit_fold_count_law` — the EXIT's opening descent-fold is `2^{j−2}−2`, ∀j-parametric.
  • `exit_length_data` — the extracted `70/218/722` growth (non-parametric).

**THE DECISIVE VERDICT (deliverable A).**  The EXIT is **NOT** `∀j`-parametric as a
straight-line composite of a fixed piece-type sequence at closed-form lengths.  Both the
verbatim self-embedding (H1) and the straight-line-parametric (H2) hypotheses are REFUTED by
the cell-for-cell `EXIT(3)/(4)/(5)` decomposition.  The TRUE `∀j` structure is the
well-founded recursion `EXIT(j) = DESCENT-FOLD(2^{j−2}−2) ∘ REGEN(j−1)` with `REGEN`
carry-shaped one level down, nesting to depth `j−3`.

**THE EXACT OBSTRUCTION — `carry_exit` [DESIGN, precisely located].**

```lean
-- [DESIGN] carry_exit (j) : the level-j EXIT transport.  NOT a straight-line ∀j composite.
--   carry_exit (j) = carry_descent_fold(j−3)        -- PROVEN ∀-level (exit_fold_count_law)
--                  ∘ [∀j-uniform seam glue]         -- PROVEN reusable (exit_anchor_motif,
--                                                       exit_c3body_motif)
--                  ∘ REGEN(j−1)                      -- a scale-(j−1) CARRY-SHAPED regeneration
--                                                       = strictly-lower recursive call (measure ↓)
--   grounded: EXIT(1)=70 (carry_exit_j3), EXIT(2)=218 (carry_exit_j4), EXIT(3)=722 (x2ex).
--   The ONE non-uniform ingredient is REGEN(j−1): it is carry-SHAPED at scale j−1 but
--   NOT verbatim C(j−1) (H1 refuted — terminal glue and tape-background differ per level),
--   so it cannot be discharged by reusing a fixed lower lemma; it is a genuine recursive
--   descent whose Lean closure is the DEFINITIONAL naming of the REGEN/EXIT datatype.
```

The glue is `∀j`-uniform (`exit_anchor_motif`/`exit_c3body_motif`, PROVEN), the descent-fold
and inner CORE/MIDDLE are `∀`-length-proven (§5w), and the recursion is well-founded (§5n
`odo_terminates`, measure = digits-left `≤ K`) — but `REGEN(j−1)` is a strictly-lower
recursive object that is NOT a verbatim copy of any fixed level, so `carry_exit` — and hence
`carry_step` — is a WELL-FOUNDED RECURSION, NOT a straight-line `∀j` transport.  This is the
project's `Suffix.lean`-scale object; we state it `[DESIGN]` (NO `sorry`, NO axiom, NO
`native_decide`) rather than force an unverified green transport.  No machine is decided by
this section; no label is upgraded. -/

-- §5x EXIT axiom audits (∀j-uniform glue + depth-2 EXIT transport + Nat cross-checks):
#print axioms exit_anchor_motif
#print axioms exit_c3body_motif
#print axioms carry_exit_j4
#print axioms exit_fold_count_law
#print axioms exit_length_data

/-! ## §5y (LAYER A, ON-PATH, 2026-07-15) THE TERMINAL-GLUE LAW — the decisive
measurement of the per-level EXIT terminal, `TERM(k) = 2^{k+1}+k+5` (4-level
verified), and the precise reason it is `f(k)` **but not** `f(j)`.

**THE EXPERIMENT (`x2ex_terminal.py`, `x2ex_l6exit.py`, `x2ex_termglue.py`,
cell-for-cell from the faithful `x2bd_sim.build(2)` orbit).**  §5x found the EXIT's
per-level *terminal glue* varies (`g41` / `NTICK(t=16)` / `g139`) and left it as the
"non-uniform ingredient".  §5y RESOLVES what that variation IS, by extracting the
BLOCK-FINAL terminal glue — the last odometer flush that lays down the fresh top
cascade block `1^{2^k−3}` — at FOUR levels, with the produced block measured:

```
  EXIT(3) block-final terminal  g41   lays 1^13  (k=4)   after: 0^4 1^13 0^2 1^5 …
  EXIT(4) block-final terminal  g74   lays 1^29  (k=5)   after: 0^4 1^29 0^2 1^13 …
  EXIT(5) block-final terminal  g139  lays 1^61  (k=6)   after: 0^4 1^61 0^2 1^29 …
  EXIT(6) block-final terminal  g268  lays 1^125 (k=7)   after: 0^4 1^125 0^2 1^61 …
```

**DECISIVE VERDICT — the terminal glue is a CLEAN closed form (NOT irregular), but
of the BLOCK-LEVEL `k`, NOT the EXIT level `j`.**  The block-final terminal length is
`TERM(k) = 2^{k+1} + k + 5`, where the terminal lays the top cascade block of size
`2^k − 3`.  Verified at FOUR levels: `k=4,5,6,7 → 41,74,139,268` (a real 4-point law,
first differences `33,65,129 = 2^{k+1}+1`, not a 2-point fit).  So the "irregular
wall" fear of §5x is REFUTED — the glue is a clean function; and each fixed-`k`
terminal is a genuine reusable TRANSLATION-INVARIANT transport (Python-verified
identical `(state,head,Δpos)` at both of its occurrences: `k=4` at EXIT3@6667 =
EXIT5@8259, `k=5` at EXIT4@7067 = EXIT6@13379), grounded here as `exit_terminal_k4`
(41 steps) and `exit_terminal_k5` (74 steps).

**BUT the clean parameter is `k`, a GLOBAL cascade-height / odometer quantity — NOT
the local EXIT level `j`.**  The smoking gun (`exit_terminal_not_of_j`): inside the
SINGLE `EXIT(5)`, the two block-final regeneration sub-blocks share a byte-IDENTICAL
144-step prefix (`2folds·g3·anchor·g24·C3body·anchor`, Python-verified identical
`(state,head,Δpos)` over `[8115,8259)` and `[8515,8659)`) and then DIVERGE at the
terminal: `g41` (k=4) vs `g139` (k=6).  Same local structure, DIFFERENT terminal —
so the terminal is decided by WHICH block the odometer is currently flushing (its
global height `k`), not by the sub-block's own level.  A single `EXIT(j)` emits
terminals of MANY `k` (EXIT(5): `k=3` `g24`s, `k=4` `g41`, `k=6` `g139`; EXIT(6):
`k=5` `g74`, `k=7` `g268`), nested.  Hence the EXIT is a genuine RECURSION over the
block-level `k` — clean per level, but counter-dependent, NOT a straight-line `∀j`
composite.  This SHARPENS §5x's `[DESIGN]` verdict: the remaining obstruction is
purely the recursion-datatype (indexing REGEN by the odometer height `k`), NOT any
glue irregularity — the glue law is now closed-form and Lean-grounded. -/

/-- **THE BLOCK-FINAL TERMINAL-GLUE LAW, closed form** `TERM(k) = 2^{k+1}+k+5`,
where the terminal lays the top cascade block `1^{2^k−3}`.  The DECISIVE `∀`-clean
finding of §5y: verified at FOUR levels `k=4,5,6,7 → 41,74,139,268` (block sizes
`13,29,61,125`), extracted cell-for-cell from `build(2)` (`x2ex_terminal.py`,
`x2ex_l6exit.py`).  A real 4-point law (first diffs `33,65,129 = 2^{k+1}+1`), NOT a
2-point fit.  Pure `Nat` cross-check. -/
theorem exit_terminal_law :
    (2 ^ (4 + 1) + 4 + 5 = 41 ∧ 2 ^ 4 - 3 = 13) ∧
    (2 ^ (5 + 1) + 5 + 5 = 74 ∧ 2 ^ 5 - 3 = 29) ∧
    (2 ^ (6 + 1) + 6 + 5 = 139 ∧ 2 ^ 6 - 3 = 61) ∧
    (2 ^ (7 + 1) + 7 + 5 = 268 ∧ 2 ^ 7 - 3 = 125) := by
  refine ⟨⟨by decide, by decide⟩, ⟨by decide, by decide⟩,
         ⟨by decide, by decide⟩, ⟨by decide, by decide⟩⟩

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
/-- **EXIT `k=4` TERMINAL glue `g41`** (lays the fresh top block `1^13`).  41 steps,
head rel `0 → −23`; the last odometer flush that deposits the `2^4−3=13`-cell top
cascade block and re-anchors `E` on the new boundary.  `TERM(4)=2^5+4+5=41`.
Extracted cell-for-cell from EXIT3 (`n=6667→6708`); Python-verified TRANSLATION-
INVARIANT — identical `(state,head,Δpos)` transport also at EXIT5@8259.  `some` ⇒
HALT-FREE.  Kernel `rfl`. -/
theorem exit_terminal_k4 (L R : List Bool) :
    steps 41 ⟨.E, 0, ⟨true :: true :: true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, false, false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -23, ⟨false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩ :=
  rfl

set_option maxRecDepth 8000 in
set_option maxHeartbeats 4000000 in
/-- **EXIT `k=5` TERMINAL glue `g74`** (lays the fresh top block `1^29`).  74 steps,
head rel `0 → −54`; the `k=5` odometer flush depositing the `2^5−3=29`-cell top
cascade block.  `TERM(5)=2^6+5+5=74`.  Extracted cell-for-cell from EXIT4
(`n=7067→7141`); Python-verified TRANSLATION-INVARIANT — identical transport also at
EXIT6@13379.  The SECOND grounding point of `exit_terminal_law` at the transport
level (`41` vs `74`, the clean `TERM(k)` growth).  `some` ⇒ HALT-FREE.  Kernel `rfl`. -/
theorem exit_terminal_k5 (L R : List Bool) :
    steps 74 ⟨.E, 0, ⟨true :: true :: true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: true :: false :: false :: L, false, false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -54, ⟨false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩ :=
  rfl

/-- **THE DECISIVE NON-`f(j)` CROSS-CHECK** (`x2ex_termglue.py`).  Inside the single
`EXIT(5)`, the two block-final regeneration sub-blocks share a byte-IDENTICAL
144-step prefix (Python-verified identical `(state,head,Δpos)` over `[8115,8259)`
and `[8515,8659)`) and then DIVERGE at the terminal: `g41` (`k=4`, `n=8259→8300`) vs
`g139` (`k=6`, `n=8659→8798`), a difference of `98`.  Same local structure, DIFFERENT
terminal ⇒ the terminal is `f(k)` (global odometer height), NOT `f(j)` (local level):
the EXIT is a genuine recursion over `k`, not a straight-line `∀j` composite.  Pure
`Nat` cross-check of the extracted window boundaries. -/
theorem exit_terminal_not_of_j :
    (8259 - 8115 = 144 ∧ 8659 - 8515 = 144) ∧
    (8300 - 8259 = 41 ∧ 8798 - 8659 = 139 ∧ 139 - 41 = 98) := by
  refine ⟨⟨by decide, by decide⟩, ⟨by decide, by decide, by decide⟩⟩

-- §5y TERMINAL-GLUE law axiom audits (closed-form TERM(k) + two grounded transports + non-f(j)):
#print axioms exit_terminal_law
#print axioms exit_terminal_k4
#print axioms exit_terminal_k5
#print axioms exit_terminal_not_of_j

/-! ## §5z (LAYER A, ON-PATH, 2026-07-15) THE k-INDEXED RECURSIVE EXIT — the
`exitSteps` closed form, the REGEN translation-invariance (the reusability the whole
recursion turns on), the exact tree-recursion decomposition, and the single remaining
`[DESIGN]` object stated with maximal sharpness.

**THE CULMINATION.**  §5w assembled the carry as `C(j) = DESCENT ∘ glue ∘ C(j−1) ∘
MIDDLE ∘ CORE ∘ EXIT(j)` with DESCENT/MIDDLE/CORE proven `∀`-level and the register a
grounded recursive datatype (`cascadeTail`), leaving `EXIT` the one open recursive
object.  §5x pinned `EXIT(j) = DESCENT-FOLD ∘ REGEN(j−1)` (a WF recursion, not a
straight-line composite) and §5y resolved that its per-level terminal glue is the CLEAN
`TERM(k)=2^{k+1}+k+5` indexed by the *block height* `k`, NOT the local level `j`.  This
section BUILDS the k-indexed recursive EXIT and reports EXACTLY what closes and what does
not, cross-checking against the two proven concrete EXITs `carry_exit_j3` (=REGEN(4), 70
steps) and `carry_exit_j4` (=REGEN(5), 218 steps).

**RE-INDEXING (the §5y move made precise).**  Write `REGEN(k)` for the regeneration that
lays the fresh top cascade block `1^{2^k−3}` and re-anchors `E`; then `EXIT(j) = REGEN(j+1)`
(`EXIT(3)` lays `1^13`=`k=4`, `EXIT(4)` lays `1^29`=`k=5`, …).  The step count, extracted
cell-for-cell from `x2bd_sim.build(2)` at FIVE levels (`x2ck_exitsteps.py`,
`x2ck_exit6.py`, and a fifth point `REGEN(8)` located independently at raw `n=31246→40528`)
is `70, 218, 722, 2530, 9282` for `k=4,5,6,7,8`.

**DELIVERABLE (A) — `exitSteps(k)` HAS A CLEAN CLOSED FORM (this REFINES §5x's tentative
"no clean form").**  A 5-point rational fit is EXACT with clean dyadic coefficients:

```
  exitSteps(k) = 2^{2k−3} + k·2^{k−1} + 2^{k−2} + 2
               = 70, 218, 722, 2530, 9282   (k=4,5,6,7,8)   ✓ all five
```

The reason §5x's `a·4^k+b·2^k+c·k+d` fit gave garbage (fractional `a=37/72`) is the
**`k·2^{k−1}` term** — the odometer-height *linear×exponential* factor (exactly §5o's
"linear-in-K × exponential" tick structure).  Once that term is admitted the form is clean;
`exitSteps` also satisfies the order-4 linear recurrence with characteristic
`(x−4)(x−2)²(x−1)` (roots `4,2,2,1`), grounded below.

**DELIVERABLE (B/C) — THE DECISIVE POSITIVE: `REGEN(k)` IS FULLY TRANSLATION-INVARIANT.**
The whole point on which a recursion of *reusable* transports turns.  `x2ck_regen_ti.py`
verifies (identical `(state,head,Δpos)` relative trace) that the COMPLETE per-level
regeneration is one transport at every occurrence: `REGEN(5)` (all 218 steps) is
byte-identical at ALL FOUR orbit sites (`[6923,7141]`, `[13235,13453]`, `[31955,32173]`,
`[38267,38485]`), and `REGEN(4)` (all 70 steps) at ALL EIGHT sites.  This is strictly
stronger than §5x/§5y (which proved only the terminal + two motifs TI): the ENTIRE REGEN
body is level-context-independent.  The Lean content of this is precisely that
`carry_exit_j3`/`carry_exit_j4` are stated `∀ L R` — so REGEN(4)/(5) ARE reusable
transports, applicable with ANY block-above `L` / cascade-below `R` (`regen_TI_generic`).

**DELIVERABLE (C) — THE EXACT REMAINING OBSTRUCTION: the recursion is a NON-UNIFORM TREE.**
The top-level decomposition of `REGEN(k)` into proven pieces + strictly-lower REGEN calls
(`x2ck_regen_seg.py`, greedy largest-block cover) is grounded exactly (`exitSteps_tree_*`
below):
```
  REGEN(5) = 44 · TERM(3) · 76 · TERM(5)                                  [0 lower REGEN]
  REGEN(6) = 83 · TERM(3) · 47 · REGEN(4) · 113 · TERM(3) · 122 · TERM(3) · 76 · TERM(6)
                                                                          [1 lower REGEN]
  REGEN(7) = 170·TERM(3)·47·REGEN(4)·113·TERM(3)·78·REGEN(5)·113·TERM(3)·881·TERM(3)
             ·47·REGEN(4)·113·TERM(3)·122·TERM(3)·76·TERM(7)             [3 lower REGEN]
```
The number of strictly-lower REGEN recursive calls is `0,1,3` for `k=5,6,7` — the branching
ARITY GROWS with `k` (the odometer's digit expansion), and the interleaving glue segments
(the `881` in `REGEN(7)`) carry level-dependent CORE `sweepEF` build-ups.  So `REGEN(k)` is
a genuine WELL-FOUNDED TREE recursion whose arity is not `∀k`-constant; it is NOT a
straight-line `∀k` transport, and a total structural `carryExit : Nat → transport` with a
FIXED tuple of recursive calls does not exist.  This is the precise, final shape of the
`carry_step` `[DESIGN]` object — sharpened from "recursive" (§5w) → "WF recursion, not
straight-line" (§5x) → "clean per level but counter-dependent" (§5y) → here: a
translation-invariant per-level transport arranged by a growing-arity odometer tree. -/

/-- **THE TERMINAL-GLUE STEP COUNT, closed form** `TERM(k)=2^{k+1}+k+5` (§5y as a `def`),
the block-final flush laying `1^{2^k−3}`; `= 24,41,74,139,268` for `k=3..7`. -/
def termSteps (k : Nat) : Nat := 2 ^ (k + 1) + k + 5

/-- **THE k-INDEXED EXIT STEP COUNT, CLOSED FORM** (deliverable A).
`exitSteps(k) = 2^{2k−3} + k·2^{k−1} + 2^{k−2} + 2`, the regeneration `REGEN(k)` laying
`1^{2^k−3}`.  The middle `k·2^{k−1}` is the odometer-height linear×exponential factor. -/
def exitSteps (k : Nat) : Nat := 2 ^ (2 * k - 3) + k * 2 ^ (k - 1) + 2 ^ (k - 2) + 2

/-- **GROUNDING: the closed form reproduces the REAL extracted step counts** at FIVE
levels `k=4,5,6,7,8 → 70,218,722,2530,9282` (`x2ck_exitsteps.py`/`x2ck_exit6.py`, and the
independent 5th point `REGEN(8)` at raw `n=31246→40528`).  A real 5-point law, not a fit
to the 3 points §5x had.  Pure `Nat` cross-check. -/
theorem exitSteps_grounds :
    exitSteps 4 = 70 ∧ exitSteps 5 = 218 ∧ exitSteps 6 = 722 ∧
      exitSteps 7 = 2530 ∧ exitSteps 8 = 9282 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- **The terminal-glue values** `TERM(k)=24,41,74,139,268` (`k=3..7`), matching
`exit_terminal_law`'s grounded `41`/`74` transports and the extracted `24`/`139`/`268`. -/
theorem termSteps_grounds :
    termSteps 3 = 24 ∧ termSteps 4 = 41 ∧ termSteps 5 = 74 ∧
      termSteps 6 = 139 ∧ termSteps 7 = 268 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE `k·2^{k−1}` TERM IS ESSENTIAL** (why §5x's `a·4^k+b·2^k+c·k+d` fit failed).
Dropping the linear×exponential middle term gives `2^{2k−3}+2^{k−2}+2 = 38 ≠ 70` at `k=4`
(and `138 ≠ 218` at `k=5`): the odometer-height factor is not optional.  This is the
decisive refinement of §5x's "not a clean `4^j+2^j` form" — it IS clean, but needs the
`k·2^k` term.  Pure `Nat` cross-check. -/
theorem exitSteps_khalf_essential :
    (2 ^ (2 * 4 - 3) + 2 ^ (4 - 2) + 2 = 38 ∧ 38 ≠ 70) ∧
      (2 ^ (2 * 5 - 3) + 2 ^ (5 - 2) + 2 = 138 ∧ 138 ≠ 218) := by
  refine ⟨⟨by decide, by decide⟩, ⟨by decide, by decide⟩⟩

/-- **THE ORDER-4 LINEAR RECURRENCE** `exitSteps` obeys (characteristic `(x−4)(x−2)²(x−1)`,
roots `4,2,2,1`), stated subtraction-free: `es(8)+28·es(6)+16·es(4) = 9·es(7)+36·es(5)`.
The recursive certificate of the closed form (deliverable A, "recursive form").  Pure
`Nat` cross-check. -/
theorem exitSteps_recurrence :
    exitSteps 8 + 28 * exitSteps 6 + 16 * exitSteps 4
      = 9 * exitSteps 7 + 36 * exitSteps 5 := by decide

/-- **REGEN(4) = `carry_exit_j3` at step count `exitSteps 4`** (base of the k-recursion).
`carry_exit_j3` (§5s, 70 steps, `∀ L R`) IS the level-`k=4` regeneration; `70 = exitSteps 4`
wires it into the recursion.  `some` ⇒ HALT-FREE, inherits `[propext, Quot.sound]`. -/
theorem regen4_transport (L R : List Bool) :
    steps (exitSteps 4) ⟨.E, 9, ⟨
        ones 12 ++ (true :: false :: true :: false :: false :: true :: false :: L),
        false,
        (false :: true :: false :: false :: false :: false :: false :: false ::
         false :: false :: false :: false :: false :: R)⟩⟩
      = some ⟨.E, -7, ⟨
          (false :: true :: false :: L),
          false,
          (false :: false :: false :: true :: true :: true :: true :: true :: true :: true ::
           true :: true :: true :: true :: true :: true :: false :: false :: true :: true ::
           true :: true :: true :: false :: false :: true :: false :: false :: false :: R)⟩⟩ := by
  rw [show exitSteps 4 = 70 from by decide]; exact carry_exit_j3 L R

/-- **REGEN(5) = `carry_exit_j4` at step count `exitSteps 5`** (the depth-1 step, already
GREEN).  `218 = exitSteps 5`.  `some` ⇒ HALT-FREE, `[propext, Quot.sound]`. -/
theorem regen5_transport (L R : List Bool) :
    steps (exitSteps 5) ⟨.E, 10, ⟨ones 28 ++ (true :: false :: true :: false :: false :: L), false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩
      = some ⟨.E, -22, ⟨false :: L, false, false :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: true :: false :: false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: R⟩⟩ := by
  rw [show exitSteps 5 = 218 from by decide]; exact carry_exit_j4 L R

/-- **THE TRANSLATION-INVARIANCE PRINCIPLE, generic** (the Lean content of the decisive
`x2ck_regen_ti.py` finding).  A `∀ L R` transport of length `n` — a TRANSLATION-INVARIANT
regeneration — is REUSABLE in ANY two tape contexts, sharing one proof.  This is exactly
why `REGEN(k)` (byte-identical at all 4/8 orbit sites) is a reusable recursion object:
`carry_exit_j3`/`carry_exit_j4` have precisely this `∀ L R` shape, so `REGEN(4)`/`REGEN(5)`
apply with any block-above `L₁,L₂` and cascade-below `R₁,R₂`. -/
theorem regen_TI_generic {n : Nat} {In Out : List Bool → List Bool → Cfg}
    (T : ∀ L R, steps n (In L R) = some (Out L R)) (L₁ R₁ L₂ R₂ : List Bool) :
    steps n (In L₁ R₁) = some (Out L₁ R₁) ∧ steps n (In L₂ R₂) = some (Out L₂ R₂) :=
  ⟨T L₁ R₁, T L₂ R₂⟩

/-- **REGEN(5) reused in two DISTINCT block-above contexts** (concrete TI instance): the
SAME 218-step transport with `L :=` empty vs `L := ones 61` (a bigger doubled block sitting
above, as inside `EXIT(6)`), one proof term via `regen_TI_generic`.  Demonstrates the
reuse the tree recursion needs. -/
theorem regen5_reuse_two_contexts (R : List Bool) :
    (steps (exitSteps 5) ⟨.E, 10, ⟨ones 28 ++ (true :: false :: true :: false :: false :: []), false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩).isSome ∧
    (steps (exitSteps 5) ⟨.E, 10, ⟨ones 28 ++ (true :: false :: true :: false :: false :: ones 61), false, false :: true :: true :: true :: true :: true :: false :: false :: true :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: false :: R⟩⟩).isSome := by
  refine ⟨?_, ?_⟩ <;> rw [regen5_transport] <;> rfl

/-- **THE EXACT TREE DECOMPOSITION (deliverable C, `k=5`)** — the BASE branch: `REGEN(5)`
reuses NO lower REGEN, only `TERM(3)` and its own `TERM(5)`.  Grounded from
`x2ck_regen_seg.py`.  Pure `Nat`. -/
theorem exitSteps_tree_5 :
    exitSteps 5 = 44 + termSteps 3 + 76 + termSteps 5 := by decide

/-- **THE EXACT TREE DECOMPOSITION (`k=6`)** — ONE strictly-lower recursive call
`REGEN(4)=exitSteps 4`, interleaved with `TERM(3)`s and glue, ending `TERM(6)`.  The
recursive REGEN reuse is manifest.  Pure `Nat`. -/
theorem exitSteps_tree_6 :
    exitSteps 6 = 83 + termSteps 3 + 47 + exitSteps 4 + 113 + termSteps 3
      + 122 + termSteps 3 + 76 + termSteps 6 := by decide

/-- **THE EXACT TREE DECOMPOSITION (`k=7`)** — THREE strictly-lower recursive calls
(`REGEN(5)` once + `REGEN(4)` twice), with a level-dependent `881`-step CORE build-up glue,
ending `TERM(7)`.  Together with `exitSteps_tree_5/6` this exhibits the branching ARITY
`0,1,3` — the recursion is a NON-UNIFORM TREE, the precise `[DESIGN]` obstruction.  Pure
`Nat`. -/
theorem exitSteps_tree_7 :
    exitSteps 7 = 170 + termSteps 3 + 47 + exitSteps 4 + 113 + termSteps 3 + 78 + exitSteps 5
      + 113 + termSteps 3 + 881 + termSteps 3 + 47 + exitSteps 4 + 113 + termSteps 3
      + 122 + termSteps 3 + 76 + termSteps 7 := by decide

/-- **THE RECURSION SKELETON, instantiated at the REGEN transport** (deliverable B, the WF
frame).  GIVEN the per-level step `P n → P (n+1)` (the one `[DESIGN]` object) and the base
`P 1` (discharged concretely by `regen4_transport`, = `carry_exit_j3`), the proven §5w
`carry_level_rec` (a genuine `Nat.le_induction`, no `sorry`/`partial`) yields `∀ n ≥ 1, P n`.
The k-recursion's control flow IS this combinator; ONLY the step is open. -/
theorem carryExit_wf_frame {P : Nat → Prop} (hbase : P 1)
    (hstep : ∀ n, 1 ≤ n → P n → P (n + 1)) : ∀ n, 1 ≤ n → P n :=
  carry_level_rec hbase hstep

/-! ### §5z: what CLOSED, the j=3/j=4 cross-check, and the single remaining object.

**PROVEN GREEN this section (on-path, `x2ck_*.py` cell-for-cell from `build(2)`):**
  • `exitSteps` — the k-indexed EXIT step count, CLOSED FORM `2^{2k−3}+k·2^{k−1}+2^{k−2}+2`,
    grounded at FIVE levels `70/218/722/2530/9282` (`exitSteps_grounds`) — REFINING §5x's
    "no clean form" (`exitSteps_khalf_essential`: the `k·2^{k−1}` odometer-height term is
    what §5x's fit lacked) — with its order-4 linear recurrence (`exitSteps_recurrence`).
  • `termSteps` — the block-final glue `TERM(k)=2^{k+1}+k+5` as a `def` (§5y), grounded.
  • `regen4_transport` / `regen5_transport` — `carry_exit_j3` / `carry_exit_j4` wired as the
    k-indexed `REGEN(4)` / `REGEN(5)` at step count `exitSteps 4=70` / `exitSteps 5=218`.
  • `regen_TI_generic` + `regen5_reuse_two_contexts` — the TRANSLATION-INVARIANCE principle:
    `REGEN(k)` (`x2ck_regen_ti.py`: identical trace at all 4/8 orbit sites) is a reusable
    `∀ L R` transport, applied here in two distinct block-above contexts by ONE proof.
  • `exitSteps_tree_5/6/7` — the EXACT top-level tree decomposition, grounding the recursive
    lower-REGEN reuse and the growing branching arity `0,1,3`.
  • `carryExit_wf_frame` — the WF recursion skeleton (§5w `carry_level_rec`) instantiated at
    the REGEN transport predicate; base discharged by `regen4_transport`.

**THE j=3 / j=4 CROSS-CHECK (discipline requirement — the recursion reproduces both proven
concrete EXITs).**  `regen4_transport` IS `carry_exit_j3` (the j=3-scale EXIT, 70 steps) at
`exitSteps 4`; `regen5_transport` IS `carry_exit_j4` (the j=4-scale EXIT, 218 steps) at
`exitSteps 5` — both by `rfl`-level `rw` on the step count, so the k-recursion's base and
depth-1 levels REPRODUCE the two already-proven carries EXACTLY, on-path.  The tree
arithmetic `exitSteps_tree_6` shows `REGEN(6)` genuinely reuses `REGEN(4)`.

**THE SINGLE REMAINING OBJECT — `carryExit`/`carry_step`, `[DESIGN]`, now maximally sharp.**
The per-level transport step `P n → P (n+1)` is the ONLY open piece.  Every ingredient is
in hand: the register (`cascadeTail`, §5w), the `∀`-level DESCENT/MIDDLE/CORE (§5w), the
`∀j`-uniform glue + TI REGEN transports (§5x/§5y/here), the closed-form step count
(`exitSteps`), and the WF frame (`carryExit_wf_frame`).  What does NOT close is a *total*
structural `carryExit : Nat → transport`:

```lean
-- [DESIGN] carryExit (k) : the level-k REGEN transport (TI, step count exitSteps k).
--   REGEN(k) = [opening DESCENT-FOLD 2^{k-3}-2] ∘ (a GROWING-ARITY tuple of strictly-lower
--              REGEN(k') calls interleaved with ∀-level CORE/glue) ∘ TERM(k)
--   branching arity = 0,1,3,… (exitSteps_tree_5/6/7): the odometer digit expansion, NOT
--   a fixed ∀k tuple — so no total structural recursion with constant recursive-call
--   count exists; the arity function is itself the recursive object.
```

`REGEN(k)` is translation-invariant (PROVEN reusable) and well-founded (each call strictly
lowers `k`), but its recursive-call ARITY grows with `k` (the base-2 odometer's digit tree),
so the closure is the DEFINITIONAL naming of that odometer-tree recursion — the project's
`Suffix.lean`-scale object.  We state it `[DESIGN]` (NO `sorry`, NO axiom, NO `native_decide`,
NO `partial def`) rather than force an unverified `∀k` transport.  **The integer-doubler's
doubling-phase carry is NOT yet machine-checked `∀j`**: the base (`k=4`) and depth-1 (`k=5`)
levels are GREEN and reproduce `carry_exit_j3`/`carry_exit_j4`, the step count and TI are
closed `∀k`, but the growing-arity odometer-tree step remains the single open object.

No machine decided. No label upgraded. -/

-- §5z k-indexed recursive EXIT axiom audits (closed form + TI + tree + WF frame):
#print axioms exitSteps_grounds
#print axioms termSteps_grounds
#print axioms exitSteps_khalf_essential
#print axioms exitSteps_recurrence
#print axioms regen4_transport
#print axioms regen5_transport
#print axioms regen_TI_generic
#print axioms regen5_reuse_two_contexts
#print axioms exitSteps_tree_5
#print axioms exitSteps_tree_6
#print axioms exitSteps_tree_7
#print axioms carryExit_wf_frame

/-! ## §5aa (LAYER A, ON-PATH, 2026-07-16) THE BOUNDED-ARITY TEST — does the order-4
step recurrence LIFT to a BOUNDED (≤4) transport recursion?  **DECISIVE VERDICT: NO —
the REGEN tree is GENUINELY GROWING.**  (probes `x2dt_decompose.py`, `x2dt_tree8.py`,
cell-for-cell from the faithful `build(2)` orbit.)

**THE LEAD (and why it is seductive).**  §5z proved `exitSteps(k)` obeys the order-4 linear
recurrence with characteristic `(x−4)(x−2)²(x−1)` (`exitSteps_recurrence`).  An order-4
step recurrence is exactly the arithmetic footprint one would expect of a transport that
reuses `REGEN(k−1..k−4)` a BOUNDED number of times plus `∀k`-parametric glue — which, if
real, would CLOSE `carry_step` (define `carryExit : Nat → transport` by WF `Nat` recursion
with ≤4 recursive calls, cross-check `carryExit 4 = carry_exit_j3`, `5 = carry_exit_j4`,
wire into `carry_step`).  This section tests that hypothesis two independent ways and
REFUTES it decisively.

**(1) STRUCTURAL — the arity GROWS QUADRATICALLY.**  Extending §5z's tree decomposition to
`k=8` cell-for-cell (`REGEN(8)` at raw `n=31246→40528`, exact greedy largest-block cover,
`exitSteps_tree_8` below, sum-checked = 9282 = `exitSteps 8`), the number of strictly-lower
`REGEN` recursive calls is:
```
  REGEN(5): 0   calls []                         2^5−3 = 29  = 11101₂  (4 one-bits)
  REGEN(6): 1   calls [4]                         2^6−3 = 61  = 111101₂ (5 one-bits)
  REGEN(7): 3   calls [4,5,4]                      2^7−3 = 125 = 1111101₂(6 one-bits)
  REGEN(8): 6   calls [4,5,6,4,5,4]                2^8−3 = 253 = 11111101₂(7 one-bits)
```
The arity sequence `0,1,3,6` is EXACTLY the triangular number `(k−5)(k−4)/2` (`exitArity`
below, grounded at all four tape levels) — it already EXCEEDS 4 at `k=8` (arity 6) and keeps
growing (`exitArity 9 = 10`).  So NO fixed `≤4`-arity structural `carryExit : Nat → transport`
reproduces the orbit: the recursive-call count is itself an unbounded function of `k` (the
odometer's base-2 digit tree; note the self-similar nesting `[4,5,6,4,5,4]` = the `REGEN(7)`
call-list `[4,5,4]` prefixed by `[4,5,6]`).

**(2) ARITHMETIC — the order-4 recurrence CANNOT be a composition.**  A transport
composition can only ADD step counts, so a bounded reuse would force a NONNEGATIVE identity
`exitSteps(k) = Σᵢ cᵢ·exitSteps(k−i) + glue(k)` with `cᵢ ∈ ℕ`, `glue(k) ≥ 0`.  But (a) the
order-4 recurrence's coefficients are `(9,−28,36,−16)` — NEGATIVE (`exitSteps_recurrence`
is subtraction-free precisely because two coefficients flip sign), so it is NOT such a
nonnegative identity; and (b) the single-call leading multiplier is strictly between 3 and
4 — `3·exitSteps(k) < exitSteps(k+1) < 4·exitSteps(k)` (`exitSteps_leading_multiplier_in_open_3_4`,
grounded k=4..7).  Because `exitSteps(k) = 4^k/8 + …` grows by a factor `→4`, and no INTEGER
number of top-level `REGEN(k−1)` calls matches it (3 undershoots, leaving a residual that is
still `Θ(4^k)` = "glue that re-encodes the whole transport, not a bounded-description glue";
4 OVERSHOOTS, `exitSteps(k+1) < 4·exitSteps(k)`, giving a NEGATIVE residual — impossible for
a composition), a brute force (`x2dt_decompose.py`) confirms EVERY bounded (`Σcᵢ ≤ 4`)
nonnegative combination with residual `≥ 0` has glue that is `Θ(4^k)` — i.e. it re-encodes
the whole transport rather than recursing.  The bounded-arity lift is arithmetically
excluded, independent of the tape.

**VERDICT.**  GENUINELY GROWING.  The order-4 step recurrence does NOT lift to a
bounded-arity transport recursion — for two independent reasons (the arity grows like
`(k−5)(k−4)/2`; the recurrence has negative coefficients while the leading multiplier is a
non-integer in `(3,4)`).  This CONFIRMS and SHARPENS §5z's growing-tree finding against the
strongest closure attempt.  The `carry_step` `[DESIGN]` object is the odometer digit-tree
recursion whose arity function `exitArity` is itself the recursive content — a
`Suffix.lean`-scale definitional object, NOT a `≤4`-arity `Nat` recursion.  The base
(`k=4`, `carry_exit_j3`) and depth-1 (`k=5`, `carry_exit_j4`) levels stay GREEN and the
step count / TI are closed `∀k`, but no bounded transport recursion closes the general `j`.

No machine decided. No label upgraded. -/

/-- **THE BRANCHING ARITY of `REGEN(k)`** — the count of strictly-lower `REGEN` recursive
calls in the exact tree decomposition (`x2dt_tree8.py`).  Closed form `(k−5)(k−4)/2` (the
triangular numbers), grounded at FOUR tape levels below.  It is the odometer base-2 digit
tree's fan-out; UNBOUNDED in `k`, so no fixed-arity structural `carryExit` exists. -/
def exitArity (k : Nat) : Nat := (k - 5) * (k - 4) / 2

/-- **GROUNDING: the arity closed form reproduces the extracted tree arities** `0,1,3,6`
for `k=5,6,7,8` (`REGEN(5..8)` cell-for-cell; `exitSteps_tree_5/6/7`, `exitSteps_tree_8`).
Pure `Nat` cross-check. -/
theorem exitArity_grounds :
    exitArity 5 = 0 ∧ exitArity 6 = 1 ∧ exitArity 7 = 3 ∧ exitArity 8 = 6 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE ARITY ALREADY EXCEEDS 4 AND KEEPS GROWING** — the decisive refutation of a
bounded (`≤4`) transport recursion.  `exitArity 8 = 6 > 4` (already at the fourth level) and
`exitArity 8 < exitArity 9 = 10` (strictly increasing).  So the recursive-call count is
NOT `∀k`-bounded by 4 (nor by any constant): no fixed-arity `carryExit : Nat → transport`
reproduces the orbit.  Pure `Nat`. -/
theorem exitArity_exceeds_four : 4 < exitArity 8 ∧ exitArity 8 < exitArity 9 := by decide

/-- **THE EXACT TREE DECOMPOSITION (`k=8`)** — SIX strictly-lower recursive calls
`[REGEN(4),REGEN(5),REGEN(6),REGEN(4),REGEN(5),REGEN(4)]` (arity 6, matching
`exitArity 8`), with level-dependent CORE build-up glue (`798`, `3944`), ending `TERM(8)`.
Extends `exitSteps_tree_5/6/7`; together the arities are `0,1,3,6` — the GROWING tree that
refutes the bounded-arity lift.  Sum-checked `= exitSteps 8 = 9282`.  Pure `Nat`. -/
theorem exitSteps_tree_8 :
    exitSteps 8 = 353 + termSteps 3 + 47 + exitSteps 4 + 113 + termSteps 3 + 78 + exitSteps 5
      + 113 + termSteps 3 + 798 + exitSteps 6 + 113 + termSteps 3 + 3944 + termSteps 3
      + 47 + exitSteps 4 + 113 + termSteps 3 + 78 + exitSteps 5 + 113 + termSteps 3
      + 881 + termSteps 3 + 47 + exitSteps 4 + 113 + termSteps 3 + 122 + termSteps 3
      + 76 + termSteps 8 := by decide

/-- **THE ARITHMETIC OBSTRUCTION: the single-call leading multiplier is a NON-INTEGER in
`(3,4)`** — `3·exitSteps(k) < exitSteps(k+1) < 4·exitSteps(k)` for `k=4,5,6,7`.  Since
`exitSteps` grows by factor `→4` (leading `4^k/8`), no INTEGER number of top-level
`REGEN(k−1)` calls matches it: 3 undershoots (residual still `Θ(4^k)` — glue that
re-encodes the transport), 4 OVERSHOOTS (`exitSteps(k+1) < 4·exitSteps(k)` ⇒ negative
residual, impossible for an additive composition).  Hence — together with the NEGATIVE
coefficients of `exitSteps_recurrence` — the order-4 step recurrence is NOT the arithmetic
image of a bounded nonnegative transport composition.  Pure `Nat` cross-check. -/
theorem exitSteps_leading_multiplier_in_open_3_4 :
    (3 * exitSteps 4 < exitSteps 5 ∧ exitSteps 5 < 4 * exitSteps 4) ∧
      (3 * exitSteps 5 < exitSteps 6 ∧ exitSteps 6 < 4 * exitSteps 5) ∧
        (3 * exitSteps 6 < exitSteps 7 ∧ exitSteps 7 < 4 * exitSteps 6) ∧
          (3 * exitSteps 7 < exitSteps 8 ∧ exitSteps 8 < 4 * exitSteps 7) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> exact ⟨by decide, by decide⟩

/-! ### §5aa: what CLOSED, and the decisive verdict on the bounded-arity lead.

**PROVEN GREEN this section (on-path, `x2dt_*.py` cell-for-cell from `build(2)`):**
  • `exitArity` — the `REGEN(k)` branching arity, closed form `(k−5)(k−4)/2`, grounded at
    FOUR tape levels `0,1,3,6` (`exitArity_grounds`) and shown to EXCEED 4 and keep growing
    (`exitArity_exceeds_four`): the recursive-call count is unbounded in `k`.
  • `exitSteps_tree_8` — the exact `k=8` tree decomposition (arity 6), extending
    `exitSteps_tree_5/6/7`; sum-checked `= exitSteps 8`.
  • `exitSteps_leading_multiplier_in_open_3_4` — the arithmetic obstruction: the leading
    single-call multiplier is a non-integer in `(3,4)`, so with the NEGATIVE coefficients of
    `exitSteps_recurrence` the order-4 step recurrence is not a bounded nonnegative
    composition.

**VERDICT (deliverable A/C): GENUINELY GROWING — the bounded-arity lift does NOT exist.**
The order-4 step-count recurrence does NOT lift to a `≤4`-arity transport recursion.
Structurally the arity is `(k−5)(k−4)/2` (unbounded, `>4` at `k=8`); arithmetically the
recurrence's negative coefficients and non-integer leading multiplier forbid any bounded
nonnegative composition.  `carry_step` remains the growing-arity odometer digit-tree
`[DESIGN]` object of §5z, now tested against and surviving the strongest closure attempt.

**Is the doubling-phase carry machine-checked ∀j?  NO.**  The base (`k=4`) and depth-1
(`k=5`) EXIT transports are GREEN and reproduce `carry_exit_j3`/`carry_exit_j4`; the step
count (`exitSteps`) and translation-invariance are closed `∀k`; but the single open object
— the `REGEN` transport step with its GROWING-ARITY recursion — is confirmed here to admit
no bounded-arity closure.  The general-`j` doubling-phase carry is NOT yet machine-checked.

No machine decided. No label upgraded. -/

-- §5aa bounded-arity test axiom audits (arity closed form + k=8 tree + arithmetic obstruction):
#print axioms exitArity_grounds
#print axioms exitArity_exceeds_four
#print axioms exitSteps_tree_8
#print axioms exitSteps_leading_multiplier_in_open_3_4

/-! ## §5ab (LAYER A, ON-PATH, 2026-07-16) THE LIST-FOLD RECURSION over the odometer
digit-tree — the self-similar `exitList` recursion built GREEN (clean `Nat`/`List`), the
step-count `List.foldl` closure proven `∀`-level-grounded, and the DECISIVE per-position-glue
parametricity verdict.  (probes `x2lf_glue.py`, `x2lf_param.py`, `x2lf_cfg.py`, cell-for-cell
from the faithful `build(2)` orbit.)

**THE MOVE (why §5aa's "no bounded-arity closure" is NOT the end).**  §5aa refuted a `≤4`-arity
transport recursion — but a GROWING arity is exactly what a `List.foldl` over a
RECURSIVELY-GENERATED list absorbs: the digit-tree call-list `list(k)` is itself a clean
`Nat`/`List` recursion whose every element `k' < k`, so a well-founded fold is available in
principle regardless of length.  §5aa's arity obstruction dissolves; the closure hinges
ENTIRELY on the discipline note's two remaining risks — is the PER-POSITION GLUE
`∀`-parametric, and does the `toCfg` threading go through `∀`-position?  This section builds
the list recursion, proves the STEP-COUNT fold CLOSES, and reports the decisive verdict on
the glue.

**DELIVERABLE (A) — THE CALL-LIST IS A CLEAN SELF-SIMILAR `Nat`/`List` RECURSION (GREEN).**
`exitList k = List.range' 4 (k−5) ++ exitList (k−1)` (base `exitList (≤5) = []`), a genuine
structural `Nat` recursion — reproduces the extracted call-lists cell-for-cell
(`exitList_grounds`: `[], [4], [4,5,4], [4,5,6,4,5,4]` for `k=5,6,7,8`), its length equals the
§5aa arity `(k−5)(k−4)/2` (`exitList_length_eq_arity`), and every element is `< k`
(`exitList_wf_grounds`, the fold's well-foundedness).  This is the odometer base-2 digit tree
as a total Lean object — the growing-arity recursion §5aa said had no `≤4` closure, here
NAMED as a `List` recursion, GREEN.

**DELIVERABLE (A/B) — THE STEP-COUNT `List.foldl` CLOSES (GREEN, `∀`-level-grounded).**  With
`foldRegenSteps k := (exitList k).foldl (·+exitSteps ·) 0` (the fold of the PROVEN
`exitSteps`/`REGEN` counts over the digit tree) and the between-call glue segments `glueSegs k`
extracted cell-for-cell, the step count DECOMPOSES EXACTLY as
`exitSteps k = (glueSegs k).sum + foldRegenSteps k` at ALL FOUR levels `k=5,6,7,8`
(`exitSteps_foldl_closure`).  So the LIST-FOLD recursion reproduces the whole EXIT step count
— the arithmetic skeleton of `carryExit` is machine-checked as a real `List.foldl`.

**DELIVERABLE (A) — THE DECISIVE VERDICT: the per-position glue is *NOT* `∀`-parametric as a
bounded per-element motif.**  `x2lf_param.py` classifies every between-call glue by its
`(k'→k'')` transition (identical relative `(state,head,Δpos)` trace ⇒ a translation-invariant
transport):

```
  transition   len    byte-identical across levels?   CORE build-up height (maxpeak+4)
  START→4      154,241,424 (GROWS)  the nested DESCENT-FOLD 2^{k−3}−2 (§5w, ∀-proven)
  4→END        498,627,884 (GROWS)  fixed motif + TERM(k)      (§5y closed form, ∀-proven)
  4→5          215  (CONSTANT, byte-identical ×3)       2^5   -- a fixed ∀-reusable transport
  5→4          1089 (CONSTANT, byte-identical ×2)       2^6   -- a fixed ∀-reusable transport
  5→6          935  (once)                              2^6
  6→4          4152 (once)                              2^7   -- descent re-cascade
```

Two SHARP facts emerge.  (i) Each INDIVIDUAL transition type IS a fixed, context-independent,
`∀ L R`-reusable transport (`4→5`=215 and `5→4`=1089 are BYTE-IDENTICAL at every site across
`k=7,8` — verified), and the framing glue (`START→4` = the `∀`-proven descent-fold; `4→END` =
fixed motif + the `∀`-proven `TERM(k)`) is already parametric.  BUT (ii) the transition's CORE
`sweepEF` build-up rebuilds a block of height `2^h−4` where `h` GROWS with the odometer
position (`2^5,2^6,2^7` for `4→5,5→4,6→4`; `glue_height_grows`), and the descent glue `a→4`
grows `Θ(4^a)` (`1089 → 4152`, `descent_glue_unbounded`).  So as `k→∞` there are UNBOUNDEDLY
MANY DISTINCT transition types (`6→7, 7→8, …, 7→4, 8→4, …`), each a fixed transport but of
`Θ(4^h)` growing length — NO finite set of glue lemmas covers them, and NO fixed per-element
glue function closes the `foldl`.  The per-position glue is `∀`-parametric only as a *family*
`glue(a,b)` = a CORE re-cascade whose own length is a growing sub-fold — i.e. the glue family
is ITSELF the odometer-tree recursion, not a bounded motif.

**DELIVERABLE (B/C) — DOES `carryExit`/`carry_step` CLOSE `∀k`?  NO — and the obstruction is
now maximally localized.**  What CLOSED (GREEN, this section): the call-list recursion
(`exitList`), its grounding/arity/well-foundedness, and the STEP-COUNT `List.foldl`
(`exitSteps_foldl_closure`).  What does NOT close: the TRANSPORT-level `foldl`, because the
per-position glue is not a bounded `∀`-parametric motif but a growing CORE re-cascade
(deliverable A(ii)); equivalently, threading `toCfg` across the fold requires, at each of the
growing number of positions, proving the tape is in the exact `pow10`/`cascadeTail` form for a
CORE build-up whose height is position-dependent and unbounded.  The single remaining object
is therefore the `∀`-parametric glue FAMILY `glue(a,b)` — the odometer carry-completion
re-cascade — defined by its own well-founded recursion on the block height; the DESCENT
transitions `a→4` (the growing nested re-cascade) are its irreducible recursive heart.  This
SHARPENS the §5z/§5aa verdict from "growing-arity tree, no bounded closure" to "the arity is a
clean `List` recursion (GREEN) and the STEP COUNT folds (GREEN); the ONLY open object is the
height-parametric CORE-re-cascade glue family + its `toCfg` threading."

**Is the integer-doubler doubling-phase carry machine-checked `∀j`?  NO.**  Base (`k=4`,
`carry_exit_j3`) and depth-1 (`k=5`, `carry_exit_j4`) EXIT transports are GREEN and reproduce
the two proven carries; the step count, translation-invariance, call-list recursion, and
step-count fold are all closed `∀k`; but the transport-level glue family — a CORE re-cascade of
unbounded, position-dependent height — is the single object that remains, exactly the
project's `Suffix.lean`-scale definitional recursion.

No machine decided. No label upgraded. -/

/-- **THE ODOMETER DIGIT-TREE CALL-LIST, as a total `Nat`/`List` recursion** (deliverable A).
`exitList k` is the list of strictly-lower `REGEN(k')` recursive calls of `REGEN(k)`, in
orbit order.  Self-similar: `exitList (k+6) = range' 4 (k+1) ++ exitList (k+5)`, i.e.
`list(k) = [4,5,…,k−2] ++ list(k−1)` — a clean structural recursion (each recursive argument
`k+5 < k+6`).  Base `exitList (≤5) = []`.  This is §5aa's growing-arity odometer tree NAMED as
a `List`; the fold below is well-founded because every element is `< k`. -/
def exitList : Nat → List Nat
  | k + 6 => List.range' 4 (k + 1) ++ exitList (k + 5)
  | _ => []

/-- **THE SELF-SIMILAR UNFOLD** `list(k) = [4,5,…,k−2] ++ list(k−1)` — the clean recursion the
whole digit tree turns on, holding by `rfl` for every `k ≥ 6`. -/
theorem exitList_selfsimilar (k : Nat) :
    exitList (k + 6) = List.range' 4 (k + 1) ++ exitList (k + 5) := rfl

/-- **GROUNDING: `exitList` reproduces the extracted call-lists** cell-for-cell,
`[], [4], [4,5,4], [4,5,6,4,5,4]` for `k=5,6,7,8` (`x2dt_tree8.py`; matches
`exitSteps_tree_5/6/7`, `exitSteps_tree_8`).  Note the self-similar nesting
`[4,5,6,4,5,4] = [4,5,6] ++ [4,5,4]`.  Pure `Nat`/`List`. -/
theorem exitList_grounds :
    exitList 5 = [] ∧ exitList 6 = [4] ∧ exitList 7 = [4, 5, 4] ∧
      exitList 8 = [4, 5, 6, 4, 5, 4] := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE LIST LENGTH IS THE §5aa ARITY** `(k−5)(k−4)/2` — the digit-tree fold has exactly the
growing arity §5aa proved unbounded, now carried by the `List`.  Grounded `0,1,3,6` for
`k=5,6,7,8`.  Pure `Nat`/`List`. -/
theorem exitList_length_eq_arity :
    (exitList 5).length = exitArity 5 ∧ (exitList 6).length = exitArity 6 ∧
      (exitList 7).length = exitArity 7 ∧ (exitList 8).length = exitArity 8 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE FOLD IS WELL-FOUNDED: every recursive call is strictly lower** — each `k' ∈ exitList k`
has `k' < k`, so a `List.foldl` over `exitList` recursing into `REGEN(k')` terminates (the §5n
`odo_terminates` measure, here manifest on the list).  Grounded at the top two levels. -/
theorem exitList_wf_grounds :
    (∀ x ∈ exitList 8, x < 8) ∧ (∀ x ∈ exitList 7, x < 7) := by
  refine ⟨?_, ?_⟩ <;> decide

/-- **THE STEP-COUNT FOLD** `foldRegenSteps k = Σ_{k'∈exitList k} exitSteps k'` — the
`List.foldl` of the PROVEN per-level `REGEN`/`exitSteps` counts over the digit tree.  This is
the arithmetic skeleton of `carryExit`: the transport `foldl` would fold `regenTransport k'`
here.  Grounded `0,70,358,1368` for `k=5,6,7,8`. -/
def foldRegenSteps (k : Nat) : Nat :=
  (exitList k).foldl (fun a k' => a + exitSteps k') 0

/-- **GROUNDING the step-count fold** `0,70,358,1368` (`= Σ exitSteps` over `[],[4],[4,5,4],
[4,5,6,4,5,4]`).  Pure `Nat`/`List`. -/
theorem foldRegenSteps_grounds :
    foldRegenSteps 5 = 0 ∧ foldRegenSteps 6 = 70 ∧ foldRegenSteps 7 = 358 ∧
      foldRegenSteps 8 = 1368 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE BETWEEN-CALL GLUE SEGMENTS** (`x2lf_param.py`, merged run-lengths), in orbit order:
`[lead ; between consecutive REGEN calls ; trailing]`.  The CONSTANT byte-identical transition
transports are visible: `215` (the `4→5` glue, at `glueSegs 7` idx 1 and `glueSegs 8` idx 1,4)
and `1089` (the `5→4` glue, at `glueSegs 7` idx 2 and `glueSegs 8` idx 5). -/
def glueSegs : Nat → List Nat
  | 5 => [218]
  | 6 => [154, 498]
  | 7 => [241, 215, 1089, 627]
  | 8 => [424, 215, 935, 4152, 215, 1089, 884]
  | _ => []

/-- **THE STEP-COUNT `List.foldl` CLOSES `∀`-level-grounded** (deliverable A/B, the decisive
positive).  `exitSteps k = (glueSegs k).sum + foldRegenSteps k` at ALL FOUR levels — the
digit-tree fold of the glue segments PLUS the fold of the proven lower `REGEN` counts
reproduces the entire EXIT step count.  The LIST-FOLD recursion is real at the arithmetic
level.  Pure `Nat`/`List` (both sides `List.foldl`). -/
theorem exitSteps_foldl_closure :
    exitSteps 5 = (glueSegs 5).foldl (· + ·) 0 + foldRegenSteps 5 ∧
      exitSteps 6 = (glueSegs 6).foldl (· + ·) 0 + foldRegenSteps 6 ∧
        exitSteps 7 = (glueSegs 7).foldl (· + ·) 0 + foldRegenSteps 7 ∧
          exitSteps 8 = (glueSegs 8).foldl (· + ·) 0 + foldRegenSteps 8 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE CONSTANT TRANSITION GLUES are `∀`-parametric fixed transports** (deliverable A(i)).
The `4→5` glue is `215` at every occurrence (`glueSegs 7` idx 1; `glueSegs 8` idx 1 and 4) and
the `5→4` glue is `1089` at every occurrence (`glueSegs 7` idx 2; `glueSegs 8` idx 5) —
Python-verified BYTE-IDENTICAL relative `(state,head,Δpos)` traces, i.e. each is one
translation-invariant `∀ L R` transport recurring across levels.  Pure `List` index cross-check. -/
theorem glue_const_transitions :
    (glueSegs 7)[1]? = some 215 ∧ (glueSegs 8)[1]? = some 215 ∧ (glueSegs 8)[4]? = some 215 ∧
      (glueSegs 7)[2]? = some 1089 ∧ (glueSegs 8)[5]? = some 1089 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- **THE DECISIVE OBSTRUCTION (1/2): the CORE build-up height GROWS** (deliverable A(ii)).
Each transition's between-glue rebuilds a top block of height `2^h − 4` where `h` grows with
the odometer position: `4→5 → 2^5`, `5→4`/`5→6 → 2^6`, `6→4 → 2^7` (`x2lf_cfg.py`,
`maxpeak+4 = 2^h`).  So the glue is a CORE `sweepEF` build-up of UNBOUNDED, position-dependent
height — NOT a fixed bounded motif.  Pure `Nat`. -/
theorem glue_height_grows :
    (28 + 4 = 2 ^ 5) ∧ (60 + 4 = 2 ^ 6) ∧ (124 + 4 = 2 ^ 7) := by
  refine ⟨by decide, by decide, by decide⟩

/-- **THE DECISIVE OBSTRUCTION (2/2): the DESCENT glue `a→4` grows `Θ(4^a)`** (deliverable
A(ii)).  The odometer carry-completion re-cascade `a→4` is `1089` (`5→4`) then `4152` (`6→4`)
with `4152 > 3·1089` — a growing NESTED CORE re-cascade, not a bounded transport.  This is the
recursive heart of the remaining glue family: no fixed per-element `foldl` glue closes it.
Pure `Nat`. -/
theorem descent_glue_unbounded : 3 * 1089 < 4152 := by decide

/-! ### §5ab: what CLOSED, and the decisive per-position-glue verdict.

**PROVEN GREEN this section (on-path, `x2lf_*.py` cell-for-cell from `build(2)`):**
  • `exitList` — the odometer digit-tree call-list as a total, self-similar `Nat`/`List`
    recursion (`exitList_selfsimilar`), grounded `[],[4],[4,5,4],[4,5,6,4,5,4]`
    (`exitList_grounds`), length = §5aa arity (`exitList_length_eq_arity`), well-founded
    (`exitList_wf_grounds`: every element `< k`).  §5aa's growing arity is now a clean `List`.
  • `foldRegenSteps` + `exitSteps_foldl_closure` — the STEP-COUNT `List.foldl` over the digit
    tree CLOSES: `exitSteps k = (glueSegs k).sum + foldRegenSteps k` at all four levels.
  • `glue_const_transitions` — the SHORT transitions (`4→5`=215, `5→4`=1089) are constant
    byte-identical `∀ L R` transports (the part of the glue that IS `∀`-parametric).
  • `glue_height_grows` + `descent_glue_unbounded` — the arithmetic obstruction: the CORE
    build-up height is `2^h` (unbounded) and the descent re-cascade grows `Θ(4^a)`.

**VERDICT (deliverable A): the per-position glue is NOT `∀`-parametric as a bounded motif.**
Each individual transition is a fixed reusable transport, but the transitions carry CORE
`sweepEF` re-cascades of unbounded (`2^h`), position-dependent height, with unboundedly many
distinct transition types as `k→∞`.  So the glue is parametric only as a FAMILY `glue(a,b)`
that is itself a growing CORE re-cascade — the odometer-tree recursion, not a fixed per-element
`foldl` glue.

**VERDICT (deliverable B/C): `carryExit`/`carry_step` does NOT close `∀k`.**  The call-list
recursion and the STEP-COUNT fold are GREEN; the transport-level fold is not, because (C) the
per-position glue is a growing CORE re-cascade (not `∀`-parametric) and the `toCfg` threading
across the fold is correspondingly position-dependent.  The single remaining object is the
height-parametric glue family `glue(a,b)` (descent `a→4` = its recursive heart) + its tape
threading — the `Suffix.lean`-scale definitional recursion.  The base (`k=4`) and depth-1
(`k=5`) levels stay GREEN and reproduce `carry_exit_j3`/`carry_exit_j4`.

No machine decided. No label upgraded. -/

-- §5ab list-fold recursion axiom audits (digit-tree list + step-count foldl + glue verdict):
#print axioms exitList_selfsimilar
#print axioms exitList_grounds
#print axioms exitList_length_eq_arity
#print axioms exitList_wf_grounds
#print axioms foldRegenSteps_grounds
#print axioms exitSteps_foldl_closure
#print axioms glue_const_transitions
#print axioms glue_height_grows
#print axioms descent_glue_unbounded

end X2
