# Annealed vs Quenched data — testing whether annealed control transfers to the orbit (2026-06-28)

**Question (from `SESSION_2026-06-28_AEV.md` / `NONPISOT_FOURIER_CHAIN.md` Link C).**
The *annealed* even-density (i.i.d. Bernoulli weights ⇒ product Φ, controlled by ν_{2/3} decay /
non-Pisot) is provably ≈ 1/2. The *quenched* object (the orbit's OWN self-generated parity weights along
c₀=8) is the open one. This is the **lone analytic missing link**. Here we take DATA on exactly **where and
how much** the two diverge, and whether any partial transfer is visible.

**Objects (exact bigint, `aq_data.py`, run with `.venv/bin/python`):**
- **QUENCHED:** real orbit `h₀=8, h_{n+1}=⌊3h_n/2⌋ = h_n+(h_n>>1)`. Parity `r_n=h_n&1`, even-density
  `E_N=(1/N)#{n<N: h_n even}`. Non-halt target: counter `c=2·evens−odds ≥ 0` forever ⇔ liminf E ≥ 1/3.
- **ANNEALED (mean):** exact carry-imbalance product `Φ(N)=∏_{j<N}|cos(π{(3/2)^j/4})| = |E[(−1)^{r_n}]|`
  under i.i.d. Bernoulli(1/2) scenery (= ν̂_{2/3} sampled along ξ_N, NONPISOT Link B). ⇒ annealed mean
  even-density = 1/2 ± Φ(n)/2.
- **ANNEALED (single draw):** i.i.d. Monte-Carlo `T_{n+1}=3T_n+2^n e_n`, `e_n~Bern(1/2)`; its parity
  even-density — fluctuates 1/2 + O(1/√N) by CLT, autocorr ≈ 0.

All labels: **[PROVEN]/[OBSERVED]/[OPEN]**. Numbers are measured; the [OPEN] single-orbit
equidistribution is never asserted — only its empirical margin is reported. Zero false proofs.

---

## 1. Side-by-side even-density vs N  (run N = 2,000,000; quenched 1.17M-bit final h)

| N | E_q (quenched) | \|E_q−½\| | annealed mean Φ(N) | 1/(2√N) | \|E_q−½\|·2√N |
|---:|---:|---:|---:|---:|---:|
| 10 | 0.700000 | 0.200000 | 1.7e-03 | 0.158 | 1.265 |
| 30 | 0.566667 | 0.066667 | 1.1e-12 | 0.0913 | 0.730 |
| 100 | 0.510000 | 0.010000 | 4.9e-32 | 0.0500 | 0.200 |
| 300 | 0.510000 | 0.010000 | 1.1e-90 | 0.0289 | 0.346 |
| 1,000 | 0.499000 | 0.001000 | 2.1e-304 | 0.0158 | 0.063 |
| 3,000 | 0.508000 | 0.008000 | **0** (underflow) | 0.0091 | 0.876 |
| 10,000 | 0.495400 | 0.004600 | 0 | 0.0050 | 0.920 |
| 30,000 | 0.499833 | 0.000167 | 0 | 0.0029 | 0.058 |
| 100,000 | 0.501590 | 0.001590 | 0 | 0.00158 | 1.006 |
| 300,000 | 0.499360 | 0.000640 | 0 | 0.00091 | 0.701 |
| 1,000,000 | 0.499501 | 0.000499 | 0 | 0.00050 | 0.998 |
| 2,000,000 | 0.499468 | 0.000532 | 0 | 0.00035 | 1.506 |

- **[OBSERVED] The annealed mean is ≈1/2 to absurd precision.** Φ(N) = |E[(−1)^r]| under i.i.d. weights
  collapses: 1.7e-3 (N=10) → 1.1e-12 (N=30) → 1.1e-90 (N=300) → float-0 by N≈3000. The running-average
  annealed-mean even-density deviation bound `(1/2N)Σ Φ(n) = 5.5e-7`. This is the **non-Pisot ⇒ Rajchman ⇒
  annealed carry balance** chain [PROVEN, NONPISOT Link A+B], confirmed numerically: the annealed even-
  density is 1/2 with deviation decaying *faster than any power* (super-exponential here).
- **[OBSERVED] The quenched orbit does NOT sit on the annealed mean.** It fluctuates around 1/2 at the
  **1/√N scale**, not the (vanishing) Φ scale. The diagnostic `|E_q−½|·2√N` stays **O(1)** (0.06–1.5)
  across five decades of N — exactly the signature of a **single CLT-typical draw**, not the ensemble mean.

**Reading (the transfer geometry):** annealed-mean and quenched are two *different* functionals.
Annealed-mean = ensemble average ⇒ deviation Φ→0 super-fast. Quenched = ONE specific (Haar-null)
realisation ⇒ deviation ~ 1/√N. So `|E_q − annealed_mean| ≈ |E_q − ½| ~ 1/√N`. **The gap between them is
exactly "one typical draw's CLT fluctuation," not a systematic bias.**

---

## 2. Transfer test — perturbation or systematic divergence?

| metric | annealed mean | annealed single draw (MC) | quenched orbit |
|---|---|---|---|
| even-density limit | 1/2 (Φ→0) | 1/2 | 1/2 (observed) |
| dev. from 1/2 scale | Φ(N) → 0 (super-exp) | 1/(2√N) [CLT] | **~1/(2√N), ratio O(1)** |
| lag-1 parity autocorr | (deterministic) | −0.0007 ± 0.0038 | −0.00057 (≈ noise) |

Annealed i.i.d. Monte-Carlo (K=12 seeds, length 10⁵): mean dev `+0.00044`, **std `0.00137`** vs CLT
`1/(2√N)=0.00158` — match. Quenched `|E_q−½|` at the same N=10⁵ is `0.00159` — **same band**.

⇒ **[OBSERVED] No systematic divergence is visible.** The quenched even-density tracks the annealed
prediction up to O(1/√N) fluctuations across N=10…2×10⁶. The quenched orbit is *statistically
indistinguishable from a single typical i.i.d. draw* at the level of the even-density. This is the
"perturbation of annealed" picture, **not** a detectable block.

---

## 3. Correlation structure (what would break the transfer)

The transfer is broken in principle because the quenched weights are the orbit's own *correlated* past
parities. We measure how correlated they actually are.

**Parity autocorrelation (quenched, N=2×10⁶; noise floor 1/√N = 7.1e-4):**

| lag | autocorr | \|ac\|/noise |
|---:|---:|---:|
| 1 | −0.000568 | 0.80 |
| 2 | +0.000599 | 0.85 |
| 3 | +0.000332 | 0.47 |
| 4 | +0.000769 | 1.09 |
| 8 | −0.000643 | 0.91 |
| 16 | −0.000238 | 0.34 |
| 32 | −0.000205 | 0.29 |
| 64 | +0.000251 | 0.35 |
| 128 | −0.000031 | 0.04 |
| 256 | −0.000156 | 0.22 |
| 1024 | −0.001467 | 2.07 |

**Renewal gap D=v₂(3h−1) at odd steps (1,001,065 odd values; noise 1/√#odd = 1.0e-3):**
mean D = **1.9979** (geometric expectation 2.0), var D = 1.9984; autocorr at lags 1–256 all within
|ac|/noise ≤ 1.67.

⇒ **[OBSERVED] Both the parity sequence and the renewal-gap sequence are near-i.i.d.** Every autocorrelation
out to lag 1024 sits at the i.i.d. noise floor (|ac|/noise ≤ ~2, the expected scatter of many lags). The
self-generated weights carry **no detectable lag-correlation** — the very thing that distinguishes quenched
from annealed is empirically ≈ 0. The gap D matches the geometric(1/2) law of the annealed model (mean 2).

**Cross-check with `correlation_margin.py`:** the threshold lag-1 correlation needed to push the output
even-density down to 1/3 is `|ρ*| ≈ 0.74`; measured `|ρ| ≈ 0.0006` ⇒ **margin factor ~1000×**. The orbit is
nowhere near the correlation regime that could break the one-sided target.

---

## 4. Safety margin of the one-sided target E ≥ 1/3 (worst dip)

Run N=2×10⁶ (5×10⁶ run appended in §6 when complete):

- **counter c min over run = 0** (= its initial value; halt needs c=−1). c drifts up to **+996,805** at
  N=2×10⁶ (≈ +0.5/step). **[OBSERVED] never approached the halting boundary.**
- **cumulative even-density min (after burn-in 1000) = 0.493356**, margin over 1/3 = **+0.160**.
- **windowed even-density minima** (worst local dip):

| window W | min windowed E | margin over 1/3 |
|---:|---:|---:|
| 100 | 0.260000 | **−0.0733** |
| 1,000 | 0.433000 | +0.0997 |
| 10,000 | 0.483300 | +0.1500 |
| 100,000 | 0.496030 | +0.1627 |
| 1,000,000 | 0.499139 | +0.1658 |

⇒ **[OBSERVED]** The cumulative even-density (the object that actually controls halting, via c) holds a
**comfortable +0.16 margin** over 1/3 — it dips to ≈0.4934 worst, never near 1/3. Only the *smallest*
windows (W=100) momentarily dip below 1/3 (to 0.26), which is exactly the expected O(1/√W) tail of a fair
sequence and does **not** threaten the cumulative counter (min_c=0). The one-sided target is satisfied with
large empirical margin and the margin *grows* with window size (1/√W shrinkage).

---

## 5. Honest assessment — "almost there" or fundamentally blocked?

**[OBSERVED] At the level of all measurable statistics, the transfer is "almost there":**
1. quenched even-density tracks the annealed 1/2 up to O(1/√N) (Table §1, ratio O(1) over 5 decades);
2. the distinguishing feature — correlation of the self-generated weights — is **empirically ≈0** (parity
   & gap autocorr at the i.i.d. noise floor out to lag 1024; gap mean = 2.00 = annealed law);
3. the one-sided 1/3 target holds with a **+0.16 margin** and a 1000× correlation safety factor.

**[OPEN] But the gap is genuine and is exactly the known wall, not closed by this data.** The annealed
*mean* deviation vanishes super-exponentially (Φ); the quenched single realisation deviation is ~1/√N. The
transfer would require asserting the single Haar-null orbit is *typical* — i.e. effective equidistribution
of `{(3/2)^n}` for this one orbit. The data shows the orbit *behaves* typical to within measurement, but:
- "autocorr ≈ noise floor out to lag 1024" is an **[OBSERVED]** finite-lag, finite-N statement; it cannot
  rule out a o(1) long-range or arithmetic correlation that a proof must exclude (this is precisely
  NONPISOT Link C: decay of the annealed *mean* does not bound the quenched *realisation*);
- 1/√N typicality holds for a.e. realisation but the orbit is a single Haar-null point — the metric/typical
  theorems (Koksma, Aistleitner LIL/CLT) say **nothing** about it (SESSION_2026-06-28_AEV §J3).

**Verdict:** the data is **maximally encouraging short of a proof**. The quenched object is empirically a
**vanishingly small perturbation of the annealed** (no measurable correlation, CLT-typical fluctuations,
fat margin over 1/3). There is **no sign of a systematic block** — the only thing missing is the *single-
orbit typicality theorem* itself (= AEV Conj 1.6 floor-mirror fragment = effective `{(3/2)^n}`
equidistribution). The transfer is "almost there" in the precise sense that *every transferable statistic
has transferred*; what remains is not a new obstruction but the bare assertion of typicality for one
Haar-null point, which is the open Mahler/AEV core and is not deliverable by annealed (ν_{2/3}) control.

---

## 6. Longest run (N = 5,000,000) — worst-dip / margin update

Run N=5,000,000 (quenched ran 865s, final h has **2,924,816 bits**; final E_q = 0.499809).

**Even-density continues to track 1/2 at the 1/√N scale** (extending Table §1):

| N | E_q | \|E_q−½\| | annealed mean Φ | 1/(2√N) | \|E_q−½\|·2√N |
|---:|---:|---:|---:|---:|---:|
| 1,000,000 | 0.499501 | 0.000499 | 0 | 0.00050 | 0.998 |
| 2,000,000 | 0.499468 | 0.000532 | 0 | 0.00035 | 1.506 |
| 3,000,000 | 0.499779 | 0.000221 | 0 | 0.00029 | 0.766 |
| 5,000,000 | 0.499809 | 0.000191 | 0 | 0.00022 | **0.852** |

The diagnostic `|E_q−½|·2√N` remains **O(1)** out to N=5×10⁶ — the single-draw CLT picture holds at the
largest run. Running-avg annealed-mean deviation bound = 2.2e-7.

**Correlation stays at the i.i.d. noise floor** (N=5×10⁶, noise 4.5e-4): parity autocorr |ac|/noise ≤ 1.61
out to lag 1024; renewal gap over 2,500,953 odd steps has **mean D = 1.9992** (annealed law 2.0), autocorr
|ac|/noise ≤ 1.57. No correlation emerges at larger N.

**Safety margin (N=5×10⁶):**
- counter c min = **0** (its initial value); c drifts up to **+2,497,141** — never near halt boundary.
- cumulative even-density min (after burn-in) = **0.493356**, margin over 1/3 = **+0.160** (the worst
  cumulative dip occurs early and does not deepen with longer runs).

| window W | min windowed E | margin over 1/3 |
|---:|---:|---:|
| 100 | 0.250000 | −0.0833 |
| 1,000 | 0.429000 | +0.0957 |
| 10,000 | 0.475300 | +0.1420 |
| 100,000 | 0.495830 | +0.1625 |
| 1,000,000 | 0.499139 | +0.1658 |

⇒ **[OBSERVED]** The longest run reinforces §1–§5 unchanged: over 5×10⁶ steps the quenched orbit is a
CLT-typical, correlation-free perturbation of the annealed mean, the one-sided 1/3 target holds with
**+0.16 cumulative margin** (worst local dip only in W=100 windows, the expected 1/√W tail), and the
counter never approaches −1. **No systematic divergence appears at any scale tested.**
