# Lean 4 formalization status — o4 run-structure crown lemmas (2026-07-07)

*Formalization layer for `PAPER_RUN_STRUCTURE.md`. STRICT labels: **FORMALIZED** = Lean source
compiles and the theorem is proved (checked by `lean` / `lake build`, axiom-audited);
**DRAFTED** = source written but not checked. Nothing below is drafted-only. Not committed.*

## Verdict: all four targets FORMALIZED (including the stretch)

Toolchain: Lean **4.31.0** (installed via elan this session), **no mathlib** — the project is
dependency-free (core `Int`/`Nat` arithmetic + `omega`; the 3-adic valuation `v3` is defined from
scratch). Project: `lean/` (`lakefile.toml`, `lean-toolchain`, `RunStructure.lean`, `crosscheck.py`).

**Axiom audit (all crown theorems): `[propext, Quot.sound]` only** — no `sorryAx`, no
`Classical.choice`. Verified via `#print axioms` on every theorem listed below.

| Target | Lean theorem(s) in `RunStructure.lean` | Status |
|---|---|---|
| T(G), integrality `3 ∣ 4G+e(ρ)` | `e`, `T`, `T_key`, `T_eq` (3·T G = 4·G + e G) | **FORMALIZED** |
| **1. Itinerary bijection** (injectivity form, as specced) | `pow3_dvd_of_dvd_four_mul` (4 a unit mod 3^L), `step_inj` (mod-3^L lift), `itinerary_inj` (equal L-itineraries ⇒ 3^L ∣ G−G′) | **FORMALIZED** |
| **2. Run closed form** | `v3n`/`v3` (from-scratch valuation) + `v3n_unit_mul`, `v3_three_mul`, `v3_four_mul`; `fixedpoint_e` (e(ρ)=−x_ρ), `fixedpoint_conj` (3·(T G+e G)=4·(G+e G)), `v3_step_down` (v₃ drops by exactly 1), `run_invariant`, `run_length_lower`, `run_length_exact`, **`run_closed_form`** (maximal run = v₃(G+e G) = v₃(G−x_ρ), both halves) | **FORMALIZED** |
| **3. Run cap** | `v3n_pow_le`, `run_cap` (3^{v₃ n} ≤ \|n\|), `run_cap_orbit` (3^{run} ≤ G+14, i.e. run ≤ log₃(G+14)) | **FORMALIZED** |
| **4. Stretch: o15/o18 ×8/3 mirrors** | `T8`, `T8_eq`, `o15_conj` (3(5V′+c)=8(5V+c)), `v3_step_down8`, `o15_val_drop`, `o15_queued` (3(V′−1)=8(V−1); c=−5 ≡ o18 depth push law), `o15_queued_val_drop` | **FORMALIZED** |

Notes on statement fidelity:
- Theorem 1 is formalized exactly in the injectivity form the spec asked for (via `G = 3H+ρ`
  cleared of division: `3(T G − T G′) = 4(G − G′)` + the unit lemma). Bijectivity then follows by
  counting (3^L classes on both sides); the counting step is NOT formalized — it is machine-checked
  by enumeration instead (`bijCheck` `#eval`: L=1..5 in Lean; L=1..8 in Python).
- Theorem 2's "maximal run" is formalized as the conjunction: residue ρ persists for all
  i < v₃(G+e G) AND changes at i = v₃(G+e G) (hypothesis G ≥ 1, as in the paper's setting).
- Stretch scope: the o15/o18 items are the fixed-point conjugation identities + per-step valuation
  drop (the "same pattern" content of `O15_FIXEDPOINT`/`O18_DEPTH_UNIFORM` §1). The o15 full
  run closed forms would additionally need its branch-selection structure (queue-dependent —
  provably not a congruence, per `O15_FIXEDPOINT` §6), which is out of scope here.

## Numeric sanity (both layers green)
- Lean `#eval` (run at every build): bijection L=1..5 all true; run law G=1..2000 true; o4
  real-orbit anchors `orbit 3 [5,9,12,20] = [43,151,367,3727]` (matches `O4_LEDGER_ANALYSIS` §5);
  o15/o18 identity grid true.
- `lean/crosscheck.py` (mirrors each Lean statement): bijection L=1..8; run law + caps
  G=1..200000 (0 mismatches — same range as the paper's verification); run_cap |n|≤50000;
  orbit anchors to n=36 (G=372814); o15 all four branches c∈{9,11,−17,−5}, V∈[−500,500]. All OK.

## Build commands (exact)
```
# toolchain (once): curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain stable
export PATH="$HOME/.elan/bin:$PATH"
cd /Users/aokiyousuke/busybeaver/lean
lake build            # full check; #eval sanity lines print as info
# or: lean RunStructure.lean     (single-file check, no lake needed)
/usr/bin/python3 crosscheck.py   # numeric mirror (≈20 s)
```
Axiom audit: `lake env lean <file with '#print axioms RunStructure.run_closed_form' etc.>`.

## What's left (not attempted / out of scope)
- Bijectivity-by-counting for Theorem 1 as a Lean theorem (needs finite-cardinality bookkeeping;
  cheap with mathlib's `Finset`, noisy without).
- o15 full run laws (`run = v₃(5V+c)` per branch) and any queue/branch-selection structure.
- Everything about the machine o4 itself (template closure, ledger): these are lab-note results,
  not formalized, and the ledger conjecture remains **OPEN** — the theorems formalized here are the
  paper's elementary number-theoretic layer only.

**No machine decided. No label upgraded.**
