# o4 seam-parity lemma — the odometer-critical seam class PROVEN safe unconditionally; residual = the once-per-generation cap C-seam (2026-07-06)

*Attacking the single remaining obligation (the incoming-cell / seam-parity predictor). **Major result: the feared
mechanism — "the base-4/3 carry cascade desynchronizes the seam parity" — is REFUTED.** Every gap-edge (cascade) seam
is safe by an unconditional 4-step local chain with ZERO odometer dependence `[PROVEN]`. The residual obligation
shrinks to the once-per-generation `1001`-cap C-seam (bounded, fixed structure), contingent only on uniform-interior
alternation. SOUNDNESS: assertion script re-run + transition-table claims independently re-verified by the main loop.
o4 `[OPEN]` — not decided. No machine decided.*

## The decomposition `[PROVEN from the transition table, re-verified]`
1. **B on an `11` is always on the RIGHT `1`.** B is created only by `A:0→1RB` / `F:0→0RB`; the only B-reads-1
   touching an `11` has creator `A` — A writes the fresh `1` at `p−1`, B lands on the pre-existing `1` at `p`.
   Safety ⟺ `tape[p+1]=0` (known reduction, now with creator pinned).
2. **Seam-creating A has predecessor ∈ {E, C} only** — forced by the table (A-predecessors are `C:0→1LA`, `C:1→0RA`,
   `D:0→0LA`, `E:1→1LA`; `D:0` writes `0` at `q+1` so cannot create the seam). Verified: `{E: 7,690, C: 21}`, 0 exceptions.
3. **E-seams are safe UNCONDITIONALLY, for all G `[PROVEN, the decisive piece]`.** E is entered **only** by `D:1→0LE`
   (unique in the table). The chain is forced: `D@q+2` (erases to `0`, moves L) → `E@q+1` reads `1` (`E:1→1LA`) →
   `A@q` reads `0` (`A:0→1RB`) → `B@q+1` reads `1` with **`tape[q+2]=0`** — the head went `q+2→q+1→q→q+1` and never
   retouched `q+2` after D's erase. Four steps of pure local geometry; **zero odometer information needed**.

## The odometer-critical case closed `[PROVEN + OBSERVED census]`
**Every gap-edge seam — exactly where the base-4/3 cascade meets the filler, the place the odometer could act — is
E-type**: `7,668/7,668` at G≈7.7k (and `24,413/24,413` at G≈24,644 in the wider run). So the cascade seam parity is
locally forced by the single `D:1→0LE` erase, **independent of G and of the base-4/3 digit string**. The desync
mechanism does not exist.

## The residual `[OPEN, sharply localized]`
Only **C-seams**, all at the fixed `1001` cap, once per generation (`21` by G≈7.7k — grows like #generations ≈
log_{4/3}G, NOT with G). Unified observation: for ALL seams (E and C), `q+2` was **last written by `D:1→0LE`**
(`7,711/7,711`) — since every head visit rewrites a cell, "last-writer of `q+2` is D" proves the head hasn't retouched
`q+2` since the erase. The C-case closes iff the rightward ABC-sweep turns around left of `q+2` — contingent on the
uniform-interior `(10)*` alternation (a **bounded cap-crossing**, per-filler-parity), `[OBSERVED]` through the cascade
but not yet proven through it. The remaining gap is a **fixed bounded structure at the cap**, no longer an unbounded
odometer statement.

## Verdict
**(b) — substantial proven partial: the seam-parity lemma is decomposed and its dominant, odometer-critical class
(gap-edge cascade seams) is PROVEN safe unconditionally** via the `D→E→A→B` chain — refuting the specific carry-desync
mechanism that motivated the lemma. Remaining `[OPEN]`: safety of the once-per-generation `1001`-cap C-seam
(bounded cap-crossing + uniform-interior alternation through the cascade). Combined with `O4_WINDOW_SATURATION`
(bounded-defect structure PROVEN, windows saturated+safe to 3.25×10¹⁰ events), o4 is now: **finite proven structure +
one bounded cap-local claim.** **o4 not decided.** Halting `[OPEN]`. No machine decided. No label upgraded.

## Reproduce
- `o4_seam_lemma_verify.py` (consolidated, assertion-checked; re-run by main loop: B-reads-1=7,479,444, UNSAFE=0,
  predecessors {E:7690,C:21}, q+2 last-writer {(D,1,0):7711}, gap-edge seams all-E 7,668/7,668).
- `o4_seam_parity.py`, `o4_seam_predecessor.py`, `o4_qplus2_provenance.py`, `o4_seam_trace.py` (3×10⁸-step runs).
- Table claims (E entered only by `D:1→0LE`; A-predecessors; chain geometry) re-derived independently from
  `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`. Basis: `O4_WINDOW_SATURATION_2026-07-06`, `O4_11AVOIDANCE_A2`.
