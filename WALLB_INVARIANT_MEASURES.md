# WALL (B) via the STRUCTURE OF INVARIANT MEASURES (2026-06-28)

*Attack the residual aperiodic wall-(B) piece — "the orbit is NOT Birkhoff-generic for any non-Haar
invariant measure with biased parity" — through the invariant-measure structure of the `×3/2` system.
Every line labelled `[PROVEN]`/`[CONDITIONAL]`/`[OPEN]`/`[OBSERVED]`. Numerics `.venv` only
(`scratchpad/inv_measures.py`). Zero false proofs. NOT committed.*

---

## 0. One-line answer (and the resolved trap)

**The prompt's worry is real but resolves cleanly: it depends on NOT conflating two different systems.**

- The relevant system for non-halt is the **2-adic `×3/2` map** `T(c)=(3c−(c mod 2))/2` on `ℤ₂`, which is
  **conjugate to the FULL 2-shift** (entropy `log 2`). Its measure of maximal entropy = uniform
  `Bernoulli(1/2)` = **Haar on `ℤ₂`**, and **parity = 1/2 under it `[PROVEN/standard]`**. The proof's
  target measure is **Haar = MME of the full shift**, and `parity = 1/2` holds exactly. **No problem.**
- The **`β=3/2` interval β-transformation** `T_β(x)=(3/2)x mod 1` on `[0,1)` is a **different** system: the
  (non-sofic) **β-shift**, entropy `log(3/2)`, MME = **Parry measure**, under which **`P(digit=1) ≈ 0.1995 ≠ 1/2`**
  `[OBSERVED + exact formula]`. **This is the conflation trap** the prompt flags: if one (wrongly) took the
  β-transformation as "the system," the natural invariant measure would give parity `≠ 1/2`. It is not the
  relevant system.
- **Intrinsic ergodicity does NOT crack it.** Both the full shift and the β-shift have a *unique* MME
  (Parry/Bowen; Hofbauer–Walters; Climenhaga–Thompson). But **uniqueness of the MME does not force a SPECIFIC
  orbit to be generic for it** — the set of non-generic points has **full entropy and full Hausdorff
  dimension** (Barreira–Schmeling 2000). This is the exact a.e.-vs-specific wall, now stated measure-theoretically.
- **"Full complexity `2^k` ⟹ not generic for any biased measure" is FALSE.** Full subword complexity is a
  *topological / support* fact; genericity for a measure is a *frequency* fact. A `Bernoulli(p)` sequence
  with `p≠1/2` has **full subword complexity `2^k`** (full support) yet **biased parity** `[OBSERVED]`.
  Excluding biased measures = proving genericity for Haar = **equidistribution. No shortcut; reduces to (A).**

---

## 1. Which system, which measure — the parity question `[PROVEN/standard]`

Two maps are routinely written "`×3/2`" but are **not the same dynamical system**:

| | (I) interval β-map `T_β(x)=(3/2)x mod 1` | (II) 2-adic `T(c)=⌊3c/2⌋` (Antihydra) |
|---|---|---|
| phase space | `[0,1)` | `ℤ₂` |
| symbolic model | **β-shift** (proper subshift, **non-sofic**, `3/2` non-Pisot) | **FULL 2-shift** `{0,1}^ℕ` |
| top. entropy | `log(3/2) ≈ 0.405` | `log 2 ≈ 0.693` |
| MME | **Parry measure** | uniform **Bernoulli(1/2) = Haar on `ℤ₂`** |
| symbol = | digit `⌊(3/2)x⌋` (threshold `x≥2/3`) | parity `c mod 2` |
| symbol freq under MME | `P(1) ≈ 0.1995` **≠ 1/2** | `P(odd) = 1/2` **exactly** |

The conjugacy in (II) is the repo's verified **injective itinerary coding** `c ↦ (e_n)`,
`ℤ₂ ↔ {0,1}^ℕ` (bijection `ℤ/2^{k+1} ↔` length-`(k+1)` words; `WALLB_NONATOMIC.md` §1), under which `T = σ`
(one-sided full shift, 2-to-1) and **Haar ↔ Bernoulli(1/2)**. Because the model is the **full** 2-shift, its
MME *is* the uniform Bernoulli measure, which gives `P(odd)=1/2`.

> **`[PROVEN]` The proof's target invariant measure is Haar on `ℤ₂` = the MME of the full 2-shift, and
> parity = 1/2 under it.** The MME and Haar **coincide** for the relevant system (full shift), so the
> "is parity 1/2 under the natural/MME measure?" question is answered **YES, with no tension**. The
> β-transformation's Parry measure (parity `≈0.20`) is a *different system's* MME and is **not** the relevant
> object — confirming the prompt's caution but resolving it: the danger only arises from the conflation.

**Numerics (`inv_measures.py`):**
- (I) β-map a.c.i.m. digit-1 frequency (long orbit) `= 0.19935`; **exact Parry-measure formula `P(digit=1) = 0.19945`** (Gel'fond–Parry density via the orbit of `1`). `≠ 1/2`.
- (II) Antihydra parity under Haar (40 random large starts, `N=2·10⁴`) `= 0.50031`. `= 1/2`.

---

## 2. Intrinsic ergodicity / unique-MME angle — does NOT select the orbit `[PROVEN: no; reduces to (5)]`

**Unique MME exists for both systems** `[standard]`:
- Full 2-shift: unique MME = Bernoulli(1/2) (Parry 1964; Bowen — mixing SFTs are intrinsically ergodic).
- β-shift `β=3/2`: unique MME = Parry measure (**Hofbauer–Walters**); intrinsic ergodicity extends to all
  factors of β-shifts (**Climenhaga–Thompson 2012**, *Israel J. Math.*, "Intrinsic ergodicity beyond
  specification: β-shifts, S-gap shifts, and their factors").

**But intrinsic ergodicity is the WRONG kind of theorem to select a specific orbit.** It asserts
*uniqueness of the MME among measures*; it says nothing about *which individual orbits are generic for it*.
The decisive fact:

> **`[PROVEN — Barreira–Schmeling 2000, Israel J. Math.]` In subshifts with specification (incl. the full
> shift), the set of points that are NOT generic for any measure (Birkhoff averages divergent) — and a
> fortiori the set generic for a *non-MME* invariant measure — has FULL topological entropy and FULL
> Hausdorff dimension.** So even with a unique MME, a positive-entropy / full-dimension set of orbits fails
> to be MME-generic. A unique-MME theorem cannot conclude that the *particular* orbit `c₀=8` is generic.

**Does full subword complexity `2^k` (WALLB_EFFECTIVE) interact with intrinsic ergodicity to force
genericity?** **No `[PROVEN: no]`.** Full complexity says the orbit's *language* is the full shift
(its orbit-closure carries entropy `log 2`, equal to `h_top`). A theorem of the form "if the orbit closure
has maximal entropy then the orbit is MME-generic" is **false** — the orbit closure can have full entropy
while the orbit itself is generic for a low-entropy measure, or for none (Barreira–Schmeling). Full
complexity is a property of the *support* of the empirical measures' limit set, not of *which* measure they
converge to. The variational principle (`h_top = sup h_μ`) is attained by the *measure* MME, not by a
designated orbit.

> **`[PROVEN]` Full complexity + intrinsic ergodicity does NOT force the orbit to be MME-generic.** Forcing
> it is *exactly* single-orbit equidistribution = line (5) of `PROOF_STATUS.md`. This is the same
> a.e.-vs-specific (Tao) wall, now in measure-theoretic dress: the MME is a.e.-attracting (it is, in fact,
> attracting only on a Haar-full set, which is what equidistribution would place the orbit in), while a
> full-dimension exceptional set escapes it.

---

## 3. Structure of the BIASED invariant measures — and why complexity does not exclude them `[PROVEN structure; exclusion = (A)]`

The full 2-shift `{0,1}^ℕ` carries a huge simplex of `T`-invariant measures. Those with `ν(odd) ≠ 1/2`
(biased parity) are exactly:

| family | description | parity | support | entropy | generic-set dim |
|---|---|---|---|---|---|
| `Bernoulli(p)`, `p≠1/2` | i.i.d. parities, bias `p` | `p ≠ 1/2` | **full** shift | `H(p) < log 2` | `H(p)/log2 < 1` |
| Markov (irreducible, full-support) | finite-memory, stationary `π` with `π(odd)≠1/2` | `≠1/2` | **full** shift | `< log 2` | `< 1` |
| periodic-orbit measures | uniform on a `T`-cycle, e.g. `(001)^∞` | rational `≠1/2` | finite | `0` | `0` |
| measures on proper subshifts (e.g. β-shift image) | supported on a `<`-full subshift | typ. `≠1/2` | proper subshift | `≤ log(3/2)` | `< 1` |
| non-ergodic mixtures | convex combos of the above | `≠1/2` | varies | varies | varies |

**Key structural facts `[PROVEN/standard]`:**
1. Every **ergodic** biased measure has `h_μ < log 2` (strict): equality `h_μ = log 2` forces `μ = `
   Bernoulli(1/2) by **uniqueness of the MME** (§2). So *biased ⟹ sub-maximal entropy*, **always**.
2. The set of `μ`-generic points has **Hausdorff dimension `h_μ / log 2 < 1`** (Bowen/Billingsley dimension
   formula for the full shift). So biased measures' **generic sets are positive-codimension** — *but their
   topological **support** can be the full shift* (`Bernoulli(p)`, full-support Markov).

**The trap the prompt hopes to avoid — "full complexity ⟹ not generic for any biased measure" — is FALSE.**
`[PROVEN: counterexample]` A `Bernoulli(p)`-generic sequence (`p≠1/2`) has **full subword complexity `2^k`**
(every word has positive probability `p^j(1−p)^{k−j}>0`, hence appears a.s. — complexity `→ 2^k`) yet
**biased parity `p`**. Numerics (`inv_measures.py`, `N=2·10⁶`):

```
  Bernoulli(p=0.50): parity=0.4995, complexity 2^k full for k≤12 (4096/4096)
  Bernoulli(p=0.35): parity=0.3497, complexity 2^k full for k≤12 (4093/4096; 3 rarest words just unsampled)
  Bernoulli(p=0.20): parity=0.2001, complexity 2^k full asymptotically (3240/4096 at N=2e6; rare all-1 words
                     need ~5^12 length — undercount is finite-sample, NOT a complexity deficit)
```

> **`[PROVEN]` Full subword complexity `2^k` does NOT exclude biased invariant measures.** Complexity is a
> **support/topological** statement (the orbit's language is the full shift); genericity for a measure is a
> **frequency** statement (which weights the empirical measures converge to). They are **independent**: a
> full-support biased measure is generic on a full-support, positive-codimension set whose language is the
> whole full shift. This is the **same support-vs-frequency gap** that recurs throughout the kernel
> (`WALLB_EFFECTIVE` §3: FLP's `1/3` is support not frequency; `EFFECTIVE_TOPDIGIT`: top digits are support).

**What CAN be said rigorously, and where it stops:**
- `[PROVEN]` **Every biased invariant measure is sub-maximal-entropy** (`h_μ<log 2`), with **generic set of
  Hausdorff dim `<1`** (positive codimension). The biased measures are "thin" in the dimension sense.
- `[PROVEN]` **Periodic / finite-support / proper-subshift biased measures are already excluded** by the
  arithmetic of `WALLB_NONATOMIC.md` §2 (the orbit's itinerary is not eventually periodic; growth past all
  cycle points). That removes the `h_μ=0` and proper-subshift rows for *eventually-structured* itineraries.
- `[REDUCES TO (A)]` **The remaining biased measures (full-support `Bernoulli(p)`/`Markov`, `p≠1/2`,
  aperiodic generic points) are NOT excluded by complexity.** Excluding them = showing the orbit's empirical
  measures do not accumulate at any such `ν` = the orbit is generic for Haar = **equidistribution mod `2^k`**
  = line (5) = wall (A). The positive-codimension fact does **not** help: the orbit is a single specified
  point, and "a Haar-null / lower-dimension exceptional set" is exactly the set a specified point could
  inhabit (it is the same null set as in (A); `WALL_B_EXCEPTIONAL_SET` shows it is full-dimension and
  uncharacterized for `b=3/2`).

> **`[PROVEN]` Net of §3.** "Full complexity ⟹ not generic for any biased measure" **does not hold**. The
> biased invariant measures are all sub-maximal-entropy with positive-codimension generic sets, and the
> *structured* ones (periodic/subshift) are killed arithmetically — but the *full-support aperiodic* ones
> are excluded **only by equidistribution**. So the invariant-measure route **reduces to (A)** on its
> residual piece, exactly matching the `WALLB_NONATOMIC` trichotomy (structured = `[PROVEN]` out; aperiodic
> = Mahler), now re-derived from the measure simplex instead of the valuation budget.

---

## 4. Numerics summary (`scratchpad/inv_measures.py`, `.venv`)

| object | measured | meaning |
|---|---|---|
| (I) β-map a.c.i.m. `P(digit=1)`, long orbit | `0.19935` | β-shift Parry parity ≠ 1/2 (WRONG system; the trap) |
| (I) β-map Parry `P(digit=1)`, exact formula | `0.19945` | confirms ≠ 1/2 analytically |
| (II) Antihydra parity under Haar, 40 starts | `0.50031` | MME=Haar of full shift gives parity = 1/2 ✓ |
| (III) `Bernoulli(0.35)` parity / complexity | `0.3497` / full `2^k` | full complexity coexists with bias |
| (III) `Bernoulli(0.20)` parity / complexity | `0.2001` / full (asympt.) | ditto; undercount = finite-sample only |
| dim of `Bernoulli(p)`-generic set `=H(p)/log2` | `1, .971, .881, .722, .469` for `p=.5,.4,.3,.2,.1` | biased generic sets have positive codimension |

---

## 5. Verdict (answers to the three return questions)

1. **Is parity = 1/2 under the relevant invariant measure, and which measure?** **YES `[PROVEN/standard]`.**
   The relevant measure is **Haar on `ℤ₂`**, which is the **measure of maximal entropy of the FULL 2-shift**
   (the 2-adic `×3/2` map's symbolic model). Parity = 1/2 under it, exactly; MME and Haar **coincide** here.
   The `β=3/2` *interval* β-transformation is a *different* system whose Parry measure gives parity `≈0.1995 ≠ 1/2`
   — that is the conflation trap, not the relevant measure. **No problem with the target measure.**

2. **Does intrinsic ergodicity + full complexity exclude biased measures, or reduce to equidistribution?**
   **It REDUCES to equidistribution `[PROVEN: no exclusion]`.** Both systems have a unique MME (Parry/Bowen;
   Hofbauer–Walters; Climenhaga–Thompson), but **uniqueness of the MME does not select a specific orbit** —
   the non-MME-generic set has **full entropy and full Hausdorff dimension** (Barreira–Schmeling). **Full
   subword complexity `2^k` does NOT force MME-genericity**: complexity is *support* (topological), genericity
   is *frequency* (measure); they are independent (explicit `Bernoulli(p)` counterexample). Forcing the orbit
   to be MME-generic is *exactly* single-orbit equidistribution = line (5) = wall (A).

3. **Structure of the biased invariant measures.** Full-shift simplex; biased = `ν(odd)≠1/2`. Every
   ergodic biased measure has **sub-maximal entropy** `h_μ<log 2` (by MME uniqueness) and **generic set of
   Hausdorff dimension `h_μ/log2 < 1` (positive codimension)** — yet a full-support biased measure
   (`Bernoulli(p)`/Markov) has the **full shift as topological support and full subword complexity `2^k`**.
   The **structured** biased measures (periodic-orbit, proper-subshift, eventually-periodic itinerary) are
   `[PROVEN]` excluded arithmetically (`WALLB_NONATOMIC` §2: orbit not eventually periodic, grows past all
   cycle points). The **full-support aperiodic** biased measures are excluded **only by equidistribution**
   = wall (A).

### Bankable conclusions (0 false proofs)
- `[PROVEN/standard]` **Relevant measure = Haar = MME of the full 2-shift; parity = 1/2 under it.** The
  β-transformation Parry measure (parity ≈0.20) is a different system's MME and is the conflation trap, now
  explicitly identified and excluded.
- `[PROVEN]` **Intrinsic ergodicity / unique-MME does NOT select the specific orbit** (non-generic set has
  full entropy + full dimension, Barreira–Schmeling); **full complexity `2^k` does NOT exclude biased
  measures** (support ≠ frequency; `Bernoulli(p)` counterexample). The invariant-measure route is *not* a
  shortcut.
- `[PROVEN/structure]` Biased invariant measures = sub-maximal-entropy, positive-codimension generic sets;
  **structured ones killed arithmetically, full-support aperiodic ones reduce to (A)**. This **independently
  re-derives the `WALLB_NONATOMIC` trichotomy from the measure simplex** (a second, conceptually distinct
  proof of the same split), strengthening confidence in it.

### Live next angle
The residual is unchanged in *content* (full-support aperiodic biased measures = Mahler) but is now
sharpened: it is precisely **"the orbit's empirical measures do not accumulate at any sub-maximal-entropy
full-support `ν`."** Since every such `ν` has `h_ν<log 2`, a conceivable attack is an **entropy/pressure
lower bound on the orbit's empirical measures** (show any weak-* limit has entropy `=log 2`, forcing it to be
the MME by uniqueness). That would be a *quantitative-entropy* route to genericity — but producing a
positive-entropy lower bound for a single specified orbit is itself an effective-equidistribution statement,
so it is expected to terminate at line (5) again. Worth scoping whether a partial entropy bound (e.g.
`h_limit ≥ log(3/2)` from FLP-type support) is extractable as a *partial* result.

### Sources
- Hofbauer–Walters; **Climenhaga–Thompson**, "Intrinsic ergodicity beyond specification: β-shifts, S-gap
  shifts, and their factors", *Israel J. Math.* 192 (2012), https://link.springer.com/article/10.1007/s11856-012-0052-x
- **Barreira–Schmeling**, "Sets of 'non-typical' points have full topological entropy and full Hausdorff
  dimension", *Israel J. Math.* 116 (2000), https://link.springer.com/article/10.1007/BF02773211
- Parry, "On the β-expansions of real numbers" (1960); Bowen, intrinsic ergodicity of SFTs with specification.
- Gel'fond–Parry invariant density for β-transformations (used for the exact Parry-parity formula).
