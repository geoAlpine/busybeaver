# Red-team audit — RANK1_AMENABLE_EQUIDISTRIBUTION.md (2026-06-30)

**Overall verdict: [OVER-CLAIM FOUND, must correct].**

The Coverage Theorem facts and the per-row disqualifications are sound and the Tier-1/Tier-2
separation is honest, but two structural claims are over-stated and must be corrected: (1) the
central reduction is written as the equivalence `T(d) ⟺ (K)` "(no slack)" when the program's own
package proves it is only `⟸` (sufficient, **strictly stronger**); (2) §4 asserts `[PROVEN that the
hypotheses are mutually exclusive]`, which is false (unipotent uniquely-ergodic systems sit in both
toolbox halves). Everything else [CONFIRM]s, with two minor caveats.

---

## 1. [CORRECT] — CENTRAL: `T(d) ⟺ (K)` is an over-claim; the true relation is `T(d) ⟹ (K)` (sufficient, strictly stronger)

This is the single most important finding and it is **decided against the note by the program's own
package**, not merely by my judgment.

`(K)` is, canonically, the **one-sided** statement: even-density `≥ 1/3` `=` `mean D ≥ 3/2` `=`
`liminf` cell-frequency bound. `T(d)` as the note defines it is **full equidistribution of the orbit
toward Haar**. Full Haar equidistribution forces *every* cell frequency to its exact Haar value (a
two-sided convergence statement for all test functions); `(K)` is only a *lower bound on one cell
statistic* and does **not** pin the full invariant measure to Haar. Hence:

- `T(d) ⟹ (K)` — VALID (the note's "Backward" paragraph actually proves exactly this).
- `(K) ⟹ T(d)` — **NOT VALID**: a one-sided liminf on a single statistic cannot determine the whole
  weak-`*` limit measure.

`BB6_FRAMEWORK_PACKAGE.md` §2 states this verbatim and explicitly contradicts the note:

> "non-halt `⟺` even-density `≥1/3` `⟺` mean `D ≥ 3/2` (these three mutually **equivalent**, Kac)
> `⟸` `liminf freq(D≥2) ≥ 1/2` `⟸` **single-orbit equidistribution of `c_n mod 2^k`. The last two
> links are `⟸` (sufficient, strictly stronger), not `⟺`** … **full equidistribution is stronger
> still.**"  (package §2, "The chain")

and the Kernel box: "(K) is `mean D ≥ 3/2 ⟺ liminf even-density ≥1/3`. **Sufficient (strictly
stronger, `⟹`) forms: … single-orbit equidistribution of `c_n mod 2^k`; equidistribution of
`8·(3/2)^n mod 1`.**"  So the note imports the *stronger-than-warranted* side of an internal package
inconsistency (package §5 lines ~223/237 loosely write "`(K) ⟺ μ=Haar`", but the careful, explicitly
hedged §2 / Kernel statement is the governing one: equidistribution is `⟹`, not `⟺`).

The note also internally conflates the two: its own `T(d)` definition writes
"equidistributes toward Haar — **equivalently** a one-sided positive-density bound on its
cell-frequencies." Those are **not** equivalent; the "equivalently" is the embedded error.

**Offending phrases (verbatim) and corrections:**

(a) §0, line 18:
> `T(d) ⟺ (K)` (no slack: this is not a sub-problem but the same wall in homogeneous-dynamics language).

CORRECT TO:
> `T(d) ⟹ (K)` (`T(d)` is **sufficient and strictly stronger**: full Haar equidistribution forces every
> cell frequency to its Haar value and hence implies the one-sided liminf bound `(K)`, but `(K)` — a
> lower bound on a single cell statistic — does **not** pin the limit measure to Haar, so the converse
> fails. `T(d)` becomes *equivalent* to `(K)` only if `T(d)` is restricted to exactly the one-sided
> cell-frequency liminf form, in which case "equidistributes toward Haar" must be dropped.)

(b) §1, definition (lines 33–34):
> `T(d)`: the forward orbit of the **specified** algebraic seed `8` (equivalently `1`) equidistributes
> toward Haar — equivalently a one-sided positive-density bound on its cell-frequencies.

CORRECT TO: delete "— equivalently a one-sided positive-density bound on its cell-frequencies" and add:
> … equidistributes toward Haar. (This **implies, and is strictly stronger than**, the one-sided
> positive-density / liminf cell-frequency bound that is `(K)`; see package §2.)

(c) §1, line 36:
> **Status `[PROVEN]`:** `T(d) ⟺ (K)`.

CORRECT TO:
> **Status `[PROVEN]`:** `T(d) ⟹ (K)` (sufficient, strictly stronger); equivalence holds only for the
> restricted one-sided cell-frequency form of `T(d)`.

And the "Forward" sentence ("§5 … reduces `(K)` to `μ=`Haar … is exactly orbit equidistribution") only
establishes `μ=Haar ⟹ (K)` (Haar gives even-density exactly `1/3`); it does **not** establish
`(K) ⟹ μ=Haar`. Relabel: the "Backward" paragraph is the valid `T(d) ⟹ (K)` direction; there is no
proof of the reverse beyond the package's contested `⟺`.

(d) §1, line 39–40: "So `T(d)` is **not a proper sub-problem** of `(K)` … it is `(K)` re-coordinatized
… any theorem proving `T(d)` proves `(K)`." — The last clause ("any theorem proving `T(d)` proves
`(K)`") is TRUE and may stay; but "not a proper sub-problem / re-coordinatized / same wall" must be
softened: `T(d)` is a **strictly stronger** target whose proof would settle `(K)`, not a literal
recoordinatization of it.

(e) §3, line 85: "the truth value of `T(d)=（K)`" (note also a stray full-width parenthesis `（`) and
§6, line 141: "`T(d) = (K)` remains `[OPEN]`". Replace "`T(d) = (K)`" with "`T(d)` (which implies
`(K)`)" or "`(K)` (the strictly weaker target of `T(d)`)".

**Knock-on consequence for the Coverage Theorem (sub-point of #1):** because `T(d)` is strictly
stronger than `(K)`, "no framework proves `T(d)`" does not *by itself* give "no framework proves the
weaker `(K)`." The note should add one sentence: the disqualifications are at the level of *framework
hypotheses* (rank, amenability, divergence type, degree, quantifier) that fail for the **action/seed**
regardless of whether the sought conclusion is full equidistribution or the one-sided bound — so the
no-go survives for `(K)` too, but for that reason, not because `T(d)=(K)`.

---

## 2. [CORRECT] — §4 "mutually exclusive" is mislabelled `[PROVEN]`; the proven claim is only that OUR system has neither feature

Offending phrases (§4, lines 106–109):
> the two halves require **mutually exclusive** structural features (large group vs. tame dynamics),
> and `amenable ∩ hyperbolic` has *neither*. … `[PROVEN that the hypotheses are mutually exclusive;
> SURVEY-VERDICT that no method bridges them]`

This is false as a statement about all systems. The two feature-sets are **not** mutually exclusive: a
system can satisfy a hypothesis from *both* halves. Counter-example: the **horocycle flow** on a
compact hyperbolic surface is **unipotent** (rigidity half — Ratner/effective-Ratner applies) **and
uniquely ergodic** (Weyl/UE half — Furstenberg) simultaneously. (Likewise irrational rotations are
amenable-acting *and* uniquely ergodic.) So "mutually exclusive" / "disjoint regimes" over-states.

The genuinely proven content is the *weaker* statement the prompt-class allows: **our** system
(`amenable ∩ hyperbolic ∩ rank-1`) satisfies **neither** feature-set.

CORRECT TO (line 106–109):
> the two halves were developed for different regimes (large group vs. tame dynamics), and our system
> `amenable ∩ hyperbolic` satisfies **neither** — it has no large/non-amenable/unipotent acting
> structure and no unique ergodicity / degree drop. (The two feature-sets are **not** mutually
> exclusive in general — unipotent uniquely-ergodic systems such as the horocycle flow lie in both —
> so the claim is specifically the *double absence* for this action, not a partition of all systems.)
> `[PROVEN that this action satisfies neither feature-set; SURVEY-VERDICT that no method bridges them]`

Also soften §4 line 96 "covering **disjoint** dynamical regimes" → "developed for **different**
dynamical regimes" for the same reason.

---

## 3. [CONFIRM] — Coverage Theorem table rows are individually rigorous

Checked each row's hypothesis statement and its failure-for-`T(d)` reason:

- **Row 1 (rank-≥2 rigidity, E–L/Rudolph–Johnson/Furstenberg).** `⟨A⟩=⟨3/2⟩` cyclic, rank 1; rank-1
  diagonalizable actions carry an uncountable simplex of invariant measures (E–L JMD 2008). CONFIRM.
- **Row 2 (BFLM).** `Γ=ℤ[1/6]⋊⟨3/2⟩`: `ℤ[1/6]` abelian, `⟨3/2⟩≅ℤ` acting on it ⇒ metabelian ⇒
  **solvable ⇒ amenable**; `⟨A⟩` abelian. Disqualification holds. CONFIRM. *(Minor note: BFLM's exact
  hypothesis is "not virtually abelian + strongly irreducible/proximal," for which "non-abelian,
  generating a large/non-amenable subgroup" is fair shorthand; the failure is robust since `⟨3/2⟩` is
  abelian outright.)*
- **Row 3 (effective Ratner / LM / EMV).** `A` hyperbolic/diagonalizable, exponential divergence, no
  unipotent direction; orbit neither periodic nor higher-rank. CONFIRM.
- **Row 4 (Weyl/vdC/unique-ergodicity).** `A` is a hyperbolic solenoid automorphism ⇒ not uniquely
  ergodic (continuum of invariant measures); geometric `(3/2)ⁿ` has no degree drop under vdC
  differencing. CONFIRM. The "no neutral direction" is correctly attributed to **`A`** (dilations
  `(3/2,2,1/3)`, none `=1`); the note does **not** confuse this with `|2|_3=1` neutrality of the host
  generator `×2`. CONFIRM.
- **Row 5 (Gibbs–Markov / thermodynamic).** Endogenous scenery; a.e./annealed only; `F` has periodic
  points on every branch — consistent with `EMPTY_TOOLBOX_QUESTION.md` §2(a). CONFIRM.
- **Row 6 (self-similar-measure normality, ABS / Hochman–Shmerkin).** Quantifier is `μ`-a.e.-in-support;
  integer base. Attribution to **ABS, Adv. Math. 2022** is correct (matches the sweep's explicit
  correction that arXiv:2504.18192 is Algom-solo exposition). CONFIRM. *(Minor: "Hochman–Shmerkin" is
  named in the framework label but only ABS 2022 is cited; harmless.)*

---

## 4. [CONFIRM, with caveat] — Row 7 (Berkovich/adelic) is accurate but not from the EMPTY_TOOLBOX sweep

Row 7 cites **Favre–Rivera-Letelier (FRL 2010)** and **Baker–Rumely (B–R 2010)**; the characterization
(degree ≥ 2, small-height points, backward/Galois orbits) is correct, and `A=×(3/2)` is degree 1 with a
growing-height forward seed, so all three hypotheses fail — the `[PROVEN]` disqualification is sound.
**Caveat:** these citations are **not** in `EMPTY_TOOLBOX_QUESTION.md` (its sweep never surveyed
Berkovich/adelic equidistribution). They are, however, grounded in `BB6_FRAMEWORK_PACKAGE.md`'s
candidate-fields discussion ("Berkovich / adelic equidistribution (Favre–Rivera-Letelier;
Baker–Rumely; Chambert-Loir) … backward/Galois orbits of small-height points"). So this is not a
mis-attribution, but the note's masthead "Builds on `EMPTY_TOOLBOX_QUESTION.md`" slightly over-states
provenance for this row (and for Row 8, which cites repo notes rather than the sweep's primary
Mauduit–Rivat/Drmota–Spiegelhofer/Stewart references). Recommend a one-line note that Rows 7–8 extend
the sweep using the package's broader citation set.

---

## 5. [CONFIRM] — Tier-1 (PROVEN) vs Tier-2 (SURVEY-VERDICT) separation is clean; ~85% honestly carried

The per-row failures are facts about `A`, `Γ`, and the seed (rank 1; solvable/amenable; hyperbolic;
degree 1; growing height; a.e. quantifier) — each independent of the survey. The `[SURVEY-VERDICT,
~85%]` is correctly confined to the **intersection being unpopulated today**, and the `~85%` matches
the sweep's "HIGH (~85%)" for "no existing framework contains the needed specified-orbit statement"
(the sweep's *separate* MODERATE confidence about *permanence* is not misused). §3's explicit
disclaimers ("NOT proven that no framework can ever reach `T(d)`", "NOT `(K)`, NOT `¬(K)`") are
appropriately scoped. CONFIRM.

---

## 6. [CONFIRM] — no mis-attribution among sweep-sourced citations; a.e. baseline is sound

E–L JMD 2008, BFLM JAMS 24 (2011), LM arXiv:2202.11815, EMV arXiv:0708.4040, ABS Adv. Math. 2022 all
match `EMPTY_TOOLBOX_QUESTION.md` Sources; Rudolph 1990 is the standard `×2,×3` reference. §1's "A.e.
baseline `[PROVEN-in-lit]`" is correct: a hyperbolic solenoid automorphism with non-root-of-unity
multiplier `3/2` is ergodic w.r.t. Haar, so Haar-a.e. orbit equidistributes (Birkhoff). CONFIRM.

---

## Summary of required edits (priority order)

1. **#1 (CORRECT, critical):** replace every `T(d) ⟺ (K)` / "no slack" / "same wall" / "`T(d)=(K)`"
   with `T(d) ⟹ (K)` (sufficient, **strictly stronger**); delete the "equivalently a one-sided
   positive-density bound" gloss; note equivalence holds only for the restricted one-sided form. This
   is mandated by the package's own §2 ("strictly stronger, not `⟺`; full equidistribution is stronger
   still").
2. **#2 (CORRECT):** drop "mutually exclusive" / "disjoint" and the `[PROVEN that the hypotheses are
   mutually exclusive]` label; claim only the *double absence* for this action (horocycle flow is both
   unipotent and uniquely ergodic, so the feature-sets overlap in general).
3. **#1 knock-on:** add one sentence that the no-go survives for the weaker `(K)` because it operates
   at the level of framework hypotheses, not because `T(d)=(K)`.
4. **#4 caveat (minor):** flag that Rows 7–8 extend beyond the EMPTY_TOOLBOX sweep (grounded in the
   package's candidate-fields list), to keep the "Builds on" provenance honest.

*No edits made to the note. This is an audit verdict only.*
