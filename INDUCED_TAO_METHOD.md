# Tao's log-density / Collatz method, aimed at the induced odd map (2026-06-28)

Angle: does Tao (2019, arXiv:1909.03562) "Almost all Collatz orbits attain almost bounded values",
its Syracuse-random-variable machinery, or Krasikov–Lagarias (2003) give a *one-sided unconditional*
control of the D-statistics of OUR single induced orbit, enough for the non-halt target?

Setup (GAP LEMMA, this repo). Base map `h ← floor(3h/2)`, `h₀=8`. Non-halt ⇔ counter
`c = 2·evens − odds = 3·E_n − n ≥ 0` forever ⇔ **even-density `E_n/n ≥ 1/3`** forever.
Induced odd map: from odd `o`, `D = v2(3o−1)`, next odd `o' = 3^{D−1}(3o−1)/2^D`; the base-map GAP
to the next odd is exactly `D` (1 odd step + (D−1) even steps per renewal). Hence over `R` renewals
covering `n = ΣD_j` base-steps,
> even-density `= 1 − R/ΣD_j = 1 − 1/mean(D)`  ⟹  **non-halt target ⇔ `liminf` running-mean `D ≥ 3/2`.**

Syracuse heuristic: for "random" odd `o`, `D = v2(3o−1)` is **Geometric(1/2)**, `P(D=k)=2^{-k}`,
**mean 2**. `2 > 3/2` with margin `1/2`. The whole question is whether the SINGLE orbit's `liminf`
mean(D) stays `≥ 3/2`. Every line labelled. **Zero false proofs. NOT committed.**

---

## 0. One-line verdict
**[OPEN — same wall.]** Neither Tao 2019 nor Krasikov–Lagarias gives an unconditional one-sided bound
`liminf mean(D) ≥ 3/2` for our fixed orbit. Both are **averages over STARTING POINTS** (Tao: log-density-1
set of starts; K–L: a count of starts), and **neither converts to "almost all TIMES n" along one fixed
orbit.** The transfer fails at exactly the documented a.e.-starts → specified-orbit gap (= line (5) /
Mahler 3/2). What is real: the induced D-sequence empirically matches Geometric(1/2) to 3 decimals with
`liminf` running-mean(D) ≈ 1.75–2.0 (margin `≳ +0.25`), i.e. the target holds with ~`+0.5` margin
**OBSERVED, not proven.**

---

## 1. What Tao 2019 actually proves, and the exact role of "almost all starts" — [surveyed]

**Main theorem (Thm 1.2).** For *any* `f` with `f(N) → ∞`, `Col_min(N) ≤ f(N)` for **almost all** `N ∈ ℕ+1
in the sense of LOGARITHMIC density**, where `Col_min(N) = min` of the orbit of `N`. (E.g. `Col_min(N) <
log log log log N` for a.a. N.) It is **not** convergence to 1, and **not** natural density.

**The machinery.**
- Syracuse map `Syr(N) = (3N+1)/2^a`, `2^a ‖ (3N+1)`. The exponent `a = v2(3N+1)` is **Geometric**:
  `P(a=k) = 2^{-k}`, mean 2 (same distribution as our `D`).
- **Syracuse random variable** `Syrac(ℤ/3ⁿℤ) = Σ_{j} 3^{j-1} 2^{-(a_1+...+a_j)} mod 3ⁿ`, with
  `a_1,...,aₙ` iid Geometric(mean 2). Key proposition: the iterates, viewed `mod 3ⁿ`, **stabilize toward
  uniform** — the stated TV bound `Σ_Y |P(Syrac(ℤ/3ⁿ)=Y) − 3^{m−n}P(Syrac(ℤ/3ᵐ)=Y mod 3ᵐ)| ≪_A m^{-A}`.
  Proven via the characteristic function of a skew random walk on a 3-adic cyclic group at high
  frequency (a 2-D renewal process meeting a union of triangles).
- **Logarithmic density** is what lets the local "almost-sure control" be iterated using an invariant
  measure for the dynamics: `1/N`-weighting is preserved under the multiplicative-ish Syracuse step, so
  the a.s. local statement can be propagated; natural density is **not** so preserved (this is *why* Tao
  must drop from Korec's natural density to log density).

**The exact role of "almost all STARTS" — [PROVEN limitation, from the paper's own structure].** Every
probabilistic statement is over the **ensemble of starting integers** `N` (weighted by `1/N`). The
"transport"/stabilization is a statement about the **distribution of `Syr^k(N)` as `N` ranges over the
log-density measure**, never about the temporal sequence `a_1(N₀), a_2(N₀), …` for a single fixed `N₀`.
Tao's own framing: the result addresses **population-level** behavior; the abstract/intro give **nothing**
for an individual fixed orbit, and nothing for "almost all times `n`" within one trajectory. The
exceptional set is log-density 0 but **uncountable** and may contain any prescribed computable point —
our `c₀=8` is one such point.

## 2. The transfer question: "almost all TIMES n" for our single orbit? — [OPEN, method averages over starts]

The hope: maybe Tao-style machinery controls the D-statistics of our **one** orbit for a log-density-1
set of **times `n`**, which (with the finite check + the `≥1/3` threshold) could suffice if exceptional
times are sparse. **Honest assessment: Tao's method does NOT deliver this, for a structural reason.**

- Tao's averaging variable is the **starting point `N`**; the invariant measure / `1/N` weighting and the
  3-adic characteristic-sum cancellation are all taken **over that ensemble**. There is no "time average
  over one orbit" anywhere in the argument — the renewal process he analyzes is the *fresh* `a_j` of
  *independent draws*, realized by *varying the start*, not by *advancing one orbit*.
- To turn it into a single-orbit time statement one needs the orbit's empirical `D`-sequence to behave
  like the Geometric ensemble — i.e. **single-orbit equidistribution of `c_n mod 2ᵏ`** (so that
  `v2(3c_n−1)` has the Geometric law along the orbit). That is precisely **line (5) / Mahler 3/2 / the
  §3.6 effective-single-orbit-equidistribution object** that the whole program is stuck on. The
  "almost-all-n" reformulation does not dodge it; it **is** it. (Same conclusion reached from the
  cocycle-ergodicity side in `COCYCLE_ERGODICITY.md` §3, and the effective-bootstrap side in
  `WALLB_EFFECTIVE.md` §2.)
- Caveat in our favor, but not a proof: "almost all `n`" with a `1/3` threshold is **genuinely weaker**
  than full equidistribution — we would only need the running mean of `D` to stay `≥ 3/2`, i.e. the
  density of "deficit" times to be controllable, not the digit to be exactly uniform. But Tao's method
  supplies neither a single-orbit a.a.-`n` statement nor a one-sided deficit bound; it supplies only an
  over-STARTS statement. **No partial transfer is available.** [OPEN]

## 3. Unconditional one-sided bound? Krasikov–Lagarias (2003) — [PROVEN it does NOT transfer]

**Krasikov–Lagarias, "Bounds for the 3x+1 problem using difference inequalities", Acta Arith. 109 (2003)
237–258 (arXiv:math/0205002).** Main theorem (abstract, verbatim): *"at least `x^{0.84}` of the integers
below `x` contain 1 in their forward orbit under the 3x+1 map"* (more generally any fixed `a` not divisible
by 3, in place of 1, for large `x`). Proven by computer-aided analysis of difference-inequality systems.

**Assessment — it does not give `mean D ≥ 3/2` for our orbit:**
- It is a **COUNT of starting integers `n < x`** whose orbit hits a target value — a *population* lower
  bound, **not** a statement about any single orbit, and **not** about the `v2`-valuation / `D`-distribution
  or the even-step density along an orbit.
- The `x^{0.84}` exponent measures how many starts are "tamed"; it says **nothing** about the temporal
  even-density of the one start `8` (which is the quantity we need). There is **no** one-sided
  `liminf mean(D) ≥ 3/2` (nor `even-density ≥ 1/3`) extractable from it for a fixed orbit.
- This matches the only unconditional *single-orbit* facts we have: trivially `#odd ≤ log_2(3)·n` ⟹
  `mean(D) ≥ 1` (i.e. `even-density ≥ 0`), and `D ≥ 1` always — both far short of `3/2`. Any `D ≥ 3/2`
  is, like the Geometric mean-2 heuristic, **conditional on equidistribution** (cf.
  `WALLB_VALUATION_SHARP.md`: `{D≥k} = {c ≡ 3^{-1} mod 2ᵏ}`, a cylinder of relative measure `2^{1−k}`;
  bounding its frequency = single-orbit equidistribution).

> **[PROVEN-in-scope]** No unconditional one-sided bound `mean D ≥ 3/2` (equivalently `even-density ≥ 1/3`)
> for the specific orbit follows from Krasikov–Lagarias or any counting-of-starts result. The only
> unconditional single-orbit valuation facts are `D ≥ 1` and `mean(D) ≥ 1`.

## 4. Numerics — `induced_tao_method.py` (.venv, exact bigint, N = 3·10⁵ base-steps) — [OBSERVED]

| quantity | real orbit (c₀=8) | Geometric(1/2) model |
|---|---|---|
| renewals `R` | 150,192 | 150,192 (3 seeds) |
| even-density (base) | 0.499360 | — |
| `mean(D)` | 1.99742 | 1.998–1.999 |
| `1 − 1/mean(D)` vs even-density | 0.499355 vs 0.49936 (renewal identity ✓) | — |
| running-mean(D) MIN after warmup-20 | **1.7500** | 1.60–1.86 |
| running-mean ever `< 1.7 / 1.6 / 1.5` | **never / never / never** | (model dips toward 1.6) |
| worst prefix slack `min_j[ΣD_i − 1.5j]` | **+2.5 at renewal 1** (>0 ⟹ running mean never < 3/2 at any time) | — |
| end slack `ΣD − 1.5R` | **+74,709** (huge margin) | — |

`D`-distribution (real vs `2^{-k}`): k=1 .500/.500, k=2 .250/.250, k=3 .125/.125, k=4 .0623/.0625,
k=5 .0307/.0312, k=6 .0157/.0156, k=7 .0078/.0078, k=8 .0039/.0039 — **matches Geometric(1/2) to 3
decimals.** Real orbit's `liminf` running-mean(D) holds `≥ 1.5` with `+0.25` margin (warmup) and in fact
**never crosses `1.5` from renewal 1 onward** (worst prefix slack strictly positive), with end slack
`≈ +7.5·10⁴`. The `3/2` target is robust **empirically**.

> **[OBSERVED, not proven]** The single orbit's `D`-statistics are Geometric(1/2)-like and keep
> `liminf mean(D) ≈ 2 ≥ 3/2` with a large absolute slack. This is the visible content of the Syracuse
> heuristic — but it is OBSERVED data of the very equidistribution that is open, not a derivation of it.

## 5. Bankable conclusions (0 false proofs)
1. **[surveyed]** Tao 2019 = `Col_min(N) ≤ f(N)` for **log-density-a.a. STARTS `N`** (any `f→∞`); engine =
   Geometric `v2`, Syracuse random variable `Syrac(ℤ/3ⁿ)`, TV-stabilization toward uniform mod `3ⁿ` via
   3-adic skew-walk characteristic sums; **log density is essential** (preserved by the step, natural
   density is not). The averaging is **over starting points**, never over time along one orbit.
2. **[OPEN — = line (5)]** An "almost-all-TIMES-n" statement for our fixed orbit is **not** delivered by
   Tao's method (it has no time-average; its independence comes from varying the start). Converting it
   would require single-orbit equidistribution of `c_n mod 2ᵏ` (Mahler 3/2) — the wall itself. The weaker
   one-sided `1/3` threshold does not help because the method supplies no single-orbit / one-sided output.
3. **[PROVEN-in-scope]** Krasikov–Lagarias gives `≥ x^{0.84}` **STARTS below `x` reach 1** — a count of
   starting points, **not** a single-orbit `D`/even-density bound. No `mean D ≥ 3/2` transfers. Only
   unconditional single-orbit valuation facts: `D ≥ 1`, `mean(D) ≥ 1` (= `even-density ≥ 0`).
4. **[OBSERVED]** `induced_tao_method.py`: real induced `D` ≈ Geometric(1/2), `mean(D)=1.997`,
   `liminf` running-mean never below `1.5` (worst prefix slack `+2.5`, end slack `+74,709`). Target holds
   with `~+0.5` margin empirically — the Syracuse heuristic made quantitative, still not a proof.

**Net:** the Tao / Syracuse / Krasikov–Lagarias family is **a STARTS-ensemble theory**; our problem is a
**single fixed orbit's TIME statistics**. The translation is exactly the a.e.-starts → named-orbit gap =
line (5) / Mahler 3/2, the recurring wall. The angle is **closed as a shortcut** but productive: it pins
that even the *one-sided, `1/3`-slack, almost-all-`n`* relaxations all still reduce to single-orbit
equidistribution, and it quantifies the `+0.5` empirical margin of the `mean D ≥ 3/2` target.

### Sources
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi (2022),
  arXiv:1909.03562 — https://arxiv.org/abs/1909.03562 ;
  blog: https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/
- Krasikov & Lagarias, *Bounds for the 3x+1 problem using difference inequalities*, Acta Arith. 109
  (2003) 237–258, arXiv:math/0205002 — https://arxiv.org/abs/math/0205002
