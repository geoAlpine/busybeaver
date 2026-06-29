# Is the UNIFORM AEV statement (all/a.e. α) easier, and does it reach the specific α=8? (2026-06-29)

*Assigned angle: both diagonals are the single AEV object `d_n(α) = bit_k(⌊α(3/2)^n⌋)` —
`α=8` (first/Mahler diagonal), `α=α*≈0.135822737943` (second/carry diagonal, `TWO_DIAGONAL_COMPARISON`).
Question: is the UNIFORM-in-α statement structurally easier, and does it imply the specific `α=8`? Make the
a.e.-α statement precise and cite what is provable; hunt for a CHECKABLE Diophantine condition on α that (i)
provably gives equidistribution and (ii) α=8 could meet; give the honest (a)/(b)/(c) verdict; test
numerically whether α=8 is typical or special. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/uniform_aev.py`, exact big-int
`⌊α(3/2)^n⌋=(p·3^n)//(q·2^n)`, α as reduced rationals, N=2500–8000, <2s. Every claim labelled. Zero false
proofs. NOT committed.*

---

## 0. One-line verdict

**(b) — SAME a.e.→specific wall, now exhibited at the α (leading-coefficient) level.** "Uniform" splits into
two readings and NEITHER helps `α=8`: (i) the **a.e.-α** version is **already a 1935 THEOREM** (Koksma) — for
Lebesgue-a.e. α, `d_n(α)` equidistributes — so it is genuinely *easier*, but it is a null-set-excepting
statement that says **nothing** about the single point `α=8`; (ii) the **all-α** version *does* contain `α=8`
but is therefore **strictly HARDER** than the specific problem (it implies it), so it is no reduction. The
hunted-for middle — a **checkable Diophantine condition on α** that provably forces equidistribution and that
`α=8` could be verified to satisfy — **does not exist in the literature**: the Davenport–Erdős–LeVeque
criterion reduces the specific case back to bounding the per-α Weyl self-correlations of `{α(3/2)^n}` (= the
problem itself), and the exceptional set of α for `{α(p/q)^n}` has **full Hausdorff dimension** (de
Mathan–Pollington; Bugeaud), so no soft condition can certify `α=8` out of it; `α=8` is moreover an *integer*
= the Mahler / hardest `p<q²` regime. **Numerics: `α=8` is dead typical** — its digit balance rides the random
`1/√N` floor and sits at the 21st percentile of 120 generic α (cleaner than ~79% of them), with no integer or
Diophantine anomaly. **No machine decided. No label upgraded.**

---

## 1. The uniform statement, made precise — and what is provable for a.e. α  `[PROVEN-in-lit, metric]`

**Exact reduction of the digit to a fractional part `[PROVEN, this note]`.** For the integer
`M_n(α)=⌊α(3/2)^n⌋`, the binary digit is `bit_k(M_n)=⌊2·{M_n/2^{k+1}}⌋`, and `M_n/2^{k+1}` differs from
`(α/2^{k+1})(3/2)^n` by `{α(3/2)^n}/2^{k+1}∈[0,2^{-(k+1)})`. Hence

> **`d_n(α)=bit_k(⌊α(3/2)^n⌋)` is governed by `{(α/2^{k+1})(3/2)^n} mod 1`**, and full equidistribution of the
> low `k+1` bits of `⌊α(3/2)^n⌋` is equivalent to u.d. mod 1 of `{β(3/2)^n}` with `β=α/2^{k+1}`.

This is the same bit↔fractional-part dictionary the repo already uses for `σ_n`
(`SECOND_DIAGONAL_RAJCHMAN §1`: `σ_n=⌊2{S_n/2^{n+k+1}}⌋`). It places `d_n(α)` squarely on the metric theory of
`{β θ^n}`.

**The provable a.e.-α statement.**
> **`[PROVEN-in-lit, metric]` (Koksma 1935).** For any *fixed* real `θ>1` and any sequence of distinct
> exponents, `{β θ^n}` is u.d. mod 1 for **Lebesgue-a.e. β**. Apply with `θ=3/2` and the affine rescale
> `β=α/2^{k+1}` (measure-preserving up to scale): **for a.e. α, `{(α/2^{k+1})(3/2)^n}` is u.d. mod 1 for every
> `k`, hence `d_n(α)=bit_k(⌊α(3/2)^n⌋)` equidistributes (digits balanced; full equidistribution mod `2^{k+1}`).**

So the **a.e.-α reading of the uniform AEV conjecture is not open — it is a 90-year-old theorem.** The engine
under it is the **Davenport–Erdős–LeVeque criterion** (1963): `{f_n(α)}` is u.d. for μ-a.e. α whenever
`Σ_N (1/N)∫|N^{-1}Σ_{n≤N} e(h f_n(α))|² dμ(α) < ∞`; integrating in α kills the off-diagonal correlations
(`f_n−f_m` has growing derivative `((3/2)^n−(3/2)^m)/2^{k+1}`, the Koksma/van der Corput condition), giving the
a.e. conclusion *without any per-point information*. (Companions, all **metric**: Erdős–Koksma 1949 / Cassels
1950 discrepancy `O(N^{-1/2}log N(loglog N)^{3/2+ε})` a.e.; Aistleitner 2014 metric LIL/CLT.)

> **Reconciliation with `TWO_DIAGONAL_COMPARISON §3`** (which called uniform AEV "strictly harder"): that note
> meant the **all-α** reading (every α at once ⟹ implies `α=8`). The **a.e.-α** reading is the *opposite* — the
> easy, proven one. Both statements are true; they refer to the two faces of "uniform," and §3 below shows why
> neither reaches `α=8`.

---

## 2. The decisive a.e.→specific question: is there a CHECKABLE Diophantine condition α=8 might meet?

This is the real prize: a condition `C(α)` with (i) `C(α) ⟹ {α(3/2)^n}` u.d. **provable**, and (ii) `C(8)`
**checkable**. **Search result: no such condition is known.** The obstructions, precisely:

- **DEL is not checkable per-point.** Davenport–Erdős–LeVeque applied to a *single* α (point mass `μ=δ_α`)
  requires `Σ_N (1/N)|N^{-1}Σ_{n≤N} e(h(α/2^{k+1})(3/2)^n)|² < ∞`, i.e. a bound on the **self-correlations**
  `C_N(h,α)=N^{-2}Σ_{m,n≤N} e(h(α/2^{k+1})((3/2)^m−(3/2)^n))` — which **is the original problem**. The averaging
  that makes the criterion *deliver* a.e.-u.d. is exactly `∫dα`, the step unavailable for a fixed α. Koksma
  bounds `∫C_N dα`, never `C_N(8)`.
- **No positive single-α theorem for non-Pisot θ.** The only per-point results for `{α θ^n}` are for `θ`
  **Pisot/Salem** (then `{αθ^n}→0` for `α∈ℤ[θ]` — the *opposite* of u.d.) or for **constructed** α
  (Stoneham/Bailey–Crandall, but integer base only — `WALL_B_SPECIFIC_LITERATURE §1B`). `θ=3/2` is **non-Pisot**
  and `α=8` is *given*, not constructed: both routes are closed (`WALL_B §1,2`).
- **The exceptional set is large, so no soft exclusion exists.** For lacunary / `{ξ(p/q)^n}` sequences the set
  of α that are **not** u.d. (even not dense) mod 1 has **full Hausdorff dimension 1** (de Mathan; Pollington;
  Bugeaud, *Exceptional parameters of linear mod-one transformations and fractional parts `{ξ(p/q)^n}`*, CRAS
  2015). A measure-zero-but-dimension-1 exceptional set cannot be ruled out for a specific algebraic point by
  any dimension/genericity argument — there is **no checkable predicate** separating `α=8` from it.
- **`α=8` is the worst regime.** `α=8` is an *integer* and `3/2` has `p=3<q²=4`: this is the `Z_{p/q}`/**Mahler**
  regime (`AEV_DIGEST §4`), where even *density* (let alone u.d.) of `{(3/2)^n}` is unknown and
  `limsup−liminf{(3/2)^n}` is only known `>1/3` (Flatto–Lagarias–Pollington), not `≥1/2`. Any Diophantine
  condition on `α` that could help would have to crack this.

**Net:** the checkable-condition hunt comes back **empty**. Every per-point success in the literature is gated on
*Pisot θ*, *constructibility of α*, or *integer base* (so `b^k mod c^n` lives in a finite group) — Antihydra has
none. (Consistent with `AEV_METHODS §2(d)`, `WALL_B §3`.)

---

## 3. Honest verdict (the three asks)

| ask | answer | label |
|---|---|---|
| **(a) a provable a.e.-α statement AND a checkable condition α=8 might meet (⇒ a route)?** | **Half: the a.e.-α statement is PROVEN (Koksma); the checkable condition does NOT exist.** So it is **not** a route to `α=8`. | a.e. `[PROVEN-in-lit]`; condition **none** |
| **(b) same a.e.→specific wall at the α level?** | **YES — this is the verdict.** Precise reason: Koksma already gives a.e.-α u.d. for *any fixed* `θ>1`, so the **entire** difficulty is concentrated in "`θ=3/2` fixed (one algebraic number) **and** `α=8` one point." The a.e. statement excepts a (dimension-1) null set with no checkable membership test; the all-α statement is strictly stronger than `α=8`. Identical in nature to Wall (B) (`WALL_B`), re-expressed on the leading coefficient α rather than the orbit start. | `[OPEN]`, wall identified |
| **(c) reduces?** | **No reduction.** "Uniform" trades the single hard point either for a proven-but-weaker a.e. statement (loses `α=8`) or for an all-α statement that *contains* `α=8` (no easier). Same `(K)` = Mahler/AEV Conj 1.6 residue. | `[OPEN]` |

**Exact residual gap (sharpened, at the α level).** The one missing input is a **per-point** bound
`Σ_N (1/N)|C_N(h,8)| < ∞` on the Weyl self-correlations `C_N(h,α)` of `{(α/2^{k+1})(3/2)^n}` **at the single value
`α=8`** (equivalently `α=α*`). Koksma/DEL prove `∫|C_N(h,α)|dα→0` (a.e. α closed); the all-α conjecture asserts
`C_N(h,α)→0` for *every* α (⟹ α=8). Between "a.e." and "every" lies exactly the one Haar-null point `α=8`, with
**no checkable Diophantine sieve** known to land on it. That residue is `(K)` = Mahler 3/2 / AEV Conj 1.6,
untouched.

---

## 4. Numerics — is α=8 typical or special?  `[OBSERVED]`

`scratchpad/uniform_aev.py`, exact `⌊α(3/2)^n⌋=(p·3^n)//(q·2^n)`, balance `|P(d_n=1)−½|` over `n∈[burn,N)`,
`N=2500`, burn 500, `max` over read levels `k=1..6`. CLT floor `1/√(N−burn)=0.0224`.

- **Bulk of 120 generic rational α∈(0.05,16):** `max_k|bal|` min/median/max = **0.0060 / 0.0185 / 0.0375** —
  all riding the `1/√N` floor.
- **`α=8` (first diagonal):** `max_k|bal| = 0.0130`, **21st percentile** of the bulk (i.e. *more* balanced than
  ~79% of random α). **`α*≈0.1358` (second diagonal):** `0.0205`, **59th percentile** — dead median.
- **Diophantine-feature sweep** (`max_k|bal|`): int 8 = 0.013, int 1 = 0.020, int 27 = 0.013, 8/3 = 0.013,
  1/7 = 0.034, ~e = 0.016, ~π = 0.024, Liouville(base-2) = 0.016 — **all in one band at the floor; integers,
  simple rationals, and a Liouville value are indistinguishable** at this N. No Diophantine feature of `α=8`
  correlates with faster or slower convergence.
- **Decay (k=1) vs `1/√N`, N=1000→8000:** `α=8` balance/floor ratio = 0.32, 0.20, 0.27, 0.54 (vs `α=1`:
  1.56, 1.03, 0.14, 0.61; `α≈π`: 0.25, 0.28, 0.44, 0.27) — **`α=8` tracks the random floor**, no anomaly.

**Reading:** `α=8` is **typical**, not special — numerically it behaves exactly like a Koksma-generic α. This is
the empirical face of the wall: the specific point looks generic, but "looks generic" is not "is provably
generic," and the a.e. theorem cannot certify the one point. (Caveat: a genuine Liouville-resonant α would only
reveal slow convergence at far larger N / closer approximation than tested; at N≤8000 it too is typical.)

---

## 5. Genuinely new vs prior

- **vs `TWO_DIAGONAL_COMPARISON §3`** ("uniform AEV strictly harder"): disambiguates **uniform** into
  **a.e.-α (PROVEN, Koksma — easier)** vs **all-α (strictly harder)**, and shows *both* miss `α=8` — sharpening
  §3 rather than contradicting it. New: the exact bit↔`{β(3/2)^n}` reduction with `β=α/2^{k+1}`, placing
  `d_n(α)` directly under the metric theory.
- **vs `AEV_METHODS §2(b)`** (lists Koksma/Cassels/Aistleitner as metric): adds the **per-point DEL obstruction**
  (the integral `∫dα` is the irreplaceable step) and the **full-dimension exceptional set** (de Mathan–Pollington;
  Bugeaud CRAS 2015) as the precise reason no checkable condition can exist — the cleanest statement that the
  a.e.→specific gap is at the **α level**.
- **vs `WALL_B_SPECIFIC_LITERATURE`** (a.e.→specific via construction/integer base only): re-projects the same
  wall onto the **leading coefficient α**, and supplies the numerics showing `α=8` is empirically Koksma-typical.

## Sources

- **Koksma 1935** — `{β θ^n}` u.d. mod 1 for a.e. β (any fixed θ>1). (J.F. Koksma, *Ein mengentheoretischer Satz
  über die Gleichverteilung modulo Eins*, Compositio Math. 2 (1935) 250–258.) Kuipers–Niederreiter,
  *Uniform Distribution of Sequences*, Ch.1. https://web.maths.unsw.edu.au/~josefdick/preprints/KuipersNied_book.pdf
- **Davenport–Erdős–LeVeque 1963** — metric u.d. criterion `Σ(1/N)∫|Weyl|²dμ<∞ ⟹ μ-a.e. u.d.`
  (H. Davenport, P. Erdős, W.J. LeVeque, Michigan Math. J. 10 (1963) 311–314); generalises to any μ
  (e.g. arXiv:2408.03473). https://projecteuclid.org/euclid.mmj/1028998917
- **Aistleitner 2014** — quantitative metric u.d. of geometric progressions; states specific-x u.d. "notoriously
  difficult," no metric lower bounds for typical x. arXiv:1210.4215. https://arxiv.org/pdf/1210.4215
- **de Mathan; Pollington; Bugeaud (CRAS 2015)** — exceptional set of α for `{ξ(p/q)^n}` not dense/u.d. has full
  Hausdorff dimension. *Exceptional parameters of linear mod-one transformations and fractional parts `{ξ(p/q)^n}`*,
  C. R. Acad. Sci. https://www.numdam.org/articles/10.1016/j.crma.2015.01.017/ ; cf. arXiv:2409.00775,
  arXiv:2512.05690 (non-Archimedean Koksma + exceptional-set dimensions).
- **Flatto–Lagarias–Pollington** Acta Arith. 70 (1995): `Ω(3/2)>1/3` (range, not density). Mahler 1968.
- Repo: `TWO_DIAGONAL_COMPARISON.md` (§1 both diagonals = `bit_k⌊α(3/2)^n⌋`; §3 all-α harder),
  `SECOND_DIAGONAL_RAJCHMAN.md` (bit↔fractional dictionary), `AEV_METHODS.md` (§2 metric results),
  `AEV_DIGEST.md` (Conj 1.6; `p<q²`=Mahler regime), `WALL_B_SPECIFIC_LITERATURE.md` (a.e.→specific gated on
  construction/integer base), `EMPTY_TOOLBOX_QUESTION.md` (a.e.→specified is the missing bridge).
- Numerics: `scratchpad/uniform_aev.py` (N≤8000; α=8 at 21st pct of 120 generic α, rides `1/√N`; Diophantine
  sweep flat; α=8 balance/floor O(1) across N).

**No machine decided. No label upgraded.**
