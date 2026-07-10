# o4 bespoke exponential-sum / frequency build — the freq↔S dictionary, the run-cap→frequency margin, and the concrete non-Pisot regress (2026-07-10)

*A genuinely-new tool: a bespoke exponential-sum estimate built for the ACTUAL integer sequence W_n of the o4 orbit
(seed G₀=43), never done here (the digit-bridge scanned literature; nobody BUILT S for this sequence). Exploits the
large margin (need freq{3|W_n} ≤ 4/5, annealed 1/3). Interpreter `.venv` python, exact big-int; every structural
identity assertion-checked in `o4_expsum_frequency.py` (all passed, N=2×10⁵). STRICT labels. NOT committed.*

---

## 0. One-line verdict

**[INSUFFICIENT — does not decide, no label upgraded].** Three NEW artifacts, all verified: (a) an **exact
freq↔exponential-sum dictionary** `#1 = N/3 + (2/3)Re(S₁)` that translates the fatal threshold into the crisp
analytic target **`Re(S₁(n))/n < 7/10`** — decide o4 by proving the o4 orbit's cube-root-of-unity sum stays below
**70 % of trivial** (a huge slack: even a weak nontrivial cancellation suffices); (b) the **run-cap→frequency margin
is exactly zero** — the forced-exit density is not bounded below, so the proven run-cap yields no unconditional
frequency bound at all; (c) a **concrete van-der-Corput regress identity** pinning why the bespoke sum admits no
*effective* cancellation. The real orbit exhibits clean **square-root cancellation** (fit exponent α = 0.491), so
`|S₁|/N → 0` like `N^{-1/2}` ≪ 0.7 empirically — but no *provable* rate exists, blocked at the δ₋₁₄ orbit
(`Re(S₁)/N = 1 > 0.7`) exactly as the annealed→quenched wall predicts. **No machine decided. No label upgraded.**

---

## 1. Setup [PROVEN, verified]

Odometer `3G'=4G+e(ρ)`, `ρ=G mod 3`, `e={0:9,1:14,2:1}`; mirror `W=G+14`, `3W'=4W+(e−14)`, `e−14={1:0,2:−13,0:−5}`.
`ρ=1 ⇔ 3|W`; run theorem: maximal ρ=1 run at G has length `v₃(W)` exactly (on a ρ=1 step `W'=(4/3)W`, `v₃` drops by
1). Ledger `a'=a+δ`, `δ={1:−1,2:+4,0:+6}`, `ψ=−δ`, fatal ⇔ prefix `Σψ≥a₀−1` ⇔ **`#1/n ≥ 4/5`** (`ρ=2` cheapest
filler). `freq{3|W_n}=freq{ρ=1}=#1/n`. Real orbit N=2×10⁵: `#1/N=0.33386`, mean run 1.5001, max run 12 (gen 84 788,
cap 0.262N≈52 360), ledger min 16, max prefix `Σψ = 1 ≪ 15`. Run theorem verified on all 44 513 complete runs;
ledger identity `a_N = a₀−#1+4#2+6#0` exact.

## 2. The freq↔exponential-sum dictionary — the margin made analytic [PROVEN, assertion-checked]

Cube roots of unity `ω=e^{2πi/3}`: `1{3|W} = (1/3)(1+ω^W+ω^{2W}) = (1/3)(1+2Re(e^{2πiW/3}))`. Summing, with
`S₁(N)=Σ_{n<N} e(W_n/3)`:

> **`#1 = N/3 + (2/3)·Re(S₁)`, i.e. `freq{3|W_n} = 1/3 + (2/3)·Re(S₁(N))/N`.** (Verified: `Re(S₁)=158.000` exactly,
> `N/3+(2/3)·158 = 66772 = #1`.)

Therefore the fatal threshold `freq ≥ 4/5` is **exactly** `Re(S₁(n))/n ≥ 7/10`. The whole decision problem becomes:

> **DECIDE o4 ⟺ prove `Re(S₁(n)) < (7/10)·n` for all/cofinally-many n on the seed-43 orbit.**

The trivial bound is `|S₁| ≤ N`. So we need only **70 % of trivial** — a `0.30` absolute slack (equivalently the
`0.467` freq margin). This is the sharpest statement yet of *why* the margin helps: **any effective cancellation,
however weak, that beats the constant `0.7` decides o4.** Observed: `Re(S₁)/N = 0.00079` — 890× inside the target.

**Why this is still not free (the obstruction, exact).** The all-ρ=1 fixed-point orbit δ₋₁₄ (`T(−14)=−14`) has
`W_n≡0` always, so `S₁=N`, `Re(S₁)/N = 1 > 0.7` — **fatal**. Hence **no unconditional bound `Re(S₁)/N<0.7` can hold
over all orbits**; a proof must READ the seed-43 arithmetic. The target is precisely quenched single-orbit
equidistribution of the ×4/3 3-adic orbit — (K) at base 4/3, level 1, with a `0.30` slack.

## 3. Run-cap → frequency: the margin is exactly zero [OBSERVED/CONSTRUCTED, decisive against the hope]

The brief's central hope: does the forced exit from each ρ=1 run (each run of length `≤ v₃(W_entry) ≤ 0.262n`) give a
**positive density of ρ≠1 steps**, hence `freq{ρ=1} ≤ 1−c`? Exact accounting:

- The itinerary is (ρ=1 run L₁)(non-1 block B₁)(ρ=1 run L₂)… with every `|B_i| ≥ 1` (maximality). **Forced non-1
  steps = R** (number of complete runs); `freq{non-1} ≥ R/N`. So a positive frequency margin requires **`R/N ≥ c > 0`**.
- Real orbit: `R/N = 0.2226` (mean run 1.5 ⟹ R ≈ N/4.5). **But `R/N` is NOT bounded below.** Two explicit
  cap-and-magnitude-legal witnesses (verified):
  - **cap-saturating tiling** (runs `≈0.262·position`, one non-1 between): `R = 42`, forced density `0.00021`,
    `freq{ρ=1} = 0.99979` — freq→1 with R = O(log N).
  - **shallow burst** `(1⁵2)*`: `freq = 5/6 = 0.833 ≥ 4/5`, runs of depth 5 (`≪` cap), magnitude tiny.

  Both drive `R/N → 0` while respecting the run-cap AND the magnitude bound `Σv₃(W_j) ≤ 0.131n²`. **Therefore the
  run-cap forces no positive lower bound on the non-1 density: `c = 0`.**
- The only literal consequence of the cap: an **all-ρ=1 tail is impossible** (`v₃` drops by 1 per step; the longest
  real run's ladder is `[12,11,…,1]` — a run cannot exceed `v₃(W_entry)`, and an infinite tail needs `v₃=∞`). But
  this excludes only `ρ_n=1 ∀n≥n₀`, i.e. a length-∞ run; it does **not** exclude `freq{ρ=1}=1` (density 1 with
  density-0 exceptions), which the cap-saturating tiling realizes in the limit. **No unconditional bound below the
  trivial `#1 ≤ n` is obtained.**

This is the exact quantitative confirmation of `O4_NEWMATH_BUILD`'s orthogonality lemma: run-cap (support) and
magnitude (quadratic 2nd moment) are both blind to the linear first moment `#1`. The margin (`0.467`) is real but
**irrelevant here — there is no unconditional bound to compare it against.**

## 4. The bespoke exponential sum — square-root cancellation, but no effective rate [OBSERVED + PROVEN mechanism]

`S_k(N)=Σ_{n<N} e(W_n/3^k)`, exact `W_n mod 3^k`, big-int. Measured k=1..6 at a ladder of N up to 2×10⁵:

| quantity | finding |
|---|---|
| `|S_k|/N` all k | decreasing, `→ 0` |
| `|S₁|/√N` across N | fluctuates `0.37–0.88`, **O(1)** — square-root size |
| least-squares slope of `log|S₁|` vs `log N` | **α = 0.491** (0.5 = square-root cancellation / equidistribution) |
| VdC inner corr. `C_h=(1/M)Σe((W_{n+h}−W_n)/3^k)` | `|C_h| ≈ 0.001–0.005 ≈ 1/√M` (k=1,2, h=1,2,3,4,8) |

So the actual orbit's bespoke sum has **clean square-root cancellation**: `|S₁(N)| ~ N^{0.49}`, `|S₁|/N ~ N^{−1/2}`,
i.e. `Re(S₁)/N` sits ~890× *inside* the `0.7` target. Numerically, o4 equidistributes and is nowhere near fatal.

**Why no *effective* bound follows (the non-Pisot regress, concrete) [PROVEN identity].** Van der Corput bounds
`|S|²` by inner sums of the differenced phase `f(n+h)−f(n)`. The first difference is (verified exactly, 5000 steps):

> **`W_{n+1} − W_n = (W_n + e_n − 14)/3`**, hence
> `e((W_{n+1}−W_n)/3^k) = e(W_n/3^{k+1})·e((e_n−14)/3^{k+1})`.

Differencing the level-`k` sum produces a **level-`(k+1)` sum**, twisted by a residue-dependent phase, with
**multiplier `|4| = 1` (a unit mod 3) — no contraction.** Each VdC step pushes one 3-adic digit deeper and gains
nothing; the process is an infinite regress. This is `NEW_MATH_PROGRAM §8.7`'s non-Pisot obstruction made completely
explicit for o4: `4/3` non-Pisot ⟹ the transfer/differencing operator has no spectral gap, the numerically-small
`C_h` is itself the unprovable equidistribution, and **Weyl/van-der-Corput/Vinogradov machinery yields `o(1)` but no
effective rate.** (Vinogradov/Weyl need a polynomial phase or a Pisot base; the ×4/3 orbit supplies neither.)

## 5. What was built, what obstructs

| item | content | label |
|---|---|---|
| freq↔S dictionary | `freq = 1/3 + (2/3)Re(S₁)/N`; **fatal ⇔ `Re(S₁)/n ≥ 7/10`** | `[PROVEN, verified]` |
| Analytic target for the decision | prove `Re(S₁)/n < 0.7` (70 % of trivial; `0.30` slack) for seed-43 | `[CONSTRUCTED]` |
| Unconditional obstruction | δ₋₁₄ orbit: `Re(S₁)/N = 1 > 0.7`, fatal ⟹ no bound over all orbits | `[PROVEN]` |
| Run-cap → frequency margin | forced non-1 density `= R/N`, **not bounded below** (cap-saturating tiling `R=O(log N)`), `c = 0` | `[OBSERVED/CONSTRUCTED]` |
| all-1 tail impossible | run `≤ v₃(W_entry)`; excludes length-∞ run only, **not** `freq=1` | `[PROVEN, verified]` |
| bespoke S measurement | square-root cancellation `α=0.491`, `|S₁|/N ~ N^{−1/2}` ≪ 0.7 | `[OBSERVED, N=2×10⁵]` |
| effective bound? | VdC regress `W_{n+1}−W_n=(W_n+e_n−14)/3`: level `k→k+1`, unit multiplier, no contraction | `[PROVEN obstruction]` |

## 6. Verdict

The bespoke exponential-sum build produces the **cleanest reformulation of o4's open core to date** — a single
scalar inequality `Re(S₁(n)) < 0.7 n` for the cube-root-of-unity sum of the actual orbit — and makes the `0.467`
margin analytically concrete (`0.30` absolute slack, 70 % of trivial). It does **not** decide o4: (i) the proven
run-cap contributes *zero* unconditional frequency margin (forced-exit density is not bounded below — the freq→1
cap-saturating tiling respects every proven bound); (ii) the sum equidistributes with textbook square-root
cancellation on the real orbit but admits **no effective bound**, because van-der-Corput differencing of the ×4/3
orbit regresses to a deeper 3-adic level with unit multiplier — the non-Pisot wall, now written as an exact
one-line identity. Any *unconditional* cancellation fails at δ₋₁₄ (`Re(S₁)/N=1`); the seed-43 bound is precisely
quenched base-4/3 level-1 equidistribution, (K)-species, with a large but non-decisive slack.

**No machine decided. No label upgraded.**

Script: `o4_expsum_frequency.py` (exact big-int, all assertions passed, N=2×10⁵). Not committed.
