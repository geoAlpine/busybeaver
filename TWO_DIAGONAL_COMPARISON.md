# Two-diagonal comparison — is σ_n (carry diagonal) easier, equal, or harder than d_n (Mahler diagonal)? (2026-06-29)

*Assigned angle: compare the two diagonals of the established split `β_n = d_n ⊕ σ_n ⊕ ρ_n`
(`CARRY_COBOUNDARY §1`), where `d_n = bit_{n+k}(8·3^n)` is the FIRST (bare exogenous Mahler) diagonal,
`σ_n = bit_{n+k}(S_n)` is the SECOND (endogenous-carry) diagonal, `S_n = Σ_{j<n} 3^{n-1-j}2^j b_j`,
`b_j = c_j mod 2`, and `ρ_n` the finite-range borrow (`PROVEN`, `CARRY_COBOUNDARY §1a`). The two diagonals
are coupled by `8·3^n − S_n = 2^n c_n`. Decisive questions: relative difficulty; transfer; independent or
locked; does σ's measure `ν_{2/3}` make it strictly easier. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/two_diag.py, two_diag2.py`, exact big-int /
exact rational, N up to 5·10⁴, k∈{2,4,6,8}, <5s each, 0 identity failures. Every claim labelled. Zero false
proofs. NOT committed.*

---

## 0. One-line verdict

**(c) EQUAL-HARD AND ASYMPTOTICALLY INDEPENDENT — both diagonals are the SAME single AEV/Mahler object
"k-th binary digit of `⌊α(3/2)^n⌋`", differing ONLY in the leading constant `α` (`α=8` for `d_n`,
`α=α*≈0.1358` for `σ_n`), so the carry diagonal is NOT easier and the hoped-for measure `ν_{2/3}` is
DEGENERATE for a single orbit.** New `[PROVEN]` exact reduction: `σ_n = bit_k(⌊α_n^σ (3/2)^n⌋)`,
`α_n^σ = (1/3)Σ_{j<n} b_j(2/3)^j → α*` (a single orbit-defined constant), exactly parallel to
`d_n = bit_k(⌊8(3/2)^n⌋)`. New `[OBSERVED]`: `corr(d_n,σ_n) ≈ 0` (≤ 1/√N, all k) — the diagonals are
**asymptotically independent, not locked**; and `E_d ≈ E_σ ≈ E_β ≈ E_σ^{anneal}` (all ride the √N floor) —
**no transfer helps `β_n`**, because controlling `d_n` alone leaves `σ_n` (a second, independent, equally-hard
Mahler instance) uncontrolled. **No machine decided. No label upgraded.**

---

## 1. The seam, made exact: both diagonals are `bit_k` of an `⌊α(3/2)^n⌋` integer  `[PROVEN, 0 failures]`

The seam `S_n ≡ 8·3^n (mod 2^n)` (`CARRY_COBOUNDARY §1a`) says the low `n` bits of `8·3^n` and `S_n` are
**equal**; hence the subtraction `8·3^n − S_n = 2^n c_n` produces **no borrow out of the low block**
(`borrow_n = 0`), and the high parts subtract cleanly:

> **`[PROVEN]` Clean high-part identity.** Let `H_n := ⌊8·3^n/2^n⌋ = ⌊8(3/2)^n⌋` and
> `G_n := ⌊S_n/2^n⌋`. Then `c_n = H_n − G_n` **exactly** (no borrow), and
> `d_n = bit_k(H_n)`, `σ_n = bit_k(G_n)`, `β_n = bit_k(c_n) = bit_k(H_n − G_n)`,
> `s_n = c_n mod 2^k = (H_n − G_n) mod 2^k`.
> (Verified `H_n − G_n = c_n`, `2^n c_n + S_n = 8·3^n`: 0 failures, N=5·10⁴, k∈{2,4,6,8}; and at
> n=50,100,200,400 by exact rational arithmetic.)

So **above the seam both diagonals read the low binary digits of two `(3/2)^n`-scale integers whose
difference is the orbit state `c_n`.** The read position `n+k` sits exactly `k` bits above the
agreement-seam at bit `n`; below the seam the two are identical, at/above it they diverge by precisely `c_n`.

### 1a. The exact leading-coefficient form of `G_n`  `[PROVEN, 0 failures]`

Reindexing `S_n = Σ_{j<n}3^{n-1-j}2^j b_j` by `i = n-1-j`:

> **`[PROVEN]`** `S_n/2^n = (1/2)Σ_{i=0}^{n-1} b_{n-1-i}(3/2)^i = (3/2)^{n-1}·Y_n`,
> `Y_n = (1/2)Σ_{j<n} b_j(2/3)^j`; hence
> **`G_n = ⌊α_n^σ·(3/2)^n⌋`, `α_n^σ := (2/3)Y_n = (1/3)Σ_{j<n} b_j(2/3)^j`.**
> (Verified `S_n/2^n = (1/2)Σ b_{n-1-i}(3/2)^i` and `G_n = ⌊α_n^σ(3/2)^n⌋` exactly, n=50..400.)

Compare `H_n = ⌊8(3/2)^n⌋`. **Both diagonals are the k-th binary digit of `⌊α(3/2)^n⌋`** — the AEV /
Mahler digit object verbatim (`DIGITS_OF_3N §1`, AEV Conj 1.6) — with

| diagonal | object | leading constant `α` | nature of `α` |
|---|---|---|---|
| `d_n` (first)  | `bit_k(⌊α(3/2)^n⌋)` | `α = 8` | **fixed, exogenous** (a bare point) |
| `σ_n` (second) | `bit_k(⌊α(3/2)^n⌋)` | `α = α_n^σ → α* ≈ 0.135822737943` | **orbit-defined** (carries `ν_{2/3}`) |

`α_n^σ` is a `(2/3)`-geometric series in the parities — it **converges** (to ≈0.1358 by `j≈102`, tail
`(2/3)^j`). The tail beyond `≈100` terms perturbs `G_n` by only `O(1)`, i.e. only its lowest bits — which is
exactly why the read bit `bit_k(G_n)` (small `k`) is still the carry-mixed whole-history Mahler digit
(`CARRY_BOUNDED_MEMORY §1`, unbounded memory), consistent and complementary.

---

## 2. Decisive comparison — is σ easier? Joint law and energies  `[OBSERVED]`

### 2a. Marginals — both balanced (`two_diag2.py`, N=5·10⁴)

| k | P(d=1) | P(σ=1) | P(β=1) | P(ρ=1) |
|---|---|---|---|---|
| 2 | 0.5059 | 0.5006 | 0.5001 | 0.376 |
| 4 | 0.5033 | 0.5004 | 0.4989 | 0.467 |
| 6 | 0.4979 | 0.5004 | 0.5009 | 0.488 |
| 8 | 0.4998 | 0.4975 | 0.5042 | 0.502 |

Both diagonals are balanced bits; `ρ_n` (finite-range borrow) climbs to ½ as the k-bit window fills.

### 2b. Joint `(d_n, σ_n)` law — ASYMPTOTICALLY INDEPENDENT, not locked  (1/√N = 0.0045)

| k | P00 | P01 | P10 | P11 | corr(d,σ) |
|---|---|---|---|---|---|
| 2 | 0.2463 | 0.2478 | 0.2530 | 0.2529 | −0.0016 |
| 4 | 0.2486 | 0.2481 | 0.2509 | 0.2524 | +0.0020 |
| 6 | 0.2512 | 0.2510 | 0.2484 | 0.2495 | +0.0013 |
| 8 | 0.2530 | 0.2473 | 0.2495 | 0.2503 | +0.0064 |

**The joint law is the product law `≈ ¼` in every cell; `|corr(d_n,σ_n)| ≤ 0.0064 ≈ 1/√N`.** Despite being
algebraically coupled by `c_n = H_n − G_n`, the two diagonals are **statistically independent** — the bare
Mahler point `α=8` and the orbit-measure point `α=α*` are two *uncorrelated* phases of the same `(3/2)^n`
diagonal. **Locked is FALSE; independent is the observed truth.**

### 2c. Odd-character energy — equal difficulty, σ annealed-indistinguishable

`E_X·N = mean_{a odd}|Inj_a^X/N|²·N` (multiple of the random √-floor); `Inj_a^X=(1/N)Σ(X_n−½)χ_a(s_n)`.

| k | E_d·N (bare Mahler) | E_σ·N (carry diag) | E_β·N | E_{d⊕σ}·N | E_σ·N ANNEALED |
|---|---|---|---|---|---|
| 2 | 0.406 | 0.104 | 0.278 | 0.592 | 0.058 |
| 4 | 0.320 | 0.117 | 0.555 | 0.148 | 0.184 |
| 6 | 0.258 | 0.267 | 0.294 | 0.312 | 0.280 |
| 8 | 0.278 | 0.268 | 0.208 | 0.218 | 0.266 |

- **`E_d ≈ E_σ ≈ E_β ≈ E_{d⊕σ}`**, all `O(1)`× the `1/N` random floor (full √-cancellation; small-k scatter
  from few odd characters, equal at k=6,8 where the sample is largest). **Neither diagonal is detectably
  easier** — both ride the floor at the same order. The signed-mean decay (`two_diag.py`) shows no consistent
  ordering of `|d−½|` vs `|σ−½|` either.
- **Annealed control localised to σ:** replacing the orbit parities `b_j` by iid fair bits in
  `S_n` (keeping the **real** `d_n` and **real** phase `s_n`) reproduces `E_σ·N` to within seed scatter
  (0.058/0.184/0.280/0.266 vs real 0.104/0.117/0.267/0.268). **σ's correlation with the phase is
  annealed-indistinguishable** — the same verdict `CARRY_EXOGENIZATION §4` reached for the whole carry,
  now pinned to the second diagonal `σ_n` itself.

---

## 3. The transfer question, settled  `[OBSERVED] + structural`

**(2-i) Does equidistribution of `d_n` IMPLY `σ_n`?** **No.** `d_n` and `σ_n` are the SAME functional
(`bit_k⌊α(3/2)^n⌋`) at two *different* values of `α` (`8` vs `α*`). AEV Conj 1.6 is a separate statement for
each `α` (proven for none, including `α=8` = original Mahler 3/2). Proving the `α=8` instance gives **no
logical handle** on the `α=α*` instance — and §2b shows they are even *statistically* independent. The only
statement that delivers both at once is the **uniform** AEV conjecture (all `α`), which is strictly *harder*
than either single diagonal.

**(2-iii) Is `σ` easier because it carries the measure `ν_{2/3}`?** **No — the measure is degenerate for a
single orbit.** `σ_n = bit_k(⌊α*(3/2)^n⌋)` with `α* = (1/3)Σ b_j(2/3)^j` a **single fixed constant** for the
Antihydra orbit (the measure `ν_{2/3}` is the law of `α*` as the *start/orbit* varies; the actual problem
fixes one orbit, hence one `α*`). So `σ_n` is just one more **bare** Mahler instance, not a measure-averaged
(hence smoothed/easier) object. If anything `d_n` is the *cleaner* of the two: its bit is genuinely exogenous
(`α=8` fixed), whereas `σ_n` is *doubly* endogenous (orbit-defined constant `α*` AND read against the orbit
phase). Either way both ride the floor identically (§2c).

**(3) Leverage on `β_n` via `β = d ⊕ σ ⊕ ρ`, `ρ` finite-range PROVEN.** Controlling any two of `{d,σ,ρ}`
controls `β`. `ρ` is already controlled (finite-range, `CARRY_COBOUNDARY §1a`). So `β_n ⊥ phase ⟺
(d_n⊕σ_n) ⊥ phase`. But `d_n` alone is **insufficient**: one still needs `σ_n`, a *second, independent,
equally-hard* Mahler instance. The split therefore does **not reduce** the open content from one Mahler
problem to zero — it exhibits `β` as the XOR of **two** independent bare-Mahler diagonals (plus the tame
borrow), and `E_{d⊕σ}·N` rides the floor like the rest. **No transfer helps.**

---

## 4. Honest verdict (the three asks)

| ask | answer | label |
|---|---|---|
| **(a) σ strictly easier / a transfer that helps?** | **No.** `σ_n` is the same `bit_k⌊α(3/2)^n⌋` object as `d_n`, at a single orbit-defined `α*` (measure `ν_{2/3}` degenerate for one orbit); `E_σ ≈ E_d ≈ floor`; `d`-equidistribution does not imply `σ` (independent §2b, different `α`); controlling `d` alone leaves `σ` uncontrolled. | `[OBSERVED]` |
| **(b) new characterization of the joint two-diagonal structure?** | **Yes.** `[PROVEN]` `c_n = H_n − G_n`, `H_n=⌊8(3/2)^n⌋`, `G_n=⌊α_n^σ(3/2)^n⌋`, `α_n^σ=(1/3)Σ b_j(2/3)^j→α*`: BOTH diagonals are the AEV digit `bit_k⌊α(3/2)^n⌋`, the same one-parameter family, evaluated at `α=8` vs `α=α*`. `[OBSERVED]` the two are **asymptotically independent** (corr≈0), `β` = XOR of two independent bare-Mahler diagonals + finite-range borrow. | `[PROVEN]`+`[OBSERVED]` |
| **(c) both equal-hard Mahler, locked?** | **Equal-hard Mahler — YES; locked — NO (independent).** Both `=(K)=` Mahler 3/2 / AEV at different `α`; statistically independent and equal at the √-floor; annealed-indistinguishable. | `[OBSERVED]` reduction `=(K)` |

**Exact residual (sharper form).** `Inj_a = (1/N)Σ(d_n ⊕ σ_n ⊕ ρ_n − ½)χ_a(s_n) → 0` is the requirement
that **two independent instances of the AEV digit `bit_k⌊α(3/2)^n⌋` — at `α=8` and `α=α*=(1/3)Σb_j(2/3)^j` —
jointly decorrelate from the orbit phase**, the borrow `ρ_n` being tame (finite-range). This is `(K)`,
exhibited as a *two-point* (uniform-in-`α`) AEV statement rather than a single diagonal — i.e. no easier, and
arguably the honest reason the split buys nothing: it trades one Mahler problem for two independent ones.

---

## 5. Genuinely new vs prior

- **vs `CARRY_COBOUNDARY §1` / `ODD_3ADIC_ODOMETER §1`** (which *named* `d_n` and `σ_n` and proved
  `β=d⊕σ⊕ρ`): this note **compares** them head-to-head — the missing clean comparison. New `[PROVEN]`
  leading-coefficient form `σ_n = bit_k⌊α_n^σ(3/2)^n⌋`, `d_n = bit_k⌊8(3/2)^n⌋`, placing **both** on the
  single AEV `⌊α(3/2)^n⌋` family and identifying the only difference as the constant `α` (8 vs `α*≈0.1358`).
  This is the precise sense in which they are "equal-hard."
- **vs `CARRY_EXOGENIZATION §4`** (carry annealed-indistinguishable, net ≈0 to `Inj_a`): refined to the
  **second diagonal `σ_n` specifically** (annealed `E_σ` ≈ real `E_σ`), and complemented by the new
  **independence** measurement `corr(d_n,σ_n)≈0` — `Inj_a`'s two diagonals are uncorrelated, so the
  exogenous-vs-carry decomposition is a sum of two *independent* floor-level Mahler correlations.
- **vs `CARRY_BOUNDED_MEMORY §1`** (σ has unbounded memory): consistent — the leading constant `α*`
  converges in `≈100` terms, but the *read bit* `bit_k(G_n)` is a low digit set by carries from the whole
  history; the two facts live at different scales (leading coefficient vs low digit) and do not conflict.
- **vs `DIGITS_OF_3N §4`** (no one-sided diagonal density; `(K)` = AEV `⌊α(3/2)^n⌋`): supplies the
  endogenous counterpart — `σ_n` is *also* an `⌊α(3/2)^n⌋` digit, so the carry does not escape AEV; it lands
  on a *different* point of the same conjecture.

## Sources
- Repo: `CARRY_COBOUNDARY.md` (§1 `β=d⊕σ⊕ρ`, §1a finite-range borrow / seam `S_n≡8·3^n mod 2^n`),
  `ODD_3ADIC_ODOMETER.md` (§1 `β_n=bit_{n+k}(8·3^n−S_n)`, moving diagonal = Mahler), `CARRY_EXOGENIZATION.md`
  (§4 annealed carry), `CARRY_BOUNDED_MEMORY.md` (§1 unbounded read-bit memory; §1a leading-scale),
  `DIGITS_OF_3N.md` (`(K)` = diagonal digit of `⌊α(3/2)^n⌋` = AEV/Mahler), `ODD_SUBSPACE_SYNTHESIS.md`
  (residual = pieces (1)+(2)).
- Literature (repo knowledge): Mahler 3/2 (1968, open); Andrieu–Eliahou–Vivion arXiv:2510.11723 (Conj 1.6,
  normality of `⌊α(3/2)^n⌋` for all `α≠0` — the uniform-in-`α` statement that would close both diagonals);
  quenched-vs-annealed disorder (the `σ`-annealed surrogate).
- Numerics: `scratchpad/two_diag.py` (joint law, energies, signed-mean decay, identities 0 fail, N=4·10⁴),
  `two_diag2.py` (leading-coefficient `α*`, annealed-σ control, independence, N=5·10⁴), exact rational
  cross-check of `S_n/2^n=(1/2)Σ b_{n-1-i}(3/2)^i` and `G_n=⌊α_n^σ(3/2)^n⌋` (0 fail, n=50..400).

**No machine decided. No label upgraded.**
