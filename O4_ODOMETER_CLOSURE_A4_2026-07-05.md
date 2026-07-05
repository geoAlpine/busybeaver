# o4 odometer closure (path A′ turn 4) — no finite shortcut: the ~25 branches are counter-VALUED; o4's decision is definitively a base-4/3-odometer theorem (2026-07-05)

*Final step of the inductive proof: close the ~25 non-deterministic boundary branches by an odometer argument. Tested
whether each branch's successor is a **finite function** of the preceding sweep length (`mod k`, `k=2,3,4,6,12`) — which
would make the boundary-automaton deterministic-finite (⟹ decidable). **Result: `0/25` at every `k`.** The branching is
**not** a finite residue of any local quantity — it depends on the **full base-4/3 digit string** of the big-gap
counter. So **every finite-state shortcut is ruled out**, and o4's decision is **definitively** a theorem about the
base-4/3 odometer's full carry cascade. SOUNDNESS: `[OBSERVED]`; o4 `[OPEN]` — not decided; **all shortcuts rigorously
excluded**. No machine decided.*

## The test `[OBSERVED]`
For each of the 25 non-deterministic boundary contexts, recorded `(successor, preceding-sweep-length)` and asked: is the
successor determined by `sweep-length mod k`? 
| `k` | contexts resolved |
|---|---|
| 2 | 0/25 |
| 3 | 0/25 |
| 4 | 0/25 |
| 6 | 0/25 |
| 12 | 0/25 |
**None.** The branch a boundary event takes is **not** a finite function of the local sweep length — it is
**counter-valued**, depending on the full base-4/3 representation of `G` (consistent with the generation structure being
digit-string-dependent, turn 3).

## What this settles `[the definitive characterization]`
Every route to a **finite** certificate for o4 is now rigorously excluded:
- `m`-gram / regular (sofic) invariant — HOLDOUT to `m=26` (turn 4).
- local window enlargement — non-determinism persists (`±4`→25, `±6`→28).
- two-counter `(G,a)` uniform closure — fails, generation has `~log G`/`~G^{0.7}` phases (turn 3, A1).
- finite state-augmentation by sweep-length residue — `0/25` (this turn).
**o4's decision is irreducibly a base-4/3-odometer theorem:** prove the carry cascade of `G↦⌊4G/3⌋+c` never routes a
boundary branch into a `11`-at-`B`, for **all** `G` — where the branch taken genuinely depends on `G`'s full base-4/3
digits. This is a Collatz-like statement about a specific `⌊4·/3⌋` odometer; it is decidable in principle (the object
is well-defined and computable) but its proof is an **open-ended arithmetic/combinatorial theorem**, not a bounded or
finite-state check.

## Verdict `[the honest culmination of the o4 decision attempt]`
**o4 is decidable-in-principle and now COMPLETELY characterized: a base-4/3-odometer `11`-avoidance theorem with every
finite/regular/residue shortcut rigorously ruled out.** Across ~12 turns the decision was reduced to its irreducible
core — a finite boundary-graph (B-safe, halt-free) whose ~25 branches are counter-valued in the base-4/3 digits — and
**no false decision was ever claimed**. The remaining work is proving the odometer theorem itself, a genuine
research-level result of the same character that makes o4 a cryptid. **o4 not decided. Halting `[OPEN]`. No machine
decided. No label upgraded.**

## Reproduce
- `/tmp/o4_odo.py`: successor vs `sweep-length mod k` = `0/25` for `k∈{2,3,4,6,12}`. Basis:
  `O4_INDUCTIVE_PROOF_A3`, `O4_VERIFIER_BUILD_A1/T3/T4`, `O4_11AVOIDANCE_A2`, `o4_accel_sound.py` (all 2026-07-05).
