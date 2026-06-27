# Attack: Mauduit–Rivat (Drmota / Spiegelhofer / Konieczny) digital exponential-sum machinery (2026-06-28)

**Target object.** The Antihydra parity `e_n = bit_n(8·3ⁿ) ⊕ bit_n(T_n)`, `bit_n` a binary DIGIT at the
*moving* position `n`; `T_{n+1}=3T_n+2ⁿe_n` (the self-generated carry sum). Kernel (K) = single-orbit
balance `(1/N)Σ(−1)^{e_n}=o(1)`. **Question of this attack:** does the MR sum-of-digits / digital
exponential-sum machinery reach this object, or is it Mahler-equivalent?

**Verdict up front [PROVEN structural, conjecture-independent reasoning + MEASURED numerics]:**
The MR machinery does **not** reach the object, and the obstruction is *structural and identifiable*, not a
gap in effort. MR's engine is built for **polynomial / prime** arguments via **van der Corput degree
reduction**; the Antihydra argument is the **geometric** sequence `3ⁿ`, for which the reduction step has no
degree to lower and the carry lemma's central hypothesis fails. The single piece of MR that *does* transfer
exactly — the digit Fourier transform `F_λ(h)=∏|cos π(α−h/2ⁱ)|` — reproduces only the **annealed/Rajchman**
fact (already in hand, the *easy* part), because the geometric argument pins the MR parameter `h` to a
single resonant ray, removing the `h`-average that is the heart of the MR saving. **MR ⇒ Antihydra is
Mahler-equivalent.** Every line labelled. Zero false proofs.

---

## 1. What MR / Drmota / Spiegelhofer / Konieczny actually proved, and the EXACT hypotheses [survey]

Notation: `s_q(n)` = base-`q` sum of digits, `e(t)=exp(2πit)`, `g(n)=e(α s_q(n))`.

- **[Gelfond 1968]** introduced the problem: distribution of `s_q(n)` for `n` in arithmetic progressions, and
  posed Problem A — distribution of `s_q(p)` (primes) and `s_q(P(n))` (`P` polynomial, e.g. `n²`).
- **[Mauduit–Rivat 2009, *La somme des chiffres des carrés*, Acta Math. 203, 107–148]** —
  **Theorem 2:** for `(q−1)α ∉ ℤ`, `|Σ_{n≤x} e(α s_q(n²))| ≤ C x^{1−σ_q(α)}`, σ_q(α)>0. ⇒ `s_q(n²)`
  equidistributed mod `m` when `(m,q−1)=1`.
- **[Mauduit–Rivat 2010, *Sur un problème de Gelfond: la somme des chiffres des nombres premiers*,
  Annals of Math. 171, 1591–1646]** — **Theorem 1:** `|Σ_{p≤x} e(α s_q(p))| ≤ C x^{1−σ_q(α)}`. ⇒
  `s_q(p) ≡ a (mod m)` equidistributed (`(m,q−1)=1`).
- **[Drmota–Mauduit–Rivat / Müllner; *Normality along squares*; Müllner, *The Rudin–Shapiro sequence and
  similar sequences are normal along squares*, arXiv:1704.06472]** — Thue–Morse and digital sequences mod `m`
  are **normal along `n²`** (every block of length `k` has frequency `q^{−k}`).
- **[Fouvry–Mauduit 1996, Math. Ann.]** — the type-I / almost-prime precursor (`s_q` along `n` and `p₁p₂`).
- **[Spiegelhofer 2020, *The level of distribution of the Thue–Morse sequence*, Compositio 156; arXiv:1803.01689;
  and arXiv:2504.02784]** — Thue–Morse (`= s_2 mod 2`) has **level of distribution 1** (Bombieri–Vinogradov-type
  for every θ<1). Sharpest known equidistribution-in-AP for a digit function.
- **[Konieczny 2019, *Gowers norms for the Thue–Morse and Rudin–Shapiro sequences*, Ann. Inst. Fourier 69;
  arXiv:1611.09985] and [Byszewski–Konieczny–Müllner, *Gowers norms for automatic sequences*, arXiv:2002.09509]**
  — `‖·‖_{U^k}` smallness for TM/RS and, generally, **every automatic sequence orthogonal to periodic sequences
  is Gowers-uniform**. This gives uniformity along all polynomial patterns.

### 1.1 The MR engine (exact, from Mauduit–Rivat's own exposition)
For a bilinear ("type II") sum `Σ_{m∼M}Σ_{n∼N} a_m b_n e(α s(mn))`, `MN=x`:
1. **Cauchy–Schwarz + van der Corput in `n`** ⇒ reduce to the **difference** `s(m(n+r)) − s(mn)` with
   `|r|<R`, `R=q^ρ`. (Lemma: `|Σ_{1≤ℓ≤L} z_ℓ|² ≤ ((L+(S−1)k)/S) Σ_{|s|<S}(1−|s|/S) Σ z_{ℓ+sk}\bar z_ℓ`.)
2. **Carry-propagation lemma.** In `s(mn+mr)−s(mn)` the added quantity `mr` is **much smaller** than `mn`
   (`μ+ρ` digits vs `μ+ν`), so digits above index `μ+ρ` change **only by carry**. The number of pairs whose
   carry exceeds `λ:=μ+2ρ` is `O(q^{μ+ν−ρ})` (negligible). ⇒ replace `s` by the **truncated detour**
   `s_λ(n)=Σ_{k<λ} n_k`, **periodic of period `q^λ`**.
3. **Discrete Fourier transform of the periodic detour:**
   `F_λ(h)=q^{−λ} Σ_{0≤u<q^λ} e(α s_λ(u) − hu/q^λ)`, and for `q=2`,
   `|F_λ(h)| = ∏_{i=1}^{λ} |cos π(α − h/2ⁱ)|`.
4. **The crucial saving** is the *averaged* bound `Σ_{0≤h<q^λ} |F_λ(h)| = O(q^{η_q λ})` with **`η_q < 1/2`**
   (sub-square-root). Combined with classical (Gauss-sum / geometric-sum) control of the *arithmetic* factor,
   this beats the trivial bound.

**EXACT hypotheses that make it run:**
- **(H1) Polynomial/multiplicative argument** so that vdC differencing `P(n+r)−P(n)` (resp. the bilinear `mn`)
  has **lower degree / much smaller magnitude** → the perturbation is **digit-localized** (occupies `≪`
  digits). This is what licenses step 2.
- **(H2) The full sum-of-digits `s` (or an automatic sequence)**, so the truncated detour `s_λ` is periodic.
- **(H3) A genuine `h`-range to average over** in step 4 (the saving is an *average* over `h`, not a single
  value); `(q−1)α∉ℤ` to avoid the trivial mode.

---

## 2. Does `bit_n(8·3ⁿ)` fit? — the crucial fit question [VERDICT: (c) Mahler-equivalent]

Two independent structural mismatches, each fatal; both are *named, classified* obstructions, not gaps.

### 2.1 Mismatch A — geometric vs polynomial argument: (H1) fails [PROVEN, elementary; numerics §4 STEP i]
MR's whole leverage is vdC **degree reduction**: for `P(n)=n²`, `(n+r)²−n² = 2nr+r²` is **degree 1**, a
**digit-localized** perturbation (`≈ν+ρ` digits inside a `2ν`-digit number). For the geometric argument,
```
   3^{n+r} − 3ⁿ = 3ⁿ(3^r − 1)
```
is the **same order of magnitude** as `3ⁿ` (a fixed constant multiple). **It is not digit-localized at all.**
Measured (STEP i): `bits(8·3ⁿ(3^r−1))/bits(8·3ⁿ) → 1.00` (vs `→0.53` for `n²`). The carry lemma (step 2)
has nothing to bite on: there is no small perturbation, hence no truncation to a periodic detour.
This is precisely why **geometric/lacunary sequences `aⁿ` are outside MR** — the sum of digits of `2ⁿ`
(and `3ⁿ`) is a *recognized open problem* (e.g. the conjecture `s_{10}(2ⁿ)/n → (9/2)log₁₀2`, and `log₃2`
not known normal to any base). The only published "powers" result, **Liu–Mauduit/collab., *The truncated
sum-of-digits function of powers*, Acta Math. Hungar. (2022), doi:10.1007/s10474-022-01267-6**, treats only
the **truncated** (first-`k`-digit) sum of digits of `aⁿ` — i.e. it explicitly retreats to the regime where
the full digit sum is intractable. Cf. also *Collisions of digit sums in bases 2 and 3* (arXiv:2105.11173),
*Ternary digits of powers of two* (arXiv:2511.03861) — all confirm the full-digit geometric regime is open.

### 2.2 Mismatch B — moving MIDDLE digit vs full sum / low-digit truncation: (H2) fails
[PROVEN structural; numerics §4 STEP ii-detour]
MR controls the **full** `s` (a sum over *all* digits) and truncates to the **low** `λ` digits (periodic
detour `s_λ`). The Antihydra object is a **single** digit at the **moving middle** position `n` (of the
`≈1.585n`-bit number `3ⁿ`) — neither a digit *sum* nor a *low* digit. Measured (STEP ii-detour): the best
*periodic* (low-`L`-digit) predictor of `bit_n(8·3ⁿ)` has accuracy `0.50` for genuinely periodic `L`
(`L=4,8,12`, #keys ≪ N); the apparent rise at `L=16,20` is **in-sample memorization** (#keys → N), not a
periodic law. The middle digit is **invisible to low-digit truncation**, so MR's detour mechanism does not
even define a non-trivial approximant here. (This is the same "support-vs-frequency / leading-vs-middle"
mismatch already mapped in PROOF_STATUS §3.6: leading bits `{n log₂3}` ARE effectively equidistributed, but
the parity uses the middle bit.)

### 2.3 Classification of the fit — answer to the task's (a)/(b)/(c)
- **(a) within reach of MR's carry lemma?** **No.** The carry lemma needs a digit-localized perturbation
  (H1); geometric differencing produces none.
- **(b) a known hard *variant*?** Partly: it is the *full digit function of a geometric sequence*, a regime
  where only **truncated** results exist (Liu–Mauduit 2022) and the full problem is acknowledged open.
- **(c) exactly Mahler in disguise?** **Yes — this is the operative verdict.** Once (H1)–(H2) fail, what is
  left is precisely effective single-orbit equidistribution of `{(3/2)ⁿ}`-type data = Mahler's 3/2 problem /
  AEV normality (arXiv:2411.03468, arXiv:1806.03559, arXiv:2510.11723), identical to kernel (K) /
  GM-skeleton line (5).

---

## 3. Can MR's carry lemma apply to the `T_{n+1}=3T_n+2ⁿe_n` recursion? [VERDICT: only the additive half]

The recursion is two operations per step: **(α) add `2ⁿe_n`** (a single localized digit), **(β) multiply by 3**.

- **The additive step (α) IS MR-amenable [PROVEN].** Adding `2ⁿe_n` is the textbook MR situation: a
  perturbation localized at digit `n`, changing higher digits only by carry. The MR carry-propagation lemma
  applies verbatim and shows the number of indices with long carry from this single addition is negligible.
  The natural **truncation/detour functions** are exactly `s_{μ,λ}(n)=Σ_{μ≤j<λ} n_j` (the windowed digit
  block around position `n`), periodic of period `2^λ` — the analogue of MR's `s_λ`. So the *injection* of
  the new parity bit is controllable.
- **The multiplicative step (β) is the wall [OPEN = Mahler].** Iterating ×3 is the geometric expansion =
  the `(3/2)`-odometer. Over `n` steps it composes to the `3ⁿ` argument of §2.1, where (H1) fails. The carry
  lemma cannot be applied across the ×3 because ×3 is *not* a small perturbation — it is the Mahler map.
- **Why this matters.** It pins the obstruction precisely: the difficulty is **not** the self-generated input
  bit `e_n` per se (its single-step injection is MR-tame); it is the **compounded geometric carry** `3ⁿ`
  through which past bits re-enter. This matches the closed-loop / quenched diagnosis in PROOF_STATUS §3.7–3.8
  (renewal variable contracts; bit-shift does not). MR formalizes *exactly which half* is hard.

---

## 4. Numerics — `mr_decomp.py` (`.venv`), MR step-by-step diagnosis [MEASURED]

```
STEP (i)  digit-localization of the vdC perturbation:
  n^2:   bits(2nr+r^2)/bits(n^2)         -> 0.53   (LOCALIZED  => MR carry lemma applies)
  8*3^n: bits(8*3^n(3^r-1))/bits(8*3^n)  -> 1.00   (NOT localized => carry lemma has no handle)

STEP (ii)-detour  best PERIODIC (low-L-digit) predictor of bit_n(8*3^n):
  L=4:0.50  L=8:0.52  L=12:0.56(#keys=128)   [genuinely periodic: ~chance]
  L=16:0.75 L=20:1.00 (#keys=N)              [in-sample memorization, NOT a periodic law]
  => MR's low-digit detour carries ~no info about the moving MIDDLE digit.

STEP (iii)  F_lambda = prod|cos pi(alpha - h/2^i)|, the heart of the MR saving:
  (A) MR-AVERAGED  Sum_h|F_L(h)| = 2^{eta*L} with eta ~ 0.35-0.38 < 1/2  over L=6..14
      => the MR sub-sqrt saving genuinely EXISTS in the h-aggregate.
  (B) single RESONANT ray h~(3/2)^j (the orbit = exp_sum.py product): 6.96e-22 at lam=60
      => decays, but it is ONE term: NO h-average is available for the geometric argument.

STEP (ii)-vdC  differenced correlation gamma(r)=mean (-1)^{x_{n+r} XOR x_n} (null 1-sigma ~ 0.0022):
  parity & pure-3^n digit both WHITE for r=1..21 (|gamma|<=~3 sigma).
  => vdC differencing removes NO structure (no degree to lower); matches the CLOSED vdC note.
```

**Reading.** STEP (iii) is the decisive one: the MR machinery's saving is real but is an **average over
`h`** (panel A, η≈0.37<1/2). The Antihydra geometric argument collapses that average to the **single resonant
ray** `h~(3/2)ʲ` (panel B), which is exactly the `exp_sum.py` product `∏|cos π{(3/2)ʲ/4}|`. That single ray
**does** tend to 0 — but that is the **annealed / Rajchman** statement (non-Pisot of 3/2, NONPISOT_FOURIER_CHAIN
Link A/B), i.e. the *already-provable easy part*. The orbit needs the **quenched** single-realization version
= Mahler. STEP (i) explains *why* there is only one ray (no localized perturbation ⇒ no truncation ⇒ no `h`
to sum over).

---

## 5. Findings (the requested deliverables)

**(1) Precise applicable MR theorems + citations.** MR cancellation theorems exist for `s_q(n²)` (Mauduit–
Rivat, Acta Math. 203, 2009), `s_q(p)` (Mauduit–Rivat, Annals 171, 2010), normality along `n²` (Müllner,
arXiv:1704.06472; *Normality along squares*), level of distribution of Thue–Morse (Spiegelhofer, Compositio
156, 2020, arXiv:1803.01689; arXiv:2504.02784), and Gowers-uniformity of automatic sequences (Konieczny,
AIF 69, 2019, arXiv:1611.09985; Byszewski–Konieczny–Müllner, arXiv:2002.09509). **None has the geometric
argument `3ⁿ` in its hypotheses; all require polynomial/prime/automatic structure (H1).**

**(2) Honest verdict on moving-digit-of-`3ⁿ`.** It is **(c) Mahler-equivalent.** Two structural mismatches
disqualify MR: geometric differencing `3ⁿ(3^r−1)` is not digit-localized (carry lemma hypothesis H1 fails),
and the object is a moving *middle single digit*, not a full/low digit sum (H2 fails). The only published
"powers" result is the **truncated** sum-of-digits of `aⁿ` (Liu–Mauduit, Acta Math. Hungar. 2022) — itself a
retreat from the open full-digit regime; the full digit behavior of `2ⁿ,3ⁿ` is acknowledged open.

**(3) Does MR's decomposition give ANY partial cancellation here?** **Yes, but only the part already known.**
The single MR component that transfers exactly is the digit Fourier transform `F_λ(h)=∏|cos π(α−h/2ⁱ)|`,
which along the geometric ray **is** the `exp_sum.py` product and yields the **annealed/Rajchman carry
balance** (non-Pisot of 3/2) — the easy, already-provable tier. MR adds **no new quenched cancellation**: the
geometric argument removes the `h`-average that is the source of MR's saving. Separately, MR cleanly
**localizes the obstruction inside the `T_n` recursion**: the additive injection `+2ⁿe_n` is MR-tame
(detour `s_{μ,λ}` = windowed digit block), the multiplicative `×3` is the Mahler wall.

**Net.** MR is *the right language* (it names the carry lemma, the detour, the `F_λ` product, and pinpoints
which half of the recursion is hard) but **not a tool that closes (K)**: it confirms, with a precise
mechanism, that the remaining gap is exactly Mahler / single-orbit equidistribution. Consistent with
PROOF_STATUS line (5) and NONPISOT_FOURIER_CHAIN Link C.

### Citations
- Gelfond, *Acta Arith.* 13 (1968) 259–265.
- Mauduit–Rivat, *La somme des chiffres des carrés*, Acta Math. 203 (2009) 107–148.
- Mauduit–Rivat, *Sur un problème de Gelfond: la somme des chiffres des nombres premiers*, Ann. of Math. 171 (2010) 1591–1646.
- Fouvry–Mauduit, *Math. Ann.* 305 (1996).
- Müllner, *The Rudin–Shapiro sequence and similar sequences are normal along squares*, arXiv:1704.06472.
- Spiegelhofer, *The level of distribution of the Thue–Morse sequence*, Compositio Math. 156 (2020), arXiv:1803.01689; arXiv:2504.02784.
- Konieczny, *Gowers norms for the Thue–Morse and Rudin–Shapiro sequences*, Ann. Inst. Fourier 69 (2019), arXiv:1611.09985.
- Byszewski–Konieczny–Müllner, *Gowers norms for automatic sequences*, arXiv:2002.09509.
- Liu–Mauduit (collab.), *The truncated sum-of-digits function of powers*, Acta Math. Hungar. (2022), doi:10.1007/s10474-022-01267-6.
- Mahler 3/2 / equidistribution: arXiv:2411.03468, arXiv:1806.03559; AEV normality arXiv:2510.11723.
- Geometric-digit context: *Collisions of digit sums in bases 2 and 3* arXiv:2105.11173; *Ternary digits of powers of two* arXiv:2511.03861.

*(Scripts: `mr_decomp.py`, `exp_sum.py`. Not committed.)*
