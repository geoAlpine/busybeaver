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
| **I — Mahler value orbit** (two-counter: o2/o7/o11/o12/o14/o16, **+L921 new**) | `00`/phase defect, **thin** | **convergent**-lean | **YES** (conditional on EFF-EQ, BC-I) | `[OBSERVED thin]` + `[CONDITIONAL]` |
| **III — scalar generalized-Collatz** (Space Needle) | orbit hits **sparse** `S={2^k−1}∪sporadic` | **convergent** (shrinking target) | **YES** (conditional; sparse ⇒ Σ<∞) | `[ARGUED]` (S proven sparse) |
| **II — bounded-digit cascade** (o3, o17-class) | `00`/marker-parity **existence** | **unknown** — `00`-appearance density decay not established | **UNCLEAR** | `[OPEN]` (needs RE of the cascade density) |
| **IV — fixed-arity counter bouncer** (H5-class) | `11`/`00` adjacency over a **counter machine** | **not a reseed-BC substrate** (Minsky-general) | **NO** (as posed) | `[OPEN]` / more general |

**Reading.** EFF-EQ's non-halt reach = the **convergent** rows = {thin-target Type-I two-counter} ∪ {sparse-target
Type-III}. This is broader than the 12 named Type-I machines (it adds Space Needle and the new L921; L373=o7 is a rediscovery) but
is **not** all of B2: the divergent Type-I (o10), Type IV, and un-RE'd Type-II sit outside it. The A11 gate result
(the `00`/`11` existence-gate mechanism is *uniform* across all four types) is consistent: a uniform gate whose
**target thinness** — the p_e decay — is what places a machine convergent vs divergent, and that thinness is *not*
readable from the gate (matching the `(K)`-hard classifier, `BB6_WALLS_ENTANGLEMENT` Angle 3(i)).

## 3. The convergent-lean evidence (L921 new + o7=L373) `[OBSERVED, ties A9 in]`

The A9 halt-gate invariant (`BB6_TYPE_IV_CENSUS` §5b, `gate_invariant.py`) is exactly the **thinness / convergence**
evidence for L921 (new) and L373 (= the named **o7**): the `00`-gate's dangerous neighbour never appears — state
`C` reads `0` 7645 (L373=o7) / 7333 (L921) times in 100 M steps with the left neighbour `1` in **every** case
(0 firings). So the per-epoch halt-target density is empirically `0` on the tested horizon ⇒ **convergent-lean ⇒
BC-I ⇒ within EFF-EQ's non-halt reach**. L921 joins the convergent Type-I family (o2/o7/o11/o12/o14/o16) — the
L373=o7 numbers independently confirm o7 is in that family too — non-halt-leaning,
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
- **All thin-target Type-I** (the ~12 named + L921 + any convergent two-counter in the 5% band) — the (K)
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
all Type-I two-counters (incl. new L921), Type-III (Space Needle), and the o3-class Type-II — i.e. **everything
except the single generic-event divergent machine o10 and the Type-IV counter machines**. That is materially
broader than "the ~12 Type-I machines," and now with a *readable* membership criterion (§7.3). But the tool it
requires is the **same** one — crossing the log→linear single-orbit digit-frequency gap (§7.4) — so there is still
**no reachable sub-`(K)` rung**; the gain is the unified, criterion-based leverage map.

## 9. Bricks 5–7 — the two out-of-scope classes + the wall itself `[OBSERVED + ARGUED + lit-verified]`

Completing the map at both ends: the two classes EFF-EQ does **not** reach (o10, Type-IV), and a fresh look at the
shared wall.

### 9.1 Brick 5 — o10 is the frontier APEX (sole generic-event / divergent machine) `[OBSERVED]`
o10's extracted outer model (`O10_HALTER.md`: `HALT ⟺ ∃ epoch e whose countdown from (6,B_e) lands on b=0 at odd
m`) gives an **ensemble halt-probability `p_e = 0.33245 ≈ 1/3`** (`brick5_o10.py`, B=1..20000) — **constant,
non-decaying**, the defining generic-event signature and the sole such target on the frontier. Its deterministic
reseed orbit `B_1=5 → 57 → 210273201 → …` is **doubly-exponential**: epochs 1–2 are feasible (both **refill /
non-halt**), epoch 3 has a terminal `m` of ≈24.7 million digits — **unreachable**.

**[CORRECTED by the o10 apex deep-dive, `O10_APEX_2026-07-04.md`]** An earlier framing here said "o10's wall is
BC-II = a 2nd-moment / pair-correlation statement, strictly harder than `(K)`." The deep-dive **corrects the
order**: o10 halting reduces `[PROVEN structural, 0-mismatch verified]` to a **first-order single-orbit hitting**
— `o10 halts ⟺ the deterministic doubly-exp reseed orbit B_e ever lands in a FIXED density-⅓ set
S_halt={C_t : m_t odd}` (the `⌈3m/2⌉`-from-6 odd-`m` cumulative positions; the `1/3 = (½)/(1.5)`). So o10 is **not**
a higher-moment object — it is the **mirror of Antihydra** on the *same* single-orbit axis: its target is **thick**
(density 1/3), which flips the generic verdict to **HALT** (the sole annealed-HALT machine). BC-II "needs
independence" describes the *failed annealed-halt heuristic*, not the intrinsic hardness. **o10 is the apex because
it is the only machine whose generic verdict is HALT**: deciding it needs either a hitting epoch (finite but
doubly-exp **infeasible** — so if o10 halts it is decidable *in principle*) or, for non-halt, a proof the orbit
**avoids a positive-density set forever** = anti-genericity, stronger than the genericity `(K)` asks.

### 9.2 Brick 6 — Type-IV is a counter-machine, not a scalar reseed `[OBSERVED, structural]`
The nested reseed-BC framework needs a **single scalar** outer value `B_e` per epoch (o10's `B`, o18's seed). H5's
outer-epoch state is instead a **multi-coordinate counter VECTOR** (`brick6_typeIV.py`: block-vectors like
`(17,1,8)`, `(15,1,7,6)`, `(11,6,16,2)`; among epochs with 3 blocks, **3/3 coordinates vary**) — a bounded set of
**interacting** unbounded counters, with the leading one doing the `⌈2A/3⌉` descent + refill. There is **no scalar
hitting-set orbit** to run Borel–Cantelli over; the halt (an `11`-adjacency) is a **fixed-arity counter-machine
reachability** event (Minsky-general). So Type-IV sits **outside the BC dichotomy entirely** — the second
EFF-EQ-unreachable class, orthogonal to o10's (o10 is a scalar-but-divergent; Type-IV is vector-valued).

### 9.3 Brick 7 — the log→linear wall: Space Needle is annealed-easier but the SAME provable depth `[lit-verified, (c)+(b)]`
A fresh literature + structural probe (WebSearch/WebFetch-verified) on whether the Space Needle all-ones-avoidance
framing cracks the log→linear gap — all four angles `(c)`, with one `(b)` refinement:
- **CDT holonomy** (arXiv:2510.04156, verified) — `(c)`: the all-ones event *looks* like a Pillai/S-unit equation
  (`m_n+1 = 2^k`) but is **not** — the orbit is a non-algebraic 2-adic floor iteration, no true power / G-function /
  linear form in logs. CDT stays a fixed-constant tool.
- **Mersenne/digit-avoidance literature** (Stewart, Bugeaud, verified) — `(c)`: digit-sum bounds are the **wrong
  direction** (lower-bound *nonzero* digits; avoidance needs to guarantee a *zero* digit) and need
  multiplicative/automatic structure the floor-orbit lacks. No single-specified-orbit result exists.
- **2024–26 effective equidistribution** (LMW/ELMW unipotent/semisimple, verified) — `(c)`: all spectral-gap
  homogeneous, a.e./averaged; the floor-orbit has no group, no gap, is single-orbit.
- **Angle 3 `(b)` refinement — the payoff:** Space Needle (`avoid {2^k−1}` = **one zero bit** suffices to disprove
  halting at step n, a sparse *existential* target, `Σp_n=1.73` super-summable) is the **existential-single-zero-bit
  face**; Antihydra (`liminf even-density ≥ 1/3`, a **universal density** constraint) is the **universal-density
  face** — **of the SAME kernel.** Space Needle is decisively **annealed-EASIER** (cleaner heuristic target), **but
  NOT provably easier**: certifying "not all-ones for all n" still needs **linear-depth** control of the same
  uncontrolled 2-adic low-bit sub-orbit (the log-controlled block is the *top* `O(log n)` bits; the all-ones failure
  lives across the *entire* bit-string). **Both carry the identical `Θ(n/log n)` gap.** ⇒ record all-ones-avoidance
  as a **weaker sufficient condition of EQUAL provable depth**, not a shortcut.

### 9.4 The completed hardness order `[the synthesis]`
> **spontaneous-defect convergent frontier** (Type-I two-counters, Type-III Space Needle, o3-class Type-II) —
> the **thin-target / generic-non-halt pole** of the single-orbit axis, `(K)`-depth, EFF-EQ-reachable, **one tool
> for all** — vs. — **o10**, the **thick-target / generic-HALT pole** (mirror of Antihydra; non-halt needs
> anti-genericity) ; and **off-axis**: **Type-IV** (counter-machine reachability, no scalar reseed, outside BC).

Antihydra and o10 are the **two poles of the single-orbit-equidistribution axis** (`O10_APEX_2026-07-04.md`); the
whole spontaneous-defect frontier clusters at the Antihydra (thin, generic-non-halt) pole, o10 alone at the thick
(generic-HALT) pole. Space Needle is the **cleanest annealed face** of that thin pole; Type-IV is off-axis. EFF-EQ
/ P1′ is the single tool for the entire thin-pole (spontaneous-defect convergent) band — everything except the
opposite-pole o10 and the off-axis Type-IV.

## 10. Attack A — the unified EFF-EQ hypothesis, concretized `[OBSERVED batch + CONDITIONAL]`

The "one tool for the whole spontaneous-defect band" claim is made concrete by (a) a **uniform thinness
measurement** and (b) a **single hypothesis** covering every band member.

**Uniform thinness `[OBSERVED, 20 M steps, haltgate2.py]`.** Nine spontaneous-defect machines, one table — every
one has a unique-predecessor `00`/`11` gate, **0 firings**, and the halt-state-entry read is the **safe symbol in
100 % of entries**:

| machine | gate | halt-state entries | firings | entry-read |
|---|---|---:|---:|---|
| o2 | F:0 (`00`) | 4 295 | 0 | always 1 |
| o11 | C:0 (`00`) | 4 205 | 0 | always 1 |
| o12 | F:0 (`00`) | 7 016 | 0 | always 1 |
| o13 | E:0 | 4 701 | 0 | always 1 |
| o14 | F:0 (`00`) | 3 881 | 0 | always 1 |
| o16 | F:0 (`00`) | 15 | 0 | always 1 |
| o3 (Type II) | F:0 (`00`) | 666 299 | 0 | always 1 |
| L921 (new) | D:0 (`00`) | 3 688 | 0 | always 1 |
| Space Needle (III) | F:0 (`00`) | 1 231 | 0 | always 1 |

The dangerous neighbour never appears at the reflection state — the halt-target's empirical density is `0` across
the entire band (Type I two-counters, the o3 Type-II cascade, and the Type-III scalar), confirming **uniform BC-I
convergence**.

**The single hypothesis `[CONDITIONAL]`.** Every band member shares one structural skeleton: a **2-adic-driven
floor-orbit driver** (`⌊(p/q)x⌋` for Type-I, the odometer for Type-II, the 2-adic map `f(m)` for Space Needle) and
a **thin defect target** — a specific residue/alignment cylinder the driver must land in for the `00`/`11` to
appear. So the band's non-halt follows from **one** statement:

> **(UNIFIED EFF-EQ).** *There is an effective single-orbit equidistribution rate `ρ(N)→0` for 2-adic-driven
> floor-orbits `x_{n+1}=⌊(p/q)x_n⌋+c(x_n mod 2^k)` such that, for each band member, the orbit's empirical measure
> on its defect cylinder has discrepancy `< (defect density) − o(1)` at the orbit's actual (linear) depth.*

`(UNIFIED EFF-EQ)` ⟹ every defect density stays below the summable threshold ⟹ (BC-I) each orbit hits its defect
finitely often ⟹ **non-halt for the entire spontaneous-defect frontier simultaneously**. This is the precise sense
in which **one tool resolves the band**: the members differ only in `(p/q, c, k, cylinder)`, all instances of the
*same* floor-orbit equidistribution object. `[CONDITIONAL on UNIFIED EFF-EQ]`; the hypothesis is the empty-toolbox
generational object (§4, §7.4) — the `1/3`-strictly-weaker BC-I rate at the same log→linear depth.

**Honest scope.** `[OBSERVED]` the uniform thinness (0 firings, entry-read always safe, 9 machines); `[CONDITIONAL]`
the reduction of the whole band to one hypothesis; the hypothesis itself stays `[OPEN]` = generational. This
concretizes the leverage map's central claim without opening a rung.

## 8. Honest verdict

**(b) — a consolidating/positioning theory-brick set; no machine decided, no new provable rung.** The genuine gains:
(i) the **tetrachotomy → BC-direction map** (§2), placing all four phenotypes on the convergent/divergent axis and
showing EFF-EQ = the BC-I engine; (ii) the **sharpened, partly-corrected** leverage claim (EFF-EQ reaches the
convergent-target frontier, not all of B2); (iii) the **rate hierarchy** ("strictly-weaker hypothesis (BC-I),
identical annealed→quenched wall"); (iv) the A9 tie-in (L921 new + o7=L373 convergent-lean); **(v) brick 3 — Space Needle
computed super-convergent BC-I** (`Σp_n=1.73`, avoids `S` to `10^558`); **(vi) brick 2 — o3-class Type-II are
spontaneous-defect, empirically thin ⇒ convergent-lean** (map cell upgraded); **(vii) the emergent CRITERION**
(spontaneous-defect ⇒ convergent/EFF-EQ-reachable vs generic-event ⇒ divergent/o10-wall — *structurally readable*,
orthogonal to the (K)-hard phenotype classifier); **(viii) brick 4 — the annealed→quenched gap is quantitatively the
SAME log-vs-linear depth gap** (`16×→199×→∞` for Space Needle), so the weaker hypothesis buys nothing on the depth
axis. Net: EFF-EQ is one tool for the non-halt of the **entire spontaneous-defect frontier** (all but o10-type and
Type-IV), with a readable membership criterion — but no sub-`(K)` *rung* opens (the wall is the identical log→linear
single-orbit digit-frequency gap). Bricks 5–7 complete the map: **(ix) o10 is the frontier APEX** — the sole
**annealed-HALT** machine, `[PROVEN structural]`-reduced (deep-dive `O10_APEX_2026-07-04.md`) to a **first-order
single-orbit hitting** of a fixed density-⅓ set `S_halt` by the doubly-exp reseed orbit (`1/3=(½)/1.5`); the mirror
of Antihydra (thick target ⇒ generic verdict HALT), decidable-in-principle *if* it halts (hitting epoch, doubly-exp
infeasible) but needing **anti-genericity** for non-halt; **(x) Type-IV is a counter-machine** (multi-coordinate vector,
not a scalar reseed — outside BC); **(xi) the log→linear wall is empty of new tools** (CDT / digit-avoidance /
effective-equidist all `(c)`), refined: **Space Needle's all-ones-avoidance is annealed-easier than `(K)` but of
EQUAL provable depth**. Hardness order: {spontaneous-defect convergent = `(K)`-depth, EFF-EQ-reachable} `<` {o10,
BC-II}; Type-IV off-axis. **(xii) Attack A** concretizes the band: 9 spontaneous-defect machines are **uniformly
thin** (0 firings, entry-read always safe) and reduce to **one (UNIFIED EFF-EQ) hypothesis** (§10). **(xiii) Attack
B** (`TYPEIV_DECIDABILITY_2026-07-04.md`): Type-IV, though off the `(K)` axis, is **not independently decidable** —
its `⌈2A/3⌉` floor-multiplier keeps it on the generalized-Collatz wall (empirically Collatz-irregular). **`(K)` /
P1′ remain `[OPEN]` = generational. No machine decided. No label upgraded.**

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
