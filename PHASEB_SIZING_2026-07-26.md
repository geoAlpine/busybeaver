# Phase B sizing after `C` — what the next machines actually cost (2026-07-26)

`C` cost almost nothing because it **is** `x2`'s transition graph, started in a different state.
`D`, `E`, `F`, `H` are genuinely different tables.  This is the measurement that sizes them.
**No machine decided beyond `x2`; `C`'s label is held pending its cold build.**

## `D = 1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---` — measured

* **`D` grows LEFTWARD.**  At every milestone the head sits at `+16, +24, +32, +40, +48`
  (uniform `+8`), the RIGHT tape is entirely blank, and all content is to the left.
  `x2` is the mirror image.
* Milestone left tapes, read outward from the head:

      even-type (t = 291 168, 4 846 662) : 0^33 (1 0)^…
      odd-type  (t = 66 906, 1 196 412)  : 0^2 (1 0)^4 0^6 (1 0)^…

  So `D` alternates two milestone shapes, exactly as `x2` does.

## What ports and what does not

| layer | `C` | `D`, `E`, `F`, `H` |
|---|---|---|
| `TapeCalc` — boundary congruences (forward, reverse, EXACT) **on both sides**, translation, monotonicity, `nonhalt_of_invariant` | reused | **reused** — and the LEFT half matters here, since `D` grows leftward |
| comb primitives `pow10`, `pow01`, `ones`, `zeros` and their algebra | reused | **reused** — `D`'s markers are built from the same primitives |
| `x2`'s specific words: `uUnits`, `m1casc`, `frameZ`, `descCascade`, `seamZ`, `oddSeamZ` | reused verbatim | **NEW** — `D`'s marker words are a different structure over the same alphabet |
| the tiles (`descLaw`, `ladderToCascade`, `topRung`, `frameFold`, the carry folds) | reused verbatim | **NEW** — must be measured and built |
| the phase skeleton (low → entry → descent → ladder → rung → tail) | reused | expected to recur, but must be measured |

> **`C` was a re-instantiation; `D`/`E`/`F`/`H` are new developments on a much larger reusable
> base.**  What `x2` had to build from nothing — the boundary calculus, the non-halting wrapper, the
> comb algebra — is now library.  What remains per machine is its own word structure and tiles.

## Consequence for the plan

* Building the **left twin** of the dichotomy in `TapeCalc` (move 2) was not optional bookkeeping —
  `D` grows leftward and would otherwise need the whole boundary calculus re-proved mirrored.
* A cheaper route for left-growing machines exists and should be checked first: the holdout list is
  deduplicated up to **left–right reversal**, so the reversed machine is the same entry.  Reversing
  `D` gives a right-growing machine, which may match `x2`'s word structure more directly.  **That is
  the first thing to measure for `D`, before any Lean work.**

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**


## `D` reversed — and the species distinction

The holdout list is deduplicated up to left–right reversal, so `D^R` is the same entry:

    D   = 1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---     (grows LEFT)
    D^R = 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---     (grows RIGHT)

`D^R`'s milestone right tapes:

    even-type : 0^33 ++ pow10 k      (a long dense (1 0) comb, 43+ alternating runs and continuing)
    odd-type  : 0^2 (1 0)^4 0^6 ++ pow10 k

Compare `x2`'s `MEven 0 []`:  `0^21 ++ uUnits 1 ++ (1 :: 0^10 ++ ones 1021 ++ m1casc …)`.

> **`x2` and `D` are different species.**  `x2` is a CASCADE doubler — a sparse `uUnits` register
> (`(1 0^6)^k`) plus long `ones` blocks in a descending `2^k − 3` cascade.  `D` is a COMB doubler —
> a pure dense `pow10` register.

That is a genuinely new word structure, so `D` needs its own development.  But `pow10` / `pow01`
and their algebra are already library (built for `x2`), and a pure comb register is *simpler* than a
cascade, so `D` may well be **cheaper than `x2` was**, not harder.

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**
