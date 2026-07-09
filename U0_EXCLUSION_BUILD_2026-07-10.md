# Excluding the fatal reload-adversary u₀ — the solenoid diagonal EXCLUDES the ℚ_q-only construction, but only via the run-cap, and a run-cap-legal fatal adversary survives (2026-07-10)

*Genuine BUILD at the single un-blocked target of `NEWMATH_BUILD_SYNTHESIS`: an a-priori mechanism that excludes the
explicit fatal adversary u₀ of `RELOAD_EXCURSION_BUILD` (a free ℤ_q^× element realizing `E[K²]=∞`). The reframe (from
the brief): yesterday's u₀ was built in ℚ_q ALONE; the REAL reload unit `w_i=(v_i−x)/q^{d_i}` is the q-adic tail of a
specific integer `v_i` of prescribed ARCHIMEDEAN magnitude `≈α(p/q)^{n_i}`, living on the (2,3)-solenoid
`ℝ×ℚ₂×ℚ₃` via the ℤ[1/6] diagonal. Does the diagonal forbid the pure-ℚ_q fatal alignment? STRICT soundness:
`[PROVEN]`/`[CONSTRUCTED-partial]`/`[OBSERVED]`/`[OPEN]`. Numerics exact big-int,
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/u0_exclusion_build.py`. NOT committed.*

---

## 0. One-paragraph verdict

The solenoid diagonal supplies exactly one archimedean constraint on the reload units beyond the first moment: the
**run-cap** `K_i ≤ log_q|v_{n_i}| = log_q(α) + n_i·log_q(p/q)`, `[PROVEN]` (elementary: `q^K∣m≠0 ⟹ K≤log_q|m|`), a
per-excursion **support** bound. This constraint is **real and it BITES the naive adversary**: the explicit fatal u₀
of `RELOAD_EXCURSION_BUILD` — solved as a free ℤ₂^× element window-by-window, ignoring the archimedean place —
**violates the run-cap** (its heavy-tail construction places a depth-**42** excursion at reload `i=21`, where the
accumulated archimedean budget permits only **31.66** bits: excess **+10.34 bits**). So **that u₀ is an archimedean
phantom — NOT the reload sequence of any real integer orbit** `[CONSTRUCTED, verified]`. This is a genuine exclusion,
and it downgrades `RELOAD_EXCURSION_BUILD`'s "explicit map-faithful fatal u₀" to "ℚ_q-faithful but solenoid-infeasible."
**But it does not exclude the fatal CLASS.** I construct a **run-cap-respecting, map-faithful, heavy-tail adversary**
(deep excursions scheduled only when the growing archimedean budget permits them): 0/4000 run-cap violations, every
reload congruence solvable, and `E[K²]` still **diverges** (running excursion-average `E[K²] ≈ 2.2·M → ∞`). So the
diagonal constrains u₀ to the run-cap-legal cone but the fatal class is non-empty inside it. **The residual is
precisely the run-cap's proven orthogonality to the first-moment fatal frequency (`O4_NEWMATH_BUILD` §2), now shown to
be the EXACT residual of the entire solenoid-diagonal coupling.** No machine decided. No label upgraded.

---

## 1. The diagonal's content, decomposed `[PROVEN + OBSERVED]`

The orbit is `ℤ[1/6]`-integral, embedded diagonally in `X=ℝ×ℚ₂×ℚ₃` under `A=×(p/q)`. Its archimedean coordinate
`|v_n|_∞` is read TWO ways by the reload partition `n_i = Σ_{j<i}K_j` (the step index at reload `i` = accumulated
drained depth, an **exact identity** — verified 0 mismatch / 100 067 reloads):

- **(i) Summed / telescoped = the product formula = INTRATERM tautology `[OBSERVED, exact]`.**
  `log₂|v_{n_i}|_∞ = Σ_{j<i}K_j·log₂(p/q) + O(1)`. Verified on seed 8: `log₂(v_{n_i})` vs `3+0.585·n_i` agrees to
  **≤0.03 bits** at `i=100,10³,10⁴,5·10⁴`. This is `INTRATERM_ADELIC_MINING` §3 verbatim — a **codimension-1**
  (one scalar/step) constraint pinning `ΣK_i ↔ log v_n`, the **first moment** only.

- **(ii) Per-excursion inequality = the RUN-CAP `[PROVEN]`.**
  `K_i = v_q(v_{n_i}−x) ≤ log_q|v_{n_i}−x| = log_q(α)+n_i·log_q(p/q)`. Slopes: Antihydra `log₂(3/2)=0.585`,
  o4 `log₃(4/3)=0.262` (both reproduce the banked run-cap constants). This is a **support/sup** functional —
  genuinely NOT first-moment.

**Sharpening of the INTRATERM verdict.** `INTRATERM_ADELIC_MINING` concluded the adelic coupling is a *pure*
codim-1 tautology, but it only examined reading (i) (the summed product formula, one term at a time). The
excursion/reload structure exposes reading (ii) — the per-excursion run-cap — which the single-term analysis never
surfaced. **So the solenoid diagonal is NOT purely the INTRATERM tautology: it is `first-moment (product formula)
⊕ run-cap (support)`.** The honest question then becomes whether the extra tooth (the run-cap) excludes u₀.

---

## 2. COMP 1 — the run-cap EXCLUDES the naive ℚ_q-only u₀ `[CONSTRUCTED, verified]`

Rebuilding the two `RELOAD_EXCURSION_BUILD` fatal constructions and auditing them against the run-cap:

| naive u₀ (built in ℚ₂ alone) | map-faithful? | run-cap violations | worst excess |
|---|---|---|---|
| linear-growth depths `[1..19]` (`ΣK²∼M³`) | yes | **0 / 20** | — (grows slowly enough) |
| heavy-tail `P(K≥k)∼1/k`, `E[K²]=∞`, maxK=42 | yes | **2 / 41** | **+10.34 bits** (K=42 at i=21, cap 31.66) |

**The heavy-tail fatal u₀ is solenoid-INFEASIBLE.** A depth-42 excursion requires `2^42 ∣ (v−x)`, hence
`|v−x| ≥ 2^42`, hence `n_i·0.585 ≥ 42 ⟹ n_i ≥ 67` steps of accumulated magnitude — but the construction reaches it at
`n_i=49`. A free ℤ₂^× element has no archimedean size, so the congruence solver happily produces it; **no real integer
of magnitude `≈8·(3/2)^{49}` can be divisible by `2^42`.** The diagonal excludes it. (Note the *linear-growth*
construction survives — depths that grow no faster than `0.585·ΣK` are already budget-legal; the exclusion bites only
the genuinely heavy, suddenly-deep tail.)

---

## 3. COMP 2 — a run-cap-legal fatal adversary SURVIVES `[CONSTRUCTED-partial]`

Construct a heavy-tail depth sequence that respects the archimedean budget at every step: typical depths `∼Geom(½)`,
truncated to `⌊cap_i⌋`; at sparse indices `i=2^m` **saturate** `K_i=⌊cap_i⌋` (a deep excursion placed exactly when
the growing budget first permits it). Verified:

- **map-faithful:** the reload congruences `3^{K_i}w_i≡−s_i (mod 2^{K_{i+1}})` are solvable for the whole sequence
  (the ℚ₂ solver realizes it exactly) `[CONSTRUCTED]`;
- **run-cap-legal:** **0 / 4000** violations `[verified]`;
- **still fatal:** running excursion-average `E[K²] = 519 (M=250), 2198 (M=10³), 9790 (M=4·10³)` — i.e.
  `E[K²] ≈ 2.2·M → ∞`, `E[K]` also drifting up (4.29→4.67). Sparse cap-saturating excursions (each
  `≈0.585·ΣK ∼ i`) keep `ΣK` linear yet make `ΣK²` grow like `M²` `[CONSTRUCTED-partial]`.

This is the reload-map instance of `O4_NEWMATH_BUILD`'s cap-saturating adversary B ("deep-tiling at cap equality,
still fatal"): **run-cap legality is necessary but NOT sufficient to exclude `E[K²]=∞`.** Honest scope: run-cap
legality + ℚ₂-solvability place the adversary on the solenoid's feasible cone; whether **seed-8's own orbit**
realizes such a run-cap-legal fatal pattern is exactly (K) — the diagonal removes the archimedean obstruction that
killed the naive u₀ but supplies no further exclusion.

---

## 4. COMP 3 — why the diagonal stops here (the precise residual) `[PROVEN reduction]`

The real orbit obeys the run-cap at **all 100 067** reloads (0 violations — the necessary condition) and `E[K²]=5.97`
finite — but *that finiteness is the conclusion, not forced by any archimedean identity*. The diagonal reads the
archimedean place as **`log|v_n| = ΣK_i·log(p/q)` (first moment) and `K_i ≤ log|v_{n_i}|` (support)** — the SUM of
depths and the SUP of depths. The fatal statistic is `Σ K_i²` (`E[K²]` / the level-1 cylinder frequency), which is
**neither a sum nor a sup of the archimedean read-out**: the second moment is not a function of the transported
archimedean coordinate. Formally:

> **`[PROVEN, dimension count]`** The solenoid diagonal contributes `{ codim-1 product formula (first moment) } ∪
> { run-cap (per-excursion support) }`. The product formula is orthogonal to the tail by INTRATERM (codim-1 vs
> codim-∞); the run-cap is orthogonal to the fatal **frequency** by `O4_NEWMATH_BUILD` §2 (support vs first-moment
> count; the o4 fatal mode is shallow, depth-5, the cap vacuous). Neither reaches `Σ K_i²`. **The diagonal excludes
> exactly the archimedean-illegal adversaries (naive u₀) and nothing more.**

So the answer to the brief's decisive question — *does the solenoid diagonal add a real constraint beyond first
moment, or collapse to the INTRATERM tautology?* — is **it adds ONE real constraint (the run-cap, a support bound,
strictly beyond first-moment in kind), and that constraint is precisely the already-proven weapon orthogonal to the
fatal frequency.** It does not collapse to the pure tautology (INTRATERM missed the run-cap by looking one term at a
time), but the extra content is exactly the known-insufficient one.

---

## 5. What was built / the residual

| item | result | label |
|---|---|---|
| Diagonal decomposition | solenoid archimedean coupling = product formula (first moment) ⊕ run-cap (support); sharpens INTRATERM's "pure tautology" | `[PROVEN + OBSERVED]` |
| **u₀ real-orbit-realizable?** | the naive ℚ₂-only heavy-tail u₀ **VIOLATES the run-cap** (K=42 at i=21, +10.34 bits) — an archimedean phantom, not any real orbit | `[CONSTRUCTED, verified]` |
| Does the diagonal exclude it? | **YES** — the run-cap excludes the ℚ_q-only construction; genuine, previously unstated | `[CONSTRUCTED, verified]` |
| Does it exclude the CLASS? | **NO** — a run-cap-legal, map-faithful, heavy-tail adversary survives with `E[K²]≈2.2M→∞` (0/4000 cap violations) | `[CONSTRUCTED-partial]` |
| (p,q)-uniformity | identical mechanism at o4: run-cap slope `log₃(4/3)=0.262`, depth-20 needs `n≥62` budget; a free ℚ₃ u₀ ignores it | `[PROVEN, uniform]` |
| **Residual** | run-cap-legal ⟹ solenoid-feasible cone; realization by seed-8 = (K). The diagonal's teeth = {first moment} ⊕ {support}, both proven orthogonal to `ΣK²` | `[OPEN = (K)]` |

**Precise residual (sharpest form).** The solenoid diagonal is a genuine a-priori mechanism and it **does** exclude
the fatal adversary as constructed yesterday (that u₀ ignored the archimedean place and is infeasible). But the
exclusion it delivers is exactly the run-cap, whose orthogonality to the first-moment fatal frequency is already
proven. A single refinement — schedule the deep excursions to respect the growing budget — restores a fully
solenoid-legal, map-faithful `E[K²]=∞` adversary. So **the diagonal moves the wall from "ℚ_q-realizable" to
"run-cap-legal-and-ℚ_q-realizable," and the fatal class is non-empty on the new side.** Whether seed-8's orbit sits
among the run-cap-legal fatal patterns is (K) = single-orbit base-p/q normality = AEV Conj 1.6, unchanged in species.

Reproduce: `scratchpad/u0_exclusion_build.py` (COMP 1 naive-u₀ run-cap audit; COMP 2 solenoid-legal heavy adversary,
0/4000 violations + divergent `E[K²]`; COMP 3 product-formula identity 0-mismatch/10⁵ + real-orbit run-cap 0
violations). Basis: `RELOAD_EXCURSION_BUILD_2026-07-09`, `RELOAD_MAP_UNIFIED_2026-07-09`,
`INTRATERM_ADELIC_MINING` (the first-moment tautology this refines), `O4_NEWMATH_BUILD_2026-07-09` (run-cap
orthogonality), `NEWMATH_BUILD_SYNTHESIS_2026-07-09`. Kernel anchor AEV arXiv:2510.11723.

No machine decided. No label upgraded.
