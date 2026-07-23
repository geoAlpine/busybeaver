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

---

## O2 — the odd `topEntry`: head shared with even, bulk UNMAPPED `[MEASURED, g=3]`

Odd `M6 g` right = `0 · (10)^4 · 1^9 · 00 · rUnits g · (10)^10 · 1^{2^{g+8}−13} · m1casc(g+6)(g+7)`
(vs even: `rUnits (g+1)`, then `1 0 0`, then `1^{2^{g+8}−3}`).

**`[PREDICTED → CONFIRMED]` (M4).** From the confirmed odd `topEntry(g) = 6080·2^g + 53g + 105`
minus `h_low_odd`'s `N(g) = 305 + 38g`, the `M6 → entry` span should be `6080·2^g + 15g − 200`,
i.e. **48 485 at g=3**, entry at 2 900 995. Stated before the run; the measured `descIn 9` entry
is at exactly 2 900 995. ✓

### Good news — the opening is IDENTICAL to the even branch

| phase | odd (g=3) | even |
|---|---|---|
| P1 | rel 0…88, 4 cycles of 22, blocks 9,7,5,3,1 | **same** |
| T | rel 88…99, 11 steps | **same** |
| `rUnitsFold` | rel 99…144, 15 steps/block, `g` blocks | **same tile**, `g` vs `g+1` blocks |

So `p1t` (99 steps) and `rUnitsFold` apply to the odd branch **verbatim** — the first 144 of the
48 485 steps are already proven machinery.

### The finding — the odd bulk passes through NO known family

Scanning rel 144 … 48 485 for `descIn` / `regenIn` / `cascadeReg` at **full shape**:

```
1 known-family config found — and it is the endpoint itself (descIn 9 @ rel 48 485).
```

The remaining **48 341 steps** (99.7 % of the odd `topEntry`) traverse configurations in none
of the established families. Where the even branch crossed `1 0 0` in 3 steps and then chewed
one big block (`eChewFold`, 1 536 steps at g=2), the odd branch crosses `(10)^10` and then does
something ~30× larger that has not been characterised.

**This is the real content of O2/O3**, and it is a *discovery* task of the same kind as the even
4-phase decomposition was — not an assembly task. O1's result (the ladder is canonical at odd g)
does **not** cover it: the unmapped stretch is inside `topEntry`, before the ladder.

**Honest revision to the strategy review.** O3 (odd ladder-top → tail) was priced as the one
mathematical unknown; that is now understood to be *low* risk (O1). But **O2's bulk is a second,
larger unknown** that the review did not price, because the odd `topEntry` had only ever been
measured as a *cost* (the closed form), never as a *structure*. Its discovery needs its own
measurement campaign.
