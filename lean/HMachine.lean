import RungCalc

set_option maxRecDepth 4000000
set_option maxHeartbeats 1000000

/-!
# `H` — the rung tile, obtained for free from `RungCalc`

`H = 1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---` is a 1104-holdout entry of the BB(6) residual,
`[OPEN]`.  This file supplies the machine and discharges `RungCalc.Atoms` for it — six closed
kernel `rfl`s — and the rung tile follows.

## What this file settles, and what it does not

**Settles.**  A's claim that `H` is a *cheap same-species re-instantiation* of `D` was demoted
to `[unverified]` when `D` turned out to be a cascade rather than a pure comb.  It is now
`[MEASURED and PROVEN]` **for the rung tile specifically**, and in a stronger form than the
original claim:

* `H`'s transition graph is **not** a relabeling of `D`'s.  An exhaustive search over state
  permutations, in both orientations (`D`/`Dᴿ` against `H`/`Hᴿ`), returns **zero** isomorphisms
  (`h_vs_d_tile.py §1`).  So the mechanism that made `C` free — *`C` was `x2`'s graph* — does
  **not** apply here.
* Nevertheless all four distinct tile atoms occur in `H` (`h_vs_d_tile.py §2`), and the tile
  fires verbatim: **23040/23040** on the same grid `D`'s proof was verified on, including
  `c = 0` and hostile `TAIL`/`REST`, with the `g = 0,1,2` and span+1 controls failing as
  required (`h_tile_fire.py §C,§D`).
* `H` *splits* a state that `D` reuses: `Dᴿ`'s `D` is entered from `E` inside the crawl and from
  `C` inside the turn, and `H` uses `F` and `C` for those two roles.  The state correspondence
  is therefore not a function — but the *atoms* match, which is all `RungCalc.Atoms` asks.

**Does not settle.**  `H` remains **`[OPEN]`**.  The tile is one lemma.  `H`'s own epoch
anatomy, entry segment, milestone family and cascade-level induction are all unmeasured here —
nothing in this file is evidence about them, and the honest reading of the D experience is that
the tile was the *cheap* part.  No machine is decided; no label is upgraded.

Zero-Mathlib, core only.  No `sorry`, no `native_decide`, no `decide`.
-/

namespace HMachine

open TapeCalc RungCalc

/-! ## §1 The machine. -/

inductive St | A | B | C | D | E | F
deriving DecidableEq, Repr

/-- `H = 1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---`.
`none` = HALT, which happens exactly when `F` reads `1`.  `H` grows rightward as written, so —
unlike `D` — no mirroring is needed. -/
def hT : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true,  .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .R, .E)   -- A1 → 0RE
  | .B, false => some (false, .R, .C)   -- B0 → 0RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (true,  .L, .D)   -- C0 → 1LD
  | .C, true  => some (true,  .R, .E)   -- C1 → 1RE
  | .D, false => some (true,  .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .L, .D)   -- D1 → 0LD
  | .E, false => some (true,  .R, .A)   -- E0 → 1RA
  | .E, true  => some (false, .L, .F)   -- E1 → 0LF
  | .F, false => some (true,  .L, .D)   -- F0 → 1LD
  | .F, true  => none                   -- F1 → --- HALT

/-- The blank-tape start configuration. -/
def init : Cfg St := ⟨.A, 0, ⟨[], false, []⟩⟩

/-! ## §2 The six atoms.

`H`'s outward-sweep state is `D` and its return-sweep state is `A` (in `D`'s file these are
`A` and `B`).  Each atom is a closed `rfl` on the genuine machine, so any drift in `hT` breaks
the build.  Written out, the walks are:

| atom | `H`'s walk | `Dᴿ`'s walk |
|---|---|---|
| `crawl` | `D0→1LA`, `A1→0RE`, `E1→0LF`, `F0→1LD` | `A0→1LB`, `B1→0RE`, `E1→0LD`, `D0→1LA` |
| `marker` | `D1→0LD` | `A1→0LA` |
| `turnaround` | `D0→1LA` | `A0→1LB` |
| `swap10` | `A1→0RE`, `E0→1RA` | `B1→0RE`, `E0→1RB` |
| `swap01` | `A0→1RB`, `B1→0RA` | `B0→1RC`, `C1→0RB` |
| `turn` | `A0→1RB`, `B0→0RC`, `C0→1LD` | `B0→1RC`, `C0→0RD`, `D0→1LA` |

Note `H`'s `D` appears in both `crawl` (as the closing state, from `F`) and `marker`, while
`Dᴿ`'s single state `D` covers what `H` splits between `F` and `C`. -/
theorem hAtoms : Atoms hT .D .A 4 1 1 2 2 3 where
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

/-! ## §3 The rung tile, for free. -/

/-- `H`'s milestone-region configuration family: `RungCalc.IN` at `H`'s outward state. -/
abbrev IN (u m c g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg St :=
  RungCalc.IN St.D u m c g p TAIL REST

/-- **`H`'s rung tile — `[PROVEN]`, `∀ u m c g p TAIL REST`.**  Not one line of the nine-phase
composition is repeated here; it comes from `RungCalc.tile` applied to `hAtoms`. -/
theorem rungTile (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps hT (6 * (u + m) + 21) (IN u (m + 1) c (g + 3) p TAIL REST)
      = some (IN (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * (u + m) + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact RungCalc.tile hAtoms u m c g p TAIL REST

theorem rungTile_holds : Tile hT St.D (span 4 1 1 2 2 3) := tile_holds hAtoms

/-! ## §3.1 The turn phase (RF-4), for free.

`RungCalc.tile2` is the rung with the return sweep crossing a `(1 0)^w` comb — the shape `D`'s
inter-segment turn phases actually have.  `H` inherits it from the same `hAtoms`; not one line of
the composition is repeated. -/

abbrev IN2 (u m c w g : Nat) (p : Int) (TAIL REST : List Bool) : Cfg St :=
  RungCalc.IN2 St.D u m c w g p TAIL REST

/-- **`H`'s turn phase — `[PROVEN]`, `∀ u m c w g p TAIL REST`.** -/
theorem turnPhase (u m c w g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps hT (6 * (u + m) + 21 + 2 * (w + 1)) (IN2 u (m + 1) c (w + 1) (g + 3) p TAIL REST)
      = some (IN 0 w 1 g (p + 3 + 2 * (w + 1))
          (pow01 (u + 1) ++ (pow10 (m + 1) ++ (false :: true :: (ones c ++ TAIL)))) REST) := by
  rw [show 6 * (u + m) + 21 + 2 * (w + 1) = span 4 1 1 2 2 3 u m + 2 * (w + 1)
      from by simp [span]; omega]
  exact RungCalc.tile2 hAtoms u m c w g p TAIL REST

/-- Grounded: `H`'s turn phase at `u=1, m=2, w=2, g=3`, span `6·3+15+4 = 37`, kernel `rfl`. -/
theorem turn_grounded :
    steps hT 37 (IN2 1 2 2 2 3 0 [true, false] [true, true])
      = some (IN 0 1 1 0 7
          (pow01 2 ++ (pow10 2 ++ (false :: true :: (ones 2 ++ [true, false])))) [true, true]) := by
  rfl

/-! ## §4 Kernel-grounded instances (anti-vacuity).

The law above is a composition; these are the kernel executing `hT`.  Same propositions, two
independent proofs — a one-step drift in either would stop the build. -/

/-- Anti-vacuity: `H`'s **real blank-tape orbit** is in the tile's own configuration family
after 17 steps — state `D` at `pos 5`, left `1 1 0 1 0 0 1`, head `0`, right `1`.  That left
word is exactly `IN`'s at `u=0, m=1, c=1`.  (The trailing blanks are hooked up through
`TapeCalc.steps_runpad_zeros`, as in the `x2` and `C` developments.) -/
theorem anchor17 :
    steps hT 17 init
      = some ⟨.D, 5, ⟨pow10 0 ++ [true, true] ++ pow01 1 ++ [false, false] ++ ones 1,
                      false, [true]⟩⟩ := by rfl

/-- The crawl atom fires on the real orbit shape. -/
theorem crawl_grounded :
    steps hT 4 ⟨.D, 0, ⟨pow10 1 ++ [true, true], false, []⟩⟩
      = some ⟨.D, -2, ⟨[true, true], false, pow10 1⟩⟩ := by rfl

/-- Tile at `u=0, m=1, c=1, g=3`, span `21` (the `g`-floor case). -/
theorem tile_0_1_1_3 :
    steps hT 21 (IN 0 1 1 3 0 [] []) = some (IN 2 0 2 0 3 [] []) := by rfl

/-- Tile at `u=1, m=2, c=2, g=4`, span `33`, with non-trivial `TAIL`/`REST`. -/
theorem tile_1_2_2_4 :
    steps hT 33 (IN 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-- Tile at `u=2, m=3, c=2, g=4`, span `45` — the level whose `H` itinerary is
`(DAEF)³ · D · (DAEF)³ · D · AB · (AE)³ · (AB)⁵ · C`, the same word as `Dᴿ`'s
`(ABED)³ · A · (ABED)³ · A · BC · (BE)³ · (BC)⁵ · D`. -/
theorem tile_2_3_2_4 :
    steps hT 45 (IN 2 3 2 4 0 [true, false, true, true, false] [true, true, false, true])
      = some (IN 4 2 3 1 3 [true, false, true, true, false] [true, true, false, true]) := by
  rfl

/-- **The span control.**  One step past the span the machine is in `A` at `pos 2`, not `D` at
`pos 3` — the span law is exact, not an inequality. -/
theorem tile_span_control :
    (steps hT 22 (IN 0 1 1 3 0 [] [])).map (fun c => (c.st, c.pos))
      = some (St.A, (2 : Int)) := by rfl

/-! ### §4.1 Law-vs-kernel cross-check. -/

theorem tile_0_1_1_3_via_law :
    steps hT 21 (IN 0 1 1 3 0 [] []) = some (IN 2 0 2 0 3 [] []) :=
  rungTile 0 0 1 0 0 [] []

theorem tile_2_3_2_4_via_law :
    steps hT 45 (IN 2 3 2 4 0 [true, false, true, true, false] [true, true, false, true])
      = some (IN 4 2 3 1 3 [true, false, true, true, false] [true, true, false, true]) :=
  rungTile 2 2 2 1 0 _ _

/-- `c = 0`: the `1`-counter is never read, on `H` as on `D`. -/
theorem tile_c_zero :
    steps hT 33 (IN 1 2 0 3 0 [true, true] [true]) = some (IN 3 1 1 0 3 [true, true] [true]) :=
  rungTile 1 1 0 0 0 _ _

-- AXIOM AUDIT
#print axioms hAtoms
#print axioms rungTile
#print axioms turnPhase
#print axioms turn_grounded
#print axioms rungTile_holds
#print axioms anchor17
#print axioms tile_2_3_2_4
#print axioms tile_2_3_2_4_via_law
#print axioms tile_span_control

end HMachine
