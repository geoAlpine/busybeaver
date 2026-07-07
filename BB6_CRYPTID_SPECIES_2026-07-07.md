# The cryptid species map — gate / structure / protection: the B1/B2 dichotomy refined into a five-shape classification (2026-07-07)

> **CORRECTION (2026-07-07, `O15_O18_IDENTITY_2026-07-07.md`): o18 is o15's machine table mirrored and re-rooted
> (verified isomorphism A→D,B→E,C→C,D→F,E→B,F→A) — one table, two seeds/orbits, analyzed here in two coordinate
> systems.** The machine count below should be read accordingly (five distinct tables, six analyzed orbits). Also:
> the o18 rows' "no fatal set found" is SUPERSEDED — via the identity, o15's proven fatal family and a
> community Lean-verified halting congruence class (mod 3¹⁰⁸, @-d) apply to the same table; community status for
> these orbits is "probviously halting". See the identity note for the integrated picture.

*Synthesis of the 2026-07-06/07 template-closure campaign (o4 → o3 → o17 → o18 → o15). The old B1/B2 wall dichotomy
(`BOUNDARY_GRAPH_B1`: "equidistribution vs arithmetic odometer") is superseded: every analyzed cryptid decomposes as
**GATE + STRUCTURE + PROTECTION**, the first two now largely PROVEN per machine, and the whole open content living in
the protection — an orbit-specific quenched statement in five different coordinates. No machine decided.*

## The decomposition (uniform across the family)
- **GATE `[PROVEN per machine, from the transition table]`** — a local halt condition with a forced predecessor
  chain, and a halt-relevant window census that SATURATES small and safe: o4 (23 @ r=5), o3 (6), o17 (11), o18 (**1**
  — sharpest), o15 (2). Universal: the gate half is never the obstruction.
- **STRUCTURE** — what the generation dynamics is:
  | machine | structure | status |
  |---|---|---|
  | o4 | rigid template prefix·body^r·suffix (period-2 sweeps) | `[PROVEN, certified + red-teamed]` |
  | o3 | rigid template (cycle certificates p=10/20/6) | `[PROVEN on grid]` |
  | o15 | rigid template (5 shape classes, queue-stable) | `[PROVEN on grid]` |
  | o18 | rigid at every closed level; the whole tower = **pushdown 3-adic odometer** (one finite table on `D(m,t,e)`, refined 2026-07-07) | levels + table `[PROVEN on grid]`; multi-defect regime `[OPEN]` |
  | o17 | **no template** — generation shapes unbounded (state = whole digit string, √step growth) | `[OBSERVED refutation]` (label corrected 2026-07-07: the class-growth is measured, not proven unbounded) |
  | Antihydra | boundary-graph finite but counter-dependent; no template extracted | (2026-07-05) |
- **PROTECTION (= the open core)** — why the gate never fires, in five shapes:
  | machine | protection shape | fatal set | margin |
  |---|---|---|---|
  | o4 | **residue-ledger** `a′=a+δ(G mod 3)` | `[PROVEN nonempty]` Z(41,3,0) halts | drift +3/gen, ruin η^a, η≈0.335 |
  | o3 | **residue-ledger** — roles swapped vs o4: `a` is the base-4/3 odometer, `k` the ledger, `Δk=δ(a mod 3)` exactly (V3-final report; refutes `O3_TRANSDUCER` §4's "history-dependent" claim) | `[PROVEN nonempty]` + **predicted-then-confirmed** | drift +0.248/gen, drains ≤10 |
  | o15 | **string-ledger** — carry cascade never stacks leading `[2,2]` at a split (cylinder avoidance in the Mahler-8/3 digit string) | `[PROVEN nonempty]` + **predicted-then-confirmed** | no leading 2 in 11 gens (exposure record) |
  | Antihydra | **density** — even-density ≥ 1/3 = `(K)` | (halt = density failure) | zero margin (critical) |
  | o17 | **tower-sparse regenerative-wall carry-timing** (formulated 2026-07-07, `O17_GATE_LAW`): gate-to-gate map `F(μ,d⃗)` exact & validated; `t≈3.97n²`, **`log n_{k+1} ≈ a·n_k`** (iterated-exponential sparsity, next blank gate ~10⁶⁰); protection SELF-REINFORCING (each survival erects a wall delaying the next exposure exponentially) yet distance-1 in value; branch determinant has rigid islands (m≤2) but m≥3 provably reduces to F itself | fatality distance ≤1 at every gate | tower-sparse timing |
  | o18 | **pushdown 3-adic odometer** (refined 2026-07-07, `O18_DEPTH_UNIFORM`): the whole tower = ONE finite
  transition table on `D(m,t,e)` states, grid-proven; prior "unclosed mod-81 branches" REFUTED — both LAND (12/12
  predict-and-confirm to 3.44×10⁹ steps); push law `m′−1=(8/3)(m−1)` (the fixed-point trick again — o18 joins the
  ×8/3 family); depth = v₃(m−1) DERIVED. Remaining: the multi-defect rewrite grammar (orbit exits the single-defect
  family at m≈10³⁵⁷⁷) — a finite explicit rewrite system away from a candidate decision | **none found** (0 halting configs) | n/a |

## The meta-facts
1. **Every protection is an orbit-specific quenched statement** — the `(K)`-species in five coordinates: one-sided
   prefix-sums (o4/o3), cylinder avoidance in a digit string (o15), Cesàro density (Antihydra), sparsity-in-time
   (o17), well-foundedness of a recursion (o18). Where tested, **seed-specificity is PROVEN** (o4's itinerary
   bijection: fatal patterns realized by full seed classes; no seed-uniform theorem exists).
2. **Fatal sets are REAL where they exist** — o4/o3/o15 have genuine halting standalone configs, twice found by
   **a-priori ledger prediction confirmed by simulation** (the method's predictive validation). o18's absence of any
   fatal set (negative search) makes its level-induction arguably the most decision-adjacent target in the family.
3. **The old dichotomy's fate:** B2 ("arithmetic") machines bottom out in ledgers (o4, o3) or towers (o18) — the
   "arithmetic vs density" wall MERGES at the ledger level for o4/o3 (same one-sided species as `(K)`, huge margin)
   but NOT uniformly (o17 is timing, o18 is induction). B1's density call survives at Antihydra and — sharpened to
   string-ledger/cylinder form — at o15.
4. **Margins order the family:** o4 (+3 drift) ≫ o3 (+0.248) > o15 (cylinder exposure) > o17 (timing) > Antihydra
   (zero margin). If an orbit-specific tool ever materializes, this is the predicted falling order; o18's
   level-induction may be attackable independently (no fatal set, closed laws at every examined level).

## Honest status
GATE+STRUCTURE ≈ closed by this campaign (with red-team + corrections logged: C-seam localization, o18 framework law,
o15 queue bookkeeping, per-a templates, pinning lemma). PROTECTION `[OPEN]` in all six machines — that is the
generational wall in its now-fully-mapped form. Tools banked: validated macro machines (o4, o3), certified
trace-template method (red-teamed), ledger extraction + predict-and-confirm protocol. **No machine decided. No label
upgraded.**

## Sources
`O4_TEMPLATE_CLOSURE` + `O4_LEDGER_ANALYSIS` + `O4_SEAM_PARITY_LEMMA` + `O4_CSEAM_LOCALIZATION` +
`O4_WINDOW_SATURATION` (2026-07-06); `O3_TEMPLATE_PORT`, `O17_HALT_FLAVOR` (2026-07-06); `O18_TEMPLATE_PORT`,
`O15_TEMPLATE_PORT` (2026-07-07); `BOUNDARY_GRAPH_B1`, `B2_DECISION_FORK` (2026-07-05, superseded in part).
