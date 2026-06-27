# Wall (B) refined target: structure of the digit–carry decorrelation a_n ⊥ b_n (2026-06-28)

Angle: **structural + literature framing of the digit–carry decorrelation**. The refined wall-(B)
binding object (`SESSION_2026-06-28_WALL_B.md`, `WALL_B_WHICH_PART.md`) is the **asymptotic
orthogonality** of two digital functions of the *same* 3/2-system:

> `A_r = (1/N) Σ (−1)^{a_n}(−1)^{b_n} → 0`,  with
> `a_n = bit_n(8·3ⁿ)` = `1[{4·(3/2)ⁿ} ∈ [½,1)]` — **explicit, deterministic** top digit;
> `b_n = bit_n(T_n)`, `T_{n+1}=3T_n+2ⁿr_n`, `r=a⊕b` — **self-generated** carry digit.

This is WEAKER than balancing either factor: it is a *correlation* statement, not an equidistribution
statement. Script: `wallb_decorr.py` (exact big-int, `.venv`). Zero false proofs; all numerics carry a
`1/√N` null band and are labelled [OBSERVED].

---

## 1. Precise framing: this IS a "correlation of two digital functions" [PROVEN framing]

Both factors are *digital functions read at the moving position n*:
- `a_n` is digit `n` of the explicit integer `8·3ⁿ`. Its leading Fourier mode is `e({4(3/2)ⁿ})`, i.e. a
  function of the **single** phase `θ_n := {4·(3/2)ⁿ}` — one point of the Mahler orbit `{(3/2)ⁿ}`.
- `b_n` is digit `n` of `T_n`. By the identity in `exp_sum.py`,
  `T_n/2^{n+1} = (1/4) Σ_{j≥0} r_{n−1−j} (3/2)ʲ  (mod 1)`,
  so its leading mode is `e((1/4)Σ_j r_{n−1−j}(3/2)ʲ)` — a function of a **(3/2)ʲ-weighted sum of the
  past bits** (the Mauduit/Korobov object).

So `A_r → 0` is literally: **the explicit single-phase top digit is asymptotically uncorrelated with a
(3/2)ʲ-weighted accumulator of the self-generated past bits, both of the same 3/2-orbit.** It is a
correlation of two digital functions, in the sense of Bésineau–Kim / Drmota joint distribution — but
with two structural twists (below) that put it *outside* the existing theorems.

---

## 2. Literature on correlation / joint distribution of digital functions [survey, OPEN for our case]

The matching body of work is "statistical independence / joint distribution of digital functions":

- **Bésineau (1972)** introduced statistical independence of sets defined by sum-of-digits functions; a
  weak error term for the joint distribution of `s_{q₁}, s_{q₂}` in two bases. **D.-H. Kim** later
  obtained the full statement (sharp error term). [Bésineau, *Indépendance statistique d'ensembles liés
  à la fonction "somme des chiffres"*, Acta Arith. 20 (1972); Kim, *On the joint distribution of
  q-additive functions in residue classes*, J. Number Theory 74 (1999).]
- **Drmota**, *The joint distribution of q-additive functions*, Acta Arith. 100 (2001) 17–39 — a local
  limit theorem for `(s_{q₁}(n), s_{q₂}(n))`; **Drmota–Schoissengeier**, *Digital expansion with respect
  to different bases*, Monatsh. Math. 138 (2003) 31–59; **Drmota–Gutenbrunner** (function-field analogue,
  JTNB 17 (2005) 125–150).
- **Drmota–Mauduit–Rivat**, *Prime numbers in two bases*, Duke Math. J. 169 (2020) 1809–1876 — strongly
  q-multiplicative functions in **two coprime bases** are statistically independent **along primes**.
- **Hofer–Iacò–Tichy** and the Tichy school (e.g. Iacò–Paštéka–Tichy 2015): correlation / uniform
  distribution of `(q₁,q₂)`-multiplicative functions, Riesz-product methods, **mutual singularity of the
  digit spectra in multiplicatively independent bases**.

**The decisive structural point.** *Every* one of these decorrelation results draws its independence from
**multiplicative independence of two DIFFERENT bases** `q₁, q₂` (e.g. 2 and 3, `log q₁/log q₂ ∉ ℚ`),
realized via Riesz products / mutual singularity of the two spectral measures. Our object has:
1. **One base (q=2) and one multiplier (3/2)** — `a_n` and `b_n` are BOTH base-2 digits driven by the
   SAME `3/2`. There is no second incommensurable base to supply independence. The Bésineau–Kim /
   DMR / Hofer–Iacò–Tichy mechanism (arithmetic incommensurability of bases) **does not apply**.
2. **Same position n** (the moving middle digit `bit_n`), not a digit *sum* over all positions, and one
   factor is **self-generated** (carry of the orbit's own parity), not a fixed q-additive function.

**Verdict.** `a_n ⊥ b_n` is the *same KIND of question* the joint-distribution-of-digital-functions
literature answers, but it is **not an instance of any existing theorem**: the published decorrelation
engines need two multiplicatively-independent bases, whereas here both digital functions live in the
**same 3/2-system**. So this is genuinely outside Bésineau/Kim/Drmota/Hofer–Iacò–Tichy — consistent with
the `ATTACK_MAUDUIT_RIVAT.md` verdict that the single-multiplier geometric case is the open frontier
(arXiv:2504.18192 Problem 3 = non-integer base). [OPEN]

---

## 3. A mechanism making a_n ⊥ b_n weaker than full equidistribution [CONDITIONAL — innovation/phase-lag]

There is a real structural reason the decorrelation should be *easier* than balancing either factor, and
it is NOT base-incommensurability (which is unavailable). It is a **phase-lag / innovation** structure:

- `a_n` is a function of the **newest** phase `θ_n = {(3/2)ⁿ}` ALONE, and — crucially — `a_n` is an
  **exogenous deterministic sequence** (depends only on `8·3ⁿ`, not on the orbit's bits).
- `b_n` is a function of the **weighted accumulated past** `(1/4)Σ_{j≥1} r_{n−1−j}(3/2)ʲ`, i.e. of the
  σ-field `F_{n−1}` generated by `r_0,…,r_{n−1}`. The newest phase `θ_n` enters `b_n` only through the
  *largest-lag* term, which mod 1 is the high-frequency / Mahler tail.

Hence `A_r = (1/N)Σ (−1)^{a_n}·(−1)^{b_n}` couples a **fixed structured sequence** (the `θ_n`-driven top
digit) against a **self-generated accumulator of the past**. The natural sufficient condition is the
**conditional first-moment / innovation** property
> `E[(−1)^{a_n} | F_{n−1}] = o(1)` on average  (the newest top-digit phase is asymptotically balanced
> *given* the accumulated carry history),

which yields `A_r → 0` by `(−1)^{b_n}` being `F_{n−1}`-measurable and the tower property — a
**martingale-difference / orthogonality-to-the-past** statement. This is **strictly weaker than full
equidistribution of `θ_n`**: it asks only that the *conditional* mean of one digit vanish against a
specific (carry-weighted) test function, not that `{(3/2)ⁿ}` equidistribute against *all* intervals.

**Honest status [CONDITIONAL].** This re-expresses the target as "newest phase decoupled from the
weighted past" (innovation/freshness) rather than "each factor equidistributes." It is a genuine
*weakening of the requirement*; it is NOT a proof, because establishing the conditional balance of the
single phase `{(3/2)ⁿ}` against the carry filtration still touches the same `(3/2)ⁿ` orbit (the closed
loop re-injects `a` into `b` via `r=a⊕b`). The `coupling_brick` evidence (parity decorrelated from every
*provable* surrogate; carry has sensitive dependence ≈ chaotic) says no *local* coupling realizes this —
only a global/measure (innovation) decoupling. So the mechanism is "innovation-type decorrelation,"
weaker than equidistribution but still anchored on the Mahler phase.

---

## 4. Numerical cross/lagged-correlation findings [OBSERVED, N=200000, null band 1/√N=0.00224]

`wallb_decorr.py`:

**(a) Cross-correlation A_r, sqrt-cancellation.** `A_r·√M` stays O(1) across scales:
| M | A_r | A_r·√M |
|---|---|---|
| 1000 | −0.0020 | −0.06 |
| 3000 | +0.0160 | +0.88 |
| 10000 | −0.0092 | −0.92 |
| 30000 | −0.0003 | −0.06 |
| 100000 | +0.0032 | +1.01 |
| 200000 | +0.0004 | +0.17 |

`A_r·√M` is bounded and sign-oscillating ⇒ **`A_r` decays at the √-cancellation rate, like two
INDEPENDENT balanced digital functions.** (The naïve log-log slope −1.18 is an artifact of `|A_r|`'s
zero-crossings, not a true rate; `A_r·√M = O(1)` is the faithful diagnostic.)

**(b) Lagged sign-correlation `g(k)=mean (−1)^{a_n}(−1)^{b_{n+k}}`, k=−12..+12.** All 25 lags are white:
every `|g(k)| < 3σ` (extreme = +2.29σ at k=−11, −2.06σ at k=+3, fully expected over 25 lags). The
on-lag value `g(0)=+0.0004=+0.17σ`. ⇒ **No short-range phase-lag resonance** between the explicit top
digit and the carry at any small lag; the decorrelation has **no detectable short-range structure**.

**(c) a_n vs INDEPENDENT digital-function surrogates** (replace b by genuinely independent digital fns):
| surrogate for b | corr(a, ·) | σ |
|---|---|---|
| **b (real self-gen carry)** | **+0.00037** | **+0.17** |
| Thue–Morse | −0.00275 | −1.23 |
| Rudin–Shapiro | +0.00333 | +1.49 |
| indep-scenery (3/2)ʲ carry | −0.00156 | −0.70 |

The real self-generated carry's correlation with `a_n` is **the same order (in fact smaller) than that of
genuinely independent digital functions.** ⇒ **Cross-correlation-wise, the real `b_n` is statistically
indistinguishable from an independent digital function.** There is no fine conspiracy and no resonance;
`a_n ⊥ b_n` behaves empirically exactly like "two independent balanced digital functions."

---

## 5. Returned conclusions (the three asks)

1. **Does digit–carry decorrelation match a known digital-function-correlation theorem?**
   It is the *same kind* of object as the Bésineau–Kim / Drmota / Hofer–Iacò–Tichy "joint distribution /
   statistical independence of digital functions" results, **but it is NOT an instance of any of them.**
   Those theorems get independence from **two multiplicatively-independent bases** (Riesz products /
   mutual singularity of spectra); our `a_n, b_n` are **both base-2 digits of the SAME 3/2-system at the
   SAME position n**, with one factor self-generated — no second base, so the literature mechanism is
   unavailable. This places `a_n⊥b_n` squarely on the single-multiplier geometric frontier
   (arXiv:2504.18192 Problem 3; matches `ATTACK_MAUDUIT_RIVAT.md`). [OPEN]

2. **Mechanism making a_n⊥b_n weaker than full equidistribution?**
   Yes, an **innovation / phase-lag** mechanism: `a_n` reads the single newest phase `{(3/2)ⁿ}` (and is
   exogenous), while `b_n` is a `(3/2)ʲ`-weighted accumulator of the past (`F_{n−1}`-measurable). The
   sufficient condition is the **conditional balance** `E[(−1)^{a_n} | F_{n−1}] = o(1)` (newest phase
   decoupled from the carry-weighted past) — a martingale-difference orthogonality that is **strictly
   weaker than full equidistribution** of either factor. [CONDITIONAL — a re-routing, not a proof; the
   closed loop `r=a⊕b` re-anchors it on the same `(3/2)ⁿ` Mahler phase, and `coupling_brick` shows only a
   global/measure (not local) decoupling can realize it.]

3. **Numerical cross/lagged findings.** `A_r·√M = O(1)` (√-cancellation, independent-like); all 25 lagged
   correlations white (`<3σ`, on-lag +0.17σ) ⇒ no short-range structure; and `corr(a, real b)=+0.17σ` is
   ≤ `corr(a, Thue–Morse/Rudin–Shapiro/indep-carry)` ⇒ the self-generated carry is cross-correlation-
   indistinguishable from a genuinely independent digital function. **Empirically `a_n ⊥ b_n` is an
   instance of "two independent balanced digital functions," with no resonance or conspiracy.** [OBSERVED]

Scripts: `wallb_decorr.py`, `exp_sum.py`, `coupling_brick.py`. Not committed.
