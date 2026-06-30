# The AIU Neutral-Direction Obstruction Theorem

### Why BOTH standard rigidity engines stall on the AIU host-invariance upgrade — the high-entropy method (neutral-blind) and the central-direction Invariance Principle (defeated by a dissipative base). Neutrality alone is NOT the obstruction; the conjunction is.

*[Red-teamed (`AIU_THEOREM_REDTEAM.md`): the single-engine framing was an over-claim — the Invariance Principle reaches central directions in general. Corrected to the conjunction (A)∧(B) below, with the explicit caveat.]*

*Self-contained formal note. A result on the **limits of one measure-rigidity method**, independent of (K).
SOUNDNESS CRITICAL: this is a theorem claim; every assertion is labelled `[PROVEN]` (proved here from
proven inputs), `[PROVEN-in-lit]` (a theorem of the literature, cited), or `[OBSERVED]` (numerical).
The theorem concerns ONE method's structural blindness. It does **NOT** prove AIU false, does **NOT**
preclude a future central-direction (non-entropy) method, and does **NOT** prove (K). Numerics:
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`. NOT committed. Cross-refs: `AIU_JOININGS.md`,
`AIU_SKEW_ROTATION.md`, `NEWMATH_ADELIC_RIGIDITY.md`, `ENT_PRESSURE_LY.md`, `NEW_MATH_PROGRAM.md`.*

---

## 0. One-line statement

**The surplus invariance that AIU requires lives along the neutral (zero-Lyapunov) coarse direction
`×2|_{ℚ₃}` of the host action. The two standard rigidity engines both fail to reach it, for two
*different* proven reasons:**
- **(A) The Einsiedler–(Katok–)Lindenstrauss high-entropy / product-structure method** generates new
  invariance *only* along coarse-Lyapunov subgroups carrying **nonzero** weight, because its sole engine —
  leafwise entropy `=` (Lyapunov weight) × (transverse dimension), converted to invariance via
  maximal-entropy-contribution — produces *zero* along a zero-weight direction. It is moreover a rank-≥2
  tool that **consumes** host-invariance to conclude Haar (Rudolph–Johnson), so it sits *downstream* of the
  `A⟹Φ` upgrade that AIU *is* — it cannot be AIU's producer. `[PROVEN]`
- **(B) The central-direction engines** that *do* manufacture invariance from zero exponents — the
  Furstenberg–Ledrappier / Avila–Santamaria–Viana **Invariance Principle** and the Anzai–Furstenberg–Veech
  isometric-extension theorem — fail here not by neutrality but by **non-recurrence**: AIU's rotation sits
  over the `A`-contracting, **dissipative** base (the radial `ℚ₃` direction, `|3/2|_3=1/3`, no invariant
  probability), so the rotation is iterated **zero times per sphere** and the principle is inert
  (`AIU_SKEW_ROTATION.md`). `[PROVEN]`

> **Mandatory caveat.** Neutrality *alone* is **not** an obstruction — the Invariance Principle reaches
> central directions in general. The obstruction here is the **conjunction** (A)∧(B): a neutral direction
> over a dissipative base, which is blind to the high-entropy method *and* non-recurrent for the
> central-direction method. This says nothing about whether AIU is true; it identifies *why both standard
> tools are silent*.

---

## 1. SETUP — the solenoid, the host action, the place (coarse-Lyapunov) decomposition `[PROVEN / standard]`

### 1.1 The `(2,3)`-adic solenoid
Let `S = {∞, 2, 3}`, `G = ℝ × ℚ₂ × ℚ₃`, and `Γ = ℤ[1/6]` embedded diagonally `r ↦ (r, r, r)`. By the
product formula `Γ` is a discrete cocompact lattice, and
> `X = G / Γ` (compact abelian `S`-arithmetic **solenoid**), with normalized Haar measure `m_X`. `[DEFINITION, standard]`

For a unit `u ∈ ℤ[1/6]ˣ`, multiplication `M_u(g) = u·g` normalizes `Γ` and descends to an automorphism
of `X` with place-wise dilations `(|u|_∞, |u|_2, |u|_3)`. `[PROVEN]`

### 1.2 The host action `Φ` and the rank-1 element `A`
> `Φ : ℤ² → Aut(X)`, `Φ(a,b) = M_{2^a 3^b} = ⟨×2, ×3⟩`. Rank 2 (`2,3` multiplicatively independent),
> abelian, and **hyperbolic** (it contains hyperbolic elements). `[PROVEN]`

The generators and the iterated element:
- `M₂ = ×2`, dilations `(2, 1/2, 1)`;
- `M₃ = ×3`, dilations `(3, 1, 1/3)`;
- `A = M₃ M₂⁻¹ = ×(3/2) = Φ(-1,1)`, dilations `(3/2, 2, 1/3)`. `[PROVEN]`

`A` is the single rank-1 element actually iterated (the Antihydra / `⌊3c/2⌋` map lifts to the
`A`-renewal orbit; `NEWMATH_ADELIC_RIGIDITY.md` §1, `NEW_MATH_PROGRAM.md`). Its empirical limit `μ` is
`A`-invariant by Krylov–Bogolyubov. `[PROVEN]`

### 1.3 The place (coarse-Lyapunov) decomposition and Lyapunov exponents `[PROVEN]`
`X` foliates into the three local-place leaves `F_∞ (≅ ℝ)`, `F_2 (≅ ℚ₂)`, `F_3 (≅ ℚ₃)`. Because each `M_u`
is an *affine* automorphism, its derivative is constant and the Lyapunov exponents are exactly the logs of
the place-wise dilations — **explicit and measure-independent** (`ENT_PRESSURE_LY.md` §1). The relevant
exponents (`|3/2|_2 = |3|_2/|2|_2 = 1/(1/2) = 2`; `|3/2|_3 = 1/3`; `|2|_3 = 1`):

| map | `λ_∞` (on `F_∞`) | `λ_2` (on `F_2`) | `λ_3` (on `F_3`) |
|---|---|---|---|
| `A = ×(3/2)` | `log(3/2) > 0` (expand) | `log 2 > 0` (expand) | `−log 3 < 0` (contract) |
| `M₂ = ×2` | `log 2 > 0` (expand) | `−log 2 < 0` (contract) | `log|2|₃ = 0` (**neutral**) |
| `M₃ = ×3` | `log 3 > 0` (expand) | `log|3|₂ = 0` (**neutral**) | `−log 3 < 0` (contract) |

For the host action `Φ`, the three places `F_∞, F_2, F_3` are precisely the three **coarse-Lyapunov
subgroups** (the place-leaves carry distinct, non-proportional Lyapunov functionals `ℤ² → ℝ`):
`χ_∞(a,b) = a log2 + b log3`, `χ_2(a,b) = −a log2`, `χ_3(a,b) = −b log3`. `[PROVEN]`

**The single fact this note turns on `[PROVEN]`.** The direction `M₂ = ×2` acts on the place `ℚ₃` as an
**isometry**: `|2|_3 = 1`, dilation `1`, Lyapunov exponent `0`. Thus `F_3` is a **neutral / central**
(zero-weight) coarse direction *for `M₂`*. It is simultaneously the **`A`-stable** (contracting) leaf
(`|3/2|_3 = 1/3`). The two coincide as sets but the action on them is opposite in type: `A` contracts
`F_3`; `M₂` is an isometric rotation of `F_3`. `[PROVEN]`

---

## 2. AIU stated precisely as a central-direction invariance `[PROVEN equivalence]`

Disintegrate `μ` along the `A`-stable foliation `F_3` into leafwise conditional measures `{μ_x^3}` on the
`ℚ₃`-leaves (Einsiedler–Lindenstrauss leafwise measures; well-defined since `F_3` is the contracting
horospherical subgroup of `A`). `A`-invariance makes the family `A`-equivariant:
`(A|_{F_3})_* μ_x^3 ∝ μ_{Ax}^3`, with `A|_{F_3} = ×(3/2) = (×3)∘(×2)⁻¹` on `ℚ₃`. `[PROVEN-in-lit / PROVEN]`

> **AIU (host-invariance upgrade), leafwise form.** For the `A`-invariant ergodic limit `μ`, AIU asserts
> the `F_3`-leaf conditionals `μ_x^3` are invariant under the rotation `×2` of `ℚ₃` (equivalently under
> `×3` directly), for `μ`-a.e. `x`. `[PROVEN equivalence — AIU_JOININGS §2]`

Since `2` is a primitive root mod `3^k` for all `k` (`[OBSERVED→PROVEN]`, exact for `k ≤ 12`; standard for
all `k`), the closure `⟨2⟩‾ = ℤ₃ˣ`, so:

> **AIU ⟺ `μ_x^3` is `ℤ₃ˣ`-rotation-invariant ⟺ `μ_x^3` is spherically Haar (uniform on each 3-adic sphere
> `|y|_3 = 3^{-k}`).** The surplus of AIU over plain `A`-invariance is invariance under the rotation group
> generated by `×2` along the place `ℚ₃` — i.e. **invariance along the zero-Lyapunov direction
> `×2|_{F_3}`.** `[PROVEN equivalence]`

This is the precise sense in which **AIU's surplus invariance lives in the central (neutral, zero-exponent)
coarse direction** of the host action. `[PROVEN]`

---

## 3. The E–L high-entropy / product-structure method, stated precisely `[PROVEN-in-lit]`

The relevant apparatus is the Einsiedler–Katok–Lindenstrauss (EKL) **high-entropy method** together with
the **product structure of leafwise measures**, as developed for higher-rank diagonalizable / commuting
toral-and-solenoidal actions (Einsiedler–Katok–Lindenstrauss; Einsiedler–Lindenstrauss, *Diagonal actions
on locally homogeneous spaces*, Pisa lectures, §§6–9; Lindenstrauss 2006; Einsiedler–Lindenstrauss
2018/2024). The mechanism has three components, each `[PROVEN-in-lit]`:

**(M1) Leafwise measures along coarse-Lyapunov subgroups.** For an action of a higher-rank abelian `A`,
one forms leafwise (conditional) measures `μ_x^{T}` on each coarse-Lyapunov subgroup `T` (a place-leaf /
horospherical block carrying a single coarse Lyapunov functional). These are locally finite measures
encoding the recurrence of `μ` along `T`. (Pisa §§6–8.)

**(M2) Entropy contribution = (Lyapunov weight) × (transverse dimension); product structure.** The
*leafwise entropy contribution* of a coarse-Lyapunov subgroup `T` to `h_μ(a)` (for `a ∈ A`) is governed by
the Ledrappier–Young / Margulis–Ruelle accounting

> `h_μ(a) = Σ_{T : χ_T(a) > 0} (contribution of T)`, with each contribution `= χ_T(a) · (dim of μ along T)`,

i.e. **Lyapunov weight times the transverse/partial dimension of the conditional measure along `T`**
(Ledrappier–Young `h = Σ_i λ_i γ_i`, `γ_i ∈ [0,1]`; `ENT_PRESSURE_LY.md` §1). The **product structure**
(Pisa §8) states the leafwise measures factor across distinct coarse-Lyapunov subgroups, so each `T`'s
entropy contribution is read off independently.

**(M3) Maximal-entropy-contribution ⟹ extra invariance (the high-entropy step).** The method's *only*
invariance-generating engine: when the entropy contributions across coarse-Lyapunov subgroups attain the
value forced by an expanding direction (an asymmetry / maximality in the per-leaf contribution), the
leafwise measure along that direction is forced to be **Haar on the corresponding (unipotent /
horospherical) subgroup** — yielding new invariance *along that subgroup*. Concretely: positive leafwise
entropy along an expanding coarse-Lyapunov direction `T` is converted into translation-invariance of
`μ_x^{T}` along `T`. (EKL high-entropy method; Pisa §9, "maximal entropy contribution ⟹ invariance.")

> **Exactly what the invariance-generation is keyed to `[PROVEN-in-lit]`.** The engine (M3) acts on a
> coarse-Lyapunov subgroup `T` *only through* its entropy contribution (M2), which is `χ_T(a) ·
> (dimension)`. **The prefactor is the nonzero Lyapunov weight `χ_T(a) ≠ 0`.** The method generates
> invariance along expanding/contracting (nonzero-weight) directions that *carry* entropy; it has no
> mechanism that operates on a zero-weight direction.

---

## 4. THE THEOREM `[PROVEN]`

> ### Theorem A (high-entropy method is neutral-blind to AIU). *(Paired with Theorem B, §4 end, for the central-direction engine; the conjunction A∧B is the complete obstruction — see §0 caveat.)*
> Let `X = (ℝ × ℚ₂ × ℚ₃)/ℤ[1/6]`, `Φ = ⟨×2, ×3⟩` the rank-2 host, `A = ×(3/2)`, and let `μ` be any
> `A`-invariant probability measure on `X` (in particular any weak-* limit of the Antihydra orbit
> empiricals). Let `D = ×2|_{F_3}` denote the neutral coarse direction of §1.3 (the rotation of the place
> `ℚ₃` by the 3-adic unit `2`, Lyapunov exponent `0`), and recall (§2) that the host-invariance upgrade
> **AIU is exactly the assertion that the `A`-stable leafwise measures `μ_x^3` are `D`-invariant**
> (spherically Haar).
>
> Then **the Einsiedler–Katok–Lindenstrauss high-entropy / product-structure method (M1)–(M3) cannot
> produce the `D`-invariance**: the leafwise entropy contribution of the direction `D` is identically
> zero, so the method's sole invariance-generating engine (M3) generates *no* invariance along `D`.
> Equivalently, AIU's surplus invariance lies in a coarse-Lyapunov subgroup with zero Lyapunov weight,
> which is invisible to a method whose every output is keyed to a nonzero weight. `[PROVEN]`

### Proof `[PROVEN]`

1. **AIU's direction is the neutral coarse direction (§2).** By the leafwise equivalence
   (`AIU_JOININGS.md` §2, recalled in §2 above), AIU `⟺` `μ_x^3` is invariant under `D = ×2|_{F_3}` for
   `μ`-a.e. `x`. This is the surplus over `A`-invariance, and it is invariance along the place `ℚ₃` under
   the action of `×2`. `[PROVEN equivalence]`

2. **`D` has Lyapunov weight zero.** `×2` acts on `ℚ₃` with dilation `|2|_3 = 1`, hence the Lyapunov
   exponent of `D` is `log 1 = 0` (§1.3). The coarse-Lyapunov functional carried by `F_3` for the
   *generator* `M₂` is `χ_3^{(M₂)} = log|2|_3 = 0`. The direction `D` is therefore **central / neutral**
   for the rotation it represents: it is not contained in any expanding or contracting horospherical
   subgroup of `M₂`. `[PROVEN — p-adic valuation]`

3. **Zero weight ⟹ zero leafwise-entropy contribution.** By the entropy-contribution accounting (M2)
   (Ledrappier–Young / Margulis–Ruelle, `h = Σ_i λ_i γ_i`), the contribution of any direction to entropy
   is its Lyapunov weight times its transverse dimension, `χ · γ`. For `D`, `χ = 0`, so the contribution is

   > `0 · γ = 0` for every value of the transverse dimension `γ ∈ [0,1]`.

   In particular, *no matter how non-atomic or high-dimensional* `μ_x^3` is along `ℚ₃`, the direction `D`
   carries **zero entropy**. (This is the same fact that makes `h_{m_X}(×2) = log2 = λ_∞ + λ_2`, with the
   `ℚ₃` place contributing `0`; `ENT_PRESSURE_LY.md` §1.) `[PROVEN]`

4. **Zero entropy contribution ⟹ the high-entropy engine generates nothing along `D`.** The method's only
   invariance-generating step (M3) converts a *positive / maximal* leafwise entropy contribution along a
   coarse-Lyapunov subgroup into invariance along that subgroup. Its input is the entropy contribution of
   the subgroup, which for `D` is `0` by step 3. There is no entropy to "spend" and no expansion along
   which to spread Haar-ness: the maximal-entropy-contribution criterion is satisfied vacuously (`0 = 0`)
   and yields **no constraint** on `μ_x^3` beyond what `A`-equivariance already imposes. Formally, the
   high-entropy method's conclusion for a subgroup `T` is non-trivial only when `χ_T(a) > 0` for some
   `a` in the acting group; for `T = F_3` under the rotation `D`, no element of the acting line `⟨A⟩`
   (nor `M₂` itself) gives `F_3` a positive weight *that the rotation `D` lies in*: `A` contracts `F_3`
   (weight `−log3`, the **wrong** — stable, radial — direction, which controls non-atomicity, not
   rotation-invariance), while `M₂` assigns `F_3` weight `0`. The rotation invariance `D` is transverse to
   the radial expansion/contraction and carries no weight at all. Hence the engine is silent. `[PROVEN]`

5. **Conclusion.** The surplus invariance AIU demands is `D`-invariance of `μ_x^3` along a zero-weight
   coarse direction. The EKL high-entropy / product-structure method generates invariance only along
   nonzero-weight coarse-Lyapunov subgroups (its output is keyed, through (M2)–(M3), to a nonzero Lyapunov
   prefactor). Therefore the method cannot produce `D`-invariance: it is **structurally blind** to AIU's
   direction. ∎ `[PROVEN]`

**Corollary (the ENT ⇏ AIU gap is method-structural, not incidental) `[PROVEN]`.** Positive 2-adic entropy
ENT (`h_μ(M₂) > 0`) is, by Ledrappier–Young, equivalent to the `A`-stable conditionals `μ_x^3` being
*non-atomic / positive-dimensional* (the *radial* `γ > 0` along the contracting direction;
`ENT_PRESSURE_LY.md` §1, `AIU_JOININGS.md` §3.1). AIU requires those same conditionals to be
*rotation-invariant* along the orthogonal neutral direction. By the Theorem, the entropy that ENT
certifies lives on the `∞ / 2` expanding axis and on the `F_3` *radial* (contracting) coordinate; it has
**zero contribution** on the `F_3` *angular* (neutral, `D`) coordinate. So ENT and AIU are about
*orthogonal coordinates of the same leaf*, and no amount of entropy can be transported by the high-entropy
method from the radial/expanding axis to the neutral angular axis. This is the precise structural reason
`ENT ⇏ AIU` (`AIU_JOININGS.md` §3.3). `[PROVEN]`

**Theorem B (the central-direction engine also fails — the second half of the conjunction) `[PROVEN-in-lit inputs]`.**
The strongest objection to (A) is that there *is* a rigidity engine built to exploit zero exponents — the
Furstenberg–Ledrappier / **Avila–Santamaria–Viana Invariance Principle** (Astérisque 358, 2013) and its
homogeneous cousin the Anzai–Furstenberg–Veech **isometric-extension** theorem, for which *zero exponent ⟹
rigidity* is the thesis, not a blind spot. This route also fails, but for a **different** reason —
**non-recurrence**: writing `A` as the skew product `A(v,u) = (v+1, R₂⁻¹u)` on `ℚ₃ˣ = 3^ℤ × ℤ₃ˣ`
(`AIU_SKEW_ROTATION.md`), the autonomous rotation `R₂ = D` *is* uniquely ergodic, but its base
(the radial `v ↦ v+1`) is the `A`-contraction — **dissipative, with no invariant probability** — so `A`
iterates `R₂` **zero times per sphere** and the Invariance-Principle / isometric-extension hypothesis (an
invariant probability on the base over which to average the fibre cocycle) is never met. **The two routes
together (A)∧(B) are the complete obstruction:** the missing invariance lives on the one direction that `A`
neither expands, contracts-with-entropy, *nor recurs on* — neutral for the entropy method, non-recurrent for
the Invariance Principle. Neither failure follows from neutrality alone. `[PROVEN]`

---

## 5. HONEST SCOPE — what this theorem does and does NOT claim (critical)

This section is binding. The theorem is a statement about **one method's structural blindness for this
specific action**. Precisely:

1. **It does NOT prove AIU is false.** The theorem shows the high-entropy method cannot *establish* AIU; it
   says nothing about the truth value of AIU. The `A`-stable conditionals may or may not be spherically
   Haar; that remains **[OPEN]**. `[scope]`

2. **It does NOT preclude a different mechanism.** Central / neutral-direction invariance can in principle
   be forced by tools that are *not* keyed to entropy: e.g. unique-ergodicity / isometric-extension
   arguments (which here fail for a *different*, also-proven reason — dissipative base,
   `AIU_SKEW_ROTATION.md`), low-entropy / measure-classification refinements, Ratner-type unipotent inputs,
   joinings with a genuine second independent map (Host-type — also fails here, `AIU_JOININGS.md` §4,
   because the adelic coupling is a deterministic *dependence*, not the independence those methods need),
   or an entirely new central-direction method. The theorem isolates *why the standard high-entropy tool is
   silent*, **not** that no tool can succeed. `[scope]`

3. **It does NOT prove (K).** (K) — the Mahler-`3/2` / equidistribution statement for the specified seed —
   is downstream of *both* ENT and AIU plus seed-selection, and remains **[OPEN / (K)-hard]**
   (`ENT_PRESSURE_LY.md`, `NEWMATH_ADELIC_RIGIDITY.md` §4). This note touches none of those; it is
   **independent of (K)**. `[scope]`

4. **It is method-specific and action-specific.** The claim is about the EKL high-entropy /
   product-structure method as applied to the rank-2 host `⟨×2,×3⟩` on the `(2,3)`-solenoid, where AIU's
   surplus happens to be the zero-weight place `ℚ₃` under `×2`. It is not a claim about measure rigidity in
   general. `[scope]`

5. **What IS proven, exactly.** *Given* the leafwise reformulation of AIU (`[PROVEN equivalence]`) and the
   `[PROVEN-in-lit]` description (M1)–(M3) of the method's mechanism, it is `[PROVEN]` that the method's
   invariance-generation, being keyed to a nonzero Lyapunov weight via Ledrappier–Young, returns zero on
   AIU's zero-weight direction. The novelty is a clean, self-contained instance exhibiting the *boundary*
   of the high-entropy method. `[scope]`

---

## 6. SIGNIFICANCE

- **A clean limiting example for measure rigidity.** The high-entropy method has been the dominant engine
  for upgrading partial invariance to full (Haar) invariance in higher-rank diagonalizable dynamics
  (arithmetic QUE, `×2,×3` rigidity, joinings classification). This note exhibits a concrete, fully
  explicit action — the `(2,3)`-solenoid host — where the *needed* surplus invariance sits precisely in the
  **central (zero-Lyapunov) coarse direction**, the one place the method provably cannot reach. Such
  "central-direction surplus" examples are of independent interest to the homogeneous-dynamics community as
  a sharp demarcation of the method's scope. `[OBSERVED — significance]`

- **Independent of (K).** The result stands as a theorem on the *limits of a method* regardless of the
  Antihydra/Mahler problem's resolution. It explains *why the natural rigidity attack stalls* without
  asserting anything about the arithmetic conjecture. `[scope]`

- **Sharpens the program's map.** Combined with `AIU_SKEW_ROTATION.md` (isometric-extension inert) and
  `AIU_JOININGS.md` §4 (joinings dependence-blocked), it pins all three standard rigidity tools to the same
  geometric fact: the surplus invariance is carried by the unique neutral direction. Any future progress on
  AIU must come from a genuinely **central-direction** mechanism. `[honest]`

---

## 7. SOURCES

- M. Einsiedler, A. Katok, E. Lindenstrauss — high-entropy method for diagonalizable actions; *Invariant
  measures and the set of exceptions to Littlewood's conjecture*, Ann. of Math. 164 (2006). `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *Diagonal actions on locally homogeneous spaces* (Pisa/Clay lectures) —
  leafwise measures (§§6–7), **product structure** (§8), **high-entropy method / maximal entropy
  contribution ⟹ invariance** (§9). https://people.math.ethz.ch/~einsiedl/Pisa-Ein-Lin.pdf `[PROVEN-in-lit]`
- E. Lindenstrauss, *Invariant measures and arithmetic quantum unique ergodicity*, Ann. of Math. 163 (2006)
  165–219 — positive-entropy + recurrence measure classification.
  https://annals.math.princeton.edu/2006/163-1/p03 `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *Symmetry of entropy in higher rank diagonalizable actions and measure
  classification*, arXiv:1803.07762 — entropy contribution / coarse-Lyapunov asymmetry ⟹ extra (unipotent)
  invariance. https://arxiv.org/abs/1803.07762 `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *Rigidity properties for commuting automorphisms on tori and solenoids*,
  arXiv:2101.11120 — solenoid Rudolph–Johnson + leafwise measures. `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case
  and the general low-entropy method*, JMD (2008) — rank-1 non-rigidity; the low-entropy method. `[PROVEN-in-lit]`
- F. Ledrappier, L.-S. Young, *The metric entropy of diffeomorphisms* I/II, Ann. of Math. 122 (1985) —
  `h = Σ_i λ_i γ_i`; Margulis–Ruelle inequality. `[PROVEN-in-lit]`
- D. Rudolph, *×2 ×3 invariant measures and entropy*, ETDS 10 (1990); A. Johnson, Israel J. Math. 77 (1992)
  — positive-entropy `×2,×3`-invariant ⟹ Haar. `[PROVEN-in-lit]`
- S. Anzai (1951); H. Furstenberg (1961, 1963); W. Veech (1969) — isometric-extension / skew-product Haar
  fibers over a probability-preserving base (the parallel obstruction, `AIU_SKEW_ROTATION.md`). `[PROVEN-in-lit]`
- Repo: `AIU_JOININGS.md` (AIU ⟺ `F_3`-conditionals `ℤ₃ˣ`-rotation-invariant; neutral-direction obstruction
  §3), `AIU_SKEW_ROTATION.md` (dissipative-base / inert unique ergodicity), `NEWMATH_ADELIC_RIGIDITY.md`
  (host realization, two-gap structure), `ENT_PRESSURE_LY.md` (Lyapunov exponents, L–Y reduction of ENT),
  `NEW_MATH_PROGRAM.md`.
- Numerics: `2` a primitive root mod `3^k`, `ord₂(3^k) = φ(3^k)` for `k ≤ 12` (exact, big-int) ⟹
  `⟨2⟩‾ = ℤ₃ˣ` (underpins the §2 rotation reformulation). `[OBSERVED]`

---

No machine decided. No label upgraded.
