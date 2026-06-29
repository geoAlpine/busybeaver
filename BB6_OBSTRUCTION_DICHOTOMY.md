# The Antihydra obstruction dichotomy — why every route hits the same wall (2026-06-30)

*A meta-theorem organizing the entire BB(6)/Antihydra obstruction landscape: across ~20 independent attack routes the
proven/open boundary is always the SAME boundary. This note states it precisely, isolates the [PROVEN] core that forces it,
and classifies every route as an instance. Red-teamed (`DICHOTOMY_REDTEAM.md`): the naive "constant on one measure set"
form was falsified and is corrected here. SOUNDNESS: the HARD direction is a [PROVEN] theorem; the comprehensive dichotomy
is a [PROVEN core] + an [OBSERVED organizing principle] with the registers honestly separated. NOT committed by default.*

---

## 0. One-line statement

> **Every functional of the Antihydra orbit that the program has unconditionally PROVEN is determined by the orbit's
> CLOSURE / topology / tail (a conservation law, a count, a support fact, an annealed/measure-constant average, a
> complexity floor); every functional that is (K)-HARD is one that SEPARATES Haar from the other feasible invariant
> measures on the orbit closure (a cell-frequency, an occupancy tail, a second-or-higher moment, the measure entropy, the
> density, host-invariance). The proven/open boundary IS the topological-closure-determined vs measure-(Haar)-selecting
> boundary** — the topological-entropy/measure-entropy split, promoted to the program's global organizing principle. The
> HARD direction is [PROVEN] (ergodic-optimization + specification); the FREE direction is the observed pattern of every
> proven partial.

---

## 1. The two measure sets (the red-team's decisive correction)

Let `Ω` = the orbit closure of the seed `8` under `A=×(3/2)` on the solenoid. Three sets of `A`-invariant measures:
- **`M_orb`** = weak-* limits of the seed-8 empirical measures. **(K) ⟺ `M_orb = {Haar}`** (single-orbit genericity).
- **`M_feas`** = invariant measures on `Ω` consistent with all PROVEN (topological + first-moment) constraints. `{Haar} ⊆
  M_orb ⊆ M_feas`.
- **`M_sys`** = the specification / ergodic-optimization set of the *system* (`×(3/2)` on `ℤ₂`), **full Hausdorff dimension,
  contains the halting fixed point `δ₁` and every interior Birkhoff value** [PROVEN: `MINPROP_COUPLING.md`,
  `COMPLETE_PROOF_CAPSTONE.md`]. `M_feas ⊊ M_sys` (the seed-8 orbit provably escapes `δ₁`, but `δ₁ ∈ M_sys`).

The naive dichotomy "FREE ⟺ constant on M" is **FALSE as a literal biconditional** [red-team]: e.g. `#even(n) ≥ 0.89 log n`
is PROVEN yet equals 0 at `δ₁ ∈ M_sys`, so it is *not* constant on `M_sys`. The resolution: **FREE facts are
orbit-closure/topology/tail-determined**, which is a *superset* of "measure-constant" — it includes a topological/tail
register (orbit-growth facts, "infinitely many …", subword-complexity floors, non-periodicity) that are **not measure
functionals at all** (they survive even when the empirical measure degenerates). The HARD side is the clean one.

---

## 2. The HARD direction — a [PROVEN] theorem (this is the rigorous core)

> **Theorem (no structure-only selection).** Let `Φ` be a bounded functional of the empirical measure that is **not constant
> on `M_feas`** and whose value at Haar is a (K)-target. Then no argument using only orbit-closure / topological /
> first-moment / annealed data can prove `Φ(seed-8) = Φ(Haar)`; establishing it is equivalent to collapsing `M_orb={Haar}`
> = single-orbit genericity = (K).

*Proof.* Closure/topological/first-moment/annealed data is, by definition, shared by every measure in `M_feas` (it is the
data defining `M_feas`); so any argument built from it is **constant on `M_feas`** and cannot distinguish Haar from the
other members. `Φ` is not constant on `M_feas`, so its Haar-value is not forced by that data. That `M_feas` genuinely
contains non-Haar measures is [PROVEN] twice over: **ergodic optimization** gives `β = max_μ ∫(θ−ϕ)dμ = +½ > 0` attained
off Haar (at the `δ₁`-class), and **specification** realizes every interior Birkhoff value of `1{D≥2}` on a full-dimension
set (`MINPROP_COBOUNDARY_LP.md`, `MINPROP_COUPLING.md`). Hence the only remaining route to `Φ(Haar)` is the orbit's own
arithmetic = (K). ∎

This is exactly the program's two impossibility meta-theorems, restated as the **engine of the whole dichotomy**: the HARD
side is HARD *for a proven reason*, not for lack of tools.

---

## 3. The FREE direction — the observed mechanism (two registers)

Every unconditionally proven result sits in one of two FREE registers, both orbit-closure/topology/first-moment-determined:

- **(R1) Measure-constant / first-moment / annealed.** Conservation laws and counts that hold for *all* of `M_feas`:
  the valuation budget `ΣD_i = n` (renewal first moment), `M_orb`-independent annealed averages (Rajchman `ν̂_{2/3}→0`,
  `dim ν_{2/3}=1`), mean gap `≈2`, FLP support-spread `Ω≥1/3`. **Mechanism — telescoping self-closure** (`EK2_SECOND_BUDGET`):
  a *degree-1* depth potential telescopes to a **count `≤N`** (free, external to the orbit's statistics); a *degree-≥2*
  potential telescopes to a **tautology** (its increment sums back to the same higher moment). So first moments are free,
  second+ moments are not — a concrete face of the dichotomy.
- **(R2) Topological / tail / growth.** Facts about `Ω` or the tail that are *not* measure functionals: `#even(n)≥0.89 log n`
  ("infinitely many even steps"), subword-complexity floor `p(ℓ)≥1.71ℓ`, non-periodicity (C3), top-`Θ(log N)`-digit
  equidistribution, orbit growth `0.585n`, max-depth `M(N)=O(log N)` (annealed). These survive measure-degeneration and are
  proven via growth/separation, never via cell-frequencies.

Neither register can reach a HARD functional, because both are constant on `M_feas` (R1) or blind to the empirical measure
(R2), while HARD functionals separate Haar within `M_feas`.

---

## 4. Every session route is an instance [the catalogue]

| Route | FREE side (proven) | HARD side (= (K)) | the boundary crossed |
|---|---|---|---|
| Reduction chain | halt ⟺ even-density<1/3 [PROVEN] | even-density value | identity vs frequency |
| Valuation budget | `ΣD_i=n` (1st moment) | density / `E[K²]` | 1st moment vs 2nd |
| Endogenous-UE | gap on EVEN block (`L_annχ_even`) | ODD block `L_annχ_odd≡0` | spectral vs frequency |
| Carry / 2nd diagonal | annealed marginal `=ν_{2/3}` (Rajchman) | quenched single-orbit | annealed vs quenched |
| AIU | `(K)⟹AIU` | `(×2)_*μ=μ` (host-inv) | constant vs Haar-selecting (neutral dir.) |
| ENT | topological entropy `=log2` | measure entropy `h_μ>0` | topological vs measure entropy |
| Non-atomicity | orbit avoids periodic (per-visit) | `μ` charges zero mass (occupancy) | avoidance vs occupancy |
| `E[K²]<∞` | `ΣK_i≤N` (count) | `ΣK_i²` (weighted tail) | 1st moment vs 2nd |
| separation | min-gap (birthday-scale) | density / occupancy | min-gap vs frequency |
| top-digit | top `Θ(log N)` digits (Weyl) | moving middle digit | leading vs diagonal |
| uniform AEV | a.e.-`α` (Koksma) | specified `α=8` | a.e. vs specified |
| computability | finite-state-random level | specific computable point | level vs point |

**All twelve are the single boundary of §1–§2:** closure/topology/1st-moment/annealed/a.e. (FREE) vs
cell-frequency/2nd-moment/measure-entropy/occupancy/specified-Haar (HARD).

---

## 5. Honest scope — what is theorem, what is principle, what is separate

- **[PROVEN] §2** (the HARD direction = no structure-only selection) is a genuine theorem, = the ergodic-optimization +
  specification meta-theorems. It is *why* the program never crosses.
- **[OBSERVED, organizing principle] §1, §3, §4** (that every proven result is FREE and every open target is HARD, and the
  registers as described) is a pattern verified across the whole corpus by the red-team, not a biconditional theorem — the
  FREE side is a superset (closure/tail register) that resists a single "constant on M" phrasing.
- **[SEPARATE register] not on the measure axis at all:** the conditional "if X then halt" theorems (morphisms between
  problems) and the certificate-complexity hierarchy (star-free⊊…⊊CS, descriptive invariants of the *language*). These are
  orthogonal to the measure dichotomy and are FREE in their own (descriptive/proof-theoretic) sense.
- **Red-team corrections banked:** `M_sys` is the correct HARD-side witness but the wrong FREE-side test; the FREE side has
  the extra topological/tail register; no hard-but-constant counterexample exists (HARD direction is proven-backed).

---

## 6. Why this is the durable contribution

The dichotomy explains, in one principle, *why* ~20 independent routes — analytic, dynamical, arithmetic, computability,
measure-rigidity — all stop at exactly the same place, and proves (via §2) that the stopping is structural, not a tooling
gap. For an external reader it converts "we tried many things and they all failed" into **"the proven and the open are
separated by a single, identified, proven-to-be-real boundary (topological-closure-determined vs Haar-selecting), and (K)
is precisely the one functional that crosses it."** This is the sharpest available statement of what makes Antihydra hard.

**No machine decided. No label upgraded.** (K) remains [OPEN] = Mahler 3/2 / AEV.
