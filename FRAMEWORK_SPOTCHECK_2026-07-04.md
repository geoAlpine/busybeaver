# Framework spot-check — 6 fresh unseen holdouts all fit the grand synthesis, no anomaly (2026-07-04)

*Detailed per-machine validation of the session's framework (`GRAND_SYNTHESIS_2026-07-04.md`) on **6 randomly-picked,
previously-unanalyzed** holdouts (lines 200/300/552/700/800/1000 of the 1104). Each was fully characterized (halt
gate + block-structure growth). **All 6 fit** — every one has a bounded-context `00`/`11` existence gate and is
either an o3-type bounded-alphabet odometer or an o17-type skew product. **No anomaly.** SOUNDNESS: `[OBSERVED]`;
halting `[OPEN]`; no machine decided.*

## The 6 spot-checks `[OBSERVED, 10 M steps each]`
| line | TM | halt gate | structure |
|---|---|---|---|
| L200 | `1RB1RE_1RC1LE_1LD0RA_1LF0LA_1LB0LC_---1RA` | `F:0` (unique-pred, `00`) | **o3-type** (maxblk `17→21` bounded, #blk `28→416` grows) |
| L300 | `1RB0RE_1RC1RE_1LD1RA_1LA0LD_0RA0LF_1LD---` | `F:1` (unique-pred, `11`) | **o3-type** (maxblk `2→3` bounded — a `{1,11}` alphabet odometer) |
| L552 | `1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD` | `F:0` (unique-pred, `00`) | **o17-type** (maxblk `13→1200` grows) |
| L700 | `1RB1RE_1LC0RA_0RD1LB_---1RC_1LF1RE_0LB0LE` | `D:0` (unique-pred, `00`) | **o17-type** (maxblk `94→849` grows) |
| L800 | `1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA1LD` | `D:1` (**2**-pred, disjunctive) | **o17-type** (maxblk `25→971` grows) |
| L1000 | `1RB1LA_0LC0RE_1LD1LB_1RE1LF_1RC0RA_0RC---` | `F:1` (unique-pred, `11`) | **o3-type** (maxblk `2→2` — pure bounded-alphabet) |

## Reading
- **Every fresh machine fits the grand synthesis:** a **bounded-context existence gate** (5 unique-predecessor
  `00`/`11`, 1 two-predecessor disjunctive — matching the 87%/13% gate census) over a **non-affine growing
  structure** that is either an **o3-type odometer** (all blocks bounded — L200/L300/L1000, the last two pure
  `{1,11}` alphabets) or an **o17-type skew product** (a block's length unbounded — L552/L700/L800). No value-orbit
  (Type-I) or scalar (Type-III) in this small sample; 3:3 o3/o17 (small-sample noise around the 81%/16% census).
- **No anomaly** — nothing outside the {o3-type, o17-type} × {`00`/`11` gate} predicted by the framework. The
  detailed per-machine picture matches the aggregate censuses (gate, structural) on unseen data.

## Addendum — even the simplest machine (L1000, pure `{1,2}`) is not trivially decidable `[OBSERVED]`
L1000 has the **simplest** structure in the sample (`maxblk = 2` throughout — a pure `{1,11}`-alphabet odometer,
the extreme o3-type). Tested for decidability: **not trivially so.** Its digit string (`block-length−1`) is
**dominated by `0`s with rare `1`s** (an almost-all-single-block tape with occasional doublings), **linear-ish
subword complexity** (`p(ℓ)=2,4,8,12,15,18,21,24` — low, like o3), but **non-periodic** (complexity keeps growing)
with a **growing carry-defect** (`maxgap 3→4` — the cascade produces widening `0`-runs). So L1000 carries the exact
o3 signature — **statically simple (low complexity) but dynamically irregular (non-periodic, growing carry
defects)** — and is *not* eventually periodic (as no holdout is) nor obviously affine/automatic. The "simplest
structure ⇒ maybe decidable" hope does **not** pan out; even the extreme o3-type machine has Collatz-hard-looking
carry dynamics. (A rigorous decidability call needs the cycle-phase recurrence analysis that showed o3 irregular,
`O17_O3_STRUCTURE §3c`.) No decidable cryptid found.

## Honest verdict
**(b) — a clean detailed validation.** 6 randomly-picked, previously-unanalyzed holdouts each fully fit the grand
synthesis (bounded-context existence gate + non-affine o3/o17 structure), with no anomaly — complementing the
frontier-wide aggregate censuses with per-machine confirmation on fresh data. The framework predicts unseen machines
correctly. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad` (`/opt/homebrew/bin/python3.13`): per-machine halt-gate (unique/multi-predecessor, `00`/`11`) +
  block-structure trajectory (maxblk bounded ⇒ o3-type, grows ⇒ o17-type). Lines 200/300/552/700/800/1000 of
  `_bbdata/bb6_holdouts_1104.txt`. Basis: `GRAND_SYNTHESIS_2026-07-04.md`, `CRYPTID_GATE_CENSUS_2026-07-04.md`,
  `STRUCT_CENSUS_2026-07-04.md`.
