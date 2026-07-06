# o4 run-structure theorem — exact 3-adic closed forms for itinerary runs; the ledger's failure modes quantified; o4⟷Antihydra mirror unification (2026-07-07)

*Emerged from the "what is needed to close the protections" analysis. THREE-LINE THEOREM `[PROVEN]`: the residue
itinerary's maximal runs have exact 3-adic closed forms via the branch fixed points. Consequences: an UNCONDITIONAL
run cap (kills the single-catastrophic-run failure mode), a sharp quantification of what a ledger failure would
require, and — deepest — the o4 ledger process IS Antihydra's countdown structure in mirror (p,q)-coordinates.
o4 `[OPEN]`. No machine decided.*

## 1. The theorem `[PROVEN]`
The three branch maps `G′=(4G+e(ρ))/3`, `e={0:9, 1:14, 2:1}` have 3-adic (in fact integer) fixed points
`x_ρ = −e(ρ)`: **x₁ = −14, x₂ = −1, x₀ = −9** (each ≡ ρ mod 3). Then:
> **The maximal run of residue ρ starting at G equals `v₃(G − x_ρ)` exactly.**
*Proof:* at the fixed point `3x = 4x + e`, so `e = −x`; hence on a ρ-step
`G′ − x = (4G+e)/3 − x = (4G − 4x)/3 = (4/3)(G − x)` — the distance-to-fixed-point multiplies by exactly 4/3, so
`v₃` drops by exactly 1 per step (4 a unit); and `G ≡ ρ ⟺ 3 | G − x_ρ` since `x_ρ ≡ ρ`. ∎
Verified exhaustively G=3..200,000 (0 mismatches, all three residues) + real orbit 60 generations exact.

## 2. Consequences for the ledger `[PROVEN]`
- **Unconditional run cap:** `run(G) ≤ log₃(G + 14)`; on the real orbit (`G_n ≈ 43·(4/3)ⁿ`),
  **run at generation n ≤ 0.262·n + O(1)**. A ledger drain is −1 per ρ=1 step ONLY, so:
- **The single-catastrophic-run failure mode is impossible** beyond a bounded horizon: sustained pure draining for
  `m` consecutive generations is a ρ=1 run of length `m ≤ 0.262n + 4`, while the verified ledger stands at
  `a₄₀ = 124` — pure-drain fatality would need `n−40 ≤ 0.262n+4`, i.e. is impossible past `n ≈ 60`, and the
  first 40 generations are verified. **Any fatality must be a MULTI-RUN conspiracy:** ≥ `(a_m−1)/(0.262n+4)`
  separate maximal-depth 3-adic returns interleaved with ≤ that many +4/+6 recoveries — each return an
  exponentially-deep congruence `G ≡ −14 (mod 3^L)` event.
- The failure condition in exact form: fatality ⟺ the weighted prefix sums fail, and the drains decompose into runs
  with `Σ_runs v₃(G_{n_i}+14) ≥ 4·#{ρ=2} + 6·#{ρ=0} + a₀ − 1` — **the open content is exactly the frequency of deep
  3-adic returns**, no longer their depth.

## 3. The mirror unification `[structural, verified]`
Set `W_n = G_n + 14`. Then `3W_{n+1} = 4W_n + (e−14)` with `e−14 ∈ {0 (ρ=1), −13 (ρ=2), −5 (ρ=0)}`:
**ρ=1 steps are EXACTLY ×(4/3) on W**, and the ledger-relevant quantity is the 3-adic depth `v₃(W_n)` of an affine
×4/3 orbit — the precise mirror of Antihydra's `v₂(c_n−1)` countdown under ×3/2 (there: 2-adic depth of a ×3/2
orbit, constant budget; here: 3-adic depth of a ×4/3 orbit, **linearly-growing budget** `a_n`). The two flagship
open cores are the SAME object with (p,q) swapped and o4 enjoying a growing budget — confirming the (K)-species
conservation at the deepest coordinate level, and making o4 formally the easiest instance.

## 4. What a proof now needs (the sharpened spec)
The needed tool for o4 is EXACTLY the NEW_MATH_PROGRAM object in its cleanest coordinates: a **quenched bound on the
FREQUENCY of deep p-adic returns** (`v₃(W_n) ≥ ℓ` has frequency ≲ 3^{−ℓ}-ish, effectively, for the specific orbit) —
depth is now unconditionally controlled (§2), frequency is the whole残り. Any effective return-frequency bound with
budget-growth awareness decides o4; the same tool at (2,3) with constant budget is Antihydra/(K). The margin ladder
(o4 ≫ o3 > o15 > Antihydra) is thus a genuine STAGING for building the missing mathematics.

## Verdict
**(b) — a new proven structural theorem + the sharpest quantification yet of o4's open core.** The ledger conjecture
is not weakened, but its failure modes are now exactly classified (multi-run conspiracies only), and o4/Antihydra are
unified as mirror instances of one p-adic return-frequency problem. o4 `[OPEN]`. **No machine decided. No label
upgraded.**

## Reproduce
- inline verification (exhaustive G≤2×10⁵, 0 mismatches; real orbit 60 gens; three residues).
- Basis: `O4_LEDGER_ANALYSIS_2026-07-06.md` (bijection, ruin), `O4_TEMPLATE_CLOSURE_2026-07-06.md`,
  `NONATOMIC_FIXEDPOINT.md`/`EXCURSION_SYNTHESIS.md` (the Antihydra countdown mirror), `NEW_MATH_PROGRAM.md`.
