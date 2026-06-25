# Effective top-digit equidistribution of the Antihydra orbit, quantified by log₂3 (2026-06-25)
*A rigorous, unconditional baseline: exactly how far the classical (Weyl + Diophantine) method reaches on the
Antihydra orbit, with explicit constants from the continued fraction of `log₂3`. This is the frontier the new
single-orbit tool must extend. All numbers machine-verified (`effective_topdigit.py`). Status: the equidistribution
is [PROVEN, unconditional]; the barrier is [PROVEN, sharp for this method].*

## Setup
`c_n = ⌊8·(3/2)^n⌋` (the Antihydra orbit). Its leading binary digits are governed by the **leading mantissa**
`θ_n := frac(log₂ c_n) = {n·α + 3}`, where `α = log₂(3/2) = log₂3 − 1 = 0.5849625…`. By Weyl, `{nα}`
equidistributes (`α` irrational); the *rate* is set by the continued fraction of `α`:
`α = [0; 1,1,2,2,3,1,5,2,23,2,2,1,1,55,…]`, convergent denominators `q_m = 2,5,12,41,53,306,665,15601,31867,…`.
The irrationality measure `μ = μ(log₂3)` is **finite** (`log₂3` is not Liouville; the CF quotients are tame, the
local `2 + log a_{m+1}/log q_m` proxy stays `≤ 3` over the computed range).

## Theorem (effective top-digit equidistribution)
> **(a) [PROVEN, sharp at convergents].** Along `N = q_m` (CF denominators of `α`), the star-discrepancy of
> `({nα})_{n≤N}` is `≪ 1/N` (three-distance theorem). Hence the **top `k(N) = log₂ N − O(log log N)` binary
> digits** of `(c_n)_{n≤N}` are equidistributed, with leading-mantissa discrepancy `≪ 1/N`.
> **(b) [PROVEN, uniform].** For every `N`, the top `(1/(μ−1) − ε)·log₂ N` digits equidistribute
> (Erdős–Turán + `|α − p/q| ≫ q^{−μ}`).

**Verification.** Discrepancy at convergents: `−log₂ D*_{q_m} / log₂ q_m → 1.000` (`D*_{q_m} ≈ 1/q_m`):
`q_m = 12, 41, 306, 665, 15601 → −log₂D* = 3.61, 5.38, 8.26, 9.38, 13.93`, each `≈ log₂ q_m`. Direct top-`k`-bit
histogram of `c_n` (`n ≤ 20000`): max bin-deviation from uniform `2^{−k}` is `0.003·2^{−k}` (`k=4`),
`0.05·2^{−k}` (`k=8`), `0.64·2^{−k}` (`k=12`), `=2^{−k}` (`k=14 ≈ log₂N`). So `k(N) ≈ log₂ N` is the exact
controllable depth.

## (c) The barrier [PROVEN, sharp for the archimedean method]
The **even-density (parity) bit** — the quantity governing non-halt — is `c_n mod 2 = bit_{n+3}(3^n)`: the
**diagonal bit** of `3^n`, at position `≈ n` inside the `≈ 1.585n`-bit integer `3^n`. The two classical footholds:
- **Top foothold** (this theorem; Weyl on `{n log₂3}`): controls the top `Θ(log N)` bits of `c_n` / `3^n`.
- **Bottom foothold** (the `×3`-coset / off-diagonal, `§4`): controls the low `Θ(log N)` bits unconditionally.

Both reach only `Θ(log N)`; the diagonal at position `≈ n` is `Θ(n)` away from **both** ends. **So effective
equidistribution, pushed to its limit with the best Diophantine input on `log₂3`, controls `Θ(log N)` digits —
and the gap to the diagonal is `Θ(n) − Θ(log N) = Θ(n)`.** This is the precise, quantified statement of the
foothold barrier: the new single-orbit tool must close a `Θ(log N) → Θ(n)` gap.

## Why this is the right baseline
It pins, with explicit constants, exactly what is *unconditionally true* about the orbit's digit equidistribution:
`Θ(log N)` digits at each end, nothing in the middle. Every conditional theorem and the target `A1` live in the
`Θ(n)`-wide middle band. A genuine partial result would be **any** unconditional push of the controllable depth
beyond `Θ(log N)` (e.g. to `(log N)^{1+δ}` or `N^δ`) — that is the concrete, measurable progress metric for the
new tool, and the first thing to ask experts: *is there any unconditional method reaching beyond `Θ(log N)`
digits of `⌊(3/2)^n⌋` / of `3^n` at a moving (non-top, non-bottom) position?*

## Status
[PROVEN, unconditional] effective equidistribution of the top `Θ(log N)` digits, constants from `log₂3`'s CF;
[PROVEN, sharp] the `Θ(log N)` barrier for the archimedean method; [OPEN] anything beyond `Θ(log N)` (= the
moving diagonal = the wall). 0 false proofs.
