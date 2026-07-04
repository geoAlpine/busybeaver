# Antihydra balance dips do NOT correlate with log₂3 footholds — control refutes an apparent pattern (2026-07-04)

*Fresh empirical probe of the `(K)` kernel: do the **deep dips** of Antihydra's balance walk `B_n=3E_n−n` (where
the running even-density comes closest to the halting threshold `1/3`) locate near the **log₂3 continued-fraction
footholds** (the `n` where `3ⁿ≈2ᵖ`, i.e. convergent/semiconvergent denominators)? A Diophantine structure in the
`(K)` fluctuations would be a genuine new handle. **Answer: NO** — a statistical control shows the dips are **no
closer to footholds than random points** (observed median rel-distance `2.1%` vs random control `2.0%`). An
apparent correlation (a deep-dip cluster `n≈8950` sitting `0.04%` from foothold `8951`) is **an artifact of dense
semiconvergent footholds**, not a real effect. SOUNDNESS: `[OBSERVED]`, control-verified; no over-claim; no machine
decided.*

## The probe and the control `[OBSERVED]`
- **log₂3 footholds** (convergent + semiconvergent denominators): `12,17,29,41,53,94,147,200,253,306,359,665,971,
  1636,…,8286,8951,9616,…` — increasingly *dense* (semiconvergents fill in at spacing `≈` the last convergent
  denominator).
- **Deep balance dips** (local minima of `B_n/n` below `0.49`, `n≥55`, to `N=3·10⁵`): the deepest are `n=123`
  (`B/n=0.439`, the famous one), `n≈830–887`, `n≈8900–9100`.
- **Apparent pattern:** the `n≈8900–9100` dips sit `0.04–1.8%` from foothold `8951` — *looks* striking.
- **Control (decisive):** over the deepest 60 dips, the **median relative distance to the nearest foothold is
  `2.100%`**; for **random `n`** in the same ranges it is **`1.968%`** — essentially identical. Dips within `2%`
  of a foothold: **observed `48.3%` vs control `51.1%`**. **The dips are NOT closer to footholds than random.**

## Reading
- **No Diophantine-foothold structure in the `(K)` dips.** The apparent `n≈8950`-at-`8951` coincidence is explained
  entirely by **foothold density** — near `n=9000` the semiconvergents are spaced `≈665`, so *any* point (dip or
  random) is `~2%` from one. The famous `n=123` dip is `19.5%` from its nearest foothold `147` — not close at all.
- **Consistent with i.i.d.-indistinguishability.** The program already proved the balance walk passes every tested
  i.i.d.-geometric test (`SINGLE_REALIZATION_WALL.md`); the deep dips behave like a **drifted random walk's** dips,
  not Diophantine-placed events. This probe adds one more: the dips carry **no log₂3-foothold signal**.
- **Disciplined negative.** The apparent `n≈8950` correlation was tempting to record as a "partial Diophantine
  structure"; the statistical control **refuted it**. (This is the session's habit — verify before claiming.)

## Honest verdict
**(c) — no correlation; the apparent pattern is a foothold-density artifact.** The `(K)` balance dips do not locate
near log₂3 footholds (observed `2.1%` ≈ random `2.0%` median distance); the fluctuations show no Diophantine-foothold
structure, consistent with the walk's i.i.d.-indistinguishability. No new handle on `(K)`. **Halting `[OPEN]`. No
machine decided. No label upgraded.**

## Reproduce
- `scratchpad` (`/opt/homebrew/bin/python3.13`): log₂3 CF `[1,1,1,2,2,3,1,5,2,23,…]`, footholds = conv+semiconv
  denominators; Antihydra `B_n=3E_n−n`, local minima below `0.49`; control = random `n` in same ranges (observed
  `2.1%` vs control `2.0%` median rel-dist). Basis: `SINGLE_REALIZATION_WALL.md` (i.i.d.-indistinguishability),
  `P1_DATA_GATHER.md` (log₂3 CF footholds), `OCCUPANCY_PROFILE_THEORY.md` (balance walk).
