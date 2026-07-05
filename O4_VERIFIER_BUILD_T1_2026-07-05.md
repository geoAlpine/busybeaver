# Counter-automaton verifier for o4 — build turn 1: bouncer architecture + halt-freeness reduced to a structural fact (2026-07-05)

*Turn 1 of the careful, validated, multi-turn build of a sound counter-automaton verifier to decide o4. This turn
**determines the verifier architecture** and **reduces halt-freeness to a bounded/structural obligation**. o4's
generation is a **bouncer** (two period-2 sweeps growing with the big-gap counter `G`) driving the base-4/3 odometer,
and **`B` structurally never faces `11`**. SOUNDNESS: `[OBSERVED, validated]`; o4 `[OPEN]` — **not decided**; the
symbolic accelerator is not yet built/validated. No machine decided.*

## Architecture determined `[OBSERVED, one generation segmented]`
One generation (e.g. big-gap `G=30`, 818 steps) has the head **sweep a region of width `≈2G` (bouncer)**, decomposing
into: bounded period-1 **turn-around** work at the ends + two **uniform period-2 sweeps** that grow with `G`:
- **`B1 F0`** (rightward): `B` reads `1`→`1RF`, `F` reads `0`→`0RB` — crosses a `(10)`-region rightward.
- **`D1 E0`** (leftward): `D` reads `1`→`0LE`, `E` reads `0`→`1LD` — crosses leftward, converting.
The sweep counts grow `~G/2`; the odometer `G ↦ ⌊4G/3⌋+c(G mod3)` advances per generation. So o4 = **a bouncer whose
bounce-region is a base-4/3 counter** — this is the object the verifier must accelerate.

## Halt-freeness reduced to a structural/bounded fact `[VALIDATED, 10M steps]`
The halt is `B` reading a `1` with right-neighbour `1`. Measured over 10M steps: **`B` reads `1` 2,488,447 times, with
right-neighbour `0` EVERY time (0 with right `1`)**; the only `(left,right)` contexts at a `B`-reads-`1` are `(0,0)`
and `(1,0)`. **Reason (structural):** `B` reads `1` only inside the uniform `B1 F0` rightward sweep, which crosses a
`1010…` pattern — so the cell right of `B` is **always** `0`. Hence:
> **Halt-freeness reduces to: (i) the `B1F0` sweep is over a uniform `(10)` region (right-neighbour `0` by
> construction), and (ii) the bounded turn-arounds never present `B` with `11`.** (i) is a **uniform-sweep** fact, (ii)
> a **finite boundary** check — both discharge-able **per residue class `G mod 3`**, not `(K)`.

## The verifier's remaining obligations (turns 2+) `[the plan]`
1. **Sound symbolic sweep accelerator.** Represent the bounce-region symbolically; accelerate `B1F0`/`D1E0` sweeps by a
   parameterized count, **validated** by checking the per-step cycle is uniform (first/last iterations concrete) before
   each jump. (The repo's `bouncer_prove_sound.py` is a template for sound sweep acceleration.)
2. **One-generation closure.** Verify `0^G (10)^a 1001 → 0^{G'} (10)^{a'} 1001` with `G'=⌊4G/3⌋+c(G mod3)`, for each
   `G mod 3` and general `a`, via the accelerated symbolic run.
3. **Halt-freeness.** Confirm no `B`-reads-`11` in the (bounded) turn-arounds symbolically (the sweeps are `11`-free by
   §above).
On passing all three **with a validated accelerator**, o4 is decided. Until then, **o4 is not decided**.

## Verdict
**(b) — turn 1: architecture + halt-free reduction, both validated; o4 still OPEN.** o4's generation is a bouncer over
a base-4/3 counter, and `B` structurally never faces `11` (right-neighbour always `0`, 10M-validated), reducing the
decision to a **validated symbolic-sweep closure per residue class**. This is genuine progress toward a sound decision;
**o4 is not claimed decided** (the accelerator is unbuilt/unvalidated). **Halting `[OPEN]`. No machine decided.**

## Reproduce
- `/tmp/o4_bigprocess.py` (one generation = bouncer, sweeps `B1F0`/`D1E0`), B-reads-1 always right-`0` (10M).
  Basis: `O4_FAR_VERIFICATION_2026-07-05` (non-regular ⇒ counter needed), `O4_COUNTER_CERTIFICATE_2026-07-05`
  (`0^G(10)^a1001`), `bouncer_prove_sound.py` (sound sweep acceleration template).
