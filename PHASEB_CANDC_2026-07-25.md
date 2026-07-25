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
