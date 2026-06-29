# ENT via Margulis–Ruelle / Pesin entropy–Lyapunov inequalities across places (2026-06-30)

*WEAPONS_AUDIT style. NEW angle: attack `ENT` (= `h_μ(M₂)>0`, positive 2-adic measure entropy of the
empirical limit measure `μ` of the single `⟨3/2⟩`-orbit `c₀=8, c_{n+1}=⌊3c_n/2⌋` on the `(2,3)`-solenoid
`X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`) using the Margulis–Ruelle inequality (`h_μ ≤ Σ` positive Lyapunov exponents) and
Pesin's formula (equality for SRB), with the PROVEN, explicit, measure-independent Lyapunov exponents
`λ_∞=log(3/2)`, `λ_2=log2`, `λ_3=−log3`, and the PROVEN positive archimedean expansion. SOUNDNESS
PARAMOUNT: every claim labelled; (K) NOT claimed; TOPOLOGICAL vs MEASURE entropy kept distinct; no label
upgraded. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/ent_pesin_margulis.py`
(exact big-int, N≤10⁵, <5s). NOT committed.*

---

## 0. One-line verdict

**Verdict (c): the route REDUCES TO (K).** Margulis–Ruelle is an **upper** bound on `h_μ` (it cannot
lower-bound it); Pesin **equality** holds iff `μ` is SRB = absolutely continuous unstable conditionals =
Haar = (K). The decisive new soundness point specific to THIS system: the Lyapunov exponents are **frozen
structural constants** (derivative of the affine automorphism `A`, the same for *every* invariant measure,
atomic or not), so they carry **zero** entropy information by themselves. The PROVEN positive archimedean
expansion is a property of the map `A`, **not** of `μ`, and therefore does **NOT** force positive entropy
in any place: an atomic measure on a periodic `A`-orbit has the **identical** positive `λ_∞=log(3/2)` and
`λ_2=log2` yet `h_μ=0` and is 2-adically atomic. The measure **can** expand archimedean (automatically)
while being 2-adically atomic (entropy 0). The adelic multi-place structure adds only the
measure-preservation balance `Σ_v λ_v = log(3/2)+log2−log3 = 0` (the product formula = `det A` adelically
`=1`), which constrains nothing about a *specific* `μ`'s entropy. Pesin/Margulis–Ruelle here degenerate to
the Yuzvinskii/Lind–Schmidt–Ward fact "`h_μ(A) ≤ log3` for all `μ`, equality iff Haar" — the upper-bound /
variational direction already audited in `ENT_PRESSURE_LY.md`. No new lower bound. No machine decided. No
label upgraded.

---

## 1. Setup: Margulis–Ruelle and Pesin for the affine solenoid automorphism `A` [PROVEN-in-lit]

`A=×(3/2)=M₃M₂^{-1}` is an **affine automorphism** of the compact abelian solenoid `X`. Its derivative
`DA` is the **constant** linear map `×(3/2)` acting place-wise on the tangent `ℝ⊕ℚ₂⊕ℚ₃`; the Lyapunov
exponents are the logs of the place-wise dilations and are **explicit, measure-independent, PROVEN**:

| place `v` | dilation `|3/2|_v` | exponent `λ_v` | role |
|---|---|---|---|
| `∞` (ℝ) | `3/2` | `λ_∞=log(3/2)≈0.405` | **expanding** |
| `2` (ℚ₂) | `2` | `λ_2=log2≈0.693` | **expanding** |
| `3` (ℚ₃) | `1/3` | `λ_3=−log3≈−1.099` | contracting |

`Σ_v λ_v = log(3/2)+log2−log3 = 0` [PROVEN — product formula; `A` is Haar-measure-preserving, the adelic
`det A = ∏_v|3/2|_v = 1`]. The **unstable** (expanding) leaf is `ℝ×ℚ₂`; the **stable** leaf is `ℚ₃`.

**Margulis–Ruelle inequality** (Ruelle 1978; algebraic/non-uniformly-hyperbolic form valid on the
solenoid): for ANY `A`-invariant Borel probability `μ`,
```
   h_μ(A) ≤ Σ_v λ_v⁺  =  λ_∞ + λ_2  =  log(3/2)+log2  =  log3 .          (MR)
```
**Ledrappier–Young refinement** (Ledrappier–Young 1985; leafwise/adelic form, Einsiedler–Lindenstrauss):
with `γ_∞,γ_2∈[0,1]` the partial (transverse) dimensions of `μ` along the `ℝ`- and `ℚ₂`-unstable
sub-leaves,
```
   h_μ(A) = λ_∞·γ_∞ + λ_2·γ_2  =  log(3/2)·γ_∞ + log2·γ_2 .              (LY)
```
**Pesin's formula** (equality case of MR): `h_μ(A)=log3` **iff** `μ` is an **SRB measure**, i.e. the
conditional measures of `μ` on the unstable `(ℝ×ℚ₂)`-leaves are **absolutely continuous** (`γ_∞=γ_2=1`,
densities = Lebesgue×Haar). On this homogeneous solenoid the only such `μ` is **Haar `m_X`**. [PROVEN-in-lit]

> **Direction of the inequalities — the load-bearing fact.** MR bounds `h_μ` from **ABOVE**. Pesin gives a
> **lower** bound on `h_μ` ONLY as the equality case, and ONLY under the SRB hypothesis (absolute
> continuity of unstable conditionals). There is **no** version of MR/Pesin that lower-bounds `h_μ` from
> the mere positivity of `λ_∞` or `λ_2`. [PROVEN-in-lit]

---

## 2. THE key question: does PROVEN positive archimedean expansion FORCE positive entropy? — NO [PROVEN]

The prompt's central ask. The honest, decisive answer is **no**, and the reason is structural and sharp.

### 2.1 The exponents are frozen constants, not measure-generated [PROVEN]
In the generic (smooth, non-uniformly-hyperbolic) Pesin setting the Lyapunov exponents are *produced by the
measure* (Oseledets averages of a non-constant cocycle `Df`), and their positivity is a substantive
measure-dependent fact. **Here `Df ≡ ×(3/2)` is constant**, so

> **every `A`-invariant measure `μ` has the SAME exponents** `(λ_∞,λ_2,λ_3)=(log\tfrac32,\,log2,\,−log3)`,
> regardless of whether `μ` is Haar, atomic, fractal, or supported on a single periodic orbit. [PROVEN]

Hence "positive archimedean Lyapunov exponent `λ_∞=log(3/2)>0`" is a statement about the **map `A`**, true
**vacuously for all `μ`**, and carries **no** information distinguishing positive-entropy `μ` from
zero-entropy `μ`. It cannot force `h_μ>0`.

### 2.2 Explicit counterexample: a measure that expands archimedean but is 2-adically atomic, `h_μ=0` [PROVEN]
`A` has **periodic points** on `X`: `A^n x = x` ⟺ `((3/2)^n−1)x∈Γ=ℤ[1/6]`, which has rational solutions
`x∈X` for every `n` (e.g. `x` with `(3^n−2^n)x∈2^nℤ[1/6]`). The atomic measure `μ_{per}` equidistributed
on such a periodic `A`-orbit is `A`-invariant with:
- `h_{μ_per}(A)=0` and `h_{μ_per}(M₂)=0` (atomic ⇒ zero entropy), `γ_∞=γ_2=0`;
- the **identical** positive exponents `λ_∞=log(3/2)>0`, `λ_2=log2>0` (frozen, §2.1);
- conditionals that are **atomic** in every place, in particular **2-adically atomic**.

> **Therefore: positive archimedean (and 2-adic) expansion is fully compatible with a 2-adically ATOMIC,
> zero-entropy invariant measure.** Expansion does NOT force positive-dimensional conditionals; the measure
> CAN be 2-adically atomic while the map expands at `∞` and `2`. [PROVEN] This kills the hoped-for
> "expansion ⟹ `γ>0`" implication outright.

### 2.3 Why the orbit's "growth" does not rescue it [PROVEN distinction]
The orbit *integers* `c_n` grow like `(3/2)^{ΣD}` archimedean — but that is the growth of the **renewal
cocycle / the `Γ=ℤ[1/6]`-unwinding**, NOT expansion of the measure on the **compact** solenoid `X` (the
`ℝ`-coordinate lives mod `Γ`). The archimedean drift `D·log(3/2)>0` (`REPELLER_ESCAPE.md`) is the
PROVEN positive *cocycle* drift; on `X` it is exactly cancelled by the `Γ`-translations that keep `x_n∈X`
compact. So "the orbit grows" is a statement about the lift, and supplies **no** lower bound on `γ_∞,γ_2`,
which are properties of the limit measure on the compact quotient. (This is the same lift-vs-quotient
distinction that makes the archimedean place a *transported* copy of the 2-adic information, `T2` of
`NEWMATH_ADELIC_RIGIDITY.md` §3.3.) [PROVEN]

---

## 3. Does the MULTI-PLACE / adelic structure give what single-place Pesin cannot? — NO [PROVEN]

The prompt asks whether the *product* of expansions across places, or the exact dual-repulsion rates, yield
an adelic entropy–Lyapunov balance forcing positivity. Audited route by route:

| multi-place input | what it would need to give | what it gives | obstruction |
|---|---|---|---|
| **Adelic balance `Σ_v λ_v=0`** | a lower bound on `h_μ` from the positive part `log3` | only "`A` preserves Haar" (`det_𝔸 A=1`); equivalently the negative exponent equals the positive (`λ_3=−(λ_∞+λ_2)`) | A **measure-preservation** identity, satisfied by every `A`-invariant `μ` including atomic ones. It pins `h(A)=h(A^{-1})` (sum of positive = |sum of negative|) but **never** a specific `μ`'s value. [PROVEN] |
| **Two expanding places (`∞` and `2`)** | MR in each place separately, hoping a per-place Pesin lower-bounds one of `γ_∞,γ_2` | `h_μ(A)=log(3/2)γ_∞+log2γ_2`; `h_μ(M₂)=log2·γ_∞^{(2)}` (LY) | LY is an **identity**, not a bound; MR caps the sum at `log3`. There is no per-place LOWER bound; `γ_∞,γ_2` can both be `0` (§2.2). [PROVEN] |
| **Dual-repulsion exact rates** (`|o−1|_∞×3/2`, `|o−1|_2×2` per `D=1` step; `REPELLER_ESCAPE.md`) | a forced positive-dimension via simultaneous escape in both places | a PROVEN per-step, per-point identity (orbit escapes `o=1` adelically by `×3`) | The adelic height telescopes to the **trivial `ΣD` identity** (`REPELLER_ESCAPE.md` §3, degeneracy theorem); the two valuations are NOT independent constraints. Pointwise escape ≠ measure-level dimension. [PROVEN] |
| **Pesin equality across places (SRB)** | `h_μ(A)=log3` ⟹ `γ=1` ⟹ Haar | exactly Haar, IF SRB | **SRB = absolutely continuous unstable conditionals = Haar = (K).** Assuming the hypothesis IS assuming (K). [PROVEN-in-lit] |

> **Net.** The adelic/multi-place structure contributes exactly one new scalar — the balance `Σλ_v=0` — and
> that scalar is measure-preservation, not an entropy lower bound. A genuine adelic *Pesin equality* (the
> only thing that lower-bounds `h_μ`) requires SRB in the unstable `(ℝ×ℚ₂)`-foliation, i.e. absolute
> continuity = Haar = (K). The multi-place picture gives **nothing a single-place Pesin does not**; both
> reduce to SRB. [PROVEN]

---

## 4. Honest verdict

| disposition | status |
|---|---|
| **(a)** ENT or a partial of it PROVEN via MR/Pesin | **NO** — MR is upper-bound only; it cannot lower-bound `h_μ(M₂)` |
| **(b)** new characterization of ENT | **PARTIAL/known** — LY (= §1) already characterizes ENT as `γ_∞^{(2)}>0` (`ENT_PRESSURE_LY.md`); MR/Pesin add only the *upper* cap `h_μ(A)≤log3` and the SRB-equality criterion. The genuinely new, sound contribution here is the **rigidity-of-exponents observation** (§2.1–2.2): the exponents are frozen, so expansion is measure-blind and an atomic 2-adic counterexample exists. |
| **(c)** reduces to (K) = SRB = Haar | **YES — this is the verdict.** Lower-bounding `h_μ` via Pesin needs SRB = absolutely continuous unstable conditionals = Haar = (K). Margulis–Ruelle only upper-bounds. |

**The gap, stated precisely.** Pesin/Margulis–Ruelle relate entropy to expansion only when the expansion is
**measure-generated**. On the affine solenoid the expansion is a **frozen constant of the map**, so the
inequality degenerates to a measure-independent upper bound `h_μ(A)≤log3` (Yuzvinskii/Lind–Schmidt–Ward +
variational principle), with the lower (Pesin-equality) direction available **only** under SRB = Haar = (K).
Positive archimedean expansion is automatic and measure-blind; it neither forces positive-dimensional
conditionals nor rules out a 2-adically atomic, zero-entropy invariant measure. ENT stays **[OPEN /
(K)-hard]**; (K) stays **[OPEN]** = Mahler 3/2 / AEV Conj 1.6 at `α=8`.

---

## 5. Numerics — `h_μ(A)` SATURATES the Margulis–Ruelle cap `log3` (SRB-like), but only as undersampled equidistribution evidence [OBSERVED]

`scratchpad/ent_pesin_margulis.py` (exact big-int, `c₀=8`, `c_{n+1}=⌊3c_n/2⌋`, `N≤10⁵`):

```
 archimedean rate (1/N)log(c_N/c0) = 0.40546   (λ_∞=log(3/2)=0.40547)   ← matches frozen exponent
 k   distinct   2^k     H_k(bits)  h_k     fill     pred 1-e^{-N/2^k}
 8       256       256    7.9981   0.9991   1.0000   1.0000
12      4096      4096   11.9700   0.9850   1.0000   1.0000
14     16356     16384   13.8756   0.9365   0.9983   0.9978   ← rolloff = undersampling
16     51205     65536   15.4499   0.7114   0.7813   0.7826
18     83067    262144   16.2544   0.3046   0.3169   0.3171   (≤0.2% from uniform-sampling)
 γ̂_2 (H_k/k at last full level) ≈ 0.9975
 MR cap log3 = 1.0986 ;  ĥ_μ(A)=log(3/2)·1+log2·γ̂_2 = 1.0969 ;  saturation ratio = 0.9984
```

- **Archimedean expansion rate** `(1/N)log(c_N/c_0) → log(3/2)` confirmed (PROVEN per-step; it is `meanD`-independent because each ⟨3/2⟩-step multiplies by ≈3/2). This is the frozen `λ_∞` — measured, but measure-blind (§2.1).
- **2-adic per-bit entropy** `H_k/k ≈ 1 = log2/log2` through every fully-resolved level ⟹ `γ̂_2≈1`, `ĥ_μ(M₂)≈log2` (`ENT` would hold). Deep-`k` rolloff = pure undersampling `1−e^{−N/2^k}` (≤0.2%).
- **MR saturation:** the empirical `ĥ_μ(A) = log(3/2)·γ̂_∞ + log2·γ̂_2 ≈ log3` (the cap), i.e. the empirical measure looks **SRB / Haar** (`γ̂_∞≈γ̂_2≈1`). **But this is exactly the equidistribution evidence already in hand**, read on the Lyapunov axis: it confirms `μ≈`Haar where the sample resolves, it does NOT certify the `k→∞`/`N→∞` limit — and certifying that limit (SRB saturation of MR) **is** (K). The numerics cannot distinguish "true SRB" from "atomic-with-huge-undersampled-period."

---

## Sources
- Ruelle, *An inequality for the entropy of differentiable maps*, Bol. Soc. Bras. Mat. **9** (1978) — the
  Margulis–Ruelle UPPER bound `h_μ ≤ Σλ_i⁺`. [PROVEN-in-lit]
- Pesin, *Characteristic Lyapunov exponents and smooth ergodic theory*, Russ. Math. Surv. **32** (1977);
  Ledrappier–Young, Ann. Math. **122** (1985) — Pesin equality (SRB) and `h=Σλ_iγ_i`. [PROVEN-in-lit]
- Lind–Schmidt–Ward / Yuzvinskii — solenoid automorphism entropy `h(×u)=Σ_v log⁺|u|_v` (= MR cap = `log3`).
  [PROVEN-in-lit]
- Einsiedler–Lindenstrauss, leafwise measures / adelic Ledrappier–Young; arXiv:2101.11120 (solenoid RJ).
  [PROVEN-in-lit]
- Repo: `ENT_PRESSURE_LY.md` (LY reduction ENT⟺`γ>0`; pressure upper bound; annealed≠quenched),
  `LIMIT_MEASURE_ENTROPY.md` (ENT necessary & (K)-hard; topological≠measure), `REPELLER_ESCAPE.md`
  (dual-repulsion rates; adelic-height degeneracy theorem), `NEWMATH_ADELIC_RIGIDITY.md` (AIU; T1–T2
  pointwise-vs-measure; SRB=Haar=(K)).
- Numerics: `scratchpad/ent_pesin_margulis.py`.

No machine decided. No label upgraded.
