# The carry-transparency dichotomy — classifying the BB(6) open frontier by what drives the carries (2026-07-11)

*Second weapon from the campaign-wide analysis. Every open core on the frontier is a safety invariant
about a carry/branch sequence; this note classifies each machine by WHAT determines that sequence — a
fully-understood explicit register (carry-TRANSPARENT: decidable-in-principle by the
faithfulness+carry-calculus method) or the residues/digits of an orbit whose distribution is itself the
open problem (carry-OPAQUE: the true (K) wall). The result is the refined complete-proof map: the
transparent set is the actual decidable frontier. STRICT: `[PROVEN]`/`[OBSERVED]`/`[OPEN]`; borderline
cases labeled honestly. Probes: `cd_probe.py`, `cd_probe2.py` (caps 12M/40M, exact
simulation, interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`; census rows JSON in the
session scratchpad, regenerable from `mse_census.py`). **This note decides no
halting and upgrades no label** — it classifies difficulty type, not truth.*

---

## 1. The dichotomy, formalized

Every analyzed frontier machine reduces (with per-machine confidence) to a safety invariant of the
form *"the gate-fatal carry/branch event never occurs."* The classifying question: **what mathematical
object determines the carry/branch sequence?**

**Definition (carry-TRANSPARENT).** The machine's carry/branch sequence is determined by a register
whose update law is an explicit, fully-analyzable map — a pure increment (base-b odometer: carries =
the ruler sequence v_b(n)), a pure doubling/shift `v ↦ 2v+c` (or affine with an explicitly drifting
constant), or a fixed affine map on a bounded state. Then the carry sequence IS explicit mathematics:
every question about it ("is every settled carry gap even?") is a theorem-or-not about a computable,
structured, completely specified dynamical system, **conditioned on no open conjecture**. Such a
machine is *decidable-in-principle*: what stands between it and a decision is proof engineering
(faithfulness of the tape→register abstraction + a carry calculus over the explicit law), not new
mathematics about an unknown distribution.

**Definition (carry-OPAQUE).** The carry/branch sequence is (or depends on) the residue/digit
itinerary of an orbit whose distribution is itself an open problem — the ×(p/q) orbits of the
(K)/Mahler-3/2 type, or a Collatz-type mixed-multiplier orbit. Then the safety invariant **inherits
the open distribution**: any carry calculus over the sequence would have to know the residue
itinerary, and — modulo the machine⟺orbit reduction — an explicit analyzable law for the carries
*would itself resolve* the open equidistribution/avoidance instance. Opacity is exactly the (K) wall
worn as a carry sequence.

**The load-bearing distinction: counter-dependent ≠ opaque.** The x2 record calls its residual
"o4-wall-class" because it resists bounded-window closure just as o4's does. The dichotomy splits
that class in two: o4's counter-dependence bottoms out in the residues of a ×4/3 orbit whose
equidistribution is OPEN (opaque); x2's bottoms out in the reachable configurations of an explicit
base-2 doubling odometer, with no open conjecture underneath (transparent). Both are *hard*; only one
is *conditionally* hard. Transparency is a statement about what kind of theorem is needed, never a
promise that the theorem is easy — the x2 parity/ordering work (`X2_PARITY_ORDERING_2026-07-11`)
shows a transparent residual can still defeat every bounded-radius and uniform-parity attack.

**Edge case.** A machine with no scalar register at all (o17) falls outside the dichotomy; for reach
purposes it sits with the opaque set (there is no explicit register to be transparent about).

---

## 2. The 17 named — 16 OPAQUE, 1 outside the dichotomy `[grounded in the record]`

The classification here is inherited from the PROVEN/grid/observed reductions in the record; no new
computation was needed.

| machine(s) | engine | carry driver | class | grounding |
|---|---|---|---|---|
| Antihydra, o10, o2, o11, o13, o14, o16, o12, o8 | ×3/2 (ℤ₂) | parity itinerary of the ×3/2 orbit = its 2-adic digit stream | **OPAQUE** | run law `v₂(v−x)` [PROVEN, Lean corollaries] (`PAPER_CENSUS §2–3`); protection = `Normality32(seed)` (`MINIMAL_CONJECTURE_SET §2`); o5/o8/o12 reductions [OBSERVED, catalogue] |
| o4, o3, o5 | ×4/3 (ℤ₃) | ρ = G mod 3 of the ×4/3 orbit; runs = `v₃(G−x_ρ)` exactly | **OPAQUE** | o4 [PROVEN, Lean END-TO-END]: the itinerary run law (`O4_RUN_STRUCTURE §1`) makes the carry sequence *literally* the 3-adic return process whose frequency is the open content (§2 ibid.) |
| o15, o18 | ×8/3 (ℤ₃) | `v₃(V−1)` depth of the ×8/3 orbit | **OPAQUE** | `Normality83` instances (`PAPER_CENSUS §3`) |
| o7 | ×3/2 / ×1/2 two-multiplier | parity of a genuine Collatz-type orbit; halt ⟺ orbit hits 2^k | **OPAQUE** (thin-set/B2 subtype) | not (K)-seeded but the branch driver is the orbit's own parity sequence — the archetypal open register (`PAPER_CENSUS §5b`, `TwoPowerAvoidance`) |
| Space Needle | ×5/2, v-indexed odd carry | orbit digits; halt ⟺ 2^k hit | **OPAQUE** (thin-set subtype) | odd branch has no fixed point (`PAPER_CENSUS §3`); `TwoPowerAvoidance(snOrbit)` |
| o17 | none | no scalar register; Nerode index 1,2,6,19,54,132 unbounded | **outside dichotomy** (opaque for reach) | `MINIMAL_CONJECTURE_SET §2` |

The opacity of the 14 NormalityPQ machines is as solid as their reductions (only o4 is Lean
end-to-end; the rest are grid/observed — stated per `PAPER_CENSUS §6`). For o4 the statement is
sharp and unconditional: **the carry sequence and the (K)-type open object are the same sequence**
(the itinerary bijection), so a transparent carry law for o4 would *be* a proof of its
`Normality43` instance. That is the precise sense in which OPAQUE = the wall.

**Named transparent machines: 0.** `[This is expected — the named frontier is the residue of every
decider, i.e. exactly the machines whose carries encode open mathematics.]`

---

## 3. The x2 species (7) + the ~13/7 recruit — the transparent candidates `[OBSERVED probes, cap 12M/40M]`

Probes (`cd_probe.py`, `cd_probe2.py`): exact peak recurrence `v' = 2v + d_k` on settled tails
(trailing incomplete segment dropped), reset-value structure, final-milestone cascade RLE.

| spec | probe findings | class |
|---|---|---|
| `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` (primary) | register law PROVEN pure doubling, `v_k = 2^k−2` explicit; finite-state parity-only routing PROVEN; open residual = carry-gap parity of the explicit base-2 odometer (`X2_FRONTIER_MAP`, `X2_PARITY_ORDERING`) | **TRANSPARENT** `[structural; register law PROVEN]` |
| `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` (twin) | same `2^k−2` block cascade (1-runs 14,30,62,…,1022, ratios → 2.004) | **TRANSPARENT-candidate** `[OBSERVED]` |
| `1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC` (pair A) | maxrun peaks **7·2^k EXACT** (224,448,896,1792,3584; d_k ≡ 0); resets drain arithmetically 26,22,18,14,10 (−4/gen) with a rigid super-cycle refill | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` |
| `1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD` (pair B) | maxrun peaks **3·2^k EXACT** (96,…,3072; d_k ≡ 0); identical reset drain 26,22,18,14,10,6 | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` |
| `1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD` | maxrun peaks **EXACT `v'=2v+1`** (71,143,287,575,1151 = 9·2^k−1); resets CONSTANT 14 | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` |
| `1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE` | period-2 doubling envelope (peaks pair up 609/613, 1239/1237, 2495/2473) but corrections vary non-affinely (+21,+17,+43 / +4,−2,−22) — possible digit coupling | **UNCLEAR** `[OBSERVED]` |
| `1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE` | mixed phases: alternate steps EXACT `d=+5`, the others erratic and value-proportional (−11,−204,−693) — correction plausibly reads deep digits | **UNCLEAR** (opaque-leaning) `[OBSERVED]` |
| `1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---` (was "~13/7") | resets **EXACTLY arithmetic +3/gen** (24,27,…,39); peak ratio rises monotonically 1.878→1.977→2: a ×2 envelope with a linear secondary register. The "~13/7" label is a transient artifact; d_k drift ≈ −3k with residual noise not yet pinned | **TRANSPARENT-leaning UNCLEAR** — reclassified out of "unpinned rational" `[OBSERVED]` |

Honest caveats: (i) except for the primary, these are *observable-level* probes (total1/maxrun as
register proxies), not certified milestone reductions — each transparent-candidate still needs the
primary's treatment (milestone form + value map + halt gate + faithfulness) before its class is
firm; (ii) an exact envelope does not preclude a hidden digit-coupled branch (the primary itself
has data-dependent resets 9/21/31 yet is transparent because the *whole* low-region law is the
explicit odometer); (iii) conversely, the two UNCLEARs may become transparent once the right
register coordinates are found — their "erratic" corrections could be a second explicit register
read through the wrong observable.

## 4. The remaining unpinned candidates (4) `[OBSERVED]`

| spec | probe | class |
|---|---|---|
| `…_1LC1RE_---1LD_…` (~11/7, ratio 1.579 cv 0.10) | monotone growth, no clean reset; q>1 rational engine presumptive | **OPAQUE-presumptive / UNCLEAR** |
| `1RB0RC_1RC---_…` (~7/5; re-probe median 1.34) | drifts near 4/3 — plausibly collapses to the known ×4/3 engine | **OPAQUE-presumptive** |
| `…1LF0RD_---0LE` (~8/5, 1.59 cv 0.15) | stable fractional ratio, growing resets | **OPAQUE-presumptive / UNCLEAR** |
| `…0RC0RF_1RA---` (~23/7, 3.26 cv 0.19) | monotone ~×3.3 growth both peaks and resets; multiplier unpinned | **UNCLEAR** |

If any of these is a genuine ×(p/q) engine with q>1, its carries are mod-q residues of its own orbit
— opaque by the §2 argument, as a new seed-instance of the same schema family.

## 5. The 105 robust collapsed holdouts `[OBSERVED-extractor + sample re-probe]`

All 105 robust collapses (`MILESTONE_EXTRACTOR_V2`: {sawtooth 54, slowgeom 31, transfer 20}) are onto
the q∈{2,3} engines {×3/2, ×4/3, ×8/3} — i.e. onto OPAQUE engines. Sample re-probe (8 drawn, seed 7,
`cd_probe.py` part 3): 3/8 cleanly reconfirm geometric known-engine peaks at 12M with my cruder
segmenter (e.g. `1RB0RB_1LC1RF_…` → 1.3306, cv 0.002 → ×4/3); the rest need the full validated
extractor (which is where the 0-WRONG property lives). Classification: **OPAQUE-presumptive, all
105** — each would need a certified per-machine reduction to firm the label, but every one of them,
if its extraction is faithful, is a new seed of an already-opaque engine. None is a transparent
candidate.

---

## 6. The dichotomy table — the weapon's reach

| population | OPAQUE | TRANSPARENT(-candidate) | UNCLEAR / outside | notes |
|---|---|---|---|---|
| 17 named | **16** (14 NormalityPQ + 2 avoidance) | **0** | 1 (o17, no register) | opacity grounded in PROVEN/grid reductions |
| x2 species (7) + recruit | 0 | **5** (+1 leaning) | 2 | primary = deepest-mapped |
| unpinned candidates (4) | 2 presumptive | 0 | 2 | |
| 105 robust collapsed | **105 presumptive** | 0 | — | seeds of opaque engines |
| rest of 1104 (851 undetected + 46 weak + artifacts) | — | — | unclassified | out of scope of any current probe |

**The transparent target list** (for the faithfulness+carry-calculus decider, in order of map depth):

1. `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` — fully mapped; residual = odometer carry-gap parity
2. `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` — twin cascade
3. `1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC` — 7·2^k exact, −4 reset drain
4. `1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD` — 3·2^k exact, same drain
5. `1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD` — 9·2^k−1 exact, constant reset 14
- watchlist: the ×2+linear machine (`…1LA0LA_1RA---`) and the two UNCLEAR x2 machines.

**Honest reach assessment.** The expectation held: essentially the whole named-and-collapsed frontier
(16 + ~105 + 2) is carry-opaque — that is *why* it is the frontier — and the transparent set is
exactly the integer-×2 species (5 candidates + up to 3 more pending), a ~5-machine island created by
q=1 degenerating the (K) framework. The weapon does not shrink the wall; it draws the wall's exact
boundary and hands the parallel carry-calculus agent a definite, finite target list: if the x2
calculus works on the primary, the same method should sweep machines 2–5 (their laws are *more* rigid
than the primary's), and the two UNCLEARs become the next test of whether the transparent island is
larger than it looks. What the dichotomy proves about the rest is conditional but sharp: any decider
that works on an opaque machine without solving its NormalityPQ/avoidance instance would contradict
the reduction — so decider effort spent there is misdirected by theorem, not by taste.

## 7. Soundness ledger

- Dichotomy definitions: formal but meta-mathematical (classify difficulty type); no halting claim.
- §2 classifications: inherited from the record's reductions at their existing labels ([PROVEN, Lean]
  for o4; grid/observed elsewhere; `PAPER_CENSUS §6` scope discipline applies).
- §3–5 probes: `[OBSERVED, exact simulation]`, caps 12M/40M; exact-tail laws are finite observations
  (4–5 consecutive exact doublings), NOT proofs of the laws; observable-proxy caveat stated.
- Reclassification of "~13/7" as a ×2-with-drift candidate: `[OBSERVED]` (monotone ratio → 2 + exact
  +3 resets); its previous cand-new label was already `[OBSERVED-extractor]` only.
- No borderline case silently resolved: o7/SN opaque-subtype reasoning stated; o17 outside; two x2
  UNCLEARs left unclear.

**No machine decided. No label upgraded.**
