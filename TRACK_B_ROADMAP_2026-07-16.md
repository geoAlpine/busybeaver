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

### 1A. The 5 firm transparent-candidates (≈5 distinct; two peak-identical pairs)

| # | transition table | register law (OBSERVED) | reset structure | why transparent | class |
|---|---|---|---|---|---|
| **B1 (primary)** | `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` | maxrun `v'=2v+2`, `v_k=2^k−2` exact (resid 0.000); pure binary shift, no bit-mixing | data-dependent 9/21/31 | register law **PROVEN** pure doubling; low-phase safety **PROVEN ∀g** (mechanized induction); halt gate PROVEN (B reads 1) | **TRANSPARENT** `[register law PROVEN; residual OPEN]` |
| **B2 (twin of B1)** | `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` | maxrun `v'=2v+2`, same `2^k−2` cascade (14,30,62,…,1022; ratios→2.004; resid 0.003) | (unprobed in detail) | peak-identical to B1 → same base-2 odometer cascade; "TNF-adjacent" to B1 | **TRANSPARENT-candidate** `[OBSERVED]` |
| **B3 (pair A)** | `1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC` | total1 `v'=2v−28.5`; maxrun peaks **7·2^k EXACT** (224,448,896,1792,3584; `d_k≡0`); resid 0.004 | arithmetic drain 26,22,18,14,10 (**−4/gen**), rigid super-cycle refill | exact geometric ×2 envelope with `d_k≡0` (no correction term); arithmetic (register-driven) resets | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` |
| **B4 (pair B)** | `1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD` | total1 `v'=2v−28.5`; maxrun peaks **3·2^k EXACT** (96,…,3072; `d_k≡0`); resid 0.005 | **identical** drain 26,22,18,14,10,6 (−4/gen) | same as B3 (peak-identical pair) — one analysis covers both | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` |
| **B5** | `1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD` | maxrun peaks **EXACT `v'=2v+1`** (71,143,287,575,1151 = 9·2^k−1) | **CONSTANT 14** | most rigid: exact affine doubling + constant reset (no digit read visible) → candidate *pure* linear odometer | **TRANSPARENT-candidate** `[OBSERVED, exact tail]` (noisier fit resid 1.23) |

Pairing note (`CANDIDATE_NEW §1`): B1≡B2 are peak-identical (likely one structure / mirror /
TNF-adjacent); B3≡B4 are peak-identical. So the 5 firm candidates are **≈3 distinct structural
problems** (B1/B2, B3/B4, B5), which is why `CANDIDATE_NEW` reports "≈5–7 genuine, ≈5 distinct."

### 1B. The watchlist (3 — 1 transparent-leaning, 2 UNCLEAR)

| # | transition table | probe finding | class | risk |
|---|---|---|---|---|
| **W1 (~13/7 recruit)** | `1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---` | resets **EXACTLY arithmetic +3/gen** (24,27,…,39); peak ratio 1.878→1.977→2 (→×2 envelope + a linear secondary register); "~13/7" was a transient artifact | **TRANSPARENT-leaning UNCLEAR** `[OBSERVED]` | `d_k` drift ≈−3k with residual noise not yet pinned |
| **W2** | `1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE` | period-2 doubling envelope (peaks pair 609/613, 1239/1237, 2495/2473) but corrections vary **non-affinely** (+21,+17,+43 / +4,−2,−22) | **UNCLEAR** `[OBSERVED]` | possible digit coupling → could eject to opaque |
| **W3** | `1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE` | mixed phases: alternate steps EXACT `d=+5`, others erratic and **value-proportional** (−11,−204,−693) — correction plausibly reads deep digits | **UNCLEAR (opaque-leaning)** `[OBSERVED]` | strongest ejection risk (value-proportional = digit read) |

**Island count: 8 machines flagged** = 5 firm transparent-candidates (≈3 distinct problems: B1/B2,
B3/B4, B5) + 1 transparent-leaning (W1) + 2 UNCLEAR (W2, W3). This matches the "~5–8" expectation and
`CARRY_DICHOTOMY §6`'s "~5-machine island (5 candidates + up to 3 more pending)."

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
**Similarity to B1: maximal** — likely the *same* shrinking-comb quadratic braid. First action must be
a genuineness check (confirm B2 is not literally B1 under a TNF/mirror normalization, i.e. not a
duplicate of an already-listed machine).

### 2.2 B3/B4 (pair A/B) — status: exact-tail proxy; possibly SIMPLER core

No milestone reduction sketched. Observationally **cleaner than B1**: peaks are `7·2^k` / `3·2^k` with
`d_k≡0` (no correction term at all in the doubling envelope) and resets are **arithmetic −4/gen**, i.e.
a register-driven drain rather than B1's data-dependent 9/21/31. **This is the key structural
difference:** B1's data-dependent resets are precisely what force its `carry_step` to be a *growing-arity
digit tree* (the reset reads digits). If B3/B4's resets are genuinely arithmetic-only (no digit read),
their doubling-phase carry could be a **simpler recursion — a linear/bounded-arity odometer, not the
triangular braid.** `CARRY_DICHOTOMY §6` states their laws are "*more* rigid than the primary's," so if
the B1 calculus works it "should sweep machines 2–5." **Deciding requires** the full B1 treatment;
**similarity: same `sweepEF` ×2 primitive, plausibly a strictly simpler `carry_step`.** One analysis
covers both B3 and B4 (peak-identical).

### 2.3 B5 — status: most rigid; candidate *pure* odometer, possibly NO braid

No milestone reduction sketched. Exact `v'=2v+1` (`9·2^k−1`) with **CONSTANT reset 14** — the most
rigid observed. Per `CANDIDATE_NEW §1b`, a machine whose register is a *pure* deterministic `v↦2v+c`
orbit with a fixed-modulus gate is **outright DECIDABLE** (the gate `2^k≡r mod M` is eventually
periodic — `2^k mod M` is computable and periodic), *without any braid at all*. B5's constant reset is
the strongest signal of this pure-orbit structure. **If B5 is a pure `v↦2v+c` orbit with a modular halt
gate, it is strictly easier than B1 and INDEPENDENT of B1's `carry_step` closing** — a linear-odometer
decision. **Risk:** the fit was noisier (resid 1.23), and a constant reset can still hide a digit-read
that happens to be constant on the observed range; must verify the reset is register-forced, not
data-coincidental. **Similarity: potentially the *degenerate* case of B1 (no digit tree).**

### 2.4 W1 (~13/7) — status: ×2 + explicit linear secondary register

Resets **exactly arithmetic +3/gen** and peak ratio monotone →2: a ×2 envelope with a *linear*
secondary register. Structurally this is "B1's odometer + one extra explicit affine register," which
is *more* structure than B1 but still explicit. **Deciding requires** pinning the `d_k≈−3k` drift's
residual noise (is it register-forced or a digit read?). If register-forced, W1 is transparent with a
two-register odometer core — comparable to B1, possibly needing its own (but explicit) recursion.

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
`carry_step` is the growing-arity digit-tree braid, gated on the `descentGlue` transport-assembly. Three
outcomes per member:
- **Strictly easier (no braid).** If the member's resets are register-forced (arithmetic/constant, no
  digit read) — candidates **B5** (constant reset), possibly **B3/B4** (arithmetic −4 drain) — the
  doubling carry may be a *linear/bounded-arity odometer* with a modular halt gate, decidable *without*
  the quadratic braid, and *independent of B1's `carry_step`*. These would be the **fastest wins** and
  do not wait on B1.
- **Same braid (template transfers if B1 closes).** If the member's reset is data-dependent like B1's —
  candidate **B2** (twin) and possibly **W1** — its `carry_step`-analogue is the *same* shrinking-comb
  digit-tree recursion. The B1 `regen`/`descentGlue` stratified-recursion design
  (`X2_UNIFIED_RECURSION_DESIGN`) should port with re-grounded constants. **These are gated on B1's
  braid closing first** — no template exists to transfer until it does.
- **Distinct/opaque core (ejects).** If the member's carry reads deep digits with a
  non-register-forced law — candidates **W2, W3** — it hits a *new* base-2 return-frequency conjecture
  and leaves Track B for a Track-C-like new-math gate.

**Net templateability:** Layer 1 free, Layer 2 routine-but-real, Layer 3 the discriminator. The island
is **template-friendly for the register-forced members and gated-on-B1 for the digit-dependent ones**.

---

## 4. The honest risks

1. **Track B has zero decided machines and its exemplar is undecided.** B1's `carry_step` is OPEN.
   For the "same braid" members (B2, W1), the template *does not yet exist* — it is B1's own open core.
   If B1's braid does not close, the template transfer for those members is vacuous. Mitigant: the
   register-forced members (B5, B3/B4) may be decidable *independently* of B1.
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
5. **Possible duplication.** B2 is "TNF-adjacent" to B1 and the pairs are peak-identical; some island
   "members" may be the same machine under mirror/TNF normalization, shrinking the true distinct-problem
   count below 5 (to ≈3). First action per twin: a genuineness/normalization check.

---

## 5. The Track B work-list (ordered, easiest first)

Two orthogonal notions of "easy": (i) **intrinsic** (decidable without B1's braid) and (ii)
**transfer** (closest to B1). The ordering below front-loads the members that are *decidable
independently of B1* (de-risking the track), then the template transfers.

| order | target | why this order | shared template used | effort estimate | risk |
|---|---|---|---|---|---|
| **0 (prereq/parallel)** | close B1's `carry_step` (`descentGlue` transport-assembly) | unblocks the "same braid" transfers; owned by the X2.lean agent | — (this IS the template source) | multi-session (`Suffix.lean`-scale); assessed constructible | the master gate for B2/W1 |
| **1** | **B5** — test the *pure-odometer* hypothesis | most rigid (constant reset); if a pure `v↦2v+c` orbit with modular gate, **decidable with no braid, independent of B1** | Layer 1 frame + a *linear* odometer `h_doub` (not the braid); halt gate `2^k≡r mod M` | small–moderate IF pure-orbit confirmed; the fastest possible win | may hide a constant-looking digit read (risk 3) |
| **2** | **B3 + B4** (pair A/B, one analysis) | arithmetic −4 reset drain + `d_k≡0`; candidate register-forced ⟹ simpler-than-B1 carry; peak-identical so 2-for-1 | Layer 1 + Layer 2 pipeline (`sweepEF` shared); `h_doub` a bounded/linear-arity odometer | moderate (1 milestone analysis for both) | reset could be digit-coupled (risk 3) |
| **3** | **B2** (twin of B1) | maximal template reuse — same `2^k−2` cascade; but gated on B1's braid | full B1 template incl. `carry_step`-analogue (same braid) | small IF B1 closed (near-verbatim); else blocked | genuineness/duplication check first (risk 5) |
| **4** | **W1** (~13/7) | ×2 + explicit *linear* secondary register; more structure than B1 but explicit | B1 frame + a two-register odometer core | moderate–large; pin the `d_k≈−3k` residual first | drift residual may be digit-read (risk 3) |
| **5** | **W2** | period-2 non-affine corrections; classify transparent vs opaque before any proof | (diagnosis only) | diagnosis session | high ejection risk |
| **6** | **W3** | value-proportional (opaque-leaning); lowest transparency confidence | (diagnosis only) | diagnosis session | highest ejection risk |

**Shared template (the reusable spine for every order ≥1):**
1. Halt gate from the table (forced-predecessor chase) — routine.
2. Milestone form M(g) via symbolic-RLE decode (`x2cc_decode`/`x2cc_symb` pipeline).
3. `h_low` (∀g) via the mechanized-induction prover (`x2cc_faith` pipeline; certified cycle lemmas +
   case-split + loop-acceleration).
4. `h_doub` (∀g) — the discriminator: *linear/bounded odometer* (orders 1–2, no braid) OR *the B1
   `carry_step` braid* (orders 3–4) OR *ejection to a new base-2 schema* (orders 5–6).
5. Assemble via the machine-agnostic `x2_nonhalt` / `nonhalt_of_segments` frame (free).

**Strategic note.** Orders 1–2 (B5, B3/B4) are the *de-risking* front: they can be decided — if truly
register-forced — *without waiting on B1's braid*, and would be the first actual Track B decisions.
Orders 3–4 (B2, W1) are the *template-transfer* front, gated on B1. Orders 5–6 are *triage*: decide
whether they belong to Track B at all before spending proof effort.

---

## 6. Report summary

- **Island size: 8 flagged machines** = 5 firm transparent-candidates (B1 primary + B2 twin + B3/B4
  pair + B5) reducing to **≈3 distinct structural problems** (B1/B2, B3/B4, B5, since the pairs are
  peak-identical), + 1 transparent-leaning (W1, ~13/7), + 2 UNCLEAR (W2, W3). Named cryptids in the
  island: 0.
- **Easiest:** **B5** (constant reset 14 → candidate *pure* `v↦2v+c` odometer, potentially decidable
  with no braid and independent of B1), then **B3/B4** (arithmetic −4 drain, `d_k≡0`, one analysis for
  two machines, plausibly simpler-than-B1 core). These are the de-risking front. **B2** (twin) is the
  easiest *template transfer* but is gated on B1's `carry_step` closing.
- **Shared template:** the machine-agnostic `x2_nonhalt`/`nonhalt_of_segments` frame (free) + the
  shared `sweepEF` ×2 repack primitive + the per-machine {halt gate, milestone decode, `h_low`
  mechanized induction, `h_doub`}. The frame and low-phase pipeline transfer mechanically; `h_doub` is
  the discriminator (linear odometer / B1 braid / ejection).
- **Honest risks:** (1) B1 itself is undecided — the "same-braid" transfers (B2, W1) have no template
  until B1's `carry_step` closes; (2) B2–B5 are OBSERVED-only, not certified reductions; (3) a clean ×2
  envelope can hide a digit-coupled branch that ejects a member to a *new* base-2 return-frequency
  (opaque) conjecture — W3 (value-proportional) and W2 are the prime ejection risks, B3/B4/B5 lower but
  unproven; (4) transparency ≠ easy (residuals can be o4-wall-class hard); (5) possible duplication —
  peak-identical/TNF-adjacent members may collapse the distinct count to ≈3.

**No machine decided. No label upgraded.**
