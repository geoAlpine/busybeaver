# Session index — 2026-07-06: o4's tightest reduction — one localized odometer lemma inside a fully-proven structure

*Picked up the top actionable remaining thread (the o4 base-4/3-odometer 11-avoidance theorem — decidable-in-principle,
unlike the `(K)`-hard `(K)` kernel which awaits external outreach). Multi-angle parallel assault (bounded-cascade-width
+ AFS-numeration subagents + structural block-count). Net: o4 reduced from "finite boundary-graph, counter-dependent
branching" (2026-07-05) to **a single precisely-localized parity lemma inside a PROVEN bounded-defect structure**. Zero
false proofs; one unsound accelerator caught and discarded. o4 `[OPEN]`; no machine decided.*

## The advance (`O4_WINDOW_SATURATION_2026-07-06.md`)
1. **Reframe `[PROVEN logic]`:** o4 non-halt ⟺ every `B`-reads-`1` has right-neighbour `0`. Only `B`-reads-`1` windows
   are halt-relevant; the turn-4 `0/25` "no finite shortcut" is about branch PREDICTION — **orthogonal to safety**. So
   decision ⟺ the set `S` of `B`-reads-`1` local windows is finite + complete + all-safe.
2. **Saturation `[OBSERVED]`:** `S` saturates at every radius (|S|=8/23/45/69 at r=3/5/7/9), all SAFE, to 200M steps /
   G≈19,566 / 49.9M events — and to **G≈15,509 / 3.25×10¹⁰ events** via the subagent's tooling. |S| grows with radius,
   never with G = a bounded-width traveling disturbance.
3. **PROVEN structure:** (i) uniform-interior **sweep lemmas** (`B1F0` read-only rightward, `D1E0` leftward invert);
   (ii) the tape is always `0^G · uniform(10)-regions · D`, with `D` = **≤4 defect runs, each length exactly 2**
   (`[(1,2),(0,2),(0,2),(0,2)]`) ⇒ finite G-independent window set; (iii) **HALT-in-closure impossibility** — the
   background-agnostic (free-incoming-cell) closure contains HALT at radius ≤5 (reproduced), so no local sofic
   certificate works and the incoming/seam-parity bit is **load-bearing**.
4. **Invariant corroboration `[OBSERVED]`:** milestone form `(10)^a1001` preserved; odometer `G↦⌊4G/3⌋+c(G mod3)`,
   `c={0→3,1→5,2→1}` **exact to G=11,799** (prior: G=206).
5. **AFS-numeration `[PROVEN-in-lit]`:** the base-4/3 odometer is an Akiyama–Frougny–Sakarovitch object; three theorems
   (non-regular/non-CF digit language; order & mod-q not p/q-recognisable; only equidistribution closures) EXPLAIN every
   finite/regular/residue wall. **Orthogonality:** non-regularity governs the digit-string/branch order, NOT the tape's
   bounded-width factors — so it does not pre-empt the window-closure route. Verdict (b): sharpens, does not close.

## The single remaining obligation (`[OPEN]`, Collatz-type)
The **incoming-cell / seam-parity predictor:** the odometer `G↦⌊4G/3⌋+c(G mod3)` never desynchronizes the seam parity
into a `B`-reads-`11`, for all `G`. All of closure sits here; the impossibility result proves it is irreducibly a
carry-cascade theorem (no finite certificate). This is o4's tightest reduction to date.

## Soundness ledger
Zero false proofs; zero false decisions. One **unsound accelerator caught and discarded** (`o4_accel_windows.py`, phase
bug: disagreed with concrete sim by 9 windows) — per zero-false-proof discipline, concrete simulation used as ground
truth throughout. Decisive impossibility computation independently reproduced. o4 `[OPEN]`. No machine decided. No label upgraded.

## Part 2 — the two follow-on tasks (user-requested: prove the lemma + build the macro-machine)
- **(1) incoming-cell / seam-parity lemma — MAJOR PARTIAL PROVEN (`O4_SEAM_PARITY_LEMMA_2026-07-06.md`):** the feared
  odometer-desync mechanism is **REFUTED** — every gap-edge (cascade) seam is E-type and safe by the unconditional
  4-step `D→E→A→B` chain (`D:1→0LE` unique E-entry; zero odometer dependence) `[PROVEN, re-verified]`. Residual
  `[OPEN]`: the once-per-generation `1001`-cap C-seam (bounded cap-crossing, ~log G occurrences), contingent on
  uniform-interior alternation through the cascade. o4 = finite proven structure + one bounded cap-local claim.
- **(2) sound accelerated macro-machine — BUILT, VALIDATED, and RUN TO G≈884k (`o4_bouncer_macro.py`).** Foundations:
  `o4_accel_probe.py` (validated accel==concrete & probe==pure-concrete), `o4_macro.py` (faithful RLE, 200k exact). KEY
  FINDINGS: steps-to-gap-`G` ~ **½G²**; one generation = **triangular BOUNCER** (~G/4 growing sweeps) + **odometer reset
  (G mod 3)** — the reset is why o4 escapes existing bouncer/cycler deciders. Final tool: segment tape + generic
  VERIFIED p=2 cycle jumps (behind/ahead tiling checks; phase bug structurally excluded). **Validation: V1 exact
  tape/state/head equality at 200k/1M/5M; V2 window-set exact equality over 32M (23==23).** **PRODUCTION:
  5.003×10¹¹ steps in 587s (~×1,800), G=3→883,719, 40 milestones, odometer EXACT on all 39 transitions, window set
  = canonical 23 exactly, UNSAFE=0, F-reads-1=0.** Closure evidence ×45 in G; C-seam instances ~40 generations all
  safe. Development soundness ledger: 3 detector/representation bugs found & fixed via validation (seg fragmentation
  → rephasing rules; "00"-pattern first1 miscount → canonicalization; milestone timing → per-micro check +
  record-breaking-G filter); tape equality re-verified after each fix. Reusable B2-cryptid template (o3/o15/o18).

## Part 3 — the "next move": template closure + the a-ledger discovery (`O4_TEMPLATE_CLOSURE_2026-07-06.md`)
The cap C-seam move escalated into the o4 track's sharpest result:
- **Rigid template:** every generation = prefix(454, one hash ∀gens) · body(51)^r · suffix(G mod 3); turn-4's `0/25`
  counter-dependence = template-position projected out.
- **Certified lemmas `[PROVEN, certified trace-template method]`:** PREFIX = fixed 471-step word (span [−11,30], all
  G≥37, all a); BODY = `B(k)→B(k+2)` in 15+4k steps, all odd k≥19 (verified to k=251); SUFFIX per class g∈{3,4,5}:
  exact milestone landing, `G′={2k+12, 2k+9, 2k+13}`, `a′={a−1, a+4, a+6}`, valid a≥2 (g=3) / a≥0 (g=4,5).
- **Odometer DERIVED:** `G′=⌊4G/3⌋+c`, `c={0→3,1→5,2→1}` falls out of the templates (matches real orbit).
- **THE DISCOVERY — the a-ledger:** `a′=a+δ(G mod 3)`, `δ={1:−1, 2:+4, 0:+6}`; **`Z(41,g=3,a=0)` genuinely HALTS**;
  o4 non-halt ⟸ ledger stays ≥2 at every G≡1 generation `[PROVEN + induction, base to G≈884k]`. **The B2 "arithmetic"
  wall merges with the (K)-shaped one-sided ledger** — same species, enormous margin (drift +3/gen, failure needs
  prefix ρ=1-freq ≳ 4/5 vs observed ≈ 1/3). o4's decision = an explicit Collatz-like ledger conjecture now.
- **Cap/C-seam localization (parallel subagent, `O4_CSEAM_LOCALIZATION_2026-07-06.md`):** headline CORRECTION —
  C-seams are NOT at the `1001` cap (census key was too coarse); they sit at the **filler-internal phase boundary**
  (previous invert-sweep's turnaround). `[PROVEN]`: C-seam = forced sweep-end template (`B:0·C:1·A:0`), safety decided
  by 14 fixed cells, k-uniform ∀k≥4, 26/26 real instances step-identical; the **cap crossing is seam-free**, single
  F-type arrival, k-uniform, requires a≥7 (corroborates the small-a danger). `[OBSERVED]` type-saturation (44
  sweep-end / 4 cap-arrival) through G=883,719 via a soundly-hooked macro. Residual = arrival completeness, subsumed
  under the a-ledger. Correction propagated into `O4_SEAM_PARITY_LEMMA`.
- Red-team of the composition/locality argument IN FLIGHT; G=10⁷ run in flight (results to be folded in).

## Remaining tasks / open threads (updated)
- **o4:** prove the incoming-cell/seam-parity predictor lemma (the base-4/3 carry-cascade / Collatz-type theorem). All
  surrounding structure now PROVEN; reusable tools banked (`o4_wave_width.py`, `o4_seam_closure.py`,
  `o4_frontier_trace.py`, `o4_closure_fixpoint.py`, `o4_concrete_safety.py`, `o4_window_saturation.py`, `o4_macro.py`,
  `o4_accel_probe.py`).
- **Bouncer+odometer-reset macro-machine** would push closure to G~10⁶–10⁷ soundly and decide the B2 cryptids
  (o3/o15/o18). Foundation (validated RLE) in place; the triangular-jump + reset step is the remaining careful build.
- **`(K)` kernel (the real frontier):** unchanged — external outreach to the Eliahou/AEV Normality-Conjecture group
  (materials ready: `OUTREACH_ABSTRACT`, `MEETING_BRIEF_4`, `OUTREACH_EMAIL_DRAFT`; not sent — needs recipient + sender
  identity + go-ahead).
