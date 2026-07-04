# Grand synthesis — one floor-multiplier object, one thin-target reachability, one master tool (2026-07-04)

*Capstone of the 2026-07-04 arc. The session's threads — the tetrachotomy→dichotomy projection
(`BB6_TYPE_IV_CENSUS`), the EFF-EQ leverage map (`P1PRIME_EFFEQ_LEVERAGE`), the non-affine unification
(`CRYPTID_NONAFFINE_UNIFICATION`), the o17 skew product / o3 structure (`O17_SKEW_PRODUCT`, `O17_O3_STRUCTURE`),
the o10 apex (`O10_APEX`), and the P1′ core characterization — collapse into **one picture**: every BB(6) cryptid
is a **floor-multiplier `⌊(p/q)·⌋` orbit**, every halt is **reachability of a target config**, and the target's
**thinness grades the difficulty** so that a **single master tool** (single-orbit equidistribution of the
floor-multiplier) resolves all but the lone thick-target outlier `o10`. SOUNDNESS: `[ARGUED]` synthesis over
`[PROVEN]`/`[OBSERVED]` components; halting `[OPEN]` for all; no machine decided.*

## The three-line picture
> **1. One object.** Every cryptid runs a **non-affine floor-multiplier `⌊(p/q)·⌋` update** (verified this
> session): a **value** for Type I (`⌊3c/2⌋,⌊8c/3⌋,⌊4c/3⌋`), a **scalar counter** for Type III (Space Needle
> `f(m)=m+3⌊m/2^{v+1}⌋+v`), a **fixed-arity counter vector** for Type IV (H5 `⌈2A/3⌉`), a **carry cascade** for
> Type II (o3 length-transfer, o17 base-3 carry). The `⌊(p/q)·⌋` ratio **varies with the 2-adic/3-adic data** —
> that non-affinity is why no bouncer/VASS decider catches them (`CRYPTID_NONAFFINE_UNIFICATION`).
>
> **2. One halt-form.** Every halt is **reachability of a target config** on that orbit: `B1` Antihydra = balance
> `B_n<0` ever; `III` Space Needle = orbit becomes all-ones `2^k−1`; `II/IV` o3/o17/H5 = a `00`/`11` defect
> appears; `I-nested` o10 = a reseed lands in a density-`⅓` set. There is no separate "equidistribution wall" and
> "reachability wall" — **B1's halt is a reachability event too**; the walls differ only in the target's thinness.
>
> **3. One master tool, thinness-graded.** The difficulty is set by **how thin the halt target is**:

| target thinness | cryptids | resolved by | direction |
|---|---|---|---|
| **thin / spontaneous-defect** (density → 0) | Antihydra, o2/o7/o11/o12/…, Space Needle, o3, o17, H5 | **single-orbit equidistribution of the floor-multiplier** (BC-I: thin ⇒ avoided ⇒ non-halt) | non-halt generic |
| **thick / generic-event** (density ⅓, constant) | **o10 alone** | **BC-II / pair-correlation** (harder than `(K)`; the apex) | halt generic |

**So a single tool — single-orbit equidistribution of the floor-multiplier — resolves the non-halt of the ENTIRE
thin-target frontier at once** (all of B1 + all convergent B2), scalar for the value/scalar cryptids and a
**multi-dimensional** variant for H5's counter vector. Only **o10** (thick target, generic-HALT, the mirror of
Antihydra) sits outside, needing BC-II.

## Why this is the same object as (K), EFF-EQ, and the Gauss-map analogue
The master tool is exactly the missing tool `P1′`, now seen to have **frontier-wide** reach:
- as **(K) / Mahler-3/2 / AEV** — single-orbit equidistribution of `⌊3c/2⌋` (`BB6_FRAMEWORK_PACKAGE`);
- as **EFF-EQ** — an effective rate crossing the log→linear digit-frequency gap (`P1PRIME_EFFEQ_LEVERAGE`);
- as a **Gauss-map analogue** — a non-sofic symbolic coordinate on the amenable `(2,3)`-solenoid in which the
  thin-target reachability becomes a decidable boundedness condition (`ALT_COORDINATE_PROBE`).

All three are the same single-orbit-equidistribution object; the synthesis shows its target is not "Antihydra" but
**the whole thin-target frontier**, and its obstruction is uniformly the `(dim 1, measure 0)` / non-Pisot /
log→linear wall (`EXCEPTIONAL_FINE_STRUCTURE`).

## The residual, precisely
Two things sit outside the master tool:
1. **o10** — the sole thick-target (generic-HALT) machine; needs quenched **pair-correlation** (BC-II), strictly
   beyond single-orbit equidistribution (`O10_APEX`).
2. **Exact (non-thin) reachability** — for any B2 machine where the halt target is not thin, single-orbit
   equidistribution gives non-halt only for the thin ones; a genuinely thick or exact target needs more.
Everything else — the equidistribution/thin-target majority — is one tool away.

## Honest verdict
**(b) — the capstone synthesis.** The BB(6) cryptid frontier is **not 1104 independent problems, nor even two
walls, but one floor-multiplier object with a thin-target reachability halt**, resolved (non-halt direction) by a
**single** single-orbit-equidistribution tool for all but the lone thick outlier `o10`. This unifies the session's
tetrachotomy, EFF-EQ leverage, non-affine, and P1′-core results, and states the sharpest possible form of "one tool
decides the frontier." No decision follows — the master tool is the generational `(K)`/P1′ object — but the target
picture is now maximally compressed. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce / basis
Components (all this session unless noted): `CRYPTID_NONAFFINE_UNIFICATION_2026-07-04.md` (floor-multiplier),
`P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md` (thin/thick = convergent/divergent, master-tool reach), `O10_APEX_2026-07-04.md`
(thick outlier), `O17_SKEW_PRODUCT` / `O17_O3_STRUCTURE` (II structure), `SPACE_NEEDLE_HALT.md` (`f(m)` + all-ones),
`ALT_COORDINATE_PROBE` / `EXCEPTIONAL_FINE_STRUCTURE` (the wall), `NEW_MATH_PROGRAM.md` (P1′, 3 languages),
`PROBLEM_LIST.md` (B1/B2). Thinness table: `scratchpad` reachability/thinness summary.
