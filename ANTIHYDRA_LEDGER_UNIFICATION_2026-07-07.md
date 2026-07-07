# Antihydra recast in the o4-ledger framework — exact verified constants, THE CRITICALITY CRITERION (run-cap slope / budget slope), and the family table that makes Antihydra provably the critical rung (2026-07-07)

*The LEDGER-UNIFICATION pass: Antihydra's kernel restated completely in the campaign's o4-ledger coordinates
(branch fixed points → exact v₂ run closed forms → cumulative ledger → drift/ruin constants → criticality ratio),
every identity verified against the real orbit (exhaustive c ≤ 2·10⁵ + orbit to n = 10⁶). Headline: the family
criterion **single-run fatality is a-priori excluded iff (run-cap slope)/(budget slope) < 1** evaluates to
**log₂(3/2)/(1/2) = log₂(9/4) = 1.1699 > 1** for Antihydra — and this is EXACTLY `PROOF_TOOL_ATTEMPT`'s
independently derived "1.17× ceiling improvement = (K)". o4 sits at 0.0873, o3 at 0.79 (and above 1 under the
unconditional cap — new), o18 at ∞ (reset budget). One numeric correction to the memory (worst running avg is
−2/23 at N=46, not −0.0407) and one bug self-caught (mean-D bookkeeping). Antihydra `[OPEN]`. No machine decided.*

## 1. The kernel in ledger coordinates `[PROVEN]` (`ah_ledger_kernel.py`)

**Gate (machine level).** Antihydra halts ⟺ the maintained counter underflows ⟺ `B_n < 0` for some `n`, where
`c₀ = 8`, `c_{n+1} = ⌊3c_n/2⌋`, `E_n = #{evens among c₀..c_{n−1}}`, **`B_n := 3E_n − n`**. This is the repo's
proven reduction (`BB6_FRAMEWORK_PACKAGE.md` §2, Link 0, `[PROVEN, machine-verified]`); equivalently non-halt ⟺
`E_n/n ≥ 1/3 ∀n` ⟺ running average of `(−1)^{c_n}` ≥ −1/3 (all three forms checked pointwise here).
**Conventions:** `B₀ = 0` (seed), `B₁ = 2` (c₀ = 8 even); increments **`{even: +2, odd: −1}`** (verified
pointwise to n = 10⁶); first violation would be `B = −1`. Min over n ≥ 1: **B = 2 at n = 1**, never approached
again (matches the framework's "min balance +2" to N₀ = 2·10⁵).

**Branch maps and fixed points (the family fixed-point theorem, (p,q) = (2,3) instance).** The two branches
`c ↦ (3c − r)/2`, `r = c mod 2`, have integer fixed points `x_r = r` (solve `2x = 3x − r`): **x_even = 0,
x_odd = 1**, each ≡ r (mod 2). On an r-branch step `c′ − x_r = (3/2)(c − x_r)` exactly (3 a 2-adic unit), so —
verbatim the `O4_RUN_STRUCTURE`/`PAPER_RUN_STRUCTURE` Theorem 2 argument —
> **even-run = v₂(c), odd-run = v₂(c − 1), exactly.**
Verified exhaustively c = 2..2·10⁵ (0 mismatches) and on all 100,068 completed runs of the real orbit to
n = 2·10⁵ (0 mismatches). (The known Antihydra countdown, now literally the o4 theorem at (2,3).)

**Magnitude and the unconditional depth cap.** `7·(3/2)ⁿ ≤ c_n − 1` and `c_n ≤ 8·(3/2)ⁿ` (2-line induction;
checked exactly to n = 2000), hence **run ≤ v₂(c_n − 1) ≤ n·log₂(3/2) + 3 = 0.585n + 3** `[PROVEN]` — the
Corollary-2.1 analogue.

**Multi-run identity.** Runs alternate even/odd from `e₁ = v₂(8) = 3` (8→12→18→27). With `e_j`/`s_j` the
even/odd run lengths, the ledger at odd-run entry is **`B = 2·Σ_{j≤i} e_j − Σ_{j<i} s_j`** (verified on all
50,034 odd runs to 2·10⁵), and
> **halt ⟺ ∃i: s_i ≥ 2·Σ_{j≤i} e_j − Σ_{j<i} s_j + 1** — a pure statement about interleaved 2-adic depths.

**Constants.** Annealed drift = ½·(+2) + ½·(−1) = **+1/2** per step. Ruin base: `E[η^{−ΔB}] = 1` ⟺
`(η² + η⁻¹)/2 = 1` ⟺ `η³ − 2η + 1 = 0 = (η−1)(η²+η−1)` ⟺ **η = (√5−1)/2 = 1/φ ≈ 0.618034** — the
golden-ratio conjugate (exact factorization checked). Annealed ruin from balance B is `η^{B+1}`; from the
n = 10⁶ frontier `B = 498,503` this is ~10^(−104,000) (heuristic only, as always).

## 2. THE CRITICALITY CRITERION and the family table (`ah_ledger_criticality.py`)

A maximal drain run is fixed AT ENTRY: length `= v_p(entry value − x) ≤ log_p(c_{n₀}) + O(1) ≈ ρ·n₀`, with
**ρ = (orbit log-growth per generation)/log p** the *run-cap slope*; the ledger at entry is `≈ β·n₀`, with
**β** the *budget slope* (drift). So — since the run cannot lengthen mid-run, no end-of-run correction is
needed —
> **Criterion.** Single-run fatality is excluded at scale **iff ρ/β < 1**; then any fatality needs ≥ β/ρ
> separate deep p-adic returns interleaved with recoveries (the multi-run conspiracy). If ρ/β ≥ 1, even ONE
> run can exhaust the ledger within the a-priori magnitude ceiling — no counting argument can exclude it.
Status: ρ is `[PROVEN]` where the growth is (Antihydra exactly ×3/2±; o4 exactly ×4/3 given template); β is
`[OBSERVED = annealed]` for every machine (the drift is itself part of the open protection). The criterion is
the sharp form of "even granting the ledger its full observed drift, is one run enough?"

| machine | depth process | run-cap slope ρ | budget slope β (memory class) | **ρ/β** | verdict |
|---|---|---|---|---|---|
| **Antihydra** | v₂ under ×3/2 | log₂(3/2) = 0.58496 `[PROVEN]` | 1/2, cumulative `[OBS=annealed]` | **1.1699** | **> 1: NOT excluded — THE critical rung** |
| o4 | v₃ under ×4/3 | log₃(4/3) = 0.26186 `[PROVEN\|template]` | 3, cumulative `[OBS=annealed]` | **0.0873** | < 1: excluded (also unconditionally via banked a₄₀ = 124) |
| o3 | v₃ under ×4/3-mix | 0.19641 `[OBSERVED growth]` | 0.248, cumulative `[OBSERVED]` | **0.7911** | < 1 given orbit stats; **1.0547 under the unconditional cap** (new — see below) |
| o15 | v₃ under ×8/3 | log₃(8/3) = 0.89279 `[PROVEN\|grid]` | string-valued (queue) — no scalar slope | n/a | criterion inapplicable; single-run kill gated on v₃(V−1) ≥ 3 `[grid]` |
| o18 | v₃ under ×8/3 | log₃(8/3) = 0.89279 `[PROVEN\|grid]` | **RESET per generation** ⇒ β_cum = 0 | ∞ | formally supercritical: no accumulation — exactly why its annealed model halts |

- **The 1.17 identity.** Antihydra's ratio `log₂(3/2)/(1/2) = log₂(9/4) = 1.169925` **is**
  `PROOF_TOOL_ATTEMPT`'s independently derived minimal target: proven ceiling `0.585n` vs needed `< 0.5n`,
  "a 1.17× improvement = (K)". Same number, now seen as the family-uniform criticality ratio. Equivalently:
  Antihydra's budget grows at only **0.855×** its worst-case single-run cap; o4's grows at 11.5×.
- **o3 finding (new).** The exact (a,k) map re-run 200k generations reproduces `O3_TEMPLATE_PORT` §5 to the
  digit (freqs 0.5009/0.2500/0.2492, drift +0.24828, k = 49,658, min k at drain = 2, longest drain run = 10),
  PLUS a new verified closed form: **every maximal a≡0 (mod 3) drain run = v₃(a + 9) at entry** (fixed point
  −9 of `a ↦ 4a/3 + 3`; 0 mismatches). o3's ratio is 0.79 with the *observed* growth γ = 0.2158/gen
  (idealized ¾·ln(4/3) = 0.21576), but **1.05 under the unconditional magnitude cap** log₃(4/3)/0.248: o3's
  single-run exclusion genuinely needs the orbit's growth statistics — o3 is nearer criticality than any
  margin ordering so far recorded (o4 0.09 ≪ o3 0.79 < 1 < Antihydra 1.17).
- **Reconciliation with `PAPER_RUN_STRUCTURE.md` §4 (FLAGGED, not edited).** Its mirror table's Antihydra
  budget entry "constant (critical)" should become: **"cumulative, slope 1/2 (obs.); critical because
  run-cap/budget = log₂(3/2)/(1/2) = 1.17 > 1"**. Same precisification applies to `O4_RUN_STRUCTURE` §3
  ("constant budget" → both budgets grow linearly; the real distinction is ratio > 1 vs < 1) and to the
  campaign/species tables' "zero margin (critical)" (→ "criterion margin 1 − ρ/β = −0.17"; o4 +0.91, o3 +0.21).

## 3. What EXACTLY remains for Antihydra (the multi-run decomposition, o4-style)

With the run closed forms banked `[PROVEN]`, the orbit IS its interleaved depth sequence
`(e₁, s₁, e₂, s₂, …)` and halt ⟺ the §1 prefix inequality fails. Split as o4 does:
- **Depth axis: NOT banked — unique in the family.** For o4/o3 the fixed-point theorem + ratio < 1 kills
  single-run fatality; for Antihydra ratio 1.17 > 1 means a single return of depth `≥ B_n + 1 ≈ 0.5n` is
  *permitted* by the proven ceiling `0.585n + 3`. The single-run form of the open content is
  **`c_n ≢ 1 (mod 2^{B_n+1}) ∀n`** — single-orbit residue avoidance, and already this weakest fragment is (K)
  (`PROOF_TOOL_ATTEMPT`). Truth on the orbit: max depth to 10⁶ is **20** (at n = 67,940 — ~log₂ n = 16.1),
  vs needed 33,970, vs ceiling 39,745: the truth beats the needed bound by a factor ~1,700, and the gap
  between needed and proven is the bare 1.17.
- **Frequency axis (the aggregate form).** Non-halt ⟺ mean D ≥ 3/2 (Kac; D = v₂(3o−1) = 1 + following even
  run). Orbit: mean D = 1.99801 at 10⁶, needed 1.5, annealed 2.
- **Orbit margins (`ah_ledger_orbit.py`, n ≤ 10⁶).** 250,136 even runs (mean 1.9969) / 250,135 odd runs
  (mean 2.0009); the depth histogram matches the annealed `2^{−d}` law over five decades on BOTH sides
  (e.g. d = 10: 268 odd vs 244 expected; d ≥ 17: 3 vs 3.7); worst single-run drain fraction
  `s_i/B(entry)` = **0.2308 at n = 11** (startup) — fatality means exceeding 1; even-density 0.499501,
  `B(10⁶) = 498,503` (slope 0.4985); worst dips: running avg **−2/23 at N = 46** (global) and −5/123 at
  N = 123 (worst for N ≥ 100), margins 0.246 / 0.293 above −1/3.

**Family statement.** Antihydra's remaining problem = the deep-2-adic-return problem of the mirror ladder at
the 1.17-tight threshold, with BOTH axes open (depth and frequency), whereas every other rung has depth
banked and only frequency open. That, in one line, is why Antihydra is the hardest rung and o4 the easiest.

## 4. LEDGER-MEMORY: the axis completed for all six `[Task 4]`

Antihydra's balance is **CUMULATIVE — it never re-seeds**: increments are only {+2, −1} by definition of B
(verified pointwise to 10⁶); the prefix minimum is frozen at n = 1 forever after; suffix minima grow linearly
(min B over [10⁴, 10⁶] = 4,862; over [8.1·10⁵, 10⁶] = 403,536; zero halvings/reset events). Classification:

| machine | ledger object | memory class | source |
|---|---|---|---|
| Antihydra | scalar B = 3E−n | **CUMULATIVE** (slope 0.4985 obs.) | verified here |
| o4 | scalar a | **CUMULATIVE** (+3/gen) | `O4_TEMPLATE_CLOSURE` |
| o3 | scalar k | **CUMULATIVE** (+0.248/gen) | `O3_TEMPLATE_PORT`, re-verified here |
| o15 | digit queue | **CUMULATIVE-STRING** (queue persists; drains from the V-side) | `O15_FIXEDPOINT` §2 |
| o18 | word w | **RESET** (renewal: every dirty generation re-seeded at `((1,6),)`) `[EXACT given T]` | `O18_ANNEALED_STANDOFF` §0 |
| o17 | none | **NO LEDGER** — tower-sparse gate timing | `O17_GATE_LAW` |

The axis is decision-relevant: RESET ⇒ margins cannot accumulate ⇒ the annealed model halts regardless of
drift (o18's standoff); CUMULATIVE + ratio < 1 ⇒ single-run dead and annealed ruin η^B → 0 (o4, o3);
CUMULATIVE + ratio > 1 = Antihydra alone, exactly at the critical point of the family.

## 5. Corrections and soundness ledger `[discipline]`

- **CORRECTION (memory numeric):** `bb6-frontier-state`'s "worst running avg −0.0407 at n=122" is the
  *post-startup* dip (worst over N ≥ 100: −5/123 at N = 123). The TRUE global worst is **−2/23 = −0.086957 at
  N = 46** (margin 0.246 above −1/3, not 0.293). Even-density 0.50018 confirmed exactly at N = 2·10⁵
  (0.499501 at 10⁶). Max v₂(c_n−1) = 20 at N = 2·10⁵ confirmed (`PROOF_TOOL_ATTEMPT`); it is not exceeded
  up to 10⁶.
- **Self-caught bug:** first version of the orbit census printed "mean D = 2.997" (divided even steps by odd
  *runs*, not odd *values*); corrected to Kac's `mean D = N/O_N = 1.99801` and re-run.
- Everything labeled: run laws / fixed points / magnitude cap / multi-run identity / η factorization
  `[PROVEN]` (elementary + machine-checked); halt-gate reduction cited `[PROVEN, machine-verified]`
  (`BB6_FRAMEWORK_PACKAGE` §2); budget slopes and o3 growth `[OBSERVED = annealed]`; ruin numbers heuristic
  only. The criticality criterion itself is a theorem GIVEN the labeled slopes; for Antihydra its verdict is
  the *absence* of a protection, so nothing here strengthens any non-halting claim.
- Flagged paper edits (§2) NOT made. Nothing committed. Antihydra `[OPEN]`.
  **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`ah_ledger_kernel.py` (fixed points, exhaustive + orbit run laws, ledger/halt-form identities, magnitude
bounds, η, multi-run identity, margins to 2·10⁵) · `ah_ledger_criticality.py` (the table; o3 (a,k) map 200k
generations + new v₃(a+9) drain law) · `ah_ledger_orbit.py` (n ≤ 10⁶ census: histograms vs 2^{−d}, suffix
minima, mean D, drain fractions; ~2 min). Basis: `PAPER_RUN_STRUCTURE.md`, `O4_RUN_STRUCTURE_2026-07-07.md`,
`O4_LEDGER_ANALYSIS_2026-07-06.md`, `O3_TEMPLATE_PORT_2026-07-06.md`, `O15_FIXEDPOINT_2026-07-07.md`,
`O18_ANNEALED_STANDOFF_2026-07-07.md`, `BB6_FRAMEWORK_PACKAGE.md` §1–2, `PROOF_TOOL_ATTEMPT_2026-07-04.md`.
