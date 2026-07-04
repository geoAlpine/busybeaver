# The non-affine unification — every BB(6) cryptid is a floor-multiplier / non-VASS machine; the two walls are two ways to halt on it (2026-07-04)

*Synthesis of the session's structural findings (`O17_SKEW_PRODUCT`, `O17_O3_STRUCTURE`, `BB6_TYPE_IV_CENSUS`,
`P1PRIME_EFFEQ_LEVERAGE`, `SPACE_NEEDLE_HALT`) into a **decidability-theoretic** characterization: the generalized-
Collatz wall (B2) is precisely the **affine (VASS/Presburger-decidable) → floor-multiplier (Collatz-hard)
boundary**, crossed by every B2 cryptid via its specific non-affine update; and more deeply, **every** BB(6)
cryptid — B1 and B2 alike — runs a **non-affine (`⌊(p/q)·⌋` or irregular-carry) update**, with the two walls being
the two ways a halt reads it (equidistribution vs reachability). SOUNDNESS: `[OBSERVED]`/`[PROVEN-in-lit]`/
`[ARGUED]`; halting `[OPEN]` for all; no machine decided.*

## 0. Headline
- **The decidability line for counter/bouncer machines is affine vs floor-multiplier.** An update built from
  **constant increments** (`A↦A+c`, `(a,b)↦(a−2,b+3)`) is **Presburger/VASS-definable ⇒ reachability DECIDABLE**
  (Karp–Miller / Presburger). A **floor-multiplier** `⌊(p/q)·⌋` — whose ratio *varies with the 2-adic data* —
  is **not** VASS-definable and is the **generalized-Collatz / Collatz-class** operation.
- **Every B2 (generalized-Collatz) cryptid crosses this line** via a non-affine update; the **arity varies** (scalar
  → fixed → skew-product) but the **non-affinity is uniform** = the B2 wall (§1).
- **Deeper: every BB(6) cryptid — B1 too — runs a non-affine update.** B1 (Type I) is a floor-multiplier on a
  **value** (`⌊3c/2⌋` orbit), B2 on a **counter/carry**. The two walls are the two **halt-readings** of the same
  non-affine engine: **equidistribution** of the value's digits (B1 → `(K)`) vs **reachability** of a target
  config (B2 → generalized-Collatz) (§2).

## 1. The B2 cryptids, decidability-theoretically `[OBSERVED / PROVEN-in-lit]`
| cryptid | type | structure (arity) | the non-affine update | why non-VASS |
|---|---|---|---|---|
| **Space Needle** | III | **scalar** (1 block) | `f(m)=m+3⌊m/2^{v+1}⌋+v`, `v=`trailing-ones | ratio `f/m` **varies** `2.5,1.46,2.5,1.77,…` with the 2-adic data `v` — a floor-multiplier |
| **H5** | IV | **fixed-arity** (~4–6 counters) | leading `A↦⌈2A/3⌉` descent + refill | `⌈2A/3⌉` floor-multiplier (ratio 2/3), not constant-increment |
| **o3** | II | **bounded-arity** (6–7 segments) | irregular length-transfer between segments; reservoir `Δd∈{0,1,2}` | matched-phase increments **irregular / non-affine** (`O17_O3_STRUCTURE §3c`) |
| **o17** | II | **skew product** (bounded base × unbounded fiber) | base-3 **carrying counter**; leading-block base automaton driven by carry | unbounded-digit carry cascade, carry-dependent (non-VASS) |

**Reading.** The four B2 cryptids have *different arities* — a scalar, a fixed-arity counter, a bounded-arity
bouncer, a skew product — yet **all four replace an affine transfer with a floor-multiplier or a carry-dependent
(non-affine) update.** That is exactly why **no bouncer / affine / VASS decider certifies them** (those deciders
verify constant-increment transfers only): the B2 wall, in decidability terms, **is** the affine → floor-multiplier
boundary. This unifies the B2 side structurally, parallel to how `(K)` unifies B1.

## 2. The deeper unification — one non-affine engine, two halt-readings `[ARGUED]`
Both walls run the **same kind of engine** and differ only in **what the halt reads off it**:

| | **B1 (Type I)** | **B2 (Type II/III/IV)** |
|---|---|---|
| non-affine update | `⌊(p/q)x⌋` on a **value** (`3/2, 8/3, 4/3`) | `⌊(p/q)·⌋` / carry on a **counter** |
| what grows | an exponential arithmetic **value** | a **counter/segment** structure |
| the halt reads | **equidistribution** of the value's digits (parity/density) | **reachability** of a target config (`00`/`11`/sparse set) |
| the wall | `(K)` / Mahler-3/2 / AEV (single-orbit equidist) | generalized-Collatz reachability |
| why hard | the value's digit **frequency** at linear depth | the counter's **orbit** hits a target (no bounded predictor) |

> **One-line synthesis.** Every BB(6) cryptid is a **floor-multiplier `⌊(p/q)·⌋` machine** (or, for o3/o17, a
> non-affine carry cascade of the same character). The two generational walls are the **two questions you can ask
> of a non-affine orbit**: *does its digit-frequency equidistribute* (B1 = `(K)`) or *does its orbit reach a target
> config* (B2 = generalized-Collatz). The floor-multiplier is the common root; the halt-reading picks the wall.

This explains, from one principle, both the tetrachotomy→dichotomy projection (`BB6_TYPE_IV_CENSUS`) and the
`(K)`-hardness of the classifier: telling B1 from B2 = telling **which reading** a machine's halt uses, and both
readings sit on the same non-affine engine (whose entropy is what the `(K)`-hard classifier must detect).

## 3. Decidability consequence `[ARGUED]`
- **The floor-multiplier is the exact obstruction to the standard deciders.** Cyclers/Bouncers/FAR/Presburger
  deciders (bbchallenge Kind-R/affine) certify **affine** transfers; a floor-multiplier `⌊(p/q)·⌋` is non-affine,
  so it **escapes all of them** — which is *why* these machines are Cryptids (`DECIDER_PREEMPTION.md`, now seen
  update-theoretically, not just via the No-Structure over-approximation).
- **The affine↔floor-multiplier boundary is the decidable↔Collatz boundary** for counter/bouncer machines. o3
  (§`O17_O3_STRUCTURE §3c`) sits **on** it — bounded-arity (affine-decidable if the transfer were affine) but with
  an **irregular (non-affine)** transfer — which is the honest reason its decidability stayed `[OPEN]`.

## 4. Honest verdict
**(b) — a decidability-theoretic unification.** The B2 wall = the **affine (VASS/Presburger) → floor-multiplier
(Collatz-hard) boundary**, crossed by every B2 cryptid (Space Needle scalar-`⌊·⌋`, H5 `⌈2A/3⌉`, o3 irregular
transfer, o17 carrying counter) despite differing arity; and every BB(6) cryptid runs a non-affine engine, the two
walls being **equidistribution vs reachability** readings of it. This synthesizes the session's o17/o3 structure
work with H5/Space Needle and gives B2 a clean characterization parallel to `(K)` for B1. No decision follows (the
floor-multiplier is undecidable-in-kind); the value is the **unifying structural principle**. **Halting `[OPEN]`.
No machine decided. No label upgraded.**

## Reproduce
- Floor-multiplier signature (`scratchpad`, `/opt/homebrew/bin/python3.13`): Space Needle `f/m` ratio varies with
  trailing-ones `v`; H5 `⌈2A/3⌉`; contrast constant-increment affine transfers (VASS-definable). Basis:
  `O17_SKEW_PRODUCT_2026-07-04.md`, `O17_O3_STRUCTURE_2026-07-04.md` (§3c irregular transfer), `SPACE_NEEDLE_HALT.md`
  (`f(m)`), `BB6_TYPE_IV_CENSUS_2026-07-04.md` (H5 `⌈2A/3⌉`, tetrachotomy→dichotomy), `DECIDER_PREEMPTION.md`,
  `PROBLEM_LIST.md` (B1/B2). VASS/Presburger decidability: Karp–Miller; Collatz-class = floor-multiplier iteration.
