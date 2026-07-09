/-!
# The o17 cryptid — Lean 4 formalization (L1 machine + the halt gate, machine-checked)

Formalizes the BB(6) cryptid

  o17 = `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`  (blank tape),

at the level its structure honestly supports: the **machine itself (L1)** and its
**halt gate**, mirroring the tape-zipper / `step`-`steps`-`steps_add` architecture of
`O3.lean` / `Template.lean`.

Why this — and only this — is the honest target
(`O17_HALT_FLAVOR_2026-07-06.md`, `O17_GATE_LAW_2026-07-07.md`): o17 has **no rigid
template**.  Its per-generation shape classes grow without bound (69 distinct shapes in
1,006 generations, level-2 compression collapses NOTHING), so there is no
`prefix·body^r·suffix` and no finite-residue ledger `a′ = a + δ(ρ)`; its protection lives
in the *timing* of carry-to-top events over an unbounded digit string (√-step growth).
So there is **no body lemma to prove** — attempting one would be dishonest.  The achievable,
machine-checked result is L1 + a full characterization of the halt gate.

Layers (labels: FORMALIZED = `lake build` / `lean` green + `sorry`-free, axiom-audited):

* **L1 (the machine)** — `step`/`steps`: o17 as a step function on the tape zipper.
  `step = none` iff HALT.  Kernel-`rfl` anchors against the Python simulator
  (`o17_halt_reduction_2026-07-06.py`, zipper-faithful) at N = 5, 100, 300.
* **The halt gate (the honest prize)** — a complete, machine-checked account of *how o17
  halts*, matching the `[PROVEN]` reduction in `O17_HALT_FLAVOR` §1a:
  - **`halt_gate`**: `step c = none ⟺ (c reads a 0 in state F)` — the literal gate.
  - **`into_F` / `into_D`**: F is entered ONLY by `D:0→0LF`; D is entered ONLY by
    `A:1→1LD` (predecessor structure, proved by case analysis on the table).  Chaining
    these two facts backward through the gate: **a halt is reached exactly 2 steps after
    the local seam `0 0 [1]_A`** (state A reads a 1 whose two left neighbours are `0 0`).
  - **`seam_to_gate` / `seam_halts`**: the forward direction — from the seam `0 0 [1]_A`
    the head reaches an `F`-reads-`0` configuration in exactly 2 steps, hence halts at
    step 3.
  - **`near_miss_safe` / `near_miss_not_halt`**: the near miss `1 0 [1]_A` instead reaches
    `F`-reads-`1` (the `4,712` safe F-entries of the blank census) and does NOT halt.
  The local safety invariant is thus made literal: *A never reads a 1 with `0 0` to its
  immediate left*.
* **Gate-event anchors** — `#eval` sanity vs the Python blank-orbit gate census: the
  true-frontier A-gates fire at steps `5, 22, 44, 101, 314, 724, 2005` (positions
  `−1,−2,−2,−3,−4,−4,−5`), each a frontier `A`-reads-`0` config (`O17_GATE_LAW` §1) — and
  the blank orbit does not halt through these (all `some`).

Honest scope: this file adds **no** template lemma and decides **nothing** about o17's
haltedness (the sparse-gate carry-timing conjecture stays `[OPEN]`, `O17_GATE_LAW` §4).
It makes o17's halt gate — the one rigid, finite, `[PROVEN]` part of its structure —
machine-checked.

Dependency-free (core Lean only, no mathlib), self-contained in namespace `O17`.
No `sorry`, no `native_decide`.
-/

namespace O17

/-! ## §1 (L1) The machine o17. -/

/-- The six states of o17. -/
inductive St where
  | A | B | C | D | E | F
deriving DecidableEq, Repr

/-- Tape zipper (as in `O3.lean`): `left` = cells left of head (nearest first),
`head` = scanned cell, `right` = cells right of head (nearest first); off-list cells
are blank (`false`). -/
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

/-- One step of o17 = `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`.
`none` = HALT, which happens exactly when `F` reads `0` (`---` = the halt transition;
the halt gate is characterized in §3: `F` is entered only by `D:0→0LF`, `D` only by
`A:1→1LD`, so HALT ⟺ the seam `0 0 [1]_A`, `O17_HALT_FLAVOR` §1a). -/
def step (c : Cfg) : Option Cfg :=
  match c.st, c.tape.head with
  | .A, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩   -- A0 → 1RB
  | .A, true  => some ⟨.D, c.pos - 1, mvL (wr c.tape true)⟩   -- A1 → 1LD
  | .B, false => some ⟨.C, c.pos + 1, mvR (wr c.tape true)⟩   -- B0 → 1RC
  | .B, true  => some ⟨.E, c.pos - 1, mvL (wr c.tape false)⟩  -- B1 → 0LE
  | .C, false => some ⟨.A, c.pos - 1, mvL (wr c.tape true)⟩   -- C0 → 1LA
  | .C, true  => some ⟨.E, c.pos + 1, mvR (wr c.tape true)⟩   -- C1 → 1RE
  | .D, false => some ⟨.F, c.pos - 1, mvL (wr c.tape false)⟩  -- D0 → 0LF
  | .D, true  => some ⟨.A, c.pos - 1, mvL (wr c.tape true)⟩   -- D1 → 1LA
  | .E, false => some ⟨.B, c.pos + 1, mvR (wr c.tape true)⟩   -- E0 → 1RB
  | .E, true  => some ⟨.B, c.pos + 1, mvR (wr c.tape false)⟩  -- E1 → 0RB
  | .F, false => none                                          -- F0 → HALT
  | .F, true  => some ⟨.B, c.pos - 1, mvL (wr c.tape false)⟩  -- F1 → 0LB

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

/-! ### §2 (L1 sanity): kernel-checked anchors vs the Python simulator. -/

/-- o17 on the blank tape. -/
def init : Cfg := ⟨.A, 0, ⟨[], false, []⟩⟩

/-- After 5 steps from blank: `0 [A]0 1 1 1 0` — o17's blank orbit IS the `j=1` member
of its own core family `0 A 0 1^{3j}` (`O17_HALT_FLAVOR` §1c).  Full-config `rfl`. -/
theorem sanity5 :
    steps 5 init = some ⟨.A, -1, ⟨[], false, [true, true, true]⟩⟩ := rfl

set_option maxRecDepth 4000 in
/-- After 100 steps from blank: state D, position −2 (Python cross-check). -/
theorem sanity100 :
    steps 100 init = some ⟨.D, -2,
      ⟨[], true,
       [true, true, false, true, true, false, true, true, true, true, true, true,
        true, true]⟩⟩ := rfl

set_option maxRecDepth 8000 in
/-- After 300 steps from blank: state D, position 6 (Python cross-check). -/
theorem sanity300 :
    steps 300 init = some ⟨.D, 6,
      ⟨[true, true, true, true, true, false, true, true, false], true,
       [true, true, false, true, true, false, true, true, true, true, true, true,
        true, true, true, true, true, true, true, true]⟩⟩ := rfl

/-! ## §3 The halt gate — machine-checked (the honest prize).

The one rigid, finite, `[PROVEN]` part of o17's structure (`O17_HALT_FLAVOR` §1a):
o17 halts ⟺ `F` reads `0`; `F` is entered only by `D:0→0LF` and `D` only by `A:1→1LD`,
so — chasing the two forced steps backward — o17 halts ⟺ the local seam `0 0 [1]_A`
(state `A` reads a `1` whose two left neighbours are both `0`).  The safety invariant is
therefore the local condition *A never reads a 1 with `0 0` to its immediate left*. -/

/-- **The halt gate.**  `step c = none` is EXACTLY "`c` is in state `F` reading a `0`".
Proved by case analysis on the twelve `(state, symbol)` branches of the table. -/
theorem halt_gate (c : Cfg) :
    step c = none ↔ (c.st = .F ∧ c.tape.head = false) := by
  obtain ⟨st, pos, l, hd, r⟩ := c
  cases st <;> cases hd <;> simp [step]

/-- **F has a unique entry transition.**  If a step lands in state `F`, the predecessor
was `D` reading a `0` (`D:0→0LF` is the only transition whose target is `F`). -/
theorem into_F {c c' : Cfg} (h : step c = some c') (hF : c'.st = .F) :
    c.st = .D ∧ c.tape.head = false := by
  obtain ⟨st, pos, l, hd, r⟩ := c
  cases st <;> cases hd <;> simp only [step] at h <;>
    first
    | (rw [Option.some.injEq] at h; subst h; simp_all)
    | simp_all

/-- **D has a unique entry transition.**  If a step lands in state `D`, the predecessor
was `A` reading a `1` (`A:1→1LD` is the only transition whose target is `D`). -/
theorem into_D {c c' : Cfg} (h : step c = some c') (hD : c'.st = .D) :
    c.st = .A ∧ c.tape.head = true := by
  obtain ⟨st, pos, l, hd, r⟩ := c
  cases st <;> cases hd <;> simp only [step] at h <;>
    first
    | (rw [Option.some.injEq] at h; subst h; simp_all)
    | simp_all

/-- **The seam reaches the gate.**  From the local seam `0 0 [1]_A` (state `A` reads a `1`
with two `0`s to its left) the head reaches an `F`-reads-`0` configuration in exactly
2 steps (`A:1→1LD` then `D:0→0LF`), for arbitrary tails `L`, `R`. -/
theorem seam_to_gate (p : Int) (L R : List Bool) :
    steps 2 ⟨.A, p, ⟨false :: false :: L, true, R⟩⟩
      = some ⟨.F, p - 2, ⟨L, false, false :: true :: R⟩⟩ := by
  have h : steps 2 (⟨.A, p, ⟨false :: false :: L, true, R⟩⟩ : Cfg)
      = some ⟨.F, p - 1 - 1, ⟨L, false, false :: true :: R⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- **The seam halts.**  Composing `seam_to_gate` with the gate (`halt_gate`): the seam
`0 0 [1]_A` halts at step 3.  `none` output = HALT. -/
theorem seam_halts (p : Int) (L R : List Bool) :
    steps 3 ⟨.A, p, ⟨false :: false :: L, true, R⟩⟩ = none := by
  rw [show (3 : Nat) = 2 + 1 from rfl, steps_add, seam_to_gate, someBind]
  show (step ⟨.F, p - 2, ⟨L, false, false :: true :: R⟩⟩).bind (steps 0) = none
  rw [(halt_gate ⟨.F, p - 2, ⟨L, false, false :: true :: R⟩⟩).mpr ⟨rfl, rfl⟩, noneBind]

/-- **The near miss is safe.**  The near miss `1 0 [1]_A` (state `A` reads a `1` with `1 0`
to its left) instead reaches `F`-reads-`1` in 2 steps — the `4,712` safe F-entries of the
blank census (`O17_HALT_FLAVOR` §1b). -/
theorem near_miss_safe (p : Int) (L R : List Bool) :
    steps 2 ⟨.A, p, ⟨false :: true :: L, true, R⟩⟩
      = some ⟨.F, p - 2, ⟨L, true, false :: true :: R⟩⟩ := by
  have h : steps 2 (⟨.A, p, ⟨false :: true :: L, true, R⟩⟩ : Cfg)
      = some ⟨.F, p - 1 - 1, ⟨L, true, false :: true :: R⟩⟩ := rfl
  rw [h]; exact congrArg some (cfgPos (by omega))

/-- The near-miss landing config does NOT halt (`F` reads `1`, not `0`) — via `halt_gate`. -/
theorem near_miss_not_halt (p : Int) (L R : List Bool) :
    step ⟨.F, p - 2, ⟨L, true, false :: true :: R⟩⟩ ≠ none := by
  rw [ne_eq, halt_gate]; simp

/-! ## §4 Gate-event anchors + non-halt sanity (`#eval`, kernel/interpreter-executed,
cross-checked vs `o17_halt_reduction_2026-07-06.py` / the blank-orbit gate census). -/

-- The blank orbit's true-frontier A-gates: state A, left-empty (frontier), reading 0,
-- at the census step numbers 5,22,44,101,314,724,2005 with positions −1,−2,−2,−3,−4,−4,−5.
#eval decide ((steps 5 init).map (fun c => (c.st, c.pos, c.tape.left, c.tape.head))
  = some (St.A, (-1 : Int), ([] : List Bool), false))   -- expect true
#eval decide ((steps 22 init).map (fun c => (c.st, c.pos, c.tape.left, c.tape.head))
  = some (St.A, (-2 : Int), ([] : List Bool), false))   -- expect true
#eval decide ((steps 44 init).map (fun c => (c.st, c.pos, c.tape.left, c.tape.head))
  = some (St.A, (-2 : Int), ([] : List Bool), false))   -- expect true
#eval decide ((steps 101 init).map (fun c => (c.st, c.pos, c.tape.left, c.tape.head))
  = some (St.A, (-3 : Int), ([] : List Bool), false))   -- expect true
#eval decide ((steps 314 init).map (fun c => (c.st, c.pos, c.tape.left, c.tape.head))
  = some (St.A, (-4 : Int), ([] : List Bool), false))   -- expect true
#eval decide ((steps 724 init).map (fun c => (c.st, c.pos, c.tape.left, c.tape.head))
  = some (St.A, (-4 : Int), ([] : List Bool), false))   -- expect true
#eval decide ((steps 2005 init).map (fun c => (c.st, c.pos, c.tape.left, c.tape.head))
  = some (St.A, (-5 : Int), ([] : List Bool), false))   -- expect true

-- The blank orbit does not halt through the gate census (all `some`):
#eval decide ((steps 2005 init).isSome)                 -- expect true
#eval decide ((steps 5000 init).isSome)                 -- expect true

-- The gate law, kernel-executed on a concrete seam / near-miss (synthetic tails):
#eval decide (steps 3 ⟨.A, 0, ⟨[false, false], true, []⟩⟩ = none)          -- seam halts: true
#eval decide ((steps 2 ⟨.A, 0, ⟨[false, true], true, []⟩⟩).isSome)          -- near miss safe: true
#eval steps 5 init  -- full config cross-check vs Python (N = 5)

/-! ## §5 Axiom audit (printed at every build). -/

#print axioms steps_add
#print axioms sanity5
#print axioms sanity100
#print axioms sanity300
#print axioms halt_gate
#print axioms into_F
#print axioms into_D
#print axioms seam_to_gate
#print axioms seam_halts
#print axioms near_miss_safe
#print axioms near_miss_not_halt

end O17
