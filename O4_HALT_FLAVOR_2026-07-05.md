# New thread — o4's halt-flavor resolved: reachability (wall B2), not normality (wall B1); object-axis ⟂ wall-axis (2026-07-05)

*Resolving the open sub-question raised in `TYPEI_NORMALITY_FAMILY_2026-07-05` ("is o4's non-halting normality or
anti-normality?"). Answer, by direct analysis: **neither — it is a reachability/existence event (wall B2)**, cleanly
distinct from Antihydra's density/normality (wall B1). o4 is a **Type-I base-4/3 OBJECT with a wall-B2 HALT-FLAVOR** —
showing the object-classification (Type I/II/III/IV) and the wall-classification (B1 density vs B2 reachability) are
**independent axes**. SOUNDNESS: `[OBSERVED]`/`[PROVEN-structure]`; halting `[OPEN]`; no machine decided.*

## The resolution `[PROVEN structure + OBSERVED]`
o4's exact value orbit is the base-4/3 odometer `G′=⌊4G/3⌋+c(G mod3)`, `c={0→3,1→5,2→1}` (`O4_HALT`). Its base-4/3
last digit `3G mod 4` runs on `{1,2}` (freq `1:0.68, 2:0.32`). **The halt condition, however, is the `11`-existence
gate** (`[PROVEN from the table]`): halt `⟺` state `B` ever meets a `1`-block of length `≥2` in its sweep. This is an
**existence / reachability** event over the carry cascade — "does the pattern `11` ever occur in `B`'s path" — **not a
density/frequency** condition. Contrast:
- **Antihydra (3/2):** halt `⟺` even-density drops below `1/3` — a **density** event = **wall B1** (`(K)`/Mahler/
  normality).
- **o4 (4/3):** halt `⟺` `11` ever reached in `B`'s sweep — a **reachability** event = **wall B2** (generalized-Collatz
  reachability).

So "anti-normality" (my earlier guess) was imprecise: o4's non-halting is not a density statement at all (neither
normality nor its negation) — it is **pattern-reachability**, the B2 wall.

## The structural refinement `[the new-thread payoff]`
> **The object-axis and the wall-axis are independent.** A machine's *object* (how it stores its value: Type-I
> scalar `×p/q` odometer, Type-II bounded-digit cascade, Type-III scalar Collatz, Type-IV counter bouncer) is separate
> from its *halt-flavor* (wall B1 = a **density/equidistribution** read of the orbit, vs wall B2 = a
> **reachability/existence** read). **o4 = Type-I × B2** (a `×4/3` odometer object whose halt is a reachability event),
> whereas Antihydra = Type-I × B1. The tetrachotomy (object) and the two-walls (halt) are **orthogonal
> classifications**, and o4 is the witness that they don't coincide.
This sharpens `TYPEI_NORMALITY_FAMILY §2`: Type-I unifies the *objects* under the Normality-Conjecture family, but the
*halt statements* split across BOTH walls — Antihydra/o10 on B1 (density), o4 on B2 (reachability), consistent with the
program's two-wall picture (`BB6_TWO_WALLS`).

## Verdict
**(b) — a genuine classification refinement; open sub-question resolved.** o4's non-halting is a **reachability event
(wall B2)**, not a density/normality one (wall B1); o4 is Type-I×B2, proving the object-axis ⟂ wall-axis. This is
internal progress on a non-`(K)` thread (o4's decidability is a B2/reachability question, a different problem from
`(K)`). **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `/opt/homebrew/bin/python3.13`: `G′=⌊4G/3⌋+c(G mod3)`; base-4/3 last digit `3G mod4 ∈{1,2}`. Halt gate from
  `O4_HALT.md`/`o4_transducer.py` (`11`-existence, 0 firings/60M). Basis: `TYPEI_NORMALITY_FAMILY_2026-07-05`,
  `BB6_TWO_WALLS_2026-07-04`, `CRYPTID_CLASSIFICATION_2026-07-04`.
