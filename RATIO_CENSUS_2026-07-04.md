# Floor-multiplier ratio census (bounded-arity band) — method-limited, no new p/q confirmed (2026-07-04)

*Attempt to census the value-orbit growth ratios `p/q` of the bounded-arity holdouts, to find any new Mahler-family
ratio beyond the named `{3/2, 8/3, 4/3}` (as o4's `4/3` was found this session). Result: **inconclusive** — the
crude leading-block record-ratio method is **unreliable** (it mis-reads o7's known `×3/2` as `~1.8`, because the
leading block mixes the value with the balance counter), so **no new `p/q` is confirmed**; 5 clean `×3/2` machines
are reliably re-confirmed, and one candidate (`~2.4`) is flagged for proper RE. SOUNDNESS: `[OBSERVED]`; no
over-claim of a new ratio; no machine decided.*

## What the census found `[OBSERVED, ratio_census.py, 40 machines]`
- **Reliable: 5 clean `×3/2` machines** (leading-value ratio stable `1.49–1.53` over 8–16 records) — the Type-I
  `×3/2` band, consistent with the named family.
- **Unreliable "NEW?" flags (~19):** the record-ratio method returned assorted values (`1.8, 1.91, 2.20, 2.41,
  1.02, 1.04, …`), but **these are mostly artifacts or non-Type-I**:
  - the near-`1.0` ones (`1.0016` with 1227 records, `1.03`, `1.04`) are **arithmetic/slow counters** (Type-II
    odometers), not geometric value orbits;
  - the mid-range ones are **contaminated**: the method reads the *leading block*, which for a two-counter Mahler
    machine mixes the `×3/2` value with the balance/refill counter, giving a spurious ratio.

## The method's failure, demonstrated `[OBSERVED]`
**o7** (`1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC`) is a **proven `×3/2`** machine (value peaks
`317→477→717→1077→1617→2427 = ×1.5`, `verify_ratio.py` earlier). Yet this census reports it as `~1.8` and the
dip-aware re-check gives irregular record-ratios `1.19, 1.8, 1.16, 1.27, 1.91, 9.63`. **So the leading-block
ratio ≠ the value-orbit ratio** when a balance counter is present — the census method cannot reliably extract `p/q`.
A proper census needs per-machine RE separating the value orbit from the balance counter (as `verify_ratio.py`
does for individual machines).

## One flagged candidate `[OPEN, for future RE]`
`1RB1LF_0RC1RD_1LA1LD_1LE0RA_---1LC_0LA1LA` — upper-envelope records `17,75,181,437,871,2009`, ratios
`4.41, 2.41, 2.41, 1.99, 2.31` (`~2.4`, moderately geometric but with variation). **Possibly** a Mahler-family
member with a ratio near `12/5=2.4` / `7/3≈2.33`, **or** a contaminated extraction. **Not confirmed** — flagged for
proper value-orbit RE before any claim.

## Honest verdict
**(c) / inconclusive — no new `p/q` confirmed.** The crude ratio census is method-limited (the o7 artifact proves
leading-block ratio ≠ value ratio); it reliably re-confirms 5 `×3/2` machines and flags one `~2.4` candidate for RE,
but claims **no** new Mahler ratio. A reliable ratio census requires per-machine value-orbit RE. **No machine
decided. No label upgraded.** *(Conservatism deliberate — after four self-caught over-claims this session, a crude
"new ratio" is exactly the kind of claim to withhold pending proper RE.)*

## Reproduce
- `scratchpad/ratio_census.py` (leading-block record-ratio, unreliable), dip-aware re-check inline (o7 artifact;
  candidate `~2.4`). `verify_ratio.py` is the reliable per-machine method. Band `bounded_specs.txt`. Named ratios
  `{3/2, 8/3, 4/3}` in `CRYPTID_CLASSIFICATION_2026-07-04.md` / `O4_HALT.md`.
