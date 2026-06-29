# The core extra input every SPECIFIED-point method needs — and whether seed-8 can supply it (2026-06-30)

*WEAPONS_AUDIT-style audit of the methods that actually PROVE equidistribution/normality of a **specified** (not
a.e.) point or orbit. For each: the EXACT extra arithmetic input it consumes, and a concrete assessment of
whether the (2,3)-adic / S-arithmetic structure of seed `8` (induced map `T(o)=3^{D-1}(3o-1)/2^D` on `ℤ₂^*`,
`c_{n+1}=⌊3c_n/2⌋`, `c₀=8`) could plausibly supply it. (K) = equidistribution of the one specified orbit.
SOUNDNESS: every line labelled [PROVEN-in-lit] / [OPEN] / [DOES-NOT-TRANSFER]; citations precise; no proof
claims. Companion to `WALL_B_SPECIFIC_LITERATURE.md`, `INDUCED_TAO_METHOD.md`, `SELECTOR_COMPUTABILITY.md`,
`BB6_NO_STRUCTURE_THEOREM.md`, `EMPTY_TOOLBOX_QUESTION.md`. NOT committed.*

---

## 0. One-line verdict

There are exactly **four** mechanisms in the literature that pin a *specified* point/orbit, and each consumes a
**different** extra arithmetic input: **(BC) an integer base** (→ finite power-residue group), **(Tao) averaging
over the starting point** (→ ensemble, a.e.-quantifier), **(Constr.) freedom to engineer the digits**, **(KS) a
still-open analytic certificate on the number itself**. Seed-8 can supply **none unconditionally**. Its
(2,3)-adic structure supplies *one half* of the closest one — the finite multiplicative group `(ℤ/2^kℤ)^*` with
its 3-action — but the orbit is **not** a pure power-orbit in that group: it is the 3-action **twisted by an
orbit-dependent 2-adic shift** (`÷2^{D_n}`, `D_n=v₂(3c_n-1)`), and that twist has **no finite-group model**.
The single seed-8 input that would close the closest method is exactly **single-orbit equidistribution of
`c_n mod 2^k` = (K) itself**. No method's extra input is something seed-8 meets short of (K).

---

## 1. Bailey–Crandall (Stoneham `α_{b,c}` is `b`-normal) — [PROVEN-in-lit]

**The map family is identical to ours** (`WALL_B_SPECIFIC_LITERATURE.md §2`): the proof studies the perturbed
orbit `y_{n+1} = b·y_n + r_n (mod 1)`, `r_n` rational; our carry/phase recursion is the same with `b=3/2`.

**EXACT extra input.** An **integer base `b`** (coprime to `c`). The whole unconditional proof is the reduction:
evaluating `b^{c^m}·α_{b,c} mod 1`, the block at scale `c^n<c^m` contributes `(b^{c^m−c^n} mod c^n)/c^n`, so
normality ⟺ **equidistribution of the power-residue orbit `{b^k mod c^n}` inside the FINITE cyclic group
`(ℤ/c^nℤ)^*`** — a *fixed integer's powers in a finite group*, where UD is elementary (primitive-root /
order counting). [PROVEN-in-lit: Bailey–Crandall 2002, Exp. Math. 11(4); strong hot-spot Bailey–Misiurewicz
PAMS 2006.] For `π, log2, e` the same machine needs the **unproven** dichotomy hypothesis (orbit is finite-or-UD);
**only Stoneham is unconditional**, *precisely because* the finite-group reduction exists there.

**Can seed-8's (2,3)-adic structure supply a finite-group surrogate? — examined concretely, [NO].**
- The multiplicative half **does** exist: `3 ∈ (ℤ/2^kℤ)^*` generates a finite cyclic subgroup (order `2^{k-2}`),
  and the *pure* 3-power orbit `{3^j mod 2^k}` equidistributes over that subgroup by elementary order-counting —
  a genuine Stoneham-type finite group with a 3-action.
- **But our orbit is not that power-orbit.** One step is `o ↦ 3o−1` **followed by `÷2^{D}`, `D=v₂(3o−1)`**. The
  division by 2 is **not an operation in `(ℤ/2^kℤ)^*`** (2 is a non-unit / zero-divisor mod `2^k`), and `D_n`
  is **determined by the current state** `c_n`. So the increment is the fixed group element `3` **twisted by a
  state-dependent 2-adic right-shift**. This twist is exactly the non-integrality of base `3/2`.
- **The decisive arithmetic reason the surrogate fails:** the shift couples high bits to low bits, so the action
  **does not descend to any finite quotient `(ℤ/2^kℤ)^*`** — no finite truncation is invariant. Equivalently, in
  the carry form `T_{n+1}=3T_n+2^n e_n` the relevant modulus is `2^n` and **grows with `n`** (it tracks the step
  index), whereas Stoneham reduces every digit-block to a **fixed** modulus `c^n` and takes a limit *over blocks*.
  A growing modulus = the full 2-adic limit = **no finite group**. The `(2,3)`-adic structure supplies the
  multiplier but not the "orbit = `g^n`" structure the reduction requires.
- This is the same fork as `PROOF_STATUS.md §2` (`T_n` not an S-unit) and the non-Pisot/non-sofic wall
  (`SELECTOR_COMPUTABILITY.md §5`): `3/2` non-Pisot ⟹ the β-shift is **not even sofic** [PROVEN-in-lit, Frougny;
  arXiv:1410.8594], so there is no finite-state digit machinery to run the hot-spot/automaton argument on.

**Verdict.** [DOES-NOT-TRANSFER unconditionally.] The extra input "integer base → fixed finite power-residue
group" has **no base-`3/2` analogue**; seed-8 supplies only the multiplier half, and the orbit-dependent 2-adic
shift defeats the rest. This is the single closest *proven* theorem (specified point, dynamical `b^n x`
equidistribution, proven) and the gap is exactly **integrality**.

## 2. Tao 2019 log-density (almost all Collatz orbits) — [PROVEN-in-lit, a.e.-starts only]

**EXACT extra input.** **Averaging over the STARTING POINT.** Every probabilistic statement is over the ensemble
of starts `N` weighted by `1/N` (log-density); the engine is the Geometric `v₂(3N+1)`, the Syracuse random
variable `Syrac(ℤ/3^nℤ)`, and TV-stabilization toward uniform `mod 3^n` via 3-adic skew-walk characteristic
sums. The `1/N`-weighting is **preserved by the Syracuse step** (natural density is not) — this is *why* log
density is essential. Independence comes from **varying the start** (fresh draws), never from advancing one orbit
(`INDUCED_TAO_METHOD.md §1`). [PROVEN-in-lit: Tao, Forum Math. Pi 2022, arXiv:1909.03562.]

**Is there a partial single-orbit statement? — [NO].** The method has **no time-average over one orbit**
anywhere. A single-orbit "positive-density-of-times" or one-sided `liminf mean D ≥ 3/2` would require the orbit's
empirical `D`-sequence to behave like the Geometric ensemble — i.e. **single-orbit equidistribution of
`c_n mod 2^k`**, which **is** (K)/Mahler 3/2, not a corollary of it. The weaker `1/3`-threshold relaxation does
not dodge it; it *is* it. Krasikov–Lagarias (`x^{0.84}` starts reach 1, arXiv:math/0205002) is likewise a
**count of starts**, giving nothing single-orbit; the only unconditional single-orbit valuation facts are
`D≥1`, `mean(D)≥1`. Nothing new 2023–2026: arXiv:2401.17241 (real-Collatz analogue, 2024) is still **a.e.-starts**.

**Can seed-8 supply the ensemble? — [NO, structural].** A single orbit is one realization; "make its time-stats
equal the starts-ensemble" is (K). The averaging freedom is the input, and a fixed orbit has none.

## 3. Recent specified/given-point results (2019–2026, WebSearch) — the constructed-vs-given dichotomy

| Method | Crosses to a SPECIFIED point? | EXACT extra input | Seed-8? |
|---|---|---|---|
| **Constructed normals** (Champernowne; Copeland–Erdős; Becher–Heiber–Slaman *computable* a.n., poly-time, nested intervals) [PROVEN-in-lit] | Yes — but by **design** | **Freedom to engineer the digit string** (choose the word to force normality) | **[NO]** — our parity word is **forced by the dynamics**, not free to engineer. The one mechanism that is computable-compatible AND routinely succeeds needs construction, which a *given* point denies. |
| **Kanado–Saito 2024**, *Normality of algebraic numbers and the Riemann zeta function*, arXiv:2412.02337 | Yes — a *given* algebraic α, **integer base** | A **characterization**: α is simply normal to base `b` ⟺ a specified `ζ`-limit on vertical arithmetic progressions vanishes for all `k≥0`. **The certificate is itself OPEN.** | **[NO]** — needs an **integer base** and an algebraic α whose base-`b` digits are the target; it trades normality for an unproven analytic condition. Closest *given*-point (not constructed) method found, but conditional, integer-base, and not orbit-dynamical. |
| **Algom–Baker–Shmerkin** (Rajchman ⇒ pointwise normality; exposition arXiv:2504.18192) [PROVEN-in-lit] | **No — ν-a.e.** | **Fourier decay (Rajchman) of a measure** + the a.e.-in-support quantifier | **[FIRES on our exact `ν_{2/3}`** (non-Pisot ⟹ Rajchman) **but stays ν-a.e.]**; the paper's own **Problem 1 (effective rate)** and **Problem 3 (non-integer base)** are our two walls. |
| **Periodic-orbit equidistribution** (ergodic torus endomorphisms, arXiv:2407.19665, Nov 2024) | A **sequence** of periodic orbits, not one given orbit | Freedom to **select which periodic orbits**; our orbit is aperiodic & prescribed | **[NO]** |
| **Effective homogeneous dynamics** (BFLM 2011; effective Ratner; LMMS arXiv:2202.11815) [PROVEN-in-lit] | Single orbit, but only for | **unipotent / non-abelian / rank≥2** actions | **[DOES-NOT-TRANSFER]** — `×(3/2)` is rank-1, amenable, expanding (`EMPTY_TOOLBOX_QUESTION.md`). |
| **Mahler-3/2 frontier** (arXiv:2502.17090 asymptotic Mahler 2025; arXiv:2405.08281 Turyn polynomials 2024) | The named target itself | — | **[OPEN]** — these *are* Wall (A), not external tools. |

**Computability lens (`SELECTOR_COMPUTABILITY.md`):** every *effective-randomness* selector (ML/computable/
Schnorr/Avigad-UD/Kurtz; effective-Birkhoff good set = Schnorr randoms) **provably excludes every computable
point** [PROVEN-in-lit]; our orbit point is computable. The only randomness rung compatible with computability —
finite-state randomness = normality — **is (K) itself** at base `3/2`, and the Pisot-requiring finite-automaton
characterization (arXiv:1410.8594) is unavailable since `3/2` is non-Pisot. So the "given (not constructed)
computable point" sits in the gap between *selectable-by-an-effective-test* and *computable*.

## 4. Synthesis — the common missing ingredient, and the closest method

**Each specified-point success consumes one of four extra inputs, all of which seed-8 lacks:**
1. **Integer base** → a *fixed finite multiplicative group* `(ℤ/c^nℤ)^*` on which the orbit is a pure power
   `g^k` (Bailey–Crandall). Seed-8: base `3/2`, modulus `2^n` **grows**, orbit is `g`-action **twisted by an
   orbit-dependent 2-adic shift** → no finite-group model.
2. **Ensemble averaging over the start** → an a.e.-quantifier (Tao, Krasikov–Lagarias, Rajchman⇒a.e., Birkhoff,
   effective-Birkhoff). Seed-8: a single fixed orbit, zero averaging freedom.
3. **Construction freedom** → engineer the digits (Champernowne, Becher–Heiber–Slaman). Seed-8: digits forced.
4. **A still-open analytic certificate on the number** (Kanado–Saito `ζ`-condition). Seed-8: integer-base,
   algebraic-α form; trades (K) for another open statement.

**The COMMON missing arithmetic ingredient** is a **fixed finite (or sofic / bounded-carry) multiplicative model
in which the orbit's increments act as one fixed group element** — equivalently a place where the orbit becomes a
*pure power-orbit* and equidistribution is elementary OR averageable. Integrality, Pisot-soficity, ensemble
freedom, and construction freedom are the four ways the literature obtains it; **base `3/2` is non-integer,
non-Pisot, the orbit is single and given, and the relevant modulus `2^n` grows** — so all four are absent.

**Closest method + its precise requirement.** **Bailey–Crandall** is the closest (identical map family
`y_{n+1}=b y_n + r_n mod 1`). The one seed-8-specific arithmetic input it would need is a **finite-group
surrogate for the 3-action-twisted-by-2-adic-shift** — i.e. that the shift exponents `D_n=v₂(3c_n−1)` be
Geometric/equidistributed along the orbit, which is precisely **single-orbit equidistribution of `c_n mod 2^k`
= (K) = Mahler 3/2 / AEV Conj. 1.6**. The (2,3)-adic structure supplies the *multiplier* `(ℤ/2^kℤ)^*` but not
this; supplying it **is** the open problem, not an input to it.

---

## Sources
- Bailey–Crandall, *Random Generators and Normal Numbers*, Exp. Math. 11(4) (2002):
  https://projecteuclid.org/euclid.em/1057864662 ; *On the Random Character of Fundamental Constant Expansions*,
  Exp. Math. 10(2) (2001): https://projecteuclid.org/journals/experimental-mathematics/volume-10/issue-2/.../em/999188630.pdf
- Bailey–Misiurewicz, *A strong hot spot theorem*, PAMS (2006); Bailey–Borwein, *Nonnormality of Stoneham
  constants*, Ramanujan J. (2012); Coons et al., *An arithmetical excursion via Stoneham numbers*, arXiv:1212.3449.
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi (2022),
  arXiv:1909.03562 ; Krasikov–Lagarias, Acta Arith. 109 (2003), arXiv:math/0205002 ; real-Collatz analogue
  arXiv:2401.17241 (2024).
- **Kanado–Saito, *Normality of algebraic numbers and the Riemann zeta function*, arXiv:2412.02337 (Dec 2024)**
  — given algebraic α, integer base; normality ⟺ a `ζ`-vertical-AP vanishing condition (itself open).
- Algom, *Recent progress on pointwise normality of self-similar measures*, arXiv:2504.18192 (2025), expounding
  Algom–Baker–Shmerkin, Adv. Math. (2022), arXiv:2107.02699 (Rajchman ⇒ ν-a.e. absolutely normal; open Problems
  1 effective rate, 3 non-integer base).
- Becher–Heiber–Slaman, *A polynomial-time algorithm for computing absolutely normal numbers*,
  https://math.berkeley.edu/~slaman/papers/poly.pdf ; nearly-linear time, ScienceDirect S0890540121000614.
- Madritsch–Scheerer et al., *Normality in non-integer bases and polynomial time randomness*, arXiv:1410.8594
  (P-martingales; poly-time random + **Pisot** ⇒ β-normal — Pisot essential).
- Avigad, *Uniform distribution and algorithmic randomness*, JSL 78(1) (2013), arXiv:1203.4126; Gács–Hoyrup–Rojas
  / Bienvenu et al. effective Birkhoff arXiv:1007.5249.
- Andrieu–Eliahou–Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025);
  Eliahou–Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*, arXiv:2504.13716 (2025).
- Mahler 3/2 frontier: arXiv:2502.17090 (asymptotic Mahler problems, 2025); arXiv:2405.08281 (*Mahler's problem
  and Turyn polynomials*, 2024); ergodic periodic-orbit equidistribution arXiv:2407.19665 (2024);
  BFLM, JAMS 24 (2011); effective homogeneous dynamics arXiv:2202.11815.
- (repo cross-refs) `WALL_B_SPECIFIC_LITERATURE.md`, `INDUCED_TAO_METHOD.md`, `SELECTOR_COMPUTABILITY.md`,
  `BB6_NO_STRUCTURE_THEOREM.md`, `EMPTY_TOOLBOX_QUESTION.md`.

**No machine decided. No label upgraded.**
