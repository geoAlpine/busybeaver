# New thread — attacking B2 decidability: the decision fork, and Space Needle is (K)-hard (μ=5/2) (2026-07-05)

*Actually attacking the decidability of B2/reachability cryptids (`CRYPTID_2D_CLASSIFICATION`). Result: a clean
**decision fork** for B2 machines, o15/o18/o17 halt-flavors pinned (with one correction to the prior note), and a
concrete decision outcome for Space Needle — **it is on the anti-normal-avoidance fork = `(K)`-hard for `μ=5/2`, not
decidable.** No machine decided; the value is the precise hardness-classification. SOUNDNESS: `[OBSERVED]`/`[PROVEN
from lit-note]`; halting `[OPEN]`; no machine decided.*

## The B2 decision fork `[the structural result]`
For a B2 machine, non-halt `⟺` the value orbit **avoids the halt-set forever**. Three exclusive forks:
- **Fork A — decidable.** A **finite structural invariant** (window/DFA certificate) excludes the halt-set ⟹ provably
  non-halting. *(The `far_dfa`/`far_finder`/`far_cegar` tools search exactly this.)*
- **Fork B1 — fixed-cylinder anti-normal avoidance `= (K)`-analogue.** The halt-set is a **fixed 2-adic cylinder**;
  the orbit is **normal** (visits every cylinder), so avoiding it forever is an **anti-normal avoidance** = an
  equidistribution/`(K)`-type statement for that machine's multiplier. Equidistribution-hard, generational.
- **Fork B2 — carry-timing / moving target `=` generalized-Collatz.** The halt is a **carry-timing** event over a
  *moving* frontier (not a fixed cylinder), so even *automatic* equidistribution doesn't force a hit. Collatz-hard
  (`Π⁰₂`, Kurtz–Simon).

## Per-machine (this thread) `[OBSERVED / lit-note]`
- **Space Needle** (`μ=5/2`, `T(x)=⌊5x/2⌋`): the orbit **visits all residues mod `2^k`, `k≤6`** (empirically normal);
  halt `=` a fixed 2-adic carry/adjacency alignment at the `C→F` frontier. ⟹ **Fork B1**: non-halt `=` anti-normal
  avoidance of the halt-cylinder `= (K)`-analogue for `μ=5/2`. The `far_*` tools returned **HOLDOUT** (no finite
  invariant), consistent. **Decision outcome: not decidable by structural invariant; `(K)`-hard at ratio `5/2`.**
- **o17** (`1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`, halt `A`... actually `F` reads `0`): `CRYPTID_KERNEL`/`O17_O15`
  say o17's base object is a **`+1` carrying odometer — an isometry of `ℤ_p`, uniquely ergodic ⟹ equidistribution is
  AUTOMATIC**; the hardness is **only** the halt predicate `=` a **carry propagating past the MSB** = **carry-timing**.
  ⟹ **Fork B2** (moving target, Collatz-irregular). **Correction:** the prior 2D note called o17 "B1-leaning
  (bit-density `=(K)`)"; the kernel note is clearer — o17 has **no** equidistribution-kernel hardness, so it is **B2
  carry-timing**, not B1.
- **o15** (`1RB---_..._1RC1RA`, halt `A` reads `1`): "**parity-irregular Mahler-8/3**" that **does** carry an
  equidistribution kernel (contrasted with kernel-less o17). Leans **B1/density**. So the `×8/3` pair is **not
  uniform**: **o15 ≈ B1**, **o18 ≈ B2** (frontier-alignment existence, `O17_REG_BARRIER`).

## What this buys `[honest]`
- **No new machine decided** — Space Needle/o13/o14/o16 remain HOLDOUT; Space Needle is now *classified* as Fork-B1
  `(K)`-hard (`μ=5/2`), so it will **not** yield to invariant search — the tools' HOLDOUT is explained, not a gap.
- **A decidable cryptid, if one exists, is on Fork A** — a finite structural invariant. The current tools search
  Fork A up to `m≤8`/`k≤6`/120 CEGAR rounds and find none among the B2 holdouts, so any decidable one needs either a
  **larger window** or a **hand invariant** the tools miss. That is the concrete target for a future decision.
- **The B2 wall splits into two distinct hardnesses:** fixed-cylinder anti-normal avoidance (`(K)`-analogue: Space
  Needle `5/2`, o4 `4/3`) vs carry-timing (generalized-Collatz: o17, o3). Both `[OPEN]`, different in kind.

## Verdict
**(b)/(c) — B2 decidability attacked; a decision fork established, one machine classified `(K)`-hard, corrections
banked.** Space Needle is Fork-B1 (`μ=5/2` anti-normal avoidance), not decidable by invariant; o17 corrected to Fork-B2
(carry-timing, no kernel); o15 (B1) vs o18 (B2) split the `×8/3` pair. A decidable cryptid must be Fork-A, which the
current tools have not found among these holdouts. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce / basis
- `/opt/homebrew/bin/python3.13`: `T(x)=⌊5x/2⌋` from `x=3` visits all residues mod `2^k` (`k≤6`). Basis:
  `CATALOGUE_O13_SN.md` (Space Needle `μ=5/2`, halt), `CRYPTID_KERNEL.md`/`CRYPTID_O17_O15.md` (o17 no-kernel, o15
  Mahler-8/3), `O17_REG_BARRIER.md` (o18 alignment), `CRYPTID_2D_CLASSIFICATION_2026-07-05` (corrected here).
