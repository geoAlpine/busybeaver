import RungCalc

set_option maxRecDepth 4000000
set_option maxHeartbeats 1000000

/-!
# The rung tile for every `Atoms`-satisfying machine in the BB(6) residual

**MACHINE-GENERATED** by `gen_island_tiles.py`; regenerate rather than hand-edit.

`atoms_island_scan.py` scanned the curated still-open residual
(`_bbdata/bb6_holdouts_1104.txt`, 1104 entries) for machines satisfying
`RungCalc.Atoms`, in either orientation, at any state.  **17 of 1104 do.**  Since
`RungCalc.tile` proves the rung tile from `Atoms` alone, each of them gets the tile for six
closed kernel `rfl`s — which is what this file spends.

Distribution over the residual (best count of the six atoms, over both orientations × all
six candidate outward states): `6/6: 17`, `5/6: 1`, `4/6: 4`, `3/6: 31`, `2/6: 377`,
`1/6: 674`.  The lone 5/6 near-miss (`1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC`, at
`sA = E`) fails only `turn`.

## How to read this, and how not to

**What it shows.** The machine-independent tile is not a one-machine coincidence: it covers
17 still-open machines, and the per-machine cost really is six `rfl`s.  Among the named
island candidates, `D`, `E` and `H` are hits; `x2` (1/6), `F` (2/6), `G` (2/6) and `I` (1/6)
are not — so this tile is *not* x2's mechanism.

**What it does not show.**  `Atoms` pins 9–10 of a 6-state machine's 12 transition entries
(10 when the roles `sA, b, e, d, c, f` are distinct, 9 when `d = f`), so the family it
describes is structurally narrow by construction; the hits differ only in the 2–3 entries
`Atoms` leaves free, and in whether `d = f` (12 of the 17) or `d ≠ f` (5).  The tile is one
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

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep), `e = E`, `d = C`, `c = B`, `f = C`  (`d = f`). -/
theorem AM01 : Atoms TM01 .D .A where
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

/-- The rung tile for `M01`, `∀ u m c g p TAIL REST`. -/
theorem tileM01 : Tile TM01 St.D := tile_holds AM01

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

/-- Roles: `sA = E` (outward sweep), `sB = B` (return sweep), `e = A`, `d = D`, `c = C`, `f = D`  (`d = f`). -/
theorem AM02 : Atoms TM02 .E .B where
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

/-- The rung tile for `M02`, `∀ u m c g p TAIL REST`. -/
theorem tileM02 : Tile TM02 St.E := tile_holds AM02

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

/-- Roles: `sA = C` (outward sweep), `sB = D` (return sweep), `e = F`, `d = B`, `c = E`, `f = B`  (`d = f`). -/
theorem AM03 : Atoms TM03 .C .D where
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

/-- The rung tile for `M03`, `∀ u m c g p TAIL REST`. -/
theorem tileM03 : Tile TM03 St.C := tile_holds AM03

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

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep), `e = E`, `d = A`, `c = D`, `f = A`  (`d = f`). -/
theorem AM04 : Atoms TM04 .B .C where
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

/-- The rung tile for `M04`, `∀ u m c g p TAIL REST`. -/
theorem tileM04 : Tile TM04 St.B := tile_holds AM04

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

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep), `e = E`, `d = D`, `c = C`, `f = D`  (`d = f`). -/
theorem AM05 : Atoms TM05 .A .B where
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

/-- The rung tile for `M05`, `∀ u m c g p TAIL REST`. -/
theorem tileM05 : Tile TM05 St.A := tile_holds AM05

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

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep), `e = E`, `d = F`, `c = C`, `f = D`  (`d ≠ f`). -/
theorem AM06 : Atoms TM06 .A .B where
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

/-- The rung tile for `M06`, `∀ u m c g p TAIL REST`. -/
theorem tileM06 : Tile TM06 St.A := tile_holds AM06

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

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep), `e = E`, `d = A`, `c = D`, `f = A`  (`d = f`). -/
theorem AM07 : Atoms TM07 .B .C where
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

/-- The rung tile for `M07`, `∀ u m c g p TAIL REST`. -/
theorem tileM07 : Tile TM07 St.B := tile_holds AM07

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

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep), `e = E`, `d = C`, `c = B`, `f = C`  (`d = f`). -/
theorem AM08 : Atoms TM08 .D .A where
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

/-- The rung tile for `M08`, `∀ u m c g p TAIL REST`. -/
theorem tileM08 : Tile TM08 St.D := tile_holds AM08

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

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep), `e = E`, `d = F`, `c = D`, `f = A`  (`d ≠ f`). -/
theorem AM09 : Atoms TM09 .B .C where
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

/-- The rung tile for `M09`, `∀ u m c g p TAIL REST`. -/
theorem tileM09 : Tile TM09 St.B := tile_holds AM09

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

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep), `e = E`, `d = D`, `c = C`, `f = D`  (`d = f`). -/
theorem AM10 : Atoms TM10 .A .B where
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

/-- The rung tile for `M10`, `∀ u m c g p TAIL REST`. -/
theorem tileM10 : Tile TM10 St.A := tile_holds AM10

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

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep), `e = E`, `d = C`, `c = B`, `f = C`  (`d = f`). -/
theorem AM11 : Atoms TM11 .D .A where
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

/-- The rung tile for `M11`, `∀ u m c g p TAIL REST`. -/
theorem tileM11 : Tile TM11 St.D := tile_holds AM11

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

/-- Roles: `sA = F` (outward sweep), `sB = C` (return sweep), `e = B`, `d = E`, `c = D`, `f = E`  (`d = f`). -/
theorem AM12 : Atoms TM12 .F .C where
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

/-- The rung tile for `M12`, `∀ u m c g p TAIL REST`. -/
theorem tileM12 : Tile TM12 St.F := tile_holds AM12

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

/-- Roles: `sA = E` (outward sweep), `sB = B` (return sweep), `e = A`, `d = F`, `c = C`, `f = D`  (`d ≠ f`). -/
theorem AM13 : Atoms TM13 .E .B where
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

/-- The rung tile for `M13`, `∀ u m c g p TAIL REST`. -/
theorem tileM13 : Tile TM13 St.E := tile_holds AM13

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

/-- Roles: `sA = D` (outward sweep), `sB = A` (return sweep), `e = E`, `d = F`, `c = B`, `f = C`  (`d ≠ f`). -/
theorem AM14 : Atoms TM14 .D .A where
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

/-- The rung tile for `M14`, `∀ u m c g p TAIL REST`. -/
theorem tileM14 : Tile TM14 St.D := tile_holds AM14

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

/-- Roles: `sA = B` (outward sweep), `sB = C` (return sweep), `e = E`, `d = A`, `c = D`, `f = A`  (`d = f`). -/
theorem AM15 : Atoms TM15 .B .C where
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

/-- The rung tile for `M15`, `∀ u m c g p TAIL REST`. -/
theorem tileM15 : Tile TM15 St.B := tile_holds AM15

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

/-- Roles: `sA = E` (outward sweep), `sB = B` (return sweep), `e = A`, `d = F`, `c = C`, `f = D`  (`d ≠ f`). -/
theorem AM16 : Atoms TM16 .E .B where
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

/-- The rung tile for `M16`, `∀ u m c g p TAIL REST`. -/
theorem tileM16 : Tile TM16 St.E := tile_holds AM16

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM16 :
    steps TM16 33 (IN St.E 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.E 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## §17 `M17` — `1RB0RA_1LC0LE_0LD0LB_1RA1LF_1LB0RD_1LE---` -/

/-- `1RB0RA_1LC0LE_0LD0LB_1RA1LF_1LB0RD_1LE---`.
Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the
atoms hold; halting is invariant under mirroring. -/
def TM17 : St → Bool → Option (Bool × Dir × St)
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

/-- Roles: `sA = A` (outward sweep), `sB = B` (return sweep), `e = E`, `d = D`, `c = C`, `f = D`  (`d = f`). -/
theorem AM17 : Atoms TM17 .A .B where
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

/-- The rung tile for `M17`, `∀ u m c g p TAIL REST`. -/
theorem tileM17 : Tile TM17 St.A := tile_holds AM17

/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,
independent of the law above — so a drift in the table breaks the build. -/
theorem groundM17 :
    steps TM17 33 (IN St.A 1 2 2 4 0 [true, false, true] [true, true])
      = some (IN St.A 3 1 3 1 3 [true, false, true] [true, true]) := by rfl

/-! ## Summary -/

/-- All the tiles in one list, so the count is checkable at a glance. -/
theorem all_tiles :
    Tile TM01 St.D
    ∧ Tile TM02 St.E
    ∧ Tile TM03 St.C
    ∧ Tile TM04 St.B
    ∧ Tile TM05 St.A
    ∧ Tile TM06 St.A
    ∧ Tile TM07 St.B
    ∧ Tile TM08 St.D
    ∧ Tile TM09 St.B
    ∧ Tile TM10 St.A
    ∧ Tile TM11 St.D
    ∧ Tile TM12 St.F
    ∧ Tile TM13 St.E
    ∧ Tile TM14 St.D
    ∧ Tile TM15 St.B
    ∧ Tile TM16 St.E
    ∧ Tile TM17 St.A
    := ⟨tileM01, tileM02, tileM03, tileM04, tileM05, tileM06, tileM07, tileM08, tileM09, tileM10, tileM11, tileM12, tileM13, tileM14, tileM15, tileM16, tileM17⟩

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
#print axioms all_tiles

end IslandTiles
