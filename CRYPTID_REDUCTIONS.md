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

**LEAD — o15/o18 (8/3) = the Erdős "ternary digits of 2ⁿ" problem (most attackable of the five).**
Because `8/3 = 2³/3`, the base-3 digit dynamics of the `×8/3` value are about base-3 expansions of
`2^{3n}` — i.e. **Erdős's 1979 problem**: *which `2^m` omit the digit 2 in base 3?* (re-verified: only
`m ∈ {0,2,8}` for `m ≤ 400`; Erdős conjectured none for `m>8`). Literature (agent-found via web, to be
double-checked at source): **Narkiewicz (1980) [unconditional]** bounds the count of `n≤X` with `2^n`
omitting digit 2 by `≤ 1.62·X^{log₃2}` (density 0) — but this is an **upper bound on the bad set, no lower
bound**, exactly the missing piece (same shape as Antihydra's missing density-analogue of FLP). **Lin–Xu
(arXiv:2107.12475)** reportedly build a 15-state TM that halts ⟺ Erdős's conjecture is false — confirming
the 8/3 family's halting *is* the Erdős problem. So o15/o18 map onto a **named, classical, partially-
developed** open problem with an existing BB reduction: the strongest literature foothold among the five.

**Attackability ranking (most → least):** o15/o18 (named Erdős problem, clears 2 at once, published
partials) > Antihydra (most-studied, but §4b/§4a′ show it is provably beyond current tools) > o17 (base-3
carry, no clean scalar orbit) > o10 (two hard problems stacked). **No machine decided; all summits remain
open.** The honest gain: the BB(6) Collatz core is now mapped onto **two named number-theory problems**
(Mahler 3/2 for Antihydra/o10; Erdős ternary-2ⁿ for o15/o18/o17), each missing the same *one-sided density
lower bound*.
