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

## Honest scope + next cut

`[OBSERVED]` recon only; the growth fit is crude and mislabels near boundaries; **no machine decided, none
shown decidable**. The natural **next cut** is a *second axis* — max-1-block growth (unary value present ⇒
Type-I-Mahler-like, e.g. o2/o7; bounded digits ⇒ Type-II-outlier-like, e.g. o3's max block ≡ 2) — to estimate
the Type-I/II split across the 665 `√t` machines. That, plus running the repo's sound decider suite
(`tier3_suite.py`) to confirm `0/1104` decided, would complete the frontier map.

## Reproduce
- `holdout_census.py [cap]` — runs all 1104, prints the class partition, saves per-machine rows to
  `census_rows.json`. Interpreter `/opt/homebrew/bin/python3.13`. Data: `_bbdata/bb6_holdouts_1104.txt`.
