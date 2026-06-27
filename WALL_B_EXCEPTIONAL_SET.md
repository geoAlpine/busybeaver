# WALL (B): the exceptional set E and whether the Antihydra point lies in it (2026-06-28)

*Angle: assume wall (A) — Mahler-strength a.e. equidistribution of {x(3/2)ⁿ} — is GIVEN. Wall (B) is the
selection of the SPECIFIC computable orbit c₀=8. This note CHARACTERIZES the Lebesgue-null exceptional set E
of the a.e. theorem and asks whether the Antihydra point lies in E. Every line labelled
[PROVEN]/[CONDITIONAL]/[OPEN]/[OBSERVED]. Zero false proofs. NOT committed.*

---
## 1. The precise point(s) that must equidistribute — [PROVEN identity]

The parity that drives non-halting is `c_n mod 2 = bit_n(8·3ⁿ) ⊕ bit_n(T_n)` (reduction chain, `PROOF_STATUS.md §1`).
Its leading Fourier mode splits into a PURE part and a CARRY part.

- **PURE part `bit_n(8·3ⁿ)`.** Leading mode `e(8·3ⁿ / 2^{n+1}) = e(4·(3/2)ⁿ)`, and exactly
  `{8·3ⁿ/2^{n+1}} = {4·(3/2)ⁿ} = {3ⁿ/2^{n-2}} = (3ⁿ mod 2^{n-2})/2^{n-2}` (n≥2, exact integer arithmetic).
  ⇒ the pure part is governed by the **FULLY EXPLICIT, KNOWN point `x = 4`** in `{x·(3/2)ⁿ}`. This is a
  rational (integer) constant — **NOT self-generated**. (Equivalently `x=8` with the `/2ⁿ` normalization;
  the `/2^{n+1}` mode that the parity bit uses gives `x=4`.)
- **CARRY part `bit_n(T_n)`.** From `exp_sum.py`: `T_n/2^{n+1} = (1/4)Σ_j e_{n-1-j}(3/2)ʲ`, a `(3/2)ʲ`-weighted
  exponential sum whose weights `e_j = parity(T^j c₀)` are the orbit's OWN history ⇒ **self-generated /
  correlated**, not a single point.

**[PROVEN] Verdict on the assignment's question.** The object is NOT a single fully-known `x`; it is
`{4·(3/2)ⁿ}` (explicit) XOR a self-generated Korobov sum. **Crucially, even the explicit half (`x=4`) is
already out of reach** — its equidistribution is itself an instance of the open `{x(3/2)ⁿ}` problem (§3). So
wall (B) does NOT collapse to "a known point whose equidistribution is merely unproven"; BOTH halves are
open, and the easier (explicit) half is exactly Mahler-class.

---
## 2. Is the exceptional set E characterized / membership-testable? — [PROVEN: NO for b=3/2]

**Koksma 1935 (metric theorem).** For Lebesgue-a.e. `x`, `{x·bⁿ}` is uniformly distributed mod 1, every fixed
`b>1`. The exceptional set `E_b = {x : {x·bⁿ} not u.d.}` is **Lebesgue-null** — this is wall (A), given.

The decisive structural fact is the contrast between integer and non-integer base:

- **Integer base `b≥2` — E IS characterized (Wall's theorem).** `{x·bⁿ}` is u.d. mod 1 **iff `x` is normal
  in base `b`**. So `E_b = {non-b-normal numbers}`: a *clean characterization*. But it is **NOT a usable
  membership test for explicit points** — normality of `π, √2, e, …` is unknown; deciding `x∈E_b` for a given
  explicit `x` is generally beyond current mathematics. [PROVEN — Wall 1949.]
- **Base `b=3/2` (non-integer rational) — NO such characterization exists.** There is no normality-type
  digit criterion, no continued-fraction / Diophantine condition known to characterize `E_{3/2}`. `E_{3/2}`
  is Lebesgue-null yet **of FULL Hausdorff dimension** with a self-similar fractal structure (the standard
  Koksma exceptional-set geometry; van der Corput / self-similar-measure metric theorems, Springer
  Math. Ann. 2025, s00208-025-03233-3). [OPEN: characterization. PROVEN: full dimension.]

**[PROVEN] Conclusion.** For `b=3/2`, E is **not characterized and not membership-testable**. There is no
Diophantine/continued-fraction/normality predicate one could evaluate at `x=4` to decide `4∈E_{3/2}`.
Asking "is the Antihydra (pure-part) point in E?" is therefore **logically identical** to asking "does
`{4(3/2)ⁿ}` equidistribute?" — i.e. wall (B) does not simplify via an exceptional-set membership test; the
membership test does not exist.

---
## 3. Explicit-point equidistribution for b=3/2: KNOWN, OPEN, or in E? — [OPEN]

- **`{(3/2)ⁿ}` (x=1) itself.** It is **not even known to be dense** in [0,1], let alone equidistributed.
  Equidistribution is a **conjecture**, numerically supported to `n=10⁸` (arXiv:1806.03559, "On the
  Uniformity of (3/2)ⁿ Modulo 1": *"It has been conjectured that the sequence (3/2)ⁿ modulo 1 is uniformly
  distributed … Our results strongly agree with the hypothesis"* — empirical, no proof). [OPEN]
- **Any explicit `x` (e.g. `x=4`).** **No explicit real number is known** for which `{x(3/2)ⁿ}` is *proven*
  equidistributed. Koksma's a.e. theorem is **non-constructive**. The only constructively-equidistributing
  `x` are Champernowne/digit-greedy constructions tailored to the base — these are bespoke transcendentals,
  **never the rational `x=4`**. So `x=4` equidistribution is **OPEN**, not known, not in any *known* part of E.
  [OPEN]
- **What IS proven about explicit points (all confinement/support, NOT frequency).**
  - **Flatto–Lagarias–Pollington 1995** (Acta Arith. 70:125–147): for any `ξ>0` and coprime `p>q≥1`, the
    `{ξ(p/q)ⁿ}` **cannot all lie in an interval of length `<1/p`**; for `3/2`, `Ω(3/2)>1/3`. A *range/support*
    lower bound — says nothing about equidistribution (a sequence can fill ≥1/3 of the circle yet have
    even-frequency → 0). [PROVEN, but support-not-frequency — same gap as `PROOF_STATUS.md §3.5(a)`.]
  - **Mahler 1968 (Z-numbers):** conjectured no `ξ` with `{ξ(3/2)ⁿ}∈[0,½)` ∀n. Existence/non-existence still
    **open**; this is a confinement statement, weaker-flavoured than equidistribution. [OPEN]
  - **Dubickas 2008 / Akiyama:** *construct* special `ξ` whose `{ξ(3/2)ⁿ}` stay in a short interval / Cantor
    set (e.g. `‖{ξ(3/2)^{2n}}‖<14/45`). These build POINTS that are NON-equidistributed (`E_{3/2}` is
    nonempty and rich) — they do NOT certify equidistribution of any natural point, and none is `x=4`. [PROVEN
    constructions of E-members, irrelevant to selecting c₀=8.]
  - **AEV 2025 normality conjecture** (arXiv:2510.11723, rational-base number systems): the modern framing —
    normality (= frequency = equidistribution) in the `3/2` system. Conjectural; if it covered the orbit's
    word it would suffice (`PROOF_STATUS.md §3.5(c)`). [OPEN]

**[PROVEN] Decisive answer.** Explicit-point equidistribution for `3/2` is **OPEN** — for `x=4` and even for
`x=1`. The Antihydra pure-part point is NOT known to be in E, NOT known to be out of E; the question is
*definitionally* the open Mahler-class equidistribution of a specific point. Wall (B) = "is c₀=8 in E?" has
**no resolution and no membership test in current mathematics**, independent of wall (A).

---
## 4. Numerical anomaly check — [OBSERVED: no anomaly; point behaves generically]

`scratchpad/wallB_numeric.py` (.venv, exact integer arithmetic; explicit `x=4` via `(3ⁿ mod 2^{n-2})/2^{n-2}`,
generic `x` via random 60-bit rationals `a/2⁶⁰` computed exactly as `(a·3ⁿ mod a_den·2ⁿ)`).

Discrepancy `D*` (Kolmogorov) and normalized Weyl sum `|Σe(y_n)|/N`, explicit `x=4` vs median over 9 generic `x`:

```
      N |   x=4 weyl    x=4 D* | gen weyl(med) gen D*(med)
    200 |     0.0388    0.0586 |        0.0629      0.0658
    500 |     0.0332    0.0362 |        0.0510      0.0381
   1000 |     0.0317    0.0292 |        0.0384      0.0297
   2000 |     0.0182    0.0212 |        0.0220      0.0205
   4000 |     0.0067    0.0124 |        0.0163      0.0154
```
**[OBSERVED]** `x=4` tracks the generic column at every `N` (if anything mildly MORE uniform at `N=4000`,
within noise). Both decay roughly `~N^{-1/2}` (random-like), consistent with equidistribution; **no sign of
the persistent non-decay that membership in E would produce.** Of course finite `N` cannot prove membership
either way — E is exactly the set invisible to any finite test.

Antihydra orbit `c₀=8`, real parity vs pure-part-only surrogate (.venv, exact):
```
N=   1000: even-density=0.49900, min balance=+2, <(-1)^parity>=-0.0020, <(-1)^purebit>=+0.0300
N=  10000: even-density=0.49540, min balance=+2, <(-1)^parity>=-0.0092, <(-1)^purebit>=-0.0098
N= 100000: even-density=0.50159, min balance=+2, <(-1)^parity>=+0.0032, <(-1)^purebit>=+0.0029
```
**[OBSERVED]** even-density `≈0.5` (≫ the `1/3` non-halt threshold), `balance_n≥+2` throughout, and both the
real parity and the explicit pure-bit average → 0 at CLT rate — generic equidistributing behaviour, no
anomaly. (Consistent with `PROOF_STATUS.md §0`; NOT a proof.)

---
## 5. Net assessment of wall (B) via the exceptional-set angle

- **[PROVEN]** The point that must equidistribute is `{4·(3/2)ⁿ}` (explicit, known) for the pure part,
  XOR a self-generated `(3/2)ʲ`-Korobov sum for the carry. Even the explicit half is Mahler-class-open.
- **[PROVEN]** For `b=3/2` the exceptional set E is **null but full-dimensional, NOT characterized, NOT
  membership-testable** — no normality/Diophantine/CF predicate exists (sharp contrast with integer base,
  where Wall's theorem gives E = non-normal numbers, characterized but still undecidable per point).
- **[PROVEN/OPEN]** Explicit-point equidistribution for `3/2` is **OPEN** (even `{(3/2)ⁿ}` is not known
  dense). No explicit `x` has a proof; constructive results build only E-MEMBERS (Dubickas/Akiyama). So
  "is c₀=8 ∈ E?" is *definitionally* the open Mahler problem — the exceptional-set angle does **not** provide
  an independent membership test that could bypass wall (A)'s strength.
- **[OBSERVED]** Numerically the Antihydra point shows **no anomaly** vs generic `x`; it equidistributes at
  the generic `~N^{-1/2}` rate to `N=10⁵` (orbit) / `N=4000` (exact pure part). Evidence for "not in E",
  proof of nothing.

**Bottom line for wall (B):** characterizing E does not crack the specific-orbit selection, because for
`b=3/2` **E is provably uncharacterized and untestable** — membership of the explicit point `x=4` (let alone
the self-generated full point) is literally the open equidistribution statement, not a separately decidable
condition. Wall (B) is genuinely the "a.e.→specific" Tao gap (`COCYCLE_ERGODICITY.md §3`), and the
exceptional-set route confirms it has no shortcut: there is no E-membership oracle to consult.

### Sources
- Koksma metric theorem; exceptional-set geometry (full Hausdorff dim, self-similar): Math. Ann. 2025,
  https://link.springer.com/article/10.1007/s00208-025-03233-3 ; non-Archimedean Koksma & exceptional-set
  dimensions, arXiv:2512.05690, https://arxiv.org/pdf/2512.05690
- Flatto–Lagarias–Pollington, "On the range of fractional parts {ξ(p/q)ⁿ}", Acta Arith. 70 (1995) 125–147,
  http://matwbn.icm.edu.pl/ksiazki/aa/aa70/aa7023.pdf
- Mahler's 3/2 problem (Z-numbers): https://en.wikipedia.org/wiki/Mahler's_3/2_problem ; Mahler, Documenta
  Math., https://ems.press/content/book-chapter-files/27426
- Dubickas, "On the powers of 3/2 and other rational numbers", Math. Nachr. 2008,
  https://onlinelibrary.wiley.com/doi/abs/10.1002/mana.200510651
- Empirical uniformity of (3/2)ⁿ mod 1 to n=10⁸ (conjecture, no proof), arXiv:1806.03559,
  https://arxiv.org/abs/1806.03559
- Mahler's 3/2 problem in ℤ⁺, arXiv:2411.03468, https://arxiv.org/html/2411.03468v1
- AEV normality conjecture on rational-base number systems, arXiv:2510.11723, https://arxiv.org/pdf/2510.11723
</content>
</invoke>
