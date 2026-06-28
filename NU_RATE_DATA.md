# Effective Fourier-decay rate of ν_{2/3} — DATA (2026-06-28)

Object: `ν̂_{2/3}(ξ) = Π_{j≥0} cos(2π ξ (2/3)^j)`. 3/2 non-Pisot ⇒ Rajchman (`→0`, [PROVEN], Erdős–Salem).
This file MEASURES the RATE: is it polynomial (power law `|ν̂|≲|ξ|^{-a}`) or only logarithmic?
Script: `nu_rate_data.py` (run with `.venv/bin/python`). Soundness: all magnitudes use EXACT rational
phase reduction `{ξ(2/3)^j}=(ξ·2^j mod 3^j)/3^j` (no fp argument-reduction loss even at ξ=10^15);
mpmath cross-check agrees to all printed digits. Numerics only — no proof; labels [OBSERVED]/[PROVEN]/[OPEN].

---

## 1. Generic-ξ decay over 14 decades (ξ = 10 … 10^15, exact)  [OBSERVED]

| ξ | \|ν̂_{2/3}(ξ)\| | log10 |
|---|---|---|
| 10 | 1.557e-03 | -2.808 |
| 10^2 | 4.592e-08 | -7.338 |
| 10^3 | 4.121e-06 | -5.385 |
| 10^4 | 1.956e-09 | -8.709 |
| 10^5 | 1.477e-12 | -11.831 |
| 10^6 | 1.530e-11 | -10.815 |
| 10^7 | 5.367e-10 | -9.270 |
| 10^8 | 2.945e-15 | -14.531 |
| 10^9 | 9.013e-19 | -18.045 |

**Global power-law fit** `log|ν̂| = c − a·log|ξ|` over 700 log-spaced integer ξ in [10,10^15]:
**a = 1.713, C ≈ 0.0149, R² = 0.892.**

**Slope drift (local exponent per decade):**

```
[1,2] 1.41  [2,3] 1.69  [3,4] 1.21  [4,5] 1.72  [5,6] 1.60  [6,7] 1.19  [7,8] 0.79
[8,9] 1.68  [9,10] 2.62 [10,11] 3.92 [11,12] 1.90 [12,13] -0.62 [13,14] 1.62 [14,15] -1.64
```

Reading: the **average/envelope** decay is power-like with exponent ≈ 1.7, but pointwise the decay is
**ERRATIC** — local exponents swing from −1.6 to +3.9, including **negative** decades (|ν̂| *increases*
from 10^6→10^7: 1.5e-11→5.4e-10). So there is NO clean *pointwise/uniform* power law; there are
slow ("bad", near-resonant) frequencies. Crucially the local slope does **not systematically drift toward
0** as ξ grows — it bounces around ≈1.7 — so the data does NOT look sub-polynomial (logarithmic) either.
The erratic slow frequencies are exactly the phenomenon Varjú–Yu prove (decay can be as slow as
logarithmic along *a* subsequence); the envelope/typical decay is power-like.

---

## 2. The structured subsequence ξ_N = (3/2)^N/8  +  identity with Φ(N)  [PROVEN identity]

`ξ_N = (3/2)^N/8 = 3^N/2^{N+3}` (dyadic ⇒ exact). Algebraically `ξ_N(2/3)^j = (3/2)^{N−j}/4`, so
`|ν̂_{2/3}(ξ_N)| = Π_{k≤N}|cos(π(3/2)^k/4)| = Φ(N)·C`, where `Φ(N)=Π_{k=0}^{N}|cos(π{(3/2)^k/4})|`
is the **annealed carry product** (`exp_sum.py`) and `C=Π_{k<0}|cos(π(2/3)^{|k|}/4)|` is a convergent
constant tail.

| N | \|ν̂(ξ_N)\| | Φ(N) | ratio |
|---|---|---|---|
| 5 | 2.300e-02 | 2.969e-02 | 0.7748 |
| 10 | 3.425e-04 | 4.420e-04 | 0.7748 |
| 20 | 1.607e-08 | 2.074e-08 | 0.7748 |
| 40 | 1.411e-15 | 1.821e-15 | 0.7748 |
| 80 | 1.735e-26 | 2.239e-26 | 0.7748 |
| 160 | 4.540e-49 | 5.860e-49 | 0.7748 |
| 320 | 2.617e-97 | 3.377e-97 | 0.7748 |

**Ratio = 0.7748, constant to 4 digits across N=5…320 ⇒ identity `|ν̂(ξ_N)| = 0.7748·Φ(N)` confirmed
(NONPISOT_FOURIER_CHAIN Link B).** So the annealed carry product *is* ν̂_{2/3} sampled on this sparse
arithmetic subsequence.

---

## 3. Rate of Φ(N) in N — THE DISCRIMINATOR  [OBSERVED, log-space, N→30000]

Since `ξ_N ~ (3/2)^N` grows exponentially, the subsequence cleanly separates the two hypotheses:
- power law in ξ (`|ν̂|~ξ^{-a}`) ⇔ `logΦ(N) ~ −a·log(3/2)·N` (LINEAR in N),
- logarithmic in ξ (`|ν̂|~(log ξ)^{-b}`) ⇔ `logΦ(N) ~ −b·log N` (linear in log N).

Per-term decrement is `log|cos(π{(3/2)^k/4})|`; if the phases `{(3/2)^k/4}` equidistribute then the running
mean `logΦ(N)/N → ∫_0^1 log|cos πu| du = −log 2 = −0.69315` (integral verified numerically), giving a power
law in ξ with **a = log2/log(3/2) = 1.7095**.

Running mean `logΦ(N)/N` (→ −log2):  N=99: −0.728 · N=990: −0.699 · N=9950: −0.691 · N=30000: −0.687.

- **Fit A** `logΦ = α − s·N`:  s = 0.68609/term ⇒ **a = s/log(3/2) = 1.692**, **R² = 0.999984.**
- **Fit B** `logΦ = β − b·log N`:  b = 1684, **R² = 0.592.**
- Local slope `−dlogΦ/dN` across windows: [10,100] 0.686 · [100,1k] 0.675 · [1k,10k] 0.684 · [10k,50k] 0.685
  — **rock-steady ≈ 0.68, NO drift toward 0.**

**Verdict (subsequence): clean POWER law in ξ, exponent a ≈ 1.69 (→ theoretical 1.7095 = log2/log(3/2)),
R² = 0.99998, no slope drift.** Logarithmic fit is decisively rejected (R² 0.59 vs 0.99998).
Caveat: this clean power law *is* the numerical statement that `{(3/2)^k}` equidistributes = **Mahler/AEV
(OPEN)**. `logΦ(N)/N → −log2` is exactly that equidistribution.

---

## 4. Comparison: generic-ξ vs (3/2)^N/8 subsequence  [OBSERVED]

- **Same exponent** ≈ 1.71 = log2/log(3/2): generic global fit a=1.713; subsequence a=1.69→1.7095.
- **Very different quality:** subsequence is a CLEAN power law (R²=0.99998, constant local slope);
  generic ξ is ERRATIC (R²=0.89, local exponents −1.6…+3.9, slow/near-resonant frequencies). The common
  exponent is the same constant `∫log|cos|/log(3/2)` governing the average decay; the subsequence happens to
  realize it cleanly because `(3/2)^k` cycles through the phase uniformly.

---

## 5. Citable effective-rate theorems & what provably applies to 2/3

| Result | Hypothesis on λ | Rate | Covers λ=2/3? |
|---|---|---|---|
| Erdős–Salem dichotomy | 1/λ non-Pisot | Rajchman (→0), **no rate** | YES (qualitative only) |
| **Kershner (1936)** | λ = p/q **rational**, q>1 | **logarithmic** (class D_{1,log}) | **YES — directly** |
| **Varjú–Yu** (arXiv:2004.09358) | ratios = powers of λ, 1/λ algebraic, **not Pisot, not Salem** | **≥ logarithmic; SHARP** (∃ freq subseq with only log decay) | **YES — directly** |
| Dai–Feng–Wang (2007) | 1/λ a **Garsia number** (algebraic *integer*, all conjugates >1, \|const term\|=2) | **power** `\|ξ\|^{-a}` | **NO** — 3/2 not an algebraic integer |
| Streck (2023) | wider but still **special algebraic** ratios (and a.e./thin exceptional set for the generic statement) | power | **NO** — single value 2/3 not reachable |
| Solomyak (a.e.) | outside a **zero-dimensional** exceptional set of ratios | power | **NO** — a.e. cannot specialise to 2/3 |

**Best citable rate provably applying to ν_{2/3}: LOGARITHMIC** (Kershner, because 2/3=p/q rational;
independently Varjú–Yu, because 1/λ=3/2 is algebraic-non-Pisot-non-Salem and the ratios are powers of λ).
The literature consensus: for rational λ / ratios that are inverses of integers, "logarithmic decay is what
one should expect." **No citable theorem gives a POWER rate for the specific value 2/3** — every power-decay
theorem needs 1/λ to be an algebraic integer (Garsia) or restricts to a.e./thin-complement classes, and
3/2 (rational, not an algebraic integer) is explicitly outside all of them. Varjú–Yu even prove the
logarithmic bound is *sharp* for this class along a subsequence — matching the erratic slow frequencies in §1.

---

## 6. Honest verdict: polynomial vs logarithmic

- **DATA:** strongly supports **POLYNOMIAL** decay with exponent **a ≈ 1.71 = log2/log(3/2)**, NOT
  logarithmic. The decisive evidence is the subsequence (§3): `logΦ(N)` is linear in N (R²=0.99998) with a
  constant per-term slope ≈ log2 and **no drift toward 0** — the signature of genuine power decay, not of a
  logarithmic law masquerading as a power over a finite range. Generic ξ (§1) is erratic but its envelope is
  also ≈ ξ^{-1.71}, with local exponents that do not trend to 0.
- **BUT** this empirical power law is precisely the numerical manifestation of `{(3/2)^k}` equidistribution
  = **Mahler's 3/2 problem / AEV normality, OPEN.** `logΦ(N)/N → −log2` *is* that equidistribution
  statement; the data exhibits it but does not prove it.
- **CITABLE:** the only rate that provably holds for ν_{2/3} is **logarithmic** (Kershner / Varjú–Yu).
  The effective **power** rate — the ingredient flagged missing by the AEV reading — is **OBSERVED (a≈1.71)
  but NOT provable from any citable theorem for the specific value 2/3.**
- **Bottom line (consistent with NONPISOT_FOURIER_CHAIN Link C and SESSION_2026-06-28_AEV):** the missing
  effective power-decay rate is empirically real and clean along the Antihydra-relevant subsequence
  (3/2)^N/8, with exponent a = log2/log(3/2) ≈ 1.71, but it sits on the open Mahler/AEV equidistribution and
  no theorem in the literature delivers it for 2/3. Provable today = logarithmic only.

### Citations
- Erdős (1939) / Salem (1944) — Rajchman ⇔ 1/λ non-Pisot. Survey: Li–Sahlsten arXiv:1910.03463;
  Peres–Schlag–Solomyak "Sixty Years of Bernoulli Convolutions".
- Kershner (1936) — rational λ=p/q ⇒ logarithmic decay (D_{1,log}); see Solomyak survey.
- Varjú–Yu, "Fourier decay of self-similar measures and self-similar sets of uniqueness," arXiv:2004.09358
  — ≥ logarithmic decay when ratios are powers of λ, 1/λ algebraic non-Pisot non-Salem; sharpness along a subsequence.
- Dai–Feng–Wang (2007) — power decay for Garsia numbers (1/λ algebraic integer, conjugates >1, |const term|=2).
- Streck (2023), "On the Fourier decay and the dimension of self-similar measures" (Cambridge) — power decay
  for wider special algebraic ratios / generic complements.
- Mahler's 3/2 problem; AEV normality arXiv:2510.11723.
