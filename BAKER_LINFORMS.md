# Baker's theory of linear forms in logarithms — what it gives for `(3/2)^n`, and the exact gap to a density bound
*2026-06-28. Angle: the archimedean side of the Antihydra wall is the distribution of `{θ(3/2)^n}`; the
parity/`D` data is which dyadic arc `{θ(3/2)^n}` lands in. Question: does Baker's method (or its
Padé/hypergeometric descendants, or FLP's spread theorem) give any ONE-SIDED density/frequency bound, beyond
the trivial? Every line labelled [PROVEN-in-literature] / [OBSERVED] / [OPEN] / [DOES-NOT-TRANSFER].
SOUNDNESS PARAMOUNT, zero false proofs. Numerics `.venv` exact big-int. NOT committed.*

---

## 0. One-line verdict
The archimedean toolbox (FLP spread, Mahler/Flatto Z-number counts, Beukers–Dubickas–Habsieger–Zudilin
lower bounds on `‖(3/2)^n‖`, Baker linear forms on `a log2 − b log3`) is **entirely a toolbox of
SUPPORT/INDIVIDUAL-TERM statements**: it bounds the *range* (limsup − liminf) and forbids *individual*
super-close returns. **None of it gives a frequency/density statement, one-sided or otherwise, for a single
orbit.** The gap is exact and is a *known hard barrier*: equidistribution — even a one-sided power-saving in
the count `#{n≤N : {(3/2)^n}∈ arc}` — would require **cancellation in the Weyl sums `Σ e(θ(3/2)^n)`**, and
Baker-type bounds give lower bounds on *single terms*, never cancellation in a *sum*. `[PROVEN-in-literature
that the tools are support/individual-term only; the density gap is OPEN and equals the famous open
equidistribution of `(3/2)^n`].`

---

## 1. The map from our parity/`D` data to `{(3/2)^n}` `[PROVEN, exact — verified numerically]`
The parity bit driving the Antihydra carry is, exactly,
```
a_n = bit_n(8·3^n) = ⌊8(3/2)^n⌋ mod 2  =  0  ⟺  {4(3/2)^n} ∈ [0, 1/2).
```
**Verified** (`scratchpad/baker_num2.py`, exact big-int, all `n<2000`): `bit_n(8·3^n)=0 ⟺ {4(3/2)^n}∈[0,½)`
holds with zero exceptions. So the parity word is *literally* the itinerary of the orbit `{θ(3/2)^n}` (θ=4)
under the half-partition of `[0,1)`. The `D`-statistics of the induced map are the *finer* itinerary: which
**dyadic sub-arc** `{θ(3/2)^n}` occupies (mod `2^k` ⇔ a length-`k` dyadic arc). So the open core *is*
literally a statement about the **single-orbit visit frequencies of `{θ(3/2)^n}` to dyadic arcs**.

---

## 2. What is UNCONDITIONALLY proven about `{(3/2)^n}` and `{x(3/2)^n}`

### 2A. Flatto–Lagarias–Pollington (1995): a SPREAD bound, proved by SYMBOLIC DYNAMICS `[PROVEN-in-literature]`
- **Object.** `Ω(α) := inf_{θ>0} ( limsup_n {θα^n} − liminf_n {θα^n} )` (the smallest possible *spread* of the
  orbit over all real multipliers θ).
- **Theorem (FLP, Acta Arith. 70.2 (1995) 125–147).** For rational `p/q>1` in lowest terms,
  `Ω(p/q) ≥ 1/p`. In particular `Ω(3/2) ≥ 1/3`. (Mahler's conjecture would follow from `Ω(3/2) > 1/2`, which
  is **OPEN** — the FLP `1/3` falls short of `1/2`.)
- **Method `[PROVEN-in-literature]`: SYMBOLIC DYNAMICS / combinatorial digit analysis in the `p/q`-number
  system — NOT Baker's theorem.** The proof studies the admissible digit strings of the `β=p/q` expansion
  (forbidden-pattern / beta-shift combinatorics) and extracts a forced spread. Linear forms in logarithms are
  **not the engine**. (Two independent source summaries confirm "symbolic dynamics methods"; the original PDF
  did not text-extract, but this is the established characterization. Companion: AEV arXiv:2510.11723 frames
  the same object via the `T_{p/q}` map.)
- **CRUCIAL for us — RANGE vs FREQUENCY.** FLP bounds the **range/support** (`limsup−liminf` ≥ 1/3): it says
  the orbit *visits* points at least `1/3` apart. It says **NOTHING about how OFTEN** the orbit is in any arc.
  A sequence can have spread `1/3` (even spread `1`) while spending `99%` of its time in one arc. **FLP gives
  ZERO frequency/density information.** `[PROVEN: range only]`

### 2B. Mahler / Flatto Z-number counts: a SUPPORT/CONFINEMENT count, not a frequency `[PROVEN-in-literature]`
- A Z-number is `x>0` with `{x(3/2)^n} ∈ [0,½)` for **all** `n` (orbit *confined* to the lower half forever).
- **Mahler (1968):** the set of Z-numbers below `x` has size `≤ x^{0.7}` (in particular density 0; countable).
  **Flatto:** improved to `O(x^{θ})`, `θ=log₂(3/2)≈0.59`. **Recent (arXiv:2411.03468):** *no Z-number is a
  positive integer.*
- These are statements about the **rare confined orbits** (full one-sided confinement) — a measure/counting
  statement over *the multiplier `x`*, **not** a frequency statement along *one fixed* orbit. They forbid
  *permanent* one-sided confinement; they do not bound the *fraction* of `n` in an arc for a given `x`.
  `[PROVEN: confinement-count only]`

### 2C. `‖(3/2)^n‖` lower bounds (Beukers→Zudilin): INDIVIDUAL-TERM, via Padé — NOT Baker `[PROVEN-in-literature]`
- `‖·‖` = distance to nearest integer. **Trivial bound:** `‖(3/2)^n‖ ≥ 2^{−n}` (numerator `|3^n−m2^n|≥1`).
- **Beukers (1981):** `‖(3/2)^n‖ > 2^{−0.79 n}`. **Dubickas / Habsieger:** `> 0.5769^n / 0.5770^n`.
  **Zudilin (J. Théor. Nombres Bordeaux 19 (2007) 311–323):** `‖(3/2)^n‖ > 0.5803^n` for `n ≥ K`, `K`
  effective. (Constant `0.5803 = 2^{−0.78513}`.)
- **Method `[PROVEN-in-literature]`: hypergeometric / Padé approximation (Beukers construction), NOT Baker's
  linear forms.** Zudilin explicitly uses Padé approximations to a tail of `1/(1−z)^{m+1}` plus `p`-adic
  valuations of binomials. **The Padé method BEATS Baker here:** applying Baker's three-log bound to
  `n log3 − log m − n log2` (the third log `log m ~ n` has large height) gives only
  `‖(3/2)^n‖ > exp(−Cn log n)` — *worse* than the exponential Padé bound. So for `‖(3/2)^n‖` Baker is the
  wrong tool and is strictly weaker.
- **What it gives us:** these forbid `(3/2)^n` from being **exponentially** close to an integer. They are
  **single-`n`** statements. They say nothing about how the values *distribute*. `[PROVEN: individual-term]`

### 2D. Baker's genuine contribution: separation of powers `|a log2 − b log3|` `[PROVEN-in-literature]`
- The clean Baker (two-log; Laurent–Mignotte–Nesterenko sharpening) statement is for **fixed bases**:
  `|a log2 − b log3| > c·(max(a,b))^{−κ}`, `c,κ` effective. Equivalently `|2^a − 3^b| > 2^a·a^{−κ}` —
  **polynomial separation** of powers of 2 and 3. Related: `log3/log2` is transcendental (Gelfond–Schneider)
  with a **finite effective irrationality measure** (and `μ(γ)≤11.10…` for `γ∈ℚlog2+ℚlog3` via Padé,
  Rhin/Brisebarre/Wu). This is a real *archimedean* anti-clustering fact.
- **But it is again INDIVIDUAL-TERM / SUPPORT:** it controls *gaps* between powers (no two powers ultra-close),
  hence the geometry of the *support* of `{(3/2)^n}` — never the *visit frequency* of one orbit. `[PROVEN:
  separation/support only]`

---

## 3. Does ANY one-sided DENSITY statement follow? — NO `[OPEN; equals the famous open equidistribution]`
- **FLP `1/3`** is a *spread*; it gives no upper bound on `#{n≤N : {θ(3/2)^n}∈ arc}` beyond the trivial `N`.
- **Z-number counts** forbid *permanent* confinement, not a density `< 1` of visits.
- **`‖(3/2)^n‖ > 0.5803^n`** and **`|a log2−b log3|` bounds** are lower bounds on *single terms*; summed
  trivially they give `0` cancellation, hence **no discrepancy bound**.
- **Established fact:** *whether `{(3/2)^n}` is equidistributed mod 1 is OPEN*; even whether it is dense is
  open; no nontrivial one-sided density `#{n≤N:{(3/2)^n}<½} ≤ (½+o(1))N` or `≥ (½−o(1))N` is known. Our target
  `freq(D=1) ≤ ½` (⇔ `freq({4(3/2)^n}∈[0,½)) ≤ ½`) is a **one-sided special case of this open problem**.
  `[OPEN]`

---

## 4. The EXACT gap, and why it is a known hard barrier `[honest assessment]`
**Individual-term lower bounds ⟹ no clustering. Density ⟹ cancellation in a sum. These are different worlds.**
- A frequency bound `#{n≤N:{θ(3/2)^n}∈I}` is controlled (Erdős–Turán) by the **Weyl sums**
  `S_N(h)=Σ_{n≤N} e(h·θ(3/2)^n)`. A one-sided density needs **`|S_N(h)| = o(N)`** for `h≠0` (power-saving
  ⇒ quantitative). 
- Baker/Padé give `‖θ(3/2)^n‖ > (lower bound)` for **each fixed `n`** — i.e. each summand `e(hθ(3/2)^n)` is
  *bounded away from the degenerate accumulation*, which **prevents the trivial `|S_N|=N` blow-up from a single
  fixed point** but provides **no cancellation between different `n`**. There is no mechanism in an
  individual-term lower bound to make a sum small; the phases `θ(3/2)^n` are not linked by any algebraic
  relation Baker can exploit (the `(3/2)^n` are not values of a linear form in fixed logs — the exponent `n`
  sits in the base, not as a coefficient of a fixed log).
- **What would have to improve.** One would need a *power-saving in the number of close returns*: a bound of
  the shape `#{n≤N : ‖θ(3/2)^n‖ < δ} ≤ C·δ·N + N^{1−ε}` (a **discrepancy / metric** statement), uniformly in
  the arc. Baker/Padé deliver instead a *pointwise* `‖θ(3/2)^n‖ > 0.58^n` with **no `N`-averaged count**.
  Upgrading a pointwise lower bound to an averaged power-saving for the *lacunary-base* sequence `(3/2)^n` is
  **exactly the open equidistribution problem** — no method (Baker, Padé, FLP symbolic dynamics) is known to
  cross it. This is the *same* "averaged-cancellation vs pointwise-bound" barrier that appears on the ergodic
  side (`SESSION_2026-06-28_MINPROP.md`: need SRB average-genericity = effective exponential-sum cancellation,
  not a structural/pointwise fact). `[OPEN — known hard barrier]`

---

## 5. Numerics `[OBSERVED]` (`scratchpad/baker_num{,2,3}.py`, exact big-int)
**5a. Empirical equidistribution (consistent with, but not proving, the target):**
| multiplier θ | `freq({θ(3/2)^n}∈[0,½))`, `N=20000` |
|---|---|
| 1 | 0.49745 |
| 4 (our parity bit) | 0.49860 |
| 8 | 0.50085 |
| `freq(a_n=0)=bit_n(8·3^n)` | 0.4986 |
All `≈ ½`. (Finite `N` proves nothing about the limit — exactly the wall.)

**5b. Individual-term lower bound is ASTRONOMICALLY far from constraining the density.**
`‖(3/2)^n‖` in `−log₂` units (bits of closeness) vs Zudilin's forbidden floor `0.78513·n`:
| n | `−log₂‖(3/2)^n‖` (observed) | `0.78513·n` (Zudilin floor) | slack |
|---|---|---|---|
| 100 | 1.33 | 78.5 | 77 bits |
| 800 | 3.76 | 628.1 | 624 bits |
| 3200 | 1.76 | 2512.4 | 2511 bits |
The observed closeness is `O(1)`–polynomial; the only proven lower bound lives at the **exponential** scale,
`~10^{180}×` (at `n=800`) looser than reality. **The proven individual bound operates `~2500` bits away from
where the density question lives** — it cannot even *see* the `½`-vs-arc question.

**5c. Worst archimedean clustering is only POLYNOMIAL (and far above the Zudilin floor):**
`min_{n≤M} ‖(3/2)^n‖`: `−log₂(min)/log₂(M) ≈ 0.83–1.17` across `M=100..8000` ⇒ closest return scales like
`~M^{−1}` (polynomial). The proven bound forbids only `0.5803^n` (exponential). So even the *extremal* behavior
the bounds address (close returns) is empirically polynomial, with the proven floor exponentially below it —
the bounds are nowhere near tight, and tightening them to the *true* polynomial scale would *still* be a
pointwise statement giving no density.

---

## 6. Net (bankable)
1. `[PROVEN, exact]` Our parity/`D` data = single-orbit dyadic-arc itinerary of `{θ(3/2)^n}` (θ=4), verified.
2. `[PROVEN-in-literature]` FLP `Ω(3/2)≥1/3` is a **SPREAD/support** bound (symbolic dynamics, not Baker);
   Mahler/Flatto are **confinement counts**; Beukers–Zudilin `‖(3/2)^n‖>0.5803^n` and Baker `|a log2−b log3|`
   are **individual-term / separation** bounds (Padé beats Baker for `‖(3/2)^n‖`).
3. `[PROVEN-in-literature]` **NONE of these gives a frequency/density statement** (one-sided or otherwise) for
   a single orbit. FLP's `1/3` is support, not frequency; it also stops short of Mahler's `1/2` even as a
   spread.
4. `[OPEN — known hard barrier]` A one-sided density `freq({4(3/2)^n}∈[0,½)) ≤ ½` is a special case of the
   **open equidistribution of `(3/2)^n`**. The exact missing ingredient is **cancellation/power-saving in the
   Weyl sums `Σe(θ(3/2)^n)`** (a discrepancy/metric count of close returns), which individual-term Baker/Padé
   lower bounds **cannot** produce. Same averaged-vs-pointwise barrier as the ergodic SRB-genericity target.
5. `[OBSERVED]` Numerically `freq≈½` and clustering is polynomial, sitting `~2500` bits above the only proven
   (exponential) floor — quantifying *how far* the proven individual bounds are from the density question.

### Sources
- Flatto–Lagarias–Pollington, *On the range of fractional parts {ξ(p/q)^n}*, Acta Arith. 70.2 (1995) 125–147:
  http://matwbn.icm.edu.pl/ksiazki/aa/aa70/aa7023.pdf ; EUDML https://eudml.org/doc/206742
- Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. (1968); essay
  https://ems.press/content/book-chapter-files/27426
- Mahler's 3/2 problem (Ω, FLP, Z-number counts): https://en.wikipedia.org/wiki/Mahler%27s_3/2_problem
- Mahler's 3/2 problem in ℤ⁺ (no integer Z-numbers): https://arxiv.org/abs/2411.03468
- Zudilin, *A new lower bound for ‖(3/2)^k‖*, JTNB 19 (2007) 311–323:
  https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.588/ ; https://www.math.ru.nl/~zudilin/PS/wr.pdf
- *On the Uniformity of `(3/2)^n` modulo 1*: https://arxiv.org/pdf/1806.03559
- Andrieu–Eliahou–Vivion, rational-base normality (T_{p/q} equidistribution): https://arxiv.org/html/2510.11723
- Baker's theorem / linear forms in logarithms: https://en.wikipedia.org/wiki/Baker%27s_theorem ;
  irrationality measure of ℚlog2+ℚlog3 (Rhin/Brisebarre, μ≤11.10): projecteuclid em/999188419
