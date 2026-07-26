import TapeCalc

set_option maxRecDepth 4000000
set_option maxHeartbeats 1000000

/-!
# `D` — the second transparent species of the BB(6) template island: machine, words, rung tile

`D` is a 1104-holdout entry of the BB(6) residual, `[OPEN]`.  This file is the **foundation**
of its formalization (Tier I-1 of `SYNTHESIS_2026-07-26.md`): the machine on the
machine-independent `TapeCalc` layer, the word vocabulary, the milestone-region config family,
the `∀`-parametric **left-crawl atom and its fold**, and kernel-grounded instances of the
**rung tile** — the single lemma that carries 30 of the 33 measured epoch segments.

We work in the reversed form
`Dᴿ = 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---`, which grows rightward like `x2`.

**The rung tile** (`D_SPEC_2026-07-26.md` §4; re-verified independently by the integrator,
144/144 over `u ≤ 3, 1 ≤ m ≤ 3, 1 ≤ c ≤ 3, 3 ≤ g ≤ 6`, and again by `d_rung_general.py`,
23040/23040 over `u ≤ 4, 1 ≤ m ≤ 4, 0 ≤ c ≤ 3, 3 ≤ g ≤ 6` × 9 `TAIL`s × 8 `REST`s, plus a
span+1 control and a `g = 0,1,2` control that fail as required):

```
IN(u,m,c,g) := ⟨A, p, ⟨pow10 u ++ [1,1] ++ pow01 m ++ [0,0] ++ ones c ++ TAIL,
                       false, [1] ++ zeros g ++ REST⟩⟩

steps (6·(u+m) + 15) IN(u,m,c,g)  =  some IN(u+2, m−1, c+1, g−3)  at pos + 3
```

One `(1 0)` is eaten off the comb (`m → m−1`, −2 cells) while **two** `(0 1)` are emitted behind
the head (`u → u+2`, +4 cells) and the counter gains one — net `+3` cells and a `×2` register,
which is the measured `(2, 4)` width/time signature.  The head's visited window is exactly
`[p − 2(u+m) − 4, p + 4]`, so `TAIL` and `REST` are arbitrary and the tile feeds directly into
`TapeCalc.steps_lpad_dich` / `steps_rpad_dich`.

`g ≥ 3` is a genuine hypothesis, not slack: at `g = 2` the machine reaches `F` instead of
turning.  `c ≥ 1` is **not** — the outward sweep dies on the `0 0` gap one cell short of the
`1^c` block, so the `1`-counter is never read and the tile holds at `c = 0` (`tile_c_zero`).

**Atom decomposition** (`d_rung_atoms.py`, re-measured 2026-07-26 at every `u ≤ 4, 1 ≤ m ≤ 4`;
the state itinerary, not just a sample trace):

```
(ABED)^{u+1} · A · (ABED)^{m} · A · (BC) · (BE)^{m} · (BC)^{u+2} · D
   4(u+1)      1     4m         1     2      2m         2(u+2)     3     = 6(u+m)+15
```

There are **two** primitives, not one.  Outward: `ABED` is a 4-step, tape-preserving leftward
crawl over one `(1 0)` unit (`crawlB`, `crawlFold`), and it is blind to the cell it lands on —
which is why the *same* atom carries the head over the `[1,1]` marker.  Return: `BE` and `BC`
are 2-step, `+2`, **`B`-to-`B`** transposition atoms (`swap10`, `swap01`) that exchange
`1 0 ↔ 0 1`; they fold into `sweep10` / `sweep01`.  The two runs meet at the `pow10`/`pow01`
seam, and the identity `pow10 n ++ 1 :: R = 1 :: (pow01 n ++ R)` (`pow10_true`) is what lets the
return sweep read as `(0 1)` exactly the block the outward sweep wrote as `(1 0)`.

**STATUS.** The `∀ u m c g p TAIL REST` rung tile is **`[PROVEN]`** (`rungTile`, via
`rung_core`), `[propext, Quot.sound]`, no `sorry`, no `native_decide`, no `decide`.  The three
pre-existing kernel-`rfl` instances are retained and are *also* re-derived from the law
(§5.1) — two independent proofs of the same three propositions.

`D` itself remains **`[OPEN]`**.  The tile is one of the four things D's non-halting proof
needs; the `k+1` turn phases per epoch (RF-4), the shifted even-`k` `S1` segments (RF-5), the
cascade-level inner induction, and the blank→`M1(4)` entry segment are all still open.  This
file decides no machine and upgrades no label.

Zero-Mathlib, core only.  No `sorry`, no `native_decide`.
-/

namespace DMachine

open TapeCalc

/-! ## §1 The machine. -/

inductive St | A | B | C | D | E | F
deriving DecidableEq, Repr

/-- `Dᴿ = 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---`.
`none` = HALT, which happens exactly when `F` reads `1`. -/
def dT : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true,  .L, .B)   -- A0 → 1LB
  | .A, true  => some (false, .L, .A)   -- A1 → 0LA
  | .B, false => some (true,  .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .E)   -- B1 → 0RE
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true,  .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .R, .F)   -- D1 → 0RF
  | .E, false => some (true,  .R, .B)   -- E0 → 1RB
  | .E, true  => some (false, .L, .D)   -- E1 → 0LD
  | .F, false => some (true,  .R, .D)   -- F0 → 1RD
  | .F, true  => none                   -- F1 → --- HALT

/-- The blank-tape start configuration. -/
def init : Cfg St := ⟨.A, 0, ⟨[], false, []⟩⟩

/-! ## §2 Word vocabulary (as in the `x2` development; `zeros` comes from `TapeCalc`). -/

/-- `(1 0)` repeated `j` times. -/
def pow10 : Nat → List Bool
  | 0 => []
  | j + 1 => true :: false :: pow10 j

/-- `(0 1)` repeated `k` times. -/
def pow01 : Nat → List Bool
  | 0 => []
  | k + 1 => false :: true :: pow01 k

/-- `n` `true`s. -/
def ones : Nat → List Bool
  | 0 => []
  | n + 1 => true :: ones n

theorem pow10_add : ∀ (a b : Nat), pow10 (a + b) = pow10 a ++ pow10 b := by
  intro a
  induction a with
  | zero => intro b; rw [Nat.zero_add]; rfl
  | succ a ih =>
    intro b
    rw [show a + 1 + b = (a + b) + 1 from by omega]
    show true :: false :: pow10 (a + b) = pow10 (a + 1) ++ pow10 b
    rw [ih]; rfl

/-- `pow10` absorbs a `1 0` handed to it from the right: this is the word identity the crawl
fold needs (each crawl moves one `(1 0)` unit across the head, front-to-back). -/
theorem pow10_snoc : ∀ (n : Nat) (R : List Bool),
    pow10 n ++ true :: false :: R = pow10 (n + 1) ++ R := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show true :: false :: (pow10 n ++ true :: false :: R)
        = true :: false :: (pow10 (n + 1) ++ R)
    rw [ih]

/-- Mirror of `pow10_snoc` for the return sweep's `(0 1)` deposit. -/
theorem pow01_snoc : ∀ (n : Nat) (R : List Bool),
    pow01 n ++ false :: true :: R = pow01 (n + 1) ++ R := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show false :: true :: (pow01 n ++ false :: true :: R)
        = false :: true :: (pow01 (n + 1) ++ R)
    rw [ih]

/-- Head-peel, as a `rw`-able equation (both sides are definitionally equal). -/
theorem pow10_cons (n : Nat) (X : List Bool) :
    pow10 (n + 1) ++ X = true :: false :: (pow10 n ++ X) := rfl

theorem pow01_cons (n : Nat) (X : List Bool) :
    pow01 (n + 1) ++ X = false :: true :: (pow01 n ++ X) := rfl

/-- **Re-phasing.**  A `(1 0)`-comb followed by a `1` is a `1` followed by a `(0 1)`-comb.
This is the identity that lets the *return* sweep read as `(0 1)` exactly the block the
*outward* sweep wrote as `(1 0)` — it is used twice, once on the tape and once on the
target word. -/
theorem pow10_true : ∀ (n : Nat) (R : List Bool),
    pow10 n ++ true :: R = true :: (pow01 n ++ R) := by
  intro n
  induction n with
  | zero => intro R; rfl
  | succ n ih =>
    intro R
    show true :: false :: (pow10 n ++ true :: R) = true :: (false :: true :: (pow01 n ++ R))
    rw [ih]

/-- **The comb re-reading.**  After the `[1,1]` marker has been consumed, the left context
`1 · (0 1)^n · 0 0 · Z` — which is how `IN` writes it — is literally `(1 0)^(n+1) · 0 · Z`,
which is what `crawlFold` needs.  This is the one word identity that makes the second
outward sweep a *single* fold instead of an ad-hoc phase. -/
theorem pow01_shift : ∀ (n : Nat) (Z : List Bool),
    true :: (pow01 n ++ false :: false :: Z) = pow10 (n + 1) ++ false :: Z := by
  intro n
  induction n with
  | zero => intro Z; rfl
  | succ n ih =>
    intro Z
    show true :: false :: (true :: (pow01 n ++ false :: false :: Z))
        = true :: false :: (pow10 (n + 1) ++ false :: Z)
    rw [ih]

/-! ## §3 The left-crawl atom and its fold — the `∀`-uniform primitive.

`ABED`: from `A` scanning `0` with `1 0` immediately to its left, the machine writes
`1` then `0` back onto the scanned cell and `0` then `1` back onto its left neighbour —
**the tape is returned unchanged** — and the head ends two cells further left, again in `A`.
So the whole left sweep of a rung is this atom iterated, and it is blind to everything
outside the two cells it rewrites. -/

/-- Position-congruence helper (the only thing the phase arithmetic needs). -/
theorem cfgPos {s : St} {p q : Int} {t : Tape} (h : p = q) :
    (⟨s, p, t⟩ : Cfg St) = ⟨s, q, t⟩ := by rw [h]

/-- **The crawl atom, in its true generality** — the cell two to the left is *never read*,
so the atom is `∀ b`.  4 steps, head `−2`, the two rewritten cells handed to the right
verbatim.  (`crawl` below is the `b = false` case; the `b = true` case is what carries the
head over the `[1,1]` marker.) -/
theorem crawlB (p : Int) (b : Bool) (L R : List Bool) :
    steps dT 4 ⟨.A, p, ⟨true :: b :: L, false, R⟩⟩
      = some ⟨.A, p - 2, ⟨L, b, true :: false :: R⟩⟩ := by
  rw [show (p - 2 : Int) = p - 1 + 1 - 1 - 1 from by omega]
  rfl

/-- **The crawl atom** — 4 steps, head `−2`, tape unchanged, `∀ L R`. -/
theorem crawl (p : Int) (L R : List Bool) :
    steps dT 4 ⟨.A, p, ⟨true :: false :: L, false, R⟩⟩
      = some ⟨.A, p - 2, ⟨L, false, true :: false :: R⟩⟩ :=
  crawlB p false L R

/-- **The crawl fold** — the left sweep over `pow10 n`, `∀ n L R`: `4n` steps, head `−2n`,
tape unchanged (the comb is handed over to the right side verbatim). -/
theorem crawlFold : ∀ (n : Nat) (p : Int) (L R : List Bool),
    steps dT (4 * n) ⟨.A, p, ⟨pow10 n ++ L, false, R⟩⟩
      = some ⟨.A, p - 2 * n, ⟨L, false, pow10 n ++ R⟩⟩ := by
  intro n
  induction n with
  | zero => intro p L R; show some _ = some _; simp [pow10]
  | succ n ih =>
    intro p L R
    have hstep : 4 * (n + 1) = 4 + 4 * n := by omega
    rw [show ((n + 1 : Nat) : Int) = (n : Int) + 1 from by omega]
    rw [hstep, steps_add]
    show (steps dT 4 ⟨.A, p, ⟨true :: false :: (pow10 n ++ L), false, R⟩⟩).bind _ = _
    rw [crawl p (pow10 n ++ L) R, someBind, ih (p - 2) L (true :: false :: R)]
    have hpos : p - 2 - 2 * n = p - 2 * (n + 1) := by omega
    rw [hpos, pow10_snoc n R]

/-! ## §3b The three boundary atoms and the two return-sweep folds.

The outward (leftward) sweep is `crawlFold`; it is interrupted once by the `[1,1]` marker and
ends on the `0 0` gap.  The return (rightward) sweep is a *different* primitive: two 2-step,
`+2` atoms that both start and end in state `B`, one swapping `1 0 → 0 1` and one swapping
`0 1 → 1 0`.  Measured against `d_rung_atoms.py` (state itinerary
`(ABED)^{u+1} · A · (ABED)^{m+1} · A · B · (BC) · (BE)^{m+1} · (BC)^{u+2} · D`). -/

/-- **The marker step** `A1 → 0LA` — the single step between the two outward crawls. -/
theorem marker (p : Int) (x : Bool) (L R : List Bool) :
    steps dT 1 ⟨.A, p, ⟨x :: L, true, R⟩⟩ = some ⟨.A, p - 1, ⟨L, x, false :: R⟩⟩ := by rfl

/-- **The turnaround** `A0 → 1LB` — the outward sweep dies on the `0 0` gap and the return
sweep is born, one cell further left, in state `B`. -/
theorem turnaround (p : Int) (x : Bool) (L R : List Bool) :
    steps dT 1 ⟨.A, p, ⟨x :: L, false, R⟩⟩ = some ⟨.B, p - 1, ⟨L, x, true :: R⟩⟩ := by rfl

/-- **Return atom S1** (`B1 → 0RE`, `E0 → 1RB`): 2 steps, head `+2`, rewrites `1 0 ↦ 0 1`. -/
theorem swap10 (p : Int) (b : Bool) (L R : List Bool) :
    steps dT 2 ⟨.B, p, ⟨L, true, false :: b :: R⟩⟩
      = some ⟨.B, p + 2, ⟨true :: false :: L, b, R⟩⟩ := by
  rw [show (p + 2 : Int) = p + 1 + 1 from by omega]
  rfl

/-- **Return atom S2** (`B0 → 1RC`, `C1 → 0RB`): 2 steps, head `+2`, rewrites `0 1 ↦ 1 0`. -/
theorem swap01 (p : Int) (b : Bool) (L R : List Bool) :
    steps dT 2 ⟨.B, p, ⟨L, false, true :: b :: R⟩⟩
      = some ⟨.B, p + 2, ⟨false :: true :: L, b, R⟩⟩ := by
  rw [show (p + 2 : Int) = p + 1 + 1 from by omega]
  rfl

/-- **The turn** (`B0 → 1RC`, `C0 → 0RD`, `D0 → 1LA`): the return sweep hits the `0 0 0`
landing pad, deposits the new `1` and settles back into `A` at `+1`.  This is the `+3` net
head advance of the rung (and the reason `g ≥ 3` is a genuine hypothesis: at `g = 2` the
machine reaches `F` instead). -/
theorem turn (p : Int) (L R : List Bool) :
    steps dT 3 ⟨.B, p, ⟨L, false, false :: false :: R⟩⟩
      = some ⟨.A, p + 1, ⟨true :: L, false, true :: R⟩⟩ := by
  rw [show (p + 1 : Int) = p + 1 + 1 - 1 from by omega]
  rfl

/-- **Fold of S1** — `k+1` atoms over a `(1 0)^{k+1}` block, `∀ k b L R`. -/
theorem sweep10 : ∀ (k : Nat) (p : Int) (b : Bool) (L R : List Bool),
    steps dT (2 * k + 2) ⟨.B, p, ⟨L, true, false :: (pow10 k ++ b :: R)⟩⟩
      = some ⟨.B, p + 2 * k + 2, ⟨pow10 (k + 1) ++ L, b, R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p b L R
    show steps dT 2 ⟨.B, p, ⟨L, true, false :: b :: R⟩⟩
        = some ⟨.B, p + 2 * ((0 : Nat) : Int) + 2, ⟨true :: false :: L, b, R⟩⟩
    rw [swap10 p b L R]
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p b L R
    rw [show 2 * (k + 1) + 2 = 2 + (2 * k + 2) from by omega, steps_add, pow10_cons]
    rw [swap10 p true L (false :: (pow10 k ++ b :: R)), someBind,
        ih (p + 2) b (true :: false :: L) R, pow10_snoc (k + 1) L]
    exact congrArg some (cfgPos (by omega))

/-- **Fold of S2** — `k+1` atoms over a `(0 1)^{k+1}` block, `∀ k b L R`. -/
theorem sweep01 : ∀ (k : Nat) (p : Int) (b : Bool) (L R : List Bool),
    steps dT (2 * k + 2) ⟨.B, p, ⟨L, false, true :: (pow01 k ++ b :: R)⟩⟩
      = some ⟨.B, p + 2 * k + 2, ⟨pow01 (k + 1) ++ L, b, R⟩⟩ := by
  intro k
  induction k with
  | zero =>
    intro p b L R
    show steps dT 2 ⟨.B, p, ⟨L, false, true :: b :: R⟩⟩
        = some ⟨.B, p + 2 * ((0 : Nat) : Int) + 2, ⟨false :: true :: L, b, R⟩⟩
    rw [swap01 p b L R]
    exact congrArg some (cfgPos (by omega))
  | succ k ih =>
    intro p b L R
    rw [show 2 * (k + 1) + 2 = 2 + (2 * k + 2) from by omega, steps_add, pow01_cons]
    rw [swap01 p false L (true :: (pow01 k ++ b :: R)), someBind,
        ih (p + 2) b (false :: true :: L) R, pow01_snoc (k + 1) L]
    exact congrArg some (cfgPos (by omega))

/-! ## §4 The milestone-region config family and the rung tile. -/

/-- The rung-tile configuration family.  In tape order the neighbourhood reads
`… TAILᴿ 1^c 0 0 (1 0)^m 1 1 (0 1)^u [head=0] 1 0^g REST …`. -/
def IN (u m c g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg St :=
  ⟨.A, p, ⟨pow10 u ++ [true, true] ++ pow01 m ++ [false, false] ++ ones c ++ TAIL,
           false,
           true :: (zeros g ++ REST)⟩⟩

/-- Right-associated normal form of `IN`'s left word — the shape every atom consumes. -/
theorem IN_norm (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    IN u m c g p TAIL REST
      = ⟨.A, p, ⟨pow10 u ++ (true :: true :: (pow01 m ++ (false :: false :: (ones c ++ TAIL)))),
                 false, true :: (zeros g ++ REST)⟩⟩ := by
  show (⟨.A, p, ⟨pow10 u ++ [true, true] ++ pow01 m ++ [false, false] ++ ones c ++ TAIL,
                 false, true :: (zeros g ++ REST)⟩⟩ : Cfg St) = _
  rw [List.append_assoc, List.append_assoc, List.append_assoc, List.append_assoc]
  rfl

/-- **The rung tile, as a `∀`-statement** — the target of the induction.

**CORRECTION (2026-07-26).**  The span previously recorded here was `6*(u+m)+15`.  That is
wrong by exactly one crawl-plus-return period (`6`): `IN`'s own `m` argument is `m+1` in these
variables, and the measured span is `6*(u + m_IN) + 15`.  The three grounded `tile_*` instances
below (spans `21/33/45`) were always right; only this `Prop` was off.  `d_rung_general.py §A`
re-measures both readings side by side.

Also **weakened**: the `1^c` block is never read by the rung (the outward sweep dies on the
`0 0` gap one cell short of it), so the hypothesis `c ≥ 1` is unnecessary — the tile holds for
`c = 0` too.  `[PROVEN]` by `rungTile` below. -/
def RungTile : Prop :=
  ∀ (u m c g : Nat) (p : Int) (TAIL REST : List Bool),
    steps dT (6 * (u + m) + 21) (IN u (m + 1) c (g + 3) p TAIL REST)
      = some (IN (u + 2) m (c + 1) g (p + 3) TAIL REST)

/-! ### §4.1 The rung tile, proven.

`rung_core` is the tile with its two frozen contexts abstracted into bare list variables:
`W` is everything at or left of the `1^c` block, `Z` everything right of the `1 0 0 0` landing
pad.  Neither is read (the visited window is `[p − 2(u+m) − 6, p + 4]` in *these* variables —
`[p − 2(u + m_IN) − 4, p + 4]` in `IN`'s), which is what makes
the tile composable under `TapeCalc.steps_lpad_dich` / `steps_rpad_dich`.

The nine phases, in order (total `6(u+m)+21`):

| # | steps | atom | what it does |
|---|---|---|---|
| 1 | `4u` | `crawlFold u` | outward over `(0 1)^u` |
| 2 | `4` | `crawlB _ true` | outward over the first `1` of `[1,1]` |
| 3 | `1` | `marker` | `A1 → 0LA` on the second `1` |
| 4 | `4(m+1)` | `crawlFold (m+1)` | outward over the comb, re-read by `pow01_shift` |
| 5 | `1` | `turnaround` | `A0 → 1LB` on the `0 0` gap |
| 6 | `2` | `swap01` | first return atom |
| 7 | `2(m+1)` | `sweep10 m` | return over the comb |
| 8 | `2(u+2)` | `sweep01 (u+1)` | return over the deposit, re-phased by `pow10_true` |
| 9 | `3` | `turn` | land in `A` at `+3` -/
theorem rung_core (u m : Nat) (p : Int) (W Z : List Bool) :
    steps dT (6 * (u + m) + 21)
        ⟨.A, p, ⟨pow10 u ++ (true :: true :: (pow01 (m + 1) ++ (false :: false :: W))),
                 false, true :: false :: false :: false :: Z⟩⟩
      = some ⟨.A, p + 3,
          ⟨pow10 (u + 2) ++ (true :: true :: (pow01 m ++ (false :: false :: true :: W))),
           false, true :: Z⟩⟩ := by
  rw [show 6 * (u + m) + 21
        = 4 * u + (4 + (1 + (4 * (m + 1) + (1 + (2 + ((2 * m + 2) + ((2 * (u + 1) + 2) + 3)))))))
      from by omega]
  -- 1 ── outward crawl over `(0 1)^u`
  rw [steps_add, crawlFold u p (true :: true :: (pow01 (m + 1) ++ (false :: false :: W)))
        (true :: false :: false :: false :: Z), someBind]
  -- 2 ── the same atom carries the head over the first `1` of the `[1,1]` marker
  rw [steps_add, crawlB _ true (pow01 (m + 1) ++ (false :: false :: W))
        (pow10 u ++ (true :: false :: false :: false :: Z)), someBind]
  -- 3 ── the marker step
  rw [pow01_cons, steps_add, marker _ false (true :: (pow01 m ++ (false :: false :: W))) _,
      someBind]
  -- the comb now re-reads as `(1 0)^(m+1) 0`
  rw [pow01_shift m W]
  -- 4 ── outward crawl over the comb
  rw [steps_add, crawlFold (m + 1) _ (false :: W) _, someBind]
  -- 5 ── the turnaround on the `0 0` gap
  rw [steps_add, turnaround _ false W _, someBind]
  -- 6 ── the first return atom
  rw [pow10_cons, steps_add, swap01 _ true W _, someBind]
  -- 7 ── the return sweep over the comb
  rw [steps_add, sweep10 m _ false (false :: true :: W) _, someBind]
  -- the deposit re-phases from `(1 0)` to `(0 1)`
  rw [← pow10_cons u (true :: false :: false :: false :: Z),
      pow10_true (u + 1) (false :: false :: false :: Z)]
  -- 8 ── the return sweep over the deposit
  rw [steps_add, sweep01 (u + 1) _ false (pow10 (m + 1) ++ (false :: true :: W)) _, someBind]
  -- 9 ── the turn
  rw [turn _ (pow01 (u + 2) ++ (pow10 (m + 1) ++ (false :: true :: W))) Z]
  -- the target word, read back through the same two identities
  rw [pow01_shift m (true :: W), pow10_true (u + 2) (pow10 (m + 1) ++ (false :: true :: W))]
  exact congrArg some (cfgPos (by omega))

/-- **The rung tile — `[PROVEN]`, `∀ u m c g p TAIL REST`.** -/
theorem rungTile (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps dT (6 * (u + m) + 21) (IN u (m + 1) c (g + 3) p TAIL REST)
      = some (IN (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [IN_norm, IN_norm]
  exact rung_core u m p (ones c ++ TAIL) (zeros g ++ REST)

theorem rungTile_holds : RungTile := rungTile

/-! ## §5 Kernel-grounded instances (anti-vacuity + the tile at concrete levels).

Each is a closed `rfl` on the genuine machine, so a drift in `dT` or in the word vocabulary
breaks the build.  The tile instances cover both `u = 0` and `u > 0`, `m` at its floor and
above, and both the `g`-limited and comb-limited regimes.  Cross-checked cell-for-cell against
the integrator's independent simulator (`d_independent_check.py`, 144/144). -/

/-- Anti-vacuity: the real blank-tape orbit reaches the measured milestone at `t = 160`
(state `A`, `pos −4`, left blank, right `0^3 (1 0)^8 1`).  This pins the machine against the
published `PHASEB_D_M0` table. -/
theorem anchor160 :
    steps dT 160 init = some ⟨.A, -4, ⟨[], false, zeros 3 ++ (pow10 8 ++ [true])⟩⟩ := by rfl

/-- The crawl atom fires on the real orbit shape (`u = 1` prefix). -/
theorem crawl_grounded :
    steps dT 4 ⟨.A, 0, ⟨pow10 1 ++ [true, true], false, []⟩⟩
      = some ⟨.A, -2, ⟨[true, true], false, pow10 1⟩⟩ := by rfl

/-- Rung tile at `u=0, m=1, c=1, g=3`, span `6·(0+1)+15 = 21`, with blank `TAIL`/`REST`
(the `g`-floor case: `g` goes to `0`). -/
theorem tile_0_1_1_3 :
    steps dT 21 (IN 0 1 1 3 0 [] []) = some (IN 2 0 2 0 3 [] []) := by rfl

/-- Rung tile at `u=1, m=2, c=2, g=4`, span `6·(1+2)+15 = 33`, with non-trivial `TAIL`/`REST`
— the locality window is what makes those arbitrary. -/
theorem tile_1_2_2_4 :
    steps dT 33 (IN 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-- Rung tile at `u=2, m=3, c=2, g=4`, span `6·(2+3)+15 = 45` — the level whose trace gave the
atom decomposition `(ABED)³ · A · (ABED)³ · B(EB)*(CB)* · CD · A`. -/
theorem tile_2_3_2_4 :
    steps dT 45 (IN 2 3 2 4 0 [true, false, true, true, false] [true, true, false, true])
      = some (IN 4 2 3 1 3 [true, false, true, true, false] [true, true, false, true]) := by
  rfl

/-- **The span control.**  One step past the tile span the machine is in state `B` at `pos 2`,
NOT the rung's `A` at `pos 3` — so the span law is exact, not an inequality.  Stated as the
positive `rfl` fact (`Cfg` has no `DecidableEq`, so a `≠` would not `decide`). -/
theorem tile_span_control :
    (steps dT 22 (IN 0 1 1 3 0 [] [])).map (fun c => (c.st, c.pos))
      = some (St.B, (2 : Int)) := by rfl

/-! ### §5.1 Law-vs-kernel cross-check.

Each of the three `tile_*` statements above is proven a *second* time, now as an instance of
the `∀`-law.  The two proofs share nothing: the `rfl` ones are the kernel executing `dT`, the
ones below are `rung_core`'s nine-phase composition.  Because the *statements* are literally
the same propositions, a one-step drift in the law's span arithmetic, or a one-cell drift in
its word bookkeeping, would stop these from typechecking. -/

theorem tile_0_1_1_3_via_law :
    steps dT 21 (IN 0 1 1 3 0 [] []) = some (IN 2 0 2 0 3 [] []) :=
  rungTile 0 0 1 0 0 [] []

theorem tile_1_2_2_4_via_law :
    steps dT 33 (IN 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN 3 1 3 1 3 [true, false, true] [true, true]) :=
  rungTile 1 1 2 1 0 _ _

theorem tile_2_3_2_4_via_law :
    steps dT 45 (IN 2 3 2 4 0 [true, false, true, true, false] [true, true, false, true])
      = some (IN 4 2 3 1 3 [true, false, true, true, false] [true, true, false, true]) :=
  rungTile 2 2 2 1 0 _ _

/-- The law also fires where `RungTile`'s old `c + 1` shape could not state it: `c = 0`,
i.e. with the `1`-counter empty and `TAIL` pressed right up against the `0 0` gap. -/
theorem tile_c_zero :
    steps dT 33 (IN 1 2 0 3 0 [true, true] [true]) = some (IN 3 1 1 0 3 [true, true] [true]) :=
  rungTile 1 1 0 0 0 _ _

-- AXIOM AUDIT — everything here must be `[propext, Quot.sound]` or axiom-free.
#print axioms crawl
#print axioms crawlB
#print axioms crawlFold
#print axioms sweep10
#print axioms sweep01
#print axioms rung_core
#print axioms rungTile
#print axioms rungTile_holds
#print axioms anchor160
#print axioms tile_1_2_2_4
#print axioms tile_2_3_2_4_via_law
#print axioms tile_span_control

end DMachine
