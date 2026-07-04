# Blind-run #2: the harmonic-analysis family — measured, all predictions confirmed; the wall's second face (2026-07-05)

*Continuing the blind-run effectiveness method (`BLIND_EFFECTIVENESS_2026-07-05.md`) on a DIFFERENT family: harmonic
analysis / exponential sums on `x_n = frac(4·(3/2)^n) = (4·3^n mod 2^n)/2^n`. `(K)` `⟺` one-sided cancellation in the
Weyl sums `Σ e(k x_n)` (`BAKER_LINFORMS §0`). Predicted (stated before running): no power-saving (Weyl `~√N`),
discrepancy `~N^{-1/2}`, autocorrelations at the `1/√N` noise floor. **All three confirmed.** The payoff is a clean
**duality**: this family shows the SAME `(K)` as the arithmetic blind-run, but as its opposite face —
statistically-indistinguishable-from-random, vs. the 2-adic view's fully-deterministic-countdown. SOUNDNESS:
`[OBSERVED]` exact big-int `N=8000`; `(K)` `[OPEN]`; no machine decided.*

## (A) Weyl sums — no power-saving `[OBSERVED]`
`|S_N(k)| = |Σ_{n<N} e(k x_n)|` for `k=1,2,3,5,8`: `|S_N|/√N ∈ [0.70, 1.27]` — right at the random-walk scale;
`|S_N|/N ≈ 0.01` (decays like `1/√N` = **no cancellation beyond random**). Growth exponent `α=log|S_M|/log M ≈ 0.47`
across `M=500..8000` (`√N` is `0.5`). **No power-saving, no `k`-resonance.** Prediction confirmed — this IS the
equidistribution-rate `= (K)` wall, appearing as "equidistributes at exactly the random rate, no better."

## (B) Star discrepancy — random rate `[OBSERVED]`
`D*_N ≈ N^{-1/2}` (`D*/N^{-1/2}` = 0.95, 0.97, 0.80, 0.79 at `M=1000..8000`; matches the `√(½ loglog N / N)` random
baseline). No structured fast decay. (A mild `0.79` dip at the top two `M` — slightly *sub*-random — is non-monotone
and within finite-`N` noise; **not** a power-saving signal, not pursued.) Prediction confirmed.

## (C) Autocorrelation — noise floor `[OBSERVED]`
`s_n=(−1)^{b_n}`, `b_n=[x_n≥½]`: `C(h)=⟨s_n s_{n+h}⟩` oscillates in `[−0.019,+0.008]`, all `~1/√N` (`1/√8000≈0.011`)
= the noise floor; no decay *rate* because there is no genuine correlation to decay. `Σ_{h=1}^{199}|C(h)|=1.85`
(avg `≈0.0093≈1/√N`). `mean s_n=−0.013` ⇒ even-density `≈0.507`. Rajchman holds trivially (correlations are already at
measurement noise). Prediction confirmed.

## The duality — one wall, two faces `[synthesis]`
Two blind runs, two families, the same `(K)` — as **opposites**:

| | blind-run #1 (2-adic / arithmetic) | blind-run #2 (archimedean / harmonic) |
|---|---|---|
| face | **fully deterministic** countdown renewal | **statistically indistinguishable from random** |
| all content in | a single up-jump height law `P(h∣d=0)` | Weyl `√N`, discrepancy `N^{-1/2}`, corr. noise-floor |
| why unprovable there | up-jump law = single-orbit = `(K)` | no structure ⇒ harmonic tools have no purchase |

`(K)` is *simultaneously* a one-parameter deterministic renewal (2-adic) and a structureless random-looking sequence
(archimedean). The two "why no proof" reasons — **too-deterministic-but-one-free-orbit** and **too-random-to-grip** —
are the **same object's dual faces**. This is why neither a purely arithmetic (odometer/renewal) nor a purely harmonic
(Weyl/discrepancy) attack crosses: each sees only one face, and the crossing needs the coupling between them
(= effective single-orbit equidistribution = `P1′`).

## Verdict
**All harmonic-family predictions confirmed (3/3); calibration reinforced** — my "closed" verdicts on this family are
reliable. The blind run paid via the **duality synthesis** (2-adic determinism ⟷ archimedean randomness are one wall).
**No crossing.** `(K)` `[OPEN]`. No machine decided. No label upgraded.

## Reproduce
- `scratchpad/blind_harmonic.py` (`/opt/homebrew/bin/python3.13`, exact big-int, `N=8000`): `x_n=(4·3^n mod 2^n)/2^n`;
  Weyl `|S_N(k)|~√N`, `D*_N~N^{-1/2}`, `C(h)~1/√N`. Basis: `BAKER_LINFORMS.md` (Weyl = the `(K)` object; support-only),
  `BLIND_EFFECTIVENESS_2026-07-05.md` (run #1, the arithmetic face), `BB6_NO_STRUCTURE_THEOREM.md`, `NEW_MATH_PROGRAM.md` (P1′).
