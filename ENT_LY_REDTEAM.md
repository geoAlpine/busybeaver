# RED-TEAM: "ENT Ledrappier–Young Collapse" theorem — adversarial verification (2026-06-30)

*Adversarial audit of the sibling claim: on the affine `(2,3)`-solenoid automorphism, Ledrappier–Young is
EXACT (`h_μ = Σ_i λ_i^+ γ_i`), so `h_μ(M₂)=log2·γ` and therefore **ENT ⟺ γ>0**; and ENT (radial
conditional dimension) is orthogonal to AIU (angular `ℚ₃`-rotation invariance). Targets: over-claims and
apparatus errors. Labels [CONFIRMS]/[OVER-CLAIM]/[NEEDS-CAVEAT]. Sources cited. Not committed; no machine
decided; no label upgraded.*

---

## 0. Verdict

**[CONFIRMS] with [NEEDS-CAVEAT] on three secondary points.** The headline equivalence **ENT ⟺ γ>0 is a
genuine two-sided equivalence, NOT an over-claim** — *provided* `γ` is read as the conditional dimension
along the **expanding (unstable) leaf** of `M₂`. The crucial point the prompt worried about (Margulis–Ruelle
is only an upper bound; positive dimension can give zero entropy) **does not bite here**, because the docs
correctly invoke the Ledrappier–Young *dimension* formula (an **equality** `h=Σλ_iγ_i`), not the
Margulis–Ruelle *inequality*, and because "positive unstable-conditional dimension ⟺ positive entropy" is a
known **equivalence** in homogeneous/algebraic dynamics. The remaining issues are: (i) the cross-place
identification ENT ⟺ "`ℚ₃`-conditionals positive-dimensional" is stated with an *insufficient* one-line
justification (it is nonetheless true via a fuller argument); (ii) the numerics measure a marginal, not a
conditional; (iii) "positive-dimensional (non-atomic)" is loosely equated. None overturns the theorem; all
three are caveats. It is, as the docs themselves repeatedly state, an honest **reformulation**, not progress
toward (K).

---

## 1. Is L–Y EXACT/an EQUIVALENCE here, or only the Margulis–Ruelle inequality? — **[CONFIRMS: equivalence]**

This is the crux the prompt flagged, and the answer is favorable to the sibling claim.

There are **two different** entropy–exponent statements, routinely conflated, and the docs keep them apart:

- **Margulis–Ruelle inequality** (Ruelle 1978): `h_μ(f) ≤ Σ_i χ_i^+ · dim E_i` — an **upper** bound, full
  multiplicities, **no** dimension weights. Equality ("Pesin's formula") **iff SRB** (absolutely continuous
  unstable conditionals). If this were the only tool, then `h>0 ⟹ γ>0` (one direction) but `γ>0 ⟹ h>0`
  could fail — exactly the prompt's worry.
- **Ledrappier–Young dimension formula** (Ledrappier–Young 1985, Part II): `h_μ(f) = Σ_i λ_i (δ_i−δ_{i−1})`,
  i.e. `Σ_i λ_i γ_i` with `γ_i∈[0,1]` the **transverse (conditional) dimensions** of `μ` on the unstable
  sub-foliations. This is an **EQUALITY for every** (C², or affine/algebraic) invariant measure — **not**
  only SRB. SRB is merely the case `γ_i≡1`. The dimension weights `γ_i` absorb the SRB gap.

The docs (`ENT_PRESSURE_LY.md` §1; `ENT_PESIN_MARGULIS.md` §1, which explicitly writes "**(LY) is an
identity, not a bound**; MR caps the sum") use the **L–Y equality**. Hence `h_μ(M₂)=log2·γ` with a strictly
positive prefactor `log2`, so

> `h_μ(M₂)>0  ⟺  γ>0`   — a true biconditional, because it is an equality with positive prefactor.

This is **reinforced**, not merely asserted, by the homogeneous-dynamics equivalence "an invariant measure
has **positive entropy iff its unstable-leaf conditionals are non-atomic**, equivalently positive Hausdorff
dimension" (standard for hyperbolic toral/solenoidal automorphisms; see Lindenstrauss-school references). So
the equivalence stands on **two** legs: the L–Y equality, and the entropy⟺non-atomic-unstable-conditional
theorem. **[CONFIRMS — equivalence, not one-directional]**

**The one indispensable caveat [NEEDS-CAVEAT].** The prompt's general caution — "a positive-dimension
measure can have zero entropy" — is **true for the TOTAL dimension** of `μ`, and would also be true if `γ`
denoted the **stable** or **neutral**-direction dimension. The equivalence survives **only because `γ` is the
conditional dimension along the EXPANDING (unstable) leaf**. The theorem statement must therefore pin `γ` to
the unstable foliation explicitly; "positive conditional dimension" unqualified is ambiguous and, read as
total/stable dimension, would make `γ>0 ⟹ h>0` **false**. (This is also exactly why ENT is orthogonal to
AIU — §4 — so the caveat is internally consistent with the program.)

---

## 2. Is the `M₂` place / exponent accounting correct? — **[CONFIRMS]**

`M₂=×2` has place-wise dilations `(|2|_∞,|2|_2,|2|_3)=(2,1/2,1)`: expand `ℝ` (`λ_∞=log2>0`), contract `ℚ₂`
(`−log2`), **neutral** `ℚ₃` (`log|2|_3=log1=0`). The **only positive exponent is `log2` on the `ℝ` place**,
so L–Y gives `h_μ(M₂)=log2·γ_∞` with `γ_∞` = dimension of `μ`'s conditional on the `ℝ`-unstable leaf.
**Correct.** [CONFIRMS]

A subtlety worth recording in the theorem's favor: `ENT_HOCHMAN_DIMENSION.md` raised a "place-mismatch"
worry (real-place dimension vs the `ℚ₂` entropy). For `h_μ(M₂)` this worry **dissolves**: by time-symmetry
`h_μ(M₂)=h_μ(M₂^{-1})`, and `M₂^{-1}=×½` expands `ℚ₂` (`|½|_2=2`), giving `h_μ(M₂)=log2·γ_2`. Hence
`γ_∞=γ_2` — the `ℝ`- and `ℚ₂`-conditional dimensions of `M₂` **coincide**, so measuring 2-adic structure is
a legitimate proxy for `γ_∞^{(2)}` (modulo §3 below). The `ℚ₃`-place contributes 0 (neutral), which is the
geometric basis of the §4 orthogonality. **[CONFIRMS]**

---

## 3. Does the apparatus APPLY to the adelic solenoid and to a NON-SRB measure? — **[CONFIRMS, with caveat]**

- **Entropy of the automorphism (Haar):** `h_{m_X}(M_u)=Σ_v log⁺|u|_v` (Yuzvinskii / Lind–Schmidt–Ward).
  `h(M₂)=log2`, `h(A)=log3`. Standard. [CONFIRMS-in-lit]
- **Leafwise/coarse-Lyapunov entropy theory on solenoids:** the relevant apparatus is **exactly** the
  Einsiedler–Lindenstrauss leafwise-measure machinery for commuting automorphisms of **tori AND solenoids**
  (arXiv:2101.11120) — leafwise measures, entropy-contribution bound, coarse-Lyapunov subgroups, **product
  structure**. So "L–Y on the adelic solenoid" is **not** an unjustified transplant of the 1985 manifold
  theorem; it is the cited, purpose-built `S`-arithmetic version. [CONFIRMS-in-lit]
- **Non-SRB / general ergodic `μ`:** because the automorphism is **affine** (constant derivative,
  measure-independent exponents — `ENT_PESIN_MARGULIS.md` §2.1), the leafwise theory applies to **any**
  invariant `μ`, atomic or fractal. The equivalence `h_μ(M₂)>0 ⟺ γ>0` needs no SRB hypothesis (SRB is only
  the `γ=1` endpoint). [CONFIRMS]
- **[NEEDS-CAVEAT] "exact dimensionality."** The clean statement `γ_v = ` a genuine Hausdorff dimension of
  the conditional (rather than just "non-atomic / positive lower dimension") requires **exact-dimensionality**
  of the leafwise conditionals for an *arbitrary* ergodic invariant measure on the solenoid. This is the
  hardest-leaning input; for self-affine measures it is a real theorem with hypotheses (Bárány–Käenmäki;
  Feng; Hochman–Solomyak), and in the homogeneous setting it follows from the E–L leafwise theory but should
  be cited as such, not asserted as automatic. **The equivalence ENT ⟺ γ>0 is robust even without exact-
  dimensionality** (read `γ>0` as "non-atomic / positive lower dimension"); only the precise *numeric value*
  `γ=h/log2` needs the exact-dimension theorem. So labelling the formula "EXACT" is defensible for the
  equality `h=Σλγ`, but "exact-**dimensional**" for general `μ` is a [PROVEN-in-lit, with hypotheses] input,
  not free.

---

## 4. Is the orthogonality-to-AIU corollary sound? — **[CONFIRMS, structural]**

ENT lives in the **radial/expanding** coordinate: `γ` on the `ℝ`(/`ℚ₂`) unstable leaf. AIU's surplus
invariance lives in the **angular/neutral** coordinate: `ℚ₃`-rotation (`×2|_{ℚ₃}`, exponent `0`) of the
`A`-stable leaf conditionals (`AIU_NEUTRAL_OBSTRUCTION_THEOREM.md` §2, §4). These are **genuinely different
attributes of the same leaf conditional** (a positive-dimension measure on a `ℚ₃`-leaf can be rotation-
invariant or not, independently of being positive-dimensional). The claim "no entropy can be transported from
the radial axis to the neutral angular axis" is the content of the AIU neutral-direction theorem and is
[CONFIRMS-in-lit] sound (the neutral direction carries `0·γ=0` entropy for every `γ`). **This orthogonality
is, pleasingly, the same fact that forces the §1 caveat**: ENT = unstable-direction dimension is exactly the
kind of dimension that controls entropy, whereas AIU's neutral-direction structure is exactly the kind that
does not. Internally consistent. [CONFIRMS]

**[NEEDS-CAVEAT] terminology.** "Orthogonal" is informal (these are not orthogonal in an inner-product sense);
read as "logically independent attributes (radial dimension vs angular invariance) of the same conditional."
Fine as stated, but should not be over-read as a proof that ENT and AIU are *probabilistically* independent.

---

## 5. The cross-place identification, and is it honestly a reformulation? — **[NEEDS-CAVEAT] / [CONFIRMS]**

**[NEEDS-CAVEAT] The "ENT ⟺ `ℚ₃`-conditionals positive-dimensional" step is under-justified (though true).**
`ENT_PRESSURE_LY.md` §1 and the `AIU` corollary write: "Equivalently (via `h_μ(A)=h_μ(A^{-1})`) the
`A`-stable `ℚ₃`-leaf conditionals are positive-dimensional." But `h_μ(A)=h_μ(A^{-1})` **alone** gives only
the single linear relation `log3·γ_3 = log(3/2)·γ_∞ + log2·γ_2`. From this, `γ_∞>0 ⟹ γ_3>0` (forward), but
the **reverse** `γ_3>0 ⟹ γ_∞>0` does **not** follow (`γ_3>0` could be carried by `γ_2` alone). So the
stated one-line reason is **insufficient** for the biconditional.
*The conclusion is nevertheless correct* via a fuller argument the doc omits: applying time-symmetry to the
generators separately — `h_μ(M₂)=h_μ(M₂^{-1})⟹γ_∞=γ_2` and `h_μ(M₃)=h_μ(M₃^{-1})⟹γ_∞=γ_3` (each generator
has a single expanding place) — together with the **product structure** of leafwise measures (E–L), forces
`γ_∞=γ_2=γ_3=:γ`. Then all the cross-place equivalences are exact. **Recommendation:** state the equality of
the three conditional dimensions (with product structure as the cited input), rather than leaning on
`h_μ(A)=h_μ(A^{-1})`, which is too weak by itself.

**[NEEDS-CAVEAT] Numerics measure a marginal, not a conditional.** `ENT_PRESSURE_LY.md` §4 estimates
`γ̂≈1.00` from the Shannon entropy of `c_n mod 2^k` — the **2-adic marginal** of `μ`. The L–Y `γ` is a
**conditional** (leafwise) dimension; marginal dimension only upper-bounds the relevant content and `γ̂≈1`
from a marginal certifies nothing about the conditional. The doc does flag "equidistribution evidence, NOT a
proof," but the object measured should be labelled a **marginal proxy**, not `γ_∞^{(2)}` itself.

**[NEEDS-CAVEAT, minor] "positive-dimensional (non-atomic)."** §1 parenthetically equates these. In general
positive-dimensional ⟹ non-atomic but **not** conversely. *In this specific homogeneous setting they happen
to coincide* (both ⟺ `h_μ(M₂)>0`, via the entropy⟺non-atomic-conditional equivalence), so the parenthetical
is harmless here — but it is not a general identity and §3 of the same doc (correctly) treats non-atomicity
as strictly weaker. Keep the two notions distinct in the theorem statement.

**[CONFIRMS] Honest reformulation, not progress.** The reduction converts ENT into "`γ>0` for the quenched
single-orbit limit measure," and **`γ>0` stays exactly (K)-hard**: no proven structure lower-bounds `γ`
(`ENT_PRESSURE_LY.md` §3 — every proven input controls an unweighted/support/**annealed** quantity, rate
`≥0`); pressure gives the wrong-direction (upper) bound; large-deviation/Gibbs–Markov give positivity only
for Haar/SRB-typical points, never the Haar-null seed; Hochman/Varjú give `dim ν_{2/3}=1` only **annealed**
and at the **wrong place** (`ENT_HOCHMAN_DIMENSION.md`). The docs are emphatic and correct that this is a
*sharper restatement* of ENT, not a step toward proving it. [CONFIRMS]

---

## 6. Precise correct form (recommended statement)

> **ENT–L–Y reduction (corrected/caveated).** Let `μ` be an `A`-invariant ergodic probability measure on the
> `(2,3)`-solenoid. The Ledrappier–Young *dimension* formula (an **equality**, via E–L leafwise/coarse-
> Lyapunov entropy theory for solenoid automorphisms; arXiv:2101.11120) gives `h_μ(M₂)=log2·γ`, where `γ` is
> the **conditional dimension of `μ` along the `M₂`-EXPANDING (unstable) leaf** (`= γ_∞ = γ_2` by inversion
> symmetry; `= γ_3` by product structure + generator time-symmetry). Since `log2>0`,
>
> **ENT (`h_μ(M₂)>0`) ⟺ `γ>0`** — a genuine two-sided equivalence (NOT merely `ENT⟹γ>0`).
>
> The equivalence is the L–Y **equality** (reinforced by "positive entropy ⟺ non-atomic unstable
> conditional"), **not** the Margulis–Ruelle inequality, and holds for non-SRB `μ`. It requires that `γ` be
> the **unstable**-leaf conditional dimension (for stable/neutral or total dimension the reverse implication
> fails). The exact numeric `γ=h/log2` additionally uses exact-dimensionality [PROVEN-in-lit, with
> hypotheses]. ENT is **orthogonal** (logically independent) to AIU: AIU is invariance along the
> **neutral** `ℚ₃` angular direction, which carries `0·γ=0` entropy for every `γ`. Reducing ENT to `γ>0`
> for the **quenched** single-orbit limit measure is an honest **reformulation**; `γ>0` remains **(K)-hard**.

---

## 7. Sources

- F. Ledrappier, L.-S. Young, *The metric entropy of diffeomorphisms* I/II, Ann. of Math. **122** (1985) —
  L–Y **dimension equality** `h=Σ_i λ_i(δ_i−δ_{i−1})`, distinct from Margulis–Ruelle. [PROVEN-in-lit]
- D. Ruelle, *An inequality for the entropy of differentiable maps*, Bol. Soc. Bras. Mat. **9** (1978) —
  Margulis–Ruelle **upper** bound; Pesin equality iff SRB. [PROVEN-in-lit]
  https://arxiv.org/abs/2606.13384 , https://arxiv.org/abs/2509.16981 (modern C¹/dominated-splitting L–Y,
  confirming the equality character and the multiplicity-one transverse-dimension reading).
- M. Einsiedler, E. Lindenstrauss, *Rigidity properties for commuting automorphisms on tori and solenoids*,
  arXiv:2101.11120 — leafwise measures, **entropy contribution / coarse-Lyapunov / product structure** on
  **solenoids** (the apparatus that legitimizes "adelic L–Y"). [PROVEN-in-lit]
  https://arxiv.org/pdf/2101.11120
- M. Einsiedler, E. Lindenstrauss, *Diagonal actions on locally homogeneous spaces* (Pisa) — leafwise
  measures, product structure §8, entropy=contribution. [PROVEN-in-lit]
- Lindenstrauss-school equivalence "positive entropy ⟺ non-atomic unstable conditional ⟺ positive Hausdorff
  dimension of the unstable conditional" for hyperbolic toral/solenoidal automorphisms (search: *Entropy and
  ergodic measures for toral automorphisms*, arXiv:1103.1115; EKL, Ann. Math. 164 (2006)).
- Bárány–Käenmäki / Feng / Hochman–Solomyak — **exact-dimensionality** and L–Y for self-affine measures
  (the hypothesis-laden input behind "exact-dimensional"). https://arxiv.org/abs/1503.00892 ;
  https://www.sciencedirect.com/science/article/pii/S0001870817301962
- Lind–Schmidt–Ward / Yuzvinskii — solenoid automorphism entropy `h(M_u)=Σ_v log⁺|u|_v`. [PROVEN-in-lit]
- Repo: `ENT_PRESSURE_LY.md` (L–Y reduction; annealed≠quenched; (K)-hardness), `ENT_PESIN_MARGULIS.md`
  (MR is upper-bound only; "(LY) is an identity, not a bound"; frozen exponents),
  `ENT_HOCHMAN_DIMENSION.md` (annealed-only, place mismatch G1/G2),
  `AIU_NEUTRAL_OBSTRUCTION_THEOREM.md` (neutral-direction orthogonality), `NEWMATH_ADELIC_RIGIDITY.md`.

---

No machine decided. No label upgraded.
