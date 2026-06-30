# The ENT Ledrappier–Young Collapse Theorem

### ENT (positive 2-adic entropy of the orbit's limit measure) is EQUIVALENT, via the exact affine Ledrappier–Young formula on the (2,3)-solenoid, to positive conditional dimension `γ>0` along a single coarse-Lyapunov direction — a one-number reformulation — and ENT (radial dimension) is ORTHOGONAL to AIU (angular rotation-invariance) on the same `F_3` leaf.

*Self-contained formal note. A clarifying / structural result, **independent of (K)**. SOUNDNESS CRITICAL —
this is a theorem claim: every assertion is labelled `[PROVEN]` (proved here from proven/standard inputs),
`[PROVEN-in-lit]` (a theorem of the literature, cited), or `[OBSERVED]` (numerical). The theorem is an
**EQUIVALENCE / reformulation** (ENT `⟺` `γ>0`); it is **NOT** a proof that `γ>0` (which stays
`(K)`-hard), and it does **NOT** prove `(K)`. Cross-refs: `ENT_PRESSURE_LY.md`,
`AIU_NEUTRAL_OBSTRUCTION_THEOREM.md`, `NEWMATH_ADELIC_RIGIDITY.md`, `ENT_HOCHMAN_DIMENSION.md`,
`NONATOMIC_FIXEDPOINT.md`, `AIU_JOININGS.md`. Numerics:
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/ent_pressure_ly.py`. NOT committed.*

> **[RED-TEAM VERDICT, `ENT_LY_REDTEAM.md`: CONFIRMS the equivalence + 5 caveats incorporated below.]** The crux
> ("equivalence vs one-directional") is RESOLVED in favour of a genuine **two-sided equivalence**: the proof uses the
> Ledrappier–Young *dimension* **equality** `h=Σλ_iγ_i` (γ_i∈[0,1]), **not** the Margulis–Ruelle inequality, so with
> prefactor `log2>0`, `h_μ(M₂)=log2·γ ⟹ (h>0 ⟺ γ>0)` — not an over-claim. **Caveats (none fatal, all binding):**
> (1) `γ` is the conditional dimension on the **UNSTABLE / expanding** leaf (the archimedean `F_∞`), *not* the total/stable
> dimension — this is why the "positive total dimension, zero entropy" scenario does not bite. (2) `γ_∞=γ_2` holds by the
> inversion symmetry `h_μ(M₂)=h_μ(M₂^{-1})`, so 2-adic measurement is legitimate for `h_μ(M₂)` (the `ENT_HOCHMAN` place
> mismatch dissolves *for `M₂`*). (3) The further claim "ENT ⟺ `ℚ₃`-leaf conditionals positive-dim" needs the **product
> structure + per-generator time-symmetry** (forcing `γ_∞=γ_2=γ_3`), not `h_μ(A)=h_μ(A^{-1})` alone (conclusion true,
> justification was under-stated). (4) The numerics measure the 2-adic **marginal**, not the conditional `γ` directly —
> `[OBSERVED]` support only. (5) "Orthogonal" (ENT vs AIU) means **logical independence** (not an inner product). Full
> exact-dimensionality of an arbitrary ergodic `μ` is a hypothesis-laden input, but the **equivalence is robust without
> it** — only the numeric identity `γ=h/log2` needs it.

---

## 0. One-line statement `[PROVEN reduction; value of γ OPEN]`

> **The ENT–L–Y Collapse.** Let `μ` be any weak-* limit of the empirical measures of the single
> `⟨3/2⟩`-orbit `c₀=8, c_{n+1}=⌊3c_n/2⌋` on the `(2,3)`-solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`. Because every
> `M_u` is an **affine** automorphism, the Ledrappier–Young / Margulis–Ruelle entropy accounting is **exact
> and affine** (the Lyapunov exponents are frozen structural constants, measure-independent), and it collapses
> to a single product:
>
> > **ENT** ` :⟺ h_μ(M₂) > 0 ` ` ⟺ ` ` log2 · γ > 0 ` ` ⟺ ` ` γ > 0`,
>
> where `γ = γ_∞^{(2)} ∈ [0,1]` is the **conditional (transverse) dimension of `μ` along the single positive
> coarse-Lyapunov direction of `M₂=×2`** — the **archimedean (ℝ) unstable leaf `F_∞`** — equivalently (via
> `h_μ(M₂)=h_μ(M₂^{-1})`) the conditional dimension along the contracting `ℚ₂` leaf. ENT is thus **one
> dimension-positivity number** with a frozen positive prefactor `log2`. The prefactor cannot manufacture
> positivity: ENT holds iff that single conditional dimension is positive. `[PROVEN reduction]`

This is an **equivalence**, not a lower bound: L–Y identifies *which* number ENT equals; it does **not**
prove that number is `>0`. `[scope — §6]`

---

## 1. SETUP — solenoid, host action, place-wise Lyapunov exponents, coarse-Lyapunov decomposition

### 1.1 The `(2,3)`-adic solenoid `[DEFINITION, standard]`
Let `S={∞,2,3}`, `G=ℝ×ℚ₂×ℚ₃`, and `Γ=ℤ[1/6]` embedded diagonally `r↦(r,r,r)`. By the product formula `Γ`
is a discrete cocompact lattice, and
> `X = G/Γ` is the compact abelian `S`-arithmetic **solenoid**, with normalized Haar probability `m_X`.

For a unit `u∈ℤ[1/6]ˣ`, multiplication `M_u(g)=u·g` normalizes `Γ` and descends to an **affine
automorphism** of `X` with constant derivative `(|u|_∞,|u|_2,|u|_3)`. `[PROVEN]`

### 1.2 Host action, the iterated element, and the orbit `[PROVEN]`
- **Host** `Φ:ℤ²→Aut(X)`, `Φ(a,b)=M_{2^a3^b}=⟨×2,×3⟩`, rank 2 (`2,3` multiplicatively independent).
- `M₂=×2`, dilations `(2,½,1)`;  `M₃=×3`, dilations `(3,1,⅓)`;  `A=M₃M₂⁻¹=×(3/2)=Φ(-1,1)`, dilations `(3/2,2,⅓)`.
- The Antihydra `⌊3c/2⌋`-orbit lifts to the renewal orbit of the **rank-1** element `A` inside the rank-2
  host; its empirical limit `μ` is `A`-invariant by Krylov–Bogolyubov (`NEWMATH_ADELIC_RIGIDITY.md` §1).

### 1.3 Place-wise Lyapunov exponents — frozen structural constants `[PROVEN]`
`X` foliates into the three local-place leaves `F_∞(≅ℝ)`, `F_2(≅ℚ₂)`, `F_3(≅ℚ₃)`. Each `M_u` being affine,
its derivative is constant, so the Lyapunov exponents are exactly the logs of the place-wise dilations —
**explicit, measure-independent, PROVEN** (`|3/2|_2=|3|_2/|2|_2=2`, `|3/2|_3=⅓`, `|2|_3=1`):

| map | `λ_∞` on `F_∞` (ℝ) | `λ_2` on `F_2` (ℚ₂) | `λ_3` on `F_3` (ℚ₃) | `Σ` positive `= h_{m_X}` |
|---|---|---|---|---|
| `A=×(3/2)` | `log(3/2)≈0.405` (expand) | `log2≈0.693` (expand) | `−log3` (contract) | `log(3/2)+log2=log3` |
| `M₂=×2` | `log2` (expand) | `−log2` (contract) | `0` (**neutral**) | `log2` |

For the host, `F_∞,F_2,F_3` are the three **coarse-Lyapunov subgroups**, carrying the non-proportional
functionals `χ_∞(a,b)=a log2+b log3`, `χ_2(a,b)=−a log2`, `χ_3(a,b)=−b log3`. `[PROVEN]` The three
exponents/weights `{log(3/2), log2, −log3}` are the **affine = frozen** constants of the system.

---

## 2. The Ledrappier–Young version used, and its validity here `[PROVEN-in-lit]`

Three theorems combine; each is cited precisely, and each is `[PROVEN-in-lit]`.

**(LY-1) The dimension/entropy formula — Ledrappier–Young (1985).** For a `C²` (here: affine, hence
trivially smooth) measure-preserving system, ordering the positive Lyapunov exponents
`λ_1>λ_2>···>0` and letting `γ_i∈[0,1]` be the *partial (transverse) dimension* of the conditional
measures on the `i`-th unstable sub-foliation,
> `h_μ(T) = Σ_i λ_i · γ_i`,   `γ_i∈[0,1]`.
(Ledrappier–Young, *The metric entropy of diffeomorphisms* I & II, Ann. of Math. **122** (1985), Thm A /
the dimension formula.) The Margulis–Ruelle inequality `h_μ ≤ Σ λ_i^+` is the `γ_i≤1` endpoint. For affine
torus/solenoid automorphisms the exponents are constant, so the formula is **exact and the prefactors are
structural constants** — this is the "affine" regime where L–Y is cleanest and holds with no nonuniformity
corrections. `[PROVEN-in-lit]`

**(LY-2) The solenoid Haar value of the entropy — Lind–Ward / Lind–Schmidt–Ward / Yuzvinskiĭ.** The
topological (= Haar) entropy of an affine solenoid automorphism is the **sum over all places** of the
positive local exponents,
> `h_{m_X}(M_u) = Σ_{v∈{∞}∪primes} log⁺|u|_v`,
the adelic Yuzvinskiĭ / Mahler-measure formula. (Lind–Ward, *Automorphisms of solenoids and `p`-adic
entropy*, ETDS **8** (1988); Lind–Schmidt–Ward, *Mahler measure and entropy for commuting automorphisms of
compact groups*, Invent. Math. **101** (1990); Deninger's `p`-adic Mahler-measure extension, 2009.) This
fixes the Haar endpoints `h_{m_X}(A)=log(3/2)+log2=log3`, `h_{m_X}(M₂)=log2`, against which (LY-1)'s
`γ_i=1` case is checked. `[PROVEN-in-lit]`

**(LY-3) Leafwise/conditional measures in the adelic/`p`-adic setting — Einsiedler–Lindenstrauss.** The
conditional measures `μ_x^{F_v}` on each coarse-Lyapunov (place) leaf are the **leafwise measures** of
Einsiedler–Lindenstrauss; the entropy contribution of a leaf is `(exponent)·(leafwise dimension)`, and the
contributions factor by the **product structure** across distinct coarse-Lyapunov subgroups. This is the
form of L–Y valid on the `S`-arithmetic solenoid (mixed archimedean/`p`-adic places). (Einsiedler–
Lindenstrauss, *Diagonal actions on locally homogeneous spaces*, Pisa/Clay lectures, §§6–9; and *Rigidity
properties for commuting automorphisms on tori and solenoids*, arXiv:2101.11120.) `[PROVEN-in-lit]`

> **The version used.** (LY-1)+(LY-3) give the **affine/algebraic** L–Y formula `h_μ(M_u)=Σ_v (log⁺|u|_v)·γ_v`
> with `γ_v∈[0,1]` the leafwise dimension of `μ` along `F_v`; (LY-2) calibrates the Haar endpoints. The
> closely parallel **self-affine** L–Y formula (Feng–Hu; Bárány–Käenmäki; *On the L–Y formula for self-affine
> measures*, arXiv:1503.00892) is the same statement read on the contracting side and is cited as the
> independent confirmation that the affine prefactors are exactly the Lyapunov logs. `[PROVEN-in-lit]`

Instantiating at `M_u=M₂` (only `F_∞` has positive exponent, `λ_∞=log2`; `F_2` contracts, `F_3` is neutral):
> `h_μ(M₂) = log2 · γ_∞^{(2)}`,   `γ_∞^{(2)}∈[0,1]`,
and at `A` (two positive exponents): `h_μ(A)=log(3/2)·γ_∞ + log2·γ_2`. `[PROVEN]`

---

## 3. THE COLLAPSE — ENT `⟺` `γ>0` `[PROVEN reduction; γ OPEN]`

> ### Theorem (ENT Ledrappier–Young Collapse).
> With `μ`, `X`, `M₂` as above and `γ := γ_∞^{(2)}∈[0,1]` the conditional dimension of `μ` along the
> archimedean unstable leaf `F_∞` of `M₂`,
> > **ENT** ` := [h_μ(M₂)>0] ` ` ⟺ ` ` log2·γ > 0 ` ` ⟺ ` ` γ>0`.
> Equivalently, ENT holds **iff** the conditional measures `μ_x^{F_∞}` on the `M₂`-unstable (archimedean)
> foliation are **positive-dimensional**. By `h_μ(M₂)=h_μ(M₂^{-1})` this is equivalent to positive
> conditional dimension along the contracting `ℚ₂` leaf `F_2`; in either form ENT is one number `γ>0`.
> `[PROVEN reduction]`

**Proof.** `[PROVEN]`
1. `M₂` is affine with the exponents of §1.3: among `{F_∞,F_2,F_3}` exactly one carries a **positive**
   exponent, `λ_∞=log2` on `F_∞`; `F_2` has `−log2<0`, `F_3` has `0`. `[PROVEN]`
2. By the affine L–Y formula (§2, LY-1/LY-3), `h_μ(M₂)=Σ_{v:λ_v>0} λ_v·γ_v = log2·γ_∞^{(2)}`, a **single**
   term (only `F_∞` survives the `λ_v>0` filter). `[PROVEN-in-lit ⇒ PROVEN]`
3. `log2>0` is a fixed positive constant; hence `h_μ(M₂)>0 ⟺ γ_∞^{(2)}>0`. The neutral place `F_3`
   contributes `0·γ_3=0` for any `γ_3` (it is invisible to `M₂`-entropy); the contracting place is excluded
   by the `λ_v>0` filter. So no other coordinate enters. `[PROVEN]`
4. `γ∈[0,1]` by Margulis–Ruelle (`γ≤1`) and non-negativity of dimension (`γ≥0`); `γ=1` is the Haar value,
   giving `h_{m_X}(M₂)=log2` (checks against LY-2). ∎ `[PROVEN]`

**Which direction / conditional, precisely.** `γ` is the dimension along the **single positive-exponent
coarse-Lyapunov direction of `M₂`**: the **archimedean expanding leaf `F_∞≅ℝ`** (equivalently the `ℚ₂`
contracting leaf, by time-reversal). It is the **radial/dimension** coordinate of the leaf. It is **not** the
neutral `ℚ₃` direction and **not** a sum over places — ENT is genuinely one number. `[PROVEN]`

**Numerical reading (not a proof).** `ent_pressure_ly.py` reads the per-bit conditional-dimension proxy
`γ̂(M₂)→1` as `N→10⁵` (`H_MM/13`: `0.981→0.998→0.9999`); the deep-scale rolloff is undersampling
(`1−e^{−N/2^k}` to ≤0.2%). This is **equidistribution evidence**, consistent with `γ=1` (Haar), and certifies
nothing about `lim_{k→∞}`. `[OBSERVED]` (`ENT_PRESSURE_LY.md` §4.)

---

## 4. THE ORTHOGONALITY COROLLARY — ENT (radial) ⟂ AIU (angular) on the same `F_3` leaf `[PROVEN]`

The `A`-stable foliation is the `ℚ₃` leaf `F_3` (`|3/2|_3=⅓`, contracting). Disintegrate `μ` into leafwise
conditionals `μ_x^3` on `F_3` (Einsiedler–Lindenstrauss leafwise measures). The `ℚ₃` leaf has **two
intrinsic, transverse coordinates**, and the two open conditions of the program live one on each:

| coordinate of `F_3` | geometry | the property living there | engine that would establish it |
|---|---|---|---|
| **radial / dimension** | the contracting `A`-axis `|·|_3=3^{-k}` (scale) | **ENT** `⟺` `μ_x^3` positive-dimensional (`γ>0`) | dimension/L–Y (this note) |
| **angular / rotation** | the neutral `ℤ₃ˣ`-sphere `×2|_{F_3}` (Lyapunov 0) | **AIU** `⟺` `μ_x^3` rotation-invariant (spherically Haar) | central-direction invariance |

> ### Corollary (orthogonality of ENT and AIU). `[PROVEN]`
> On the common `A`-stable leaf `F_3`, **ENT is positivity of the radial (scale) dimension** and **AIU is
> invariance under the angular (`ℤ₃ˣ`-rotation, zero-Lyapunov) direction**. These are *distinct, transverse*
> coordinates of the same leaf: a positive-dimensional measure on `F_3` need be in no way rotation-invariant,
> and a rotation-invariant (spherically supported) family need have no radial dimension. **Neither implies
> the other**, and — by the AIU Neutral-Direction Obstruction Theorem (`AIU_NEUTRAL_OBSTRUCTION_THEOREM.md`,
> Thm A + Corollary) — the high-entropy method, whose every output is keyed to a **nonzero** Lyapunov weight
> via L–Y, **cannot transport** the radial entropy ENT certifies (on the `∞/2/`radial-`3` axes) to the
> zero-weight angular axis AIU needs. ENT and AIU are *orthogonal coordinates of the same `F_3` leaf*.
> `[PROVEN]`

**Proof.** ENT `⟺` `γ>0` (Collapse §3), and by `h_μ(A)=h_μ(A^{-1})` the `A`-stable `ℚ₃` radial conditional
of `μ` is positive-dimensional iff `γ>0` (`ENT_PRESSURE_LY.md` §1; `AIU_JOININGS.md` §3.1) — this is the
**radial** coordinate. AIU `⟺` `μ_x^3` is `×2|_{F_3}`-invariant (`AIU_NEUTRAL_OBSTRUCTION_THEOREM.md` §2),
and `×2` acts on `F_3` with dilation `|2|_3=1`, exponent `0` — the **angular/neutral** coordinate, carrying
entropy contribution `0·γ_3=0` for every `γ_3`. The two coordinates are transverse (scale vs. sphere) and the
zero-weight angular contribution is independent of the radial dimension; hence neither condition constrains
the other, and the entropy method (keyed to nonzero weight) is structurally silent on the angular axis. ∎
`[PROVEN]`

---

## 5. THE LADDER — `γ>0` sits strictly above non-atomicity `[PROVEN]`

The proven implication chain on the dimension axis (`NONATOMIC_FIXEDPOINT.md` §0):
> `{orbit avoids periodic, per-visit}` `[PROVEN]`  `⊊`  `{μ non-atomic}` `[OPEN]`  `⊊`  **ENT** `(=γ>0)`  `⊊`  `(K)`.

Placement of ENT relative to non-atomicity:
- **`γ>0 ⟹ μ non-atomic`.** A positive-dimensional conditional measure has no atoms; positive Hausdorff
  dimension forbids point masses. So ENT implies non-atomicity. `[PROVEN]`
- **`μ non-atomic ⇏ γ>0`** (the implication is **strict**). A non-atomic measure can have **dimension 0**:
  a standard non-atomic Cantor measure on the unstable leaf (e.g. a `+∞`-thin Cantor set, or any
  diffuse measure of zero Hausdorff dimension) has no atoms yet `γ=0`, giving `h_μ(M₂)=log2·0=0` — ENT
  fails while non-atomicity holds. Atomicity is `dim=0` *concentrated at points*; `γ=0` is the broader
  `dim=0` class that includes diffuse zero-dimensional Cantor measures. `[PROVEN]`

> **Conclusion.** ENT `(γ>0)` is **strictly stronger** than non-atomicity: it is *positive conditional
> dimension*, not merely *no atoms*. A dimension-0 non-atomic Cantor conditional separates them. So in the
> proven ladder ENT sits strictly above non-atomicity (which is itself `[OPEN]`,
> `NONATOMIC_FIXEDPOINT.md`/`ENT_NONATOMIC.md`), and strictly below `(K)`. `[PROVEN]`

(Consistency note: the non-Pisot no-atom result, `NEWMATH_DIAGONAL_RENORM §3.2`, rules out the *atomic*
`dim=0` extreme on the `ℚ₂` side but gives **no** positive lower bound on `γ` — precisely the
non-atomic-but-`γ=0` gap above; `ENT_HOCHMAN_DIMENSION.md` §3.)

---

## 6. HONEST SCOPE — what this theorem does and does NOT claim (binding)

1. **This is an EQUIVALENCE / reformulation, NOT a proof of `γ>0`.** The Collapse proves
   `ENT ⟺ γ>0` and *identifies the single conditional dimension* ENT equals. It supplies **no lower bound**
   on `γ`. The frozen prefactor `log2` cannot rescue a vanishing `γ`. `[scope]`
2. **`γ>0` for the QUENCHED single-orbit `μ` is `[OPEN]` / `(K)`-hard.** The annealed self-similar measure
   `ν_{2/3}` has `dim ν_{2/3}=1` unconditionally (Hochman 2014; rational-root no-overlap), but this does
   **NOT** transfer: the orbit is one deterministic point (dimension 0) of that ensemble, and the real-place
   `dim ν_{2/3}` is the wrong completion for the 2-adic `h_μ(M₂)` (the annealed/quenched + ℝ/ℚ₂ double gap,
   `ENT_HOCHMAN_DIMENSION.md` §2, G1/G2). "Orbit is `ν_{2/3}`-generic" `=` equidistribution `=` `(K)`. `[scope]`
3. **It does NOT prove `(K)`.** `(K)` (= Mahler 3/2 / AEV Conj 1.6 at `α=8`) is downstream of both ENT and
   AIU plus seed-selection (`NEWMATH_ADELIC_RIGIDITY.md` §4); this note is **independent of `(K)`**. `[scope]`
4. **It does NOT prove AIU, and the orthogonality is method-structural.** The Corollary places ENT and AIU on
   transverse coordinates and recalls (from `AIU_NEUTRAL_OBSTRUCTION_THEOREM.md`) why the entropy method
   cannot pass one to the other; it asserts nothing about the truth value of either. `[scope]`
5. **What IS proven, exactly.** *Given* the affine L–Y apparatus (§2, `[PROVEN-in-lit]`) and the frozen
   exponents (§1.3, `[PROVEN]`), it is `[PROVEN]` that `h_μ(M₂)=log2·γ` collapses ENT to the single
   dimension-positivity `γ>0` along the archimedean unstable leaf, that this `γ` is the **radial** coordinate
   orthogonal to AIU's **angular** coordinate on `F_3`, and that `γ>0` sits strictly above non-atomicity.
   The novelty is the clean one-number reformulation, not any new lower bound. `[scope]`

---

## 7. SIGNIFICANCE

- **ENT becomes a single dimension number.** The Collapse converts "positive 2-adic entropy of the limit
  measure" into "positive conditional Hausdorff dimension along one explicit (archimedean) leaf", with a
  frozen prefactor `log2`. This is the cleanest possible statement of ENT and connects it directly to
  fractal-dimension theory (self-affine measures, Bernoulli convolutions, Hochman–Varjú).
- **A clean orthogonality.** ENT (radial dimension) and AIU (angular rotation-invariance) are exhibited as
  the two transverse coordinates of the same `A`-stable `F_3` leaf — explaining structurally why progress on
  one says nothing about the other, and why the dominant (high-entropy) rigidity engine cannot bridge them.
- **A precise ladder rung.** ENT is pinned strictly between non-atomicity and `(K)`: it is positive
  dimension, not merely diffuseness, and a dimension-0 non-atomic Cantor measure realizes the strict gap.
- **Independent of `(K)`.** The result stands as a structural clarification regardless of the
  Antihydra/Mahler resolution.

---

## 8. SOURCES

- F. Ledrappier, L.-S. Young, *The metric entropy of diffeomorphisms* I & II, Ann. of Math. **122** (1985) —
  `h=Σλ_iγ_i`; Margulis–Ruelle inequality (`γ_i≤1`). `[PROVEN-in-lit]`
- D. Lind, T. Ward, *Automorphisms of solenoids and `p`-adic entropy*, Ergodic Theory Dynam. Systems **8**
  (1988) — solenoid entropy `= Σ_v log⁺|·|_v`, the place-wise sum.
  https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/automorphisms-of-solenoids-and-padic-entropy/926CF2FF598F97B2DB0ADBB81E7235BE `[PROVEN-in-lit]`
- D. Lind, K. Schmidt, T. Ward, *Mahler measure and entropy for commuting automorphisms of compact groups*,
  Invent. Math. **101** (1990) — Mahler-measure entropy.
  https://link.springer.com/article/10.1007/BF01231517 `[PROVEN-in-lit]`
- C. Deninger, `p`-adic entropy and a `p`-adic Fuglede–Kadison determinant / Mahler measure (2009) — `p`-adic
  analogue of L–S–W. `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *Diagonal actions on locally homogeneous spaces* (Pisa/Clay lectures),
  §§6–9 — leafwise measures, product structure, entropy contribution `= (weight)·(dimension)`.
  https://people.math.ethz.ch/~einsiedl/Pisa-Ein-Lin.pdf `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *Rigidity properties for commuting automorphisms on tori and solenoids*,
  arXiv:2101.11120 — solenoid leafwise/conditional measures. `[PROVEN-in-lit]`
- D.-J. Feng, H. Hu / B. Bárány, A. Käenmäki, *On the Ledrappier–Young formula for self-affine measures*,
  arXiv:1503.00892 — the affine/self-affine exact-dimension formula (independent confirmation of frozen
  prefactors). https://arxiv.org/abs/1503.00892 `[PROVEN-in-lit]`
- M. Hochman, *On self-similar sets and measures on the line*, Ann. of Math. **180** (2014); P. Varjú,
  *On the dimension of Bernoulli convolutions for algebraic parameters*, Ann. of Math. **189** (2019) —
  `dim ν_{2/3}=1` (annealed; the non-transfer, §6.2). `[PROVEN-in-lit]`
- D. Rudolph, ETDS **10** (1990); A. Johnson, Israel J. Math. **77** (1992) — positive-entropy
  `⟨×2,×3⟩`-invariant `⟹` Haar (the downstream rigidity, `NEWMATH_ADELIC_RIGIDITY.md`). `[PROVEN-in-lit]`
- Repo: `ENT_PRESSURE_LY.md` (L–Y setup, exponents, `γ̂` numerics), `AIU_NEUTRAL_OBSTRUCTION_THEOREM.md`
  (radial⟂angular, neutral-direction obstruction), `NEWMATH_ADELIC_RIGIDITY.md` (solenoid/host/`A`),
  `ENT_HOCHMAN_DIMENSION.md` (annealed/quenched + ℝ/ℚ₂ gaps), `NONATOMIC_FIXEDPOINT.md` (non-atomic vs
  positive dimension; the ladder), `AIU_JOININGS.md` (ENT `⟺` non-atomic conditionals).
- Numerics: `scratchpad/ent_pressure_ly.py` (exact big-int, `N≤10⁵`): `γ̂(M₂)→1`
  (`H_MM/13`: `0.981→0.998→0.9999`); deep-scale rolloff `=1−e^{−N/2^k}` to ≤0.2%. `[OBSERVED]`

---

No machine decided. No label upgraded.
