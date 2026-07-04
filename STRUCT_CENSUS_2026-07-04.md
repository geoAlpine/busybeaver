# Frontier structural census — the Type-II band splits ~81% o3-type / ~16% o17-type (2026-07-04)

*Frontier-wide structural census (`struct_census.py`, all 1104 holdouts, 600 K steps each) by the **max-block-length
trajectory**, refining the tetrachotomy's dominant "Type-II" cell into the two structures found this session:
**o3-type** (uniform bounded-alphabet odometer — all blocks bounded, block-count grows) vs **o17-type** (skew
product — some block's length is unbounded). Result: the frontier is **dominated (~81%) by o3-type odometers**, with
**o17-type skew products a substantial ~16% minority**. SOUNDNESS: `[OBSERVED]`, **crude classifier** — reliable for
the o3/o17 split, **under-counts dense Type-I value-orbits** (balance-counter contamination); no machine decided.*

## The census `[OBSERVED, crude, all 1104]`
| structure | count | share |
|---|---|---|
| **o3-type** — bounded-alphabet odometer (max-block bounded, #blocks grows) | **898** | **81 %** |
| **o17-type** — skew product (a block's length unbounded; #blocks grows or bounded) | **182** (159+23) | **16 %** |
| mixed | 16 | 1.4 % |
| dense value-orbit (few blocks, value grows) | 8 | 0.7 % |

## Reading
- **The frontier is dominated by o3-type bounded-alphabet odometers (~81%)** — a growing string of bounded-value
  blocks (like o3's `1`/`5` runs), whose halt is a `00`/`11` carry-defect existence (generalized-Collatz, and — as
  `O17_O3_STRUCTURE §3c` showed for o3 — with an *irregular non-affine* carry recurrence, Collatz-hard).
- **o17-type skew products (unbounded interior) are ~16%** — not rare: a substantial minority of the frontier has
  o17's structure (a bounded finite-state base over an unbounded carry/value fiber).
- So the tetrachotomy's `~80% Type-II` cell **splits structurally into `~81%` o3-type + `~16%` o17-type**; the two
  Type-II exemplars (o3, o17) are the two dominant frontier structures, in a `~5:1` ratio.

## Honest caveat `[the classifier's limit]`
The crude max-block/#blocks classifier **under-counts dense Type-I value-orbits** — it reports only 8, but the named
Type-I machines alone (o2, o7, o11, o12, o13, o14, o16, o4, Antihydra-class) exceed that. Type-I two-counter
machines carry a balance counter that inflates the block structure, so they mis-classify as o3-type or o17-type
(the same contamination the ratio census hit, `RATIO_CENSUS_2026-07-04.md`). **So the `o3-type` bucket contains an
unknown number of mis-classified Type-I machines**; the reliable statement is the *qualitative* dominance of
bounded-alphabet-odometer structure and the substantial o17-type minority, not the exact Type-I count. A clean
per-machine split remains `(K)`-hard (`BB6_TYPE_IV_CENSUS §5c`).

## Honest verdict
**(b) — a structural refinement of the tetrachotomy's Type-II cell.** The frontier is dominated (~81%) by o3-type
bounded-alphabet odometers, with o17-type skew products a substantial ~16% minority — the two Type-II exemplars are
the two dominant frontier structures (~5:1). Caveat: the crude classifier under-counts dense Type-I value-orbits, so
the o3-type bucket is contaminated; the qualitative split is robust, the exact Type-I count is not. **No machine
decided. No label upgraded.**

## Reproduce
- `scratchpad/struct_census.py` — max-block-length + #blocks trajectory (50 K/200 K/600 K), classify bounded-vs-growing.
  Data `_bbdata/bb6_holdouts_1104.txt`, interpreter `/opt/homebrew/bin/python3.13`. Basis:
  `O17_SKEW_PRODUCT_2026-07-04.md` / `O17_O3_STRUCTURE_2026-07-04.md` (o3-type vs o17-type), `BB6_TYPE_IV_CENSUS_2026-07-04.md`.
