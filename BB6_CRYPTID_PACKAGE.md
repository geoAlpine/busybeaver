# BB(6) cryptid package — the slow-width frontier, classified and gated (2026-07-04)

*External-shareable consolidation of the cryptid side of the BB(6) program (the counterpart of
`BB6_FRAMEWORK_PACKAGE.md`, which packages the (K)/Mahler kernel side). It collects: the machine-verified
**trichotomy** of the named cryptids, the **`[PROVEN from table]` halt gates** for all ten reverse-engineered
slow-width machines, the **Type-II structural-outlier** dissections (o17, o3), and the **1104-holdout frontier
census**. SOUNDNESS: every claim is `[PROVEN]`/`[OBSERVED]`/`[OPEN]`, machine-verified vs the raw TM;
**no machine is decided**; halting is `[OPEN]` for all. Interpreter `/opt/homebrew/bin/python3.13`.*

## 1. The one-paragraph statement

The BB(6) open frontier is **1104 undecided holdouts**, and they are **structurally homogeneous**: every one is
a **slow polynomial-growth counter/bouncer** (tape width `∼ step^a`, `a ≤ ~0.8`; none halts or grows
exponentially in width within cap). The ~15 named cryptids are **representatives** of this mass, and split by
*where their hardness lives* into a machine-verified **trichotomy** — each type's halting reduces, via a
`[PROVEN from the table]` halt gate, to one of **two walls**: single-orbit **(K)/Mahler-3/2 (Erdős)
equidistribution**, or **generalized-Collatz** reachability. No new tool crosses either wall.

## 2. The trichotomy (15 machines, `[OBSERVED]`, machine-verified)

| type | machines | mechanism | wall |
|---|---|---|---|
| **I — equidistribution-kernel Mahler** | Antihydra, o10, o15, o18, o2, o7, o11, o12, o13, o14, o16, **o4** (12) | a scalar/counter **value orbit `×3/2` (p=2), `×8/3` (p=3), or `×4/3` (p=3, o4)**, unary/odometer-encoded; halt = a parity/existence event on it | **(K) / Mahler-3/2 (Erdős)** |
| **II — kernel-less carry-cascade outlier** | **o17, o3** (2) | a **tame bounded/small-digit odometer, no value orbit**; all hardness is a Collatz-irregular halt predicate | **generalized-Collatz** carry-existence |
| **III — scalar generalized-Collatz** | Space Needle (1) | a single **scalar block** with an explicit 2-adic map; halt = orbit hits a sparse set | **generalized-Collatz** reachability |

**Key finding — `√t` is not a hardness discriminant.** Type-I (unary-Mahler), Type-II (odometer), and the sub-√t
Type-III all wear polynomial-growth geometry; even Antihydra (exponential Mahler *value*) has `√t` *width*. The
discriminator is the **content** (an exponential value orbit vs a bounded-digit carry cascade vs a scalar
Collatz orbit), not the growth rate.

## 3. The `[PROVEN from table]` halt gates (all 10 reverse-engineered machines)

Each halt state has a **unique predecessor transition**, so halting reads straight off the table as a single
bounded-context event; machine-verified never to fire from the blank tape (`cryptid_halt_gates_verify.py`,
`o3_transducer.py`):

| machine | type | HALT ⟺ | decides on |
|---|---|---|---|
| o17 | II | leading block (odometer MSB) ever **even** | own carry cascade (no-jump, core-hard) |
| o3 | II | state `E` reads a `00` | own carry cascade (marker `Δk∈{−1,+1,+2}`, core-hard) |
| o11 | I | state `B` reads a `00` | `⌊3D/2⌋+ε` odometer |
| o12 | I | state `E` reads a `00` (right) | `V'=⌊3V/2⌋+c` (`V=3a+2b`) |
| o13 | I | a `D,1→1LE` step lands on `0` (parity) | `a'=⌊3a/2⌋+c` |
| o14 | I | state `C` reads a `00` (left) | `A'=⌊3A/2⌋+6` |
| o16 | I | state `E` reads a `00` (right) | `S'=⌊3S/2⌋+c` |
| o2 | I | state `D` reads a `00` (right) | balance `b→0` at `a≡1 (mod4)` |
| o7 | I | state `C` reads a `00` (left) | left counter `a→1` |
| o4 | I (μ=4/3) | state `B` reads a `11` (right) — dual to `00` | `G'=⌊4G/3⌋+c(G mod3)` base-4/3 odometer |
| Space Needle | III | state `C` reads a `00` (left) | scalar `f(m)=m+3⌊m/2^{v+1}⌋+v` reaches `S` |

Type-I gates are **provably unreachable within the normal form** (the sweep always finds a nonempty/even block);
Type-II/III gates **are** reachable (the machine halts for constructed seeds) — the blank orbit just avoids them.

## 4. The Type-II outliers, dissected to o17's standard

- **o17** (`O17_CORE_TRANSDUCER.md`): finite-control base-3 digit-string transducer; unbounded digits + poly
  growth = one free-running LSB counter; `[PROVEN]` HALT ⟺ marker ever even; the no-jump residual (marker moves
  `≤1` base-3 step) shown **core-hard** (3 cascade-invariant angles fail; the change is history-dependent).
- **o3** (`O3_TRANSDUCER.md`): the **second** structural outlier — bounded `{0,1}` digits (tamer than o17), a
  free-running **length** counter (`W=2m+S+2`), `[PROVEN]` HALT ⟺ `E` reads a `00`; carry cascade = a migrating
  defect (`+3`/milestone) + a marker reservoir `k` with bounded irregular jumps `Δk∈{−1,+1,+2}`, **core-hard**.

## 5. The 1104-holdout frontier census (`BB6_FRONTIER_CENSUS_2026-07-04.md`)

Over **all 1104** holdouts (`holdout_census.py`, `holdout_census_axis2.py`):

- **Growth (axis 1):** `√t` bouncer **665** (60%), sub-`√t` **399** (36%), log-growth 33, intermediate 7;
  **0 halt, 0 exponential-width**.
- **Structure (axis 2):** bounded-digit (`B≤6`) **~522**, digit-string 540, unary-counter 22, mixed 20.
- **The bounded-digit (o3-class) form is ~half the frontier** — o3 is representative, not exceptional. A
  digit-sum-growth proxy splits the ~522 into **~183 o3-like (no value orbit)** and **~176 with a growing value
  (bounded-radix odometers)**, the rest slow/ambiguous — an estimate; a clean Type-I/II split needs per-machine
  reverse-engineering.
- **Sound deciders:** the repo's sound suite decides **0/15** sampled (all `HOLDOUT`), consistent with the prior
  `0/300` and community-holdout-by-construction.

## 6. Honest verdict + the two walls

**All fifteen named cryptids `[OPEN]`; the frontier is `0`-decidable by available sound deciders; no machine
decided.** Each reduces (via its `[PROVEN]` gate) to one of two walls:

- **(K) / Mahler-3/2 (Erdős)** — single-orbit equidistribution of `⌊(p/q)^n⌋`; unlocks all 12 Type-I at once;
  proven internal barriers (No-Structure, Coverage No-Go, decider-preemption, even-count floor); **generational**
  (`BB6_FRAMEWORK_PACKAGE.md`, `PROBLEM_LIST.md` P1/P1′).
- **generalized-Collatz** — reachability/parity over a carry cascade (Type II) or a scalar orbit (Type III); no
  bounded predictor (verified core-hard); a Collatz-class breakthrough per family.

If the trichotomy extends across the frontier's structural bands — plausible from the representatives, `[OPEN]`
for the ~1090 un-analyzed — **deciding BB(6) is gated by these same two walls uniformly**, not by 1104
independent problems. That reframing — a homogeneous frontier behind two named walls — is the cryptid side's
durable contribution. **No machine decided. No label upgraded. Halting `[OPEN]`.**

## Reproduce / index
- Halt gates: `cryptid_halt_gates_verify.py`, `o17_core_transducer.py`, `o3_transducer.py`, `o4_transducer.py`.
- Notes: `CRYPTID_CLASSIFICATION_2026-07-04.md` (trichotomy), `O17_CORE_TRANSDUCER.md` / `O3_TRANSDUCER.md`
  (Type II), `MAHLER_HALT_GATES_2026-07-04.md` / `O2_O7_HALT.md` / `SPACE_NEEDLE_HALT.md` (gates),
  `BB6_FRONTIER_CENSUS_2026-07-04.md` (census), `CRYPTID_AUDIT_2026-07-04.md` (soundness audit).
- Kernel side: `BB6_FRAMEWORK_PACKAGE.md`, `BB6_NO_STRUCTURE_THEOREM.md`, `CRYPTID_KERNEL.md`.
