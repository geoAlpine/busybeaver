# o18 depth-uniform attack — the 3-adic tower IS a closed-form pushdown odometer: complete single-defect transition table [PROVEN on grid], the "unclosed Collatz-irregular" branches all LAND (N=26, N=53 predict-confirmed), and the exact blocker is now a single object: the multi-defect word grammar (2026-07-07)

*Follow-up to `O18_TEMPLATE_PORT_2026-07-07.md`, executing the depth-uniform program (non-halt needs closure +
safety, NOT well-foundedness). Verdict: **(b) partial with the exact blocker pinned — and the sharpest state o18
has ever been in.** The entire branch tower collapses into ONE finite transition table on states
`D(m,t,e) = 0^∞ [F] 1^m 0 (10)^t 1^e 0^∞`, exact and grid-proven, with every previously-mysterious phenomenon
(depth irregularity, the mod-3^k branch laws, the ≡26/53 (mod 81) "non-closure") DERIVED or REFUTED-and-corrected.
o18 stays `[OPEN]`: the single-defect family has exactly one exit cell, the true orbit takes it (symbolically, at
tower-step 8394), and the multi-defect rewrite grammar beyond it is probed but not closed. No machine decided.*

## 0. The reframe this session executes
Halt ⟺ F reads 1 ⟺ D reads 1 with left-neighbour 1 `[PROVEN, prior]`. So o18 does not halt iff every reachable
step lies inside certified safe passages — **whether or not the descent recursion terminates**. The target is a
closed, level-uniform family of F-entry-to-F-entry passages, NOT a termination proof. This note delivers the
family and its transition laws at the single-defect level, and locates the exact closure gap.

## 1. The state space `[PROVEN on grid + all in-orbit data]`
Every F-entry (gate event) in every run observed today is one of:
- **clean reset** `C_N = 0^∞ [F] 0 1^{N-1} 0^∞`;
- **frontier form** `D(m,t,e) = 0^∞ [F] 1^m 0 (10)^t 1^e 0^∞` (head on the 0 left of the block, state F);
- **interior meet form** `1^2 0 (10)^T 1^k` (transitional, occurs inside level-entry and RECYCLE passages only);
- (beyond the exit cell, §5) **multi-defect words** `[F] 1^m 0 w`, `w` = 1-runs separated by single (once: double) 0s.
The prior note's "self-similar dirty-form ladder" is exactly the D(m,t,e) family; its (t,e) tail is a STACK.

## 2. THE TRANSITION TABLE `[PROVEN on grid; exact, zero exceptions, unsafe=0]`
Branch on `m mod 3` (`o18_depth_map.py`; grid m ∈ {6..29(floor scan), 30..32, 100..103, 301..303} ×
t ∈ {0,1,2,3,4,5} × e ∈ {1..12,14,15,18}, ~900 runs, every cell ONE outcome):

| cell | action | result |
|---|---|---|
| `m≡0`, `e≢2 (mod 3)` | **LAND** | `C_L`, `L = (8m+8e+6t+10)/3` if `e≡1`, `…+12)/3` if `e≡0 (mod 3)` |
| `m≡0`, `e≡2 (mod 3)` | **FLUSH** | `D((8m+8e+6t−19)/3, 0, 6)` |
| `m≡1`, `e ≥ 4` | **PUSH2** | `D((8m−5)/3, t+2, e−3)` |
| `m≡1`, `e = 3` | **PUSH** | `D((8m−5)/3, t+1, 1)` |
| `m≡1`, `e = 1` | **RECYCLE** | `D((8m−17)/3, 0, 2t+8)` (via one interior meet, `T=(m′−1)/2`) |
| `m≡1`, `e = 2` | **EXIT** | leaves the family: `((8m−17)/3, w=[2t+2, 6])` for t≥1; `((8m−23)/3, w=[4,1,1,1])` for t=0 |
| `m≡2`, `t > 0` | **POP** | `D((8m+14)/3, t−1, e)` (near-defect only; far tail untouched) |
| `m≡2`, `t = 0` | **LAND** | `C_L`, `L = (8m+3e+14)/3` |
Level entry: `C_N, N≡2 (mod 3) → D((8N−25)/3, 0, 6)` (grid N=8..119 step 3; spot checks N=998, 2003, 3002).
`C_N, N≡0,1 (mod 3) → C_{⌊8N/3⌋+2}` [prior note]. **Every halt-gate exposure in every run: safe. Zero halting
configs found anywhere (incl. the m=6..29 floor scan × all cells: NO small-parameter irregularity — unlike o4).**

## 3. Predict-and-confirm (o3 gold standard) — the "unclosed" branches all land
- **N=26** (the flagship "≥7 levels, no reset in 2.5·10⁸" claim of the prior note): table predicts the chain
  `61,0,6 →161,2,3 →434,1,3 →1162,0,3 →3097,1,1 →8253,0,10 → C_22038`. Concrete guarded run: **lands
  `C_22038` at step 105,994,679, unsafe=0**, every F-entry exactly as predicted. **The prior "no clean reset
  >2.5·10⁸" for N=26 is CORRECTED** (it lands; the old observation was a budget artifact).
- **N=53**: predicted `133,0,6 →353,2,3 →946,1,3 →2521,2,1 →6717,0,12 → C_17948`; concrete: **lands
  `C_17948` at step 70,313,821, unsafe=0**, chain exact.
- **D(8253,0,10)** standalone: predicted LAND `L=(8·8253+90)/3=22038`; concrete 91,083,071 steps ✓.
- **Batch 12/12 CONFIRMED** N ∈ {56,62,71,80,89,98,104,107,116,125,134,143}: full predicted F-chains
  (every intermediate (m,t,e) + landing L) vs fresh simulation (`o18_depth_confirm.py`), all exact, unsafe=0.
  Highlights: N=71→C_3428, N=80→C_3902, N=107→C_14029 (43.0M steps),
  **N=98→C_90744 (1,796,617,596 steps, 6-state chain)**, N=125→C_43772 (418.1M steps),
  **N=134→C_125526 (3,437,998,769 steps, 6-state chain incl. RECYCLE)** — the deepest exact
  predict-and-confirms in the o18 track.
- **All prior partial laws are compositions of the table**: `(64N−20)/9` = entry∘LAND(m≡0,e=6) (N≡2 mod 9 ⇒
  m₁≡0 mod 3); `(64N−104)/9` = entry∘LAND(m≡2,t=0,e=6); `(512N−1288)/27` = entry∘PUSH2∘LAND(m≡0,t=2,e=3)
  (N=8: 104 ✓);
  `(4096N−11618)/81` at N=80: entry∘PUSH2∘POP∘LAND = 3902 ✓ exactly reproduces the old mod-81 law.
- **Step counts are exactly quadratic per cell**: `steps = (4/3)m² + βm + γ` with cell-specific rational β,γ —
  fitted on three small m, **predicted and confirmed EXACT at m≈1000 for all 7 transition kinds** (POP, PUSH,
  PUSH2, RECYCLE, LAND₀, LAND₂, FLUSH). This is strong template-rigidity evidence.

## 4. Structure theorems (from the laws; one-line proofs)
- **Push renormalization fixed point**: PUSH/PUSH2 have `m′−1 = (8/3)(m−1)` exactly (integer fixed point m=1,
  o4's `x_ρ=−e` trick). Hence `v₃(m−1)` drops by exactly 1 per push and **a maximal push cascade starting at m
  has length exactly min(v₃(m−1), stack budget of e)** — the o4 run-structure theorem's mirror.
- **Depth is not `v₃(N+10)` and not any fixed 3-adic valuation — it is the stack excursion of (t,e) driven by
  the mod-3 itinerary of m under the affine maps.** The Collatz-irregularity of the prior note is thereby
  EXPLAINED, not merely observed: the tower is a **pushdown 3-adic odometer** — a finite rule table whose
  branch sequence reads m's 3-adic digits and whose depth is stack dynamics, exactly the o17-species unbounded
  recursion BETWEEN levels wearing o4's rigid arithmetic.

## 5. The exact blocker: the family has ONE exit, and the true orbit takes it
- `e=2` is reachable inside the family (RECYCLE→e=8, then PUSH2: 8→5→2 under consecutive `m≡1`, i.e. deep
  3-adic returns `m ≡ 1 (mod 27)`-style events). At `(m≡1, e=2)` the passage leaves D(m,t,e) into two-defect
  words (§2 EXIT row; laws exact on the grid, unsafe=0).
- **Symbolic orbit** (table iterated exactly from N=10, `o18_depth_symbolic.py`): generations 0..10 match the
  corrected orbit (…3890→27660→…→1,398,744→3,729,986 ✓); the orbit stays in-family for 8393 tower-steps
  (5157 clean generations, max stack t=8, max e=20, max tower depth 15) and **EXITS at tower-step 8394,
  generation 5157, from (t=5,e=2), m ≈ 10^3577**. The multi-defect regime is ON the true orbit (far beyond
  concrete simulation; statement conditional on the grid laws holding at all magnitudes).
- **Multi-defect probes** (`o18_depth_word.py`, 153 runs + battery): transitions stay lawful, unsafe=0, zero
  halts; 138/153 outcomes match prefix-locality predictions (POP consumes `[1]+X→X`; MERGE `[a≥2]+X →
  ((8m+3a+11)/3, X)`; PUSH2 carries X inert). The remaining 15 = one systematic new phenomenon each:
  (i) PUSH from v=3 with rest leaves a **double-0 separator** (`1^{j+2} 0 0 X`, m′ exactly (8m−5)/3 as
  predicted); (ii) `m≡0` passes are **compositional carry-cascades over the whole word** (e.g. `[8,6] →
  ((8m+57)/3, [1,1,3])`: near-flush constant `8v+6j−19` PLUS a fixed increment (+12) for the far block's
  push2-rewrite `[6]→[1,1,3]`) — lawful (one outcome per key across m) but the general schema is UNCLOSED.
- **The o18 decision therefore reduces to exactly this**: (a) close the general defect-word rewrite grammar
  (finite schema conjecture: POP/MERGE/PUSH-with-carry/RECYCLE/m≡0-cascade over words, incl. double-0 words);
  (b) certify each rewrite as a trace template uniform in ALL block-length parameters (o4 standard: episodes +
  sweeps + landmark pinning — sweeps over `1^k` and `(10)^k` regions are 2-transition-inductive, so this is
  plausible); (c) conclude non-halt by invariant closure + per-passage safety. NO termination argument needed.

## 6. Honest gap list (what is NOT done)
1. Template certification (pinning) is not done for ANY cell — laws are exact-on-grid `[PROVEN on grid]`, their
   extension to all m,t,e is `[OBSERVED/exact-fit]` (supported by the exact quadratic step laws and one-outcome
   uniformity, but the o4 red-team standard requires the pinning lemma).
2. The multi-defect grammar is open (the m≡0 cascade schema, double-0 words, and whether word length stays
   finite per pass — probes suggest yes: every pass ends in a lawful word or clean reset).
3. The symbolic-orbit exit statement assumes the laws at astronomical m (unverifiable concretely; that is what
   (1) would license).

## 7. Soundness ledger `[discipline]`
- **A detection bug was found and fixed in THIS session's own tooling**: the standalone prober initialized the
  span-scan bound at the head position, so tape content written-but-not-yet-visited was excluded — producing
  spurious "clean" landings (e.g. `D(257,3,1)` mis-reported LAND while in-orbit it POPs). Diagnosed by lockstep
  comparison (in-orbit vs standalone, step-for-step identical tapes); fix: `hi` covers the written config
  (`o18_depth_map.py`). **All tables above are post-fix; the in-orbit census was never affected** (its content
  is head-written), and the lockstep run doubles as an independent standalone≡in-orbit equivalence check.
- All confirmations are exact concrete simulation (guarded tapes, no acceleration). Predictions computed FIRST.
- unsafe=0 in every run of this session (~1000 runs incl. two >7·10⁷-step in-orbit landings); zero halting
  configurations anywhere, extending the "no fatal set" evidence to the D(m,t,e) grid and the word probes.
- Corrections to `O18_TEMPLATE_PORT_2026-07-07.md`: the "N≡26,53 (mod 81) run >2.5·10⁸ without reset /
  ≥7 recursion levels" items are SUPERSEDED (both land, §3); "depth Collatz-irregular `[OBSERVED]`" is upgraded
  to "stack dynamics `[derived from the table]`"; the mod-3^k laws table is subsumed as compositions.
- o18 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`o18_depth_census.py` (in-orbit F-entry chains; N=26 → C_22038 @105,994,679; N=53 → C_17948 @70,313,821) ·
`o18_depth_map.py` (the (m,t,e) grid + floor scan; the span-scan fix) · `o18_depth_word.py` (multi-defect
probes, 138/153 prefix-locality) · `o18_depth_symbolic.py` (symbolic machine; orbit exit at tower-step 8394) ·
`o18_depth_confirm.py` (batch predict-and-confirm incl. N=71→C_3428, N=80→C_3902) · inline: step-law quadratic
fits (7 kinds, exact at m≈1000). Basis: `O18_TEMPLATE_PORT_2026-07-07.md`, `O4_TEMPLATE_CLOSURE_2026-07-06.md`,
`O4_RUN_STRUCTURE_2026-07-07.md`.
