# Type-IV/H5 has NO scalar reduction — confirming it is a genuine (vector) residual (2026-07-04)

*Follow-up test to the red-teamed grand synthesis (`GRAND_SYNTHESIS_2026-07-04.md`), which put **Type-IV/H5**
outside the scalar single-orbit-equidistribution tool (as a counter *vector*). Question: does H5 secretly reduce to
a **scalar** floor-multiplier orbit (a weighted invariant like Type-I's `V=3a+2b`)? If so it would rejoin the
scalar majority and the residual would shrink to o10 alone. **Answer: NO** — H5 has no scalar reduction; it is
**scalar `⌈2A/3⌉` descent + vector-determined irregular refill**, a skew-product-like structure, genuinely vector.
SOUNDNESS: `[OBSERVED]`; confirms the red-team correction; halting `[OPEN]`; no machine decided.*

## Finding
Extracting H5's counter vector at successive milestones (`scratchpad`, corrected left-turn detection): H5
oscillates between **middle-dominated** states `(1, b, 1)` and **first-dominated** states `(a, 1, c)` — a bouncer
transferring content between two counters. No linear combination is a clean orbit:

- Candidate scalars `a+b+c`, `2a+3b+2c`, `3a+b+2c`, `2a+b+c` are **none conserved** and **none** follows a
  `⌊(p/q)·⌋` law across milestones.
- The "value" (the peak counter `b` in the `(1,b,1)` phase) has record values `6,8,18,23,45,59,99,101` growing
  **irregularly** (ratios `1.02–2.25`, matching the earlier record-peak irregularity, `BB6_TYPE_IV_CENSUS`).

**Structure `[OBSERVED]`.** Within an excursion the leading counter descends cleanly `A↦⌈2A/3⌉` (a scalar
floor-multiplier, verified earlier: `25→17→11`), but the **refill** — which peak the next excursion jumps to — is
**determined by the other counters** and grows irregularly. So H5 is a **scalar descent skew-producted with a
vector-determined refill**: the descent is scalar, the refill is genuinely multi-coordinate. This parallels o17
(bounded base × unbounded fiber) — H5 is *another* skew product, but with a **vector** refill fiber rather than a
carry fiber.

## Consequence
**H5/Type-IV does NOT reduce to a scalar orbit** — confirming the red-team correction (`GRAND_SYNTHESIS`): the
residual outside the scalar single-orbit-equidistribution tool is **two** classes, o10 (thick scalar) **and**
Type-IV/H5 (thin vector), not o10 alone. The test had a real upside (a scalar reduction would have shrunk the
residual to o10); it came back negative, so the corrected two-residual picture stands. H5's non-halt needs a
genuine **multi-dimensional** equidistribution / counter-machine reachability tool, distinct from the scalar `(K)`.

## Honest verdict
**(b) / confirming — no scalar reduction for Type-IV.** H5 is a scalar `⌈2A/3⌉` descent + vector-determined
irregular refill (a skew product with a vector fiber); no weighted-scalar invariant follows a floor-multiplier law.
Type-IV stays a genuine (vector) residual alongside o10. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad` (`/opt/homebrew/bin/python3.13`): H5 milestone counter-vectors (left-turn detection), scalar-combo
  search (none clean), record `b` = `6,8,18,23,45,59,99,101` irregular. H5 TM
  `1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA`. Basis: `GRAND_SYNTHESIS_2026-07-04.md` (residual),
  `P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md §9.2` (Type-IV off-axis), `BB6_TYPE_IV_CENSUS_2026-07-04.md` (`⌈2A/3⌉`, peaks).
