# Second-moment / energy attack on `avgD_odd ≥ 3/2`: it reduces to a character sum, but energy is sign-blind (2026-06-26)
*Program: rank-1 specified-orbit genericity. Attacks the cleanest criterion form (`avgD_odd ≥ 3/2`, from the
valuation budget) with a second-moment / additive-energy method. Result: the obstruction's leading term is a
one-sided **character sum**, and second-moment/energy is **structurally sign-blind** to exactly the one-sided
direction the criterion needs. `energy_attack.py`. Verified to `n=3·10⁵`. 0 false claims.*

## Exact decomposition (the character-sum reduction)
`avgD_odd = Σ_{k≥1} P(D_i ≥ k | odd)`, `D_i = v2(3c_i−1)`. For odd `c_i`: `c_i ≡ 1 (4) ⇒ D=1`; `c_i ≡ 3 (4) ⇒ D≥2`.
With `χ = χ_{−4}` the nontrivial character mod 4 (`χ(1)=+1, χ(3)=−1`): `1[D_i≥2] = (1−χ(c_i))/2`, so
```
avgD_odd = 3/2 − ½·avgχ_odd + (deeper-cylinder bonus ≥ 0),   avgχ_odd = (1/O_n) Σ_{odd} χ(c_i).
```
Hence the leading term of non-halt (`avgD_odd ≥ 3/2`) is the **one-sided character sum**
`S_n := Σ_{odd i<n} χ_{−4}(c_i) ≤ 0`. A character sum is the natural home of second-moment / large-sieve methods.

## Why second-moment / energy fails: it is sign-blind
The additive energy / depth-2 collision count is, with `N_r = #{odd i<n : c_i ≡ r (4)}` (`N_1+N_3 = O_n`):
```
Energy = #{(i,j) odd : c_i ≡ c_j (4)} = N_1² + N_3² = O_n²/2 + S_n²/2.     [verified: excess energy = S_n²/2]
```
The energy's only orbit-dependent part is `S_n²` — the **squared** imbalance. It is **symmetric in `(N_1,N_3)`**:
it pins `|S_n|` but **cannot determine the sign of `S_n = N_1 − N_3`**. The criterion needs the sign (`S_n ≤ 0`).
> **Second-moment / energy is structurally sign-blind to the one-sided criterion** — it controls the *magnitude*
> of the mod-4 imbalance, never its *direction*. This is the method-level analog of the `#2` one-sided wall.

## What the magnitude bound would give — and why it is still the wall
Empirically `|S_n| ~ √O_n` with **fluctuating sign** (`S_n = +122` at `n=10⁴`, `−209` at `n=10⁵`, `+76` at
`3·10⁵`) — square-root cancellation, energy at the random rate (`excess energy = S_n²/2 ~ O_n`). A random-rate
energy gives `avgχ_odd = O(1/√n) → 0`, so `avgD_odd → 2` (margin holds). **But** proving `|S_n| = o(n)` *is* the
single-orbit equidistribution of `χ_{−4}(c_i)` — energy reduces the wall to a character-sum cancellation it cannot
itself certify (and cannot sign).

## Honest nuance: the mod-4 term is only the leading term, not the margin
`S_n` fluctuates in sign and **crosses zero** — so the sufficient condition `S_n ≤ 0` is **not necessary**: when
`S_n > 0` (e.g. `n=10⁴`), non-halt still holds because the **deeper-cylinder bonus** (`P(D≥3)+P(D≥4)+⋯ ≈ ¼+⅛+⋯ ≈
0.5`, the geometric tail) carries it. So the real margin lives in the **all-scale** bonus, not the mod-4 term —
exactly the `MARGIN_DECOMPOSITION` conclusion (all-scale control needed), now seen from the energy side. A perfect
mod-4 character-sum bound would *not* suffice without the deeper tail.

## Net result (responds to "attack avgD_odd with second-moment/energy")
- **Reduction achieved:** the criterion's leading obstruction is a one-sided character sum `Σχ_{−4}(c_i) ≤ 0`.
- **Method verdict:** second-moment/energy is **sign-blind** (controls `S_n²`, not `S_n`) — it cannot deliver a
  one-sided bound, and the magnitude bound it would give (`|S_n|=o(n)`) is the equidistribution input. Two
  independent reasons it cannot close the gap.
- **Precise escalation (new analytic-NT door):** the right object is **large-sieve / exponential-sum cancellation
  for the specified deterministic orbit's character sum `Σ_{n} χ_{−4}(c_n)`** (and its higher-modulus analogs for
  the deeper bonus). This is a crisper, analytic-number-theory-flavored question than the dynamical framing — worth
  adding to the expert ask: *is there square-root cancellation for a character sum along a single `⌊μ·⌋`-orbit?*

## Follow-through: the bilinear / sum-product route is also blocked — the orbit is multiplicatively structureless
We then tried to get cancellation in `S_N = Σ_n χ_{−4}(c_n)` by **bilinear / Vaughan / sum-product** methods
(`bilinear_probe.py`). These need the index `n` to couple to *multiplicative* structure of the summand. But
`c_n = (3^n c_0 − T_n)/2^n` makes `c_n mod 4` a function of the **high bits of the dynamical carry `T_n`** (the
whole parity history) — no multiplicative function of `n` controls it. Verified (`N=10⁵`):
- **Uncorrelated with Liouville `λ(n)`:** `Σ_n f(n)λ(n)` has the *same* square-root size as `S_N` itself (no
  enhancement) — `f(n)=χ_{−4}(c_n)` multiplies against `λ` like an independent `±1`.
- **Flat over arithmetic progressions:** the mean of `f` over `n ≡ a (mod q)` is `≈ 0` for `q=2,3,4,5,8` (spreads
  `0.01–0.04`, CLT noise) — `f(n)` does not depend on `n`'s residue.
So **Vaughan's identity / Type-I–II / sum–product have no entry point**: the summand is a positive-entropy
*dynamical* function of `n`, not a multiplicative one. The only available cancellation is **dynamical** (Birkhoff
for the specified point) = the equidistribution wall.

## Three tool-families, three distinct structural reasons (the meta-finding)
The orbit evades each major unconditional tool family for a **tool-specific** reason — strong evidence the wall is
real, not an artifact of one framing:
| tool family | what it needs | why the orbit blocks it |
|---|---|---|
| measure / spectral (5 probes) | a uniquely-ergodic or rank-≥2 / a.e. handle | rank-1, continuum of measures; needs infinitary input |
| p-adic Baker / S-units | bounded-height algebraic inputs | `height(T_n) ≈ n·log₂3` — **unbounded** |
| character sum / bilinear | multiplicative structure in `n` | `c_n mod 4` = high bits of dynamical `T_n` — **structureless** |
Each closure is a *different* precise obstruction; together they pin the wall from three independent technologies.

## Honest caveats
- Empirical to `n=3·10⁵` (energy) / `10⁵` (bilinear); the `|S_n|=o(n)` (let alone signed) limit is the open problem.
- The character-sum reduction is exact; the "sign-blind" obstruction is a rigorous property of the quadratic form,
  not a heuristic — it is *why* a symmetric second moment cannot prove a one-sided bound. The "structureless"
  finding is empirical (correlation tests), consistent with the exact `c_n=(3^n c_0−T_n)/2^n` structure.
