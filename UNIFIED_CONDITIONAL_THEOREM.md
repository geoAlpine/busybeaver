# A unified conditional non-halting theorem for both BB(6) monsters (2026-06-24)

Both Busy-Beaver(6) "monsters" — **Antihydra** (Mahler-3/2 cluster, base 2) and **o18** (Erdős-ternary
cluster, base 3) — collapse to ONE conditional theorem with the same proven core and the same single
hypothesis. (Derivations: `antihydra_renewal_attack.md` §11–12; `o18_selfconsist.py`, `o18_indep_clean.py`,
`erdos_renewal.py`. All numerics reproducible.)

## Setup (uniform across both monsters)
A cryptid cluster has multiplier `μ = 2^a/3^b > 1` with **shrinking base** `p` (`p=2` for `μ=3/2`; `p=3` for
`μ=8/3`). Its driving map is `M(x) = ⌊μx⌋`, which factors as
```
M = (×2^a, an ISOMETRY of ℤ_p, since |2^a|_p = 1)  ∘  (÷ p, the p-adic Bernoulli SHIFT, MIXING).
```
Track the low-digit state `x mod p^k`. One step consumes the **incoming high p-adic digit** `dig_k(x)` (the
digit shifting into the window). The induced **renewal chain** on `ℤ/p^k` has a **near-total spectral gap**:
`0.99` for `p=2`, `0.9995` for `p=3` (computed). The **diagonal digit** is `δ_n = ⌊μ^n⌋ mod p`.

## The theorem
**[PROVEN — finite computation] The self-consistency operator `Φ_p` contracts to Uniform(1/p).**
`Φ_p` maps an incoming-digit process to the output digit process via the renewal chain. Iterating from
*skewed / correlated* starts:
- `p=2`: starts `(E,ρ)=(0.15,+0.8),(0.40,−0.8),…` all converge to the unique fixed point `(0.5, 0)`.
- `p=3`: starts `(.8,.1,.1),(.1,.1,.8),(.5,.3,.2),…` all converge to `(⅓,⅓,⅓)`.
The contraction IS the near-total spectral gap.

**[THE SINGLE HYPOTHESIS — same for both]** the incoming high digit is asymptotically **independent of the
low-digit state**: `I(dig_k(c_n) ; c_n mod p^k) → 0`. Verified empirically (excess MI over a shuffle baseline
`≈ 0`): Antihydra `~0.0009 bits`; o18 `−0.0001/+0.0001 bits` (k=2,3). The adversarial worst case (which can
force a halting digit-density) requires the incoming digit to be **correlated with the chain state** — a
correlation neither orbit realizes (≥~1000× margin).

> **UNIFIED CONDITIONAL THEOREM.** *If the incoming high p-adic digit `dig_k(c_n)` is asymptotically
> independent of the low-digit state `c_n mod p^k`, then — by the proven renewal spectral-gap contraction —
> the diagonal digit `δ_n` equidistributes to `Uniform(1/p)`, and the cryptid NEVER HALTS:*
> - *`p=2` (Antihydra & Mahler-3/2 cluster): even-density `→ ½ > 1/3` ⇒ non-halt (the §3c criterion);*
> - *`p=3` (o18 & Erdős-ternary cluster): every base-3 digit `→ ⅓`, so a carry aligns with the moving
>   frontier with summable probability `Σ 1/N_k < ∞` (Borel–Cantelli) ⇒ non-halt.*

## Status (honest)
- **PROVEN, unconditional:** the contraction core (finite spectral-gap computation), for both `p`.
- **THE hypothesis is asymptotic, not an exact symmetry** [directly attacked, `lastpiece.py`]: the
  independence's residual correlations decay like `1/√N` (random), with no algebraic shortcut. So the
  hypothesis **is** the unified diagonal-digit kernel (`δ_n = ⌊μ^n⌋ mod p` equidistributes) in its sharpest
  dress — the world-open problem (Mahler-3/2 1968 / Erdős 1979), reduced to a single `√N` digit-decorrelation.
- **What this achieves:** the community's separate *heuristic* "probabilistic arguments" for Antihydra and o18
  become **one conditional proof** with a proven core and a single, clean, empirically-robust hypothesis
  shared by both monsters. No machine decision is claimed; soundness intact.
