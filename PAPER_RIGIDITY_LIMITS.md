# Limits of measure rigidity for single-orbit ×(p/q) systems on the (2,3)-solenoid

*Paper-style writeup of the campaign's (K)-independent partial results — a standalone theorem on the LIMITS of the
existing measure-rigidity toolkit for the busy-beaver cryptid family, provable now and not contingent on any open
conjecture. Discovery/red-team notes: `AIU_NEUTRAL_OBSTRUCTION_THEOREM.md`, `ENT_LY_COLLAPSE_THEOREM.md`,
`EUE_COISOMETRY_NOGO_THEOREM.md`, `NEWMATH_SOLENOID_BUILD_2026-07-09.md`, `RIGIDITY_LIMITS_HOST_2026-07-09.md`.
Numerical verification: `rigidity_limits_verify.py`. This document proves inapplicability of named methods; it does
NOT prove undecidability, does NOT prove any (K)-type statement, and does NOT claim future methods must fail.*

## 1. Setting and the object of study

The {2,3}-smooth BB(6) cryptids — Antihydra (×3/2), o4 (×4/3), o11/o13/o14/o16 (×3/2 variants), o15/o18 (×8/3), o2
(ceiling ×3/2) — are each the single-orbit renewal of a **lattice element** `Φ(a,b) = ×(2^a 3^b)` of one rank-2 host
group `⟨×2, ×3⟩` acting on the S-arithmetic solenoid `X = (ℝ × ℚ₂ × ℚ₃)/ℤ[1/6]` (Antihydra = Φ(−1,1), o4 = Φ(2,−1),
o15/o18 = Φ(3,−1); `[PROVEN]` via the product formula, `NEWMATH_SOLENOID_BUILD`). Deciding such a machine is
equivalent to upgrading a rank-1-invariant single-orbit limit measure `μ_g` to Haar. This paper delimits which
standard rigidity methods can perform that upgrade.

## 2. The whole-host neutral-obstruction theorem `[PROVEN]`

**Theorem A (deformation-uniform neutral obstruction).** *For every lattice element `Φ(a,b)` of the (2,3)-host, the
Haar-completion surplus invariance the machine needs lives on a **zero-Lyapunov (neutral) coarse direction** of a
transverse host generator, sitting over a **dissipative, non-recurrent** contracting radial base. Consequently the
conjunction*
> (A) the Einsiedler–Lindenstrauss high-entropy / product-structure method is neutral-blind (leafwise-entropy
> contribution `0·γ = 0` by Ledrappier–Young), AND
> (B) the central-direction engine (Furstenberg–Ledrappier / Avila–Santamaria–Viana Invariance Principle;
> Anzai–Furstenberg–Veech isometric extension) is defeated by non-recurrence (the skew base is A-contracting, no
> invariant probability, the neutral rotation iterated 0× per sphere)

*holds **uniformly over the entire host** — it depends only on the 2↔3-symmetric unit facts (`|2|₃ = |3|₂ = 1`) and
the sign of the contracting exponent, not on `(a,b)`.* (Extends the single-machine AIU partial to the whole host,
`NEWMATH_SOLENOID_BUILD`; red-team caveat kept verbatim: **neutrality alone is not the obstruction — the conjunction
(A)∧(B) is**.)

## 3. The entropy collapse `[PROVEN, two-sided]`

**Theorem B (Ledrappier–Young collapse).** *On the affine solenoid the L–Y prefactors are frozen constants, so
`h_μ(M₂) = log 2 · γ` with `γ` the conditional dimension on the M₂-unstable archimedean leaf; hence
`ENT ⟺ γ > 0` (a genuine two-sided equivalence — from the dimension EQUALITY, not the Margulis–Ruelle inequality,
`ENT_LY_REDTEAM` confirmed). Entropy — the natural quantitative lever the high-entropy method would use — is thus a
single conditional dimension `γ` that the method can reformulate but cannot lower-bound, and that is orthogonal to
(logically independent of) AIU's neutral angular direction.* (Ladder: `{avoid periodic} ⊊ {non-atomic} ⊊ ENT (=γ>0)
⊊ (K)`.)

## 4. The cross-scale coisometry no-go `[PROVEN]`

**Theorem C (op-norm Lyapunov ≡ 0).** *The cross-scale carry-renormalization cocycle `Φ` is a chain of coisometries
`R_k = (M_{r_k} T_k)*` (`R_k R_k* = I`, `R_k* R_k ≠ I`, `dim ker = (q−1)q^{k−1}`); its operator-norm cross-scale
Lyapunov exponent ≡ 0. Verified in closed form and numerically for `q = 2` AND `q = 3`, `k = 2..6`
(`‖R_k R_k* − I‖ ≤ 3.5×10⁻¹⁵`, all singular values 1) — the twisted `q`-to-1 pullback is an isometry, so its adjoint
is a coisometry, a base-agnostic structural fact. Hence no uniform operator-norm / top-exponent contraction in any
fixed or telescoping norm survives across scales.* (Caveat verbatim: this rules out only the UNIFORM top-exponent
contraction; a coisometry's Lyapunov spectrum is `{0, −∞}` — directional Oseledets decay on the kernel is a
different, data-direction object.)

## 5. The combined meta-theorem `[PROVEN]`

**Theorem (limits of rigidity for the {2,3}-host).** *No method in the class*
> **X** = { EKL high-entropy/product-structure propagation; Invariance-Principle / isometric-extension central-direction
> rigidity; uniform operator-norm contraction of the cross-scale renormalization cocycle }

*decides any lattice element of the (2,3)-host by its native mechanism, uniformly over the host:* (A) neutrality,
(B) non-recurrence, (C) coisometry op-norm 0; *and the natural quantitative lever, entropy, collapses (D) to one
conditional dimension `γ` that these methods cannot lower-bound. All three pin to one geometry — the surplus sits on
the unique direction the iterated element neither expands, contracts-with-entropy, nor recurs on. The single surviving
channel is the quenched Oseledets exponent along the data direction, i.e. `(K)` itself.*

## 6. Scope and significance `[honest]`

**Proves:** the inapplicability of three named, standard method-classes to the WHOLE {2,3}-host, uniformly, with
two-element numerical confirmation (×3/2 AND ×4/3, so not an Antihydra artifact). **Does NOT prove:** undecidability
of any machine; any (K)-type distribution statement; that some future/other method must fail. **Excludes:** Space
Needle (×5/2, non-{2,3}-smooth, on a different (2,3,5)-solenoid). This is a clean **limits-of-measure-rigidity**
result — a family of single-orbit systems where the surplus invariance sits, provably and uniformly, in a central
direction over a dissipative base beyond the reach of both standard rigidity engines and the cross-scale contraction.
It is publishable independently of the halting question, and it maps precisely which new ingredient any future
decision must supply: control of the quenched data-direction exponent (= effective single-orbit equidistribution),
the object of `NEW_MATH_PROGRAM`.

## References to the record
`AIU_NEUTRAL_OBSTRUCTION_THEOREM.md` + `AIU_THEOREM_REDTEAM.md`; `ENT_LY_COLLAPSE_THEOREM.md` + `ENT_LY_REDTEAM.md`;
`EUE_COISOMETRY_NOGO_THEOREM.md` + `EUE_COISOMETRY_REDTEAM.md`; whole-host extension + 2-element verification
`NEWMATH_SOLENOID_BUILD_2026-07-09.md` / `RIGIDITY_LIMITS_HOST_2026-07-09.md` (`rigidity_limits_verify.py`); host
placement `NEW_MATH_PROGRAM.md`, `BB6_FRAMEWORK_PACKAGE.md`. Home theory: Einsiedler–Lindenstrauss leafwise measures;
Ledrappier–Young 1985; Rudolph–Johnson; Avila–Santamaria–Viana.
