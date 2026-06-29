# PROBE — Siegel's (p,q)-adic Wiener Tauberian machinery vs the Antihydra frequency kernel (K) (2026-06-30)

*WEAPONS_AUDIT-style probe of ONE sharp question: does Maxwell C. Siegel's (p,q)-adic Fourier / Wiener
Tauberian theory for `qx+1` maps deliver a SINGLE-ORBIT Cesàro density (= the frequency kernel (K)), or only
an ANNEALED / measure-level average (reducing, like the Rajchman tier)? SOUNDNESS: every claim labelled; this
note does NOT claim to solve (K). Honest verdict only. NOT committed.*

Kernel **(K)** (recap): single-orbit equidistribution of `c_n mod 2^k` for `c_{n+1}=⌊3c_n/2⌋` (= base-3/2
normality = mean `D=v2(3o−1) ≥ 3/2` = Mahler 3/2 / AEV). Antihydra is a (2,3)-adic object (2 in denominator,
3 in numerator), an induced `qx+1`-type map `T(o)=3^{D−1}(3o−1)/2^D` with `q=3`.

---

## 0. One-line verdict

**[ANNEALED / reduces]** — and, more sharply, Siegel's framework is built to answer a *different invariant*
(periodicity vs. divergence = boundedness/cycle structure), whose Tauberian output is an explicit
**"almost every integer"** (measure-level) statement. The Wiener Tauberian step **never descends to one
specified orbit**, and even if it did it would not produce a Cesàro residue-*frequency*. It does **not** reach
(K). It is one more, particularly clean, incarnation of the annealed/quenched seam — and, as a bonus, of the
*boundedness-vs-frequency* mismatch.

---

## 1. What Siegel's framework actually computes (precise)

Siegel (USC PhD 2022; *The Collatz Conjecture & Non-Archimedean Spectral Theory*, Parts I–IV; survey
arXiv:2412.02902) builds a **Fourier theory of functions `ℤ_p → ℤ_q`** for distinct primes `p≠q` — here the
native `(2,3)`-adic setting for a `3x+1`-type map. The objects:

- **The numen `χ_H` (a.k.a. `χ_q`).** A function `χ_H : ℤ_2 → ℤ_q` (for the shortened `qx+1` / Hydra map `H`)
  that *encodes the dynamics*: the rational-integer **values attained** by `χ_H` on 2-adic inputs control the
  periodic and divergent points of `H` in `ℤ`. It is **discontinuous**, so it is handled not as a function but
  as a **(2,q)-adic measure** `χ_q(z)dz`, analyzed via its **Fourier–Stieltjes transform** `\hat{χ_q}`.
  [Output type marker: a measure / spectral object, not an orbit functional.]
- **The Correspondence Principle (CP).** A near-equivalence: a rational integer `x` is a **periodic point** of
  `H` iff a certain rationality/value condition on `χ_H` holds; and if an **irrational** 2-adic integer satisfies
  a complementary condition, the associated point is a **divergent point**. CP translates *which points cycle vs.
  which escape to infinity* into value-distribution properties of `χ_H`.
- **The (p,q)-adic Wiener Tauberian Theorem (WTT).** Equates **density of the span of translates** of the
  Fourier–Stieltjes transform `\hat{χ_q}` with **non-vanishing of the Radon–Nikodym derivative of the measure
  at all points of `ℤ_p`**. Siegel calls the resulting program **"Tauberian Spectral Theory."**

> **Output type [PINNED].** The terminal conclusions are of the form *"`\hat{χ_q}` is bounded away from zero
> (in `q`-adic absolute value) ⟹ **almost every integer** is a divergent point of `H`"* (and dually for
> periodicity). This is an **`a.e.`-integer / measure-level** statement — a property of the *ensemble* of
> starting points carried by the (2,q)-adic measure, NOT of any one specified seed's trajectory, and NOT a
> Cesàro frequency of residues. (Confirmed: Part IV exposition states the WTT "operates at the measure-theoretic
> level rather than individual orbits… system-wide behavior… not individual orbit characteristics.")

---

## 2. Instantiation for Antihydra — [framework APPLICABLE, target MISMATCHED]

- **Class membership: YES.** Antihydra's induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v2(3o−1)`, is a
  shortened `qx+1`-type (Hydra) map with `q=3`, living in exactly the `(2,3)`-adic dictionary Siegel's theory is
  native to. A numen `χ_3 : ℤ_2 → ℤ_3` and its Fourier–Stieltjes transform are *constructible* in principle.
  The program's proven `(2,3)` coupling `v3(o_{j+1}) = D_j − 1` (`ADELIC_COUPLING.md §1a`) is precisely the kind
  of 2-adic-input ↔ 3-adic-output linkage `χ_3` is designed to package. So the framework is **not vacuously
  NOT-APPLICABLE** — it genuinely covers the map.
- **But the invariant is the wrong one.** Siegel's CP/WTT classify **periodic vs. divergent** points =
  *boundedness / cycle structure*. The Antihydra orbit grows `|o_n| ≈ (3/2)^n` — it is **trivially a "divergent
  point"** for *every* seed; boundedness carries **zero** information about halting. Antihydra halting reduces
  to the **even-step density / `freq(D=1)`** along the one orbit (a Cesàro *frequency*), which is a strictly
  finer functional than "does the orbit escape to ∞." Siegel's machine, fully instantiated, would report
  "divergent" and say nothing about the density (K) needs. **The object it computes and (K) are different
  functionals** (the same boundedness-vs-frequency split catalogued in `BB6_OBSTRUCTION_DICHOTOMY.md §4`).

---

## 3. The decisive single-orbit-vs-annealed determination — the exact deciding step

The averaging is **structural to the Wiener Tauberian theorem itself**, not an incidental choice:

> **Deciding step.** WTT is the statement *"translates of `f∈L^1` are dense ⟺ `\hat f` vanishes nowhere."*
> Its non-archimedean (p,q)-adic form (Siegel, Part III) reads: *density of the span of translates of the
> Fourier–Stieltjes transform `\hat{χ_q}` ⟺ the Radon–Nikodym derivative `dχ_q` is non-vanishing **at all
> points of `ℤ_p`***. Both sides are **`L^1` / measure-global** quantities (an integral / a.e. condition over
> all of `ℤ_p` against Haar measure). The theorem **converts a spectral non-vanishing into an `a.e.`-integer
> dynamical conclusion** — the canonical Tauberian `transform-decay ⟹ averaged-asymptotic` move. There is **no
> evaluation functional `δ_{seed}`** anywhere in the chain: a single 2-adic point (the seed) is Haar-null, and
> WTT's hypotheses/conclusions are insensitive to null modifications. The annealing happens **exactly at the
> passage from `χ_q` to the measure `χ_q(z)dz` and its Fourier–Stieltjes transform** (Part IV: χ_q is
> discontinuous, so it is *forced* to be read as a measure) — the same `function → measure → annealed average`
> seam as the program's Rajchman second-diagonal route (`SECOND_DIAGONAL_RAJCHMAN.md`) and the transfer-operator
> route. Antihydra lands on the **annealed** side.

So: the Tauberian step delivers an **annealed `a.e.`-integer** statement (about boundedness), **not** the
single-orbit Cesàro density (K). This matches the honest prior exactly.

No single-orbit handle appears, hence no circularity to scrutinize on the upgrade side — there is nothing to
upgrade.

---

## 4. Where it averages (the seam, pinpointed) — and why no reduction of difficulty

- **The seam:** `χ_q` (a single dynamical encoder) `⟶` `χ_q(z)dz` (a (2,q)-adic **measure**, forced by χ_q's
  discontinuity) `⟶` `\hat{χ_q}` Fourier–Stieltjes transform `⟶` WTT `⟶` **`a.e.`-integer** value-distribution.
  The orbit-specific information (which seed, its residue statistics) is integrated out at the first arrow and is
  never recovered.
- **Two independent reasons it cannot reach (K),** either one fatal:
  1. **Annealed, not quenched.** Output is `a.e.`-integer / measure-level (`ν`-tier), not a property of seed `8`.
  2. **Wrong invariant.** Output is periodicity/divergence (boundedness); (K) is a Cesàro residue-*frequency*.
     Antihydra is divergent for all seeds, so Siegel's classification is *constant* on the relevant family.
- **Net:** like the adelic product formula (first-moment-only) and Furstenberg/Rudolph (measure-only), Siegel's
  (p,q)-adic WTT is a real, native, un-instantiated-before formalism for the `(2,3)`-adic map, but it is an
  **isomorphic restatement on the annealed/boundedness tier**, not a reduction of (K)'s difficulty.

---

## 5. Verdict

| Question | Answer | Label |
|---|---|---|
| Is the framework applicable to the Antihydra `(2,3)`-adic map? | Yes — a shortened `qx+1`/Hydra map with `q=3`; numen `χ_3:ℤ_2→ℤ_3` constructible | [APPLICABLE at framework level] |
| Does the Wiener Tauberian step give a SINGLE-ORBIT Cesàro density (= K)? | **No** — it gives an `a.e.`-integer / measure-level statement; no `δ_seed` functional exists in the WTT chain | [ANNEALED] |
| Does it even compute a residue *frequency*? | **No** — it classifies periodic vs. divergent (boundedness); Antihydra is trivially divergent for all seeds | [wrong invariant] |
| Overall | Native, un-instantiated formalism; lands on the annealed/boundedness tier; isomorphic restatement, not a reduction | **[reduces]** |

**Decisive deciding step:** the (p,q)-adic Wiener Tauberian theorem's `L^1`/measure-global form
(`density of translates of \hat{χ_q} ⟺ a.e. non-vanishing of dχ_q on ℤ_p`) converts spectral non-vanishing into
an **almost-every-integer** dynamical conclusion; the seed is Haar-null and drops out at the `χ_q → χ_q(z)dz`
measure passage. Annealed side.

---

## Sources

- M. C. Siegel, *The Collatz Conjecture & Non-Archimedean Spectral Theory — Part I — Arithmetic Dynamical
  Systems and Non-Archimedean Value Distribution Theory*, arXiv:2007.15936 (numen `χ_q`, Correspondence
  Principle).
- M. C. Siegel, *… Part I.5 — How To Write The (Weak) Collatz Conjecture As A Contour Integral*, arXiv:2111.07883.
- M. C. Siegel, *… Part II — (p,q)-Adic Fourier Analysis and Wiener's Tauberian Theorem*, arXiv:2208.11082
  (Springer, *p-Adic Numbers, Ultrametric Analysis and Applications*, 2025; DOI 10.1134/S2070046625020062).
- M. C. Siegel, *(p,q)-adic Analysis and the Collatz Conjecture* (PhD dissertation; survey arXiv:2412.02902).
- M. C. Siegel, Collatz Research / Parts III–IV expository pages, siegelmaxwellc.wordpress.com (Tauberian
  Spectral Theory; "operates at the measure-theoretic level rather than individual orbits"; "Fourier–Stieltjes
  transform bounded away from zero ⟹ almost every integer is a divergent point").
- Cross-refs (this repo): `SCOUT_ARITH_DYNAMICS.md §4`, `BB6_CROSSFIELD_SCOUT.md §2.1`, `ADELIC_COUPLING.md §1a`,
  `BB6_OBSTRUCTION_DICHOTOMY.md §4` (boundedness-vs-frequency, annealed-vs-quenched seams),
  `SECOND_DIAGONAL_RAJCHMAN.md` (the `function→measure→a.e.` Rajchman tier this matches).

No machine decided. No label upgraded.
