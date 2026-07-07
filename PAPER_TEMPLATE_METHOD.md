# The certified trace-template method, with a complete reduction of the cryptid o4

*Paper-style writeup (method–theorem only; discovery narrative, red-team logs, and reproduction scripts live in the
lab notes `O4_TEMPLATE_CLOSURE_2026-07-06.md`, `O4_WINDOW_SATURATION_2026-07-06.md`, `O4_SEAM_PARITY_LEMMA_2026-07-06.md`,
`O4_CSEAM_LOCALIZATION_2026-07-06.md`, `O3_TEMPLATE_PORT_2026-07-06.md`, `O4_GROWING_REGIME_2026-07-07.md`.
Verification: items `o4_body_proof.py`, `o4_seam_lemma_verify.py`, `o4_growing_certify.py`, `o4_wander_certify.py`,
`o4_closure_fixpoint.py`, `o3_body_proof.py`, `o4_bouncer_macro.py` in `verify_all.py`.)*

**Status of claims.** Every statement below carries the label under which it is recorded in the lab notes:
`[PROVEN]` (exact concrete simulation on constructed configurations, plus the stated generalization argument),
`[OBSERVED]` (measured on stated ranges, no generality claimed), `[OPEN]`, or `[PROVEN — candidate]` where the
source note itself attaches that qualifier. Nothing here is new; this document restates the record. The method's
generalization step is grid-certified with a stated composition argument — it is **not** formalized in a proof
assistant (see §5). **No machine is decided.**

---

## 1. Introduction

The BB(6) *cryptids* are 6-state Turing machines whose halting problem resists all known certified deciders; each
runs a growing, self-similar computation whose non-halting appears to encode an unbounded arithmetic fact.
The bbchallenge project's certified deciders (in particular *bouncers*: machines whose tape grows by a repeated
back-and-forth sweep, decided by a closed-form triangular jump certificate) handle machines whose macroscopic
behavior is eventually periodic modulo a uniform translation. The cryptids fall outside these deciders because each
generation ends in a **parameterized reset**: the counters that shape the next generation are updated by a nontrivial
arithmetic map (for o4, a base-4/3 odometer with a residue-dependent carry), so no single closed-form jump covers
the whole orbit (`O4_WINDOW_SATURATION_2026-07-06.md`, "bouncer + base-4/3-odometer-reset").

A **certified template** for such a machine is: (i) an exact decomposition of every generation's micro-event stream
into a rigid word `prefix · body^r · suffix` over compressed trace pieces, each piece a parameter-uniform lemma
proven by the method of §2; (ii) a derived arithmetic law for the counters across generations; and (iii) an explicit
residual condition ("ledger") equivalent to (or sufficient for) non-halting. The method takes a cryptid from
"unbounded simulation evidence" to "finitely many certified lemmas + one explicit Collatz-like conjecture."

## 2. The method

Throughout, fix a deterministic Turing machine and call a *configuration* a (state, head, tape) triple.

### 2.1 Sweep lemmas `[PROVEN]`

A **sweep** is a 2-transition cycle traversing a periodic tape region. For o4 the two sweeps are `B1F0`
(`B:1→1RF`, `F:0→0RB`), a *read-only rightward* sweep preserving any `(10)*` region, and `D1E0`
(`D:1→0LE`, `E:0→1LD`), a *leftward invert-sweep*. Each is proven for **arbitrary length by 2-transition
induction**: one checks the two transitions once, and induction on the region length gives the sweep for every
length (`O4_WINDOW_SATURATION_2026-07-06.md`; the o3 port uses the same certificate for cycles of periods 10, 20, 6,
`O3_TEMPLATE_PORT_2026-07-06.md` §1). Sweep lemmas are **conditional**: they guarantee continuation only while the
tape ahead is correctly tiled by the sweep's period.

### 2.2 Trace compression

A concrete trace is compressed into **bounded episodes** (maximal step runs not inside a sweep) alternating with
**uniform sweeps**. The compressed object — the *skeleton* — is the sequence of episode trace-hashes and sweep
identities; the sweep lengths are recorded separately as functions of the parameters.

### 2.3 Grid verification

A candidate lemma "configuration family `X(k) → Y(k)` in `s(k)` steps" is verified across a parameter grid by exact
concrete simulation, requiring: (a) the compressed **skeleton is identical** at every grid point; (b) the **sweep
lengths are exactly affine** in the parameters; (c) the landing configuration, step count, and safety counts (no
halt-relevant unsafe event) are exact at every grid point.

### 2.4 The generalization argument (red-team-corrected form)

The naive argument — "if the lemma failed at some off-grid parameter, the first divergence from the skeleton would
lie inside an episode, and episodes are finite objects already checked" — has a **genuine logical gap**
(`O4_TEMPLATE_CLOSURE_2026-07-06.md` §2): because sweep lemmas are conditional, sweep *termination* is
tape-determined, and a parameter-dependent defect inside a swept region was not excluded by episode checks alone.

The repair is:

**Lemma (episode-landmark pinning) `[VERIFIED from the traces]`.** Every episode step sits at a
parameter-INDEPENDENT offset (at most 3) from a structural landmark (zone edge, cap, filler edge, or landing point).
For o4: body — all 8 grid values of k, offsets exactly affine; suffix — zero unpinned steps across the grid to
k = 251, all classes; prefix — span [−11, 30] never touches gap-end or filler, for all G ≥ 31, all a.

**Soundness argument of the method (as stated in the record).** With every episode pinned to landmarks at
parameter-independent offsets, and with sweeps traversing only regions that are uniform by the sweep invariants, the
tape content at every step is **symbolically reconstructible** as a function of the parameters; the first-divergence
argument then closes, and skeleton identity + affine sweep lengths on the grid certify the lemma for the whole
stated parameter cone. *Epistemic status:* this composition argument is stated and grid-verified
(including adversarially strengthened grids under red-team); it is **not** a machine-checked symbolic induction.
Lemmas certified this way are labelled `[PROVEN, certified trace-template method]` in the record, with this caveat
attached (`O4_TEMPLATE_CLOSURE_2026-07-06.md` §6, `O4_GROWING_REGIME_2026-07-07.md` §5).

### 2.5 Small-parameter restatement (mandatory companion to §2.3)

At the method's own compression threshold, "one skeleton per class" can be FALSE for small parameter values (for o4's
suffix, a-dependent stretches of length ~a straddle the threshold for a ≤ 4). The correct general form: the
parameter cone is covered by **finitely many per-small-parameter templates plus one generic large-parameter template
per class**, with identical landings and safety; only the template *count* changes, and the lemma's conclusion is
unaffected (`O4_TEMPLATE_CLOSURE_2026-07-06.md` §2; the o3 port hits the same phenomenon at one k = 2 prefix
variant, `O3_TEMPLATE_PORT_2026-07-06.md` §3).

## 3. Application: the reduction of o4

**Machine.** o4 = `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`, blank tape; halt = state F reads 1.

### 3.1 Halt gate `[PROVEN from the transition table]`

F is entered only by `B:1→1RF`, so F reads the cell immediately right of a B-read-1, and the halt condition is
`F:1`. Hence **o4 does not halt ⟺ every 1 that B reads has right-neighbour 0** ("safety")
(`O4_WINDOW_SATURATION_2026-07-06.md`). A complementary impossibility result pins why locality alone cannot finish:
the least window-set closed under the *adversarial* microstep (incoming cell treated as free) provably contains the
HALT window at every radius ≤ 5, so **no purely-local sofic head-window certificate of radius ≤ 5 proves non-halt**
`[PROVEN]` (`o4_closure_fixpoint.py`) — the incoming cell is background-determined, and that determination carries
the odometer information. The template method supplies exactly this global structure.

### 3.2 Seam decomposition `[PROVEN from the table + forced local chains]`

A B-read-1 touching an `11` ("seam") always has B on the RIGHT 1, with creator A, and the seam-creating A has
predecessor in {E, C} only (`O4_SEAM_PARITY_LEMMA_2026-07-06.md`).

**E-seams are safe unconditionally, for all G `[PROVEN]`.** E is entered only by `D:1→0LE`; the forced 4-step chain
`D@q+2` (erase, move L) → `E@q+1` reads 1 → `A@q` reads 0 → `B@q+1` reads 1 with `tape[q+2] = 0` — the head goes
`q+2 → q+1 → q → q+1` and never retouches `q+2` after D's erase. Zero odometer information is needed. Every
gap-edge (cascade) seam — exactly where the base-4/3 carry meets the filler — is E-type (census 24,413/24,413 at
G ≈ 24,644), so the feared carry-desynchronization mechanism does not exist.

**C-seams `[PROVEN per event]`.** C-seams occur at the phase boundary *inside the filler* (the previous invert-sweep's
turnaround), not at the `1001` cap — a corrected location (`O4_CSEAM_LOCALIZATION_2026-07-06.md`). Every recurring
C-seam is the forced tail of a sweep-end event (`B:0→1RC · C:1→0RA · A:0`, or its doubled form), safe by a **forced
14-cell bounded template**, k-uniform for all k ≥ 4 by a locality lemma, with real-trace step-for-step identity on
all recurring instances. The cap crossing itself is seam-free and k-uniform (k ≥ 4).

### 3.3 The rigid template and its three lemmas

**Milestone.** `M(G, a)`: head on the gap-left 0, state E; tape = left zone · gap `0^G` · filler `(10)^a` · cap
`1001` (the prefix lands the zone as `(10)^19 1001`). Every generation's micro-event stream is exactly
`prefix(454 events) · body(51 events)^r · suffix(class-dependent)` with only sweep lengths and r varying
`[OBSERVED → certified]` (`O4_TEMPLATE_CLOSURE_2026-07-06.md` §1).

- **PREFIX `[PROVEN]`.** From `M(G, a)`: a fixed **471-step word** (identical trace hash across the grid), span
  [−11, 30] (bounded, (G, a)-independent), unsafe = 0, landing with gap and filler intact. Valid for all G ≥ 37,
  all a.
- **BODY `[PROVEN]`.** Standalone `B(k) = 0^∞ [E] (10)^k 1001 0^∞ → B(k+2)` shifted −1, in exactly **15 + 4k**
  steps; skeleton identical (9 episodes + 2 sweeps), sweep lengths exactly `(2+2k, 4+2k)`, unsafe = 0; verified at
  k = 19..27, 49, 101, 251 ⇒ all odd k ≥ 19. Consumes 3 gap cells per application. (Red-team note: span is
  [−1, 2k+6], tighter than the originally claimed [−1, 2k+8].)
- **SUFFIX `[PROVEN]`, 3 classes.** With gap-at-meet `g ∈ {3,4,5}`, `g ≡ G − 31 (mod 3)`: `Z(k, g, a) → M(G′, a′)`,
  exact milestone landing, steps affine, unsafe = 0, landings verified to k = 251:

  | g | valid | G′ | a′ |
  |---|---|---|---|
  | 3 | a ≥ 2 | 2k + 12 | a − 1 |
  | 4 | a ≥ 0 | 2k + 9 | a + 4 |
  | 5 | a ≥ 0 | 2k + 13 | a + 6 |

  Per §2.5, for a ≤ 4 the cone is covered by finitely many per-a templates (each k-uniform to k = 251) plus one
  generic a ≥ 5 template per class; landings and safety are identical.

### 3.4 The derived odometer and ledger `[PROVEN from templates]`

Composing prefix + r bodies + suffix, with `r = (G − 31 − g)/3` and `k_end = 19 + 2r`:

$$G' = \Big\lfloor \tfrac{4G}{3} \Big\rfloor + c(G \bmod 3), \qquad c(0)=3,\; c(1)=5,\; c(2)=1,$$

the empirically known odometer law, now derived (checked against the real orbit 275 → 367 → 494 → 659). The three
`G mod 3` classes are exactly the three gap-at-meet residues. The filler count evolves by the **ledger**

$$a' = a + \delta(G \bmod 3), \qquad \delta(1) = -1,\; \delta(2) = +4,\; \delta(0) = +6.$$

### 3.5 The reduction theorem and the halting witness

**Theorem (reduction) `[PROVEN: template closure + induction]`.** *o4 does not halt ⟸ the ledger satisfies a ≥ 2 at
every generation with G ≡ 1 (mod 3).* Base case raw-concrete to G ≈ 19.5k (the induction needs only G ≤ 43);
macro-validated to G ≈ 8.8M. (Provenance as red-team-corrected: the raw-concrete and macro-validated ranges are
distinguished.) The converse holds partially; the full ⟺ awaits the completed small-a case analysis.

**Non-vacuity `[verified concrete]`.** The standalone configuration `Z(41, g=3, a=0)` **halts** at step 55,170.
It is not claimed reachable from o4's initial tape — reachability of small-a at g = 3 is exactly the open ledger
question.

### 3.6 Auxiliary regimes: the small-a case map

The tested small-a grid is completely decided (`O4_LEDGER_ANALYSIS_2026-07-06.md` §4 with its wander resolution):
every observed outcome is {recover to a′ ≥ 3} ∪ {halt — only Z(41, 3, 0)} ∪ {translated cycler} ∪ {translated
bouncer}. The translated cyclers Z(29,0), Z(101,0), Z(23,1), Z(41,1) are NON-HALTING `[PROVEN]` by verified
cycler certificates (`o4_wander_certify.py`). The remaining three configs Z(21,3,0), Z(23,3,0), Z(27,3,0) collapse to
the bare-zone family `C(m) := 0^∞ [A] (10)^m 0 1 0^∞` — the body lemma with empty right context — and iterate
`C(m) → C(m+2)` in exactly 4m + 11 steps, a **translated bouncer**; all three are NON-HALTING
`[PROVEN — candidate, pending main-loop re-verification]` (`O4_GROWING_REGIME_2026-07-07.md`; the even-m instances
are inherited from the banked body lemma by a 1-step conjugation).

## 4. Portability

**o3 (positive port, verdict (a)).** o3 = `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC`; halt gate: HALT ⟺ E reads a
0 whose right neighbour is 0 `[PROVEN from table]`. The pipeline replicates fully (`O3_TEMPLATE_PORT_2026-07-06.md`):
sweep-cycle certificates of periods **10, 20, 6**; milestone `M(a,k) = 0^∞ [A] 0 0 (10)^a (110)^k 0^∞`; certified
body lemma (all j ≥ 12, j ≡ 0 mod 3, exactly 10j + 4 steps, same landmark-pinning standard); and a generation law
that collapses to a **deterministic integer map on (a, k)** — here a is the odometer (`a′ = ⌊4a/3⌋ + c`, derived
from template velocities) and k the ledger, with explicit fatal set `{k=1 ∧ a ≡ 6 (mod 9)} ∪ {k=0 ∧ a ≡ 2 (mod 3)}`.
The ledger **predicted** the standalone halting configurations M(1005, 1) (halt at step 1,694,235) and M(302, 0),
both confirmed exactly `[verified concrete]`. Iterated 200,000 generations from (6, 2): no fatal hit. o3 `[OPEN]`.

**o17 (negative case — the method's boundary).** Applying the same lens to o17, the halt **gate** exists, but the
template premise **fails** `[OBSERVED over 1,635 generations]`: 69 distinct generation shapes in 1,006 generations,
91 in 1,635, new shapes appearing indefinitely, shape length growing with carry depth — there is no
`prefix · body^r · suffix` and no finite-residue δ-map (`O17_HALT_FLAVOR_2026-07-06.md`). The method is thus not a
universal cryptid solvent; it applies where generation shape-classes are finite with counter-only variation.

## 5. Honest scope and open problems

- **Formalization.** No lemma in this document is Lean/Coq-formalized. The `[PROVEN]` labels denote: exact concrete
  simulation on constructed configurations for every grid point (no acceleration in any proof path), plus the §2.4
  generalization argument in its red-team-corrected (landmark-pinned) form. The macro-machine
  (`o4_bouncer_macro.py`, validated) is used only for discovery and large-range checks, never in a proof step.
- **The open cores.** The o4 ledger condition (a ≥ 2 at every ρ = 1 generation) and the o3 ledger condition (the
  (a, k) orbit avoiding its fatal set) remain `[OPEN]`. Consequently o4 and o3 are undecided; **no machine is
  decided** by this document or its sources.
- **Structure of the open cores.** The exact 3-adic run structure, the seed–itinerary bijection (no seed-uniform
  proof of the ledger condition can exist), the run cap, and the mirror unification with Antihydra/o15/o18 are the
  subject of the companion document `PAPER_RUN_STRUCTURE.md`.
- **Verification.** One command: `verify_all.py`, items `o4_body_proof.py`, `o4_seam_lemma_verify.py`,
  `o4_growing_certify.py`, `o4_wander_certify.py`, `o4_closure_fixpoint.py`, `o4_ledger_bijection.py`,
  `o3_body_proof.py`, `o4_bouncer_macro.py`.

## References to the record

- `O4_TEMPLATE_CLOSURE_2026-07-06.md` — the o4 master note: prefix/body/suffix lemmas, derived odometer, a-ledger,
  Z(41,3,0), and the red-team corrections (episode-landmark pinning; per-a restatement; base-case provenance).
- `O4_WINDOW_SATURATION_2026-07-06.md` — halt gate and safety reframe; sweep lemmas; bounded-defect structure;
  HALT-in-closure impossibility; validated macro-machine and G ≈ 8.8M runs.
- `O4_SEAM_PARITY_LEMMA_2026-07-06.md` — seam decomposition; the unconditional E-seam chain.
- `O4_CSEAM_LOCALIZATION_2026-07-06.md` — C-seam location correction; 14-cell forced template; seam-free cap.
- `O4_LEDGER_ANALYSIS_2026-07-06.md` — small-a case map and its wander resolution.
- `O4_GROWING_REGIME_2026-07-07.md` — the growing bouncer C(m); the last small-a completeness item.
- `O3_TEMPLATE_PORT_2026-07-06.md` — the o3 port; (a, k) map; predicted-and-confirmed halting configurations.
- `O17_HALT_FLAVOR_2026-07-06.md` — the negative case delimiting the method's scope.
- `CAMPAIGN_2026-07-06_TEMPLATE_LEDGER.md` — campaign index; status table; tool map.
- `PAPER_RUN_STRUCTURE.md` — companion paper on the odometer's run structure.
