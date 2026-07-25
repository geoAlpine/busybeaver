# ATTACK #18 — premise-complement mining, FIRED (2026-07-25)

The last unfired `(K)` generator.  `ATTACK_CATALOG_2026-07-24.md`'s audit note required that when
`#18` is fired, **the dismissal reasons in §V-33…47 must themselves be re-examined as premises** —
several were snap judgements made when the catalogue was first written.  Done.

## The method

For each no-go layer `L` with premise `P(L)`, form the complement `¬P(L)` and ask what would have to
be true.  Classify the complement as (i) already refuted, (ii) equivalent to `(K)`, or
(iii) **genuinely untried and cheap**.  Two complements came out (iii).  Both were fired.

## PROBE A — the subword complexity of 43's itinerary  →  premise CONFIRMED

Layers 2/5/6/11, and dismissals #33 (Gowers), #34 (nonstandard), #40 (continued fractions), all
presuppose that the orbit carries **no low-complexity structure**.  That premise had never been
measured.  If the itinerary `ρ_j = G_j mod 3` had linear factor complexity (Sturmian-like) or were
`k`-automatic, `φ` would be computable outright and `(K)` would be the wrong diagnosis.

`attack18_premise_probes.py`, itinerary of seed 43, `N = 4·10⁵`:

| n | p(n) | 3^n |
|---|---|---|
| 1…9 | **3^n exactly** | 3^n |
| 10 | 58 976 | 59 049 (sampling-limited at `N = 4·10⁵`) |

**Every word of length ≤ 9 over `{0,1,2}` occurs — full 3-shift complexity.**  Symbol frequencies
`0.3332 / 0.3334 / 0.3333`; `φ(43) = 0.33386`.

> The complement is **refuted by measurement**: the itinerary is not automatic, not Sturmian, not
> low-complexity.  This converts the §V dismissals of the low-complexity family from snap
> judgements into **measured facts**, which is exactly what the audit note asked for.

## PROBE B — is the `φ = 1` obstruction confined to periodic points?  →  sharpens layer 1

Layer 1 kills seed-uniform bounds with the counterexample `−14` (`φ = 1`), which is a **fixed
point**.  Complement: if every high-`φ` integer seed is eventually periodic, then
"aperiodic integer seed ⟹ `φ < 4/5`" is a **different** target statement that `−14` does not refute.

First sweep (seeds `−60 … 120`, 181 seeds): **exactly one seed has `φ > 0.60` — `−14`, `φ = 1.0000`,
and it is periodic.  Zero aperiodic high-`φ` seeds.**  A `±2·10⁵` sweep is running.

**Honest reading.**  Even if the exceptional set inside `ℤ` is exactly the periodic points, proving
"aperiodic ⟹ `φ < 4/5`" is still a statement about specific orbits, and layer 2's multifractal
machinery lives on the completion where every countable set — including all of `ℤ` — has measure
zero.  So the complement **does not escape `(K)`**.  What it does is sharpen layer 1: the
seed-uniformity obstruction is (measurably) confined to a characterisable set rather than being
generic.

## Verdict on #18

**Fired; no new live attack produced.**  That is a legitimate outcome for a generator, and it has
two consequences worth recording:

1. **The `(K)` side now has zero unfired generators.**  #16, #17, #21, #19, #20, #22, #30 and the
   o17 frontier probe were all fired earlier; #18 was the last.
2. **Several §V dismissals are no longer snap judgements** — the low-complexity family is refuted by
   direct measurement of the factor complexity, which is a stronger and auditable footing.

**No machine decided. No label upgraded.**
