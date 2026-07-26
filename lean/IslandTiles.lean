import RungCalc

set_option maxRecDepth 4000000
set_option maxHeartbeats 1000000

/-!
# The rung tile for every `Atoms`-satisfying machine in the BB(6) residual

**MACHINE-GENERATED** by `gen_island_tiles.py`; regenerate rather than hand-edit.

`atoms_island_scan.py` scanned the curated still-open residual
(`_bbdata/bb6_holdouts_1104.txt`, 1104 entries) for machines satisfying
`RungCalc.Atoms`, in either orientation, at any state.  **18 of 1104 do.**  Since
`RungCalc.tile` proves the rung tile from `Atoms` alone, each of them gets the tile for six
closed kernel `rfl`s — which is what this file spends.

Detection is **behavioural** (`atoms_flex_scan.py`): each atom is matched by its exact
input/output configuration at whatever step count the machine takes, and the count must
agree across several tape contexts.  Step counts are not part of the mechanism — the fixed
`(4,1,1,2,2,3)` of the first scan was an accident of `D`.  Distribution over the residual:
`6/6: 18`, `5/6: 0`, `4/6: 4`, `3/6: 36`, `2/6: 401`, `1/6: 645`.  **No 5/6 near-miss
remains**, so this relaxation is exhausted: no further machine is within one atom.

Seventeen hits have `D`'s step counts `(4,1,1,2,2,3)`, span `6(u+m)+21`; one
(`1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC`, `sA = E`) has a **five**-step turn
(`A0→1RB, B0→0LC, C1→1RD, D0→0RC, C0→1LE`) reaching the identical output configuration,
giving `(4,1,1,2,2,5)` and span `6(u+m)+23`.  It was the fixed-shape scan's lone 5/6.

## How to read this, and how not to

**What it shows.** The machine-independent tile is not a one-machine coincidence: it covers
18 still-open machines, and the per-machine cost really is six `rfl`s.  Among the named
island candidates, `D`, `E` and `H` are hits; `x2` (1/6), `F` (2/6), `G` (2/6) and `I` (1/6)
are not — so this tile is *not* x2's mechanism.

**What it does not show.**  `Atoms` pins 9–10 of a 6-state machine's 12 transition entries
(10 when the roles `sA, b, e, d, c, f` are distinct, 9 when `d = f`), so the family it
describes is structurally narrow by construction; the hits differ only in the 2–3 entries
`Atoms` leaves free, and in the role coincidences.  The tile is one
lemma.  **None of these machines is decided by this file**, and nothing here bears on their
epoch anatomy, entry segments, milestone families or cascade inductions — for `D`, that
remainder is where all the difficulty turned out to live.  Every machine below is `[OPEN]`.

Zero-Mathlib, core only.  No `sorry`, no `native_decide`, no `decide`.
-/

namespace IslandTiles

open TapeCalc RungCalc

/-- One six-element state type shared by every machine below. -/
inductive St | A | B | C | D | E | F
deriving DecidableEq, Repr

/-! ## §1 `M01` — `1RB0RE_0RC0RA_1LD1RF_1LA0LD_1RA0LC_1RE---` -/

/-- `1RB0RE_0RC0RA_1LD1RF_1LA0LD_1RA0LC_1RE---`.
Transcribed as written — the atoms hold in this orientation. -/
def TM01 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .R, .E)   -- A1 → 0RE
  | .B, false => some (false, .R, .C)   -- B0 → 0RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (true , .L, .D)   -- C0 → 1LD
  | .C, true  => some (true , .R, .F)   -- C1 → 1RF
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .L, .D)   -- D1 → 0LD
  | .E, false => some (true , .R, .A)   -- E0 → 1RA
  | .E, true  => some (false, .L, .C)   -- E1 → 0LC
  | .F, false => some (true , .R, .E)   -- F0 → 1RE
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM01 : Atoms TM01 .D .A 4 1 1 2 2 3 where
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

/-- The rung tile for `M01`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM01 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM01 (6 * u + 6 * m + 21)
        (IN St.D u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.D (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM01 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM01 :
    steps TM01 33 (IN St.D 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.D 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §2 `M02` — `1RB0LD_1RC0RA_0RD0RB_1LE1RF_1LB0LE_1RA---` -/

/-- `1RB0LD_1RC0RA_0RD0RB_1LE1RF_1LB0LE_1RA---`.
Transcribed as written — the atoms hold in this orientation. -/
def TM02 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .L, .D)   -- A1 → 0LD
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true , .L, .E)   -- D0 → 1LE
  | .D, true  => some (true , .R, .F)   -- D1 → 1RF
  | .E, false => some (true , .L, .B)   -- E0 → 1LB
  | .E, true  => some (false, .L, .E)   -- E1 → 0LE
  | .F, false => some (true , .R, .A)   -- F0 → 1RA
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = E` (outward sweep), `sB = B` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM02 : Atoms TM02 .E .B 4 1 1 2 2 3 where
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

/-- The rung tile for `M02`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM02 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM02 (6 * u + 6 * m + 21)
        (IN St.E u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.E (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM02 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM02 :
    steps TM02 33 (IN St.E 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.E 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §3 `M03` — `1RB---_1LC0RA_1LD0LC_1RE0RF_0RB0RD_1RD0LB` -/

/-- `1RB---_1LC0RA_1LD0LC_1RE0RF_0RB0RD_1RD0LB`.
Transcribed as written — the atoms hold in this orientation. -/
def TM03 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => none                    -- A1 → --- HALT
  | .B, false => some (true , .L, .C)   -- B0 → 1LC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (true , .L, .D)   -- C0 → 1LD
  | .C, true  => some (false, .L, .C)   -- C1 → 0LC
  | .D, false => some (true , .R, .E)   -- D0 → 1RE
  | .D, true  => some (false, .R, .F)   -- D1 → 0RF
  | .E, false => some (false, .R, .B)   -- E0 → 0RB
  | .E, true  => some (false, .R, .D)   -- E1 → 0RD
  | .F, false => some (true , .R, .D)   -- F0 → 1RD
  | .F, true  => some (false, .L, .B)   -- F1 → 0LB

/-- Roles: `sA = C` (outward sweep), `sB = D` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM03 : Atoms TM03 .C .D 4 1 1 2 2 3 where
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

/-- The rung tile for `M03`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM03 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM03 (6 * u + 6 * m + 21)
        (IN St.C u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.C (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM03 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM03 :
    steps TM03 33 (IN St.C 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.C 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §4 `M04` — `1RB0LF_1RC0RB_1LD0LE_0LA0LC_1LC0RA_1LA---` -/

/-- `1RB0LF_1RC0RB_1LD0LE_0LA0LC_1LC0RA_1LA---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM04 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (false, .R, .F)   -- A1 → 0RF
  | .B, false => some (true , .L, .C)   -- B0 → 1LC
  | .B, true  => some (false, .L, .B)   -- B1 → 0LB
  | .C, false => some (true , .R, .D)   -- C0 → 1RD
  | .C, true  => some (false, .R, .E)   -- C1 → 0RE
  | .D, false => some (false, .R, .A)   -- D0 → 0RA
  | .D, true  => some (false, .R, .C)   -- D1 → 0RC
  | .E, false => some (true , .R, .C)   -- E0 → 1RC
  | .E, true  => some (false, .L, .A)   -- E1 → 0LA
  | .F, false => some (true , .R, .A)   -- F0 → 1RA
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM04 : Atoms TM04 .B .C 4 1 1 2 2 3 where
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

/-- The rung tile for `M04`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM04 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM04 (6 * u + 6 * m + 21)
        (IN St.B u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.B (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM04 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM04 :
    steps TM04 33 (IN St.B 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.B 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §5 `M05` — `1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---`   (D  (lean/DMachine.lean)) -/

/-- `1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---`, i.e. D  (lean/DMachine.lean).
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM05 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (false, .L, .A)   -- A1 → 0LA
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .E)   -- B1 → 0RE
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .R, .F)   -- D1 → 0RF
  | .E, false => some (true , .R, .B)   -- E0 → 1RB
  | .E, true  => some (false, .L, .D)   -- E1 → 0LD
  | .F, false => some (true , .R, .D)   -- F0 → 1RD
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM05 : Atoms TM05 .A .B 4 1 1 2 2 3 where
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

/-- The rung tile for `M05`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM05 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM05 (6 * u + 6 * m + 21)
        (IN St.A u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.A (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM05 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM05 :
    steps TM05 33 (IN St.A 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.A 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §6 `M06` — `1RB0RA_1LC0LE_0LD0LB_1RA1LE_1LB0RF_1RA---` -/

/-- `1RB0RA_1LC0LE_0LD0LB_1RA1LE_1LB0RF_1RA---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM06 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (false, .L, .A)   -- A1 → 0LA
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .E)   -- B1 → 0RE
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (true , .R, .E)   -- D1 → 1RE
  | .E, false => some (true , .R, .B)   -- E0 → 1RB
  | .E, true  => some (false, .L, .F)   -- E1 → 0LF
  | .F, false => some (true , .L, .A)   -- F0 → 1LA
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM06 : Atoms TM06 .A .B 4 1 1 2 2 3 where
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

/-- The rung tile for `M06`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM06 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM06 (6 * u + 6 * m + 21)
        (IN St.A u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.A (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM06 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM06 :
    steps TM06 33 (IN St.A 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.A 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §7 `M07` — `1RB1LF_1RC0RB_1LD0LE_0LA0LC_1LC0RA_1LE---` -/

/-- `1RB1LF_1RC0RB_1LD0LE_0LA0LC_1LC0RA_1LE---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM07 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (true , .R, .F)   -- A1 → 1RF
  | .B, false => some (true , .L, .C)   -- B0 → 1LC
  | .B, true  => some (false, .L, .B)   -- B1 → 0LB
  | .C, false => some (true , .R, .D)   -- C0 → 1RD
  | .C, true  => some (false, .R, .E)   -- C1 → 0RE
  | .D, false => some (false, .R, .A)   -- D0 → 0RA
  | .D, true  => some (false, .R, .C)   -- D1 → 0RC
  | .E, false => some (true , .R, .C)   -- E0 → 1RC
  | .E, true  => some (false, .L, .A)   -- E1 → 0LA
  | .F, false => some (true , .R, .E)   -- F0 → 1RE
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM07 : Atoms TM07 .B .C 4 1 1 2 2 3 where
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

/-- The rung tile for `M07`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM07 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM07 (6 * u + 6 * m + 21)
        (IN St.B u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.B (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM07 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM07 :
    steps TM07 33 (IN St.B 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.B 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §8 `M08` — `1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_1RC---`   (E  (island candidate E)) -/

/-- `1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_1RC---`, i.e. E  (island candidate E).
Transcribed as written — the atoms hold in this orientation. -/
def TM08 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .R, .E)   -- A1 → 0RE
  | .B, false => some (false, .R, .C)   -- B0 → 0RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (true , .L, .D)   -- C0 → 1LD
  | .C, true  => some (false, .R, .F)   -- C1 → 0RF
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .L, .D)   -- D1 → 0LD
  | .E, false => some (true , .R, .A)   -- E0 → 1RA
  | .E, true  => some (false, .L, .C)   -- E1 → 0LC
  | .F, false => some (true , .R, .C)   -- F0 → 1RC
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM08 : Atoms TM08 .D .A 4 1 1 2 2 3 where
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

/-- The rung tile for `M08`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM08 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM08 (6 * u + 6 * m + 21)
        (IN St.D u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.D (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM08 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM08 :
    steps TM08 33 (IN St.D 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.D 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §9 `M09` — `1RB1LE_1RC0RB_1LD0LE_0LA0LC_1LC0RF_1RB---` -/

/-- `1RB1LE_1RC0RB_1LD0LE_0LA0LC_1LC0RF_1RB---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM09 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (true , .R, .E)   -- A1 → 1RE
  | .B, false => some (true , .L, .C)   -- B0 → 1LC
  | .B, true  => some (false, .L, .B)   -- B1 → 0LB
  | .C, false => some (true , .R, .D)   -- C0 → 1RD
  | .C, true  => some (false, .R, .E)   -- C1 → 0RE
  | .D, false => some (false, .R, .A)   -- D0 → 0RA
  | .D, true  => some (false, .R, .C)   -- D1 → 0RC
  | .E, false => some (true , .R, .C)   -- E0 → 1RC
  | .E, true  => some (false, .L, .F)   -- E1 → 0LF
  | .F, false => some (true , .L, .B)   -- F0 → 1LB
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM09 : Atoms TM09 .B .C 4 1 1 2 2 3 where
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

/-- The rung tile for `M09`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM09 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM09 (6 * u + 6 * m + 21)
        (IN St.B u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.B (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM09 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM09 :
    steps TM09 33 (IN St.B 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.B 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §10 `M10` — `1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_0RC---` -/

/-- `1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_0RC---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM10 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (false, .L, .A)   -- A1 → 0LA
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .E)   -- B1 → 0RE
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .R, .F)   -- D1 → 0RF
  | .E, false => some (true , .R, .B)   -- E0 → 1RB
  | .E, true  => some (false, .L, .D)   -- E1 → 0LD
  | .F, false => some (false, .L, .C)   -- F0 → 0LC
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM10 : Atoms TM10 .A .B 4 1 1 2 2 3 where
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

/-- The rung tile for `M10`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM10 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM10 (6 * u + 6 * m + 21)
        (IN St.A u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.A (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM10 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM10 :
    steps TM10 33 (IN St.A 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.A 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §11 `M11` — `1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_0RD---` -/

/-- `1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_0RD---`.
Transcribed as written — the atoms hold in this orientation. -/
def TM11 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .R, .E)   -- A1 → 0RE
  | .B, false => some (false, .R, .C)   -- B0 → 0RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (true , .L, .D)   -- C0 → 1LD
  | .C, true  => some (false, .R, .F)   -- C1 → 0RF
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .L, .D)   -- D1 → 0LD
  | .E, false => some (true , .R, .A)   -- E0 → 1RA
  | .E, true  => some (false, .L, .C)   -- E1 → 0LC
  | .F, false => some (false, .R, .D)   -- F0 → 0RD
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM11 : Atoms TM11 .D .A 4 1 1 2 2 3 where
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

/-- The rung tile for `M11`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM11 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM11 (6 * u + 6 * m + 21)
        (IN St.D u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.D (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM11 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM11 :
    steps TM11 33 (IN St.D 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.D 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §12 `M12` — `1RB---_1RC0LE_1RD0RB_0RE0RC_1LF1RA_1LC0LF` -/

/-- `1RB---_1RC0LE_1RD0RB_0RE0RC_1LF1RA_1LC0LF`.
Transcribed as written — the atoms hold in this orientation. -/
def TM12 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => none                    -- A1 → --- HALT
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .L, .E)   -- B1 → 0LE
  | .C, false => some (true , .R, .D)   -- C0 → 1RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (false, .R, .E)   -- D0 → 0RE
  | .D, true  => some (false, .R, .C)   -- D1 → 0RC
  | .E, false => some (true , .L, .F)   -- E0 → 1LF
  | .E, true  => some (true , .R, .A)   -- E1 → 1RA
  | .F, false => some (true , .L, .C)   -- F0 → 1LC
  | .F, true  => some (false, .L, .F)   -- F1 → 0LF

/-- Roles: `sA = F` (outward sweep), `sB = C` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM12 : Atoms TM12 .F .C 4 1 1 2 2 3 where
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

/-- The rung tile for `M12`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM12 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM12 (6 * u + 6 * m + 21)
        (IN St.F u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.F (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM12 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM12 :
    steps TM12 33 (IN St.F 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.F 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §13 `M13` — `1RB0LF_1RC0RA_0RD0RB_1LE1RA_1LB0LE_1LE---` -/

/-- `1RB0LF_1RC0RA_0RD0RB_1LE1RA_1LB0LE_1LE---`.
Transcribed as written — the atoms hold in this orientation. -/
def TM13 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .L, .F)   -- A1 → 0LF
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true , .L, .E)   -- D0 → 1LE
  | .D, true  => some (true , .R, .A)   -- D1 → 1RA
  | .E, false => some (true , .L, .B)   -- E0 → 1LB
  | .E, true  => some (false, .L, .E)   -- E1 → 0LE
  | .F, false => some (true , .L, .E)   -- F0 → 1LE
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = E` (outward sweep), `sB = B` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM13 : Atoms TM13 .E .B 4 1 1 2 2 3 where
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

/-- The rung tile for `M13`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM13 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM13 (6 * u + 6 * m + 21)
        (IN St.E u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.E (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM13 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM13 :
    steps TM13 33 (IN St.E 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.E 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §14 `M14` — `1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---`   (H  (lean/HMachine.lean)) -/

/-- `1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---`, i.e. H  (lean/HMachine.lean).
Transcribed as written — the atoms hold in this orientation. -/
def TM14 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .R, .E)   -- A1 → 0RE
  | .B, false => some (false, .R, .C)   -- B0 → 0RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (true , .L, .D)   -- C0 → 1LD
  | .C, true  => some (true , .R, .E)   -- C1 → 1RE
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (false, .L, .D)   -- D1 → 0LD
  | .E, false => some (true , .R, .A)   -- E0 → 1RA
  | .E, true  => some (false, .L, .F)   -- E1 → 0LF
  | .F, false => some (true , .L, .D)   -- F0 → 1LD
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM14 : Atoms TM14 .D .A 4 1 1 2 2 3 where
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

/-- The rung tile for `M14`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM14 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM14 (6 * u + 6 * m + 21)
        (IN St.D u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.D (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM14 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM14 :
    steps TM14 33 (IN St.D 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.D 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §15 `M15` — `1RB0LF_1RC0RB_1LD0LE_0LA0LC_1LC0RA_0RD---` -/

/-- `1RB0LF_1RC0RB_1LD0LE_0LA0LC_1LC0RA_0RD---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM15 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (false, .R, .F)   -- A1 → 0RF
  | .B, false => some (true , .L, .C)   -- B0 → 1LC
  | .B, true  => some (false, .L, .B)   -- B1 → 0LB
  | .C, false => some (true , .R, .D)   -- C0 → 1RD
  | .C, true  => some (false, .R, .E)   -- C1 → 0RE
  | .D, false => some (false, .R, .A)   -- D0 → 0RA
  | .D, true  => some (false, .R, .C)   -- D1 → 0RC
  | .E, false => some (true , .R, .C)   -- E0 → 1RC
  | .E, true  => some (false, .L, .A)   -- E1 → 0LA
  | .F, false => some (false, .L, .D)   -- F0 → 0LD
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM15 : Atoms TM15 .B .C 4 1 1 2 2 3 where
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

/-- The rung tile for `M15`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM15 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM15 (6 * u + 6 * m + 21)
        (IN St.B u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.B (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM15 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM15 :
    steps TM15 33 (IN St.B 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.B 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §16 `M16` — `1RB0LF_1RC0RA_0RD0RB_1LE0RF_1LB0LE_1LE---` -/

/-- `1RB0LF_1RC0RA_0RD0RB_1LE0RF_1LB0LE_1LE---`.
Transcribed as written — the atoms hold in this orientation. -/
def TM16 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .L, .F)   -- A1 → 0LF
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true , .L, .E)   -- D0 → 1LE
  | .D, true  => some (false, .R, .F)   -- D1 → 0RF
  | .E, false => some (true , .L, .B)   -- E0 → 1LB
  | .E, true  => some (false, .L, .E)   -- E1 → 0LE
  | .F, false => some (true , .L, .E)   -- F0 → 1LE
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = E` (outward sweep), `sB = B` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM16 : Atoms TM16 .E .B 4 1 1 2 2 3 where
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

/-- The rung tile for `M16`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM16 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM16 (6 * u + 6 * m + 21)
        (IN St.E u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.E (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM16 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM16 :
    steps TM16 33 (IN St.E 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.E 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §17 `M17` — `1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC` -/

/-- `1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC`.
Transcribed as written — the atoms hold in this orientation. -/
def TM17 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .R, .B)   -- A0 → 1RB
  | .A, true  => some (false, .R, .F)   -- A1 → 0RF
  | .B, false => some (false, .L, .C)   -- B0 → 0LC
  | .B, true  => some (false, .R, .A)   -- B1 → 0RA
  | .C, false => some (true , .L, .E)   -- C0 → 1LE
  | .C, true  => some (true , .R, .D)   -- C1 → 1RD
  | .D, false => some (false, .R, .C)   -- D0 → 0RC
  | .D, true  => none                    -- D1 → --- HALT
  | .E, false => some (true , .L, .A)   -- E0 → 1LA
  | .E, true  => some (false, .L, .E)   -- E1 → 0LE
  | .F, false => some (true , .R, .A)   -- F0 → 1RA
  | .F, true  => some (false, .L, .C)   -- F1 → 0LC

/-- Roles: `sA = E` (outward sweep), `sB = A` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 5)` ⇒ span `6u + 6m + 23`. -/
theorem AM17 : Atoms TM17 .E .A 4 1 1 2 2 5 where
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
    rw [show (p + 1 : Int) = p + 1 - 1 + 1 + 1 - 1 from by omega]
    rfl

/-- The rung tile for `M17`, `∀ u m c g p TAIL REST`, span `6u + 6m + 23`. -/
theorem tileM17 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM17 (6 * u + 6 * m + 23)
        (IN St.E u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.E (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 23 = span 4 1 1 2 2 5 u m from by simp [span]; omega]
  exact tile AM17 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 35) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM17 :
    steps TM17 35 (IN St.E 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.E 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §18 `M18` — `1RB0RA_1LC0LE_0LD0LB_1RA1LF_1LB0RD_1LE---` -/

/-- `1RB0RA_1LC0LE_0LD0LB_1RA1LF_1LB0RD_1LE---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM18 : St → Bool → Option (Bool × Dir × St)
  | .A, false => some (true , .L, .B)   -- A0 → 1LB
  | .A, true  => some (false, .L, .A)   -- A1 → 0LA
  | .B, false => some (true , .R, .C)   -- B0 → 1RC
  | .B, true  => some (false, .R, .E)   -- B1 → 0RE
  | .C, false => some (false, .R, .D)   -- C0 → 0RD
  | .C, true  => some (false, .R, .B)   -- C1 → 0RB
  | .D, false => some (true , .L, .A)   -- D0 → 1LA
  | .D, true  => some (true , .R, .F)   -- D1 → 1RF
  | .E, false => some (true , .R, .B)   -- E0 → 1RB
  | .E, true  => some (false, .L, .D)   -- E1 → 0LD
  | .F, false => some (true , .R, .E)   -- F0 → 1RE
  | .F, true  => none                    -- F1 → --- HALT

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep).
Atom step counts `(cr, mk, ta, s10, s01, tu) = (4, 1, 1, 2, 2, 3)` ⇒ span `6u + 6m + 21`. -/
theorem AM18 : Atoms TM18 .A .B 4 1 1 2 2 3 where
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

/-- The rung tile for `M18`, `∀ u m c g p TAIL REST`, span `6u + 6m + 21`. -/
theorem tileM18 (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps TM18 (6 * u + 6 * m + 21)
        (IN St.A u (m + 1) c (g + 3) p TAIL REST)
      = some (IN St.A (u + 2) m (c + 1) g (p + 3) TAIL REST) := by
  rw [show 6 * u + 6 * m + 21 = span 4 1 1 2 2 3 u m from by simp [span]; omega]
  exact tile AM18 u m c g p TAIL REST

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM18 :
    steps TM18 33 (IN St.A 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.A 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## Summary -/

/-- All the tiles in one list, so the count is checkable at a glance. -/
theorem all_tiles :
    Tile TM01 St.D (span 4 1 1 2 2 3)
    ∧ Tile TM02 St.E (span 4 1 1 2 2 3)
    ∧ Tile TM03 St.C (span 4 1 1 2 2 3)
    ∧ Tile TM04 St.B (span 4 1 1 2 2 3)
    ∧ Tile TM05 St.A (span 4 1 1 2 2 3)
    ∧ Tile TM06 St.A (span 4 1 1 2 2 3)
    ∧ Tile TM07 St.B (span 4 1 1 2 2 3)
    ∧ Tile TM08 St.D (span 4 1 1 2 2 3)
    ∧ Tile TM09 St.B (span 4 1 1 2 2 3)
    ∧ Tile TM10 St.A (span 4 1 1 2 2 3)
    ∧ Tile TM11 St.D (span 4 1 1 2 2 3)
    ∧ Tile TM12 St.F (span 4 1 1 2 2 3)
    ∧ Tile TM13 St.E (span 4 1 1 2 2 3)
    ∧ Tile TM14 St.D (span 4 1 1 2 2 3)
    ∧ Tile TM15 St.B (span 4 1 1 2 2 3)
    ∧ Tile TM16 St.E (span 4 1 1 2 2 3)
    ∧ Tile TM17 St.E (span 4 1 1 2 2 5)
    ∧ Tile TM18 St.A (span 4 1 1 2 2 3)
    := ⟨tile_holds AM01, tile_holds AM02, tile_holds AM03, tile_holds AM04, tile_holds AM05, tile_holds AM06, tile_holds AM07, tile_holds AM08, tile_holds AM09, tile_holds AM10, tile_holds AM11, tile_holds AM12, tile_holds AM13, tile_holds AM14, tile_holds AM15, tile_holds AM16, tile_holds AM17, tile_holds AM18⟩

-- AXIOM AUDIT
#print axioms tileM01
#print axioms tileM02
#print axioms tileM03
#print axioms tileM04
#print axioms tileM05
#print axioms tileM06
#print axioms tileM07
#print axioms tileM08
#print axioms tileM09
#print axioms tileM10
#print axioms tileM11
#print axioms tileM12
#print axioms tileM13
#print axioms tileM14
#print axioms tileM15
#print axioms tileM16
#print axioms tileM17
#print axioms tileM18
#print axioms all_tiles

end IslandTiles
