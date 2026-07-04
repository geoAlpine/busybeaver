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

| target | orbit | cryptids | resolved by | outside? |
|---|---|---|---|---|
| **thin, SCALAR** (density → 0, scalar orbit) | scalar value/counter | Antihydra, o2/o7/o11/o12/…, Space Needle, o3, o17 | **scalar single-orbit equidistribution of the floor-multiplier** (BC-I: thin ⇒ avoided ⇒ non-halt) | in reach |
| **thin, VECTOR** (thin target but multi-coord orbit) | counter **vector** | **Type-IV (H5)** | **counter-machine reachability** — no scalar orbit; needs a multi-dim tool `≠` scalar EFF-EQ | **OUTSIDE (off-axis)** |
| **thick / generic-event** (density ⅓) | scalar reseed | **o10** | **BC-II / pair-correlation** (harder than `(K)`) | **OUTSIDE (apex)** |

**So the scalar single-orbit equidistribution tool resolves the non-halt of the entire thin-target *scalar*
frontier** (all of B1 + the convergent *scalar* B2 — o3, o17-base, Space Needle). **TWO classes sit outside it**
`[SOUNDNESS CORRECTION, red-team 2026-07-04]`: **o10** (thick target, generic-HALT, needs BC-II) *and* **Type-IV /
H5** (thin target but a counter *vector*, off the scalar axis — `P1PRIME_EFFEQ_LEVERAGE §9.2`, brick 6). The earlier
draft's "only o10 outside, H5 resolved by a multi-dim variant" **over-unified**: H5's thinness makes non-halt
*annealed*-generic, but its quenched resolution is counter-machine reachability, not scalar equidistribution.

## Why this is the same object as (K), EFF-EQ, and the Gauss-map analogue
The master tool is exactly the missing tool `P1′`, now seen to have **frontier-wide** reach:
- as **(K) / Mahler-3/2 / AEV** — single-orbit equidistribution of `⌊3c/2⌋` (`BB6_FRAMEWORK_PACKAGE`);
- as **EFF-EQ** — an effective rate crossing the log→linear digit-frequency gap (`P1PRIME_EFFEQ_LEVERAGE`);
- as a **Gauss-map analogue** — a non-sofic symbolic coordinate on the amenable `(2,3)`-solenoid in which the
  thin-target reachability becomes a decidable boundedness condition (`ALT_COORDINATE_PROBE`).

All three are the same single-orbit-equidistribution object; the synthesis shows its target is not "Antihydra" but
**the whole thin-target frontier**, and its obstruction is uniformly the `(dim 1, measure 0)` / non-Pisot /
log→linear wall (`EXCEPTIONAL_FINE_STRUCTURE`).

## The residual, precisely `[corrected]`
**Two classes** sit outside the scalar master tool:
1. **o10** — the sole **thick-target** (generic-HALT) machine; needs quenched **pair-correlation** (BC-II), strictly
   beyond single-orbit equidistribution (`O10_APEX`).
2. **Type-IV / H5** — thin target but a **counter vector** (off the scalar axis); its non-halt is a
   fixed-arity counter-machine reachability, needing a **multi-dimensional** tool distinct from the scalar
   equidistribution (`P1PRIME_EFFEQ_LEVERAGE §9.2`).
Everything else — the thin-target **scalar** majority (all B1 + o3/o17/Space Needle) — is one (scalar) tool away.

**Caveat `[honest]`.** "One tool" means one **kind** of tool — single-orbit equidistribution / thin-target
avoidance — not one identical theorem: the specific equidistribution object varies by structure (a scalar **value**
for B1 and Space Needle, a **bounded-segment** counter for o3, a **skew-product fiber** for o17). o17's is the
subtlest (its object is the fiber's equidistribution, not a pure scalar). They are unified at the level of *kind*
and *obstruction* (the `(dim 1, measure 0)` / non-Pisot / log→linear wall), which is the defensible claim.

## Honest verdict
**(b) — the capstone synthesis, red-team-corrected.** The BB(6) cryptid frontier is **not 1104 independent problems,
nor even two walls, but one floor-multiplier object with a thin-target reachability halt**, whose non-halt direction
is resolved by a **single scalar single-orbit-equidistribution tool** for the thin-target *scalar* majority
(all B1 + o3/o17/Space Needle) — with **two** classes outside: **o10** (thick, BC-II) and **Type-IV/H5** (thin but
vector, counter-reachability). This unifies the session's tetrachotomy, EFF-EQ leverage, non-affine, and P1′-core
results into the sharpest form of "one tool decides *most* of the frontier." No decision follows — the master tool
is the generational `(K)`/P1′ object. **Halting `[OPEN]`. No machine decided. No label upgraded.**
*(Red-team catch: the first draft's "only o10 outside" over-unified — Type-IV/H5 is a second, off-axis residual.)*

## Reproduce / basis
Components (all this session unless noted): `CRYPTID_NONAFFINE_UNIFICATION_2026-07-04.md` (floor-multiplier),
`P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md` (thin/thick = convergent/divergent, master-tool reach), `O10_APEX_2026-07-04.md`
(thick outlier), `O17_SKEW_PRODUCT` / `O17_O3_STRUCTURE` (II structure), `SPACE_NEEDLE_HALT.md` (`f(m)` + all-ones),
`ALT_COORDINATE_PROBE` / `EXCEPTIONAL_FINE_STRUCTURE` (the wall), `NEW_MATH_PROGRAM.md` (P1′, 3 languages),
`PROBLEM_LIST.md` (B1/B2). Thinness table: `scratchpad` reachability/thinness summary.
