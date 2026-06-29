# The empty-toolbox question — does the object Antihydra needs already exist in some field? (2026-06-29)

*Recommended move #4 from `WEAPONS_AUDIT_2026-06-29.md` §6. This is a LITERATURE / FRAMING task, not a proof
attempt. Goal: decide whether the new-math object the BB(6) program requires is **genuinely new mathematics**
("empty toolbox spot") or an **existing framework under a different name** ("a new bridge"), and craft the
sharpest expert question. SOUNDNESS: claims labelled [PROVEN-in-lit] / [OBSERVED] / [OPEN]; citations precise;
zero false proofs. WebSearch was available this run (US); results captured in §1 and Sources. NOT committed.*

---

## 0. The needed object (the program's own spec, restated for an outside reader)

> **NEEDED:** effective equidistribution (or even just a one-sided positive-density bound) for a **single
> specified** orbit `{Aⁿx₀}` of a **rank-1 expanding map `×(3/2)`**, where `x₀` is the explicit algebraic seed
> (`8`, or `1`). Equivalently (proven equivalent in `TRACTABILITY_MAP.md` / `EXPERT_ASK_HOMOGENEOUS.md`):
> **specified-orbit genericity** for the hyperbolic automorphism `A(x)=(3/2)x` of the S-arithmetic solenoid
> `X = (ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, whose acting group `ℤ[1/6]⋊⟨3/2⟩` is **amenable** (solvable), with dilations
> `|3/2|_∞=3/2`, `|3/2|₂=2` (expanding), `|3/2|₃=1/3` (contracting) — no neutral direction.

**Claimed empty-toolbox locus (`amenable ∩ hyperbolic`):** amenability blocks the rigidity engines
(Ratner / Einsiedler–Lindenstrauss / BFLM need rank ≥ 2 or a non-amenable/unipotent direction); hyperbolicity
(exponential divergence) blocks the rotation/Weyl/unique-ergodicity engines. The two halves of the toolbox cover
disjoint regimes and this object sits in the gap between them.

---

## 1. Literature findings (WebSearch available this run; precise citations)

**The named special-case anchors are confirmed alive and exactly on our two axes:**

- **AEV — Andrieu, Eliahou & Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723
  (Oct 2025, 26 pp).** [OPEN conjecture, attribution now CONFIRMED — previously flagged "unverified" in
  `DERANDOMIZATION_LITERATURE.md`.] Conjecture: in the Akiyama–Frougny–Sakarovitch rational-base `p/q` system,
  **every minimal and maximal word is normal over an appropriate subalphabet**. The authors explicitly list as
  consequences: existence of Z-numbers (Mahler 1968), Z_{p/q}-numbers (Flatto 1992), triple expansions in base
  `p/q` (Akiyama 2008), and the Collatz-inspired **4/3 problem** (Dubickas–Mossinghoff 2009). This is our (K),
  one inch short on the **specified-orbit** axis (it conjectures normality of a *distinguished* word but proves
  none).
- **NEW FIND — Eliahou & Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*,
  arXiv:2504.13716 (Apr 2025; to appear, Comptes Rendus Math.).** [PROVEN-in-lit, but structural not density.]
  Directly ties base-`3/2` representation validity and the lexicographically-largest length-`n` word to the
  Collatz `T(n)`. This is the closest published paper to our exact `×(3/2)` / Collatz bridge; it formalizes the
  base-3/2 ↔ Collatz dictionary but contains **no equidistribution/density theorem** — it is the same
  combinatorial layer our `LIMIT_THEOREM.md` complexity floors live on. Worth citing as the canonical reference
  for the base-3/2–Collatz link.
- **Algom, *Recent progress on pointwise normality of self-similar measures*, arXiv:2504.18192 (Apr 2025,
  exposition).** [PROVEN-in-lit core theorem; OPEN on our axes.] Underlying theorem is **Algom–Baker–Shmerkin**
  (*On normal numbers and self-similar measures*, Adv. Math. 2022): **Rajchman (Fourier decay, no rate needed) ⇒
  μ-a.e. point is normal to all bases** (improving Davenport–Erdős–LeVeque 1964). The exposition's stated open
  problems are **exactly our two gaps: (i) effective equidistribution, (ii) non-integer bases** (plus
  higher-order correlations). *Correction to repo note:* arXiv:2504.18192 is **Algom solo (exposition)**; the
  "Algom–Baker–Shmerkin" credit belongs to the 2022 Adv. Math. theorem it expounds. Crucially this is an
  **a.e.-in-support** statement — the quantifier we cannot use.

**Homogeneous-dynamics sweep (single specified orbit of a cyclic / rank-1 action):**
- **Bourgain–Furman–Lindenstrauss–Mozes, JAMS 24 (2011) 231–280.** [PROVEN-in-lit.] Individual-orbit
  equidistribution on `Tᵈ` at **exponential rate**, *unless the start is near a finite orbit* — but requires a
  **non-abelian** semigroup in `SL_d(ℤ)` generating a large (non-amenable) subgroup. Our `⟨3/2⟩` is cyclic /
  amenable: the hypothesis fails at the root.
- **Effective equidistribution (Lindenstrauss–Mohammadi arXiv:2202.11815; effective Ratner, Annals 2025
  arXiv:2208.02525; Einsiedler–Margulis–Venkatesh arXiv:0708.4040; Wieser arXiv:2407.12760).** [PROVEN-in-lit.]
  All for **unipotent / semisimple / higher-rank / periodic** orbits — none covers a single cyclic *hyperbolic*
  orbit.
- **Shi, *Pointwise equidistribution for one-parameter diagonalizable group actions* (arXiv:1405.2067), and the
  rank-one / low-entropy measure-classification line (Einsiedler–Lindenstrauss).** [PROVEN-in-lit.] These
  describe the *size* of the exceptional (non-generic) set (Hausdorff dimension / Birkhoff-generic full measure)
  but give **no tool to certify a single named algebraic point** is outside it. Rank-1 diagonal actions carry an
  uncountable simplex of invariant measures and invariant Cantor sets (Einsiedler–Lindenstrauss JMD 2008) —
  the structural reason no specified-point theorem exists.
- **Statistical-physics / LABS — merit-factor problem (Golay; Jedwab; Boškovic et al. arXiv:1406.5301).**
  [OPEN.] Whether `max F_N` is bounded is open; rigorous results are **lower bounds for an extremal/optimized
  sequence** (e.g. 6.34 from rotated Legendre sequences) — an *optimization over all sequences*, **not** a
  genericity statement about one *given dynamically-generated* sequence. Confirms the "self-induced disorder"
  analogy is real but supplies no specified-orbit theorem.

**Net literature verdict:** every positive single-orbit / pointwise theorem found requires one of
{rank ≥ 2, non-amenable acting semigroup, unipotent/polynomial divergence, a.e.-in-support, or
optimization-over-sequences}. **None gives a specified-orbit (not a.e., not extremal) genericity statement for
a rank-1 amenable hyperbolic system.** No paper names this intersection as a studied object.

---

## 2. Per-candidate-field assessment (the four homes named in WEAPONS_AUDIT §5)

| Candidate home | Has a *specified-orbit* (not a.e./not extremal) genericity statement? | Nearest result | The gap |
|---|---|---|---|
| **(a) Gibbs–Markov 2-adic decay-of-correlations** (Aaronson–Denker; twisted RPF; Lasota–Yorke / Keller–Liverani) | **No.** Controls `(F, Haar)` and a.e. / annealed orbits only (decay of correlations, quenched CLT for a.e. sequence). | Spectral gap ρ<1 ⇒ annealed Rajchman + a.e.-sequence CLT (`THERMO_FORMALISM.md`). | Orbit-blind: `F` has fixed/periodic points on every branch violating the visit-count bound. The per-scale **injection** term (not the contraction) is the wall (`ENDOGENEITY_DEFECT.md`). Descent a.e.→specified point absent. |
| **(b) Effective rank-1 S-arithmetic / homogeneous-dynamics equidistribution** | **No** (for a cyclic hyperbolic orbit). Positive single-orbit results exist only for non-abelian (BFLM) or unipotent/higher-rank/periodic. | BFLM 2011 (torus, non-abelian, exp. rate); effective Ratner/EMV (unipotent/semisimple). | Acting group `ℤ[1/6]⋊⟨3/2⟩` is **amenable + rank-1**; both rigidity hypotheses (rank ≥ 2 / non-amenable 2nd direction) fail. Mahler 3/2 is the archimedean shadow (`TRACTABILITY_MAP.md`). |
| **(c) Low-autocorrelation binary sequences / self-induced disorder (stat-phys, merit factor)** | **No.** Statements are extremal (over all sequences) or numerical for a *designed* sequence; never genericity of one *dynamically-forced* trajectory. | Merit-factor lower bounds (Legendre, 6.34); LABS open boundedness. | Optimizes over sequences; our sequence is **prescribed by `×3/2`** with no design freedom. The "self-induced quenched disorder / deterministic spin-glass" framing (`MINIMAL_OPEN_KERNEL.md` §"self-generated subcriticality") is a **metaphor with no theorem to import**. |
| **(d) Self-referential 2-adic digit fixed points** (Mauduit–Rivat carry lemma + Gowers norms; Drmota–Spiegelhofer; Senge–Straus/Stewart) | **No.** Digit theorems need an *independent/bounded* carry, or give only `o(n)` (sublinear) counts. | Mauduit–Rivat (balanced digit w/ bounded carry); Drmota–Spiegelhofer arXiv:2501.00850 (longest equal-bit block of `3^n` is `o(n)`); Stewart 1980 (#nonzero digits ≫ log m/log log m). | The target digit `bit_n(T_n)` is a carry-sum of the **entire self-fed parity history** (closed loop), height `≈ n log₂3`, unbounded → outside the Subspace-Theorem / Mauduit–Rivat reach; all density-level statements (Erdős/Pegg/Ren, Tao β=1) are conjectural (`THREEADIC_LITERATURE.md`). |

**Conclusion of the table:** in all four candidate homes the *machinery exists* but stops at the
a.e./annealed/extremal/bounded-carry tier; **none contains a specified-orbit positive-genericity statement** for
a rank-1 amenable hyperbolic system. The object is a missing **bridge** between (a) Gibbs–Markov a.e. theory and
a single computable trajectory — and that bridge is itself **new mathematics**, not a renaming.

---

## 3. The polished 1-page expert question

> **To: authors of AEV (Andrieu–Eliahou–Vivion) / the Tao circle / homogeneous-dynamics & effective-equidistribution
> specialists.**
>
> **One-line ask.** Is *single-specified-orbit effective equidistribution of a rank-1 amenable hyperbolic action*
> a **known concept** (under any name), a **known obstruction we have overlooked**, or **genuinely open** — and
> if open, what is the precise reason it falls between the rigidity and the Weyl toolboxes?
>
> **The object.** Let `A(x) = (3/2)·x` on the S-arithmetic solenoid `X = (ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`. `A` is a
> **hyperbolic automorphism** (expanding at `∞` and `2`, contracting at `3`, product = 1, no neutral direction),
> so a.e. orbit equidistributes (Birkhoff). The acting group `ℤ[1/6]⋊⟨3/2⟩` is **solvable, hence amenable**, and
> `⟨A⟩` is **cyclic (rank 1)**. Question: does the orbit of the **specified algebraic point** `x₀` (image of the
> integer 8) equidistribute toward Haar? Its `ℝ`-shadow is `{(3/2)ⁿ}`, so the question **contains Mahler's 3/2
> problem** — we are not asking you to solve that, but to **locate the residue**.
>
> **Where the known methods break (lead with this).**
> 1. **Rigidity engines need what we lack.** Furstenberg/Rudolph–Johnson/Einsiedler–Katok–Lindenstrauss measure
>    rigidity needs **rank ≥ 2** (two multiplicatively-independent maps); BFLM (JAMS 2011) gets *individual-orbit*
>    torus equidistribution but needs a **non-abelian** acting semigroup; effective Ratner / Lindenstrauss–Mohammadi
>    need **unipotent/polynomial** divergence. Our action is **rank-1, amenable, exponentially divergent** — it
>    violates each hypothesis at the root. Rank-1 diagonal actions carry an uncountable simplex of invariant
>    measures + invariant Cantor sets (Einsiedler–Lindenstrauss JMD 2008), so there is no rigidity to invoke.
> 2. **Weyl / unique-ergodicity engines need what hyperbolicity destroys.** The map is **not uniquely ergodic**
>    (continuum of invariant measures), and van der Corput differencing **fixes** `(3/2)ⁿ` at every degree
>    (no degree drop) — so the rotation/Weyl side cannot start.
> 3. **The Gibbs–Markov side stops at the wrong quantifier.** The induced 2-adic renewal map is full-branch
>    expanding with a spectral gap; this yields decay of correlations and a CLT **for a.e. realization / annealed**
>    — but the orbit's driving "scenery" is **generated by the orbit itself** (closed loop), so the natural
>    surrogate (shuffled/i.i.d. copy) is solvable while the real single quenched trajectory is not. We can phrase
>    the whole problem as a single inequality `‖F‖ < 1` for an **endogenous (self-generated) cocycle** — a
>    "propagation of chaos for one computable trajectory" — and standard mean-field / RWRS / Gibbs–Markov theory
>    stops at a.e. random realizations.
>
> **Precise questions.**
> - **Q-A.** Is there *any* single-orbit (non-a.e.) equidistribution result for a **specified point** of an
>   **amenable hyperbolic (rank-1 Anosov)** toral/solenoid automorphism — under a Diophantine input on `log₂3`,
>   a Margulis-function / non-escape-of-mass argument, or otherwise? If not, is the *correct obstruction* exactly
>   that amenability removes the spectral gap of the acting group while hyperbolicity removes unique ergodicity —
>   so the point falls in a genuine gap between the two toolboxes?
> - **Q-B.** The Algom–Baker–Shmerkin route (Rajchman ⇒ a.e.-in-support normal) and AEV's normality conjecture
>   both stop on the **specified-point** axis, and Algom's exposition (arXiv:2504.18192) lists **effective
>   equidistribution** and **non-integer bases** as open. Is our object the same open problem wearing
>   S-arithmetic clothing, or is the solenoid's **extra contracting 3-adic (stable) direction** a genuine lever
>   the bare real `{(3/2)ⁿ}` lacks?
> - **Q-C (framing).** Does the intersection *"specified-orbit genericity for a rank-1 amenable hyperbolic
>   system"* have an existing name / literature? If it has **none**, that absence is itself the answer we need —
>   it would confirm this is a missing bridge, and suggest the right way to frame the whole class.
>
> **A sharp "no, here is why" is as useful as a "yes, see X." A pointer is plenty — no write-up needed. And if the
> reduction is malformed, the most valuable reply is how you would reformulate it.**

**One-sentence sharpest form:** *Is there any theorem forcing a single specified algebraic orbit of a rank-1,
amenable, hyperbolic (`×3/2`) action on an S-arithmetic solenoid to equidistribute — or is "specified-orbit
genericity for an amenable-hyperbolic system" a genuinely empty spot between the rigidity and the Weyl toolboxes?*

---

## 4. Verdict — new math vs new bridge (with confidence)

**Verdict: this is an EMPTY-TOOLBOX SPOT — genuinely new mathematics, framed as a missing bridge.**
**Confidence: HIGH (~85%)** that no existing framework contains the needed *specified-orbit* genericity statement;
**MODERATE** that the gap is *permanent* (vs. one good idea away).

- **Why "new math," not "new bridge to an existing theorem":** the four candidate homes each possess the relevant
  machinery but **all stop one quantifier short** (a.e. / annealed / extremal / bounded-carry). The specific
  combination `amenable ∩ hyperbolic ∩ rank-1 ∩ specified-point` is **not a named or populated object** in any
  field surveyed — confirming the WEAPONS_AUDIT §5 "empty spot in the toolbox" claim with literature in hand.
- **Why "framed as a bridge" is still the honest nuance:** the object is precisely the **missing descent map**
  from Gibbs–Markov / homogeneous a.e.-equidistribution to a single computable trajectory. So the new theorem,
  if it exists, would be a *bridge between two existing developed theories*, not an isolated invention — which is
  the most hopeful reading and the right way to pitch it to experts.
- **Residual uncertainty:** the strongest "this might already exist" candidates are (i) the rank-1 / low-entropy
  measure-classification program (Einsiedler–Lindenstrauss) producing a sharper exceptional-set bound than we
  found, and (ii) some single-orbit shrinking-target estimate in the Gibbs–Markov literature reaching a one-sided
  density (the strictly-weaker target of `EXPERT_ASK.md` Q0). These are exactly what Q-A / Q-C above probe; a
  specialist could overturn the verdict with one pointer — which is why the question is worth asking before
  declaring it new.

---

## Sources

- M. Andrieu, S. Eliahou, L. Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025). https://arxiv.org/abs/2510.11723
- S. Eliahou, J.-L. Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*, arXiv:2504.13716 (2025; to appear C. R. Math.). https://arxiv.org/abs/2504.13716
- A. Algom, *Recent progress on pointwise normality of self-similar measures*, arXiv:2504.18192 (2025). https://arxiv.org/abs/2504.18192
- A. Algom, S. Baker, P. Shmerkin, *On normal numbers and self-similar measures*, Adv. Math. (2022). https://arxiv.org/pdf/2107.02699
- J. Bourgain, A. Furman, E. Lindenstrauss, S. Mozes, *Stationary measures and equidistribution for orbits of nonabelian semigroups on the torus*, J. Amer. Math. Soc. 24 (2011) 231–280. https://www.ams.org/journals/jams/2011-24-04/
- E. Lindenstrauss, A. Mohammadi, *Polynomial effective equidistribution*, arXiv:2202.11815. https://arxiv.org/pdf/2202.11815
- M. Einsiedler, G. Margulis, A. Venkatesh, *Effective equidistribution for closed orbits of semisimple groups*, arXiv:0708.4040. https://arxiv.org/pdf/0708.4040
- R. Shi, *Pointwise equidistribution for one-parameter diagonalizable group actions*, arXiv:1405.2067. https://arxiv.org/pdf/1405.2067
- M. Einsiedler, E. Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case and the general low-entropy method*, JMD (2008).
- Low-autocorrelation binary sequences / merit factor: arXiv:1406.5301; arXiv:1503.05067 (survey of rigorous bounds & Golay).
- (repo cross-refs) `WEAPONS_AUDIT_2026-06-29.md` §5, `EXPERT_ASK.md`, `EXPERT_ASK_HOMOGENEOUS.md`, `TRACTABILITY_MAP.md`, `MINIMAL_OPEN_KERNEL.md`, `THREEADIC_LITERATURE.md`, `DERANDOMIZATION_LITERATURE.md`, `SELECTOR_COMPUTABILITY.md`.

*Convention: factual repo claims are machine-checked in exact integer/2-adic arithmetic per the program's
soundness policy. Literature labelled [PROVEN-in-lit] / [OPEN]. No labels upgraded; no proofs claimed. Not committed.*
