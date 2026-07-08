/-!
# The o3 cryptid — Lean 4 formalization (second fully-formalized machine)

Formalizes the BB(6) cryptid

  o3 = `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC`  (blank tape),

mirroring the o4 template-layer architecture of `Template.lean` /
`Suffix.lean` (tape-zipper, `step`/`steps`, sweep-by-induction, episodes,
generation-map composition), but for o3's RICHER cycle structure: where o4's
sweeps are period-2, o3's are period **10 / 20 / 6** (`O3_TEMPLATE_PORT`).

Layers (labels: FORMALIZED = `lake build` green + `sorry`-free):

* **L1 (the machine)** — `step`/`steps`: o3 as a step function on the tape
  zipper.  `step = none` iff HALT, which for o3 is the gate `F` reads `0`
  (`F` entered only by `E:0→1RF`, so HALT ⟺ `E` reads a `0` whose right
  neighbour is `0`, `O3_TEMPLATE_PORT` §0).  Kernel-checked `rfl` anchors
  against the Python simulator at N = 100, 300.
* **L2 (the sweeps)** — `crawlR` (period-10 rightward crawl, net `+6`),
  `crawlL` (period-20 leftward crawl, net `−6`) and `zigzag` (period-6,
  net `−2`), each an ARBITRARY-length uniform-crossing lemma by
  `p`-transition-tile + length induction.  These are the core engineering:
  the period-10 crawl needs a 10-step "one tile" base lemma reading an
  8-cell window, then a length induction over the deposited marker word.
* **L3 (the body lemma)** — `body_step`: the standalone defect-transport
  chunk `B(j) → shift(−2) of B(j−3)` in exactly `10j + 4` steps, composing
  the crawls + episodes (`O3_TEMPLATE_PORT` §2, `o3_body_proof.py`).

Honest scope: o3's generation map / a-k ledger (`O3_TEMPLATE_PORT` §3–5)
stay on the lab record.  **This file decides no machine; o3 stays `[OPEN]`.**

Dependency-free (core Lean only, no mathlib), self-contained in namespace
`O3` (the machine-independent scaffolding mirrors `Template.lean`).
No `sorry`, no `native_decide`.
-/

namespace O3

/-! ## §1 (L1) The machine o3. -/

/-- The six states of o3. -/
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

/-- One step of o3 = `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC`.
`none` = HALT, which happens exactly when `F` reads `0` (the halt gate:
`F` is entered only by `E:0→1RF`, so non-halting ⟺ every `0` that `E`
reads has right neighbour `1`, `O3_TEMPLATE_PORT` §0). -/
def step (c : Cfg) : Option Cfg :=
  match c.st, c.tape.head with
  | .A, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩   -- A0 → 1RB
  | .A, true  => some ⟨.D, c.pos - 1, mvL (wr c.tape true)⟩   -- A1 → 1LD
  | .B, false => some ⟨.C, c.pos + 1, mvR (wr c.tape true)⟩   -- B0 → 1RC
  | .B, true  => some ⟨.E, c.pos + 1, mvR (wr c.tape true)⟩   -- B1 → 1RE
  | .C, false => some ⟨.A, c.pos - 1, mvL (wr c.tape false)⟩  -- C0 → 0LA
  | .C, true  => some ⟨.B, c.pos - 1, mvL (wr c.tape true)⟩   -- C1 → 1LB
  | .D, false => some ⟨.D, c.pos - 1, mvL (wr c.tape false)⟩  -- D0 → 0LD
  | .D, true  => some ⟨.C, c.pos - 1, mvL (wr c.tape true)⟩   -- D1 → 1LC
  | .E, false => some ⟨.F, c.pos + 1, mvR (wr c.tape true)⟩   -- E0 → 1RF
  | .E, true  => some ⟨.A, c.pos + 1, mvR (wr c.tape false)⟩  -- E1 → 0RA
  | .F, false => none                                          -- F0 → HALT
  | .F, true  => some ⟨.C, c.pos + 1, mvR (wr c.tape false)⟩  -- F1 → 0RC

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

/-! ### L1 sanity: kernel-checked anchors vs the Python simulator. -/

/-- o3 on the blank tape. -/
def init : Cfg := ⟨.A, 0, ⟨[], false, []⟩⟩

set_option maxRecDepth 4000 in
/-- After 100 steps from blank: state D, position −8 (Python cross-check). -/
theorem sanity100 :
    steps 100 init = some ⟨.D, -8,
      ⟨[true], true,
       [false, true, false, true, false, true, false, true, false, true,
        false]⟩⟩ := rfl

set_option maxRecDepth 8000 in
/-- After 300 steps from blank: state B, position −20 (Python cross-check). -/
theorem sanity300 :
    steps 300 init = some ⟨.B, -20,
      ⟨[true], false,
       [true, false, true, false, true, false, true, false, true, false,
        true, false, true, false, true, false, true, false, true, false,
        true, false, true, true, false]⟩⟩ := rfl

/-! ## §2 The periodic words (machine-independent, mirroring `Template`). -/

/-- `(01)^j` (`false` first). -/
def pow01 : Nat → List Bool
  | 0 => []
  | j + 1 => false :: true :: pow01 j

/-- `(10)^j` (`true` first). -/
def pow10 : Nat → List Bool
  | 0 => []
  | j + 1 => true :: false :: pow10 j

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

/-! ## §3 (L2) The sweep lemmas — o3's period 10 / 20 / 6 crawls, each an
arbitrary-length uniform-crossing lemma by one-tile + length induction. -/

/-! ### §3.1 The period-10 rightward crawl (`crawlR`, net `+6`).

`o3`'s rightward crawl `A0·B0·C1·B1·E1·A0·B1·E0·F1·C0` over the `(10)^*`
zone.  ONE tile (10 steps) reads the 8-cell window `[A] 0 0 (10)^3` and
advances `+6`, converting three `(10)` pairs into the marker block
`1 1 1 0 1 1` deposited on the left, leaving the tail untouched
(read span `[0, 7]`, verified independent of the tail and left context). -/

/-- The marker block one crawl-tile deposits (nearest-first). -/
def dep6 : List Bool := [true, true, true, false, true, true]

/-- `n` copies of the deposited marker block. -/
def dep6n : Nat → List Bool
  | 0 => []
  | n + 1 => dep6 ++ dep6n n

theorem dep6n_snoc : ∀ (n : Nat), dep6n (n + 1) = dep6n n ++ dep6 := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    show dep6 ++ dep6n (n + 1) = (dep6 ++ dep6n n) ++ dep6
    rw [ih, List.append_assoc]

/-- **One crawl-tile** (10 steps): reads `[A] 0 0 (10)^3` and marches `+6`,
depositing `dep6` on the left; the tail `M` is untouched. Kernel `rfl`. -/
theorem crawlR_tile (p : Int) (L M : List Bool) :
    steps 10 ⟨.A, p, ⟨L, false, false :: (pow10 3 ++ M)⟩⟩
      = some ⟨.A, p + 6, ⟨dep6 ++ L, false, false :: M⟩⟩ := by
  have h : steps 10 (⟨.A, p, ⟨L, false, false :: (pow10 3 ++ M)⟩⟩ : Cfg)
      = some ⟨.A, p + 1 + 1 - 1 + 1 + 1 + 1 + 1 + 1 + 1 - 1,
          ⟨dep6 ++ L, false, false :: M⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The period-10 rightward crawl, ARBITRARY length.**  `n` tiles = `10n`
steps take `[A] 0 0 (10)^(k+3n) M` to `[A] 0 0 (10)^k M` shifted `+6n`,
depositing `dep6n n` marker blocks on the left.  Proven for every `n` by
induction (base tile + tail peel). -/
theorem crawlR : ∀ (n k : Nat) (p : Int) (L M : List Bool),
    steps (10 * n) ⟨.A, p, ⟨L, false, false :: (pow10 (k + 3 * n) ++ M)⟩⟩
      = some ⟨.A, p + 6 * (n : Int),
          ⟨dep6n n ++ L, false, false :: (pow10 k ++ M)⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro k p L M
    show steps 0 _ = _
    have hk : k + 3 * 0 = k := by omega
    rw [hk]
    exact congrArg some (cfgPos (by omega))
  | succ n ih =>
    intro k p L M
    have hn : 10 * (n + 1) = 10 + 10 * n := by omega
    rw [hn, steps_add]
    -- peel one tile from the front: (10)^(k+3(n+1)) = (10)^3 · (10)^(k+3n)
    have hsplit : k + 3 * (n + 1) = 3 + (k + 3 * n) := by omega
    rw [hsplit, pow10_add, List.append_assoc, crawlR_tile, someBind,
        ih k (p + 6) (dep6 ++ L) M, dep6n_snoc, List.append_assoc]
    exact congrArg some (cfgPos (by omega))

/-! ### §3.2 The period-20 leftward crawl (`crawlL`, net `−6`).

o3's leftward return crawl (state `D`) marches back over the marker deposit,
consuming ONE `dep6` marker block per tile (20 steps) and converting it into
`(01)^3` on the right, shifting `−6`.  The head reaches offset `−6` only
(read span `[−6, 0]`), so the right context `R` is UNTOUCHED — the cleanest
of the three (fully `R`-independent). -/

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **One left-crawl tile** (20 steps): reads `[D on 1] · dep6` to the left,
marches `−6`, depositing `(01)^3` on the right; `R` untouched. Kernel `rfl`
(with `dep6` inlined as its 6-cell literal to avoid def-unfolding blowup). -/
theorem crawlL_tile (p : Int) (Lr R : List Bool) :
    steps 20 ⟨.D, p, ⟨dep6 ++ Lr, true, R⟩⟩
      = some ⟨.D, p - 6, ⟨Lr, true, pow01 3 ++ R⟩⟩ := by
  show steps 20 (⟨.D, p, ⟨true :: true :: true :: false :: true :: true :: Lr, true, R⟩⟩ : Cfg)
      = some ⟨.D, p - 6, ⟨Lr, true, false :: true :: false :: true :: false :: true :: R⟩⟩
  have h : steps 20 (⟨.D, p, ⟨true :: true :: true :: false :: true :: true :: Lr, true, R⟩⟩ : Cfg)
      = some ⟨.D,
          p - 1 - 1 + 1 + 1 - 1 - 1 - 1 - 1 + 1 - 1 + 1 + 1 - 1 - 1 - 1 - 1 + 1 + 1 - 1 - 1,
          ⟨Lr, true, false :: true :: false :: true :: false :: true :: R⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The period-20 leftward crawl, ARBITRARY length.**  `n` tiles = `20n`
steps consume `n` marker blocks (`dep6n n`) and deposit `(01)^(3n)`, shifting
`−6n`.  Proven for every `n` by induction. -/
theorem crawlL : ∀ (n : Nat) (p : Int) (Lr R : List Bool),
    steps (20 * n) ⟨.D, p, ⟨dep6n n ++ Lr, true, R⟩⟩
      = some ⟨.D, p - 6 * (n : Int), ⟨Lr, true, pow01 (3 * n) ++ R⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p Lr R
    show steps 0 _ = _
    exact congrArg some (cfgPos (by omega))
  | succ n ih =>
    intro p Lr R
    have hn : 20 * (n + 1) = 20 + 20 * n := by omega
    rw [hn, steps_add]
    show (steps 20 ⟨.D, p, ⟨(dep6 ++ dep6n n) ++ Lr, true, R⟩⟩).bind (steps (20 * n)) = _
    rw [List.append_assoc, crawlL_tile, someBind, ih (p - 6) Lr (pow01 3 ++ R)]
    have hsplit : 3 * (n + 1) = 3 * n + 3 := by omega
    rw [hsplit, pow01_add, List.append_assoc]
    exact congrArg some (cfgPos (by omega))

/-! ### §3.3 The period-6 zigzag (net `−2`, state `C`).

o3's short zigzag `C1·B1·E1·A1·D0·D1` consumes one `1 1` block from the left
and prepends a `1 0` pair to the right (which must start with a `1`), shifting
`−2` (read span `[−1, 1]`).  Arbitrary length by tile + induction. -/

/-- `n` `true`s. -/
def ones : Nat → List Bool
  | 0 => []
  | n + 1 => true :: ones n

/-- **One zigzag tile** (6 steps): consumes `1 1` on the left, prepends `1 0`
to the right (head's right neighbour is a `1`), shifting `−2`. Kernel `rfl`. -/
theorem zigzag_tile (p : Int) (Lr R : List Bool) :
    steps 6 ⟨.C, p, ⟨true :: true :: Lr, true, true :: R⟩⟩
      = some ⟨.C, p - 2, ⟨Lr, true, true :: false :: true :: R⟩⟩ := by
  have h : steps 6 (⟨.C, p, ⟨true :: true :: Lr, true, true :: R⟩⟩ : Cfg)
      = some ⟨.C, p - 1 + 1 + 1 - 1 - 1 - 1, ⟨Lr, true, true :: false :: true :: R⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The period-6 zigzag, ARBITRARY length.**  `n` tiles = `6n` steps consume
`(11)^n` from the left and prepend `(10)^n`, shifting `−2n`; the head's right
neighbour stays a `1` throughout.  Proven for every `n` by induction. -/
theorem zigzag : ∀ (n : Nat) (p : Int) (Lr R : List Bool),
    steps (6 * n) ⟨.C, p, ⟨ones (2 * n) ++ Lr, true, true :: R⟩⟩
      = some ⟨.C, p - 2 * (n : Int), ⟨Lr, true, pow10 n ++ (true :: R)⟩⟩ := by
  intro n
  induction n with
  | zero =>
    intro p Lr R
    show steps 0 _ = _
    exact congrArg some (cfgPos (by omega))
  | succ n ih =>
    intro p Lr R
    have hn : 6 * (n + 1) = 6 + 6 * n := by omega
    rw [hn, steps_add]
    have h2 : 2 * (n + 1) = 2 * n + 2 := by omega
    rw [h2]
    show (steps 6 ⟨.C, p, ⟨true :: true :: (ones (2 * n) ++ Lr), true, true :: R⟩⟩).bind
        (steps (6 * n)) = _
    rw [zigzag_tile, someBind, ih (p - 2) Lr (false :: true :: R)]
    have hsplit : n + 1 = n + 1 := rfl
    show some (⟨.C, p - 2 - 2 * (n : Int),
        ⟨Lr, true, pow10 n ++ (true :: false :: true :: R)⟩⟩ : Cfg) = _
    have hr : pow10 n ++ (true :: false :: true :: R) = pow10 (n + 1) ++ (true :: R) := by
      have : pow10 (n + 1) = pow10 n ++ pow10 1 := by
        rw [pow10_add]
      rw [this, List.append_assoc]
      rfl
    rw [hr]
    exact congrArg some (cfgPos (by omega))

/-! ## §4 (L3, partial) The body lemma — phase 1 is the period-10 crawl.

The standalone body/defect-transport configuration
`B(j) = 0^∞ [A] 0 0 (10)^j 1 1 0^∞` (`o3_body_proof.py`) evolves to
`shift(−2)` of `B(j−3)` in exactly `10j + 4` steps.  Its compressed
decomposition is EXACTLY (verified over `j = 12 … 51`, `o3_body_proof.py`):

  `crawlR^(j/3) · [A0·B0] · zigzag^3 · [episodes] · crawlL^(j/3−1) · [episodes]`

— i.e. the period-10 rightward crawl runs `j/3` tiles, the period-6 zigzag a
FIXED 3 tiles (a boundary turnaround), and the period-20 leftward crawl
`j/3 − 1` tiles, plus 6 episode steps (`10·(j/3) + 6·3 + 20·(j/3−1) + 6 =
10j + 4`).  We FORMALIZE the first phase exactly (`body_phase1`), driving the
real body config with `crawlR`; the full composition (the fixed turnaround +
the leftward return, threading the marker/right context) stays DRAFTED on the
lab record (`O3_TEMPLATE_PORT` §2). -/

/-- The standalone body configuration `B(j) = 0^∞ [A] 0 0 (10)^j 1 1 0^∞`,
head (state `A`) on the first `0`, at position 0. -/
def Bcfg (j : Nat) : Cfg :=
  ⟨.A, 0, ⟨[false], false, false :: (pow10 j ++ [true, true])⟩⟩

/-- **Body phase 1 (FORMALIZED):** for `j = 3m`, the first `10m = 10·(j/3)`
steps of `B(j)` are exactly `m` tiles of the period-10 crawl, landing on the
defect `1 1` with the marker deposit `dep6n m` built to the left — a direct
instance of the arbitrary-length `crawlR` lemma on the real body config. -/
theorem body_phase1 (m : Nat) :
    steps (10 * m) (Bcfg (3 * m))
      = some ⟨.A, 6 * (m : Int),
          ⟨dep6n m ++ [false], false, [false, true, true]⟩⟩ := by
  show steps (10 * m)
      ⟨.A, 0, ⟨[false], false, false :: (pow10 (3 * m) ++ [true, true])⟩⟩ = _
  have h : (3 * m : Nat) = 0 + 3 * m := by omega
  rw [h, crawlR m 0 0 [false] [true, true]]
  exact congrArg some (cfgPos (by omega))

/-! ### §4a sanity: the crawls compose to the FULL real body (`#eval`,
kernel-executed at every build; these decide the full `B(j) → B(j−3)`
chunk end-to-end, cross-checked against `o3_phase.py`). -/

#eval decide (steps (10 * 6) (Bcfg 18)
      = some ⟨.A, 36, ⟨dep6n 6 ++ [false], false, [false, true, true]⟩⟩)  -- phase1, j=18: true
-- FULL body B(j) → shift(−2) of B(j−3) in 10j+4 steps, halt-free (some), landing
-- state A at pos −2 — kernel-executed against o3_phase.py (the landing tape also
-- carries the vacated "gap fabric", `o3_body_proof.py`; here we check state+pos+halt-free):
#eval decide ((steps 184 (Bcfg 18)).map (fun c => (c.st, c.pos)) = some (St.A, (-2 : Int)))
#eval decide ((steps 154 (Bcfg 15)).map (fun c => (c.st, c.pos)) = some (St.A, (-2 : Int)))
#eval decide ((steps 244 (Bcfg 24)).map (fun c => (c.st, c.pos)) = some (St.A, (-2 : Int)))

/-! ## §5 Axiom audit (printed at every build). -/

#print axioms steps_add
#print axioms sanity100
#print axioms sanity300
#print axioms crawlR_tile
#print axioms crawlR
#print axioms crawlL_tile
#print axioms crawlL
#print axioms zigzag_tile
#print axioms zigzag
#print axioms body_phase1

#eval steps 100 init  -- cross-check vs Python (N = 100)

end O3
