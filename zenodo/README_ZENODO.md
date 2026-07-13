# The BB(6) Cryptid Frontier: Certified Templates, Ledger Reductions, and a Unified p-adic Return Problem

**Yosuke Aoki (GeoAlpine LLC)** — research artifact, version 1.0 (2026-07-14)

## Quick start

```
# 1. Re-run the whole proof-path verification battery (pure Python stdlib, no pip install):
cd verification && python3 verify_all.py --quick     # ~30 s;  drop --quick for the full run

# 2. Build the Lean 4 formalization (needs elan/lake; toolchain pinned in lean/lean-toolchain):
cd lean && lake build                                # green, zero sorry, axiom audit [propext, Quot.sound]
```
**Dependencies:** the `verification/` scripts use the Python **standard library only** (Python 3.10+; no
`requirements.txt` needed). Lean needs `elan` (installs the pinned toolchain automatically).

## Reading guide

**Shortest path** (specialist, ~5 min): `papers/MINIMAL_OPEN_KERNEL.md` — the single open problem the whole program reduces to, with the per-method obstruction map. Then, if you only read **three more files**: `papers/PAPER_CENSUS.md` (the whole frontier as one map),
`papers/PAPER_MIRROR_LADDER.md` (the uniform theorem), and this README's *Epistemic status* section below.

- **~10 min** — this README + `papers/PAPER_CENSUS.md` §0–6 (what every cryptid is, what's proven, what's open).
- **~30 min** — add `papers/PAPER_MIRROR_LADDER.md` (the uniform fixed-point theorem) and
  `papers/PAPER_RIGIDITY_LIMITS.md` (the (K)-independent limits-of-rigidity theorem).
- **~30 min (decision track)** — `papers/PAPER_X2_INTEGER_DOUBLER.md` (the integer-doubler machine: how the
  frontier's carry-transparent candidate's non-halting is reduced, in Lean, to a single recursive lemma).
- **~2 hours** — add `lean/Mirror.lean` + `lean/Completion.lean` + `lean/X2.lean` (the machine-checked core, the
  conditional completion frame, and the integer-doubler architecture), run `verify_all.py`, and skim the
  `notes/` corrections trail.

## What this is

A self-contained research artifact on the **BB(6) frontier** — the halting problems of the hardest 6-state Turing
machines ("cryptids"), each of which encodes an open arithmetic problem. It contains a ~2-page specialist entry point (MINIMAL_OPEN_KERNEL) plus seven paper-style documents,
the machine-verification battery that re-checks every proof-path certificate in one command, a Lean 4 formalization
of the core arithmetic theorems, and the supporting lab notes.

**Headline results** (none of the machines is decided; every claim carries an explicit epistemic label):

1. **Certified trace-template reductions.** For the cryptids here called o4, o3, o15/o18, o2, o11, the full
   generation dynamics is certified ("templates"), reducing each machine's non-halting to a single explicitly-stated
   open conjecture — e.g. o4's halting problem is equivalent to a prefix-sum ledger over the residue itinerary of the
   base-4/3 odometer `G ↦ ⌊4G/3⌋ + c(G mod 3)`. **For o4 this machine→arithmetic reduction is now machine-checked
   end-to-end in Lean 4**: the odometer and the ledger update law are proven theorems (`generation_odometer`),
   leaving only the ledger conjecture itself as informal content.
2. **Exact run structure.** The branch maps' integer fixed points give exact closed forms: the maximal run of a
   residue ρ from G equals `v₃(G − x_ρ)` — with an unconditional run cap, a seed↔itinerary bijection (hence
   provable orbit-specificity), and a golden-ratio ruin constant for Antihydra's ledger. Machine-checked in
   Lean 4 (zero `sorry`, zero external dependencies) — including the **full o4 template layer**: the o4 machine
   itself, the arbitrary-length sweep lemmas, the body lemma `B(k) → B(k+2)` for ALL k, the suffix lemmas, and the
   composed generation map — all with axiom audit `[propext, Quot.sound]` only.
3. **The unification (uniform theorem).** EVERY analyzed Type-I cryptid (Antihydra, o2, o4, o11, o13, o14, o16 —
   all ×3/2 or ×4/3/×8/3; and Space Needle ×5/2) is the q-adic depth process of an explicit affine ×(p/q) orbit:
   the branch maps have integer fixed points x, and since p is a q-adic unit the maximal run equals `v_q(v − x)`
   (`mirror_census.py` verifies the whole census; **the abstract theorem is machine-checked in `lean/Mirror.lean`** — 8 machines are corollaries of one Lean theorem (Antihydra, o2, o4, o11, o13, o14, o15, o16; mirror_census.py covers the full 11-orbit census)). So the frontier is ONE problem — an effective quenched bound on
   deep q-adic return frequency — graded by an exact criticality criterion (Antihydra/o2 at 1.1699 > 1, the
   critical rung matching the "1.17×" barrier; o4 at 0.087). Space Needle's odd branch, the sole machine without a
   single fixed point, is the one non-(K)-seeded outlier.
4. **A gate/structure/protection classification** of the analyzed cryptid orbits, with proven fatal
   configurations for the template machines (including a-priori predicted halting configurations later confirmed
   by simulation) and a ledger-memory dichotomy (cumulative vs resetting) that exactly tracks the annealed
   halt/non-halt lean.
5. **The integer-doubler machine — a machine-checked non-halting *architecture* reduced to one recursive
   lemma.** The machine `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` is a base-2 doubling odometer, `×2` with
   integer multiplier `q=1` — it sits *outside* the (K)/normality wall (carry-transparent, not carry-opaque),
   the frontier's best-mapped candidate for a decidable-in-principle machine. In Lean 4 (`X2.lean`) we build the
   entire non-halting proof architecture: a conditional theorem `x2_nonhalt` reducing non-halting to three
   explicit halt-free phase transports; the doubling phase resolved as a **clean binary odometer** (exact
   closed-form tick count `Tfaithful`, a verified power-of-2 comb-at-carry ladder, a terminating well-founded
   recursion — refuting an "irreducibly tape-determined" reading); and a library of ∀-parametric on-path
   primitives (the tick, the steady run, the carry's `sweepEF`-core, the factored depth-1 carry, the low-phase
   forward tile). The remaining open content is isolated to a **single** named lemma — `carry_step`, a
   well-founded ripple recursion whose exact structure is measured. **The machine is not decided;** this is a
   reduction, not a decision. (`papers/PAPER_X2_INTEGER_DOUBLER.md`.)

## Contents

- `papers/` — `MINIMAL_OPEN_KERNEL.md` (the ~2-page specialist entry point: the single open problem + obstruction map)
  and the seven paper-style documents (theorem–proof style): `PAPER_RUN_STRUCTURE.md`, `PAPER_TEMPLATE_METHOD.md`,
  `PAPER_SPECIES_SURVEY.md`, `PAPER_MIRROR_LADDER.md`, `PAPER_CENSUS.md`, `PAPER_RIGIDITY_LIMITS.md`,
  `PAPER_X2_INTEGER_DOUBLER.md` (the integer-doubler machine's machine-checked non-halting architecture)
- `verification/` — `verify_all.py` (one-command re-verification; `--quick` ≈ 30 s, full ≈ minutes) and all
  scripts it invokes, self-contained
- `lean/` — Lean 4 project (v4.31.0, no mathlib): run-structure theorems, the abstract uniform fixed-point
  theorem (`Mirror.lean`, 8 machines as Lean corollaries), and the o4 AND o3 template cores (both machines,
  sweep lemmas, body lemmas — o4's full generation map, o3's body AND generation map (odometer), o18 machine+all-sweeps, o2 machine+phase-1, o17 machine+gate, and **Completion.lean** — the conditional completion theorem `BB6_eq_championSteps` (the complete BB(6) proof's machine-checked logical frame, hard content isolated into 17 named conjectures = 11 explicit axioms); plus the abstract uniform fixed-point theorem and the criticality comparison; and **X2.lean** — the integer-doubler machine's non-halting *architecture* (the conditional theorem `x2_nonhalt`, the clean binary-odometer of its doubling phase, and the ∀-parametric phase primitives, reducing the machine to a single open recursive lemma `carry_step`; see `papers/PAPER_X2_INTEGER_DOUBLER.md`)) — 387 theorem/lemma declarations across the 10 shipped Lean files, zero `sorry`, zero `native_decide`, axiom audit `[propext, Quot.sound]` only; build with `lake build`
- `notes/` — the supporting lab notes referenced by the papers ("References to the record"), including the
  novelty audit, the o15/o18 identity correction, and the retraction/correction trail
- `LICENSE-DOCS` (CC-BY 4.0, applies to `papers/`, `notes/`, this README),
  `LICENSE-CODE` (MIT, applies to `verification/`, `lean/`)

## Epistemic status — read this first

Claims live at two assurance tiers. **Machine-checked (Lean 4):** the arithmetic run-structure theorems and the FULL o4
template reduction — the machine itself, the sweep lemmas, the body lemma (all k), the suffix lemmas, and the
composed generation map (odometer + ledger law as theorems) — proven in the proof assistant with axiom audit
`[propext, Quot.sound]` only. For the **integer-doubler machine (`X2.lean`)**, what is machine-checked is the
non-halting *architecture*: the conditional theorem `x2_nonhalt` (non-halting *given* the phase transports), the
doubling phase's clean binary-odometer structure, and the ∀-parametric on-path phase primitives — **not** a
decision; its `carry_step` ripple recursion is an explicit open lemma, and `x2_nonhalt`'s hypotheses are the
still-unproven phase transports. **Grid-certified:** the remaining template reductions (o3/o15/o18/o2/o11) are
exhaustively grid-verified with an explicitly stated composition argument (episode-landmark pinning),
adversarially red-team-audited, and independently re-verified — but not yet formalized. The
corrections/retraction trail (~46 self-caught over-claims, all logged in place in `notes/`) is part of the record.
**No cryptid is decided.** Prior work by the bbchallenge community (machine discoveries and reduction statements
for several of these machines; a Lean-verified halting congruence class for the o15/o18 table) is cited in
`notes/NOVELTY_AUDIT_2026-07-07.md` and in the papers.

Methodology note: this program was conducted with extensive AI assistance (Anthropic Claude) under a strict
soundness discipline (labels, adversarial red-teams, independent re-verification, zero-false-proof record);
the discipline and its audit trail are themselves documented in the notes.

## How to verify

```
cd verification && python3 verify_all.py --quick   # ~30 s  (pure Python stdlib)
cd lean && lake build                              # Lean 4.31.0 via elan
```

`verify_all.py` runs every proof-path certificate and reports PASS/FAIL per item. What each certifies:

| script | verifies |
|---|---|
| `o4_body_proof.py` | o4 body lemma `B(k) → B(k+2)`, all k to 251 |
| `o4_growing_certify.py` / `o4_wander_certify.py` | o4 growing-config + translated-cycler non-halt certificates |
| `o4_ledger_bijection.py` | the seed↔itinerary bijection + ruin constant |
| `o4_closure_fixpoint.py` | the HALT-in-closure impossibility (no local certificate) |
| `o4_seam_lemma_verify.py` | the o4 seam-decomposition census |
| `o3_body_proof.py` | o3 body lemma, period-10/20/6 cycles |
| `o18_depth_map.py` / `o15_fp_vmap.py` | o18 pushdown-odometer table; o15 fixed-point run laws |
| `mirror_census.py` | the uniform fixed-point run law across the whole census |
| `o4_bouncer_macro.py` | the macro-machine validation battery (slow) |
| `freq_rundepth_whiteness.py` | the frequency-axis white/structureless measurement |

**Proven vs measured:** items whose name ends in `_proof`/`_verify`/`_bijection`/`_census` are exact assertion-checked
certificates (`[PROVEN]`); `freq_*`/`*_probe` are empirical measurements (`[OBSERVED]`). The Lean layer is the strict
machine-checked tier; see *Epistemic status* above for exactly what Lean guarantees and what it does not (the
`NormalityPQ` conjecture is an uninterpreted axiom — Lean verifies the reduction's assembly, not the conjecture's truth).

## Cite as

Aoki, Y. (2026). *The BB(6) Cryptid Frontier: Certified Templates, Ledger Reductions, and a Unified p-adic
Return Problem* (Version 1.0) [Research artifact]. Zenodo. https://doi.org/10.5281/zenodo.21252622

Related: Andrieu, Eliahou & Vivion, arXiv:2510.11723 (the Normality Conjecture this program's kernel instantiates);
the bbchallenge project (machine discoveries and prior analyses; see the novelty audit for exact attributions).
