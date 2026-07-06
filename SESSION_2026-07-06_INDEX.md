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
- **G=10⁷ run COMPLETE:** 5.003×10¹³ steps in 7,341s — **G=8,827,295**, 48 milestones, odometer exact on all 47
  transitions, |S|=23 frozen, UNSAFE=0, F-reads-1=0. Evidence now **450×** the pre-macro range.
- **RED-TEAM COMPLETE — no unsound conclusion; labels stand with 3 corrections applied** (`o4_redteam_*.py`):
  (1) GAP-FOUND in the generalization step (sweep termination is tape-determined; conditional sweep lemmas don't
  exclude parameter-dependent defects inside swept regions) — REPAIRED by the episode-landmark-pinning lemma (every
  episode step at parameter-independent offset ≤3 from a structural landmark; verified body/suffix/prefix, to k=251);
  (2) suffix small-a "one skeleton per class" OVER-CLAIM → restated as per-a templates (a∈{0..4}) + generic a≥5;
  (3) provenance mislabel (raw concrete = G≈19.5k, macro-validated = 8.8M) fixed. Independent confirmations:
  Z(41,3,0) halt at 55,170; zero spurious milestones (72 runs); composition verified at G=37..500; cone edges
  conservative. This is the ~31st–33rd self-caught correction; discipline held under the day's biggest claim.

## Part 4 — the a-ledger attack (`O4_LEDGER_ANALYSIS_2026-07-06.md`) + o3 port (in flight)
- **Itinerary bijection theorem `[PROVEN]`** (3-line proof + exhaustive L=1..8, `o4_ledger_bijection.py`): seed mod 3^L
  ↔ residue itinerary. Consequences: fatal patterns are realized by full seed classes ⇒ **halting template orbits
  exist for every a₀**; the safe seed set is a 3-adic Cantor set; **no seed-uniform safety theorem can exist** — the
  o4 analogue of the No-Structure theorem, proving the ledger is irreducibly orbit-specific ((K)'s species) at the
  B2 flagship.
- **Ruin quantification:** annealed `P[fatal from a] ~ η^a`, **η = 0.334895 ≈ 1/3**; from the current frontier
  (a=124): ~10⁻⁵⁹.
- **Small-a map `[OBSERVED]`:** `Z(k,3,a≤1)` is k-IRREGULAR — {LAND via a different recovery branch (G′=2k+29, a′≥3) /
  HALT (only k=41) / WANDER>3M `[OPEN]`}; the safety direction (non-halt ⟸ ledger ≥2) is UNAFFECTED.
- **Real-orbit ledger `[OBSERVED to G=884k]`:** δ-rule exact; min a at ρ=1 = **12** (template regime), growing
  +3/generation (115 by G=373k); longest ρ=1 run = 2. Margin enormous and widening.
- Verdict: o4's remaining core = a quenched one-sided prefix condition on a specific 3-adic itinerary — (K)'s
  species with a +3-drift margin = **the easiest-margin open case in the cryptid family**.
- **o3 template-port subagent** in flight (stalled once on watchdog, resumed with a focused plan).

## Part 5 — easy-tasks sweep: o17 halt-flavor pinned (`O17_HALT_FLAVOR_2026-07-06.md`) — the in-family COUNTEREXAMPLE
o17 (`1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`) pinned as **verdict (iii): "sparse-gate carry-timing"** — a THIRD
species: `[PROVEN]` halt ⟺ `0 0 [1]_A` local seam condition (F only via (D,0), D only via (A,1)); 11-window
saturation, all safe; blank orbit = core seed j=1. **Template test FAILS** (generation shapes unbounded: 69→91
classes still growing — √step growth means the generation state is the whole digit string). Old "B1-leaning
parity-density" REFUTED (the bit is a deterministic 3-state automaton read — no density statement exists); but **no
o4-style ledger either** (no finite-residue δ-map; branch driver = full carry cascade; distance-to-fatal ≤1 at every
gate, protection = super-exponentially thinning gate TIMING). ⇒ **the B2 wall does NOT uniformly bottom out in a
(K)-shaped ledger** — the family now has three species: (i) template+ledger (o4), (ii) density/(K) (Antihydra B1),
(iii) sparse-gate carry-timing (o17). Re-verified by main loop (halt-reduction census reproduces).

## Part 6 — o3 template port COMPLETE, verdict (a): o3 is the SECOND template+ledger machine (`O3_TEMPLATE_PORT_2026-07-06.md`)
- o3 = `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC` (spec pinned across 4 repo files). Halt gate `[PROVEN from table]`;
  windows saturate (6 at r=5 by step 1,370), 0 unsafe / 1.67M events.
- **Body lemma `[PROVEN]`** (`o3_body_proof.py`, re-verified): certified trace-template with **cycle certificates
  (periods 10/20/6** — richer than o4's period-2) + landmark pinning + exact landing, j to 501, all j≥12 ≡0 mod 3;
  locality span [−2, 2j+3] ⇒ valid with arbitrary content right of the defect block.
- Generation law exact on grids (k=50/120, a to 1005); **halting configs FOUND & PREDICTED A-PRIORI by the ledger:
  M(a,0) for a≡2 (mod 3), M(a,1) for a≡6 (mod 9) — two predicted halts confirmed by simulation** (the method's
  strongest validation yet). Fatal set: (k=1 ∧ a≡6 mod 9) ∨ (k=0 ∧ a≡2 mod 3), reachable only via drains at a≡0 mod 3.
- **Ledger:** deterministic (k,a) joint map; 200,000 generations NO fatal hit; drift +0.248/gen (much thinner than
  o4's +3), max drain run 10; the counter `a` is a growing big integer (18,743 digits by gen 200k) — the ledger
  driver is the digit string itself, a harder flavor than o4's residue-δ.
- Macro machine ported & validated (V1/V2 exact). **Species (i) now has TWO members (o4, o3)**; combined with Part 5,
  the three-species classification {template+ledger, density/(K), sparse-gate} is populated 2/1/1.

## Part 7 (2026-07-07) — o18 port: a FOURTH species; WANDER cases = a milestone-free growing regime
- **o18 (`1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`, halt=F reads 1) — verdict (c), NEW species: "self-similar
  3-adic recursion-tower bouncer"** (`O18_TEMPLATE_PORT_2026-07-07.md`): gate `[PROVEN]` (halt ⟺ D reads 1 with left-1;
  window census saturates at ONE window — sharpest in family); clean resets `C_N=[F]01^{N-1}` with `⌊8N/3⌋+2` exact for
  N≡0,1 (mod 3); rigid template `[PROVEN on grid]` with 3 certified sweep cycles; **CORRECTION to
  `CRYPTID_O18_FRAMEWORK`**: the reset law is FALSE for N≡2 (mod 3) (old detector counted a dirty F-entry as a reset;
  real orbit 3890→27660, 163.7M steps concrete). N≡2 recurses through a **self-similar 3-adic branch tower** with
  closed exact laws at several levels (`(64N−20)/9`, `(64N−104)/9`, `(512N−1288)/27`, `(4096N−11618)/81` —
  predict-and-confirm passed at fresh N), deeper branches `[OPEN]` and Collatz-irregular in depth (v₃-hypothesis
  refuted); blank orbit enters the unclosed tower at generation 11. **No δ-map AND no fatal set found** (zero halting
  configs — contrast o3/o4). Non-halt = a LEVEL-INDUCTION target — arguably the most decision-adjacent cryptid.
  Family classification now **four species: {template+ledger (o4,o3), density/(K) (Antihydra), sparse-gate (o17),
  recursion-tower (o18)}**.
- **WANDER cases resolved-in-kind:** the `Z(k,3,a≤1)` "WANDER" configs are a **milestone-free growing regime** —
  1.1×10¹² steps each (bounded-time macro runs), G~530k, segs=5, **unsafe=0** — a different attractor family with no
  halt signature; classified `[OPEN, non-halting-like]` (not needed for the safety reduction).

## Part 8 (2026-07-07) — o15 port (fifth shape: template + STRING-LEDGER) + the species synthesis
- **o15 (`1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA`, halt=A reads 1) — the B1/density call SURVIVES, sharpened
  in mechanism** (`O15_TEMPLATE_PORT_2026-07-07.md`): gate `[PROVEN]` (halt ⟺ F reads 1 with right-1; 2-window
  saturation); complete state = digit-block queue + big block (prior `O15_REDUCTION` "carry corrections" corrected to
  exact queue bookkeeping); template RIGID (5 shape classes, ~800 standalone runs, o17 failure-mode absent).
  **DISCOVERY: a genuine fatal set on a B1-called machine** — `M([2,2,…],V)`, V≢2 (mod 3) HALTS; 9 found + fresh
  members **a-priori predicted and confirmed** (`[2,2,151]`, `[2,2,301]`, `[2,2,1000]`, `[2,2,2,150]`). The ledger is
  a digit-string TRANSDUCER (an end-local absorption law was honestly refuted by predict-and-confirm inside the
  session); non-halt = "the carry cascade never stacks a leading `[2,2]` at a split step" — cylinder avoidance in the
  Mahler-8/3 digit coordinate = Fork-B1's shape now grounded in a proven fatal set. Re-verified (fatal census
  reproduces).
- **`BB6_CRYPTID_SPECIES_2026-07-07.md`** — the campaign synthesis: every cryptid = **GATE `[PROVEN]` + STRUCTURE
  (mostly PROVEN) + PROTECTION `[OPEN]`**; five protection shapes {residue-ledger o4, int-ledger o3, string-ledger
  o15, density Antihydra, gate-timing o17} + level-induction (o18); margins ordered o4 ≫ o3 > o15 > o17 > Antihydra;
  fatal sets real & predictive where they exist, none found for o18. The B1/B2 dichotomy superseded by the
  gate/structure/protection decomposition.

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
