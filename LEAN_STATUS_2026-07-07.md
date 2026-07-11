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
# O3 APPEND (2026-07-08) — a SECOND fully-formalized machine: o3's period 10/20/6 sweeps are FORMALIZED (L1–L2, L3 partial)

*Second machine formalized (after o4): the BB(6) cryptid
`o3 = 1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC`, mirroring the
`Template.lean` zipper/step/sweep-by-induction architecture but for o3's
RICHER cycle structure — where o4's sweeps are period-2, o3's are period
**10 / 20 / 6** (`O3_TEMPLATE_PORT_2026-07-06.md`). New module `lean/O3.lean`
(same zero-dependency project; `lake build` builds all four libs, O3 ≈ 7 s;
own namespace `O3`, machine-independent scaffolding copied from `Template`).
Cross-check `lean/o3_crosscheck.py` (faithful zipper AND independent dict-tape
sims). Not committed.*

## Verdict: L1 FORMALIZED, L2 FORMALIZED (all THREE cycle lemmas), L3 partial (`body_phase1` FORMALIZED; full body DRAFTED)

| Target | Lean theorem(s) in `O3.lean` | Status |
|---|---|---|
| **L1: the machine** | `St`/`Tape`(zipper)/`Cfg`, `step` (`none` ⟺ o3's halt gate `F` reads `0` = "`E` reads `0` with right-neighbour `0`"), `steps`, `steps_add`; kernel `rfl` anchors `sanity100`, `sanity300` (full config at N=100/300 vs two Python sims) | **FORMALIZED** |
| **L2: sweep 1 — period-10 rightward crawl** | `crawlR_tile` (one 10-step tile: reads `[A] 0 0 (10)^3`, marches `+6`, deposits marker `dep6 = 111011`), **`crawlR`** (ARBITRARY length `n` by tile+length induction: `[A] 0 0 (10)^(k+3n) M → [A] 0 0 (10)^k M` shifted `+6n`, `dep6n n` deposited) | **FORMALIZED** |
| **L2: sweep 2 — period-20 leftward crawl** | `crawlL_tile` (one 20-step tile: consumes one `dep6` block, deposits `(01)^3`, `−6`; fully right-context-independent), **`crawlL`** (ARBITRARY `n`: consumes `dep6n n`, deposits `(01)^(3n)`, `−6n`) | **FORMALIZED** |
| **L2: sweep 3 — period-6 zigzag** | `zigzag_tile` (one 6-step tile: consumes `11`, prepends `10`, `−2`), **`zigzag`** (ARBITRARY `n`: consumes `(11)^n`, prepends `(10)^n`, `−2n`) | **FORMALIZED** |
| **L3: body lemma** | `Bcfg j = 0^∞ [A] 0 0 (10)^j 1 1 0^∞`; **`body_phase1`** (`j=3m`: the first `10m` steps of the real body ARE `m` crawlR tiles → `dep6n m` deposit at the defect, an exact instance of `crawlR` on the live body config). Full `B(j)→shift(−2) B(j−3)` in `10j+4` steps: decomposition `crawlR^(j/3)·[A0 B0]·zigzag^3·[eps]·crawlL^(j/3−1)·[eps]` (zigzag count is a FIXED 3; verified `j=12…51`) — the fixed turnaround + leftward return not composed in Lean | **`body_phase1` FORMALIZED; full body DRAFTED** |

## Axiom audit (printed at every build, `#print axioms` in-file)
**All 10 audited theorems** (`steps_add`, `crawlR_tile`/`crawlR`,
`crawlL_tile`/`crawlL`, `zigzag_tile`/`zigzag`, `body_phase1`): **`[propext,
Quot.sound]` only** — no `sorryAx`, no `Classical.choice`, no `native_decide`.
`sanity100`/`sanity300` depend on **no axioms at all**. No `sorry` anywhere;
`lake build` green.

## What the formalization establishes (the core challenge)
- **All three of o3's sweeps are formalized as arbitrary-length uniform-
  crossing lemmas** — the flagged "core challenge" (`O3_TEMPLATE_PORT` says
  even ONE would be a result; all three are done). Each is a `p`-transition
  "one tile" kernel-`rfl` lemma (reading a bounded window) + a length
  induction over the deposited/consumed marker word — strictly harder than
  o4's period-2 sweeps (`crawlL_tile` is a 20-step kernel reduction; the
  crawls read AHEAD of their advance, offset `+7` vs advance `+6`, so the
  tile carries lookahead the induction absorbs).
- **The period-10 crawl is verified to BE the real body's first phase**
  (`body_phase1`, an exact `crawlR` instance on `Bcfg (3m)`), and `#eval`
  kernel-executes the FULL `B(j)→B(j−3)` chunk (state A at pos −2, halt-free)
  for j = 15, 18, 24 — the crawls are the real building blocks.

## Numeric sanity (all green)
- Lean `#eval` at build: `crawlR` grid point (n=6) `true`; `body_phase1`
  (j=18) `true`; full body (st,pos) checks j=15/18/24 `true`.
- `lean/o3_crosscheck.py`: L1 anchors vs zipper+dict sims; crawlR/crawlL/
  zigzag grids (all three sweeps, several n); `body_phase1` m=4…17; full
  body j=12…51 (zipper==dict, halt-free, lands (A,−2)); o3 halt gate
  (standalone `M(a,0)`, a≡2 mod 3, HALTS). **ALL OK** (exit 0).

## Build commands (exact)
```
export PATH="$HOME/.elan/bin:$PATH"
cd /Users/aokiyousuke/busybeaver/lean
lake build                          # RunStructure + Template + Suffix + O3
/usr/bin/python3 o3_crosscheck.py
```

## What's left (honest)
- The full o3 body lemma composition (the fixed zigzag turnaround + the
  leftward crawlL return, threading the marker deposit and the right/gap
  context) — DRAFTED: structure and exact tile counts (crawlR = j/3,
  zigzag = 3, crawlL = j/3−1) verified computationally, `body_phase1`
  formalized, but the episode glue between the sweeps is not yet Lean.
- Hence o3's generation map / the (a,k) counter ledger (`O3_TEMPLATE_PORT`
  §3–5, the swapped-roles base-4/3 odometer) stay on the lab record.
- o3's decision status is untouched: the (a,k)-ledger conjecture is OPEN.

**No machine decided. No label upgraded.**
# MIRROR APPEND (2026-07-08) — the UNIFORM fixed-point run theorem is FORMALIZED for arbitrary base q

*Fourth formalization target: the single ABSTRACT theorem that makes every Type-I cryptid's run
law a corollary (`PAPER_MIRROR_LADDER.md` §1). Generalizes `RunStructure.lean`'s q=3 `v3`/
`v3_step_down`/`run_closed_form` to an ARBITRARY base `q ≥ 2` and a general branch map. New module
`lean/Mirror.lean` (same zero-dependency, zero-mathlib project; `lake build Mirror` ≈ 0.5 s; own
namespace `Mirror`, arithmetic over ℤ). Subsumes `mirror_census.py`. Not committed.*

## Verdict: ALL FOUR TARGETS FORMALIZED

Toolchain Lean **4.31.0**, no mathlib (core `Int`/`Nat` + `omega`; from-scratch `q`-adic valuation
`vqn`/`vq`). **Axiom audit (every crown theorem): `[propext, Quot.sound]` only** — no `sorryAx`, no
`Classical.choice` (note: `Nat.mul_lt_mul_right` pulls in `Classical.choice`, so `k < q·k` is proved
Classical-free via `lt_mul_self` using `Nat.mul_le_mul` + `omega`), no `native_decide`. No `sorry`.

| Target (spec) | Lean theorem(s) in `Mirror.lean` | Status |
|---|---|---|
| **1. `vpadic q v`** (q-adic valuation from scratch, q≥2) + basic lemmas | `vqn` (guarded recursion, terminates for VARIABLE base via `Nat.div_lt_self`), `vqn_of_dvd`/`vqn_of_not_dvd`, **`vqn_q_mul`** (`v_q(q·n)=v_q(n)+1`), and — the crux below — the unit lemma; ℤ wrappers `vq`, `vq_q_mul`, `vq_unit_mul`, `vq_pos_dvd`, `vq_eq_zero_not_dvd` | **FORMALIZED** |
| **1-crux. coprime ⇒ valuation preserved** | **`vqn_unit_mul`** (`gcd(u,q)=1 → v_q(u·n)=v_q(n)`), resting on **`vqn_euclid`** (Euclid: `gcd(u,q)=1 ∧ q∣u·n → q∣n`) proved from scratch via `gcd(u·n,q·n)=gcd(u,q)·n=n` (`Nat.gcd_mul_right`+`Nat.dvd_gcd`, both core) | **FORMALIZED** |
| **2. abstract branch map + fixed point** | `bmap p e q v = (p·v+e)/q`; **`branch_conj`** (at integer fixed point `q·x=p·x+e`, on-branch `q∣(v−x)`: `q·(bmap v − x) = p·(v−x)`, incl. integrality of `bmap` there); **`vq_step_down`** (`q·a=p·b, q∣b, b≠0, gcd ⇒ v_q(a)+1=v_q(b)`) | **FORMALIZED** |
| **3. the uniform run theorem** | `orb` (orbit of `bmap`); **`run_invariant`** (`v_q(orb i − x)=v_q(v−x)−i` ∧ `orb i − x ≠ 0` inside the run); **`run_closed_form`** (maximal run = `v_q(v−x)`: branch residue `≡ x (mod q)` persists for all `i < v_q(v−x)` and breaks at `i = v_q(v−x)`, both halves); **`run_cap`** (`q^{v_q n} ≤ |n|`, i.e. run `≤ log_q|v−x|`) | **FORMALIZED** |
| **4. census corollaries** (each `= run_closed_form` at concrete `(p,q,e,x)`; obligations `gcd`+fixed-point by `decide`/`omega`) | `antihydra_even` (x=0), `antihydra_odd` (x=1); `o16_even/odd` (x=−4,−3); `o11_even/odd` (x=−8,−7); `o4_r0/r1/r2` (q=3, x=−9,−14,−1); `o15_queued` (q=3, x=1 = o18 depth push); `space_needle_even` (×5/2, q=2, x=0) | **FORMALIZED** |

The single `run_closed_form` covers the whole (2,3)/(2,5)-even/(3,4)/(3,8) ladder; `x`-values match
`PAPER_MIRROR_LADDER.md` §2 and `mirror_census.py`. Space Needle's ODD branch is out of scope (no
single fixed point, per paper §3) — only its even branch is a corollary.

## The coprime→valuation lemma (the mathematical content), proof approach
`vqn_unit_mul` by strong induction on `n`: (i) `n=0` trivial; (ii) `q∣n`, write `n=q·k`, then
`u·(q·k)=q·(u·k)` and `v_q` drops the shared `q` on both sides, IH on `k`; (iii) `q∤n`, then by
`vqn_euclid` (Euclid's lemma) `q∤u·n`, so both valuations are `0`. Euclid is the ONLY place
coprimality is used and is proved WITHOUT Bézout: `q ∣ u·n` and `q ∣ q·n` give `q ∣ gcd(u·n,q·n) =
gcd(u,q)·n = 1·n = n` (core `Nat.gcd_mul_right`, `Nat.dvd_gcd`). This is the general-`q` replacement
for RunStructure's hard-wired `pow3_dvd_of_dvd_four_mul`/`v3n_unit_mul` ("4 is a unit mod 3^L").

## Which census machines are now corollaries
Antihydra (both branches), o16, o11 (hence o14/o13-flavor by the same closure), o4 (all three
residue branches — the entire `RunStructure.lean` o4 run law is now a special case), o15/o18, and
Space Needle's even branch — nine `example`-grade theorems, each a one-line specialization of
`run_closed_form`. The lab-note per-machine run laws are now instances of ONE Lean theorem.

## Numeric sanity (green) + build
- Lean `#eval` at build: `[vq 2 12, vq 2 6, vq 3 57, vq 3 39] = [2,1,1,1]`; `vqCheck` (self-
  consistency vs `vqn` over a range) `true`. `mirror_census.py` (ALL RUN LAWS VERIFIED) is the
  independent Python mirror this module subsumes.
- Build: `export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build Mirror` (green, axiom prints).

## What's left (honest) / statement fidelity
- The run law is formalized as: residue `(orb i − x) % q = 0` persists for `i < v_q(v−x)` and fails
  at `i = v_q(v−x)` (the abstract mirror of RunStructure's `run_closed_form`; "branch residue" =
  `≡ x (mod q)`, which for q=2 is the parity used in the paper). No hypothesis of positivity on `v`
  is needed — only `v ≠ x`.
- Off-branch dynamics (where `bmap` is not the true affine map) are out of scope by construction —
  the theorem governs only the same-branch run, which is all the run law asserts.
- Space Needle's odd branch (no fixed point), and the census's criticality/ledger-memory axes
  (`PAPER_MIRROR_LADDER.md` §4), are NOT formalized — they are not part of the uniform depth theorem.
- Nothing here decides any machine; it is the elementary p-adic depth layer, made uniform.

(Concurrent-session note: at build time `lean/O3.lean` was mid-edit by another session and did not
compile; `Mirror.lean` is independent and builds/audits clean on its own via `lake build Mirror`.)

**No machine decided. No label upgraded.**

---

# O3 BODY-LEMMA APPEND (2026-07-09) — o3's FULL body lemma is now FORMALIZED: the SECOND machine with a complete, sorry-free defect-transport chunk

*Completes the o3 append above (which had `L3 partial`: `body_phase1` FORMALIZED, full body DRAFTED).
The full episode glue is now composed and machine-checked. `lean/O3.lean` extended in place; STRICT
labels as above. Not committed.*

## Verdict: L3 FULLY FORMALIZED — `body_step` + `body_iter` + `body_descent`

The standalone o3 body chunk `B(j) = 0^∞ [A] 0 0 (10)^j 1 1 · G → shift(−2) of B(j−3)` (gap `G`
grown by one word `0101 0101`) in EXACTLY `10j + 4` steps, for every `j ≡ 0 (mod 3)`, `j ≥ 3`, and
ARBITRARY right context `G`, is proved by gluing the three FORMALIZED sweeps to three fixed episodes.

| Target (spec) | Lean theorem(s) in `O3.lean` | Status |
|---|---|---|
| **1. full body glue** `B(j) → shift(−2) B(j−3)` in `10j+4` | **`body_step`** (`steps (30·m'+34) (BodyCfg (3(m'+1)) p G) = some (BodyCfg (3m') (p−2) (pow01 4 ++ G))`), composing `crawlR^(m'+1) · [A0 B0] · zigzag^2 · mid8 · crawlL^(m') · [D1 C0]`; helpers `ep_intro`/`ep_mid8`/`ep_final` (fixed episodes, symbolic tails, `rfl`), `BodyCfg` (position + gap context) | **FORMALIZED** |
| **the config-identity that unblocked the glue** | **`cons_pow01`** (`true :: (01)^n = (10)^n · 1`) + `cons_pow01'`/`landing_id` — converts the leftward crawl's deposited `(01)` fabric into the `(10)` marker the next pass reads | **FORMALIZED** |
| **2. iterated body / halt-free descent** | **`body_iter`** (`r`-fold: `BodyCfg (3(M+r)) p G → BodyCfg (3M) (p−2r) (pow01 (4r) ++ G)` in `bodyTime r M` steps) and **`body_descent`** (`M`-fold to `BodyCfg 0`) — `some` = halt-free (all-`E`-reads-0-safe) over the whole descent | **FORMALIZED** |

## The config-identity that unblocked the glue (and the DRAFTED-skeleton corrections)
Concrete recomputation (`o3_zipper.py`/`o3_detect.py`, cross-checked vs the trace for `m = 1..19`
and three gap contexts) showed the DRAFTED `zigzag^3` was really **`zigzag^2`**: the 3rd
period-6-shaped tile lands its head on a `0` (so it is NOT a `zigzag_tile` — those end on a `1`);
it is a different phase, absorbed into a fixed **8-step `mid8`** turnaround (`C1 B1 E1 A1 D0 D1 C0 A1`)
that reads only a 4-cell left window `[1 0 1 1]` and 2 of a 5-cell right window `[1 0 1 0 1]` — the
"shared marker region" the earlier note flagged — leaving both tails UNTOUCHED (locality ⇒ arbitrary
`G`). The leftward return is `crawlL^(m')` (= `crawlL^(j/3−1)`). Step count closes exactly:
`10(m'+1) + 2 + 12 + 8 + 20m' + 2 = 30m' + 34 = 10·(3(m'+1)) + 4`. The LANDING config-identity is
`cons_pow01 : true :: pow01 n = pow10 n ++ [true]` (proved by induction, axiom-free) — the o3
analogue of o4's `pow01_of_pow10`; assembled by `landing_id` it shows the leftward crawl's `(01)^{3m'}`
deposit, re-read shifted by one cell, is exactly the `(10)^{3m'}` zone the next `B(j−3)` pass consumes.

## Honest scope note (why `body_iter`, not an infinite non-halt)
Unlike o4's body (which GROWS the zone, so `body_nonhalt` is an infinite non-halting certificate),
o3's body SHRINKS `j` by 3 per pass and bottoms out at `BodyCfg 0`, whose fate depends on the
accumulated gap (`o3_b0.py`: `BodyCfg 0` HALTS for a short gap, survives for a long one). So the
honest o3 certificate is the FINITE halt-free descent `body_descent` (its `some` output is the
all-safe guarantee); o3's actual haltedness is the ledger conjecture and stays `[OPEN]`.

## Axiom audit (printed at every build via in-file `#print axioms`)
`body_step`, `body_iter`, `body_descent`, `ep_mid8`, `landing_id`: **`[propext, Quot.sound]`** only
(`landing_id` `[propext]`; `cons_pow01` depends on NO axioms). No `sorryAx`, no `Classical.choice`,
no `native_decide`. Two `#eval decide` sanity checks (`body_step` at `j=12`; `body_iter` r=3,M=1)
print `true` (kernel-executed against `o3_zipper.py`).

## Build (exact)
`export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build O3` — **green** (`Build completed
successfully`). Full `lake build` green (all modules).

**No machine decided. No label upgraded.**

---

# MIRROR CENSUS-COMPLETION + CRITICALITY APPEND (2026-07-09) — the FULL §2 census and the abstract CRITICALITY theorem are FORMALIZED in `Mirror.lean`

*Fifth extension of `lean/Mirror.lean` (the uniform base-`q` run theorem). Two targets:
(a) complete the census so EVERY machine in `PAPER_MIRROR_LADDER.md` §2 is a Lean
corollary, and (b) formalize the run-cap-slope / budget-slope comparison that orders
the mirror ladder — kept in pure `ℕ`/`ℤ` (no real logarithms). STRICT labels as above;
`lake build Mirror` green, full axiom audit clean. Not committed.*

## Verdict: BOTH targets FORMALIZED. `lake build Mirror` green; all 20 audited theorems `[propext, Quot.sound]` only (no `sorryAx`, no `Classical.choice`, no `native_decide`); zero `sorry`.

### (a) Census now COMPLETE — every §2 machine is a `run_closed_form` corollary

Added six one-line specializations (each `run_closed_form (by decide) (by decide) (by omega)`):

| machine | Lean theorem(s) | (p,q,e) → fixed point x | run law |
|---|---|---|---|
| **o14** (o11 twin) | `o14_even`, `o14_odd` | (3,2,12)→−12, (3,2,11)→−11 | v₂(a+12), v₂(a+11) |
| **o13** (o12-flavor) | `o13_even`, `o13_odd` | (3,2,14)→−14, (3,2,7)→−7 | v₂(a+14), v₂(a+7) |
| **o2** (ceiling ×3/2) | `o2_even`, `o2_odd` | (3,2,0)→0, (3,2,1)→−1 | v₂(y), v₂(y+1) |

**o2 ceiling status (the flagged subtlety): NO ceiling variant of the abstract lemma
was needed.** On each parity branch `⌈3y/2⌉` is affine — even `y`: `3y/2` (e=0);
odd `y`: `(3y+1)/2` (e=1) — and on-branch (`2 ∣ 3v+e`) the division is exact, so
`bmap 3 e 2` coincides with the true ceiling map for the whole run. Both branches are
therefore plain `run_closed_form` instances. Fidelity note: the §2 table's "fixed
points (0,1)" lists the odd **correction** `c_o=1`; the run-law-consistent odd fixed
point is `x = 1−2c_o = −1`, giving `run = v₂(v+1) = v₂(y+1)` exactly as tabulated
(and as `mirror_census.py` verifies). With these, the census corollaries are:
Antihydra, o2, o16, o11, o14, o13 (all ×3/2), o4 (three ×4/3 branches), o15/o18 (×8/3),
Space Needle even (×5/2) — **all of §2**; Space Needle's odd branch stays out of scope
(no single fixed point, paper §3).

### (b) The criticality comparison — abstract, integer, FORMALIZED (`Mirror.lean` §6)

The real-number slopes `ρ = log_q(p/q)` (run-cap) and `β` (budget) appear ONLY in
comments; everything provable is exponentiated to `ℕ`:

- **`run_cap_le`** : `|n| ≤ B ⇒ q^(v_q n) ≤ B` (run_cap + a bound).
- **`run_cap_slope`** : `|n|·q^k ≤ C·p^k ⇒ q^(v_q n + k) ≤ C·p^k` — the integer form of
  `run ≤ k·log_q(p/q) + log_q C`; the coefficient of `k` **is** `ρ = log_q p − 1`.
- **`criticality_core`** : single-run fatality `b ≤ r`, run bound `q^(r+k) ≤ C·p^k`,
  budget slope `(β+1)·k ≤ b+k` ⟹ `q^((β+1)·k) ≤ C·p^k`.
- **`geom_binom`** (`p^(k+1)+k·p^k ≤ p·(p+1)^k`, elementary induction) → **`geom_horizon`**
  (`1 ≤ p < base, k ≥ C·p ⇒ C·p^k < base^k`): the pure-ℕ fact that `q^(β+1)` outgrows
  `C·p^k` once `p < q^(β+1)` — this integer condition **is** `ρ < β` (since
  `log_q p − 1 < β ⇔ p < q^(β+1)`).
- **`criticality_excluded`** (abstract punchline) : add subcriticality `p+1 ≤ q^(β+1)`;
  then core ∧ horizon are contradictory ⟹ single-run fatality is impossible for `k ≥ C·p`.
- **`o4_criticality_excluded`** : `(q,p,β) = (3,4,3)`, subcriticality witness the integer
  `p+1 = 5 ≤ 81 = 3⁴`. ρ = log₃(4/3) ≈ 0.262, β = 3, ρ/β ≈ 0.087 < 1: **single maximal
  3-adic run CANNOT exhaust the linearly-growing budget past the horizon `k ≥ 4C`.**

**Antihydra is the criticality boundary and the lemma does NOT apply**: its budget slope
`β = 1/2` is non-integer (cannot instantiate the ℕ-lemma at all), and the subcriticality
test would be `p+1 = 4 ≤ 2^(3/2) ≈ 2.83` — FALSE (`ρ/β = log₂(3/2)/(1/2) = 1.1699 > 1`).
The integer-vs-commented split is exactly as the task specified: the exponentiated
inequalities are theorems; the logarithmic slope reading (and Antihydra's non-integer β)
are comments.

## What is integer (Lean-proved) vs commented
- **Integer / proved:** all run laws (`run_closed_form` + 17 census corollaries), the
  run cap `q^(v_q n) ≤ |n|`, the slope-exponentiated `q^(run+k) ≤ C·p^k`, the geometric
  horizon, `criticality_core`, `criticality_excluded`, and the o4 instance — all in ℕ/ℤ.
- **Commented only:** the identification of the `k`-coefficient with `log_q(p/q)`, the
  numeric slope values (0.262, 0.087, 0.585, 1.1699), and Antihydra's non-integer β.

## Axiom audit (printed at build) + sanity
All twenty `#print axioms` targets (incl. `o13_odd`, `o14_even`, `o2_odd`, `geom_binom`,
`geom_horizon`, `run_cap_slope`, `criticality_core`, `criticality_excluded`,
`o4_criticality_excluded`): **`[propext, Quot.sound]` only.** `geom_horizon` was made
Classical-free by avoiding `Nat.mul_lt_mul_right`/`Nat.lt_of_mul_lt_mul_left` (both pull
`Classical.choice`) — the strict step uses `Nat.mul_le_mul` + `omega`, the cancellation
uses `Nat.lt_or_ge` + `Nat.not_lt`. `#eval` sanity: `decide (5 ≤ 3^4) = true` (o4
subcritical), `decide (1·4^4 < 81^4) = true` (horizon at k=C·p=4). `mirror_census.py`
independently reconfirms o13 x=(−14,−7), o14 x=(−12,−11) (ALL RUN LAWS VERIFIED).

## Build (exact)
```
export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build Mirror   # green, audit prints
/usr/bin/python3 ../mirror_census.py                             # ALL RUN LAWS VERIFIED
```

**No machine decided. No label upgraded.**

---

# O18 APPEND (2026-07-09) — a THIRD machine toward formalization: o18's L1 machine + BOTH period-2 sweeps + one m-parametric branch tail are FORMALIZED

*Exploratory third formalization target (after o4, o3): the BB(6) pushdown-odometer cryptid
`o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` (halt = F reads 1), mirroring the
`Template.lean`/`O3.lean` zipper/step/sweep-by-induction architecture. New module `lean/O18.lean`
(same zero-dependency, zero-mathlib project; `lake build O18` ≈ 0.5 s; own namespace `O18`).
Cross-check `lean/o18_crosscheck.py` (independent zipper sim). Goal: L1 + one/two structural
lemmas, honestly labeled, pinning the exact scale-obstacle for a future full effort. Not committed.*

## Verdict: L1 FORMALIZED, L2 FORMALIZED (BOTH sweeps), L3 FORMALIZED (the clean-reset formation tail)

| Target | Lean theorem(s) in `O18.lean` | Status |
|---|---|---|
| **L1: the machine** | `St`/`Tape`(zipper)/`Cfg`, `step` (`none` ⟺ o18's halt gate `F` reads `1` = "`D` reads a `1` with left-neighbour `1`"), `steps`, `steps_add`; kernel `rfl` anchors `sanity100`, `sanity300` (full config at N=100/300 vs the Python sim) | **FORMALIZED** |
| **L2: sweep 1 — rightward `A0·B1` crawl** (net `+2`) | `sweepAB_tile` (one 2-step tile: reads `[A] 0 (10)`, marches `+2`, deposits `(01)`), **`sweepAB`** (ARBITRARY length `k` by tile+`pow01_mid` induction: `[A] 0 (10)^k M → [A] 0 M` shifted `+2k`, `(01)^k` deposited — the filler-inversion pass, o18's `sweepBF`/`sweepDE` analogue) | **FORMALIZED** |
| **L2: sweep 2 — leftward `D0·C1` crawl** (net `−2`) | `sweepDC_tile` (one 2-step tile: reads `[D] 0` over `(10)` on the left, deposits `1 1` on the right, `−2`), **`sweepDC`** (ARBITRARY `k` by tile+`ones_mid` induction: consumes `(10)^k` from the left, BUILDS the clean block `1^(2k)` on the right, `−2k`; `R` untouched — the clean-reset-formation sweep) | **FORMALIZED** |
| **L3: one m-parametric branch tail** | `gate_episode` (fixed 3-step `D0·C1·D1`: collapses `[D] 1 1` into the F-gate, symbolic tail `R` untouched); **`clean_gate`** (`steps (2k+3) ⟨D, p, (10)^k 1 1 R⟩ = some ⟨F, p−2k−3, 0 1^(2k+3) R⟩`, the CLEAN-RESET FORMATION uniform in block length `k` = the LAND-branch `→ C_L` tail); **`clean_reset`** (`R=[]`: the fresh reset `C_(2k+4)`). `some` output ⇒ halt-free AND the landing gate is SAFE (`F` reads `0`, not the halting `1`) | **FORMALIZED** |

## Axiom audit (printed at every build via in-file `#print axioms`)
**All 8 audited theorems** (`steps_add`, `sweepAB_tile`/`sweepAB`, `sweepDC_tile`/`sweepDC`,
`gate_episode`, `clean_gate`, `clean_reset`): **`[propext, Quot.sound]` only** — no `sorryAx`,
no `Classical.choice`, no `native_decide`. `sanity100`/`sanity300` depend on **no axioms at all**.
No `sorry` anywhere; `lake build` green (all six modules). Three `#eval decide` sanity checks
(sweepAB k=5, sweepDC k=5, clean_gate/`C_16` k=6) print `true` (kernel-executed).

## What this establishes (the exploratory finding)
- **o18's in-cell crossings are architecturally the SAME as o4's** — both period **2**, both an
  arbitrary-length uniform-crossing lemma by a one-tile kernel-`rfl` + a `_mid` length induction.
  o18 is *easier* at the sweep layer than o3 (period 10/20/6). The `×8/3` pushdown structure lives
  entirely in the branch ARITHMETIC (already formal, machine-independent, in `Mirror.lean`'s
  `o15_queued`/`RunStructure.lean`'s stretch), NOT in the tape sweeps, which are plain period-2.
- **The clean-reset formation is now an m-parametric theorem**: every LAND branch's shared tail
  (`→ C_L`) is `sweepDC^k · gate_episode`, giving a fresh SAFE F-gate uniformly in the 1-block
  length — the o18 analogue of o3/o4's `body_step` composition, at the clean-reset (`C_N`) level.

## The exact scale-obstacle to going further (pinned)
- The **full single-defect transition `D(m,t,e) → …`** (`O18_DEPTH_UNIFORM` §2 table) needs the
  DEFECT-TURNAROUND front-end: the passage over `1^m 0 (10)^t 1^e`, whose branch (LAND/PUSH/POP/
  FLUSH/RECYCLE/EXIT) depends on `m mod 3` and on `(t,e)`. That front-end is NOT a single uniform
  sweep — it is a per-residue composition of the two sweeps with several fixed episodes and an
  `m`-dependent number of tiles (the `m′−1=(8/3)(m−1)` push law). Formalizing even ONE full branch
  (e.g. POP or a LAND from a real `D(m,t,e)`) would require pinning that residue-indexed episode
  algebra — the same effort scale as o3's full `body_step`, times the 8-row branch table.
- The **multi-defect word grammar** (`O18_DEPTH_UNIFORM` §5, the true-orbit exit at tower-step 8394)
  is entirely out of scope — it is the open blocker even at the lab-note level.
- Consequently the transition table's laws (`[PROVEN on grid]`), the derived `×8/3` odometer, and
  o18's fate stay on the lab record. This file adds the L1 machine, the two reusable sweeps, and the
  clean-reset-formation tail — the shared infrastructure a full branch proof would build on.

## Build (exact)
```
export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build O18   # green; axiom audit prints
/usr/bin/python3 o18_crosscheck.py                             # L1 anchors + both sweeps + clean_gate grid; ALL OK
```

**No machine decided. No label upgraded.**

---

# O3 GENERATION-MAP APPEND (2026-07-09) — o3 becomes the SECOND machine whose machine→arithmetic reduction is machine-checked to the GENERATION MAP (a≡0 class), after o4

Extends `lean/O3.lean` (L1 machine, L2 sweeps, L3 body_step/body_iter/body_descent
— all already FORMALIZED) to **L4: the generation map for the `a ≡ 0 (mod 3)`
residue class**, mirroring `Suffix.lean`'s `generation_odometer`. o3's roles are
SWAPPED vs o4: `a` (single-`1` blocks) is the base-4/3 ODOMETER, `k` (trailing
`110` markers) is the LEDGER (`O3_TEMPLATE_PORT_2026-07-06.md` §1–5).

## Verdict: the `a≡0` GENERATION is FORMALIZED (odometer + ledger derived); a≡1/a≡2 reorgs are the remaining gap

The generation decomposition found (the subtlety flagged in the task — o3's body
SHRINKS `a`): one generation = **descent · reorganization**, NOT o4's grow-then-
suffix. `M(a,k)` is literally o3's body config with the surviving markers as the
never-read right context, so the body DESCENT (`body_descent`, already proven)
transports the defect left, shrinking `a` to 0; then a **fixed 17-step
reorganization** rebuilds `a` via the `(01)→(10)` re-read. Measured exactly
(`o3_gen_proof.py`): the reorg is a constant 17 steps, INDEPENDENT of `M` and `k`
(head span `[p−3,p+3]`, the fabric/markers untouched).

| Target | Lean theorem in `O3.lean` | Status |
|---|---|---|
| **1. milestone `M(a,k)`** | `mk` (marker word), `Mcfg a k p = 0^∞[A]00(10)^a(110)^k` (= Python `build_M`), `Mcfg_as_body` (`M(a,k+1)=BodyCfg a p (0·(110)^k)`, rfl) | **FORMALIZED** |
| **2. reorg episode** | `reorg17` (17 fixed steps, `11·X → (01)^3·X` shift −3, symbolic tail `X` never read; kernel `rfl`), helper `pow01_cons_false` (`(01)^n·0Z = 0·(10)^n Z`) | **FORMALIZED** |
| **3. `o3_gen0` (the prize)** | `M(3M,k+1) → M(4M+3,k)` in EXACTLY `bodyTime M 0 + 17` steps (descent · reorg); `o3_odometer_mod0`: `∀ a k, 3∣a → k≥1 → M(a,k)→M(⌊4a/3⌋+3, k−1)` — the ODOMETER (`c(0)=3`) and LEDGER drain (`Δk=−1`) as theorems | **FORMALIZED** |
| **real-orbit anchor** | `blank_to_M62` (blank → `M(6,2)` at −14, 184 steps, `rfl`), `blank_to_M111` (→ `M(11,1)` at −21, 299 steps; `blank_to_M62 · o3_gen0 2 1`) | **FORMALIZED** |

## Axiom audit (printed at every build, `#print axioms` in-file)
`pow01_cons_false`, `blank_to_M62`: **no axioms.** `reorg17`, `o3_gen0`,
`o3_odometer_mod0`, `blank_to_M111`: **`[propext, Quot.sound]` only.** No `sorry`,
no `native_decide` (kernel `rfl`/`decide` anchors only).

## Numeric sanity (`#eval decide`, kernel-executed, all `true`)
`M(12,3)→M(19,2)` (333 steps), `M(15,4)→M(23,3)` (487), the k=1 floor
`M(6,1)→M(11,0)` (115; successor halts downstream), `blank → M(6,2)` (184),
`blank → M(11,1)` (299 = 184+115). Cross-checked cell-for-cell vs
`o3_gen_proof.py`/`o3_ledger.py` (real orbit joins at `(6,2)`; first two ledger
steps `(6,2)→(11,1)` reproduced).

## What is FORMALIZED vs the remaining gap (honest)
- **Formalized end-to-end (machine → arithmetic):** the full `a≡0` generation
  `M(3M,k+1)→M(4M+3,k)`, deriving the base-4/3 odometer step and the ledger drain
  as Lean theorems. o3 is now the second machine (after o4) reduced to its
  arithmetic generation map by a `lake build`-green, `sorry`-free proof.
- **Remaining gap (on the lab record):** (i) the `a≡1` cascade (`M(a,k)→M(a−1,k+2)`,
  one chunk) and `a≡2` deposit (`M(a,k)→M((4a+4)/3,k+1)`) reorgs — their descents
  do NOT bottom out at `BodyCfg 0` (they stay in residue class 1/2, running the
  cascade/deposit boundary chunks, not the `j≡0` body), so each needs its own fixed
  boundary episode + a phase-align prefix (both measured & pinned in
  `o3_boundary_pinning.py`, not yet ported); (ii) the ledger conjecture (drains never
  push `k` below the fatal floor). Same species as o4's open core.

## Build (exact)
```
export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build O3   # green, audit prints, all #eval true
/Users/aokiyousuke/quantum-ecc/.venv/bin/python ../o3_gen_proof.py   # generation-law grid
```

**No machine decided. No label upgraded.**

---

# O17 L1+GATE APPEND (2026-07-09) — o17's machine + halt gate are FORMALIZED; the FIRST template-FREE cryptid honestly formalized (gate only, NO body lemma)

*New module `lean/O17.lean` (namespace `O17`, zero-dependency/zero-mathlib, verified with
`lake env lean O17.lean` — green, `sorry`-free, axiom-audited; `lakefile.toml` untouched).
o17 = `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt = F reads 0). Cross-checked vs the
zipper-faithful Python simulator (`o17_halt_reduction_2026-07-06.py` semantics; blank-orbit
gate census). Not committed.*

## Verdict: L1 FORMALIZED + the HALT GATE fully machine-checked. NO template (by design).

o17 has **no rigid template** (`O17_HALT_FLAVOR_2026-07-06.md`, `O17_GATE_LAW_2026-07-07.md`:
shape classes grow without bound, level-2 compression collapses nothing, no finite-residue
δ-map; protection is carry-TIMING over an unbounded digit string). So there is **no body lemma
to prove** — attempting one would be dishonest. The achievable, honest result is L1 + a complete
characterization of the halt gate — the one rigid, finite, `[PROVEN]` part of o17's structure.

| Target | Lean theorem(s) in `O17.lean` | Status |
|---|---|---|
| **L1: the machine** | `St`/`Tape`(zipper)/`Cfg`, `step` (`none` ⟺ HALT), `steps`, `steps_add`, `cfgPos`; full-config kernel-`rfl` anchors `sanity5`/`sanity100`/`sanity300` (blank orbit at N=5/100/300 vs Python; N=5 = `0 [A]0 1 1 1 0`, the core seed `A 0 1³`) | **FORMALIZED** |
| **halt gate (iff)** | **`halt_gate`** : `step c = none ⟺ (c.st = .F ∧ c.tape.head = false)` — the literal gate, by case analysis on the 12 table branches | **FORMALIZED** |
| **gate predecessor structure** | **`into_F`** (a step landing in `F` had predecessor `D`-reads-`0`), **`into_D`** (a step landing in `D` had predecessor `A`-reads-`1`) — "F entered only by `D:0→0LF`, D only by `A:1→1LD`" made literal; chaining backward: HALT ⟺ the seam `0 0 [1]_A` occurred 2 steps earlier | **FORMALIZED** |
| **the seam ⟺ halt (forward)** | **`seam_to_gate`** (`0 0 [1]_A` → `F`-reads-`0` in exactly 2 steps, arbitrary tails), **`seam_halts`** (`steps 3 = none`, via `seam_to_gate`+`halt_gate`); **`near_miss_safe`**/`near_miss_not_halt` (`1 0 [1]_A` → `F`-reads-`1`, the 4,712 safe F-entries, does NOT halt) | **FORMALIZED** |
| **gate-event anchors** (`#eval decide`, all `true`) | blank-orbit true-frontier A-gates at steps 5,22,44,101,314,724,2005 (positions −1,−2,−2,−3,−4,−4,−5, each `A`-reads-`0`, left empty), non-halt through 5000, seam/near-miss kernel checks — vs the C/Python gate census | **FORMALIZED** |

## Axiom audit (in-file `#print axioms`, printed at every check)
`steps_add`, `halt_gate`, `into_F`, `into_D`, `seam_to_gate`, `seam_halts`, `near_miss_safe`,
`near_miss_not_halt`: **`[propext, Quot.sound]` (or fewer)** — `halt_gate`/`into_F`/`into_D`/
`near_miss_not_halt` are `[propext]` only; **`sanity5`/`sanity100`/`sanity300` depend on NO axioms.**
No `sorryAx`, no `Classical.choice`, no `native_decide`. No `sorry` anywhere.

## What is FORMALIZED vs out of scope (honest)
- **Formalized:** the machine (L1) and the ENTIRE halt gate — the `step=none ⟺ F:0` iff, the
  unique-predecessor structure (`into_F`/`into_D`), and the two-step seam reduction both ways
  (seam halts; near-miss safe). o17's halt condition is now machine-checked exactly as the
  lab-note `[PROVEN]` reduction (`O17_HALT_FLAVOR` §1a) states it.
- **Not attempted (by design):** any template/body lemma — o17 provably has none (unbounded
  shape classes). The sparse-gate carry-timing protection conjecture (`O17_GATE_LAW` §4) stays
  `[OPEN]`; the gate anchors prove nothing about halting, only cross-check the finite orbit.

## Build (exact)
```
export PATH="$HOME/.elan/bin:$PATH"; cd lean
lake env lean O17.lean     # green; #eval sanity all true; axiom audit prints (lakefile.toml untouched)
```

---

# MIRROR CRITICALITY-COMPLETION APPEND (2026-07-09) — the cumulative-ledger criticality verdict is FORMALIZED for ALL FIVE machines (o4 is the unique freely-subcritical rung)

*Extends `lean/Mirror.lean` §6 (the criticality comparison). Completes the integer criticality
verdict across the whole CUMULATIVE-ledger family (`PAPER_MIRROR_LADDER.md` §4: Antihydra, o2,
o4, o3, Space Needle), with the resetting/inapplicable cases documented. `lake build Mirror`
green, axiom audit clean. Everything integer/ℤ; real slopes in comments. Not committed.*

## Verdict: o4 is the SOLE instantiation of `criticality_excluded` in the ledger family.

The honest integer certificate instantiates `criticality_excluded` at `β = ⌊β*⌋` (the largest
integer that is a valid LOWER bound on the machine's real budget growth `β*`). Worked through
the five cumulative machines (`Mirror.lean` §6a, all integer facts by `decide`):

| machine | ×p/q | real budget slope β* | ⌊β*⌋ integer test `p+1 ≤ q^(⌊β*⌋+1)` | verdict |
|---|---|---|---|---|
| **o4** | ×4/3 | β* = 3 | `5 ≤ 3⁴ = 81` **TRUE** (`o4_has_certificate`) | **SUBCRITICAL** (`o4_criticality_excluded`), ρ/β≈0.087 |
| **Antihydra** | ×3/2 | β* = 1/2 | `4 ≤ 2¹ = 2` **FALSE** (`antihydra_o2_no_certificate`) | **CRITICAL** boundary, ρ/β=1.17 |
| **o2** (ceiling) | ×3/2 | β* = 1/2 | same rung as Antihydra — same FALSE | **CRITICAL** (shares Antihydra's (p,q) AND slope) |
| **o3** | ×4/3 | β* ≈ 0.248 (ledger DRAINS, Δk=−1) | `5 ≤ 3¹ = 3` **FALSE** (`o3_no_certificate`) | **NOT subcritical**; criterion applies differently |
| **Space Needle** | ×5/2 | — (odd branch: no fixed point) | no β — no scalar ledger | **INAPPLICABLE** (replaced by summability) |

New Lean facts (all `decide`, **axiom-free**): `o4_has_certificate`, `antihydra_o2_no_certificate`,
`o3_no_certificate`, `o3_beta1_overstated` (o3's `β=1` test `5 ≤ 3²=9` PASSES but overstates the
real slope `0.248`, so it is NOT a valid instantiation — recorded to make the "different criterion"
explicit). Space Needle documented as an `example` (no β exists).

## The two flagged subtleties, resolved
- **o2 = Antihydra's boundary rung** (task 1): o2 shares `(p,q)=(3,2)` and the cumulative slope
  `β*=1/2`; `ρ/β = log₂(3/2)/(1/2) = 1.1699 > 1`. `β*` is non-integer, so `criticality_excluded`
  is NOT instantiable; the `β=⌊β*⌋=0` floor test already FAILS (4 > 2). Mirrors the existing
  Antihydra note attached to `o4_criticality_excluded`, now with its own named theorem.
- **o3's ledger DRAINS** (task 3): o3 is ×4/3 like o4 (same `ρ≈0.262`) but roles are SWAPPED —
  the ledger `k` drains `Δk=−1` per generation (budget SHRINKS toward the floor), vs o4's `a`
  growing `+3` away from it. So `β*≈0.248 ≈ ρ` (`ρ/β≈1.06>1`), the `⌊β*⌋=0` test FAILS, and o3
  admits NO honest integer subcriticality certificate. o3's safety is the ledger-drain-vs-floor
  question (the OPEN o3 ledger conjecture, `O3.lean` §5), not a slope comparison — exactly why
  **o4 is the only freely-subcritical instance** (task 2, confirmed).

## Axiom audit (in-file `#print axioms`)
All four new theorems: **depend on NO axioms** (`decide` on decidable `ℕ` inequalities). The
existing §6 crown theorems unchanged (`[propext, Quot.sound]` only). `lake build Mirror` green.

## Build (exact)
```
export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build Mirror   # green, audit prints
```

**No machine decided. No label upgraded.**

---

# O18.lean — L2 extended: the third uniform crawl `sweepEB` (2026-07-09)

**Goal (this session):** push o18's Lean formalization from L3 (one branch tail) toward the
single-defect transition branches (POP `m≡2`, LAND `m≡0`, PUSH2 `m≡1`).

## What was formalized (compiles, sorry-free, axiom-audited)
- **`sweepEB`** — NEW arbitrary-length uniform crossing, the odometer's **leftward
  filler-transport crawl**: period-4 cycle `E1→0LB · B0→1LC · C0→1LA · A1→0RE`. `4k` steps take
  `[E on 1] 0 0 (10)^k L` to `[E on 1] 0 0 L`, transporting `(10)^k` UNCHANGED to the right,
  shifting `−2k`. Proven for every `k` by one-tile (`sweepEB_tile`, `rfl`) + length induction,
  exactly like `sweepAB`/`sweepDC`. This is the third (and last) uniform in-cell crossing of o18
  and the crawl the head makes returning over the counter inside every defect turnaround.
- Helper `pow10_snoc : pow10 k ++ [true,false] = pow10 (k+1)` (**axiom-free**) folds the
  transported filler in the induction.
- Grid `#eval` cross-check at `k=5` (`decide ⇒ true`).

## Branches NOT closed — the exact obstacle (pinned by trace this session)
The task hypothesis "POP = one sweep + a fixed turnaround episode" is **REFUTED**. Trace of
`D(m,t,e) → D(m′,t′,e′)` (e.g. `D(5,1,1)→D(18,0,1)` in 101 steps, `D(8,1,1)→D(26,0,1)` in 186)
shows every branch routes through a **growing-amplitude odometer bounce**: alternating `sweepAB`
rightward passes and `sweepEB` leftward passes whose lengths CHANGE each bounce, glued by
turnaround pivots that are **counter-dependent** (the reflect pivot branches `A→B→A→E→C→A→…` on
surrounding counter digits — not a uniform frame). Step count is quadratic `≈(4/3)m²` = `O(m)`
bounces of `O(m)` length; the aggregate `m′−1=(8/3)(m−1)` push law is the o4-species odometer
CLOSURE, which stays OPEN. So no full transition branch reduces to sweeps + a fixed episode.
`clean_gate`/`clean_reset` remain the shared clean-reset-formation TAIL of every LAND/POP landing.
PUSH2's `8/3` growth needs the same odometer aggregate (not blocked by the missing `ring`; blocked
by the open closure). No `DRAFTED` block was needed — nothing partial is fit to isolate.

## Axiom audit (in-file `#print axioms`, printed at build)
`sweepEB`, `sweepEB_tile`, `sweepAB(_tile)`, `sweepDC(_tile)`, `gate_episode`, `clean_gate`,
`clean_reset`, `steps_add`: **`[propext, Quot.sound]`** only. `pow10_snoc`, `sanity100`,
`sanity300`: **NO axioms**. No `native_decide`, no `sorry`, no `sorryAx`.

## Build (exact)
```
export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build O18   # green, audit + #evals print
```

**No machine decided. No label upgraded.**

---

# o2 machine formalization — the SECOND Antihydra (ceiling ×3/2), phase-1 generation branch (2026-07-09)

*Third fully-formalized BB(6) machine after o4 (`Template.lean`) and o3 (`O3.lean`). File
`lean/O2.lean`, namespace `O2`, zero-mathlib, core Lean only. Spec + certified decomposition from
`o2_link0_certify.py` / `O2_LINK0_CERTIFIED_2026-07-08.md`.*

Verified green by `~/.elan/bin/lake env lean lean/O2.lean` (the identical per-file kernel
elaboration `lake build` runs): **no errors/warnings, no `sorry`, no `native_decide`**; `lake build
O2` pending the main-loop `lean_lib O2` registration in `lakefile.toml` (not edited per task
constraint). Machine: `o2 = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA`, halt gate F,0 (F entered
only by D:0→0RF).

**Axiom audit (`#print axioms`, every theorem): `[propext, Quot.sound]` only** (sanity/`cons_pow01`
depend on no axioms) — no `sorryAx`, no `Classical.choice`.

| Layer | Lean theorem(s) in `O2.lean` | Status |
|---|---|---|
| **L1 machine** | `step`/`steps`/`steps_add`; anchors `sanity44` (blank→D(2,1)), `sanity100`, `sanity200` (kernel `rfl` vs Python) | **FORMALIZED** |
| **L2 both sweeps** | `sweepBE` (B1E1 leftward invert `1^{2n}→(01)^n`, head −2n) and `sweepCA` (C0A1 rightward invert `(01)^n→1^{2n}`, head +2n), arbitrary length by 2-transition tile + induction; helper `cons_pow01` (`1·(01)^n = (10)^n·1`) | **FORMALIZED** |
| **L3 generation branch (phase 1)** | milestone `Mcfg a b` (=D(a,b)); `prefix10`/`prefix_mil` (fixed 10-step D(a+1,b)→cut 1); **`unit`** (canonical 16-item unit V(t,m+2)→V(t+1,m) in exactly 12t+32=12k+20 steps, suffix untouched — composition `ep_pre·sweepBE(3t+3)·ep_bnd·sweepCA(3t+4)·ep_tail`); `unit_iter` (J-fold drain); **`phase1`** (`prefix·unit^J`: D(a+1,b)→V(J) with m=r, a=2J+r); anchors `blank_to_D21`, `blank_to_cut1` | **FORMALIZED** |

`#eval` sanity (kernel-executed each build, all `true`): `sweepBE` n=7, `sweepCA` n=5; `unit` at
t=1,m=7 and t=2 with a symbolic W-suffix; `phase1` on D(9,3) (J=4). All cross-checked against
`o2_link0_certify.py`'s standalone-unit / cut grids.

**Honest scope / remaining gap.** Only PHASE 1 of a generation is Lean-checked (prefix + the unit
loop, halt-free). NOT formalized (stay on the lab record `O2_LINK0_CERTIFIED` §2–5): the 7 exit
templates (SUF_EVEN/ODD/MID/ESC/TERMINAL) that convert the last cut → the next milestone, the
phase-2 drain, and hence the full milestone automaton `D(a,b)→D(a',b')`, the (y,b)=`⌈3y/2⌉`
conjugacy, and the mod-4 halt/escape hatch. The ceiling-(K) ledger conjecture stays `[OPEN]`.
**No machine decided. No label upgraded.**

---

# O3 MARKER-SWEEP APPEND (2026-07-09) — the a≡1/a≡2 boundary chunks: BOTH period-3 ledger sweeps + the k-parametric marker ROUND-TRIP are FORMALIZED; full generations kernel-DECIDED

Extends `lean/O3.lean` (L1 machine, L2 crawls, L3 body, L4 a≡0 generation — all
already FORMALIZED) toward the two OPEN residue classes. Concrete finding (traced
via `o3_gen_proof.py`): the a≡1 CASCADE and a≡2 DEPOSIT generations do **not** bottom
out at `BodyCfg 0` (they never leave residue class 1/2). Their boundary chunks are a
genuine **2-parameter** composition — the odometer crawls `crawlR^M`/`crawlL^M`
(scaling with `a=3M+r`) sandwiching a NEW **period-3 sweep over the trailing ledger
word `(110)^k`**, plus fixed episodes. Full decompositions found:
```
a≡1 cascade  M(3M+1,k) → M(3M, k+2)  (one chunk, 30M+32 steps, net −2):
   crawlR^M · Ep_meet(5) · markR^k · turn(4) · markL^(k+1) · Ep_mid · crawlL^M · Ep_final
a≡2 deposit  M(3M+2,k) → M(4M+4, k+1)  (bodyTime M 0 + 30M + 62 steps):
   crawlR^M · [markR/markL marker excursion + episodes] · crawlL^M · body_descent M · reorg17
```

## Verdict: the two MARKER sweeps + the k-parametric round-trip are FORMALIZED; the M-scaling odometer glue is the remaining gap

| Target | Lean theorem in `O3.lean` (§3.4–3.6) | Status |
|---|---|---|
| **markR** (rightward ledger sweep) | `tri3`/`dtri3`, `markR_tile` (3-step `A0·B1·E1`, `011`→`110`, +3), `markR` (ARBITRARY length `j`: crosses `(110)^j`, deposits `(011)^j`, +3j, tail-independent; tile+induction) | **FORMALIZED** |
| **markL** (leftward return sweep) | `etri3`, `markL_tile` (3-step `D1·C0·A1`, consumes `011`, emits `101`, −3), `markL` (ARBITRARY length: consumes `(011)^j`, emits `(101)^j`, −3j) | **FORMALIZED** |
| **marker round-trip** (the k-scaling core) | `dtri3_add`, `ep_turn` (fixed 4-step reflect `A0·B0·C0·A1`), **`marker_excursion`**: `markR^K · turn · markL^(K+1)`, PARAMETRIC in ledger `K`, exactly `6K+7` steps, halt-free | **FORMALIZED** |
| **full a≡1/a≡2 generations** | kernel-DECIDED at concrete params (§5d): `M(13,3)→M(12,5)`@152, `M(10,3)→M(9,5)`@122; `M(14,3)→M(20,4)`@497, `M(11,3)→M(16,4)`@343, `M(17,3)→M(24,4)`@681 — all `some` (halt-free) + exact landing milestone | **DECIDED (concrete), not parametric** |

## Axiom audit (`#print axioms`, in-file, printed each build)
`dtri3_snoc`, `etri3_snoc`: **no axioms.** `markR_tile`/`markR`/`markL_tile`/`markL`/
`dtri3_add`/`ep_turn`/`marker_excursion`: **`[propext, Quot.sound]` only.** No `sorry`,
no `native_decide`, no `Classical.choice`.

## Numeric sanity (`#eval decide`, kernel-executed, all `true`)
markR `j=4,7`; markL `j=5`; marker round-trip `K=4` (`6·4+7=31` steps); and the five
full-generation anchors above (§5d), all cross-checked cell-for-cell vs `o3_gen_proof.py`.

## What is FORMALIZED vs the remaining gap (honest)
- **Formalized:** both period-3 ledger sweeps (`markR`/`markL`, arbitrary length) and
  their k-parametric round-trip `marker_excursion` — the ledger-scaling heart shared by
  BOTH open boundary chunks, composing the two sweeps through the fixed `ep_turn`.
- **Kernel-decided (concrete, not generic):** the full a≡1 cascade and a≡2 deposit
  generations at 5 grid points — halt-free, exact next-milestone landing.
- **Remaining gap for PARAMETRIC `o3_gen1`/`o3_gen2`/`o3_generation`:** the M-scaling
  odometer episodes `Ep_meet`/`Ep_mid`/`Ep_final` that sandwich `crawlR^M`/`crawlL^M`
  around `marker_excursion` (and, for a≡2, chain into the already-proven `body_descent`
  + `reorg17`). These are body_step-style fixed rfl episodes with symbolic tails, fully
  traced and landmark-pinned (`o3_boundary_pinning.py`) but not yet assembled into the
  parametric theorem — a multi-episode glue like `body_step`, left for the next pass.
- The ledger conjecture (drains never push `k` below the fatal floor) stays `[OPEN]`.

## Build (exact)
```
export PATH="$HOME/.elan/bin:$PATH"; cd lean; lake build O3   # green, audit prints, all #eval true
```

**No machine decided. No label upgraded.**

## Completion.lean (2026-07-10) — the conditional completion theorem [FORMALIZED]
`lake build Completion` green; part of the full 19-job build. `theorem BB6_eq_championSteps
(h : AllHoldoutsNonHalt) : BB6 = championSteps` — the complete BB(6) proof as one conditional
theorem, proven by `Nat.le_antisymm` from the champion lower bound + the enumeration upper
bound. AXIOM AUDIT (`#print axioms BB6_eq_championSteps`): NO sorryAx; depends ONLY on the
17 named protection conjectures (`o4_nonhalt`…`o17_nonhalt`), `holdouts1087_nonhalt`, the two
enumeration bridges (`champion_lower`, `enumeration_upper`), and the interface `BB6`/
`championSteps` — the hard content is isolated into exactly these explicit, documented axioms
(not even propext/Quot.sound are needed). This is the machine-checked FRAME: the logical
structure of the complete proof is verified; the remaining difficulty is localized to 17
famous-open-problem conjectures + the community-scale 1087 sweep. Resolving one named axiom
upgrades it to a theorem and decides that machine.

---

# COMPLETION o4-LITERALIZATION APPEND (2026-07-10) — `o4_nonhalt` is now the REAL machine statement + a PROVEN reduction; only the arithmetic ledger stays axiomatic

*Tightens `lean/Completion.lean`. Previously `axiom o4_nonhalt : Prop` was an opaque placeholder
whose equivalence to the arithmetic conjecture was only DOCUMENTED. Now Completion `import Suffix`s
the actual o4 formalization (`Template`/`Suffix`) and makes o4 literal. Same zero-dependency project;
`lake build` green (19 jobs, Completion ≈ 2.5 s). Not committed.*

## What o4's Lean layer proves about non-halting (assessment)
- `Template.body_nonhalt` — the STANDALONE bouncer family `B(k)` never halts (unconditional).
  Explicitly decides nothing about o4 from blank: blank-left context only.
- `Suffix.generation_odometer` — the real machine→arithmetic generation map `M(G,a) →
  M(⌊4G/3⌋+c(G%3), ledgerNext G a)`, exact step counts, for every `G ≥ 34`, `a ≥ 1`.
- `Template.real_milestone` — blank tape reaches `M(43,18)` at step 1548 (kernel `rfl`, axiom-free).
- The FULL "blank orbit non-halts ⟺ frequency/ledger conjecture" is NOT a single pre-existing
  theorem; the pieces above are chainable into the reduction DIRECTION (arithmetic ⇒ non-halt).

## What is now LITERAL / PROVEN in `Completion.lean`
| Object | Definition / statement | Status |
|---|---|---|
| `o4_nonhalt` | `def := ∀ n, Template.steps n Template.init ≠ none` — the real o4 TM (`Template.step`) from blank never hits its halt transition | **LITERAL def** (was opaque `axiom … : Prop`) |
| `Gseq`/`aseq` | the arithmetic milestone orbit, seeded `M(43,18)`, advanced by `Template.cOdo`/`ledgerNext` | def |
| `Gseq_ge`, `mu_strict`, `pow10_len`, `Mcfg_right_len`, `prefix_ne_none` | odometer stays `≥34`; measure `G+2a` strictly grows/gen; tape-length; halt-free prefixes | **PROVEN** |
| `orbit_reaches` | ledger `≥1` ⇒ blank orbit reaches `M(Gseq n, aseq n)` at a step `N ≥ n` (base = `real_milestone`; step = `generation_odometer`; `>0` steps/gen via `mu_strict`) | **PROVEN** `[propext, Quot.sound]` |
| **`o4_reduction`** | **`o4_ledger_conjecture → o4_nonhalt`** — the machine→arithmetic reduction direction, now a Lean theorem (was documented prose) | **PROVEN** `[propext, Quot.sound]` |
| `o4_ledger_conjecture` | `def := ∀ n, 1 ≤ aseq n` — the genuinely-open arithmetic content (base-4/3 (K)-normality rung) | def |
| `o4_ledger` | the ONLY remaining o4 axiom (the arithmetic conjecture) | **axiom** |
| `o4_nonhalt_of_ledger` | `: o4_nonhalt := o4_reduction o4_ledger` | **PROVEN** (from `o4_ledger`) |

## New axiom audit (`#print axioms`, printed at build)
- `Completion.BB6_eq_championSteps` — **`o4_nonhalt` is GONE from the list.** Now:
  `[BB6, championSteps, champion_lower, enumeration_upper, holdouts1087_nonhalt,
  antihydra/o2/o3/o5/o7/o8/o10/o11/o12/o13/o14/o15/o16/o17/o18/spaceNeedle_nonhalt]`
  — the 16 still-opaque machines + holdouts + 2 enumeration bridges + interface. **No `sorryAx`.**
- `Completion.o4_reduction`, `Completion.orbit_reaches` — **`[propext, Quot.sound]` only** (no `sorryAx`,
  no `o4_ledger`): the reduction is unconditionally proven.
- `Completion.o4_nonhalt_of_ledger` — `[propext, o4_ledger, Quot.sound]`: o4's non-halting now rests
  on ONE named arithmetic axiom via a proven reduction, not an opaque `Prop`.

## Honest scope — what remains genuinely axiomatic
- o4: only `o4_ledger` (the a-ledger / base-4/3 return-frequency conjecture). The generation
  dynamics, odometer, ledger update, and the non-halt reduction are all Lean theorems.
- The other 16 named machines (`o3_nonhalt … o17_nonhalt`, `spaceNeedle_nonhalt`) stay opaque
  `Prop` axioms — their machines are not literalized in Completion (o3/O18/O2/O17 have partial Lean
  layers elsewhere, not wired in here). The 1087-holdout residual and the two enumeration bridges
  stay axioms (community-scale engineering).
- The full ⟺ (halting ⇒ ledger fails, the reverse direction) is NOT formalized; only the
  protective direction (ledger ⇒ non-halt) is proven, which is the one the completion frame needs.

**No machine decided. No label upgraded.**

---

## Append 2026-07-10 — minimal distinct-conjecture-schema collapse in `Completion.lean`

The 17 named protection conjuncts were 16 opaque `axiom *_nonhalt : Prop` (+ literal o4). They are
now regrouped into **5 conjecture SCHEMAS**, each `*_nonhalt` *defined* as its schema at a
per-machine seed (`rfl`-checked). Full project still green (19 jobs), no new `sorry`/`sorryAx`.

| schema | Lean form | seed-instances |
|---|---|---|
| `NormalityPQ 3 2` (`Normality32`) base-3/2 normality, place ℤ₂ | `axiom NormalityPQ : Nat→Nat→Int→Prop` | antihydra, o10, o2, o11, o13, o14, o16, o12, o8 (9) |
| `NormalityPQ 4 3` (`Normality43`) base-4/3, place ℤ₃ | same symbol | o4 (Lean-literal), o3, o5 (3) |
| `NormalityPQ 8 3` (`Normality83`) base-8/3, place ℤ₃ | same symbol | o15, o18 (2) |
| `TwoPowerAvoidance` (generalized-Collatz 2^k-avoidance) | `def orbit ↦ ∀ n k, orbit n ≠ 2^k` (LITERAL) | o7 (`o7orbit`), Space Needle (`snOrbit`) (2) |
| o17 gate-timing (own form) | `axiom o17_nonhalt : Prop` | o17 (1) |

**Count:** 5 named schemas; the 3 normality bands are one meta-schema `NormalityPQ` at 3
genuinely-distinct p-adic places → **3 meta-schemas** (`NormalityPQ`, `TwoPowerAvoidance`, o17)
covering **17 seed-instances**. Distinctness of instances is preserved (per-seed open content
transfers no bound — reload doc §3.3); only the FORM is unified.

Numerically re-verified 2026-07-10 (`scratchpad/reload_unified.py` basis): gap-1 ×3/2 machines
identical to `W↦⌊3W/2⌋` (20000/20000 exact); o2 negation-conjugate (4000/4000); o13 gap-7
genuinely different map (2020/4000 mismatch) — hence o13 is a distinct instance, not the canonical
engine; ×3/2 reads v₂ while ×4/3, ×8/3 read v₃ (different places, no ℤ₂→ℤ₃ map).

### New axiom audit (`Completion.BB6_eq_championSteps`)
`[BB6, NormalityPQ, championSteps, champion_lower, enumeration_upper, holdouts1087_nonhalt,
o17_nonhalt, o7orbit, seed, snOrbit]` — the **16 opaque `*_nonhalt` axioms are gone**; the entire
13-machine (K)-band now contributes the SINGLE symbol `NormalityPQ` (applied through `seed`), the
thin-set band `o7orbit`/`snOrbit` (via the `TwoPowerAvoidance` def), o17 its own form. No `sorryAx`.
`antihydra_nonhalt` audits as `[NormalityPQ, seed]`; `o7_nonhalt` as `[o7orbit]`.

### Honest scope
The definitional identities `oX_nonhalt := schema (seed X)` ENCODE the machine⟺arithmetic
reductions ([PROVEN-in-lit]/[PROVEN on grid]/[OBSERVED]; only o4 is Lean end-to-end and kept
literal). The enumeration bridge folds those reductions into its hypothesis. `NormalityPQ` stays
uninterpreted (as the 16 Props were); its docstring pins its meaning. o13 shares the `Normality32`
FORM but is documented as the gap-7 variant, not claimed identical to the gap-1 engine.

**No machine decided. No label upgraded.**

---

# X2 APPEND (2026-07-11) — the integer-×2 odometer machine + halt gate + the EVEN comb-repack sweep are FORMALIZED (and the "A1D0 eraser" is corrected)

*New module `lean/X2.lean` (namespace `X2`, same zero-dependency zero-mathlib project;
`lake build X2` ≈ 0.4 s). Target from the task: formalize the ERASER-EVEN channel of
`x2 = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`. STRICT labels as above. Not committed.*

## Verdict: L1 machine + halt gate + the genuine EVEN sweep FORMALIZED; the literal `0^{2j}` eraser is corrected as a source-doc conflation.

| Target | Lean theorem(s) in `X2.lean` | Status |
|---|---|---|
| **L1: the machine** | `St`/`Tape`(zipper)/`Cfg`, `step` (12 transitions read off the TNF spec), `steps`, `steps_add`; kernel `rfl` anchors `sanity50`/`sanity100` (full zipper config vs the Python simulator, exact incl. trailing blanks) | **FORMALIZED** |
| **L2: the halt gate** | `halt_gate` : `step c = none ↔ (c.st = B ∧ head = true)` — the ONLY halt is `B:1` (the `---` field), proved by cases on `(state, read)` | **FORMALIZED** |
| **L3: the EVEN sweep (the target)** | `sweepEF_tile` (one 2-step tile `E:0→1RF · F:1→1RE`) + **`sweepEF`** (ARBITRARY `m`: comb `(01)^m → 1^{2m}` in `2m` steps, `ones(2m)` deposited, `+2m`, by tile+length induction — the `Template.sweepBF`/`O3.crawlR` pattern); **`sweepEF_even`** pins the produced block length `= 2*m` (EVEN, all `m`) | **FORMALIZED** |
| **L3′: leftward `D`-sweep** | `dSweepTurn` (ARBITRARY block length: `D:1→1LD` crosses `1^{n+1}` left, `D:0→0RE` turns into `E` at the left edge, `n+2` steps, block preserved) | **FORMALIZED** |

## The correction (the load-bearing finding — SOUND, no false proof avoided)
The lab notes (`X2_ARITHMETIC_PROOF`, `X2_TEMPLATE_PROOF`, `x2a_eraser.py`) describe an "`A1D0`
eraser" 2-cycle `A:1→0LD · D:0→0LA` giving `(01)^j → 0^{2j}`. **That 2-cycle is o4's**
(`Suffix.lean`'s `sweepAD`, machine `1RB0LD_...`), **NOT x2's**: here `A:1→0RE` and `D:0→0RE`
both move RIGHT, and a brute-force search over all entry states finds x2 has NO clean cell-zeroing
uniform-crossing sweep. The even-gap stream `[2,4,4,6,8,…]` `x2a_eraser.py` reports is an EMERGENT
parity of the full compound sweep on a boundary-contaminated isolated comb (the script itself flags
"the boundary differs, so the length is not the in-context `2j`") — not a clean single-cycle lemma.
x2's genuine, cleanly-formalizable EVEN channel is the DUAL: the comb-REPACK `(01)^m → 1^{2m}` (the
base-2 doubling engine, `X2_TEMPLATE §1/§3.1`), whose output length `2m` is provably even for all
`m`. `sweepEF`/`sweepEF_even` formalize exactly that.

## Axiom audit (printed at every build via in-file `#print axioms`)
`steps_add`, `sweepEF`, `sweepEF_even`, `dSweepTurn`: **`[propext, Quot.sound]` only**; `halt_gate`
**`[propext]`**; `sanity100` **NO axioms**. No `sorryAx`, no `Classical.choice`, no `native_decide`,
no `sorry`. Four `#eval decide` sanity checks (repack `(01)^3→1^6`; D-sweep `1^4`→E; halt gate at
`B:1` and non-halt at `B:0`) all print `true`. `lake build` green (all 21 jobs).

## Honest scope
Local channel only. This is NOT the global non-halt (the open core = "the `E`-scanner never meets a
length-3 gap"), which is counter-dependent (`X2_TEMPLATE §3.2`) and not formalized. The literal
`0^{2j}` eraser does not exist in this transition table; the even-block repack is the sound analogue.

**No machine decided. No label upgraded.**

---

## Appendix (2026-07-12): x2 doubling-phase — G1 cascade FOLD + G3 arithmetic core formalized

Extended `lean/X2.lean` (full project green, 21 jobs, no `sorry`/`native_decide`; every new
theorem audits to `[propext, Quot.sound]`), targeting the `X2_COMPOSITION_2026-07-11.md` gaps.

NEW, FORMALIZED:
- `sepCross_tile` (15-step kernel `rfl`): the cascade separator crossing `[D] 0^3 1^3 0^2 1^2·X
  → (deposit) [D] 0^3·X`, head +7, opaque `X` untouched — derived from + cross-checked against
  the verified machine.
- `blockStep m s` (`chewFold m · sepCross_tile`, `6m+15` steps): the per-block cascade step
  `[D] 0^3 1^{2m+3} 0^2 1^{2s+5} 0^2 T → (comb) [D] 0^3 1^{2s+3} 0^2 T` — this is
  `x2co_compose.py`'s certified `L1`, now a Lean composite.
- **`cascadeFold` (G1)**: `blockStep` iterated over an ARBITRARY, non-uniform `List Nat` of
  blocks by List induction, halt-free (`some`) for every list. This closes the exact
  representational gap G1 — the fold the affine `x2cc` executor (fixed-length run-lists,
  distinct block sizes 61,29,13,5,1) provably could not express. In Lean it is a routine
  `List` recursion whose inductive step (`blockStep`) is a kernel composite.
- **`doubling_id` (G3 arithmetic core)**: `2·(2^K−3)+3 = 2^{K+1}−3` (all `K≥2`), the
  exponential-`2^K` block-doubling identity the affine executor could not represent.

STILL OPEN (the exact remaining Lean gaps, NOT closed): (1) the low-phase M1(g)→M6(g) ∀g
sweep-induction (Python-`x2cc_prove` PROVEN, not ported — ~1k-line analogue of Template+Suffix);
(2) G2 entry/big-block-marked-sweep/repack as parametric tiles (machine-checked g=2..6 only);
(3) the **G3 register-rebuild WIRING** — `cascadeFold` is not yet instantiated at the milestone
cascade (`2^j−3` blocks) and the accumulated comb-total is not yet equated (via `doubling_id`)
to the rebuilt block, the deepest step; (4) the milestone `Cfg` M(g), the transport
M1(g)→M1(g+1) ∀g, and the composed `x2_nonhalt`.

**Verdict: NO decision.** G1 (the fold engine) and G3's arithmetic core are formalized with
clean axioms; the low-phase composition, G2, the G3 wiring, and top-level `x2_nonhalt` remain.
No machine decided. No label upgraded.

---

## Append 2026-07-12 — G3 WIRING (structural part) + the honest obstruction

Extended `lean/X2.lean` §5e (single-agent; full project green, axioms `[propext, Quot.sound]`
only, no `sorry`, no `native_decide`):

- **`cascadeBlocks K : List Nat`** — the milestone `M(K)` cascade as a CONCRETE fold block list
  (fold `a`-convention: waiting block stored `1^{2a+5}`). Milestone blocks `2^j−3` (j = K−1…3)
  map to `a = 2^{j−1}−4`. Kernel `#eval` cross-checked vs the Python `m1_spec` for K = 10..14
  (g = 2..6): `(cascadeBlocks K).map (2a+5)` reproduces `509,253,…,5` etc. exactly.
- **`cascade_traversal K`** — `cascadeFold` INSTANTIATED at `cascadeBlocks K`, starting on the
  leading `1^{2·(2^{K−1}−3)+3} = 1^{2^K−3}` big block; halt-free (`some`), lands on
  `1^{2·lastBlock+3}`. Immediate corollary of G1.
- **`cascDesc_sum` / `cascadeBlocks_sum`** — the accumulator SUM lemma by List/Nat induction:
  `Σ cascadeBlocks K = 2^{K−1} − 4K + 8` (geometric telescoping, additive form to dodge `Nat`
  truncation; uses `four_le_two_pow` + `Nat.pow_succ`). The "Σ blocks → closed form" step.
- **`doubling_transport`** — composes `H_entry` (low-phase/entry, NAMED hyp) + `cascade_traversal`
  (proven) + `H_repack` (G2 repack, NAMED hyp) into a HALT-FREE transport to `M1next`, via
  `steps_add`. The structural G3 result standing on the two still-open pieces.

**HONEST OBSTRUCTION (the accumulator-to-`2^K` identity does NOT close as posed):**
(a) the terminal `1^1` (`2^2−3`, j=2) block is not fold-representable (`2a+5=1 ⟹ a=−2`) — it
sits in the opaque tail `T`; the cascade cut is at j=3. (b) `cascadeFold` lands on
`1^{2·lastBlock+3}`, NOT `1^{2·acc+3}` — the comb→big-block repack is a separate G2 episode,
absent here. (c) `Σ ≈ 2^{K−1}` ⟹ `2·Σ+3 ≠ 2^{K+1}−3` (`#eval`: 963 ≠ 2045 at K=10). **`doubling_id`
is the BIG-BLOCK marked-sweep episode's law, not the cascade fold's** — the framing
"cascadeFold accumulator = 2^K via `doubling_id`" is REFUTED. The register-rebuild
`2·(comb)+corrections = 2^{K+1}−3` needs the G2 big-block sweep, not the fold.

**Verdict: G3 wiring STRUCTURAL part closed (concrete instantiation + Σ closed form + composed
transport with named hypotheses); the G3 accumulator IDENTITY does not close (obstruction (a)-(c),
the doubling lives in G2). No machine decided. No label upgraded.**

---

## Append 2026-07-12 (b) — G2 the BIG-BLOCK `(10)^10`-MARKED SWEEP, lifted to all lengths

Extended `lean/X2.lean` §5f (single-agent; full project green — 21 jobs; all new lemmas
`[propext, Quot.sound]` only, no `sorry`, no `native_decide`; 4 kernel `#eval` = `true`).

**Episode EXTRACTED cell-for-cell from the raw x2 machine** (a raw simulator matching Lean
`step`, run on the M6 tape reconstructed from `m1_spec`; NOT from prose). In the doubling
phase the head enters state `D` on the first `0` of a fixed marker `0^3 (10)^10` left of the
big block `1^{2v+1}` and runs a UNIFORM `4·10+6 = 46`-step R/L cycle: sweep RIGHT across the
whole `(10)^10` marker (24 R), edit the block's first two `1`s, sweep back LEFT (22 L, net +2),
depositing one `1 0` comb pair, shrinking the block by 2, marker + tail preserved. Marker
length `10` is `K`-INDEPENDENT (the constant `1 0^10` even-parity tail `T_g`; verified g=2..8).

- **`markedChew_tile`** (46-step kernel `rfl`): `[D] 0^3 (10)^10 1^{b+2} … → 1 0 [D] 0^3 (10)^10 1^b …`.
- **`markedChew` ∀v** (tile + length induction, the `chewFold`/`crawlR` pattern): grinds the big
  block `1^{2v+1}` down to `1^1` in `46v` steps, depositing `pow10 v`, marker preserved,
  head +2v, HALT-FREE. **This is the G2 marked sweep as an arbitrary-length parametric lemma.**
- **`markedTurn`** (29-step `rfl`): repacks the exhausted `(10)^10 1^1` into `1^{21} = 1^{2·10+1}`
  and crosses the `0^2` separator into the next block `1^{n+2}`→`1^n`, head +25.
- **`markedBlock v s` ∀v,s** (compose): the FULL big-block episode `46v+29` steps, HALT-FREE.
- **`marked_not_doubling`**: `2·(2^{K−1}−2) = 2^K−4 ≠ 2^{K+1}−3` — the exact off-by.

**HONEST VERDICT — the ×2 doubling is NOT in this episode (framing scrutinised).** The marked
sweep is the block→COMB CHEW, not the ×2. With `2v+1 = B_K = 2^K−3` (so `v = 2^{K−1}−2`) the
deposited comb `pow10 v` repacks (via `sweepEF`) to `1^{2v} = 1^{2^K−4}` — plus a fixed `1^{21}`
residue and a next-block trim; it does NOT emit the doubled solid block `1^{2^{K+1}−3}`. So
`doubling_id` (`2·(2^K−3)+3 = 2^{K+1}−3`) is the milestone ARITHMETIC law, realised only by the
FULL compound (this chew → comb repack → register/cascade rebuild carrying the `−4K+8`
correction), NOT by the marked sweep alone (`marked_not_doubling` records the `2^K+1` gap).

**`H_repack` of `doubling_transport` is NOT discharged** and I did not force it: (i) `H_repack`
is literally the DISTINCT post-cascade repack episode (episodes 5–6), whereas the big-block
marked sweep is episode 3 (before the cascade fold); (ii) even under the task's "big-block
sweep = the doubling episode" framing, the sweep performs only the chew half of the ×2. What
IS lifted to all lengths here: the marked sweep's SAFETY (halt-free ∀v) and STRUCTURAL
transport — the G2 engine — as clean parametric Lean lemmas.

**Verdict: G2 big-block marked sweep formalized as an arbitrary-length halt-free lemma
(`markedChew`/`markedBlock`); the ×2 doubling identity remains OPEN (it is a compound, not this
episode). No machine decided. No label upgraded.**

---

## 2026-07-12 — §5g COMPOSITION: the doubling-phase MIDDLE assembled (`markedBlock ∘ cascadeFold`)

Extracted the full M6(k)→M1(k+1) doubling-phase episode sequence from `x2co_trace.py`
(g=2..6, uniform): 1 ENTRY, 2 REGISTER-CHEW, 3 BIG-BLOCK marked sweep (`markedBlock`,
PROVEN ∀v,s), 4 CASCADE FOLD (`cascadeFold`, PROVEN ∀list), 5 REPACK, 6 REGISTER-REBUILD.
The traces confirm the doubling `big_k→big_{k+1}` (`1021→2039 = 2·1021−3`, parity-flip) and
that episodes 5–6 are a HUGE interleaved sweep/rebuild (g=2: R:3914, L:3914, D:1025 macros),
not a single repack; halt-free (doubling phase emits only gaps 1,2).

**PROVEN NEW (`bigCascade`, green, axioms `[propext, Quot.sound]`):** episodes 3+4 compose
into ONE halt-free transport `46v+29+foldTime m bs` steps. The glue is SYMBOLIC: `markedBlock v s`
leaves `[D] 0^2 1^{2s+1} 0^2 T`; `cascadeFold bs m` wants `[D] 0^2 1^{2m+3} 0^2 (casc bs T')`;
they glue by `2s+1 = 2m+3 ⟺ s = m+1` with `T := casc bs T'`. Kernel `#eval` cross-check (v=2,
m=0: 121 steps, lands `[D] 0^2 1^3 0^2`, `some`) vs the raw x2 machine. This CORRECTS the
`cascade_traversal` framing (which mis-treated the marked big block as an unmarked first
fold-block): physically the big block carries the `(10)^10` marker (episode 3, `markedBlock`),
the cascade blocks are plain (episode 4, `cascadeFold`).

**`doubling_transport_mid` (green):** composes `H_entry` + `bigCascade` + `H_repack` via
`steps_add`. Discharges episodes 3+4 into the PROVEN middle — a strict tightening of
`doubling_transport` (which covered only episode 4). Remaining named hypotheses: `H_entry`
(episodes 1,2, reaching the MARKED-big-block start), `H_repack` (episodes 5,6, the repack +
register-rebuild to `M1next`).

**The exact NET-DOUBLING obstruction (`bigCascade_not_doubling`, green).** The ×2 does NOT
close from the composed middle. Even granting a clean repack of every deposited comb: the
big-block comb repacks to `2(v+1) = 2^K−2`; the cascade combs sum to `2^{K-1}−4K+8`
(`cascadeBlocks_sum`, the `−4K+8` correction); plus the `1^{21}` residue. These are
K-DEPENDENT and do NOT combine to a fixed `2^{K+1}−3`: the residual (target − naive-repack
total) is `Θ(K)` — numerically `−7, −6, −3` at `K=10, 11, 14` (Python check). So the `−4K+8`
correction does NOT self-cancel to `doubling_id`'s `2^{K+1}−3`; the missing `Θ(K)` must be
supplied by the register-rebuild (episode 6), which couples to `2^K` and is captured by NO
lemma in this file. **This is the exact compositional obstruction: episodes 3+4 (chew+fold)
are proven and halt-free; the ×2 lives entirely in the un-formalized repack+rebuild
(`H_repack`), which carries a K-dependent register correction.**

**Verdict: the doubling-phase MIDDLE (episodes 3+4) is now a single PROVEN halt-free transport
(`bigCascade`); episodes 1–2 (entry) and 5–6 (repack+rebuild = the actual ×2) remain named
hypotheses. `H_repack` NOT discharged — the ×2 is a compound whose closing step couples to
2^K. No machine decided. No label upgraded.**

---

## §5h (2026-07-12) — Episodes 5,6 (REPACK + REGISTER-REBUILD) EXTRACTED cell-for-cell; the FOURTH framing, REFUTED

**Goal.** Formalize episodes 5,6 as `rebuild_transport : M_mid(k) → M1(k+1)`, discharging
`doubling_transport_mid`'s `H_repack`. **Result: NOT dischargeable as posed — but now with a
machine-checked reason.** Extraction ran the RAW machine (= X2.lean `step`) on the real
milestone tapes M1(g) for g=2,3 (harness cross-checks `x2co_trace.py`/`x2cc_gencheck.py`).

**Extracted reality of the doubling phase M6(g)→M1(g+1).** It is ONE braided
milestone-to-milestone segment (no intermediate E-on-leading-0 milestones). Length
`2 119 358` steps (g=2), `8 477 210` (g=3) — a `≈4×` jump = `Θ(2^{2K})`, `K=g+8`. In this
file's certified macros (`try_R_cycle` = `sweepEF`, `try_L_cycle`, `try_D_loop` =
`dSweepTurn`): g=2 `R=L=3914`, `D=1025`; g=3 `R=9856, L=9854, D=2050`. `R≈L` and both
`Θ(2^K)`. The macro STREAM is a continuous braid `…L,R,L,R,…,D,D,…` with the register units
`(1^5 0^2)` pulled in INTERMITTENTLY across the WHOLE phase. One full round-trip = an
`E`-sweep RIGHT over the live comb `(01)^n` (this is `sweepEF`, the genuine on-path ×2
primitive, PROVEN ∀n), a turn into `C` at the next 1-block boundary, and a leftward RETURN;
the next round-trip runs over a comb SHORTER by one unit → a shrinking-comb ODOMETER
(quadratic, matching the `4×` scaling), interleaved with `D`-loop register/cascade crossings.

**The exact Lean obstruction (three findings, all machine-checked).**
1. **`M_mid(k)` is OFF-path.** `bigCascade`/`markedBlock` require the `(10)^10`-MARKED big
   block `[D] 0^2 (10)^10 1^{2v+1} 0^2 …`. That marked input occurs **0 times** in the real
   doubling phase (exhaustive scan, g=2): the real big block `1^{2^K−3}` is preceded by the
   register `(1^5 0^2)^{g-1} 1 0^2`, NOT a `(10)^10` marker, and is crossed by `D`-sweeps
   INSIDE the block (`1^24 [D] 1^24`) interleaved with the repack. So `bigCascade` — a VALID
   `step` lemma — lies off the trajectory; `doubling_transport_mid`'s `H_entry`/`H_repack`
   are jointly UNSATISFIABLE on the real path (no `[D]`-marked hand-off exists there).
2. **No fixed tile, no uniform-shift invariant.** The braid's `L`/`R` round-trip lengths
   shrink every trip; there is no recurring `Cfg(p)→Cfg(p−1)`. Neither `steps_add`
   composition of a bounded tile set nor a `List`-fold (the `cascadeFold` pattern) captures
   it — it is a genuine DOUBLE induction whose outer invariant must carry the ENTIRE cascade
   + register state; it does not localize.
3. **The ×2 couples to `2^K` and the FULL cascade.** Consistent with the prior
   `bigCascade_not_doubling` `Θ(K)` residual: the missing `Θ(K)` is realized only by the
   braid's SIMULTANEOUS processing of every cascade block + the register `U^g`.

**Lean deliverable (green, sorry-free, axioms `[propext, Quot.sound]` only).** X2.lean §5h:
the obstruction documented cell-for-cell, plus a kernel HALT-FREE anchor for the on-path
repack round-trip context (`steps 800 ⟨E,0,⟨ones 20, false, pow10 8 ++ ones 5⟩⟩ ≠ none`).
NO `rebuild_transport` added (any such lemma would be false-on-path or vacuous). §7 scope +
final verdict updated. What stays certified on-path: `sweepEF` (×2 repack primitive ∀n),
`dSweepTurn` (block crossings ∀n), and repack-round-trip halt-freedom.

**Verdict: `H_repack` NOT discharged; episodes 5,6 do not exist as a localizable segment —
they are one interleaved shrinking-comb odometer braid coupling to the full cascade and 2^K.
`doubling_transport`/`doubling_transport_mid` now prove exactly: IF a marked-big-block entry
and a post-cascade repack existed as segments, the doubling phase would compose halt-free —
but the real machine realizes no such segments. No machine decided. No label upgraded.**

---

## APPEND 2026-07-12 (session 2): ON-PATH inner comb-shrink induction, independently re-extracted by RAW simulation

**What was done.** Rebuilt a raw `step`-level simulator (matching X2.lean `step` exactly, no
macros) and simulated the concrete milestone tape `m1_spec(2)` cell-for-cell. Independently
re-confirmed the doubling phase `M6(2)→M1(3)`: **M6 at raw step 343, M1(3) at 2 119 358 —
exactly 2 119 015 steps, `Θ(2^{2K})`, K=10** (matches §5h's earlier macro-derived figure).

**The genuine ON-PATH round-trip, taken from the real orbit (not prose, not the executor).**
In the long steady region the head sits in **state `E` on a boundary `0`** between a growing
`(10)`-comb (LEFT) and the big block `1^{2v+1}` (RIGHT), running a uniform 6-step cycle
`E:0·F:0·A:1·E:1·C:0·D:0·E:0` that eats two block `1`s, deposits one `0 1` comb pair, re-lands
`E` on the next boundary `0`, `+2`. **Verified at raw step n=646: block length 969 → (6 steps)
→ 967 at n=652, head E@0** — reproduced in Lean as `ecombChew_tile` (kernel `rfl`). This is the
same physical 6-loop as §5b `chew_tile`, phase-anchored at the on-path milestone state `E`.

**New Lean content (X2.lean §5i, green, sorry-free, axioms `[propext, Quot.sound]` only):**
- `pow01`, `pow01_add` — the `(01)^k` comb the E-tile deposits (mirror of `pow10`).
- `ecombChew_tile` — the on-path 6-step E-anchored comb-deposit tile (kernel `rfl`, reproduces
  the raw n=646 transition).
- **`ecombChewFold` — THE INNER COMB-SHRINK INDUCTION**: `1^{2v+1} → 1^1` depositing `pow01 v`
  in `6v` steps, HALT-FREE ∀v, by tile + length induction. This is the doubling phase's inner
  loop, ON the real orbit (the steady chew of the `1^{2^K−3}` big block, n=646… at g=2).
- `inner_is_linear_not_quadratic` — kernel arithmetic pinning why the inner fold is only
  `Θ(2^{K−1})` while the phase is `Θ(2^{2K})`: the missing quadratic factor is the outer
  odometer.
- ON-path #eval anchors: the tile at n=646 shape, the fold over `1^{41}` (v=20, 120 steps,
  halt-free), and the `sweepEF` repack half fired at the n=6626 shape.

**The EXACT remaining gap (outer induction), re-confirmed by independent raw trace.** The inner
chew produces the comb `pow01 v` (v = 2^{K−1}−2) in `Θ(2^{K−1})` steps; the phase is `Θ(2^{2K})`
because the comb is then repacked by **`sweepEF` round-trips whose length shrinks by one every
trip** (observed raw: comb pair-count descends 6,5,4,3 at n=6626 and grows across successive
round-trips), interleaved at data-dependent positions with the register `(1^5 0^2)` and every
cascade block. No recurring `Cfg(n)→Cfg(n−1)` with uniform shift ⇒ the outer odometer does NOT
localize into a `steps_add`-tile or a `List`-fold — the same non-localizability §5h recorded,
now independently re-derived from the raw orbit with concrete step numbers. The outer invariant
must carry the entire cascade+register symbolically; not closed here.

**Verdict: the inner comb-shrink induction is now PROVEN on-path (`ecombChewFold`); the outer
shrinking-comb odometer remains the exact open gap. No machine decided. No label upgraded.**
