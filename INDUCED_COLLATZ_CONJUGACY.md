# Importing the Collatz / Lagarias 2-adic conjugacy framework into the induced odd map (2026-06-28)

*Angle: take the GAP-LEMMA reduction (`WALLB_VALUATION_SHARP.md`) — the entire aperiodic wall = the law of
`D = v2(3o−1)` along the INDUCED ODD MAP `o' = 3^{D−1}(3o−1)/2^D` — and confront it with the classical
Collatz 2-adic conjugacy machinery (Lagarias parity-vector map `Q_∞`, Bernstein–Lagarias conjugacy map,
Matthews–Watts ergodicity, Terras/Everett parity-vector density). Goal: pin down whether the conjugacy is
explicit enough to constrain OUR specific orbit, and whether it yields any ONE-SIDED bound. Numerics `.venv`
only, exact big-int. Zero false proofs. NOT committed.*

---

## 0. One-line answer

The conjugacy framework **applies in kind** (the parity/`D` sequence equidistributes for Haar-a.e. 2-adic
point — `[PROVEN/standard]`) but **the a.e.-vs-specific wall reappears verbatim inside the conjugacy**: the
conjugating map `Q_∞` is *explicit and exactly computable mod `2^k`* (Terras bijection) — so we can compute
any finite prefix of `Q_∞(o_0)` — but it is **non-constructive for the infinite object**: "`Q_∞(o_0)` is
Haar-generic/normal" is *literally identical* to our equidistribution target, with no closed form to certify
it. The conjugacy gives **no one-sided inequality** for a single orbit. The genuine new gain is **not** from
the conjugacy but from the GAP-LEMMA arithmetic: it reduces the proof target from full equidistribution to a
**one-sided lower bound on finitely many low cylinder frequencies** (mod 4 and mod 8). `[PROVEN reduction]`

---

## 1. Identifying the induced map as a known accelerated 3x±1 map `[PROVEN/standard]`

Induced odd map (GAP LEMMA, `WALLB_VALUATION_SHARP.md` §1):
```
o' = 3^{D−1} (3o−1)/2^D ,   D = v2(3o−1) ≥ 1.
```
- The factor **`(3o−1)/2^D`** is exactly the **accelerated "3x−1" Syracuse map** `o ↦ odd-part(3o−1)`.
- The extra factor **`3^{D−1}`** is the multiplicative residue of the `D−1` intervening EVEN steps of the base
  Antihydra map `c ↦ ⌊3c/2⌋` (each even step is `×3/2`, contributing one factor 3 and one halving). So the
  induced map is **not** the pure Syracuse map; it is the Syracuse-`3x−1` map **dressed with the even-run
  growth `3^{D−1}`**. Per return it multiplies magnitude by `≈ (3/2)^D` (verified numerically, §4: mean
  log-growth `1.168 bits/step = E[D]·log₂(3/2)`).
- This places it inside the **"generalized 3x+1 / relatively-prime-type" family** of Matthews–Watts. Crucially,
  the extra `3^{D−1}` is a *unit factor 2-adically* (3 is a 2-adic unit), so it **does not change the
  `v2`-statistics question** — the law of `D = v2(3o−1)` is governed by `o mod 2^k`, exactly as for the
  base 2-adic dynamics. (`WALLB_INVARIANT_MEASURES.md` D1 already identified the base map `T(c)=⌊3c/2⌋ on ℤ₂`
  with the full 2-shift via itinerary coding; the `D`-sequence here is the run-length encoding of that shift.)

---

## 2. The exact Lagarias 2-adic conjugacy `[PROVEN/standard, citations]`

**Parity-vector map (Everett 1977; Terras 1976; named & developed by Lagarias 1985).** For the 3x+1 map on
`ℤ₂`, `T(x) = (3x+1)/2` (x odd), `T(x) = x/2` (x even), define
```
Q_∞ : ℤ₂ → ℤ₂ ,   Q_∞(x) = Σ_{k≥0} t_k 2^k ,   t_k = T^k(x) mod 2.
```
i.e. `Q_∞(x)` is the 2-adic integer whose binary digits are the **parity sequence** of the orbit of `x`.

**Theorem (Lagarias 1985; Bernstein–Lagarias 1996).** `Q_∞` is a **measure-preserving homeomorphism** of
`ℤ₂` (a continuous bijection preserving Haar measure), and it **conjugates `T` to the 2-adic shift** `S`
(`S(x)=x/2` if even, `(x−1)/2` if odd):
```
Q_∞ ∘ T = S ∘ Q_∞.
```
The inverse `Φ = Q_∞^{-1}` is the **Bernstein–Lagarias "3x+1 conjugacy map"** (Canad. J. Math. 48 (1996)
1154–1169): the unique homeomorphism of `ℤ₂` with `Φ(0)=0` conjugating `T` to the shift; it is *solenoidal*
(induces a well-defined map mod `2^n` for every `n`).

**Ergodic strengthening (Matthews–Watts 1984; Matthews "Generalized 3x+1 Mappings").** The unique continuous
2-adic extension of `T` (and of the whole relatively-prime-type family, including the `5x+1` and the `×3/2`
Antihydra-type maps) is **measure-preserving and ergodic — in fact strongly mixing / Bernoulli — for Haar
measure** on `ℤ₂`.

**Consequence we want.** Conjugacy to the shift `S` (which is the one-sided Bernoulli(1/2) shift) means: for
**Haar-almost-every** `x ∈ ℤ₂`, the parity sequence `(t_k)` is an i.i.d. fair coin, hence equidistributed;
equivalently `Q_∞(x)` is **Haar-generic (2-adically normal)** for a.e. `x`. In our run-length encoding this is
exactly **`P(D=k) = 2^{−k}` (geometric, mean 2)** for a.e. starting odd `o`. `[PROVEN/standard for a.e.]`

Sources: Bernstein–Lagarias, *The 3x+1 Conjugacy Map*, Canad. J. Math. 48 (1996) 1154–1169
(https://cr.yp.to/papers/3x1conjmap-19960215-retypeset20220326.pdf); Lagarias, *The 3x+1 Problem and its
Generalizations*, Amer. Math. Monthly 92 (1985) 3–23; Lagarias (ed.), *The 3x+1 Problem: An Overview*
(https://arxiv.org/pdf/2111.02635); Matthews, *Generalized 3x+1 Mappings: Markov Chains and Ergodic Theory*
(http://www.numbertheory.org/PDFS/matthews-final-revised.pdf); Terras, *A stopping time problem on the
positive integers* (1976); Everett (1977).

---

## 3. Is `Q_∞` explicit enough to constrain OUR specific `o_0`?  `[the a.e.-vs-specific wall, INSIDE the conjugacy]`

**The FINITE conjugacy is exact and explicit (Terras bijection).** `Q_∞` is *solenoidal*: the first `k`
parities depend **only on `x mod 2^k`**, and the map
```
ℤ/2^k → {0,1}^k ,   (x mod 2^k) ↦ (t_0,…,t_{k−1})
```
is a **bijection** (Terras 1976 / Everett). Hence each length-`k` parity vector has density exactly `2^{−k}`,
and **`Q_∞ mod 2^k` is an explicitly computable permutation of `ℤ/2^k`**. So for our specific `o_0` we can
compute **any finite prefix** of `Q_∞(o_0)` exactly (this is literally what §4 does).

**The INFINITE object is non-constructive for a specific point.** The measure-preserving / ergodic statement
is `[a.e. x]`. For our **specific computable 2-adic integer `o_0`** (the odd part near `c_0=8`, `o_0=27`):
- There is **no closed form** for `Q_∞(o_0)`; only its finite prefixes are computable.
- "The parity/`D` sequence of `o_0` equidistributes" `⇔` "`Q_∞(o_0)` is 2-adically normal" — and proving
  **normality of one explicitly constructed 2-adic integer** is exactly the kind of statement no general
  method reaches. The conjugacy **translates** our problem to "is this specific point generic for the shift?"
  but **does not solve it**: the a.e.-vs-specific gap is *preserved* by the (measure-preserving) conjugacy, not
  closed by it.

**Verdict.** `Q_∞` is **explicit enough to TEST/COMPUTE** (every finite cylinder of `Q_∞(o_0)` is exact) but
**NOT explicit enough to PROVE genericity at `o_0`**. The conjugacy is a faithful change of coordinates that
relocates the wall without lowering it — the *same* single-point-vs-a.e. obstruction reappears as
"normality of `Q_∞(o_0)`". `[PROVEN: the obstruction transfers; no breach]`

---

## 4. One-sided information `[conjugacy gives NONE; GAP-LEMMA arithmetic gives a real reduction]`

### 4a. The conjugacy / classical density theorems give no single-orbit one-sided bound `[OBSERVED/standard]`
- The conjugacy is **qualitative (a.e.)** — measure-preserving + ergodic says nothing one-sided about one orbit.
- Terras/Everett: the set of integers with finite stopping time has **density 1**, and the parity-vector
  density is exactly `2^{−k}` — but these are statements about **density over ALL integers (= Haar)**, not the
  frequency along a **single** induced orbit. They do **not** bound our single-orbit cylinder frequencies.

### 4b. The GAP-LEMMA one-sided reduction (OUR gain, conjugacy-independent) `[PROVEN reduction]`
We need only `mean D ≥ 3/2` (`⇔` even-density `≥ 1/3` via the renewal identity `p_odd·E[D]=1`), **not**
`mean D = 2`. Using `E[D] = Σ_{k≥1} P(D≥k)` (D is a positive integer):
```
E[D] = 1 + P(D≥2) + P(D≥3) + …  ≥  1 + freq(o ≡ 3 mod 4).
```
**Exact mod-4 dictionary** (3 is a unit mod 4; `3·1≡3`, `3·3≡1`):
```
D = 1  ⇔  3o−1 ≡ 2 (mod 4)  ⇔  o ≡ 1 (mod 4)
D ≥ 2  ⇔  3o−1 ≡ 0 (mod 4)  ⇔  o ≡ 3 (mod 4).
```
So a **single one-sided low-cylinder bound suffices**:
```
freq(o ≡ 3 mod 4) ≥ 1/2   ⟹   E[D] ≥ 3/2.        (★)
```
This is a *one-sided*, *single-cylinder* (mod 4) target — vastly smaller than full equidistribution.

**Honest sharpness caveat.** At Haar `freq(o≡3 mod4)=1/2` **exactly**, so the two-term bound `1 + freq(o≡3
mod4)` lands **right at `3/2` with ZERO margin** (numerically `1.4997 < 1.5`, §4c). To clear `3/2` *robustly*
one must keep the next term:
```
E[D] ≥ 1 + freq(o ≡ 3 mod 4) + freq(D ≥ 3),     freq(D≥3) = freq(3o−1 ≡ 0 mod 8 …) — a mod-8 cylinder.
```
Haar values: `1 + 1/2 + 1/4 = 7/4`, clearing `3/2` with **margin `1/4`**. So the minimal robust target is a
**one-sided lower bound on the frequency of TWO low cylinders (mod 4 and mod 8)**, namely
`freq(D≥2) + freq(D≥3) ≥ 1/2`, with Haar margin `1/4`.

**Status of this target.** Still a single-orbit cylinder-frequency statement (a *weak, one-sided, finite*
equidistribution claim), hence still **not arithmetically forced** — but it is a strictly smaller object than
"full equidistribution mod `2^k` for all `k`". This is the live, honest localization. `[REDUCES TO weak
one-sided cylinder equidistribution — a proper sub-target of (A)]`

### 4c. Numerics (`scratchpad/induced.py`, exact big-int, `o_0 = 27` from `c_0 = 8`, `N = 2·10^5`) `[OBSERVED]`
| quantity | measured | Haar |
|---|---|---|
| `mean D` | **1.99627** | 2 |
| `freq(D=1) = freq(o≡1 mod4)` | **0.50034** | 0.5 |
| `freq(D≥2) = freq(o≡3 mod4)` | **0.49966** | 0.5 |
| `freq(D≥3)` | **0.24888** | 0.25 |
| `P(D=k)/2^{−k}`, `k=1..9` | `∈ [0.97, 1.03]` | 1 |
| `freq(D≥k)/2^{1−k}`, `k=1..8` | `∈ [0.987, 1.001]` | 1 |
| lag-1 autocorr(`D`) | **−0.0062** (≈0) | 0 (i.i.d.) |
| mean log₂-growth / step | 1.168 (`= E[D]·log₂(3/2)`) | 1.17 |

- One-sided bound (★) two-term: `1 + freq(o≡3 mod4) = 1.4997` — **just below `3/2`** (zero Haar margin, as
  predicted). Three-term: `1 + 0.49966 + 0.24888 = 1.7485 ≥ 3/2` — clears by **0.248** (≈ Haar margin `1/4`).
  ⇒ confirms: **need ≥ 2 cylinders** (mod 4 AND mod 8) for a robust one-sided proof.
- `D`-sequence is empirically **i.i.d.-geometric** (geometric law to 2–3 dp through `k≈9`; zero lag
  correlation), consistent with `Q_∞(o_0)` being 2-adically normal — exactly the a.e. conjugacy prediction,
  exactly the unprovable-for-a-specific-point object.

(Finite `N` proves nothing about the limit; the tail `k≥10` shows the expected finite-sample ratio drift.)

---

## 5. Verdict

| question | answer | label |
|---|---|---|
| Is the induced map a known map? | Syracuse `3x−1` map dressed with the even-run growth `3^{D−1}`; in the Matthews–Watts generalized family; `v2`-statistics identical to the base 2-shift. | `[PROVEN/standard]` |
| Exact Lagarias conjugacy? | `Q_∞(x)=Σ t_k 2^k`, `t_k=T^k(x) mod 2`; `Q_∞` is a measure-preserving homeomorphism of `ℤ₂` with `Q_∞∘T = S∘Q_∞`; `T` ergodic/Bernoulli for Haar ⇒ parity/`D` equidistributes for a.e. start. | `[PROVEN/standard]` |
| Is `Q_∞` explicit enough to constrain our `o_0`? | **Finite part yes, infinite part no.** `Q_∞ mod 2^k` is an explicit bijection (Terras) ⇒ every finite prefix of `Q_∞(o_0)` is computable; but no closed form, and "`Q_∞(o_0)` normal" = our target. **The a.e.-vs-specific wall reappears INSIDE the conjugacy.** | `[PROVEN: obstruction transfers]` |
| Any one-sided consequence from the conjugacy / Terras-Everett? | **No** for a single orbit (a.e. and all-integer-density statements only). | `[OBSERVED/standard]` |
| One-sided arithmetic from the GAP LEMMA? | `E[D] ≥ 1 + freq(o≡3 mod4)`; `D=1 ⇔ o≡1 mod4`. Sufficient: `freq(o≡3 mod4) ≥ 1/2`. But two-term bound is Haar-tight (zero margin); robust target = `freq(D≥2)+freq(D≥3) ≥ 1/2` (mod 4 & mod 8, Haar margin `1/4`). | `[PROVEN reduction]` |
| Numerics | `mean D=1.996`, `freq(o≡1 mod4)=0.5003`, geometric law, autocorr≈0; two-term one-sided bound `=1.4997` (fails), three-term `=1.7485` (clears). | `[OBSERVED]` |

### Net (bankable)
1. **`[PROVEN/standard]`** The Lagarias `Q_∞` conjugacy and Matthews–Watts ergodicity give the a.e.
   equidistribution of the `D`-sequence; the induced map sits squarely in that framework.
2. **`[PROVEN]`** `Q_∞` is *explicit mod `2^k`* (Terras bijection) but *non-constructive for the infinite
   value*: the specific-point genericity of `Q_∞(o_0)` is **identical** to our wall. The conjugacy relocates
   the wall (parity equidistribution ↦ 2-adic normality of one constructed point) **without lowering it**.
3. **`[PROVEN reduction — NEW, conjugacy-independent]`** The target drops from full equidistribution to a
   **one-sided lower bound on two low cylinder frequencies** (mod 4 & mod 8): `freq(D≥2)+freq(D≥3) ≥ 1/2`,
   Haar margin `1/4`. Strictly smaller object than (A), still a (weak, one-sided, finite) single-orbit
   cylinder-frequency statement.

### Live next angle
The robust one-sided target is now concrete and *finite-cylinder*: prove `freq_{orbit}(o≡3 mod4) +
freq_{orbit}(o≡3 mod8-type) ≥ 1/2`. Two un-mined handles: (i) a **mod-8 transfer/return inequality** —
does the induced map's action on `ℤ/8` admit a one-sided drift (a sub-stochastic comparison forcing the joint
mod-4/mod-8 occupation above `1/2`) without full equidistribution? (ii) The GAP-LEMMA extremal
self-correction (`o≡3^{-1} mod 2^K ⇒ D_1=1`, `WALLB_VALUATION_SHARP.md` §3) is a one-sided arithmetic fact
at the *deep* cylinders — can it be combined with (★) (which only needs the *shallow* mod-4 cylinder) into a
two-sided squeeze on the mod-4 frequency? Both stay strictly below "full equidistribution".
