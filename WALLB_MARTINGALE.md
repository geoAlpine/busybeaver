# Wall (B) — martingale / compensator decomposition of the parity sum (2026-06-28)

Angle: attack `W_N = Σ_{n<N} (−1)^{r_n}` (Antihydra non-halt ⇐ `W_N = o(N)`) through the
**Doob martingale / compensator** decomposition, and test whether a **low-bits (skew-product)
filtration** moves the hard part out of the predictable compensator and into a *free* martingale
remainder. Object: `r_n = c_n mod 2`, `c_0 = 8`, `c_{n+1} = ⌊3c_n/2⌋`; equivalently
`r_n = bit_{n+3}(3^n)` = the **moving-middle diagonal bit** (`EFFECTIVE_TOPDIGIT.md`).

Script: `martingale_compensator.py` (exact integer arithmetic, `.venv`). 0 false proofs; every
number is a finite-sample out-of-sample statistic carried with its `1/√N` null band.

---

## 1. The clean decomposition [PROVEN — but only inside a probability model]

For **any** filtration `(F_n)` on a probability space, define the predictable compensator and the
innovation/martingale remainder:

> `A_n := E[(−1)^{r_n} | F_{n−1}]`  (predictable, `F_{n−1}`-measurable)
> `D_n := (−1)^{r_n} − A_n`,  `M_N := Σ_{n<N} D_n`,  `C_N := Σ_{n<N} A_n`.
> **`W_N = C_N + M_N`** exactly.

`(M_N)` is a martingale with **bounded differences** `|D_n| ≤ 2`. Azuma–Hoeffding gives, with
probability `≥ 1 − δ`,
> **`|M_N| ≤ 2√(2 N log(2/δ))  =  O(√(N log N))  — unconditionally and for free.`**

**Consequence (the clean structural statement).** *The entire difficulty of `W_N = o(N)` lives in
the **predictable compensator** `C_N = Σ E[(−1)^{r_n}|F_{n−1}]`. The random/martingale half is
controlled at the `√N`-cancellation rate for free by Azuma; nothing hard is in it.* The target
reduces to **`C_N = o(N)`**, i.e. to the **conditional balance** `E[(−1)^{r_n}|F_{n−1}] = o(1)` on
average (`WALLB_DECORR_STRUCTURE.md §3`). This is the martingale-difference reformulation, strictly
weaker than equidistributing either digital factor. [PROVEN within a probability model.]

**The catch, stated up front.** Azuma's `√N` is free **only if there is a genuine probability
measure** under which `(F_n)` is a filtration and `D_n` are real conditional-mean-zero martingale
differences. For a **single deterministic orbit there is no such measure**, and the whole proof
turns on whether a coarse filtration can supply one. §2–§4 test exactly that.

---

## 2. The deterministic vacuity, and the two horns of the filtration [PROVEN/OBSERVED]

For the single orbit, conditioning on the **full** past `F_{n−1} = σ(r_0,…,r_{n−1})` makes
everything deterministic: `A_n = (−1)^{r_n}`, `D_n ≡ 0`, `M_N ≡ 0`, `C_N ≡ W_N`. The decomposition
is **vacuous** — the compensator *is* the whole sum.

The only escape is a **coarse** filtration `F_{n−1} = σ(coarse statistic at n)` under which the
current parity is *not* `F_{n−1}`-measurable, treating the unresolved bits as "random." Three
natural coarsenings, and what each does (numerics, `N = 200000`, split-sample: kernel
`g(s)=E[f|s]` learned on `[0,N/2)`, applied **out-of-sample** on `[N/2,N)`; decisive metric =
out-of-sample `R² = 1 − Σ(sign−g)²/Σ(sign−mean)²`, where `R² ≤ 0` ⟺ *no predictive power*):

| filtration `F_{n−1}` | k | #states | OOS `R²` | reading |
|---|---|---|---|---|
| **(i) `c_n mod 2^k`** (low bits of orbit) | 4/8/12 | 16/256/4096 | **+1.000** | contains `bit0 = r_n` literally → "predicts" perfectly = **vacuous determinism**, not a legitimate `F_{n−1}` |
| **(ii) `T_n mod 2^k`** (low bits of carry) | 4/8/12 | 2/9/129 | **−0.00003 / −0.0001 / −0.0016** | **no predictive power** (slightly negative = overfit) |
| **(iii) (top 6 bits, bits 1–6) of `c_n`** = BOTH proven footholds | — | 2052 | **−0.0235** | **no predictive power** (overfit) |

Here `|W'| = 244 = 0.77√(N/2)` is the held-out sum; the no-model baseline. In (ii)/(iii) the
out-of-sample compensator is pure noise (`|C| ≈ √N`) and the residual is **not reduced below**
the baseline — the learned kernel *hurts* (R² < 0). [OBSERVED]

**Why (ii) carries no information — structural [PROVEN].** `T_{n+1} = 3T_n + 2^n r_n`, so for
`n ≥ k` the input term `2^n r_n ≡ 0 (mod 2^k)` and `T_n mod 2^k = 3·(T_{n−1} mod 2^k)` — a
**fixed multiply-by-3 rotation**. Verified: `T_{n+1} ≡ 3T_n (mod 2^k)` with **0 violations** over
`n = k…N` for `k = 8, 12`; eventual period `8` (k=8) and `128` (k=12). So the low carry bits are a
**deterministic function of `n` alone** (a rotation through the `×3`-orbit), carrying **no live
orbit information** about the middle parity bit. Conditioning on `T_n mod 2^k` ≈ conditioning on
`n mod period` — and the parity is not periodic mod any `2^m` (it has full subword complexity,
`EFFECTIVE_TOPDIGIT.md`). Hence `R² ≈ 0`. [PROVEN structural + OBSERVED]

---

## 3. Where it lands: re-collapse to the middle-digit Mahler object [the verdict]

The two horns of the coarse filtration are a genuine dichotomy, and **neither gives a free bound**:

- **Horn A — the filtration sees the answer.** Low bits of the orbit `c_n` *contain* `r_n = bit0`.
  Then `C_N = W_N`, `M_N = 0`: the compensator is the whole sum. Vacuous determinism. (Filtration (i),
  `R²=1` at every `k`.)
- **Horn B — the filtration is uninformative.** Low bits of the carry `T_n` (a fixed rotation) and
  the proven top/bottom footholds carry **zero predictive information** about the parity
  (`R² ≤ 0`, filtrations (ii),(iii)). Then `A_n ≈ 0`, so `C_N ≈ 0` and **`W_N ≈ M_N` — the entire
  sum sits in the "martingale" remainder.**

Horn B *looks* like the good case ("`E[(−1)^{r_n}|F_{n−1}] = 0`, just apply Azuma"), and this is the
**precise trap**: with `C_N ≈ 0` the remainder `M_N = W_N` is **literally the original deterministic
sum**, and Azuma's `O(√N)` bound on it is **unavailable** — there is no probability measure making
the deterministic increments `(−1)^{r_n}` true martingale differences. Manufacturing that measure
(a mixing/CLT structure on the orbit) is **exactly** the equidistribution of the moving-middle
diagonal bit = **Mahler**. So:

> **The compensator is either the whole sum (Horn A, vacuous) or zero (Horn B, uninformative); in
> the only non-trivial case the bound re-collapses to proving `M_N = W_N = O(√N)` for the single
> orbit — the original middle-digit Mahler problem verbatim.** [verdict: NOT a genuine partial
> bound; re-collapses to Mahler.]

This is the `EFFECTIVE_TOPDIGIT` `Θ(log N) ↔ Θ(n)` gap reappearing exactly: any coarse statistic a
finite `F_{n−1}` can hold is a top/bottom **foothold** (≤ `Θ(log N)` bits, here the `×3`-rotation of
the low carry bits + the top mantissa), while the parity is the **moving-middle bit at depth ≈ n**,
`Θ(n)` away from any foothold. There is **no Goldilocks filtration** — no coarse `F_{n−1}` that (a)
omits the current parity yet (b) predicts it well enough to make the compensator the easy part.
Filtration (iii) confirms: **both** proven footholds combined still give `R² < 0`. [OBSERVED + PROVEN]

---

## 4. Numerical summary [OBSERVED, N = 200000, sqrt(N)=447]

- Global: `W_N = 74 = +0.17√N`, odd-density `0.49982` — the sum is at `√N` scale, consistent with
  free martingale cancellation *if a measure existed*.
- Out-of-sample `R²` of every coarse low-bit / foothold predictor for the parity is `≤ 0`
  (i: degenerate +1; ii: `−0.00003 → −0.0016` as k=4→12; iii: `−0.024`). The compensator built from
  any of them is statistical noise (`|C| ≈ √N`), and **does not shrink toward an O(1) predictable
  part as k grows** — increasing k only adds overfit (R² drifts *more* negative). The compensator
  neither vanishes usefully (it is already noise) nor stays a *meaningful* `O(N)` predictable signal:
  there is no predictable signal to capture.
- Structural: `T_n mod 2^k` is an exact `×3` rotation (0 violations, periods 8/128) — a function of
  `n` only.

**One-line numeric verdict.** No low-bits filtration splits `W_N` into a (free) `√N` martingale plus
a *smaller* compensator: the only filtration that predicts the parity is the one containing it (Horn
A, vacuous); every information-respecting coarse filtration predicts the parity with `R² ≤ 0` (Horn
B), leaving the whole sum in a remainder whose `√N` control is exactly Mahler.

---

## 5. Returned conclusions (the asks)

1. **Clean decomposition [PROVEN in a model].** `W_N = C_N + M_N` with `M_N` a bounded-difference
   martingale ⇒ Azuma `M_N = O(√(N log N))` for free; **all difficulty is the predictable
   compensator** `C_N = Σ E[(−1)^{r_n}|F_{n−1}]`, i.e. the conditional balance
   `E[(−1)^{r_n}|F_{n−1}] = o(1)`. The `√N` freebie is **conditional on a probability measure that a
   single deterministic orbit does not have**.

2. **Does a low-bits filtration give a genuine partial bound, or re-collapse to Mahler? — It
   re-collapses.** [verdict] A coarse filtration faces a dichotomy: it either *contains* the parity
   (low bits of the orbit `c_n`; compensator = whole sum, vacuous) or is *uninformative* about it
   (low bits of the carry `T_n` = a fixed `×3` rotation; top/bottom footholds; OOS `R² ≤ 0`). In the
   uninformative case `C_N ≈ 0` and `W_N ≈ M_N` is the **original deterministic sum**, whose `O(√N)`
   control needs the very mixing measure that = middle-digit equidistribution = **Mahler**. No
   Goldilocks filtration exists; the parity is the moving-middle bit `Θ(n)` from every foothold a
   finite `F_{n−1}` can see (`EFFECTIVE_TOPDIGIT` `Θ(log N)↔Θ(n)` gap). **Not a genuine partial
   bound.**

3. **Numerics [OBSERVED].** Out-of-sample `R²` of all low-bit (k=4,8,12) and combined-foothold
   predictors for the parity is `≤ 0`; the compensator is `√N`-noise and does not develop a smaller
   `O(1)` predictable part as k grows; `T_n mod 2^k` is an exact `×3` rotation (0 violations, period
   `2^{k−2}`-class). `W_N = +0.17√N`.

Honest net: the martingale framing is **the correct reformulation** (it isolates the obstruction to
the compensator and makes the freebie explicit) but it is **not a reduction** — for a single
deterministic orbit the freebie is unavailable, and the compensator route lands back on the
middle-digit Mahler object. This sharpens, and is fully consistent with, the
`WALLB_BILINEAR_VDC.md` [CLOSED] (the a/b split re-fuses to the parity kernel) and the
`EFFECTIVE_TOPDIGIT` foothold barrier.

Script: `martingale_compensator.py`. Not committed.
