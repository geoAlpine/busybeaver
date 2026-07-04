# Blind-run effectiveness measurement — run three "predicted-closed" attacks WITHOUT pre-filtering, measure prediction accuracy (2026-07-05)

*Method (user): instead of skipping attacks I predict will close (risk: self-fulfilling dismissal), **run them blind**
and use the run to measure my prediction accuracy — and catch premature NO-GOs. Ran three routes I had labelled
"closed at the seam": (1) occupancy tail `f_k`/moments, (2) deep-entry spacing/repulsion, (3) potential-drift search
for a `−d²` supermartingale. Outcome: **all three top-line verdicts CONFIRMED** (my "closed" calls are reliable), but
the blind run **(a) exposed a cleaner mechanism** (the depth process is an exact countdown renewal) and **(b) caught a
phrasing error** (deep visits *attract* 33×, not iid). SOUNDNESS: `[OBSERVED]` exact big-int `N=2·10⁵`; `(K)` `[OPEN]`;
no machine decided.*

## (1) Tail `f_k` and moments — prediction CONFIRMED precisely `[OBSERVED]`
`f_k = freq(d_n ≥ k)` vs the iid-geometric null `2^{-(k-1)}`: ratio is **flat ≈ 0.50** for `k=1..12` (i.e.
`f_k ≈ 2^{-k}`, the induced-map factor), then climbs (0.68, 0.86, 0.98, 1.31 at `k=13..16`) — **finite-`N` tail noise**
(few samples: `freq~10^{-4}`). Moments: `E[d]=0.994`, `E[d²]=2.95`, `Σ N_k=1.000`, `Σ k N_k=0.994`, `Σ k² N_k=2.95`,
max depth `20`. Exactly the geometric `= (K)` picture; empirically finite but with **no a-priori source** (as predicted).

## (2) Deep-entry spacing — prediction PARTLY WRONG, but it closes the route HARDER `[OBSERVED]`
I had said "iid-like, min-gap=1." Measured: mean gap **matches** iid at every threshold (`thr≥4`: 16.3 vs 16.3;
`≥6`: 68.4 vs 68.4; `≥8`: 282 vs 284) and `min_gap=1` as said — **but** adjacent-deep pairs (`d_n,d_{n+1}≥6`) number
**1422 vs iid-expected 42.75 — a 33× excess (short-range ATTRACTION, not repulsion).** The surprise: this attraction
is the **deterministic countdown cascade** (a peak descends `d,d−1,d−2,…`, so consecutive steps near a peak are both
deep). It makes a covering / separation upper bound **more** hopeless, not less — a repulsion `min-gap ≳ 2^k` (needed
for summability, `EK2_TAIL_SEPARATION`) is the exact opposite of the observed clustering. **The route closes harder;
the phrasing "iid" was imprecise (iid at medium scale + deterministic attraction at short scale).**

## (3) Potential-drift search — prediction CONFIRMED, mechanism laid bare `[OBSERVED, essentially exact]`
Searched weights `w(d)∈{d, d², 2^d}` for a net negative drift bounding `Σd²`. Result — the conditional drift is
**deterministic**: from depth `d≥1`, `E[Δw | d]` is **exactly** `w(d−1)−w(d)` with ~zero variance (`w=d`: `−1.000`
∀`d≥1`; `w=d²`: `−(2d−1)` exactly; `w=2^d`: `−2^{d-1}` exactly). Meaning:
> **The depth process `d_n` is an EXACT countdown renewal: `d_{n+1}=d_n−1` deterministically whenever `d_n≥1`, then a
> fresh up-jump from `d=0`.** All content — every moment, the max, the tail — lives **solely** in the **up-jump height
> law** `P(jump to h | d=0)`, and that law **is** the single-orbit occupancy `= (K)`.
Every `w` telescopes to overall drift `0` (the `d=0` up-jump exactly balances the countdown descent — e.g. `w=d²`:
`+2.975` from `d=0` balances `Σ−(2d−1)`). **No potential yields a net `−d²` drift; the second moment is the up-jump
law's variance = the conclusion, not an input.** Prediction confirmed, with the cleanest statement yet of *why*.

## Meta — the blind method's value `[the point of the exercise]`
**My "predicted-closed" verdicts are reliable** (3/3 top-line confirmed → I am not discarding live routes). **Yet the
blind run still paid**: it produced a **sharper structural theorem** (depth = deterministic countdown renewal; the
entire open problem is one up-jump renewal law), and it **caught a phrasing error** (attraction, not iid). So running
predicted-dead attacks is not wasted even when the verdict holds — it upgrades *mechanism* and *precision*. **Verdict:
no crossing** (the up-jump law is `(K)`), but a genuine calibration + sharpening. **Halting `[OPEN]`. No machine
decided. No label upgraded.**

## Reproduce
- `scratchpad/blind_effectiveness.py` (`/opt/homebrew/bin/python3.13`, exact big-int, `N=2·10⁵`): Antihydra
  `c₀=8,c→⌊3c/2⌋`, `d_n=v₂(c_n−1)`; tail/moments, deep-entry spacing + 33× adjacency, deterministic countdown drift.
  Basis: `MINPROP_RUNS.md` (countdown self-limiting), `EK2_TAIL_SEPARATION.md` (min-gap=1 wall),
  `EK2_SECOND_BUDGET.md` (0=0 telescope), `RUNCEILING_DIOPHANTINE_NOGO_2026-07-05.md`, `PROOF_TOOL_ATTEMPT_2026-07-04.md`.
