# The TRACKING BRIDGE — does the mean-field contraction reach the single orbit? (2026-06-28)

The single named OPEN gap of the contraction route (`mckean_contraction.py`, `NEW_FRAMEWORK.md`):
the contraction makes the mean-field fixed point `ν*=Haar` **unique and attracting** at the level of
*distributions*; the gap is whether the **single deterministic orbit** `c₀=8, c_{n+1}=⌊3c_n/2⌋` has its
empirical low-bit measure **track** `ν*`. This note formalizes the claim, settles whether contraction
implies single-orbit convergence (it does not), tests it numerically, and states plainly whether the
bridge is a genuine sidestep or reduces to the known [OPEN] effective-equidistribution core. Zero false
proofs; every line labelled. **NOT committed to git.**

## 1. The precise tracking lemma — what exactly must be shown

Let `s_n^{(k)} = c_n mod 2^k ∈ ℤ/2^k` be the low-bit state, and the **empirical measure**
`μ_N^{(k)} = (1/N) Σ_{n<N} δ_{s_n^{(k)}}`. The mean-field fixed point is `ν* = Haar`, i.e.
`ν*^{(k)} = uniform on ℤ/2^k`.

> **TRACKING LEMMA (target).** For each fixed `k`, `μ_N^{(k)} → uniform` as `N→∞`, **with an effective
> rate** `‖μ_N^{(k)} − unif‖₁ ≤ f_k(N) → 0`. Equivalently: the orbit equidistributes mod `2^k`.

The complete proof needs strictly less — only the `k=1` marginal with one-sided slack:
`|E_N/N − 1/2| < 1/6` for all `N > N₀` (`E_N` = #evens), `+` the finite check `n ≤ N₀` (`PROOF_STATUS §0`).
But it must be **effective** (an `all-n` tail bound), not merely asymptotic.

**[OBSERVATION — soundness] Formalizing the tracking claim reproduces the open core verbatim.** The
tracking lemma *is* line (5) / kernel (K) / Mahler–AEV: single-orbit equidistribution of `{(3/2)ⁿ}`-type
data. So "tracking" is not a new, smaller statement — written precisely, it equals the kernel.

## 2. Does the contraction alone give single-orbit convergence? — NO. [PROVEN structurally]

The contraction is a statement about the map `S: P(ℤ₂) → P(ℤ₂)`, `ν ↦ L_ν ν`, on the space of
**probability measures**: `S` has a unique fixed point Haar and `S^m(ν₀) → Haar` geometrically
(rate `≤ λ₂(L) + ‖F‖ ≈ 0.04`). This governs the evolution of **distributions** (the annealed /
McKean–Vlasov flow). A single orbit is **one deterministic point**, and `μ_N` is a **time average along
one path**. "`S` contracts ⟹ `μ_N(one orbit) → ν*`" is **false in general**, for three independent
reasons:

1. **Same wall as (4)→(5).** Contraction of `S` lives at the level of measures; it cannot see a
   **Haar-null** orbit (integers are dense but Haar-null in `ℤ₂`). This is exactly the gap between
   "[PROVEN] (4) the transfer operator has a spectral gap ⇒ **Haar-a.e.** point equidistributes" and
   "[OPEN] (5) **this specific** Haar-null point is generic." The nonlinear `S` does not move that wall.

2. **What the nonlinear `S` actually buys is orthogonal to tracking.** Over the linear `L`, `S` buys only
   that **other** self-consistent measures are excluded (atomic invariant measures are not self-consistent
   — the variational-principle *sidestep*, `mckean_contraction.py`). It does **not** upgrade distributional
   convergence to single-trajectory convergence. Both `L` and `S` act on `P(ℤ₂)`, never on a point.

3. **No chaos hypothesis to propagate.** In McKean–Vlasov theory the bridge from mean field to realizations
   is **propagation of chaos**, which requires an **ensemble of `N` exchangeable particles with independent
   driving noise**; the LLN over the ensemble concentrates the empirical measure on the mean field. Here
   there is **no ensemble and no independent noise** — one deterministic trajectory. The "particles" are the
   successive states `s_n`, whose joint law **is** the orbit; they are not asymptotically independent. The
   chaos hypothesis (asymptotic independence/decorrelation) is precisely what is missing — and it is
   precisely the decorrelation/equidistribution being claimed. **Single-orbit determinism breaks the chaos
   hypothesis.**

**Conclusion of §2:** contraction of the mean-field map does **not**, by itself, imply single-orbit
convergence. (This matches the focused-document audits `ROUTE_RENEWAL_CLT §7` and `PROOF_STATUS §3.8`.)

## 3. Numerical findings — the orbit tracks, but at the ergodic (CLT) rate, NOT the contraction rate

`tracking_test.py` (`.venv` python, numpy; orbit to `N=2·10⁶`, full bigint, ~4 min):

```
         N   |E/N-1/2|  L1(mod4) L1(mod8) L1(mod16) L1(mod32)
     10000     0.00460   0.01680  0.02060   0.03300   0.04440
    100000     0.00159   0.00368  0.00548   0.01016   0.01466
   1000000     0.00050   0.00127  0.00207   0.00345   0.00494
   2000000     0.00053   0.00135  0.00208   0.00284   0.00368

fitted  metric ~ N^{-β} :   even-dev β=0.22 ;  L1 mod 2^k : β = 0.39, 0.44, 0.44, 0.46
mean-field L^t δ₀ → uniform (k=4):  t=1:1.75  t=2:1.50  t=3:1.00  t=4:0.0  (EXACT in 4 steps)
```

- **[OBSERVED] The orbit DOES track Haar.** `μ_N^{(k)} → uniform` for every tested `k`; even-density `→ 1/2`.
  So the *target* of the tracking lemma is empirically correct (consistent with bbchallenge / `flp_margin`).
- **[OBSERVED — the decisive contrast] The rate is the ergodic/CLT power law `≈ N^{-1/2}`, NOT geometric.**
  `L1(mod 2^k)` decays as `N^{-0.4..0.46}` (≈ CLT `1/√N`); even-density `N^{-0.22}` (slower, noisier, still
  → 0). Meanwhile the **mean-field/transfer operator** relaxes a delta to uniform **exactly in 4 steps**
  (one-step exact, geometric/finite). The contraction's geometric rate (`0.04`) **does not appear anywhere**
  in the orbit's convergence.
- **[READING] Numerically, single-orbit convergence is a different phenomenon from mean-field relaxation.**
  The orbit converges because of **ergodic time-averaging of one path** (CLT rate), not because the mean-field
  map is a contraction (which would be near-instant geometric). This is direct evidence that the bridge is
  **not** the contraction.

## 4. The bridging ingredient — and whether it reduces to the known core

**The proposed mechanism (renewal/regeneration):** even steps are renewal points, gaps `g_i = v₂(c−1)`,
parity sum `= Σ(2 − g_i)`; a renewal/Gibbs–Markov CLT would give `Σ(2−g_i) = O(√K) = o(N)` ⇒
even-density `→ 1/2`. Empirically (`renewal_clt.py`) `|S|/√K = O(1)`, mean gap `2.002`, gap autocorrelations
null, mean gap `≈2` in every base-phase window. So the *hypotheses* of a renewal-CLT are all measured.

**[STANDARD] The GM-CLT is a real theorem — but for the wrong realization.** Gibbs–Markov CLT/LLN holds
for the **invariant (Haar/Gibbs) measure**: for a `μ`-typical realization, or a genuinely **random**
environment where the inter-renewal blocks are independent/mixing. For the **single deterministic orbit**
the blocks are **not** independent; their joint law is the orbit. The required input is an **effective
mixing / decorrelation bound on the self-generated gap sequence `{g_i}`**.

**[REDUCTION — the answer to the crux] The bridge is NOT an independent sidestep; it reduces to the known
[OPEN] effective-equidistribution core.** The gaps are functions of `s_n mod 2^k`, so "the orbit's renewal
gaps decorrelate / satisfy a CLT" is **equivalent to** "the orbit equidistributes mod `2^k`" = the tracking
lemma = kernel (K) = Mahler/AEV. The contraction supplies:
- the **target** (where the orbit must go) and its **uniqueness** (only Haar is self-consistent), and
- **linear stability** (Haar is attracting at the *distributional* level, `‖F‖<1` qualitatively),

but it does **not** supply the single-orbit tracking. The tracking step **secretly requires the same
effective-equidistribution / decorrelation input**. In `NEW_FRAMEWORK` language: the **qualitative** `‖F‖<1`
gives the unique stable fixed point; the **quantitative closed-loop** `‖F‖<1` (effective mixing of the
orbit's *own* scenery) is the tracking — and **that quantitative closed-loop bound IS the open core**
(`NEW_FRAMEWORK §5` already states this; this note confirms it and rules out a cheaper route).

## 5. Status summary

- **[PROVEN]** Mean-field map `S` is a contraction ⇒ unique, attracting, self-consistent fixed point = Haar
  (engine; `mckean_contraction.py`). Sidestep of the variational-principle UE block holds.
- **[OBSERVED]** The single orbit's empirical low-bit measure tracks Haar, at the **CLT rate `~N^{-1/2}`**,
  **not** the contraction's geometric rate (`tracking_test.py`). Target correct; mechanism is ergodic
  averaging, not distribution relaxation.
- **[PROVEN structurally]** Contraction of the mean-field map does **NOT** imply single-orbit convergence
  (Haar-null orbit; `S` acts on measures; no ensemble/independent noise ⇒ no propagation-of-chaos hypothesis
  to invoke). The single-orbit determinism breaks the chaos hypothesis.
- **[OPEN = Mahler/AEV]** The tracking lemma itself = single-orbit equidistribution mod `2^k` =
  effective mixing of the self-generated renewal gaps = quantitative closed-loop `‖F‖<1`. **The bridge
  reduces to the known core; it is not a sidestep around it.** The contraction is a genuine, provable
  *engine*; the *bridge* is the kernel restated, not a way past it.

**One honest weakening (still open):** even the one-sided `liminf E_N/N ≥ 1/3` (much weaker than the
observed `→ 1/2`) would suffice (`PROOF_STATUS §3`); it too has no proof. The reduction in §4 applies to it
as well — a one-sided decorrelation bound on the gaps is still single-orbit equidistribution-class.
