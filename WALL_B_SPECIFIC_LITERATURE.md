# Wall (B): the a.e.→SPECIFIC gap — literature attack on "any framework that proves
# equidistribution/normality for a SPECIFIC, computable point"
*2026-06-28. Wall (B) = the named-orbit selection wall (`c₀=8` is a single point = measure zero; Tao
a.e.→specified). This note surveys EVERY framework that crosses a.e.→specific in ANY setting, then assesses
transfer to the base-`3/2` orbit. Companion to `COCYCLE_ERGODICITY.md §4` (homogeneous-dynamics route, closed)
and `SESSION_2026-06-28_TWISTED_RPF.md` (wall (A) = gap=Mahler). Every line labelled
[PROVEN-in-literature] / [CONDITIONAL] / [OPEN] / [DOES-NOT-TRANSFER]. Zero false proofs. NOT committed.*

---
## 0. One-line verdict
The literature crosses a.e.→specific in exactly **two** ways, and a near-miss third:
1. **CONSTRUCTED points** — digits *engineered* to force normality (Champernowne, Copeland–Erdős,
   Sierpiński, Lehmer, Becher–Heiber–Slaman computable a.n., **and Stoneham `α_{b,c}`**). All **integer base**.
2. **Effective homogeneous dynamics** — unipotent/polynomial orbits pinned by effective Ratner / spectral
   gap. Needs **unipotency**; `×(3/2)` is **expanding** (opposite). [DOES-NOT-TRANSFER] — already in
   `COCYCLE_ERGODICITY.md §4`.
3. **Near-miss:** Rajchman ⟹ *pointwise absolute normality* of self-similar measures (Algom–Baker–Shmerkin
   circle, 2025). Strongest recent a.e.→"specific" upgrade — but it is **ν-a.e., not a named point**, and the
   non-integer-base case is its **explicitly open Problem 3**.

**Our orbit `c₀=8` fails to qualify for all three:** it is (i) **pre-given, not constructible** — we cannot
choose its digits to force normality, the mechanism behind family 1; (ii) **non-integer base `3/2`** — kills
the integer power-residue reduction that makes the Stoneham member of family 1 *unconditional*; (iii)
**expanding, not unipotent** — kills family 2. The Bailey–Crandall Stoneham theorem is **the single closest
proven theorem** ("specific point + dynamical `bⁿx mod 1` equidistribution + proven"), and the **exact extra
hypothesis it needs and we cannot supply is integrality of the base**.

---
## 1. The frameworks that pin a SPECIFIC point — full list with citations

### 1A. Constructed normal numbers (digits engineered) — [PROVEN-in-literature, but by design]
The orbit's digits are *built* to be normal; normality is not *deduced* from a pre-existing definition.
- **Champernowne 1933** `0.123456789101112…` — normal base 10 by concatenation. (Wolfram MathWorld;
  arXiv:2109.00562 "Equidistribution Mod 1 And Normal Numbers".)
- **Copeland–Erdős 1946** `0.235711131719…` (primes) — normal base 10; Besicovitch/Davenport–Erdős
  (squares, integer-valued polynomials `σ_q(f)`). (MathWorld Copeland–Erdős; arXiv:1511.07532 strong
  normality & generalised Copeland–Erdős.)
- **Sierpiński 1917 / Lehmer / Becher–Figueira** — explicit *absolutely* normal numbers (every integer base).
- **Becher–Heiber–Slaman 2013** — a **computable** absolutely normal number, digits in **polynomial time**
  (just above quadratic), discrepancy `~O(1/log N)`; nested-interval construction. (math.berkeley.edu
  slaman/poly.pdf; arXiv:1511.03582, 1702.04072, 1510.02004 Levin low-discrepancy.)
- **[KEY] Why none transfer:** every one of these *chooses the digit string*. Our `c₀=8` orbit's parity word
  `bitₙ(Tₙ)` is **forced by the dynamics**, not free to engineer. Family 1's mechanism — "design a
  normal-by-construction word" — is structurally unavailable. (This is the cleanest statement of why Wall (B)
  is hard: the only routinely-successful a.e.→specific route is *construction*, and we have a *given* point.)

### 1B. Bailey–Crandall Stoneham — the bridge from "constructed" to "proven dynamical equidistribution"
- **Object.** `α_{b,c} = Σ_{n≥1} 1/(cⁿ b^{cⁿ})`, `b,c≥2` integers, `gcd(b,c)=1` (Stoneham 1973).
- **[PROVEN-in-literature] Theorem (Bailey–Crandall 2002, *Random Generators and Normal Numbers*, Exp. Math.
  11(4) 527–546).** `α_{b,c}` is **`b`-normal**, *unconditionally*. (davidhbailey.com/dhbpapers/bcnormal.pdf;
  projecteuclid em/1057864662.) Later: it is **not** `bc`-normal (Bailey–Borwein, *Nonnormality of Stoneham
  constants*, Ramanujan J. 2012) — abnormal in a related base, sharpening the role of the base.
- **Mechanism (Wall criterion + hot-spot lemma).**
  - **Wall's criterion:** `x` is `b`-normal ⟺ `{bⁿ x mod 1}` is **uniformly distributed mod 1**.
  - **Hot-spot lemma (Bailey–Crandall; strong form Bailey–Misiurewicz, *A strong hot spot theorem*, PAMS
    2006):** `x` is `b`-normal ⟺ the `b`-ary shift orbit has **no hot spot** (no `y` whose shrinking
    neighbourhoods are visited with anomalously high frequency). This is a property of the **integer
    `b`-transformation `T(x)=bx mod 1`** on the circle.
  - **Reduction to a perturbed orbit (the shape that matches us):** they study
    `y_{n+1} = b·y_n + r_n  (mod 1)`, `r_n = p(n)/q(n)` rational, and show the perturbed orbit asymptotically
    tracks the pure `b`-transformation orbit, so it is UD ⟺ the constant is normal. **(Bailey–Crandall, *On
    the random character of fundamental constant expansions*, Exp. Math. 10(2) 2001, projecteuclid
    em/999188630; arXiv:math/0101055.)**
- **Hypothesis A (the conditional part).** For `π, log 2, e, ζ(3)` etc. they reduce normality to a
  **dichotomy hypothesis**: each BBP-type orbit `y_{n+1}=b y_n + r_n mod 1` *either has finitely many limit
  points or is UD*. **This hypothesis is UNPROVEN** — `π/log2/e` normality stays conditional. **Only the
  Stoneham class is unconditional**, precisely because there the orbit's UD is provable by elementary number
  theory (next bullet).
- **WHERE INTEGER `b` IS ESSENTIAL (the load-bearing point for us).** For the Stoneham proof one evaluates
  `b^{c^m}·α_{b,c} mod 1`. The term `1/(cⁿ b^{cⁿ})` contributes `b^{c^m−cⁿ}/cⁿ`; for `cⁿ<c^m` this is
  *integer over `cⁿ`*, so mod 1 it equals `(b^{c^m−cⁿ} mod cⁿ)/cⁿ`. **The whole proof is the equidistribution
  of the power-residue orbit `b^k mod cⁿ` inside the finite cyclic group `(ℤ/cⁿℤ)*`** — an *integer*
  multiplier acting on a *finite group*, where UD is elementary. **`b^{k} mod cⁿ` is meaningless for `b=3/2`**
  (you cannot reduce a non-integer power modulo an integer; there is no finite-group orbit). That single
  arithmetic step is where integrality is irreplaceable.

### 1C. Effective homogeneous dynamics (Ratner/spectral) — [DOES-NOT-TRANSFER]
Pins specific orbits, but needs **unipotent/polynomial** flows on finite-volume homogeneous spaces
(LMMS arXiv:2202.11815; horosphere translates 2110.00706, 1701.04977; BFLM needs rank≥2 / two
multiplicatively independent directions). `×(3/2)` is **rank-1 expanding, self-dual** → opposite regime.
Already adjudicated and closed in `COCYCLE_ERGODICITY.md §4`. **Restated here only to confirm it is not a
specific-point loophole for us.**

### 1D. Rajchman ⟹ pointwise normality of self-similar measures — [near-miss, still a.e.]
- **Theorem (Algom–Baker–Shmerkin and successors; survey arXiv:2504.18192 "Recent progress on pointwise
  normality of self-similar measures").** If a self-similar measure `ν` is **Rajchman** (`ν̂(q)→0`,
  `|q|→∞`) then `ν` is **pointwise absolutely normal**: `ν`-a.e. point is absolutely normal — *with no decay
  rate required* (improves Davenport–Erdős–LeVeque 1964).
- **VERY relevant to us, yet [STILL a.e.]:** our scenery measure is the Bernoulli convolution `ν_{2/3}`,
  which is **Rajchman** because `3/2` is **non-Pisot** (Li–Sahlsten / Varjú–Yu; `THERMO_FORMALISM.md`,
  `mckean_contraction.py`). So this theorem *fires on exactly our measure* — but its conclusion is **`ν`-a.e.,
  not a named point**: "the measure assigns full weight to normal numbers," seed 8 is one null point and
  nothing selects it (verbatim the §0 obstruction). The paper's **Problem 1** is precisely *effective*
  equidistribution of the orbit when `x` is sampled from `ν` (open), and **Problem 3** is precisely the
  *non-integer base* extension (open). **The strongest recent a.e.→specific upgrade stops one inch short on
  both axes that we need.**

### 1E. AEV rational-base normality — the named target itself (a CONJECTURE, not a tool) — [OPEN]
- **Andrieu–Eliahou–Vivion 2025, arXiv:2510.11723, "A Normality Conjecture on Rational Base Number
  Systems".** Conjecture 1.2: in base `p/q` (here `3/2`) every minimal word is normal over `{0,…,q−1}`
  (= `{0,1}`), every maximal word over `{p−q,…,p−1}` (= `{2}`). **Theorem 1.7:** normality (Conj. 1.2) ⟺
  equidistribution of the `T_{p/q}` iterates (Conj. 1.6); and **normality ⟹ Mahler's 3/2 / `Z_{p/q}`
  (Conj. 1.4) when `p<q²`** (a minimal word containing letter `0` forbids confinement to `[0,1/q)`).
- **[OPEN, and contains the same gap]:** AEV prove an *equivalence* and *numerical evidence* (139 minimal
  words to `10⁶`, deviations indistinguishable from random) but **no specific word/number is proven normal**.
  It is the **named statement of Wall (B)+(A) together for base 3/2**, not an external theorem that crosses
  the gap.

---
## 2. The CRUCIAL transfer question — precisely why Bailey–Crandall breaks at base `3/2`
**Our recursions have *exactly* the Bailey–Crandall shape** (`PROOF_STATUS.md §1`,
`SESSION_2026-06-28_TWISTED_RPF.md`):
- carry: `T_{n+1} = 3T_n + 2ⁿ e_n` ; phase: `φ_{n+1} = (3/2)φ_n + e_n/4 (mod 1)`
- Bailey–Crandall: `y_{n+1} = b·y_n + r_n (mod 1)` with **`b` integer**, `r_n` rational.

So the **map family is identical with `b = 3/2`.** The method fails at three nested points, all the
non-integer/non-Pisot obstruction:

1. **Wrong invariant measure / wrong symbolic coding.** For integer `b`, `T(x)=bx mod 1` preserves
   **Lebesgue**, is a **full one-sided `b`-shift**, and `k`-th digit `= ⌊bᵏx⌋ mod b` *is* the symbol. For
   `b=3/2` the relevant map is the **β-transformation `T_β(x)=βx mod 1`**, whose invariant measure is the
   **Parry measure (≠ Lebesgue)**, and whose β-shift is **constrained, not a full shift**. (Rényi;
   arXiv:1410.8594 "Normality in non-integer bases and polynomial time randomness"; 1707.01013.) The
   hot-spot↔digit-frequency equivalence is built on the full-shift integer picture.

2. **`3/2` is NOT Pisot/Parry ⇒ the β-shift is not even sofic.** Normalization in base `β` is computable by a
   finite automaton **iff `β` is Pisot** (Frougny). `3/2` is non-Pisot, so there is **no finite-state digit
   structure** to run a hot-spot/automaton argument on. (Grokipedia non-integer base; arXiv:1503.08047
   Normality in Pisot numeration systems.) This is the *same* non-Pisot fork that, on the Fourier side, makes
   `ν_{2/3}` Rajchman (`THERMO_FORMALISM.md`): non-Pisot helps the *annealed* tier but destroys the *finite
   symbolic* machinery that pins a *specific* orbit.

3. **No finite power-residue reduction (the decisive arithmetic).** Stoneham is unconditional *only* because
   `b^{k} mod cⁿ` lives in the finite cyclic group `(ℤ/cⁿℤ)*` and equidistributes by elementary means
   (§1B). With `b=3/2` there is **no `b^{k} mod cⁿ`** — the integer-modulus reduction that converts "orbit
   UD" into "finite-group power equidistribution" **does not exist**. This is the exact analogue of
   `PROOF_STATUS.md §2`'s "T_n not an S-unit / `8·3ⁿ−T_n` not S-unit": the multiplicative structure that
   carries integer-base proofs is absent.

**Light numeric (illustrative, `.venv`; recursion-shape match + the dichotomy):** running
`y_{n+1}=b y_n + r_n mod 1`, `r_n∈{0,¼}`, `N=2·10⁵`:
- `b=2` (integer): orbit **confines to dyadic rationals** → χ²(10 bins) huge (`3·10⁵`) = the *"finitely many
  limit points"* horn of the Bailey–Crandall dichotomy (degenerate, but a *clean* alternative).
- `b=3/2` (ours): orbit does **not** confine (χ²≈5·10³, spread) **but is biased** (`P(y<½)=0.555≠0.5`) —
  **neither finite nor visibly UD**: precisely the regime the dichotomy hypothesis cannot resolve, and where
  no integer-base tool applies. The true Antihydra orbit `c₀=8` has even-density `0.4997–0.5016` over
  `N=1.5·10⁵` (consistent with UD, unproven). The shapes coincide; only the base differs, and the base is the
  whole obstruction.

---
## 3. The single closest theorem, and the exact missing hypothesis
- **Closest PROVEN theorem:** **Bailey–Crandall (2002): the Stoneham constant `α_{b,c}` is `b`-normal**, i.e.
  the specific orbit `{bⁿ α_{b,c} mod 1}` is *provably* uniformly distributed with the right (BBP-style)
  effectivity — a **specific point, dynamical `bⁿx` equidistribution, proven**. It is the unique place the
  literature proves a *pre-presented constant's* `bⁿx`-orbit equidistributes (everything else of family 1 is
  digit-construction; family 1C/1D are a.e.).
- **Exact extra hypothesis it needs that we cannot supply:** **the base `b` must be an integer** (so that
  `b^{k} mod cⁿ` is a power-residue orbit in the finite group `(ℤ/cⁿℤ)*`, where equidistribution is
  elementary, and so that `T(x)=bx mod 1` is the Lebesgue-preserving full `b`-shift on which the hot-spot
  lemma operates). **Our base is `3/2`** — non-integer, non-Pisot. There is no `(ℤ/cⁿℤ)*`, no full shift, no
  Parry-trivial measure, no finite automaton.
- **Closest CONJECTURE (same base, right object):** **AEV Conj. 1.2/1.6 (base `3/2`)** — literally "specific
  word/point, base `3/2`, equidistribution," but **open**, and it *is* Wall (A)+(B) restated, not a tool.
- **Strongest a.e.→specific upgrade that touches our exact measure:** **Rajchman ⟹ pointwise normality**
  (arXiv:2504.18192) — fires on `ν_{2/3}` because `3/2` is non-Pisot, but delivers only **ν-a.e.** and lists
  the two things we need (effective rate; non-integer base) as its own **open Problems 1 and 3**.

---
## 4. Net assessment for Wall (B)
- **[PROVEN-in-literature]** The only routinely-successful a.e.→specific mechanism is **construction**
  (engineer the digits). Our orbit is **given**, not constructible → unavailable.
- **[PROVEN-in-literature]** The one case where a *given* constant's `bⁿx`-orbit is *proven* equidistributed
  is **Stoneham (Bailey–Crandall)**, and it is unconditional **only via the integer power-residue reduction
  `b^{k} mod cⁿ`**, which has **no base-`3/2` analogue**.
- **[DOES-NOT-TRANSFER]** Effective Ratner/BFLM (needs unipotency/rank≥2); confirmed, with
  `COCYCLE_ERGODICITY.md §4`.
- **[near-miss / STILL a.e.]** Rajchman⟹pointwise normality fires on our exact `ν_{2/3}` but stays ν-a.e.;
  the non-integer + effective extensions are its stated open problems.
- **[OPEN]** **No framework in the literature crosses a.e.→specific for a *given* orbit in a *non-integer*
  base.** Wall (B) for `c₀=8` coincides with AEV's open rational-base normality conjecture; supplying it for
  this orbit is (with Wall (A)=Mahler) the new mathematics. The honest position is unchanged: *path-short
  (one named open point), calendar-far (the named point is an open conjecture)* — but now with the precise
  reason pinned: **every successful specific-point method is gated on either constructibility or integrality
  of the base, and we have neither.**

### New attack surface opened by this pass (do not narrow)
- **Most exploitable lead:** the **Rajchman ⟹ pointwise normality** machinery (Algom–Baker–Shmerkin,
  arXiv:2504.18192) is the *only* a.e.→specific upgrade that already fires on `ν_{2/3}`. Its **Problem 1
  (effective rate when `x ~ ν`)** and **Problem 3 (non-integer base)** are *exactly* our two walls stated as
  the field's own open problems — meaning Wall (A)+(B) for Antihydra is a **named special case of an active
  research frontier**, not an isolated curiosity. Worth tracking and, if a non-integer extension of Thm 1.2
  appears, transferring immediately.
- The β-transformation / Parry-measure framing (`T_{3/2}`, non-sofic shift) is the correct symbolic home for
  Wall (B) and connects directly to AEV's `T_{p/q}` equidistribution Conj. 1.6 — a citable, precise bridge
  between our object and the published conjecture.

### Sources
- Bailey–Crandall, *Random Generators and Normal Numbers*, Exp. Math. 11(4) (2002):
  https://www.davidhbailey.com/dhbpapers/bcnormal.pdf ; https://projecteuclid.org/euclid.em/1057864662
- Bailey–Crandall, *On the Random Character of Fundamental Constant Expansions*, Exp. Math. 10(2) (2001):
  https://projecteuclid.org/journals/experimental-mathematics/volume-10/issue-2/.../em/999188630.pdf ;
  arXiv:math/0101055
- Bailey–Misiurewicz, *A strong hot spot theorem*, PAMS (2006): https://www.osti.gov/servlets/purl/886604
- Bailey–Borwein, *Nonnormality of Stoneham constants*, Ramanujan J. (2012):
  https://www.davidhbailey.com/dhbpapers/nonnormality.pdf
- Andrieu–Eliahou–Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723:
  https://arxiv.org/html/2510.11723
- *Recent progress on pointwise normality of self-similar measures* (Rajchman⟹pointwise normality),
  arXiv:2504.18192: https://arxiv.org/html/2504.18192
- *Normality in non-integer bases and polynomial time randomness*, arXiv:1410.8594:
  https://arxiv.org/pdf/1410.8594 ; *Numbers with simply normal β-expansions*, arXiv:1707.01013
- *Normality in Pisot Numeration Systems*, arXiv:1503.08047 (finite automaton ⟺ Pisot)
- Becher–Heiber–Slaman, *A polynomial-time algorithm for computing absolutely normal numbers*:
  https://math.berkeley.edu/~slaman/papers/poly.pdf ; discrepancies arXiv:1511.03582, 1702.04072
- Champernowne / Copeland–Erdős: MathWorld; arXiv:2109.00562, 1511.07532
- Mahler's 3/2 problem (Flatto–Lagarias–Pollington `Ω(p/q)>1/p`): https://en.wikipedia.org/wiki/Mahler%27s_3/2_problem
