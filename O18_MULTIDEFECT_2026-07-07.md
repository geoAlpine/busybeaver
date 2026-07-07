# o18 multi-defect grammar CLOSED as a transducer — and the first FATAL CELLS in the o18 track: the word space contains genuine halting configurations, the exit cone empirically never reaches them, and the o18 decision reduces to ONE reachability invariant (the push-margin law) (2026-07-07)

*Executes the `O18_DEPTH_UNIFORM_2026-07-07.md` §5 program: close the general defect-word rewrite grammar
beyond the single-defect exit cell. Verdict: **the transducer is extracted and closed operationally**
(zero splits, 900/900 full-chain predict-and-confirms including 26 predicted halts), **but the hoped-for
"closure + safety, no arithmetic" decision is DEAD in its naive form**: the multi-defect word space
contains genuine fatal cells — the first ever found for o18 — and closure under *adversarial* residue
itineraries reaches them. Every *exact* search (2.1M exhaustive flights, exhaustive itineraries to depth
16, danger-guided beam to depth 70, the true orbit continued 24× past its exit) finds the fatal region
UNREACHABLE from the exit cone. o18 stays `[OPEN]`; the blocker is now a single sharply-stated
reachability invariant. No machine decided.*

## 0. State space `[PROVEN adequate on all data]`
General anchored state: `0^∞ [F] 1^m 0^{s_1} 1^{b_1} 0^{s_2} 1^{b_2} … 0^{s_k} 1^{b_k} 0^∞`, head left of
the leftmost 1, state F; encoded `(m, w)`, `w = ((s_i, b_i))_i`, `s_i ≥ 1`, `b_i ≥ 1`. A **pass** =
anchored-F-entry → next anchored-F-entry (interior meets skipped). `D(m,t,e) = (m, (1,1)^t (1,e))`;
clean reset `C_N = (N−1, ())`-ish as before. **Separators are unbounded**: a `v=3` PUSH increments the
following separator (`3.0|b → [1,1,(3,b)]` observed, s up to 4 exercised); all rules handle general s.

## 1. THE TRANSDUCER `[PROVEN on grid; zero splits; exact]` (`o18_md_probe.py`, `o18_md_rules.py`)
One outcome per `(m mod 3, w)` — **3075-run grid + ~1500 targeted probes + fuzz, zero splits anywhere**.
`m' = (8m+c)/3` with `c = c(m mod 3, w)`. Complete schema (T in `o18_md_rules.py`; j = leading units):
- **r=2**: `1^1` alone → LAND c=17; `(1,1)+X` → POP c=14; `(1,a≥2)` → LAND c=3a+14; `(1,a≥2)+X` → MERGE
  c=3a+11, X inert; `(s≥2,b)+X` → c=11, `(s−1,b)+X` (separator decrements).
- **r=1**: all-units → RECYCLE c=−17, `[2j+6]`; `1^j(s≥2,b)+X` → c=−17, `[2j+6]⊕_{s−2}b + X` (⊕₀ =
  block merge); `1^j(1,v≥3)+X` → PUSH c=−5, `1^{j+2} + pushtail(v,X)` (`pushtail`: v>3 → `(1,v−3)+X`;
  v=3 → X with first separator +1); `1^j(1,2)+X` → the recursive R₁ region (below).
- **r=0**: all-units → LAND c=6j+12; `1^j(2,b)+X` → LAND c=6j+3b+12 / c=6j+3b+9 with `w'=X`;
  `1^j(s≥3,b)+X` → c=6j+9, `(s−2,b)+X`; `1^j(1,v)`, no tail → LAND c=6j+8v+10/12 (v≡1/0 mod 3) or FLUSH
  c=6j+8v−19 → `[6]` (v≡2); **`1^j(1,v)+X` → DELEGATION: c = 6j+8v−2 + c′, `w' = w′` where
  `(c′,w′) = T((v+2) mod 3, X)`** — the m≡0 "carry-cascade" of the prior note is EXACTLY a recursive
  delegation of the tail to the branch `(v+2) mod 3`; FLUSH is its base case (empty tail = RECYCLE j=0).
- **R₁ region** (`r=1`, `w = 1^j (1,2) X`): a recursive descent with margin-dependent HALTS:
  units tail → `[2j+2, 2p+6]` (j≥1, c=−17) / `[4,1,1,1,(1,2p)]` (j=0, c=−23); gap tail `(s≥2,b)` →
  separator-decrement templates; `1^p(1,v≥3)` tail → `[2j+6] 1^{p+2} pushtail(v,·)`;
  `X=(1,2)+Z` (**adjacent 2s**): inner := R₁ on `(1,2)+Z`: inner-HALT → HALT; inner c=−23 → `[2j]+inner`
  for j≥2, **HALT for j≤1**; inner c=−17 → `[2j+2]+inner` (j≥1), special `[4,1,1,1,(2,1)]…` template
  (j=0); `X=1^p(1,2)+Z` (p≥1) → delegation `[2j+2]+R₁(1^p(1,2)Z)` (j≥1), `h_p` templates (j=0, pinned
  p=1,2,3). Deep fractal subcells (`h_{p≥4}`, some j=0 nestings) raise `Unknown` — none is reachable in
  any exact run below.

## 2. Validation — the o3 gold standard (`o18_md_rules.py` fuzzers)
- **Single-pass fuzz**: 3588/3588 exact vs fresh concrete simulation (random words, blocks ≤9, seps ≤3,
  len ≤6, m ∈ 3 magnitudes × all residues), **0 mismatches, 0 unknown cells**.
- **FULL-CHAIN predict-and-confirm: 900/900** — complete symbolic pass-chains (every intermediate
  `(m,w)` + landing `L` or HALT) vs fresh concrete runs, **including 26 predicted-HALT chains confirmed
  step-for-step**. Landings up to `L = 5,344,782,364` (m'≈2·10⁹) exact.
- T restricted to `D(m,t,e)` reproduces the PROVEN single-defect table + exit law on 4000 random cells
  (m to 10¹², t≤8, e≤24) — 0 discrepancies.
- unsafe=0 on every non-halting pass everywhere (~10⁶ concrete passes this session).

## 3. THE DISCOVERY — o18 HAS fatal configurations `[PROVEN, verified concrete]`
`(m≡1 mod 3, w=[2,2])` **HALTS** (m=40,43,46,100,301,…; the halt is the gate: D reads 1 with left-1,
unsafe=1 then halt). The fatal sub-language is exactly the R₁ adjacent-2 recursion bottoming out at
margin j≤1: `1^j 2 2 Z` halts for j≤1 unless rescued by a `v≥3` block right after; deeper 2-trains
(`2 2 2 Z`) halt at ALL j; all other residues funnel into these (e.g. `[2,2,2]` halts within ≤2 passes
from every m mod 3). **This kills the prior "no fatal set anywhere" picture** (`O18_TEMPLATE_PORT` §5,
`O18_DEPTH_UNIFORM` §2 grid): those searched only `B(m,e)`/`D(m,t,e)`/single-word families — the fatal
set lives strictly in the multi-defect regime. o18 is therefore NOT the "nothing fatal exists" species;
it joins o3/o4 in having a genuine fatal region, entered only through words with two adjacent 2-blocks
at low unit-margin.

## 4. Reachability — the fatal region vs the exit cone
The single-defect family's ONE exit (`(m≡1,e=2)` cell) emits `[2t+2, 6]` (t≥1) / `[4,1,1,1]` (t=0).
From these:
- **Exhaustive small-m**: every m ∈ [6, 300000] × 7 exit shapes, full flights (≤400 passes):
  **2,099,958/2,099,958 LAND on clean resets. Zero halts, zero unknown cells.**
- **Exhaustive itineraries**: exact 3-adic DFS (m as CRT-refined congruence class, `o18_md_witness.py`):
  ALL residue itineraries to depth 16 from all exit shapes — **every branch LANDS**; no halt, no unknown.
- **Danger-guided beam search** (120k beam, depth 70, score = 2-blocks × inverse margin + ≡2-mod-3
  cascade potential): **no halt, no unknown found**; danger peaks at lone-2 states (`1^{≤1} (1,2) (1,big)`)
  and decays — the second 2 never forms in reach of the first.
- **Precursor census**: in ~10⁶ exhaustive flights, NO reachable word EVER contains two 2-blocks
  separated only by units — nor even the precursor `(v≡2 mod 3, v>2) 1^* (1,2)`. `[OBSERVED, 0 exceptions]`
- **BUT adversarial closure fails abstractly** (`o18_md_closure.py`): with values/trains abstracted
  (exact ≤12 / mod-3 classes), BFS from the exit cone under arbitrary per-step residues reaches 10
  abstract HALT cells and does not close (200k states). The abstraction loses the correlation that
  protects the exact system, so it can neither prove safety nor exhibit a real witness.
- **The protection mechanism (the margin law)** `[derived from the rules, not yet an invariant proof]`:
  an exact 2-block is only created by pushing a `v≡2 (mod 3)` block down (v→v−3→…→2), and each push
  prepends 2 units — so a fresh 2 carries `≥ 2(v−2)/3` units of left-margin; margins drain only 1 per
  POP; and the fatal cells need TWO exact-2s adjacent at margin ≤1. Every exact search above is
  consistent with this being a theorem; the abstract escape paths all violate its bookkeeping.

## 5. The TRUE ORBIT continued (`o18_md_orbit.py`) `[conditional on the laws at magnitude]`
The symbolic orbit from N=10 — which exits the single-defect family at tower-step 8394 (m≈10³⁵⁷⁷) — now
CONTINUES through the multi-defect regime with exact big-int arithmetic: **200,000 tower-steps —
24× past the old horizon — m ≈ 10⁸⁵¹⁹⁴, 122,015 clean generations, zero halts, zero unknown cells,
max word length 13 blocks, max separator 1 (no double-0 ever occurs on-orbit), never two adjacent
2-blocks**. Multi-defect excursions (60k-step census): 4696, all brief (the genuine
beyond-D words are the exit products and 1–3 descendants before MERGE/LAND re-absorbs them). The orbit
is nowhere near the fatal region at any point.

## 6. Honest gap list — why this is NOT a candidate decision
1. **The reachability invariant is unproven.** The chain entry→single-defect→exit→transducer→safety
   needs "fatal cells unreachable from the exit cone" as a THEOREM. Evidence is massive (§4) but a
   closed inductive invariant is missing: the naive "no two units-separated 2s" is not inductive
   (PUSH 5→2 can create the second 2 if a 2 already waits in the tail — exact dynamics never lets the
   precursor form, but proving THAT is the same problem one level up). The right statement is a weighted
   margin/potential inequality (§4 last bullet). **This is the exact blocker, and it is o4-ledger-SHAPED:
   a one-sided condition along the orbit's own itinerary — but unlike o4's (K)-shaped razor, here every
   probed itinerary satisfies it with enormous margin, and it may even hold for ALL itineraries (depth-16
   exhaustive + beam-70 found no counterexample at any residue choice).**
2. Transducer uniformity in parameters is `[PROVEN on grid + fuzz]`, per-rule template certification
   (o4 pinning standard) not done; deep R₁ fractal subcells (`h_{p≥4}` etc.) remain `Unknown` — never
   reached by any exact run, but they must be closed or proven unreachable for a certificate.
3. True-orbit continuation assumes the laws at astronomical m (as before).
4. The abstract closure needs either a finer domain (carrying the margin potential) or a different
   proof shape (well-founded potential argument per excursion).

## 7. Soundness ledger `[discipline]`
- All rules extracted from exact concrete simulation of standalone configs (guarded tapes, span-scan
  covers written content — the `O18_DEPTH_UNIFORM` fix inherited); predictions computed FIRST everywhere.
- Probe attribution bug found & fixed in THIS session's tooling: the first prober returned HALT for
  runs that halted in a LATER pass (after lawful anchored entries); fixed to per-pass attribution
  (`o18_md_probe.py`); all tables above post-fix. Multi-pass halts are compositions of lawful passes
  ending in a genuine fatal cell (verified: `[2,2,2]` from m≡2 MERGEs then halts at `(m'≡1,[2,2])`).
- One flagged "UNSAFE-NONHALT" was this same multi-pass attribution effect, not a gate violation:
  unsafe events occur iff the run halts (gate reduction intact).
- HALT claims: 26 predicted halting chains confirmed by fresh concrete simulation (step-exact);
  standalone fatal cells verified at 5+ magnitudes each. NOT claimed reachable from o18's blank tape —
  reachability is exactly the open invariant (§6.1).
- o18 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`o18_md_probe.py` (general-word prober + 3075-run grid; zero splits) · `o18_md_rules.py` (the transducer
T + R₁; single-pass and full-chain fuzzers: `python o18_md_rules.py <seed> <nwords>`) ·
`o18_md_orbit.py` (`orbit N` = true-orbit continuation; `mc` = random-large-m flights) ·
`o18_md_closure.py` (abstract adversarial-residue BFS) · `o18_md_witness.py` (exact 3-adic itinerary
DFS; depth 16 exhausted, all LAND) · inline: exhaustive small-m flights, precursor census, beam search.
Basis: `O18_DEPTH_UNIFORM_2026-07-07.md`, `O18_TEMPLATE_PORT_2026-07-07.md`,
`O4_TEMPLATE_CLOSURE_2026-07-06.md`.
