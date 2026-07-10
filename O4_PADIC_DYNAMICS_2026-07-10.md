# o4 as a 3-adic dynamical system — the δ₋₁₄ repelling fixed point IS the run-cap; frequency = forward-orbit equidistribution to Haar = (K), not effective (2026-07-10)

*A genuinely different lens on the (K) wall: the 3-adic dynamics of the o4 host map as a
dynamical system (Benedetto / Rivera-Letelier non-archimedean Fatou–Julia theory), not
equidistribution/rigidity/transfer-operator. Question: is the integer orbit's shadowing of
δ₋₁₄ controlled by 3-adic dynamical structure? STRICT `[PROVEN]`/`[OBSERVED]`/`[OPEN]`;
exact 3-adic arithmetic (`scratchpad/o4_padic_dynamics.py`). Not committed.*

---

## 0. What object we are actually iterating `[clarified — matters for the theory]`

The host map is `T(v) = (4v + e(v mod 3))/3`, `e = {0:9, 1:14, 2:1}`, branch fixed points
`x_ρ = −e = {−9, −14, −1}`. **T is NOT a single rational function of `v`** — `e(v mod 3)`
is not rational — it is **piecewise-affine on the three residue classes** of `ℤ₃`, each
class clopen. So the correct dynamical objects are two:

- **(a) a single affine branch** `b_ρ(v) = (4v+e(ρ))/3` (degree 1, the run dynamics), and
- **(b) the full self-map** `T : ℤ₃ → ℤ₃`. Since `|4/3|₃ = 3`, each branch **expands 3-adic
  distance by exactly 3**, mapping its residue class (radius 3⁻¹) *onto* all of `ℤ₃`
  (radius 1) bijectively. Hence **T is a 3-to-1, everywhere-expanding, full-branch self-map
  of `ℤ₃`** (the "loses one 3-adic digit per step" of the transfer note, now as a dynamical
  fact). This is the degree ≥ 2 object where Julia/equilibrium theory lives.

## 1. The multiplier — δ₋₁₄ is 3-adically REPELLING `[PROVEN, exact]`

`b_ρ'(v) = 4/3`, and `|4/3|₃ = 3^{−v₃(4/3)} = 3^{−(0−1)} = 3 > 1`. So **all three branch
fixed points −9, −14, −1 are 3-adically repelling with identical multiplier |·|₃ = 3.**
Verified exact (`§1` of the script): each `b_ρ(x_ρ)=x_ρ`, multiplier 3, repelling.

Consequence for the theory: an affine (degree-1) map has **empty Julia set and no
equilibrium measure** (Brolin/Favre–Rivera-Letelier need degree ≥ 2). On Berkovich `ℙ¹`
the branch `v ↦ (4/3)v + 14/3` is a loxodromic Möbius map: repelling Type-I fixed point
−14, attracting Type-I fixed point ∞, and `ℙ¹∖{−14}` is the single attracting basin of ∞.
**All the run dynamics carries is the multiplier.**

## 2. The run-cap as a p-adic dynamical statement `[PROVEN, exact — clean restatement, old content]`

Inside a ρ=1 run, `b₁(v) − (−14) = (4/3)(v+14)`, so `|v_n+14|₃` multiplies by exactly 3 and
`v₃(v_n+14)` drops by exactly 1 each step. The orbit escapes −14 at the geometric rate fixed
by the repelling multiplier; the run ends when `v₃` hits 0. Therefore

> **run length = v₃(v₀ + 14) = (3-adic closeness to δ₋₁₄), i.e. the run-cap IS "geometric
> escape from a repelling fixed point at rate |mult|₃ = 3."**

Script `§2`: an explicit 6-deep seed escapes in exactly 6 steps; exhaustive check `v₀=−14+m`,
`m≤20000`: **0 mismatches**. This is a genuinely *new description* of the mirror-ladder run
law (`PAPER_MIRROR_LADDER §1`, `O4_RUN_STRUCTURE §1`) — but it is the **depth axis**, already
unconditionally controlled. No new content: the multiplier only sees one branch = one run.

## 3. The genuinely new question — beyond the multiplier `[OBSERVED + literature]`

p-adic dynamics offers structure past the multiplier: wandering domains, the Julia set, and
the **equilibrium (maximal-entropy) measure**. We ask whether any bounds the **frequency** of
returns to the δ₋₁₄ shadow.

**Equilibrium measure of the full map = Haar `[OBSERVED, and structurally forced]`.** The
full 3-to-1 expanding, full-branch map T has as its measure of maximal entropy the balanced
measure spreading `1/3` onto each inverse branch — on `ℤ₃` this is **Haar (uniform)** (same
object as the transfer-operator's Haar-stationary density, `O4_TRANSFER_OPERATOR §1`). Under
Haar the frequency of `{ρ=1 to depth L}` is exactly `2·3^{−(L+1)}`. Script `§3`, real orbit
`G₀=8`, `N=1.2·10⁵`: `ρ`-frequencies `0.3321/0.3330/0.3349` (Haar 1/3), depth histogram
`0.2211, 0.0741, 0.0251, 0.0085, 0.0028, …` vs Haar `0.2222, 0.0741, 0.0247, 0.0082, 0.0027`.
**The orbit empirically equidistributes to the equilibrium measure Haar.** So frequency-of-ρ=1
= Haar-measure-of-the-shadow — *provided* the forward orbit equidistributes to Haar.

**Is that equidistribution EFFECTIVE?** Here the p-adic theory is decisive and negative, for a
sharp reason. Every effective equidistribution theorem in non-archimedean dynamics equidistributes
the **WRONG orbit**:

- **Brolin / Favre–Rivera-Letelier** (`arXiv:math/0407469`, `math/0407426`): the **iterated
  preimages** (backward orbit) of a point equidistribute to the equilibrium measure. Effective
  because the `d`-to-1 preimage tree *injects branching entropy* — this is the **annealed**
  direction, the exact analog of the transfer-operator's near-maximal gap (`O4_TRANSFER §3`).
- **Baker–Rumely–Hsia / Bilu / Yuan** (`arXiv:math/0407426`, `1210.7885`): Galois orbits of a
  sequence of points of **height → 0** equidistribute. Our orbit is a *single forward orbit* of
  the fixed rational point 8 with `h(G_n) ∼ n·log(4/3) → ∞` — **growing height, the exact
  opposite hypothesis.** The machinery is inapplicable in principle, not merely in practice.

The **forward orbit of one rational point** equidistributing to the equilibrium measure is not
a theorem of p-adic dynamics for any non-trivial map — it is a genuinely ergodic (quenched
Birkhoff / decay-of-correlations) statement, as hard as its archimedean cousin. Script `§3`
rate test: the single-orbit character `|N⁻¹Σ e_{3⁴}(G_n)|` decays as `1/√N` (`0.0031` at
`N=1.2·10⁵`, tracking `1/√N=0.0029`), the **CLT/Birkhoff floor** — NOT the geometric annealed
rate the equilibrium measure's mixing would give. Frequency is the time-average, and its rate
is the quenched question.

**Wandering domains / Julia structure — no help `[OPEN, argued]`.** Benedetto's
no-wandering-domains results constrain the *topology of Fatou components* of a single rational
map. Even granted, they say nothing about the *frequency of a forward orbit's returns to a
clopen set* — an ergodic quantity orthogonal to Fatou/Julia topology. For our affine branch the
Julia set is empty; for the full expanding map all of `ℤ₃` is repelling (the Julia set is `ℤ₃`),
which again gives Haar as the natural measure but no frequency control on a single orbit.

## 4. Verdict `[honest]`

- **`[PROVEN]`** The multiplier at δ₋₁₄ is `|4/3|₃ = 3` (repelling); the run-cap is *exactly*
  geometric escape from this repelling fixed point (`v₃(v_n+14)` drops by 1/step, run
  = `v₃(v₀+14)`). A clean new **description**, verified exact — but depth, not frequency, and
  already known content.
- **`[OBSERVED]`** The full 3-to-1 expanding map's equilibrium / maximal-entropy measure is
  Haar; the integer orbit **does** empirically equidistribute to it, so ρ=1-frequency = Haar
  measure of the δ₋₁₄ shadow.
- **`[OPEN, and structurally so]`** p-adic equidistribution is **NOT effective for this orbit.**
  The effective non-archimedean equidistribution theorems govern **backward orbits** (preimage
  branching = annealed = the transfer-operator gap) and **height→0 Galois orbits** (our orbit
  has height→∞) — both are the *wrong object*. Forward single-orbit equidistribution to the
  equilibrium measure is the **quenched Birkhoff rate (1/√N observed)** = (K) = Mahler 3/2 /
  AEV Conj 1.6. **p-adic dynamics gives the DEPTH (run-cap) but not the FREQUENCY**, and the
  seam is exactly the annealed/quenched (backward/forward) split already located spectrally
  (`O4_TRANSFER_OPERATOR §3–5`). No independent height/Baker input exists in the direction
  that would help, because the orbit's height grows.

**Placement:** this is the third operator/dynamics-flavored tool to reach (K) by the same door
— rigidity cocycle (faithful, no gap), annealed RPF operator (maximal gap, but injects a
digit), and now non-archimedean Fatou–Julia (effective only for backward/small-height orbits).
All three separate the annealed/backward object (effective) from the quenched forward orbit
(= (K)). δ₋₁₄ is the exact seam: a *repelling* fixed point (§1, giving depth) whose *return
frequency* is the equilibrium measure a single deterministic orbit is not known to see
effectively.

## Reproduce
`scratchpad/o4_padic_dynamics.py` — `§1` multipliers (exact), `§2` run-cap = geometric escape
(explicit + exhaustive m≤20000, 0 mismatches), `§3` orbit equidistribution to Haar + 1/√N rate
test. Basis: `O4_RUN_STRUCTURE_2026-07-07`, `PAPER_MIRROR_LADDER`, `O4_TRANSFER_OPERATOR_2026-07-10`.
Literature: Benedetto, *Dynamics in One Non-Archimedean Variable* (GSM 198); Favre–Rivera-Letelier,
*Théorème d'équidistribution de Brolin p-adique* (arXiv:math/0407469); Baker–Rumely, *Equidistribution
of small points* (arXiv:math/0407426).

No machine decided. No label upgraded.
