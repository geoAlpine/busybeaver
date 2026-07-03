# BB(6) 1104-holdout frontier census — the frontier is structurally homogeneous (2026-07-04)

*Task A2 (`REMAINING_TASKS_2026-07-04.md`): a structural census of **all 1104** BB(6) undecided holdouts
(`_bbdata/bb6_holdouts_1104.txt`, the machines that survived the community's strong deciders), partitioning
them by blank-tape dynamics. Only ~14 named cryptids had been analyzed before; this covers the whole set.
SOUNDNESS: `[OBSERVED]` recon by crude growth-exponent fitting; it **decides nothing** and a growth label does
NOT imply decidability. Reproduce: `holdout_census.py`.*

## Result: growth-class partition (blank tape, cap 4·10⁵, exponent `width ∼ step^a`)

| class | `a` range | count | share |
|---|---|---|---|
| **√t bouncer** | `0.42–0.62` | **665** | 60% |
| **sub-√t** | `0.12–0.40` | **399** | 36% |
| log-growth (very slow) | `< 0.12` | 33 | 3% |
| intermediate | `0.60–0.85` | 7 | 0.6% |
| **halted within cap** | — | **0** | 0% |
| **super-linear / exponential width** | `> 1` | **0** | 0% |

Growth-exponent histogram (rounded to 0.1): bimodal — a dominant **`a≈0.5` peak (571)** and a secondary
**`a≈0.2` peak (217)**, tails at `0.1`(78), `0.3`(77), `0.4`(104), `0.6`(51), `0.7–0.8`(6).

## Three findings

**1. The frontier is uniformly slow polynomial-growth.** Every one of the 1104 holdouts is a
**polynomial-width counter/bouncer** (`a ≲ 0.8`); **none halts within the cap** and **none has super-linear
(exponential) width**. BB(6)'s open frontier is not "a few hard machines among easy ones" — it is **1104
uniformly slow-growing Collatz/Mahler-class counters**, `√t`-dominant.

**2. Width-growth is NOT a hardness discriminant `[re-confirmed at scale]`.** Even **Antihydra** — the flagship
exponential-Mahler cryptid — sits in the `√t` band (`a=0.487`): its *value* grows exponentially but, stored in
binary, its *tape width* grows only `∼√t`. So the growth exponent cannot separate Mahler-hard (Type I) from
Collatz-outlier (Type II) from decidable — the hardness lives in the **content**, exactly as
`CRYPTID_CLASSIFICATION_2026-07-04.md` §1 found for the 9 reverse-engineered machines.

**3. The analyzed cryptids are representative.** All six spot-checked named cryptids are in the set and land
where expected: **Antihydra 0.487, o2 0.502, o3 0.478, o7 0.468, o11 0.543 (√t); Space Needle 0.348 (sub-√t)**.
So the reverse-engineered trichotomy (Type I Mahler-3/2 / Type II Collatz-outlier / Type III scalar-Collatz)
samples the two dominant bands; the 9 exact reductions are representatives of the `√t`/sub-√t bulk, not special
cases. The `a<0.12` log-growth subclass (33) — very slow binary-counter-like machines, still growing at 8M
steps (`w:106→152`) so genuine holdouts, not decidable cyclers — is the one band with no named representative yet.

## What this means for P0 (deciding BB(6))

The census sharpens the obstruction: deciding BB(6) is **not** a heterogeneous zoo but a **homogeneous mass of
1104 slow polynomial-growth counters**, whose halting each (by the analyzed representatives) reduces to a
`⌊3x/2⌋`/`⌊8x/3⌋` equidistribution ((K)/Mahler — Type I) or a generalized-Collatz existence event over a carry
cascade (Type II/III). If the trichotomy extends across the bands — plausible given the representatives but
**`[OPEN]`, not verified for the un-analyzed ~1090** — then BB(6) is gated by the **same two walls** ((K) and
generalized-Collatz) uniformly, rather than by 1104 independent problems.

## Second axis: block structure `[OBSERVED, holdout_census_axis2.py]`

Per-machine final block structure (max 1-block `B`, #blocks `N`, and whether `B` grew):

| structure | count | reading |
|---|---|---|
| **bounded-digit** (`B≤6`, non-growing) | **522** | o3-class: small blocks, growth only by block **count** — no unary value orbit |
| **digit-string** (`N≥8`, `B` grows) | 540 | many blocks + a growing block (o17 / the o11–o16 Mahler "sea + value") |
| unary-counter / scalar (`N≤4`, one big block) | 22 | the value **is** a single block (o2/o7/Antihydra/Space Needle) |
| mixed / small | 20 | — |

Named placements (all as expected): **Antihydra `N=3,B=601`; o7 `N=3,B=434`; Space Needle `N=3,B=160`**
(unary-counter — the value is one block); **o3 `N=242,B=5`** (bounded-digit); **o11 `N=455,B=293`, o2 `N=133,
B=934`** (digit-string — sea/markers + a growing block).

> **Finding: the bounded-digit (o3-class) structure is ~half the frontier, not a rare outlier.** **522** holdouts
> keep every 1-block `≤6` and grow only by adding blocks — the o3 signature (bounded digits + free-running length
> counter, no unary value orbit). o3 is therefore *representative of a large band*, sharpening
> `CRYPTID_CLASSIFICATION_2026-07-04.md` §3 ("o17 not unique") to "the bounded-digit outlier form is a **major
> structural class**." **Caveat:** `B≤6` alone does not settle the kernel question — a bounded-digit tape can still
> hide a Mahler orbit in a bounded-radix numeration (e.g. an o11-style odometer whose marker happened not to grow
> past 6 in-cap). Separating genuine kernel-less outliers (o3) from bounded-digit odometers inside the 522 needs
> per-machine analysis; the count is an **upper bound** on the o3-class, a **lower bound** on non-unary machines.

**Digit-sum-growth proxy split of the ~522** (`holdout_census_axis2.py`; `[OBSERVED, rough proxy]`): binning by
the growth exponent of the #length-`≥2` blocks (the "nonzero digits") gives **~183 log-digit-sum** (o3-like, no
value orbit), **~176 growing** (a value present ⇒ bounded-radix odometer / Type-I-like), **~132 slow**, 33 flat.
So the genuine o3-class is roughly **~183–315**; the bounded-digit band mixes kernel-less outliers with
bounded-radix Mahler odometers. A clean split still needs per-machine reverse-engineering, but the o3-form is a
**major band**, not a rarity.

## Sound-decider confirmation `[OBSERVED, sampled]`

The repo's sound decider suite (`tier3_suite.py`: `verdict` with `sim_cap=2·10⁵`, bouncer/translated-cycler
macro checks) decides **0/15** on a sample — all `HOLDOUT` — consistent with the prior "0/300 decided"
(`cryptid_census.py`) and with these being **community holdouts by construction** (they already survived stronger
deciders). The full 1104 run is prohibitively slow (`≈25 s/machine`, `~7.5 h`) and adds nothing: the frontier is
`0`-decidable-by-available-sound-deciders. So the census's classes are **structural**, not decidability claims.

## Honest scope + verdict

`[OBSERVED]` recon; growth/structure fits are crude and mislabel near boundaries; **no machine decided, none
shown decidable** (sound suite `0/15`). **Verdict:** the BB(6) frontier is a **structurally homogeneous mass of
1104 slow polynomial-growth counters** — two growth peaks (`√t` 665, sub-`√t` 399), no exponential-width or
halting machine — split by block structure into a **large bounded-digit (o3-class) band (~522)** and a
growing-block (unary-value / digit-string, Mahler/counter) remainder. Width-growth is not a hardness
discriminant (Antihydra sits in the `√t` bulk). The 9 reverse-engineered cryptids are representatives of these
bands; **if** the trichotomy extends (plausible, `[OPEN]` for the ~1090 un-analyzed) BB(6) is gated by the same
two walls — (K)/Mahler and generalized-Collatz — uniformly.

## Reproduce
- `holdout_census.py [cap]` — axis 1 (width-growth exponent) over all 1104; class partition + `census_rows.json`.
- `holdout_census_axis2.py [cap]` — axis 2 (block structure: max-block `B`, #blocks `N`); the 522 bounded-digit split.
- Sound suite: `tier3_suite.py` (slow, `~25 s/machine`; sampled `0/15` decided). Interpreter
  `/opt/homebrew/bin/python3.13`. Data: `_bbdata/bb6_holdouts_1104.txt`.
