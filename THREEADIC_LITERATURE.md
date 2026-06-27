# 3-adic / divisibility-by-3 framing of the Antihydra kernel — literature survey (2026-06-28)

*Angle: the `ADELIC_COUPLING.md` exact identity `v3(o_{j+1}) = D_j − 1` re-encodes the kernel as a
**3-adic divisibility-density** statement: `freq(D=1)=density{3∤o_{j+1}}`, target ⟺
`density{3|o_j}+density{9|o_j} ≥ 1/2`, with orbit 3-adic law `P(v3=k)=2^{−(k+1)}`. QUESTION: does the
3-adic / divisibility-by-3 side connect to an EASIER or DIFFERENT literature than the 2-adic Mahler `(3/2)^n
mod 2^k` side? Includes the dual digit problem (binary digits of `3^n`, ternary digits of `2^n`). Numerics
`.venv` only (`adelic_coupling.py` re-run inline). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

The 3-adic framing connects to a **genuinely DIFFERENT body of literature** than the 2-adic Mahler side —
specifically **Tao's Syracuse-random-variable 3-adic equidistribution (the `β=1` conjecture)** and the
**(2,3) digit-exchange literature** (ternary digits of `2^n` / binary digits of `3^n`: Senge–Straus,
Stewart, Ren 2025, Erdős). **But it is NOT easier**: every member of that literature is (i) on the same
single-orbit / equidistribution / density axis, (ii) **open**, and (iii) gives **no one-sided positive
density** for any specific orbit or any specific digit value. For OUR orbit the two sides are **provably
isomorphic** (the coupling `v3(o_{j+1})=D_j−1` is a verbatim relabeling, 0 exceptions / 2·10⁵ steps), so
the 3-adic side carries the **same wall**, only dressed in different citations. **`[verdict: distinct
literature, identical difficulty — no easier route found]`**

---

## 1. The exact coupling makes the two sides isomorphic FOR OUR ORBIT `[PROVEN]`

`3o−1 ≡ −1 (mod 3)` ⟹ `3∤(3o−1)` ⟹ `3∤m` (odd part) ⟹ `v3(o') = v3(3^{D−1}m) = D−1`. Re-verified inline:

```
steps 200000  coupling exceptions 0
density{3|o_next}= 0.49966   density{9|o_next}= 0.24888   sum= 0.74854   (target ≥ 1/2, big margin)
freq(D=1)= 0.50034   mean D= 1.99627
v3 law vs 2^-(k+1):  k=0 .50034/.50000  k=1 .25078/.25000  k=2 .12535/.12500 ... (matches to 3 dp through k=7)
```

> **`[PROVEN]`** The 3-adic divisibility statistic of the orbit is the 2-adic `D`-statistic **relabeled by a
> bijection** `k ↦ k+1`. There is no information in the 3-adic side that is not already in the 2-adic side
> for THIS orbit. Hence any hope of an "easier 3-adic theorem" must come from a literature that controls the
> 3-adic side **without** going through the 2-adic depth — i.e. a *3-side-native* density result. §2–§4 ask
> whether such a thing exists. It does not.

Note the orbit's 3-adic law `P(v3=k)=2^{−(k+1)}` is **NOT** the `Z_3`-Haar law `(2/3)3^{−k}` and **NOT**
Tao's Syracuse-`Z/3` law `(0,1/3,2/3)` (§2). Our map is `×3/2` (one ×3, geometric # of ÷2), so its 3-adic
fingerprint is dictated by the **2-adic predecessor**, not by an intrinsic 3-adic mixing. This already warns
that the 3-side-native Collatz literature (which is about the `3x+1` Syracuse 3-adic law) is about a
**different object**.

---

## 2. 3-side-native Collatz/Syracuse literature — Tao's `β` conjecture `[survey; OPEN, ensemble]`

**Tao 2019/2022, "Almost all orbits of the Collatz map attain almost bounded values"** (Forum of Math. Pi;
blog "Equidistribution of Syracuse random variables and density of Collatz preimages", 2020-01-25). This is
the **one place the 3-adic structure of a Collatz-type map is the central object** (Tao explicitly: the
Syracuse map — largest odd divisor of `3N+1` — is *better suited than Collatz for the 3-adic structure*,
"one multiplication by 3, a variable number of ÷2"). What is actually there:

- **Explicit 3-adic law of the Syracuse random variable** `Syrac(Z/3^n)`: e.g.
  `P(Syrac(Z/3) = b) = 0, 1/3, 2/3` for `b ≡ 0,1,2 (mod 3)` (avoids `0 mod 3`), with explicit higher-`3^n`
  distributions. `[PROVEN, but for the random-variable MODEL]`
- **`β` parameter.** Let `c_n = inf` over non-`0(mod3)` classes of the `Syrac(Z/3^n)` mass; submultiplicative
  (Lemma 2), so `c_n = 3^{−βn+o(n)}`, `β ≥ 1`. **Full 3-adic equidistribution = the conjecture `β = 1`.**
  This is **OPEN**. Tao's positive-density-of-preimages corollary is **conditional on `β=1`**.
- **Ensemble, not single-orbit.** `Syrac(Z/3^n)` is a *random variable* (geometric ÷2 steps assumed); the
  "almost all" theorem is **log-density over starting points**. It produces **no per-orbit time statistics**
  and in particular **no `density{3|o_j}` for a specified orbit** (the WebFetch of the blog confirms: "does
  NOT establish density of divisibility by 3").

> **`[survey verdict]`** The 3-adic side of Collatz-type maps **is** a studied literature (Tao's `β`), and it
> is **different** from Mahler 2-adic `(3/2)^n mod 2^k`. **But (a)** it is about the `3x+1` Syracuse 3-adic
> law `(0,1/3,2/3)`, **not** our `×3/2` law `2^{−(k+1)}` — a different object; **(b)** it is **ensemble /
> almost-all**, never single-orbit; **(c)** the equidistribution we would need (`β=1`-type) is itself
> **OPEN**. So the 3-adic Collatz literature is neither easier nor applicable to `o₀=27`. It is the **same
> tier of openness** (effective single-orbit equidistribution), reached from the other valuation.

---

## 3. The (2,3) digit-exchange — binary digits of `3^n` / ternary digits of `2^n` `[survey; NO one-sided density]`

The prompt's dual statement `a_n = bit_n(8·3^n)` is a **binary digit of `3^n`**; the 3-adic side is "`3 |
orbit`". The `(2,3)`-digit-exchange asks for the distribution of digits of `3^n` in base 2 (or `2^n` in
base 3). State of the art — **all results are either "→∞ sublinearly" or conjectural; none give a positive
or one-sided density**:

- **Senge–Straus (1973), "PV-numbers and sets of multiplicity", Period. Math. Hungar.** If `log a/log b` is
  irrational then the number of **nonzero base-`b` digits of `a^n` → ∞**. Covers BOTH directions (nonzero
  binary digits of `3^n` → ∞, nonzero ternary digits of `2^n` → ∞). **Ineffective.** `[PROVEN]`
- **Stewart, C.L. (1980), "On the representation of an integer in two different bases", J. Reine Angew. Math.
  319.** Effective quantitative version: for `m≥25`, `n_3(2^m) > (log m)/(log log m + c) − 3`. By symmetry the
  same shape bounds nonzero binary digits of `3^n`. `[PROVEN, EFFECTIVE]`
  - **Crucial for us:** this lower bound is `Θ(log m / log log m)` = **`o(n)`** in the length `n ≍ m`. It is
    **sublinear**, so it **does NOT establish positive density of nonzero digits**, let alone a one-sided
    density `≥ const` of any digit *value*. It is **infinitely far** from what the kernel needs (a `≥1/2`
    density). Same "individual-term / counting, not density" failure mode catalogued in `BAKER_LINFORMS.md`.
- **Ren, Xuyi (2025), arXiv:2511.03861 "Ternary Digits of Powers of Two".** Conjectures **uniform
  distribution** of length-`k` blocks in base-3 digits of `2^n`; numerics to `n=10⁶` support it; **nothing
  proven** about any frequency/density; cites a *weaker* Erdős conjecture, still open. (Also studies
  normality of `log_3 2`, conjectural.) `[OPEN]`
- **arXiv:2202.13256, "On two conjectures concerning the ternary digits of powers of two"** — same circle,
  open. **Erdős conjecture**: only `2^0,2^2,2^8` (=1,4,256) have base-3 digits ⊂ {0,1}. **OPEN.**
- **arXiv:2105.06440, "Powers of 3 with few nonzero bits and a conjecture of Erdős"** — the **direct dual**
  (binary digits of `3^n`): "about half the bits of `3^n` are nonzero" is **Ed Pegg's CONJECTURE**; proven
  results only finiteness of `3^n` with few nonzero bits, not a density. `[OPEN]`
- **Dimitrov–Howe / Lagarias-type observations** (via the search): "powers of 2 omitting digit 2 in base 3
  form a small set" — a **support/sparsity** statement (cf. the support-vs-density axis split in
  `KERNEL_FINAL.md §3–5`), not a density of `3|·`.

> **`[survey verdict]`** The `(2,3)` digit-exchange is a real, distinct, classical literature
> (Senge–Straus / Stewart / Bugeaud / Ren / Erdős). It gives exactly **one** unconditional handle —
> *#nonzero digits → ∞ at rate `log n/log log n`* — which is **`o(n)`, hence no density**, one-sided or
> otherwise. Everything at the density/uniformity level is **conjectural** (numerics to `10⁶`). So the dual
> digit problem supplies **no one-sided density** and is **as open as** the 2-adic Mahler side.

---

## 4. Linear-recurrence / multiplicative-function `v_3` density results — DO NOT apply `[survey; off-class]`

Asked: are densities `density{3|a_n}` / distributions of `v_3(a_n)` *known* for dynamically-defined `a_n`?
**Yes — but only for the CLOSED-FORM (constant-recursive / linear-recurrence) class, which our orbit is not.**

- **Rowland, "p-adic asymptotic properties of constant-recursive sequences".** For a **linear recurrence**
  `a_n`, the density of residues mod `p^α` converges (as `α→∞`) to the Haar measure of an explicit subset of
  `Z_p`; `v_p(a_n)` distributions are computable. `[PROVEN — for linear recurrences only]`
- **arXiv:2402.18279 (3rd-order linear recurrences), Marques–Lengyel-type `v_p` conjectures** — exact `v_p`
  laws for recurrence sequences (Fibonacci-like). `[PROVEN/partly — linear recurrences]`

**Why inapplicable.** These methods rest on a **closed form** (`a_n = Σ c_i α_i^n`) so the `mod p^α` orbit
is **eventually periodic / automatic**, giving exact densities. Our `o_j` is the orbit of a **non-affine,
non-eventually-periodic** map `o ↦ 3^{D−1}(3o−1)/2^D` with `D=v2(3o−1)` state-dependent: the `mod 3^k` orbit
is **not** a linear-recurrence residue sequence (it is the very Collatz/3-2 dynamics whose equidistribution
is open). So the one literature that DOES give exact `density{3|·}` is exactly the class our sequence escapes.
`[verdict: off-class, no transfer]`

---

## 5. Bottom line — the three asks

| ask | answer | label |
|---|---|---|
| Does the 3-adic / divisibility-by-3 framing connect to a DIFFERENT / EASIER literature than 2-adic Mahler? | **Different: YES** (Tao Syracuse `β`-conjecture §2; `(2,3)` digit-exchange Senge–Straus/Stewart/Ren/Erdős §3; linear-recurrence `v_p` densities §4). **Easier: NO** — each is open, single-orbit-or-ensemble equidistribution, and gives no one-sided density; the linear-recurrence one is off-class. | `[survey]` |
| Any result on digits of `3^n` or `v3` of a Syracuse orbit giving a ONE-SIDED density? | **NO.** Best unconditional fact = *#nonzero base-`b` digits of `a^n` → ∞* at rate `log n/log log n` (Senge–Straus / Stewart) = **`o(n)`, sub-density**. All density/uniformity statements (Ren, Erdős, Pegg, Tao `β=1`) are **conjectural**. No published `density{3|o_j} ≥ c>0` for any specific 3/2- or Syracuse orbit. | `[PROVEN-negative]` |
| Isomorphic to the 2-adic wall, or genuinely distinct? | **For our orbit: ISOMORPHIC** — `v3(o_{j+1})=D_j−1` is an exact bijection (0 exc / 2·10⁵), so the 3-adic density IS the 2-adic `D`-law relabeled; same wall. **As a literature: distinct citations, identical difficulty tier** (effective single-orbit equidistribution of a `×2,×3`/`(3/2)`-type system). | `[PROVEN]` |

### What was gained (banked)
- **New literature placement (3-adic axis):** the kernel's 3-adic form sits next to **Tao's Syracuse `β=1`
  conjecture** (3-adic equidistribution of `3x+1`) and the **`(2,3)` digit-exchange** (Senge–Straus 1973 /
  Stewart 1980 / Ren arXiv:2511.03861 / Erdős–Pegg binary digits of `3^n`, arXiv:2105.06440 / 2202.13256).
  This **complements** the 2-adic AEV / Mahler placement in `KERNEL_FINAL.md` — same wall, two literatures.
- **Sharp negative:** the ONLY unconditional digit theorem is sublinear (`o(n)` nonzero digits), so the
  digit-exchange route **cannot** yield the `≥1/2` density; it fails on the same *individual-term-vs-density*
  axis as Baker/Padé (`BAKER_LINFORMS.md`) and FLP spread (`KERNEL_FINAL.md §5`).
- **Off-class clarification:** exact `density{3|a_n}` results exist ONLY for **linear recurrences** (Rowland;
  Marques–Lengyel); our 3-2 orbit is provably not in that class, so no transfer.

### Honest non-breach
The 3-adic re-encoding is a **change of citations, not of difficulty**. The decisive obstruction is unchanged:
single-orbit equidistribution of an explicit `×3/2` orbit (Mahler / AEV `p/q=3/2` / Tao `β`), open in every
valuation. Consistent with `ADELIC_COUPLING.md` ("isomorphism of obstructions, not a reduction") and
`KERNEL_FINAL.md` (AEV is the weakest named conjecture that closes it).

## References
- Senge, H.G., Straus, E.G., *PV-numbers and sets of multiplicity*, Period. Math. Hungar. 3 (1973) 93–100.
- Stewart, C.L., *On the representation of an integer in two different bases*, J. Reine Angew. Math. 319 (1980) 63–72.
- Tao, T., *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi 10 (2022) e12; blog "Equidistribution of Syracuse random variables…" (2020-01-25).
- Ren, X., *Ternary Digits of Powers of Two*, arXiv:2511.03861 (2025).
- *On two conjectures concerning the ternary digits of powers of two*, arXiv:2202.13256.
- *Powers of 3 with few nonzero bits and a conjecture of Erdős*, arXiv:2105.06440.
- Rowland, E., *p-adic asymptotic properties of constant-recursive sequences* (ericrowland.github.io/papers).
- *On the p-adic valuation of third order linear recurrence sequences*, arXiv:2402.18279.
- (cross-refs) `ADELIC_COUPLING.md`, `KERNEL_FINAL.md`, `BAKER_LINFORMS.md`, `INDUCED_RESIDUE_STRUCTURE.md`.
