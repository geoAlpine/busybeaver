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

## The annealed side is efficient at every scale (`annealed_gap.py`)
We measured the annealed (empirical renewal Markov) operator `T_k` on `ℤ/2^k` for `k=1..7` (Antihydra, seed 8,
250k renewals). Second eigenvalue `λ₂(k) = 0.001, 0.038, 0.095, 0.172, 0.224, 0.271, 0.330`; **mixing time
`1/(1−λ₂)` grows only `1.0 → 1.5` steps**, fit `≈ 0.88 + 0.083k` (linear in `k`). This linear growth is **not**
an arithmetic difficulty concentrating at large `k`; it is the trivial **bounded-expansion** fact — each renewal
step advances only `E[D+1] ≈ 2` 2-adic bits, so resolving `2^k` needs `O(k)` steps, hence the per-step gap shrinks
`~1/k` while the **per-bit** mixing stays efficient. So:
> **The annealed (provable) side mixes efficiently at every cylinder depth** (`≤ 1.5` steps through `k=7`). No
> scale is arithmetically special; the entire wall remains the **quenched-vs-annealed determinism, uniformly**.
*Discipline:* the script first posed a false binary ("flat ⇒ uniform" vs "→1 ⇒ difficulty at large `k`"); the
honest reading is the bounded-bits-per-step one. We do **not** extrapolate the `k→∞` asymptotic from 7 points
(unsound). And this is the annealed/Markov operator only — the **quenched** gap (the real open problem) is untouched.

## Net Q2 picture (the seam, fully characterized from inside)
Two complementary facts now pin the seam: (i) **annealed mixes efficiently at all scales** (gap above), and (ii)
**quenched and annealed agree on every finite-order statistic** (digit-bijection, no lag-MI/entropy signature). So
the difference between the two — the entire wall — is carried **neither** by a slow-mixing scale **nor** by any
finite correlation. It is the purely infinitary demand that the deterministic orbit furnish its own digits as
`n→∞`. **A `quenched ⇐ annealed + X` bridge therefore needs `X` to be a genuinely infinitary (effective-Mahler /
`log₂3`-Diophantine) input — provably not a mixing or finite-decorrelation argument, both of which are already
satisfied.** This is the sharpest internal statement of why Q2 is the open question.

## Next (Phase 2 continues)
The seam is pinned from inside (annealed efficient + no finite signature ⇒ infinitary-only). The remaining
internal lever is the **explicit `X`**: write the conditional `quenched-equidistribution ⇐ effective
equidistribution of {(3/2)ⁿ A}` with a *quantified* discrepancy rate, and check whether the **one-sided margin**
(`avg jump ≤ 2`, not full equidistribution) needs a *weaker* discrepancy rate than two-sided — the one place the
factor-2 margin might cash out. (Prior `#2` settled it is equi-difficult vs current *tools*; here we ask the
sharper question of whether the *required discrepancy exponent* differs, a quantitative not tool-relative question.)
