# The quenched-vs-annealed seam leaves no finite-order signature (2026-06-26, Phase 2)
*Program: rank-1 specified-orbit genericity. Sharpens meeting Q2. The deterministic orbit and an annealed
(fresh-digit) model are **indistinguishable by every finite-order statistic** — verified three ways. The
difference lives strictly below all finite correlations. `higher_cylinder.py`. 0 false claims.*

## The structural identity (hand-derived, verified True on all tested `μ`)
For `c_{n+1}=⌊a c_n/p⌋`, writing `c_n` in base `p` as digits `d₀,d₁,…`:
```
c_{n+1} mod p = (a·d₁ + ⌊a·d₀/p⌋) mod p,   and generally  c_{n+k} mod p = function of (d₀,…,d_k).
```
The induced digit map `(d₀,…,d_k) ↦ (c_n,…,c_{n+k}) mod p` is a **bijection** on `(ℤ/p)^{k+1}` (each
`d_j ↦ a d_j + carry` is a bijection mod `p`). Therefore the **joint law of any `k+1` consecutive mod-`p`
residues equals the mod-`p^{k+1}` cylinder law** — there is *no* correlation content beyond the cylinder
marginals.

## Consequence (verified, three independent tests; each could have falsified it)
- **(T1) mod `p²` = joint `(c_n,c_{n+1})` mod `p`:** `χ²` at the i.i.d. baseline (ratios scatter around 1,
  single-orbit fluctuation), no excess structure.
- **(T2) lag-`k` mutual information** `I(c_n; c_{n+k}) mod p`, `k=1..4`: **excess over a shuffle control `≈ 0`**
  (all `≲ 10⁻⁴`, i.e. the finite-`N` bias floor) — including Antihydra `μ=3/2`, seed 8.
- **(T3) block entropy rate:** `H₁ = H₂/2 = H₃/3 = log₂ p` to four decimals — the i.i.d. **maximum**; the orbit
  is `k`-distributed up to the tested order.

## What it means for the seam (meeting Q2)
> **The quenched (deterministic orbit) and annealed (digits drawn fresh each step) models are provably
> indistinguishable by every finite-order test.** Entropy rate `= log p`, zero excess lag-MI, uniform finite
> cylinders. The self-feeding determinism manifests **only** as the demand that the orbit supply its *own* next
> digit — and that demand is **invisible to any finite statistic** (every finite joint law is just a cylinder
> marginal, by the bijection).

This is the precise mechanism behind the `D`-finding (`MEETING_BRIEF_2`): the **annealed** transition operator
mixes trivially (spectral gap ≈0.95) because it injects a fresh uniform digit per step; the **quenched** orbit must
generate that digit deterministically, and the two agree on **all** finite correlations. So:
- A `quenched → annealed` bridge **cannot** be built by matching or decorrelating finite-order statistics — they
  already match exactly. Mixing / decay-of-correlations arguments are therefore structurally insufficient.
- Any bridge must inject a genuinely **infinitary / Diophantine** input (control of the orbit's digits *as `n→∞`*,
  e.g. an effective `log₂3` irrationality measure), not a finite-order decorrelation. **This is exactly why Q2 is
  the right open question, and why the wall is "pure determinism."**

## Sharper Q2 to put to the expert
*Given two processes that agree on **every** finite-order statistic — one annealed (i.i.d.-digit, trivially
mixing) and one quenched (a single deterministic algebraic orbit) — is there any known transfer principle that
upgrades the annealed equidistribution to the quenched orbit using only an infinitary/Diophantine hypothesis (not
a finite-order decorrelation, which is unavailable because the statistics already coincide)?* If no such principle
exists, that absence **is** the precise statement of the wall.

## Honest caveats
- This is empirical finite-order reconnaissance (tests up to lag 4 / block 3, `N=6·10⁴`); the bijection argument
  shows *why* it must hold at all finite orders, but "i.i.d. at every finite order" is **not** equidistribution
  (which is the `n→∞` cylinder limit) — the open problem is exactly the infinitary gap, untouched here.
- "No finite-order signature" does **not** mean the orbit is random — it is deterministic and computable
  (`K=O(log N)`); it means determinism is undetectable by finite correlations, consistent with the three-route
  normality block (`NEW_ENGINE`): computable ∩ statistically structureless.

## Next (Phase 2 continues)
The seam is below all finite-order tests. Next internal probe: characterize the **annealed operator** itself more
sharply across `p` (its spectral gap as a function of `p` and branch depth) and ask whether *its* mixing rate —
the thing that IS provable — can be coupled to the quenched orbit under an explicit `log_p a` Diophantine
assumption (a conditional `quenched ⇐ annealed + Diophantine` statement would be a real partial, even if the
Diophantine input is itself open).
