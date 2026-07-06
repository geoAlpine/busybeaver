# o4 a-ledger analysis — itinerary bijection (seed-specificity PROVEN), ruin quantification, the small-a map, and the real-orbit margin (2026-07-06)

*Direct attack on the a-ledger conjecture (the sole remaining `[OPEN]` core of o4 after the template closure). Three
results: (1) an **itinerary bijection theorem** `[PROVEN]` — every residue pattern is realized by exactly one seed
class, so fatal orbits EXIST for every a₀ and **no seed-uniform safety theorem can exist** (the o4 analogue of the
Antihydra No-Structure theorem); (2) the annealed **ruin constant η≈0.3349** quantifying the margin; (3) the **small-a
region mapped**: k-irregular mix {LAND/HALT/WANDER} — the safety direction (⟸) is unaffected; the ⟺ is precisified.
Real-orbit ledger extracted to G≈884k: margin enormous and widening. o4 `[OPEN]`. No machine decided.*

## 1. The ledger conjecture (o4's decision, formal statement)
Odometer `3G′ = 4G + e(ρ)`, `ρ = G mod 3`, `e = {0:9, 1:14, 2:1}`; ledger `a′ = a + δ(ρ)`, `δ = {1:−1, 2:+4, 0:+6}`.
**Conjecture (⟸ o4 non-halt, PROVEN direction):** the orbit from the template-regime seed
(`G=43, a=17` — first milestone with G≥37; earlier generations concrete-verified) never has `a ≤ 1` at a `ρ=1`
generation. Real-orbit status: `[OBSERVED]` to G=8.8M (via the 5×10¹³-step run) with the δ-rule exact.

## 2. Itinerary bijection theorem `[PROVEN]` — seed-specificity
**Theorem:** for every `L≥1`, the map `{G mod 3^L} → (ρ₀,…,ρ_{L−1})` is a **bijection**.
*Proof:* write `G = 3H + ρ`; then `G′ = (4G+e(ρ))/3 = 4H + s(ρ)`, `s = {0:3, 1:6, 2:3}`; `H ↦ 4H+s` is a bijection of
`ℤ/3^{L−1}` (4 invertible); induct. ∎ (Verified exhaustively L=1..8 + identity on 10⁴ random (H,ρ);
`o4_ledger_bijection.py`.)
**Consequences:**
- **Fatal orbits exist for every a₀:** the pattern `ρ=1` repeated `a₀` times is realized by a full seed class mod
  `3^{a₀}`; from any such seed the ledger hits `a≤1` at a `ρ=1` step. Combined with the fatal-region map (§4, e.g.
  `Z(41,3,0)` halts), the template family contains **halting orbits arbitrarily deep in the parameter space**.
- **No seed-uniform safety theorem exists** — safety genuinely depends on the seed's full 3-adic expansion; the safe
  seed set is a closed 3-adic Cantor-type set (complement of a countable union of cylinders). This is the **o4
  analogue of the No-Structure theorem**: any proof of the ledger conjecture must use the SPECIFIC seed's arithmetic —
  the same "orbit-specific" character as `(K)`, now `[PROVEN]` at the B2 flagship.

## 3. Ruin quantification `[annealed, exact numerics]`
For the uniform-random itinerary (the annealed model), `P[ledger ever fatal from a] ~ η^a` with **η = 0.334895**
(root of `(η⁻¹+η⁴+η⁶)/3 = 1`; note η ≈ 1/3). Margins: a=8 → 1.6×10⁻⁴; a=34 → 7×10⁻¹⁷; a=124 (current frontier) →
3×10⁻⁵⁹. The conjecture is annealed-certain; the quenched (specific-orbit) statement is the open content — the exact
count-vs-frequency shape of `(K)`, but with drift +3/generation instead of Antihydra's zero-margin criticality.

## 4. The small-a (fatal-region) map `[OBSERVED, 3M-step runs]`
`Z(k, g=3, a)` for `a∈{0,1}`, k odd 19..101 — **genuinely k-irregular** (the digit-dependent wall's residue):
| a | LAND (recovers, a′≥3) | HALT | WANDER >3M |
|---|---|---|---|
| 0 | k=19,25,31,61 (G′=2k+29!, a′=3) | **k=41 @55,170** | k=21,23,27,29,101 |
| 1 | k=19,21,25,27,29,31,61,101 (a′∈{3,4,6}, G′ off-template) | — | k=23,41 |
Recovery landings follow a DIFFERENT (still milestone-landing) template branch (`G′=2k+29` at a=0 etc.). **The safety
direction is unaffected:** o4 non-halt ⟸ ledger stays ≥2 `[PROVEN]`. The ⟺ precisifies to: hitting `a≤1` at `ρ=1`
enters a k-dependent finite mix {recover to a′≥3 / halt / unresolved}; the unresolved WANDER cases are `[OPEN]`
(not needed for the safety reduction).

## 5. The real-orbit ledger `[OBSERVED, exact to G=883,719 here; G=8.8M in the big run]`
| n | G | a | ρ | | n | G | a | ρ |
|---|---|---|---|---|---|---|---|---|
| 0 | 3 | 3 | 0 | | 20 | 3,727 | 63 | 1 |
| 5 | 43 | 17 | 1 | | 26 | 20,983 | 90 | 1 |
| 9 | 151 | 30 | 1 | | 31 | 88,462 | 99 | 1 |
| 12 | 367 | 37 | 1 | | 36 | 372,814 | 115 | 1 |
δ-rule exact for G≥37 (and odometer exact throughout). **Min a at any ρ=1 generation: 9 (startup, G=7); in the
template regime: 12 (G=19), then 17, 30, 37, 54, 63, …, 115 — growing ≈+3/generation.** Longest observed ρ=1 run: 2
(three occurrences: n=26–27, 30–31, 35–36). The margin is enormous and widening; combined with §3, the cumulative
ruin heuristic from the current frontier is ~10⁻⁵⁹.

## 6. Verdict `[honest]`
**(b) — the ledger conjecture is now fully characterized:** seed-specific by a PROVEN bijection (no structural
escape), annealed-certain with an exact ruin constant, fatal region mapped (safety direction unharmed), real-orbit
margin enormous. The open content is exactly a quenched one-sided prefix condition on a specific 3-adic itinerary —
`(K)`'s species, o4's instance, with a +3-drift margin that makes it the **easiest-margin open case in the whole
cryptid family** (and hence the most promising place for a first genuine decision, if any orbit-specific tool ever
materializes). o4 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce
- `o4_ledger_bijection.py` (bijection L=1..8, proof identity, η).
- Small-a map: inline (Z(k,3,a) classification, 3M steps each).
- Real-orbit ledger: instrumented `o4_bouncer_macro.py` milestones (G,a,ρ) to G=883,719; δ-rule + odometer exact.
- Basis: `O4_TEMPLATE_CLOSURE_2026-07-06.md` (+ red-team corrections), `o4_redteam_*.py`.
