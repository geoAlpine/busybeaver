# Type-IV decidability — off the (K) axis, but on the generalized-Collatz wall (not independently decidable) (2026-07-04)

*Attack B: since Type-IV (H5-class fixed-arity counter bouncers) is the one cryptid class **off** the single-orbit
equidistribution axis (`P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md` §9.2, brick 6), does being off-axis make it
**independently decidable**? Answer: **no** — it is off the `(K)` axis but squarely on the **B2 generalized-Collatz
wall** (a bounded-vector floor-multiplier counter machine), empirically Collatz-irregular. SOUNDNESS:
`[OBSERVED]`/`[ARGUED]`; H5 undecided, halting `[OPEN]`; no machine decided.* Script: `scratchpad/typeIV_decide.py`.

## 0. Headline
- **"Off-axis" ≠ "decidable."** Type-IV is off the single-orbit-equidistribution `(K)` axis (its outer state is a
  **multi-coordinate counter vector**, not a scalar reseed — brick 6), but its inner map is a **floor-multiplier**
  `A ↦ ⌈2A/3⌉` — a generalized-Collatz operation — so it sits on the **generalized-Collatz (B2)** wall with Types
  II/III, not in a decidable class.
- **H5 is empirically Collatz-irregular** `[OBSERVED]`: over 60 M steps the leading-counter **record-peaks grow
  irregularly** (ratios `1.02…2.0`, mean `1.13`, stdev `0.19` — no clean geometric law) and the peak sequence is
  **not eventually periodic** (no exact tail period in the last 200 peaks); the block-count fluctuates over
  `{2,…,12}` with an irregular tail. This is genuine generalized-Collatz behaviour, not a decidable bouncer.

## 1. Why the floor-multiplier escapes decidable counter classes `[ARGUED]`
A fixed-arity machine over unbounded counters with only **additions/subtractions/resets** is a **vector addition
system (VASS / Petri net)**, whose reachability is **decidable** (Ackermann-complete). H5's inner update is not of
that form: `A ↦ ⌈2A/3⌉` **multiplies by `2/3` and floors** — a genuine `⌊(p/q)·⌋` Collatz-type operation. Counter
machines with such floor-multiplier updates are exactly the setting where reachability leaves the decidable VASS
world and becomes **generalized-Collatz / Collatz-class** (no bounded predictor; Minsky-general in the limit). So
Type-IV's halt (an `11`-adjacency reachability event over the counter vector) is a **generalized-Collatz
reachability** question — the same B2 wall as o17/o3 (Type II) and Space Needle (Type III), **not** a decidable one.

## 2. H5 empirics — Collatz-irregular, not a bouncer `[OBSERVED, 60 M steps]`
- **Record-peak sequence** (running maxima of the leading counter across refills):
  `8,10,20,25,30,47,48,61,101,103,118,159,162,174,217,…,1354`. Consecutive ratios
  `1.25, 2.0, 1.25, 1.2, 1.57, 1.02, 1.27, 1.66, 1.02, …` — **mean `1.13`, stdev `0.19`**: irregular, no fixed
  growth constant.
- **Not eventually periodic:** the leading-peak sequence has **no exact period** in the last-200 window
  (`tail-period = None`); the `⌈2A/3⌉` descent + refill never settles into a repeating shape.
- **Block-count** ranges over `{2,3,…,12}` with histogram peaked at `4,5,3,6` and an irregular tail — a *bounded
  but fluctuating* arity (fixed-arity in the "large counters" sense, transient sweep-blocks not counted), consistent
  with a genuine counter machine rather than a period-`p` bouncer (which the sound deciders would already have
  caught — H5 is a cryptid).

## 3. Placement and consequence
Type-IV therefore **completes the wall dichotomy without adding a decidable third category**: the phenotype
tetrachotomy `{I, II, III, IV}` still projects onto exactly two walls `{I}→(K)/Mahler`, `{II, III, IV}→
generalized-Collatz`, and **within** the generalized-Collatz side, Type-IV is the **bounded-vector floor-multiplier
counter-machine** sub-case (Types II/III are the growing-digit-cascade and scalar sub-cases). Being off the `(K)`
single-orbit axis buys it nothing decidability-wise — it is Collatz-class, no bounded predictor, **not proven
undecidable** (like Collatz itself) and **not decidable by any available method**.

## 4. Honest verdict
**(c) — rederives the wall (generalized-Collatz), with a structural placement.** Type-IV is off the `(K)` axis but
on the B2 wall; the floor-multiplier `⌈2A/3⌉` is the Collatz-type operation that keeps it out of decidable VASS,
and H5 is empirically Collatz-irregular (irregular record-peaks, no eventual periodicity). So "the only off-axis
class" is **not** independently decidable — it is the counter-machine face of the same generalized-Collatz wall.
**Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad/typeIV_decide.py` — H5 leading-peak + record-peak + block-count trajectories over 40–60 M steps
  (irregular ratios, no tail period). H5 TM `1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA`. Interpreter
  `/opt/homebrew/bin/python3.13`. Basis: `BB6_TYPE_IV_CENSUS_2026-07-04.md` (Type-IV phenotype),
  `P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md` §9.2 (off-axis).
