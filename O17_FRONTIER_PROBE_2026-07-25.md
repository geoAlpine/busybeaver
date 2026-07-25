# o17 frontier probe — FIRED and REFUTED (2026-07-25)

`ANALYSIS_2026-07-25.md` §VI flagged one place where today's exact frontier calculus touches the
`(K)` side: **o17's halt IS a left-frontier event** (the head walks off the left edge of the written
region).  `route_o17_locality.py` had refuted bounded-window and periodic-in-`j` predicates for the
family `C(3j) = 0^∞ [A0] 1^(3j) 0^∞` ("no modulus"), but a **frontier-advance statistic** is neither
bounded-window nor obviously periodic, so it was **not strictly covered**.  §VI said it deserved one
firing under M0 before being dismissed.  Fired.

## Result — REFUTED

`o17_frontier_probe.py`, `j = 1..40`, budget `6·10⁶` steps.  For `j = 9 … 30` **every seed — halter
and non-halter alike — has the identical frontier statistic**:

    left frontier = −2,  left-extension count = 2

| j | fate | steps | left frontier | L-ext |
|---|---|---|---|---|
| 9 | RUN | 6 000 000 | −2 | 2 |
| 10 | **HALT** | 7 263 | −2 | 2 |
| 11 | RUN | 6 000 000 | −2 | 2 |
| 12 | **HALT** | 13 811 | −2 | 2 |
| … | … | … | −2 | 2 |
| 29 | **HALT** | 3 930 997 | −2 | 2 |
| 30 | RUN | 6 000 000 | −2 | 2 |

> **The frontier statistic does not separate the classes.**  The exact frontier calculus built today
> (`steps_rpad_dich` / `steps_lpad_dich` and the block absorb lemmas) therefore gives **no purchase
> on o17**, and with it none on `(K)`.

This closes the last unfired item on the `(K)` side of `ANALYSIS_2026-07-25.md`.

## Incidental observations (recorded, not over-read)

* For `j ≥ 15` the halters in range are exactly the ODD `j` (15, 17, 19, 21, 23, 25, 27, 29), with
  halt times roughly DOUBLING: `45 689, 52 933, 117 161, 232 605, 600 057, 1 029 413, 1 614 529,
  3 930 997`.
* `j ≥ 31` shows "RUN" only because the `6·10⁶` budget cuts off — the doubling trend puts the next
  halt beyond it.  **That is not evidence of non-halting.**
* The small `j` halters (2, 4, 5, 7, 8, 10, 12) break the parity pattern, so the existing "no
  modulus" characterisation of the family stands.

**No machine decided.  No label upgraded.**
