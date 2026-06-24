# Completing everything except the world-open kernel (TIER 1–3, 2026-06-24)

Per "do everything except TIER 0", this records the rigorous closure of TIER 1 (rigorize the conditional
theorem) and TIER 2 (fold all cryptids), and an honest scoping of TIER 3 (full holdout set).

## TIER 1 — the conditional theorem, now RIGOROUS (exact arithmetic) ✅
See `UNIFIED_CONDITIONAL_THEOREM.md` "RIGOROUS upgrade". Everything a finite computation certifies is
exact-arithmetic proved (no floating point):
- **Model exactness** — `M(x) mod p^k` depends only on `x mod p^{k+1}` (low digits + one incoming digit).
- **Total contraction** — Dobrushin `δ(P^k)=0` exactly (the chain forgets its start in `k` steps; stronger
  than a spectral gap).
- **Bijection** — the `k`-step map (incoming `k`-digits → state mod `p^k`) is a bijection, so the
  contraction→equidistribution transfer is rigorous.
- ⇒ The theorem is rigorous *except for the single hypothesis* (TIER 0): incoming digit ⊥ low state.

## TIER 2 — all cryptids folded ✅ (with one honest correction)
- **`2^a/3^b` family — rigorously unified.** The exact core (model-exact + `δ(P^k)=0` + bijection) holds
  identically for `μ ∈ {3/2, 4/3, 8/3}` = **Antihydra, o5, o7, o8, o10, o15, o18** (`tier2_sweep.py`). Both
  monsters and all family members are covered by the one rigorous conditional theorem.
- **`o17` (odometer) — NOT decidable by the simple route [CORRECTION].** The 2026-06-22 note conjectured
  o17 non-halts because "a `00` gap never forms" (halt ⟺ `00` read by D). **Direct test (`o17_verify.py`,
  20M steps): a `00` gap DOES form** (max 0-separator reaches 2) while the machine does not halt — so the
  transient `00`s do not (yet) trigger the halt, and the clean "no `00`" invariant is **false**. o17 remains
  a genuine holdout; its decision needs a finer (carry-aware) certificate that no current sound decider
  produces. (Honest retraction of the optimistic "live decision target" framing — soundness discipline.)
- Settled-block invariant `≡2 (mod 3)` held (0 violations / ~9000 sampled blocks), but it is a counting-DFA
  property the m-gram FAR cannot certify; and it alone does not preclude the transient `00`.

## TIER 3 — full holdout set: honest scope
- **Community frontier:** mxdys's list has **1104 holdouts** (up to equivalence, April 2026); BB(5) is solved,
  BB(6) open and provably Hard (bbchallenge).
- **What we established:** all cryptids we reverse-engineered reduce to the unified diagonal-digit kernel,
  and the `2^a/3^b` families share one rigorous conditional theorem. The cluster set is **{Mahler-3/2,
  Erdős-ternary (4/3,8/3), base-3 odometer}**.
- **What remains (genuinely large, mostly mechanical + partly TIER-0-bound):** reducing **all 1104** machines
  individually to the kernel (we worked a representative sample); confirming the cluster list is exhaustive
  over the full set; and ultimately deciding every holdout (needs TIER 0 for the cryptid cores). This is a
  community-scale cataloguing effort, not a single-session task; no shortcut was found that collapses it.

## Net state (everything except TIER 0)
- **DONE rigorously:** the unified conditional theorem (proven core, exact arithmetic) covering both monsters
  + the entire `2^a/3^b` family.
- **DONE honestly:** o17 retraction (no clean decision); cluster map; world placement.
- **REMAINS:** TIER 0 (the single digit-independence hypothesis = Mahler-3/2 / Erdős-ternary, world-open) and
  the mechanical-but-large TIER 3 cataloguing of all 1104 holdouts. 0 machine decisions claimed; 0 false
  proofs; over-claims retracted (now including the o17 "decision target").
