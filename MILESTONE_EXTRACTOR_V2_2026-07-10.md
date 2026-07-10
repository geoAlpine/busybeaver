# Milestone-form multiplier extractor V2 — the slow-side base-odometer power-fit recovers o2/o3, gate 15/16 with 0 WRONG

*Second-generation upgrade of `MILESTONE_EXTRACTOR_2026-07-10.md`. Adds one estimator — the
**slow-side base-odometer power-fit** (G) — that reads the base-(p/q) odometers whose value register
lives on the macro-generation (slow) side, not the intra-generation crawl. VALIDATION-FIRST: the gate
rises from **13/16 → 15/16 named multipliers with 0 WRONG** (recovers o2 and o3); o11 stays a miss
(confirmed structural). Census robust-collapse rises **74 → 105**. Every number is `[OBSERVED,
extractor]`, NOT a certified engine assignment; decides NO halting. Interpreter
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact `Fraction`. Scripts: `mse_extract.py`
(extractor + gate), `mse_census.py` (1104 run).*

## 1. Diagnosis of the three named misses (why the V1 tool could not read them)

All three are base-(p/q) odometers, but V1's two estimators (T) block-transfer and (S) fast-side
sawtooth both read the **fast** side (the side with more milestones). Instrumenting the milestone
streams (`diag.py`, `diag2.py`) showed the fast side of all three is a **linear crawl**: `total1 +1`,
`width +2` per milestone, `maxrun` flat — no geometric signal at all. The multiplier lives elsewhere:

- **o2** (ceiling ×3/2): the odometer value is sampled only at **slow-side record extremes**. Those
  extremes SKIP macro-generations irregularly, so the slow ratios come out as *powers* of 3/2
  (observed maxrun tail 155→551→1253→1883 gives 3.55, 2.27, 1.503 = (3/2)^{3,2,1}). V1 took a naive
  tail median → 1.0 (the state-pair duplicates), so it read nothing.
- **o3** (role-swapped odometer, `M(a,k)=(10)^a(110)^k`, `a` = odometer, `k` = ledger — per
  `O3_TEMPLATE_PORT`): `a` grows ×4/3 per macro-generation and shows up in slow-side `total1`/`width`
  (tail 1476→1965→2615 = ×1.33), but it never RESETS, so the fast-side sawtooth segmenter fired zero
  segments. The signal is on the slow side.
- **o11** (doubly-exp-sparse refills, per `O11_REFILL_LAW`): the sea `m` follows ×3/2 but its refills
  sit at t = 9, 46, 271, 28100, **6.4×10²⁸** — so any feasible cap lands inside the single 4th epoch.
  `nslow` stays **3 at caps 8M / 30M / 80M** (verified); the odometer is masked by the draining leading
  block and the affine `+4` keeps small-m ratios far from 3/2. **Adaptive cap cannot help** — it is the
  genuine doubly-exponential residual.

## 2. The new estimator (G) — slow-side power-fit (validation-gated)

For each slow-side observable (total1/maxrun/width): dedupe consecutive equal values (kills o2's
state-pair duplicates), take the tail, form value-ratios `r_i` and step-ratios `s_i`. Keep pairs that
are **self-consistent** (`s_i ≈ r_i²`, since steps ∝ value² at any skip depth). Then report a KNOWN
engine `e ∈ {3/2,4/3,8/3,5/2}` **only if every self-consistent slow ratio is a consistent integer
power `e^{n_i}` (n_i ≥ 1, within 6%)**. Requiring EVERY ratio to be a power of a *single* engine is
strongly identifying — powers of one engine never collide with another engine (e.g. (3/2)²=2.25 is
near no engine; a clean 2.0 does NOT misfit to 3/2). This is why it adds **zero** false labels.

## 3. THE GATE after improvement (the trust test) — 15/16, **0 WRONG**

`python mse_extract.py 8000000`: recovered **15/16** (was 13/16). **o2 → ×3/2** (slow-geom power-fit,
maxrun) and **o3 → ×4/3** (slow-geom, width) are now recovered; five machines rose to
`high(2-estimator agree)` (Antihydra, o4, o5, o15, o18 — sawtooth/transfer now corroborated by
slow-geom). **WRONG (false labels): none.** o11 remains the sole miss (structural, §1). The 0-WRONG
property is preserved because (G) only ever emits a known engine under the single-engine power-fit +
self-consistency gate, and the decision still prefers exact-transfer among known matches.

## 4. The 1104 census with V2 (observe-only, cap 4×10⁶)

- **DETECTION RATE: 253 / 1104 = 22.9%** (was 229 / 1104 = 20.7%; +24).
- **Matched a KNOWN engine: 151** (was 120) — `{×4/3: 73, ×3/2: 66, ×8/3: 7, ×5/2: 5}`.
- **ROBUST collapse (trusted gate level): 105** (was 74) — by source `{sawtooth: 54, slowgeom: 31,
  transfer: 20}`; the **entire +31 is the new slow-geom estimator** (all 31 are known-engine and
  robust: `{×4/3: 24, ×3/2: 7}`). Plus 46 weaker known (single non-self-consistent sawtooth, incl. all
  5 ×5/2).
- **Candidate-new: 102** — 57 at ratio ≥ 1.3 (incl. ~23 near ×2, a possible binary-doubling class), 45
  below 1.3 (discounted as fit-curvature near 1).
- **Undetected: 851** (was 875) — 272 too-slow (<100 milestones at 4M) + **579 milestone-rich-but-
  unreadable** (was 600; the o11-type doubly-exp-sparse refills and residual linear observables).

## 5. Honest verdict

V2 is a real, validation-gated improvement: one new estimator lifts the gate **13/16 → 15/16 with 0
WRONG**, and lifts the census robust collapse **74 → 105 (+42%)** by reading exactly the base-odometer
class (odometer on the slow side, linear fast crawl) that o2/o3 exemplify. The zero-false-label
property is intact — this is trusted extraction, not certified reduction: each detected machine's
milestone-form still needs a per-machine proof (base + macro-period + value-map). **The residual is
honest:** o11-type doubly-exponentially-sparse refills (only ONE macro-period reachable — no cap can
fix it), the 272 too-slow, and the remaining ~579 unreadable — the genuine community-scale remainder.
A validated 22.9% is worth more than an untrusted 60%; the label on every machine stays
`[OBSERVED-extractor]`.

**No machine decided. No label upgraded.**
