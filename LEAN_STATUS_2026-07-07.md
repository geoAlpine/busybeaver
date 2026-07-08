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
# TEMPLATE-LAYER APPEND (2026-07-08) — the o4 TEMPLATE LEMMAS are FORMALIZED (L1–L4)

*Second formalization target: the certified trace-template method's lemmas themselves
(`PAPER_TEMPLATE_METHOD.md` §2–3), pilot = the o4 body lemma, stretch = the prefix. New module
`lean/Template.lean` (same zero-dependency project; `lake build` builds both, Template in ~4 s).
Cross-check `lean/template_crosscheck.py` (zipper semantics AND an independent dict-tape
simulator). Not committed.*

## Verdict: ALL FOUR LAYERS FORMALIZED (including the L4 stretch)

| Layer | Lean theorem(s) in `Template.lean` | Status |
|---|---|---|
| **L1: the machine** | `St`/`Tape` (zipper)/`Cfg` (with `pos : Int`), `step` (`none` ⟺ the halt gate `F:1`), `steps`, `steps_add`; anchors `sanity100`, `sanity1000` (full-configuration `rfl` at N = 100, 1000, matching two independent Python simulators) | **FORMALIZED** |
| **L2: sweep lemmas** | `sweepBF` (`B1F0` read-only rightward over `(01)^j`, exactly `2j` steps, tape unchanged), `sweepDE` (`D1E0` leftward invert: left `(01)^j` → right `(10)^j`, `2j` steps) — **for ARBITRARY `j` by 2-transition induction**, the method's "proven for arbitrary length" ingredients | **FORMALIZED** |
| **L3: the body lemma** | `body_step`: `B(k) = 0^∞ [E] (10)^k 1001 0^∞ → B(k+2)` shifted −1 in **exactly `4k+15` steps**, composed as episode(2) · sweep(2k) · episode(8) · sweep(2k+4) · episode(1); `some` output = halt-free = every B-reads-1 safe (halt gate) | **FORMALIZED** |
| L3 corollaries | `body_iter` (r-fold: `B(k) → B(k+2r)` shifted −r, exact step count); **`body_nonhalt`** (the standalone `B(k)` family NEVER halts — a fully formal translated-bouncer certificate; decides nothing about o4 itself: blank-left context only) | **FORMALIZED** |
| **L4: the prefix lemma** (stretch) | `prefix471` — the fixed **471-step prefix word in parametric-window form**: from the real milestone shape `M(G,a) = 0^∞ [E] 0^G (10)^a 01 0^∞`, span [−11,30], with an ARBITRARY untouched suffix `Y` beyond 30 gap zeros ⇒ **(G,a)-uniform for ALL G ≥ 31, all a** (`prefix_milestone`; the note claimed G ≥ 37 — the window needs only 31). Kernel-checked in sixteen 30-step symbolic chunks (a monolithic symbolic-tail `rfl` blows the elaborator's whnf budget at ~60 steps; chunks are cheap) | **FORMALIZED** |
| L4 composition | `steps_shift` (translation equivariance); `body_step_ctx`/`body_iter_ctx` (body with explicit right context — "consumes exactly 3 gap cells per application" made literal); **`prefix_bodies`** (`M(G,a) →` prefix · body^r `→` the suffix-entry zone `(10)^(19+2r) 1001`, all r with 31+3r ≤ G); real-orbit anchors **`real_milestone`** (blank tape reaches exactly `M(43,18)` at step 1548 — 1548-step kernel `rfl`, axiom-free) and **`real_generation`** (blank tape → step 2431 = the real generation's suffix-entry configuration) | **FORMALIZED** |

## Axiom audit (printed at every build, `#print axioms` in-file)
**All 13 audited theorems: `[propext, Quot.sound]` only** — no `sorryAx`, no `Classical.choice`,
no `native_decide`/`ofReduceBool`. `real_milestone` and the `rfl` sanity anchors depend on **no
axioms at all**. No `sorry` anywhere; `lake build` green (Template ≈ 3.3 s).

## What the formalization ADDS to the lab-note record (statement deltas, all sound)
- **The body lemma holds for ALL `k ≥ 0`, both parities** (formal composition), strictly
  extending the note's odd `k ≥ 19` grid claim (red-team had k ≥ 13 "conservative"). Grid
  anchor preserved: `example : steps 91 (Bcfg 19 0) = some (Bcfg 21 (-1)) := body_step 19 0`;
  the k = 251 red-team point runs in `#eval` at every build.
- **The §2.4 generalization argument (episode-landmark pinning + first-divergence) is
  REPLACED, for the body and prefix lemmas, by machine-checked induction/symbolic
  computation** — for these lemmas the method's grid-certification caveat is GONE. The prefix's
  G,a-uniformity is exactly "the symbolic suffix `Y` is never inspected", now a kernel fact.
- `body_nonhalt` is a new fully-formal non-halting theorem for the standalone bouncer family
  `B(k)` (the `O4_GROWING_REGIME` growing-bouncer flavor, with the `1001` cap).
- Prefix validity extended G ≥ 37 → **G ≥ 31**; the real-orbit milestone form is pinned by
  kernel computation (steps 731/1548), and one real generation is driven formally to its
  suffix entry (step 2431).

## Numeric sanity (all green)
- Lean `#eval` at build: N=100 config print; k=251 body check `true`.
- `lean/template_crosscheck.py`: N=100/1000 zipper == Lean anchors; zipper == independent
  dict-tape semantics; body k = 0..60, 101, 251; body_iter r=10; the five body proof
  landmarks at k=5; prefix471 with adversarial suffixes; milestone grid G=31..501;
  body_step_ctx grid; real-orbit anchors at steps 1548 and 2431. ALL OK (exit 0).

## Build commands (exact)
```
export PATH="$HOME/.elan/bin:$PATH"
cd /Users/aokiyousuke/busybeaver/lean
lake build                          # RunStructure + Template; axiom audit prints
/usr/bin/python3 template_crosscheck.py
```

## What's left (honest)
- The SUFFIX lemmas (3 classes g ∈ {3,4,5}, plus the per-a small-parameter templates) — not
  attempted; they are the remaining unformalized template piece.
- Hence the full generation map `M(G,a) → M(G′,a′)`, the derived odometer `G′ = ⌊4G/3⌋ + c`,
  and the a-ledger law stay on the lab-note record (the arithmetic layer is already formal in
  `RunStructure.lean`).
- o4's decision status is untouched: the a-ledger conjecture remains the open core.

**No machine decided. No label upgraded.**
# SUFFIX + GENERATION-MAP APPEND (2026-07-08) — the o4 SUFFIX lemmas AND the FULL GENERATION MAP are FORMALIZED

*Third formalization target: the suffix lemmas (`O4_TEMPLATE_CLOSURE_2026-07-06` §2, all 3 classes
incl. the small-filler per-parameter case) and — the milestone — the full generation composition
`M(G,a) → M(⌊4G/3⌋+c, a+δ)`. New module `lean/Suffix.lean` (imports Template only; same
zero-dependency project; compiles in ≈11 s). Cross-check `lean/suffix_crosscheck.py` (zipper AND
independent dict-tape semantics). Not committed.*

## Verdict: ALL FOUR TARGETS FORMALIZED (S1 configs, S2 g=3, S3 g=4/g=5(+small), S4 generation map)

Convention (important): the Lean filler count equals the lab-note/`O4_TEMPLATE_CLOSURE` count and
the Python `o4_redteam_suffix.py` count PLUS ONE (`(10)^a 01 = (10)^{a_py} 1001`, `a = a_py + 1`);
pinned against the real orbit (`Mcfg 43 18` at step 1548 ↔ dump `gap=43, a_py=17`).

| Target | Lean theorem(s) in `Suffix.lean` | Status |
|---|---|---|
| **S1: suffix configs** | `Zcfg k g a p` (= `BcfgCtx k p (0^g ++ filler)`, definitionally the `prefix_bodies` landing shape); `#eval` anchors vs Python at Z(19,3,4), k=251, Z(41,3,0), Z(19,4,8), Z(21,4,0), Z(23,5,8), Z(19,5,0) | **FORMALIZED** |
| **S2: g=3 class** | `suffix_g3 : Z(k,3,a+1) → M(2k+12, a)` shifted −3 in exactly `8k+35` steps, ALL `k`, ALL filler ≥ 1; new sweep **`sweepAD`** (the `A1D0` leftward ERASER, arbitrary length by 2-transition induction — the third o4 sweep flavor, converts zone → next gap) + episodes `capEnter4`, `fin2` | **FORMALIZED** |
| **S3: g=4, g=5** | `suffix_g4 : Z(k,4,a+1) → M(2k+9, a+5)` in `8k+8a+71`; `suffix_g5 : Z(k,5,b+2) → M(2k+13, b+8)` in `12k+16b+164`; **`suffix_g5_small` : Z(k,5,1) → M(2k+13, 7)` in `12k+148`** (the lab's genuine per-parameter skeleton, k-parametric via two fixed 38/58-step kernel-checked episode words); episodes `ep2DA`, `turn3A1`, `turnL3_int`, `gapSkip5`, `seamGap8` | **FORMALIZED** |
| **S4: the generation map** | `gen_mod1/gen_mod2/gen_mod0/gen_mod0_small` (`M(G,a) → M(G′,a′)` with EXACT step counts, `G = 34/35/36 + 3s`, all `s`, filler ≥ 1); **`generation_odometer`** (master: `G ≥ 34`, filler ≥ 1 ⇒ `M(G,a) → M(4G/3 + cOdo G, ledgerNext G a)`) — **the base-4/3 odometer `c = {0→3,1→5,2→1}` and the a-ledger `δ = {1→−1,2→+4,0→+6}` are now DERIVED inside Lean**; `odometer_arith`; real-orbit anchor `real_next_milestone` (blank tape → step **2551** = `M(62,17)` at −59 = the 43→62 generation, matching the instrumented dump) | **FORMALIZED** |

## Axiom audit (printed at every build, `#print axioms` in-file)
**All 12 audited theorems (`sweepAD`, 4 suffix classes, 4 gen classes, `generation_odometer`,
`odometer_arith`, `real_next_milestone`): `[propext, Quot.sound]` only** — no `sorryAx`, no
`Classical.choice`, no `native_decide`. No `sorry` anywhere; full `lake build` green.

## What the formalization ADDS to the lab-note record (statement deltas, all sound)
- **Suffix validity extended:** the lab table's floors (`a_py ≥ 2` at g=3; per-a templates
  `a_py ≤ 4`) are ITERABILITY thresholds, not template thresholds. The formal lemmas hold for ALL
  `k ≥ 0` (lab grid: odd k ≤ 251) and ALL filler ≥ 1 (= `a_py ≥ 0`) — one parametric proof per
  class; the sweep inductions absorb the per-a small templates. Only g=5 `a_py = 0` is genuinely
  a different skeleton (`suffix_g5_small`, also k-parametric — stronger than the lab's per-a form).
- **`Z(41,3,0)_py` (the halting configuration's shape) DOES follow the g=3 template**: it lands on
  the DEGENERATE milestone `M(94, 0)` (filler `01`) at step 363; the lab-observed halt at 55,170
  is downstream, where the next generation's suffix needs filler ≥ 1. This sharpens the small-a
  story: failure is a next-generation event, not a suffix deviation.
- **The generation map is now a single machine-checked theorem chain** (prefix471 · body^s ·
  suffix_g composed): the odometer law and the ledger law are theorems, not observations. The step
  count of a full generation is exact (e.g. 1003 steps for 43→62; kernel-checked 1548+1003 = 2551
  against the real orbit).
- The o4 reduction machine → arithmetic is machine-checked END TO END: the ONLY informal content
  left in the o4 decision is the a-ledger conjecture itself (does the base-4/3 orbit's residue
  sequence keep the ledger ≥ 2 before every G≡1 drain? — `O4_TEMPLATE_CLOSURE` §5, OPEN).

## Numeric sanity (all green)
- Lean `#eval` at build: 7 suffix anchors + generation grid anchor (M(100,9) → M(138,8)) + the
  2551 step count; all `true`.
- `lean/suffix_crosscheck.py`: suffix grids k = 0..30, 101, 251 × filler grid, all 4 classes;
  zipper vs independent dict-tape at 4 suffix runs; generation map G = 34..60, 100, 275, 367 ×
  a grid incl. odometer/ledger arithmetic; real-orbit anchor at 2551. ALL OK (exit 0).
  `template_crosscheck.py` still ALL OK.

## Build commands (exact)
```
export PATH="$HOME/.elan/bin:$PATH"
cd /Users/aokiyousuke/busybeaver/lean
lake build                          # RunStructure + Template + Suffix; axiom audits print
/usr/bin/python3 suffix_crosscheck.py
```

## What's left (honest)
- The a-ledger conjecture (the open core): *the orbit `G ↦ ⌊4G/3⌋ + c` from the real seed keeps
  `ledgerNext`-iterates ≥ 2 at every G≡1 step*. `generation_odometer` makes each single step
  formal; the INDUCTION along the real orbit (and hence o4's fate) needs exactly this conjecture.
- Formal glue not attempted: a Lean statement of "the real orbit's milestone sequence" as an
  inductively-defined object (currently each generation instantiates the theorem separately, as
  in `real_next_milestone`); the G ∈ {31,32,33} sub-prefix classes (never reached: the real orbit
  enters at G = 43).
- o4's decision status is untouched.

**No machine decided. No label upgraded.**
