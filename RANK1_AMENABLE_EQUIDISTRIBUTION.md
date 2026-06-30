# Rank-1 amenable effective equidistribution — the coverage no-go (roadmap (d)) (2026-06-30)

*Self-contained formal note formalizing roadmap item (d) (`NEW_MATH_PROGRAM.md` §5). UNLIKE the (a)(b)(c) trilogy
(AIU / ENT / EUE), (d) is the **generational target itself** — completing it equals solving `(K)` — so it admits
**no** self-contained sub-theorem proving it. The publishable content is instead a **Coverage Theorem**: a
two-tier statement separating what is rigorously proven (each named effective-equidistribution framework's
defining hypothesis demonstrably FAILS for this action — `[PROVEN]`) from what is a literature verdict (the
intersection `amenable ∩ hyperbolic ∩ rank-1 ∩ specified-point` is unpopulated — `[SURVEY-VERDICT, ~85%]`).
SOUNDNESS CRITICAL: the disqualifications prove inapplicability of EXISTING theorems, NOT impossibility of any
future theorem, and NOT `(K)`. Builds on `EMPTY_TOOLBOX_QUESTION.md` (literature sweep with citations); the Berkovich
and digit/Mauduit–Rivat rows extend that sweep using the package's candidate-fields list. No label upgraded. NOT
committed by default.*

> **[RED-TEAM VERDICT, `RANK1_REDTEAM.md`: over-claim found, corrected.]** The per-row disqualifications, the
> Tier-1/Tier-2 split, the `Γ`-amenability and `A`-hyperbolicity facts, and the citations all CONFIRM. Two structural
> over-claims were caught and are now fixed in place: **(1)** `T(d) ⟺ (K)` was wrong — the program's own package (§2)
> records single-orbit equidistribution as `⟸` (sufficient, **strictly stronger**), so this note now states `T(d) ⟹ (K)`
> and flags that only the restricted one-sided form is equivalent; **(2)** "the two toolbox halves are mutually exclusive"
> was false (the horocycle flow is both unipotent and uniquely ergodic) — relabeled to the proven *double absence* for
> this action. A knock-on sentence (§3) confirms the no-go still covers the weaker `(K)`, since the disqualifications act
> on framework *hypotheses*, not conclusion strength.

---

## 0. One-line synthesis

The arithmetic content `(K)` is equivalent, on the `(2,3)`-solenoid, to **effective equidistribution of a single
specified rank-1 orbit of an amenable hyperbolic automorphism** — call this target `T(d)`. `T(d) ⟹ (K)` (sufficient,
**strictly stronger**: full Haar equidistribution of the orbit implies the one-sided `liminf` cell-frequency bound that
is `(K)`, but not conversely — a one-sided bound cannot pin the whole invariant measure; equivalence holds only for the
restricted one-sided form, dropping "toward Haar"). The Coverage Theorem below proves
`[PROVEN]` that **every** named effective-equidistribution framework's defining hypothesis fails for `T(d)` for an
explicit structural reason, and records `[SURVEY-VERDICT]` that no existing framework populates the intersection.
This is a **positioning** result (where the problem sits relative to the developed toolboxes), not a proof of
`T(d)` and not a proof that `T(d)` is unprovable.

---

## 1. The target `T(d)` and its status `[PROVEN reduction; OPEN target]`

> **`T(d)` (the generational target).** Let `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` be the compact abelian `S`-arithmetic solenoid
> and `A=M_{3/2}=M_3M_2^{-1}∈Aut(X)` the hyperbolic automorphism with dilations `(|3/2|_∞,|3/2|_2,|3/2|_3)=(3/2,2,1/3)`
> (expanding at `∞` and `2`, contracting at `3`, product `=1`, **no neutral direction**). The acting group
> `Γ=ℤ[1/6]⋊⟨3/2⟩` is **solvable, hence amenable**; `⟨A⟩` is **cyclic (rank 1)**. `T(d)`: the forward orbit of the
> **specified** algebraic seed `8` (equivalently `1`) equidistributes toward Haar. (Its *restricted one-sided form* —
> a `liminf` positive-density bound on a single cell-frequency — is the exact equivalent of `(K)`; the full toward-Haar
> form is strictly stronger.)

**Status `[PROVEN]`:** `T(d) ⟹ (K)` (**sufficient, strictly stronger**, matching `BB6_FRAMEWORK_PACKAGE.md` §2, where
single-orbit equidistribution is recorded as "`⟸` (sufficient, strictly stronger), not `⟺` ... full equidistribution is
stronger still"). Forward (`⟹`): §5 of the package reduces `(K)` to `μ=`Haar for any weak-`*` limit `μ` of the seed-8
`A`-orbit empiricals; orbit equidistribution gives `μ=`Haar, whence the cell-frequencies whose `liminf` is `(K)`. The
converse fails: a one-sided `liminf` on one cell statistic cannot pin the whole invariant measure (the ψ-form truncates
the tail; full equidistribution controls every cell). So `T(d)` is **not a proper sub-problem** of `(K)` only in the
sense that it is at-least-as-hard (any theorem proving `T(d)` proves `(K)`); as *statements* `T(d)` is strictly stronger,
and the genuine equivalent of `(K)` is the restricted one-sided form. This is *why* (d) has no self-contained partial:
proving even the one-sided form for the specified seed is `(K)`.

**A.e. baseline `[PROVEN-in-lit]`:** `A` is hyperbolic, so Haar-**a.e.** orbit equidistributes (Birkhoff +
ergodicity of `A` on `X`). The whole difficulty is the single Haar-null specified point — the same a.e.-vs-specified
gap as `(K)` (§3 No-Structure theorem).

---

## 2. The Coverage Theorem `[PROVEN per-framework; SURVEY-VERDICT for the intersection]`

> **Coverage Theorem.** For each named framework `F` that proves effective equidistribution (or single-orbit
> genericity) for *some* dynamical system, the defining hypothesis of `F` **fails for `T(d)`**, for the explicit
> structural reason in the table — `[PROVEN]` in each row. Consequently no existing `F` applies to `T(d)`.
> Whether the resulting intersection `{amenable ∩ hyperbolic ∩ rank-1 ∩ specified-point}` is *permanently* empty or
> one idea from a new framework is `[SURVEY-VERDICT, ~85%]`, not proven (§3).

| Framework `F` | Defining hypothesis of `F` | Fails for `T(d)` because — `[PROVEN]` | Citation |
|---|---|---|---|
| Furstenberg / Rudolph–Johnson / Einsiedler–Katok–Lindenstrauss measure rigidity | **rank ≥ 2** (two mult.-independent maps) | `⟨A⟩=⟨3/2⟩` is **cyclic, rank 1**; rank-1 diagonal actions carry an *uncountable* simplex of invariant measures (incl. positive-entropy) — no rigidity to invoke | E–L JMD 2008; Rudolph 1990 |
| Bourgain–Furman–Lindenstrauss–Mozes (individual-orbit, exp. rate) | acting semigroup **non-abelian**, generating a large (non-amenable) subgroup | `Γ` is **solvable ⟹ amenable**; `⟨A⟩` abelian — the non-amenability hypothesis fails at the root | BFLM, JAMS 24 (2011) |
| Effective Ratner / Lindenstrauss–Mohammadi / Einsiedler–Margulis–Venkatesh | **unipotent / polynomial** divergence (or semisimple, higher-rank, periodic) | `A` is **hyperbolic (diagonalizable, exponential divergence)** — no unipotent direction; orbit is neither periodic nor higher-rank | LM arXiv:2202.11815; EMV arXiv:0708.4040 |
| Weyl / van der Corput / unique-ergodicity | a **degree drop** under differencing, or unique ergodicity | `A` is **not uniquely ergodic** (continuum of invariant measures); vdC differencing **fixes** `(3/2)ⁿ` at every degree (geometric, no finite degree) | classical; `CORE_MR_EXTENSION.md` |
| Gibbs–Markov / thermodynamic (twisted RPF, Aaronson–Denker, Lasota–Yorke) | controls `(F,`Haar`)`, **a.e. / annealed** realizations | the driving scenery is **endogenous** (generated by the orbit itself); gives decay-of-correlations + quenched CLT for a.e./annealed sequences only, never the single named trajectory; `F` has periodic points on every branch violating the visit bound | `THERMO_FORMALISM.md`; `ENDOGENEITY_DEFECT.md` |
| Self-similar-measure normality (Algom–Baker–Shmerkin; Hochman–Shmerkin) | conclusion is **a.e.-in-support** | quantifier is `μ`-a.e. point; `T(d)` asks for **one specified** point — the precise quantifier the method cannot deliver; also integer-base | ABS, Adv. Math. 2022 |
| Berkovich / adelic equidistribution (Favre–Rivera-Letelier; Baker–Rumely) | **degree ≥ 2** map, **small-height** points, **backward/Galois** orbits | `A=×(3/2)` is **degree 1**; the seed is a **growing-height forward** orbit — all three hypotheses fail | FRL 2010; B–R 2010 |
| Digit / Mauduit–Rivat / Gowers-norm methods | **bounded / independent** carry, free averaging index | the target digit is a carry-sum of the **entire self-fed parity history** (closed loop), height `≈n log₂3`, unbounded — outside Subspace-Theorem / MR reach; density-level statements are themselves conjectural | `CORE_MR_EXTENSION.md`; `THREEADIC_LITERATURE.md` |

**Net `[PROVEN]`:** every positive single-orbit / pointwise theorem in the surveyed literature requires one of
`{rank ≥ 2, non-amenable semigroup, unipotent/polynomial divergence, a.e.-in-support, degree ≥ 2 + small height,
bounded carry}`. `T(d)` provably has **none** of these. The disqualifications are individually rigorous: each is a
true statement about `A`, `Γ`, or the seed (rank 1; amenable; hyperbolic; degree 1; growing height; endogenous
closed-loop carry).

---

## 3. What the Coverage Theorem does and does NOT claim (honest scope)

This is the binding soundness boundary, distinguishing (d) from a genuine impossibility theorem:

- **Proven (Tier 1):** each named framework's hypothesis fails for `T(d)`. This rules out *applying those theorems*.
- **NOT proven:** that *no* framework can ever reach `T(d)`. The intersection being unpopulated *today* is a
  literature verdict (`[SURVEY-VERDICT, ~85%]`, `EMPTY_TOOLBOX_QUESTION.md` §4), not a theorem. A new framework —
  e.g. an effective shrinking-target estimate, a Margulis-function / non-escape-of-mass argument adapted to the
  amenable-hyperbolic regime, or a Diophantine input on `log₂3` — is exactly what is sought, and a single expert
  pointer could overturn the "empty" verdict. This note does **not** close that door; it locates it.
- **NOT `(K)`, NOT `¬(K)`:** the Coverage Theorem says nothing about the truth value of `T(d)` or of `(K)`; it is a
  statement about the *toolbox*, orthogonal to the answer.
- **The no-go covers the weaker `(K)` too, despite `T(d)⟹(K)` (not `⟺`).** Although `T(d)` is strictly stronger than
  `(K)` (#0/§1), the disqualifications operate at the level of each framework's *hypotheses* — rank, amenability,
  divergence type, degree, quantifier — which fail for the **action / seed** regardless of how strong a conclusion the
  framework would output. So no named framework reaches even the weaker one-sided `(K)` for this specified orbit either;
  the strength gap between `T(d)` and `(K)` does not create a coverage loophole.
- **The disqualifications are of hypotheses, not of approaches in spirit.** E.g. "rigidity needs rank 2" disqualifies
  the *theorem as stated*; the AIU bridge (§5 of the package) is precisely an attempt to *manufacture* the missing
  rank-2 invariance from the rank-1 orbit — which is why (a) (P-AIU) is a separate, sharper no-go about that specific
  manufacturing attempt, not subsumed here.

---

## 4. Why the gap is structural (the two-toolbox picture) `[PROVEN framing]`

The effective-equidistribution toolbox splits into two halves, each running on a structural feature that **our action
lacks**, and `T(d)` sits in the gap:

- **Rigidity half** (Ratner / E–L / Rudolph–Johnson / BFLM) needs a *large acting group* — rank ≥ 2, or
  non-amenable, or unipotent — to generate enough invariance/mixing to pin a single orbit. **Amenability of `Γ`
  removes the acting-group spectral gap** these engines run on. `[PROVEN: Γ solvable]`
- **Weyl / unique-ergodicity half** needs *tameness* — bounded orbits, a degree drop, or a unique invariant measure.
  **Hyperbolicity (exponential divergence + continuum of invariant measures) removes unique ergodicity** and pins
  the geometric sequence at full degree. `[PROVEN: A hyperbolic, not uniquely ergodic]`

So one half needs a large acting group and the other needs tame dynamics, and our action `amenable ∩ hyperbolic` has
**neither feature-set** — proven. (This is *not* the false claim that the two feature-sets partition all systems:
they can co-occur — the horocycle flow is *both* unipotent and uniquely ergodic — so a system can satisfy both halves;
the proven statement here is only the *double absence* for our specific action.) This is the precise sense in which the
spot is "between the toolboxes" — not a coincidence of missing papers but a regime no single existing method targets.
`[PROVEN: this action satisfies neither feature-set; SURVEY-VERDICT that no method bridges the gap]`

---

## 5. Relation to the (a)(b)(c) trilogy and the package

(a) (P-AIU), (b) (P-ENT), (c) (P-EUE) are **sub-mechanism** no-gos *inside* the solenoid placement: they pin the
failure of the high-entropy invariance-upgrade, the entropy lower bound, and the uniform-spectral contraction,
respectively — the three tools an expert reaches for **after** accepting the placement. (d) is the **meta-frame**:
it states that the *entire effective-equidistribution apparatus*, at the level of named frameworks, is absent for
this action — the reason the placement needs new mathematics at all. Logically:

> (d) Coverage Theorem ⟹ "no off-the-shelf framework proves `T(d)`" ⟹ one must either manufacture a missing
> hypothesis (the AIU/ENT route, where (a)(b) say *how* the manufacture fails) or build a new framework for the
> amenable-hyperbolic-rank-1 regime (genuinely new mathematics, `NEW_MATH_PROGRAM.md`).

The four together give the package a complete *negative map*: §3 (No-Structure, rules out structural certificates),
§4 (dichotomy, the single proven boundary), §5.5 (a,b,c, the three sub-mechanism no-gos), and (d) (the toolbox-level
coverage no-go).

---

## 6. The publishable contribution (honest)

(d) yields **no theorem of the form "`T(d)` holds/fails"** — it cannot, since `T(d)⟹(K)` and even the weaker one-sided
equivalent of `(K)` is the open wall. Its contribution is the
**Coverage Theorem of §2** plus the **two-toolbox structural picture of §4**: a precise, citation-backed positioning
result establishing that single-specified-orbit effective equidistribution for a rank-1 amenable hyperbolic
solenoid automorphism is *not covered* by any named framework, with each non-coverage proven from an explicit
hypothesis failure. This is publishable as a *survey-with-no-go* / problem-positioning paper (the natural venue: a
homogeneous-dynamics or arithmetic-dynamics expository/problems volume), and it is exactly the object the §7 expert
question (package) asks the AEV authors and the E–L–Host circle to confirm or overturn.

**No machine decided. No label upgraded.** `T(d)` (and its one-sided equivalent `(K)`) remains `[OPEN]` = Mahler 3/2 / AEV.
