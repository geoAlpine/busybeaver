# CORE_DIGITS3N_FRONTIER — the exogenous arithmetic frontier of (K)

*Deep arithmetic examination (2026-06-30), WEAPONS_AUDIT style. Scope: the EXOGENOUS part of the
kernel ONLY — the moving diagonal `d_n = bit_{n+k}(8·3ⁿ)` = a moving (index-dependent) binary digit
of `3ⁿ`. The self-referential carry `S_n` (so that `β_n = bit_{n+k}(8·3ⁿ − S_n) = d_n ⊕ σ_n ⊕ ρ_n`)
is a sibling agent's job and is excluded here. GOAL: pin the EXACT arithmetic frontier for `d_n` and
the precise gap to equidistribution. SOUNDNESS: every line labelled [PROVEN-in-lit]/[OBSERVED]/[OPEN];
citations heavy-WebSearch-checked 2019–2026; NO proof claims; no label upgraded. Numerics `.venv`
exact big-int. NOT committed.*

---

## 0. The exact exogenous object [PROVEN, exact]

`8·3ⁿ = 2³·3ⁿ`, so for a fixed read-level `k` the exogenous bit is
> **`d_n = bit_{n+k}(8·3ⁿ) = bit_{n+k−3}(3ⁿ)`.**

In the bit-grid (row = `n`, column = position `j`, `0 ≤ j ≲ 1.585 n`), `d_n` reads **column `n+k−3`
of row `n`** — a slope-1 **moving diagonal**, at relative depth `(n+k−3)/(1.585 n) → 0.63` from the
top. As `n→∞` the read column scales like `n`, so this is genuinely **index-dependent** (moving),
NOT a fixed column and NOT the leading band. For fixed `k` it is the same diagonal family as the
repo's `a_n = bit_n(8·3ⁿ)` (`DIGITS_OF_3N.md`), merely shifted by `k`. This is exactly the
Erdős / Mahler-`(3/2)` / AEV digit object.

**Numerics (`.venv`, exact, N = 2·10⁵), the exact object `bit_{n+k}(8·3ⁿ)`:**

| k | freq(d_n = 1) |
|---|---|
| 0 | 0.49867 |
| 3 | 0.50139 |
| 7 | 0.50001 |
| 12 | 0.50169 |

Balanced at every read-level (consistent with, NOT proof of, equidistribution). [OBSERVED]

---

## 1. Sharpest UNCONDITIONAL facts about the binary digits of 3ⁿ — statistic | reach | citation

| # | Statistic | EXACT reach (which positions / what is controlled) | Status | Citation |
|---|---|---|---|---|
| 1 | **Leading-digit / mantissa** `{n log₂3}` equidistributes (Benford) | Only the **top** band, columns ≈ `1.585n − O(log n)`; depth Θ(log n) from the top. **Wrong position** for `d_n` (depth 0.63·1.585n). | [PROVEN-in-lit] | Weyl 1916 (equidistribution of `{nα}`, α irrational) |
| 2 | **Fixed-column periodicity:** each fixed column `j ≥ 3` is periodic in `n` with period `2^{j−2}` (= ord of 3 mod `2^j`); exact rational column-frequencies. Low bits of `3^{2ⁿ}` given by a 2-adic power series (diagonal stripes). | A **fixed** column `j`, sampled over all rows `n`. Provably **misses the moving diagonal**: the diagonal hits column `j` once, at row `n = j+3−k ≪ 2^{j−2}` (inside the first period) ⇒ **zero density transfer**. | [PROVEN-in-lit] | Rowland, *Complex Systems* 18 (2009), arXiv:0902.3257 |
| 3 | **Nonzero-digit count → ∞** (number of 1-bits of `3ⁿ` diverges) | A **global count**, no position. Rate `Θ(log n / log log n)` = **o(n)** ⇒ NO positive density of any digit value at any position. | [PROVEN-in-lit] (ineffective: Senge–Straus 1973; effective: Stewart 1980, J. reine angew. Math. 319; Bugeaud–Kaneko 2018, arXiv:1609.07926, via Schmidt subspace + linear forms in logs) | as listed |
| 4 | **Longest run of equal bits** `L(M·3^K) ≤ ηK + o(K)` for `M < 2^{ηK}`; in particular `L(3^K) = o(K)` (no monochromatic run is linear in the length) | A **horizontal** run-length inside one row. Gives only the **two-sided** per-row density bound `1/(L+1) ≤ dens(1s) ≤ 1−1/(L+1)`, i.e. each value has density `≥ 1/o(n) → 0`. **No positive-constant density**; nothing pinned to the moving diagonal cell. | [PROVEN-in-lit] — method is **Schlickewei's p-adic subspace theorem** (lower bounds for `|M·3^K − 2^{m}·b|`). | **ATTRIBUTION CAVEAT below.** The bound itself is real and is the standard subspace-theorem output; the repo's prior cite (DIGITS_OF_3N.md "2501.00850 Lemma 4.1") could not be confirmed (see ⚠). |
| 5 | **Erdős-conjecture partials:** the only `3ⁿ` with very few nonzero base-2 digits occur for small `n` (finiteness of few-1s powers); ties to Wieferich primes. | **Finiteness**, not density; says nothing positional. | [PROVEN-in-lit] (Howe 2021, arXiv:2105.06440, Thm 1.1; Lacroix-type J. Number Theory 159 (2015) S0022314X15002139, "Bits of 3ⁿ … Wieferich primes") | as listed |
| 6 | **Joint digit-sum normality:** `(s_2(3^K n), s_3(n))` jointly asymptotically normal; `(s_2,s_3)` attains a.a. values in ℕ². | About **digit SUMS over n with a free multiplier**, not a single specified power and not a position. | [PROVEN-in-lit] | **Drmota–Spiegelhofer**, *The joint distribution of binary and ternary digit sums*, arXiv:2501.00850 (Jan 2025) — main tool **Baker's theorem (linear forms in logs)**, NOT a run lemma (verified by direct fetch). |
| 7 | **"≈ half the bits of `3ⁿ` are 1"** (Pegg / folklore); base-3 of `2ⁿ` block-uniform; `log₃2` normal | global density / block normality, all conjectural | [OPEN] (numerics to `10⁶`) | Ren–Roettger, arXiv:2511.03861 (2025); folklore |

> ⚠ **Attribution correction (soundness).** `DIGITS_OF_3N.md` attributes the longest-run bound to
> "Spiegelhofer–Wallner 2025, arXiv:2501.00850, Lemma 4.1." Direct fetch of 2501.00850 shows it is by
> **Drmota and Spiegelhofer** (no Wallner), its subject is **joint digit-sum normality**, and its
> stated Diophantine engine is **Baker's theorem (Lemma 3.1)**, not a longest-run lemma via the
> subspace theorem. The longest-run bound `L(M·3^K) ≤ ηK+o(K)` **does exist** as a standard
> consequence of **Schlickewei's p-adic subspace theorem** (WebSearch-confirmed phrasing), but the
> exact paper/lemma number in the repo is **unverified** and should be re-sourced before any external
> use. Treat row 4 as [PROVEN-in-lit, citation-pending]. No mathematical content changes; only the
> reference.

---

## 2. The MOVING diagonal specifically — is ANYTHING unconditional? Pin the gap

**Verdict: NOTHING unconditional touches a moving (index-dependent) digit position of `3ⁿ`.** [OPEN]

The unconditional handles partition cleanly, and each lands at the **wrong place** for `d_n`:

| Handle | Where it lives | Why it cannot reach the moving diagonal |
|---|---|---|
| Weyl / Benford (#1) | **fixed depth** (top band) | moving diagonal sits at depth 0.63·length, not the top |
| Rowland fixed-column (#2) | **fixed column** | diagonal samples each column once, far below its period `2^{j−2}` ⇒ no averaging |
| nonzero-count (#3) | **global, no position** | `o(n)` ⇒ no positive density anywhere |
| longest-run (#4) | **horizontal run, one row** | gives only `density ≥ 1/o(n) → 0`, two-sided; no diagonal cell |
| digit-sum normality (#6) | **sum over n, free multiplier** | not a single specified power, not a fixed position |

Every PROVEN positive-density statement is at a **fixed** position (Benford top, Rowland columns);
every **moving/global** proven statement is a sublinear count or a vanishing-density run bound. **The
single moving-diagonal marginal `freq{n : d_n = b}` is exactly the open object** — it is
literally `{8·(3/2)ⁿ}`'s digit, i.e. Mahler-`(3/2)` / AEV Conj 1.6 at the leading constant `α=8`.

**The precise gap.** Even the weakest non-degeneracy — a single **one-sided** density
`freq{n : d_n = 0} ≤ 1 − c` for some constant `c > 0` — is **beyond the proven frontier**. The
strongest proven structure (run bound #4) yields only `c = 1/o(n) → 0`. So the gap between "what is
proven about a moving digit of `3ⁿ`" and "what (K) needs" is the entire distance from a *vanishing*
constant to a *positive* constant. There is **no published one-sided positive density at any
index-dependent position of `3ⁿ`.**

---

## 3. AEV (arXiv:2510.11723) — what is actually PROVEN vs the gap

**Proven content (purely structural — the paper proves NO unconditional 3/2 distribution fact):**

- **Theorem 1.7 [PROVEN]:** the **normality conjecture** for minimal/maximal words of the base-`p/q`
  system is **equivalent** to **equidistribution mod `q^k`** of the ceiling-map orbits
  `T_{p/q}(x) = ⌈p·x/q⌉` (AEV's Conj 1.6). (v2 numbering: Conj 1.2 ⟺ Conj 1.6; a v1/search-index
  variant lists this as "Conj 1.3 ⟺ 1.6" — same theorem, renumbered. Use v2.)
- **Theorem 1.5 [PROVEN]:** the normality conjecture **implies** non-existence of `Z_{p/q}`-numbers
  (Conj 1.4), **under the hypothesis `p < q²`**. For `3/2`: `p=3 < 4 = q²` holds, so the chain
  specializes to **Mahler's 1968 Z-number conjecture**.
- **Supporting:** computation of `10⁶` letters of `wmin_{3/2}(2)`; richness thresholds; deviation-
  from-normality "looks like a random word." Empirical only. [OBSERVED]

**What is conjectured (ALL open, all bases incl. 3/2):** Conj 1.2 (normality), Conj 1.4 (no
`Z_{p/q}`-numbers ⊇ Mahler), Conj 1.6 (equidistribution mod `q^k`).

**Methods NOT used (so no analytic input to borrow):** no ergodic/transfer-operator, no exponential-
sum/Fourier, no subspace-theorem attack on the distribution itself. The hard analytic equidistribution
is **left entirely open**; AEV contribute the *equivalences* and *numerics*.

**The precise logical gap from AEV-proven to (K):** (K) needs the single **marginal** equidistribution
of `d_n`, which (via the repo's reduction chain, `SESSION_2026-06-29_AEV_CORE.md` §1) is exactly
Conj 1.6 at `α=8` / the `p=3,q=2` case. AEV prove Conj 1.6 is **equivalent** to a normality statement
and **implies** Mahler — but prove **neither**. So the gap = the full unproven core: Conj 1.6 itself.
AEV reframe the wall; they do not lower it. `(K)` ⊆ Conj 1.6 = Conj 1.2; the digit-community headline
(Ren–Roettger / full block normality) is a strict **superset** of `(K)`.

---

## 4. The precise missing arithmetic input for the EXOGENOUS part

The cleanest equivalent open lemmas for `d_n` alone (each [OPEN], each ⟺ Mahler-`(3/2)` at `α=8`):

- **(K-Weyl, single-orbit lacunary cancellation) — the sharpest analytic form.** For each fixed
  integer `h ≠ 0`,
  > **`(1/N) Σ_{n<N} e( h · 8 · (3/2)ⁿ / 2^{k+3} ) = o(1)`  as `N → ∞`.**
  Equivalently `(1/N) Σ_{n<N} e(h·(3/2)ⁿ·c) → 0` for the specific constant `c`. This is a
  **single, specified lacunary geometric orbit** `(3/2)ⁿ`. Even **`o(1)` with no rate** is open; a
  **power-saving** `≪ N^{−δ}` would be far beyond anything known. (Contrast: for a.e. `α`,
  `{α(3/2)ⁿ}` equidistributes — **Koksma 1935** — but `α=8` is one measure-zero point; the
  exceptional set has **full Hausdorff dimension**, de Mathan–Pollington / Bugeaud, so no soft sieve
  selects `α=8` out of it.)

- **(K-density, weakest sufficient non-degeneracy).** `liminf_N (1/N)#{n<N : d_n = 0} > 0` — a single
  **positive** lower density of one digit value at the moving position. The frontier yields only the
  vanishing `1/o(n)` (run bound). **A constant `c>0` here is the minimal missing arithmetic fact.**

- **What KIND of input would close it.** Any ONE of:
  (i) a **sub-polynomial / power-saving bound on the single exponential sum** `Σ_{n<N} e(h·(3/2)ⁿ c)`
  for the specified `c` (the K-Weyl sum) — the analytic crux;
  (ii) an **effective single-specified-orbit equidistribution** theorem for `x↦⌈3x/2⌉ mod 2^k` (AEV
  Conj 1.6 at one orbit) — the dynamical crux;
  (iii) a **lower bound on the gap to a half-plane carry pattern**, i.e. `|8·3ⁿ mod 2^{n+k+1} − (a
  diagonal-fixing target)| ≥ 2^{(1−δ)n}`, strong enough to force the diagonal bit to oscillate — a
  Diophantine/linear-forms crux. The existing subspace/Baker bounds give run-length `o(n)` but **not**
  the per-index oscillation needed for positive density.

All three are restatements of the **same** missing fact: **cancellation in a single lacunary
geometric exponential sum at the integer base point `α=8`.** This is the exogenous wall. No known
method (Weyl — wrong position; Rowland — fixed column, no transfer; subspace/linear-forms — sublinear
counts and run bounds, vanishing density; Mauduit–Rivat digit-sum machinery — needs a polynomial/prime
input feed, not a single lacunary orbit) supplies even the one-sided `c>0`.

---

## Sources

- Weyl, H., *Über die Gleichverteilung von Zahlen mod. Eins*, Math. Ann. 77 (1916). (leading-digit equidistribution)
- Rowland, E., *Regularity versus complexity in the binary representation of 3ⁿ*, Complex Systems 18 (2009), arXiv:0902.3257.
- Senge, H.G., Straus, E.G., *PV-numbers and sets of multiplicity*, Period. Math. Hungar. 3 (1973) 93–100.
- Stewart, C.L., *On the representation of an integer in two different bases*, J. reine angew. Math. 319 (1980) 63–72.
- Bugeaud, Y., Kaneko, H., *On the digital representation of integers with bounded prime factors*, arXiv:1609.07926; Ann. Sc. Norm. Super. Pisa (2018).
- Drmota, M., Spiegelhofer, L., *The joint distribution of binary and ternary digit sums*, arXiv:2501.00850 (Jan 2025). [main tool: Baker's theorem; NOT the run lemma — attribution caveat §1]
- Schlickewei, H.P., *p-adic subspace theorem* (the engine of the `L(M·3^K)=ηK+o(K)` run bound; exact recent paper/lemma reference PENDING re-sourcing).
- Howe, E., *Powers of 3 with few nonzero bits and a conjecture of Erdős*, arXiv:2105.06440 (2021).
- *Bits of 3ⁿ in binary, Wieferich primes and a conjecture of Erdős*, J. Number Theory 159 (2015), S0022314X15002139.
- Ren, X., Roettger, C., *Ternary Digits of Powers of Two*, arXiv:2511.03861 (Nov 2025).
- Andrieu, M., Eliahou, S., Vivion, L., *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (v1 Oct 2025; v2 Apr 2026). Thm 1.5, Thm 1.7.
- Koksma, J.F. (1935) — a.e.-`α` equidistribution of `{α(3/2)ⁿ}`; de Mathan–Pollington, Bugeaud — full-dimension exceptional set.
- Mauduit, C., Rivat, J.; Drmota, Mauduit, Rivat — sum-of-digits equidistribution (polynomial/prime feeds; not applicable to a single lacunary orbit).
- Cross-refs: `DIGITS_OF_3N.md`, `AEV_DIGEST.md`, `SESSION_2026-06-29_AEV_CORE.md`, `WALL_B_WHICH_PART.md`, `WEAPONS_AUDIT_2026-06-29.md`.

---

No machine decided. No label upgraded.
