# ATTACK: van der Corput / Weyl differencing on the (3/2)^j exponential sum (2026-06-28)

Target = GM-skeleton line (5) / the Mahler-AEV kernel: cancellation of the self-generated
exponential sum that governs the Antihydra carry bit. This note runs the standard
van-der-Corput / Weyl-differencing machinery against it, pins **exactly** where it fails as a
precise inequality, records the best citable unconditional bound, analyses the correlated
weights, and reports measured cancellation. Every line labelled. **Zero false proofs — the
conclusion is a NEGATIVE result: this machinery cannot reach the kernel, and why.**

---

## 0. The object, in lacunary form  [PROVEN identity, `exp_sum.py` + reduction this session]

Carry bit governed by `{S_n/4}` with `S_n = Σ_{j=0}^{n-1} e_{n-1-j} (3/2)^j`, `e` = orbit parity.
Re-index `k=n-1-j`:
```
S_n = (3/2)^{n-1} · P_n ,   P_n = Σ_{k=0}^{n-1} e_k (2/3)^k  →  P_∞  (a CONTRACTING, convergent sum).
```
So the **Weyl/Birkhoff cancellation sum** that the proof needs to be `o(N)` is
```
W_N = Σ_{n<N} (−1)^{bit_n(T_n)} = Re Σ_{n<N} e(S_n/4) ≈ Re Σ_{n<N} e( ξ·(3/2)^n ),
        ξ = P_∞/6   (numerically ξ = 0.06791137, orbit-determined).
```
**This is literally the lacunary / Mahler exponential sum `Σ e(ξ(3/2)^n)`** with `ξ` built from
the orbit's own parity. (Faithfulness checked: `c_n mod2 == bit_n(8·3^n) ⊕ bit_n(T_n)`, ok=2000/0.)

---

## 1. The precise obstruction  [PROVEN, elementary — the inequality that fails]

Treat the phase as the smooth function `f(x) = ξ·(3/2)^x = ξ·e^{x·ln(3/2)}`.

### 1a. k-th derivative test — the bounded-ratio hypothesis fails exponentially
Van der Corput's k-th derivative test (e.g. Graham–Kolesnik / Titchmarsh form): if on `[a,b]`
```
λ ≤ |f^{(k)}(x)| ≤ A·λ      (A = max/min ratio of the k-th derivative over the range),
```
then with `K = 2^{k-1}`,
```
|Σ_{a<n≤b} e(f(n))| ≪_k (b−a)(Aλ)^{1/(2K−2)} + (b−a)^{1−1/(K−1)} λ^{−1/(2K−2)} .
```
This beats the trivial bound `(b−a)` **only if `A = O(1)`** (the ratio is bounded independent of
the range length). For our phase
```
f^{(k)}(x) = ξ·(ln 3/2)^k·(3/2)^x  ⇒  A = f^{(k)}(b)/f^{(k)}(a) = (3/2)^{b−a}.
```
**THE OBSTRUCTION INEQUALITY (which fails):**
```
   required:  A = (3/2)^{L}  =  O(1)        (L = b−a = range length)
   actual:    A = (3/2)^{L}  →  ∞           exponentially in L.
```
The hypothesis holds **only on blocks of length `L = O(1/ln(3/2)) = O(1)`**. On each `O(1)`-block
the test returns `O(1)` cancellation = the trivial count of that block. Covering `n=1..N` needs
`≈ N·ln(3/2)/ln 2 ≈ 0.585·N = Θ(N)` such blocks. Summing the per-block `O(1)` bounds gives
`|W_N| ≪ N` = **the trivial bound. No cross-block cancellation. ∎ (failure)**

The single inequality `(3/2)^{b−a} = O(1)` is the whole obstruction: it is the statement that
`(3/2)^x` is **not slowly varying** on any long range — exactly the lacunarity (Hadamard gap
ratio `3/2 > 1`).

### 1b. Weyl differencing (A-process) — degree is not reduced (self-reproducing fixed point)
```
|Σ_{n≤N} e(f(n))|² ≤ N + 2 Σ_{h=1}^{H}(1−h/H)·|Σ_n e(Δ_h f(n))|,   Δ_h f(n)=f(n+h)−f(n).
```
For a **polynomial** `f` of degree `d`, `Δ_h f` has degree `d−1`; iterate `d−1` times → linear
phase → geometric series sums to `O(‖·‖^{−1})`. For our phase:
```
Δ_h f(n) = ξ((3/2)^h − 1)·(3/2)^n = ξ'·(3/2)^n ,   ξ' = ξ((3/2)^h − 1).
```
**The differenced sum is the SAME (3/2)^n lacunary exponential sum with a rescaled coefficient.**
Differencing is a **fixed point** of the functional form — it never lowers the degree, the
induction never terminates, and (1a) shows each level is still range-restricted. So the A-process
yields only `|W_N|² ≤ N + (sums of the same type)` ⇒ **no gain. ∎**

This is the precise, well-known reason van der Corput controls *polynomial* phases (`{nᵏα}`,
`{n·log₂3}` leading bits — which ARE effectively equidistributed) but **not geometric/lacunary
phases `λ^n`**. The earlier note that "van der Corput differencing fixes (3/2)ⁿ (white differenced
sums)" (`PROOF_STATUS.md` §2) is exactly this fixed-point: differencing whitens nothing.

---

## 2. Best citable UNCONDITIONAL bound for `Σ e(ξ(3/2)^n)`  [theorem vs conjecture, pinned]

For a **specific** `ξ > 0` (our case, `ξ = P_∞/6`):
- **[OPEN — no nontrivial unconditional bound exists]** Even `Σ_{n≤N} e(ξ(3/2)^n) = o(N)` is
  **unknown for every specific `ξ`**. Equivalently it is **not even known that `{ξ(3/2)^n}` is
  dense or equidistributed**, nor that `(3/2)^n mod 1` is dense — all open (Mahler 1968 circle).
  So **the best citable unconditional bound for our sum is the TRIVIAL `O(N)`.**

What *is* unconditionally proven (none give cancellation/`o(N)` for a fixed `ξ`):
- **[THEOREM] Flatto–Lagarias–Pollington (1995),** *On the range of fractional parts {ξ(p/q)ⁿ}*,
  Acta Arith. 70, 125–147: for `p/q=3/2` (so `p=3`), `Ω(3/2) := limsupₙ{ξ(3/2)ⁿ} − liminfₙ ≥ 1/3`
  for every `ξ>0`. A **support-spread** bound — orbit can't be confined to an interval shorter
  than `1/3`. **Not a cancellation bound** (an orbit can be unconfined yet have biased frequency).
  Mahler would follow from `Ω(3/2) > 1/2`; `>1/2` is open.
- **[THEOREM] Vijayaraghavan:** `{(3/2)ⁿ}` has infinitely many limit points. (Support, not freq.)
- **[THEOREM, METRIC / a.e. — NOT specialisable to our ξ] Salem–Zygmund (1947–48)** lacunary CLT
  + Erdős–Gál LIL: for **Lebesgue-a.e.** `ξ`, `Σ_{n≤N} e(ξ(3/2)ⁿ)` obeys a CLT and
  `= O(√(N log log N))` — full square-root cancellation. A.e. statements **cannot be specialised
  to the single algebraic-flavoured value `ξ=P_∞/6`** (same a.e.-vs-single-orbit wall as Solomyak
  for ν_{2/3} in `NONPISOT_FOURIER_CHAIN.md`).
- **[THEOREM, METRIC] Algom–Chang–Wu–Wu (2024/25, Math. Ann.; arXiv:2401.01120)** *Van der Corput
  and metric theorems for geometric progressions for self-similar measures* — the **modern** vdC
  machinery for geometric progressions, but again **a.e./measure-theoretic**, not single `ξ`.
- **[THEOREM] Dubickas (2006), Akiyama et al.:** distance-to-integer `‖ξ(3/2)ⁿ‖` and Z-number
  structure — separation/support results, **not cancellation**.
- **[CONJECTURE — all open]** Mahler (no Z-number), AEV normality (2025, arXiv:2510.11723),
  equidistribution of `(3/2)ⁿ`.

**Vinogradov / Vaughan:** designed for polynomial phases and Type I/II bilinear structure over
primes; they give **nothing** here — the phase `(3/2)ⁿ` is not polynomial and reduces to (1b)'s
fixed point under any differencing. No logarithmic, no conditional standard-machinery bound is
obtainable for a fixed `ξ`.

**Verdict (2):** No unconditional cancellation bound — even logarithmic, even conditional on
standard hypotheses — is available for the specific `(3/2)ⁿ` sum. Only the trivial bound and the
FLP support bound `Ω≥1/3` are theorems.

---

## 3. The weights are the orbit's own parity — does correlation help or hurt?  [analysis]

The sum is doubly self-referential: weights `w_n = (−1)^{e_n}` AND the coefficient `ξ = P_∞/6 =
(1/6)Σ e_k(2/3)^k` are both built from the same parity bits `e`.

- **General bounded weights break the machinery.** Handling weights by Cauchy–Schwarz/bilinear
  discards the phase: `|Σ w_n e(f(n))|² ≤ (Σ|w_n|²)(Σ_h |Σ_n w̄_n w_{n+h} e(Δ_h f(n))|)` — needs
  the weight-autocorrelations `Σ w̄_n w_{n+h}` to be small AND to not resonate with `Δ_h f`. Weyl
  differencing of `w_n e(f(n))` mixes weight correlations into the phase and (by 1b) still does
  not lower the degree. So vdC/Weyl require the weights to be **smooth or well-factorable**; the
  parity sequence is neither.
- **Correlation HURTS — it is the obstruction, not an aid.** The square-root cancellation of §2's
  Salem–Zygmund theorem is **driven by independence** (typical/independent `ξ`, weights
  independent of phase). Here the weights are correlated **with the very phase they multiply**
  (both emitted by the one orbit) — exactly the regime where that independence is absent. Worst
  case the weight resonates with the phase (`w_n ≈ sign Re e(ξ(3/2)ⁿ)`) and the sum does not
  cancel at all. This is the **closed-loop / quenched / self-induced-disorder** obstruction
  already isolated as line (5): the bias is a self-referential identification bias.
- **Could it ever help?** Only via a *proof* that `w` decorrelates from the phase (a
  mixing/disjointness statement). The `coupling_brick.py` measurements show empirical
  decorrelation from every provable surrogate (Thue–Morse, Rudin–Shapiro, Legendre, leading-bit
  Sturmian), but **that decorrelation is itself unproven and IS the theorem to build.** So the
  correlated weights are neither demonstrably benign nor exploitable by standard machinery — they
  ARE the open kernel. **Net: correlation strictly hurts the standard estimates.**

---

## 4. Numerics — real orbit `c₀=8`, up to `N=2·10^5`  [measured; `vdc_num.py`]

Implementation faithfulness verified: `c_n mod2 == bit_n(8·3ⁿ) ⊕ bit_n(T_n)`, **ok=2000, bad=0**.

| sum | `N` | `|·|/N` (vs trivial=1) | `|·|/√N` (vs random≈0.8) | note |
|---|---|---|---|---|
| parity `W_N=Σ(−1)^{c_n mod2}` | 10⁴ / 10⁵ / 2·10⁵ | 0.0092 / 0.0032 / 0.0004 | 0.92 / 1.01 / 0.16 | even-dens 0.495→0.502 |
| carry kernel `B_N=Σ(−1)^{bit_n(T_n)}` | 10² / 10³ / 2·10³ | 0.040 / 0.032 / 0.021 | 0.40 / 1.01 / 0.92 | the literal (K) |
| exact Weyl `L_N=Σe({S_n/4})` | 10² / 10³ / 2·10³ | 0.107 / 0.028 / 0.018 | 1.07 / 0.87 / 0.81 | log-log slope ≈ 0.41 |
| random ±1 surrogate | 2·10³ (200 trials) | — | **mean 0.79** | Salem–Zygmund √N |
| random-phase `Σe(U)` surrogate | 2·10³ | — | **0.87** | i.i.d. phases √N |

**Reading:**
- **Observed cancellation rate ≈ `√N`** (`|W_N|/N → 0`; `|·|/√N` stays `O(1)`, slope ≈ 0.41–0.5),
  **statistically indistinguishable from the random / random-phase surrogate (≈0.8)**. The real
  orbit's exponential sum behaves **exactly like Salem–Zygmund's typical-`ξ` square-root regime** —
  the orbit "looks generic."
- **What van der Corput / Weyl WOULD give here: nothing better than the trivial `|W_N| ≤ N`**
  (`|·|/N ≤ 1`, no decay), per §1. The empirically observed `√N` is **a full power of `N` better
  than anything this machinery can prove.**
- **The entire open problem = the gap between observed `N^{1/2}` and vdC-provable `N^{1.0}`.** The
  numbers say the orbit is generic; the machinery cannot certify even `o(N)`.

---

## 5. Conclusions (the four asks)

1. **Precise obstruction inequality.** vdC k-th-derivative test needs the derivative ratio
   `A = max|f^{(k)}|/min|f^{(k)}|` over the summation range to be `O(1)`; for `f=ξ(3/2)^x`,
   `A = (3/2)^{b−a} → ∞`. Equivalently, Weyl differencing maps `ξ(3/2)^n ↦ ξ((3/2)^h−1)(3/2)^n` —
   a **fixed point** that never lowers the degree. Both express lacunarity (gap ratio `3/2>1`).
   **[PROVEN, elementary]**

2. **Best citable unconditional bound for `Σe(ξ(3/2)^n)`, specific `ξ`:** the **trivial `O(N)`**;
   no nontrivial (even logarithmic, even conditional) standard bound exists. Only structural
   theorems are **FLP 1995 `Ω(3/2) ≥ 1/3`** (support spread, Acta Arith. 70:125–147) and the
   **a.e./metric** Salem–Zygmund `O(√(N log log N))` and Algom–Chang–Wu–Wu — none specialisable to
   a fixed `ξ`. Mahler / AEV-normality remain conjectures. **[OPEN]**

3. **Correlated (self-generated) weights HURT.** They remove the independence that drives the
   Salem–Zygmund square-root cancellation and break the smoothness/well-factorability vdC needs;
   they are precisely the closed-loop / quenched obstruction (= line (5)), not an aid. **[analysis]**

4. **Numerical cancellation rate ≈ `N^{1/2}` (square-root), matching a random surrogate**, while
   van der Corput can prove only the trivial `N^{1.0}`. The orbit is empirically generic but
   unprovably so by this machinery. **[measured]**

**Bottom line.** van der Corput / Weyl differencing is **[CLOSED]** against this kernel for a
structural, conjecture-independent reason (the `(3/2)^{L}` ratio blow-up / differencing
fixed point). It joins the closed technique-axes in `PROOF_STATUS.md` §2 with the failure mode now
stated as a single inequality. The kernel (5) = Mahler/AEV remains **[OPEN]**: the data show the
sum *behaves* like a generic √N-cancelling lacunary sum, but every tool that could *prove* √N
(Salem–Zygmund, Algom et al.) is a.e./metric and cannot be specialised to this one orbit, and vdC
gives nothing. The gap `N^{1/2}` (observed) vs `N^{1.0}` (provable) IS the open problem.
