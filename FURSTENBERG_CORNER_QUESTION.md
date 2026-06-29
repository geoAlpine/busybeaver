# Is the Antihydra corner a tractable piece of Furstenberg ×2,×3? — literature survey + expert question (2026-06-29)

> **[SOUNDNESS CORRECTION 2026-06-29 — read first].** This note's central premise "the limit measure plausibly has
> `h_μ(×2)=0`" is **numerically REFUTED and retracted.** Direct computation (`scratchpad/subword.py`) shows the parity
> sequence has **FULL subword complexity `p(ℓ)=2^ℓ`** (exact for ℓ≤13; ℓ≥14 limited only by sample size), so topological
> entropy `= log2 > 0`, and block entropies → log2 — the orbit looks **positive-entropy / Haar-like**, the opposite of
> zero. The repo's `p(ℓ)≥1.71ℓ` is only a *lower* bound and does **not** imply entropy 0 (this note, and an earlier draft
> of `NEWMATH_SYNTHESIS.md`, mis-read it). **Corrected status:** `h_μ=0` is the **(K)-FALSE** regime (Haar has positive
> entropy), so it cannot be assumed; the live reduction is **(K) ⟺ AIU ∧ `h_μ(M₂)>0`**, and with both the **proven**
> Rudolph–Johnson gives Haar. So this is a bridge to a *proven* theorem needing two open (K)-hard inputs — NOT a
> "zero-entropy Furstenberg corner." The §0 dichotomy-lemma claim that Φ-invariance alone forces Haar without entropy is
> ALSO suspect (entropy-free Φ-rigidity is Furstenberg's open conjecture) and should be treated as [OPEN], not [PROVEN].
> The literature survey (§4) and the expert-question skeleton below remain useful once re-framed around the corrected
> two inputs (AIU + positive entropy). See `LIMIT_MEASURE_ENTROPY.md` for the full correction.

*LITERATURE + WRITEUP task. Decides whether the placement of (K) inside the Furstenberg/Rudolph–Johnson
×2,×3 program (`NEWMATH_SYNTHESIS.md`, `NEWMATH_ADELIC_RIGIDITY.md`) lands in a **tractable corner** or in
the **open core of Furstenberg's conjecture**, and crafts the sharpest expert question. SOUNDNESS PARAMOUNT:
every claim labelled `[PROVEN]` (machine-verified in repo) / `[PROVEN-in-lit]` / `[OBSERVED]` / `[OPEN]`.
No claim to prove (K). WebSearch available this run; citations in §4. NOT committed.*

---

## 0. The object, restated for a rigidity expert (one paragraph, all PROVEN)

`X = (ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` is the (2,3)-adic solenoid; `m_X` = Haar. `M_2,M_3 ∈ Aut(X)` are commuting
hyperbolic automorphisms with dilations `(2,½,1)` and `(3,1,⅓)`; they generate a **rank-2** abelian group
`Φ=⟨×2,×3⟩` (`2,3` mult. independent). `[PROVEN]` The Antihydra map is the single **anti-diagonal** line
`A = M_3M_2⁻¹ = ×(3/2)`, dilations `(3/2,2,⅓)`, hyperbolic, product 1. `[PROVEN]` The seed `8∈ℤ[1/6]`
gives a single `A`-orbit; `μ_N=(1/N)Σ_{n<N}δ_{Aⁿ8}` and any weak-* limit `μ` is `A`-invariant. `[PROVEN]`
**(K)** (= Mahler 3/2 / AEV Conj 1.6 at α=8 = Antihydra non-halt, via the machine-verified reduction chain
`SESSION_2026-06-29_AEV_CORE.md`) ⟺ `μ = m_X` for every limit (the seed is `A`-generic). Two PROVEN
structural facts frame the problem:
- **Dichotomy lemma `[PROVEN]`** (Berend topological rigidity on the solenoid + 2-adic periodic-repulsion):
  the **only** gap between `A`-invariance and Haar is the upgrade **`A`-invariant ⟹ `Φ`-invariant** (AIU); a
  `Φ`-invariant ergodic limit is forced to be Haar or a `μ`-null finite set, the latter excluded for `8`.
- **Non-Pisot, no atomic obstruction `[PROVEN]`**: `|3/2|₂=2>1` (2-adic place expands); `R*:ξ↦(3/2)ξ` on
  `ℤ[1/6]` has no nonzero periodic point ⇒ no atomic/Pisot/sofic `A`-fixed point; the diagonal is
  non-automatic; the annealed transducer has spectral gap ½ with unique uniform (Haar) fixed point.

So (K) reduces — with everything else `[PROVEN]` or `[PROVEN-in-lit]` — to **two questions about one explicit,
transducer-generated, non-Pisot, `A`-invariant measure**:
> **(a)** is the entropy `h_μ(M_2)` of the orbit's empirical limit measure **positive or zero**?
> **(b)** is `μ` invariant under the full host `Φ=⟨×2,×3⟩` (the AIU upgrade), or only under `A`?

---

## 1. Literature table — which rigidity result fires, and the missing hypothesis

| Result | Citation | What it proves | Applies to our `μ`? | Missing hypothesis (exact) |
|---|---|---|---|---|
| **Rudolph** ×2,×3 + entropy | Rudolph, *×2 and ×3 invariant measures and entropy*, ETDS **10** (1990) 395–406 | `(×2,×3)`-invariant, ergodic, **`h>0`** ⇒ Lebesgue; non-Lebesgue ⇒ both maps zero-entropy & a.s. invertible | **No** | needs (i) **joint `×2,×3`-invariance** [we have only `A`] and (ii) **`h_μ(M_2)>0`** [plausibly 0] |
| **Johnson** non-lacunary semigroup | Johnson, *Measures on the circle invariant under mult. by a nonlacunary subsemigroup*, Israel J. **77** (1992) 211–240 | same conclusion for any non-lacunary multiplicative semigroup with one positive-entropy element | **No** | same two: joint multi-invariance + positive entropy |
| **Berend** topological rigidity | Berend, *Multi-invariant sets on tori* (1983); solenoid form (see 2101.11120) | totally-irreducible, non-virtually-cyclic, hyperbolic `ℤ^d`-action ⇒ every orbit finite or dense | **Used** (gives the dichotomy lemma) | topological only; gives no measure ⇒ cannot reach Haar |
| **Einsiedler–Lindenstrauss** commuting autos, solenoids | *Rigidity properties for commuting automorphisms on tori and solenoids*, arXiv:2101.11120, ETDS | positive-entropy measure rigidity for higher-rank abelian auto actions on **solenoids** | **No** | **positive entropy** for the rank-2 action; and again needs `Φ`-invariance, not `A`-invariance |
| **Einsiedler–Fish** (removes entropy!) | Einsiedler–Fish, *Rigidity of measures invariant under a multiplicative semigroup of polynomial growth on 𝕋*, arXiv:0804.3586 | semigroup-invariant ergodic measure ⇒ Lebesgue or finite, **no entropy hypothesis** | **No** | needs the acting semigroup to have **positive lower logarithmic density**; `⟨2,3⟩` (and a fortiori `⟨3/2⟩`) has **density 0** — exactly the hypothesis we fail |
| **Host** pointwise normality | Host, *Nombres normaux, entropie, translations*, Israel J. **91** (1995) 419–428 | `T_p`-invariant ergodic, **`h>0`**, `gcd(p,m)=1` ⇒ `μ`-a.e. `x` normal in base `m` | **No** | positive entropy; and **a.e.-in-support**, not our single specified seed |
| **Lindenstrauss** AUE / QUE | *Invariant measures and arithmetic unique ergodicity*, Ann. of Math. **163** (2006) 165–219 | positive-entropy + recurrence classification on `Γ\SL₂×L` | **No** | positive entropy + a non-abelian (`SL₂`) acting direction; ours is abelian rank-1 |
| **Bourgain–Lindenstrauss** entropy of quantum limits | *Entropy of quantum limits*, CMP (2003) | arithmetic QUE limits have `h≥2/9>0` | **No** | produces entropy from Hecke symmetry; no Hecke/extra symmetry on a single `A`-orbit |
| **Hochman–Shmerkin** local entropy averages | *Local entropy averages and projections of fractal measures*, Ann. of Math. **175** (2012); *Equidistribution from fractals* | `×m,×n`-invariant **fractal** `μ` (or `+t` push) ⇒ projections/normality conclusions; proves a Furstenberg dimension conjecture | **Partial / wrong quantifier** | conclusions are **`μ`-a.e.** normality (a.e.-in-support); needs the measure given a priori as `×m`-invariant fractal — not a single `A`-orbit's empirical limit; gives no `Φ`-invariance upgrade |
| **Shmerkin** `L^q`, intersection conj. | *On Furstenberg's intersection conjecture, self-similar measures, `L^q` norms*, Ann. of Math. **189** (2019) 319–391 | settles Furstenberg's **dimension/intersection** conjecture for `×p,×q`-invariant **sets** | **No** | a statement about **dimensions of invariant sets**, not classification of a single invariant measure; no Haar conclusion |
| **Wu** intersection conjecture | *A proof of Furstenberg's conjecture on intersections of ×p- and ×q-invariant sets*, Ann. of Math. **189** (2019) 707–751 | `dim((uA+v)∩B) ≤ max{0,dimA+dimB−1}`, `log p/log q ∉ ℚ` | **No** | same: invariant **sets**, dimension bound, not measure ⇒ Haar |
| **Algom–Baker–Shmerkin** | *On normal numbers and self-similar measures*, Adv. Math. (2022); Algom exposition arXiv:2504.18192 | **Rajchman** (Fourier decay, no rate) ⇒ `μ`-a.e. point normal to all bases | **Partial / wrong quantifier** | **a.e.-in-support**, not the specified seed; and gives normality (a real-place statement), not `Φ`-measure-invariance |
| **Furstenberg conjecture, zero-entropy core** | Furstenberg (1967); see survey Tal, arXiv:2110.05989 | *conjectured*: nonatomic `×2,×3`-invariant `μ` ⇒ Lebesgue | **This is the regime we land in** | **OPEN.** Nonatomic **zero-entropy** non-Lebesgue `×2,×3`-invariant measures **provably exist** (Host's criterion regime); so `Φ`-invariance alone does **not** force Haar |

**Reading of the table.** Every theorem that concludes "= Haar/Lebesgue" requires **positive entropy** (Rudolph,
Johnson, Host, E–L 2101.11120, Lindenstrauss 2006) **or** a large/non-abelian acting group (E–Fish needs
positive-density semigroup; Lindenstrauss/BFLM need non-abelian). The one result that *removes* the entropy
hypothesis (Einsiedler–Fish) fails on us for a sharp, named reason: `⟨2,3⟩` is a **logarithmic-density-zero**
semigroup. The fractal/`L^q` results (Hochman–Shmerkin, Shmerkin, Wu, Algom–Baker–Shmerkin) either bound
**dimensions of sets** (not classify a measure) or conclude **a.e.-in-support** normality (the quantifier we
cannot use for the single seed `8`). And the regime we actually fall into — **nonatomic zero-entropy
`×2,×3`-invariant measure** — is precisely the **open core of Furstenberg's conjecture**, where non-Lebesgue
examples are known to exist, so even *full* host-invariance would not by itself give Haar.

---

## 2. Verdict — tractable corner vs full-Furstenberg-hard (with confidence)

> **Verdict: FULL-FURSTENBERG-HARD, in fact the *open core* of it. Confidence HIGH (~85%).**

Reasoning, layered by the two questions (a),(b):

1. **Even granting AIU (question (b)) for free, entropy decides everything, and the evidence points to zero.**
   The Antihydra symbolic orbit has **linear subword complexity** `p(ℓ) ≥ 1.71ℓ` ⇒ **topological entropy 0**
   `[PROVEN, LIMIT_THEOREM]`; any weak-* limit `μ` therefore plausibly has `h_μ(M_2)=0` `[OBSERVED — not proven;
   this is question (a)]`. If `h_μ(M_2)=0`, the host-invariant measure lands **exactly** in the zero-entropy
   case that Rudolph (1990) explicitly **leaves open** and that Einsiedler–Fish cannot reach (wrong-density
   semigroup). In that regime nonatomic non-Lebesgue `×2,×3`-invariant measures **provably exist**
   `[PROVEN-in-lit]`, so `Φ`-invariance is **demonstrably insufficient** — the problem is not "apply
   Rudolph–Johnson," it is "solve the part of Furstenberg that Rudolph–Johnson was invented to avoid."

2. **AIU (question (b)) is itself unproven and is the program's stated single gap.** The dichotomy lemma
   `[PROVEN]` shows AIU is *exactly* the missing step, but supplies no proof; the tautology barrier
   (T1)–(T2) `[PROVEN, NEWMATH_ADELIC_RIGIDITY §3.3]` shows the per-orbit ×2↔×3 lock is **codim-1 /
   pointwise** and cannot, by itself, deliver measure-level `×3`-invariance. So question (b) is genuinely open
   and is not implied by any structure proven to date.

3. **The two open questions are not independent and there is no known dependency that helps.** If `h_μ(M_2)>0`
   (question (a) "positive") *and* AIU holds, then E–L 2101.11120 / Rudolph finish — but Rudolph's own theorem
   says a non-Lebesgue host-invariant `μ` **must** be zero-entropy, so the "positive-entropy + host-invariant"
   branch is *self-defeating* unless it already is Haar. Thus the realistic live branch is precisely
   (a)=zero ∧ (b)=holds = **zero-entropy Furstenberg**, the open core.

**Why not "tractable":** there is **no published theorem** — surveyed across Rudolph, Johnson, Host,
Lindenstrauss, Einsiedler–Lindenstrauss/Fish, Hochman–Shmerkin, Shmerkin, Wu, Berend — that classifies a
**single zero-entropy `×2,×3`-invariant (let alone only `A`-invariant) measure on a non-Pisot solenoid** as
Haar. The corner inherits both open problems of the field at once (the zero-entropy Furstenberg case **and**
single-specified-orbit genericity).

**Residual (~15%) — the honest case *for* tractability.** The Antihydra measure is **not** a generic
zero-entropy measure; it is **explicit**, with three structural assets a generic zero-entropy `×2,×3` measure
lacks:
- **Fourier decay / Rajchman.** The carry (second-diagonal) marginal is the Rajchman measure `ν_{2/3}`
  `[PROVEN, SECOND_DIAGONAL_RAJCHMAN]` — Fourier decay is *exactly* the input of the Algom–Baker–Shmerkin
  normality route; if it could be promoted from the carry to `μ` itself it would attack normality (though
  still at the a.e.-in-support, not specified-seed, quantifier).
- **Explicit transducer + non-Pisot spectrum.** `R=×(3/2)` is a concrete carry-coupled ×3-adder with proven
  annealed gap ½, purely Lebesgue spectrum, and **no** atomic/Pisot/sofic fixed point `[PROVEN]` — i.e. the
  one obstruction Furstenberg's zero-entropy examples rely on (a finite-state/odometer skeleton) is provably
  **absent** here.
- **S-adic / linear-complexity classification.** Linear-complexity subshifts have at most countably many
  ergodic measures and are partially rigid (Cyr–Kra; Donoso–Durand–Maass–Petite circle) `[PROVEN-in-lit]` —
  a finite-data structure theory a generic measure lacks.

But **no current theorem converts any of these into the AIU upgrade or into Haar without positive entropy.**
They sharpen the *target* (and rule out the standard zero-entropy counterexample mechanism), without closing
it. Hence the verdict stands at full-Furstenberg-hard, with the structure as the only plausible lever and the
explicit reason the generic counterexamples don't directly apply.

**Nearest applicable rigidity result:** Rudolph (1990) / Einsiedler–Lindenstrauss solenoid form
(arXiv:2101.11120). **Missing hypothesis:** *positive `M_2`-entropy of `μ`* (plausibly false here) **and**
*joint `⟨×2,×3⟩`-invariance* (the unproven AIU; we have only `A`-invariance). The lone entropy-free theorem
(Einsiedler–Fish) is blocked because `⟨2,3⟩` has **logarithmic density 0**.

---

## 3. The expert question (≈1.5 pp; for Einsiedler, Lindenstrauss, Host, Hochman, Shmerkin, and the AEV authors)

> **Subject.** A single, explicit, transducer-generated, *non-Pisot* `×(3/2)`-invariant measure on the
> (2,3)-adic solenoid: is its entropy positive or zero under `×2`, and — if zero — is the `×2,×3`-invariance
> upgrade we need a tractable special case, or exactly the open core of Furstenberg's conjecture?
>
> **What is PROVEN (so you can trust the reduction before reading the ask).**
> Let `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, `Φ=⟨M_2,M_3⟩` the rank-2 group of commuting hyperbolic automorphisms
> (dilations `(2,½,1)`,`(3,1,⅓)`), and `A=M_3M_2⁻¹=×(3/2)` the anti-diagonal rank-1 line (dilations
> `(3/2,2,⅓)`). For the explicit rational seed `8∈ℤ[1/6]` we study the empirical measures
> `μ_N=(1/N)Σ_{n<N}δ_{Aⁿ8}` and any weak-* limit `μ` (`A`-invariant by Krylov–Bogolyubov). A machine-verified
> chain reduces a Busy-Beaver / Collatz-type halting problem (Antihydra) — equivalently Mahler's 3/2 problem
> and the AEV rational-base normality conjecture (arXiv:2510.11723) at α=8 — to: **`μ=m_X` (Haar) for every
> limit `μ`.** We have proven, unconditionally:
> 1. **Dichotomy.** Via Berend topological rigidity on `X` plus 2-adic periodic-repulsion, the **only** gap
>    between `A`-invariance and Haar is the upgrade `A`-invariant ⟹ `Φ`-invariant. A `Φ`-invariant ergodic
>    limit is Haar or supported on a finite (`μ`-null, excluded) set.
> 2. **No atomic/Pisot obstruction.** `|3/2|₂=2>1`; `ξ↦(3/2)ξ` on `ℤ[1/6]` has no nonzero periodic point ⇒
>    `μ` has no atomic/Pisot/sofic `A`-fixed component; the generating sequence is non-automatic; the annealed
>    ×3-adder transducer has spectral gap ½ and unique uniform (Haar) fixed point.
> 3. **Tautology barrier.** The per-orbit ×2↔×3 coupling `v₃(o_{n+1})=v₂(3o_n−1)−1` is exact but codim-1 /
>    pointwise — it pins first moments, not the distribution; it does **not** by itself yield measure-level
>    `×3`-invariance.
>
> **Where every known method breaks (lead with this).**
> - **Rudolph/Johnson/Host/E–L(2101.11120)/Lindenstrauss(2006)** all conclude Haar only under **positive
>   entropy** (and joint `×2,×3`-invariance, not the `A`-invariance we actually have). Our orbit has **linear
>   subword complexity** `p(ℓ)≥1.71ℓ`, hence **topological entropy 0**, so we expect `h_μ(M_2)=0`.
> - **Einsiedler–Fish (0804.3586)** removes the entropy hypothesis — but needs a **positive-density**
>   multiplicative semigroup; `⟨2,3⟩` has **logarithmic density 0**, so it does not apply.
> - **Hochman–Shmerkin / Shmerkin / Wu / Algom–Baker–Shmerkin** give either **dimension** statements about
>   invariant **sets**, or **a.e.-in-support** normality from Fourier decay — never the classification of a
>   single given measure as Haar, and never the specified-seed quantifier.
> - So we land in the **nonatomic zero-entropy `×2,×3` regime**, the part of Furstenberg's conjecture that is
>   **open** and where non-Lebesgue invariant measures are **known to exist** — i.e. `Φ`-invariance alone is
>   provably insufficient.
>
> **Q-(a) [entropy].** Is the empirical limit measure `μ` of this *specific* `A`-orbit **zero-entropy** under
> `M_2` (as the linear complexity strongly suggests), or could the carry inject positive 2-adic fibre entropy?
> A proof either way is decisive: positive entropy + the upgrade below ⇒ Rudolph–Johnson ⇒ Haar; zero entropy
> sends us to Q-(b).
>
> **Q-(b) [the AIU upgrade, our only gap].** For this **explicit, transducer-generated, non-Pisot**,
> zero-entropy, `A`-invariant `μ`, is the upgrade `A`-invariant ⟹ `⟨×2,×3⟩`-invariant — and thence Haar —
> (i) **provable** by exploiting the explicit structure [Rajchman/Fourier decay of the carry marginal
> `ν_{2/3}`; the proven *absence* of any Pisot/odometer/finite-state skeleton that the standard zero-entropy
> counterexamples require; the S-adic / countable-ergodic-measure structure of linear-complexity systems], or
> (ii) **exactly as hard as Furstenberg's `×2,×3` conjecture in the zero-entropy case** (and thus not a
> shortcut)? Concretely: does the proven non-Pisot spectrum (no atomic/sofic fixed point) plus Fourier decay
> rule out the Host-type zero-entropy non-Lebesgue measures for *this* `μ`, or is there a transducer-generated
> zero-entropy `×2,×3`-invariant measure that is **not** Haar, killing the route?
>
> **Q-(c) [framing].** Is "**force a single specified `×(3/2)`-orbit's zero-entropy empirical limit measure on
> a non-Pisot solenoid to be Haar**" a recognised tractable sub-problem (under a Diophantine input on
> `log₂3`, a scenery-flow/CP-process argument à la Hochman–Shmerkin, a Fourier-dimension/Rajchman criterion,
> or otherwise), or is it a genuinely empty spot inheriting **both** open difficulties of the field at once —
> the zero-entropy Furstenberg case **and** single-specified-orbit genericity?
>
> **A sharp "no — here is the transducer-generated zero-entropy counterexample" is as valuable as a "yes — the
> Rajchman/non-Pisot structure suffices, see X." A pointer is plenty; if the reduction is malformed, the most
> useful reply is how you would reformulate it.**

**One-sentence sharpest form.** *Does the orbit of `8` under `×(3/2)` on the (2,3)-adic solenoid have an
empirical limit measure of zero entropy under `×2`, and if so, is upgrading its `×(3/2)`-invariance to
`⟨×2,×3⟩`-invariance — our single proven gap — achievable from the measure's explicit Rajchman/non-Pisot
transducer structure, or is it exactly Furstenberg's zero-entropy `×2,×3` conjecture in disguise?*

---

## 4. Sources

- D. J. Rudolph, *×2 and ×3 invariant measures and entropy*, Ergodic Th. Dynam. Sys. **10** (1990) 395–406. https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/2-and-3-invariant-measures-and-entropy/64243AD8323B37089540F911F8CC77EB
- A. S. A. Johnson, *Measures on the circle invariant under multiplication by a nonlacunary subsemigroup of the integers*, Israel J. Math. **77** (1992) 211–240. https://link.springer.com/article/10.1007/BF02808018
- B. Host, *Nombres normaux, entropie, translations*, Israel J. Math. **91** (1995) 419–428. https://link.springer.com/article/10.1007/BF02761660
- E. Lindenstrauss, *Invariant measures and arithmetic unique ergodicity*, Ann. of Math. **163** (2006) 165–219. https://annals.math.princeton.edu/2006/163-1/p03
- J. Bourgain, E. Lindenstrauss, *Entropy of quantum limits*, Comm. Math. Phys. (2003). https://math.huji.ac.il/~elon/Publications/pos_entropy.pdf
- M. Einsiedler, A. Fish, *Rigidity of measures invariant under the action of a multiplicative semigroup of polynomial growth on 𝕋*, arXiv:0804.3586. https://arxiv.org/pdf/0804.3586
- *Rigidity properties for commuting automorphisms on tori and solenoids* (E–L solenoid measure rigidity), arXiv:2101.11120, ETDS. https://arxiv.org/pdf/2101.11120
- D. Berend, *Multi-invariant sets on tori*, Trans. AMS (1983) [topological rigidity, solenoid form via 2101.11120].
- M. Hochman, P. Shmerkin, *Local entropy averages and projections of fractal measures*, Ann. of Math. **175** (2012) 1001–1059. https://arxiv.org/abs/0910.1956 ; *Equidistribution from fractal measures*, Invent. Math. (2015). https://arxiv.org/pdf/1302.5792
- P. Shmerkin, *On Furstenberg's intersection conjecture, self-similar measures, and the L^q norms of convolutions*, Ann. of Math. **189** (2019) 319–391. https://arxiv.org/abs/1609.07802
- M. Wu, *A proof of Furstenberg's conjecture on the intersections of ×p- and ×q-invariant sets*, Ann. of Math. **189** (2019) 707–751. https://arxiv.org/abs/1609.08053
- A. Algom, S. Baker, P. Shmerkin, *On normal numbers and self-similar measures*, Adv. Math. (2022); A. Algom, *Recent progress on pointwise normality of self-similar measures*, arXiv:2504.18192. https://arxiv.org/pdf/2107.02699 , https://arxiv.org/pdf/2504.18192
- M. Einsiedler, E. Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case and the general low-entropy method*, JMD (2008); *Symmetry of entropy in higher rank diagonalizable actions*, arXiv:1803.07762; *Recent progress on rigidity ...*, arXiv:2101.11114.
- M. Tal, *Furstenberg's Times 2, Times 3 Conjecture (a short survey)*, arXiv:2110.05989. https://arxiv.org/pdf/2110.05989
- V. Cyr, B. Kra and the Donoso–Durand–Maass–Petite circle on linear-complexity subshifts (countably many ergodic measures, partial rigidity, S-adic structure): arXiv:2305.03096, arXiv:2412.08884, arXiv:1902.08645.
- M. Andrieu, S. Eliahou, L. Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723.
- Repo: `NEWMATH_SYNTHESIS.md`, `NEWMATH_ADELIC_RIGIDITY.md`, `NEWMATH_DIAGONAL_RENORM.md`,
  `SESSION_2026-06-29_AEV_CORE.md`, `EMPTY_TOOLBOX_QUESTION.md`, `LIMIT_THEOREM.md`,
  `SECOND_DIAGONAL_RAJCHMAN.md` (carry marginal = `ν_{2/3}` Rajchman, `[PROVEN]`).

*Convention: repo facts are machine-verified in exact integer/2-adic arithmetic (program soundness policy);
literature labelled `[PROVEN-in-lit]` / `[OPEN]`. No labels upgraded; (K) remains `[OPEN]` = Mahler 3/2 /
AEV / a non-Pisot, zero-entropy corner of Furstenberg ×2,×3.*

**No machine decided. No label upgraded.**
