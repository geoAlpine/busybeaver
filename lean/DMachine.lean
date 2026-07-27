import RungCalc

set_option maxRecDepth 4000000
set_option maxHeartbeats 1000000

/-!
# `D` — the second transparent species of the BB(6) template island: machine, atoms, rung tile

`D` is a 1104-holdout entry of the BB(6) residual, `[OPEN]`.  This file is the **foundation** of
its formalization (Tier I-1 of `SYNTHESIS_2026-07-26.md`): the machine on the machine-independent
`TapeCalc` layer, the six rung atoms, and — via `RungCalc` — the **rung tile**, the single lemma
that carries 30 of the 33 measured epoch segments.

We work in the reversed form
`Dᴿ = 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---`, which grows rightward like `x2`.

**The rung tile** (`D_SPEC_2026-07-26.md` §4; independently re-verified 144/144 over
`u ≤ 3, 1 ≤ m ≤ 3, 1 ≤ c ≤ 3, 3 ≤ g ≤ 6`, and again by `d_rung_general.py`, 23040/23040 over
`u ≤ 4, 1 ≤ m ≤ 4, 0 ≤ c ≤ 3, 3 ≤ g ≤ 6` × 9 `TAIL`s × 8 `REST`s, plus span+1 and `g = 0,1,2`
controls that fail as required):

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

**Atom decomposition** (`d_rung_atoms.py`, the full state itinerary at every
`u ≤ 4, 1 ≤ m ≤ 4`):

```
(ABED)^{u+1} · A · (ABED)^{m} · A · (BC) · (BE)^{m} · (BC)^{u+2} · D
   4(u+1)      1     4m         1     2      2m         2(u+2)     3     = 6(u+m)+15
```

There are **two** primitives, not one.  Outward: `ABED` is a 4-step, tape-preserving leftward
crawl over one `(1 0)` unit, and it is blind to the cell it lands on — which is why the *same*
atom carries the head over the `[1,1]` marker.  Return: `BE` and `BC` are 2-step, `+2`,
**`B`-to-`B`** transposition atoms exchanging `1 0 ↔ 0 1`.  Both fold; see `RungCalc`.

**STATUS.** The `∀ u m c g p TAIL REST` rung tile is **`[PROVEN]`** (`rungTile`), with axioms
`[propext, Quot.sound]`, no `sorry`, no `native_decide`, no `decide`.  The nine-phase proof does
not live here: it is `RungCalc.rung_core`, machine-independent, and this file's entire
contribution to it is `dAtoms` — six closed kernel `rfl`s.  (`lean/HMachine.lean` reuses the
same layer for `H`, whose transition graph is *not* a relabeling of `D`'s.)

`D` itself remains **`[OPEN]`**.  The tile is one of the four things D's non-halting proof
needs; the `k+1` turn phases per epoch (RF-4), the shifted even-`k` `S1` segments (RF-5), the
cascade-level inner induction, and the blank→`M1(4)` entry segment are all still open.  This
file decides no machine and upgrades no label.

Zero-Mathlib, core only.
-/

namespace DMachine

open TapeCalc RungCalc

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

/-! ## §2 The six atoms.

`D`'s outward-sweep state is `A`, its return-sweep state is `B`.  Each atom is a closed `rfl` on
the genuine machine, so any drift in `dT` breaks the build.  The walks are
`crawl = A0→1LB, B1→0RE, E1→0LD, D0→1LA`; `marker = A1→0LA`; `turnaround = A0→1LB`;
`swap10 = B1→0RE, E0→1RB`; `swap01 = B0→1RC, C1→0RB`; `turn = B0→1RC, C0→0RD, D0→1LA`. -/
theorem dAtoms : Atoms dT .A .B 4 1 1 2 2 3 where
  crawl := by
    intro p b L R
    rw [show (p - 2 : Int) = p - 1 + 1 - 1 - 1 from by omega]
    rfl
  marker := by intro p x L R; rfl
  turnaround := by intro p x L R; rfl
  swap10 := by
    intro p b L R
    rw [show (p + 2 : Int) = p + 1 + 1 from by omega]
    rfl
  swap01 := by
    intro p b L R
    rw [show (p + 2 : Int) = p + 1 + 1 from by omega]
    rfl
  turn := by
    intro p L R
    rw [show (p + 1 : Int) = p + 1 + 1 - 1 from by omega]
    rfl

/-! ## §3 The rung tile. -/

/-- `D`'s milestone-region configuration family: `RungCalc.IN` at `D`'s outward state.
In tape order the neighbourhood reads
`… TAILᴿ 1^c 0 0 (1 0)^m 1 1 (0 1)^u [head=0] 1 0^g REST …`. -/
abbrev IN (u m c g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg St :=
  RungCalc.IN St.A u m c g p TAIL REST

/-- **The rung tile — `[PROVEN]`, `∀ u m c g p TAIL REST`.**

Note the span.  An earlier revision of this file stated it as `6*(u+m)+15` on
`IN u (m+1) …`, which is wrong by exactly one crawl-plus-return period (`6`): `IN`'s own `m`
argument is `m+1` in these variables, so the span is `6*(u+m)+21`.  The kernel-`rfl` instances
below (spans `21/33/45`) were always right; only the `∀`-statement was off.
`d_rung_general.py §A` re-measures both readings side by side. -/
theorem rungTile (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps dT (6 * (u + m) + 21) (IN u (m + 1) c (g + 3) p TAIL REST)
      = some (IN (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * (u + m) + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact RungCalc.tile dAtoms u m c g p TAIL REST

theorem rungTile_holds : Tile dT St.A (span 4 1 1 2 2 3) := tile_holds dAtoms


/-! ## §5 The turn phase — RF-4, closed form.

`D_SPEC_2026-07-26.md` §5/§8 recorded the inter-segment turn phases as `≈2 steps/cell` with
additive constants that are "not a closed function of `k` alone", each needing "a separate small
lemma".  That reading was **too pessimistic**: measurement (`d_rf4_turns.py`, `d_rf4_law.py`)
shows the rightward turn phase is the *same rung*, with the return sweep crossing a `(1 0)^w`
comb before it reaches the landing pad.  The constants are not free parameters — they are
`6(u+m)+15`, i.e. functions of the **local rung shape**, which is why they never looked like
functions of `k`.

So `RF-4`'s rightward half needs no new lemma at all: it is `RungCalc.tile2`, and the rung tile
is its `w = 0` case.  The *leftward* return turns use a different primitive and are still open —
see `D_RF4_2026-07-27.md`. -/

/-- `IN` with the landing pad pushed `2w` cells right by a `(1 0)^w` comb. -/
abbrev IN2 (u m c w g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg St :=
  RungCalc.IN2 St.A u m c w g p TAIL REST

/-- **D's turn phase — `[PROVEN]`, `∀ u m c w g p TAIL REST`.**  Span `6(u+m)+21+2(w+1)`, head
advance `+3+2(w+1)`, and the output is again an `IN` — at `u'=0, m'=w, c'=1` — so a turn feeds
straight back into the rung tile, which is exactly what an epoch does. -/
theorem turnPhase (u m c w g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps dT (6 * (u + m) + 21 + 2 * (w + 1)) (IN2 u (m + 1) c (w + 1) (g + 3) p TAIL REST)
      = some (IN 0 w 1 g (p + 3 + 2 * (w + 1))
          (pow01 (u + 1) ++ (pow10 (m + 1) ++ (false :: true :: (ones c ++ TAIL)))) REST) := by
  rw [show 6 * (u + m) + 21 + 2 * (w + 1) = span 4 1 1 2 2 3 u m + 2 * (w + 1)
      from by simp [span]; omega]
  exact RungCalc.tile2 dAtoms u m c w g p TAIL REST

/-- The turn phase at the parameters of `D`'s **real orbit** turn at `t = 291698`
(`u=9, m=2, c=6, w=66`; span `6·(9+2)+15+2·66 = 213`, measured 213), by the law. -/
theorem turn_291698_via_law :
    steps dT 213 (IN2 9 2 6 66 3 0 [true, false] [true, true])
      = some (IN 0 65 1 0 135
          (pow01 10 ++ (pow10 2 ++ (false :: true :: (ones 6 ++ [true, false])))) [true, true]) :=
  turnPhase 9 1 6 65 0 0 _ _

/-- The same proposition, by the kernel executing `dT` for 213 steps.  Two independent proofs. -/
theorem turn_291698_kernel :
    steps dT 213 (IN2 9 2 6 66 3 0 [true, false] [true, true])
      = some (IN 0 65 1 0 135
          (pow01 10 ++ (pow10 2 ++ (false :: true :: (ones 6 ++ [true, false])))) [true, true]) := by
  rfl

/-- The other measured orbit turn, `t = 310271`: `u=72, m=29, w=309`, span
`6·(72+29)+15+2·309 = 1239`, measured 1239. -/
theorem turn_310271_via_law :
    steps dT 1239 (IN2 72 29 1 309 4 0 [true] [false, true])
      = some (IN 0 308 1 1 621
          (pow01 73 ++ (pow10 29 ++ (false :: true :: (ones 1 ++ [true])))) [false, true]) :=
  turnPhase 72 28 1 308 1 0 _ _

/-- The rung tile is the `w = 0` case of the turn phase, not a separate law: at `w = 0` the comb
is empty and `IN2 … 0 … = IN …` definitionally. -/
theorem tile_is_turn_at_w_zero (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    IN2 u m c 0 g p TAIL REST = IN u m c g p TAIL REST := rfl


/-! ### §5.1 The **leftward** turn phase (RF-4, part 2).

`d_rf4_left.py` reads the leftward turns as `rung0` (the rung with an exhausted comb) followed by
`descend` (`crawlFold ; crawl ; markerFold ; crawl`), and the head trajectory confirms the split:
the first piece advances `+3`, the second is a pure descent.  Both come from `RungCalc`; no new
atom.  The step budgets close exactly against the orbit — see `left_turn_budget_*` below. -/

/-- **The rung with an exhausted comb** (`m_literal = 0`), span `6u+15`, head `+3`.
This is the boundary case the `IN` family excludes, and every ladder segment ends in it. -/
theorem combExhausted (u : Nat) (p : Int) (W Z : List Bool) :
    steps dT (6 * u + 15)
        ⟨.A, p, ⟨pow10 u ++ (true :: true :: (false :: false :: W)),
                 false, true :: false :: false :: false :: Z⟩⟩
      = some ⟨.A, p + 3,
          ⟨true :: (pow01 (u + 2) ++ (false :: true :: W)), false, true :: Z⟩⟩ := by
  rw [show 6 * u + 15 = 4 * (u + 1) + 1 + 1 + 2 * (u + 3) + 3 from by omega]
  exact RungCalc.rung0 dAtoms u p W Z

/-- **The descent**, span `4(q+2) + (r+1)`, head `−2(q+1) − (r+1) − 2`. -/
theorem descent (q r : Nat) (p : Int) (b : Bool) (L R : List Bool) :
    steps dT (4 * (q + 2) + (r + 1))
        ⟨.A, p, ⟨pow10 q ++ (true :: true :: (ones r ++ (false :: true :: b :: L))), false, R⟩⟩
      = some ⟨.A, p - 2 * (q + 1) - (r + 1) - 2,
          ⟨L, b, true :: false :: (zeros (r + 1) ++ (true :: false :: (pow10 q ++ R)))⟩⟩ := by
  rw [show 4 * (q + 2) + (r + 1) = 4 * (q + 2) + 1 * (r + 1) from by omega]
  exact RungCalc.descend dAtoms q r p b L R

/-- Grounded: `combExhausted` at `u = 3` (span 33) as a closed kernel `rfl`. -/
theorem combExhausted_grounded :
    steps dT 33 ⟨.A, 0, ⟨pow10 3 ++ (true :: true :: (false :: false :: [true, false])),
                         false, true :: false :: false :: false :: [true, true]⟩⟩
      = some ⟨.A, 3, ⟨true :: (pow01 5 ++ (false :: true :: [true, false])),
                      false, true :: [true, true]⟩⟩ := by rfl

/-- Grounded: `descent` at `q = 3, r = 4` (span 25) as a closed kernel `rfl`. -/
theorem descent_grounded :
    steps dT 25 ⟨.A, 0, ⟨pow10 3 ++ (true :: true :: (ones 4 ++ (false :: true :: true :: [false]))),
                         false, [true, true]⟩⟩
      = some ⟨.A, -15, ⟨[false], true,
          true :: false :: (zeros 5 ++ (true :: false :: (pow10 3 ++ [true, true])))⟩⟩ := by rfl

/-- The same proposition from the law -- `descent 3 4 0 true [false] [true, true]` -- so the
grounded `rfl` and the `∀`-law are two independent proofs of one statement. -/
theorem descent_grounded_via_law :
    steps dT 25 ⟨.A, 0, ⟨pow10 3 ++ (true :: true :: (ones 4 ++ (false :: true :: true :: [false]))),
                         false, [true, true]⟩⟩
      = some ⟨.A, -15, ⟨[false], true,
          true :: false :: (zeros 5 ++ (true :: false :: (pow10 3 ++ [true, true])))⟩⟩ :=
  descent 3 4 0 true [false] [true, true]

/-- **Budget check against the real orbit.**  The leftward turn at `t = 1194806` is 1371 steps and
splits as `rung0 (u = 127)` then `descend (q = 130, r = 65)`.  If either law's span were off by a
step this would not hold. -/
theorem left_turn_budget_1194806 : (6 * 127 + 15) + (4 * (130 + 2) + (65 + 1)) = 1371 := by rfl

/-- The same for the other leftward turn, `t = 1168982`, 6504 steps: `rung0 (u = 616)` then
`descend (q = 619, r = 308)`. -/
theorem left_turn_budget_1168982 : (6 * 616 + 15) + (4 * (619 + 2) + (308 + 1)) = 6504 := by rfl


/-- **A second `swap10` anchor.**  `D`'s epoch-entry turn runs a `1 0 → 0 1` sweep in state `D`
(`D1→0RF`, `F0→1RD`) rather than in the return state `B`.  Measured once per epoch
(`d_rf4_epochs.py`: the `(DF)^n` runs).  Only `swap10` holds at `D` — `swap01` does not, since
`D0 → 1LA` moves left — so this is a *partial* atom set, which is exactly why `sweep10At` takes
the atom rather than the whole `Atoms`. -/
theorem swapD (p : Int) (b : Bool) (L R : List Bool) :
    steps dT 2 ⟨.D, p, ⟨L, true, false :: b :: R⟩⟩
      = some ⟨.D, p + 2, ⟨true :: false :: L, b, R⟩⟩ := by
  rw [show (p + 2 : Int) = p + 1 + 1 from by omega]
  rfl

/-- The `(DF)^{k+1}` run, folded. -/
theorem sweepD (k : Nat) (p : Int) (b : Bool) (L R : List Bool) :
    steps dT (2 * (k + 1)) ⟨.D, p, ⟨L, true, false :: (pow10 k ++ b :: R)⟩⟩
      = some ⟨.D, p + 2 * k + 2, ⟨pow10 (k + 1) ++ L, b, R⟩⟩ :=
  RungCalc.sweep10At swapD k p b L R

/-- Grounded: the `(DF)^4` run of the `k=5` epoch-entry turn, as a kernel `rfl`. -/
theorem sweepD_grounded :
    steps dT 8 ⟨.D, 0, ⟨[true, false], true, false :: (pow10 3 ++ (true :: [false]))⟩⟩
      = some ⟨.D, 8, ⟨pow10 4 ++ [true, false], true, [false]⟩⟩ := by rfl


/-! ### §5.2 The ladder segment.

A whole ladder — `n` consecutive rungs — as one law, from `RungCalc.tileIter`.  The spans below
are the **measured** `k = 4` ladder segments (`d_rf4_epochs.py`), and `ladderSpan` reproduces each
exactly; the 308-rung one is the epoch's main segment. -/

/-- **D's ladder segment**, `∀ n u m c g p TAIL REST`. -/
theorem ladder (n u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps dT (ladderSpan 4 1 1 2 2 3 u m n) (IN u (m + n) c (g + 3 * n) p TAIL REST)
      = some (IN (u + 2 * n) m (c + n) g (p + 3 * n) TAIL REST) :=
  RungCalc.tileIter dAtoms n u m c g p TAIL REST

/-- The six measured `k = 4` ladder spans, reproduced by `ladderSpan`.  The `IN` parameters are
those measured at each segment's start; a drift in `span` or in the iterate would break these. -/
theorem ladderSpans_measured :
    ladderSpan 4 1 1 2 2 3 0 0 2 = 60 ∧ ladderSpan 4 1 1 2 2 3 1 2 4 = 264
      ∧ ladderSpan 4 1 1 2 2 3 0 29 36 = 18360 ∧ ladderSpan 4 1 1 2 2 3 0 0 308 = 857472
      ∧ ladderSpan 4 1 1 2 2 3 71 0 28 = 19320 ∧ ladderSpan 4 1 1 2 2 3 8 0 1 = 69 := by
  refine ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- The main segment as a single application: 308 rungs, 857,472 steps, `IN 0 308 1 (g+924)`
to `IN 616 0 309 g`, head `+924`. -/
theorem ladder_main (g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps dT 857472 (IN 0 308 1 (g + 924) p TAIL REST)
      = some (IN 616 0 309 g (p + 924) TAIL REST) := by
  have h := ladder 308 0 0 1 g p TAIL REST
  rw [show ladderSpan 4 1 1 2 2 3 0 0 308 = 857472 from by rfl] at h
  rw [show (0 : Nat) + 308 = 308 from by omega, show 3 * 308 = 924 from by omega,
      show (0 : Nat) + 2 * 308 = 616 from by omega, show (1 : Nat) + 308 = 309 from by omega,
      show (3 : Int) * ((308 : Nat) : Int) = 924 from by omega] at h
  exact h

/-! ## §6 Kernel-grounded instances (anti-vacuity + the tile at concrete levels).

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
atom decomposition `(ABED)³ · A · (ABED)³ · A · BC · (BE)³ · (BC)⁵ · D`. -/
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

/-! ### §6.1 Law-vs-kernel cross-check.

Each of the three `tile_*` statements above is proven a *second* time, now as an instance of the
`∀`-law.  The two proofs share nothing: the `rfl` ones are the kernel executing `dT`, the ones
below are `RungCalc.rung_core`'s nine-phase composition.  Because the *statements* are literally
the same propositions, a one-step drift in the law's span arithmetic, or a one-cell drift in its
word bookkeeping, would stop these from typechecking. -/

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

/-- The law also fires where the old `c + 1` shape could not state it: `c = 0`, i.e. with the
`1`-counter empty and `TAIL` pressed right up against the `0 0` gap. -/
theorem tile_c_zero :
    steps dT 33 (IN 1 2 0 3 0 [true, true] [true]) = some (IN 3 1 1 0 3 [true, true] [true]) :=
  rungTile 1 1 0 0 0 _ _

-- AXIOM AUDIT — everything here must be `[propext, Quot.sound]` or axiom-free.
#print axioms dAtoms
#print axioms rungTile
#print axioms turnPhase
#print axioms turn_291698_via_law
#print axioms turn_291698_kernel
#print axioms turn_310271_via_law
#print axioms combExhausted
#print axioms descent
#print axioms combExhausted_grounded
#print axioms descent_grounded
#print axioms swapD
#print axioms sweepD
#print axioms ladder
#print axioms ladderSpans_measured
#print axioms ladder_main
#print axioms rungTile_holds
#print axioms anchor160
#print axioms tile_1_2_2_4
#print axioms tile_2_3_2_4_via_law
#print axioms tile_span_control

end DMachine
