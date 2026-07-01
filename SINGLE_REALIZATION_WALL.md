# Attacking the single-realization wall via the deterministic linkage — honest negative (2026-07-01)

*Attack attempt #2 on the one residual the occupancy-profile theory leaves open: single-realization genericity =
`(K)`. The theory proved the seed-27 orbit is annealed-indistinguishable at the second-moment level
(`OCCUPANCY_PROFILE_THEORY.md` §11). The one thing an i.i.d. model ignores is that the depths are DETERMINISTICALLY
linked (`D_{j+1}` is a function of `o_j`). This note tests whether that deterministic linkage imposes any QUENCHED
constraint i.i.d. lacks — a rigidity that could forbid the halting mechanism. HONEST RESULT: it does not; the linkage
is 50/50-mixing at the decisive transition, giving no quenched leverage. The wall stands `= (K)`. SOUNDNESS: all
`[OBSERVED]` exact big-int, `N=2·10⁵`, `scratchpad/linkage.py`; no proof claimed. NOT committed by default.*

---

## The three probes and their verdicts

**(A) Finite-window predictability of the next depth `[OBSERVED — non-closure re-derived].** `D_{j+1}` is determined
by `o_j \bmod 2^w` for a fraction of samples that `→1` as `w` grows (`0.50` at `w=4`, `0.94` at `w=8`, `0.9999` at
`w=18`), but never all — the undetermined cells are exactly the deep cylinders (`D_{j+1}\ge k` needs `o_j \bmod
2^{D_j+k}`). So the next depth is finite-window predictable *with a growing window*: the same non-descent-to-a-finite-
quotient (non-integrality of `3/2`) that blocks every finite-state approach. No new constraint.

**(B) The orbit is on the safe side of the annealed Lundberg bound `[OBSERVED]`.** Actual running-min balance (after
burn-in) `= 17`; the i.i.d. golden-ratio LDP would *typically* permit dips of order `-\log_φ N ≈ -25`. So the orbit
sits above the annealed-typical dip — consistent with non-halting — but establishing that the quenched minimum stays
`\ge 0` is exactly `(K)`.

**(C) The decisive transition is 50/50 — no rigidity `[OBSERVED, the key test].** Halting requires a long run of
`D=1` (`o\equiv 1 \bmod 4`), each `-1` for the balance. After a `D=1` step the next residue splits
`o'\bmod 4 = \{1: 50037,\ 3: 50031\}` — **essentially exactly 50/50**. So a `D=1` step is followed by another `D=1`
(run continues) or by `D\ge2` (run ends) with probability `≈½` each: the `D=1` runs are **geometric, memoryless** —
neither forced to continue nor forbidden. The deterministic linkage behaves, at the transition that governs halting,
identically to i.i.d.

## Verdict

**The deterministic-linkage angle collapses.** At the one-step transition that controls the halting mechanism, the
deterministic orbit is indistinguishable from i.i.d. (50/50 continuation of `D=1` runs), so the linkage supplies
**no quenched constraint** beyond the annealed model. This *sharpens* the i.i.d.-indistinguishability of §11 from the
second-moment level down to the **one-step deterministic transition**: even the exact next-step rule is `½`-mixing,
carrying no rigidity to exploit. Combined with (A) (the finite-window predictor inherits the non-closure) and (B)
(the orbit is annealed-safe but unprovably so), the single-realization wall stands intact.

This is the expected honest outcome and the right kind: an attack on the wall that fails for a *specific, verified
reason* (the transition is `½`-mixing), not for lack of effort. It reconfirms — now at the finest (transition) scale
— that the residual is genuinely single-realization genericity `= (K)`: nothing short of controlling the specific
orbit's deterministic-yet-`½`-mixing trajectory decides it.

## Addendum — rigorous statistical GOF: the depth sequence passes every i.i.d.-geometric test (2026-07-01)

To make the "annealed-indistinguishable" statement as sharp as hypothesis testing allows, we ran standard tests on
the depth sequence `D_j` (`scratchpad/gof.py`, `N=4·10⁵`, exact big-int depths):
- **χ² goodness-of-fit** vs geometric `2^{-d}` (12 bins): `χ²=11.11`, `dof=11`, **`p=0.43`** — consistent.
- **Independence** `D_j` vs `D_{j+1}` (χ² contingency, 6×6): `χ²=25.4`, `dof=25`, **`p=0.44`** — independent.
- **Autocorrelation** lags 1–10: all within `±1/\sqrt N = 0.0016` of zero — no serial correlation.
- **Moments:** mean `1.99741` (geom `2`), variance `1.99923` (geom `2`), skewness `2.145` (geom `2.12`) — all match.
- *(Runs test: raw runs `177686` vs expected `177904` — within `0.1\%`; the normalizing variance formula overflowed
  `int64` (a numerical artifact, not a result), so the `z`-score is not reported. `[caveat]`)*

**No anomaly at any tested order.** The depth sequence is statistically **indistinguishable from i.i.d. geometric**:
it passes χ²-GOF, independence, autocorrelation, and moment tests. This upgrades the §11 second-moment match to
"passes standard i.i.d. hypothesis tests," and combined with the `½`-mixing transition (C above) leaves the residual
as pure single-realization genericity `= (K)` with **no detectable statistical handle** of any tested kind.
**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
