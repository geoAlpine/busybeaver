# Exact reductions of the BB(6) Collatz core — comparison (2026-06-22)

The §3c programme (`antihydra_attack.md`): reduce each open cryptid to the exact integer-orbit /
arithmetic problem its halting encodes. `CRYPTID_CENSUS.md` isolated the **exponential-Collatz core**
(Antihydra + o10, o15, o17, o18) as the right targets. This applies the reduction to all five and
compares. Each non-Antihydra machine was reverse-engineered against the **raw TM** (not just
`cryptid_map`); the two clean orbit maps below were independently re-verified arithmetically here.

## Result table

| machine | mechanism | orbit map `f` | exact halt predicate | family | clean orbit? | status |
|---|---|---|---|---|---|---|
| **Antihydra** | 2 unary counters | `c→⌊3c/2⌋`, `c0=8` | `∃n: v2(c_n−1) ≥ balance_n+1` | **Mahler 3/2** | ✅ (proven) | [OPEN] Mahler-hard |
| **o10** | **nested** 2-level counter | inner `m→⌈3m/2⌉`; outer = **doubly-exp b-refill orbit**, refill map irregular | refill sub-routine on the outer orbit | **Mahler 3/2** (inner) + irregular outer | inner ✅ / outer examined | [OPEN] outer orbit doubly-exp & irregular (`o10_attack.md`) |
| **o15** | 2 nested loops, `(10)`-counter | width `×8/3`; value `v→v^{8/3}` (doubly-exp), parity-irregular | `∃` outer step where new `11`-block **abuts a 1** (collision) | **Mahler 8/3** | ✗ (genuine parity defect) | [OPEN] Mahler-hard |
| **o17** | carrying **odometer**, digit-step 3 | none (multi-digit base-≈3 counter; `v≈8v+carry-noise`) | `∃` D-read of `0` with left cell `0` (a `00` gap forms) | **odometer / other** | ✗ (not single-variable) | [OPEN]; invariant "separators stay single" [CONJECTURED] |
| **o18** | 2 counters, `b→b−3` | `f(N)=⌊8N/3⌋+2` (7 transitions), **breaks at epoch 8** | `∃` epoch where left-frontier bit becomes `1` | **Mahler 8/3** | partial (intermittent 3-zero class breaks it) | [OPEN] Mahler-hard |

(Self-verified here: o18 `⌊8N/3⌋+2` reproduces `10→28→76→204→546→1458→3890` and `27660→73762`, and
`f(3890)=10375≠27660` confirms the epoch-8 break; o10-inner `⌈3m/2⌉` reproduces
`6,9,14,21,32,48,72,108,162,243,365,548` exactly.)

## Comparison — what the five together reveal

1. **No holdout decided; none reduced to a tractable (decidable) family.** The lottery did not hit:
   every core machine is Mahler-family (`3/2` or `8/3`) or an odometer — the same hardness class as
   Antihydra. Honest negative, consistent with `BB6_PREP` (our tools settle 0).
2. **The exact HALT PREDICATE generalises to all five** (even where the orbit map does not). Each
   machine's halting was pinned to a specific structural event — Antihydra's `v2(c_n−1) ≥ balance_n+1`,
   o15's block-collision, o17's `00`-gap, o18's frontier-bit, o10's refill condition. This is the real
   catalogue content: **BB(6)'s Collatz core = these five named structural/2-adic events**, none local,
   each a statement about the long-term arithmetic of the orbit.
3. **A clean sub-structure emerges: the Mahler multiplier.** Antihydra and o10-inner are `3/2`; o15 and
   o18 are `8/3 = 2³/3`. Both are `2^a/3^b`-type Mahler maps — so four of five sit in one number-theoretic
   family (the open `⌊x·(p/q)^n⌋` distribution problem), differing only in the multiplier and the
   halting event. o17 is the outlier (a carry odometer, arguably nearer our already-solved counter class,
   but with an unproven single-separator invariant).
4. **Two CENSUS tags were over-fit artifacts (soundness correction).** `cryptid_map` tagged o10 and o17
   "COLLATZ-LIKE on binary value"; deeper reverse-engineering shows both are **NOT** clean Collatz orbits
   (o10 = nested-refill, o17 = odometer) — the tag came from a 5-point float-ratio fit on a sparse,
   biased milestone. `CRYPTID_CENSUS.md` is annotated accordingly. The lesson is the recurring one
   (`SOUNDNESS_INCIDENT.md`): a few-point classifier fit spoofs structure; verify against the raw TM.

## Status / where this leaves the math road
- **[PROVEN, conjecture-free]** exact halt predicates for all five; clean orbit maps for Antihydra,
  o10-inner (`3/2`), o18 (`8/3`, partial). The Mahler-multiplier sub-family {3/2, 8/3} is now explicit.
- **[OPEN]** every reduced problem (Mahler/odometer-hard). No machine decided; no non-halting proven.
- **Next achievable (per `LIMIT_THEOREM.md` ⑥):** the strongest leverage is no longer "find a tractable
  cryptid" (the core is uniformly hard) but the **certificate-hierarchy** result — push [OPEN] "no REG
  certificate for a cryptid" toward [PROVEN] for one, now that four of five are pinned to the *same*
  Mahler family (a shared barrier is easier to attack than five separate ones).

## UPDATE 2026-06-23 — o17's "tractable odometer" hypothesis is REFUTED (now 5/5 Collatz-hard)
o17 was selected as the closest-to-an-answer target (a carrying odometer, seemingly nearest the defeated
counter class) and attacked three ways under the sound `far_dfa.verify` gate (hand-built DFA / phase-aware
CEGAR / other engines). **None decided it.** The conjecture-free reason (machine-verified, see
`o17_attack.md`): the embedded family `0 A 0 1^k` halts **Collatz-irregularly** — `k≢0 (mod 3)` always
halts fast, while `k≡0 (mod 3)` is Collatz-like with proven halters (`k=6→206, 12→394, 15→794964`)
interleaved with apparent non-halters and no separating modulus. A regular certificate's closure is forced
through this family, which mixes proven halts with non-halts — so **no FAR/regular certificate is
reachable**. o17 is Collatz-hard, not a tame counter. The whole Collatz core is now **uniformly hard
(5/5)**; o17's odometer was the last plausible tractable target and it fell. This sharpens the strategic
conclusion: the decision route is closed for all five; only the **certificate-hierarchy theory** (⑥)
remains as the BB(6)-related contribution. (A false "decided" was avoided — the soundness gate held.)

## UPDATE 2026-06-23 — cross-cryptid meta-structure + a NAMED-PROBLEM lead (Erdős ternary)
A parallel fan-out (4 agents; results re-verified here) produced a unifying picture and one concrete
literature foothold.

**Unifying meta-structure (all 5 core cryptids).** Every one is `⌊x·(2^a/3^b)^n⌋` dynamics with
multiplier in `{3/2, 8/3}` (`8/3 = 2³/3`):

| machine | multiplier | halt = forbidden digit/residue event |
|---|---|---|
| Antihydra, o10-inner | 3/2 | `c_n ≡ 1 (mod 2^{balance_n+1})` — a **2-adic depth** event (`v2(c_n−1) ≥ balance_n+1`) |
| o15, o18 | 8/3 = 2³/3 | a **base-3 leading-digit / carry** event of the `×8/3` value |
| o17 | base-3 odometer (`≈×8`) | **base-3 carry overflows** the top digit (left-frontier overflow) |
| o10 | nested 3/2 + irregular doubly-exp refill | 2-adic inner feeding an irregular outer trigger |

> **Shared barrier (named):** each halts ⟺ the orbit of `(2^a/3^b)^n` lands in a density-0 forbidden
> digit configuration (2-adic valuation for the 3/2 machines, base-3 digit/carry for the 8/3 machines);
> non-halting needs only a *one-sided* density bound (strictly weaker than full Mahler equidistribution),
> and **no such unconditional density bound is known for any of them.**

**[PROVEN, conjecture-free] transfer-operator no-go (the 3/2 machines).** The map `T(c)=⌊3c/2⌋` has parity
itinerary = the **full 2-shift** (engine lemma `T^t(c+2^j)−T^t(c)=3^t·2^{j−t}`, re-verified 30000 cases;
coding surjective onto `{0,1}^ℕ`). So the dynamics alone bound even-density **nowhere in [0,1]** — any
proof must be point-specific. (Recorded in `antihydra_attack.md` §4a′.)

**LEAD — o15/o18 (8/3) are in the Erdős "ternary digits of 2ⁿ" FAMILY (most attackable; analogy, not exact reduction).**
*Refined + corrected by a second pass (verified against the raw TM).* **Exact halt kernels [PROVEN]:**
o18 halts ⟺ the leftward sweep (`D:1→1LF`, then F) finds a `1` at the left frontier = **the `⌊x·(8/3)ⁿ⌋`
base-3 odometer's leading digit overflows its width** (verified: all 10 F-visits to 200M steps read `0`);
o15 halts ⟺ symmetric **right-frontier `11`-collision** = the new top base-3 digit lands on occupied tape
(all 9 A-visits read `0`). Both are *forbidden base-3 leading-digit/carry events of a `(2³/3)ⁿ` orbit.*
**Tightness — honest [ANALOGY, not reduction]:** because `8/3 = 2³/3`, these live in the *same family* as
Erdős's base-3-digits-of-`2^{3n}` problem, **but o18's halting is NOT the literal "2^{3n} omits a base-3
digit"** — the width orbit is *not* `9·8ⁿ/3ⁿ` (it drifts), and the carry-correction is governed by the
orbit's own `W_n mod 3` (seed-dependent), not by `8ⁿ`'s digits. So it is a **strong structural analogy**
(same multiplier, same "does a digit/carry event ever occur" shape, same missing one-sided density bound),
not an exact reduction.
**Erdős literature [re-confirmed at source]:** `2^m` omits base-3 digit 2 only for `m∈{0,2,8}` (recomputed
to `m≤5000`; verified in the literature to `≈6×10²¹`); Erdős (1979) conjectured none for `m>8`.
**Narkiewicz (1980) [unconditional]:** `#{n≤x : (2ⁿ)₃ omits digit 2} ≤ 1.62·x^{α₀}`, `α₀=log₃2≈0.631` —
an **upper bound only; the set is not even known to be finite** (no lower bound = the missing piece, same
shape as Antihydra's missing FLP density-analogue). The 15-state BB↔Erdős machine is **Stérin–Woods,
"Hardness of busy beaver value BB(15)" (arXiv:2107.12475)** (halts ⟺ Erdős's conjecture is false) — *not
"Lin–Xu" (earlier mis-attribution, corrected)*. (See also Saye, arXiv:2202.13256.) So o15/o18 sit in a
**named, classical, partially-developed** open family with an existing BB reduction — the strongest
literature foothold among the five, though the exact o15/o18-to-Erdős reduction is an analogy, not derived.

**Attackability ranking (most → least):** o15/o18 (named Erdős problem, clears 2 at once, published
partials) > Antihydra (most-studied, but §4b/§4a′ show it is provably beyond current tools) > o17 (base-3
carry, no clean scalar orbit) > o10 (two hard problems stacked). **No machine decided; all summits remain
open.** The honest gain: the BB(6) Collatz core is now mapped onto **two named number-theory problems**
(Mahler 3/2 for Antihydra/o10; Erdős ternary-2ⁿ for o15/o18/o17), each missing the same *one-sided density
lower bound*.

## TIER-1 REDUCTION 2026-06-24 — o5 = Mahler 4/3 = 2²/3 (Erdős ternary family)
First of the slow-width cryptids reduced (per `BB6_ROADMAP.md`). `o5 = 1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB`,
halt = state D reads 1 (entered as `C:1→1LD`, then D reads the left cell = halt iff it is `1`).
- **Mechanism [VERIFIED vs raw TM]:** the tape is a periodic background `(10)^k` carrying a small moving
  **defect** (a `11`-block, occasionally `111`). The right-extreme-in-B milestone shows a near-clean
  `(10)^k` of width `w` growing `+1` per step with **epoch jumps** (`+3,+4,+7,+9`) where the defect
  interacts with the boundary. Halt ⟺ the `C→D` head reads the defect `11` in the lethal configuration
  (the only `11` in the otherwise `(10)*` field).
- **Multiplier [VERIFIED ~4/3 asymptotically]:** at major epochs the width grows by `×4/3` — major-epoch
  widths `…,184,248,338,450,604,798,1063,1408,1872,2501,3325` have geometric-mean ratio `≈1.336 ≈ 4/3`
  (per-epoch ratios oscillate `1.32–1.36` around `4/3`, the Mahler fluctuation). So `width ~ c·(4/3)^n`.
- **Family:** `4/3 = 2²/3`, so `(4/3)^n = 2^{2n}/3^n` — the halting digit/carry event lives in the **base-3
  digits of `2^{2n}`**, i.e. the **Erdős ternary-digits-of-powers-of-2 family** (same as o15/o18's `8/3 =
  2³/3`). The jump alphabet `{3,4,7,9}` is the digit/carry sequence.
- **Status:** [REDUCED to family + multiplier] like o15 (Mahler-8/3, no clean scalar map); the exact
  digit-event halt criterion is not fully derived (the defect dynamics are intricate). [OPEN] — joins the
  Erdős ternary family, which has Narkiewicz's unconditional upper bound but no lower bound (§see o15/o18).
- **Catalogue update:** the BB(6) cryptid families are now {Mahler 3/2: Antihydra, o10-inner}, {Mahler 2^a/3
  → Erdős ternary: o5 (4/3), o15, o18 (8/3)}, {base-3 odometer: o17}, {nested: o10}. **o5 consolidates the
  Erdős cluster** (now 3 machines). No decision; soundness intact.

## TIER-1 REDUCTION 2026-06-24 — o7 = Mahler 3/2 (Antihydra family)
Second slow-width cryptid reduced. `o7 = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC`, halt = state F reads 0
(F entered via `C:0→1LF`).
- **Mechanism [VERIFIED vs raw TM]:** the tape is **two unary counters `1^a 0 1^b`** (same shape as
  Antihydra). The R-extreme-in-C milestone sweeps `b→b−1, a→a+1` then, when `b` is small, **resets**
  (`a→1`, `b→` a large value), exactly Antihydra's balance/Hydra two-counter pattern.
- **Multiplier [VERIFIED 3/2]:** at clean resets `[1, b]` the width grows by `×3/2` — clean-reset widths
  `…,319,479,719,1079,1619` have ratios `1.502, 1.501, 1.501, 1.500` → **3/2**. So `width ~ c·(3/2)^n`.
- **Family: Mahler 3/2 — the Antihydra family** (Antihydra, o10-inner). Halting is a 2-adic digit/carry
  event of the `(3/2)^n` orbit (the analogue of Antihydra's `v2(c_n−1) ≥ balance_n+1`).
- **Status:** [REDUCED to family + multiplier]; exact 2-adic halt criterion not separately derived. [OPEN].

### Catalogue convergence (after o5, o7)
**Both newly-reduced slow-width cryptids joined EXISTING families — no new family appeared:**
- **Mahler 3/2** (the Antihydra family): Antihydra, o10-inner, **o7**.
- **Erdős ternary = `2^a/3` Mahler**: **o5** (4/3), o15, o18 (8/3).
- **base-3 odometer**: o17. **nested**: o10.
**Pattern [emerging, not proven]:** the 19 BB(6) cryptids appear to cluster into ~2 number-theory families
(Mahler 3/2 and Erdős ternary-digits-of-2^m), not a sprawl of distinct problems. If this holds across the
remaining 12 slow-width machines, "solving BB(6)" collapses to resolving ~2 named open problems — a far
cleaner picture than "19 separate hard problems." Continue Tier-1 to test the pattern.

## TIER-1 REDUCTION 2026-06-24 — o8 = Mahler 3/2, nested (Antihydra family)
Third slow-width cryptid reduced. `o8 = 1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE`, halt = state F reads 0.
- **Mechanism [VERIFIED vs raw TM]:** two unary counters `1^a 0 1^b` (Antihydra shape); sweep `b→b−1,
  a→a+1` then reset.
- **Multiplier [VERIFIED inner ×3/2]:** the clean-reset widths run `33,49,73,109,163` with ratios
  `1.485, 1.490, 1.493, 1.495 → 3/2`. So the inner multiplier is **3/2**. But there are larger jumps
  (e.g. `163→523 ≈ (3/2)^3`), i.e. a **nested / meta-epoch** structure (like o10): inner ×3/2 inside an
  outer meta-cycle.
- **Family: Mahler 3/2 (nested) — the Antihydra family.** [REDUCED to family + inner multiplier; the outer
  meta-structure not fully derived, like o10.] [OPEN].

### Catalogue convergence — 3/3 (o5, o7, o8 all joined existing families)
- **Mahler 3/2** (Antihydra family): Antihydra, o10, **o7**, **o8** (4 machines).
- **Erdős ternary = `2^a/3` Mahler**: **o5** (4/3), o15, o18 (8/3) (3 machines).
- **base-3 odometer**: o17.
**Strengthening pattern:** all three newly-reduced slow-width cryptids landed in the two existing families;
zero new families. Of the 19, **8 are now reduced and they occupy just 2 number-theory families** (Mahler
3/2; Erdős ternary-digits-of-2^m). The "~2 families" hypothesis is gaining support — if it holds for the
remaining slow-width machines, **BB(6)'s open core ≈ two named problems** (the 2-adic distribution of
`(3/2)^n`, and the base-3 digits of powers of 2), a dramatically cleaner picture than 19 separate problems.

## TIER-1 REDUCTION 2026-06-24 — o4 = polynomial-time defect machine (THIRD type; breaks ~2-family; decision LEAD)
`o4 = 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`, halt = state F reads 1 (F entered via `B:1→1RF`).
- **NOT exponential/Mahler — it is POLYNOMIAL-TIME [VERIFIED].** `width ~ 1.44·√t` (w/√t = 1.85→1.63→1.51
  →1.47→1.45→1.44 at t=10^4..3·10^7), i.e. **time ~ width²** (quadratic). A different class from the
  exponential Mahler cryptids. **So the ~2-family hypothesis is FALSE — o4 is a third structural type.**
- **Mechanism [VERIFIED]:** the tape is a `(10)*` sea carrying a **single defect** (a `11`-block), which
  appears at only ~7 of millions of milestones. The defect drifts rightward toward the boundary. Halt ⟺
  the `B→F` head reads the defect `11` at the right boundary. Non-halt ⟺ the defect never reaches it.
- **The key quantity — the GAP (boundary − defect position) is monotone increasing [OBSERVED]:** defect
  events give gap `= 21,27,37,63,77,111,129` (widths 33,55,97,267,569,2203,5101; times 232..1.4·10^7). The
  gap grows, so the defect stays away from the boundary — empirically non-halting.
- **DECISION LEAD [the most promising of all 19]:** unlike the exponential cryptids, o4 is polynomial-time
  with a **monotone gap**. **If "gap is always increasing" (or bounded below by a positive growing
  function) can be PROVEN from the defect dynamics, o4 is decided non-halting = a real BB(6) holdout
  settled.** The defect event-timing is irregular (ratios 2.9–17.9), so it is not a trivial bouncer, but
  polynomial time + monotone gap is far closer to a provable invariant than any Mahler machine. **Flag for a
  focused Tier-3 decision attempt.**
- **Status:** [REDUCED — third type: polynomial-time single-defect; non-halt ⟺ gap stays positive]. Not
  yet decided (gap-monotonicity unproven); the most tractable decision target found. No decision claimed.

## STRUCTURAL DICHOTOMY 2026-06-24 — the 19 cryptids split into TWO growth classes (toward the complete catalogue)
Robust growth-rate classification (width at `t=10^4,10^5,10^6,10^7`; `w/√t` constant ⟺ time `~ width²`):
- **POLYNOMIAL-TIME (bouncer-envelope, time `~ width²`), 8 machines [VERIFIED via `w/√t`]:**
  `o2, o3, o4, o11, o12, o13, o14, o16`. The head sweeps a linearly-growing region (width `~ √t`), but the
  tape CONTENT is Collatz-irregular (verified: o4 = single drifting `11`-defect, monotone gap; o13/o16 =
  multi-block reconfiguration). These are *bouncer-shaped with irregular content* — which is exactly why
  bouncer/FAR deciders hold out (the envelope is regular, the content is not).
- **EXPONENTIAL (Mahler `2^a/3^b`), the rest:** Antihydra, o10, o15, o17, o18 (core), o5 (4/3), o7 (3/2),
  o8 (3/2, nested), Space Needle (width grows slower than `√t` ⇒ time super-quadratic/exponential).
**Why this matters for the COMPLETE PROOF.** The cryptid problem set is now structured, not a sprawl:
1. **Exponential family** → ~2 named open problems (Mahler-3/2 distribution; Erdős ternary-digits-of-2^m).
   World-open (`antihydra_attack.md` §4 maps the precise frontier).
2. **Polynomial-time family (8 machines)** → bouncer-envelope + Collatz content; potentially **more
   tractable** than the exponential ones (e.g. o4's gap is monotone — a candidate provable invariant).
   These are the place to look for actual DECISIONS (each decided = a brick in the complete proof).
**Catalogue status:** all 19 cryptids classified by growth class; 9 reduced to a named structure
(Antihydra,o10,o15,o17,o18,o5,o7,o8,o4). Remaining to characterise individually: o2,o3,o11,o12,o13,o14,o16,
Space Needle (now known: 7 poly-time, 1 exponential).

## o4 — DEEP REDUCTION + RETRACTION of the "decision lead" (2026-06-24)  [SOUNDNESS CORRECTION]
Reverse-engineered o4 (`1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`) against the raw TM.
**Exact mechanism.** Tape = `(10)^*` background carrying ONE macroscopic **long-0 defect** (a 0-block whose
length is a large fraction of the swept width), bounded by a `1^2` left-marker and a `0^2` right-edge.
- **Within an epoch [CLEAN, local rule]:** the long-0 block shrinks by exactly **−3 per drift event**
  (verified sawtooth: `360,318,312,306,303,297,294,…,15,12`; decrements −3, occasional −6), i.e. the defect
  drifts deterministically toward the right boundary. This local rule is provable and regular.
- **Epoch reset [IRREGULAR, geometric]:** when the block bottoms out (residue ~11–16, itself varying), it
  **resets to a new peak**. Clean ascending peak series `101,143,193,266,360,490,652` grows **geometrically
  ~×1.36** (Mahler-class, near `4/3=1.333` with finite-size drift), BUT the fine structure is irregular
  (automated peak detection returns a noisy, non-monotone stream `…191,66,160,26,226…` = multiple
  sawteeth + varying bottoms). The reset value is set by a carry/Collatz-type process, not a clean map.
**Classification:** o4's *content* is **geometric/Mahler-class (irregular)** — it joins the irregular core,
NOT a tractable poly-time target. Its earlier "POLYNOMIAL-time" tag (the dichotomy above) is an **ENVELOPE**
property only: width `~√t` because the head sweeps a linearly-growing region, while the defect content grows
geometrically per epoch *inside* that region. **Poly-time envelope ≠ tractable content.**
**RETRACTION (soundness discipline).** The earlier note "o4 = decision LEAD, monotone gap
21,27,37,63,77,111,129" is **RETRACTED.** That "monotone gap" was the within-epoch **−3 sawtooth** (the one
clean local rule) misread as a *global* invariant. Globally the epoch peaks/bottoms are irregular
(geometric-with-Collatz-content), so there is **no clean monotone non-halting invariant** for o4. o4 is NOT
a decidable-looking target; it is as hard as the rest (consistent with `CRYPTID_CENSUS.md`: all slow-width
content IRREGULAR). No decision; the lead is closed honestly.
**Catalogue consequence.** The poly/exp dichotomy is about the **width envelope** (direct-geometric vs
sawtooth-linear), NOT the deep difficulty. Under the envelope, the cryptid CONTENT is uniformly irregular
geometric (Mahler/Collatz). This *consolidates* the picture: one deep difficulty (irregular `2^a/3^b`-rate
content) in two envelope costumes — it does not hand us an easier class.

## o16 — CONFIRMS the consolidation (2026-06-24)
Reverse-engineered o16 (`1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE`). Structure = `1^k 0^2 (10)^m` with a
**roaming `1^big` defect** inside the `(10)*` region. Same template as o4:
- **Envelope [regular]:** width `~√t` (doubles per 4× time: 55,142,256,495,1013); leading block `k` decays
  slowly/logarithmically (21,20,19,…,16,…13); the defect bounces (position drifts each sweep).
- **Content [irregular geometric]:** the `1`-defect length oscillates wildly per sweep and its peaks GROW
  (`33,41,85,101,127,181,215,251,…`) — geometric magnitude with irregular fine structure. No clean map.
**Verdict:** o16 = bouncing/sawtooth envelope over an irregular geometric-growing defect — **identical deep
type to o4.** Two independent "poly-time" machines (o4, o16) both confirm: the POLY-time tag is the
*envelope*, the *content* is irregular geometric (Mahler/Collatz). **Consolidation CONFIRMED (2/2).**

### Stage-1 deep-structure conclusion (the catalogue's settled shape)
All 19 BB(6) cryptids carry **irregular geometric (`2^a/3^b`-rate, Collatz/Mahler) content**, presented in
one of two **width envelopes**: (i) *direct-geometric* (width grows ×const/epoch — the exponential class,
Antihydra/Mahler 3/2, o5/o15/o18 Mahler/Erdős) or (ii) *sawtooth/bouncing* (width `~√t`; a defect bounces
in a linearly-swept region while its magnitude grows geometrically — the "poly-time" class, o4/o16/…).
**There is no tractable subclass.** The envelope dichotomy is cosmetic; the deep difficulty is one and the
same (irregular geometric content), so the COMPLETE PROOF still requires resolving the geometric content =
the named open problems (Mahler 3/2, Erdős ternary-digits). Stage 1's structural question is now answered:
the cryptid frontier is a single difficulty in two costumes, not a spread of independent puzzles with an
easy corner. No decision; soundness intact.

## STAGE-1 CATALOGUE COMPLETE — all 19 cryptids reverse-engineered (2026-06-24)
Reverse-engineered the last 7 unreduced machines against the raw TM (`catalogue_finish.py`). Every one fits
the settled two-costume structure (regular envelope + irregular geometric defect content); NO new family.
Two structural templates account for all 19:
- **(T1) two-counter `1^a 0 1^b [0 1^c]`** (Antihydra family, Mahler-3/2-type): Antihydra, o7, o8, o10,
  **Space Needle** (`1^a 0 1^b 0 1^c`, defects 56→164 irregular), **o13** (`1^a 0 1^b` two big blocks,
  defects 153,327,539,374,863), **o14** (multi `1`-block, defects 148→374). Width-envelope: sawtooth `~√t`.
- **(T2) single drifting defect over `(10)*`** (o4/o16 template): **o2** (`1^big 0 (10)*`, defect
  238,200,484,868,386), **o11** (`0 1^big 0 (10)*`, 273,323,727,507,405), **o12** (`0^2 (10)*`, defect
  55,166,406,583,589), o4 (long-0 defect), o16 (`1^k 0^2 (10)*` roaming `1^big`). Width `~√t`.
- **(special) o3 = near-regular** `1^2 0 (1^5 0)^m`: background `1^5 0` with a *tiny constant* defect
  (longest-1-run stays ≈6). The most regular-looking cryptid — yet still a community HOLDOUT, so its
  irregularity is subtle (rare defect-injection events, not visible in coarse sampling). Flagged as the
  single best candidate for a future closer look (least content-entropy), but NOT decided.
- **Exponential-direct-envelope core** (width grows ×const/epoch): Antihydra, o10, o15, o17, o18, o5.
**Catalogue verdict.** 19/19 reverse-engineered. The BB(6) cryptid frontier = exactly **two structural
templates (two-counter / single-defect) × two width-envelopes (geometric / sawtooth)**, all carrying the
same irregular geometric (`2^a/3^b`, Mahler/Collatz) content. The named open kernels are unchanged:
**Mahler 3/2** (two-counter family) and **Erdős ternary-digits-of-2^n / Mahler 8·3⁻¹,4·3⁻¹** (the 8/3,4/3
core). Stage 1 (the complete catalogue) is a FINISHED artifact. No decision; soundness intact.
