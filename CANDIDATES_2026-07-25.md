# Template-island candidates — running verdicts (2026-07-25)

x2's control fingerprint, stable under every cluster threshold:
**width ratio → 2 AND time ratio → 4** (`w = 1.9866, 1.9904, 1.9937, 1.9961, 1.9977`;
`t = 3.895, 3.892, 3.972, 3.971, 3.992`).  A candidate must hold that for ≥3 consecutive epochs at
a long run.

| candidate | graph = `x2`'s? | in 1104 | verdict |
|---|---|---|---|
| **`x2`** `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` | — | ✅ | **[PROVEN non-halting]** |
| **C** `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` | **YES** (σ(x2), start = `x2`'s `B`) | ✅ | genuine `(2,4)` doubler, but **not a new family**; spec for deciding it in `CANDC_SPEC_2026-07-25.md` |
| **B** `1RB0RD_1RC1RB_1LD0LA_1LE0RA_0LF---_0LA0LC` | no | ✅ | **REFUTED** — phase change `w = 4.68`, `t = 26.1` |
| **A** `1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE` | no | ✅ | **REFUTED at 4·10⁸** — holds `(≈2, ≈4)` for six epochs (`ws = 29, 58, 117, 253, 513, 1013, 2105`) then breaks: `w = 6.774`, `t = 38.70`, `ws → 14259`.  The doubling was a transient. |
| **D** `1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---` | **no — genuinely independent** | ✅ | found by the deep `(2,4)` screen; `w = 2.0515, 2.0235, 2.0108` converging DOWNWARD to 2, `t ≈ 4.10`.  **Decisive 4·10⁸ run in progress.** |

## Reading

* Both earlier independent candidates (A, B) **broke at longer runs in the same way** — a phase
  change after a handful of clean doubling epochs.  That is a real failure mode of the screen and it
  is why the long run is mandatory before any claim.
* The deep screen (2·10⁷ steps, strict `(2,4)`) has returned **2 hits in the first 300** of 1104:
  `x2` itself (calibration) and **D**.
* So `D` is currently the **only live test** of whether the template method leaves `x2`'s graph.

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**


## Update — the island is NOT one graph

**`D` CONFIRMED at 4·10⁸ steps.**  R side: `ws = 185, 422, 893, 1832, 3707, 7454, 14945, 29924`;
`w = 2.2811, 2.1161, 2.0515, 2.0235, 2.0108, 2.0050, 2.0023` and
`t = 4.735, 4.352, 4.109, 4.051, 4.021, 4.010, 4.005` — **seven consecutive epochs converging
MONOTONICALLY to `(2, 4)`**, with no phase change, unlike `A` and `B`.
The recurrence is the doubler signature with a linear correction, as `x2`'s is:

    D  : w(k+1) = 2·w(k) + (52, 49, 46, 43, 40, 37, 34)      — decreasing by 3
    x2 : w(k+1) = 2·w(k) − (8, 8, 14, 20, 26, 32, 38)        — decreasing by 6

**The deep screen has returned 4 hits in the first 500 of 1104, on 4 DISTINCT transition graphs:**

| | spec | status |
|---|---|---|
| 1 | `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` | `x2` — calibration |
| 2 | `1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---` | **`D`, CONFIRMED at 4·10⁸** |
| 3 | `1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_1RC---` | **`E`, decisive run in progress** |
| 4 | `1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---` | **`F`, decisive run in progress** |

> **This overturns the reading in `ROADMAP_2026-07-25_v2.md` §1** that the island might be a single
> graph.  It is not: `D` alone settles that the `(2,4)` template class contains a machine outside
> `x2`'s graph, and two more candidates are under test with the screen only 45 % done.

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**


## Update 2 — E and F CONFIRMED; the island has FOUR graphs

Both decisive `4·10⁸` runs came back clean, stable under every cluster threshold, no phase change:

| | spec | epoch widths | `w →` | `t →` |
|---|---|---|---|---|
| **D** | `1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---` | 185, 422, 893, 1832, 3707, 7454, 14945, 29924 | **2.0023** (from above) | **4.005** |
| **E** | `1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_1RC---` | 125, 290, 617, 1268, 2567, 5162, 10349, 20720 | **2.0021** (from above) | **4.007** |
| **F** | `1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---` | 435, 829, 1609, 3151, 6227, 12357, 24605, 49071 | **1.9944** (from below) | **3.989** |
| `x2` | `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` | 267, 526, 1044, 2074, 4128, 8230, 16428, 32818 | **1.9977** (from below) | **3.992** |

All four have **distinct graph-canonical forms**, all four are in the 1104 list, and all four show
seven consecutive epochs converging monotonically to `(2, 4)`.

> **The template island is real and multi-graph.**  This reverses the pessimistic reading of
> `ROADMAP_2026-07-25_v2.md` §1 entirely: it is not one graph, it is at least four, with the deep
> screen only 72 % complete.

Phase B therefore has **three genuinely new targets (D, E, F)** plus `C` (`x2`'s own graph from
state `B`, already specified in `CANDC_SPEC_2026-07-25.md`).

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**
