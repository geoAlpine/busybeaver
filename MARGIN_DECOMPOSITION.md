# The factor-2 margin needs all-scale control — it buys no weaker discrepancy exponent (2026-06-26)
*Program: rank-1 specified-orbit genericity. Quantitative sharpening of `#2` via a cylinder-by-cylinder
decomposition of the avg-jump excess. `margin_exponent.py`. 0 false claims.*

## Setup
`avg jump = Σ_{k≥1} N_k/J`, `N_k/J = ` empirical frequency of the shrinking cylinder `{c'_j ≡ 1/3 mod 2^k}`
(Haar mass `2^{−k}`). Non-halt ⟺ `avg jump ≤ 2` ⟺ **excess** `:= avg jump − 1 = Σ_k D_k ≤ 1`, where
`D_k = N_k/J − 2^{−k}` is cylinder `k`'s signed discrepancy. The factor-2 margin is a **budget of 1** on `Σ_k D_k`.

## Two decompositions
**Real orbit (seed 8, `J = 2·10⁵`):** `avg jump = 1.0036`, excess `+0.0036` — it uses **0.36 %** of the budget.
The excess localizes to small `k` (`k ≤ 5`); the deep-excursion tail `Σ_{k>K} N_k/J = mean_j (v2_j − K)^+` sits at
`≤` its Haar value `2^{−K}` (ratio `1.00, 1.00, 0.99, 0.93, 0.90, 0.86` for `K=2..12`). The individual `D_k` are
at the **CLT noise floor** (`~1/√J ≈ 0.002`) — no decay exponent is extractable; they are generic fluctuations,
consistent with the i.i.d.-likeness finding.

**Adversarial orbit (`avg jump > 2`):** model the branch process as i.i.d. geometric `P(D=d)=(1−q)q^d`, so
`N_k/J = q^k`, `D_k = q^k − 2^{−k}`. For `q > ½` the excess is **positive at every `k`** and decays only like
`q^k`:

| avg jump | `q` | excess at k=1..6 | tail `k>8` | total |
|---|---|---|---|---|
| 1.0 (Haar) | 0.500 | 0 0 0 0 0 0 | 0 | 0 |
| 2.0 | 0.667 | +.17 +.19 +.17 +.14 +.10 +.07 | +0.071 | +0.997 |
| 3.1 | 0.756 | +.26 +.32 +.31 +.26 +.22 +.17 | +0.292 | +2.065 |

The adversarial excess is **spread across all scales**; the deep tail (`k>8`) contributes materially once
`avg jump > 2`.

## Verdict (sharpens `#2` quantitatively)
> The realized small-`k` localization is a property of the **generic** orbit, **not** of the margin. To rule out
> budget overflow the proof must control cylinder frequencies at **all** `k` (an adversary inflates `q^k` at every
> scale, deep tail included). **The factor-2 margin relaxes the *threshold* (`Σ ≤ 1` vs `→ 0`), not the
> *scale-range* of control — it is the same discrepancy class as equidistribution, with no weaker exponent.**

This is the quantitative form of `#2` ("weaker target, equi-difficult"): now pinned not as tool-relative but as a
direct statement about the **required control** — all-scale one-sided cylinder-frequency bounds. It also **corrects
a naive hope** ("the margin localizes to small `k`, so a finite-scale input suffices"): false — small-`k` is where
the *generic orbit's* tiny excess sits, while the *margin's* adversarial failure mode spans every scale. The
`EXPERT_ASK` Q0 "small-`k`" hint has been annotated accordingly.

## Honest caveats
- Empirical: one real orbit + an i.i.d.-geometric adversary model. The `n→∞` per-`k` limit `D_k → 0` is the open
  problem, untouched.
- The i.i.d.-geometric adversary is a *model* of how excess distributes; the actual reduction's adversaries
  (constructed earlier via inverse branches, `avg jump = 3.1`) confirm the same all-scale spread.

## Where this leaves the margin (and #3)
No internal weakening remains: the one-sided target needs all-scale control, so a future tool must deliver
**one-sided constant-factor anti-concentration of a specified orbit's cylinder frequencies at every scale** — the
refined `#3` design spec, now with the scale-range explicitly closed (it cannot be finite-`k`). The only relaxation
the margin genuinely buys is the constant (`2×` vs `1×`, two-sided→one-sided), already recorded.
