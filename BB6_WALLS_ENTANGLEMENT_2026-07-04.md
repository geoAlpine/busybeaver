# B1/B2 fresh-angle probe: the dichotomy is (K)-hard to compute, and the walls entangle on the non-halt axis (2026-07-04)

*Task B1/B2 from `REMAINING_TASKS_2026-07-04.md`: does the new tetrachotomy→dichotomy projection
(`BB6_TYPE_IV_CENSUS_2026-07-04.md`) open any non-circular angle on either generational wall
(B1 = (K)/Mahler-3/2, B2 = generalized-Collatz)? Four adversarial angles, web-verified. Result: **no crack**, both
walls stand, but **two genuine `(b)` sharpenings** worth banking. SOUNDNESS: labels throughout; every external
paper WebFetch-verified and placed at its actual tier; **no machine decided, no label upgraded.***

## Verdicts by angle

**Angle 1 — a uniform B2 substrate across II/III/IV?** `(c)` + `(b)`. II/III already share the
`NESTED_COLLATZ_THEOREM` reseed Borel–Cantelli substrate, but it funnels to the two known obstructions: the
convergent BC-I (non-halt) direction needs `EFF-EQ` = effective single-orbit equidistribution rate = **B1-shaped
(P1′)**, and the divergent BC-II (halt) direction needs quenched quasi-independence which `O10_HALTER`
`[PROVEN-negative]` a single orbit cannot supply. **Type IV does NOT fit the reseed substrate** — its fixed-arity
counter machine with `⌊(p/q)·⌋` updates generalizes Minsky machines (strictly more general than the odometer
cascade). So the only statement uniform across {II,III,IV} degenerates to plain `Σ⁰₁` reachability — no per-machine
leverage.

**Angle 2 — counting/generic leverage from B1 being a ~12-machine minority vs 80% B2?** `(c)`, clean kill. A finite
holdout set carries no decision-theoretic measure; each machine's halting is a definite `Π⁰₁` fact and P0 needs
**all** of them. The ~12 Type-I/B1 machines are a strict **bottleneck** — and they are the *generationally harder*
wall — so "most cryptids are B2" means the easier-in-kind wall dominates the count while the harder wall is
rate-limiting. No shortcut.

**Angle 3 — bridge between the walls; re-examine the o4 "provably-distinct" separation.** `(b)`, no crack — the two
bankable results:
- **(i) The wall-classifier is itself (K)-hard.** The B1-vs-B2 discriminator is positive-entropy / abs-continuous
  (I) vs zero-entropy / singular (II/III/IV), but `p(ℓ)=2^ℓ` for a Mahler orbit is `(K)`-hard content
  (`BB6_TWO_WALLS` caveat). So **deciding "Type I vs the rest" for an arbitrary machine = detecting positive
  entropy of its driver orbit = (K)-adjacent.** Evidence: H4 was proxy-flagged Type-I then RE-refuted to Type-II;
  o4 wears a Type-II presentation over a B1 driver. **⇒ the tetrachotomy→dichotomy projection is a real STRUCTURAL
  truth but NOT an effective classifier** — "which wall" is undecidable-in-kind. (This is the rigorous form of the
  program's repeated "a clean per-machine split needs full RE" observation — see `BB6_TYPE_IV_CENSUS` §2 and the A10
  split, which can only classify by *observed* phenotype.)
- **(ii) The walls entangle on the NON-HALT axis, orthogonal only on the HALT axis.** B2's convergent (BC-I,
  non-halt) direction across the whole nested class consumes `EFF-EQ` = a B1-type effective single-orbit
  equidistribution rate = **P1′**. So P1′ (the one missing B1 tool) *also* delivers the non-halt direction across
  much of B2 — **broader reach than the ~12 Type-I machines**. Genuine orthogonality survives only on the halt
  direction (BC-II quenched quasi-independence, provably unavailable to a single deterministic orbit). The "two
  independent breakthroughs needed" framing (`BB6_TWO_WALLS`) is correct for the *halt* directions but overstates
  orthogonality on the *non-halt* direction.

**Angle 4 — new external single-orbit generalized-Collatz / counter-reachability tools 2024–26?** `(c)`. Verified,
nothing reaches the quenched tier: AEV Conj 1.6 = arXiv:2510.11723 (the named wall, `[OPEN-in-lit]`, not a tool);
arXiv:2511.03861 "Ternary Digits of Powers of Two" (2025) = computational evidence to n=10⁶ only, states even the
weaker Erdős conjecture is open; arXiv:2512.05690 "Non-Archimedean Koksma" (2025) = a.e.-x with full-Hausdorff-dim
exceptional set, explicitly not single-orbit. Empty-toolbox reconfirmed through the current frontier.

## Synthesis

The projection **opened no crack** and reinforced both walls, but banked two `(b)` results: (1) the
`{I}→B1` vs `{II,III,IV}→B2` split is a structural truth that is **itself (K)-hard to compute** (classifying a
machine's wall = detecting positive entropy of its driver), so the dichotomy is not a decision procedure; and
(2) the walls are **entangled on the provable non-halt axis** — B2's convergent direction consumes the same
unbuilt P1′ effective-equidistribution tool as B1, giving P1′ broader leverage than the ~12 Type-I machines, while
orthogonality survives only on the halt (quenched quasi-independence) axis, which no 2024–26 tool touches. Type IV
is confirmed a distinct phenotype but a strictly-more-general counter machine collapsing into B2 reachability.
**No machine decided. No label upgraded.**

New verified citation for `CITATIONS.md`: arXiv:2511.03861 (Ternary Digits of Powers of Two, 2025) — computational
normality evidence, same wall.

## Reproduce
- Angle 4 via WebSearch/WebFetch (arXiv:2510.11723, 2511.03861, 2512.05690). Structural angles rest on
  `NESTED_COLLATZ_THEOREM.md`, `O10_HALTER.md`, `BB6_TWO_WALLS_2026-07-04.md` (`two_walls_verify.py`),
  `BB6_TYPE_IV_CENSUS_2026-07-04.md`.
