# Phase B — candidate C, foundation and first measurements (2026-07-25)

`C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD`, a member of the 1104-holdout residual selected by
the pre-flight (`PREFLIGHT_2026-07-25.md`).  Set up in `lean/CandC.lean` on the machine-independent
`TapeCalc`.  **No machine decided. No label upgraded.**

## Instrument audit — clean

    table read back cell by cell : 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD
    spec                         : 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD
    initC                        : (A, 0, [], false, [])
    halting transitions          : [(A, true)] only — exactly the `---` field
    halt reachable, none propagates : steps 1 and steps 400 from (A reading 1) are `none`

## Lean ↔ simulator agreement

`#eval` of `steps TC n initC` at the four MEASURED milestone times reproduces the Python
measurements exactly:

| step | state | pos | left | right |
|---|---|---|---|---|
| 49 469 | C | −19 | 0 | 522 |
| 192 508 | C | −22 | 0 | 1037 |
| 727 066 | C | −28 | 0 | 2067 |
| 2 866 580 | C | −34 | 0 | 4121 |

Head position advances by a uniform `−6` per milestone, as `x2` does.  Note `left.length = 0` at
every milestone — `C`'s left tape is completely empty, where `x2`'s carried one blank.

## The milestone marker words ARE `x2`'s word family (the decisive Phase-B measurement)

Run-length encoding of `C`'s milestone right tapes:

    @192 508  (w 1037) : 0^26 1^509  0^2 1^253  0^2 1^125 0^2 1^61 0^2 1^29 0^2 1^13 …
    @727 066  (w 2067) : 0^22 1 0^4 1 0 1 0 1 0 1 0 1 0 …
    @2 866 580(w 4121) : 0^22 1 0^6 1 0^10 1^2045 0^2 1^1021 0^2 1^509 0^2 1^253 …

* the descending blocks are **exactly `2^k − 3`**: `509 = 2⁹−3`, `253 = 2⁸−3`, `125 = 2⁷−3`,
  `61 = 2⁶−3`, `29 = 2⁵−3`, `13 = 2⁴−3`; and `2045 = 2¹¹−3`, `1021 = 2¹⁰−3`.  That is `x2`'s
  **`m1casc`** — "the milestone cascade `0^2 1^{2^hi−3} 0^2 1^{2^{hi−1}−3} …`" — verbatim.
* the even-milestone prefix `0^21 (1 0^6) 1 0^10 1^{2^k−3} 0^2 …` is `x2`'s
  `MEven h R`.right `= zeros 21 ++ (uUnits (2h+1) ++ (1 :: (zeros 10 ++ evenLowFrame h R)))`
  with `uUnits 1 = 1 :: zeros 6`.
* the odd-milestone prefix `0^21 1 0^4 (1 0)^… ` is `x2`'s
  `MOdd h R`.right `= zeros 21 ++ (uUnits j ++ (1 :: (zeros 4 ++ (pow10 6 ++ (ones 4 ++ …)))))`.

The `uUnits` count and the cascade's top index are offset from `x2`'s by the one-epoch phase shift
already measured (`PREFLIGHT` §4).

> **The `x2` word algebra — `m1casc`, `uUnits`, `pow10`, `pow01`, `ones`, `frameZ` — applies to `C`
> verbatim.**  That is the machine-specific layer of the whole `x2` proof, and it ports.

## What remains for `C`

1. Re-measure the tile step counts (they differ from `x2`'s: milestones at
   `49 469 / 192 508 / 727 066 / 2 866 580` vs `52 132 / 188 098 / 732 732 / 2 852 090`).
2. Re-index the word-algebra lemmas by the phase offset and the `−7` width offset.
3. Reuse `TapeCalc` wholesale, then `chainE`-style depth induction and `nonhalt_of_invariant`.
4. Entry segment + audit, as for `x2`.

**No machine decided. No label upgraded. Push HELD.**

## The epoch SKELETON is `x2`'s, offset by a constant 6 (MEASURED)

Sampling head position and max-reach at 28 equally-spaced fractions of one epoch
(`x2` 732 733 → 2 852 091, `C` 727 066 → 2 866 580):

| fraction | `x2` max-reach | `C` max-reach | diff |
|---|---|---|---|
| 0.04 | 2329 | 2323 | 6 |
| 0.07–0.18 | 2585 | 2579 | 6 |
| 0.21 | 2841 | 2835 | 6 |
| 0.29–0.71 | 3097 | 3091 | 6 |
| 0.79 | 3353 | 3347 | 6 |
| 0.82–0.93 | 3609 | 3603 | 6 |
| 0.96 | 3865 | 3859 | 6 |
| 1.00 | 4121 | 4115 | 6 |

* **The plateau skeleton is identical** — same number of plateaus, at the same fractions of the
  epoch, with max-reach differing by exactly `6` throughout.
* The plateau levels `2585, 3097, 3609, 4121` are an arithmetic progression of step
  `512 = 2⁹` — **that is the LADDER**, and `C` has the same rungs.
* Both epochs END at head offset `−2`.
* The fine structure (`dpos` inside each plateau) DIFFERS: `x2` marches monotonically right where
  `C` oscillates.

  **CORRECTION (measured after the above was written).**  I inferred from the differing `dpos`
  wiggle that "the tile step counts are genuinely different and must be re-measured".  **That was
  wrong.**  Measuring the plateau ARRIVAL TIMES and the spans between them shows the tile
  arithmetic largely ports — see the next section.

### Honest scope of the port

| layer | portability |
|---|---|
| `TapeCalc` (boundaries, translation, monotonicity, non-halting) | **verbatim** — already machine-independent |
| word algebra (`m1casc`, `uUnits`, `pow10`, `pow01`, `ones`, `frameZ`) | **verbatim, re-indexed** by the one-epoch phase and the `−6/−7` offset |
| phase skeleton (descent → ladder → top rung → tail; ladder step `2⁹`) | **same shape**, re-indexed |
| tile step counts | **largely SHARED** — see the plateau-span measurement below |
| the fine trajectory inside a plateau | differs (`x2` monotone, `C` oscillating) |
| entry segment, audit | same method as `x2` |

**No machine decided. No label upgraded. Push HELD.**


## The tile SPANS are shared (MEASURED — and this corrects the paragraph above)

Plateau arrival times over 6·10⁶ steps, and the spans between consecutive plateaus:

| | `x2` | `C` |
|---|---|---|
| reach levels | 1530, 1658, 1786, 2554, 2810, 3066, 3322, 3578, 4602, 5114, 5626, 6138 | 1527, 1655, 1783, 2551, 2807, 3063, 3319, 3575, 4599, 5111, 5623, 6135 |
| offset | — | **constant `−3`** |
| spans | 25032, 271624, 25032, 141660, **99464**, **296576**, **99464**, 1084024, **99464**, 586708, **396040**, **1183488**, **396040** | 271544, **25032**, **99464**, 62380, **99464**, **296576**, **99464**, 1084104, **99464**, 545884, **396040**, **1183488**, **396040** |

**`25032`, `99464`, `296576`, `396040`, `1183488` appear in BOTH, exactly.**  Only the entry/exit
spans differ (`271624 ↔ 271544`, `1084024 ↔ 1084104`, `586708 ↔ 545884`, `141660 ↔ 62380`).

So the corrected scope of the port is:

* the LADDER tile constants are **shared with `x2`** — the `exitSteps` / `topGrindSteps`-style
  library ports rather than being re-derived;
* what must be re-measured is the **entry and exit episodes** (the spans that differ), i.e. the
  analogue of `x2`'s low phase / topEntry / seam, not the ladder itself.

That is a much smaller job than the previous paragraph claimed.

**No machine decided. No label upgraded. Push HELD.**

## The epoch spans differ from `x2`'s by an alternating `±≈10·2^k` (MEASURED)

Milestones over 5·10⁷ steps, both machines:

| k | `x2` t | `x2` w | `C` t | `C` w | Δw | `x2` span | `C` span | **Δspan** |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 52 132 | 526 | 49 469 | 522 | −4 | 38 463 | 34 907 | **−3 556** |
| 9 | 188 098 | 1044 | 192 508 | 1037 | **−7** | 135 966 | 143 039 | **+7 073** |
| 10 | 732 732 | 2074 | 727 066 | 2067 | **−7** | 544 634 | 534 558 | **−10 076** |
| 11 | 2 852 090 | 4128 | 2 866 580 | 4121 | **−7** | 2 119 358 | 2 139 514 | **+20 156** |
| 12 | 11 329 300 | 8230 | 11 302 994 | 8223 | **−7** | 8 477 210 | 8 436 414 | **−40 796** |
| 13 | 44 986 994 | 16428 | 45 042 284 | 16421 | **−7** | 33 657 694 | 33 739 290 | **+81 596** |

* **width offset is a constant `−7`** from `k = 9` on;
* **the span difference alternates in sign and doubles**: `−3556, +7073, −10076, +20156, −40796,
  +81596` — dividing by `2^k` gives `−13.9, +13.8, −9.84, +9.84, −9.96, +9.96`, converging to
  `±10`;
* **the alternation has period 2 — the even/odd epoch parity**, which is exactly `x2`'s own
  even/odd doubling-phase split.

`x2`'s `k = 11` span is `2 119 358 = costEven 0` and `k = 12` is `8 477 210 = costOdd 0` (both
already `decide`-certified in `T7OddBridge`).  So:

> **`C`'s cost formulas have the same shape as `x2`'s `costEven` / `costOdd`, plus ONE
> parity-dependent `≈ 10·2^k` term.**

The Lean cost definitions therefore port with a single extra summand, to be pinned by re-measuring
the entry/exit episodes.

**No machine decided. No label upgraded. Push HELD.**
