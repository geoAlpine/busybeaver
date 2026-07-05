# New thread — Fork A found: o4 is the first plausibly-DECIDABLE cryptid; o15/o18 flavors finalized (2026-07-05)

*Searching for Fork A (a finite structural invariant that decides a B2 machine). **Found: o4.** Its tape language and
finite control are empirically **closed** (50M steps, ~20k milestones, zero violations, no new control symbols, halt
gate never fires), so a **finite invariant excludes the halt** — the Fork-A signature, in sharp contrast to the
`(K)`-hard Fork-B1 machines (Space Needle) whose orbit is normal. o4's decision **reduces to a bounded, finite-state
closure proof** — genuinely tractable, unlike `(K)`. Also: **o15 = B1** (Mahler-8/3 kernel), **o18 = B2** (alignment),
finalizing the `×8/3` split. SOUNDNESS: `[OBSERVED]` closure to 50M (not yet a proof); halting `[OPEN]`; no machine
decided.*

## o4 is Fork A — the decidability signature `[OBSERVED, 50M steps]`
o4's transducer (`o4_transducer.py`) over 50M steps / 19901 milestones:
| check | result | meaning |
|---|---|---|
| tape-language violations | **0** | unit 1-blocks, `0`-gaps `∈{1,2}`, `≤1` big gap — a **closed regular** tape language |
| new boundary/reflection/gate symbols | **NONE** | the **finite control is closed** (fixed `11/4/5` symbol sets) |
| multi-big-gap events | **0** | never two big gaps (single odometer defect) |
| `B` reads `1` with right neighbour `1` | **0** / 12.5M `B`-reads | the **`11`-existence halt gate never fires** |
Plus: the base-4/3 orbit's digits are `∈{1,2}` (structurally restricted, `O4_HALT_FLAVOR`). **Together this is the
Fork-A signature: a finite structural invariant (closed tape language + closed finite control) that excludes the
halt.** Contrast Space Needle (Fork B1): its `×5/2` orbit visits **all** residues mod `2^k` — no invariant can exist,
so it is `(K)`-hard. **o4 is different in kind: an invariant demonstrably exists (to 50M).**

## The decision reduces to a BOUNDED proof `[the tractable obligation]`
To turn this into a `[PROVEN]` decision (o4 does not halt), it suffices to prove **two bounded, finite-state claims**:
1. **Finite-control closure is inductive.** The transition-symbol sets (`CROSS_OK`/`REFL_OK`/`GATE_OK`, sizes `11/4/5`)
   are closed under one TM step over all reachable local patterns — a **finite case check** (the big-gap `G` grows, but
   the *local* dynamics depend only on a **bounded window** around the head, so the state space is finite).
2. **`B` never reads a transient len-2 block.** The only `1`-blocks of length `≥2` are transient, mid-carry, and
   off-milestone; proving `B`'s read-position never coincides with one is a **bounded relative-timing** argument.
Both are **finite/inductive invariance claims** — the kind a decider *can* discharge (VASS/Presburger-style or an
explicit closed automaton) — **fundamentally unlike `(K)`**, which is an infinite equidistribution. **o4 is the first
BB(6) cryptid reduced to a bounded, plausibly-dischargeable decision obligation.**

## o15/o18 finalized `[lit-note]`
- **o15** (`1RB---_..._1RC1RA`, halt `A` reads `1`): "**parity-irregular Mahler-8/3**" that **carries an equidistribution
  kernel** (`CRYPTID_O17_O15`, contrasted with kernel-less o17). Non-halt needs that kernel ⟹ **B1 (density)**.
- **o18** (`×8/3`): halt `=` **frontier alignment**, handled by window/existence barriers (`O17_REG_BARRIER`) ⟹ **B2
  (reachability/existence)**.
- So the `×8/3` pair **splits**: **o15 = B1, o18 = B2** — another instance of object ⟂ wall (same ratio, different wall).

## Verdict
**(b) — genuine progress: the first Fork-A (decidable-candidate) cryptid, and the `×8/3` split finalized.** o4's halt is
excluded by a finite structural invariant (closed tape language + finite control, 50M-verified; digits `∈{1,2}`), so its
decision reduces to two **bounded** closure/timing invariants — tractable, not `(K)`. This separates o4 (decidable-
candidate, Fork A) sharply from Space Needle (Fork B1, `(K)`-hard, `μ=5/2`). o15 = B1, o18 = B2. **A rigorous o4 decision
is now a concrete finite target** (discharge the two invariants). **Halting `[OPEN]` (closure observed, not yet proven).
No machine decided. No label upgraded.**

## Reproduce / basis
- `o4_transducer.py` `run(50_000_000)`: `lang=0`, `newX/newR/newG=NONE`, `multibig=0`, `b_r1_right1=0/12.5M`. Basis:
  `O4_HALT_FLAVOR_2026-07-05`, `B2_DECISION_FORK_2026-07-05`, `CRYPTID_O17_O15.md`/`CRYPTID_KERNEL.md` (o15/o17),
  `O17_REG_BARRIER.md` (o18), `CATALOGUE_O13_SN.md` (Space Needle Fork-B1).
