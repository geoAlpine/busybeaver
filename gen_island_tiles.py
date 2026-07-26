#!/usr/bin/env python3
"""Emit `lean/IslandTiles.lean`: the rung tile for EVERY residual holdout satisfying `Atoms`.

`atoms_island_scan.py` found 17 of the 1104 still-open holdouts satisfy `RungCalc.Atoms`.  Each
therefore gets the rung tile for six closed kernel `rfl`s.  This script writes those out so the
claim is checked, not asserted.

The emitted file is machine-generated on purpose: the content per machine is the transition
table (transcribed from the holdout spec, mirrored when the hit was in the reversed orientation)
plus `Atoms`' six fields.  Nothing about the nine-phase tile proof is repeated -- that lives once,
in `lean/RungCalc.lean`.

Regenerate with:  python3 gen_island_tiles.py > lean/IslandTiles.lean
"""
import os, sys
from atoms_island_scan import parse, reverse, atoms_report, scan, SC, ALL6

HOLDOUTS = "/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt"

# the two already formalized by hand, so we can point at them instead of duplicating
KNOWN = {
    "1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---": "D  (lean/DMachine.lean)",
    "1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---": "H  (lean/HMachine.lean)",
    "1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_1RC---": "E  (island candidate E)",
}

def emit_table(T):
    """Lean match arms for `St -> Bool -> Option (Bool x Dir x St)`"""
    out = []
    for s in range(6):
        for r in (0, 1):
            e = T[s][r]
            lhs = f"  | .{SC[s]}, {'true ' if r else 'false'} =>"
            if e is None:
                out.append(f"{lhs} none" + " " * 20 + f"-- {SC[s]}{r} → --- HALT")
            else:
                w, d, nx = e
                out.append(f"{lhs} some ({'true ' if w else 'false'}, .{'R' if d == 1 else 'L'}, .{SC[nx]})"
                           f"   -- {SC[s]}{r} → {w}{'R' if d == 1 else 'L'}{SC[nx]}")
    return "\n".join(out)

def main():
    hits = []
    with open(HOLDOUTS) as fh:
        for line in fh:
            spec = line.strip().split()[0] if line.strip() else ""
            if not spec or spec.count('_') != 5:
                continue
            best, hs = scan(spec)
            if best == 6:
                o, sA, held, roles = hs[0]
                hits.append((spec, o, sA, roles))

    W = sys.stdout.write
    W("import RungCalc\n\n")
    W("set_option maxRecDepth 4000000\n")
    W("set_option maxHeartbeats 1000000\n\n")
    W("/-!\n")
    W("# The rung tile for every `Atoms`-satisfying machine in the BB(6) residual\n\n")
    W("**MACHINE-GENERATED** by `gen_island_tiles.py`; regenerate rather than hand-edit.\n\n")
    W("`atoms_island_scan.py` scanned the curated still-open residual\n")
    W("(`_bbdata/bb6_holdouts_1104.txt`, 1104 entries) for machines satisfying\n")
    W(f"`RungCalc.Atoms`, in either orientation, at any state.  **{len(hits)} of 1104 do.**  Since\n")
    W("`RungCalc.tile` proves the rung tile from `Atoms` alone, each of them gets the tile for six\n")
    W("closed kernel `rfl`s — which is what this file spends.\n\n")
    W("Distribution over the residual (best count of the six atoms, over both orientations × all\n")
    W("six candidate outward states): `6/6: 17`, `5/6: 1`, `4/6: 4`, `3/6: 31`, `2/6: 377`,\n")
    W("`1/6: 674`.  The lone 5/6 near-miss (`1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC`, at\n")
    W("`sA = E`) fails only `turn`.\n\n")
    W("## How to read this, and how not to\n\n")
    W("**What it shows.** The machine-independent tile is not a one-machine coincidence: it covers\n")
    W(f"{len(hits)} still-open machines, and the per-machine cost really is six `rfl`s.  Among the named\n")
    W("island candidates, `D`, `E` and `H` are hits; `x2` (1/6), `F` (2/6), `G` (2/6) and `I` (1/6)\n")
    W("are not — so this tile is *not* x2's mechanism.\n\n")
    W("**What it does not show.**  `Atoms` pins 9–10 of a 6-state machine's 12 transition entries\n")
    W("(10 when the roles `sA, b, e, d, c, f` are distinct, 9 when `d = f`), so the family it\n")
    W("describes is structurally narrow by construction; the hits differ only in the 2–3 entries\n")
    W("`Atoms` leaves free, and in whether `d = f` (12 of the 17) or `d ≠ f` (5).  The tile is one\n")
    W("lemma.  **None of these machines is decided by this file**, and nothing here bears on their\n")
    W("epoch anatomy, entry segments, milestone families or cascade inductions — for `D`, that\n")
    W("remainder is where all the difficulty turned out to live.  Every machine below is `[OPEN]`.\n\n")
    W("Zero-Mathlib, core only.  No `sorry`, no `native_decide`, no `decide`.\n")
    W("-/\n\n")
    W("namespace IslandTiles\n\n")
    W("open TapeCalc RungCalc\n\n")
    W("/-- One six-element state type shared by every machine below. -/\n")
    W("inductive St | A | B | C | D | E | F\n")
    W("deriving DecidableEq, Repr\n\n")

    names = []
    for i, (spec, o, sA, roles) in enumerate(hits, 1):
        T = parse(spec) if o == "as-written" else reverse(parse(spec))
        sA_, b, e, d, c, f = roles
        ns = f"M{i:02d}"
        names.append((ns, spec, o, sA_, b, d, f))
        known = KNOWN.get(spec)
        W(f"/-! ## §{i} `{ns}` — `{spec}`" + (f"   ({known})" if known else "") + " -/\n\n")
        W(f"/-- `{spec}`" + (f", i.e. {known}." if known else ".") + "\n")
        if o == "reversed":
            W("Transcribed in the **reversed** (mirrored) form, in which it grows rightward and the\n")
            W("atoms hold; halting is invariant under mirroring. -/\n")
        else:
            W("Transcribed as written — the atoms hold in this orientation. -/\n")
        W(f"def T{ns} : St → Bool → Option (Bool × Dir × St)\n")
        W(emit_table(T) + "\n\n")
        W(f"/-- Roles: `sA = {SC[sA_]}` (outward sweep), `sB = {SC[b]}` (return sweep), "
          f"`e = {SC[e]}`, `d = {SC[d]}`, `c = {SC[c]}`, `f = {SC[f]}`"
          + ("  (`d = f`)." if d == f else "  (`d ≠ f`).") + " -/\n")
        W(f"theorem A{ns} : Atoms T{ns} .{SC[sA_]} .{SC[b]} where\n")
        W("  crawl := by\n    intro p b L R\n")
        W("    rw [show (p - 2 : Int) = p - 1 + 1 - 1 - 1 from by omega]\n    rfl\n")
        W("  marker := by intro p x L R; rfl\n")
        W("  turnaround := by intro p x L R; rfl\n")
        W("  swap10 := by\n    intro p b L R\n")
        W("    rw [show (p + 2 : Int) = p + 1 + 1 from by omega]\n    rfl\n")
        W("  swap01 := by\n    intro p b L R\n")
        W("    rw [show (p + 2 : Int) = p + 1 + 1 from by omega]\n    rfl\n")
        W("  turn := by\n    intro p L R\n")
        W("    rw [show (p + 1 : Int) = p + 1 + 1 - 1 from by omega]\n    rfl\n\n")
        W(f"/-- The rung tile for `{ns}`, `∀ u m c g p TAIL REST`. -/\n")
        W(f"theorem tile{ns} : Tile T{ns} St.{SC[sA_]} := tile_holds A{ns}\n\n")
        W("/-- Anti-vacuity: the tile at `u=1, m=2, c=2, g=4` (span 33) is a closed kernel `rfl`,\n")
        W("independent of the law above — so a drift in the table breaks the build. -/\n")
        W(f"theorem ground{ns} :\n")
        W(f"    steps T{ns} 33 (IN St.{SC[sA_]} 1 2 2 4 0 [true, false, true] [true, true])\n")
        W(f"      = some (IN St.{SC[sA_]} 3 1 3 1 3 [true, false, true] [true, true]) := by rfl\n\n")

    W("/-! ## Summary -/\n\n")
    W("/-- All the tiles in one list, so the count is checkable at a glance. -/\n")
    W("theorem all_tiles :\n")
    for i, (ns, spec, o, sA_, b, d, f) in enumerate(names):
        conj = "    " if i == 0 else "    ∧ "
        W(f"{conj}Tile T{ns} St.{SC[sA_]}\n")
    W("    := ⟨" + ", ".join(f"tile{ns}" for ns, *_ in names) + "⟩\n\n")
    W("-- AXIOM AUDIT\n")
    for ns, *_ in names:
        W(f"#print axioms tile{ns}\n")
    W("#print axioms all_tiles\n\n")
    W("end IslandTiles\n")

if __name__ == "__main__":
    main()
