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
