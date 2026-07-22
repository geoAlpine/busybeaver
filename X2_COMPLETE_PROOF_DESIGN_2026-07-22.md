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

## ✅ Progress 2026-07-22 (post-design, first attack: D2 + D3-start)

- **D2 — odd-g premise audit DONE, FAVORABLE.** Re-ran the nesting audit at g=3 (all rungs).
  Marker nesting `marker_k = layer_k ++ marker_{k+1}` EXACT for k=5…9; pad nesting
  `z_k − z_{k+1} = 2^{k-1}` EXACT for **k=5…11** (deeper than g=2 — includes rungs 11,12). So the
  interior nesting is **parity-robust** (holds g=2 AND g=3): **the `∀g` wiring needs NO parity split
  for the interior.** Risk #1 downgraded. The g=3 rung-11 `+80` is NOT a nesting deviation — block
  (`1^2045`) and pad both canonical there; it is a localized top-region span anomaly (does not recur
  at g=4) for D4 to run down, not an interior obstruction.
- **D3-start — the base is BLANK-framed.** Extracted `base_g` (the marker residual beyond the
  `ascMarker` stack) at g=2/3/4: it begins with a long **zeros run** (≥40 bits measured, all `0`) at
  every g. So `ladderFold`'s residual `marker'` is essentially blank tape, **not hidden structure** —
  Risk #3 downgraded. `|base_g|` = 14344/12297/8202 (`base_g − base_{g+1} = 2^{g+9}−1`, tape geometry).
  Full base structure beyond the zeros head still TBD (D3 continues).

- **D1-start — the HEAD is a DESCENDING CHEW-LADDER, the mirror of the ascending one.** Traced the
  g=2 head (6 580 steps, M6(2)→regenIn 5): the big block collapses stair-step through **exactly the
  levels `2^k−3` for k = 10,9,8,7,6,5** (1021→509→253→125→61→29), one "chew" per level. So the head
  is NOT a monolithic block-chew and NOT fog — it is a **descending ladder from level `K(g)=g+8`
  down to 5**, structurally the mirror of the (proven) ascending `ladderFold`. Per-rung descent costs
  1681 / 2295 / 1143 / 567 / 279 (levels 10→9…6→5): the interior obeys a **clean recursion
  `cost_k = 2·cost_{k-1} + 9`** (2295=2·1143+9, 1143=2·567+9, 567=2·279+9, all exact); only the top
  rung (the M6 entry, 10→9 = 1681) is special, and a final 615-step entry lands `regenIn 5`. **So the
  head's "no closed form" flag is downgraded** — there IS clean per-rung structure; D1 likely closes
  as a `headFold` (a `∀`-fold of a banked descent chew rung — `ecombChewFold` / `descent_glue`
  family), the mirror of `ladderFold`. Full config-level rung identification + the special
  top/bottom + parity (odd-g head 53382 ≫ even) remain (D1 continues).

**Net:** the three risks most likely to hide work (odd-g nesting split; base = hidden bulk; head =
formless) ALL measured favorable on first contact — nesting is parity-robust, the base is blank-
framed, and the head is a clean descending mirror-ladder. Remaining front: D1-finish (identify the
descent rung + top/bottom + parity) → D3-finish/D4 (base+tail) → D5 (`∀g`). The design's shape is
now **symmetric**: `headFold (descend K→5) ∘ ladderFold (ascend 5→K+1) ∘ tail`. Source: this
session's g=2/3 audits + head trace (`x2t7_boundary.py` / head-trace family).

- **D1-refine — the head's descent-rung cost is `9·(2^{k-1}−1)`; the g=2 head accounts EXACTLY.**
  The interior descent rung (chewing level k→k−1) costs `9·(2^{k-1}−1)` — exact at k=9,8,7,6
  (2295, 1143, 567, 279). Full g=2 head accounting: `1681 (top: M6 entry 10→9) + 2295+1143+567+279
  (rungs) + 615 (regenIn 5 entry) = 6 580` ✓ — a clean closed form, **risk #2 stays downgraded**.
  **HONEST tempering [MEASURED]:** the detector shows the head does NOT pass through
  `regenIn`/`cascadeReg` configs (only the final `regenIn 5` + one `cascadeReg 4`). So the descent is
  a **distinct transport family, NOT the ascending ladder backwards** — `headFold` mirrors the SHAPE,
  not the transport, and needs its OWN descent-rung lemma. The mid-rung boundary config is state C,
  right `0 1^59` (not an E-milestone). Open D1 sub-task: identify the descent rung as a banked
  transport (candidate: a `sweepEF`/`chew` de-doubling composition). Top rung scales `~2^K`; odd-g
  head (53382 ≫ even) carries the `h_low` odd decoration.
- **D1-refine₂ — the descent is LINEAR, so it is NOT the ascent inverted.** The rung cost
  `9·(2^{k-1}−1)` is Θ(2^k) — LINEAR in the block. The ascent rung (`topGrindSteps k = 4^k−3·2^k+7`)
  is Θ(4^k), QUADRATIC. So building level k (doubling, `braid_topgrind`) needs the quadratic
  odometer, but CHEWING a block down one level is cheap and linear — the head is a genuinely
  different, cheaper mechanism, not `ladderFold` reversed. Banked linear primitives that must compose
  into the rung: `chewFold` (`6m` steps, block `1^{2m+3}→1^3`, deposits `pow10 m`) and `sweepEF`
  (`2m` steps, comb↔block repack) — both `∀m`, `[propext, Quot.sound]`. The rung is a
  chew+repack+turn round-trip; `8·2^{k-1}` (chewFold+sweepEF) ≈ the measured `9·2^{k-1}−9`, so the
  exact composition is one chew + one sweep + a small turn per level. **Pinning that composition
  (a `descentRung` lemma) + folding it (`headFold`) is the concrete remaining D1 build** — same
  method as `ladderStep`/`ladderFold`, on cheaper (linear) primitives.
- **D1-BREAKTHROUGH — the descent DOES have clean level-indexed endpoints (`descIn k`).** The earlier
  "no clean endpoints" was a MIS-MEASUREMENT (I parsed left of the head; the block is to the RIGHT).
  With the right window, each descent milestone is a clean level-`k` config:
  `descIn k := ⟨E, p, ⟨pow01 (2^{k-1}) ++ M, false, false :: ones(2^k−3) ++ 0² ++ descCascade(k−2) ++ 0^z ++ R⟩⟩`.
  Verified at k=8 (comb `(01)^128`, right `0 1^253 0² descCascade(6)`) and k=7 (`(01)^64`, `0 1^125 0²
  descCascade(5)`) — comb `= (01)^{2^{k-1}}`, block `= 1^{2^k−3}`, cascade `= descCascade(k−2)`, all
  level-`k`-indexed and EXACT. **So the descent rung is `descIn k → descIn (k−1)`** (comb halves,
  block/cascade drop one level), with the clean cost `9·(2^{k-1}−1)`. `descIn` is close to
  `cascadeReg` but distinct (leading `0^1` vs `0^3`, `descCascade(k−2)` vs `(k−3)`, comb `2^{k-1}`).
  **`headFold` is back on the buildable path** — the endpoints exist; the remaining D1 work is to
  identify the `descIn k → descIn (k−1)` transport as a `chewFold`/`sweepEF` composition (measured
  cost `9·2^{k-1}−9`) and prove `descentStep` + fold it, exactly the `ladderStep`/`ladderFold` method.
- **✅ D1 CORE BUILT — `descTile` + `descFold` (lean/T7Head.lean, lake-green, `[propext,Quot.sound]`).**
  Traced the descent rung cell-for-cell: it is a **6-step E-tile `descTile`** repeated —
  `steps 6 ⟨.E, p, ⟨L, false, 0::1::1::X⟩⟩ = ⟨.E, p+2, ⟨0::1::L, false, 0::X⟩⟩` (chews `1 1`→ deposits
  comb `0 1`, the mirror-direction of `sweepEF_tile`). Folded `∀m`:
  **`descFold : steps (6m) ⟨.E, p, ⟨L, false, 0::(ones(2m) ++ Y)⟩⟩ = ⟨.E, p+2m, ⟨pow01 m ++ L, false,
  0::Y⟩⟩`** — the descent chew fold, the head analogue of `sweepEF`, proven by tile+length induction.
  This is the CORE of the descent rung. Remaining for `descentStep` (`descIn k → descIn (k−1)`):
  compose `descFold` (the `6m ≈ 6·2^{k-1}` chew) with the return sweep + level-drop (the residual
  `~3·2^{k-1}` of the measured `9·2^{k-1}−9`), then fold into `headFold`. **The head is now on the
  same rails as the interior** — a banked tile-fold (`descFold`) mirroring `sweepEF`/`ladderFold`.
- **D1-refine₃ — the rung is PURE `descTile` (no return sweep), traversing the cascade.** Measured:
  rung 8→7 (1143 steps) = **exactly 190 `descTile`s + 3 settle** (190·6+3=1143), all rightward chew,
  head never returns. So `descentStep` is a `descFold`-family fold with NO separate return phase —
  simpler than the "chew + sweep + turn" guess. The catch: the 190 tiles traverse the whole
  `descCascade` structure (blocks separated by `0^2`), not one `ones(2m)` block, so the rung needs a
  **cascade-traversal variant of `descFold`** (the tile applies across separators via the right
  invariant). Tile-count per rung `= (9·(2^{k-1}−1)−3)/6` (190 at k=8). **Remaining D1: state the
  descIn k → descIn (k−1) invariant that lets `descTile` fold over the cascade** — a single fold, no
  return, the cleanest possible shape. **Tile count per rung `= 3·2^{k-2}−2`** (382/190/94/46 at
  k=9/8/7/6, all exact). `descTile` chews the `0 0 1 1` pattern, so it **naturally spans the
  `descCascade` `0^2` separators** — the traversal is uniform; the invariant just tracks the
  block/separator position. This is the single remaining head build (a `descFold` generalized from
  one `ones(2m)` block to the full `descCascade` traversal).
- **D1-refine₄ — the rung is TWO-PHASE (correcting "pure descTile").** Tile-level trace of rung 8→7:
  **phase 1 = 126 `descTile`s** (head-on-0, chewing the top block `1^253`: 126·2 = 252 ≈ 253), then a
  transition, then **phase 2 = 64 tiles of a SECOND 6-step E-tile** (head-on-1, `0 0 [1] 1 1 → 0 0 1`
  deposit comb `01`, +2). Both tiles deposit `01` / shrink block by 2 / advance +2 over 6 steps —
  structurally twins, differing only in head offset (on the `0` vs on the `1`). Phase-2 count 64 = the
  target-level comb width `2^6`. **So `descentStep` = descTile-fold (top block) ∘ phase-transition ∘
  descTile2-fold (cascade traversal).** `descTile`+`descFold` cover phase 1 (proven). Remaining:
  the phase-2 tile lemma + its fold + the transition + the descIn-level bookkeeping — a clean but
  multi-lemma build, all on the same `rfl`+`cfgPos` / tile+induction rails as `descTile`/`descFold`.
  The descent is now characterized to the individual machine step; no fog remains, only assembly.
- **✅ BOTH descent tiles + folds now GREEN (T7Head.lean).** Built the phase-2 pair:
  `descTile2 : steps 6 ⟨.E,p,⟨0::0::L, 1, 1::1::Y⟩⟩ = ⟨.E,p+2,⟨0::0::1::0::L, 1, Y⟩⟩` (head-on-1 chew,
  twin of `descTile`), and `descFold2 : steps (6m) ⟨.E,p,⟨0::0::L,1,ones(2m)++Y⟩⟩ =
  ⟨.E,p+2m,⟨0::0::(pow10 m ++ L),1,Y⟩⟩` (folded via `pow10_add`). **So all four descent primitives are
  proven `[propext, Quot.sound]`:** `descTile`/`descFold` (phase 1, head-on-0, deposits `pow01`) and
  `descTile2`/`descFold2` (phase 2, head-on-1, deposits `pow10`). The remaining D1 work is pure
  ASSEMBLY: the phase-1→phase-2 transition (3 settle steps at the block end) + the `descIn k →
  descIn (k−1)` statement composing `descFold` (126 tiles) ∘ transition ∘ `descFold2` (64 tiles),
  then `headFold`. No new tile mechanics remain — every 6-step unit of the head is now a theorem.
- **✅ THE TRANSITION IS ALSO GREEN — `descTrans` (T7Head.lean).** The phase-1→phase-2 bridge is a
  fixed, level-independent 12-step episode:
  `descTrans : steps 12 ⟨.E,p,⟨L,false, 0 1 1 1 0 0 1 1 ++ X⟩⟩ = ⟨.E,p+8,⟨(fixed 8-cell comb)::L, true, X⟩⟩`
  — consumes the block-leftover `1 1 1`, the `0 0` separator and the next block's first `1 1`, lands
  head-on-1. **So EVERY component of the head descent is now a proven theorem** (`[propext,
  Quot.sound]`): `descTile`/`descFold` (phase 1) + `descTrans` (transition) + `descTile2`/`descFold2`
  (phase 2). **The entire remaining D1 build is now a single composition** — state `descIn k →
  descIn (k−1)` as `descFold ∘ descTrans ∘ descFold2` with the block/comb/cascade counts, then fold
  `∀`-levels into `headFold`. ~~pure Lean assembly of five banked lemmas~~
- **⚠ D1-CORRECTION — the descIn composition is NOT a simple 5-lemma chain (comb halving).**
  [MEASURED] `descIn k → descIn (k−1)` transforms: comb `(01)^{2^{k-1}} → (01)^{2^{k-2}}` (**HALVES**),
  block `1^{2^k-3} → 1^{2^{k-1}-3}`, cascade `descCascade(k−2) → descCascade(k−3)`. Verified at
  descIn 6→5 (comb 32→16) and 8→7 (128→64). **The tiles DEPOSIT comb (grow it), but the descIn comb
  HALVES — so a comb-reorganization mechanism is present that the five chew tiles do not capture.**
  The `descTile`/`descFold`/`descTrans`/`descTile2`/`descFold2` lemmas are correct and proven (the
  chew of ONE block into comb), but `descentStep` is more than their linear composition: the head
  must also consume/repack the pre-existing comb `(01)^{2^{k-1}}` to the left. **This is the honest
  remaining D1 obstacle** — the comb transformation, unmeasured until now. Correction to the earlier
  "pure assembly" optimism: the tiles are the chew engine, but the level-drop's comb bookkeeping
  needs its own analysis (measure the comb's fate during a rung, then formalize). Calibration: the
  tiles were MEASURED (all hold); "descentStep = the 5-chain" was NARRATIVE (now shown incomplete).
- **✅ NEW THEOREM `ladderToCascade` (T7Ladder.lean, lake-green, `[propext, Quot.sound]`).** Packages
  the maximal proven MIDDLE of the doubling phase into one lemma: from `regenIn b` with nested
  marker/pad, `ladderSteps b n + exitSteps (b+n)` steps reach `cascadeReg (b+n) 1 q' marker' R''` —
  i.e. `ladderFold` (interior) ∘ `regenLaw_pos` (top REGEN rung). Non-vacuity: `ladderToCascade 5 · 3`
  type-checks `regenIn 5 → cascadeReg 8`. **This is exactly the object D5's final assembly composes
  between the head's `regenIn 5` and the tail's `cascadeReg (g+9)`** — the whole span from first
  ladder rung to the tail's IN is now a single citable theorem.

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

1. ~~**Odd-g anomaly (D2) is the live risk.**~~ **DOWNGRADED 2026-07-22.** D2 ran: nesting is
   parity-robust (marker+pad EXACT at g=2 AND g=3). No odd-g seam variant needed for the interior.
   Residual: the g=3 rung-11 `+80` (canonical surrounding data; localized; a D4 item, not a blocker).
2. ~~**Head has no closed form yet.**~~ **DOWNGRADED 2026-07-22.** D1-start: the head is a descending
   chew-ladder (levels K→5) with a clean per-rung recursion `cost_k = 2·cost_{k-1}+9` — the mirror of
   `ladderFold`, not a formless total. Residual: identify the descent rung as a banked transport +
   the special top/bottom + the odd-g decoration (odd head ≫ even).
3. ~~**Base reconciliation (D3) could be the hidden bulk.**~~ **DOWNGRADED 2026-07-22.** D3-start:
   `base_g` begins with a long zeros run at every g — it is blank frame, not more comb. Base is not
   hidden bulk. Residual: pin the base's far structure + its `m1_spec` reconciliation (D3 continues).
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
