# Track B roadmap — the carry-transparent island of the BB(6) frontier (2026-07-16)

*Scoping + planning document for Track B of the complete-proof roadmap: the machines whose carry
sequence is set by an EXPLICIT register (carry-TRANSPARENT / integer-×2 "island"), hence
decidable-in-principle, as opposed to the (K)-wall carry-OPAQUE machines (Track C, gated on the
Andrieu–Eliahou–Vivion Normality Conjecture). READ-ONLY analysis. **This document decides no halting
and upgrades no label**; it is a difficulty-type map and a work-list. Grounded in
`CARRY_DICHOTOMY_2026-07-11.md`, `X2_FRONTIER_MAP_2026-07-11.md`,
`CANDIDATE_NEW_INVESTIGATION_2026-07-10.md`, `PAPER_X2_INTEGER_DOUBLER.md`,
`X2_STATUS_2026-07-12.md`, `X2_UNIFIED_RECURSION_DESIGN_2026-07-16.md`,
`X2_CARRY_CALCULUS_2026-07-11.md`, `PAPER_SPECIES_SURVEY.md`. No Lean file was edited.*

> ### ⚠ CORRECTED 2026-07-17 — READ THIS FIRST
>
> This document's **founding premise is dead**. It was written to find a *friendlier* transparent
> machine that dodges B1's quadratic braid, and it nominated B5 (and B3/B4) as the "de-risking
> front". Re-measurement (`TRACK_B_REAUDIT_2026-07-17.md`, reproduced independently again today by
> `x2ti_island.py`) finds **no such machine anywhere on the island**:
>
> | machine | register | per-doubling cost ratio | |
> |---|---|---|---|
> | B1 *(control — known Θ(4^k) wall)* | maxrun | **3.97** | Θ(v²) |
> | B2 | maxrun | **3.94** | Θ(v²) |
> | B3 | total1 | **3.99** | Θ(v²) |
> | B4 | total1 | **3.98** | Θ(v²) |
> | **B5** | maxrun *(phase-conditioned)* | **4.15** | Θ(v²) — **BRAID-BOUND** |
> | W2 | total1 | **3.94** | Θ(v²) |
> | W1 | total1 | *(gate refuses — not a doubler)* | — |
>
> *Ratios as tabulated at cap 40 M (`TRACK_B_REAUDIT_2026-07-17.md` §3). Independently re-run at
> cap 12 M by `x2ti_island.py`: B1 3.85, B2 3.90, B3 3.97, B4 3.96, W2 3.94, **B5 4.145** — the same
> verdict on every machine, converging upward toward 4 with cap. B5's ratios reproduce **exactly**
> (4.119, 4.142, 4.158, 4.145, 4.130), on an instrument sharing no code with the original.*
>
> **2 = linear/braid-free. 4 = Θ(v²) per doubling. Not one ratio-2 machine exists on the island.**
> B5 — this roadmap's §5 order-1 "fastest possible win", the machine that was supposed to be the
> braid-free counter-example — is braid-bound, on four independent reproductions (`885f6de` 4.10,
> coordinator 4.09, `TRACK_B_REAUDIT` 4.145, `x2ti_island.py` 4.145).
>
> **Two caveats that must survive any future rewrite of this file:**
>
> 1. **Ratio 4 is a COST SIGNATURE, not a MECHANISM.** It shows a doubling costs Θ(v²) — Θ(v) passes
>    over the register rather than one sweep. It does **NOT** prove that B1's specific combinatorial
>    object (the growing-arity digit tree / `carry_step`) lives in B2–B5. No mechanism is asserted
>    for any machine but B1, where it was independently derived.
> 2. **For ANY machine whose cost ∝ width², doubling an observable gives 4× automatically** — that
>    is every ordinary quadratic bouncer, with no braid anywhere. A ratio is evidence only for a
>    register that *genuinely doubles once per macro-generation*. A **`doubling_gate`** (refuse to
>    answer where the register does not double) is what keeps W1 out of the table above, and its
>    absence is what produced a spurious "W1: BRAID" reading. Every ratio here is gated.
>
> Sections below are corrected in place. `[UNSUPPORTED]` marks a claim that was **never
> established** — it is *not* a refutation, and must not be read as one.

---

## 0. What "carry-transparent" means, and why the island exists

From `CARRY_DICHOTOMY_2026-07-11.md` §1 (the load-bearing definition):

- **carry-OPAQUE** (Track C, the (K) wall): the carry/branch sequence IS the residue/digit itinerary
  of an affine `×(p/q)` orbit (`q>1`) whose distribution is itself the open problem. A transparent
  carry law would *be* a proof of that orbit's Normality/avoidance instance. 16 of the 17 named
  cryptids + ~105 collapsed holdouts are here. NOT Track B.
- **carry-TRANSPARENT** (Track B): the carry sequence is driven by an explicit, fully-analyzable
  register — a pure doubling/shift `v↦2v+c`, a base-b odometer, or a bounded affine map — with **no
  open conjecture underneath**. Every question about the carries is a theorem-or-not about a
  completely specified computable dynamical system. Decidable-in-principle: what stands between it and
  a decision is *proof engineering* (faithful tape→register abstraction + a carry calculus over the
  explicit law), not new mathematics.

The island exists because **`q=1` (integer multiplier) degenerates the (K)/Mahler framework**: `×2` in
binary is a clean SHIFT with no bit-mixing, so the `v_q`-depth machinery of the NormalityPQ schema (2
is not a unit mod 1) has nothing to act on (`CANDIDATE_NEW §1b`, `PAPER_X2 §1`). This is the first —
and, on all current evidence, the ONLY — genuinely new engine multiplier beyond `{3/2, 4/3, 8/3, 5/2}`
to survive scrutiny.

**Transparency is NOT a promise of easiness.** The exemplar x2 machine is transparent yet still
undecided: its residual is `o4-wall-class` in hardness (a counter-/context-dependent invariant that
defeats every bounded-window attack), differing from Track C only in that the hardness bottoms out in
an *explicit* register rather than an *open* orbit distribution (`X2_FRONTIER_MAP §3`,
`CARRY_DICHOTOMY §1` "counter-dependent ≠ opaque").

---

## 1. The island members — the concrete list

Source: `CANDIDATE_NEW_INVESTIGATION_2026-07-10.md` §1 (the geometric-sawtooth discriminator, validated
on the 17-named gate, caps 12–60 M, exact big-int) + `CARRY_DICHOTOMY_2026-07-11.md` §3, §6. All
multiplier/reset claims are `[OBSERVED, exact simulation, cap 12–60 M]` unless a Lean/mechanized label
is attached; none is a certified milestone reduction except the primary.

**Named transparent machines among the 17 cryptids: 0.** (Expected — the named frontier is exactly the
machines whose carries encode open mathematics; `CARRY_DICHOTOMY §2`.) The island is drawn entirely
from the 1104-holdout census, ×2 cluster.

### 1A. The 5 firm transparent-candidates (≈4 distinct structural problems, ONE difficulty class)

*Corrected 2026-07-17. The "reset structure" column was built on `min` over a **sparse
record-triggered subsample** (fault F2) — such a min is an **upper bound** on the true
per-generation minimum, never a floor. Only rows re-measured **dense stride-1** are supported;
the rest are marked `[UNSUPPORTED]` (= never established, NOT refuted).*

| # | transition table | register law (OBSERVED) | reset structure | why transparent | class |
|---|---|---|---|---|---|
| **B1 (primary)** | `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` | maxrun `v'=2v+2`, `v_k=2^k−2` exact (resid 0.000); pure binary shift, no bit-mixing | data-dependent 9/21/31 — dense re-measure **CONSISTENT** (true minima include 9 and 21) | register law **PROVEN** pure doubling; low-phase safety **PROVEN ∀g** (mechanized induction); halt gate PROVEN (B reads 1) | **TRANSPARENT** `[register law PROVEN; residual OPEN]` · cost ratio **3.97 = Θ(v²)** *(positive control: matches its independently-known Θ(4^k) TOPGRIND wall)* |
| **B2 (twin of B1)** | `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` | maxrun `v'=2v+2`, same `2^k−2` cascade (14,30,62,…,1022; ratios→2.004; resid 0.003) | (unprobed in detail) | cascade-identical to B1 → same base-2 odometer cascade. **NOT a TNF/mirror relabel of B1** (settled 2026-07-17: a relabel preserves step counts exactly; B1's cascade fires at 153443/597615/2318803/9212415, B2's at 157966/591922/2333374/9186082 — same values, different times) | **TRANSPARENT-candidate** `[OBSERVED]` · cost ratio **3.94 = Θ(v²)** |
| **B3 (pair A)** | `1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC` | total1 `v'=2v−28.5`; maxrun peaks **7·2^k EXACT** (447/448,895/896,1791/1792,3583/3584; `d_k≡0`); resid 0.004 | ~~arithmetic drain 26,22,18,14,10 (−4/gen)~~ **`[UNSUPPORTED]`** — a sparse-sample min (F2); never re-measured dense. An upper bound, not a floor. | exact geometric ×2 envelope with `d_k≡0` (no correction term). **The inference "cleaner envelope ⟹ cheaper core" is DEAD**: B3 pays the same Θ(v²) | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` · cost ratio **3.99 = Θ(v²)** |
| **B4 (pair B)** | `1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD` | total1 `v'=2v−28.5`; maxrun peaks **3·2^k EXACT** (383/384,767/768,1535/1536,3071/3072; `d_k≡0`); resid 0.005 | ~~identical drain 26,22,18,14,10,6~~ **`[UNSUPPORTED]`** — same F2 fault as B3 | ~~same as B3 (peak-identical pair) — one analysis covers both~~ **REFUTED 2026-07-17**: B3 peaks are `7·2^k`, B4's are `3·2^k`. **Not peak-identical on either observable**; step-times differ ~3×. They share only a *fit shape*. **Nothing shows one analysis covers both** | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` · cost ratio **3.98 = Θ(v²)** |
| **B5** | `1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD` | maxrun peaks **EXACT `v'=2v+1`** (17,35,71,143,287,575,1151 = 9·2^k−1). **Register is PHASE-CONDITIONED** — visible only in state C at a left-extent record; B5's *global* maxrun record is an arithmetic ramp (+3/record) and fails the `doubling_gate` | **CONSTANT 14** — **REAL**, dense stride-1 verified. But it is a **per-generation MINIMUM of full-tape maxrun**, a *different statistic* from the C-milestone floors `5·2^k+6`/`+8` (the value at the next state-C left-record after the peak). Both are true of different quantities; neither refutes the other. **No mechanism for 14 is re-derived** `[OPEN]` | ~~most rigid: exact affine doubling + constant reset (no digit read visible) → candidate *pure* linear odometer~~ **RETRACTED 2026-07-17.** B5 is **BRAID-BOUND**: per-doubling ratio **4.15** over k=1..8, four independent reproductions. The constant reset did **not** buy a cheaper core | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` · cost ratio **4.15 = Θ(v²)** — **BRAID-BOUND** |

**Pairing note — re-derived 2026-07-17, not inherited.** `59749fb` claimed *"5 firm candidates ≈ 3
distinct problems (B1/B2, B3/B4, B5)"*. That count rested on two asserted peak-identical pairs. Both
were re-tested:

- **B1/B2 — pairing SURVIVES.** Identical `2^k−2` cascade values across all 9 records; step-times
  differ. One structural problem, two genuinely distinct machines. `[OBSERVED]`
- **B3/B4 — pairing REFUTED.** `7·2^k` vs `3·2^k`. Two problems, not one.
- **B5 — a *difficulty-class* merge, not a *structural* merge.** B5 shares B1's cost signature, but
  its register law (`9·2^k−1` vs `2^k−2`) differs and its register is phase-conditioned where B1's is
  global. "Same difficulty class" is supported; **"same structural problem" is not**. B5 subtracts
  nothing from the structural count.

**The count went UP, not down:** **≈4 distinct structural problems — `{B1,B2}`, `{B3}`, `{B4}`,
`{B5}`** — in **ONE difficulty class** (all five pay Θ(v²) per doubling). The island is *less*
consolidated than claimed, and simultaneously *more* uniform in difficulty than anyone hoped.

### 1B. The watchlist (3 — 1 transparent-leaning, 2 UNCLEAR)

| # | transition table | probe finding | class | risk |
|---|---|---|---|---|
| **W1 (~13/7 recruit)** | `1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---` | ~~resets EXACTLY arithmetic +3/gen (24,27,…,39); peak ratio 1.878→1.977→2 → ×2 envelope + a linear secondary register~~ — **BOTH CLAIMS `[UNSUPPORTED]` 2026-07-17.** **W1 is not a doubler.** Its `total1` is an arithmetic ramp (records increment by ~1) and it sets **~1274 records in its top octave**, where a doubler sets O(1). Decisively: **W1's maxrun never exceeds 5** over 12 M steps — no long run ever forms, so there is no binary register to double. The `doubling_gate` **refuses** to report a ratio for it; that refusal is the only reason W1 is not in the braid table as a spurious "4". Its reset row rests on the same sparse-min fault (F2) as B3/B4. *"~13/7" was already known to be a transient artifact* | **UNCLEAR** `[OBSERVED]` *(was "TRANSPARENT-leaning" — that rested entirely on the ×2 envelope, which a correct full-tape instrument does not see)* | register unidentified. **W1 is neither decided nor refuted here — it needs a re-measure, not a ruling** |
| **W2** | `1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE` | period-2 doubling envelope (peaks pair 609/613, 1239/1237, 2495/2473) but corrections vary **non-affinely** (+21,+17,+43 / +4,−2,−22) | **UNCLEAR** `[OBSERVED]` · cost ratio **3.94 = Θ(v²)** | possible digit coupling → could eject to opaque |
| **W3** | `1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE` | mixed phases: alternate steps EXACT `d=+5`, others erratic and **value-proportional** (−11,−204,−693) — correction plausibly reads deep digits | **UNCLEAR (opaque-leaning)** `[OBSERVED]` | strongest ejection risk (value-proportional = digit read) |

**Island count (corrected 2026-07-17): 8 machines flagged** = 5 firm transparent-candidates
(**≈4 distinct structural problems: `{B1,B2}`, `{B3}`, `{B4}`, `{B5}` — in ONE difficulty class**)
+ 3 UNCLEAR (W1, W2, W3). This still matches the "~5–8" expectation and `CARRY_DICHOTOMY §6`'s
"~5-machine island". *(Superseding `59749fb`'s "≈3 distinct problems"; the B3/B4 pairing is refuted
and B5's merge is a difficulty merge, not a structural one. W1 moves from transparent-leaning to
UNCLEAR — its register is not a doubler.)*

**Honesty on how well-defined the island is.** The boundary is *sharp in principle* (transparent ⟺
`q=1` register-driven) but *empirically soft at the edges*. Only B1 has a certified milestone
reduction; B2–B5 rest on **observable-level probes** (total1/maxrun as register proxies over 12–60 M
steps, 4–5 consecutive exact doublings), NOT proofs of their laws. An exact envelope does **not**
preclude a hidden digit-coupled branch (`CARRY_DICHOTOMY §3` caveat ii — B1 itself has data-dependent
resets 9/21/31 yet is transparent because the *whole* low-region law is the explicit odometer). So
"transparent-candidate" for B2–B5 means "no opaque signal detected and an exact ×2 envelope observed,"
not "proven register-driven." W2/W3 may or may not be transparent once the right coordinates are found.

---

## 2. Per-machine reduction status and similarity to B1

### 2.0 The B1 template (the only worked reduction) — the thing to be transferred

B1's non-halt architecture, as built in `lean/X2.lean` and documented in `PAPER_X2_INTEGER_DOUBLER.md`:

```
x2_nonhalt (M1 M6 : Nat→Cfg) (h_init) (h_low) (h_doub)  : ∀N, steps N init ≠ none    -- [PROVEN, conditional]
    ⟸  nonhalt_of_segments   (infinite chain of nonempty halt-free segments ⟹ never halts)   -- [PROVEN, pure, machine-agnostic]
    per-generation cycle  M1(g) →* M1(g+1)  split as:
        h_low  : ∀g, M1(g) → M6(g)   (register setup / low phase)      -- [PROVEN ∀g in Python; small Lean port remaining]
        h_doub : ∀g, M6(g) → M1(g+1) (the base-2 doubling)             -- [OPEN], hinges on:
            carry_step  — the doubling-phase carry recursion            -- [OPEN], the single deep wall
    halt_gate : HALT ⟺ B reads 1                                       -- [PROVEN, from table]
```

Proven on-path primitives (`PAPER_X2 §4`): `sweepEF` (the `×2` repack `(01)^m→1^{2m}`, ∀m — the
generic doubling engine), `dSweepTurn` (block crossing), the odometer tick `outer_tick_noCarry_run`
(∀n), the depth-1 carry factored ENTRY∘CORE∘EXIT, the recursive register `cascadeTail`, the closed-form
tick/step counts. The **open core** is `carry_step`: the general-`j` doubling carry is a
**growing-arity digit-tree recursion** (fan-out `(k−5)(k−4)/2`, the triangular base-2 digit tree), a
**shrinking-comb quadratic braid** of length `Θ(2^{2K})` — a nested double-induction, NOT a linear
episode chain (`X2_STATUS_2026-07-12 §3`). Per the newest study
(`X2_UNIFIED_RECURSION_DESIGN_2026-07-16`), this recursion is now assessed **CONSTRUCTIBLE** as a
finite stratified well-founded recursion (two function types `regen`/`descentGlue`, one-directional
coupling, unified measure `k²+a`); the single remaining obligation is the `descentGlue`
transport-assembly (`Suffix.lean`-scale definitional threading), `[DESIGN]`-labelled, not yet proven.

So B1 status: **reduced two independent, cross-validated ways to one sharp invariant; low phase PROVEN
∀g; residual = the `carry_step` nested recursion, OPEN but characterized and assessed constructible.
NOT decided.**

### 2.1 B2 (twin) — status: peak-identical proxy only; expected near-verbatim transfer

No standalone milestone reduction sketched anywhere; the only evidence is the peak-identical `2^k−2`
cascade (`CANDIDATE_NEW §1`). Because it shares B1's exact register law and reset pattern class, its
milestone form and halt gate are expected to be B1's up to relabeling/mirroring. **Deciding it requires**
the same four objects (milestone form, halt gate, `h_low`, `h_doub` with a `carry_step`-analogue).
**Similarity to B1: maximal** — and its cost signature agrees (**3.94**, vs B1's 3.97).

**The genuineness check is DONE (2026-07-17) — B2 is a real, distinct machine.** A TNF/mirror
relabeling preserves step counts *exactly*. B1 and B2 have identical `2^k−2` cascade **values** across
all 9 records but **different step-times** (B1 `153443, 597615, 2318803, 9212415`; B2 `157966, 591922,
2333374, 9186082`). So B2 is **not** a duplicate of B1: two genuinely distinct machines with an
identical register law. One structural problem, and risk 5 (duplication) is **closed** for this pair.

*Caveat that must not be lost: B2's matching ratio 4 says its doubling costs Θ(v²). It does **not**
prove B2 hosts B1's growing-arity digit tree. Cost signature ≠ mechanism.*

### 2.2 B3 and B4 — status: exact-tail proxy; TWO problems, NOT a simpler core

*Rewritten 2026-07-17. This section previously nominated B3/B4 as "possibly SIMPLER core" and treated
them as one target. Both claims are corrected.*

No milestone reduction sketched for either. Observationally they remain **cleaner than B1**: peaks
are exactly `7·2^k` (B3) / `3·2^k` (B4) with `d_k≡0` — no correction term at all in the doubling
envelope. **`d_k≡0` and the clean envelopes are REAL and remain the island's cleanest observables.**

**What died is the *inference*, in two independent places:**

1. **"Cleaner envelope ⟹ cheaper core" is refuted by measurement.** The argument was: B1's
   data-dependent resets are what force its `carry_step` to be a growing-arity digit tree, so
   arithmetic-only resets should give a linear/bounded-arity odometer instead. **B3 and B4 pay
   `3.99` and `3.98` per doubling — the same Θ(v²) as B1's `3.97`.** They were the best remaining
   hope for a digit-read-free core after B5 fell; they are not cheaper.
2. **The pairing is refuted — B3 and B4 are TWO analyses, not one.** They are **not peak-identical**:
   B3's maxrun records are `7·2^k` (`447/448 … 3583/3584`), B4's are `3·2^k`
   (`383/384 … 3071/3072`), and their step-times differ ~3× on both observables. What they actually
   share is a **fit shape** (both fit `total1: v'=2v−28.5`) — a far weaker statement that must not be
   reported as identity. *"One analysis covers both"* is `[UNSUPPORTED]`.

Their **reset structure** (the "arithmetic −4/gen drain") is `[UNSUPPORTED]` — a `min` over a sparse
record-triggered subsample (F2), i.e. an upper bound, never established as a floor. It is **not
refuted**; it was never re-measured densely. That re-measure is now the prerequisite for any
structural claim about them.

**Deciding requires** the full B1 treatment, **twice**. Similarity: same `sweepEF` ×2 primitive; the
`carry_step`-analogue is **not** shown simpler — and, per the standing caveat, **not shown to be B1's
digit tree either**. Ratio 4 is a cost signature, not a mechanism.

### 2.3 B5 — status: **BRAID-BOUND**. The pure-odometer hypothesis is REFUTED by measurement.

*Rewritten 2026-07-17. This section previously nominated B5 as the single fastest win on the track —
"candidate pure odometer, possibly NO braid, independent of B1". **That is now settled negative.***

No milestone reduction sketched. The register law **`v'=2v+1` (`9·2^k−1`, k=1..8) is REAL** and
reproduced. Two corrections of substance:

**(a) The register is PHASE-CONDITIONED, and that matters.** B5's *global* maxrun record is an
arithmetic ramp (+3 per record, ~179 records in the top octave) and **fails the `doubling_gate`
outright**. Its doubling register is visible only in **state C at a left-extent record**. Read there,
with a tape-derived extent, the family `9·2^k−1` is exact. Reading any ratio off B5's *global* record
is the F3 artifact and must not be done.

**(b) B5 pays Θ(v²) per doubling — it is BRAID-BOUND.** First-attainment times of the register peaks:

```
peak      17        35        71       143       287       575
step   2,559    10,541    43,663   181,553   752,545  3,108,325
ratio      -     4.119     4.142     4.158     4.145     4.130      median 4.145
```

Not 2. **Four independent reproductions** — `885f6de` 4.10, coordinator 4.09, `TRACK_B_REAUDIT` 4.145,
`x2ti_island.py` 4.145 (an instrument sharing no code with the others). The `CANDIDATE_NEW §1b`
pure-orbit route — *a pure `v↦2v+c` orbit with a fixed-modulus gate is outright decidable, since
`2^k mod M` is eventually periodic* — remains **correct as a theorem**; B5 simply **is not such a
machine**. Its constant reset did not buy a cheaper core.

**The "CONSTANT 14" is REAL — and must not be "fixed" into a new error.** It is dense stride-1
verified (gens 1–3 reproduced here at `14,14,14`; gens 1–5 in `TRACK_B_REAUDIT`, out-of-sample at
gen 5). Two traps around it, both already sprung once:

- It is a **per-generation MINIMUM of full-tape maxrun**. The C-milestone floors `5·2^k+6`/`+8`
  (`6b6d739`) measure a **different statistic** — the value at the next state-C left-record milestone
  *after* the peak. **Both readings are true of different quantities; neither refutes the other.**
  `6b6d739` over-corrected 14 to "REFUTED / origin UNEXPLAINED" by comparing the two; `c65bad5`
  restored it. **Over-correction is a measurement error too.**
- The "half-tape bug made 14" lead is a **red herring**: 14's origin is `cd_probe2.py` →
  `mse_extract.simulate`, which maintains **both** bounds. Its extent was never truncated.

`885f6de`'s headline *mechanism* for 14 ("the k=2 tooth recurring verbatim") remains **`[OPEN]`** —
14 is a confirmed constant, but **no mechanism for it is established**, and none is asserted.

**Similarity to B1: same difficulty class, NOT shown to be the same structure.** B5's register law
(`9·2^k−1` vs `2^k−2`) differs and its register is phase-conditioned where B1's is global. Ratio 4
is a cost signature, not a mechanism: **nothing here shows B1's growing-arity digit tree lives in B5.**

### 2.4 W1 (~13/7) — status: UNCLEAR. **Not a doubler**; the ×2 envelope is `[UNSUPPORTED]`.

*Rewritten 2026-07-17.* This section previously read W1 as "a ×2 envelope with a linear secondary
register — B1's odometer plus one extra explicit affine register". **The ×2 envelope is not visible
to a correct full-tape instrument.**

What a tape-derived-extent measurement actually finds: W1's `total1` is an **arithmetic ramp** —
records increment by ~1, with ~1274 records in its top octave (a genuine doubler sets O(1) there).
Decisively, **W1's maxrun never exceeds 5** over 12 M steps: no long run ever forms, so **there is no
binary register to double**. This is exactly the failure mode `CANDIDATE_NEW` itself warned of —
*"the sawtooth's peak~√step gate passes spuriously on the transient startup of a plain linear
counter"*.

The `doubling_gate` **refuses** to report a cost ratio for W1. That refusal is load-bearing: a first
pass without it reported "W1: BRAID" at ratio ≈4, which was pure F3 artifact — *any* machine whose
cost ∝ width² returns 4 when you "double" an arbitrary observable. **No extent discipline would have
caught that; only the gate did.**

Its resets ("exactly arithmetic +3/gen") rest on the same sparse-min fault (F2) as B3/B4 and are
`[UNSUPPORTED]`.

**W1 is NOT decided and NOT refuted here — it needs a re-measure, not a ruling.** The prerequisite is
now prior: *identify W1's register at all* (if it has one), before any question about `d_k` drift or
transparency can be posed. It moves from **TRANSPARENT-leaning → UNCLEAR**.

### 2.5 W2, W3 — status: UNCLEAR, ejection risks (see §4)

No reduction. W2's non-affine period-2 corrections and W3's value-proportional corrections are the
signature of a **digit-coupled** branch. If confirmed, the carry is a function of the orbit's deep
digits — which, for a base-2 odometer, is a **base-2 return-frequency statement** (the ×2 sibling of
o15/o18's base-3 odometer conjectures; `CANDIDATE_NEW §1b`). That would be OPEN-and-gated-on-new-math —
NOT (K)/Mahler (q=1 degenerates it) but a *new* opaque schema. W3 is explicitly "opaque-leaning."

---

## 3. Templateability — how mechanically B1's architecture transfers

The B1 architecture decomposes into **three layers of decreasing transferability**:

**Layer 1 — the logical frame `x2_nonhalt` + `nonhalt_of_segments`: transfers for FREE.** This is
machine-agnostic: "an infinite chain of nonempty halt-free milestone segments ⟹ never halts," with the
per-generation cycle `h_low ∘ h_doub` composed by `steps_add`. It is already written as a *conditional*
theorem taking `M1, M6, h_init, h_low, h_doub` as hypotheses (the `Completion.lean` pattern). For any
island member one supplies its own `(M1, M6)` milestone families and the three transports; the frame
is reused verbatim. **Effort: ~0** (parameterize the existing theorem).

**Layer 2 — the halt gate + register-law + milestone form + `h_low`: transfers with per-machine work,
but of a routine, demonstrated kind.** Each member needs: (a) its halt gate (local, forced-predecessor
chase from the table — the easiest object, cf. the 17-named gate censuses in `PAPER_SPECIES_SURVEY §2`,
all small and saturating); (b) its milestone form M(g) (the deepest hand-step, but the B1 method —
`x2cc_decode.py`-style symbolic RLE + template match — is a reusable pipeline); (c) `h_low` via the
mechanized-induction prover (`x2cc_faith.py` pattern: certified cycle lemmas + exhaustive case-split +
loop-acceleration). The `sweepEF` `×2` repack primitive is **shared by construction** — every island
member is a base-2 doubler, so the `(01)^m→1^{2m}` comb-repack is the common engine. **Effort: moderate
per distinct structure (~1–2 focused sessions once the pipeline is warm), mechanical for the
peak-identical twins.**

**Layer 3 — `h_doub` / the `carry_step`-analogue: this is where a member can hit its own core.** B1's
`carry_step` is the growing-arity digit-tree braid, gated on the `descentGlue` transport-assembly.

*Corrected 2026-07-17: this section's first bullet — the "strictly easier (no braid)" outcome — was
the roadmap's central bet. **Measurement has emptied that bucket.*** Revised outcomes:

- **~~Strictly easier (no braid)~~ — NO MEMBER IS KNOWN TO BE IN THIS CLASS.** The bet was that
  register-forced resets (B5's constant 14, B3/B4's arithmetic −4 drain) would yield a
  *linear/bounded-arity odometer* decidable without the braid and independent of B1. **B5 measures
  4.15, B3 3.99, B4 3.98 — all Θ(v²).** The class is not *proven* empty, but **nothing is in it**,
  and the two best candidates are out.
- **Same COST, mechanism unknown (the honest replacement for "same braid").** Every island member
  with a genuine doubling register — **B1, B2, B3, B4, B5, W2** — pays Θ(v²) per doubling. For B2
  (identical register law to B1) a near-verbatim port of the `regen`/`descentGlue` stratified design
  (`X2_UNIFIED_RECURSION_DESIGN`) is *plausible*; for B3/B4/B5 (different laws, and B5's register
  phase-conditioned) it is **not established that the same object is even present**. **Ratio 4 is a
  cost signature, not a mechanism** — it says a doubling takes Θ(v) passes, not that those passes are
  B1's digit tree. These remain **gated on B1's braid closing first**; no template exists until it does.
- **Distinct/opaque core (ejects).** If the member's carry reads deep digits with a
  non-register-forced law — candidates **W2, W3** — it hits a *new* base-2 return-frequency conjecture
  and leaves Track B for a Track-C-like new-math gate.
- **Register not identified (new).** **W1** has no visible doubling register at all (maxrun ≤ 5). It
  cannot be placed in any of the above until that is resolved.

**Net templateability (corrected):** Layer 1 free, Layer 2 routine-but-real, Layer 3 the
discriminator — and Layer 3 now has **no known cheap side**. The island is **gated on B1 for every
member with a register**, with no register-forced shortcut identified.

---

## 4. The honest risks

1. **Track B has zero decided machines and its exemplar is undecided.** B1's `carry_step` is OPEN.
   The template *does not yet exist* — it is B1's own open core. If B1's braid does not close, the
   template transfer is vacuous. ~~Mitigant: the register-forced members (B5, B3/B4) may be decidable
   *independently* of B1.~~ **THE MITIGANT IS GONE (2026-07-17).** B5, B3 and B4 all pay Θ(v²) per
   doubling. **There is no known member decidable independently of B1**, so this risk is now
   unhedged and is the track's dominant risk.
2. **The reduction status of B2–B5 is OBSERVED-only.** Only B1 has a certified milestone reduction.
   Every "transparent-candidate" label rests on 4–5 exact doublings via observable proxies — a finite
   observation, NOT a proof of the law (`CARRY_DICHOTOMY §7`). Each needs the full B1 treatment
   (milestone form + value map + halt gate + faithfulness) before its class is firm.
3. **A clean ×2 envelope can hide a digit-coupled branch → silent ejection to opaque.** The sharpest
   Track-B-specific risk (`CARRY_DICHOTOMY §3` caveat ii, `CANDIDATE_NEW §1b`): even B3/B4/B5's exact
   envelopes could conceal a reset that reads deep digits, making the true invariant a **base-2
   return-frequency statement** — a *new* opaque schema (the ×2 sibling of the o15/o18 base-3 odometer
   conjectures). This would NOT be the (K)/Mahler wall (q=1 degenerates it) but would still be
   gated-on-new-math and would **eject the member from Track B**. W2 and especially W3 (value-proportional
   corrections) are the prime ejection candidates; B3/B4/B5 are lower-risk but not proven safe.
4. **Even a transparent residual can be `o4-wall-class` hard.** Transparency guarantees "no open
   *distribution*," not "easy." B1's residual defeated every uniform/local/parity/bounded-radius attack
   (`X2_FRONTIER_MAP §3`, `X2_STATUS_2026-07-12`). A member's `carry_step`-analogue can be a genuine
   nested recursion requiring `Suffix.lean`-scale formalization even when fully explicit.
5. ~~**Possible duplication.**~~ **CLOSED 2026-07-17 — and it resolved the OTHER way.** The
   genuineness checks are done. **B2 is NOT a TNF/mirror relabel of B1** (identical cascade values,
   different step-times — a relabel preserves step counts exactly), and **B3/B4 are NOT
   peak-identical** (`7·2^k` vs `3·2^k`). Rather than shrinking the distinct-problem count to ≈3,
   the checks **raised it to ≈4**: `{B1,B2}`, `{B3}`, `{B4}`, `{B5}`. There is no duplication to
   exploit.

6. **NEW — instrument risk is a first-class risk on this track.** Three distinct faults corrupted
   Track B evidence in one week: **F1** truncated extent (a caller-maintained `lo` with no matching
   `hi` → a half-tape scan); **F2** minima over sparse record-triggered samples (an upper bound read
   as a floor — this fault silently underwrites the *entire* "reset structure" column); **F3** a
   ratio of 4 read off a register that does not double (automatic for any width² machine). Mitigants
   that actually worked: *structural defence* — an API that takes only the tape, so F1 is
   inexpressible; *dense stride-1* for any min; *a gate that refuses to answer* outside its
   applicability. Mitigants that did not: vigilance. **And over-correction is a measurement error
   too** — `6b6d739` "refuted" a real result (B5's 14) by comparing two incommensurable statistics.

---

## 5. The Track B work-list (ordered, easiest first)

**REORDERED 2026-07-17.** The previous ordering front-loaded the members *"decidable independently of
B1"* (B5 at order 1 as "the fastest possible win", then B3/B4) — **the de-risking front. It does not
exist.** No member is known to be decidable without B1's braid. With the intrinsic-easiness axis
empty, only the **transfer** axis survives, and every entry on it is gated on order 0.

| order | target | why this order | shared template used | effort estimate | risk |
|---|---|---|---|---|---|
| **0 (prereq — now the ONLY unblocking move)** | close B1's `carry_step` (`descentGlue` transport-assembly) | with no braid-free member left, **every** other target is gated on this; owned by the X2.lean agent | — (this IS the template source) | multi-session (`Suffix.lean`-scale); assessed constructible | **the master gate for the entire track** |
| **1** | **B2** (twin of B1) | *(was order 3)* now the **best** target: identical `2^k−2` register law, matching cost signature (3.94 vs 3.97), genuineness **confirmed** (not a B1 relabel) | full B1 template incl. `carry_step`-analogue | small IF B1 closed (near-verbatim); else **blocked** | its `carry_step`-analogue is *plausibly* B1's, but **not established** — cost ≠ mechanism |
| **2** | **B3** (alone) | *(was half of order 2)* `d_k≡0` + exact `7·2^k` envelope remain the island's cleanest observables — but the "simpler core" inference is dead (ratio 3.99) | Layer 1 + Layer 2 pipeline (`sweepEF` shared); `h_doub` **not** known simpler | moderate — **one full analysis, covering B3 only** | prerequisite: **dense re-measure of its resets** (F2) |
| **3** | **B4** (alone — **NOT** 2-for-1 with B3) | *(was half of order 2)* pairing with B3 **refuted** (`3·2^k` vs `7·2^k`); needs its own analysis | as B3, separately | moderate — a **second** full analysis | same; the 2-for-1 saving is gone |
| **4** | **W1** (~13/7) | *(was "×2 + linear secondary register")* — **prerequisite is now prior:** identify whether W1 has a doubling register *at all* (maxrun ≤ 5 over 12 M steps) | (diagnosis only, until a register is found) | diagnosis session | its ×2 envelope is `[UNSUPPORTED]`; may not belong to the island |
| **5** | **W2** | period-2 non-affine corrections; classify transparent vs opaque before any proof. *(Note: W2 does have a doubling register and pays 3.94.)* | (diagnosis only) | diagnosis session | high ejection risk |
| **6** | **W3** | value-proportional (opaque-leaning); lowest transparency confidence | (diagnosis only) | diagnosis session | highest ejection risk |

**Cross-cutting prerequisite (new).** Before any structural claim is built on the "reset structure"
column, **dense stride-1 re-measurement** of B3/B4/W1's resets. Those rows are `[UNSUPPORTED]` — a
`min` over a sparse subsample is an upper bound. This is cheap and it gates orders 2–4.

**Shared template (the reusable spine for every order ≥1):**
1. Halt gate from the table (forced-predecessor chase) — routine.
2. Milestone form M(g) via symbolic-RLE decode (`x2cc_decode`/`x2cc_symb` pipeline).
3. `h_low` (∀g) via the mechanized-induction prover (`x2cc_faith` pipeline; certified cycle lemmas +
   case-split + loop-acceleration).
4. `h_doub` (∀g) — the discriminator: ~~*linear/bounded odometer* (no braid)~~ **[no member known to
   be in this class]** OR *a Θ(v²) core, plausibly B1's `carry_step` braid but **not established** for
   any machine but B1* (orders 1–3) OR *ejection to a new base-2 schema* (orders 5–6).
5. Assemble via the machine-agnostic `x2_nonhalt` / `nonhalt_of_segments` frame (free).

**Strategic note — REWRITTEN 2026-07-17.** The previous note read: *"Orders 1–2 (B5, B3/B4) are the
de-risking front: they can be decided — if truly register-forced — without waiting on B1's braid, and
would be the first actual Track B decisions."* **There is no de-risking front.** B5 was measured
braid-bound (4.15) and B3/B4 pay the same 4. Every remaining target is gated on order 0 — B1's
`carry_step`. Orders 1–3 are the *template-transfer* front, all downstream of B1; orders 4–6 are
*triage* (does the machine belong to Track B at all — now including W1). **The track's whole value
now rides on closing B1's braid**; nothing on the island de-risks that.

**What this does NOT license.** The island is *not* shown to be one problem. Ratio 4 is a **cost
signature, not a mechanism** — it does not prove B1's growing-arity digit tree lives in B2–B5, and
for any width² machine a doubled observable gives 4 for free. B3/B4's `d_k≡0` and clean envelopes
remain **real** and remain the island's best observables; what died is the *inference* from "cleaner
envelope" to "cheaper core". **No machine here is decided, and no label is upgraded or downgraded —
that is the owner's call.**

---

## 6. Report summary

*Corrected 2026-07-17.*

- **Island size: 8 flagged machines** = 5 firm transparent-candidates (B1 primary + B2 twin + B3 + B4
  + B5) resolving to **≈4 distinct structural problems** — `{B1,B2}`, `{B3}`, `{B4}`, `{B5}` — in
  **ONE difficulty class**, + 3 UNCLEAR (W1, W2, W3). Named cryptids in the island: 0.
  *(The count went UP from `59749fb`'s ≈3: the B3/B4 pairing is refuted, B1/B2's survives, and B5's
  is a difficulty merge, not a structural one. W1 moves to UNCLEAR — not a doubler.)*
- **Easiest: ~~B5, then B3/B4~~ — NO MEMBER IS DECIDABLE INDEPENDENTLY OF B1.** Every island member
  with a genuine doubling register pays **Θ(v²) per doubling**: B1 3.97 *(control)*, B2 3.94,
  B3 3.99, B4 3.98, **B5 4.15**, W2 3.94. **Not one ratio-2 machine was found.** B5 — the nominated
  "fastest possible win", the pure-odometer candidate — is **BRAID-BOUND** (four independent
  reproductions). B3/B4, the best remaining hope for a digit-read-free core, pay the same 4.
  **Track B's founding premise — that a friendlier transparent machine dodges B1's braid — has no
  surviving support.** The transparent island is not a set of easier problems; it is B1's difficulty,
  repeated. **B2** is now the best target, but is gated on B1's `carry_step` closing — as is
  everything else.
- **The two caveats on that verdict.** (i) **Ratio 4 is a cost signature, not a mechanism**: it shows
  a doubling costs Θ(v) passes, **not** that B1's growing-arity digit tree lives in B2–B5. No
  mechanism is asserted for any machine but B1. (ii) For **any** machine whose cost ∝ width²,
  doubling an observable yields 4× automatically — a **`doubling_gate`** (refuse to answer where the
  register does not double) is what kept W1 out of that table, and its absence manufactured a
  spurious "W1: BRAID".
- **What survives untouched:** B3/B4's `d_k≡0` and exact `7·2^k`/`3·2^k` envelopes; B5's `9·2^k−1`
  register law and its **real, dense-verified CONSTANT 14** (a per-generation *minimum* — a different
  statistic from the C-milestone floors `5·2^k+6`/`+8`; both true, neither refuting the other; **no
  mechanism for 14 established** `[OPEN]`). The `[OBSERVED]` labels for B2–B5 survive on extent —
  their instrument was never truncated.
- **What is `[UNSUPPORTED]` (never established — NOT refuted):** the reset rows for **B3, B4, W1**
  (sparse-sample minima = upper bounds, never re-measured dense), and **W1's ×2 envelope**.
- **Shared template:** the machine-agnostic `x2_nonhalt`/`nonhalt_of_segments` frame (free) + the
  shared `sweepEF` ×2 repack primitive + the per-machine {halt gate, milestone decode, `h_low`
  mechanized induction, `h_doub`}. The frame and low-phase pipeline transfer mechanically; `h_doub` is
  the discriminator (linear odometer / B1 braid / ejection).
- **Honest risks:** (1) **B1 itself is undecided, and this risk is now UNHEDGED** — no member is
  decidable independently of B1, so every transfer waits on `carry_step`; (2) B2–B5 are OBSERVED-only,
  not certified reductions; (3) a clean ×2 envelope can hide a digit-coupled branch that ejects a
  member to a *new* base-2 return-frequency (opaque) conjecture — W3 (value-proportional) and W2 are
  the prime ejection risks, B3/B4/B5 lower but unproven; (4) transparency ≠ easy (residuals can be
  o4-wall-class hard) — **today this stopped being a caveat and became the finding**; (5) ~~possible
  duplication~~ **CLOSED, and it went the other way** — B2 is not a B1 relabel, B3/B4 are not
  peak-identical, so the count rose to ≈4; (6) **NEW — instrument risk is first-class here**: three
  faults in one week (F1 truncated extent, F2 sparse-sample minima, F3 an ungated ratio). Structural
  defences work (an API that takes only the tape; dense stride-1 for any min; a gate that refuses to
  answer); vigilance does not. **Over-correction is a measurement error too.**

**No machine decided. No label upgraded.**

---

*Corrections of 2026-07-17 are grounded in `TRACK_B_REAUDIT_2026-07-17.md` and
`B5_INVESTIGATION_2026-07-16.md` (commits `885f6de` / `6b6d739` / `c65bad5`), and every load-bearing
number above was **independently re-reproduced** before being written here by `x2ti_island.py` — an
instrument sharing no code with `x2tb_*`, `x2b5_*`, `mse_extract` or `cd_probe`: B1/B2 cascade values
and step-times, B3 `7·2^k` vs B4 `3·2^k`, B5's `9·2^k−1` first-attainment ratios
(4.119/4.142/4.158/4.145/4.130, median **4.145**), B5's dense stride-1 floor **14** at gens 1–3, W1's
maxrun ≤ 5 and its gate failure, and the full ratio table. No Lean file was edited.*
