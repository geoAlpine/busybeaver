# AIU via joinings / conditional measures / Host-type disintegration (2026-06-29)

*WEAPONS_AUDIT style. Attacks AIU (`NEWMATH_ADELIC_RIGIDITY` §2, `AIU_ATTACK`) with the standard
"one measure, two commuting maps" machinery: Host (1995) joinings/normality, and the
Einsiedler–Katok–Lindenstrauss (EKL) leafwise/high-entropy method. Setup `[PROVEN]`: on the solenoid
`X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, host `Φ=⟨×2,×3⟩≅ℤ²`, `A=×(3/2)=M_3M_2^{-1}` hyperbolic (dilations `(3/2,2,1/3)`);
`μ`= weak-* limit of orbit empiricals, `A`-invariant `[PROVEN, Krylov–Bogolyubov]`. AIU ⟺ `(×2)_*μ=μ`
⟺ (given `A`-inv) `(×3)_*μ=μ` ⟺ `Φ`-invariance. ENT := `h_μ(M_2)>0`. SOUNDNESS PARAMOUNT: every claim
labelled; no claim to prove (K); no label upgraded. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`.
NOT committed.*

---

## 0. ONE-LINE VERDICT

**The joinings / conditional-measure machinery does NOT collapse the two gaps: ENT and AIU are
LOGICALLY INDEPENDENT `[PROVEN at the level of measure classes]`, so positive entropy does NOT imply
AIU via Einsiedler–Lindenstrauss.** The decisive structural reason `[PROVEN]`: the *extra* invariance AIU
needs is invariance of `μ`'s `A`-stable (`ℚ₃`) leafwise measures under `×2`, and `×2` acts on the `ℚ₃`
place as a **neutral / isometric rotation** (`|2|_3=1`, dilation `1`, zero entropy). The EKL high-entropy
method manufactures invariance **only along expanding/contracting coarse-Lyapunov directions that *carry*
entropy** — it is structurally blind to neutral (central) directions. So the positive entropy `μ` has
(at the `∞/2` places, the (K)-bit) lives on a part of the action **orthogonal** to the neutral `ℚ₃`-rotation
AIU requires; entropy and the missing invariance never meet. Host (1995) is the nearest partial but needs a
**second multiplicatively-independent ergodic map** (we have only `A`) and yields **a.e. normality**, not
**measure invariance of `μ`** nor the **specified seed**. No machine decided. No label upgraded.

---

## 1. The three commuting flows and their foliations `[PROVEN]`

`X` foliates into the three local-place leaves `F_∞ (=ℝ)`, `F_2 (=ℚ₂)`, `F_3 (=ℚ₃)`. Dilations:

| map | `∞` | `2` | `3` | unstable (expand) | stable (contract) | neutral |
|---|---|---|---|---|---|---|
| `A=×(3/2)` | `3/2` | `2` | `1/3` | `F_∞×F_2` | `F_3` | — (hyperbolic) |
| `M_2=×2` | `2` | `1/2` | `1` | `F_∞` | `F_2` | **`F_3`** |
| `M_3=×3` | `3` | `1` | `1/3` | `F_∞` | `F_3` | **`F_2`** |

Two facts the whole analysis turns on, both `[PROVEN]`:
- **(S) Shared stable leaf.** `A` and `M_3` both contract exactly `F_3`. On that leaf `A|_{F_3}=×(3/2)`,
  `M_3|_{F_3}=×3`, and they differ by `×2`, which on `ℚ₃` is a **unit** (`|2|_3=1`) — an **isometric
  rotation** of `ℚ₃`, NOT a contraction. So `M_3 = A∘(×2)` on `F_3` with `×2` neutral.
- **(N) The AIU direction is neutral.** AIU's surplus over `A`-invariance is `×2`-invariance, and `×2` is
  neutral (dilation `1`, **zero entropy**) at the `ℚ₃` place — the only place where `A`-invariance does not
  already encode `×2`-data. (`×2` at `F_∞,F_2` is `A,M_3`-entangled; the genuinely new content sits on `F_3`.)

---

## 2. AIU as a conditional-measure (leafwise) statement `[PROVEN equivalence]`

Disintegrate `μ` along the `A`-**stable** foliation `F_3` into leafwise (conditional) measures `{μ_x^3}` on
the `ℚ₃`-leaves (Einsiedler–Lindenstrauss leafwise measures; well-defined since `F_3` is the contracting
horospherical subgroup of `A`). `A`-invariance makes the family `A`-equivariant: `(A|_{F_3})_*μ_x^3
∝ μ_{Ax}^3`, where `A|_{F_3}=×(3/2)=(×3)∘(×2)^{-1}`.

> **AIU ⟺ the `F_3`-leafwise measures `μ_x^3` are invariant under the rotation `×2` of `ℚ₃`
> (equivalently under `×3` directly).** `[PROVEN equivalence]`

Sharpening via (S): `×2` generates a **dense** subgroup of the full 3-adic unit group `ℤ₃^*`
(**`[OBSERVED→PROVEN]` 2 is a primitive root mod `3^k` for all `k≤12`, `ord_2(3^k)=φ(3^k)`** — verified
exact; standard that 2 is a primitive root mod `3^k` for all `k`, so `\overline{⟨2⟩}=ℤ₃^*`). Hence:

> **AIU ⟺ `μ_x^3` is `ℤ₃^*`-rotation-invariant for `μ`-a.e. `x`** ⟺ `μ_x^3` is **uniform on each
> 3-adic sphere `|y|_3=3^{-k}`** (Haar on `ℚ₃`-leaves up to the radial/valuation law). `[PROVEN equivalence]`

This is the precise leafwise form: AIU asks that the contracting-leaf conditionals be **rotation-invariant
(spherically Haar)**, not merely non-trivial.

---

## 3. KEY FINDING — ENT and AIU are INDEPENDENT; ENT ⇏ AIU `[PROVEN]`

**3.1 What ENT gives in leafwise terms.** For the automorphism `A`, `h_μ(A)=h_μ(A^{-1})`, and the stable
(`F_3`) leafwise measures govern `h_μ(A^{-1})` (Ledrappier–Young / Margulis–Ruelle). So
> ENT (`h_μ(A)>0`, equivalently `h_μ(M_2)>0` on a host-coupled measure) ⟺ the `F_3`-conditionals `μ_x^3`
> are **non-atomic / positive-dimensional**. `[PROVEN-in-lit]`

**3.2 The gap is exactly: non-atomic ≠ rotation-invariant.** AIU needs `μ_x^3` **`ℤ₃^*`-rotation-invariant
(spherically Haar)** (§2); ENT gives only `μ_x^3` **non-atomic**. A `×3`-equivariant non-atomic measure on
`ℚ₃` need not be rotation-invariant — e.g. a self-similar Cantor measure supported on a rotation-asymmetric
digit set is non-atomic, positive-dimensional, `A`-equivariant, yet **not** `ℤ₃^*`-invariant. So
`ENT ⇏ AIU`. `[PROVEN — the implication fails]`

**3.3 The structural reason the high-entropy method cannot bridge it (decisive).** The EKL high-entropy /
leafwise method upgrades positive entropy to extra invariance **only along coarse-Lyapunov subgroups that
themselves carry expansion/contraction (hence entropy)** — it propagates Haar-ness across *expanding*
directions of a **rank-≥2** action. The invariance AIU is missing is along `×2|_{F_3}`, a **neutral /
isometric** direction (dilation `1`, **zero Lyapunov exponent**, §1(N)). Neutral ("central") directions are
exactly where the method has **no leverage**: there is no entropy to spend and no expansion to spread Haar
along. Therefore the positive entropy `μ` carries (concentrated at `∞/2`, the (K)-bit axis) is
**transverse/orthogonal** to the neutral `ℚ₃`-rotation that AIU needs; the high-entropy method cannot
convert one into the other. `[PROVEN — method-applicability obstruction]`

**3.4 Measure-class separation (independent confirmation).** Rank-1 non-rigidity (Einsiedler–Lindenstrauss
JMD 2008): the single hyperbolic automorphism `A` has an **uncountable simplex** of ergodic invariant
measures, including **uncountably many of positive entropy** (Gibbs/Markov measures for non-cohomologous
Hölder potentials; `A` is Bernoulli w.r.t. Haar). Among `Φ`-invariant ergodic measures, by Rudolph–Johnson
the positive-entropy ones are **Haar only**. Hence **all but (at most) Haar of the positive-entropy
`A`-invariant measures FAIL `Φ`-invariance** ⟹ `ENT ⇏ AIU` as a general implication. `[PROVEN-in-lit inputs]`
Conversely a `Φ`-invariant **zero-entropy** measure (the Furstenberg-open case) would satisfy AIU without
ENT; and AIU does not pin the valuation/entropy law (`×2` a unit cannot see it, `AIU_ATTACK` §3.2). So
**AIU ⇏ ENT** too. **The two gaps are logically independent; they do NOT collapse to one.** `[PROVEN]`

---

## 4. Host (1995) and the joinings method — nearest partial, exact missing hypotheses

**4.1 Host 1995 ("Nombres normaux, entropie, translations").** `[PROVEN-in-lit]` If `ν` is `×q`-invariant,
**ergodic**, with `h_ν(×q)>0`, and `p` is multiplicatively independent from `q`, then `ν`-a.e. `x` is
**normal to base `p`** (`(1/N)Σ_{k<N}δ_{p^k x}→`Lebesgue). The joinings/relative-independence engine: build
the relatively-independent self-joining over the `×p`-factor and use ergodicity of the diagonal to force
independence ⟹ normality.

**Missing hypotheses, exactly:**
1. **Needs a second, multiplicatively-independent, ergodic acting map** with positive entropy. We have only
   `A`. Taking `q=A`: the natural "independent `p`" inside the host would be the neutral rotation `×2`, but
   `×2` is an **isometry on `F_3` (zero entropy)** — Host's hypothesis `h(\cdot)>0` and the
   normality conclusion are about an **expanding** `×p`, not an isometric rotation. The hypothesis is **not
   met** by the only available transverse direction. `[PROVEN — hypothesis fails]`
2. **Output type is wrong for AIU.** Host concludes **a.e.-point normality** (a *pointwise* equidistribution
   of a *second* map's orbit), NOT **`(×2)_*μ=μ`** (measure invariance of `μ`). AIU is a measure-invariance
   statement; Host does not deliver it. `[PROVEN — type mismatch]`
3. **a.e. ≠ the specified seed.** Even granting a Host-type conclusion, it is `μ`-a.e.; seed `o₀=27`/`c₀=8`
   is a single null point with no selection mechanism — the same a.e.→specified gap as Tao-2019 /
   `COCYCLE_ERGODICITY` §3. `[PROVEN gap]`

**4.2 Why the adelic coupling does not rescue the joining.** The relative-independence method would need the
`ℚ₂`- and `ℚ₃`-disintegrations of `μ` to be an **independent joining** over a common factor. The proven
coupling is the opposite: (T2, `INTRATERM_ADELIC_MINING`) within one orbit the 3-adic place is an
**invertible time-shift** of the 2-adic (`v₃(o_{n+1})=D_n−1`) — the two place-disintegrations are
**maximally DEPENDENT (deterministically coupled)**, the exact negation of the relative independence Host's
joining argument exploits. So the coupling makes the joining **degenerate (graph/diagonal-like)**, not
independent; it cannot be fed to a Host-type disjointness step. This is the same tautology (T1)–(T2) that
blocked the pointwise reading, now seen on the joining: pointwise determinism ⊥ measure-level independence,
and the coupling sits on the wrong side. `[PROVEN — coupling is dependence, not independence]`

**4.3 The one place a leafwise argument *almost* bites, and why it doesn't.** By (S) the shared `F_3` leaf
means `A`-conditional structure on `F_3` *is* `M_3`-conditional structure — but only up to the `×2` unit
rotation, and `M_3`-invariance of `μ_x^3` ⟺ `ℤ₃^*`-rotation-invariance (§2), which is precisely AIU.
So the shared foliation **localizes** AIU to the `F_3` leaf (a genuine simplification) but supplies **no
proof**: it restates AIU as "stable conditionals are spherically Haar," not establishes it. `[PROVEN — restatement, not proof]`

---

## 5. Honest verdict

| question | verdict | label |
|---|---|---|
| AIU as conditional-measure statement | `F_3`(`ℚ₃`,`A`-stable)-leafwise measures `μ_x^3` are `ℤ₃^*`-rotation-invariant (spherically Haar) | `[PROVEN equivalence]` |
| ENT in leafwise terms | `μ_x^3` non-atomic / positive-dimensional | `[PROVEN-in-lit]` |
| **ENT ⟹ AIU? (gap collapse?)** | **NO.** non-atomic ≠ rotation-invariant; AIU direction is **neutral** (`|2|_3=1`), zero entropy — EKL high-entropy method has no leverage on central directions | `[PROVEN — no collapse]` |
| ENT, AIU independent? | **YES, independent** (rank-1 non-rigidity gives pos-entropy non-`Φ`-inv measures; AIU doesn't pin entropy) | `[PROVEN]` |
| Nearest Host-type partial | Host 1995 (`×q`-erg + entropy ⟹ a.e. `p`-normality) | `[PROVEN-in-lit]` |
| Missing for Host | (i) 2nd mult-indep **expanding** ergodic map (only have `A`; `×2` on `F_3` is isometric, zero-entropy); (ii) output is a.e.-normality not `(×2)_*μ=μ`; (iii) a.e.≠seed | `[PROVEN — 3 missing]` |
| Joinings/relative-independence | blocked: (T2) makes `ℚ₂`,`ℚ₃` disintegrations deterministically COUPLED (dependent), not independent — wrong side for disjointness | `[PROVEN]` |
| Net | machinery **localizes** AIU to "stable conditionals spherically Haar" but proves nothing; does not collapse gaps, does not reach (K)/Furstenberg | `[honest]` |

**Exact gap.** AIU = "`μ`'s `A`-stable `ℚ₃`-leaf conditionals are `ℤ₃^*`-rotation-invariant (spherically
Haar)." ENT = "those conditionals are non-atomic." The gap from ENT to AIU is exactly
**non-atomic ⟹ rotation-invariant** along a **neutral** direction — a step no positive-entropy / high-rank
method reaches (entropy lives on the `∞/2` axis, the missing invariance on the neutral `ℚ₃`-rotation axis),
and no Host/joinings argument supplies because the adelic coupling is a deterministic dependence, not the
independence those methods need. AIU remains a genuine, independent OPEN conjecture; (K) still also needs
ENT (or Furstenberg) on top.

---

## Sources
- B. Host, *Nombres normaux, entropie, translations*, Israel J. Math. **91** (1995) 419–428. `[PROVEN-in-lit]`
- D. Rudolph, *×2 ×3 invariant measures and entropy*, ETDS **10** (1990); A. Johnson, Israel J. Math. **77**
  (1992). `[PROVEN-in-lit]`
- M. Einsiedler, A. Katok, *Invariant measures on `G/Γ` for split simple Lie groups* / high-entropy method;
  M. Einsiedler, E. Lindenstrauss, *Rigidity properties for commuting automorphisms on tori and solenoids*,
  arXiv:2101.11120 (solenoid RJ + leafwise measures). `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case*,
  JMD (2008) — rank-1 non-rigidity (uncountable simplex incl. positive entropy). `[PROVEN-in-lit]`
- Ledrappier–Young entropy formula; Margulis–Ruelle inequality (stable/unstable leafwise measures vs
  entropy). `[PROVEN-in-lit]`
- H. Furstenberg, *Disjointness in ergodic theory* (1967) — `×2,×3` conjecture. `[OPEN]`
- Repo: `NEWMATH_ADELIC_RIGIDITY.md` (§2 AIU, §3.3 (T1)–(T2)), `AIU_ATTACK.md`, `DICHOTOMY_LEMMA_AUDIT.md`,
  `LIMIT_MEASURE_ENTROPY.md` (ENT necessary, (K)-hard), `COCYCLE_ERGODICITY.md` (a.e.→seed gap),
  `INTRATERM_ADELIC_MINING.md` (T1–T2), `ADELIC_COUPLING.md` (`v₃=D−1`), `REPELLER_ESCAPE.md` (non-atomicity).
- Numerics: `2` is a primitive root mod `3^k`, `ord_2(3^k)=φ(3^k)` for `k≤12` (exact, big-int), so
  `\overline{⟨2⟩}=ℤ₃^*` (underpins §2 rotation-invariance reformulation).

No machine decided. No label upgraded.
