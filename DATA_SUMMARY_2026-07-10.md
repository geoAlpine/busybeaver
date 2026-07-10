# BB(6) complete-proof — consolidated data summary (2026-07-10)

*One-page consolidation of the campaign's data as of the [C]-frontier dig. Feeds the automatic-extractor design.
Labels: [PROVEN]/[PROVEN,Lean]/[OBSERVED]/[OPEN]. No machine decided.*

## 1. The complete-proof decomposition, current status

```
BB(6) = N(champion)   ⟸   [A] 17 named cryptids  ∧  [B] thin-set/timing  ∧  [C] 1087 holdouts  ∧  champion+enumeration
```

| part | content | status | barrier class |
|---|---|---|---|
| **[A]** | 14 (K)-band + o7/SN + o17 | **collapsed to 3 meta-schemas** [Lean: `Completion.lean`] | (K)/Mahler + Collatz + timing |
| **[B]** | o7, Space Needle, o17 | thin-set/timing, closed to internal attack (17 tool classes) | Collatz-hard / unbounded-state |
| **[C]** | 1087 un-catalogued holdouts | **landscape mapped; collapse blocked (digit-string)** | community-scale deep analysis |
| champion | `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` ≈ 10↑↑15 | BB(6) ≥ N [lit]; N exact = engineering | checkable |

## 2. The [A] collapse — the true arithmetic content is minimal `[PROVEN, Lean]`

The 17 named conjectures = **3 meta-schemas** over **17 seed-instances**:
| schema | engine, place | machines |
|---|---|---|
| `NormalityPQ 3 2` | ×3/2, v₂ | Antihydra, o10, o2, o11, o13, o14, o16, o12, o8 (9) |
| `NormalityPQ 4 3` | ×4/3, v₃ | o4 (Lean end-to-end), o3, o5 (3) |
| `NormalityPQ 8 3` | ×8/3, v₃ | o15, o18 (2) |
| `TwoPowerAvoidance` | gen-Collatz 2^k | o7, Space Needle (2) |
| o17 | gate-timing | o17 (1) |
`BB6_eq_championSteps` depends on the single symbol `NormalityPQ` for the whole 13-machine (K)-band + `o7orbit`/`snOrbit` + `o17`. Sameness is of SHAPE not difficulty (per-seed genericity stays (K)).

## 3. The [C] landscape — census over all 1104 `[OBSERVED]`

- **Growth band:** sqrt-t 663 / sub-sqrt 387 / bounded~cycler 47 / inter 7 — **all slow polynomial-width counters**.
- **Block structure:** **digit-string 924** / bounded-digit 498 / unary 19 / mixed 18.
- **Width-multiplier extracted:** only **8 / 1104** (the width-ratio proxy is blind to digit-string machines).
- **Decision yield:** 47/47 bounded~cyclers → HOLDOUT (0 decided; our suite = community decider class).

**The collapse obstruction:** the ×(p/q) multiplier is visible in tape *width* only for **unary** counters; **924 are
digit-string** (value in a digit-string, width ≈ const) — exactly o4's structure. Reading their engine needs
per-machine milestone analysis, not a width probe. → **this is why the automatic extractor is needed.**

## 4. The automatic extractor — design spec (what §block 924 needs)

To collapse the digit-string majority, the extractor must read the multiplier WITHOUT the tape width. The robust,
width-independent signal:
- **Milestone events** = record-extreme excursions (the head reaching a new leftmost/rightmost cell), which a growing
  counter hits periodically.
- **Multiplier** = the geometric ratio of consecutive inter-milestone **step-gaps**: for a value-×(p/q) counter doing
  work ∝ value per milestone, `g_{k+1}/g_k → p/q` (width-independent — works for digit-string machines).
- **Engine-match** = nearest simple rational; flag {3/2, 4/3, 8/3, 5/2, ceiling-3/2} as known, else new species.
- **Validation gate:** must recover the KNOWN multipliers of the 17 named (o4→4/3, Antihydra→3/2, o15→8/3, SN→5/2)
  before any 1104 result is trusted.

## 5. The (K)-wall state (for reference)

Every (K)-band protection = per-seed base-p/q normality; localized to the δ₋₁₄ seam (annealed effective / quenched
= (K)); crisp form: decide o4 ⟺ prove `Re(S₁(n)) < 0.7n`. ~17 tool classes all converge there; unconditional partials
banked (φ=1/3 a.e.; archimedean Baker-effective). Crossing the seam = Mahler 3/2.

## Sources
`ROADMAP_COMPLETE_PROOF_2026-07-10`, `COMPLETION_SKELETON_2026-07-10`, `MINIMAL_CONJECTURE_SET_2026-07-10`,
`HOLDOUT_CLASSIFICATION_2026-07-10`, `PAPER_CENSUS`, `lean/Completion.lean`. Zenodo v1.6 DOI 10.5281/zenodo.21288906.
