# T7 residual #1 and #2 DISCHARGED in Lean — the doubling-phase interior is a theorem (2026-07-22)

Fourth and deepest T7 document today. After the measurement chain
(`T7_RECON` → `T7_GAPLAW` → `T7_LADDER_STRUCTURE` → `T7_G4`) established that the doubling phase is a
ladder of two already-`∀`-proven transports, this document **formalizes the assembly in Lean.**

New module: **`lean/T7Ladder.lean`** (added to `lakefile.toml`, `lake build T7Ladder` GREEN). Three
new theorems, all `[propext, Quot.sound]`, no `sorry`:

## The theorems

```lean
-- GAP RAIL: braid_topgrind fires from cascadeReg k in topGrindSteps k steps.
theorem cascadeReg_topgrind (k) (hk : 4 ≤ k) (p) (marker R) :
    steps (topGrindSteps k) (cascadeReg k 1 p marker R) = some (…doubled OUT…)

-- LADDER STEP (∀-position): one rung, regenIn k → regenIn (k+1), seam discharged.
theorem ladderStep (k) (hk : 4 ≤ k) (q) (marker' R'') :
    steps (exitSteps k + topGrindSteps k)
        (regenIn k q (2^(k-1)+9) (0 0 1 (01)^{2^k-2} ++ marker') (0^{2^k} ++ R''))
      = some (regenIn (k+1) (…q shifted…) (2^k+9) marker' R'')

-- LADDER FOLD: the whole interior as ONE ∀n induction.
theorem ladderFold : ∀ (n b) , 4 ≤ b → ∀ (q) (marker' R''),
    ∃ q', steps (ladderSteps b n)
        (regenIn b q (2^(b-1)+9) (ladderMarker b n ++ marker') (ladderPad b n ++ R''))
      = some (regenIn (b+n) q' (2^(b+n-1)+9) marker' R'')
```

with the nested seam data
```lean
def ladderMarker b (n+1) = (0 0 1 (01)^{2^b−2}) ++ ladderMarker (b+1) n   -- the ascMarker stack
def ladderPad    b (n+1) = 0^{2^b} ++ ladderPad (b+1) n                    -- the blank pads
def ladderSteps  b (n+1) = (exitSteps b + topGrindSteps b) + ladderSteps (b+1) n
```

**Non-vacuity checked:** `ladderFold 3 5` type-checks to `regenIn 5 → regenIn 8` (the real ladder,
levels 5…8), the exact object measured on the g=2 orbit.

## What closed, and how

- **Residual #1 — the seam** (`braid_topgrind` OUT → `regenIn (k+1)` IN). Discharged in `ladderStep`
  by exactly two banked `List` lemmas: `ones_append_true` (the block's leading `1` merges the marker
  layer into `ones (2^{k+1}−3)`) and **`zeros_pad`** (the `0 0 0^7` OUT seam + the `2^k` pad = the
  `0^{2^k+9}` pad `regenIn (k+1)` needs). The marker unwrap is a pure `cons`/`append` reassociation.
  No new machine reasoning — the transports were already proven.
- **Residual #2 — the assembly induction.** Discharged in `ladderFold` by induction on `n`, each step
  peeling one `ladderStep`. **The key enabler was `regenLaw_pos`** — the already-banked `∀`-position
  form of `RegenLaw` (RegenLaw itself is `∃p`; `regenLaw_pos` lifts it to any `q` via
  `steps_pos_shift`). Without it the `∃p` positions would not thread; with it the fold composes
  cleanly. This is the same "the missing piece was already banked" pattern by which `RegenLaw ∀k`
  itself closed.

So **the entire interior of the doubling phase — the ~1/3 in RegenLaw transports AND the ~2/3 in
topgrind gaps — is now one Lean theorem, `∀n ∀b≥4 ∀q`.** No new transport was needed; both rails
(`regenLaw_closed`, `braid_topgrind`) were banked, and the assembly is `ladderFold`.

## What remains for T7 (honest)

`ladderFold` is the interior. `h_doub ∀g` still needs the **boundary**, now precisely three items:
1. **The head** `M6(g) → regenIn 5 (…full nested marker/pad…)`. Measured lengths 6580 (g=2), 53382
   (g=3), 25024 (g=4) — parity-split, not yet a closed form. This is where the generation's initial
   nested `ladderMarker`/`ladderPad` must be shown to be what `M6(g)` actually presents.
2. **The top-rung exit** `regenIn (g+9?) → M1(g+1)`. (The g=3 `+80` boundary anomaly lives here.)
3. **The `∀g` wiring**: that generation `g`'s phase is `ladderFold` from `b=5`, `n = g+4` rungs
   (levels 5…g+9), i.e. that `M6(g)`'s marker/pad ARE `ladderMarker 5 (g+4)` / `ladderPad 5 (g+4)`.

These are boundary/counting objects, not new transports. `ladderFold` removed the bulk.

## Caveat

`ladderFold` proves the ABSTRACT ladder: from a `regenIn b` config carrying the nested-marker/pad
data, `n` rungs reach `regenIn (b+n)`. It does **not yet** prove that the real `M6(g)` orbit presents
that data — that is boundary item #3, unproven. So this is a proven reduction of the doubling-phase
interior to the boundary, not a proof of `h_doub`. No machine is decided; no label is upgraded.
`lake build T7Ladder` green, `[propext, Quot.sound]`, no `sorry`.
