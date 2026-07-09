/-!
# The o18 cryptid — Lean 4 formalization (third machine toward formalization)

Formalizes the L1 machine layer and the uniform period-2 sweeps of the BB(6)
pushdown-odometer cryptid

  o18 = `1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`  (blank tape),

mirroring the o4 (`Template.lean`) / o3 (`O3.lean`) architecture: tape-zipper,
`step`/`steps`, sweep-by-induction, episode gluing.  o18 = o15's table
mirrored+re-rooted; its tower is ONE finite transition table on states
`D(m,t,e) = 0^∞ [F] 1^m 0 (10)^t 1^e 0^∞` with push law `m′−1 = (8/3)(m−1)`
(`O18_DEPTH_UNIFORM_2026-07-07.md`).  This file is EXPLORATORY: it establishes
that o18's crossings are architecturally the SAME period-2 sweeps as o4's, and
pins the exact scale-obstacle (the m-parametric defect turnaround / the
multi-defect grammar) that a full effort would face.

Layers (labels: FORMALIZED = `lake build` green + `sorry`-free):

* **L1 (the machine)** — `step`/`steps`: o18 as a step function on the tape
  zipper.  `step = none` iff HALT, which for o18 is the gate `F` reads `1`
  (`F` entered only by `D:1→1LF`, so HALT ⟺ `D` reads a `1` whose left
  neighbour is `1`, `O18_DEPTH_UNIFORM` §0).  Kernel-checked `rfl` anchors
  against the Python simulator at N = 100, 300.
* **L2 (the sweeps)** — o18's THREE uniform in-cell crossings, each an
  ARBITRARY-length uniform-crossing lemma by one-tile + length induction,
  mirroring o4's `sweepBF`/`sweepDE` and o3's `crawlR`:
  * `sweepAB` — the rightward `A0·B1` crawl over `(10)^k` (period 2): consumes
    one `(10)` pair per tile, deposits `(01)`, advances `+2k` (the read-only
    filler-inversion pass, the o18 analogue of `sweepBF`).
  * `sweepDC` — the leftward `D0·C1` crawl (period 2): consumes `(10)^k` from
    the left and BUILDS the clean-reset block `1^(2k)` on the right, shifting
    `−2k` (the o18 clean-reset-formation sweep).
  * `sweepEB` — the leftward `E1·B0·C0·A1` filler-TRANSPORT crawl (period 4,
    with the `A1→0RE` reflect half-step): reads `1` in the fixed frame `0 0`,
    transports one `(10)` pair from left to right UNCHANGED per tile, shifting
    `−2k`.  This is the odometer's leftward return pass — the crawl the head
    makes carrying the filler back over the counter inside a defect turnaround
    (`O18_DEPTH_UNIFORM` §2, the inner loop of every POP/LAND/PUSH transition).
* **L3 (one m-parametric branch tail, FORMALIZED)** — `clean_gate`: the
  leftward sweep glued to the fixed 3-step gate episode (`D0·C1·D1`), giving
  the CLEAN-RESET FORMATION `D → C_(2k+4)` uniformly in the block length `k`:
  from `0^∞ [D] (10)^k 1 1 R` the machine reaches the fresh F-gate
  `0^∞ [F] 0 1^(2k+3) R` in exactly `2k+3` steps, `some` output ⇒ the gate is
  SAFE (`F` reads `0`, not the halting `1`).  This is the LAND-branch tail
  (`O18_DEPTH_UNIFORM` §2, the `→ C_L` rows), formalized m-parametrically —
  ONE of the transition-table branches' shared uniform sub-passage.

Honest scope — the exact obstacle, pinned by trace (this session): the FULL
single-defect transition `D(m,t,e) → D(m′,t′,e′)` is NOT a fixed episode.  Every
branch (POP `m≡2`, LAND `m≡0`, PUSH2 `m≡1`) routes through a growing-amplitude
ODOMETER bounce — alternating `sweepAB` rightward passes and `sweepEB` leftward
passes whose lengths CHANGE each bounce, glued by turnaround pivots that are
COUNTER-DEPENDENT (traced: the reflect pivot branches `A→B→A→E→C→A→…` on the
surrounding counter digits, not a uniform frame).  The step count is exactly
quadratic (`≈ (4/3)m²`, `O18_DEPTH_UNIFORM` §3), i.e. `O(m)` bounces of `O(m)`
length — the aggregate `m′−1 = (8/3)(m−1)` push law is the o4-species odometer
CLOSURE, which stays OPEN (it is the same counter-dependent nondeterminism the
o4 boundary-graph program records as unclosed).  The multi-defect word grammar
(`O18_DEPTH_UNIFORM` §5) stays on the lab record.  What L2/L3 DO close: the three
uniform crawls the odometer is BUILT from, and the shared clean-reset-formation
tail (`clean_gate`, the last leftward pass of every LAND/POP landing).
**This file decides no machine; o18 stays `[OPEN]`.**

Dependency-free (core Lean only, no mathlib), self-contained in namespace
`O18`.  No `sorry`, no `native_decide`.
-/

namespace O18

/-! ## §1 (L1) The machine o18. -/

/-- The six states of o18. -/
inductive St where
  | A | B | C | D | E | F
deriving DecidableEq, Repr

/-- Tape zipper (as in `Template.lean`/`O3.lean`): `left` = cells left of head
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

/-- One step of o18 = `1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`.
`none` = HALT, which happens exactly when `F` reads `1` (the halt gate:
`F` is entered only by `D:1→1LF`, so non-halting ⟺ every `1` that `D`
reads has left neighbour `0`, `O18_DEPTH_UNIFORM` §0). -/
def step (c : Cfg) : Option Cfg :=
  match c.st, c.tape.head with
  | .A, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩   -- A0 → 1RB
  | .A, true  => some ⟨.E, c.pos + 1, mvR (wr c.tape false)⟩  -- A1 → 0RE
  | .B, false => some ⟨.C, c.pos - 1, mvL (wr c.tape true)⟩   -- B0 → 1LC
  | .B, true  => some ⟨.A, c.pos + 1, mvR (wr c.tape false)⟩  -- B1 → 0RA
  | .C, false => some ⟨.A, c.pos - 1, mvL (wr c.tape true)⟩   -- C0 → 1LA
  | .C, true  => some ⟨.D, c.pos - 1, mvL (wr c.tape true)⟩   -- C1 → 1LD
  | .D, false => some ⟨.C, c.pos - 1, mvL (wr c.tape true)⟩   -- D0 → 1LC
  | .D, true  => some ⟨.F, c.pos - 1, mvL (wr c.tape true)⟩   -- D1 → 1LF
  | .E, false => some ⟨.C, c.pos - 1, mvL (wr c.tape false)⟩  -- E0 → 0LC
  | .E, true  => some ⟨.B, c.pos - 1, mvL (wr c.tape false)⟩  -- E1 → 0LB
  | .F, false => some ⟨.E, c.pos - 1, mvL (wr c.tape true)⟩   -- F0 → 1LE
  | .F, true  => none                                          -- F1 → HALT

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

/-- o18 on the blank tape. -/
def init : Cfg := ⟨.A, 0, ⟨[], false, []⟩⟩

set_option maxRecDepth 4000 in
/-- After 100 steps from blank: state A, position −16 (Python cross-check). -/
theorem sanity100 :
    steps 100 init = some ⟨.A, -16,
      ⟨[], false,
       [true, true, false, true, false, true, false, true, false, true, false,
        true, false, true, false, true, true, true, true]⟩⟩ := rfl

set_option maxRecDepth 8000 in
/-- After 300 steps from blank: state B, position −26 (Python cross-check). -/
theorem sanity300 :
    steps 300 init = some ⟨.B, -26,
      ⟨[true, false, true, false, true, true], true,
       [false, true, false, true, false, true, false, true, false, true, true,
        true, true, true, true, true, true, true, true, true, true, true, true,
        true, true, true, true, true, true, true, true]⟩⟩ := rfl

/-! ## §2 The periodic words (machine-independent, mirroring `Template`/`O3`). -/

/-- `(01)^j` (`false` first). -/
def pow01 : Nat → List Bool
  | 0 => []
  | j + 1 => false :: true :: pow01 j

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

/-- A `(01)` pair commutes past `(01)^j` (the o4 `pow01_mid`). -/
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

/-- Two `true`s extend `1^(2k)` to `1^(2(k+1))` (the o18 clean-block mid). -/
theorem ones_mid (k : Nat) (X : List Bool) :
    ones (2 * k) ++ (true :: true :: X) = ones (2 * (k + 1)) ++ X := by
  have h : 2 * (k + 1) = 2 * k + 2 := by omega
  rw [h, ones_add, List.append_assoc]; rfl

/-! ## §3 (L2) The sweep lemmas — o18's two period-2 crawls, each an
arbitrary-length uniform-crossing lemma by one-tile + length induction.

Both are period **2** (o4-grade, simpler than o3's period 10/20/6): the
transition table's in-cell crossings over the `(10)^*` filler are exactly the
`A0·B1` (rightward) and `D0·C1` (leftward) 2-cycles. -/

/-! ### §3.1 The rightward crawl `sweepAB` (`A0·B1`, net `+2`).

From state `A` on a `0` whose right context starts with `(10)^k`, the 2-cycle
`A:0→1RB · B:1→0RA` traverses it in exactly `2k` steps, advancing `+2k` and
INVERTING each `(10)` into the `(01)` deposited on the left (o18's filler-pass,
the `sweepBF`/`sweepDE` analogue).  Head stays on a `0` throughout. -/

/-- **One rightward tile** (2 steps): reads `[A] 0 (10)`, marches `+2`,
depositing `(01)` on the left; the tail is untouched. Kernel `rfl`. -/
theorem sweepAB_tile (p : Int) (L rest : List Bool) :
    steps 2 ⟨.A, p, ⟨L, false, true :: false :: rest⟩⟩
      = some ⟨.A, p + 2, ⟨false :: true :: L, false, rest⟩⟩ := by
  have h : steps 2 (⟨.A, p, ⟨L, false, true :: false :: rest⟩⟩ : Cfg)
      = some ⟨.A, p + 1 + 1, ⟨false :: true :: L, false, rest⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The rightward crawl, ARBITRARY length.**  `k` tiles = `2k` steps take
`[A] 0 (10)^k M` to `[A] 0 M` shifted `+2k`, depositing `(01)^k` on the left.
Proven for every `k` by induction. -/
theorem sweepAB : ∀ (k : Nat) (p : Int) (L M : List Bool),
    steps (2 * k) ⟨.A, p, ⟨L, false, pow10 k ++ M⟩⟩
      = some ⟨.A, p + 2 * (k : Int), ⟨pow01 k ++ L, false, M⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p L M
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p L M
    have hn : 2 * (k + 1) = 2 * k + 2 := by omega
    rw [hn]
    have h2 : steps (2 * k + 2) (⟨.A, p, ⟨L, false, pow10 (k + 1) ++ M⟩⟩ : Cfg)
        = steps (2 * k) ⟨.A, p + 1 + 1, ⟨false :: true :: L, false, pow10 k ++ M⟩⟩ := rfl
    rw [h2, ih (p + 1 + 1) (false :: true :: L) M, pow01_mid]
    exact congrArg some (cfgPos (by omega))

/-! ### §3.2 The leftward crawl `sweepDC` (`D0·C1`, net `−2`).

From state `D` on a `0` whose LEFT context starts with `(10)^k` (reading
leftward), the 2-cycle `D:0→1LC · C:1→1LD` traverses it in exactly `2k` steps,
shifting `−2k` and CONVERTING the `(10)^k` region into the clean block `1^(2k)`
deposited on the right — the clean-reset-formation sweep.  Head stays on a `0`
throughout; the right context `R` is untouched. -/

/-- **One leftward tile** (2 steps): reads `[D on 0] (10)` to the left,
marches `−2`, depositing `1 1` on the right; `R` untouched. Kernel `rfl`. -/
theorem sweepDC_tile (p : Int) (L R : List Bool) :
    steps 2 ⟨.D, p, ⟨true :: false :: L, false, R⟩⟩
      = some ⟨.D, p - 2, ⟨L, false, true :: true :: R⟩⟩ := by
  have h : steps 2 (⟨.D, p, ⟨true :: false :: L, false, R⟩⟩ : Cfg)
      = some ⟨.D, p - 1 - 1, ⟨L, false, true :: true :: R⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The leftward crawl, ARBITRARY length.**  `k` tiles = `2k` steps consume
`(10)^k` from the left and deposit `1^(2k)` on the right, shifting `−2k`.
Proven for every `k` by induction. -/
theorem sweepDC : ∀ (k : Nat) (p : Int) (L R : List Bool),
    steps (2 * k) ⟨.D, p, ⟨pow10 k ++ L, false, R⟩⟩
      = some ⟨.D, p - 2 * (k : Int), ⟨L, false, ones (2 * k) ++ R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p L R
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p L R
    have hn : 2 * (k + 1) = 2 * k + 2 := by omega
    rw [hn]
    have h2 : steps (2 * k + 2) (⟨.D, p, ⟨pow10 (k + 1) ++ L, false, R⟩⟩ : Cfg)
        = steps (2 * k) ⟨.D, p - 1 - 1, ⟨pow10 k ++ L, false, true :: true :: R⟩⟩ := rfl
    rw [h2, ih (p - 1 - 1) L (true :: true :: R), ones_mid]
    exact congrArg some (cfgPos (by omega))

/-! ### §3.3 The leftward filler-transport crawl `sweepEB` (`E1·B0·C0·A1`, net `−2`).

The THIRD uniform crossing of o18, and the one that reveals why the single-defect
transition is an ODOMETER rather than a fixed episode.  In the defect turnaround,
after a rightward `sweepAB` pass hits the block's right end and reflects into state
`E`, the head crawls back LEFT over the `(10)^k` filler by the **period-4** 2½-cycle
`E:1→0LB · B:0→1LC · C:0→1LA · A:1→0RE` (note the `A1→0RE` half-step that reflects
the head one cell right to re-enter `E`).  Each tile is 4 machine steps, nets `−2`,
and TRANSPORTS one `(10)` pair from the head's left to its right UNCHANGED — the
filler is shuttled leftward past the head without inversion (contrast `sweepAB`,
which inverts `(10)→(01)`).  The head reads `1` throughout, with the fixed frame
`0 0` immediately to its left; `L` and `R` are untouched.  Kernel-confirmed against
the o18 simulator (`o18_depth_map.py`, the defect-turnaround inner loop). -/

/-- `(10)^k` with a `(10)` appended on the right equals `(10)^(k+1)` — the uniform
repetition commutes end-to-end (needed to fold the transported filler). -/
theorem pow10_snoc : ∀ (k : Nat),
    pow10 k ++ [true, false] = pow10 (k + 1) := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
    show true :: false :: (pow10 k ++ [true, false]) = true :: false :: pow10 (k + 1)
    rw [ih]

/-- **One leftward filler-transport tile** (4 steps): reads `[E on 1]` with frame
`0 0` and one `(10)` pair to the left, marches `−2`, and re-deposits that `(10)`
pair on the right; `Z`, `R` untouched, head still on `1`. Kernel `rfl`. -/
theorem sweepEB_tile (p : Int) (Z R : List Bool) :
    steps 4 ⟨.E, p, ⟨false :: false :: true :: false :: Z, true, R⟩⟩
      = some ⟨.E, p - 2, ⟨false :: false :: Z, true, true :: false :: R⟩⟩ := by
  have h : steps 4 (⟨.E, p, ⟨false :: false :: true :: false :: Z, true, R⟩⟩ : Cfg)
      = some ⟨.E, p - 1 - 1 - 1 + 1, ⟨false :: false :: Z, true, true :: false :: R⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **The leftward filler-transport crawl, ARBITRARY length.**  `k` tiles = `4k`
steps take `[E on 1] 0 0 (10)^k L` to `[E on 1] 0 0 L`, transporting the whole
`(10)^k` filler UNCHANGED to the right and shifting `−2k`.  This is the odometer's
leftward return pass — the crawl that carries the filler back over the counter.
Proven for every `k` by induction. -/
theorem sweepEB : ∀ (k : Nat) (p : Int) (L R : List Bool),
    steps (4 * k) ⟨.E, p, ⟨false :: false :: (pow10 k ++ L), true, R⟩⟩
      = some ⟨.E, p - 2 * (k : Int), ⟨false :: false :: L, true, pow10 k ++ R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p L R
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p L R
    have hn : 4 * (k + 1) = 4 + 4 * k := by omega
    rw [hn, steps_add]
    have hpeel : false :: false :: (pow10 (k + 1) ++ L)
        = false :: false :: true :: false :: (pow10 k ++ L) := rfl
    rw [hpeel, sweepEB_tile, someBind,
        ih (p - 2) L (true :: false :: R)]
    apply congrArg some
    -- fold the transported filler: pow10 k ++ (true::false::R) = pow10 (k+1) ++ R
    have hr : pow10 k ++ (true :: false :: R) = pow10 (k + 1) ++ R := by
      show pow10 k ++ ([true, false] ++ R) = pow10 (k + 1) ++ R
      rw [← List.append_assoc, pow10_snoc]
    rw [hr]
    exact cfgPos (by omega)

/-! ## §4 (L3) The clean-reset formation — one m-parametric branch tail.

The leftward sweep glued to the fixed 3-step gate episode `D0·C1·D1`.  This is
the uniform TAIL shared by every LAND branch of the transition table
(`O18_DEPTH_UNIFORM` §2, the `→ C_L` rows): once the passage has rebuilt a clean
`(10)^k 1 1` block to the head's left with blank beyond, it collapses that block
into the fresh clean reset `C_(2k+4) = 0^∞ [F] 0 1^(2k+3) 0^∞`, uniformly in `k`.
The `some` output certifies the gate is SAFE: `F` reads `0`, not the halting
`1`. -/

/-- **The gate episode** (3 fixed steps `D0·C1·D1`): from `[D on 0] 1 1 R` with
blank beyond the two `1`s, the head collapses the `1 1` into the F-gate, landing
`[F on 0] 1 1 1 R` shifted `−3` — `F` reads `0` (safe). Kernel `rfl` (symbolic
tail `R` untouched). -/
theorem gate_episode (p : Int) (R : List Bool) :
    steps 3 ⟨.D, p, ⟨[true, true], false, R⟩⟩
      = some ⟨.F, p - 3, ⟨[], false, true :: true :: true :: R⟩⟩ := by
  have h : steps 3 (⟨.D, p, ⟨[true, true], false, R⟩⟩ : Cfg)
      = some ⟨.F, p - 1 - 1 - 1, ⟨[], false, true :: true :: true :: R⟩⟩ := rfl
  rw [h]
  exact congrArg some (cfgPos (by omega))

/-- **THE CLEAN-RESET FORMATION (L3), m-parametric.**  For every block length
`k`, the config `0^∞ [D] (10)^k 1 1 R` reaches the fresh clean-reset F-gate
`0^∞ [F] 0 1^(2k+3) R` in exactly `2k + 3` steps: `sweepDC^k` (build the
`1^(2k)` block) glued to the fixed `gate_episode`.  `some` output ⇒ the whole
passage is halt-free AND the landing gate is safe (`F` reads `0`).  With `R = []`
this is the clean reset `C_(2k+4)`. -/
theorem clean_gate (k : Nat) (p : Int) (R : List Bool) :
    steps (2 * k + 3) ⟨.D, p, ⟨pow10 k ++ [true, true], false, R⟩⟩
      = some ⟨.F, p - 2 * (k : Int) - 3, ⟨[], false, ones (2 * k + 3) ++ R⟩⟩ := by
  rw [steps_add, sweepDC k p [true, true] R, someBind, gate_episode]
  apply congrArg some
  have hlist : true :: true :: true :: (ones (2 * k) ++ R)
      = ones (2 * k + 3) ++ R := by
    have h3 : 2 * k + 3 = 3 + 2 * k := by omega
    rw [h3, ones_add]
    rfl
  rw [hlist]

/-- The clean reset `C_(2k+4)` (`R = []`): `0^∞ [D] (10)^k 1 1 → 0^∞ [F] 0 1^(2k+3)`
in `2k+3` steps, landing on a SAFE gate. -/
theorem clean_reset (k : Nat) (p : Int) :
    steps (2 * k + 3) ⟨.D, p, ⟨pow10 k ++ [true, true], false, []⟩⟩
      = some ⟨.F, p - 2 * (k : Int) - 3, ⟨[], false, ones (2 * k + 3)⟩⟩ := by
  have h := clean_gate k p []
  rwa [List.append_nil] at h

/-! ## §5 Axiom audit (printed at every build). -/

#print axioms steps_add
#print axioms sanity100
#print axioms sanity300
#print axioms sweepAB_tile
#print axioms sweepAB
#print axioms sweepDC_tile
#print axioms sweepDC
#print axioms pow10_snoc
#print axioms sweepEB_tile
#print axioms sweepEB
#print axioms gate_episode
#print axioms clean_gate
#print axioms clean_reset

/-! ### §5a sanity: kernel-executed `#eval` mirrors vs the Python simulator. -/

#eval steps 100 init  -- cross-check vs o18 simulator (N = 100)

-- sweepAB grid point (k=5), sweepDC grid point (k=5), clean_gate (k=6): expect all true
#eval decide (steps (2 * 5) ⟨.A, 0, ⟨[true, true], false, pow10 5 ++ [true, true, true]⟩⟩
      = some ⟨.A, 10, ⟨pow01 5 ++ [true, true], false, [true, true, true]⟩⟩)
#eval decide (steps (2 * 5) ⟨.D, 0, ⟨pow10 5 ++ [true], false, []⟩⟩
      = some ⟨.D, -10, ⟨[true], false, ones 10⟩⟩)
#eval decide (steps (2 * 6 + 3) ⟨.D, 0, ⟨pow10 6 ++ [true, true], false, []⟩⟩
      = some ⟨.F, -15, ⟨[], false, ones 15⟩⟩)  -- clean reset C_16

-- sweepEB grid point (k=5): the leftward filler-transport crawl (expect true)
#eval decide (steps (4 * 5) ⟨.E, 0, ⟨false :: false :: (pow10 5 ++ [true, true, true]),
        true, [true, true]⟩⟩
      = some ⟨.E, -10, ⟨false :: false :: [true, true, true], true, pow10 5 ++ [true, true]⟩⟩)

end O18
