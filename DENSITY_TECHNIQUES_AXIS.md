# The "one-sided density bound" technique axis — closed, 4 distinct structural reasons (2026-06-27)
The non-halt of Antihydra needs a ONE-SIDED FREQUENCY bound: liminf even-density `E_n/n ≥ 1/3` along the
SINGLE transient orbit `c_{n+1}=⌊3c_n/2⌋`, `c_0=8`. We surveyed every classical technique that has ever
produced a density-flavored unconditional result for a Collatz-type problem. ALL fail, each for a
**different** structural reason, and all leave the single-orbit frequency exactly at the Mahler /
equidistribution barrier. No literature bridges any of them to a single specified orbit.

| technique | strongest proven result | why it does NOT reach single-orbit even-density |
|---|---|---|
| **Flatto–Lagarias–Pollington** (Acta Arith. 1995) / Dubickas | `limsup{ξ(3/2)ⁿ}−liminf ≥ 1/p = 1/3`, all real ξ | bounds the **support** (spread) of fractional parts, not the **frequency** of visiting a sub-interval. Gap of *kind*, not size. |
| **Tao 2019** (Forum Math Pi) | almost-all Collatz orbits attain almost bounded values | **a.e. / logarithmic-density over starting points** — by construction exempts any specified single orbit. |
| **Krasikov–Lagarias** (Acta Arith. 2003) | `#{n≤x : Collatz orbit reaches 1} ≥ x^0.84` | **set-counting**: leverage = branching multiplicity of the inverse tree over MANY integers. Antihydra is ONE forward path with no branching set to count. |
| **Invariant-measure / Birkhoff (ergodic)** | Birkhoff: a.e. point equidistributes w.r.t. an a.c.i.m. | `T(c)=⌊3c/2⌋` is **transient** (fixed points only {0,1}, `T(c)>c` for `c≥2`, orbit → ∞): NO nontrivial invariant probability measure, NO recurrence. Even-density is a Cesàro average along one transient orbit, not a space-average. |
| **Kontorovich–Lagarias stochastic models** (2010) | rigorous random models predicting orbit statistics | predictions/heuristics for random models, NOT theorems about the deterministic integer sequence. |

**The single clearest reason (Krasikov–Lagarias, the closest density technique):** its only source of
quantitative leverage is "many preimages per inverse-tree node," i.e. a *population* of integers. A single
specified transient orbit is one path with no population to count. The bridge from set-counting density to
single-orbit frequency *would itself be* an unconditional single-orbit equidistribution result — which is
the open Mahler barrier. The bbchallenge wiki attributes Antihydra's intractability to exactly this.

**Conclusion.** Combined with the earlier analytic/algebraic/digit/symbolic/transfer-operator obstruction
map, this closes the remaining "density-bound" axis: there is no known technique — averaged, support-based,
set-counting, or ergodic — that yields a one-sided frequency bound for a single specified transient orbit.
The wall is the specified-orbit equidistribution itself (Mahler 3/2 / AEV 2025), now confirmed from the
density-technique side with four independent structural reasons.

*Citations verified to abstract/record level; Krasikov–Lagarias internal LP formulation unverified at
line level. The set-vs-single-orbit and transience obstructions are solid (transience machine-checked:
fixed points {0,1}, T(c)>c for 2≤c<2·10⁵).*
