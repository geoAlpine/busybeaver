# A gate/structure/protection classification of the BB(6) cryptids

> **CORRECTION APPENDED 2026-07-07 (`O15_O18_IDENTITY_2026-07-07.md`):** after this survey was drafted, the
> pre-release novelty audit established that **o18 is o15's machine table mirrored and re-rooted** (verified
> isomorphism) — one table, two seeds, two coordinatizations. Read "six machines" as five tables / six orbits.
> Further, o18's "no fatal set found" is superseded: o15's proven fatal family and a community **Lean-verified
> halting congruence class (mod 3¹⁰⁸)** apply to the same table, whose orbits the community expects to HALT
> ("probviously halting"). Community priors for the o3/o4 reduction statements (bbchallenge wiki, 2024) must be
> cited on release; see `NOVELTY_AUDIT_2026-07-07.md` for the full verdict table.

*Paper-style survey (classification only; no new results). Every claim below is a restatement of a result already
established in the lab notes cited inline and in §7, with that note's own epistemic label. Discovery narrative,
red-team logs, and reproduction scripts live in the notes; the theorem-level companion for the o4 run structure is
`PAPER_RUN_STRUCTURE.md`.*

**Status of claims.** Nothing in this document is new. Labels are quoted from the source notes: `[PROVEN]`
(machine-verified or elementary within the program — *not* formalized in a proof assistant), `[PROVEN on grid]`
(exact concrete simulation on the stated parameter grids), `[OBSERVED]` (exact numerics over stated ranges, not a
proof), `[OPEN]`. **No machine is decided; every protection conjecture is open** (§6).

---

## 1. Introduction

Six machines on the bbchallenge BB(6) frontier — the "cryptids" analyzed by this program — with their specs and
proven local halt conditions:

| machine | transition table | halt transition |
|---|---|---|
| Antihydra | `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` | balance counter underflow (see §2) |
| o3 | `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC` | F reads 0 |
| o4 | `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---` | F reads 1 |
| o15 | `1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA` | A reads 1 |
| o17 | `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` | F reads 0 |
| o18 | `1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` | F reads 1 |

**The superseded dichotomy.** The earlier organizing scheme was a B1/B2 wall dichotomy — "equidistribution/density
(B1) vs deterministic arithmetic odometer (B2)" — living in the counter-dependence of a finite boundary graph
(`BOUNDARY_GRAPH_B1_2026-07-05.md`: Antihydra, o4, o3 all reduce to finite boundary graphs of 125/121/175 contexts
with 24/25/36 counter-dependent branches; the graph shape does not distinguish B1 from B2). The template-closure
campaign refined this (`BB6_CRYPTID_SPECIES_2026-07-07.md`): the B2 machines do not uniformly bottom out in one
kind of wall — o4 and o3 bottom out in ledgers of the same one-sided species as Antihydra's density kernel `(K)`,
o17 in timing, o18 in an induction — while B1's density call survives at Antihydra and, sharpened to cylinder
form, at o15. The dichotomy is superseded by a decomposition.

**The decomposition thesis** (`BB6_CRYPTID_SPECIES_2026-07-07.md`). Every analyzed cryptid decomposes as

> **GATE** (a proven local halt condition with a forced predecessor chain) **+ STRUCTURE** (certified generation
> dynamics) **+ PROTECTION** (the single remaining open conjecture: why the gate never fires on the real orbit).

The first two components are largely `[PROVEN]` per machine; the entire open content of each machine lives in its
protection, an orbit-specific quenched statement appearing in five distinct coordinate systems (§4).

## 2. Gates

For each machine the halt state has a unique in-table predecessor, so chasing forced steps turns "halt" into a
local tape pattern; and the census of halt-relevant windows around gate events saturates at a small, safe set
early in the run. `[PROVEN from table]` for each reduction; censuses `[OBSERVED]` on the stated runs.

| machine | forced chain | halt ⟺ | window saturation | source |
|---|---|---|---|---|
| o18 | F entered only by `D,1→1LF` | D reads a 1 with left neighbour 1 | **1** window (`000[1]_D111`), by step 35 | `O18_TEMPLATE_PORT_2026-07-07.md` §0 |
| o15 | A entered only by `F,1→1RA` | F reads a 1 with right neighbour 1 | **2** windows, by step 107 | `O15_TEMPLATE_PORT_2026-07-07.md` §0 |
| o3 | F entered only by `E,0→1RF`; `F,1→0RC` | E reads a 0 with right neighbour 0 | **6** windows (r=5), last new at step 1,370 of a 50M-step run | `O3_TEMPLATE_PORT_2026-07-06.md` §0 |
| o17 | F only by `D,0→0LF`; D only by `A,1→1LD` | the pattern `0 0 [1]_A` occurs | **11** windows (r=5), by step 706 | `O17_HALT_FLAVOR_2026-07-06.md` §1 |
| o4 | F entered only by `B,1→1RF` | B reads the left 1 of an `11` pair | **23** windows (r=5) | `BB6_CRYPTID_SPECIES_2026-07-07.md` (from `O4_WINDOW_SATURATION_2026-07-06`) |
| Antihydra | the `(K)` reduction chain | balance `3E_n − n < 0` for some n | (chain in place of census; Link 0–3) | `BB6_FRAMEWORK_PACKAGE.md` §2 |

Antihydra's "gate" is the machine-verified reduction chain `[PROVEN]`: the computation tracks `c₀=8`,
`c_{n+1}=⌊3c_n/2⌋` with `E_n` = even count, and halts iff `balance_n = 3E_n − n < 0` for some `n` (Link 0); the
GAP lemma collapses the orbit to the induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`, seed `o₀=27`
(Link 1); Kac/renewal converts the density threshold to `mean D ≥ 3/2` (Link 2); the valuation formula gives the
one-sided cylinder form (Link 3).

**The universal pattern.** In every machine the gate half is small, local, proven, and saturates safely — the
gate is never the obstruction (`BB6_CRYPTID_SPECIES_2026-07-07.md`). What is open is always whether the certified
dynamics ever *delivers* the fatal pattern.

## 3. Structures

| machine | structure | status |
|---|---|---|
| o4 | rigid template `prefix · body^r · suffix` (period-2 sweeps); odometer `G′=⌊4G/3⌋+c(G mod 3)` derived from the templates | `[PROVEN, certified + red-teamed]` (`O4_TEMPLATE_CLOSURE_2026-07-06.md`) |
| o3 | rigid template (sweep-cycle certificates p=10/20/6); complete state = two counters `(a,k)`; generation laws exact | `[PROVEN on grid]` (`O3_TEMPLATE_PORT_2026-07-06.md`) |
| o15 | rigid template, 5 shape classes, stable under queue depth; complete state = digit queue `D` + big block `V` | `[PROVEN on grid]` (`O15_TEMPLATE_PORT_2026-07-07.md`) |
| o18 | pushdown 3-adic odometer: rigid template at every closed level, and the whole recursion tower = ONE finite transition table on states `D(m,t,e)` | levels + table `[PROVEN on grid]`; multi-defect regime `[OPEN]` (`O18_TEMPLATE_PORT_2026-07-07.md`, `O18_DEPTH_UNIFORM_2026-07-07.md`) |
| o17 | NO template found: generation shapes unbounded on the measured ranges (69 distinct in 1,006 generations, 91 in 1,635, new shapes still appearing; second-level compression collapses nothing); generation state = the whole digit string; √step width growth | template refutation `[OBSERVED]` over the stated ranges (`O17_HALT_FLAVOR_2026-07-06.md` §2; the species synthesis's earlier stronger label was corrected to `[OBSERVED refutation]`, 2026-07-07) |
| Antihydra | finite boundary graph (125 contexts) with counter-dependent branching (24); no template extracted | `[OBSERVED]` (`BOUNDARY_GRAPH_B1_2026-07-05.md`) |

Details worth stating exactly. **o4**: prefix (fixed 471-step word), body (`B(k)→B(k+2)` in exactly `15+4k`
steps), and three suffix classes are each parameter-uniform certified lemmas (episodes + sweeps + the red-team
episode-landmark-pinning repair); composing them *derives* the odometer law. **o3**: the milestone `M(a,k)` is a
complete state, and the generation map is a deterministic integer map on `(a,k)`, exact on the grids with 0
exceptions. **o15**: the milestone state is an unbounded digit-block vector — rigid template, but no O(1)
counter state. **o18**: every previously mysterious tower phenomenon (mod-3^k branch laws, depth irregularity)
is derived from or refuted by the finite `D(m,t,e)` table; the push law `m′−1=(8/3)(m−1)` gives depth
`= v₃(m−1)` per cascade by the fixed-point argument. **o17** is the in-family counterexample: the o4 template
premise fails structurally, which is the content of the √step growth.

## 4. Protections — the five shapes + one

Each protection is the single `[OPEN]` conjecture of its machine: an orbit-specific quenched statement, in five
different coordinates (`BB6_CRYPTID_SPECIES_2026-07-07.md`).

### 4.1 Residue-ledger (o4, o3)

**o4** (`O4_TEMPLATE_CLOSURE_2026-07-06.md`, `O4_LEDGER_ANALYSIS_2026-07-06.md`). Alongside the odometer `G`, a
filler counter evolves by `a′ = a + δ(G mod 3)`, `δ = {1: −1, 2: +4, 0: +6}` — a prefix-sum ledger over the
odometer's residue sequence. **o4 does not halt ⟸ `a ≥ 2` at every `G ≡ 1 (mod 3)` generation** `[PROVEN
direction]`. The fatal set is `[PROVEN nonempty]`: the standalone configuration `Z(41, g=3, a=0)` halts at step
55,170. Margin: drift ≈ +3/generation; annealed ruin probability `η^a` with `η = 0.334895…`; real-orbit frontier
`a = 124` gives ≈ 10⁻⁵⁹. Seed-specificity is `[PROVEN]` (itinerary bijection: every residue pattern is realized
by a full seed class mod `3^L`, so no seed-uniform safety theorem exists; see `PAPER_RUN_STRUCTURE.md` Thm. 1).

**o3** (`O3_TEMPLATE_PORT_2026-07-06.md`) — the same shape with the roles swapped: `a` is the base-4/3 odometer
(`a′=⌊4a/3⌋+c`, derived from the templates) and `k` is the ledger, with `Δk = δ(a mod 3) = {1: +2, 2: +1, 0: −1}`
exactly (this CORRECTS the earlier `O3_TRANSDUCER.md` §4 `[OBSERVED]` claim that Δk is history-dependent). Fatal
set `[PROVEN nonempty]`: `{k=1 ∧ a≡6 (mod 9)} ∪ {k=0 ∧ a≡2 (mod 3)}`, with halting configurations **predicted
a priori and confirmed** (`M(1005,1)` halts at step 1,694,235; `M(302,0)`). Margin: net drift +0.248/generation;
in 200,000 exactly-iterated generations the longest drain run is 10 against a reservoir `k ≈ 10⁴–10⁵`.

### 4.2 String-ledger (o15)

(`O15_TEMPLATE_PORT_2026-07-07.md`, `O15_FIXEDPOINT_2026-07-07.md`.) The ledger coordinate is not a counter but
the whole base-3 digit string of the Mahler-8/3 orbit: non-halt ⟺ the carry cascade never stacks a **leading
`[2,2]` digit pair at a split-class step** — a cylinder-avoidance statement in the digit-string coordinate. The
fatal set is `[PROVEN nonempty]` and **predicted-and-confirmed**: `M([2,2],V)` halts for `V ≡ 0,1 (mod 3)`
(fresh members `[2,2,151]`, `[2,2,301]`, `[2,2,1000]` — halt at step 1,336,398 — and `[2,2,2,150]`, each
predicted before simulation). The fatal cylinder's exact boundary is a **recursive string language** — refined
finite laws hold 94/96 with structured misses, and it is **provably not a congruence in V**: buffers
`[1,2,1,2,1,1]` (fatal) and `[1,1,2,1,2,1]` (safe) share value, length, and digit multiset
(`O15_FIXEDPOINT_2026-07-07.md` §4). Margin: an exposure record only — no leading 2 in the 11 observed blank-orbit
generations; the queue alphabet so far is {1,3,6}, so the first prerequisite (a ≡2 digit) has not yet occurred.

### 4.3 Density (Antihydra)

(`BB6_FRAMEWORK_PACKAGE.md` §1–2.) Non-halt ⟺ even-density `E_n/n ≥ 1/3` for all `n` ⟺ `mean D ≥ 3/2` — the
kernel `(K)`, the one-sided, level-2, single-orbit floor-mirror fragment of the Andrieu–Eliahou–Vivion normality
conjecture (arXiv:2510.11723). Halting *is* density failure: there is no separate fatal set. Margin: **zero** —
the 1/3 threshold is exact (sharp in Link 0), the drift criterion sits exactly at criticality; the protection is
the razor-edge member of the family. `(K)` `[OPEN]`; the No-Structure theorem `[PROVEN]` shows no
bounded-residue, all-orbits, or measure-level certificate can decide it.

### 4.4 Tower-sparse regenerative-wall carry-timing (o17)

(`O17_HALT_FLAVOR_2026-07-06.md`, `O17_GATE_LAW_2026-07-07.md`.) No ledger value exists to protect the orbit:
the marker automaton `{3→{3,5}, 5→{3,8=HALT}}` leaves distance-to-fatal **≤ 1 at every gate**. The protection is
timing. The gate-to-gate map `F(μ, d⃗)` is exact and machine-validated (iterating F from `(3,[])` reproduces the
blank orbit's gate steps `5, 22, 44, 101, 314, 724, 2005, 1072566` exactly). The step clock is `t ≈ 3.97·n²` in
odometer ticks `[OBSERVED, tight]`, and gate ticks obey **`log n_{k+1} ≈ a·n_k`** `[OBSERVED + extrapolation —
NOT proven]`: iterated-exponential (tower) sparsity, next blank gate extrapolated at `t₉ ~ 10^{60±20}` steps.
Mechanism: each survived gate shatters its era's counter into a wall of zero-blocks whose erosion cost grows
∝ n per block — the protection is **self-reinforcing in time** (each survival delays the next exposure
exponentially) while remaining one step from death in value. The branch determinant `b = F_μ` has rigid islands
(`m ≤ 2` decided by digit count alone, value-robust to d ≤ 1000) but **every finite reduction is refuted for
m ≥ 3** (residue words mod 2/3/6, prefix/suffix windows to length 5, +6 shifts, final-tick windows, moment
recodings — all ambiguous `[OBSERVED, 4374-config ensembles]`); the minimal known description of `b` is F
itself, and future gates have `m_k ≈ n_k → ∞`, far outside every island.

### 4.5 Level-safety / multi-defect grammar (o18)

(`O18_TEMPLATE_PORT_2026-07-07.md`, `O18_DEPTH_UNIFORM_2026-07-07.md`.) The outlier: **no fatal set has been
found anywhere** — zero halting configurations across the `B(m,e)` defective family, the full `D(m,t,e)` grid
(~900 runs incl. the m=6..29 floor scan), and the multi-defect word probes; cumulative unsafe = 0 in every run
(a negative search result, not a theorem). The previously "unclosed, Collatz-irregular" deep branches are
REFUTED-and-corrected: both flagship cases land (`N=26 → C_22038` at step 105,994,679; `N=53 → C_17948`), and a
12/12 batch of full predicted F-chains was confirmed exactly, the deepest at 3,437,998,769 steps
(`N=134 → C_125526`). The push law `m′−1=(8/3)(m−1)` puts o18 in the ×8/3 family with derived depth `v₃(m−1)`.
The precisely-stated open blocker: **(a)** close the general multi-defect rewrite grammar (the `m≡0` carry-cascade
schema, double-0 words, word-length finiteness per pass); **(b)** certify each rewrite as a trace template
uniform in all block parameters (the o4 pinning standard); **(c)** conclude non-halt by invariant closure +
per-passage safety — no termination argument needed. The symbolic orbit exits the single-defect family at
tower-step 8394 (`m ≈ 10^3577`), so the multi-defect regime is on the true orbit.

## 5. The unification and the margin ladder

**The mirror ladder** (`PAPER_RUN_STRUCTURE.md` §4, Theorem 3 and Remark — cited, not re-derived here): four of
the kernels are literally the *3-adic (resp. 2-adic) depth process of an affine ×p/q orbit*:

| machine | orbit map | depth process | budget |
|---|---|---|---|
| Antihydra | `c ↦ ⌊3c/2⌋` | `v₂(c_n − 1)` under ×3/2 | constant (critical) |
| o4 | `T` (base-4/3 odometer) | `v₃(W_n)` under ×4/3 | grows +3/generation |
| o15 | `V′ = (8V+c)/3` family | `v₃(V_n − 1)` under ×8/3 | cylinder form |
| o18 (depth) | push law `m′−1 = (8/3)(m−1)` | `v₃(m − 1)` | no fatal set known |

**The unified open problem.** All the protections are the `(K)`-species in different coordinates: one-sided
prefix-sums (o4/o3), cylinder avoidance in a digit string (o15), Cesàro density (Antihydra), sparsity-in-time
(o17), well-foundedness/closure of a recursion (o18). Per-return depth is controlled unconditionally
(`PAPER_RUN_STRUCTURE.md` Cor. 2.1 and its ported analogues); what is open in every case is the frequency axis:
**an effective quenched upper bound on the frequency of deep p-adic returns of an explicit affine ×p/q orbit**.

**The margin ladder** orders the family (`BB6_CRYPTID_SPECIES_2026-07-07.md`): **o4** (drift +3/generation) ≫
**o3** (+0.248) > **o15** (cylinder-exposure record) > **o17** (tower-sparse timing) > **Antihydra** (zero
margin, critical). If an orbit-specific quenched tool ever materializes, this is the predicted falling order —
o4 first, Antihydra last. **o18 stands apart**: with no fatal set found and closed laws at every examined level, its remaining
content is a level-induction (grammar closure + uniform template certification), arguably attackable *without*
the quenched tool — the most decision-adjacent target in the family (`O18_DEPTH_UNIFORM_2026-07-07.md` §5,
`BB6_CRYPTID_SPECIES_2026-07-07.md`).

## 6. Honest scope

- **All six protections are `[OPEN]`. No machine is decided. No label has been upgraded.** The gate+structure
  halves are closed to the program's certification standard; the protection of each machine is exactly the open
  conjecture stated in §4, and for Antihydra it is `(K)`, proven structurally resistant to every certificate
  register so far examined (`BB6_FRAMEWORK_PACKAGE.md` §3).
- **Epistemic status of the labels.** `[PROVEN]` here means machine-verified or elementary within the program's
  soundness discipline (exact concrete simulation in every proof path, no acceleration; red-teamed where stated)
  — *not* formalized in a proof assistant. `[PROVEN on grid]` results are exact with zero exceptions on the
  stated finite grids; their extension to all parameters rests on certified sweep/episode arguments where the
  pinning lemma has been run (o4; o3 boundary chunks) and remains a stated gap where it has not (o18 cells, o15
  sweeps). `[OBSERVED]` claims (o17's tower law, census bounds, negative searches) prove nothing about halting.
- **Corrections and retractions are part of the record**, per the zero-false-proof discipline: o4's red-team
  found and repaired a genuine gap in the template generalization (episode-landmark pinning), restated the
  small-a suffix, and fixed a provenance conflation (`O4_TEMPLATE_CLOSURE_2026-07-06.md` §6); o3's port corrected
  `O3_TRANSDUCER.md` §4 (Δk is residue-determined, not history-dependent); o18's port corrected the prior orbit
  claim `3890 → 27660` (not 10375), and `O18_DEPTH_UNIFORM_2026-07-07.md` superseded its own predecessor's
  "unclosed ≥7-level branches" (they land) while fixing a detection bug in its own tooling; o15's notes document
  two refuted hypotheses (the end-local absorption law; "fatal ⟺ no 11 factor") and a corrected drain law. A
  labeling tension caught during this survey's preparation (the species synthesis had recorded o17's template
  refutation as `[PROVEN-refuted template]` where the underlying note says `[OBSERVED]`) was corrected in the
  species synthesis on 2026-07-07; §3 states the `[OBSERVED]` form.
- The fatal configurations of o4/o3/o15 are standalone; **reachability from the blank tape is in each case
  exactly the open protection question and is not claimed**.

## 7. References to the record

Classification synthesis: `BB6_CRYPTID_SPECIES_2026-07-07.md`. o4: `O4_TEMPLATE_CLOSURE_2026-07-06.md` (red-team
log included), `O4_LEDGER_ANALYSIS_2026-07-06.md`; theorem-level companion `PAPER_RUN_STRUCTURE.md`. o3:
`O3_TEMPLATE_PORT_2026-07-06.md`. o15: `O15_TEMPLATE_PORT_2026-07-07.md`, `O15_FIXEDPOINT_2026-07-07.md`. o17:
`O17_HALT_FLAVOR_2026-07-06.md`, `O17_GATE_LAW_2026-07-07.md`. o18: `O18_TEMPLATE_PORT_2026-07-07.md`,
`O18_DEPTH_UNIFORM_2026-07-07.md`. Antihydra: `BB6_FRAMEWORK_PACKAGE.md` §1–2 (the `(K)` reduction chain and its
AEV anchor, arXiv:2510.11723). Superseded-in-part dichotomy: `BOUNDARY_GRAPH_B1_2026-07-05.md`,
`B2_DECISION_FORK_2026-07-05.md`. Verification entry point: `verify_all.py`.
