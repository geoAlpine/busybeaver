# New-mathematics research roadmap for Antihydra / BB(6) (2026-06-30)

*A research-program specification, NOT a proof. It (i) places the missing tool against the nearest existing theories,
naming the exact gap each leaves; (ii) defines the central new object as a precise research target; (iii) gives a ranked,
dependency-ordered roadmap of sub-problems with honest tractability and partial-yield estimates; and (iv) lists the
durable intermediate contributions that stand regardless. SOUNDNESS: every external result labelled `[PROVEN-in-lit]`;
every new target `[CONJECTURE]` or `[PROGRAM]`; the irreducible kernel `[OPEN]`. No proof of `(K)` is claimed; no label is
upgraded. Sources are the program corpus (`NEWMATH_SYNTHESIS.md`, `NEWMATH_ADELIC_RIGIDITY.md`, `AIU_ATTACK.md`,
`ENT_PESIN_MARGULIS.md`, `ENDOGENOUS_UE_BUILD.md`, `EXCURSION_SYNTHESIS.md`, `CORE_ORBIT_ARITHMETIC.md`,
`EMPTY_TOOLBOX_QUESTION.md`, `FURSTENBERG_CORNER_QUESTION.md`, `BB6_CROSSFIELD_SCOUT.md`, `BB6_FRAMEWORK_PACKAGE.md` §5–§7,
`BB6_NO_STRUCTURE_THEOREM.md`, `BB6_OBSTRUCTION_DICHOTOMY.md`) plus the cited literature. NOT committed.*

---

## 0. The kernel and the missing tool (one paragraph)

Antihydra non-halting reduces by a machine-verified `[PROVEN]` chain to the kernel **`(K)`**: the single specified orbit of
`A=×(3/2)` through the rational seed `8∈ℤ[1/6]` equidistributes toward Haar `m_X` on the `(2,3)`-adic solenoid
`X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`. Equivalently `(K)` is Mahler's 3/2 problem / the Andrieu–Eliahou–Vivion (AEV, arXiv:2510.11723)
rational-base-3/2 normality conjecture at `α=8`. The acting group `ℤ[1/6]⋊⟨3/2⟩` is **amenable (solvable), rank-1,
hyperbolic** (dilations `(3/2,2,1/3)`, product 1, no neutral direction in the *acting* map). The **missing tool** is a
theorem forcing this one *specified* (not a.e., not extremal, not constructed) orbit to be generic — an object that lives
in the gap between the rigidity toolbox (wants rank ≥ 2 or a non-amenable / unipotent second direction) and the
Weyl / unique-ergodicity toolbox (killed by hyperbolicity). `(K)` remains `[OPEN]`.

---

## 1. Nearest existing theories — theory | gap it leaves | as-a-home

The solenoid placement (`A=M_3M_2^{-1}` is a **rank-1 line `ℤ·(−1,1)` inside the rank-2 host `Φ=⟨×2,×3⟩`**) makes the
×2,×3 measure-rigidity world the relevant neighborhood. The chain is `(K) ⟺ μ=Haar ⟸ (AIU) ∧ (ENT)`, the conjunction
invoking the proven Rudolph–Johnson; so the named gaps are **(AIU)** rank-1 → rank-2 host invariance and **(ENT)** positive
2-adic measure entropy `h_μ(M_2)>0`.

| Theory (citation) | The exact gap it leaves | As-a-home for the new object |
|---|---|---|
| **Rudolph–Johnson** ×2,×3 + entropy (Rudolph ETDS 10 (1990); Johnson Israel J. 77 (1992)) `[PROVEN-in-lit]`; solenoid form arXiv:2101.11120 | Needs **joint `Φ=⟨×2,×3⟩`-invariance** (we have only rank-1 `A`-invariance) **and** `h_μ(M_2)>0`. Supplies neither. | **The finisher.** Both AIU and ENT feed it; if both are established the proven theorem closes `(K)`. The home for the *output*, not the *upgrade*. |
| **Berend** topological rigidity (1983; solenoid form via 2101.11120) `[PROVEN-in-lit]` | Topological **set** conclusion only ⟹ full support, **not** a measure; applies to the rank-2 host orbit `{2^a3^b·8}` (dense), gives **nothing** for the rank-1, virtually-cyclic `A`-orbit. | Supplies the proven full-support input; cannot reach Haar. Boundary marker, not a home. |
| **Furstenberg ×2,×3 conjecture, zero-entropy core** (1967; survey Tal arXiv:2110.05989) `[OPEN]` | Entropy-free: `Φ`-invariant nonatomic ⟹ Lebesgue is exactly Furstenberg, **open**; non-Lebesgue zero-entropy examples exist. | The regime `(K)` falls into **iff ENT fails** — but `h_μ=0 ⟹ μ≠Haar ⟹ (K) false`, so this is the (K)-false branch, a wall not a home. |
| **Einsiedler–Katok–Lindenstrauss high-entropy method** (arXiv:1803.07762, 2101.11120) `[PROVEN-in-lit]` | Propagates invariance only along **entropy-carrying** (expanding/contracting) coarse-Lyapunov directions. AIU's surplus direction (`×2` on `ℚ₃`, `|2|_3=1`) is **neutral / central, zero Lyapunov** — structurally invisible to the method. | **The most plausible home** for AIU as a *low-entropy / central-direction extension* of the leafwise-measure machinery — precisely the place where a genuinely new lemma must be grafted. |
| **Einsiedler–Lindenstrauss rank-1 / low-entropy method** (JMD 2008) `[PROVEN-in-lit]` | Rank-1 diagonal actions carry an **uncountable simplex** of invariant measures + invariant Cantor sets — no rigidity for `⟨3/2⟩`, no specified-point selection. | Explains *why* no rigidity of the iterated map exists; the home for the **negative** half (the obstruction), and the leafwise/adelic Ledrappier–Young apparatus the new object would extend. |
| **BFLM** individual-orbit equidistribution (JAMS 24 (2011)) `[PROVEN-in-lit]` | Gets a *single* orbit equidistributed at exponential rate, but needs a **non-abelian** acting semigroup with a spectral gap. Our `⟨3/2⟩` is abelian/amenable. | The only individual-orbit precedent; mechanism (random-walk gap) unavailable. Template for the *shape* of the target theorem, not its engine. |
| **Host** normality from a second map (Israel J. 91 (1995)) `[PROVEN-in-lit]` | Needs a **second multiplicatively-independent *expanding* ergodic** map (we have only `A`; `×2` on `ℚ₃` is isometric); outputs **a.e.-point** normality, not measure-invariance, and a.e. ≠ the specified seed. | Nearest partial for AIU; shows the exact three deficits (expanding-pair, a.e., normality-not-invariance) a new lemma must remove. |
| **Algom–Baker–Shmerkin** (Adv. Math. 2022; Algom arXiv:2504.18192) `[PROVEN-in-lit]` | Rajchman (Fourier decay) ⟹ **a.e.-in-support** normal — the quantifier we cannot use for one specified point. | We already own the Rajchman input (`ν_{2/3}`, Varjú–Yu arXiv:2004.09358); the home for a *quantifier-upgrade* (a.e.-in-support → specified) program. |
| **Einsiedler–Fish** entropy-free semigroup rigidity (arXiv:0804.3586) `[PROVEN-in-lit]` | Removes the entropy hypothesis but needs a **positive-log-density** multiplicative semigroup; `⟨2,3⟩` has density 0. | Tells us the one entropy-free route is blocked for a *named* reason — closes a tempting shortcut. |
| **Effective equidistribution** (Lindenstrauss–Mohammadi arXiv:2202.11815; effective Ratner Annals 2025 arXiv:2208.02525; EMV arXiv:0708.4040) `[PROVEN-in-lit]` | All for **unipotent / semisimple / higher-rank / periodic** orbits, and a.e./ensemble — none for a single cyclic *hyperbolic* orbit. | The target *theory class* for sub-problem (d): a rank-1 amenable effective-equidistribution theory that does not yet exist. |
| **4 cross-field formalisms** (`BB6_CROSSFIELD_SCOUT.md`): non-Pisot diffraction; Siegel (p,q)-adic Wiener–Tauberian (arXiv:2007.15936); base-3/2 numeration (AFS; Charlier–Cisternino–Stipulanti); Berkovich/adelic equidist. (Favre–Rivera-Letelier) | Each restates the wall in a community's native language but lands on the **annealed / a.e. / first-moment / degree-≥2** tier; none reaches single-orbit frequency. | Candidate alternative homes / outreach communities. Aptest *shape*: non-Pisot diffraction (single-orbit autocorrelation = the right object). Most *unexplored*: Siegel (p,q)-adic (native single map). Neither expected to crack `(K)`. |

**Most plausible home (and why).** The **Einsiedler–Lindenstrauss leafwise-measure / adelic Ledrappier–Young program on
solenoids** (the apparatus around arXiv:2101.11120, with Rudolph–Johnson as its proven finisher). It is the unique home in
which: (a) the object *literally lives* — `A` is a proven rank-1 line in the rank-2 host acting on `X`; (b) both reductions
are native to it — ENT collapses by Ledrappier–Young to a single conditional-dimension positivity `γ_∞^{(2)}>0`, and AIU
is exactly a leafwise statement (`ℚ₃`-conditionals are `ℤ₃^*`-rotation-invariant); (c) the proven Rudolph–Johnson closes
the loop. The new tool would be a **low-entropy / neutral-direction extension** of the high-entropy method: an
invariance-propagation into a *central, zero-Lyapunov* direction driven by arithmetic (the product-formula coupling) rather
than by entropy. The literature has rank-2 rigidity and rank-1 non-rigidity but **no bridge** between a rank-1 sub-orbit and
the rank-2 invariance class — that absence is the empty spot the program names. `[OBSERVED — novelty]`

---

## 2. The central new object `[CONJECTURE / DEFINITION — research target]`

> **Effective unique ergodicity for a single specified orbit of a rank-1 amenable hyperbolic action, controlling a
> central / neutral direction by a non-spectral a-priori excursion estimate.**

Stated precisely as a target:

> **Target object.** Let `A` be a hyperbolic automorphism of a compact abelian S-arithmetic solenoid `X`, generating a
> **rank-1, amenable** group, and realized as a rational-slope line inside a rank-2 host `Φ⊃⟨A⟩` of commuting
> automorphisms. Let `x₀∈X` be a **specified** (algebraic, not generic) point with `A`-orbit empirical measures `μ_N`. The
> object is a theorem of the form:
>
> *the surplus invariance of every weak-* limit `μ` of `μ_N` — its `Φ`-invariance beyond `A`-invariance — is forced along
> the **neutral (zero-Lyapunov) coarse direction** of `Φ` by an **a-priori excursion / return-time estimate** on a proven
> arithmetic potential (`V=v₂(c−1)`), an estimate that is **non-spectral** (it cannot be a gap, by the coisometry no-go)
> and **non-structural** (it cannot be a coboundary/measure certificate, by the No-Structure theorem), yet is **uniform
> over the specified orbit** rather than a.e. / annealed.*

Three features make it genuinely new, each a proven constraint the object must respect:
- **Specified, not a.e.** — the seed `8` is `m_X`-null; the non-generic set has full Hausdorff dimension and full entropy
  (`BB6_NO_STRUCTURE_THEOREM.md`), so no measure/a.e. theorem can select it.
- **Neutral direction, no entropy to spend** — the AIU surplus is `×2` on `ℚ₃` (`|2|_3=1`, zero Lyapunov), where the
  high-entropy method is provably blind; the positive entropy `μ` carries lives transversally at `∞/2`.
- **Non-spectral, non-structural certificate** — the only contraction (`L_ann`) annihilates the odd-character subspace
  where the conclusion lives (coisometry, cross-scale Lyapunov ≡ 0); the only structural certificates are constant on the
  full feasible-measure set `M_feas`. The required estimate must read the orbit's *specific* arithmetic and live in the
  **conditional return-time law**, the one register not yet proven-closed-as-impossible (though the direct excursion
  attempt is closed — see §3(a)).

This is the precise replacement for "second independent direction." It is `[CONJECTURE]` as a theorem and `[PROGRAM]` as a
research target; nothing here proves it exists.

---

## 3. Ranked dependency roadmap — sub-problem | needs | nearest precedent | tractability | partial-yield

Dependency order: the kernel `(K)` follows from `AIU ∧ ENT` via proven Rudolph–Johnson; AIU and ENT are
`[PROVEN]`-logically-independent; (c) EUE is the same kernel in endogenous-cocycle dress; (d) is the ambient general theory
that would subsume all. Tractability is honest and relative — **all four are `(K)`-hard and generational to complete**; the
ranking is by *closeness to a publishable partial*, not to a solution.

### (a) AIU — Arithmetic Invariance Upgrade (host-invariance, neutral direction) `[CONJECTURE]`
- **Statement.** `(×2)_*μ = μ` (equivalently `⟨×2,×3⟩`-invariance; leafwise: the `A`-stable `ℚ₃`-conditionals are
  `ℤ₃^*`-rotation-invariant; seed-shift: `μ_8=μ_16`).
- **Needs.** A non-spectral invariance-propagation into a **neutral / zero-Lyapunov** direction, driven by the proven
  product-formula coupling `v₃(o_{j+1})=D_j−1` at the *measure* level (the "pointwise lock ≠ measure-level invariance"
  crossing is conceded as the open content).
- **Nearest precedent.** Host 1995 (second-map normality); EKL high-entropy / low-entropy method; Lindenstrauss AUE (Ann.
  Math. 163 (2006)). All require an expanding/entropy-carrying second direction — exactly what the neutral direction lacks.
- **Tractability.** **Hard.** The neutral-direction obstruction is proven to block every known invariance-upgrade
  mechanism (no entropy to spend); AIU is `[PROVEN]` strictly weaker than `(K)` but its only visible route is a transverse
  single-orbit equidistribution of `(K)`-comparable difficulty (`AIU_ATTACK.md` §3.4: AIU relocates, does not lower).
- **Partial-yield (publishable short of (K)).** **Yes, the strongest first partial.** (i) The leafwise equivalence
  AIU ⟺ `ℚ₃`-conditional `ℤ₃^*`-rotation-invariance `[PROVEN reduction]`; (ii) the **neutral-direction obstruction
  theorem** — a clean new result that the high-entropy method is structurally blind to a central coarse-Lyapunov direction
  — publishable as a measure-rigidity contribution in its own right; (iii) the conditional chain AIU ∧ ENT ⟹ (K) via
  proven Rudolph–Johnson; (iv) the named *bridge* (rank-1 sub-orbit → rank-2 host invariance) that the literature lacks.

### (b) ENT — positive 2-adic measure entropy `h_μ(M_2)>0` (equivalently `E[K²]<∞ / μ({1})=0`) `[CONJECTURE]`
- **Statement.** The empirical limit measure has positive entropy under `×2`; by Ledrappier–Young, `ENT ⟺ γ_∞^{(2)}>0`
  (one transverse conditional dimension positive); `(K)`-necessary (`h_μ=0 ⟹ (K)` false).
- **Needs.** A **quenched lower bound** on the conditional dimension `γ` for the specified seed — i.e. an a-priori bound on
  the return-time *second* moment `E[K²]` (or occupancy tail) that does not assume the D-statistics.
- **Nearest precedent.** Margulis–Ruelle / Pesin–Ledrappier–Young (upper bounds + SRB equality); Hochman entropy-increase
  (arXiv 2014); Bourgain–Lindenstrauss entropy of quantum limits (CMP 2003, entropy from extra symmetry).
- **Tractability.** **Hard, but the cleanest target** (collapses to one number `γ>0`). However the program shows: MR only
  *upper*-bounds `h_μ`; Pesin equality = SRB = Haar = `(K)`; the exponents are **frozen constants** so expansion is
  measure-blind (an atomic periodic orbit has the same positive `λ_∞,λ_2`); and the direct quenched excursion route on `V`
  is **closed as a sharp no-go** (`EXCURSION_SYNTHESIS.md`: every excursion drift is linear in entry-depth `K`, reading only
  `E[K]`; a heavy-tailed `E[K²]=∞` adversary matches all proven facts). So **`E[K²]` is the conclusion, not an input.**
- **Partial-yield.** **Yes (structural).** The Ledrappier–Young collapse `ENT ⟺ γ_∞^{(2)}>0`; the frozen-exponent /
  measure-blind-expansion observation (a sound new rigidity-of-exponents remark); the proven `(K)`-necessity (zero entropy
  refutes `(K)`); and the strict intermediate ladder `{avoids periodic} ⊊ {non-atomic} ⊊ {ENT} ⊊ {(K)}` with each gap
  named. No lower bound on `γ` is in reach.

### (c) Endogenous-cocycle unique ergodicity (EUE) `[CONJECTURE]`
- **Statement.** For the closed-loop carry cocycle `s_{n+1}=U(s_n,β_n)`, `β_n=bit_k(c_n)`, the odd-character feedback
  `Inj_a(N)→0` for every odd `a` and scale `k` (⟺ `(K)`).
- **Needs.** A bound on `Inj(k)` that uses a property *specific to the endogenous input* `β_n=bit_k(c_n)` — the
  self-reference — not the spectral gap or the automaton.
- **Nearest precedent.** Self-consistent dynamical systems (arXiv:1909.04484); RWRS / `(T,T⁻¹)`; propagation of chaos for a
  single deterministic trajectory (no existing theorem).
- **Tractability.** **Very hard.** Proven no-go: `L_ann` annihilates the odd-character subspace where the conclusion lives;
  the cross-scale renormalization cocycle `R_k` is a **coisometry** ⟹ operator-norm Lyapunov ≡ 0 ⟹ no spectral/operator-norm
  route can ever work; an adversary with identical `(gap, automaton)` realizes feedback `≈1`. Every natural escape
  (assume balance / bootstrap scale `k→k+1` / even-block gap) is `[PROVEN]` circular.
- **Partial-yield.** **Yes (durable no-go).** The **exact seam identity** `((I−L_ann^*)π_N)(f)=Feedback_N(f)+O(1/N)`
  (upgrades the endogeneity recursion from measured to an exact operator identity); the **coisometry no-go**; the clean
  Open Lemma isolating the single residue. These are publishable as a sharp impossibility result for spectral methods on
  self-referential cocycles.

### (d) Rank-1 amenable effective-equidistribution theory `[PROGRAM]`
- **Statement.** A general theorem certifying a *single specified* orbit of a rank-1, amenable, hyperbolic S-arithmetic
  automorphism is generic (under a Diophantine input on `log_2 3`, a Margulis-function / non-escape-of-mass argument, or a
  new mechanism).
- **Needs.** The central new object of §2, built into a theory — the missing bridge between Gibbs–Markov / homogeneous
  a.e.-equidistribution and a single computable trajectory.
- **Nearest precedent.** BFLM (non-abelian); effective Ratner / Lindenstrauss–Mohammadi (unipotent/higher-rank). Both
  violate the amenable-rank-1 hypothesis at the root.
- **Tractability.** **Generational / empty toolbox** (confidence HIGH ~85% that no existing framework contains it;
  cross-field-confirmed across ~17 fields). This is the capstone, not a near-term target.
- **Partial-yield.** The **framework / empty-toolbox classification paper** itself (the object does not exist, with the
  precise reason it falls between the two toolboxes) — already a durable contribution (§4).

**Which yields a publishable partial first.** **(a) AIU** — specifically the **neutral-direction obstruction theorem**
plus the leafwise reduction and the conditional `AIU ∧ ENT ⟹ (K)` chain. It is a genuinely new, self-contained
measure-rigidity result (the high-entropy method's blindness to a central coarse-Lyapunov direction) that does not require
solving `(K)`, and it names a bridge the literature has no entry for. (b)'s Ledrappier–Young collapse and (c)'s coisometry
no-go are close seconds and are independently publishable as the entropy-side reduction and the spectral-impossibility
result respectively.

---

## 4. Durable intermediate contributions (stand regardless of `(K)`)

These are the program's record-grade outputs — true and publishable whether or not `(K)` is ever resolved:

1. **The reduction-chain / framework paper** `[PROVEN, machine-verified]` (`BB6_FRAMEWORK_PACKAGE.md` §2): Antihydra
   non-halt ⟺ even-density ≥ 1/3 ⟺ `mean D ≥ 3/2` ⟺ single-orbit equidistribution mod `2^k` ⟺ `(K)` = Mahler 3/2 / AEV
   Conj 1.6 at `α=8`. A clean placement of a Busy-Beaver halting problem inside analytic number theory.
2. **The obstruction dichotomy** `[PROVEN core + organizing principle]` (`BB6_OBSTRUCTION_DICHOTOMY.md`): the proven/open
   boundary across ~20 routes is the single **topological-closure-determined vs Haar-selecting** boundary
   (topological-entropy/measure-entropy split). Explains in one principle why every route stops at the same place.
3. **The No-Structure-Only-Selection theorem** `[PROVEN]` (`BB6_NO_STRUCTURE_THEOREM.md`): no certificate from the
   bounded-residue-coboundary (C1), all-orbits/specification (C2), or measure-level/annealed (C3) registers — nor the
   unbounded magnitude-aware / adelic sub-action extension — can prove `(K)`; the seed gets the same verdict as the genuinely
   halting fixed point `o=1`. The obstruction is proven structural, not a tooling gap.
4. **The solenoid placement** `[PROVEN structure + CONJECTURE bridge]` (`BB6_FRAMEWORK_PACKAGE.md` §5): `A` as a rank-1 line
   in the rank-2 host; the two-gap decomposition `(K) ⟸ AIU ∧ ENT` via proven Rudolph–Johnson; AIU/ENT logical
   independence; the novelty statement (the missing rank-1→rank-2 bridge).
5. **The coisometry no-go + exact seam identity** `[PROVEN]` (`ENDOGENOUS_UE_BUILD.md`, `NEWMATH_SYNTHESIS.md` §3): the
   cross-scale renormalization cocycle is a coisometry ⟹ operator-norm Lyapunov ≡ 0 ⟹ no spectral route across scales; a
   sharp impossibility for spectral methods on self-referential cocycles, plus the new vocabulary (endogenous cocycle /
   self-consistent measure / EUE) distinct from self-consistent dynamics and RWRS.
6. **The frozen-exponent / measure-blind-expansion remark** `[PROVEN]` (`ENT_PESIN_MARGULIS.md`): on an affine solenoid
   automorphism the Lyapunov exponents are constants of the map, so positive expansion forces nothing about entropy — a
   clean rigidity-of-exponents observation with an explicit atomic counterexample.
7. **The banked unconditional partials** `[PROVEN / PROVEN-in-lit]` (`BB6_FRAMEWORK_PACKAGE.md` §6): `#even(n) ≥ 0.89 log n`;
   top-`Θ(log N)`-digit equidistribution; `ν_{2/3}` Rajchman (Varjú–Yu) and `dim ν_{2/3}=1` (Hochman); subword-complexity
   floor `p(ℓ)≥1.71ℓ`; the strict intermediate ladder; and the **first-moment-free / second-moment-hard** telescoping
   characterization (the concrete arithmetic face of the dichotomy).
8. **The empty-toolbox / cross-field robustness verdict** `[OBSERVED, HIGH confidence]` (`EMPTY_TOOLBOX_QUESTION.md`,
   `BB6_CROSSFIELD_SCOUT.md`): "specified-orbit genericity for a rank-1 amenable hyperbolic system" is unpopulated across
   ~17 fields, each failing for its own structural reason — a strong robustness check and the right framing for expert
   outreach.

---

## 5. Honest timeline framing (generational)

The resolution of `(K)` is **generational**, not one-idea-away (confidence MODERATE that the gap is permanent vs.
one-good-idea-away; HIGH that no current framework contains the tool). The realistic multi-year structure:

- **Near term (durable, now):** publish the framework paper, the obstruction dichotomy, the No-Structure theorem, the
  coisometry no-go, and the banked partials — these stand regardless and are the program's record-grade contribution.
- **Mid term (first new-math partials):** the AIU neutral-direction obstruction theorem and leafwise reduction (a); the
  ENT Ledrappier–Young collapse (b); the endogenous seam identity (c) — each a publishable advance that sharpens, but does
  not close, the kernel. These are the plausible "partial result short of `(K)`" outputs.
- **Long term (the bridge):** the rank-1 amenable effective-equidistribution theory (d) and the central new object (§2) —
  the missing bridge between homogeneous a.e.-equidistribution and a single computable trajectory. This is the capstone and
  is open-ended.

Every concrete sub-problem funnels to the same irreducible statement — single-orbit equidistribution of
`D_n=v₂(3c_n−1)` — and every proven no-go (structural, spectral, magnitude-aware/adelic, quenched-excursion) leaves the
proven facts *consistent with both `(K)` and its negation*. Only the orbit's specific arithmetic decides, and computing it
is solving Mahler 3/2 / AEV.

**No machine decided. No label upgraded.**
