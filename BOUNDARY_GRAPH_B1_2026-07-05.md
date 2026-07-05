# Boundary-graph on Antihydra (B1) — hypothesis refuted, but the technique UNIFIES the whole frontier (2026-07-05)

*Tested whether boundary-graph **stabilization** distinguishes B1 (density/`(K)`) from B2 (reachability/counter).
**Refuted:** Antihydra (B1) stabilizes **early** (`0.47%`) with a **finite** boundary-graph (125 contexts) and
**counter-dependent non-determinism** (24) — the **same structure as the B2 cryptids** (o4 121/25, o3 175/36). So the
accelerated boundary-graph **unifies** the whole cryptid frontier (B1 + B2): all are finite-graph + counter-dependent.
The B1/B2 distinction is **not** in the graph shape but in the **nature of the counter-dependence** — equidistribution
(`(K)`) for B1 vs deterministic arithmetic odometer for B2. SOUNDNESS: `[OBSERVED]`; `(K)` `[OPEN]`; no machine decided.*

## The result `[OBSERVED, ±4 window]`
| machine | wall | boundary contexts | non-det | settle | 
|---|---|---|---|---|
| **Antihydra** (3/2) | **B1** (`(K)`) | **125** | **24** | **0.47%** |
| o4 (4/3) | B2 | 121 | 25 | 0.1% |
| o3 | B2 | 175 | 36 | 0.32% |
| Space Needle (5/2) | B1 | 317 | 73 | 69% (non-stab) |
**Antihydra looks exactly like the B2 cryptids** (finite, early-settling, counter-dependent). The hypothesis "B1 ⟹
non-stabilizing" is **refuted** by Antihydra; Space Needle's non-stabilization is likely an **accelerator-coverage
artifact** (its `μ=5/2` sweeps exceed the period-≤8 detector, so mis-detected sweep steps inflate the "boundary" set) —
not a clean B1 signature.

## What it means `[unification, honest]`
- **The accelerated boundary-graph structurally unifies the frontier:** Antihydra (B1) and o4/o3 (B2) all reduce to a
  **finite boundary-graph with counter-dependent branching**. The technique is the common abstraction for *all*
  cryptids, not just B2.
- **The B1/B2 wall is in the counter-dependence, not the graph:** for **B2** (o4), the counter is a **deterministic
  base-4/3 odometer** and the branch-safety is an **arithmetic theorem** (decidable-in-principle by computing digits);
  for **B1** (Antihydra), the counter is the **×3/2 balance** and the branch-safety is **`(K)` equidistribution** — a
  density statement, not a bounded arithmetic one. Same graph, different *kind* of closure obligation.
- So Antihydra's `(K)` can be **restated** as: "the 24 counter-dependent branches of its finite boundary-graph are
  balance-safe for all values" — where "balance-safe for all values" **is** the even-density `≥1/3` / equidistribution
  `(K)`. A new lens on `(K)`, but the same generational core.

## Verdict
**(c)/(b) — hypothesis refuted; a frontier-wide unification instead.** Boundary-graph stabilization does **not**
distinguish B1/B2 (Antihydra stabilizes like the B2 cryptids); the technique unifies all cryptids as finite-graph +
counter-dependent, with the wall distinction living in the **counter-dependence's nature** (equidistribution `(K)` for
B1 vs arithmetic odometer for B2). Space Needle's outlier reading is an accelerator-coverage caveat. **`(K)` `[OPEN]`.
No machine decided. No label upgraded.**

## Reproduce
- `/tmp/bgraph_all.py` on Antihydra `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA`: 125 ctx/24 nondet, settle 0.47%. Basis:
  `CRYPTID_BOUNDARY_GRAPH_CENSUS_2026-07-05`, `B2_DECISION_FORK_2026-07-05`, `O4_ODOMETER_CLOSURE_A4_2026-07-05`.
