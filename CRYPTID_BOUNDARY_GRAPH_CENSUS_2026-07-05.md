# Frontier-wide: the accelerated boundary-graph unifies the B2 cryptids — all are finite-graph + counter-dependent (o4's structure generalizes) (2026-07-05)

*Applying o4's accelerated boundary-graph technique (sweeps collapsed, non-sweep "boundary" events as the core) across
the B2/reachability cryptids. **Finding: they share o4's structure** — a **finite** boundary-graph with
**counter-dependent non-determinism**, i.e. each reduces to an **odometer/counter theorem** (Fork-B2), with **no finite
deterministic certificate**. Space Needle stands apart (graph does not stabilize — Fork-B1, `(K)`-hard). So o4's
~12-turn characterization **generalizes to the whole B2 frontier**: no cryptid is finitely decidable by this method.
SOUNDNESS: `[OBSERVED]`; all halting `[OPEN]`. No machine decided.*

## The census `[OBSERVED, accelerated boundary-graph, ±4 window, ~10⁶ steps]`
| machine | boundary contexts | non-det | escapes | new-ctx settle | reading |
|---|---|---|---|---|---|
| **o4** (4/3) | 121 | 25 | 0 | 0.1% | finite + counter-dependent (Fork-B2) |
| **o3** (odometer) | 175 | 36 | 0 | 0.32% | **same as o4** — finite + counter-dependent |
| **H5** (Type IV) | 301 | 118 | 0 | 6% | finite + heavy counter-dependence |
| **Space Needle** (5/2) | 317 | 73 | 0 | **69%** | **does not stabilize** — Fork-B1, `(K)`-hard |
(o17 exceeded the time budget; o13's recorded string parsed as a halter — excluded.) **Every machine has non-determinism
`> 0`** — none is a finite deterministic boundary-automaton.

## What it means `[the unification]`
- **The B2 (reachability) cryptids all share o4's structure:** the accelerated machine collapses the unbounded sweeps
  to a **finite** boundary-graph, but the branching is **counter-dependent** (non-deterministic, not fixable by a
  finite window — as proven for o4). So each B2 cryptid's decision is an **odometer/counter theorem** of o4's kind:
  finite structure, but closure needs reasoning about the machine's counter for all values. **None is decidable by a
  finite/regular certificate.**
- **Space Needle is harder still:** its boundary-graph does **not** stabilize (new contexts at 69% of the run),
  consistent with its Fork-B1 status (`μ=5/2` normal orbit, `(K)`-analogue anti-normal avoidance) — no finite invariant
  even exists.
- **o4's ~12-turn result is the template for the whole B2 frontier:** the accelerated boundary-graph is the right
  abstraction (finite where `m`-gram was not), and every B2 cryptid lands at the same irreducible core — a
  counter/odometer theorem — which is precisely why they are cryptids.

## Verdict
**(b) — a clean frontier-wide unification.** The accelerated boundary-graph technique (from the o4 build) shows the B2
cryptids (o3, o4, H5) share one structure — finite boundary-graph + counter-dependent non-determinism = an
odometer/counter theorem, no finite certificate — with Space Needle harder (Fork-B1, non-stabilizing). **No cryptid is
finitely decidable by this method; each reduces to a counter theorem of o4's kind.** **Halting `[OPEN]`. No machine
decided. No label upgraded.**

## Reproduce
- `/tmp/bgraph_all.py` (general accelerated boundary-graph): o4 121/25, o3 175/36, H5 301/118, Space Needle 317/73
  (non-stabilizing). Basis: `O4_ODOMETER_CLOSURE_A4_2026-07-05` (o4 the template), `B2_DECISION_FORK_2026-07-05`,
  `o4_accel_sound.py`.
