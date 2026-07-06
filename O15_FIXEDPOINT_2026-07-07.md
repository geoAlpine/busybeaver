# o15 fixed-point structure — the o4 run theorem PORTS to the V-orbit (all four branch maps, x=−c/5 ∈ ℤ₃, exact v₃ run laws, ×8/3 mirror coordinate W=V−1); but the FATAL CYLINDER is a recursive string LANGUAGE, provably not a congruence in V (2026-07-07)

*Porting `O4_RUN_STRUCTURE_2026-07-07.md` to o15 (`1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA`, halt = A reads 1;
state = digit queue D + big block V per `O15_TEMPLATE_PORT_2026-07-07.md`). **Verdict: split decision.** The
fixed-point trick works PERFECTLY one level down — every branch map V′=(8V+c)/3 has a 3-adic fixed point and the
V-residue runs have exact v₃ closed forms, including on the real orbit (the blank orbit's only double-split is
predicted by v₃=2). But the fatal-exposure question does NOT reduce to these closed forms: the [2,2] cylinder's
boundary is a digit-STRING property (order-dependent, recursive), and the next-branch function after a ρ=0 step
provably depends on unbounded queue content. Two session hypotheses were refuted and are documented. o15 `[OPEN]`.*

## 1. The branch fixed-point theorem `[PROVEN]` (`o15_fp_vmap.py`)
The extracted branch maps (exhaustive V=20..500, 481 exact runs, 0 exceptions, unsafe=0):
| class | map | fixed point x (5x=−c) | run closed form |
|---|---|---|---|
| ρ=0, single | V′=(8V+9)/3 | −9/5 ∈ ℤ₃ | run = v₃(5V+9) |
| ρ=2, single | V′=(8V+11)/3 | −11/5 ∈ ℤ₃ | run = v₃(5V+11) |
| ρ=1, empty queue | prepend 6, V′=(8V−17)/3 | 17/5 ∈ ℤ₃ | mixed run = v₃(2V−5) |
| ρ=1, queued | drain −3, emit [1,1], V′=(8V−5)/3 | **x = 1 (INTEGER)** | run = v₃(V−1) |

*Proof of the run laws (o4 argument verbatim):* at x, 3x=8x+c, so V′−x = (8/3)(V−x); 8 is a 3-adic unit, so
v₃(V−x) drops by exactly 1 per same-branch step, and x ≡ ρ (mod 3) in each row (5⁻¹≡2 mod 3). Since
v₃(V−x)=v₃(5V+c), the runs follow. ∎ Verified exhaustively V ≤ 2·10⁵, all four laws, **0 mismatches**
(the run laws are theorems ABOUT the branch maps; the branch maps themselves are `[PROVEN on the grids]`).
- **Mirror coordinate:** W = V−1 makes the queued split EXACTLY ×8/3: W′=(8/3)W. o15's split countdown is the
  **3-adic depth of a ×8/3 orbit** — its own Mahler number (`O15_REDUCTION.md`), extending the mirror ladder:
  Antihydra v₂ of ×3/2 (constant budget), o4 v₃ of ×4/3 (growing budget), **o15 v₃ of ×8/3 (string budget)**.
- **Real-orbit confirmation:** v₃(2·289−5)=1 and v₃(2·2059−5)=2 predict the blank orbit's split runs exactly
  (2059→5485→14625 is the only double-split in 12 gates); the cascade law (§3) reproduces the 285M-step landing
  [3,1,1,14625]→[39015] by hand arithmetic: (8·14627+5)/3+8 = 39015.
- **Unconditional run cap** (given the grid laws): split-run ≤ log₃(2V); on the real orbit (V_n ≈ 39·(8/3)ⁿ),
  **≤ n·log₃(8/3)+O(1) ≈ 0.893n** — the o4 cap, with 8/3 in place of 4/3.

## 2. THE CORRECTION (this session) — the split drains the RIGHTMOST digit ≥3, not the leading
`[6,6,52]→[6,3,1,1,137]`, `[5,3,52]→[5,1,1,137]` (3 drains to 0 and vanishes), `[3,3,9,52]→[3,3,6,1,1,137]`,
`[9,5,2,52]→[9,2,1,1,6,133]`. The port's "leading drain" law (`O15_TEMPLATE_PORT` §2) holds only because its
grid shapes had the rightmost ≥3 digit in leading position. Consequence: the drain front approaches the queue
HEAD from the V-side, so a head [2,2] is exposed only when no digit ≥3 remains to its right — exactly the
buffer-language structure of §4.

## 3. The ρ=0 cascade laws `[PROVEN on the grids]` (`o15_fp_queue.py`)
Right-to-left from V: **≡1 digits are all absorbed** (V′=(8(V+Σd)+9−2k)/3 for k such digits — `[1]^k` exact for
k=0..8 at V=51 and 300, 18/18); **one ≡0 digit** absorbs as +8d/3 and the cascade continues, a second ≡0 digit
adds +d and STOPS (`[3,3,3,51]→[3,150]`, `[6,6,6,6,6,51]→[6,6,6,161]`); **≡2 digits** switch to an emission mode
(single d≡2: prepend 6, V′=(8(V+d)−19)/3, 10/10; each 1 to its left adds +2 to the emitted digit:
`[1,1,2,51]→[10,135]`; deeper ≡2 patterns emit `[1,1,1,4]`/`[2,1,1]`-type strings). ρ=2 is trivial: last digit
fuses, V′=(8V+11)/3+d_last (50/50).

## 4. The fatal cylinder is a string LANGUAGE, not a congruence (`o15_fp_cascade.py`, `o15_fp_buffers.py`, `o15_fp_confirm.py`)
Milestone `[2,2] + buffer + [V]`, single-generation fatality, all exact concrete runs (BUDGET-guarded):
- **V≡2: never fatal** (0 of all tested buffers). V≡1 and V≡0 both have infinite fatal families.
- **Hypothesis "fatal ⟺ buffer avoids factor 11" REFUTED** (20 mismatches at lengths 3–5; e.g. `[2,1,1]` fatal).
- Refined laws — V≡1: safe ⟺ buffer starts `[1,1]` and has no `22` factor; V≡0: fatal ⟺ a 2 in the first two
  digits — **predict-and-confirm 63/64 and 31/32 on unseen grids**, and the two misses are STRUCTURED:
  `[1,1,2,2,1,1]` is safe at V≡1 (an interior `22` is itself rescued by a following `[1,1]`) and `[1,1,2,2,2]`
  is fatal at V≡0 (the cascade tunnels through the 1s into a fatal `[2,2,2]`). So the exact law RECURSES — the
  fatal set looks regular (finite-state scan), NOT a finite cylinder list. **Refined laws also refuted as exact;
  kept as 94/96 approximations.**
- **Order matters, so no congruence can express it:** `[1,2,1,2,1,1]` (fatal) vs `[1,1,2,1,2,1]` (safe) have the
  same V, length, and digit multiset. Any buffer digit ≥3 protects that generation (17/17); a head digit ≥3
  protects, a head 1 does not (`[1,2,2,52]` HALTS).

## 5. [2,2]-formation and what the closed forms kill
- Literal 2s are created ONLY (in all observations) by split drains passing a ≡2 (mod 3) digit through 5→2;
  drains preserve mod 3; fresh digits enter as 6, 1, 4, or merges 6+2k — **≡2 (mod 3) digits require a 1s-merge
  with k≡1 (mod 3)** (a lead-14 was observed from single-block seeds, so the real orbit is NOT mod-3-protected).
- **The newborn pair is always buffered:** every observed [2,2]-assembly (`[2,5,2,52]→[2,2,1,1,6,133]`,
  `[2,5,52]→[2,2,1,1,137]`, `[2,5,1,370]→[2,2,1,1,1,985]`) deposits `[1,1]` — the safe cylinder — to its right,
  because the completing drain itself emits `[1,1]`. Natural-flow chase (19 queue seeds × 30 gens: **zero
  halts**; the wider 52-seed census assembled three [2,2]-heads, all born buffered, none fatal); 70 clean
  single-block seeds × 25 gens: zero leading 2s. Blank orbit (12 gates):
  queue alphabet so far {1,3,6} — no ≡2 digit has ever existed; exposure to date is ZERO with the first
  prerequisite (a ≡2 digit) not yet met.
- **Single-run kill** `[conditional on the §2/§3 rule inventory — grid-exact, not proven universal]`: within one
  split run from a 2-free queue, each split performs exactly one −3 drain, so head-pair assembly + the fatal
  split needs ≥3 split steps ⇒ **v₃(V−1) ≥ 3, i.e. V ≡ 1 (mod 27)** at the run start — fatality is gated on deep
  3-adic returns exactly as o4's multi-run conspiracy. NOT unconditional: assembly can also spread across runs
  (stuck 2s survive ρ=2 and buffered ρ=0 steps).

## 6. Where the closed forms BREAK (the task-4 pin) `[PROVEN by concrete instances]`
The first quantity that is not a finite-residue/valuation function of V: **V′ mod 3 after a single ρ=0 step.**
The `[1]^k` family gives V′=(8(V+k)+9−2k)/3 with V′ mod 3 of period 3 in k: states agreeing on V and on ANY
bounded queue window but differing in depth land in different branches. So no finite-residue δ-map and no
bounded-window transducer state can drive the itinerary. Minimal sufficient state: finite control (cascade mode
+ k mod 3 + the ≡0-digit counter of §3) scanned over the WHOLE queue — a regular transducer with integer
accumulators. o15's ledger is genuinely a string: the o4 theorem holds branch-wise, and the open content moves
from "return depth" (closed, §1) to "which branch" (queue-determined) + "pattern assembly" (§4–5).

## 7. Soundness ledger `[discipline]`
- Everything is exact concrete simulation (`run_gen`: guarded tape, budget status asserted — a BUDGET can never
  pass as "safe"; re-run with the guard was byte-identical). No acceleration anywhere; law-based predictions
  were only ever CHECKED against concrete runs, never substituted for them.
- REFUTED this session and kept: (i) "fatal ⟺ no 11 factor"; (ii) the refined §4 laws as exact (2 misses).
  CORRECTED: the port's leading-drain law (§2).
- Fatal configs are standalone; reachability from blank stays exactly OPEN (no natural-flow halt was found).
- o15 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`o15_fp_vmap.py` (branch extraction, fixed points, exhaustive run laws ≤2·10⁵, true-vs-scalar divergence) ·
`o15_fp_queue.py` (ρ=2/ρ=1/ρ=0 rule grids, censuses) · `o15_fp_cascade.py` (fatal-cylinder extent, `[1]^k`
impossibility, natural-flow chase, lead-digit table) · `o15_fp_buffers.py` (buffer language, lengths ≤5 + heads)
· `o15_fp_confirm.py` (predict-and-confirm on unseen length-6/5 grids). Basis: `O4_RUN_STRUCTURE_2026-07-07.md`,
`O15_TEMPLATE_PORT_2026-07-07.md`, `O15_REDUCTION.md`, `NEW_MATH_PROGRAM.md`. Not committed.
