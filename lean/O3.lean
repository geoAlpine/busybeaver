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
* **L3 (the body lemma, FULLY FORMALIZED)** — `body_step`: the standalone
  defect-transport chunk `B(j) → shift(−2) of B(j−3)` (with the vacated cells
  becoming gap fabric) in exactly `10j + 4` steps, for EVERY `j ≡ 0 (mod 3)`,
  `j ≥ 3`, with an ARBITRARY right gap context `G` — the composition
  `crawlR^(j/3) · [A0 B0] · zigzag^2 · mid8 · crawlL^(j/3−1) · [D1 C0]` gluing
  the three FORMALIZED sweeps with the three fixed episodes.  The glue was
  closed by the config-identity `cons_pow01` (`true :: (01)^n = (10)^n · 1`,
  the o3 analogue of o4's `pow01_of_pow10`), which converts the leftward
  crawl's deposited `(01)` fabric into the `(10)` marker the next pass reads.
  Corrections vs the DRAFTED skeleton fell out of the concrete computation:
  the zigzag is a fixed **2** tiles (the 3rd period-6-shaped tile lands on a
  `0` and is a different phase, absorbed into the fixed 8-step `mid8`
  turnaround).  Corollaries `body_iter` / `body_descent`: the FINITE
  halt-free descent `B(3(M+r)) → B(3M)` (o3's body SHRINKS `j`, unlike o4's
  growing family, so the honest certificate is the finite descent, not an
  infinite non-halt — `o3_body_proof.py`).

* **L4 (the generation map, `a ≡ 0 (mod 3)` class, FORMALIZED, §5)** — the
  milestone `Mcfg a k` (`= build_M`), the fixed 17-step reorganization `reorg17`,
  and the prize `o3_gen0`: `M(3M, k+1) → M(4M+3, k)` in exactly `bodyTime M 0 + 17`
  steps (descent · reorg), deriving o3's base-4/3 ODOMETER (`a′ = ⌊4a/3⌋ + 3`,
  `c(0)=3`) and the k-LEDGER drain (`Δk = −1`) as theorems (`o3_odometer_mod0`).
  Real-orbit anchors `blank_to_M62` / `blank_to_M111` (blank tape → `M(6,2)` →
  `M(11,1)`, kernel-checked vs the Python milestone dump).

Honest scope: only the `a ≡ 0` residue class of the generation is closed; the
`a ≡ 1` cascade and `a ≡ 2` deposit reorgs (their own boundary episodes) and the
ledger conjecture stay on the lab record (`O3_TEMPLATE_PORT` §3–5).  **This file
decides no machine; o3 stays `[OPEN]`.**

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

/-! ## §4 (L3) The body lemma — phase 1 is the period-10 crawl.

The standalone body/defect-transport configuration
`B(j) = 0^∞ [A] 0 0 (10)^j 1 1 0^∞` (`o3_body_proof.py`) evolves to
`shift(−2)` of `B(j−3)` in exactly `10j + 4` steps.  Phase 1 (`body_phase1`,
this section) drives the real body config with `crawlR` to the defect; the
FULL composition is glued in §4b (`body_step`) and iterated in §4c. -/

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

/-! ## §4b (L3) The FULL body lemma — composing the sweeps + episodes.

Computed concretely (`o3_zipper.py`/`o3_detect.py`, cross-checked vs the trace
for `m = 1 … 19` and three gap contexts) the body chunk is EXACTLY the uniform
composition, identical for every `m ≥ 1`:

  `crawlR^m · [A0·B0] · zigzag^2 · [mid8] · crawlL^(m−1) · [D1·C0]`

with step count `10m + 2 + 12 + 8 + 20(m−1) + 2 = 30(m−1) + 34 = 10·(3m) + 4`.
Two corrections to the DRAFTED skeleton fell out of the concrete computation:
the zigzag runs a fixed **2** tiles (not 3 — the extra period-6-shaped tile is a
different phase whose head lands on a `0`, so it is NOT a `zigzag_tile`; it is
absorbed into the fixed 8-step `mid8` turnaround episode), and the leftward
return is `crawlL^(m−1)`.  This resolves the flagged obstacle ("the zigzag
shares crawlL's marker region with a different phase decomposition"): the shared
region is exactly the 4-cell left window `[1 0 1 1]` and 5-cell right window
`[1 0 1 0 1]` that `mid8` reads (verified: `mid8` reads NO tail cell), landing
in state `D` on the head of the `dep6n(m−1)` deposit that `crawlL` consumes.

The body config carries an ARBITRARY right gap context `G` (the locality of the
lemma: nothing right of the defect is read), and lands as `shift(−2)` of the
same family with `G` grown by one gap word `pow01 4 = 01010101`. -/

/-- Standalone body config with explicit position and right gap context `G`:
`BodyCfg j p G = [A] 0 0 (10)^j 1 1 G` at position `p` (head on the first `0`).
`BodyCfg j 0 [] = Bcfg j`. -/
def BodyCfg (j : Nat) (p : Int) (G : List Bool) : Cfg :=
  ⟨.A, p, ⟨[], false, false :: (pow10 j ++ (true :: true :: G))⟩⟩

theorem BodyCfg_congr {j l : Nat} {p q : Int} {G H : List Bool}
    (hj : j = l) (hp : p = q) (hG : G = H) : BodyCfg j p G = BodyCfg l q H := by
  rw [hj, hp, hG]

/-- **The pivotal config-identity** (o3 analogue of o4's `pow01_of_pow10`):
the leftward crawl deposits the vacated fabric as `(01)^n`; re-reading it shifted
by one cell turns it into the `(10)^n` marker word the next body pass consumes.
This is the identity that closes the glue's landing-config equality. -/
theorem cons_pow01 : ∀ (n : Nat), true :: pow01 n = pow10 n ++ [true] := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    show true :: false :: (true :: pow01 n) = true :: false :: (pow10 n ++ [true])
    rw [ih]

/-- `true :: (01)^n · Z = (10)^n · true :: Z` (the shift-by-one restatement). -/
theorem cons_pow01' (n : Nat) (Z : List Bool) :
    true :: (pow01 n ++ Z) = pow10 n ++ (true :: Z) := by
  rw [show true :: (pow01 n ++ Z) = (true :: pow01 n) ++ Z from rfl,
      cons_pow01 n, List.append_assoc]
  rfl

/-- The landing list-identity assembled from `cons_pow01'` (at `n` and at `4`). -/
theorem landing_id (n : Nat) (G : List Bool) :
    true :: (pow01 n ++ (pow10 4 ++ (true :: G)))
      = pow10 n ++ (true :: true :: (pow01 4 ++ G)) := by
  rw [cons_pow01' n, ← cons_pow01' 4]

/-! ### The three fixed episodes (kernel `rfl` with symbolic tails `L`/`X`/`G`,
never read — the landmark-pinning made literal). -/

/-- Episode `[A0·B0]` (2 steps): from the defect head `[A] 0 0 1 1 G`, write the
first two cells and turn into state `C` on the leading `1`. -/
theorem ep_intro (p : Int) (L G : List Bool) :
    steps 2 ⟨.A, p, ⟨L, false, false :: true :: true :: G⟩⟩
      = some ⟨.C, p + 2, ⟨true :: true :: L, true, true :: G⟩⟩ := by
  have h : steps 2 (⟨.A, p, ⟨L, false, false :: true :: true :: G⟩⟩ : Cfg)
      = some ⟨.C, p + 1 + 1, ⟨true :: true :: L, true, true :: G⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- Episode `mid8` (8 fixed steps `C1·B1·E1·A1·D0·D1·C0·A1`): the boundary
turnaround.  Reads only the 4-cell left window `[1 0 1 1]` and 2 of the right
window `[1 0 1 0 1]`; the tails `X` (left) and `G` (right) are UNTOUCHED, which
is the composition's locality.  Lands in state `D` on the `crawlL` deposit,
shifting `−4` and emitting `pow10 4 = 10101010` to the right. -/
theorem ep_mid8 (p : Int) (X G : List Bool) :
    steps 8 ⟨.C, p, ⟨true :: false :: true :: true :: X, true,
        true :: false :: true :: false :: true :: G⟩⟩
      = some ⟨.D, p - 4, ⟨X, true,
          true :: false :: true :: false :: true :: false :: true :: false ::
            true :: G⟩⟩ := by
  have h : steps 8 (⟨.C, p, ⟨true :: false :: true :: true :: X, true,
        true :: false :: true :: false :: true :: G⟩⟩ : Cfg)
      = some ⟨.D, p - 1 + 1 + 1 - 1 - 1 - 1 - 1 - 1, ⟨X, true,
          true :: false :: true :: false :: true :: false :: true :: false ::
            true :: G⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- Episode `[D1·C0]` (2 steps): the landing back onto the shifted zone start,
re-entering state `A` at `−2`; the right word `W` is untouched. -/
theorem ep_final (p : Int) (W : List Bool) :
    steps 2 ⟨.D, p, ⟨[], true, W⟩⟩
      = some ⟨.A, p - 2, ⟨[], false, false :: true :: W⟩⟩ := by
  have h : steps 2 (⟨.D, p, ⟨[], true, W⟩⟩ : Cfg)
      = some ⟨.A, p - 1 - 1, ⟨[], false, false :: true :: W⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- **THE o3 BODY LEMMA (L3), fully formal.**  For every `m'` (so `j = 3(m'+1)`,
i.e. every positive multiple of 3), the standalone body config `BodyCfg j p G`
evolves in exactly `10j + 4 = 30·m' + 34` steps to `shift(−2)` of `BodyCfg (j−3)`
with the gap fabric `G` grown by one word `pow01 4`.  `some` output ⇒ halt-free ⇒
every `E`-reads-0 safe (the halt gate).  Composition:
`crawlR^(m'+1) · [A0 B0] · zigzag^2 · mid8 · crawlL^(m') · [D1 C0]`. -/
theorem body_step (m' : Nat) (p : Int) (G : List Bool) :
    steps (30 * m' + 34) (BodyCfg (3 * (m' + 1)) p G)
      = some (BodyCfg (3 * m') (p - 2) (pow01 4 ++ G)) := by
  -- split the step budget into the six phases (literal counts the lemmas emit)
  have hsplit : 30 * m' + 34
      = 10 * (m' + 1) + (2 + (6 * 2 + (8 + (20 * m' + 2)))) := by omega
  rw [hsplit]
  -- phase 1: crawlR^(m'+1)
  show steps _ (⟨.A, p, ⟨[], false,
      false :: (pow10 (3 * (m' + 1)) ++ (true :: true :: G))⟩⟩ : Cfg) = _
  have hk : (3 * (m' + 1) : Nat) = 0 + 3 * (m' + 1) := by omega
  rw [hk, steps_add, crawlR (m' + 1) 0 p [] (true :: true :: G), someBind,
      List.append_nil]
  show steps _ (⟨.A, p + 6 * ((m' + 1 : Nat) : Int),
      ⟨dep6n (m' + 1), false, false :: true :: true :: G⟩⟩ : Cfg) = _
  -- phase 2: [A0 B0]
  rw [steps_add, ep_intro, someBind]
  -- phase 3: zigzag^2.  `true::true::dep6n(m'+1) = ones 4 ++ (1 0 1 1 · dep6n m')`
  show steps _ (⟨.C, p + 6 * ((m' + 1 : Nat) : Int) + 2,
      ⟨ones (2 * 2) ++ (true :: false :: true :: true :: dep6n m'), true,
        true :: G⟩⟩ : Cfg) = _
  rw [steps_add, zigzag 2 _ _ G, someBind]
  -- phase 4: mid8.  zigzag emitted `pow10 2 = 1010`, i.e. right = `1 0 1 0 1 · G`
  show steps _ (⟨.C, p + 6 * ((m' + 1 : Nat) : Int) + 2 - 2 * (2 : Int),
      ⟨true :: false :: true :: true :: dep6n m', true,
        true :: false :: true :: false :: true :: G⟩⟩ : Cfg) = _
  rw [steps_add, ep_mid8, someBind]
  -- phase 5: crawlL^(m').  `dep6n m' = dep6n m' ++ []`
  rw [steps_add,
      show (dep6n m' : List Bool) = dep6n m' ++ [] from (List.append_nil _).symm,
      crawlL m' _ [] _, someBind]
  -- phase 6: [D1 C0], then the landing config-identity.
  rw [ep_final]
  -- assemble: position `p - 2`, gap grown by `pow01 4`.
  apply congrArg some
  show (⟨.A, _, ⟨[], false, false :: true ::
      (pow01 (3 * m') ++ (true :: false :: true :: false :: true :: false ::
        true :: false :: true :: G))⟩⟩ : Cfg) = _
  have hlist : (true :: false :: true :: false :: true :: false :: true :: false ::
        true :: G : List Bool)
      = pow10 4 ++ (true :: G) := rfl
  rw [hlist, landing_id]
  exact cfgPos (by push_cast; omega)

/-- The paper's grid instance `j = 12` (`m' = 3`): 124 steps, `10·12 + 4`. -/
example (p : Int) (G : List Bool) :
    steps 124 (BodyCfg 12 p G) = some (BodyCfg 9 (p - 2) (pow01 4 ++ G)) :=
  body_step 3 p G

/-! ## §4c (L3 corollaries) Iterated body: the finite halt-free descent.

Unlike o4's body (which GROWS the zone, so the family provably never halts),
o3's body SHRINKS `j` by 3 per pass, bottoming out at `BodyCfg 0` — whose fate
depends on the accumulated gap (`o3_b0.py`: `BodyCfg 0` halts for a short gap,
survives for a long one).  So the honest o3 certificate is the FINITE halt-free
descent `B(3(M+r)) → B(3M)` in `bodyTime r M` steps: `steps` returning `some`
is the halt-free (all-`E`-reads-0-safe) guarantee over the whole descent.  This
is why o3 stays `[OPEN]` (its haltedness is the ledger conjecture, not a body
non-halt). -/

/-- Total steps of `r` body passes ending at parameter `3M` (starting `3(M+r)`);
each pass at parameter `3(k+1)` costs `30k + 34`. -/
def bodyTime : Nat → Nat → Nat
  | 0, _ => 0
  | r + 1, M => (30 * (M + r) + 34) + bodyTime r M

/-- **Iterated body (halt-free descent):** `r` body passes take
`BodyCfg (3(M+r)) p G` to `BodyCfg (3M) (p−r)` with `r` gap words prepended
(`pow01 (4r)`), in exactly `bodyTime r M` steps — all halt-free. -/
theorem body_iter : ∀ (r M : Nat) (p : Int) (G : List Bool),
    steps (bodyTime r M) (BodyCfg (3 * (M + r)) p G)
      = some (BodyCfg (3 * M) (p - 2 * (r : Int)) (pow01 (4 * r) ++ G)) := by
  intro r
  induction r with
  | zero =>
    intro M p G
    show steps 0 _ = _
    apply congrArg some
    exact BodyCfg_congr (by omega) (by simp) rfl
  | succ r ih =>
    intro M p G
    have h1 : steps (bodyTime (r + 1) M) (BodyCfg (3 * (M + (r + 1))) p G)
        = (steps (30 * (M + r) + 34) (BodyCfg (3 * ((M + r) + 1)) p G)).bind
            (steps (bodyTime r M)) := by
      have he : (3 * (M + (r + 1)) : Nat) = 3 * ((M + r) + 1) := by omega
      rw [he]
      exact steps_add (30 * (M + r) + 34) (bodyTime r M) _
    rw [h1, body_step, someBind, ih M (p - 2) (pow01 4 ++ G)]
    apply congrArg some
    have hpos : (p - 2) - 2 * (r : Int) = p - 2 * ((r + 1 : Nat) : Int) := by
      push_cast; omega
    have hgap : pow01 (4 * r) ++ (pow01 4 ++ G) = pow01 (4 * (r + 1)) ++ G := by
      have h44 : 4 * (r + 1) = 4 * r + 4 := by omega
      rw [h44, ← List.append_assoc, ← pow01_add]
    exact BodyCfg_congr rfl hpos hgap

/-- The full descent from `BodyCfg (3M)`: `M` passes reach `BodyCfg 0` at
`p − M` with gap `pow01 (4M) ++ G`, HALT-FREE (the `some`). -/
theorem body_descent (M : Nat) (p : Int) (G : List Bool) :
    steps (bodyTime M 0) (BodyCfg (3 * M) p G)
      = some (BodyCfg 0 (p - 2 * (M : Int)) (pow01 (4 * M) ++ G)) := by
  have h := body_iter M 0 p G
  rwa [Nat.zero_add, Nat.mul_zero] at h

/-! ## §5 (the PRIZE) The milestone `M(a,k)` and the `a ≡ 0 (mod 3)` GENERATION.

o3's milestone (from raw dumps, `O3_TEMPLATE_PORT` §1) is

  `M(a,k) = 0^∞ [A] 0 0 (10)^a (110)^k 0^∞`   (head, state `A`, on the first `0`),

with `a` = #single-`1` blocks (the ODOMETER) and `k` = #trailing `110` marker
blocks (the LEDGER — roles SWAPPED vs o4).  The generation-to-generation map goes
through the body DESCENT (`body_descent`, §4c — `a` SHRINKS to 0) followed by a
fixed 17-step REORGANIZATION that rebuilds `a` via `⌊4a/3⌋`.  For the `a ≡ 0`
class this composes into a clean Lean theorem: the odometer step `a′ = ⌊4a/3⌋ + 3`
and the ledger drain `Δk = −1`, machine-checked end-to-end (`o3_gen_proof.py`,
`o3_ledger.py`).

The leading `0 0` of a milestone plus the first marker block `1 1 0 …` is exactly
o3's body config: `M(a,k+1) = BodyCfg a p (0 · (110)^k)` — so the descent applies
with the remaining `k` markers as the (never-read) right gap context `G`, and the
`a ≡ 0` milestone bottoms out cleanly at `BodyCfg 0`. -/

/-- Marker word `(110)^k` (nearest-first): `mk 0 = []`, `mk (k+1) = 1 1 0 · mk k`. -/
def mk : Nat → List Bool
  | 0 => []
  | k + 1 => true :: true :: false :: mk k

/-- The o3 milestone `M(a,k) = 0^∞ [A] 0 0 (10)^a (110)^k 0^∞`, head (state `A`)
on the first of the two leading zeros, at position `p`.  Matches the Python
`o3_gen_proof.build_M` cell-for-cell (verified: blank tape → `Mcfg 6 2 (-14)` at
step 184, `Mcfg 11 1 (-21)` at step 299). -/
def Mcfg (a k : Nat) (p : Int) : Cfg :=
  ⟨.A, p, ⟨[], false, false :: (pow10 a ++ mk k)⟩⟩

theorem Mcfg_congr {a a' k k' : Nat} {p q : Int}
    (ha : a = a') (hk : k = k') (hp : p = q) : Mcfg a k p = Mcfg a' k' q := by
  rw [ha, hk, hp]

/-- **The milestone is a body config.**  Peeling the leading defect `1 1` off the
first marker block exposes `M(a,k+1)` as `BodyCfg a p (0 · (110)^k)` — the entry
point for the descent (definitional). -/
theorem Mcfg_as_body (a k : Nat) (p : Int) :
    Mcfg a (k + 1) p = BodyCfg a p (false :: mk k) := rfl

/-- `(01)^n · 0 Z = 0 · (10)^n Z` (the reverse-shift companion of `cons_pow01'`;
converts the descent's deposited `(01)` gap fabric back into the `(10)` blocks the
milestone counts as the rebuilt odometer `a`). -/
theorem pow01_cons_false : ∀ (n : Nat) (Z : List Bool),
    pow01 n ++ (false :: Z) = false :: (pow10 n ++ Z) := by
  intro n
  induction n with
  | zero => intro Z; rfl
  | succ n ih =>
    intro Z
    show false :: true :: (pow01 n ++ (false :: Z))
        = false :: true :: false :: (pow10 n ++ Z)
    rw [ih]

/-- **The reorganization episode (17 fixed steps, FORMALIZED).**  From `BodyCfg 0`
(the bottom of the descent) the head does a fixed local dance over the frontier
`[A] 0 0 1 1`, shifting `−3` and re-coding `1 1` into `(01)^3`, with the tail `X`
(the gap fabric `(01)^(4M)` and the surviving markers) UNTOUCHED — head span
`[p−3, p+3]`, nothing at `p+4` or beyond is read (`o3_gen_proof.py` reorg trace).
This is what rebuilds the odometer: `1 1 (01)^(4M) 0 …` re-reads as `(10)^(4M+3) …`
via `pow01_cons_false`. Kernel `rfl` with symbolic tail `X`. -/
theorem reorg17 (p : Int) (X : List Bool) :
    steps 17 ⟨.A, p, ⟨[], false, false :: true :: true :: X⟩⟩
      = some ⟨.A, p - 3, ⟨[], false,
          false :: true :: false :: true :: false :: true :: X⟩⟩ := by
  have h : steps 17 (⟨.A, p, ⟨[], false, false :: true :: true :: X⟩⟩ : Cfg)
      = some ⟨.A,
          p + 1 + 1 - 1 + 1 + 1 - 1 - 1 - 1 - 1 + 1 - 1 + 1 + 1 - 1 - 1 - 1 - 1,
          ⟨[], false, false :: true :: false :: true :: false :: true :: X⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- **THE o3 GENERATION (`a ≡ 0 (mod 3)`), fully formal.**  For every `M` and `k`,
the milestone `M(3M, k+1)` reaches `M(4M+3, k)` in exactly `bodyTime M 0 + 17`
steps — the descent (`M` body passes) then the fixed reorganization.  `some` output
⇒ HALT-FREE over the whole generation.  Reading off `a = 3M`: `a′ = 4M+3 = 4a/3+3`
(the base-4/3 ODOMETER, constant `c(0)=3`) and `k+1 ↦ k` (the LEDGER drain,
`Δk = −1`).  Composition: `body_descent M · reorg17`. -/
theorem o3_gen0 (M k : Nat) (p : Int) :
    steps (bodyTime M 0 + 17) (Mcfg (3 * M) (k + 1) p)
      = some (Mcfg (4 * M + 3) k (p - 2 * (M : Int) - 3)) := by
  rw [Mcfg_as_body, steps_add, body_descent M p (false :: mk k), someBind]
  -- descent landed on `BodyCfg 0 (p−2M) ((01)^(4M) · 0 · (110)^k)`; unfold to the
  -- reorg input and fire the 17-step episode (tail `X` never read)
  show steps 17 (⟨.A, p - 2 * (M : Int), ⟨[], false,
      false :: true :: true :: (pow01 (4 * M) ++ (false :: mk k))⟩⟩ : Cfg) = _
  rw [reorg17]
  apply congrArg some
  -- assemble the landing milestone: `(01)^3 · (01)^(4M) · 0 · (110)^k`
  --   = `(01)^(4M+3) · 0 · (110)^k` = `0 · (10)^(4M+3) · (110)^k`
  have hlist : (false :: true :: false :: true :: false :: true
        :: (pow01 (4 * M) ++ (false :: mk k)) : List Bool)
      = false :: (pow10 (4 * M + 3) ++ mk k) := by
    show (pow01 3 ++ (pow01 (4 * M) ++ (false :: mk k)))
        = false :: (pow10 (4 * M + 3) ++ mk k)
    rw [← List.append_assoc, ← pow01_add, show 3 + 4 * M = 4 * M + 3 from by omega]
    exact pow01_cons_false (4 * M + 3) (mk k)
  show (⟨.A, p - 2 * (M : Int) - 3, ⟨[], false, false :: true :: false :: true
      :: false :: true :: (pow01 (4 * M) ++ (false :: mk k))⟩⟩ : Cfg)
    = ⟨.A, p - 2 * (M : Int) - 3, ⟨[], false, false :: (pow10 (4 * M + 3) ++ mk k)⟩⟩
  rw [hlist]

/-- The paper's grid instance `M(12,3) → M(19,2)` (`M = 4, k = 2`): `316 + 17 = 333`
steps (the descent `bodyTime 4 0 = 316`, then the reorg).  Position `p − 11`. -/
example (p : Int) : steps (bodyTime 4 0 + 17) (Mcfg 12 3 p)
    = some (Mcfg 19 2 (p - 2 * (4 : Int) - 3)) := o3_gen0 4 2 p

/-- **THE o3 ODOMETER + LEDGER (`a ≡ 0 (mod 3)` class), DERIVED.**  Every milestone
`M(a,k)` with `3 ∣ a` and `k ≥ 1` reaches `M(⌊4a/3⌋ + 3, k − 1)` — the base-4/3
odometer step (constant `c(0) = 3`) and the ledger drain (`Δk = −1`), as a Lean
theorem.  What is NOT here (the residual o3 OPEN core, `O3_TEMPLATE_PORT` §5): the
`a ≡ 1` cascade / `a ≡ 2` deposit reorgs (different boundary episodes), and the
ledger conjecture that the drains never push `k` below the fatal floor.  o3 stays
`[OPEN]`. -/
theorem o3_odometer_mod0 (a k : Nat) (p : Int) (ha : a % 3 = 0) (hk : 1 ≤ k) :
    ∃ (N : Nat) (q : Int),
      steps N (Mcfg a k p) = some (Mcfg (4 * a / 3 + 3) (k - 1) q) := by
  obtain ⟨M, hM⟩ : ∃ M, a = 3 * M := ⟨a / 3, by omega⟩
  obtain ⟨k', hk'⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
  subst hM; subst hk'
  exact ⟨bodyTime M 0 + 17, p - 2 * (M : Int) - 3, by
    rw [o3_gen0]; exact congrArg some (Mcfg_congr (by omega) (by omega) rfl)⟩

/-! ### §5a real-orbit anchor: blank tape → the first two milestones.

The blank-tape orbit joins the ledger map at `M(6,2)` (`O3_TEMPLATE_PORT` §5,
concretely verified), which is an `a ≡ 0` milestone; one `o3_gen0` step (`M = 2,
k = 1`) is the first generation `M(6,2) → M(11,1)`, matching the Python milestone
dump (blank → `M(6,2)` at 184, → `M(11,1)` at 299). -/

set_option maxRecDepth 8000 in
/-- Blank tape → `M(6,2)` at position `−14` in 184 steps (kernel `rfl` vs Python). -/
theorem blank_to_M62 : steps 184 init = some (Mcfg 6 2 (-14)) := rfl

/-- Blank → `M(11,1)` at `−21` in 299 steps: `blank_to_M62` composed with the first
generation `o3_gen0 2 1` (`M(6,2) → M(11,1)`, ledger drain `2 → 1`). -/
theorem blank_to_M111 :
    steps (184 + (bodyTime 2 0 + 17)) init = some (Mcfg 11 1 (-21)) := by
  rw [steps_add, blank_to_M62, someBind,
      show (Mcfg 6 2 (-14) : Cfg) = Mcfg (3 * 2) (1 + 1) (-14) from rfl, o3_gen0]
  exact congrArg some (Mcfg_congr (by omega) rfl (by decide))

/-! ## §6 Axiom audit (printed at every build). -/

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
#print axioms cons_pow01
#print axioms landing_id
#print axioms ep_mid8
#print axioms body_step
#print axioms body_iter
#print axioms body_descent
#print axioms pow01_cons_false
#print axioms reorg17
#print axioms o3_gen0
#print axioms o3_odometer_mod0
#print axioms blank_to_M62
#print axioms blank_to_M111

/-! ### §5a sanity: the FULL body lemma, kernel-executed on the real config. -/

#eval decide (steps 124 (BodyCfg 12 0 [])
      = some (BodyCfg 9 (-2) (pow01 4 ++ [])))   -- body_step m'=3: expect true
#eval decide (steps (bodyTime 3 1) (BodyCfg 12 0 [])
      = some (BodyCfg 3 (-6) (pow01 12 ++ [])))  -- body_iter r=3,M=1: expect true

#eval steps 100 init  -- cross-check vs Python (N = 100)

/-! ### §5b sanity: the GENERATION map, kernel-executed on real milestones. -/

-- a≡0 generation grid points (vs o3_gen_proof.py): M(12,3)→M(19,2), M(15,4)→M(23,3):
#eval decide (steps (bodyTime 4 0 + 17) (Mcfg 12 3 0) = some (Mcfg 19 2 (-11)))
#eval decide (steps (bodyTime 5 0 + 17) (Mcfg 15 4 0) = some (Mcfg 23 3 (-13)))
-- the k=1 floor case M(6,1)→M(11,0) (the successor M(11,0) then halts downstream):
#eval decide (steps (bodyTime 2 0 + 17) (Mcfg 6 1 0) = some (Mcfg 11 0 (-7)))
-- real-orbit milestones (blank tape):
#eval decide (steps 184 init = some (Mcfg 6 2 (-14)))          -- expect true
#eval decide (steps (184 + (bodyTime 2 0 + 17)) init = some (Mcfg 11 1 (-21)))  -- true
#eval (184 + (bodyTime 2 0 + 17))  -- = 299, the real orbit's step-2 milestone

end O3
