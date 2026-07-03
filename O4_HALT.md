# o4: Type I with a NEW kernel ratio μ = 4/3, PROVEN 11-existence halt gate (2026-07-04)

*Reverse-engineering of cryptid **o4** (`A5`), machine-verified vs the raw TM by the orchestrator. o4 is a
**Type I equidistribution-kernel Mahler** machine — but on a **new ratio `μ=4/3` (kernel prime `p=3`)** not
previously in the census (which had `3/2` and `8/3`), with an **exact closed base-4/3 value odometer** and a
`[PROVEN from the table]` **11-existence halt gate** (the dual of o3's `00`-gate). SOUNDNESS: `[PROVEN]`/
`[OBSERVED]`; **halting `[OPEN]`**. Verifier: `o4_transducer.py` (`... VERIFIED: True`).*

o4 = `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---` (blank tape; halt = F reads 1). Table:
`A:0→1RB,1→0LD · B:0→1RC,1→1RF · C:0→1LA,1→0RA · D:0→0LA,1→0LE · E:0→1LD,1→1LA · F:0→0RB,1→HALT`.

## 1. Normal form + finite control `[OBSERVED, 21515 milestones to 60M, 0 exc]`
Milestone (head A/E at left frontier) = unit `1`-blocks separated by single/double `0`-gaps, plus **exactly one
big-gap defect** of length `G` (never two big gaps; length-2 blocks only transiently). Fixed finite control:
only **11** boundary-crossing / **4** right-reflection / **5** left-gate symbols ever occur. The big gap
migrates left at constant `−3`/milestone and resets a new generation on absorption.

## 2. A genuine ×4/3 value odometer `[OBSERVED, EXACT, orchestrator-verified vs raw TM]`
The generation-reset big gap `G` is a real arithmetic value:
```
        G′ = ⌊4G/3⌋ + c(G mod 3),   c = {0→3, 1→5, 2→1}
```
Orchestrator's independent raw-TM extraction: `G = 7,14,19,30,43,62,83,111,151,206,275,367,494,659,879,1175,
1567,2094,2795,3727,4974,6635,8847,…` — the map reproduces it with **residual `0` (12+ generations)**; tail
ratio → **1.33338 = 4/3**. Contrast tests fail: `μ=3/2` and `8/3` give unbounded residuals, and total width `W`
has no clean `4/3` map — so `G` (not width) is the fundamental coordinate, and the `4/3` is a **genuine value
multiplier**, not envelope geometry (the opposite of o3, whose `4/3` was envelope).

## 3. The `[PROVEN from table]` halt gate + safety `[OBSERVED, 0 exc / 60M]`
`F` is entered **only** by `B,1→1RF`; `F,1`=HALT. So:
> **`[PROVEN]` HALT ⟺ state `B` (a rightward sweep) reads a `1` whose right neighbour is also `1`** (`B` enters
> a `1`-block of length `≥2` — an **`11`-existence gate**, the exact dual of o3's `00`-existence gate).

Audited: over **14,971,966** `B`-reads-`1` events the right neighbour is **always `0`** (`B` always enters a unit
block) — **0 firings**. (Longer `1`-runs up to length 5 form transiently but never in `B`'s path — a genuine
dynamical separation, as in o3.)

## 4. Classification — Type I, new ratio, and what it settles
`v₃(4/3) = −1`, so o4 bears the **base-3 equidistribution kernel** (`CRYPTID_KERNEL.md`'s `{μ : v_p(μ)=−1}`
theorem) — same kernel prime as o15/o18 (`8/3`), **new ratio `4/3`**. It is a boundary object: a **Type I
arithmetic value kernel** (clean `⌊4G/3⌋` odometer, *stronger* determinism than o3/o17's irregular marker walks)
wearing a **Type II presentation** (finite-control head over a digit string; `11`-existence halt race dual to
o3's `00`-race). The halt is an existence event over the carry cascade the `×4/3` odometer drives; the wall is
the **(K)/Mahler-3 (Erdős) equidistribution** wall (Mahler 1968; AEV; the o15/o18 family).

## 5. Verdict
Outcome **(c) rederives the (K)/Mahler-3 wall** with genuine **(b) gains**: (1) a machine-verified **new kernel
ratio `μ=4/3`, `p=3`**; (2) an **exact closed base-4/3 value odometer** `G′=⌊4G/3⌋+c(G mod3)`; (3) a
`[PROVEN from table]` **`11`-existence gate** (dual to o3), 0 firings from blank; (4) it flips o3's "`4/3`=envelope"
to "`4/3`=genuine value". `√t` is again non-diagnostic (Type I here, Type II for o3, both finite-control heads).
The halt predicate reduces to the `11`-existence race over the base-4/3 cascade — **not** to a single proven
digit bit (o17's parity), the honest limit. **No machine decided. No label upgraded. Halting `[OPEN]`.**

## Reproduce
- `o4_transducer.py` — (I) language closure, (II) fixed 11/4/5 finite control, (III) the `[PROVEN]` `11`-gate
  (0 firings), (IV) the exact `G′=⌊4G/3⌋+c` orbit + `4/3` ratio. Prints
  `O4 TRANSDUCER + HALT-GATE + VALUE-ORBIT VERIFIED: True`. TM in `cryptid_map.py`.
