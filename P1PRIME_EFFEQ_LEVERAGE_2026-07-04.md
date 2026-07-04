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
- **The convergent/divergent membership is READABLE (§7.3, bricks 2–4):** a **spontaneous-defect** target
  (`00`/`11` the normal form suppresses — o3-class, two-counters, Space Needle's all-ones) is convergent /
  EFF-EQ-reachable; a **generic-event** target (constant-density per-epoch parity — only o10) is divergent /
  o10-wall. Space Needle is computed **super-convergent** (`Σp_n=1.73`); yet the wall EFF-EQ must cross is the
  **same log-vs-linear depth gap** as `(K)` (brick 4).

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

## 7. Bricks 2–4 — the convergent/divergent CRITERION, computed `[OBSERVED + ARGUED]`

Three follow-up bricks fill the map's `[OPEN]` cells and pin the gap size, and a clean **structural criterion**
for the BC direction emerges.

### 7.1 Brick 3 — Space Needle (Type III) is the cleanest computed BC-I convergent `[OBSERVED, exact]`
The scalar orbit `m ↦ f(m)=m+3⌊m/2^{v+1}⌋+v` (`v`=trailing 1-bits; verified: `2,5,9,16,40,100,250,625,1094,…`)
grows geometrically `m_n ~ 2^{0.927 n}` (ratio ≈ 1.90) and **avoids the halt set `S={2^k−1}∪sporadic` completely**
(0 all-ones, 0 sporadic hits over 2000 steps, `m_n` up to 1856 bits ≈ `10^558`). The annealed per-epoch target
density `p_n = |{2^k−1}≤m_n|/m_n = ⌊log₂(m_n+1)⌋/m_n ~ n/2^{0.927n}` **decays super-geometrically** (`p_n<10^{−13}`
by `n=50`), so `Σ_n p_n = 1.73 < ∞` **decisively**. So Type III is BC-I convergent in the extreme; the annealed
non-halt prediction is overwhelming and the **entire** difficulty is quenched avoidance of the all-ones numbers.

### 7.2 Brick 2 — Type-II (o3-class) targets are spontaneous defects, empirically thin `[OBSERVED]`
For the three Type-II machines tested (true gates via `haltgate2.py`):
- **o3** `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC`: `HALT ⟺ E reads 00`; over **1 666 179** `F`-entries in 50 M
  the read is **always 1** (0 firings). Moreover o3's tape is **structurally `00`-free** beyond transient (0
  `00`-gaps at 10⁴–10⁸ steps while single-0 gaps grow 50→4959) — the normal form has only single-0 gaps, so the
  halt `00` is a **spontaneous defect**.
- **H2** `…_0RD1RA`: `HALT ⟺ 11`; halt-state entered only **2×** in 50 M (target essentially never approached).
- **H3** `…_0RB0RA`: `HALT ⟺ 11`; 111 254 entries, read **always 0** (0 firings).
So the o3-class halt-targets are **spontaneous defects in a structure that suppresses them** — empirically thin,
`convergent-lean`. This **upgrades the map's Type-II cell from `[OPEN]` to `convergent-lean [OBSERVED]`** (the
annealed *rate* is still un-extracted — Type-II has no clean outer-epoch model — so it is `[OBSERVED]`, not the
`[computed]` of Space Needle).

### 7.3 The emergent CRITERION — spontaneous-defect vs generic-event `[ARGUED]`
> **BC direction is readable from the halt-target's structural role.** A **spontaneous-defect** target (a `00`/`11`
> that the machine's normal form structurally suppresses — o3, o11, o12, the Type-I two-counters, Space Needle's
> all-ones) has **decaying/near-zero density ⇒ convergent ⇒ BC-I ⇒ within EFF-EQ's reach**. A **generic-event**
> target (a per-epoch parity/measure occurring at constant density — **only o10**: `b=0` at odd `m`, `p_e≈1/3`
> `[VERIFIED]`) is **divergent ⇒ BC-II ⇒ the o10 wall**.

This criterion is **orthogonal to the (K)-hard phenotype classifier** (§5c): the phenotype (I vs II/III/IV) needs
the driver's entropy and is (K)-hard; the BC direction needs only the target's structural role (defect vs generic)
and is **structurally readable**. It places **essentially the whole frontier except o10-type generic-event machines
and Type-IV counter machines** in the convergent / EFF-EQ-reachable group.

### 7.4 Brick 4 — the annealed→quenched gap = the SAME log-vs-linear depth gap `[ARGUED, computed for Space Needle]`
Although the convergent hypothesis is *formally weaker* than `(K)`, the **wall to cross is identical**. For Space
Needle, avoiding `{2^k−1}` = certifying `m_n` is **not all-ones** = controlling **all `bit_length(m_n) ~ 0.927 n`
bits**; but unconditional single-orbit digit control reaches only `~0.85 log₂ n` bits (the empirical depth-reach
ceiling, `DEPTH_REACH_CLARIFICATION.md`). The **need/reach ratio grows `16.5× → 199× → ∞`** (`n=100,…,2000`) as
`n/log n` — the **identical log-vs-linear gap** as the (K) kernel. So EFF-EQ's weaker hypothesis (beat a summable,
here super-convergent, target) still requires crossing the **same log→linear digit-frequency gap**; the summable
cushion buys nothing on the depth axis.

### 7.5 Refined leverage `[the sharpened statement]`
Combining: **EFF-EQ / P1′ is one tool for the non-halt direction of the entire *spontaneous-defect* frontier** —
all Type-I two-counters (incl. L373/L921), Type-III (Space Needle), and the o3-class Type-II — i.e. **everything
except the single generic-event divergent machine o10 and the Type-IV counter machines**. That is materially
broader than "the ~12 Type-I machines," and now with a *readable* membership criterion (§7.3). But the tool it
requires is the **same** one — crossing the log→linear single-orbit digit-frequency gap (§7.4) — so there is still
**no reachable sub-`(K)` rung**; the gain is the unified, criterion-based leverage map.

## 8. Honest verdict

**(b) — a consolidating/positioning theory-brick set; no machine decided, no new provable rung.** The genuine gains:
(i) the **tetrachotomy → BC-direction map** (§2), placing all four phenotypes on the convergent/divergent axis and
showing EFF-EQ = the BC-I engine; (ii) the **sharpened, partly-corrected** leverage claim (EFF-EQ reaches the
convergent-target frontier, not all of B2); (iii) the **rate hierarchy** ("strictly-weaker hypothesis (BC-I),
identical annealed→quenched wall"); (iv) the A9 tie-in (L373/L921 convergent-lean); **(v) brick 3 — Space Needle
computed super-convergent BC-I** (`Σp_n=1.73`, avoids `S` to `10^558`); **(vi) brick 2 — o3-class Type-II are
spontaneous-defect, empirically thin ⇒ convergent-lean** (map cell upgraded); **(vii) the emergent CRITERION**
(spontaneous-defect ⇒ convergent/EFF-EQ-reachable vs generic-event ⇒ divergent/o10-wall — *structurally readable*,
orthogonal to the (K)-hard phenotype classifier); **(viii) brick 4 — the annealed→quenched gap is quantitatively the
SAME log-vs-linear depth gap** (`16×→199×→∞` for Space Needle), so the weaker hypothesis buys nothing on the depth
axis. Net: EFF-EQ is one tool for the non-halt of the **entire spontaneous-defect frontier** (all but o10-type and
Type-IV), with a readable membership criterion — but no sub-`(K)` *rung* opens (the wall is the identical log→linear
single-orbit digit-frequency gap). **`(K)` / P1′ remain `[OPEN]` = generational. No machine decided. No label
upgraded.**

## Reproduce / basis
- Grounding `[PROVEN structural / CONDITIONAL / PROVEN negative]`: `NESTED_COLLATZ_THEOREM.md` (BC dichotomy +
  EFF-EQ), `O10_HALTER.md` (BC-II negative), `EXISTENCE_META_THEOREM.md` §3a (annealed BC-I proven),
  `EVEN_COUNT_FLOOR.md` (log-floor sharp). New this session: `BB6_TYPE_IV_CENSUS_2026-07-04.md` (tetrachotomy +
  census + A9/A11 gates), `BB6_WALLS_ENTANGLEMENT_2026-07-04.md` (walls entanglement, Angle 3).
- Bricks 2–4 numerics (session scratchpad, `/opt/homebrew/bin/python3.13`): `brick3_sn.py` (Space Needle orbit +
  `Σp_n` super-convergence + S-avoidance to 10⁵⁵⁸), `brick2_typeII.py` + `haltgate2.py` (o3/H2/H3 gates + `00`-gap
  density = spontaneous-defect thinness), brick-4 inline (need `0.93n` bits vs reach `0.85 log₂ n` = log-vs-linear,
  `16×→199×`). Space Needle TM `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD` (`SPACE_NEEDLE_HALT.md`); o3 TM
  `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC`.
