# o15 template port — the template closes and a GENUINE FATAL SET exists (leading `[2,2]` digit pair, predict-and-confirm PASSED); but the ledger is the whole base-3 DIGIT STRING (carry-cascade transducer, not a finite-residue δ-map): the B1 call survives in kind, sharpened in mechanism (2026-07-07)

*Porting the certified trace-template pipeline (`O4_TEMPLATE_CLOSURE_2026-07-06.md`, `O3_TEMPLATE_PORT_2026-07-06.md`,
`O17_HALT_FLAVOR_2026-07-06.md`, `O18_TEMPLATE_PORT_2026-07-07.md`) to **o15**
(`1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA`, blank tape; halt = A reads 1; spec confirmed identically in
`suite.py`, `O15_REDUCTION.md`, `CRYPTID_O17_O15.md`, `scratch_o15*.py`, `o15_orbit.py`). **Verdict: the old
B1/density call SURVIVES IN KIND but is materially REFINED** — o15 is *not* a bare Antihydra-style value orbit: it
has the full gate+template halves of the o4 decomposition AND an explicit, non-vacuous fatal set (the first
predict-and-confirm halting family outside o3), but its ledger coordinate is an **unbounded digit-block QUEUE**
processed by a carry cascade — a **string-ledger**, sitting strictly between o3/o4 (O(1)-counter ledger) and
Antihydra (raw integer). One of my own session laws was refuted by predict-and-confirm and is documented as such.
o15 stays `[OPEN]`. No machine decided.*

## 0. Ground truth `[PROVEN from table / verified concrete]` (`o15_ground_truth.py`)
- **Halt gate:** halt = `A,1`; A is entered ONLY by `F,1 → 1RA` (writes 1, moves R). So
  **HALT ⟺ F reads a 1 whose right neighbour is 1** (`11`-abutment at the F→A handoff) `[PROVEN from table]` —
  confirms `O15_REDUCTION.md` §1. Local safety condition: every F-read-of-1 has right neighbour 0. (Step 0 is an
  A-read of blank 0 — safe.)
- **Window census (concrete, 2·10⁷ steps, blank):** 10 gate events, **0 unsafe**; the radius-3/4/5 window census
  **saturates at TWO windows by step 107**: `111[1]F000` (right frontier) and `011 11[1]F 01010` (left frontier,
  `(10)*` context). Near-misses (F reads 0 with right nb 1): 4,369, all structurally safe. Second-sharpest
  saturation in the family (o18: 1; o3: 3/5/6; o17: 11). Gates fire ~once per generation (regular, geometric
  thinning with the ×8/3 epochs) — **NOT o17-sparse**.

## 1. Milestones — the complete state is a digit-block VECTOR `[OBSERVED, exact dumps]` (`o15_milestones.py`)
At every right-frontier gate the tape is EXACTLY `1^{b0} 0 1^{b1} 0 … 0 1^{V}` (single-0 separators, max
interior 0-run = 1 at all 11 blank-orbit gates to 2·10⁸ steps): a small-digit queue `D` + one huge active block
`V`. Blank orbit: `[39]→[107]→[289]→[6,765]→[2059]→[6,5485]→[3,1,1,14625]→…`. The milestone tape is exactly
`build(D,V)` — complete state, but of **unbounded arity** (contrast o3/o4/o18's O(1) counters).
**CORRECTION to the prior width story:** `W′=⌊8W/3⌋+2` (`O15_REDUCTION.md` §2, "clean scalar with carry
corrections") is NOT the complete-state map — the "corrections" (+1,+2,0,−1,0,−14 on the blank orbit) are exactly
the queue bookkeeping; the exact laws live in the block coordinates (below).

## 2. Generation template — RIGID `[OBSERVED on grid, exact; the o17 test passes]` (`o15_template_scan.py`)
Standalone `M(D,V)` run one generation (to the next right-frontier gate), token stream minimal-period-compressed
(p≤24) then level-2 shape-compressed (the o17 protocol):
- Grid: V=20..60 all residues, V=100..102, 200, 300, 500, 1000; queues up to depth 8; ~800 runs total, **unsafe=0
  on every landing run**. **ONE shape hash per class:** `ef67af7824` (no-split), `4e2824c6c2` (split, V≡1 mod 3,
  1 left mid-gate), `555f80efc2` (queue split), + two small-leading-digit anomalies (`222d13e98f` d=1,
  `70621919ad` d=2). **r exactly affine** (r=(V−2)/3-ish per class, +1 per +3 in V); steps quadratic (bouncer).
- **Anti-o17 check:** deep queues (`[1]*8+[51]`, `[6,6,6,6,6,51]`, `[3,1,1,·]`) reuse the SAME hashes — shape
  count does NOT grow with queue depth or generation. o15 is **not** template-free.
- Exact two-block landing laws `[PROVEN on the grids, 0 exceptions]`, e.g.: `[V]`, V≡2 → `[(8V+11)/3]`; V≡0 →
  `[(8V+9)/3]`; V≡1 → `[6,(8V−17)/3]`; `[d,V]`, V≡2 → `[d+(8V+11)/3]` (image fuses into the digit); V≡1, d≥3 →
  `[d−3, 1, 1, (8V−5)/3]` (leading drain −3, emit `[1,1]`; d≥4 keeps d−3, verified to queue depth 4:
  `[6,1,1,100]→[3,1,1,1,1,265]`, `[9,100]→[6,1,1,265]`). All 7 observed blank-orbit transitions reproduced
  exactly by these laws + direct standalone runs.

## 3. THE CORRECTION (my own, this session) — the δ-map is NOT end-local: predict-and-confirm FAILED
From the two-block V≡0 law I predicted `[3,1,1,14625] → [3,1,39005]`. **Actual (exact concrete, 285,426,444
steps, unsafe=0): `[39015]`** — the ENTIRE queue is absorbed. Follow-up grid: V≡0/V≡1 generations reprocess the
whole queue with digit-VALUE-dependent carries (`[1,1,51]→[143]`, `[2,1,51]→[6,137]`, `[1,2,51]→[8,135]`,
`[3,2,1,51]→[1,1,141]`, `[1]*8+[51]→[155]` full absorb, but `[6,6,6,6,6,51]→[6,6,6,161]` partial). So the
generation map is a **deterministic transducer over the digit string** (carry cascade), not a finite-residue
scalar δ-map. o4's `δ(G mod 3)` has no scalar analogue here; the honest closure target is the transducer's local
rule set `[OPEN]`. (Blank-orbit gen-11 landing `[39015]`: see §6 provenance note.)

## 4. THE DISCOVERY — a genuine fatal set, with passed predict-and-confirm (`o15_ledger.py`)
- **Standalone HALTING configurations exist:** `M([2,2],V)` HALTS for V≡0,1 (mod 3) — found `[2,2,52]`,
  `[2,2,100]`, `[2,2,2,51]`, …, `[2,2,2,2,2,52]` (halt steps 3,826–13,698); then **a-priori PREDICTED and
  CONFIRMED fresh members `[2,2,151]`, `[2,2,301]`, `[2,2,1000]` (halt at 1,336,398), `[2,2,2,150]`** — the o3
  gold standard. Controls as predicted: `[2,2,V≡2]` and single-`2` configs all land safely.
- The fatal pattern is the **literal leading digit pair `[2,2]`** (at a left-frontier drain), NOT its mod-3
  class: `[5,2,·]`, `[2,5,·]`, `[8,·]` all land safely (grid: all pairs 1..6 × 1..6 × 4 V-values, 9×46 two-block,
  small-V floor V=1..29 — only leading `[2,2…]` halts). Fatality is a LOCAL PATTERN in the digit string; the
  mechanism is the borrow cascade at the split-class leading-digit drain hitting two stacked 2s → separator
  deleted → `11`-abutment. (Standalone; NOT claimed reachable from blank tape.)
- **Small-V floor is NOT fatal** (V=1..29 with and without digits: 0 halts) — opposite of o3's k-floor.

## 5. Species verdict — the B1 call, re-examined through the template lens
| o4-decomposition piece | o3/o4 | o17 | o18 | **o15** |
|---|---|---|---|---|
| local halt gate, window-saturating | YES | YES | YES (1) | **YES (2, by step 107)** |
| rigid template prefix·body^r·suffix | YES | NO | YES/level | **YES — 5 shapes total, stable under queue depth** |
| complete O(1) counter state | YES | NO | YES (1) | **NO — complete state = unbounded digit QUEUE** |
| finite-residue δ-map / ledger | YES | NO | NO (tower) | **NO — digit-string carry-cascade TRANSDUCER** |
| standalone fatal configs | YES | family halters | NONE found | **YES + predict-confirm (leading `[2,2]`)** |
| drift/margin quantity | YES (huge) | none | none needed | **exposure record only: no leading 2 in 11 gens `[OPEN]`** |

**Does the B1/density call survive?** In kind, YES — sharpened: o15's non-halt statement is *"the base-3
digit string of the Mahler-8/3 orbit never develops a leading `[2,2]` at a split-class step"* — a **fixed local
pattern (cylinder) avoidance in the digit-string coordinate**, exactly Fork B1's shape and exactly the Erdős
ternary-digit existence facet `O15_REDUCTION.md` claimed by analogy. What the template lens ADDS: (i) the
dictionary "blocks = digits of the orbit" is no longer analogy-grade — the milestone state, the rigid template,
and the exact per-class laws are now measured/verified; (ii) the halt-set cylinder is EXPLICIT and NON-VACUOUS
(fatal configs + predict-confirm — Antihydra has nothing comparable); (iii) o15 is NOT o17 (template rigid, gate
regular, shapes finite) and NOT o18 (no recursion tower — every generation lands in one pass, ≤2 mid-gates).
Within the taxonomy o15 is a **fifth decomposition shape: template + STRING-LEDGER** — o3/o4's rigidity and
fatal-set structure, Antihydra's unbounded arithmetic state, fused. The residual `[OPEN]` conjecture is
equidistribution/genericity-flavored (does the carry cascade ever stack two 2s at the top?), i.e. (K)-adjacent —
the B1 census entry stands, now with the mechanism pinned.

## 6. Soundness ledger `[discipline]`
- Gate reduction: exhaustive table scan `[PROVEN]`. All landings/laws/halts: exact concrete simulation on
  standalone configs, GUARDED tape (raises near edges; o18 wraparound lesson), no acceleration anywhere.
- Fatal halts: each is a finite concrete run to the observed halt step `[PROVEN as configs]`; reachability from
  blank tape is exactly the open question — NOT claimed.
- Template rigidity/laws: `[OBSERVED/PROVEN on the stated grids]` (V≤1000, queue depth ≤8); episode-landmark
  pinning at the o4 red-team standard NOT yet run on o15's sweeps — the natural next step, as for o18.
- §3 documents a REFUTED session hypothesis (end-local absorption law) — kept per zero-false-proof discipline.
- Provenance: blank orbit raw-concrete to 3.4·10⁸ steps (12 gate events, all milestones cell-exact, unsafe=0,
  max interior 0-run = 1 throughout). **Standalone ≡ real confirmed at the deepest point:** the blank orbit's
  gen-11 milestone (step 332,166,743) is EXACTLY `[39015]`, identical to the standalone `[3,1,1,14625]` landing
  (285,426,444 steps; the 1-step delta to the blank gen count is the F→A gate-step convention).
- o15 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`o15_ground_truth.py` (gate + 20M census) · `o15_milestones.py` (blank-orbit milestone dumps + width-law audit;
arg = step budget) · `o15_template_scan.py` (standalone generation runner, template shapes, landing-law grid;
args = comma-separated block vectors) · `o15_ledger.py` (fatal-set hunt, ~900 configs). Inline (§3/§4):
predict-confirm runs. Basis: `O4_TEMPLATE_CLOSURE_2026-07-06.md`, `O3_TEMPLATE_PORT_2026-07-06.md`,
`O17_HALT_FLAVOR_2026-07-06.md`, `O18_TEMPLATE_PORT_2026-07-07.md`, `O15_REDUCTION.md` (§2 width story corrected
here), `CRYPTID_O17_O15.md`, `B2_DECISION_FORK_2026-07-05.md` (B1 entry refined here). Not committed.
