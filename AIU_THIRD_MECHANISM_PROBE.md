# AIU — probing for a THIRD mechanism (central/neutral-direction invariance over a dissipative base) (2026-06-30)

*One level deeper than the `(a)` Neutral-Direction Obstruction Theorem (`AIU_NEUTRAL_OBSTRUCTION_THEOREM.md`).
The `(a)` theorem proved BOTH standard rigidity engines stall — (A) the EKL high-entropy method is neutral-blind
(weight `log|2|₃=0`), (B) the central-direction Invariance Principle / Anzai–Furstenberg–Veech is defeated by a
dissipative base — but its **mandatory caveat** is that neutrality alone is not the obstruction, so a THIRD mechanism
is not ruled out. This note attacks that opening honestly: is there a third mechanism, and can the deterministic adelic
coupling `v₃(o')=D−1` be turned into a LEVER forcing ℚ₃-rotation-invariance?*

*SOUNDNESS PARAMOUNT. Every claim labelled `[PROVEN]` (here, from proven inputs), `[PROVEN-in-lit]`, `[OBSERVED]`,
`[HEURISTIC]`, `[CONJECTURE]`, `[OPEN]`. **No claim that AIU or (K) is proved. No label upgraded. Not committed.**
Numerics: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int, induced map `o↦3^{D−1}(3o−1)/2^D`,
`D=v₂(3o−1)`, seed `o₀=27`, `N=2·10⁵`. Cross-refs: `AIU_NEUTRAL_OBSTRUCTION_THEOREM.md`, `AIU_SKEW_ROTATION.md`,
`AIU_JOININGS.md`, `AIU_THREEADIC_FOURIER.md`, `BB6_FRAMEWORK_PACKAGE.md` §5/§5.5, `NEW_MATH_PROGRAM.md`.*

---

## §0. VERDICT

**No viable third mechanism, and no new crack. The third-mechanism attack produces (i) ONE new sharp partial
no-go — the coupling `v₃(o')=D−1` is, at the writable (orbit/pointwise) level, an ANTI-lever: it forces the
3-adic angular law to be the *non-Haar* push-forward of the D-law, and the self-consistency map built from it is
NOT a contraction (its core is an isometric rotation, which cannot push a measure toward Haar) — and (ii) a
literature scan confirming that every candidate third mechanism either fails a structural hypothesis here
(higher-rank acting group / non-elementary surface group / expanding-leaf spectral gap / mixing of a non-mixing
rotation) or — in the single closest case, Eskin–Lindenstrauss/Benoist–Quint stationary-measure rigidity —
delivers only the ANNEALED Haar (random i.i.d. D), reproducing the annealed→quenched wall, i.e. `(K)`.**

Classification: this is **a new partial no-go (b-type)**, not an opening and not merely the same wall — it
*sharpens* the `(a)` caveat by showing the most natural "third route" (the coupling-as-lever / self-consistency
fixed point) is not just inert (as unique ergodicity was in `(B)`) but actively points the orbit-level angular
law AWAY from Haar; and that the recurrence-free third mechanism (stationary measures) exists in the literature
but its randomness hypothesis is exactly the annealed/quenched gap. **Single most concrete new thing established:**
the `[PROVEN]` orbit-level radius↔angle lock

> **`unit(o') ≡ (−1)^{v₃(o')} (mod 3)`** — the 3-adic angle's leading residue equals the parity of its own radius,

a deterministic graph-coupling between the (dissipative) radial base and the (neutral) angular fiber that makes the
leading angular character sum equal to `freq(D odd)−freq(D even)` and hence pins it to `≈1/3` (non-zero) under the
conjectured geometric D-law. (Verified: 0 exceptions / `2·10⁵`.)

---

## §1. THE COUPLING FUNCTIONAL EQUATION — written explicitly, and why it is not a lever for Haar

### 1.1 Setup: the within-leaf skew action and the renewal update `[PROVEN]`

On the `A`-stable leaf `F₃ = ℚ₃`, in coordinates `ℚ₃* = 3^ℤ × ℤ₃*`, `y = 3^v u` (radius `v=v₃`, angle `u∈ℤ₃*`),
`A=×(3/2)` acts as the skew product `A(v,u)=(v+1, R₂⁻¹u)`, `R₂=×2` the neutral rotation (`|2|₃=1`), constant cocycle
(`AIU_SKEW_ROTATION.md` §1). AIU `⟺` the `F₃`-leaf conditionals `μ_x³` are `ℤ₃*`-rotation-invariant (spherically
Haar) (`AIU_JOININGS.md` §2). `[PROVEN equivalence]`

The actual recurrence is supplied by the renewal (induced) step, whose within-leaf law is `[PROVEN/OBSERVED, exact]`:
> `o' = 3^{D−1}·m`, `m = (3o−1)·2^{−D}`, `D = v₂(3o−1)`; so `v₃(o')=D−1` and `unit(o') = (3o−1)·2^{−D} ∈ ℤ₃*`.

Writing the current term `o = 3^{v} U` (`v=v₃(o)`, `U=u(o)∈ℤ₃*`), `3o−1 = −1 + 3^{v+1}U`, hence the **angular update**
> **(★)  `u' = (−1 + 3^{v+1}U)·2^{−D}` in `ℤ₃*`,  with `D = v₂(−1+3^{v+1}U)` supplied by the 2-adic coordinate.**

Two structural reads of (★), both `[PROVEN]`:
- it is **rotation by `2^{−D}`** (a power of the neutral `R₂`) **composed with the additive renewal `−1+3^{v+1}U`**;
- `D` is a **2-adic** functional, *not* a function of the 3-adic coordinates `(v,U)` — the exogenous coupling.

### 1.2 The functional equation on the angular law `[PROVEN identity]`

Push (★) onto characters. For `χ` a character of `ℤ₃*` and `ρ` the (orbit-empirical, pooled) angular law on `ℤ₃*`,
A-invariance + renewal give the **transfer / functional equation**
> **(FE)  `∫χ dρ = E_{(v,U)∼ρ̃,\,D}[ χ((−1+3^{v+1}U)·2^{−D}) ]`,**

where `ρ̃` is the joint radius–angle law and `D` is the (orbit's own) 2-adic depth. The **mod-3 instance** is exact and
closed-form. The unique nontrivial character mod 3 is `χ₀(1)=1, χ₀(2)=−1`; mod 3 the term `3^{v+1}U≡0`, so
`u' ≡ −2^{−D} ≡ (−1)^{D+1} (mod 3)` (since `2≡−1`), giving
> **(FE₀)  `∫χ₀ dρ = E[(−1)^{D+1}] = freq(D odd) − freq(D even)`.   `[PROVEN identity]`**

Combining `v₃(o')=D−1` (so `D=v₃(o')+1`) with the `[PROVEN]` lemma `unit(o')≡(−1)^{D+1} (mod 3)`
(`AIU_THREEADIC_FOURIER.md` §2) yields the clean **radius↔angle lock**
> **(L)  `unit(o') ≡ (−1)^{v₃(o')} (mod 3)`.   `[PROVEN]`  (verified 0 exceptions / `2·10⁵`).**

(L) says the leading angular residue is a deterministic function of the radial parity — the stable (radial, `A`-base)
and the AIU-target (angular, neutral) coordinates are a **graph** at the leading 3-adic level.

### 1.3 Does (FE) have rotation-invariance as its UNIQUE solution? **No — the opposite.** `[PROVEN]`

Spherical-Haar requires `∫χ dρ = 0` for every nontrivial `χ`. By (FE₀) that forces `freq(D odd)=freq(D even)=½`.
But the conjectured/observed D-law is geometric `P(D=k)=2^{−k}`, giving `freq(D odd)=Σ_{k odd}2^{−k}=2/3`,
`freq(D even)=1/3`, hence
> `∫χ₀ dρ = 2/3 − 1/3 = 1/3 ≠ 0`.   `[PROVEN-conditional on geometric D; OBSERVED ≈0.3336, no decay over N≤2·10⁵]`

So (FE) does **not** force Haar; its solution is the explicit **push-forward of the D-law** under (★), which is
provably non-Haar at orbit level. The coupling is therefore an **anti-lever at the writable level**: rather than
forcing `μ_x³` toward rotation-invariance, it pins the orbit-empirical angular law *away* from it, and the deviation
is exactly a D-statistic (the parity imbalance) — `(K)`-class, non-vanishing. This is `AIU_THREEADIC_FOURIER.md`'s
"orbit-AIU-3adic is DISPROVEN," re-derived here as the unique-solution test of the functional equation.

### 1.4 The honest gap: orbit level ≠ ambient measure `[PROVEN scope]`

(FE)/(L) are statements about the **orbit points** — the diagonally embedded integers `ℤ[1/6]`, a Haar-null dense set.
AIU is about the **ambient** `A`-stable conditional `μ_x³` of the Krylov–Bogolyubov limit `μ` on `X=G/Γ`, *after*
folding by the lattice `ℤ[1/6]` (dense in `ℚ₃`). This is the (T1)–(T2) "pointwise lock ≠ measure invariance" barrier
(`NEWMATH_ADELIC_RIGIDITY.md` §3.3, `INTRATERM_ADELIC_MINING.md`). **Net for §1:** at the level where the coupling
functional equation is exact and writable (orbit), its unique solution is the non-Haar D-push-forward (anti-lever);
at the level where rotation-invariance would be the desired conclusion (ambient `μ_x³`), the coupling is a statement
about a null set and does **not** transfer to a functional equation on `μ_x³`. **The lever fails on both sides.**
`[PROVEN — no-go for the coupling-as-lever]`

---

## §2. SELF-CONSISTENCY / FIXED-POINT — is the coupling map a contraction? **No.** `[PROVEN structural]`

### 2.1 The fixed-point map `[PROVEN]`

(FE) defines a self-map `ρ ↦ Tρ` on probability measures on `ℤ₃*` (the angular law reproduces itself through one
renewal step). AIU `⟺` Haar is the fixed point realized by `μ`. The question (package §5's "deterministic dependence
is the wrong side for joinings, but could a fixed-point argument work?"): is `T` a **contraction** (⟹ unique fixed
point ⟹ Haar), and is proving contraction itself `(K)`-hard?

### 2.2 The map's core is an ISOMETRY, so it is NOT a contraction `[PROVEN]`

Decompose (★): `u' = R_2^{−D}·(−1 + 3^{v+1}U)`. The dominant factor is the rotation `R_2^{−D}`, a **rotation of the
compact group `ℤ₃*`** — an **isometry** for any invariant metric, and a unitary on `L²(ℤ₃*)`. Rotations have **purely
discrete spectrum** and are the canonical example of a **non-mixing, measure-rigid** map: a rotation pushes a measure
to a *rotated copy*, never toward Haar (e.g. `R_2^{−D}` sends `δ_a ↦ δ_{2^{−D}a}`, a point mass to a point mass).
The only potential averaging comes from the additive renewal `−1+3^{v+1}U`, but mod 3 it is the *constant* `−1`
(no `U`-dependence) and at higher levels it is a high-valuation perturbation (`3^{v+1}`, `v≥0`). So `T` is
"isometric rotation + small perturbation," and on the measure space it **does not contract toward Haar**: it has no
spectral gap (the neutral direction's defining feature, `|2|₃=1`, zero Lyapunov, zero entropy). `[PROVEN]`

> **Contrast with a genuine contraction.** A self-similar IFS / transfer operator with a *contracting* fiber map and a
> spectral gap would have unique Haar-like fixed point. Here the fiber map is an isometry (the AIU direction is
> neutral by construction), so the only fixed-point uniqueness mechanism — contraction — is structurally absent.
> This is the measure-space shadow of the EKL neutral-blindness (`(a)` Theorem A) and the coisometry no-go
> (op-norm Lyapunov `≡0`, `EUE_COISOMETRY_NOGO_THEOREM.md`): no contraction, in any fixed norm, along the neutral axis.

### 2.3 The genuine fixed point is NON-Haar; forcing Haar = forcing D-equidistribution = `(K)` (circular) `[PROVEN]`

Iterating, `u_n = R_2^{−(D_0+…+D_{n−1})}·(renewal terms)`. The angular law equidistributes to Haar **iff** the
cumulative rotation exponents `Σ_{j<n} D_j` equidistribute in the cyclic group `ℤ/φ(3^m)` for every `m` — i.e. iff
the partial sums of the D-sequence equidistribute mod `2·3^{m−1}`. That is a **single-orbit D-equidistribution
statement**, precisely `(K)`-class (a sibling of the `freq(D=1)≤½` cylinder fact; `AIU_THREEADIC_FOURIER.md` §4).
So:
- **`T` is a contraction-to-Haar ⟺ the cumulative D-sums equidistribute ⟺ a `(K)`-class statement.** Proving the
  contraction *is* the open problem. Assuming it is circular. `[PROVEN — circularity]`
- Worse, by (FE₀)/§1.3 the genuine fixed point of `T` (under the orbit's actual, geometric-looking D-law) is the
  **non-Haar** D-push-forward (`∫χ₀dρ=1/3`), *not* Haar. So self-consistency does not even single out Haar as a
  fixed point; it singles out the non-Haar law. `[PROVEN-conditional on the D-law]`

**Net for §2:** the fixed-point/self-consistency route fails for a *new, sharper* reason than the `(B)`
non-recurrence: the coupling map is **not a contraction** (its core is an isometric rotation with no spectral gap),
its realized fixed point is **non-Haar**, and any proof of contraction-to-Haar is identically the cumulative-D
equidistribution = `(K)`. The "wrong side for joinings" diagnosis of package §5 is confirmed and upgraded: the
dependence is a graph (L), which kills both independence (joinings) AND contraction (fixed point). `[PROVEN no-go]`

---

## §3. LITERATURE SCAN — central-direction rigidity that does NOT need a recurrent base

For each candidate: does it produce rotation-invariance along a zero-Lyapunov direction **without** an invariant
probability on the (here dissipative `v↦v+1`) base, and is its hypothesis met?

| mechanism | central-direction? | tolerates dissipative/non-recurrent base? | hypothesis met here? | verdict |
|---|---|---|---|---|
| **Furstenberg–Ledrappier / Avila–(Santamaria–)Viana Invariance Principle** (Astérisque 358; Invent. 2010, arXiv:1606.09429) | YES (zero central exponent ⟹ holonomy-invariant disintegration) | **NO** — its "Kullback/entropy along the central foliation" is defined over a **measure-preserving base**; needs an invariant probability to average the fibre cocycle | base is `A`-contracting, dissipative, no invariant probability | **FAILS** = the `(a)` Theorem (B). `[PROVEN-in-lit hypothesis]` |
| **Anzai–Furstenberg–Veech isometric extension** | YES | **NO** — requires probability-preserving base | same dissipative base | **FAILS** (`AIU_SKEW_ROTATION.md`). `[PROVEN]` |
| **Eskin–Lindenstrauss / Benoist–Quint stationary-measure rigidity** (`math.uchicago.edu/~eskin/RandomWalks`; arXiv:2104.09546) | partially (replaces recurrence by **stationarity** `ν=μ*ν` + a Lyapunov/Margulis drift = "expanding measure") | **YES in spirit** — stationarity substitutes for base recurrence | **NO**: needs a genuine **random walk** (i.i.d./Markov steps) and `ν` *stationary probability*; our orbit is **one deterministic trajectory**, D is self-referential not i.i.d. Modelling steps `2^{−D}`, `D` i.i.d. geometric ⟹ unique stationary = Haar — but that is the **ANNEALED** statement (already had via Rajchman `ν_{2/3}`); the quenched single-orbit version is `(K)` | **CLOSEST, but reduces to the annealed→quenched wall = `(K)`.** `[PROVEN — hypothesis (genuine randomness) not met; gives only annealed Haar]` |
| **Brown–Rodriguez Hertz–Wang / Katok–Rodriguez Hertz** higher-rank rigidity (arXiv:1809.09192, 2409.05991, 1001.2473) | via higher-rank coupling | n/a | **NO**: needs a **higher-rank acting group** with one element of **positive entropy** and **no proportional exponents**; here only `A` is iterated (rank 1), and `Φ`-invariance (rank-2) IS AIU (the conclusion), positive entropy IS ENT (the *other* open gap) | **FAILS** — hypotheses are the two open inputs (circular). `[PROVEN — hypothesis not met]` |
| **Cantat–Dujardin** invariant measures for large automorphism groups (arXiv:2110.04213) | via parabolic + hyperbolic generators | n/a | **NO**: needs a **non-elementary** group of automorphisms of a compact Kähler **surface** containing a **parabolic**; here the group is abelian rank-1 elementary `⟨×3/2⟩` on a **solenoid**, no parabolic, no surface | **FAILS** on every hypothesis. `[PROVEN-in-lit hypothesis]` |
| **Exponential mixing of the neutral cocycle** | — | — | **VOID**: the neutral fibre map is the rotation `R₂` on `ℤ₃*` — an **isometry with purely discrete spectrum**, the canonical **non-mixing** map. There is no mixing (let alone exponential) to invoke | **NOT-APPLICABLE** (no mixing exists). `[PROVEN]` |
| **Effective equidistribution along leaves** (Lindenstrauss–Margulis; Strömbergsson; effective horospherical) | along **expanding** leaves | **NO** — needs an expanding leaf + **spectral gap / property (T)** of the ambient space | here the AIU leaf is **neutral**, the radial base is **contracting**, and the acting group `ℤ[1/6]⋊⟨3/2⟩` is **amenable** (no spectral gap) | **FAILS** — needs expansion + gap, has neutral + amenable. `[PROVEN — hypothesis not met]` |

**Scan verdict `[PROVEN]`.** No mechanism in the scan produces rotation-invariance along a neutral direction over a
dissipative base. They split into two failure modes: (i) **needs a recurrent/probability base or a structural feature
absent here** (Invariance Principle, AFV, higher-rank BRHW, Cantat–Dujardin, effective-equidistribution, mixing —
each fails a named hypothesis); (ii) **replaces recurrence with stationarity** (Eskin–Lindenstrauss/Benoist–Quint) —
genuinely a "third kind" of mechanism, but it needs **bona fide randomness**, and the single deterministic orbit's D
is self-referential, so it yields only the **annealed** Haar, reproducing the annealed→quenched gap = `(K)`. The
`(a)` caveat ("a third mechanism is not ruled out") survives in the abstract, but **no concrete third mechanism in
the current literature meets the hypotheses of this action.** `[PROVEN — coverage no-go for the scanned families;
does NOT prove no future mechanism exists]`

---

## §4. HONEST NET

- **A third mechanism?** None found. The recurrence-free family that exists (stationary-measure rigidity) needs
  randomness the deterministic orbit lacks and delivers only annealed Haar = the annealed→quenched wall = `(K)`.
  Every other family fails a structural hypothesis (recurrent base / higher rank / non-elementary surface group /
  expanding leaf + spectral gap / mixing). `[PROVEN — coverage no-go; NOT a proof no mechanism can exist]`
- **The coupling as a lever?** It is an **anti-lever** at the writable level and a **non-lever** at the measure
  level. The functional equation (FE) is explicit; its unique-solution test (FE₀) shows Haar would require
  `freq(D odd)=½`, which the orbit's D-law violates (`=2/3`), so (FE) forces the angular law AWAY from Haar at orbit
  level; and the orbit-level law is Haar-null, so it does not transfer to `μ_x³`. `[PROVEN]`
- **Self-consistency / fixed point?** Not a contraction (isometric-rotation core, no spectral gap), realized fixed
  point is non-Haar, and any contraction-to-Haar proof is identically the cumulative-D equidistribution = `(K)`.
  Confirms and upgrades the package §5 "wrong side" diagnosis: the dependence is a **graph** (L) that kills both
  independence (joinings) and contraction (fixed point). `[PROVEN]`
- **New concrete fact banked:** the radius↔angle lock **`unit(o') ≡ (−1)^{v₃(o')} (mod 3)`** `[PROVEN]`, exposing the
  leading angular character sum as the D-parity imbalance `≈1/3`. This is the quantitative form of "the neutral
  direction carries no free equidistribution at orbit level — its coordinate is graphed onto the radial base."
- **Scope.** Does **not** prove AIU, does **not** disprove AIU (the orbit-level non-Haar-ness is on a Haar-null set;
  AIU is an ambient measure statement), does **not** prove `(K)`. The probe **strengthens the `(a)` caveat into a
  partial answer**: among the natural third routes (coupling-lever, self-consistency fixed point, and the six scanned
  literature mechanisms), all are either inert, anti-leverage, or reduce to `(K)`. The kernel is unchanged and
  generational.

---

## Sources

- A. Avila, M. Viana, *Extremal Lyapunov exponents: an invariance principle and applications*, Invent. Math. (2010);
  invariance principle / entropy (Kullback) along the central foliation over a **measure-preserving base**.
  `[PROVEN-in-lit]` — https://link.springer.com/article/10.1007/s00222-010-0243-1, arXiv:1606.09429
- A. Eskin, E. Lindenstrauss, *Random walks on locally homogeneous spaces*; Benoist–Quint stationary-measure
  classification; Prohaska–Sert–Shi *Expanding measures* (arXiv:2104.09546) — stationarity + Lyapunov/Margulis drift
  replaces base recurrence, but requires a **genuine random walk**. `[PROVEN-in-lit]`
  https://www.math.uchicago.edu/~eskin/RandomWalks/paper.pdf
- A. Brown, F. Rodriguez Hertz, Z. Wang; A. Katok, F. Rodriguez Hertz — higher-rank abelian / lattice measure
  rigidity, **needs higher rank + positive entropy + no proportional exponents**. `[PROVEN-in-lit]`
  arXiv:1809.09192, arXiv:2409.05991, arXiv:1001.2473
- S. Cantat, R. Dujardin, *Invariant measures for large automorphism groups of projective surfaces* (arXiv:2110.04213)
  — **non-elementary surface automorphism group + parabolic**. `[PROVEN-in-lit]`
- S. Anzai (1951), H. Furstenberg (1961, 1963), W. Veech (1969); H. Weyl — isometric extensions / uniquely ergodic
  rotations over a **probability** base. `[PROVEN-in-lit]`
- Repo: `AIU_NEUTRAL_OBSTRUCTION_THEOREM.md` (the `(a)` conjunction A∧B + caveat), `AIU_SKEW_ROTATION.md`
  (dissipative-base inertness), `AIU_JOININGS.md` (§2 spherical-Haar reformulation; §4 dependence wrong side),
  `AIU_THREEADIC_FOURIER.md` (D-slaved angular Weyl sums; orbit-AIU-3adic disproven), `NEW_MATH_PROGRAM.md`,
  `BB6_FRAMEWORK_PACKAGE.md` §5/§5.5, `EUE_COISOMETRY_NOGO_THEOREM.md` (op-norm Lyapunov ≡0).
- Numerics (this note, scratchpad): induced map `N=2·10⁵`, seed `o₀=27`; `bad_coupling=0`, `bad_anglelock=0`
  (verifies `v₃(o')=D−1` and `unit(o')≡(−1)^{v₃(o')} mod 3`); `meanD≈1.996`, `freq(D odd)≈0.6668`,
  `freq(D even)≈0.3332`, leading angular sum `≈0.3336`. `[OBSERVED]`

No machine decided. No label upgraded.
