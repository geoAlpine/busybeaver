# Building the base-4/3-odometer verifier (path A) — turn 1: data structure pinned, but one generation is an UNBOUNDED computation (2026-07-05)

*Path A, turn 1: pin o4's exact data structure and the generation-transformation shape to design the sound verifier.
**Data structure pinned:** milestones are `0^G (10)^{a-1} 1001` — a big-gap **unary counter `G`** (odometer
`G'=⌊4G/3⌋+c`) and a filler-count **counter `a`**, all `1`-blocks unit. **Decisive finding:** one generation is **NOT a
bounded-description rewrite** — its jump-phase count and step count **grow with `G`** (`~G^{0.7}` phases, `~G^{1.6}`
steps), so there is **no finite (G,a)-residue generation rule**. o4's decision requires reasoning about the base-4/3
odometer's **unbounded per-generation carry cascade** — a genuine formal task, not a bounded verifier. SOUNDNESS:
`[OBSERVED]`; o4 `[OPEN]` — **not decided**. No machine decided.*

## Data structure `[OBSERVED, verified 14 milestones]`
Every milestone tape is exactly **`0^G (10)^{a-1} 1001`**: a unary big gap `0^G`, then `a−1` copies of unit-block +
unit-gap, then `1 0 0 1` (a block, a gap-2, a block). All `1`-blocks are **unit**. Two counters: `G` (odometer
`⌊4G/3⌋+c(G mod3)`, exact) and `a` (grows). E.g. `(G,a) = (7,11),(14,10),(19,14),(30,13),…,(659,42)`.

## The decisive obstruction — the generation is unbounded `[OBSERVED]`
Per-generation cost, measured with the validated accelerator:
| `G` | jump-phases | concrete-steps |
|---|---|---|
| 13 | 6 | 165 |
| 42 | 14 | 611 |
| 110 | 41 | 3564 |
| 205 | 70 | 10425 |
| 366 | 122 | 31607 |
**Both grow with `G`** (phases `~G^{0.7}`, steps `~G^{1.6}`; `jp/log₂G` climbs `0.77→14.3`). So one generation is an
**unbounded computation** whose macro-structure depends on the **full value of `G`**, not on `(G mod 3, a mod k)`. There
is **no bounded generation-rewrite rule** — the two-counter uniform-closure model (and any finite residue refinement)
**cannot** work. This is the base-4/3 odometer's **carry cascade**, which is intrinsically a `~G`-length computation
per step.

## What a sound decision now requires `[honest scale]`
Deciding o4 is **not** running a verifier — it is **proving a theorem about an unbounded computation**: that the
base-4/3 odometer `G↦⌊4G/3⌋+c`, realized as the tape bouncer, **never** produces a `11` in `B`'s path, for all `G`.
This is a genuine formal-methods result about a Collatz-like map's carry cascade — the same *kind* of difficulty that
makes o4 a cryptid. Tractable in principle (the base-4/3 numeration is well-understood), but a **substantial
theorem/formalization**, not a bounded closure check. The honest tools in hand — the validated accelerator, the exact
data structure, the halt-free structural reduction (`B` reads `1` only in `1010…` sweeps) — are the **ingredients**;
assembling them into a proof of the odometer's `11`-avoidance is the real remaining work.

## Verdict
**(c) — path A turn 1: data structure pinned; o4's decision is an unbounded-computation theorem, not a bounded
verifier.** Milestones are `0^G(10)^{a-1}1001` (two counters); one generation grows with `G` (`~G^{0.7}` phases), so no
finite generation-rule exists. o4's rigorous decision requires **proving the base-4/3 odometer never emits `11`** — a
genuine formal theorem about an unbounded carry cascade, of a piece with why o4 is a cryptid. **o4 is not decided.**
**Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- milestone form `0^G(10)^{a-1}1001`; per-generation jump-phases/steps grow with `G` (`/opt/homebrew/bin/python3.13`,
  validated accelerator). Basis: `O4_VERIFIER_BUILD_T1..T4_2026-07-05`, `o4_accel_sound.py`, AFS base-4/3 numeration.
