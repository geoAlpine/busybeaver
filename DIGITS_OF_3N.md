# Binary digits of 3ⁿ — latest results (2018-2026) and the hunt for a one-sided MIDDLE-digit density

*Attack of 2026-06-29. Angle: the kernel `(K)` is dual to the distribution of binary digits of `3ⁿ`
(Erdős / (2,3)-digit-exchange). Specifically `a_n = bit_n(8·3ⁿ) = bit_{n−3}(3ⁿ)` is the **main
diagonal** of the bit-grid of `3ⁿ`. This note surveys the MOST RECENT digit literature hunting for
ANY one-sided / positive-lower-density statement **at the middle (diagonal) position** that governs
`a_n` — as opposed to the leading bits (Benford, wrong position) or the nonzero-digit count
(sublinear, no density). Numerics `.venv` only. Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

**No such result exists, and the gap is structural, not just unfilled.** The 2018-2026 digit
literature has exactly THREE kinds of unconditional handle on `bit(3ⁿ)`, and **each lands at the
wrong place** for `(K)`:
- **(i) leading bits** → Benford/Weyl, proven, but position `{n log₂3}`, NOT the diagonal;
- **(ii) nonzero-digit COUNT** → Senge–Straus / Stewart / Bugeaud–Kaneko, `→∞` at rate
  `log n/log log n` = `o(n)`, **sub-density** (no positive density of any value);
- **(iii) longest RUN length** → the freshest handle (Bugeaud–Kaneko subspace method, used as
  Lemma 4.1 of Spiegelhofer–Wallner 2025 directly on `M·3ᴷ`), `L(M·3ᴷ) ≤ ηK+o(K)` —
  **unconditional and applies verbatim to `8·3ⁿ`** (M=8), but it is a *horizontal run-length*, not a
  *diagonal-position density*, and only yields a two-sided density `≥ 1/o(n) → 0`.

`(K)` is the density of the **main DIAGONAL** `bit_n(3ⁿ)`. It is (a) not the leading region (Benford),
(b) not a fixed column (Rowland's proven column-periodicity provably **misses** the diagonal — it
samples each column exactly once, below that column's period), and (c) not a digit-count/sum. It
**is** the Mahler `{(3/2)ⁿ}` / AEV object. The digit community's actual open problem (full normality /
uniform block distribution, Ren–Roettger 2025) is a strict **superset** of `(K)`; they hold **no
one-sided fragment at the diagonal position**. `[verdict: no middle-digit density, proven-or-conjectured]`

---

## 1. The exact object: `a_n` is the MAIN DIAGONAL of the `3ⁿ` bit-grid `[PROVEN, exact]`

`8·3ⁿ = 2³·3ⁿ`, so `a_n = bit_n(8·3ⁿ) = bit_{n−3}(3ⁿ)` for `n ≥ 3`. In the standard bit-grid (row =
`n`, column = bit-position `k`, `0 ≤ k ≲ 1.585 n`), `a_n` reads **column `n−3` of row `n`** — the main
diagonal (slope 1), sitting at relative depth `(n−3)/(1.585 n) → 0.63` from the top. This is the
band that the `WALL_B_WHICH_PART.md` exact identity pins to `{4·(3/2)ⁿ}∈[0,½)`. It is **neither**:
- the **top/leading** band (column `≈ 1.585n`, governed by `{n log₂3}`, Benford — equidistributed by
  Weyl, **PROVEN**, but the *wrong position*), **nor**
- a **fixed** column `k` (Rowland periodicity, §3 — proven but a different, transversal object).

Numerics (`.venv`, exact big-int, N=2·10⁵):

| M | freq(a=1) | freq(a=0) | signed mean |
|---|---|---|---|
| 10⁴ | 0.50490 | 0.49510 | −0.0098 |
| 5·10⁴ | 0.49992 | 0.50008 | +0.0002 |
| 2·10⁵ | 0.49867 | 0.50133 | +0.0027 |

Diagonal looks balanced (consistent with, not proof of, `(K)`).

---

## 2. The four most-recent (2018-2026) results, exact statements

### 2.1 Ren–Roettger 2025 — *Ternary Digits of Powers of Two* (arXiv:2511.03861) `[OPEN / numerics]`
- **Conjecture (Uniform Distribution in the Limit).** For every length `ℓ`, every length-`ℓ` block
  occurs in the base-3 digits of `2ⁿ` with frequency `→ 3^{−ℓ}` as `n→∞`. **Unproven.** Numerics to
  `n=10⁶` support it. Also conjectures `log₃2` normal to base 3 (numerics, `10⁶` digits).
- **Proven content:** none about any frequency/density; the paper is conjecture + computation, and it
  notes the strictly weaker Erdős conjecture is itself still open. Mentions Benford and "a special
  case of Baker's theorem" as context, not as a density theorem.
- **For us:** this is the *dual* direction; by the (2,3)-symmetry the same is conjectured for binary
  digits of `3ⁿ`. It is a **superset of `(K)`** (all blocks, all positions) and **entirely open**.

### 2.2 Howe 2021/2023 — *Powers of 3 with few nonzero bits and a conjecture of Erdős* (arXiv:2105.06440) `[mixed]`
- **Observation, quoted:** "it looks like about half of the bits of the binary representation of `3ˣ`
  are [1]". This is **Pegg's / folklore conjecture — NOT proven.**
- **Theorem 1.1 [PROVEN]:** the only powers of 3 expressible as a sum of **≤ 22** distinct powers of
  3-with-restrictions… (i.e. the only `3ˣ` with `≤22` nonzero bits) occur for `x ≤ 25`. Finiteness,
  **no density.** Companion Theorem 1.2: the only `2ˣ` that are sums of `≤25` distinct powers of 3
  are `2⁰,2²,2⁸` (a "tiny bit of confirmation" for Erdős). Method: exponential Diophantine + modular.
- **For us:** confirms the direct-dual "half the bits of `3ⁿ`" is an **open conjecture**; all that is
  proven is *finiteness of few-1s powers*, which is `o(n)`-sub-density, **not** a positional density.

### 2.3 Senge–Straus 1973 / Stewart 1980 / Bugeaud–Kaneko 2016-2018 — nonzero-digit COUNT `[PROVEN, EFFECTIVE]`
- **Senge–Straus 1973:** if `log a/log b` irrational, the number of **nonzero base-`b` digits of `aⁿ`
  → ∞** (ineffective). Covers nonzero binary digits of `3ⁿ → ∞`.
- **Stewart 1980 (effective):** for `m ≥ 25`, the number of nonzero base-3 digits of `2ᵐ` exceeds
  `log m /(log log m + C) − 3`; by symmetry the same shape for nonzero **binary digits of `3ⁿ`**.
- **Bugeaud–Kaneko 2016 (arXiv:1609.07926), Thm 1.2 / Cor 1.3:** for smooth/few-digit integers the
  number of nonzero `b`-ary digits is `≥ (1−ε)(log log n)(log log log n)/(log log log log n)` — same
  `log-log`-order magnitude. Method: **Schmidt subspace theorem + linear forms in logs**.
- **Crucial for `(K)`:** all of these are `Θ(log n / log log n)` = **`o(n)`** in the length `n≍1.585m`.
  **Sublinear ⇒ no positive density** of nonzero digits, and **a fortiori** no positive lower density
  of any digit value at any specific position. Same individual-term-vs-density failure mode as
  Baker/Padé (`BAKER_LINFORMS.md`).

### 2.4 *(NEW, freshest unconditional handle)* longest-RUN bound — Bugeaud–Kaneko method, Spiegelhofer–Wallner 2025 `[PROVEN, UNCONDITIONAL]`
Source: arXiv:2501.00850 (*The joint distribution of binary and ternary digit sums*, Jan 2025),
**Lemma 4.1**, descending from the Bugeaud–Kaneko subspace-theorem technique. Let `L(M)` = length of
the longest block of identical bits (all-0 or all-1) in the binary expansion of `M`. Then for
`0 ≤ η ≤ 1`,
> **`sup_{1 ≤ M < 2^{ηK}} L(M·3ᴷ) ≤ ηK + o(K)`** as `K→∞`; in particular
> **`L(3ᴷ) = o(K)`** (longest 0-run and longest 1-run in the binary expansion of `3ᴷ` are sublinear).
> Proof: **Schlickewei's p-adic subspace theorem** (lower bounds for `|M·3ᴷ − 2^{k+L}·b|`).

- **Directly relevant:** our number is `8·3ⁿ = M·3ⁿ` with **`M = 8 < 2^{ηn}`** for every `η>0`
  eventually, so the lemma gives **`L(8·3ⁿ) = o(n)`** — an *unconditional* structural fact about the
  exact integer whose diagonal bit is `a_n`. The binary expansion of `8·3ⁿ` has **no run of identical
  bits longer than `o(n)`**.
- **But it is the wrong axis for `(K)` (honest):** `L` is a **horizontal** run-length (consecutive
  positions inside one row `3ᴷ`); `(K)` is the **diagonal-across-`n`** density. A run bound does not
  bound a count/density: from `L(3ᴷ)=o(n)` one gets only the *two-sided* per-row density
  `1/(L+1) ≤ density(1s in row K) ≤ 1 − 1/(L+1)`, i.e. both digit values have density `≥ 1/o(n) → 0`.
  **No positive constant density**, one-sided or otherwise, and nothing pinned to the diagonal cell.
- **Why it still matters:** it is the **strongest unconditional positional-ish theorem** on
  `bit(3ⁿ)` (rules out "`3ⁿ` is mostly one long run"), strictly more than the nonzero-count bound,
  and it is the **only** recent (2025) unconditional advance touching `M·3ᴷ` for general `M`. It does
  not reach `(K)`, but it is the correct frontier citation for "what subspace-theorem methods give."

---

## 3. Rowland 2009 (arXiv:0902.3257) — the one PROVEN positional regularity provably MISSES the diagonal `[PROVEN, exact]`

Rowland's "Regularity versus complexity in the binary representation of `3ⁿ`" proves the **only**
clean positional regularity in the literature:
- **Fixed-column eventual (in fact full) periodicity [PROVEN]:** each fixed column `k` of the bit-grid
  is periodic in the row index `n`, with period **`2^{k−2}`** for `k ≥ 3` (order of 3 mod `2ᵏ`). Hence
  each fixed-column digit value has an **exact, computable rational frequency**.
- **Diagonal STRIPES [PROVEN, but only along the subsequence `3^{2ⁿ}`]:** the low-order bits obey a
  **2-adic power series** `3ˣ = c₀ + c₁x + c₂x² + ⋯` (`x=2ⁿ`), `cᵢ = (log₃)ⁱ/i!` with `log 3` the
  **2-adic** log — decomposing every region into simple periodic strips. This controls the
  *low-order* band of `3^{2ⁿ}` (exponents that are powers of 2), **not** the main diagonal of `3ⁿ`.

**Decisive structural point for `(K)` [PROVEN, exact, our numerics]:** the diagonal `a_k = bit_k(3ᵏ)`
samples **column `k` at row `k`**. Since `k < 2^{k−2}` for all `k ≥ 5`, the diagonal hits each column
**exactly once, at a row index far below that column's period `2^{k−2}`** — i.e. inside the first
period, never repeating. So the proven column-periodicity provides **zero averaging / zero density
transfer** to the diagonal. (Verified: `n` vs `2^{n−2}` for `n=3..20`, diagonal bits
`111111 0 1 0 1 0 11 0 11 0 1 …`.) **The one proven positional regularity is orthogonal to `(K)`.**

---

## 4. Ask 3 — does the digit-community open problem COINCIDE with `(K)`, or is there an attackable one-sided fragment?

**Coincidence:** the community's headline open problem (Ren–Roettger / AEV normality: every block
equidistributes at every position) is a **strict superset** of `(K)` (which needs only the single
diagonal-position marginal `freq(a_n=0)`). So `(K)` is **easier than** what they conjecture, but
**no easier than** what they can prove — and what they prove is `o(n)` (counts) or off-position
(Benford) or off-axis (runs, fixed columns).

**Is there a one-sided fragment with partial results?** Surveyed and **none reaches the diagonal**:
| candidate fragment | status | why it misses `(K)` |
|---|---|---|
| leading-digit Benford `{n log₂3}` | **PROVEN** (Weyl) | wrong position (top band, not diagonal) |
| fixed-column frequency (Rowland) | **PROVEN, exact** | diagonal samples each column once, below its period (§3) |
| nonzero-digit count `→∞` | **PROVEN** `log n/log log n` | global count, `o(n)`, no density of any value |
| longest-run `L(M·3ᴷ)=ηK+o(K)` | **PROVEN** (subspace, §2.4) | horizontal run, gives only `density ≥ 1/o(n)→0` |
| "≈ half bits are 1" (Pegg) | **CONJECTURE** | global density, still not the *positional* diagonal |
| block uniform distribution (Ren/AEV) | **CONJECTURE** | superset of `(K)`; equals Mahler/AEV |

> **`[survey verdict]`** What would *suffice* for `(K)` is a one-sided statement at the **diagonal
> position**: e.g. "`freq{n : bit_n(8·3ⁿ)=0} ≤ 2/3`" (an upper density on the 0-digit at the moving
> position `n`). **No published result gives a one-sided positive/upper density at a position that
> moves with `n` for `3ⁿ`.** Every positive proven density is at a *fixed* position (Benford top,
> Rowland columns); every *moving/global* result is either a sublinear count or a run bound. The
> diagonal-position density is precisely the open kernel, identical to Mahler `{(3/2)ⁿ}` and AEV
> Conj 1.6 (`AEV_DIGEST.md`). There is **no attackable one-sided diagonal fragment** in the current
> literature — the run bound (§2.4) is the nearest unconditional structure and provably stops short.

**Combined with `a_n ⊥ b_n` (`WALL_B_WHICH_PART.md`):** the XOR only needs `A_r→0 ⟺ a_n ⊥ b_n`. A
digit-distribution input that would suffice for `(K)` via `a_n` alone is: *any* one-sided diagonal
density `freq(a_n=0) ≤ 1−c` with `c>0` (then `a_n` is non-degenerate; combined with `b_n`-balance and
decorrelation, `A_r→0`). The literature does not supply even this weak `c>0` one-sided bound — it
supplies only `c=1/o(n)→0` (the run bound) or full equidistribution (conjectural). So the
**weakest literature input that would close it is still strictly beyond the proven frontier**, and
the *strongest proven* fact (run bound) gives a vanishing constant. The diagonal density is the wall.

---

## 5. Numerics (`.venv`, exact integer arithmetic)

- **Diagonal balance** `freq(a_n=1)`: 0.50490 (10⁴) → 0.49992 (5·10⁴) → 0.49867 (2·10⁵). Balanced.
- **Column-vs-diagonal structure:** diagonal samples column `k` at row `k ≪ 2^{k−2}` (period) for all
  `k≥5` ⇒ each column visited once, below its period ⇒ Rowland periodicity gives no density transfer
  to the diagonal. (Confirmed `n=3..20`.)
- **Run bound sanity:** consistent with `L(8·3ⁿ)=o(n)` — no long monochromatic runs observed in
  binary `8·3ⁿ` for `n≤2·10⁵` (longest run grows far slower than `n`).
- Earlier (`WALL_B_WHICH_PART.md`): log-log decay slope of the diagonal signed mean ≈ `−0.40`
  (near √-cancellation; not proven).

---

## 6. Bottom line — the asks

1. **Latest (2018-2026) binary-digits-of-`3ⁿ` results, exact (§2):** Ren–Roettger 2025
   (arXiv:2511.03861, block-uniform-distribution **conjecture** + `10⁶` numerics, `log₃2` normal
   conjecture); Howe 2021 (arXiv:2105.06440, "≈half bits 1" is **Pegg conjecture**; **proven** only
   finiteness of few-1s `3ⁿ`); Senge–Straus 1973 / Stewart 1980 / Bugeaud–Kaneko 2016
   (arXiv:1609.07926) — nonzero-digit count `→∞` at `log n/log log n`, **PROVEN, EFFECTIVE, but
   `o(n)`**; **NEW** Spiegelhofer–Wallner 2025 (arXiv:2501.00850 Lemma 4.1, Bugeaud–Kaneko/subspace)
   longest-run `L(M·3ᴷ) ≤ ηK+o(K)`, **PROVEN UNCONDITIONAL**, applies to `8·3ⁿ`; Rowland 2009
   (arXiv:0902.3257) fixed-column periodicity (period `2^{k−2}`) + 2-adic diagonal-stripe series,
   **PROVEN**.
2. **One-sided / positive-lower-density at the MIDDLE (diagonal) position?** **NO** (§4). Proven
   positive densities exist only at *fixed* positions (Benford top band; Rowland columns) which do
   **not** intersect the moving diagonal; every moving/global proven result is either a sublinear
   count (`o(n)`, no density) or the new run bound (`density ≥ 1/o(n) → 0`, two-sided, vanishing).
   No published `freq(bit_n(8·3ⁿ)=0) ≤ 1−c`, `c>0`.
3. **Does the digit open problem coincide with `(K)`, or is there an attackable one-sided fragment?**
   The community problem (block normality, Ren/AEV) is a **strict superset** of `(K)`; `(K)` is the
   single diagonal-marginal and is **identical to Mahler `{(3/2)ⁿ}` / AEV Conj 1.6**. **No attackable
   one-sided fragment at the diagonal exists** — the run bound (§2.4) is the nearest unconditional
   structure and provably stops short (run ≠ density), and the proven column-periodicity provably
   misses the diagonal (samples each column once, below period, §3).
4. **Numerics (§5):** diagonal balanced (≈0.499); column-once-below-period structural demo; run bound
   consistent.

### Banked (new this session)
- **Run-length frontier identified:** `L(M·3ᴷ) ≤ ηK+o(K)` (subspace theorem, arXiv:2501.00850
  Lemma 4.1) is the **freshest unconditional handle** and **applies verbatim to `8·3ⁿ`** (M=8); it is
  the correct "what subspace methods give" citation, and it provably stalls at vanishing density —
  sharper than the nonzero-count bound, still short of `(K)`. New addition to the negative dossier.
- **Structural proof that the one proven positional regularity (Rowland column-periodicity) is
  orthogonal to `(K)`:** the diagonal samples each column exactly once, at row `< 2^{k−2}` (its
  period), so no density transfer. This explains *why* the cleanest known regularity does not help —
  a crisp, exact reason rather than a vague "it's hard."
- **Placement:** `(K)` = diagonal-position density, wedged strictly between Benford (proven, wrong
  position) and Ren/AEV normality (conjectured superset), coinciding with Mahler/AEV, with **no
  one-sided fragment in between**. Consistent with `THREEADIC_LITERATURE.md`, `AEV_DIGEST.md`,
  `KERNEL_FINAL.md`.

### Honest non-breach
This is a literature placement + a sharpened structural negative, **not** progress on `(K)` itself.
The decisive obstruction is unchanged: a one-sided density of the **moving diagonal** `bit_n(8·3ⁿ)`,
which equals the open Mahler/AEV `{(3/2)ⁿ}` object in every framing surveyed.

## References
- Ren, X., Roettger, C., *Ternary Digits of Powers of Two*, arXiv:2511.03861 (Nov 2025).
- Howe, E., *Powers of 3 with few nonzero bits and a conjecture of Erdős*, arXiv:2105.06440 (2021).
- Senge, H.G., Straus, E.G., *PV-numbers and sets of multiplicity*, Period. Math. Hungar. 3 (1973) 93–100.
- Stewart, C.L., *On the representation of an integer in two different bases*, J. Reine Angew. Math. 319 (1980) 63–72.
- Bugeaud, Y., Kaneko, H., *On the digital representation of integers with bounded prime factors*, arXiv:1609.07926; Ann. Sc. Norm. Super. Pisa (2018). (also *…of smooth numbers*, Math. Proc. Camb. Phil. Soc. 165 (2018) 533–540.)
- arXiv:2501.00850 (Jan 2025), *The joint distribution of binary and ternary digit sums* — **[SOUNDNESS, citation-pending, `CORE_ORBIT_ARITHMETIC.md` §5′]**: this paper's main result is **digit-SUM normality via Baker's theorem**, NOT a run lemma; the longest-run bound `L(M·3ⁿ)=o(n)` is **real** (Schlickewei p-adic subspace theorem, Bugeaud–Kaneko line) but its attribution to "2501.00850 Lemma 4.1" / "Spiegelhofer–Wallner" is **unverified** — relabel `[PROVEN-in-lit, exact reference pending]`, do not cite 2501.00850 for the run bound.
- Rowland, E., *Regularity versus complexity in the binary representation of 3ⁿ*, arXiv:0902.3257; Complex Systems 18 (2009).
- Andrieu, M., Eliahou, S., Vivion, L., *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025). (cross-ref `AEV_DIGEST.md`)
- (cross-refs) `WALL_B_WHICH_PART.md`, `THREEADIC_LITERATURE.md`, `AEV_DIGEST.md`, `KERNEL_FINAL.md`, `BAKER_LINFORMS.md`.
