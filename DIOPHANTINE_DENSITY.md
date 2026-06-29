# Can an EXPLICIT Diophantine bound on log₂3 + a separation/SPACING (not cancellation) argument extract a one-sided density?
*2026-06-29. Open kernel (K): one-sided density `freq({4(3/2)^n}∈[0,½)) ≤ ½` (⇔ sub-trivial Weyl sums
`S_N = Σ_{n<N} e(h·4(3/2)^n)`). Prior verdict (`BAKER_LINFORMS.md`): Baker = individual-term, no density —
because density needs CANCELLATION and Baker bounds single terms. NEW angle examined here: bypass cancellation
with a SEPARATION/SPACING-based COUNTING argument (covering / large-sieve / Turán). Distinct from
`SEPARATION_BAKER.md` (that file = 2-adic `v₂` carry separation; THIS file = archimedean spacing of the orbit
in [0,1)). SOUNDNESS PARAMOUNT, every line labelled. Numerics `diophantine_density.py`, exact big-int. NOT committed.*

---

## 0. One-line verdict
**Separation provably CANNOT control the one-sided density — decisively, by two compounding gaps.**
A separation/covering count gives `#{n<N : x_n∈[0,½)} ≤ (½)/δ_N + 1`, which beats the trivial `N` only if the
minimum gap `δ_N > 1/(2N)` (separation must exceed *half the average gap*), and hits the target `½` only if
`δ_N ≈ 1/N` (the orbit must be a **near-perfect equispaced lattice** — strictly stronger than equidistribution).
But (i) the best Diophantine (Baker/Zudilin) separation is **exponentially small** `δ ≳ 2^{−cn}`, and (ii) the
**actual** min-gap is **Poisson-scale** `δ_N ∼ N^{−2}` (measured) — both **astronomically below** the `1/N`
threshold. The orbit *clusters freely within its separation budget* (measured: it puts ≈N/2 points in `[0,½)`
while its min-gap would permit ≈N²/2). **No new lead.** `[PROVEN that separation cannot control density]`.
Same root cause restated: **separation = min-gap; density = how min-gap relates to average-gap; for this orbit
min-gap ≪ average-gap.** Counting/covering, large-sieve, and Turán power-sum **all** require `δ⁻¹ ≲ N`, which fails.

---

## 1. The explicit Diophantine / linear-forms bounds for log₂3 (exact numbers) `[PROVEN-in-literature]`

**Irrationality measures (single constants):**
- `μ(log 2) ≤ 3.8913997…` (Rukhadze 1987; Marcovecchio's refinement of the dilogarithm method gives `≤3.57455`).
- `μ(log 3) ≤ 5.1163051` (Q. Wu & collaborators, ~2014), refining **Salikhov 5.125** (2007) and **Rhin 8.616**
  (1987). [`μ` = irrationality exponent: `|θ−p/q| < q^{−μ}` has finitely many solutions for any larger exponent.]
- **`log₂3 = log3/log2` is transcendental** (Gelfond–Schneider) with a **finite EFFECTIVE** irrationality
  measure (Baker). Note: `log3/log2` is a *ratio*, NOT an element of the ℚ-space `ℚlog2+ℚlog3`, so the
  Rhin/Brisebarre **measure of linear independence** `μ(γ) ≤ 8.616` for nonzero `γ∈ℚlog2+ℚlog3` (Rhin 1987;
  Brisebarre, *Exp. Math.* 10 (2001)) does **not** literally give `μ(log₂3)` — but it does control the
  linear form `q log3 − p log2 ∈ ℤlog2+ℤlog3`, which is what an irrationality measure of `log₂3` reduces to (§1A).

**1A. The linear-form bound = the separation Baker actually gives `[PROVEN-in-literature]`.**
An irrationality measure of `log₂3` is exactly a lower bound on the **two-log linear form**:
```
|log₂3 − p/q| = |q log3 − p log2| / (q log2),   so   |q log3 − p log2| > c·q^{−κ}  ⟹  μ(log₂3) ≤ κ+1.
```
- **Baker–Wüstholz (explicit, fully general):** `|Λ| > exp(−(16·n·d)^{2n+4} (log A)^n log B)`. For `n=2` logs,
  `d=1`, bases `A=3`: `|q log3 − p log2| > exp(−C·log B)`, `B=max(p,q)`. **Effective and polynomial in `B`** —
  but `C` is **astronomically large**: the analogous worked example for `log₁₀2` yields the exponent
  `|β log₁₀2 − α| > 0.4·β^{1−6×10¹²}` (i.e. `μ` of order `10¹²`). So Baker–Wüstholz alone gives
  `μ(log₂3) ≤ (huge effective constant)`.
- **Laurent–Mignotte–Nesterenko (1995, interpolation determinants — the sharp two-log engine):**
  for `Λ = b₂logα₂ − b₁logα₁`, `log|Λ| ≥ −C(α₁,α₂)·(max(log b' , …))²` with **small, explicit** `C`. For the
  pair `(2,3)` this gives a *practical* polynomial separation `|q log3 − p log2| ≳ B^{−κ}` with **`κ` of modest
  size** (single/low-double digits), vastly better than Baker–Wüstholz's `10¹²`. **This LMN two-log bound is the
  state-of-the-art explicit "Baker" separation for powers of 2 and 3.**
- **Equivalent multiplicative form:** `|2^a − 3^b| > 2^a · a^{−κ}` — powers of 2 and 3 are **polynomially
  separated**; no `2^a` is super-close to any `3^b`. This is a genuine archimedean **anti-clustering / SEPARATION**
  fact (vs cancellation). It is *exactly* the kind of input the counting argument below would consume.

**Bottom line on the input:** the strongest EXPLICIT Diophantine fact available is a **polynomial separation of
powers `|2^a−3^b| > 2^a a^{−κ}`** (LMN), and pointwise `‖(3/2)^n‖ > 0.5803^n` (Zudilin, Padé — *exponential*,
not polynomial; Padé beats Baker here). Both are **SEPARATION/individual-term**, never cancellation. The question
is whether SEPARATION alone, fed into a COUNTING argument, yields density.

---

## 2. The genuinely new question: SEPARATION → COUNTING → density (bypassing cancellation)?

**Setup `[PROVEN, exact — verified]`.** The orbit is `x_n := {4(3/2)^n} = {2^{2−n}3^n} ∈ [0,1)`. Verified
(`diophantine_density.py`, exact): **`x_n` is a DYADIC RATIONAL with denominator `2^{n−2}`** (`x_n =
(3^n mod 2^{n−2})/2^{n−2}`). The parity word / `D`-data is the dyadic-arc itinerary of `(x_n)` (per
`BAKER_LINFORMS.md`). Target: `#{n<N : x_n∈[0,½)} ≤ (½+o(1))N`, or even just `≤ (1−c)N`, `c>0`.

**The covering/counting principle `[PROVEN, elementary]`.** If the `N` points `x_0,…,x_{N−1}` are pairwise
**separated by `≥ δ_N`** (min gap), then any arc `I` of length `|I|` contains at most `|I|/δ_N + 1` of them:
```
#{n<N : x_n ∈ [0,½)}  ≤  (½)/δ_N + 1.
```
This uses **only spacing**, never cancellation in `Σe(·)`. **It is exactly the route the prompt asks about.**
Two thresholds fall out immediately:
- **Beats the trivial bound `N`**  ⟺  `δ_N > 1/(2N)`  (min gap > *half* the average gap `1/N`).
- **Hits the target `½`**  ⟺  `δ_N ≈ 1/N`  (min gap ≈ average gap ⟺ the points are a **near-equispaced
  lattice**). 

So the covering route is **not a priori vacuous**: *if* one could prove the orbit is near-equispaced
(`δ_N ≳ c/N`), the covering count would deliver one-sided density **with no cancellation at all**. This is the
honest re-examination the prior verdict did not isolate. The question becomes purely: **how large is `δ_N`, and
can Baker lower-bound it at the `1/N` scale?**

---

## 3. Why it FAILS — two compounding gaps, both fatal `[PROVEN / OBSERVED]`

**Gap (A) — what Baker/Zudilin can prove is EXPONENTIALLY below the `1/N` threshold `[PROVEN-in-literature]`.**
The pairwise gap `x_n − x_m` (`n>m`) is, exactly, a dyadic rational `2^{2−n}·3^m(3^{k}−2^{k})` (`k=n−m`) reduced
mod 1 — i.e. an **integer multiple of `2^{−(n−2)}`**. Hence the *smallest possible* nonzero gap is `2^{−(n−2)} =
4·2^{−n}`: orbit points can be **exponentially close** (`∼2^{−n}`). The best Diophantine lower bounds match this
exponential scale, not the polynomial `1/N`:
  - Zudilin/Padé: `‖(3/2)^n‖ > 0.5803^n = 2^{−0.785n}` — controls the gap to the single point `0`; **exponentially
    small**.
  - LMN two-log: polynomial separation of *powers* `|2^a−3^b|`, but this controls `‖(3/2)^n‖ = ‖2^{a}3^{b}…‖`
    pointwise, again **not** a uniform `≥c/N` spacing of the *orbit set*.
  No Diophantine tool gives `δ_N ≳ 1/N`; the proven floors live at `2^{−cn}`, i.e. `δ_N⁻¹ ≳ 2^{cn} ⋙ N`. Plugged
  into the covering count: `#[0,½) ≤ (½)·2^{cn} + 1 ⋙ N` — **super-trivial.** `[PROVEN]`

**Gap (B) — even the TRUE separation is Poisson-scale `N^{−2}`, still `≪ 1/N` `[OBSERVED, exact big-int]`.**
Independent of provability: the *actual* min gap is far below the `1/N` lattice scale.
| `N` | min gap `δ_N` | avg gap `1/N` | `δ_N/avg` | covering bound on `#[0,½)` | (trivial `N`) |
|---|---|---|---|---|---|
| 100 | `7.8e−5` | `1.0e−2` | 0.0078 | `6.5e3` | 100 |
| 400 | `5.8e−6` | `2.5e−3` | 0.0023 | `8.6e4` | 400 |
| 1600 | `5.7e−7` | `6.3e−4` | 0.0009 | `8.8e5` | 1600 |
`δ_N/avg → 0` (exact `−log₂ δ_N ≈ 2·log₂N`, i.e. `δ_N ∼ N^{−2}`, the **birthday/Poisson** scaling expected of a
"random" equidistributed sequence — consistent with `SEPARATION_BAKER.md`'s 2-adic finding that the orbit
separates *exactly like random*). The covering bound is `∼N²/2`, off from the truth by a factor `∼N`. `[OBSERVED]`

**The orbit clusters freely within its separation budget `[OBSERVED]`.** Direct pack test (`N=1600`):
| window `w` | actual max #pts in a width-`w` window | covering prediction `w/δ_N` |
|---|---|---|
| 0.5 | **824** (≈ N/2, as equidistribution predicts) | `8.8e5` |
| 0.1 | 186 | `1.8e5` |
| 0.01 | 31 | `1.8e4` |
The orbit places `≈N/2 = 824` points in a half-arc while its min-gap would *permit* `≈8.8×10⁵`. **Separation is
nowhere near binding** — the density (≈½) is decided entirely by how the points *cluster*, which spacing does not
see. This is the precise realization of "the orbit could cluster within the allowed separation": it does, by a
factor `∼N`. `[OBSERVED — the decisive picture]`

---

## 4. The other separation-based counting tools die at the same wall `[PROVEN]`
The prompt names large-sieve and Turán power-sum as separation (not cancellation) tools. Each consumes a
separation `δ` of points/frequencies and is nontrivial **only when `δ⁻¹ ≲ N`** — the *same* `1/N` threshold:
- **Large sieve.** `Σ_r |Σ_{n≤M} a_n e(n x_r)|² ≤ (M + δ⁻¹) Σ|a_n|²` for `δ`-separated `{x_r}`. To use the orbit
  as the separated nodes, `δ⁻¹ ∼ 2^{n}` (or `∼N²`) dominates `M`, making the inequality **trivial**. It is also
  the wrong shape: the large sieve gives an L²-**upper** bound over many nodes, not a single-orbit count or any
  cancellation. `[PROVEN — wrong threshold + wrong functional]`
- **Turán power-sum / Dirichlet-spacing.** Lower bounds `max_ν|Σ_j z_j^ν|` from separation of `{z_j}` on the
  circle; needs the *same* `δ⁻¹ ≲ N` to be nontrivial and produces a **lower** bound on a max (anti-cancellation),
  the opposite of the `o(N)` we need. `[PROVEN — opposite direction]`
- **Erdős–Turán–Koksma.** Bounds discrepancy by `Σ_h (1/h)|S_N(h)|` — this is precisely the **Weyl-sum
  (cancellation)** object, not a spacing input; it cannot be fed by separation. `[PROVEN — it IS the cancellation route]`

**Unifying reason.** Every separation→counting tool needs `δ⁻¹ ≲ N` (separation at the average-gap scale `1/N`).
Diophantine separation delivers `δ⁻¹ ∼ 2^{cn}`; the truth is `δ⁻¹ ∼ N²`. Both overshoot `N`. There is no
separation statement at the `1/N` scale, and there cannot be one short of proving near-equidistribution itself
(near-equispacing `⟹` equidistribution, and is in fact strictly stronger).

---

## 5. The exact conceptual gap (separation vs density) `[honest assessment]`
- **Separation = min-gap.** **Density = how the min-gap compares to the average-gap (`1/N`).**
- Baker/Padé/LMN give **lower bounds on min-gap to a fixed target** (the point 0, or between fixed powers),
  at the **exponential** scale `2^{−cn}`. A density bound needs the min-gap at the **average-gap** scale `1/N`,
  AND uniformly across all arcs (= near-equispacing). These are separated by a factor `∼2^{cn}/(1/N) = N·2^{cn}`.
- Near-equispacing (`δ_N ≳ c/N`) is **strictly stronger** than equidistribution (equidistributed orbits are
  generically Poisson, `δ_N ∼ N^{−2}`), so even a *perfect* separation theorem would over-deliver — and it is
  provably *false* here (`δ_N ∼ N^{−2}` measured). **Separation simply does not constrain density for an orbit
  that is allowed to (and does) cluster at scale `≪ 1/N`.**
- This is a *different* failure from the cancellation wall: the cancellation route (Weyl/Erdős–Turán) is OPEN
  (could in principle work); the **separation route is CLOSED** (provably cannot work — the required input is both
  unprovable by Baker and false). It removes a candidate, it does not open one.

---

## 6. Honest verdict
> **NOT a new lead. Separation provably cannot control the one-sided density.** A separation/covering count
> `#[0,½) ≤ (½)/δ_N + 1` needs the min gap `δ_N` at the **average-gap scale `δ_N ≳ 1/N`** (near-equispaced
> lattice) to give density `≤½`, or even just `δ_N > 1/(2N)` to beat trivial. The strongest EXPLICIT Diophantine
> bound on `log₂3` (LMN two-log: `|2^a−3^b|>2^a a^{−κ}`; Zudilin/Padé: `‖(3/2)^n‖>0.5803^n`) delivers only
> **exponential** separation `δ ≳ 2^{−cn} = δ⁻¹ ∼ 2^{cn} ⋙ N`, and the **true** min gap is **Poisson `∼N^{−2}`**
> (measured, exact) — both astronomically past the `1/N` threshold. The orbit **clusters freely inside its
> separation budget** (≈N/2 points in `[0,½)` vs ≈N²/2 permitted). Large-sieve and Turán fail by the identical
> `δ⁻¹ ≲ N` requirement (and point the wrong way). **The cancellation barrier is not circumvented by spacing;
> for this orbit, spacing carries no density information.** `[PROVEN that separation-cannot-control-density]`

The kernel (K) = effective single-orbit cancellation in `S_N` remains [OPEN] = the famous open equidistribution
of `(3/2)^n`; the unconditional contribution remains the *reduction* to it. This note closes the
"explicit-Baker-separation + clever-averaging ⟹ density" hope with a precise, quantified reason, complementing
`SEPARATION_BAKER.md` (2-adic side) with the archimedean side.

### Sources
- Baker–Wüstholz explicit form; Laurent–Mignotte–Nesterenko, *Formes linéaires en deux logarithmes et
  déterminants d'interpolation*, J. Number Theory 55 (1995) 285–321 (corollary: EUDML doc/207183).
- Worked Baker–Wüstholz two-log exponent (`log₁₀2`, exponent `1−6×10¹²`):
  https://seungukj.github.io/posts/2022/10/rational-approx-of-log/
- μ(log2)≤3.8914 (Rukhadze); μ(log3)≤5.1163 (Wu), ≤5.125 (Salikhov 2007), ≤8.616 (Rhin 1987):
  https://www.sciencedirect.com/science/article/pii/S0022314X14001218 ;
  Brisebarre, *Irrationality measures of log 2 and π/√3*, Exp. Math. 10 (2001), projecteuclid em/999188419.
- Rhin, measure of linear independence `μ(γ)≤8.616` for `γ∈ℚlog2+ℚlog3` (cited in Brisebarre).
- Zudilin, `‖(3/2)^k‖ > 0.5803^k` (Padé), JTNB 19 (2007) 311–323.
- Companion (2-adic separation, distinct): `busybeaver/SEPARATION_BAKER.md`; (cancellation wall): `BAKER_LINFORMS.md`.
- Numerics: `scratchpad/diophantine_density.py` (exact big-int; dyadic-denominator, min-gap `∼N^{−2}`, pack test).
</content>
</invoke>
