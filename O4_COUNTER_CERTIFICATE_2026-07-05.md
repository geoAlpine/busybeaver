# Building o4's counter-certificate — the explicit 2-counter invariant, verified closed; decision reduced to a bounded symbolic check (2026-07-05)

*Constructing the custom counter-certificate to decide o4. **Major progress: the invariant is now EXPLICIT** — a
regular language parameterized by **two counters** `(G, a)` — verified closed over 10 generations with the base-4/3
odometer exact and the halt never firing. This reduces o4's decision from "an invariant exists" (Fork-A) to a
**bounded symbolic one-generation verification**. SOUNDNESS: the invariant form and odometer are `[OBSERVED, verified
10 generations / 50M steps]`; the full "for all `(G,a)`" symbolic closure is **not yet executed**, so **o4 is NOT
claimed decided** — halting `[OPEN]`. No machine decided.*

## The explicit invariant `[OBSERVED, verified all generations G=7..206]`
At every generation-boundary milestone, the tape is **exactly**:
> **`0^G ( 1 0 )^a 1 0 0 1`** — a big gap of length `G`, then `a` copies of (unit `1`-block + unit `0`-gap), then a
> unit block, a length-2 gap, and a final unit block.
Verified: **all `1`-blocks are unit** (length 1), **all `0`-gaps are unit except the big gap `G` and one gap-2**, across
generations `G = 7,14,19,30,43,62,83,111,151,206`. The two counters evolve by:
- **`G ↦ ⌊4G/3⌋ + c(G mod 3)`**, `c={0→3,1→5,2→1}` — the base-4/3 odometer, **exact every generation** (10/10).
- **`a`** (block count) grows (the filler lengthens).
So the reachable set is the **regular + 2-counter** family `{ 0^G (10)^a 1001 : G,a }` — an explicit inductive-invariant
**skeleton**, not merely "an invariant exists."

## Why this is the right certificate `[structure]`
- **The filler `(10)^a` is finite-state to cross** — away from the big gap, the head-local abstraction is finite (the
  268 stable macro-states, `O4_CLOSURE_PROOF_ATTEMPT`); crossing `(10)^a` is a **uniform macro-step independent of
  `a`**. So `a` is a free counter (just makes the sweep longer), contributing no new behavior.
- **The only non-regular interaction is the big gap** — the cascade that reads `0^G` and rewrites it, producing the
  next `0^{G'}` with `G' = ⌊4G/3⌋+c`. This cascade is **local given `G mod 3`** (which selects `c`), so its
  tape-transformation is one of **finitely many** (indexed by `G mod 3`), plus a `G`-length-uniform traversal.
- **Halt-freeness** (`B` never reads `11`): the transient `[2]` blocks arise only **inside the cascade**; since the
  milestone form has **only unit blocks**, and `B`'s sweeps occur over the unit-block filler, `B` reads `11` **iff**
  its sweep coincides with a cascade `[2]` — a **phase** question resolved (empirically 0/12.5M) by the cascade being
  confined to the big-gap region that `B` does not sweep as a reader.

## The remaining obligation (bounded) `[honest]`
To **complete** the decision, one must symbolically verify **one generation**: starting from `0^G (10)^a 1001` at a
milestone, simulate with `0^G` handled as a symbolic counter and `(10)^a` as a uniform macro-step, and check the tape
returns to `0^{G'} (10)^{a'} 1001` with `G'=⌊4G/3⌋+c(G mod3)` **and** that `B` reads no `11` throughout — for **each
`G mod 3` class** and general `a`. Because the filler-crossing is uniform (finite-state) and the cascade is finite per
residue class, this is a **finite symbolic check** (a bounded macro-machine verification) — decidable, and the concrete
program to write. It is **not** `(K)`: no equidistribution, no infinite frequency — just a base-4/3 carry-cascade
closure, which the AFS rational-base numeration theory suggests is a **regular-language-preservation** fact.

## Verdict
**(b) — substantial progress: o4's invariant made EXPLICIT (2-counter regular family), verified closed with exact
odometer and halt-free over 10 generations / 50M steps.** The decision is reduced to a **bounded symbolic one-generation
verification** (uniform filler-crossing + finite per-residue cascade + phase-freeness). **o4 is NOT claimed decided**
(the symbolic closure is not yet executed) — but it is now the BB(6) cryptid **closest to a rigorous decision**, with an
explicit invariant and a finite remaining obligation, categorically unlike the `(K)`-hard machines. **Halting `[OPEN]`.
No machine decided. No label upgraded.**

## Reproduce
- `/tmp/o4_genrule.py`: milestone form `0^G (10)^a 1001` uniform, odometer `G'=⌊4G/3⌋+c` exact 10/10; `/tmp/o4_crossing.py`
  (A/B/C/E write 1 on 0, D/F preserve — cascade not uniform crossing). Basis: `O4_CLOSURE_PROOF_ATTEMPT_2026-07-05`,
  `o4_transducer.py`, `FORK_A_O4_DECIDABLE_CANDIDATE_2026-07-05`.
