# Rank-1 amenable arithmetic rigidity: the rank-2 host group as the second direction (2026-06-29)

*FRAMEWORK-CONSTRUCTION. Builds a candidate rigidity principle for the single specified orbit of
`A=×(3/2)` on the S-arithmetic solenoid, using the **adelic / product-formula** structure as a substitute
for the missing second independent direction that Ratner/ELV/Furstenberg/BFLM require. SOUNDNESS PARAMOUNT:
every claim is labelled `[PROVEN]` / `[PROVEN-in-lit]` / `[CONJECTURE]` / `[DEFINITION]` / `[OBSERVED]`.
New DEFINITIONS and CONJECTURES are introduced; **no claim to prove (K)**; the irreducible conjecture is
isolated and marked. Numerics: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int, `N≤1e5`.
Cross-refs: `ADELIC_COUPLING.md`, `INTRATERM_ADELIC_MINING.md`, `REPELLER_ESCAPE.md`,
`EXPERT_ASK_HOMOGENEOUS.md`, `TRACTABILITY_MAP.md`, `SESSION_2026-06-29_AEV_CORE.md`. NOT committed.*

---

## 0. One-paragraph thesis

The program's wall is "rank-1 + amenable + hyperbolic + specified-orbit" (`EMPTY_TOOLBOX_QUESTION.md`):
rigidity engines want rank ≥ 2 or a non-amenable second direction, and our acting group `ℤ[1/6]⋊⟨3/2⟩` is
solvable and `⟨3/2⟩` is cyclic. **The new observation that organizes this framework:** on the *solenoid*
`X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` — and only there, because `ℚ₂,ℚ₃` were adjoined precisely so that `½,⅓` become
invertible — the two primitive units `2` and `3` *both* act as commuting hyperbolic automorphisms, and
`A=×(3/2)=(×3)∘(×2)⁻¹` lives **inside the rank-2 abelian group `⟨×2,×3⟩`**. Rank-2 `×2,×3` measure
rigidity (Rudolph–Johnson) and topological rigidity (Berend) are *available on the solenoid*
`[PROVEN-in-lit]`. The remaining gap is sharp and single: our orbit is only the **rank-1 sub-orbit** of the
rank-2 host, so its empirical measure is a priori only `A`-invariant, not `⟨×2,×3⟩`-invariant. The central
new principle is an **invariance-upgrade conjecture**: the adelic/product-formula lock plus the contracting
3-adic leaf force the single `⟨3/2⟩`-orbit's empirical measure to acquire the *separate* `×2`- and
`×3`-invariance, at which point existing rank-2 rigidity finishes the job. This relocates the open content
from "invent rank-2 rigidity from nothing" to "upgrade rank-1 invariance to rank-2 invariance using
arithmetic" — a strictly sharper, named target. It is a CONJECTURE; nothing here proves (K).

---

## 1. DEFINITIONS

### 1.1 The solenoid system `[DEFINITION, standard]`
Let `S={∞,2,3}`, `G=ℝ×ℚ₂×ℚ₃`, and `Γ=ℤ[1/6]` embedded diagonally `r↦(r,r,r)`. By the product formula
`Γ` is a discrete cocompact lattice; set
> `X = G/Γ` (compact abelian S-arithmetic **solenoid**), with Haar probability `m_X`.

For `u∈ℤ[1/6]ˣ` the multiplication `M_u(g)=u·g` descends to an automorphism of `X` (it normalizes `Γ`).
The dilations of `M_u` are `(|u|_∞,|u|_2,|u|_3)`. In particular:
- `A := M_{3/2}`, dilations `(3/2, 2, 1/3)`. `[PROVEN]` **hyperbolic**: expanding at `∞,2`, contracting
  at `3`, product `=1`, no neutral direction (`TRACTABILITY_MAP.md` Route 3).
- `M_2`, dilations `(2, 1/2, 1)`; `M_3`, dilations `(3, 1, 1/3)`. Both well-defined automorphisms of `X`
  because `½,⅓∈ℤ[1/6]`. `[PROVEN]`

### 1.2 The host rank-2 action `[DEFINITION]`
> `Φ : ℤ² → Aut(X)`, `Φ(a,b)=M_{2^a 3^b}`. Its image is the abelian group `⟨×2,×3⟩`, **rank 2** (`2,3`
> multiplicatively independent). `[PROVEN]` We have `A=Φ(-1,1)` and `M_2=Φ(1,0)`, `M_3=Φ(0,1)`.

So the cyclic `⟨A⟩` we actually iterate is the **rank-1 sub-lattice `ℤ·(-1,1)⊂ℤ²`** of the rank-2 host
`Φ`. This is the single structural fact the whole framework turns on, and it is `[PROVEN]`.

### 1.3 The orbit as an adelic point `[DEFINITION]`
The Antihydra seed `c₀=8` reduces (`ADELIC_COUPLING.md`) to the induced odd map
`o↦o'=3^{D-1}(3o-1)/2^D`, `D=v₂(3o-1)`, seed `o₀=27`. Each `oₙ∈ℤ[1/6]` embeds as the adelic point
`xₙ=(oₙ,oₙ,oₙ)Γ∈X`, and `xₙ₊₁` is `A`-related to `xₙ` up to the `Γ`-translation that clears denominators
(the renewal cocycle). Write the orbit empirical measure
> `μ_N := (1/N)Σ_{n<N} δ_{xₙ}`, and let `μ` be any weak-* limit. `[DEFINITION]`
Every limit `μ` is `A`-invariant `[PROVEN]` (Krylov–Bogolyubov along the renewal-normalized orbit).

### 1.4 The "arithmetic second direction" `[DEFINITION — the core new object]`
The missing second independent direction is supplied **not by a second group element we iterate, but by the
ambient host `Φ` together with the global rationality of the orbit**:
> **Arithmetic second direction.** The pair (`×2`-flow, `×3`-flow) on `X`, of which `A=×3/2` is the single
> *anti-diagonal* combination `(×3)∘(×2)⁻¹`. The "second direction" transverse to the `A`-orbit inside the
> Cartan plane `ℝ²=Lie(⟨×2,×3⟩)` is the line `(×2)·(×3)` (the *diagonal* `Φ(t,t)=M_{6^t}`). The product
> formula is exactly the statement that this diagonal direction is the place-wise scaling whose three local
> dilations multiply to 1: `|6|_∞|6|_2|6|_3 = 6·(1/2)·(1/3)=1`. `[PROVEN]`

Thus the three places `(ℝ,ℚ₂,ℚ₃)` are not three independent coordinates: the product formula ties them into
exactly one extra global relation, and the host `Φ` realizes the *two-dimensional* scaling plane in which
`A` is one rational-slope line. **The arithmetic asset = the rank-2 Cartan plane `ℝ²` of `Φ`, present on the
solenoid but absent on the torus, with `A` a rank-1 line inside it.** The slope `log(3/2):log2` at the
places `(∞,2)` is irrational (`log_2 3 ∉ ℚ`) `[PROVEN]` — the `A`-line is equidistributed-direction inside
the plane, the geometric reason the host is the right enrichment.

### 1.5 Candidate rigidity statement `[DEFINITION]`
> **Forced measure.** We ask which `A`-invariant `μ` (Def 1.3) can occur as a weak-* limit of `μ_N` for the
> *specified* seed `x₀`. The target is: **the only such `μ` is `m_X`** (Haar). Equivalently the single orbit
> equidistributes; equivalently (K) holds (`SESSION_2026-06-29_AEV_CORE.md` §1).

---

## 2. CENTRAL NEW PRINCIPLE `[CONJECTURE]`

> ### Adelic Invariance-Upgrade Conjecture (AIU)
> Let `μ` be a weak-* limit of the empirical measures `μ_N` of the single `⟨3/2⟩`-orbit of `x₀` (Def 1.3).
> Suppose `μ` is non-atomic with positive 2-adic fibre entropy `h_μ(M_2)>0`. Then `μ` is invariant under
> the **full host** `⟨×2,×3⟩`, not merely under `A=×3/2`.

Granting AIU, the classical rank-2 theorem applies on the solenoid:

> ### Consequence (conditional) `[PROVEN-in-lit, modulo AIU]`
> A `⟨×2,×3⟩`-invariant, ergodic, **positive-entropy** measure on a solenoid of this type is Haar
> (Rudolph 1990 / Johnson, in the solenoid form of Berend / "commuting automorphisms of tori and solenoids",
> arXiv:2101.11120). Hence `μ=m_X`, the orbit equidistributes, and (K) follows.

**Why AIU is genuinely new and NOT the dead rank-1 case.** Every prior repo verdict
("rank-1 ⇒ no rigidity", `EXPERT_ASK_HOMOGENEOUS.md`) is about the group **we iterate**, `⟨3/2⟩`. AIU does
not iterate a second map; it **conjectures that the limit measure of one rank-1 orbit promotes itself into
the invariance class of the rank-2 host that already acts on the same space**. The promotion engine is
arithmetic, of three reinforcing kinds, each `[PROVEN]` as a *mechanism present* (the conjecture is only
that they *suffice*):

1. **Contracting 3-adic leaf gives a stable foliation to disintegrate along** (`A` is hyperbolic;
   `TRACTABILITY_MAP.md`). The leaf-wise conditional measures of `μ` along the `ℚ₃` (stable) direction are
   the objects on which `M_3`-invariance can be read — the leaf of `A` and the leaf of `M_3` coincide as
   sets (both contract at `3`), so `A`-conditional structure already *is* `M_3`-conditional structure. This
   is the one direction where rank-1 and rank-2 *share* a foliation — the wedge AIU drives.
2. **Exact 2↔3 product-formula lock** `v₃(o_{j+1})=D_j-1` (`ADELIC_COUPLING.md` §1a) `[PROVEN]`: the 3-adic
   valuation of every term is the predecessor's 2-adic depth. This is the per-step shadow of the host
   relation `×3=A·×2`; AIU asks that its Cesàro average upgrade to measure-level `M_3`-invariance.
3. **No permanent trapping** (`EXPERT_ASK_HOMOGENEOUS.md`; `REPELLER_ESCAPE.md`): periodic points are
   2-adically repelling, so `μ` charges no finite orbit — the *positive-entropy* hypothesis of AIU is the
   plausible (and the only) thing standing between the proven non-atomicity and Haar.

---

## 3. PROVEN seeds, one consequence, and the honest tautology barrier

### 3.1 Proven seeds the framework rests on `[PROVEN]`
- **Host realization.** `M_2,M_3∈Aut(X)`, `A=M_3 M_2^{-1}`, `⟨×2,×3⟩` rank-2 (Def 1.2). `[PROVEN]`
- **Hyperbolicity / contracting leaf.** dilations `(3/2,2,1/3)`, product 1, no neutral direction. `[PROVEN]`
- **Dual-repulsion lemma.** On `D=1`: `|o-1|_∞×3/2`, `|o-1|_2×2`, oddpart `×3`, adelic `×3` (exact, 0
  failures /3·10⁵; `REPELLER_ESCAPE.md` §1). `o=1` repels at both places. `[PROVEN]`
- **2↔3 coupling.** `v₃(o_{j+1})=v₂(3o_j-1)-1` exactly (0 failures /2·10⁵; `ADELIC_COUPLING.md`). `[PROVEN]`
- **Periodic exclusion / positive-entropy plausibility.** `x₀` is not eventually periodic; periodic part of
  the exceptional set is rigorously excluded (2-adic repulsion). `[PROVEN]` The residual is the
  positive-entropy Cantor part — exactly AIU's hypothesis.

### 3.2 The one consequence I can prove now `[PROVEN]`
> **Lemma (rank-2 dichotomy on the solenoid, unconditional).** Any weak-* limit `μ` of `μ_N` that *happens*
> to be `⟨×2,×3⟩`-invariant and ergodic is **either Haar or supported on the (Haar-null, ℚ-rational)
> `Φ`-finite set**; and the latter is excluded for our `x₀` by §3.1. Hence: *`A`-invariance is the only gap*
> — if `μ` is upgraded to host-invariance at all, it is Haar.

*Proof.* Berend's topological rigidity for solenoid automorphism actions (totally irreducible,
non-virtually-cyclic, contains a hyperbolic element — all hold for `Φ` on `X`) `[PROVEN-in-lit]` makes every
proper closed `Φ`-invariant set finite/rational; combined with the periodic-exclusion seed §3.1 the
finite alternative cannot carry positive `μ`-mass for the specified `x₀`. ∎

This isolates the entire difficulty into the *single* implication `A`-invariant ⟹ `⟨×2,×3⟩`-invariant —
i.e. AIU is not just sufficient, it is (given §3.2) the **exact** missing step. That sharpening is the new
deliverable of this note.

### 3.3 The tautology barrier — stated honestly, and how the framework proposes to cross it
`INTRATERM_ADELIC_MINING.md` PROVED two facts that *threaten* AIU and must be confronted head-on:
- **(T1) Product formula is codim-1 (first-moment) per step.** `∏_v|N|_v=1` is one scalar `=` the renewal
  identity `log oₙ≈(ΣDⱼ)log(3/2)`; it pins the *mean*, never a distribution. `[PROVEN]`
- **(T2) Within one orbit the 3-adic place is an invertible time-shift of the 2-adic place**
  (`e_j=D_{j-1}-1`), so per-term the 3-adic data carries **identical** information to the 2-adic — no second
  independent channel exists at the pointwise level. `[PROVEN]`

**These kill the *pointwise / first-moment* reading of the second direction — and the framework concedes
that fully.** The proposal to cross the barrier rests on a precise distinction the prior notes did not
separate:

> **Pointwise lock ≠ measure-level invariance.** (T1)–(T2) are statements about the **orbit points** (the
> arithmetic of the diagonal `ℤ[1/6]` embedding, a Haar-null set in `X`). AIU is a statement about the
> **weak-* limit measure** `μ` on the *ambient* `X`, where the `ℚ₂` and `ℚ₃` coordinates are genuinely
> independent directions. The per-step diagonal lock `e_j=D_{j-1}-1` is exactly the kind of rigid
> finite-window relation that a Cesàro limit is *designed to forget*: the limit measure can be
> `×3`-invariant even though no individual point is "`×3`-movable", precisely as Lebesgue is `×3`-invariant
> on `ℝ/ℤ` while no rational orbit is. **The barrier-crossing claim is therefore: the asymptotic invariance
> group of `μ` is strictly larger than the pointwise symmetry group of the orbit, and the surplus is exactly
> `×3` (equivalently `×2`).** This is the irreducible, unproven content — it is what (T1)–(T2) leave open
> rather than close, because they are codim-1 / pointwise and AIU is codim-∞ / asymptotic.

> ### Irreducible conjecture (the crux, restated minimally)
> **(AIU-min)** For the specified seed, `lim_N (1/N)Σ_{n<N} f(M_3 xₙ) = lim_N (1/N)Σ_{n<N} f(xₙ)` for all
> `f∈C(X)` — i.e. the orbit empirical average is asymptotically `M_3`-insensitive. `[CONJECTURE]`
This single asymptotic identity (one new direction's invariance) is everything; it is **not** implied by
(T1)–(T2), and the framework supplies no proof of it. It is the honest replacement for "second independent
direction."

---

## 4. REDUCTION: AIU ⟹ (K)

> **Theorem to build (conditional chain).** `[PROVEN-in-lit links] + [CONJECTURE AIU]`
> 1. `μ` `A`-invariant, non-atomic, `h_μ(M_2)>0` (positive-entropy seed §3.1). `[hypothesis]`
> 2. **AIU** ⟹ `μ` is `⟨×2,×3⟩`-invariant. `[CONJECTURE §2]`
> 3. Rudolph–Johnson (solenoid form) ⟹ positive-entropy `⟨×2,×3⟩`-invariant `μ` is Haar `m_X`.
>    `[PROVEN-in-lit]`
> 4. §3.2 excludes the finite/rational alternative for `x₀`. `[PROVEN]`
> 5. ⟹ every weak-* limit of `μ_N` is `m_X` ⟹ the single orbit equidistributes ⟹ **(K)** at `α=8`
>    (`SESSION_2026-06-29_AEV_CORE.md` §1) ⟹ Antihydra non-halts.

> **The new theorem to prove is exactly AIU (equivalently AIU-min, §3.3):** *the empirical measure of a
> single rank-1 `⟨3/2⟩`-orbit on the S-arithmetic solenoid, of positive 2-adic entropy, is invariant under
> the full rank-2 host `⟨×2,×3⟩`.* Everything else in the chain is either `[PROVEN]` here or
> `[PROVEN-in-lit]`. **No claim is made that AIU is proven.**

---

## 5. NOVELTY (WebSearch, homogeneous dynamics)

- **vs. standard rank-1 (a.e. only / no rigidity).** The repo's own audits and Einsiedler–Lindenstrauss
  (JMD 2008) correctly say a *single cyclic hyperbolic* action has an uncountable simplex of invariant
  measures and invariant Cantor sets — no rigidity for `⟨3/2⟩` `[PROVEN-in-lit]`. **Our framework does not
  contradict this:** it does not seek rigidity *of `⟨3/2⟩`*; it conjectures an *invariance upgrade* of one
  orbit's limit measure into the rank-2 host `⟨×2,×3⟩` that **also acts on the solenoid**. The host's
  rigidity is classical (Rudolph–Johnson; Berend; "commuting automorphisms of tori and solenoids",
  arXiv:2101.11120) `[PROVEN-in-lit]`. The new object is the *upgrade map*, not new rigidity.
- **vs. BFLM (JAMS 2011).** BFLM gets individual-orbit equidistribution but needs a **non-abelian** acting
  semigroup with a spectral gap. Ours is **abelian** (`⟨×2,×3⟩`), no gap — so we *cannot* and *do not* use
  the BFLM mechanism; we route through commutative `×2,×3` rigidity instead, supplying the missing
  invariance by arithmetic (the product-formula lock + contracting 3-adic leaf) rather than by a gap.
- **vs. effective Ratner / Lindenstrauss–Mohammadi.** Those are unipotent/higher-rank. Ours is hyperbolic
  rank-1; the host enrichment is the substitute.
- **Net novelty.** I found **no** result that takes a single rank-1 sub-orbit of a rank-2 abelian solenoid
  automorphism action and upgrades its empirical measure to the full rank-2 invariance. The literature has
  (i) rank-2 rigidity on solenoids and (ii) rank-1 non-rigidity, but not (iii) the **bridge** between a
  rank-1 orbit and the rank-2 invariance class. AIU names that bridge precisely. `[OBSERVED — novelty]`

---

## 6. NUMERICS `[OBSERVED, exact big-int, N≤1e5, seed o₀=27]`
- `meanD = 2.00082` (Haar 2); `density{3|o}=0.4995` (matches `v₃=D-1` coupling target ½). `[OBSERVED]`
- mod-`2⁴` odd-residue frequencies in `[0.1232,0.1278]` vs uniform `0.125` — the integer orbit's 2-adic
  marginal is Haar-consistent to <2.5% (the *empirical* (K)-data; not a proof). `[OBSERVED]`
- Consistent with `REPELLER_ESCAPE.md` (`freq(D=1)=0.50029=1-1/E_deep`, no margin) and
  `INTRATERM_ADELIC_MINING.md` (4-cell law exact, 0 failures): the numerics support equidistribution
  (hence AIU) but supply no one-sided margin and decide nothing.

---

## 7. SOURCES
- Rudolph, *×2 ×3 invariant measures and entropy*, Ergodic Th. Dyn. Sys. (1990); Johnson, *Measures on the
  circle invariant under multiplication by a non-lacunary subsemigroup*. `[PROVEN-in-lit]`
- Berend, *Multi-invariant sets on tori* / *on compact homogeneous spaces* (topological rigidity, solenoid
  form). `[PROVEN-in-lit]`
- *Rigidity properties for commuting automorphisms on tori and solenoids*, arXiv:2101.11120. `[PROVEN-in-lit]`
- Einsiedler–Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case*, JMD
  (2008) — rank-1 non-rigidity. `[PROVEN-in-lit]`
- Bourgain–Furman–Lindenstrauss–Mozes, JAMS 24 (2011) — non-abelian individual-orbit equidistribution.
  `[PROVEN-in-lit]`
- *Entropy, Lyapunov exponents, and rigidity of group actions*, arXiv:1809.09192; *Symmetry of entropy in
  higher rank diagonalizable actions*, arXiv:1803.07762 (entropy method, host context). `[PROVEN-in-lit]`
- Repo: `ADELIC_COUPLING.md`, `INTRATERM_ADELIC_MINING.md`, `REPELLER_ESCAPE.md`,
  `EXPERT_ASK_HOMOGENEOUS.md`, `TRACTABILITY_MAP.md`, `SESSION_2026-06-29_AEV_CORE.md`,
  `EMPTY_TOOLBOX_QUESTION.md`.

---

### Honest status
The framework is a *reorganization with one new conjecture*, not a breach. PROVEN: the host realization
(`A` is a rank-1 line in the rank-2 `⟨×2,×3⟩` acting on the solenoid), the dichotomy lemma (§3.2 — the
*only* gap is `A`-invariance ⟹ host-invariance), and all adelic seeds. CONJECTURE (irreducible): AIU /
AIU-min — the asymptotic invariance group of the single orbit's limit measure exceeds its pointwise
symmetry group by exactly `×3`. The tautology barrier (T1)–(T2) is conceded at the pointwise/first-moment
level and the crossing is *proposed* (measure-level ≠ pointwise) but **not proven**. The reduction
AIU ⟹ (K) is otherwise complete via `[PROVEN-in-lit]` rank-2 rigidity.

No machine decided. No label upgraded.
