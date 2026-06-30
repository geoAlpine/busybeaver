# Depth-reach clarification: empirical equidistribution depth is counting-capped — the real frontier is the moving-diagonal density (2026-06-30)

*A conceptual sharpening produced while attempting new mathematics on the minimal core. It does NOT prove anything
toward `(K)`; it CORRECTS a potential category error in our own "log-vs-linear depth gap" framing and re-locates the
genuine frontier precisely. SOUNDNESS: the counting ceiling is `[PROVEN]` (pigeonhole); the rest is labelled. NOT
committed by default until recorded.*

---

## 0. The clarification

There are **two different "depths"** in the program's language, and conflating them is a category error:

- **`R(N)` = empirical equidistribution depth** of the orbit's first `N` points: the largest `k` such that
  `{c_n mod 2^k : n<N}` is (covered / equidistributed). **`[PROVEN]` `R(N) ≤ log₂ N`** — pure counting/pigeonhole:
  `N` points occupy at most `N` of the `2^k` residues, so all `2^k` appearing forces `2^k ≤ N`. Equidistributing
  them forces `k ≤ log₂N − O(1)`. **This ceiling is information-theoretic, NOT a tool weakness — it can never be
  pushed past `log₂N`, by anyone, for any sequence.**
- **The moving-diagonal depth** in the kernel: `c_n mod 2` (the parity / even-indicator, whose `liminf` running
  mean is `(K)`) equals, via the seam identity `2ⁿc_n + S_n = 8·3ⁿ`, the bit `bit_{n+k}(8·3ⁿ) ⊕ bit_{n+k}(S_n)` —
  the binary digit of `3ⁿ` on a **moving diagonal at position `≈ n`** (depth `Θ(n)`), corrected by the endogenous
  carry. This is **one deterministic bit per `n`**; its density is well-defined and **not** capped by counting.

> **Correction to the "log-vs-linear gap" statement (`NEW_METHODS_SWEEP_2026-06-30.md` §1).** The "linear depth"
> the kernel needs is **not** an empirical-equidistribution depth (that is trivially `log`-capped and irrelevant).
> It is the depth of the **moving diagonal of `3ⁿ`** — a single-orbit *digit-frequency* question. Likewise, Tao's
> Prop 1.9 hypothesis (1.11) ("start equidistributed to depth `~2n`") is about the **start-point ensemble** (a.e. /
> 2-adic Haar over starts), not about `n` empirical points of one orbit. So the gap is real, but it lives on the
> **digit-frequency / ensemble axis**, not the empirical-equidistribution-depth axis.

## 1. Data `[OBSERVED]`

`scratchpad/depthreach2.py`, orbit `c_0=8`, exact big-int, `N` up to `2·10⁵`:

| `N` | `log₂N` | cover-depth | equidist-depth (rel. dev ≤ 0.25) |
|---|---|---|---|
| 2 000 | 10.97 | 7 | 5 |
| 32 000 | 14.97 | 12 | 7 |
| 200 000 | 17.61 | 14 | 10 |

Cover-depth `≈ 0.8·log₂N`, equidist-depth `<` cover-depth, **both `< log₂N` always** — the counting ceiling, as
predicted. (The actual kernel statistic is healthy: even-density `= 0.50018`, worst running density `0.4797` at
`n=123`, margin `0.146` above the `1/3` threshold — the orbit empirically satisfies `(K)` with room; the open
problem is *proving* the `liminf`.)

## 2. The genuine frontier, re-stated precisely

The real new-mathematics target is therefore **not** "equidistribute deeper," but:

> **Frontier target.** Improve the unconditional lower bound on the even-count `#even(n) = #{m<n : c_m even}` past
> `Θ(log n)` (the current best is `#even(n) ≥ 0.89 log n`, `LIMIT_THEOREM.md`). The truth is `#even(n) ∼ n/2`; the
> kernel `(K)` needs `liminf #even(n)/n ≥ 1/3` (**linear**, positive density). Equivalently: a one-sided
> positive-density lower bound on the **moving-diagonal binary digit of `3ⁿ`** (minus the endogenous carry).

Anything strictly between `Θ(log n)` and linear — `(\log n)^{1+ε}`, `n^c`, `\exp(c\sqrt{\log n})` — would be a
**genuine new unconditional theorem** advancing the frontier (still short of `(K)`, which needs linear/positive
density). **Honest status `[OPEN, generational]`:** no unconditional positive-density bound for a moving diagonal of
`3ⁿ` exists in the literature (AEV arXiv:2510.11723 prove none); even a sub-polynomial improvement past `log` is at
or beyond the current research frontier. This is the precise object a multi-year program must build a tool for.

**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
