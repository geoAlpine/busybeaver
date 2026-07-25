# The template island's species — `x2` is the outlier (2026-07-26)

M0 over the confirmed island members.  **No machine decided beyond `x2`.  No label upgraded.**

| machine | milestone side | state | head-pos step | marker word | species |
|---|---|---|---|---|---|
| **`x2`** | L | `E` | **−6** | `0^21 ++ uUnits 1 ++ (1 :: 0^10 ++ ones 1021 ++ m1casc …)` | **CASCADE** |
| **`D`** (`D^R`) | L | `A` | **−8** | `0^33 ++ pow10 k` / `0^2 (10)^4 0^6 ++ pow10 k` | **COMB** |
| **`F`** | L | `A` | −8, −9, −12, −13, −16 | `0^2 (10)^2 0^3 (10)^…` | **COMB** |
| **`H`** | L | `D` | **−16** | `0^2 (10)^…` | **COMB** |
| **`E`** | (L, per the confirmed run) | — | — | `(1 0)` comb | **COMB** (epoch pick needs redoing; the automatic side-choice landed on early micro-clusters) |

Span ratios, all → 4:

    F : 79 143 → 305 817 → 1 194 113 → 4 735 155      (3.86, 3.90, 3.97)
    H : 132 098 → 542 672 → 2 170 322 → 8 715 260     (4.11, 4.00, 4.02)
    D : 12 710 → 52 776 → 224 262 → 905 244 → 3 650 250 → 14 641 536  (4.15 … 4.01)

## The finding

> **The island is dominated by COMB doublers — a dense `pow10` register.  `x2` is the outlier**, a
> CASCADE doubler with a sparse `uUnits` register and descending `2^k − 3` `ones` blocks.

That matters for Phase B's cost: `x2`'s machine-specific layer (`uUnits`, `m1casc`, `frameZ`,
`descCascade`, `seamZ`) does **not** transfer to `D`/`F`/`H`/`E` — but a **comb-doubler sub-template
built once may serve all of them**, since they share the register shape.  So the right next move is
not "port `x2` to `D`" but "build the comb-doubler machinery on `D`, designed to be `∀`-parametric
from the start, the way `x2`'s turned out to be."

`x2`'s development already demonstrated the payoff of that discipline: because every lemma was `∀`
in the indices that differ, the second machine (`C`) needed **zero new dynamics**.

## Caveat

`E`'s milestone extraction needs redoing — the automatic side-choice picked early micro-clusters
(`t = 109 … 708`) instead of the epoch scale where its `(2,4)` signature was confirmed.  That is a
tooling fix, not a finding about `E`.

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**
