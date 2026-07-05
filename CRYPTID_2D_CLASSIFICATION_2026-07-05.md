# New thread — the 2D cryptid map: object-axis ⟂ wall-axis (density B1 vs reachability B2) (2026-07-05)

*Generalizing the o4 finding (`O4_HALT_FLAVOR_2026-07-05`: Type-I object + wall-B2 halt) to the whole frontier. The
**object** (how the value is stored: Type I–IV) and the **wall** (what proving "never halts" requires: **B1** = a
density/equidistribution read = `(K)`/Mahler, vs **B2** = a pattern/state reachability read = generalized-Collatz) are
**independent axes**. Both halt-forms are "∃ n: event", but the mathematics of proving *never* differs: **density
averaging** (B1) vs **reachability / invariant set** (B2). This note maps each named cryptid on both axes, honestly
separating `[verified]` from `[subtle/TBD]`, and draws the consequence for the decidability hunt. SOUNDNESS:
`[verified]`/`[subtle]`; halting `[OPEN]` throughout; no machine decided.*

## The 2D map `[verified where marked]`
| machine | object (Type) | wall (halt-flavor) | why |
|---|---|---|---|
| **Antihydra** | I (`×3/2`) | **B1 density** `[verified]` | halt ⟺ balance `3E_n−n<0` ever ⟺ even-density `<1/3` — an **accumulated-density** event = `(K)` |
| **o2, o7** | I (`×3/2`) | **B1 density** `[verified]` | Antihydra-family: `b` is a balance/refill counter returning to 0 (density) |
| **o10** | I (`×3/2`) | **B1 density** `[verified, O10_APEX]` | halt target is itself Mahler-defined (density-`½` odd-count); apex of B1 |
| **o4** | I (`×4/3`) | **B2 reachability** `[verified, this thread]` | halt ⟺ `11` ever reached in `B`'s sweep — pattern **existence**, not density |
| **o3** | II (odometer) | **B2 reachability** `[verified]` | halt ⟺ `00`-gap ever read by `E` — generalized-Collatz carry-existence |
| **Space Needle** | III (scalar Collatz) | **B2 reachability** `[verified]` | halt ⟺ scalar orbit hits a sparse set — reachability |
| **H5** | IV (counter bouncer) | **B2 reachability** `[verified, wall-class flagged OPEN earlier]` | halt ⟺ `11`-adjacency existence |
| **o17** | II (skew product) | **SUBTLE — B1-leaning** `[subtle]` | halt ⟺ marker-parity flip; the note's own reading: "that bit's **density** `= (K)`" — a density on a *kernel-less* object |
| **o15, o18** | I (`×8/3`) | **SUBTLE / TBD** `[subtle]` | classed Type-I(K) but the analyses use **window/existence** barriers (o18 floor) — halt-flavor per-machine not pinned |

## The two findings `[the new-thread payoff]`
1. **Object ⟂ wall (o4 is the witness).** The banked classification lumped all Type-I under the `(K)`/B1 wall; **o4
   (Type-I × B2) refines that** — a `×p/q` odometer *object* can carry a *reachability* halt. So "Type-I ⟹ `(K)`" is
   **too coarse**; the wall is set by the **halt-flavor**, not the object.
2. **B1 (density) is rare; the frontier is mostly B2 (reachability).** Genuine wall-B1/`(K)`/Mahler-density is (so far
   verified) confined to the **`×3/2` balance machines** (Antihydra, o2, o7, o10) — plus o17's subtle parity-density.
   **Everything else verified is B2** (o3, Space Needle, H5, o4). The "smallest open problem" (Antihydra) sits on the
   **rare** wall.

## Consequence for the decidability hunt `[actionable]`
- **B2/reachability machines are where decidability might live.** Reachability for *affine* generalized-Collatz can be
  decidable (VASS/Presburger); the B2 cryptids (o3, o4, Space Needle, H5) are **non-affine floor-multiplier**
  reachability — Collatz-hard in general, but the **right place to look for a genuine decision** (unlike B1, which is
  `(K)`-equidistribution and provably generational). The new-thread decidability effort should target **B2 machines**,
  and specifically the "closest-to-affine" ones.
- **B1 machines (Antihydra/o2/o7/o10) are all the same `(K)`** — no separate attack; they stand or fall together with
  the Normality Conjecture.

## Verdict
**(b) — a genuine 2D structural refinement.** The object and wall axes are independent (o4 = Type-I × B2, the witness);
B1/density is confined to the `×3/2` balance machines, most of the frontier is B2/reachability; the decidability hunt
should target B2. Honest limits: o17 (B1-leaning, subtle) and o15/o18 (halt-flavor TBD) need per-machine pinning.
**Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce / basis
- `O4_HALT_FLAVOR_2026-07-05` (o4 = B2), `CRYPTID_CLASSIFICATION_2026-07-04` (objects + halt conditions),
  `O10_APEX_2026-07-04` (o10 B1), `BB6_TWO_WALLS_2026-07-04` (B1/B2), `O17_REG_BARRIER.md` (o17/o18 existence barriers),
  `TYPEI_NORMALITY_FAMILY_2026-07-05`.
