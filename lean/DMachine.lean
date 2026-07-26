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
144/144 configurations over `u ≤ 3, 1 ≤ m ≤ 3, 1 ≤ c ≤ 3, 3 ≤ g ≤ 6`, plus a span+1 control
that fails as required):

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

**Measured atom decomposition** (integrator's trace, `u=2,m=3,c=2,g=4`, span 45):
`(ABED)³ · A · (ABED)³ · B(EB)*(CB)* · CD · A`.  The `ABED` block is a 4-step, **tape-preserving**
leftward crawl over one `(1 0)` unit (`crawl`, `crawlFold` below) — this is the `∀`-uniform
primitive the whole left sweep folds into.  `6(u+m)` = 4 steps out + 2 steps back per unit.

**STATUS.** `crawl`/`crawlFold` and the anchors are `[PROVEN]`.  The `∀ u m c g` rung tile is
`[MEASURED, not yet proven]` — grounded here at concrete levels by kernel `rfl`, and stated as
`RungTile` for the induction to discharge.  Following this project's discipline it is a
`def … : Prop` plus grounded instances, **not** a `sorry`.  `D` remains `[OPEN]`; this file
decides no machine and upgrades no label.

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

/-! ## §3 The left-crawl atom and its fold — the `∀`-uniform primitive.

`ABED`: from `A` scanning `0` with `1 0` immediately to its left, the machine writes
`1` then `0` back onto the scanned cell and `0` then `1` back onto its left neighbour —
**the tape is returned unchanged** — and the head ends two cells further left, again in `A`.
So the whole left sweep of a rung is this atom iterated, and it is blind to everything
outside the two cells it rewrites. -/

/-- **The crawl atom** — 4 steps, head `−2`, tape unchanged, `∀ L R`. -/
theorem crawl (p : Int) (L R : List Bool) :
    steps dT 4 ⟨.A, p, ⟨true :: false :: L, false, R⟩⟩
      = some ⟨.A, p - 2, ⟨L, false, true :: false :: R⟩⟩ := by
  rw [show (p - 2 : Int) = p - 1 + 1 - 1 - 1 from by omega]
  rfl

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

/-! ## §4 The milestone-region config family and the rung tile. -/

/-- The rung-tile configuration family.  In tape order the neighbourhood reads
`… TAILᴿ 1^c 0 0 (1 0)^m 1 1 (0 1)^u [head=0] 1 0^g REST …`. -/
def IN (u m c g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg St :=
  ⟨.A, p, ⟨pow10 u ++ [true, true] ++ pow01 m ++ [false, false] ++ ones c ++ TAIL,
           false,
           true :: (zeros g ++ REST)⟩⟩

/-- **The rung tile, as a `∀`-statement** — the target of the induction.
`[MEASURED, 144/144 + controls; NOT YET PROVEN]`.  Stated as a `Prop` (this project's
`[DESIGN]` idiom) rather than a `sorry`, so nothing here can leak into an axiom audit. -/
def RungTile : Prop :=
  ∀ (u m c g : Nat) (p : Int) (TAIL REST : List Bool),
    steps dT (6 * (u + m) + 15) (IN u (m + 1) (c + 1) (g + 3) p TAIL REST)
      = some (IN (u + 2) m (c + 2) g (p + 3) TAIL REST)

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

-- AXIOM AUDIT — everything here must be `[propext, Quot.sound]` or axiom-free.
#print axioms crawl
#print axioms crawlFold
#print axioms anchor160
#print axioms tile_1_2_2_4
#print axioms tile_span_control

end DMachine
