# Proper milestone-form multiplier extractor — macro-period detection, value-map fit, and the 1104 collapse census

*The [C]-frontier engineering of 2026-07-10, second generation. The COARSE extractor
(`MULTIPLIER_EXTRACTOR_2026-07-10.md`) FAILED its gate: `rho_time` is linear for digit-string
counters and `rho_slow = (p/q)^m` is non-identifying without the macro-period `m` (the Antihydra≡o15
`R≈6.88` collision). This PROPER version supplies `m` by detecting the config-shape recurrence and
reading the value map directly. VALIDATION-FIRST: it recovers **13/16** of the KNOWN named multipliers
with **0 WRONG**, so it is TRUSTED for the recovered classes and run observe-only on the 1104. Scripts:
`mse_extract.py` (extractor + gate), `mse_census.py` (1104 run). Interpreter:
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact `Fraction`. Every number is
`[OBSERVED, extractor]`, NOT a certified engine assignment; it decides NO halting.*

## 1. The method — two identifying, width-independent estimators

At every deduped record-extreme milestone the tape is run-length-encoded (memory-bounded: full RLE
kept only for the tail window). Two orthogonal readings of the abstract counter's multiplier `p/q`:

- **(T) Block-transfer rate.** During a macro-sweep a value-`×(p/q)` counter converts a *source* run
  into a *destination* run at the `p:q` rewrite rate. Over a window of milestones with a fixed run
  count, every run length is arithmetic; among the runs with a **consistent** nonzero per-milestone
  increment `Δ_r`, the ratio `(max +Δ)/(max −Δ)` is `p/q` **exactly** (a `Fraction`). Static runs are
  ignored, so machines with many frozen blocks plus one active `±` pair are handled. This fires for the
  sweep/sea `×3/2` family (Antihydra, o7/o8/o10/o12/o13/o14).

- **(S) Sawtooth macro-period.** A base-`(p/q)` odometer **resets** each macro-period: a value
  observable (total 1s / max 1-run / width) is a sawtooth that peaks then resets. The macro-period is
  the inter-reset segment — this is the `m` the coarse tool lacked. The ratio of consecutive segment
  **peaks** is `p/q` (the value map `v_{k+1} ≈ (p/q)v_k`). Self-consistency cross-check: total steps
  `∝ value²`, so the segment start-step ratio `≈ (p/q)²`, i.e. **peak-ratio `≈ √(step-ratio)`**. This
  fires for the base-`(p/q)` odometers: o4/o5 `×4/3`, o15/o18 `×8/3`, Space Needle `×5/2`.

Each `ρ` is matched to the nearest KNOWN engine `{3/2,4/3,8/3,5/2}` within `0.05`, else to the nearest
simple rational (candidate-new). A candidate-new label is emitted **only** if self-consistent; a
KNOWN-engine match from exact-transfer or a self-consistent sawtooth is high/med confidence.

## 2. The VALIDATION GATE (17 named) — **PASSED 13/16, 0 WRONG** (stable at caps 8M and 15M)

| machine | true | transfer | saw-peak (obs) | REPORTED | verdict |
|---|---|---|---|---|---|
| Antihydra | 3/2 | **3/2** | – | **×3/2** | PASS |
| o7 | 3/2 | **3/2** | 1.91 | **×3/2** | PASS |
| o8 | 3/2 | **3/2** | – | **×3/2** | PASS |
| o10 | 3/2 | – | 1.463 (total1) | **×3/2** | PASS |
| o12 | 3/2 | **3/2** | 37 (junk) | **×3/2** | PASS |
| o13 | 3/2 | **3/2** | 6.9 (junk) | **×3/2** | PASS |
| o14 | 3/2 | **3/2** | 1.75 (junk) | **×3/2** | PASS |
| o16 | 3/2 | – | 1.513 (maxrun) | **×3/2** | PASS |
| o4 | 4/3 | – | 1.311 (total1) | **×4/3** | PASS |
| o5 | 4/3 | – | 1.341 (total1) | **×4/3** | PASS |
| o15 | 8/3 | – | 2.669 (total1) | **×8/3** | PASS |
| o18 | 8/3 | – | 2.677 (total1) | **×8/3** | PASS |
| Space Needle | 5/2 | 2 (spur.) | **2.500** (maxrun) | **×5/2** | PASS |
| o2 | 3/2 (ceiling) | – | 1.0 (flat) | – | miss |
| o3 | 4/3 | – | – | – | miss |
| o11 | 3/2 | – | 8.7 (junk) | – | miss |
| o17 | none | – | – | – | n/a (no scalar p/q) |

**0 WRONG** is the load-bearing trust property: a noisy secondary estimator never produces a false
label because the exact-transfer match wins and cand-new is self-consistency-gated (o14's junk 1.75 is
overridden by transfer 3/2). The **three misses are structural, not fixable by cap**: o2 (ceiling) and
o3 (role-swapped odometer) have *linear* observables — the register value is not in total1/maxrun/width;
o11's refills are doubly-exponentially sparse, so <2 macro-periods occur within any feasible cap. These
are exactly the base-odometer cases `HOLDOUT_CLASSIFICATION §2` flagged as needing the hand analysis.

## 3. The 1104 census (observe-only, cap 4·10⁶, fork Pool 8; all 1104 → MAX, 0 halts, 0 errors)

- **DETECTION RATE (clean milestone-form read): 229 / 1104 = 20.7%.**
- **Matched a KNOWN engine: 120** — census `{×3/2: 59, ×4/3: 49, ×8/3: 7, ×5/2: 5}`.
  Stratified by trust: **74 robust** (exact-transfer or self-consistent sawtooth: `{×3/2:39, ×4/3:30,
  ×8/3:5}`) + **46 weaker** (single non-self-consistent sawtooth; includes all 5 `×5/2`, the
  Space-Needle-type where the odd branch breaks self-consistency).
- **Candidate-new multiplier: 109** — but **49 sit at ratio < 1.3** (`6/5,9/8,8/7,7/6…`), almost
  certainly fit-curvature near 1, NOT genuine engines (the coarse tool's `1.10–1.14` cluster); **60 are
  distinct (≥1.3)**, notably **~21 at ratio ≈ 2** (possible genuine binary-doubling class).
- **Undetected: 875** = 275 too-slow (<100 milestones at 4M) + 600 milestone-rich-but-unreadable (the
  o2/o3/o11-type base-odometers with linear observables or sparse refills).

## 4. Collapse count and how much [C] shrinks

- **Robustly collapse to a KNOWN engine (trusted level of the gate): 74** (≤120 counting weaker matches).
- **Candidate-new species with a plausible distinct multiplier: 60** (incl. ~21 near ×2) — worth
  hand-follow-up; 49 near-1 candidates discounted as curvature.
- **Undetected / needs hand-analysis: 875.**

**Honest verdict.** This is a **real partial success** and a strict improvement over the coarse tool's
`0/1104`: a validated automated extractor (13/16 named, 0 false labels) that cleanly reads the
milestone-form of ~21% of the 1104 and collapses **74 robustly** (up to 120) onto the known `{3/2,4/3,
8/3,5/2}` engines — an OBSERVED shrinkage of the [C] frontier by that subset. But **the caveat is
load-bearing**: an extracted multiplier is strong evidence, **not** a certified reduction — each
detected machine's milestone-form still needs a per-machine proof (base + macro-period + value-map),
exactly the sophistication the 17 named received by hand. The 875 undetected (base-odometers with linear
observables, or doubly-exponentially sparse refills) remain community-scale, matching the o2/o3/o11 gate
misses. No engine assignment is certified; the label on every machine stays `[OBSERVED-extractor]`.

**No machine decided. No label upgraded.**
