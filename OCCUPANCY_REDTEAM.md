# Red-team audit of OCCUPANCY_PROFILE_THEORY.md (2026-07-01)

**Auditor:** adversarial verification pass, independent re-run of all referenced numerics with exact
big-int / `Fraction` / `sympy` (`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`).

## OVERALL VERDICT: **[CONFIRMS facts, NEEDS-CAVEAT phrasing]**

Every `[PROVEN]` tag attaches to a genuinely-proven mathematical statement (exact algebra, a Haar/Kac model
theorem, or a reframing/equivalence), and **no claim crosses the annealed→quenched gap or claims progress toward
`(K)`.** Every quenched/orbit statement is labelled `[OBSERVED]`, every i.i.d.-model statement is labelled
annealed, and the scope disclaimers ("does NOT advance the frontier", "No machine decided", "quenched = `(K)`")
are accurate. All eight bricks' numerics reproduced **exactly**. The corrections below are **phrasing over-reaches
and two notational errors**, not false theorems — but several should be tightened to preserve the zero-false-proof
standard.

---

## What I reproduced (all CONFIRM)

- **Algebra, exact (`sympy`):** `x³−2x+1 = (x−1)(x²+x−1)`; root of `x²+x−1` = `(√5−1)/2 = 1/φ = 0.6180339887…`.
  General `x^m−2x+1 = (x−1)(x^{m−1}+…+x−1)` verified for `m=2..6` (quotients `x−1`, `x²+x−1`, `x³+x²+x−1`, …).
  Reciprocal `1/x` of the relevant root = the `(m−1)`-bonacci constant (`m=4→1.83929` tribonacci, `m=5→1.92756`
  tetranacci, `m=6→1.96595`). **CONFIRM (C1),(N1).**
- **MGF derivation:** `E[e^{−θX}] = e^{θ}/(2−e^{−2θ})` for `X=2D−3`, `D~geom(2^{−d})` — verified numerically to
  8 digits at multiple `θ`; at `θ=log φ` the MGF `= 1.00000000`. Increment `X=2D−3` derivation (`3(D−1)−D`) and
  `X=(m−1)D−m`, drift `m−2`, all correct. **CONFIRM.**
- **θ\* correctly labelled annealed:** `(C3),(C4),(N3),(Q4)` all say annealed / i.i.d.; the `[PROVEN]` on `(C1)`
  is the exact algebraic identity of the *annealed* Cramér exponent — legitimate. **CONFIRM (scrutiny pt 1).**
- **Balance walk (W):** drift `B_n/n → 0.49632` vs predicted `2−3/meanD = 0.49631`; increment var `2.2500`;
  running-min balance `= 17` **constant** across `N=10³,10⁴,10⁵,6·10⁵`; worst running even-density `0.45652`
  (margin `0.123` above `1/3`). `0.585 = log₂(3/2)` confirmed. **CONFIRM the numbers.**
- **Quenched LDP (Q):** drawdown ratios `0.6215,0.6161,0.6211,…` ≈ `1/φ=0.6180` (`s=1..11`); depth tail
  `0.49980,0.24937,0.12425,…` ≈ `2^{1−k}`; `max D=17`; `D≥8` events `n=1167`, mean gap `128.6` (exp `128`),
  **CV = 1.022**. All reproduced. **CONFIRM the numbers.** (Note: drawdown ratios for `s≥12` systematically dip
  to `0.55–0.60`, honestly flagged as "wobble on small counts".)
- **RG (R,F,L,U):** `R(p)_e=p_{e+1}/(1−p₁)`; every geometric `a(1−a)^{e−1}` is a fixed point (exact `Fraction`,
  `a=½,⅓,⅔,¼`); perturbed tail `r=0.4` flows to `a=0.6`, meanD `1.6667` exactly; linearized top eigenvalue
  `= 1/(1−a)` = `2.0, 3.0, 1.5` at `a=½,⅔,⅓`; first-return-to-`A₂` renormalized depth geometric shifted by `+1`
  (meanD `1.997→2.996`), `I(D';D'')=0.00069≈shuffle 0.00071`; family port `p=2` (`3/2,5/2`) and `p=3` (`8/3,4/3`)
  geometric `q=1/p`, meanD `p`, renorm `+1`. **CONFIRM (R1),(F1),(F2),(F3),(L1),(U1)–(U3).**
- **(L2) truncation artifacts honestly handled:** re-run shows the spurious "band ≈1.17–1.27" and 66/56 false
  "relevant" eigenvalues — the note **correctly flags these as truncation artifacts and does not use them**.
  Good discipline. **CONFIRM.**
- **(S1) even-count identity:** `#even=149808`, `Σ(D_j−1)=149805`, diff `3` (boundary), honestly labelled. `(P2)`
  collapse (non-closure + δ₁ feasibility) sound; its erratic truncated residue-graph correctly discarded as
  artifact. **CONFIRM.**
- **(U) dual label** `[PROVEN-in-family / OBSERVED]` is appropriate: the geometric-mean-`p` law is proven under
  Haar for the `v_p(μ)=−1` family (`CRYPTID_KERNEL.md`) and observed on the specific orbits. **CONFIRM
  (scrutiny pt 4).**

---

## Findings (corrections)

### 1. [NEEDS-CAVEAT] "i.i.d.-indistinguishable at second order" is too categorical
**Offending phrases** — §11 title, `(Q4)` heading, and Net (Q):
> "i.i.d.-indistinguishable at second order" ; "the deterministic orbit is **i.i.d.-indistinguishable**".

This rests on **three** statistics at a **single** `N=3·10⁵` (drawdown `≈1/φ`, tail `≈2^{1−k}`, `CV≈1.022`).
"Indistinguishable" is a categorical claim; finite numerics can only bound *tested* deviations.
**Fix:** "matches the annealed i.i.d. model in all **tested** second-moment statistics to within sampling noise
at `N=3·10⁵`." (All the underlying `[OBSERVED]` tags are correct; only the summary noun over-reaches.)

### 2. [NEEDS-CAVEAT] "no second-moment statistic separates the orbit from i.i.d." — unfounded universal
**Offending phrase** — `(Q4)`:
> "**no second-moment statistic** separates the orbit from i.i.d."
A universal quantifier over all statistics, established only for three. **Fix:** "none of the **tested**
second-moment statistics (drawdown law, depth tail, large-depth spacing) separates the orbit from i.i.d."

### 3. [CORRECT] §10 (C3) — the displayed sum `Σ_J φ^{−J} ≈ 1.7·10⁻⁴` is literally wrong
**Offending phrase** — `(C3)`:
> "`Σ_J φ^{−J} ≈ Σ_J φ^{−J} ≈ 1.7·10⁻⁴`".
As written (from `J=1`) `Σ_{J≥1} φ^{−J} = φ ≈ 1.618`, **not** `1.7·10⁻⁴` — off by `~10⁴`. The small number is
`Σ_{J≥20} φ^{−J} = 1.731·10⁻⁴` in `ldp_layer.py`, i.e. it depends **entirely on the arbitrary burn-in offset
`J₀=20`** (chosen to match the empirical running-min ~12–17: `J₀=17` gives `7.3·10⁻⁴`). **Fix:** write
`Σ_{J≥J₀} φ^{−J}` with the offset shown, and state that the specific value is offset-dependent (it is already
`[HEURISTIC, annealed]`, so no proof status is at stake — but the equation as printed is false and the magnitude
is a modelling choice, not a computed constant).

### 4. [NEEDS-CAVEAT] (S4) — first "⟺" should be "⟸ (sufficient)"
**Offending phrase** — `(S4)`:
> "`(K) ⟺ liminf_J N₂(J)/J ≥ 1/2` (the ψ-form / freq(D≥2)≥½ **sufficient case**)".
`freq(D≥2) ≥ ½` **implies** `(K)` (`meanD≥3/2`) but is **not** equivalent: `meanD = 1 + Σ_{k≥2}P(D≥k)`, so
`meanD≥3/2 ⟺ Σ_{k≥2}N_k/J ≥ ½` (the *sum*, which the note states correctly right after). One can have
`N₂/J<½` yet `(K)` (e.g. `D∈{1,3}` at 40% D=3: `freq(D≥2)=0.4`, `meanD=1.8`). The parenthetical "sufficient case"
shows the author knows, but the `⟺` symbol contradicts it. **Fix:** change the first `⟺` to `⟸` (sufficient
condition); keep the second, correct `⟺` with `Σ_{k≥2}N_k`.

### 5. [NEEDS-CAVEAT] §7 (W3) "[PROVEN consistency]" and §11 "morally certain"
- `(W3)` is sound as a **non-exclusion** statement (the proven run-ceiling `0.585n` exceeds the drift line
  `0.5n`, so proven bounds don't rule out halting). But make explicit that **only** `0.585n` is proven; the
  `0.5n` is the **a.e./Haar drift**, unproven for the orbit — and, crucially, `drift>0 ⟺ meanD>3/2 ⟺ (K)`, so
  the `0.5` side is itself `(K)`-grade. The note says "drift +½ from the a.e. mean," which is correct; recommend
  strengthening to "the a.e./Haar drift (not a proven property of the orbit; drift>0 is itself `(K)`)". The
  `[PROVEN consistency]` header is defensible but should read "[PROVEN: the proven bounds are consistent with
  halting]" to avoid a reader inferring the drift is proven. `(W1)[PROVEN]` correctly tags the *formula*; the
  value `0.496` is `[OBSERVED]` — fine. `(W2)` correctly `[OBSERVED]`, Net(W) says "Empirically" — fine.
- §11 Net "makes non-halting **morally certain**": heuristic rhetoric. Recommend explicit `[HEURISTIC]` and/or
  softening to "makes non-halting overwhelmingly plausible under the annealed model." Net(Q) "descriptively
  complete and matches" — "complete" means "at the tested second-order statistics"; qualify.

---

## Bottom line
No false theorem, no mislabelled `[PROVEN]`, no annealed→quenched leak, no `(K)`-progress over-claim. The theory
is honest descriptive/annealed architecture as advertised. The required corrections are: (3) the literally-wrong
`Σφ^{−J}` equation and its hidden offset; (4) the `(S4)` `⟺`-vs-`⟸`; and (1)/(2) softening "i.i.d.-indistinguishable"
/ "no second-moment statistic" from categorical to "tested statistics at `N=3·10⁵`". (5) is polish. With these,
the note meets the zero-false-proof bar.
