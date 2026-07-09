# The open problem, stated exactly — the (K) wall as a construction drawing

*A single-page statement of precisely what remains open after the campaign, in the sharpest coordinates the campaign
produced, with the full attack surface and what each angle gives. This is the hand-off drawing for the next build
round (internal or external). No machine is decided; nothing here is a new claim beyond the cited results.*

## 1. The problem, in one line

**Decide the halting of any BB(6) Type-I cryptid ⟺ prove `(K)`:** for the specific seed orbit of an explicit affine
`×(p/q)` map, an effective one-sided lower bound on the frequency of a fixed base-`q` digit — equivalently, an
a-priori upper bound on the frequency of deep `q`-adic returns `v_q(v_n − x) ≥ ℓ`. This is base-`p/q` normality
(Andrieu–Eliahou–Vivion Conjecture 1.6, arXiv:2510.11723) / Mahler's 3/2 problem, restricted to one orbit and
allowed to be lossy. **The easiest instance is o4** (×4/3, subcritical, margin 2.4): halt ⟺ `freq{3∣W_n} ≥ 4/5`;
a bound `freq ≤ 4/5 − ε` for seed W₀=57 decides it.

## 2. What is PROVEN (the floor the next round starts from)

- **Uniform reduction** `[PROVEN, Lean: Mirror.lean]`: every machine = `q`-adic depth process of `×(p/q)`; run-depth
  `= v_q(v−x)`, `x` the integer branch fixed point.
- **Depth axis controlled** `[PROVEN]`: `run ≤ log_q|v−x| ≈ 0.262n` (o4); the single-catastrophic-run failure mode is
  impossible.
- **Exact reload map** `[PROVEN]`: `d_{i+1}=v_q(p^{d_i}w_i+Δ_i)`, `w_{i+1}=(p^{d_i}w_i+Δ_i)/q^{d_{i+1}} ∈ ℤ_q^×` — a
  skew-product on the `q`-adic units; the `×3/2` family is ONE engine `⌊3W/2⌋` on different seeds.
- **Criticality** `[PROVEN, Lean]`: single-run fatality excluded iff `p+1 ≤ q^{β+1}`; o4 subcritical (`5≤81`),
  Antihydra/o2 at the boundary (ratio 1.17).
- **Rigidity limits** `[PROVEN, PAPER_RIGIDITY_LIMITS]`: the three standard method-classes (EKL high-entropy,
  Invariance-Principle, op-norm renorm contraction) are inapplicable to the whole {2,3}-host, uniformly.
- **The adversary is explicit** `[CONSTRUCTED]`: a `u₀ ∈ ℤ_q^×` realizing any depth sequence (incl. `E[K²]=∞`), each
  step satisfying the reload map exactly — the fatal object to be excluded, in hand.

## 3. What is OPEN, and why every route reaches it

The single residual: **`ℤ_q^×`-equidistribution of the reload units `w_i` for the specific orbit** (⟺ a-priori
`E[K²]<∞` ⟺ base-`p/q` normality ⟺ (K)). Why each proven weapon leaves it free:
- run-cap bounds the depth SUPPORT (orthogonal to the first-moment frequency; Cauchy–Schwarz gap `√n`);
- the reload map's carry DECOUPLES consecutive depths (unit refresh) — it models the shape, not the frequency;
- the rigidity no-gos rule out the invariant-measure methods — the surviving channel is the quenched Oseledets
  exponent = (K);
- the digit/autonomy split puts the orbit provably on the OPEN side (non-descent; `W_n` not a linear recurrence).

## 4. The attack surface (what each remaining angle offers)

| angle | status | what it would need |
|---|---|---|
| **solenoid diagonal** (u₀ built in ℚ_q alone; the real orbit lives on ℝ×ℚ₂×ℚ₃; does ℤ[1/6]↪X forbid the pure-ℚ_q fatal alignment?) | **the live probe** — the one un-tried structural constraint | a diagonal/product-formula constraint on `w_i` beyond first moment (prior adelic coupling was a 1st-moment tautology — must beat that) |
| a-priori excursion estimate on the reload map | carry decouples the tail | a mechanism reading the seed's ℤ_q^× trajectory that the constructible u₀ cannot satisfy |
| effective single-orbit equidistribution (NEW_MATH_PROGRAM) | the generational target | rank-1 amenable specified-orbit genericity — no existing tool |
| external: AEV / Eliahou group | outreach ready, not sent | the o4-easiest instance handed over with the certified reduction + ladder |

## 5. The design spec for the missing tool (unchanged, sharpened)

An a-priori one-sided bound `freq{q∣W_n} ≤ 1 − ε` for the specific seed orbit that is: **non-spectral** (coisometry),
**non-structural** (No-Structure), **non-autonomous-recurrence** (SML empty), **neutral-blind-defeating** (AIU),
**not depth-only / not second-moment** (both weapons orthogonal to the 1st-moment fatal direction), reading the seed's
**ℤ_q^× reload trajectory** via the exact reload map, and **excluding the explicit u₀**. The one un-blocked internal
mechanism is a diagonal (solenoid product-formula) constraint on `w_i` — the live probe.

## 6. Decision for the next round

If the solenoid-diagonal probe yields a real (beyond-first-moment) constraint: deepen it — it is the only internal
crack. If it collapses to the adelic tautology: the internal build is saturated, and the frontier is (i) the two
publishable partials (rigidity-limits whole-host; AIU whole-host) → arXiv; (ii) external hand-off of the o4-easiest
instance to the AEV/Eliahou circle. Either way the wall is now a drawing, not a fog, and the next builder starts from
§5, not from scratch.

## Sources
`PAPER_MIRROR_LADDER`, `PAPER_RIGIDITY_LIMITS`, `PAPER_CENSUS`; `RELOAD_EXCURSION_BUILD_2026-07-09`,
`RELOAD_MAP_UNIFIED_2026-07-09`, `NEWMATH_BUILD_SYNTHESIS_2026-07-09`; `O4_NEWMATH_BUILD_2026-07-09`,
`O4_COBOUNDARY_LP_2026-07-08`; `NEW_MATH_PROGRAM.md`; kernel anchor AEV arXiv:2510.11723. Lean: `lean/Mirror.lean`.
