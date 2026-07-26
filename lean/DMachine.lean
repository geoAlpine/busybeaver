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

/-! ## §4 Kernel-grounded instances (anti-vacuity + the tile at concrete levels).

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

/-! ### §4.1 Law-vs-kernel cross-check.

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
#print axioms rungTile_holds
#print axioms anchor160
#print axioms tile_1_2_2_4
#print axioms tile_2_3_2_4_via_law
#print axioms tile_span_control

end DMachine
