# Campaign master index — the template/ledger campaign (2026-07-06 → 07-07)

*Navigation for the 24-commit campaign that took the cryptid frontier from "boundary graphs with counter-dependent
branching" to: certified templates + precisely-formulated protections for all six machines, the mirror-ladder
unification, and o18 one rewrite system away from a candidate decision. Every note carries honest
[PROVEN]/[OBSERVED]/[OPEN] labels; zero false proofs/decisions; ~35 self-caught corrections program-wide.*

## The arc in one paragraph
o4's decision attempt (07-05) had stalled at "finite boundary graph, counter-dependent branching". This campaign:
(1) reframed safety as window-set closure, proved the bounded-defect structure, and REFUTED the odometer-desync
mechanism (seam lemmas); (2) built a validated macro-machine (×1,800), DISCOVERED the rigid generation template, and
certified it (prefix/body/suffix lemmas, red-teamed); (3) derived the odometer law and found the a-LEDGER — the
hidden second counter whose boundedness IS o4's decision, with a genuine halting config proving non-vacuity;
(4) ported the method family-wide (o3 verdict (a); o15 string-ledger with real fatal set; o17 no-template
counterexample; o18 recursion tower); (5) proved the run-structure theorem (integer fixed points ⇒ exact v₃ run
closed-forms) on o4, then o15, then o18 — unifying Antihydra/o4/o15/o18-depth as ONE p-adic return-frequency
problem (the mirror ladder); (6) formulated the last missing protection (o17's gate law, iterated-exponential
sparsity); (7) collapsed o18's tower to a pushdown 3-adic odometer, leaving one explicit blocker.

## Note map (campaign notes, chronological)
| note | content | key labels |
|---|---|---|
| `O4_WINDOW_SATURATION_2026-07-06` | safety=window-closure reframe; bounded defects; HALT-in-closure impossibility; AFS verdict; macro build+G=8.8M runs | defects/impossibility PROVEN |
| `O4_SEAM_PARITY_LEMMA_2026-07-06` | seam decomposition; E-seams unconditionally safe; desync refuted | PROVEN (+location corrected) |
| `O4_TEMPLATE_CLOSURE_2026-07-06` | **the o4 master note**: prefix/body/suffix certified; odometer derived; a-ledger; Z(41,3,0) halts; red-team corrections | template PROVEN; ledger OPEN |
| `O4_LEDGER_ANALYSIS_2026-07-06` | itinerary bijection (seed-specificity); ruin η≈0.335; small-a map (now completely decided); real-orbit margin | bijection PROVEN |
| `O4_CSEAM_LOCALIZATION_2026-07-06` | C-seams at filler phase boundary (correction); k-uniform sweep-end template; cap seam-free | PROVEN |
| `O3_TEMPLATE_PORT_2026-07-06` | o3 verdict (a); cycle certs p=10/20/6; ledger PREDICTED halting configs (confirmed); Δk=δ(a mod 3) | body PROVEN |
| `O17_HALT_FLAVOR_2026-07-06` | o17 = sparse-gate; template fails; old density call refuted | gate PROVEN |
| `O18_TEMPLATE_PORT_2026-07-07` | o18 = recursion tower; framework-law correction; no fatal set | levels PROVEN |
| `O15_TEMPLATE_PORT_2026-07-07` | o15 = string-ledger; REAL fatal set on a B1 machine (predicted+confirmed) | gate/template PROVEN |
| `BB6_CRYPTID_SPECIES_2026-07-07` | **the classification**: GATE+STRUCTURE+PROTECTION; five shapes + level-induction; margins ordered | synthesis |
| `O4_RUN_STRUCTURE_2026-07-07` | **fixed-point theorem**: run=v₃(G−x_ρ); run cap 0.262n; single-run fatality dead; o4⟷Antihydra mirror | PROVEN |
| `O4_GROWING_REGIME_2026-07-07` | 3 configs = pure body iteration C(m)→C(m+2); non-halting | PROVEN |
| `O15_FIXEDPOINT_2026-07-07` | o15 branch maps + fixed points; run=v₃(V−1); mirror ladder 3rd member | PROVEN |
| `O17_GATE_LAW_2026-07-07` | gate map F exact; t≈3.97n²; log n′≈a·n (tower sparsity); no finite reduction m≥3 | formulation |
| `O18_DEPTH_UNIFORM_2026-07-07` | tower = pushdown 3-adic odometer (one finite table); mod-81 branches land; blocker = multi-defect grammar | table PROVEN on grid |
| `O18_MULTIDEFECT_2026-07-07` | (in flight) the general word transducer — the last link to a candidate decision | — |
| `SESSION_2026-07-06_INDEX` | the full chronological session record (Parts 1–9) | — |

## Tool map (validated, reusable)
- **Macro machines:** `o4_bouncer_macro.py` (V1/V2 validated, ×1,800; off-template use unsafe — known merge hang),
  `o3_bouncer_macro.py` (V1/V2/V3 passed).
- **Certified trace-template verifiers:** `o4_body_proof.py`, `o3_body_proof.py`, `o4_growing_certify.py` (the
  method: episode skeleton identity + affine sweeps + cycle certificates + landmark pinning + exact landing;
  red-team-corrected form).
- **Certificates:** `o4_wander_certify.py` (translated-cycler), `o4_closure_fixpoint.py` (HALT-in-closure
  impossibility), `o4_ledger_bijection.py` (bijection + ruin).
- **Ledger/structure extractors:** `o4_concrete_safety.py`, `o4_window_saturation.py`, `o3_ledger.py`,
  `o15_fp_*.py`, `o17_gate_*.py` (+`o17_gate_census.c`, 280M steps/s), `o18_depth_*.py`.
- Discarded (UNSOUND, kept as failure-mode records): `o4_accel_windows.py`.

## Status table (as of 2026-07-09 — 62 commits, Zenodo v1.3, 212 Lean theorems sorry-free)
Full 13-orbit census; every machine = q-adic depth process of an explicit ×(p/q) orbit (uniform theorem, Lean-checked
in `Mirror.lean`); depth axis unconditionally controlled, ONLY the frequency axis open (measured white +
conditionally structureless — `FREQUENCY_AXIS_PROBE`). Fixed points from `PAPER_MIRROR_LADDER` §2.
| machine | ×p/q | fixed pts | protection (open core) | memory | Lean |
|---|---|---|---|---|---|
| o4 | ×4/3 | (−9,−14,−1) | residue-ledger a≥2 at ρ=1 | cumulative, ratio 0.087 (free) | **END-TO-END** (machine→odometer+ledger) |
| o3 | ×4/3 | mix | k-ledger (roles swapped) | cumulative, 0.79 | machine+body; gen-map in flight |
| o15/o18 | ×8/3 | 1 | epoch-hit fatal congruence (Lean class mod 3¹⁰⁸ exists) | resetting/pushdown | explore in flight |
| o2 | ×3/2 ceil | (0,1) | ceiling-(K) + mod-4 hatch | cumulative, 1.17 (critical) | Link0 certified; corollary in flight |
| o11 | ×3/2 | (−8,−7) | seeded-(K) at doubly-exp refills | resetting | Mirror corollary |
| o13 / o14 | ×3/2 | (−14,−7)/(−12,−11) | seeded-(K) parity/gap draw | resetting | corollary in flight |
| o16 | ×3/2 | (−4,−3) | seeded-(K), tower-sparse gate | resetting | Mirror corollary |
| o17 | — | none (no fixed pt) | gate branch, tower-sparse timing | no ledger | gate-map (Python) |
| Space Needle | ×5/2 | even 0; **odd none** | non-(K) string-ledger (base-2 cylinder) | cumulative, summable | Mirror even-branch |
| Antihydra / o10 | ×3/2 | (0,1) | even-density ≥ 1/3 = (K) | cumulative, 1.17 (critical) | Mirror corollary |

**Since 2026-07-07 (Parts 10+):** Zenodo v1.0 PUBLISHED (DOI 10.5281/zenodo.21252622) + tag-driven auto-release
(v1.1/1.2/1.3 drafts); ×3/2 trio split (o2 = 2nd Antihydra ceiling, o7 misclassified thin-set, o10 corrected); Mahler
sea + Space Needle classified (fixed-point census COMPLETE, the trick transfers to ×5/2); the UNIFORM FIXED-POINT
THEOREM (`PAPER_MIRROR_LADDER`, Lean `Mirror.lean` — 11 machines as corollaries); o4 coboundary LP → [PROVEN];
o2 Link0 certified; o11/o13/o14/o16 fixed-point closed forms; o3 = 2nd Lean machine (body); Lean generation map
(o4 machine→arithmetic END-TO-END); frequency-axis probe (K in every coordinate, run-depth white + structureless).

## The unification (what to tell an expert)
All flagship protections = **quenched deep-p-adic-return frequency bounds for explicit ×p/q orbits**:
Antihydra (×3/2, v₂, constant budget) / o4 (×4/3, v₃, budget +3/gen) / o15 (×8/3, v₃, cylinder form) /
o18-depth (×8/3, v₃, no fatal set). Depth is controlled unconditionally by the fixed-point theorem in all proved
cases; ONLY the frequency axis is open. The margin ladder is the staging for building the missing tool — and the
outreach pitch (`OUTREACH_EMAIL_DRAFT.md`, ready pending recipient/go-ahead).
