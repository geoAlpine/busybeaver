# The BB(6) Cryptid Frontier: Certified Templates, Ledger Reductions, and a Unified p-adic Return Problem

**Yosuke Aoki (GeoAlpine LLC)** — research artifact, version 1.0 (2026-07-08)

## What this is

A self-contained research artifact on the **BB(6) frontier** — the halting problems of the hardest 6-state Turing
machines ("cryptids"), each of which encodes an open arithmetic problem. It contains three paper-style documents,
the machine-verification battery that re-checks every proof-path certificate in one command, a Lean 4 formalization
of the core arithmetic theorems, and the supporting lab notes.

**Headline results** (none of the machines is decided; every claim carries an explicit epistemic label):

1. **Certified trace-template reductions.** For the cryptids here called o4, o3, o15/o18, the full generation
   dynamics is certified ("templates"), reducing each machine's non-halting to a single explicitly-stated open
   conjecture — e.g. o4's halting problem is equivalent (one direction proven, base verified) to a prefix-sum
   ledger over the residue itinerary of the base-4/3 odometer `G ↦ ⌊4G/3⌋ + c(G mod 3)`.
2. **Exact run structure.** The branch maps' integer fixed points give exact closed forms: the maximal run of a
   residue ρ from G equals `v₃(G − x_ρ)` — with an unconditional run cap, a seed↔itinerary bijection (hence
   provable orbit-specificity), and a golden-ratio ruin constant for Antihydra's ledger. Machine-checked in
   Lean 4 (zero `sorry`, zero external dependencies).
3. **The unification.** The flagship kernels (Antihydra ×3/2, o4 ×4/3, o15/o18 ×8/3) are one problem — an
   effective quenched bound on deep p-adic return/hitting frequency for explicit ×p/q orbits — graded by an exact
   criticality criterion (run-cap slope / budget slope; Antihydra sits at 1.1699 > 1, the critical rung, matching
   the known "1.17×" barrier).
4. **A gate/structure/protection classification** of the analyzed cryptid orbits, with proven fatal
   configurations for the template machines (including a-priori predicted halting configurations later confirmed
   by simulation) and a ledger-memory dichotomy (cumulative vs resetting) that exactly tracks the annealed
   halt/non-halt lean.

## Contents

- `papers/` — the three paper-style documents (theorem–proof style):
  `PAPER_RUN_STRUCTURE.md`, `PAPER_TEMPLATE_METHOD.md`, `PAPER_SPECIES_SURVEY.md`
- `verification/` — `verify_all.py` (one-command re-verification; `--quick` ≈ 30 s, full ≈ minutes) and all
  scripts it invokes, self-contained
- `lean/` — Lean 4 project (v4.31.0, no mathlib): the run-structure theorems, 42 theorems, zero `sorry`;
  build with `lake build`
- `notes/` — the supporting lab notes referenced by the papers ("References to the record"), including the
  novelty audit, the o15/o18 identity correction, and the retraction/correction trail
- `LICENSE-DOCS` (CC-BY 4.0, applies to `papers/`, `notes/`, this README),
  `LICENSE-CODE` (MIT, applies to `verification/`, `lean/`)

## Epistemic status — read this first

"PROVEN" template lemmas are exhaustively grid-verified with an explicitly stated composition argument
(episode-landmark pinning), adversarially red-team-audited, and independently re-verified; they are **not yet
formalized in a proof assistant** (the Lean layer currently covers the arithmetic run-structure theorems). The
corrections/retraction trail (~46 self-caught over-claims, all logged in place in `notes/`) is part of the record.
**No cryptid is decided.** Prior work by the bbchallenge community (machine discoveries and reduction statements
for several of these machines; a Lean-verified halting congruence class for the o15/o18 table) is cited in
`notes/NOVELTY_AUDIT_2026-07-07.md` and in the papers.

Methodology note: this program was conducted with extensive AI assistance (Anthropic Claude) under a strict
soundness discipline (labels, adversarial red-teams, independent re-verification, zero-false-proof record);
the discipline and its audit trail are themselves documented in the notes.

## How to verify

```
cd verification && python3 verify_all.py --quick   # ~30 s
cd lean && lake build                              # Lean 4.31.0 via elan
```

## Cite as

Aoki, Y. (2026). *The BB(6) Cryptid Frontier: Certified Templates, Ledger Reductions, and a Unified p-adic
Return Problem* (Version 1.0) [Research artifact]. Zenodo. DOI: (assigned on publication)

Related: Andrieu, Eliahou & Vivion, arXiv:2510.11723 (the Normality Conjecture this program's kernel instantiates);
the bbchallenge project (machine discoveries and prior analyses; see the novelty audit for exact attributions).
