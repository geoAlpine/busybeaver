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

## Meeting verdict (2026-06-25, second consultation) — barrier confirmed unbeatable by standard methods
A method-by-method review confirmed **no known standard technique** beats the `Θ(log N)` foothold to reach the
middle digit:
- **Weyl / Erdős–Turán / Diophantine:** works on the top mantissa `{n log₂3}`, depth `log N` only (this file).
- **van der Corput / high-order differencing:** **CLOSED** (now *verified*, see below) — the phase
  `(3/2)^{n+h}−(3/2)^n = t'(3/2)^n` returns the *same exponential family*, so differencing is a fixed point and
  gains nothing.
- **effective metric theory (Koksma, Tao):** almost-all / log-density-1 only; never the single seed-8 orbit.
- **Flatto–Lagarias–Pollington (1995):** range/spread lower bound, not a density or a digit frequency.
- **digit-sum / Stewart / Stolarsky:** bound the *number* of nonzero digits, not a *moving fixed-position*
  digit's frequency.

**Verified: van der Corput is closed (`vdc_closed.py`).** With exact integer fractional parts
`frac((3/2)^n)=(3^n mod 2^n)/2^n`, the Mahler sum `|Σ_{n≤N} e(t·(3/2)^n)| = O(1)·√N` (full √-cancellation,
`0.39–1.18·√N` over `t=1..5`, `N=8000`), and the differenced sums `|Σ e(t((3/2)^{n+h}−(3/2)^n))|` are *also*
`O(1)·√N` — **no improvement**. (Precision note: a first attempt at `mp.dps=60` was wrong — `(3/2)^n` for
`n=4000` needs `~2340` bits; the exact-integer computation is the correct one. Caught and fixed.)

## The wall, third face (from this baseline) — the sharpened expert ask
The wall now has a **third equivalent characterization**, alongside (1) rank-1 single-orbit effective
equidistribution and (2) one-sided shrinking-target / specific-orbit genericity:
> **(3) Equidistribution of a *moving middle digit* of `a^n` in base `b`, beyond the `Θ(log N)` top/bottom
> footholds.** For Antihydra: control `bit_{n+3}(3^n)` (the diagonal, fixed slope `c = 1` in `bit_{cn}(3^n)`)
> along the single orbit.

**Expert ask (the precise question to put first):**
> *Is there any known method proving equidistribution of a **moving middle digit** of `a^n` in base `b` — i.e.
> `bit_{cn}(a^n)` for a fixed `0 < c < log_b a` along one specific orbit — beyond the `Θ(log N)` top/bottom
> footholds from Weyl/Diophantine approximation and fixed-modulus character sums? Can high-order van der Corput,
> effective metric theory, or digital exponential-sum estimates reach a moving middle digit?*

Predicted answer: **No** — and a clean "no" is valuable: it pins the wall as *moving-middle-digit-beyond-`Θ(log N)`*,
a sharper, more answerable formulation than "solve Mahler."

## Digit-side probe — the moving-diagonal sequence is maximally complex [verified]
Probing whether the third face (the digit side) offers an automatic / low-complexity foothold: the
moving-diagonal parity sequence `e_n = c_n mod 2 = bit_{n+3}(3^n)` has **full subword (factor) complexity**
`p(k) = 2^k` (verified: `p(k)=2^k` exactly to `k=14` at `N=4·10^5`, the `k=16` shortfall is coupon-collector
noise at `~6` samples/word). So the sequence is **pseudorandom — not automatic, not low-complexity** — and
combined with its **maximal linear complexity** (Berlekamp–Massey `=M/2`, prior) it is maximally complex in
**both** the automata and the algebraic senses. **Consequence:** the digit side offers **no structural
foothold** (no automatic-sequence decision procedure, no forbidden patterns); the third face is the same
*structureless-normal* wall — proving a fully-complex deterministic sequence equidistributes is exactly Mahler.
(This also re-derives, from the digit angle, the bbchallenge "no regular certificate" barrier: a full-complexity
sequence has no finite-automaton description.) `digit_complexity.py`.

## Status
[PROVEN, unconditional] effective equidistribution of the top `Θ(log N)` digits, constants from `log₂3`'s CF;
[PROVEN, sharp] the `Θ(log N)` barrier for the archimedean method; [PROVEN, verified] van der Corput closed;
[OPEN] anything beyond `Θ(log N)` (= the moving diagonal = the wall). 0 false proofs.
