# Automatic multiplier extractor — build, validation gate, and 1104 signal census

*The [C]-frontier engineering of 2026-07-10: a width-independent multiplier extractor built to
test whether the 1087 un-catalogued BB(6) holdouts collapse to the ~5 known engine-classes.
STRICT VALIDATION-FIRST: the tool is untrusted until it recovers the KNOWN multipliers of the
17 named cryptids. Every number below is `[OBSERVED, extractor proxy]`, NOT a certified engine
assignment; it decides NO halting. Scripts: `me_extract.py` (extractor + gate), `me_census.py`
(observe-only 1104 run). Interpreter: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact
big-int. No machine decided. No label upgraded.*

## 1. The extractor method

For a value-×(p/q) counter machine the multiplier lives in the *value*, not the tape width, so
the probe must be width-independent (DATA_SUMMARY §4). `me_extract.py` simulates the machine and
records **milestone events** = record-extreme excursions (the head reaching a new leftmost /
new rightmost cell), deduped so one outward sweep counts once (the raw per-cell record *burst* —
a run of consecutive new-record steps — is collapsed to its apex). It then computes three
independent, width-independent estimators of the abstract counter's multiplier:

- **`rho_time`** (the task's primary estimator) — geometric ratio of consecutive inter-milestone
  **step-gaps** on the *fast* side (one milestone per macro-period), by log-linear regression of
  `log(gap)` vs index. For a counter whose per-period work ∝ value (unary width), `g_{k+1}/g_k → p/q`.
- **`rho_slow`** — noise-filtered geometric ratio of the *slow*-side inter-excursion gaps (cross-check).
- **`rho_val`** — ratio of the tape decoded as a big integer at successive fast milestones (value cross-check).

Each `rho` is matched to the nearest known engine {×3/2, ×4/3, ×8/3, ×5/2} within tolerance, else
the nearest simple rational; two-estimator agreement raises confidence.

## 2. The VALIDATION GATE (17 named) — **FAILED**, and demonstrably so

Running the extractor on the 17 named cryptids (cap 8·10⁶), the primary estimator recovered
**0 / 16** of the known multipliers (o17 has no scalar p/q). The reason is structural, not a fit bug:

| machine | true | `rho_time` | `rho_slow` | verdict |
|---|---|---|---|---|
| Antihydra | 3/2 | **1.0002** | 6.885 | miss |
| o4 | 4/3 | **1.0004** | 1.101 | miss |
| o15 | 8/3 | **0.9999** | **6.883** | miss |
| o18 | 8/3 | **1.0003** | 7.080 | miss |
| SpaceNeedle | 5/2 | **0.9983** | 13.74 | miss |
| o2,o3,o5,o7,o8,o10–o14,o16 | 3/2 or 4/3 | **≈1.000** | 1.1–2.0 | miss |

Two independent disqualifiers, both reproduced in the gate output:

1. **`rho_time ≈ 1.000` for every named machine.** All 16 are digit-string counters (o4's own
   structure): value ×(p/q) per period adds `log_base(p/q)` = ~1 base-digit, so **tape width grows
   ~1 cell per period and per-period work ∝ width ∝ k — step-gaps are LINEAR, not geometric**, and
   their ratio → 1. The multiplier is simply not in the timing for digit-string machines (the
   geometric step-gap signal exists only for *unary*-width counters).
2. **`rho_slow` is NON-IDENTIFYING.** It is a genuine width-independent geometric invariant but
   equals `(p/q)^m` for an unknown, machine-specific, non-integer multiplicity m. The decisive
   counterexample: **Antihydra (true 3/2) and o15 (true 8/3) both yield R ≈ 6.88** — the same
   number for two different engines. No choice of m recovers 3/2 for Antihydra; the tool cannot
   tell the two engines apart. `rho_val` degenerates to a constant 2⁸ (a window-decode width
   artifact), confirming the plain-binary value decode is uninformative (value ~ base^width, base unknown).

**Per the STRICT discipline, the tool is therefore NOT trusted and is NOT used to assign engines
to the 1104.** The gate did its job: it caught an unsound tool before it could manufacture labels.

## 3. The 1104 signal census (OBSERVE-ONLY, no assignments)

`me_census.py` ran the (gate-failed) extractor over all 1104 (cap 1.5·10⁶, fork Pool 8), purely
to characterize the signal at scale:

- **`rho_time ≈ 1` (flat, digit-string signature): 893 / 1104.** As predicted — the polynomial-width
  majority carries no time-multiplier.
- **`rho_time ≥ 1.1`: 210**, but these cluster at 1.10–1.14 (mild fit curvature) with a thin tail
  to 2.36; **0 land near ×5/2 or ×8/3**, and the 27 near ×4/3 / 7 near ×3/2 are **spurious**: the
  gate showed the tool assigns `rho_time ≈ 1.000` to the *known* ×4/3 machines, so any 1104 machine
  it tags ×4/3 is by construction untrustworthy.
- **Slow-side geometric signal (R>1.05): 667**, with a proxy tag histogram {×4/3:141, ×3/2:97,
  ×8/3:6, ×5/2:2} — recorded for completeness but **unreliable** (the Antihydra≡o15 collision proves
  these tags do not identify the engine).

## 4. The collapse count and how much [C] shrinks

- **Cleanly reduce to a KNOWN engine (certified by this tool): 0 of 1104.**
- **Candidate-new species (new certified multipliers): 0.**
- **No clean/trustworthy signal: all 1104** (893 flat + 211 with only the non-identifying `rho_slow`
  or spurious `rho_time`).

**[C] does not shrink via coarse extraction.** This build now *operationalizes* — with a tool that
was run, and honestly failed its own gate against the 17 named — the structural obstruction that
`HOLDOUT_CLASSIFICATION_2026-07-10 §2` reached: the ×(p/q) multiplier of a digit-string counter is
invisible to any width/timing/coarse-decode probe; reading it needs the per-machine milestone-form
proof each of the 17 named received by hand (auto-detecting the base and the macro-period — the
Coq-BB5-scale sophistication). The 1087 un-catalogued holdouts remain community-scale.

## 5. Honest verdict

The extractor is a correct, careful implementation of the specified width-independent method and of
two cross-checks; it **fails its mandatory validation gate for a genuine mathematical reason**, and
that failure is itself the load-bearing result — a certified-negative that sharpens the [C] boundary
rather than crossing it. An extracted multiplier here is not even reliable *evidence* (it is
non-identifying), let alone a certified reduction. No engine was assigned; no holdout collapsed.

**No machine decided. No label upgraded.**
