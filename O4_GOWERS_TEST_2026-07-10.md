# o4 Gowers-norm / nilsequence-inverse test — the frequency phase e(W_n/3) is Gowers-uniform at U² AND U³; the δ₋₁₄ wall is NOT a nilsequence (2026-07-10)

*A genuinely-new measurement on the o4 frequency problem: Gowers uniformity norms U², U³ and
inverse-theorem (Green–Tao–Ziegler structure-vs-randomness) correlation. The prior white measurement
(`FREQUENCY_AXIS_PROBE_2026-07-08`) was autocorrelation + conditional entropy = the **U¹/linear** level only.
The Gowers U²/U³ norms and correlation with polynomial-phase / nilsequence obstructions were never measured —
this is the modern tool for "does the frequency of a residue in a deterministic sequence deviate." Interpreter
`quantum-ecc/.venv` python; FFT-based exact identities; every claim carries a SHUFFLE control and an INJECTED-structure
validation. STRICT labels. NOT committed.*

---

## 0. One-line verdict

**[OBSERVED — Gowers-uniform at U² and U³; no nil obstruction; tool inapplicable as a route; no label upgraded].**
The cube-root phase `f(n)=e(W_n/3)=ω^{W_n mod 3}` of the actual seed-43 o4 orbit is, at `N=2¹⁶`, **statistically
indistinguishable from a random/shuffled sequence at every measured Gowers level**: `‖f‖_{U²}` z = −0.73 vs shuffle,
best linear phase z = −0.75, `‖f‖_{U³}` **z = +0.03 / −0.27 (exact full-h)**, and the best quadratic-phase and
best bracket-nilsequence correlations both sit **below** the shuffle control at the multiple-testing floor. A
VALIDATION control proves the estimator is not blind: an injected quadratic phase `e(αn²)` has `U²`=0.072
(random-level) yet `U³`=0.872 (≈2.3× the floor) — genuine 2-step structure invisible to U² is loudly detected by U³.
o4's `f` shows **neither**. By the U³ inverse theorem, U³-uniformity ⟹ `f` correlates with **no 2-step nilsequence**:
the δ₋₁₄ obstruction is **not nil-structured**. The Gowers/nilsequence machinery equidistributes `f` but yields
**no exploitable structured obstruction** — confirming the wall is the non-nil quenched object, exactly consistent
with the transfer-operator finding (δ₋₁₄ a fixed point, not a rotation/eigenfunction). **No machine decided. No label upgraded.**

---

## 1. Setup [PROVEN structure, from prior builds]

Odometer `3G'=4G+e(ρ)`, `ρ=G mod 3`, `e={0:9,1:14,2:1}`; mirror `W=G+14`. Phase
`f(n)=e(W_n/3)=ω^{W_n mod 3}`, `ω=e^{2πi/3}` — a unit-modulus function taking the three cube roots of unity.
The freq↔exp-sum dictionary (`O4_EXPSUM_FREQUENCY_BUILD`): `freq{3|W_n}=1/3+(2/3)·Re((1/N)Σf)`, fatal ⇔
`Re≥7/10`. Measured (`N=2¹⁶`, exact big-int G): `W mod3` counts `[21726,21904,21906]`,
`freq{3|W_n}=0.33151`, `(1/N)Σf = −0.00273−0.00003i`, `|mean f| = 0.00273`. The DC term is ~0 (`f` essentially
balanced/mean-zero), so the Gowers norms below are not inflated by a mean.

Gowers norms computed on the cyclic group Z_N by the standard FFT identities with the expectation-normalized
transform `f̂(ξ)=(1/N)Σ_x f(x)e(−2πixξ/N)`:
`‖f‖_{U²}⁴ = Σ_ξ|f̂(ξ)|⁴`; `‖f‖_{U³}⁸ = E_h Σ_ξ|FT(Δ_h f)(ξ)/N|⁴`, `Δ_h f(x)=f(x+h)·conj f(x)`
(the derivative recursion, confirmed against the literature definitions).

## 2. U² / linear level — Gowers-uniform, no linear phase [OBSERVED, N=2¹⁶]

| quantity | f (o4) | shuffle control | z | random floor |
|---|---|---|---|---|
| `‖f‖_{U²}` | 7.429·10⁻² | 7.435·10⁻² ± 8·10⁻⁵ | **−0.73** | `N^{−1/4}`=6.25·10⁻² |
| best linear `max_ξ|f̂(ξ)|` | 1.256·10⁻² (θ=0.803) | 1.306·10⁻² ± 7·10⁻⁴ | **−0.75** | `√(logN/N)`=1.30·10⁻² |

`f` is **U²-uniform**: the U² norm equals the shuffle value and the single best linear phase `e(θn)` sits at the
random `√(logN/N)` floor (the "peak" θ=0.803 is noise). This **confirms the exponential-sum agent's square-root
cancellation** (`O4_EXPSUM_FREQUENCY_BUILD` §4, α=0.491) at the Gowers level: no linear/Kronecker obstruction.

## 3. U³ / quadratic-2-step level — Gowers-uniform [OBSERVED, exact full-h]

Sampled-h estimate at `N=2¹⁶` gave `‖f‖_{U³}=0.27263` vs shuffle `0.27263` (z=+1.44, but the f- and
shuffle-estimates used independent shift-samples). The **exact full-h** computation (all N shifts, identical
treatment) settles it:

| N | `‖f‖_{U³}` (exact) | shuffle (8 draws) | z | `‖f‖_{U²}` |
|---|---|---|---|---|
| 8192 | 3.719244·10⁻¹ | 3.719242·10⁻¹ ± 8·10⁻⁶ | **+0.03** | 1.253·10⁻¹ |
| 16384 | 3.410616·10⁻¹ | 3.410623·10⁻¹ ± 3·10⁻⁶ | **−0.27** | 1.055·10⁻¹ |

`f` is **U³-uniform**: to 6–7 significant figures its third Gowers norm equals that of its own random shuffle. The
earlier z=+1.44 was pure shift-sampling noise.

## 4. Inverse-theorem obstruction search — no quadratic, no nilsequence [OBSERVED]

Direct search for the structured obstruction the inverse theorem would produce if U³ were large:

| obstruction family | best correlation, f | shuffle | floor |
|---|---|---|---|
| quadratic phase `max_{a,b}|E f·e(−an²−bn)|` (4000 a's) | 1.754·10⁻² (a≈0.446) | 1.823·10⁻² | `√(log4000/N)`≈1.12·10⁻² |
| bracket-nilseq `max_{a,b}|E f·e(−a·n⌊bn⌋)|` (1500 draws) | 9.998·10⁻³ | 1.041·10⁻² | 1.12·10⁻² |

In **both** families `f` scores **below** its own shuffle, at the multiple-testing floor. No polynomial-phase or
2-step (Heisenberg bracket) nilsequence correlates with `f` beyond chance.

## 5. VALIDATION — the estimator fires on genuine structure [OBSERVED, decisive for soundness]

The null result is meaningful only if the estimator detects structure when present. Injected controls at `N=2¹⁶`:

| injected | `‖·‖_{U²}` | best linear | `‖·‖_{U³}` | quad-search |
|---|---|---|---|---|
| linear `e(θn)` | **0.762** (huge) | **0.667** | 0.870 | — |
| quadratic `e(αn²)` | 0.072 (**random-level**) | 0.0074 | **0.872** (huge) | recovers a₀ with corr **1.0000** |

The quadratic phase is **U²-uniform yet U³-huge** — exactly the case the inverse theorem is built to catch, and the
estimator catches it (U³ ≈ 2.3× the random floor; the α-search recovers the injected frequency at correlation 1).
o4's `f` exhibits **neither** the linear nor the quadratic signature. The tool would have fired on a nilsequence;
it does not fire on o4.

## 6. Interpretation [honest]

`f=e(W_n/3)` is **Gowers-uniform at U² and U³** — indistinguishable from random at the linear, quadratic, and
2-step-nilsequence levels, with no correlated linear/quadratic/bracket obstruction above the random floor. Two
consequences:

1. **Equidistribution holds empirically** (U¹,U²,U³ all at the random value) — the frequency deviation `Re((1/N)Σf)`
   is `−0.0027`, deep inside the `0.30` slack of the `Re<0.7` target; no U^k level shows a deviation. This re-derives
   the exp-sum agent's square-root cancellation through the modern structure-vs-randomness lens.
2. **The inverse theorem yields NO structured obstruction to exploit.** U³-uniformity ⟹ (Green–Tao–Ziegler) `f`
   correlates with no 2-step nilsequence. Therefore the δ₋₁₄ wall is **not a nilsequence** — it is the non-nil,
   quenched fixed-point object. This is a *new characterization*, not a route: the nilsequence tool is **inapplicable**
   precisely because the obstruction lives outside the nil-hierarchy. It matches, from the harmonic-analysis side, the
   transfer-operator finding (`O4_TRANSFER_OPERATOR_BUILD`): δ₋₁₄ is an eigenvalue-1 **fixed point** of the quenched
   map, not a rotation/eigenfunction — there is no Kronecker or nilfactor for a nilsequence to live on. The Koopman
   operator's annihilation of all non-`3|·` frequencies (loc. cit. §2) is the exact-arithmetic shadow of the U²-uniformity
   measured here.

**Why this does not decide o4.** Gowers-uniformity is the *good* case for equidistribution but the *empty-handed*
case for a proof: the inverse theorem converts "large U^k" into exploitable structure, and there is no large U^k. A
proof still needs a **quenched, effective** equidistribution rate for the single ×4/3 3-adic orbit (the (K)/Mahler-3/2
object); the measured uniformity is empirical (`N≤2¹⁶`), and the same uniformity holds for the fatal δ₋₁₄ orbit's
*complement*, so no unconditional bound is produced. The tool confirms **no nil-structure is being missed** — closing
a route by showing it is not there — rather than opening one.

## 7. What was built

| item | content | label |
|---|---|---|
| `‖f‖_{U²}`, best linear | z=−0.73, z=−0.75 vs shuffle; at `√(logN/N)` floor | `[OBSERVED, N=2¹⁶]` |
| `‖f‖_{U³}` exact full-h | z=+0.03 (N=8192), z=−0.27 (N=16384) vs shuffle | `[OBSERVED, exact]` |
| inverse-U³ search | best quadratic & bracket-nil BELOW shuffle, at floor | `[OBSERVED]` |
| estimator validation | injected `e(αn²)`: U²-uniform, U³=2.3×floor, α recovered at corr 1 | `[OBSERVED, decisive]` |
| verdict | Gowers-uniform ⟹ no nilsequence obstruction ⟹ tool inapplicable; δ₋₁₄ non-nil | `[OBSERVED]` |

Scripts: `o4_gowers_test.py` (U²/U³ sampled, inverse search, validation; ~56s),
`o4_gowers_exact_u3.py` (exact full-h U³ cross-check + injected control). Interpreter `quantum-ecc/.venv`. Not committed.

No machine decided. No label upgraded.
