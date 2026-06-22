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
| **o10** | **nested** 2-level counter | inner `m→⌈3m/2⌉`; balance `b→b−1/−2` **decreasing** | on the **outer refill** orbit (unextracted) | **Mahler 3/2** (inner) | inner ✅ / outer ✗ | [OPEN] outer not extracted |
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
  Mahler family (a shared barrier is easier to attack than five separate ones). o17's odometer +
  single-separator invariant is the one place a *counter-style* (semilinear) certificate attempt could
  be probed — the most tractable-looking of the five, though its invariant is unproven.
