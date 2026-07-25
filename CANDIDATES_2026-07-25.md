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
