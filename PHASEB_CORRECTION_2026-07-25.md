# CORRECTION — candidate C is `x2`'s own transition graph (2026-07-25)

## What I got wrong

Across several turns I described `C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` as a **new
machine, a "close sibling" of `x2` with the same word algebra**, and made it the prime Phase-B
target.  **That characterisation was wrong.**

`C` is `x2`'s transition table with the states cyclically renamed:

    σ : A→F, B→A, C→B, D→C, E→D, F→E
    σ(x2) = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD = C     (verified, all six rows)

Since TNF pins the start state to `A`, `C` is **the same transition graph started in `x2`'s state
`B`**.  Both appear in the 1104 list because the list is deduplicated up to TNF + left–right
reversal, which fixes the start state — so different start states on one graph are different
entries.

## What was NOT wrong

Every measurement stands; only the explanation was mine to get right:

* the milestone marker words are `x2`'s word family (`m1casc`, `uUnits`, `pow10`, …);
* the epoch skeleton matches with a constant offset;
* the ladder tile spans `25032, 99464, 296576, 396040, 1183488` are shared exactly;
* the width offset is a constant `−7`;
* the epoch spans differ by an alternating `±≈10·2^k`.

All of these now have a one-line explanation: **it is the same table.**

## Structural finding about the residual (new, and useful)

* Of `x2`'s six start-variants, **exactly two are in the 1104 list** — `x2` itself and `C`.
* Computing the graph-canonical form (minimum over all 720 state permutations) of every entry:
  **the 1104 entries comprise 909 DISTINCT transition graphs.**  170 graphs occur more than once,
  covering 365 entries, with multiplicities up to 4.

> **The honest count of independent machines in the residual is 909, not 1104** — about a third of
> the list is the same graph started in different states.  Deciding one graph from all its start
> states can retire up to 4 entries at once.

## Revised Phase-B position

* **`C` is still worth doing** — it is a distinct entry of the 1104 whose orbit genuinely differs
  from `x2`'s (different start ⟹ different milestones, `−7` width, different spans) — and it should
  be **cheap**, because the tile lemmas are about the *same* `step` function.  Deciding it takes the
  `x2` graph's tally from 1 to 2 entries.
* **But `C` is NOT evidence that the template method generalises to a new machine family.**  That
  evidence does not yet exist.
* Of the three pre-flight candidates: **B refuted** at longer runs, **C is `x2`-derived**, so only
  **A** (`1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE`) remains as a possibly-independent target — and
  its `(2, 4)` signature was noisy.
* The **deep screen** (`preflight_1104_deep.py`, 2·10⁷ steps, `(2,4)` signature) is running and will
  give the fuller picture.  It should be re-run with graph-canonical dedup so that start-state
  variants are not counted as separate discoveries.

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**
