# Trichotomy-extension test: a FOURTH type appears — the frontier classification is a TETRACHOTOMY (2026-07-04)

*A falsifiable test of whether the cryptid **trichotomy** (`CRYPTID_CLASSIFICATION_2026-07-04.md`) extends across
the 1104-holdout frontier: five **un-analyzed** holdouts, one from each structural band, reverse-engineered from
blank tape (parallel agents; orchestrator-verified vs the raw TM on the decisive claims). Result: the trichotomy
is **incomplete** — a **fourth type** (fixed-arity nested-counter bouncers) appears, and **growth-rate is fully
orthogonal to type**. SOUNDNESS: `[PROVEN]`/`[OBSERVED]`; **no machine decided; halting `[OPEN]` for all five**.*

## The five tests and their verdicts

| # | machine | predicted | **verdict** | key evidence |
|---|---|---|---|---|
| **H1** | `1RB0LC_0LC1RF_1LE1RD_0RC1RC_0LA1LA_---1RA` | Type I | **Type I** (Mahler-3/2, Antihydra/o2/o7 subfamily) | ×3/2 active-counter orbit (ratio→1.5, refutes 8/3,4/3); inner invariants `X+3V`, `V−Y`; halt = B hits a block-end/unit `1` (dual of o4's 11-gate), 0 firings/150M |
| **H2** | `1RB---_0LC0LB_1RF0LD_1RE0RB_1LB0RC_0RD1RA` | Type II | **Type II** (o3-dual) | bounded digits {1..4}, log digit-sum, no value orbit; halt = F reads `11` (dual of o3's `00`), 0 firings/200M *(orchestrator-verified: F,1×2, right-nbr 1: 0; max block 3)* |
| **H3** | `1RB---_0LC1RF_0LD1LC_1RE1LB_0RE1LA_0RB0RA` | Type II | **Type II, CUBIC-time** (`step^{1/3}`) | bounded {1,2} digits, `S~log`, `step≈0.165 m³`; markers at doubling positions; 111-existence gate |
| **H4** | `1RB---_0LC0LF_1RD0LB_1RE0RC_0RF1RA_1LB0RC` | Type I odometer | **Type II** (refutes proxy) | NO rational value orbit (brute p<25: 0 fits, best resid 20); `S~√t` (richer than o3's log, still no Mahler value); 11-existence gate |
| **H5** | `1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA` | Type III / nested | **TYPE IV (new)** | **fixed-arity ~4 counters** (orchestrator-verified: #1-blocks stays 3–6 while W:159→1051), cubic-time, inner base-3/2 **descent** `A↦⌈2A/3⌉`, halt = F meets a `11` adjacency |

## Findings

**1. A genuine fourth type (H5): fixed-arity nested-counter bouncers.** H5's tape is a **bounded number of unary
counters** (`~4`, orchestrator-verified to stay 3–6 as width grows to 1051), separated by single/`0²` gaps,
running in **cubic time**. Its content is neither an exponential Mahler value orbit (Type I), nor an unbounded/
growing digit string (Type II, where `#blocks ∼ width`), nor a single scalar block (Type III). Its inner map is a
mass-conserving base-3/2 **descent** `A↦⌈2A/3⌉` (verified: `83,56,38,26,18,12,8,6,4`) to a fixed point, then
refill — a **fixed-arity counter machine**, a distinct fourth phenotype. So the frontier classification is a
**tetrachotomy**: I Mahler / II bounded-digit outlier / III scalar-Collatz / **IV fixed-arity counter bouncer**.

**2. Growth-rate is FULLY orthogonal to type.** This session's "√t is not diagnostic" sharpens to: every
growth band contains multiple types. `step^{1/3}` (cubic) now holds a Type II (H3), a Type III (Space Needle),
and a Type IV (H5); `√t` holds Type I (H1, o2, o7, Antihydra) and Type II (H2, H4, o3, o17). **The wall is set by
the content (value orbit vs bounded cascade vs scalar vs fixed-arity counters), never by the growth exponent.**

**3. Type II is common, and the census proxy over-estimated Type I.** Three of the five (H2, H3, H4) are Type II
— including **H4, which the digit-sum-growth proxy (A6) had flagged as a Type-I bounded-radix odometer**: deep RE
refutes it (no rational value orbit; `S∼√t` is a free-running counter, not a `⌊(p/q)x⌋` odometer). So the A6
proxy's `~190 Type-I odometers` is an **over-estimate**; the o3-class Type II band is larger than the proxy
suggested. **A clean per-machine Type-I/II split genuinely needs reverse-engineering** — confirmed.

**4. The `11`/block-end existence gate (dual of o3's `00`) is ubiquitous.** H1 (block-end), H2, H4, o4 all halt on
an `11`/adjacency-existence gate; o3/o11/o12/o14/o16/SN on `00`. All are `[PROVEN from the table]` unique-
predecessor gates, never firing from blank — halting is a Collatz-fragile adjacency/existence race in every case.

## Honest verdict

**(b) a materially new characterization: the trichotomy → tetrachotomy, plus growth ⊥ type.** The five tests
**strengthen** the "frontier gated by two walls" thesis for the halting *reduction* (H1 → (K)/Mahler; H2/H3/H4 →
generalized-Collatz carry-existence; H5 → generalized-Collatz adjacency over a bounded-counter substrate — all
existence/reachability or equidistribution events), while **correcting** the type-count: there are **four**
structural phenotypes, not three, and the proxy split of the bounded-digit band was optimistic for Type I.
Whether Type IV (fixed-arity base-3/2 counters) is genuinely a distinct *wall* or a sub-case of generalized-
Collatz is `[OPEN]` — its halt is still an existence event, but its bounded-arity substrate is closer to a
classical counter machine than the odometers of Type II. **No machine decided. No non-halting proven. No wall
proved. Halting `[OPEN]` for all five.**

## Reproduce
- Per-machine scratch verifiers in the session scratchpad (`h1_*`, `h2_*`, `h3_*`, `h4_*`, `h5.py`, …), each
  printing its normal-form/halt-gate/value-orbit checks. Orchestrator spot-checks (H2 halt gate + bounded digits;
  H5 fixed-arity #blocks vs width) reproduced independently. TMs are 5 rows of `_bbdata/bb6_holdouts_1104.txt`.
  Interpreter `/opt/homebrew/bin/python3.13`.
