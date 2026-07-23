# O1 + H — measured (2026-07-24)

Two cheap measurements taken after M-even closed, both bearing directly on the remaining
obligations. Instrument: `x2r2_sim.py` (anchors M1(1..3) exact) and Lean `#eval`.
**No machine decided. No label upgraded. `x2` remains `[OPEN]`.**

---

## O1 — the ladder IS canonical at ODD g `[MEASURED, g=3 full phase]`

Full-shape scan of every `regenIn`/`cascadeReg` with `k ≥ 9` in `[M1(3), M1(4)]`
(`x2o1_oddcanon.py`, left comb checked against the Lean definitions, not just the right):

| level | hits | verdict |
|---|---|---|
| `cascadeReg 9` | 4 | **CANONICAL** (comb 255 ≥ 254) |
| `cascadeReg 10` | 2 | **CANONICAL** (comb 511 ≥ 510) |
| `cascadeReg 11` | 1 | **CANONICAL** (comb 1024 ≥ 1022) |
| `cascadeReg 12` (= g+9) | **0** | does not occur |

**7 / 7 canonical, zero failures.** The last canonical level is `11 = g+8`, and there is no
`cascadeReg (g+9)` at all — exactly the even-g rule (`canonical through g+8, the top is not`).

The `regenIn … comb = -1` rows are separator-check failures at *interior* positions (the nested
sub-ladder calls); the same pattern occurs at even g and is not the main climb.

**Consequence — O3's risk drops sharply.** `ladderToCascade`, `topRung`, `seam74` and
`topRungToMilestone` are all stated `∀ marker`/`∀ k` and their endpoint families DO occur at odd
g in full shape. So the odd branch differs from the even one **only** in `topEntry` (O2) and the
approach to the tail's IN, not in the ladder. The "one remaining mathematical unknown" is
correspondingly narrower than the strategy review priced in.

---

## H — the padding law for `h_low`, measured exactly `[MEASURED, g=2 and g=4]`

Obligation H must carry the canonical milestone families to the *realized* configs the phase
theorems consume. `doubPhaseEven` starts from `M6` with left `[false] ++ zeros 10 = zeros 11`.
Measuring `h_low`'s transport under a left pad of `zeros k`:

| pad `k` | 6 | 8 | 12 | 16 |
|---|---|---|---|---|
| `M6`'s left afterwards | `zeros 1` | `zeros 3` | `zeros 7` | **`zeros 11`** |

so **`zeros k` in ⟹ `zeros (k−5)` out, for `k ≥ 6`** (identical at g=2 and g=4; the canonical
`k = 0` case gives `[false] = zeros 1`, the recorded `M6` left).

**Therefore `k = 16` is the value H needs**: padding `M1(g)`'s left with `zeros 16` makes
`h_low` deliver exactly the `zeros 11` left that `doubPhaseEven` consumes. The right lengths
already agree (2077 = `(M6 2).tape.right.length`).

What is NOT yet proven: the padded `h_low` itself. `BlankNorm.steps_lpad_zeros` gives only
`∃ j ≤ k`, and the measurement pins `j = k − 5`; pinning it in Lean needs either a
lower-bound variant or a free-left restatement of `h_low_even_core` (whose `TAIL` is already
free but whose left is the concrete `[]`). That is H's remaining content, now a *numerically
specified* task rather than an open one.

---

## Status of the S-list after these two

| # | obligation | state |
|---|---|---|
| E1/E2/E3 | even phase | **CLOSED** (`doubPhaseEven`, GREEN) |
| O1 | odd canonicity | **MEASURED — ladder is canonical, same as even** |
| O2 | odd `topEntry` | open (measure the odd 4-phase, then M8 assembly) |
| O3 | odd ladder-top → tail | open, **risk reduced by O1** |
| O4 | odd assembly | open |
| H | families → init | **padding law measured (`k=16`)**; padded `h_low` unproven |
| F | fire + audit | open |
