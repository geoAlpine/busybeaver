# The archimedean foothold is capped at Θ(log n) — a hard barrier (2026-06-24)

Attacking the unified kernel via the one provable ingredient (multiplicative independence of 2,3 ⇒
`{n·log₂3}` equidistributes ⇒ Weyl/Benford controls the TOP bits of `3ⁿ`). Question: how far DOWN does
"provable" reach — can the foothold be pushed to depth `εn` (toward the diagonal at depth `~0.585n`)?

## Result [computed, `foothold_depth.py`]
The number of provably-equidistributed top bits is `K_max(N) = log₂(1/D_N)` where `D_N` is the star
discrepancy of `{n·log₂3 : n≤N}`. Measured (mpmath, 4000 dps):
```
N      D_N         K_max
200    7.5e-3      7.06
1000   2.0e-3      8.95
20000  3.2e-4      11.6      (log₂N = 14.3)
```
**`K_max(N) = Θ(log N)`.** The control reaches only *logarithmic* depth from the top.

## The hard barrier [rigorous]
- Controlling the top `K` bits ⟺ resolving `{n·log₂3}` at scale `2^{−K}` ⟺ discrepancy `< 2^{−K}`.
- A 1-D linear sequence `{nα}` has discrepancy `D_N ≳ 1/N` (this is a **fundamental lower bound** — no
  equidistributed sequence beats `1/N`; for `α=log₂3` with finite irrationality measure, `D_N ~ (log N)/N`).
- Hence `K_max ≤ log₂ N + O(1)` — **the foothold cannot exceed `~log₂ n` top bits, ever.**
- The diagonal bit sits at depth `~0.585n = Θ(n)`. Reaching it needs discrepancy `~2^{−εn}` (exponentially
  small); the truth is `~1/N` (polynomially small). **Gap = `log n` vs `n`, exponential.**

## Consequence for the kill-both strategy
Pushing the **archimedean (real-place / leading-bit) foothold downward is provably impossible** — it is
capped at `Θ(log n)`, exponentially short of the diagonal. This **rules out an entire class of approaches**
(extend Weyl/Benford/leading-digit equidistribution to the moving diagonal). Both monsters are immune to it.
Therefore a kill-both method must come from the **p-adic side or the joint (real × 2-adic × 3-adic) solenoid**
structure — NOT from extending the top-bit control. The barrier is now a proven signpost: do not go this way.
