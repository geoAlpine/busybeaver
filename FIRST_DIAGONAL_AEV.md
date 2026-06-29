# FIRST_DIAGONAL_AEV — literature-grounded best partial + a NEW unconditional partial attempt on the bare first diagonal (2026-06-29)

*Assigned angle (`WEAPONS_AUDIT` style): the BARE FIRST DIAGONAL `d_n = bit_{n+k}(8·3^n) = bit_k(⌊8(3/2)^n⌋)`
= AEV/Mahler digit at `α=8`. Tasks: (1) pin EXACTLY what AEV 2025 / Algom / latest Mahler-3/2 & digits-of-3^n
literature actually PROVE (partials, not the conjecture), each cited; (2) decide whether each ports to the
single `α=8` diagonal and its exact reach/gap; (3) ATTEMPT a genuinely new unconditional partial on the single
diagonal; (4) honest verdict. SOUNDNESS PARAMOUNT, every claim labelled. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/first_diag.py, diverge.py`, exact big-int, N≤10⁵,
<3s. WebSearch used. NOT committed.*

---

## 0. One-line verdict

**(a) NEW unconditional partial: YES — but on the ITERATED Antihydra orbit `a_n = c_n mod 2`
(`c_{n+1}=⌊3c_n/2⌋`, the actual halting object), NOT on the literal closed-form Mahler diagonal `d_n`.**
`[PROVEN]` the iterated orbit's parity is *not eventually constant* and every maximal constant-parity run has
**exact length `v₂(c_n)`** (even runs) / **`v₂(c_n−1)`** (odd runs); hence both parities occur infinitely often,
with an explicit run-length law (0 failures, 10 022 runs, N=2·10⁴). **(b)** On the *literal target* `d_n =
bit_k(⌊8(3/2)^n⌋)` the sharpest literature partials are Weyl/Diophantine top-`Θ(log N)`-digit equidistribution
(`EFFECTIVE_TOPDIGIT`) and FLP spread `Ω(3/2)≥1/3`; **NO new partial on `d_n` is possible by the present tools —
even "both digit values occur infinitely often" is itself Mahler-type OPEN** for the closed form. **(c)** The
exact residual gap is unchanged: a one-sided positive *density* (`freq(d_n=0) ≤ 1−c`, `c>0`) at the moving
diagonal = Mahler 3/2 / AEV Conj 1.6 at `α=8`. **Key clarifying finding:** the iterated TM orbit `⌊3c_n/2⌋` and
the closed-form `⌊8(3/2)^n⌋` **diverge at n=6** (90 vs 91) and differ in parity ~½ the time — the new proof
exploits the iterated recursion and provably does NOT transfer to the closed-form diagonal. **No machine
decided. No label upgraded.**

---

## 1. What the literature actually PROVES (partials only), and whether it ports to `α=8`

`d_n = bit_{n+k}(8·3^n) = ⌊2^{3−k}(3/2)^n⌋ mod 2`, equivalently **`d_n = 1 ⟺ {2^{2−k}(3/2)^n} ∈ [½,1)`**
(exact; θ:=2^{2−k}). This is the half-interval / Z-number indicator for `θ(3/2)^n`, i.e. AEV Conj 1.6 / Mahler at
the single point `α=8`.

| # | Result (PROVEN partial) | Citation | Ports to single `α=8` diagonal? | Reach | Exact gap to "d_n equidistributes" |
|---|---|---|---|---|---|
| 1 | Top-band equidistribution: `{n log₂3}` u.d. (Weyl); star-discrepancy `≪1/N` at CF-convergents of `log₂3` | Weyl 1916; `EFFECTIVE_TOPDIGIT.md` (Thm a/b, constants from CF of `log₂3`) | **Yes**, but only the TOP `Θ(log N)` bits of `⌊8(3/2)^n⌋` | top `k(N)≈log₂N` digits equidistribute, discrepancy `≪1/N` along `N=q_m` | diagonal sits at depth `≈0.63·len` (≈n bits up); gap `Θ(n)−Θ(log N)=Θ(n)` |
| 2 | Spread of limit points: `Ω(3/2)=limsup−liminf {ξ(3/2)^n} ≥ 1/p = 1/3` for **every** `ξ>0` | Flatto–Lagarias–Pollington, Acta Arith. 70 (1995) 125–147 | **Yes** (holds for `ξ=θ`) | fractional parts spread over an interval of length `≥1/3` | spread `1/3 < 1/2`: orbit can still sit entirely in `[0,½)` ⇒ gives **nothing** on either half-interval count; not a density |
| 3 | Nonzero-binary-digit count of `3^n → ∞`, effective `≫ log n/log log n` | Senge–Straus 1973; Stewart, Crelle 319 (1980); Bugeaud–Kaneko, Ann. SNS Pisa (2018), arXiv:1609.07926 (Schmidt subspace + linear forms in logs) | **Yes** (counts 1-bits of `8·3^n`) | `o(n)` nonzero digits somewhere | global count, `o(n)` ⇒ **no positive density of any value at any position**, a fortiori not the diagonal |
| 4 | Longest equal-bit run: `sup_{M<2^{ηK}} L(M·3^K) ≤ ηK+o(K)`, so `L(8·3^n)=o(n)` | Spiegelhofer–Wallner, arXiv:2501.00850 (Jan 2025) Lemma 4.1 (Schlickewei p-adic subspace thm) | **Yes verbatim** (M=8) | no monochromatic run longer than `o(n)` in `8·3^n` | horizontal run, not diagonal; gives only two-sided per-row density `≥1/o(n)→0`; vanishing constant |
| 5 | Fixed-column periodicity: column `k` of the `3^n` bit-grid is periodic in `n`, period `2^{k−2}`, exact rational frequency | Rowland, Complex Systems 18 (2009), arXiv:0902.3257 | **No** | exact density at any FIXED column | diagonal samples column `k` at row `k≪2^{k−2}` (once, below its period) ⇒ zero density transfer (`DIGITS_OF_3N §3`) |
| 6 | Metric (a.e.-`ξ`) discrepancy / LIL / CLT for `{ξ(3/2)^n}` | Koksma 1935; Erdős–Koksma 1949; Aistleitner, arXiv:1210.4215 (`limsup √N D_N/√(loglog N)=1/√2` a.e.) | **No** | full quantitative u.d. for **Lebesgue-a.e.** `ξ` | the orbit `ξ=θ` is one fixed Haar-null point; a.e. says nothing about it. Aistleitner: "specific-`x` u.d. notoriously difficult" |
| 7 | Rajchman decay of `ν_{2/3}` (3/2 non-Pisot) ⇒ **annealed** equidistribution, effective log rate (Varjú–Yu) | Erdős 1939/Salem 1944; Varjú–Yu arXiv:2004.09358; `SECOND_DIAGONAL_RAJCHMAN.md` §1 | **No** for `α=8` | annealed (iid-parity) diagonal only | the first diagonal's annealed measure is `δ₀` (`ν̂≡1`): **Rajchman vacuous for `α=8`** (`SECOND_DIAGONAL_RAJCHMAN §2`); quenched single orbit = Mahler |
| 8 | AEV Conj 1.6 = normality of min/max words (Conj 1.2/1.3); proven content = equivalences/implications + numerics | Andrieu–Eliahou–Vivion, arXiv:2510.11723 (v1 Oct 2025, v2 Apr 2026): Thm 1.5 (1.2⇒1.4, `p<q²`), Thm 1.7 (1.2⇔1.6) | the CONJECTURE is exactly our object at `p/q=3/2` | **zero** unconditional distribution facts for 3/2 | AEV prove **no** density/discrepancy/single-orbit result; only conjecture+numerics (`AEV_DIGEST §6`) |
| 9 | Rajchman ⇒ μ-a.e.-in-support normality (no rate needed); exposition lists effective-equidist. + non-integer-base as OPEN | Algom–Baker–Shmerkin, Adv. Math. (2022), arXiv:2107.02699; Algom (exposition) arXiv:2504.18192 | **No** | μ-a.e. point of a self-similar measure | "a.e.-in-support" is the quantifier we cannot use for one specified algebraic orbit (`EMPTY_TOOLBOX §1`) |

**Sharpest literature partial toward `d_n` equidistribution:** **#1 (Weyl/Diophantine top-`Θ(log N)` digits,
discrepancy `≪1/N` at convergents of `log₂3`)** — the only result that proves *exact equidistribution of actual
digits of `⌊8(3/2)^n⌋`. Its reach is the top `Θ(log N)` band; the diagonal is `Θ(n)` bits away. The strongest
*structural* digit fact is **#4** (`L(8·3^n)=o(n)`, subspace theorem, 2025) but it lives on the wrong axis
(run ≠ density) and yields a vanishing constant. **Withdrawn (do NOT cite):** N. Kumar, "Mahler's 3/2 problem
in ℤ⁺", arXiv:2411.03468 — claimed no integer Z-numbers, **withdrawn 18 Jun 2025**.

---

## 2. NEW unconditional partial — attempt and result

### 2a. The literal target `d_n = bit_k(⌊8(3/2)^n⌋)` resists even *infinitude*  `[OPEN = Mahler]`

For the closed form, `d_n = 1 ⟺ {θ(3/2)^n} ∈ [½,1)`, `θ=2^{2−k}`. Then:
- "`d_n = 1` infinitely often" ⟺ `θ` is **not eventually a Z-number** — a Mahler-type statement, **OPEN**.
- "`d_n = 0` infinitely often" ⟺ `{θ(3/2)^n}` **not eventually in `[½,1)`** — dual Mahler-type, **OPEN**.
- Hence even "**both digit values occur infinitely often**" is OPEN for the literal target. FLP (#2) gives
  spread `≥1/3 < 1/2`, which does **not** force both half-intervals to be visited (the limit set can lie inside
  one half). **No new unconditional partial on `d_n` is available.** `[verified obstruction]`

### 2b. The ITERATED Antihydra orbit `a_n = c_n mod 2` — a genuinely PROVEN new partial  `[PROVEN]`

**Crucial distinction (new finding).** The Antihydra Turing machine's actual orbit is the *iterated* map
`c_0=8, c_{n+1}=⌊3c_n/2⌋` — **not** the closed form `⌊8(3/2)^n⌋`. Nested floors make them **diverge at n=6**
(`c_6=90` iterated vs `⌊8(3/2)^6⌋=91`); they differ at 1995/2001 indices and in **parity at 1021/2001 indices**
(`diverge.py`). The halting reduction (`AEV_KERNEL_MAP §1–2`) is about the **iterated** orbit's even-density.
On this object the parity admits a clean unconditional law:

> **`[PROVEN]` Run-length / non-constancy law.** Let `c_0=8`, `c_{n+1}=⌊3c_n/2⌋`.
> For even `c_n`: `c_{n+1}=3c_n/2`, so `v₂(c_{n+1})=v₂(c_n)−1`; a maximal even run starting at `c_n` has length
> **exactly `v₂(c_n)`**, then forces an odd term.
> For odd `c_n`: `c_{n+1}=(3c_n−1)/2`, so `c_{n+1}−1 = 3(c_n−1)/2` and `v₂(c_{n+1}−1)=v₂(c_n−1)−1`; a maximal
> odd run starting at `c_n` has length **exactly `v₂(c_n−1)`**, then forces an even term.
> Both valuations are finite (`c_n` a finite integer, `c_n>1`), so **every run is finite**; the sequence
> partitions into infinitely many finite alternating-parity runs ⇒ **both parities occur infinitely often; the
> parity diagonal is not eventually constant.**

*Proof.* Even branch: `v₂(3c_n/2)=v₂(c_n)−1` since 3 is odd; the run continues while `v₂≥1`, i.e. exactly
`v₂(c_n)` steps. Odd branch: `c_{n+1}−1=(3c_n−1)/2−1=3(c_n−1)/2`, and `v₂` drops by exactly 1 each odd step, so
the run lasts exactly `v₂(c_n−1)` steps. An infinite constant run would force `v₂=∞`, i.e. `c_n=0` (even) or
`c_n=1` (odd) in `ℤ₂`; impossible for the strictly growing integer orbit (`c_n≥8`). ∎

**Verification (`first_diag.py`, N=2·10⁴):** run-length law holds with **0 failures over 10 022 runs**; first
runs `(par,len,v₂pred)`: `(0,3,3),(1,1,1),(0,3,3),(1,1,1),(0,1,1),…` all matching. The same check on the
**closed form** `⌊8(3/2)^n⌋` **fails 686/998 runs** (`diverge.py`) — confirming the law is a property of the
*iterated* recursion and does **not** port to the bare Mahler diagonal.

**What it is and is not.** This is an honest, elementary, *modest* unconditional fact: it gives **infinitude**
(both parities i.o.) and an **exact run-length law** for the actual halting object — neither previously recorded
in the repo notes surveyed (it sharpens the `D=v₂(3o−1)` induced-map gap of `AEV_KERNEL_MAP` into a complete
two-sided run-length statement). It is **likely folklore** (elementary 2-adic argument); claimed only as
"new-to-this-repo," not as a literature first. **It yields zero density information:** the count of even terms
`= Σ(even-run lengths) = Σ v₂(c_n)` over run-starts, and the distribution of those valuations *is* the
even-density question — so no lower density bound escapes. The gap from "both parities i.o." to
"`liminf` even-density `≥1/3`" is the **entire** Mahler/AEV wall.

### 2c. Candidates that did NOT yield a new partial

- **One-sided liminf density `freq(d_n=1)≥c>0`:** = Mahler; FLP spread `≥1/3` does not transfer to a density
  (#2). Rajchman is annealed-only and vacuous at `α=8` (#7). **No.**
- **Infinitely many sign changes of the partial Weyl sum `Σ_{n≤N} e(tθ(3/2)^n)`:** equivalent to non-trivial
  oscillation of the same single-orbit sum; van der Corput is a fixed point for `(3/2)^n`
  (`EFFECTIVE_TOPDIGIT`, verified), so no unconditional handle. **No.**

---

## 3. Honest verdict (the four asks)

| ask | answer | label |
|---|---|---|
| **(a) NEW unconditional partial on the single diagonal?** | **On the literal closed-form `d_n`: NO** (even "both values i.o." = Mahler-OPEN). **On the iterated Antihydra orbit parity `a_n` (the true halting object): YES** — not eventually constant + exact run-length law `v₂(c_n)/v₂(c_n−1)`, both parities i.o. (0 failures / 10 022 runs). | closed-form **none**; iterated **`[PROVEN]`** |
| **(b) sharpest literature partial + exact gap** | **Weyl/Diophantine top-`Θ(log N)`-digit equidistribution** (discrepancy `≪1/N` at convergents of `log₂3`; `EFFECTIVE_TOPDIGIT`). Gap to the diagonal `= Θ(n)−Θ(log N)=Θ(n)` bits. Strongest *structural* digit fact: `L(8·3^n)=o(n)` (Spiegelhofer–Wallner 2025, subspace thm) — wrong axis, vanishing density. | `[PROVEN-in-lit]` |
| **(c) fully open core** | one-sided positive **density** at the moving diagonal (`freq(d_n=0)≤1−c`, `c>0`) for the single orbit `α=8` = Mahler 3/2 = AEV Conj 1.6 (`p/q=3/2`, ceiling) = the bare exogenous obstruction. AEV prove **no** unconditional 3/2 distribution fact (equivalences+numerics only). | `[OPEN]` |

**Exact residual gap.** Proven now: the iterated orbit's parity oscillates with finite runs of length
`v₂(c_n)/v₂(c_n−1)` (infinitude, **zero density**). Needed: a positive lower bound on the *frequency* of even
terms — equivalently `freq{n: {θ(3/2)^n}∈[½,1)} ≥ c>0` for the closed-form diagonal `θ=2^{2−k}`. That single step
from infinitude/spread to density is the full open wall; the literature reaches it from neither end (top/bottom
`Θ(log N)` footholds, a.e.-`ξ` metric theory, annealed Rajchman) and AEV/Algom both stop exactly there (on the
specified-orbit / effective-equidistribution axis).

---

## 4. Genuinely new vs prior

- **vs `DIGITS_OF_3N.md` / `EFFECTIVE_TOPDIGIT.md`:** those catalogued the literature's footholds (Benford top,
  Rowland columns, nonzero-count, run bound) and the `Θ(log N)` barrier. This note adds the **2025 subspace
  run-bound** (Spiegelhofer–Wallner arXiv:2501.00850) to the table with its exact reach, and re-pins AEV's
  withdrawn-companion landscape (arXiv:2411.03468 withdrawn).
- **vs `AEV_KERNEL_MAP.md` (D=v₂(3o−1) induced gap):** sharpened into a **complete two-sided run-length law**
  for both parities of the iterated orbit, with the new non-eventual-constancy corollary — a clean PROVEN fact
  not previously stated.
- **New clarifying finding:** the iterated TM orbit `⌊3c_n/2⌋` and the closed-form Mahler diagonal
  `⌊8(3/2)^n⌋` **diverge at n=6** and differ in parity ~½ the time; the run-length law is exclusively a property
  of the iterated recursion (fails 686/998 on the closed form). This pins down precisely *why* an elementary
  unconditional partial exists for the halting object yet **not** for the literal "bare first diagonal."

## Sources

- M. Andrieu, S. Eliahou, L. Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723
  (v1 Oct 2025; v2 Apr 2026). https://arxiv.org/abs/2510.11723 — Thm 1.5, Thm 1.7; Conj 1.2/1.3/1.4/1.6;
  no unconditional 3/2 distribution result (`AEV_DIGEST.md`, `AEV_METHODS.md`).
- A. Algom, *Recent progress on pointwise normality of self-similar measures*, arXiv:2504.18192 (2025);
  A. Algom, S. Baker, P. Shmerkin, *On normal numbers and self-similar measures*, Adv. Math. (2022),
  arXiv:2107.02699 — Rajchman ⇒ a.e.-in-support normal; effective-equidist. + non-integer base listed OPEN.
- L. Flatto, J. C. Lagarias, A. D. Pollington, *On the range of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. 70
  (1995) 125–147 — `Ω(3/2)≥1/3` (spread of limit points, not density).
- C. Aistleitner, *Quantitative uniform distribution results for geometric progressions*, arXiv:1210.4215 —
  metric (a.e.-`ξ`) LIL/CLT; states specific-`x` u.d. notoriously hard, no metric lower bounds.
- L. Spiegelhofer, M. Wallner, *The joint distribution of binary and ternary digit sums*, arXiv:2501.00850
  (Jan 2025) Lemma 4.1 — `L(M·3^K)≤ηK+o(K)` (Schlickewei subspace), gives `L(8·3^n)=o(n)`.
- Y. Bugeaud, H. Kaneko, *…digital representation…*, arXiv:1609.07926, Ann. SNS Pisa (2018); C. L. Stewart,
  Crelle 319 (1980); H. Senge, E. Straus (1973) — nonzero-digit count `→∞`, `o(n)`.
- E. Rowland, *Regularity versus complexity in the binary representation of 3ⁿ*, arXiv:0902.3257, Complex
  Systems 18 (2009) — fixed-column periodicity (period `2^{k−2}`).
- K. Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. 8 (1968) 313–321.
- **Withdrawn:** N. S. Kumar, *Mahler's 3/2 problem in ℤ⁺*, arXiv:2411.03468 — claimed no integer Z-numbers,
  **withdrawn 18 Jun 2025**; not citable.
- Repo: `EFFECTIVE_TOPDIGIT.md`, `DIGITS_OF_3N.md`, `TWO_DIAGONAL_COMPARISON.md`, `SECOND_DIAGONAL_RAJCHMAN.md`,
  `AEV_DIGEST.md`, `AEV_METHODS.md`, `AEV_KERNEL_MAP.md`, `EMPTY_TOOLBOX_QUESTION.md`, `CITATIONS.md`.
- Numerics: `scratchpad/first_diag.py` (orbit, run-length law 0/10022 fail, parity i.o., bit_k balance N=10⁵),
  `scratchpad/diverge.py` (iterated vs closed-form: diverge at n=6, parity differs 1021/2001, valuation law
  0/969 iterated vs 686/998 closed-form).

**No machine decided. No label upgraded.**
