# o4 11-avoidance — inductive proof attempt (path A′ turn 3): reduced to a finite boundary-graph, but its branching is counter-dependent (2026-07-05)

*Attempting the inductive proof of the local invariant ("B never created on the left `1` of a `11`"). Structure: a
two-level induction (generations × sweeps), with the accelerated machine's **boundary events** (non-sweep steps) as the
finite core. **Result: the boundary-event graph is FINITE (121 contexts at ±4), halt-free, and every `B`-reads-`1`
boundary has right-neighbour `0` (safe) — a genuine proof skeleton — BUT it is NON-DETERMINISTIC (~25–28 contexts with
multiple successors), and a larger window does not fix it (`±6` → 219 contexts, still 28 non-det).** So the branching
is **counter-dependent** (non-local, the base-4/3 big gap), and a sound proof still needs the odometer reasoning — the
irreducible core. SOUNDNESS: `[OBSERVED]`; o4 `[OPEN]` — not decided. No machine decided.*

## The proof skeleton `[OBSERVED, strong]`
Two-level induction: (outer) generations start/end at milestones `0^G(10)^{a-1}1001` (no `11`); (inner) within a
generation, **sweeps** (`B1F0` read-only over `1010`; `D1E0` invert, `1010→0101`) **preserve alternation** and `B` reads
only within alternating regions. The head traverses the big gap **as a sweep** (uniform, accelerated), so all non-sweep
("boundary") events are **turn-arounds at region edges**. Measured (accelerated machine, 20M steps):
- **Boundary-event contexts (state, ±4 window): 121** — finite and small; **0 halts**; **4** `B`-reads-`1` boundaries,
  **all with right-neighbour `0`** (safe); **0 escaping transitions** (closed over observed).
This is the accelerated macro-machine at the correct abstraction (sweeps collapsed) — **finite where the raw `m`-gram
was not** (it accelerates the sweeps the sofic language could not).

## The remaining gap — counter-dependent branching `[OBSERVED, the honest core]`
The boundary graph is **non-deterministic: ~25 contexts (±4) / 28 (±6) have multiple successors**, and enlarging the
window does **not** remove it (`±4`→121 ctx/25 nd; `±6`→219 ctx/28 nd). So a boundary event's successor depends on
**non-local** information — the **base-4/3 big-gap length** (a counter). A sound proof must therefore verify that, for
**every** counter value, each non-deterministic branch lands in the finite safe set — i.e. it must reason about the
**base-4/3 odometer's effect on the branching**. This is the same irreducible **unbounded-computation** core (turns
4/A1): finite structure, counter-dependent transitions.

## Where this leaves the proof `[honest]`
The 11-avoidance theorem is reduced to: **a finite boundary-graph (121 contexts, B-safe, halt-free) whose ~25
non-deterministic branches must be shown safe for all base-4/3 counter values.** This is a **bounded case analysis over
a finite graph, closed by an odometer argument** — genuinely more tractable than the raw machine, but the odometer
argument (proving the ~25 branches safe across all `G`) is the substantial remaining step, of a piece with proving a
Collatz-like map's behavior. Not completed; **o4 not decided**.

## Verdict
**(b/c) — the inductive proof reduced to a finite boundary-graph + a bounded odometer-closure argument.** The
accelerated boundary-machine is finite (121), halt-free, and `B`-safe on all observed branches — a real skeleton — but
its ~25 non-deterministic branches are **counter-dependent**, so closing the proof needs the base-4/3 odometer
reasoning (the irreducible core). **o4 is not decided**, held across ~11 turns without a false decision. **Halting
`[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `/tmp/o4_proof.py` (80–121 boundary ctxs, 0 halt, B-reads-1 all right-0), `/tmp/o4_bgraph.py` (±4: 121 ctx/25 nondet;
  ±6: 219/28; 0 escape). Basis: `O4_11AVOIDANCE_A2_2026-07-05`, `O4_VERIFIER_BUILD_A1/T4_2026-07-05`, `o4_accel_sound.py`.
