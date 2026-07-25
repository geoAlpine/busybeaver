# What the 1087-residual axiom actually contains — first census (2026-07-26)

`Completion.lean` carries the residual as ONE opaque axiom `holdouts1087_nonhalt`.  This is the
first measurement of its composition, using the same epoch-ratio method that classified the named
19.  `residual_census.py`, all 1104 entries, `5·10⁶` steps each.
**No machine decided. No label upgraded.**

## The histogram

| epoch width ratio | count |
|---|---|
| **UNRESOLVED** (fewer than 4 epoch clusters at `5·10⁶`) | **673** |
| 7/6 | 26 |
| 9/8 | 21 |
| 5/4 | 20 |
| 8/7 | 19 |
| **3/2** | 16 |
| 6/5 | 16 |
| **4/3** | 10 |
| **2/1** | **5** |
| 9/7 | 5 |
| near-1 band (`1.012 … 1.10`, many distinct values) | ~150 |
| assorted (`11/4, 7/4, 25/8, 17/5, 14/5, 9/5, 8/5, 10/7, …`) | 1 each |

The five at ratio `2`:

    1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE   1.9872   x2  [PROVEN]
    1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD   1.9912   C   (x2's graph, state B)
    1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---   2.0313   H   (confirmed at 4·10⁸)
    1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE   2.0268   A   (REFUTED at 4·10⁸ — phase change)
    1RB0RD_1RC1RB_1LD0LA_1LE0RA_0LF---_0LA0LC   2.0010   B   (REFUTED at 4·10⁸ — phase change)

## Honest reading

1. **The residual is NOT dominated by ratio-2 machines.**  Of the 431 that resolved, five sit at
   ratio `2`, and two of those five were refuted at longer runs.  The bulk are small fractions
   containing an ODD PRIME — `7/6`, `9/8`, `5/4`, `8/7`, `3/2`, `6/5`, `4/3` — i.e.
   **carry-OPAQUE by the transparency criterion, hence `(K)`-like.**
2. **673 of 1104 did not resolve** at `5·10⁶` steps.  That is 61 % of the list, so this census is
   PRELIMINARY, not a verdict.
3. **The near-1 band (~150 machines) is UNCLASSIFIED, not "slow".**  `x2` — a PROVEN clean doubler —
   lands in exactly that band under a crude extractor (`PREFLIGHT_2026-07-25.md` §0).  Reading it as
   "these grow slowly" would repeat the error the pre-flight already caught once.
4. The strict `(2,4)` deep screen at `2·10⁷` steps found **8 entries on 7 graphs** — more than this
   shallower census's five, which is the expected direction.

## What would make it conclusive

Re-run at `≥ 2·10⁷` steps with the `(2,4)` signature AND graph-canonical dedup, and report the
ratio histogram per GRAPH rather than per entry (the 1104 entries comprise only 909 distinct
transition graphs).  Until then the honest statement is:

> The 1087-residual block contains **at least 7 carry-transparent graphs** (the template island) and
> a **large majority whose epoch ratio carries an odd prime**, i.e. `(K)`-like — with 61 % still
> unmeasured.

**No machine decided. No label upgraded. Push HELD.**
