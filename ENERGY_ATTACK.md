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

## Honest caveats
- Empirical to `n=3·10⁵`; the `|S_n|=o(n)` (let alone signed) limit is the open problem.
- The character-sum reduction is exact; the "sign-blind" obstruction is a rigorous property of the quadratic form,
  not a heuristic — it is *why* a symmetric second moment cannot prove a one-sided bound.
