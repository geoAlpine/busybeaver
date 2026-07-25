# Pre-flight census — where the template island actually is (2026-07-25)

**Move 3 of `ANALYSIS_2026-07-25.md`.**  The programme's biggest unmeasured quantity, measured.
**No machine decided.  No label upgraded.**

---

## 0. Two discriminators failed first (recorded as failures)

* **Frontier-record bursts with a GLOBAL stall threshold.**  `x2` — a machine this programme has
  PROVEN to be a clean `×2` doubler — came out at "width ratio ≈ 1.1", i.e. **exactly the
  slow-width signature `CRYPTID_CENSUS` reports for the 10 "kernel un-extracted" machines.**
  That is direct confirmation of `ANALYSIS` §III: **the slow-width bucket is an artifact of the
  extractor, not a property of the machines.**
* **Tape-growth exponent `α` (`R ~ t^α`).**  `x2` = 0.498 but Antihydra = 0.504; all 19 sit at
  ≈ 0.5.  Uniform across the whole frontier — `α` separates nothing.

## 1. What works: scale-free epoch clustering

Cluster the frontier records so that **a gap `> t/4` opens a new epoch** (valid because epochs grow
geometrically), then read the total tape width at each epoch start.  No milestone extractor, no
reverse-engineering, one simulator run per machine.  `preflight_epoch.py`.

**Calibration — every independently-known value is recovered:**

| machine | measured | known |
|---|---|---|
| **x2** (PROVEN doubler) | **1.994** | 2 |
| Antihydra | 1.500 | 3/2 |
| o15 | 2.668 | 8/3 |
| o18 | 2.667 | 8/3 |
| o3 | 1.331 | ×4/3 schema |
| o5 | 1.331 | ×4/3 schema |

## 2. The named 19, at 4·10⁸ steps

| machine | epoch ratio | reading |
|---|---|---|
| Antihydra | 3/2 | (K) Mahler |
| o8 | 3/2 | (K) — **census had excluded it as a "7/5 heuristic artifact"** |
| o3, o5 | 4/3 | (K) |
| o4 | 1.3294, 1.3290, 1.3305, **1.3310** | 4/3, clean |
| o14 | ≈ 1.346 | 4/3 |
| o15, o18 | 8/3 | (K) Mahler |
| **Space Needle** | 2.4118, 2.4634, 2.4851, **2.4940** | converging to **5/2** (`v₂ = −1`, in the Mahler kernel family) — new |
| o2 | alternating 3.357 / 2.249 | epoch detector splits; per-epoch ≈ 2.75, unresolved |
| o7 | period-3 pattern 1.000 / 1.250 / 1.500 | unresolved |
| o10, o11, o12, o13, o16, Lucy | too few epochs even at 4·10⁸ | unresolved (slow) |
| o17 | noisy (2.0, 2.5, 2.0, 2.7, 20) | the odometer outlier, as expected |

> **NOT ONE named cryptid shows ratio 2.**  Every value that resolved is `3/2`, `4/3`, `8/3` or
> `5/2` — a Mahler multiplier with an **odd prime**, hence carry-OPAQUE, hence `(K)`.

## 3. The 1104 residual — where the island actually is

Screened all 1104 holdouts at 5·10⁶ steps (`preflight_1104.py`); `x2` is in the list, so the
calibration is *inside* the screen.

* **61 / 1104** land in the ratio-2 band on the last ratio alone.
* Requiring the **last THREE ratios all within 3 % of 2** (a consistent doubler — `x2` passes with
  1.985, 1.987, 1.990) leaves **4**:

| | spec | side | last three ratios | epoch widths |
|---|---|---|---|---|
| — | `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` | L | 1.9848, 1.9866, 1.9904 | 267, 526, 1044, 2074, 4128 — **x2, PROVEN (control)** |
| **A** | `1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE` | L | 2.0534, 1.9740, 1.9454 | 99, 131, 269, 531, 1033 |
| **B** | `1RB0RD_1RC1RB_1LD0LA_1LE0RA_0LF---_0LA0LC` | R | 1.9831, 2.0470, 1.9729 | 56, 118, 234, 479, 945 |
| **C** | `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` | L | 1.9866, 1.9932, 1.9937 | 263, 522, 1037, 2067, 4121 |

**Candidate C's width sequence tracks `x2`'s to within 5–7 cells at every epoch** — the 1104 list is
deduplicated up to TNF + left–right reversal, so it is not `x2` relabelled; it is a close sibling.

### 3b. Deep check at 10⁸–4·10⁸ steps — and a sharper signature

`x2`'s control run gives the exact doubler fingerprint: **width ratio → 2 AND time ratio → 4**
(`w = 1.970, 1.985, 1.987, 1.990, 1.994, 1.996`; `t = 3.81, 3.61, 3.90, 3.89, 3.97, 3.97`),
stable under every cluster threshold tried (`gap > 0.25t / 1.0t / 2.0t`).  Using `(2, 4)` instead of
`2` alone is the sharper test.

| candidate | verdict |
|---|---|
| **C** `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` | **CONFIRMED.**  `w = 2.023, 1.985, 1.987, 1.993, 1.994, 1.995, 1.997, 1.998`; `t → 3.985`.  Widths `130, 263, 522, 1037, 2067, 4121, 8223, 16421, 32811` — **exactly `x2`'s minus 7** from the 4th epoch on.  **Prime Phase-B target.** |
| **A** `1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE` | **plausible, not clean.**  On the R side with a coarser threshold `w = 2.000, 2.017, 2.162, 2.028, 1.975, 2.078`, `t = 5.27, 5.10, 4.08, 4.20, 3.99, 4.04` — the `(≈2, ≈4)` signature is there but the epoch structure is two-phase and the detector splits it.  Secondary target. |
| **B** `1RB0RD_1RC1RB_1LD0LA_1LE0RA_0LF---_0LA0LC` | **REFUTED at longer runs.**  A run of `≈2` ratios is followed by `w = 4.681`, `t = 26.14` — a genuine phase change, not a doubler. |

## 4. What this changes

1. **The named 19 are the `(K)` hard core** — confirmed by direct measurement, not extrapolation.
   No template machine among them.
2. **The template island is in the 1087 residual**, which is exactly where `x2` came from.
3. **Phase B has 3 concrete targets** (A, B, C) instead of an unbounded "~5–8 machines".
4. `3` is a **lower bound**: the screen ran only 5·10⁶ steps and needs ≥ 4 frontier-record clusters,
   so machines with long epochs were missed.  The 57 single-ratio rejects also deserve a re-run.

**No machine decided.  No label upgraded.  Push to the (public) origin remains HELD.**
