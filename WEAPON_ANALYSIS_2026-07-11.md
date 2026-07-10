# Cross-campaign analysis → the carry-calculus weapon (2026-07-11)

*The thorough analysis of ALL campaign data (07-06 → 07-11, ~115 commits) and the weapon design it yields toward the
complete proof. This note records the analysis itself; the two builds it launched are `X2_CARRY_CALCULUS` and
`CARRY_DICHOTOMY`. Labels strict. No machine decided.*

## 1. The universal shape of every open core `[the cross-cutting fact]`

Placing every open core on the frontier side by side:

| machine | open core | local certificates | counterexamples |
|---|---|---|---|
| o4 (×4/3) | ledger `a≥1` at ρ=1 | **HALT-in-closure [PROVEN]** (`o4_closure_fixpoint`) | 0 |
| Antihydra band (×3/2) | even-density ≥ 1/3 | No-Structure [PROVEN] | 0 |
| o15/o18 (×8/3) | epoch-hit congruence avoided | counter-dependent branching [PROVEN] | 0 |
| **×2 machine** | **every odometer carry gap even** | **HALT-in-closure R≤8 [PROVEN]** (`x2c_closure`) | 0 (3·10⁸) |
| o7 / SN | never hit 2^k | congruence fills ℤ/m [PROVEN] | 0 |
| o17 | gate-phase safe | Nerode-unbounded [OBSERVED] | 0 |

**Every open core is a counter-dependent invariant of an odometer's carry/branch sequence; the HALT-in-closure
phenomenon reproduces universally; every invariant holds with zero counterexamples.** This is the structural reason
the community decider suite (FAR/CTL = regular/bounded certificates) leaves exactly these 1104: regular certificates
are provably insufficient for this class — reproduced now in two machines (o4, ×2) as theorems.

## 2. The overlooked distinction: counter-dependent ≠ (K)

The campaign has treated "counter-dependent" as synonymous with "hard." The data does not support that equation:

> A counter-dependent invariant is hard **only if the counter itself is an object whose distribution is open**.
> If the counter is a **fully-understood register** (increment, pure doubling, fixed affine on bounded state), the
> carry sequence is **explicit mathematics**, and the invariant becomes a provable theorem about that mathematics.

- **carry-OPAQUE**: o4's ρ-sequence IS the base-4/3 orbit's residue itinerary — by the itinerary bijection [PROVEN],
  the carry sequence is exactly the (K) object. Same for the whole NormalityPQ band. Genuinely Mahler-hard.
- **carry-TRANSPARENT (candidate)**: the ×2 machine's carry gaps come from its low-part `(10)*`-comb register. If that
  register follows an explicit update law (e.g. literal binary counting), the gap sequence is the **binary carry
  structure of counting** (ruler-sequence mathematics) — and "all gaps even" may follow from the cell-pitch alone
  (each register bit occupies 2 tape cells ⟹ any carry run gives an even gap).

**The gap in all prior ×2 attacks (routes A/B, parity-ordering): they INSTRUMENTED the carries as opaque observations;
none DERIVED the low-part update law.** That derivation is the untried move.

## 3. The weapon: odometer-faithfulness certificates + carry calculus

```
(i)   Prove the low-part's rigid encoding invariant by template induction   ← STRUCTURE (the campaign always wins here)
(ii)  Derive the register's update law (increment / fixed affine)
(iii) The carry sequence becomes an explicit mathematical sequence
(iv)  Prove the safety property as a theorem about that sequence            ← decides the machine
```

This is also a NEW DECIDER CLASS design: where FAR/CTL certify regular tape languages (provably insufficient here),
a faithfulness certificate proves the machine implements an explicit register, importing the register's mathematics
as the invariant. It is the formalization of what the 17 named machines received by hand — now aimed at DECISION.

## 4. Where it can win, honestly

- **×2 machine first** (`X2_CARRY_CALCULUS` build): if the low-part decodes to an explicit law and the pitch-2
  argument holds, the open core closes and the machine is DECIDED. Honest risk: the low-part may not be rigid, or the
  law may couple back to deep state ((K)-like after all) — prior ×2 optimism was refuted twice; no optimism here.
- **The transparent sublist of the frontier** (`CARRY_DICHOTOMY` build): classify all 17 named + the ×2 species (~7) +
  the 105 collapsed holdouts by opacity. The NormalityPQ band is opaque (itinerary bijection); the transparent set may
  be small — but it is the exact list of machines decidable in principle by this weapon.
- **What this does NOT touch**: the carry-opaque band = the true (K) wall, unchanged.

## 5. Verification state feeding this analysis
Extractor V2 (15/16 gate, 0 false labels); ×2 record (2 cross-validated reductions, ordering half proven, sweepEF
Lean-proven, eraser-misattribution corrected 7760aa5); completion frame (`Completion.lean`, NormalityPQ collapse);
the (K) record (~17 tool classes → δ₋₁₄ seam). All cited facts committed and main-loop re-verified.

**No machine decided. No label upgraded.**
