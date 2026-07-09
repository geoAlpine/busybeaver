# The Limits of Measure Rigidity for the (2,3)-Solenoid Host

### A consolidated, whole-host no-go: the three standard measure-rigidity mechanisms — high-entropy propagation (EKL), entropy-as-dimension (Ledrappier–Young), and cross-scale operator-norm contraction (renormalization cocycle) — each provably fails to decide ANY lattice element of the rank-2 (2,3)-host, uniformly over the host. Independent of (K). A standalone limits-of-rigidity theorem.

*Self-contained formal note consolidating three previously red-teamed partials
(`AIU_NEUTRAL_OBSTRUCTION_THEOREM.md` + `AIU_THEOREM_REDTEAM.md`,
`ENT_LY_COLLAPSE_THEOREM.md` + `ENT_LY_REDTEAM.md`, `EUE_COISOMETRY_NOGO_THEOREM.md`) into ONE
statement on the LIMITS of measure rigidity for the whole {2,3}-smooth cryptid family, using yesterday's
whole-host extension (`NEWMATH_SOLENOID_BUILD_2026-07-09.md`, `PAPER_MIRROR_LADDER.md`).*

*SOUNDNESS CRITICAL. These are the program's most red-teamed results; every assertion is labelled
`[PROVEN]` (proved here from proven/standard inputs), `[PROVEN-in-lit]` (a theorem of the literature,
cited), or `[OBSERVED]` (numerical). This note proves the **inapplicability of three specific existing
methods** to the whole host. It does **NOT** prove any cryptid halts or does not halt, does **NOT** prove
(K), and does **NOT** assert that no future method can succeed. Numerics:
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/rigidity_limits_verify.py` (exact big-int /
machine precision). NOT committed.*

---

## 0. One-paragraph statement

Every {2,3}-smooth Type-I cryptid — Antihydra ×(3/2), o4 ×(4/3), o15/o18 ×(8/3), the powers ×(3/2)ᵏ — is
the single-orbit renewal of one lattice element `Φ(a,b) = ×(2ᵃ3ᵇ)` of a **single rank-2 host** `Φ : ℤ² →
Aut(X)` acting on **one** (2,3)-solenoid `X = (ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` `[PROVEN, §1]`. Deciding a cryptid reduces
to upgrading the rank-1 (`g`-)invariant empirical limit `μ_g` to Haar. This note assembles three
independently red-teamed no-gos into one whole-host statement: **for every host element `Φ(a,b)`, each of
the three standard rigidity mechanisms is silent, for a mechanism-specific proven reason that is uniform
across the host** — (A) the EKL high-entropy method is *neutral-blind* (the Haar-completion surplus lives on
a zero-Lyapunov coarse direction of a transverse generator); (B) entropy collapses to a single *conditional
dimension* `γ` that the method can restate but not lower-bound; (C) the cross-scale renormalization cocycle
is a *coisometry chain* with zero operator-norm Lyapunov exponent, so no uniform contraction exists. The
places {2,3} merely swap roles as `(a,b)` moves. This is a limits-of-rigidity theorem, **independent of
(K)**; it upgrades no label.

---

## 1. The shared host and its place decomposition `[PROVEN]`

### 1.1 One solenoid, one rank-2 host
`S = {∞,2,3}`, `G = ℝ×ℚ₂×ℚ₃`, `Γ = ℤ[1/6]` embedded diagonally; by the product formula `Γ` is a discrete
cocompact lattice and `X = G/Γ` is the compact abelian (2,3)-solenoid with Haar `m_X` `[standard]`. Each
{2,3}-unit `u ∈ ℤ[1/6]ˣ` gives an affine automorphism `M_u` with constant derivative (place-wise dilations
`(|u|_∞,|u|_2,|u|_3)`), so all Lyapunov exponents are **frozen structural constants = logs of the dilations,
measure-independent** `[PROVEN]`.

> **Host.** `Φ(a,b) = M_{2ᵃ3ᵇ} = ⟨×2, ×3⟩`, rank 2, abelian, hyperbolic. `[PROVEN]`
> **Membership `[PROVEN — product formula, `rigidity_limits_verify.py` F0].`** Antihydra `= Φ(-1,1)` (×3/2),
> o4 `= Φ(2,-1)` (×4/3), o15/o18 `= Φ(3,-1)` (×8/3), A² `= Φ(-2,2)`. (Space Needle ×5/2 is **not**
> {2,3}-smooth → lives on the disjoint (2,3,5)-solenoid; **it is outside the scope of this theorem**.)

### 1.2 Coarse-Lyapunov (place) decomposition and the two-way symmetry
`X` foliates into place-leaves `F_∞ (≅ℝ)`, `F_2 (≅ℚ₂)`, `F_3 (≅ℚ₃)`, the three **coarse-Lyapunov subgroups**,
carrying the non-proportional functionals `χ_∞(a,b) = a log2 + b log3`, `χ_2(a,b) = −a log2`,
`χ_3(a,b) = −b log3` `[PROVEN]`. The single fact the whole note turns on is the pair of **neutralities of the
generators**, exact 3-adic / 2-adic unit facts `[PROVEN]`:

> `M₂ = ×2` is an **isometry on ℚ₃**: `|2|_3 = 1`, `χ_3(1,0) = 0`.
> `M₃ = ×3` is an **isometry on ℚ₂**: `|3|_2 = 1`, `χ_2(0,1) = 0`.

The deformation `Φ(2,-1) ↝ Φ(-1,1)` (o4 → Antihydra) **interchanges the roles of the two finite places**
(`NEWMATH_SOLENOID_BUILD_2026-07-09.md` §2.1): the contracting finite place is ℚ₃ for Antihydra (`|3/2|_3 =
1/3`) and ℚ₂ for o4 (`|4/3|_2 = 1/4`); the expanding/depth finite place is the other one in each case. All
three no-gos below are therefore symmetric under 2↔3, which is the structural core of "whole host, not an
Antihydra artifact."

---

## 2. The strengthened AIU obstruction — whole host `[PROVEN, per element; uniform via §2.3]`

### 2.1 The Haar-completion surplus is a neutral coarse direction, for every element
Fix any host element `g = Φ(a,b)`. Its empirical limit `μ_g` is `g`-invariant (rank 1) by
Krylov–Bogolyubov `[PROVEN]`. Upgrading `μ_g` to Haar (Rudolph–Johnson) requires invariance under a
**second, transverse** host generator. Disintegrate `μ_g` along the `g`-stable (contracting finite) leaf
`F_π` (π = 3 for Antihydra, π = 2 for o4) into leafwise conditionals; the surplus invariance the completion
needs is invariance of those conditionals under the **transverse generator that is an isometry of `F_π`** —
namely `M₂ = ×2` on ℚ₃ (Antihydra) or `M₃ = ×3` on ℚ₂ (o4). That generator has **Lyapunov exponent 0** on
`F_π` (`|2|_3 = 1`, resp. `|3|_2 = 1`) `[PROVEN — §1.2; `rigidity_limits_verify.py` F1]`.

> **AIU surplus (leafwise form), whole host.** For every `Φ(a,b)`, the invariance that completes rigidity
> lives along a **zero-Lyapunov (neutral) coarse direction** of the transverse generator. `[PROVEN]`

### 2.2 The conjunction (A)∧(B) — both standard engines are silent, uniformly

> **Theorem A (high-entropy method is neutral-blind, whole host) `[PROVEN]`.** The EKL high-entropy /
> product-structure method generates invariance only along coarse-Lyapunov subgroups of **nonzero** weight
> (its sole engine, maximal-entropy-contribution, is keyed via Ledrappier–Young `h = Σᵢ λᵢγᵢ` to a nonzero
> Lyapunov prefactor: `0·γ = 0` on a neutral direction). The AIU surplus (§2.1) is neutral for **every**
> element. Hence the method produces the completion invariance for **no** host element. `[PROVEN]`

> **Theorem B (the central-direction engine also fails — non-recurrence, whole host) `[PROVEN inputs]`.** The
> dedicated zero-exponent rigidity engine — the Furstenberg–Ledrappier / Avila–Santamaria–Viana **Invariance
> Principle** and its homogeneous cousin the Anzai–Furstenberg–Veech **isometric-extension** theorem —
> requires a **recurrent (probability-preserving) base** over which to average the fibre rotation. For every
> `Φ(a,b)` the neutral rotation sits over the `g`-**contracting radial finite direction**, a base shift
> `v_π → v_π + s` (`s = v_π(u) > 0`: `s = 1` for Antihydra on ℚ₃, `s = 2` for o4 on ℚ₂) — a ℤ-translation
> with **no invariant probability**, dissipative, iterated **zero times per sphere**. The hypothesis is never
> met, for every element. `[PROVEN — `rigidity_limits_verify.py` F2]`

> **Mandatory caveat (binding, from `AIU_THEOREM_REDTEAM.md`).** Neutrality **alone** is *not* an obstruction
> — the Invariance Principle is a rigidity engine *for* neutral directions. The obstruction is the
> **conjunction (A)∧(B)**: a neutral direction (defeating the entropy method) **over a dissipative base**
> (defeating the central-direction method). A statement "neutral ⟹ no method" would be an over-claim. This
> says nothing about the truth value of AIU/halting; it identifies *why both standard tools are silent*.

### 2.3 Uniformity is deformation-invariant `[PROVEN]`
Both (A) and (B) depend only on (i) which generator is a finite-place isometry — a fixed 2↔3-symmetric fact
independent of `(a,b)` — and (ii) the sign of the contracting finite exponent — `χ_π(a,b) < 0`, a linear
condition satisfied on the whole subcritical region of the host. The exponents `χ_∞,χ_2,χ_3` are linear in
`(a,b)`; the neutralities are exact unit facts. So the obstruction (A)∧(B) is **invariant under the
deformation across the host**, not a coincidence at ×3/2 (`NEWMATH_SOLENOID_BUILD_2026-07-09.md` §2.2,
Obstruction II). This is the genuine strengthening: AIU-neutral-blindness upgraded from *one element* to the
*whole {2,3}-host, uniformly*. `[PROVEN]`

---

## 3. Entropy is exactly a conditional dimension — whole host `[PROVEN reduction; γ OPEN]`

By the affine Ledrappier–Young **dimension equality** on the solenoid (`h_μ = Σ_{v:λ_v>0} λ_v γ_v`, `γ_v ∈
[0,1]`, an equality — not the Margulis–Ruelle inequality — with frozen prefactors), instantiated at any
generator with a single expanding finite place:

> **ENT collapse, whole host `[PROVEN, `ENT_LY_COLLAPSE_THEOREM.md`; element-uniform per
> `NEWMATH_SOLENOID_BUILD` §4].`** For each element the positive-entropy condition on its expanding finite
> generator is `h_μ = log(prime)·γ`, a single positive prefactor times **one conditional dimension** `γ`
> along the unstable leaf. Hence **ENT ⟺ γ > 0** — a genuine two-sided equivalence. The neutral finite place
> contributes `0·γ = 0`.

Consequence for method-limits: entropy is not an independent lever. It is one dimension number, **orthogonal
(logically independent) to the AIU angular surplus on the same leaf** — the radial (scale) dimension `γ`
versus the angular (neutral-rotation) invariance are transverse coordinates of the one contracting leaf, and
the high-entropy method (keyed to nonzero weight) provably **cannot transport** `γ` from the radial axis to
the neutral angular axis `[PROVEN, `ENT_LY_COLLAPSE` §4]`. So even a *proof* of ENT (γ > 0) would not, by
this method, deliver AIU.

> **Caveat (binding, from `ENT_LY_REDTEAM.md`).** This is an **equivalence / reformulation**, not a lower
> bound: it identifies *which* number ENT equals and supplies none. `γ > 0` for the quenched single-orbit
> `μ_g` stays **(K)-hard**. `γ` must be read as the **unstable-leaf** conditional dimension (for total /
> stable dimension the reverse implication fails). The exact value `γ = h/log(prime)` additionally uses
> exact-dimensionality [PROVEN-in-lit, with hypotheses]; the equivalence itself is robust without it.

---

## 4. No uniform cross-scale contraction — whole host `[PROVEN]`

The third mechanism is spectral: control the orbit's Fourier data across `q`-adic scales by a contracting
cross-scale cocycle. For the depth place `q` of each element (`q = 2` for Antihydra, `q = 3` for o4), the
carry-renormalization operator `R_k` folds scale `k+1` into scale `k`. Its structural core is a **twisted
`q`-to-1 pullback**: the value map `V(t) = ⌊pt/q⌋ mod qᵏ` is exactly `q`-to-1 onto `ℤ/qᵏ`, and multiplication
by the unimodular fresh-digit twist preserves norm, so the pullback is an **isometry** `J` and its adjoint
cocycle `R_k = J*` is a **coisometry**:

> **Theorem C (coisometry ⟹ op-norm Lyapunov ≡ 0, whole host) `[PROVEN]`.** `R_k R_k* = I` for the base-`q`
> renormalization operator of each element's depth place. Every finite cross-scale product `Φ_{k,k+m} = R_k
> ⋯ R_{k+m-1}` has `‖Φ_{k,k+m}‖ = 1` for all `m` (a product of coisometries whose adjoint is an isometry, so
> the norm is saturated), hence the **operator-norm cross-scale Lyapunov exponent is identically 0**. No
> uniform / operator-norm / spectral contraction across scales exists; any EUE proof that controls the
> odd-character data by a cross-scale spectral gap is structurally impossible. `[PROVEN]`

Numerical confirmation for **both** bases (`rigidity_limits_verify.py` F3): `V` exactly `q`-to-1 onto;
`‖J^H J − qI‖ = 0` (exact); `‖R_k R_k* − I‖ ≤ 3.5e-15`; all singular values `= 1.0000`; `dim ker = (q−1)qᵏ`,
for `k = 2..6`, `q ∈ {2,3}`. The `q = 2` case reproduces the repo's established odd-block coisometry
(`EUE_COISOMETRY_NOGO_THEOREM.md`, verified there at `4.8e-15` on the exact seam operator); the `q = 3` case
confirms the same structure for o4 — **the op-norm no-go is not an Antihydra artifact**.

> **Caveat (binding, from `EUE_COISOMETRY_REDTEAM.md`).** "Op-norm Lyapunov = 0" rules out only the
> **uniform / top-exponent** contraction (Lyapunov is conjugation-invariant; interior weights cancel). A
> coisometry cocycle's Lyapunov spectrum is `{0, −∞}` — it *does* contract totally on its kernel. The
> surviving decay is a **directional (Oseledets / quenched) exponent along the specific orbit vector**, which
> is exactly (K); anisotropic-weighted-norm or subspace escapes collapse *into* that data-direction route,
> not past it. This is a no-go for the operator-norm family, not a proof EUE is false.

---

## 5. The combined meta-theorem — exactly what is ruled out, uniformly `[PROVEN, scoped]`

Deciding a cryptid = upgrading a rank-1 invariant single-orbit limit `μ_g` to Haar. There are three standard
mechanisms for such an upgrade; assemble the three no-gos:

| # | Mechanism (method class X) | Failure mode Y, uniform over the host | source |
|---|---|---|---|
| A | EKL high-entropy / product-structure propagation | surplus invariance is **neutral** (zero coarse weight); engine keyed to nonzero weight, `0·γ=0` | §2, AIU |
| B | Invariance-Principle / isometric-extension (central-direction) | neutral rotation over a **dissipative, non-recurrent** base; hypothesis never met | §2, AIU-B |
| C | cross-scale operator-norm / spectral contraction (renorm cocycle) | cocycle is a **coisometry chain**; op-norm Lyapunov ≡ 0, norm saturated | §4, EUE |
| — | (entropy as an independent lever) | ENT ⟺ **one conditional dimension** `γ`; orthogonal to A, non-transportable | §3, ENT |

> **Meta-theorem (limits of measure rigidity for the (2,3)-host) `[PROVEN, scoped]`.** Let `X` be the
> (2,3)-solenoid, `Φ = ⟨×2,×3⟩` its rank-2 host, and `μ_g` the empirical limit of any {2,3}-smooth cryptid
> `g = Φ(a,b)`. Then **no method in the class**
>
> > X = { EKL high-entropy propagation; Invariance-Principle / isometric-extension from zero exponents;
> > uniform operator-norm contraction of the cross-scale renormalization cocycle }
>
> **decides `g` by its native mechanism Y**, and this holds **uniformly for every element of the host** (the
> only variation is the 2↔3 role-swap of the finite places). Each failure is a proven structural fact:
> (A) neutrality, (B) non-recurrence, (C) coisometry / saturated norm; and entropy — the natural quantitative
> input — collapses (D) to a single conditional dimension `γ` that these methods can reformulate but not
> lower-bound. The three methods pin to **one geometric configuration**: the completion surplus sits on the
> unique direction that the iterated element neither expands, contracts-with-entropy, *nor recurs on*.
> `[PROVEN, scoped]`

Equivalently: the entire {2,3}-Type-I frontier is **one problem in |family| coordinates** — an effective
quenched bound on the frequency of deep `q`-adic returns of an explicit affine ×(p/q) orbit — and all three
standard rigidity attacks on it are simultaneously, structurally, and uniformly closed. The surviving channel
in every case is the same: a **data-direction / quenched (Oseledets)** exponent along the single orbit vector
= (K) = Mahler-3/2 / AEV Conjecture 1.6.

---

## 6. HONEST SCOPE — binding

1. **Inapplicability of existing methods, NOT undecidability.** The theorem proves three specific method
   classes cannot decide the host by their native mechanisms. It does **not** prove any cryptid halts or does
   not halt, and does **not** claim a *future* or non-listed method must fail. `[scope]`
2. **NOT (K).** (K) — Mahler-3/2 / AEV Conj 1.6 at α=8 — is downstream of ENT ∧ AIU ∧ seed-selection and
   remains **[OPEN]/(K)-hard**. This note is **independent of (K)** and touches none of it. The surviving
   data-direction route (§4 caveat) *is* (K); (CR)⟹(K) is itself a reduction, and the final "quenched ⟹ (K)"
   step is heuristic, not rigorous. `[scope]`
3. **Whole {2,3}-host only; Space Needle excluded.** The uniform statement covers exactly the {2,3}-smooth
   lattice elements `Φ(a,b)` on the one (2,3)-solenoid. Space Needle ×5/2 is not {2,3}-smooth (disjoint
   (2,3,5)-solenoid) and is outside scope. `[scope]`
4. **Method- and action-specific.** X is the three named classes as applied to `⟨×2,×3⟩` on the
   (2,3)-solenoid; this is not a claim about measure rigidity in general, nor about low-entropy /
   Ratner-unipotent / genuine-joinings / arithmetic-equidistribution / weighted-non-spectral methods (those
   fail here too, per the source notes, but for *separately-argued* reasons; the meta-theorem states only the
   three consolidated classes). `[scope]`
5. **What IS proven, exactly.** *Given* the leafwise reformulations (`[PROVEN equivalence]`) and the
   `[PROVEN-in-lit]` mechanism descriptions, it is `[PROVEN]` that (A) neutrality, (B) non-recurrence,
   (C) coisometry each returns nothing on the completion surplus, uniformly over the host, with the two
   finite places swapping under the deformation; and (D) ENT ⟺ γ>0. The novelty is the **consolidation into
   one whole-host limits-of-rigidity statement**, plus the two-element (×3/2 and ×4/3) numerical confirmation
   that the configuration is deformation-invariant, not an Antihydra coincidence. `[scope]`

---

## 7. Numerical confirmation (two elements)

`scratchpad/rigidity_limits_verify.py` (exact big-int / machine precision), both Antihydra ×3/2 = Φ(-1,1)
and o4 ×4/3 = Φ(2,-1):

- **F0 host membership:** both {2,3}-smooth units → one (2,3)-host. `[PROVEN]`
- **F1 neutral direction:** transverse generator has `|·|_π = 1` → Lyapunov `0.0000` on the contracting leaf
  (M₂ on ℚ₃ for Antihydra; M₃ on ℚ₂ for o4). `[PROVEN — exact unit fact]`
- **F2 dissipative base:** contracting-place valuation shift `+1` (Antihydra, ℚ₃) / `+2` (o4, ℚ₂), strictly
  increasing → no invariant probability, iterated 0×/sphere. `[PROVEN — exact]`
- **F3 coisometry:** `V` exactly `q`-to-1 onto; `‖J^HJ − qI‖ = 0`; `‖R_kR_k*−I‖ ≤ 3.5e-15`; all singular
  values `1.0000`; `dim ker = (q−1)qᵏ`; `k = 2..6`, `q ∈ {2,3}`. `[OBSERVED → structural PROVEN]`

All three load-bearing facts hold for both elements, with {2,3} interchanged — the whole-host claim is
confirmed non-artifactual.

---

## 8. Sources
- Consolidated repo partials: `AIU_NEUTRAL_OBSTRUCTION_THEOREM.md` + `AIU_THEOREM_REDTEAM.md` (conjunction
  (A)∧(B), neutral-over-dissipative); `ENT_LY_COLLAPSE_THEOREM.md` + `ENT_LY_REDTEAM.md` (ENT ⟺ γ>0,
  two-sided, orthogonal to AIU); `EUE_COISOMETRY_NOGO_THEOREM.md` (`R_kR_k*=I`, op-norm Lyapunov ≡ 0).
- Whole-host extension: `NEWMATH_SOLENOID_BUILD_2026-07-09.md` (§2 shared host, deformation-uniform neutral
  obstruction; §4 element-uniform ENT collapse); `PAPER_MIRROR_LADDER.md` (uniform run law, census, place
  roles).
- `[PROVEN-in-lit]`: Einsiedler–Katok–Lindenstrauss high-entropy method (Ann. of Math. 164 (2006); Pisa
  lectures §§6–9); Ledrappier–Young dimension equality (Ann. of Math. 122 (1985)); Lind–Ward / Lind–Schmidt–
  Ward / Deninger solenoid entropy `Σ_v log⁺|·|_v`; Einsiedler–Lindenstrauss commuting solenoid automorphisms
  (arXiv:2101.11120); Avila–Santamaria–Viana Invariance Principle (Astérisque 358, 2013); Anzai–Furstenberg–
  Veech isometric extension; Rudolph–Johnson ×2×3 rigidity; Oseledets MET; Andrieu–Eliahou–Vivion
  (arXiv:2510.11723, AEV Conj 1.6 = the (K) external anchor).
- Numerics: `scratchpad/rigidity_limits_verify.py` (F0–F3, both ×3/2 and ×4/3).

---

No machine decided. No label upgraded.
