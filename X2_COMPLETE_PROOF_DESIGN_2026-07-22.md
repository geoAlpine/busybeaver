# x2 complete proof — the construction design (施工図), post-2026-07-22 sweep

**What this is.** A full sweep of everything obtained through 2026-07-22 — the `RegenLaw ∀k`
closure (07-21), today's 14 documents, 3 new Lean theorems, and the g=2/3/4 orbit measurements —
assembled into a construction design for **x2 complete** (`∀N, steps N init ≠ none`). Every
component below is tagged `[PROVEN]` (Lean-green, `[propext, Quot.sound]`), `[MEASURED]`
(orbit-verified, instrument-checked), or `[OPEN]` (to build). **No machine is decided by this
document; this is a design, not a result.**

**Scope note (BB(6)).** BB(6) complete is a DIFFERENT object behind the (K) wall. Its design is
already complete and lives elsewhere: `BB6_COMPLETE_ROADMAP_2026-07-22.md` (the 11-axiom discharge
map, tiers E/C/M/X), `BB6_PROOF_HANDLES_2026-07-22.md` (the 8 doors + 14 traps), and the parked
new-math blueprint (`NEWMATH_BUILD_SYNTHESIS_2026-07-09` + `ATTACK_PLAN_2026-07-10`). Completing x2
does not touch BB(6); nothing here claims otherwise.

---

## 0. The gate (unchanged, GREEN)

```lean
x2_nonhalt (M1 M6 : Nat → Cfg)
  (h_init : ∃ n, 1 ≤ n ∧ steps n init = some (M1 1))
  (h_low  : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M1 g) = some (M6 g))
  (h_doub : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M6 g) = some (M1 (g+1))) :
  ∀ N, steps N init ≠ none
```

| hypothesis | status |
|---|---|
| `h_init` | ✅ `[PROVEN]` realized form (`HInit.lean`, T1) |
| `h_low ∀g` | ✅ `[PROVEN]` both parities (§5ao + §5bb, T2+T8) |
| `h_doub ∀g` | `[OPEN]` — **the entire remaining mathematical content of x2.** Design below. |
| family coherence (obligation H / T9) | `[OPEN]` — tie the §5am families to `init`; tools banked |

## 1. Component inventory (the sweep)

### 1a. Proven transports available to the design `[PROVEN unless noted]`

| component | statement | role in the design |
|---|---|---|
| `regenLaw_closed` (07-21) | `∀k≥4, RegenLaw k` | the REGEN rail |
| `regenLaw_pos` | RegenLaw at ANY position `q` | position threading |
| `braid_topgrind` | `∀ N Lc p marker casc` top-block doubling | the GAP rail |
| `topGrindSteps_split` | `topGrindSteps a` = braid cost at `N = 2^{a−1}−2` | rail arithmetic |
| **`cascadeReg_topgrind`** (NEW 07-22) | gap rail fires from `cascadeReg k` | rail hand-off |
| **`ladderStep`** (NEW 07-22) | one rung `regenIn k → regenIn (k+1)`, ∀-position | the inductive step |
| **`ladderFold`** (NEW 07-22) | `∀n ∀b≥4 ∀q`: n rungs `regenIn b → regenIn (b+n)` | **the whole interior** |
| `zeros_pad`, `ones_append_true` | pad/marker `List` seams | seam discharge (used in `ladderStep`) |
| `steps_add`, `steps_pos_shift`, `someBind` | composition machinery | assembly glue |
| `realizeM1_port`, `BlankNorm` | canonical→realized porting | obligation H |
| §5g episodes (`ecombChewFold`, `markedBlock`, `bigCascade`, `doubling_transport_mid`) | proven doubling-phase episodes | candidate HEAD material (D1) |

### 1b. Measured laws (instrument-validated; g=2/3/4) `[MEASURED]`

| law | verification |
|---|---|
| doubling phase = ladder `head ∘ ∏[REGEN(k) ∘ topgrind(k)] ∘ topREGEN ∘ tail` | exact accounting at g=2 (2 119 015 = 6 580 + Σ + 211) |
| transport span = `exitSteps k` on-orbit | 8 confirmations + all rungs g=4 (k≤13); ONE exception: g=3 rung 11 = `+80` |
| gap span = `topGrindSteps k` on-orbit | exact at every measured gap, g=2/3/4 (from true landings) |
| marker nesting `marker_k = layer_k ++ marker_{k+1}` | EXACT k=5…9 (g=2) — `ladderFold`'s premise holds on-orbit |
| pad nesting `z_k − z_{k+1} = 2^{k−1}` | EXACT k=5…10 (g=2) |
| ladder shape: levels `5…g+9`, i.e. `ladderFold n = g+4` rungs + top `REGEN(g+9)` | g=2/3/4 |
| milestones: `K(M1(g)) = g+8`, big block `2^{g+8}−3` (even g) / `−9` (odd g), leading gap `0^21` | g=1…5 |
| heads: 6 580 / 53 382 / 25 024 (g=2/3/4) | parity-split, no closed form |
| tails: 211 / 184* / 265 (g=2/3/4; *g=3 landing not clean) | no closed form |
| coverage: REGEN transports ≈ 1/3 of phase, stable | g=2/3/4 |

## 2. The master formula for `h_doub` (one generation)

```
M6(g) ──head_g──▶ regenIn 5 q₀ (2⁴+9) (ladderMarker 5 (g+4) ++ base_g) (ladderPad 5 (g+4) ++ pad_g)
      ──ladderFold (g+4) 5──▶ regenIn (g+9) q' (2^{g+8}+9) base_g pad_g          [PROVEN]
      ──regenLaw_pos (g+9)──▶ cascadeReg (g+9) 1 (q'−2^{g+9}) base_g pad_g       [PROVEN]
      ──tail_g──▶ M1(g+1)
```

Step count: `|head_g| + ladderSteps 5 (g+4) + exitSteps (g+9) + |tail_g|`. The middle two factors
are theorems **today**; `h_doub` is reduced to the two boundary transports plus the `∀g` wiring.

## 3. Design tasks, in dependency order

### D1. HEAD — decompose `M6(g) → regenIn 5` against the banked §5g episodes. `[OPEN, first]`
The head is NOT fog: §5g already proves the doubling-phase entry episodes (`ecombChewFold` — the
block→comb chew; `markedBlock`; `bigCascade` = episodes 3+4 of `doubling_transport_mid`). Measured
lengths 6 580 / 53 382 / 25 024 are parity-split and non-monotone — exactly the signature of the
odd-g `(10)^6→(10)^10` decoration difference that `h_low` hit (solved there by `lowTurnOdd`).
**Do:** trace the g=2 head's 6 580 steps episode-by-episode against the banked transports; expect
`head = chew ∘ repack-entry` with parity-dependent constants. Then g=3/g=4 to pin both parity
families; then g=5/6 as forward-prediction controls. *Method precedent: exactly how `h_low_even`'s
`N(g)=267+38g` chain was extracted.*

### D2. ODD-g PREMISE AUDIT — is the g=3 `+80` a nesting deviation? `[OPEN, cheap, decisive]`
The single blemish in the interior data: g=3 rung 11 spans `exitSteps(11)+80`. `RegenLaw` is exact
at canonical pad — so a deviating span means **the g=3 rung-11 config was NOT canonical** (pad or
marker off by a reconcilable term). The nesting audit (D2 = re-run `x2t7_boundary.py` at g=3, all
rungs) will either (a) find the deviation → the odd-g boundary data differs and the `∀g` wiring
splits by parity (mirroring `h_low_even`/`h_low_odd`), or (b) find canonical data → the +80 needs a
different explanation and the interior claim itself needs a caveat. **Either way this must precede
the ∀g statement.** Risk flag: today's nesting audit ran at g=2 only.

### D3. BASE — characterize `(base_g, pad_g)` at the ladder top. `[OPEN, small]`
`ladderFold` leaves the residual `base_g`/`pad_g` untouched; the top-rung `cascadeReg (g+9)` carries
them into `tail_g`. Measured: marker shrinks 18 370 → 16 391 across the g=2 ladder; the base is what
remains (the generation's outer decoration + the `0^21`-gap frame of the next milestone). **Do:**
extract `base_g` bit-exactly at g=2/3/4; find its `g`-recursion (it should BE the `M1(g+1)` frame
data — the ladder builds the next milestone's cascade, so the base should reconcile with `m1_spec`).

### D4. TAIL — the top-rung exit `cascadeReg (g+9) → M1(g+1)`. `[OPEN, small]`
Measured 211 / 184* / 265; short, but not constant and (at g=3) not landing cleanly. Likely one
fixed episode family with parity-dependent constants, like `lowExitReg`. **Do:** extract the tail
cell-by-cell at g=2/4 (clean cases) first; revisit g=3 after D2 explains its rung-11 shift.

### D5. `∀g` WIRING — state and prove `M6(g)`'s presentation. `[OPEN, the induction]`
Target lemma family (names indicative):
```lean
doubHead g   : steps (headSteps g) (M6 g) = some (regenIn 5 q₀ 17 (ladderMarker 5 (g+4) ++ base g) (ladderPad 5 (g+4) ++ pad g))
doubTail g   : steps (tailSteps g) (cascadeReg (g+9) 1 q₁ (base g) (pad g)) = some (M1 (g+1))
doubPhase g  : steps (doubSteps g) (M6 g) = some (M1 (g+1))     -- composition, via ladderFold
h_doub       : ∀ g, ∃ n, 1 ≤ n ∧ steps n (M6 g) = some (M1 (g+1))
```
`doubPhase` is four rewrites once D1–D4 exist (`steps_add` ∘ `doubHead` ∘ `ladderFold` ∘
`regenLaw_pos` ∘ `doubTail`) — the same shape as `regenLaw_of_trailLaw`. Expect the statement to
split even/odd g (D2), exactly as `h_low` did. Anti-vacuity controls: `doubPhase 2` must reproduce
the measured 2 119 015 total; `doubPhase 3/4` the measured phases.

### D6. OBLIGATION H (T9) — one family for all three hypotheses. `[OPEN, tool-complete]`
`h_init` is proven for the REALIZED milestone; `h_low`/`h_doub` for the CANONICAL §5am families.
Port via `realizeM1_port` (+ `BlankNorm`, `steps_pos_shift`) so all three hold for the SAME
`M1, M6 : Nat → Cfg`. Recon already staged: `lean/probe_g01_2026-07-21.lean` (are g=0,1
generations?). This is definitional/porting work, no new transports.

### D7. FINAL ASSEMBLY. Apply `x2_nonhalt`. One `exact`. Then **x2 complete** — and the FIRST
decided BB(6)-frontier machine, pending the full-repo cold-build audit + red-team that this repo's
discipline requires before any label changes.

## 4. Risk register (honest)

1. **Odd-g anomaly (D2) is the live risk.** If odd generations carry non-canonical mid-ladder data,
   `ladderFold` may need an odd-g variant (a second seam lemma), not just different constants.
   Mitigation: D2 is cheap and scheduled first.
2. **Head has no closed form yet** across even g (6 580 → 25 024 is not a clean recursion on two
   points). Mitigation: D1's episode decomposition replaces curve-fitting with structure — the
   `h_low` method, which worked twice.
3. **Base reconciliation (D3) could be the hidden bulk** — if `base_g` does not reduce to `m1_spec`
   frame data, D4's tail becomes a genuine transport. Watch item; measured base sizes (~16 k bits at
   g=2) are large but the ladder already reproduces them exactly, so structure is expected.
4. **Calibration discipline.** Today's score: measurements 100 % survived; every narrative
   extrapolation failed (⊕-unwired, +80-in-gap, M1(4) prediction, R≤3 scoring). **Every D-task above
   is scoped to measure before stating.** Forward-prediction controls (g=5/6) are built into D1/D5.
5. **Scope honesty.** x2 complete decides ONE 1104-holdout machine on the carry-transparent side.
   It does not move the (K) wall, and no wording in the final assembly may suggest otherwise.

## 5. Effort estimate

| task | kind | scale |
|---|---|---|
| D1 head decomposition | measurement + episode matching | days |
| D2 odd-g audit | measurement (script exists) | hours |
| D3 base extraction | measurement | hours–day |
| D4 tail transport | measurement + small Lean | days |
| D5 `∀g` wiring + `doubPhase` | Lean (chunked `rfl` heads/tails + composition) | 1–2 weeks |
| D6 obligation H | Lean porting | days–week |
| D7 assembly + audit | Lean + cold build + red-team | days |

Comparable in total to the `h_low ∀g` effort (which closed), smaller than the `RegenLaw ∀k` arc.
The bulk (the Θ(2^{2K}) interior) is **already done** — that was the object called "largest single
object" in the pre-07-22 ledgers, and it fell to banked theorems.

## 6. Immediate next three actions

1. **D2** — re-run the nesting audit at g=3 (all rungs, especially 11). Decisive for the ∀g shape.
2. **D1** — episode-trace the g=2 head (6 580 steps) against `ecombChewFold`/`markedBlock`/entry.
3. **D3** — extract `base_g` at g=2 and diff it against the `m1_spec(3)` frame.

---
*Design assembled 2026-07-22 from: T7_RECON / T7_GAPLAW / T7_LADDER_STRUCTURE / T7_G4 /
T7_LADDER_LEAN / T7_BOUNDARY (all 2026-07-22), lean/T7Ladder.lean, and the 07-21 closure record.
No machine is decided. No label is upgraded.*
