# BB(6) cryptid package — the slow-width frontier, classified and gated (2026-07-04)

*External-shareable consolidation of the cryptid side of the BB(6) program (the counterpart of
`BB6_FRAMEWORK_PACKAGE.md`, which packages the (K)/Mahler kernel side). It collects: the machine-verified
**tetrachotomy** of the named cryptids, the **`[PROVEN from table]` halt gates** (uniform across all four types),
the **Type-II structural-outlier** dissections (o17, o3), the **1104-holdout frontier census** (global
fingerprint), and the **EFF-EQ leverage map** (which cryptids' non-halt one tool would resolve). SOUNDNESS: every
claim is `[PROVEN]`/`[OBSERVED]`/`[OPEN]`, machine-verified vs the raw TM; **no machine is decided**; halting is
`[OPEN]` for all. Interpreter `/opt/homebrew/bin/python3.13`.
Update 2026-07-04: trichotomy → **tetrachotomy** (a fourth type, fixed-arity counter bouncers); the phenotype
classification is proven **`(K)`-hard to compute** but **projects onto a 2-wall dichotomy**; one new Type-I
Mahler machine (L921) found (plus an independent re-derivation of the named o7); the halt-gate mechanism is
**uniform across all four types**. See §2, §5, §7.*

## 1. The one-paragraph statement

> **Currency note (2026-07-28).** The frontier count below is the `1104` list of 2026-04-29, current
> when this package was written. The most recent published list is **`BB6_holdouts_1094.txt`
> (2026-06-29)**, and **two of its entries have since been decided by this program** — see
> `PAPER_TWO_HOLDOUTS_DECIDED.md`. Neither is a named cryptid, so nothing in the classification below
> changes; only the count does.

The BB(6) open frontier is **1104 undecided holdouts**, and they are **structurally homogeneous**: every one is
a **slow polynomial-growth counter/bouncer** (tape width `∼ step^a`, `a ≤ ~0.8`; none halts or grows
exponentially in width within cap). The ~15 named cryptids are **representatives** of this mass, and split by
*where their hardness lives* into a machine-verified **trichotomy** — each type's halting reduces, via a
`[PROVEN from the table]` halt gate, to one of **two walls**: single-orbit **(K)/Mahler-3/2 (Erdős)
equidistribution**, or **generalized-Collatz** reachability. No new tool crosses either wall.

## 2. The tetrachotomy (`[OBSERVED]`, machine-verified; `BB6_TYPE_IV_CENSUS_2026-07-04.md`)

| type | machines | mechanism | wall |
|---|---|---|---|
| **I — equidistribution-kernel Mahler** | Antihydra, o10, o15, o18, o2, o7, o11, o12, o13, o14, o16, o4, **+L921 (new)** | a scalar/counter **value orbit `×3/2` (p=2), `×8/3`/`×4/3` (p=3)**, unary/odometer-encoded; halt = a parity/existence event on it | **(K) / Mahler-3/2 (Erdős)** |
| **II — kernel-less carry-cascade outlier** | **o17, o3** (+ ~80% of the frontier) | a **tame bounded/small-digit odometer, no value orbit**; Collatz-irregular halt predicate | **generalized-Collatz** carry-existence |
| **III — scalar generalized-Collatz** | Space Needle | a single **scalar block** with an explicit 2-adic map; halt = orbit hits a sparse set | **generalized-Collatz** reachability |
| **IV — fixed-arity counter bouncer** `[NEW]` | H5-class (multiple) | a **bounded number of unbounded unary counters** (not a growing digit-string, not a scalar); inner descent + refill; halt = `11`-adjacency | **generalized-Collatz** counter-machine reachability (Minsky-general) |

**Two key findings.** (a) **Growth-rate is fully orthogonal to type** — every growth band (`√t`, cubic) holds ≥2
types; the discriminator is the **content** (exponential value orbit vs bounded-digit cascade vs scalar vs
fixed-arity counters), never the growth exponent. (b) **The phenotype (I vs II/III/IV) is `(K)`-hard to compute**
(deciding "Type I" = detecting positive entropy of the driver orbit; evidence: a proxy-flagged Type-I machine RE-
refuted to Type-II, and Space Needle presents as bounded-arity), **but it projects onto a clean 2-wall dichotomy**:
`{I} → (K)/Mahler`, `{II,III,IV} → generalized-Collatz`.

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

**The halt-gate mechanism is UNIFORM across all four types** (`BB6_TYPE_IV_CENSUS_2026-07-04.md` §5d): every
reverse-engineered gate — including the new Type-IV (H5-class) bouncers — is a **unique-predecessor `00`/`11`
adjacency-existence** event that never fires from the blank tape (verified over 10³–10⁶ halt-state entries with the
dangerous neighbour never appearing). Only the **substrate** the existence event runs over differs (Mahler orbit →
(K); cascade/counter → generalized-Collatz) — which is why the wall is *not* readable from the gate.

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
- **Global fingerprint (`BB6_TYPE_IV_CENSUS_2026-07-04.md`, all 1104 traced):** by the `#blocks`-vs-width
  signature, **~80% are Type-II** (growing-length bounded-digit cascades), **5% bounded-arity** (a *mix* of Type
  I / IV — the fingerprint over-counts, since a clean split is `(K)`-hard, §2), rest intermediate; **0 halters** in
  the sampled budget. One new Type-I Mahler `×3/2` machine (L921) was found in the bounded band and ratio-verified
  (`×1.5` tails) with its `00`-gate proven; a second bounded-band machine (L373) turned out to be the already-named
  **o7** (an independent RE cross-check — the holdout file contains the named cryptids).

## 6. Honest verdict + the two walls

**All fifteen named cryptids `[OPEN]`; the frontier is `0`-decidable by available sound deciders; no machine
decided.** Each reduces (via its `[PROVEN]` gate) to one of two walls:

- **(K) / Mahler-3/2 (Erdős)** — single-orbit equidistribution of `⌊(p/q)^n⌋`; unlocks all 12 Type-I at once;
  proven internal barriers (No-Structure, Coverage No-Go, decider-preemption, even-count floor); **generational**
  (`BB6_FRAMEWORK_PACKAGE.md`, `PROBLEM_LIST.md` P1/P1′).
- **generalized-Collatz** — reachability/parity over a carry cascade (Type II) or a scalar orbit (Type III); no
  bounded predictor (verified core-hard); a Collatz-class breakthrough per family.

The tetrachotomy is **stable** (a larger extension sample found no fifth type), and — whether or not it extends to
every un-analyzed holdout — **deciding BB(6) is gated by these same two walls uniformly**, not by 1104 independent
problems. Sharper still (§7): the frontier's **non-halt direction** collapses to a *single* effective tool (EFF-EQ)
for everything except the apex o10 and the off-axis Type-IV. That reframing — a homogeneous frontier behind two
named walls, with one tool covering the non-halt of its bulk — is the cryptid side's durable contribution.
**No machine decided. No label upgraded. Halting `[OPEN]`.**

## 7. The EFF-EQ leverage map — one tool for the frontier's non-halt direction (`P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md`)

Beyond "two walls," the **non-halt direction** of most of the frontier reduces to a *single* effective tool. Each
cryptid's halt is an existence event on a target set; **the target's structural role sets a readable
Borel–Cantelli direction** (`NESTED_COLLATZ_THEOREM.md` + this session):

- **Spontaneous-defect target** (a `00`/`11` the normal form structurally suppresses — the Type-I two-counters,
  Type-III Space Needle, the o3-class Type-II): **thin ⇒ convergent (BC-I) ⇒ non-halt is generic**. The one tool
  needed is **EFF-EQ** = *effective single-orbit equidistribution* (a rate crossing the log→linear digit-frequency
  gap). It resolves the non-halt of the **entire spontaneous-defect frontier at once** — materially broader than
  the ~12 Type-I machines. `[CONDITIONAL on EFF-EQ]`. Space Needle is the cleanest computed case (halt ⟺ its
  scalar orbit ever becomes all-ones `2^k−1`; annealed hit-probability `Σp_n=1.73<∞` super-convergent, avoids the
  set to `10^558`).
- **Generic-event target** (constant-density per-epoch parity — **only o10**, `p_e≈1/3`): **thick ⇒ divergent ⇒
  HALT is generic**. o10 is the **apex / mirror of Antihydra** — `[PROVEN structural]` it halts ⟺ a
  doubly-exponential reseed orbit hits a fixed **density-⅓** set `S_halt` (`O10_APEX_2026-07-04.md`); its non-halt
  would need *anti-genericity* (avoid a positive-density set forever), and its halt a doubly-exp-infeasible witness.
- **Counter-machine target** (**Type-IV**): a multi-coordinate counter vector, **outside** the Borel–Cantelli
  framework (no scalar reseed) — a separate generalized-Collatz reachability object.

**Hardness order:** `{spontaneous-defect convergent = EFF-EQ-reachable, one tool}` at the thin/generic-non-halt
pole `—` `{o10}` alone at the thick/generic-HALT pole `—` `{Type-IV}` off-axis. The single missing tool (EFF-EQ /
P1′, crossing the log→linear gap) is the same one the (K) kernel needs; a fresh cross-field probe (CDT holonomy,
Mersenne-avoidance, 2024–26 effective equidistribution) confirms **no existing tool reaches it**.

**Capstone (`GRAND_SYNTHESIS_2026-07-04.md`, `CRYPTID_NONAFFINE_UNIFICATION_2026-07-04.md`).** The frontier
compresses to **one object, one halt-form, one tool**: every cryptid runs a **non-affine floor-multiplier
`⌊(p/q)·⌋` update** (value for Type I, scalar/vector counter for III/IV, carry cascade for II) — which is *why* no
bouncer/VASS decider catches them; every halt is **reachability of a target config**; and the target's **thinness**
grades the difficulty, so a **single scalar single-orbit-equidistribution tool** resolves the non-halt of the
thin-target *scalar* frontier (all B1 + o3/o17/Space Needle), with **two** classes outside: **o10** (thick, density-⅓
target, BC-II) and **Type-IV/H5** (thin but a counter *vector*, off the scalar axis). B1 vs B2 is just **which
reading** — equidistribution vs reachability — of the *same* non-affine engine.

## Reproduce / index
- Halt gates: `cryptid_halt_gates_verify.py`, `o17_core_transducer.py`, `o3_transducer.py`, `o4_transducer.py`.
- Notes: `CRYPTID_CLASSIFICATION_2026-07-04.md` (trichotomy) + `BB6_TYPE_IV_CENSUS_2026-07-04.md` (tetrachotomy,
  global census, A9/A11 gates, `(K)`-hard split), `O17_CORE_TRANSDUCER.md` / `O3_TRANSDUCER.md` (Type II),
  `MAHLER_HALT_GATES_2026-07-04.md` / `O2_O7_HALT.md` / `SPACE_NEEDLE_HALT.md` (gates),
  `BB6_FRONTIER_CENSUS_2026-07-04.md` (census), `CRYPTID_AUDIT_2026-07-04.md` (soundness audit).
- Leverage / walls: `P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md` (EFF-EQ map + convergent/divergent criterion),
  `O10_APEX_2026-07-04.md` (o10 apex), `BB6_WALLS_ENTANGLEMENT_2026-07-04.md` (the two walls, `(K)`-hard classifier).
- Kernel side: `BB6_FRAMEWORK_PACKAGE.md`, `BB6_NO_STRUCTURE_THEOREM.md`, `CRYPTID_KERNEL.md`.
