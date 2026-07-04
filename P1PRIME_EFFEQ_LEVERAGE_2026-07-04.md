# P1′ theory-building — EFF-EQ as the frontier-wide non-halt engine: the leverage map + rate hierarchy (2026-07-04)

*First theory-building brick of the P1′ program (`NEW_MATH_PROGRAM.md`) that folds in this session's
tetrachotomy + census + walls-entanglement results. It positions the **EFF-EQ** object (effective single-orbit
equidistribution rate, `NESTED_COLLATZ_THEOREM.md` §2) against the full BB(6) cryptid frontier, quantifies how much
of it a single EFF-EQ theorem would resolve, and pins the exact rate each direction needs. It also **sharpens (and
partly corrects) the B1/B2 probe's "P1′ has broader leverage" claim** (`BB6_WALLS_ENTANGLEMENT_2026-07-04.md`,
Angle 3(ii)) into a precise, labeled map. SOUNDNESS: `[PROVEN]`/`[PROVEN structural]`/`[ARGUED]`/`[OBSERVED]`/
`[OPEN]` throughout; **this is a CONDITIONAL/positioning brick — it decides no machine and proves no non-halting.***

## 0. Headline

- **EFF-EQ is one object that drives the NON-HALT direction of the *convergent-case* frontier at once** — not just
  the ~12 Type-I Mahler machines, but every cryptid whose halt target is **thin/decaying** (Borel–Cantelli-I side):
  most Type-I two-counter machines **and** the sparse-target Type-III (Space Needle). This is the precise form of
  the "broader leverage" observation.
- **The B1/B2-probe claim "P1′ covers much of B2" is SHARPENED and partly CORRECTED here:** EFF-EQ covers the
  **convergent direction**, which is *not* coextensive with B2. It does **not** reach (i) the **divergent** cases
  (o10 → the BC-II / o10 wall, `[PROVEN negative]`), (ii) the **counter-machine Type IV** (does not fit the
  reseed-BC substrate), or (iii) the un-reverse-engineered **Type-II cascades** (o3-class; `00`-appearance-density
  decay `[OPEN]`). The correct statement is **"EFF-EQ = the BC-I / convergent engine,"** and BC-I ⊊ B2.
- **The rate EFF-EQ needs on the convergent side is strictly weaker than `(K)`** (a rate beating a *summable*
  per-epoch target, not a positive liminf density) — **but the gap to it is the same annealed→quenched
  empty-toolbox wall.** "Weaker hypothesis, identical wall."
- **Durable gain:** a single leverage map unifying tetrachotomy (phenotype) × BC-dichotomy (direction) × census
  (mass) × walls (B1/B2), giving the honest target-size of the one missing tool.

## 1. The EFF-EQ object and the BC dichotomy `[PROVEN structural / CONDITIONAL, NESTED_COLLATZ + EXISTENCE_META]`

For the nested/reseed cryptids, halt ⟺ **Borel–Cantelli over the outer refill orbit**: the reseeded inner orbit
hits its halt phase `H_e` in epoch `e` with per-epoch density `p_e`, and `HALT ⟺ ∃^∞ e: O_e ∩ H_e ≠ ∅`
`[PROVEN structural]`. The dichotomy:

| | **convergent** `Σ_e p_e < ∞` | **divergent** `Σ_e p_e = ∞` |
|---|---|---|
| BC side | **BC-I** — convergence, **no independence needed** | **BC-II** — divergence, **needs independence** |
| direction | **non-halt**-leaning | **halt**-leaning |
| single-orbit feasible? | **yes** (`EFF-EQ`, a rate) | **no** — a deterministic orbit has no independence to feed (`O10_HALTER.md` `[PROVEN negative]`) |

**EFF-EQ (the hypothesis):** an effective discrepancy bound `D_N(B)` for the inner map, uniform over the reseed
family, so the realized hit-count tracks `Σp_e` up to a non-overwhelming error. On the convergent side this is
"beat a **summable** target" — `[CONDITIONAL]`, and **strictly weaker than a positive liminf density** (= `(K)`).

## 2. The tetrachotomy → BC-direction map `[NEW; labels per cell]`

Positioning each of the four phenotypes (`BB6_TYPE_IV_CENSUS_2026-07-04.md`) on the BC axis — the genuinely new
content, since `NESTED_COLLATZ` predates the tetrachotomy:

| phenotype | halt target | BC side | EFF-EQ reaches non-halt? | label |
|---|---|---|---|---|
| **I — Mahler value orbit** (nested: o10, o13…) | `b=0` at odd `m`, **fixed-measure** (o10) | **divergent** | **NO** — BC-II / o10 wall | `[PROVEN negative]` for o10 |
| **I — Mahler value orbit** (two-counter: o2/o7/o11/o12/o14/o16, **L373, L921**) | `00`/phase defect, **thin** | **convergent**-lean | **YES** (conditional on EFF-EQ, BC-I) | `[OBSERVED thin]` + `[CONDITIONAL]` |
| **III — scalar generalized-Collatz** (Space Needle) | orbit hits **sparse** `S={2^k−1}∪sporadic` | **convergent** (shrinking target) | **YES** (conditional; sparse ⇒ Σ<∞) | `[ARGUED]` (S proven sparse) |
| **II — bounded-digit cascade** (o3, o17-class) | `00`/marker-parity **existence** | **unknown** — `00`-appearance density decay not established | **UNCLEAR** | `[OPEN]` (needs RE of the cascade density) |
| **IV — fixed-arity counter bouncer** (H5-class) | `11`/`00` adjacency over a **counter machine** | **not a reseed-BC substrate** (Minsky-general) | **NO** (as posed) | `[OPEN]` / more general |

**Reading.** EFF-EQ's non-halt reach = the **convergent** rows = {thin-target Type-I two-counter} ∪ {sparse-target
Type-III}. This is broader than the 12 named Type-I machines (it adds Space Needle and the two new L373/L921) but
is **not** all of B2: the divergent Type-I (o10), Type IV, and un-RE'd Type-II sit outside it. The A11 gate result
(the `00`/`11` existence-gate mechanism is *uniform* across all four types) is consistent: a uniform gate whose
**target thinness** — the p_e decay — is what places a machine convergent vs divergent, and that thinness is *not*
readable from the gate (matching the `(K)`-hard classifier, `BB6_WALLS_ENTANGLEMENT` Angle 3(i)).

## 3. This session's new Type-I machines are convergent-lean `[OBSERVED, ties A9 in]`

The A9 halt-gate invariant (`BB6_TYPE_IV_CENSUS` §5b, `gate_invariant.py`) is exactly the **thinness / convergence**
evidence for L373 and L921: the `00`-gate's dangerous neighbour never appears — state `C` reads `0` 7645 (L373) /
7333 (L921) times in 100 M steps with the left neighbour `1` in **every** case (0 firings). So the per-epoch
halt-target density is empirically `0` on the tested horizon ⇒ **convergent-lean ⇒ BC-I ⇒ within EFF-EQ's non-halt
reach**. L373, L921 therefore join the convergent Type-I family (o2/o7/o11/o12/o14/o16) — non-halt-leaning,
`[CONDITIONAL on EFF-EQ]`, decision `[OPEN]`.

## 4. The rate hierarchy — "weaker hypothesis, same wall" `[the precise sub-(K) status]`

Three nested asks, in increasing strength:

1. **BC-I convergent rate** (non-halt, thin target): a single-orbit discrepancy `D_N = o(1)` beating a *summable*
   per-epoch target, uniform over reseeds. **Strictly weaker than `(K)`** (no positive-liminf-density demand).
2. **Two-sided liminf density** `= (K)` (Antihydra: `liminf #even/n ≥ 1/3`): the full Mahler-3/2 kernel.
3. **BC-II divergent rate** (halt, fixed-measure target): additionally quenched **quasi-independence** across the
   doubly-exp reseeds — **strictly harder** than `(K)`, and structurally unavailable to a single orbit (o10 wall).

**The honest catch (why (1) is not a free win):** although (1) is a *weaker hypothesis* than (2), the **gap** to
proving (1) is the **same annealed→quenched transfer** that blocks (2). The annealed BC-I statement
(`Haar(limsup H_e)=0`) is already `[PROVEN]` (`EXISTENCE_META_THEOREM.md` §3a); the missing step is that the
**specified** orbit realises the annealed rate — single-orbit effective equidistribution, the empty-toolbox object.
`EVEN_COUNT_FLOOR.md` proved the elementary floor is `Θ(log n)` and sharp; the first super-log step is generational
on *either* the two-sided (K) or the one-sided BC-I ask. So the rate hierarchy has a **strictly-weaker rung (1)**
whose **wall is identical** to (2). This refines the milestone-ladder collapse: the sub-`(K)` target exists as a
*hypothesis* but not as a *reachable rung*.

## 5. Leverage quantification vs the census `[NEW, honest bound]`

From the global census (`BB6_TYPE_IV_CENSUS` §1): the frontier is ~80% Type II, ~5% bounded-arity (mix of I/IV),
rest intermediate; **0 halters** in the sampled budget. A single EFF-EQ theorem (BC-I strength) would resolve the
**non-halt direction** of the convergent subset:
- **All thin-target Type-I** (the ~12 named + L373/L921 + any convergent two-counter in the 5% band) — the (K)
  family, one theorem, all at once.
- **The sparse-target Type-III** (Space Needle-class).
- **NOT** the divergent Type-I (o10-class), Type IV (counter machines), or the ~80% Type-II cascades unless each is
  first RE'd and shown convergent (thin `00`-density) — an `[OPEN]` per-class question.

So the precise leverage is: **EFF-EQ = the one tool for the entire *convergent-target* frontier's non-halt
direction**, materially broader than "the 12 Type-I machines," but bounded above by the convergent fraction — it is
*not* a frontier-wide decider (the divergent/counter/uncharacterized mass needs separate BC-II / counter-machine /
per-class inputs). Quantifying the convergent fraction exactly needs the per-machine RE that §2 of the census
showed is itself `(K)`-hard.

## 6. Honest verdict

**(b) — a consolidating/positioning brick; no machine decided, no new provable rung.** The genuine gains: (i) the
**tetrachotomy → BC-direction map** (§2), placing all four phenotypes on the convergent/divergent axis and showing
EFF-EQ = the BC-I engine; (ii) the **sharpened, partly-corrected** leverage claim (EFF-EQ reaches the
convergent-target frontier, not all of B2 — divergent/IV/uncharacterized-II are outside); (iii) the **rate
hierarchy** with the precise "strictly-weaker hypothesis (BC-I), identical annealed→quenched wall" statement; (iv)
the A9 tie-in (L373/L921 are convergent-lean). No sub-`(K)` *rung* is opened — the BC-I ask, though a weaker
hypothesis, is blocked by the same empty-toolbox annealed→quenched transfer. The durable output is a single map that
sizes the one missing tool honestly. **`(K)` / P1′ remain `[OPEN]` = generational. No machine decided. No label
upgraded.**

## Reproduce / basis
- Grounding `[PROVEN structural / CONDITIONAL / PROVEN negative]`: `NESTED_COLLATZ_THEOREM.md` (BC dichotomy +
  EFF-EQ), `O10_HALTER.md` (BC-II negative), `EXISTENCE_META_THEOREM.md` §3a (annealed BC-I proven),
  `EVEN_COUNT_FLOOR.md` (log-floor sharp). New this session: `BB6_TYPE_IV_CENSUS_2026-07-04.md` (tetrachotomy +
  census + A9/A11 gates), `BB6_WALLS_ENTANGLEMENT_2026-07-04.md` (walls entanglement, Angle 3). No new numerics
  beyond A9's `gate_invariant.py`.
