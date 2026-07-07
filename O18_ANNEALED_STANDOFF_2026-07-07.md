# o18 "probviously halting" made PRECISE — the annealed (i.i.d.-residue) model over the exact transducer: the renewal structure makes the fatal-entry probability a CONSTANT per generation, the margin drift is positive with ruin η ≤ 3/8, itinerary-exhaustive safety extends 16 → 56 passes, and the margin-aware annealed model still predicts HALTING — the standoff is determinism vs randomness, not margins vs counting (2026-07-07)

*Quantifies the halting side of the `O15_O18_IDENTITY_2026-07-07.md` §4 standoff. Everything below is
labeled `[EXACT given T]` (a consequence of the grid-proven transducer `o18_md_rules.py`, no
probabilistic assumption) or `[MODEL]` (the annealed heuristic: true residues m mod 3 replaced by
i.i.d. uniform; NEVER a proof claim about the machine). Headline: the margin bookkeeping does NOT
flip the annealed prediction to non-halting — it explains the halting TIMESCALE (~10^41 generations,
m ≈ 10^(10^41)) and why 122,015 clean generations carry no evidence either way. No machine decided.*

## 0. The model and the renewal theorem
**[MODEL definition]** Keep the exact pass map `T(m mod 3, w)` (`o18_md_rules.py`, zero splits,
900/900 full-chain confirms) and the exact clean-step; replace the residue sequence by i.i.d.
uniform on {0,1,2}. **[EXACT given T]** Every dirty generation is seeded at the SAME word: clean
`N ≡ 2 (mod 3)` → `(m', ((1,6),))` (`clean_step`, `o18_md_orbit.py`). Words never persist across
generations (every excursion ends in a clean LAND). Hence under ANY i.i.d. residue model the
generations are i.i.d. trials and the per-generation fatal-entry probability is a **constant**
`p* = P(excursion tree from ((1,6),) reaches a fatal cell)`. **There is no Borel–Cantelli race in
o18's annealed model** — margins cannot accumulate across generations because the clean reset wipes
the word; the Task-1 dichotomy collapses to: `p* > 0` ⇒ halts a.s. in ~Geom(p*) generations;
`p* = 0` ⇒ never halts. `p* = 0` is EXACTLY the all-itinerary form of the reachability invariant.

## 1. p* — bounds and structure
- **Itinerary-exhaustive safety to depth 56 `[EXACT given T]`** (`o18_ann_dp.py`): probability-mass
  BFS with prune 1e-28 < 3^-58 and state cap never binding (max 38,289 states) enumerates ALL
  residue itineraries from `((1,6),)` up to length 58. Result: **halt mass = 0; no fatal itinerary
  of length ≤ 56 exists at all** (extends `o18_md_witness.py`'s exhaustive depth 16). First
  `Unknown` R₁-fractal cell only at depth 57 (subtree mass ≤ 9.5e-23); caveat applies to 57–58 only.
- **Upper bound `[MODEL]`**: at depth 80, `p* ≤ live + unknown + pruned = 5.1e-16`.
- **Monte Carlo `[MODEL]`** (`o18_ann_mc.py`): 3,000,000 excursions from the renewal seed +
  600,000 from 11 exit-cone/danger seeds: **0 halts, 0 unknown cells, 0 adjacent-2 passes**;
  excursion survival is geometric (mean length 1.916, P(len ≥ 32) = 6.7e-7).
- **Two-2 words ARE itinerary-reachable `[EXACT given T]`** (`o18_ann_wit.py`): explicit
  replay-verified itineraries of length 55–56 (e.g. `1111121212221112221112221112111222111222111222111111211`)
  reach words with two `(1,2)` blocks — but ALWAYS units-GAPPED (gap 8–9; first such state at depth
  51). Exhaustive kill-search (≤ 25 further passes, 300k states) finds NO halt from any of them:
  PUSH preserves the units-gap in front of a tail 2, so gapped double-2s cannot close to the fatal
  shape. The only fatal entrances are **gap-0**: `(1,2)(1,2)` adjacency or the armed precursor
  `(1,v≡2 mod 3,v>2)(1,2)` — and their DP occupancy is **exactly 0 through depth 56 (0 at 1e-28
  granularity through depth 80)**.
- **Lower bound (external)**: the community's fatal residue windows (length ~110, `2^13·3^15`
  variants; Lean-verified halting congruence class mod 3^108, per `O15_O18_IDENTITY` §2) give — IF
  the class is rooted at clean states — `p* ≈ 2^13·3^15/3^110 = 3.9e-42 > 0`, safely below every
  search horizon above (ours and the prior beam-70). **Checking how that Lean class is rooted is
  the single decisive external verification**: clean-rooted ⇒ the ALL-itinerary invariant is FALSE
  and only an orbit-specific (arithmetic) invariant can survive.

## 2. Margin drift and ruin `[MODEL, exact ingredients]`
- Per-pass rates at the leading edge (renewal seed, 5.7M passes): `f_PUSH = 0.290` (+2 units),
  `f_POP = 0.131` (−1 unit) ⇒ **drift +0.449 units/pass**; drained danger seeds still +0.13.
  Positive everywhere tested.
- 2-birth margin = `2(v−2)/3` + inherited escort: observed min 2, mean **5.68** per birth
  (rate 1.17e-3/pass).
- Ruin constants (probability per unit of margin that draining beats escape):
  bare fatal family **exact**: `ruin(1^M [2,2]) = (4/9)·3^(1−M)`, i.e. **η = 1/3** (DP matches to
  1e-11); armed precursor family `1^M (1,5)(1,2)`: **η → 3/8**; analytic skip-free-walk band
  0.15–0.36. All η ≤ 3/8 < 1 ⇔ positive drift.
- **The suppression cascade per generation**: 2-birth 1.2e-3 → lone 2 at escort ≤1: 8.8e-5
  (harmless alone — every residue kills a naked leading 2) → two 2s in one word (gapped): 5.7e-20 →
  gap-0 fatal entrance: 0 to depth 56 → community fatal windows: 3.9e-42. Margin bookkeeping is a
  ≥ 10^37 suppression of the naive danger rate, not a barrier.

## 3. The true orbit vs the model `[EXACT census, o18_ann_margin.py]`
200,000 tower-steps (m ≈ 10^85194, 122,015 generations, 77,985 dirty passes): true residues
0.3300/0.3345/0.3354 (uniform to 3 decimals); mean excursion length **1.918 vs model 1.916**;
153 lone-2 passes (model predicts ~90 exposed excursions × ~1.7 passes ≈ 153 — match); escort
distribution matches the model's; **orbit margin M: min escort of any 2-block ever = 0** (lone,
harmless), min protected margin of any v≡2 block = 2, **max 2-train = 1 ever** (never two 2s in one
word, gapped or not; the fatality-relevant deficit is adjacency, not escort). The orbit is
statistically indistinguishable from an annealed sample on every functional measured — no sign of
anomalous protection, and none needed: expected gapped-double-2 count by now ≈ 7e-15, expected
halts ≈ 4.7e-37.

## 4. Reconciliation — what actually separates the two positions
- **Margin-blind counting (community)**: fatal-window density δ ≈ 3.9e-42 per generation, i.i.d.
  residues ⇒ halt a.s.; expected ≈ 2.6e41 generations ≈ 4.2e41 tower-steps ⇒
  **m_halt ≈ 10^(1.8·10^41)** (iterated exponential, second level), TM halt time ~ 10^(3.6·10^41)
  steps. The observed clean run to m ≈ 10^85194 = 10^(10^4.93) is ~5e-37 of the way — the orbit
  data cannot discriminate.
- **Margin-aware annealed (this note)**: same conclusion, halting a.s., with
  3.9e-42 ≲ p* ≤ 5.1e-16 — margins RESCALE δ, they do not zero it, because the renewal resets the
  protection every generation. **The anticipated "positive drift ⇒ annealed non-halting" resolution
  FAILS**: drift is positive (+0.45/pass) but drift protects only within an excursion; excursions
  are re-drawn i.i.d. forever.
- **The genuinely separating assumption**: whether the true 3-adic residue sequence realizes its
  annealed statistics forever (community: yes ⇒ halt) or is arithmetically correlated so that gap-0
  entrances never form (our invariant direction ⇒ never halt). Both randomized readings halt; the
  push-margin invariant can only be true as an **o4-odometer-shaped arithmetic theorem about the
  actual orbit**, not as a probabilistic or all-itinerary statement (all-itinerary form: open at
  ≤ 56 exact, and refuted at ~110 if the community's Lean class is clean-rooted).

## 5. Soundness ledger `[discipline]`
- All dynamics via the grid-proven `T`; no new rule extraction. MODEL results never cited as
  machine facts; the two [EXACT given T] items are itinerary statements (depth-56 exhaustive
  safety; witness replays), inheriting T's `[PROVEN on grid]` status and the laws-at-magnitude
  caveat for §3.
- Positive controls: the DP reproduces the exact bare-family ruin `(4/9)·3^(1−M)` to 1e-11 and
  halts correctly from armed precursor seeds (`(1,5)(1,2)`: ruin 4.94e-2) — the zero from orbit
  seeds is not an artifact.
- Unknown R₁-fractal subcells: total annealed mass ≤ 9.5e-23 (first at depth 57) — bounded, not
  resolved; included in every upper bound.
- The community-side numbers (window length ~110, count 2^13·3^15, Lean class mod 3^108) are taken
  from `O15_O18_IDENTITY_2026-07-07.md` §2 as external inputs, not re-derived; the clean-rooting of
  the Lean class is flagged, not assumed, wherever it matters.
- o18 stays `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`o18_ann_mc.py [seed] [trials]` (annealed MC + event rates + 2-birth margins) ·
`o18_ann_dp.py [maxdepth]` (mass DP: p* bounds, danger occupancies, gap-0 tracking, ruin families,
analytic η) · `o18_ann_wit.py [maxdepth]` (path-tracked DP → adjacent-2 witnesses → replay → kill
search → CRT realization hook) · `o18_ann_margin.py [steps]` (instrumented true orbit: residue
histogram, 2-block escort/gap/train census, orbit margin M).
Basis: `O18_MULTIDEFECT_2026-07-07.md`, `O15_O18_IDENTITY_2026-07-07.md`, `o18_md_rules.py`,
`o18_md_orbit.py`.
