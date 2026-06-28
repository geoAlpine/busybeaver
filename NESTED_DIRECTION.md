# What determines the HALTING DIRECTION of a nested-Collatz BB(6) machine (2026-06-29)

*The direction question for the nested-Collatz class: why does o10 lean HALT while o13 leans NON-HALT?
This note pins the per-epoch halt condition for o10 and o13 side by side, formulates the general
direction principle as a Borel–Cantelli over the OUTER refill orbit (convergent ⇒ non-halt vs divergent ⇒
halt), classifies the whole class {o2,o7,o8,o10,o11,o12,o13,o14,o16} by heuristic direction, and decides
whether the o10-vs-o13 difference is structural or a small-sample artifact.*

**Soundness paramount.** Labels `[PROVEN]` (elementary/unit-tested vs raw TM) / `[VERIFIED]` (machine-checked
this program, exact big-int, bb_sim-cross-checked) / `[OBSERVED]` (numeric/heuristic) / `[HEURISTIC]`
(ensemble model, NOT a proof) / `[OPEN]`. **NO machine is decided. NO halting direction is claimed.** All
new numerics this session use `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` with bb_sim step semantics.
Sources: `O10_REDUCTION.md`, `O10_HALTER.md`, `REDUCE_O11_O16.md`, `REDUCE_O2_O7_O8.md`,
`MAHLER_3_2_DOMINANCE.md`, `BB6_STRUCTURAL_LIMIT_THEOREM.md`, `CATALOGUE_O13_SN.md`.

---

## 0. Headline

> **The halting direction of a nested-Collatz machine is governed by the SCALING of the per-epoch
> halt-probability along the OUTER refill orbit — equivalently a Borel–Cantelli dichotomy:**
> - **divergent side** (per-epoch halt-prob ≈ const > 0, `Σ p_e = ∞`) ⇒ **HALT-leaning** — *o10*;
> - **convergent side** (per-epoch halt-prob → 0 fast / thin target, `Σ p_e < ∞`) ⇒ **NON-HALT-leaning** —
>   the `00`-gap / phase-race machines o2,o7,o8,o11,o12,o14,o16.
>
> **The inner ×3/2 orbit does NOT decide direction.** In EVERY nested machine the inner eat-sweep is
> *always safe by parity* (o10 inner eat always EVEN ≠ its ODD halt target; o13 inner runs always ODD ≠ its
> EVEN halt target). The inner all-odd / all-even fact is a **shared "safe-inner" feature, not the
> discriminator** — halting lives entirely at the OUTER reconfiguration.
>
> **Is the o10(~1/3)-vs-o13(~0) gap structural? NO — not established.** It is presently a **confounded /
> small-sample** comparison: o10's ~1/3 is an *extracted abstract outer-epoch* halt-probability; o13's "~0"
> is only the *inner-sweep* observation (all-odd), which is the always-safe-inner fact o10 shares. o13's
> outer-epoch halt-probability has **not been extracted** (its outer model is not cleanly separable), so the
> direction-determining quantity for o13 is **unknown**. o13's true direction is `[OPEN]` and could even be
> halt-leaning like o10 if its per-outer-collapse even-run probability turns out constant.

---

## 1. The per-epoch halt condition, o10 vs o13, side by side

Both machines are leftward "eat-sweep" cryptids whose halt is the parity of the run consumed by the sweep —
the **exact same mechanic with opposite parity**. (o10 halt = F reads 0; o13 halt = E reads 0.)

| | **o10** `1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` | **o13** `1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA` |
|---|---|---|
| sweep | C/F leftward eat-sweep (`C:1→0LF`, `F:1→0LC`, `F:0→HALT`, `C:0→1LD`) | D/E leftward eat-sweep (`D:1→1LE`, `E:1→0LD`, `E:0→HALT`, `D:0→0RA`) |
| **HALT-MECHANIC** | **HALT ⟺ eat-sweep consumes an ODD-length 1-run** `[PROVEN, unit-tested]` | **HALT ⟺ eat-sweep consumes an EVEN-length 1-run** `[PROVEN, unit-tested]` |
| inner ×3/2 engine | `m → ⌈3m/2⌉` (literal AEV ceiling); countdown `b → b−(1+[m odd])` | inner `a`-orbit ratios → 3/2 (floor, nested, sea-coupled) |
| **inner eat length** | **`L = 2m − 8`, ALWAYS EVEN** ⇒ never the ODD halt target | **inner runs ALWAYS ODD** (7214/7214 sweeps, 50M steps) ⇒ never the EVEN halt target |
| ⇒ inner loop | **never halts** `[PROVEN]` (eat even, target odd) | **never halts** `[VERIFIED]` (eat odd, target even) |
| **per-epoch halt event** | epoch's b-countdown **lands EXACTLY on `b=0` at ODD `m`** `[PROVEN]` (base rule `b=0`:m odd / `b=1`:m≡2(4) / `b=2`:m≡3(4) / `b≥3`:never) | an **OUTER collapse produces an EVEN-length run** for the D/E sweep `[PROVEN mechanic + VERIFIED inner]` |
| outer refill orbit | `B: 5 → 57 → 2.1×10⁸ → …` (doubly-exp, piecewise-affine `R`) `[VERIFIED]` | `3,6,10,64,…` (doubly-exp, sea-countdown, NOT cleanly separable) `[VERIFIED]` |

**This session's grounding `[VERIFIED]`** (bb_sim step semantics, `scratchpad/dir_check.py`):
- o10 crafted eat-sweep over a length-`L` run: HALT for `L∈{1,3,5,7,9}`, EXIT for `L∈{0,2,4,6,8,10}` — clean
  **HALT ⟺ L odd**, reproducing `O10_REDUCTION.md` exactly.
- o13 crafted eat-sweep: my *ad-hoc* entry construction gave a **mixed** result (HALT at L=1,3,4,5,7,9,10) —
  i.e. my hand-built entry context was **unfaithful** (unnatural-right-context multi-step artifacts, exactly
  the `REDUCE_O2_O7_O8.md` §5 retraction lesson). I therefore do **NOT** assert the o13 parity from my own
  test; o13's "HALT ⟺ L even" is the **doc's unit-tested `[PROVEN]` result** (`REDUCE_O11_O16.md` §1, crafted
  blocks halt in `L+2` steps for `L∈{0,2,…,10}`, clean exit for odd). The failed reconstruction *reinforces*
  the core finding: only bb_sim-faithful constructions count, and the entry context — i.e. the OUTER state —
  is what sets the realized run, not the inner.
- Both machines run 2·10⁶ steps from blank without halting (o10: 1418 ones; o13: 1448 ones).

**The exact symmetry.** o10 and o13 are mirror eat-sweeps: same loop shape, opposite halt parity, and **each
has a parity-incompatible inner** (o10: inner-even vs target-odd; o13: inner-odd vs target-even). So for BOTH,
**the inner can never halt and the entire halting story is an OUTER event** — for o10 the b-underflow landing,
for o13 an even-run produced at an outer collapse. The "o10 always-even inner / o13 always-odd inner"
contrast is **not** a direction signal; it is the *same* safe-inner phenomenon in two parities.

---

## 2. The direction question: ~1/3 vs ~0 — structural or small-sample?

### 2.1 What "~1/3" and "~0" actually measure (they are NOT comparable as stated)

- **o10's ~1/3 is an OUTER quantity.** `O10_REDUCTION.md`/`O10_HALTER.md` extract a *clean abstract
  outer-epoch model* `epoch(B)` (inner `m→⌈3m/2⌉`, countdown `b→b−(1+[m odd])`, refill map `R`,
  bb_sim-cross-checked 0 mismatch B=1..16). The per-epoch halt fraction is `[HEURISTIC]` **33.67% over
  B=1..3000** — an *ensemble (annealed)* statistic of the OUTER refill values.
- **o13's "~0" is an INNER quantity.** The only o13 measurement is **7214/7214 inner eat-sweeps had ODD
  length** (= the always-safe-inner fact). **That is the analog of o10's "L=2m−8 always even" — also "0"
  inner halts for o10.** It is NOT o13's per-outer-collapse halt probability; that was never computed.

So "o10 ~1/3 vs o13 ~0" compares **o10's outer halt-prob against o13's inner safe-rate** — apples to oranges.
For o10 the matching *inner* number is also 0 (no inner eat is ever odd); for o13 the matching *outer* number
is **un-measured**.

### 2.2 Why o13's outer number is missing (reachability)

`REDUCE_O11_O16.md` §6: *unlike o10, o13 admits no cleanly extractable abstract outer-epoch model* — its outer
reconfigurations are sea-/δ-coupled, not reduced to a clean piecewise-affine map. And only **≈4 outer epochs
are reachable** (refill `3,6,10,64,…` is doubly-exp; the next collapse is `≳10¹³` steps away). So the
question "does some outer collapse ever produce an even run" is the **doubly-exponential existence question**,
unreached by simulation and **not** estimated by any extracted model.

### 2.3 Verdict on #2

> **The o10-vs-o13 difference is NOT established as structural.** `[OPEN]`. It is, at present:
> 1. **confounded** — o10's extracted OUTER halt-prob (~1/3) compared against o13's INNER safe-rate (the
>    always-safe-inner fact o10 *also* has); the matching outer quantity for o13 is un-extracted;
> 2. **small-sample** — only ≈4 o13 outer epochs are reachable; the even-run existence is doubly-exp-sparse.
>
> To upgrade "o13 leans non-halt" to structural one would need EITHER (a) a proof that o13's outer collapses
> are **structurally odd-only** (the analog of o10's provable `L=2m−8` even — **NOT established**), OR (b)
> o13's abstract outer model extracted and its per-collapse even-run probability computed and shown to **decay
> to 0** (convergent BC — **NOT done**). Neither exists. So o13's direction is genuinely `[OPEN]`, and the
> claim "o13 leans non-halt" rests only on the inner all-odd observation, which does **not** bear on the
> outer halt event.

**Caveat in o10's own favor (soundness).** Even o10's ~1/3 is `[HEURISTIC]` and `[OPEN]` as a *decision*:
it is an *ensemble* statement (B drawn at random); the *single deterministic* refill orbit `B:5→57→…` has
epochs 1–2 **both non-halting** (`[VERIFIED]`, consistent with the ≥40M-step holdout), epoch 3 infeasible,
and **Borel–Cantelli II cannot be applied** (needs independence a single orbit lacks — `O10_HALTER.md`
`[PROVEN negative]`). So o10 is HALT-*leaning* heuristically, **not decided**.

---

## 3. The general direction principle: a Borel–Cantelli over the OUTER refill orbit

For a nested-Collatz machine the structure is always: a clean inner ×3/2 engine that is **parity-safe**
(its eat/run never matches the halt target), wrapped in an **outer refill orbit** `B_1, B_2, …` that restarts
the inner engine each epoch. Halting can occur **only** at an outer reconfiguration. Hence:

> **(DIRECTION PRINCIPLE).** A nested-Collatz machine **halts ⟺ SOME outer epoch `e` realizes the
> halt-triggering inner parity/alignment** (o10: countdown lands `b=0` at odd m; o13: collapse eats an even
> run; o2/o7/o8/o11/o12/o14: a `00`-gap opens at the sweep frontier; o16: an F-phase `0` beats the E-phase
> exit). It **never halts ⟺ the outer orbit AVOIDS the halt target forever.** This is a hitting/avoidance
> (Π⁰₁ existence) event over the deterministic outer orbit `{B_e}`.

Define `p_e` = (heuristic) probability that epoch `e` realizes the halt target, modeling the inner-orbit phase
at the outer index as quasi-random. The direction is a **Borel–Cantelli dichotomy on `Σ_e p_e`**:

| | **(a) convergent BC** `Σ p_e < ∞` | **(b) divergent BC** `Σ p_e = ∞` |
|---|---|---|
| per-epoch halt-prob | `p_e → 0` (thin / shrinking target) | `p_e ≈ const > 0` (fixed-measure target) |
| heuristic direction | **NON-HALT-leaning** | **HALT-leaning** |
| BC side used | BC-**I** (convergence; **no independence needed**) | BC-**II** (divergence; **needs independence**) |
| rigor of heuristic | a.e. finite hits — clean annealed (cf. `EXISTENCE_META_THEOREM.md`, o18) | a.s. infinite hits ONLY for independent events; a single orbit lacks it (`O10_HALTER.md`) |
| exemplar | o18 (carry-alignment, density-0 summable target); o2/o7/o8/o11/o12/o14/o16 (`00`-gap / phase) | **o10** (parity-landing, `p_e≈1/3` constant) |

**What determines which side: the measure/scaling of the per-epoch halt target.**
- If the halt target is a **fixed-measure** event of the inner phase (e.g. "parity of `m` at a forced
  underflow index" — roughly a fair coin every epoch), then `p_e ≈ const`, `Σ = ∞` ⇒ **divergent ⇒ halt**.
  This is o10: the underflow always occurs (the countdown must bottom out), and its `m`-parity is ~50/50, so
  ~1/3 of epochs hit "b=0 at odd m" — and crucially this **does not decay with `B`**.
- If the halt target is a **thin / shrinking** event — a `00`-gap that must *spontaneously open* in a field of
  only isolated single 0s, or a phase race the leading-block exit wins — then `p_e → 0`, `Σ < ∞` ⇒
  **convergent ⇒ non-halt**. These targets get rarer as the structure grows.

**Grounding the o10 divergent signature `[VERIFIED]` (this session, `scratchpad/o10_ensemble.py`).** The
abstract per-epoch halt fraction is **roughly constant across disjoint B-windows** (`[1,500):0.146`,
`[500,1000):0.166`, `[1000,2000):0.165`, `[2000,3000):0.176`) — i.e. it **does NOT decay with the outer
index**. This non-decay is the divergent-BC signature, robust independent of the exact constant. (The
authoritative absolute value is `O10_HALTER.md`'s bb_sim-cross-checked **33.67%**; my quick reimplementation
of the small-`b` base rule gave a constant but smaller ~1/6 — a reimplementation discrepancy, so I cite the
doc's figure for the value and use only the robust *non-decay* qualitatively.)

**The decisive open content.** Reducing "direction" to (a) vs (b) requires the **per-epoch halt-prob scaling
`p_e` as a function of the outer index** — and for every nested machine except o10 this scaling has **not been
extracted** (no clean outer model). So the direction sits `[OPEN]` for all of them; o10 alone has the model,
and even there BC-II is inapplicable to the single deterministic orbit (so o10 is HALT-*leaning*, undecided).

---

## 4. Per-machine heuristic direction classification (NO decisions)

For each nested-Collatz machine: the exact halt mechanic, the inner safe-parity fact, the **per-epoch
halt-target type** (fixed-measure ⇒ divergent / thin ⇒ convergent / unknown), and the resulting **heuristic
direction**. **Every entry is `[OPEN]` as a decision**; "direction" below is heuristic-only.

| machine | halt mechanic `[PROVEN]` | inner safe-parity | per-epoch halt target | BC side (heuristic) | **heuristic direction** |
|---|---|---|---|---|---|
| **o10** | C/F eat-sweep eats ODD run | inner eat always EVEN | b-countdown lands `b=0` at odd `m` — **fixed-measure** (~1/3, non-decaying `[VERIFIED]`) | **divergent** | **HALT-leaning** (`[HEURISTIC]`; BC-II inapplicable ⇒ `[OPEN]`) |
| **o13** | D/E eat-sweep eats EVEN run | inner runs always ODD (7214/7214) | outer collapse eats an EVEN run — **scaling UNKNOWN (outer model not extracted)** | **unknown** | **UNCLEAR** (`[OPEN]`; only inner-safe observed, leans non-halt but un-measured outer; could be divergent like o10) |
| **o2** | `00`-gap right of D→F frontier | nested ×3/2; field `1^a 0 1^b 0 (10)^m`, only isolated 0s | a `00`-gap must spontaneously open — **thin** | convergent-leaning | **NON-HALT-leaning** (`[OPEN]`; `(10)*`-sea, no clean scalar outer map) |
| **o7** | C reads 0, left counter empty (`00`-left) | inner `⌊3a/2⌋+2` (even-a) + 2-adic cascade refill (odd-a); minA=2 | left counter empties at a separator consumption — **thin** (a≥2 always observed) | convergent-leaning | **NON-HALT-leaning** (`[OPEN]`) |
| **o8** | E reads 0, left counter empty (`00`-left) | inner `⌊3a/2⌋+1` (even-a) + exact cascade `a1=⌊a/2⌋−1` (odd-a); minA=2 | left counter empties — **thin** (a≥2 always observed) | convergent-leaning | **NON-HALT-leaning** (`[OPEN]`) |
| **o11** | B reads 0 with left neighbor 0 (`00`-gap) | inner `⌊3m/2⌋+4` (12/12); outer `3,9,26,303` | `00`-gap forms at refill — **thin** (neighbor=1 in 2330/2330) | convergent-leaning | **NON-HALT-leaning** (`[OPEN]`) |
| **o12** | E reads 0 with right neighbor 0 (`00`-gap) | inner `⌊3a/2⌋+3δ−1`; outer `4,10,28,370` | `00`-gap forms at refill — **thin** (neighbor=1 in 3516/3516) | convergent-leaning | **NON-HALT-leaning** (`[OPEN]`) |
| **o14** | C reads 0 with left neighbor 0 (`00`-gap) | inner `⌊3a/2⌋`+accreting `4,4,2` marker; never pure block | `00`-gap forms at refill — **thin** (neighbor=1 in 1996/1996) | convergent-leaning | **NON-HALT-leaning** (`[OPEN]`; least-clean outer = marker accretion) |
| **o16** | E/F alternation reads `0` at F-phase before `1` at E-phase | inner `⌊3s/2⌋+2`; leading `k→k−1` countdown | F-phase `0` beats leading-block exit — **thin** (exit wins 22/22, F-read-0 0×) | convergent-leaning | **NON-HALT-leaning** (`[OPEN]`; phase race) |

### 4.1 The direction-structure map of the nested-Collatz class

- **HALT-leaning (divergent, fixed-measure per-epoch target):** **o10 only.** It is the *only* nested machine
  with (i) an extracted clean outer-epoch model and (ii) a halt target of constant, non-decaying per-epoch
  measure (the forced b-underflow whose `m`-parity is a fair coin). This is *why* o10 is the catalogue's lone
  "probabilistically-halting (delayed)" cryptid.
- **NON-HALT-leaning (convergent, thin/shrinking per-epoch target):** **o2, o7, o8, o11, o12, o14, o16.** All
  seven have an **existence/`00`-gap-or-phase-race** halt target that must *spontaneously appear* in a field
  that structurally contains only isolated 0s (or a phase the leading-block exit keeps winning). The target
  gets rarer with growth ⇒ convergent-leaning. (Their per-epoch scaling is not extracted, so `[OPEN]`.)
- **UNCLEAR:** **o13.** Its halt target (an even-run at an outer collapse) has **unknown per-epoch scaling**
  (outer model not separable). It is the structural twin of o10 (same mirror mechanic, parity-safe inner) but
  with the **opposite** observed *inner* parity — which does **not** settle the outer direction. o13 could be
  divergent (halt-leaning, like o10) or convergent (non-halt-leaning); **un-determined.**

### 4.2 The unifying reading

The nested-Collatz class splits by **per-epoch halt-target measure**, not by inner parity:

1. **Forced fixed-measure target ⇒ divergent ⇒ HALT-leaning** — happens when the halt is a **parity-landing
   at a forced event** that occurs every epoch (o10's b-underflow). Direction = halt.
2. **Spontaneous thin target ⇒ convergent ⇒ NON-HALT-leaning** — happens when the halt is the **spontaneous
   appearance of a defect** (`00`-gap, phase misalignment) in an otherwise defect-free field (o2/o7/o8/o11/
   o12/o14/o16). Direction = non-halt.
3. **Un-extracted scaling ⇒ UNCLEAR** — o13: a parity-of-run target like o10, but whose per-outer-collapse
   measure is not computed; could fall in either bucket.

The **inner ×3/2 all-odd/all-even fact is shared by the whole class** (every inner is parity-safe) and is
therefore **orthogonal to direction**. Direction is a property of the **outer** refill orbit's per-epoch
halt-target measure — a Borel–Cantelli convergent-vs-divergent question — and is `[OPEN]` for all nine, with
o10 the only one whose outer model is clean enough to even *assign* a heuristic side.

---

## 5. Soundness ledger

- **NO machine decided; NO halting direction claimed.** Every "direction" is `[HEURISTIC]`/`[OPEN]`.
- **`[PROVEN]`/`[VERIFIED]` carried verbatim** from `O10_REDUCTION.md`, `REDUCE_O11_O16.md`,
  `REDUCE_O2_O7_O8.md`, `CATALOGUE_O13_SN.md`; none upgraded.
- **This session's new grounding:** (i) o10 eat-sweep "HALT ⟺ L odd" reproduced cleanly vs bb_sim
  (`dir_check.py`); (ii) my ad-hoc o13 eat-sweep entry was **unfaithful** (mixed parity) — flagged, and o13's
  "HALT ⟺ L even" is cited from the doc's unit-test, not from my test (the failure *reinforces* that the OUTER
  entry context, not the inner, sets the realized run); (iii) o10's abstract per-epoch halt fraction is
  **non-decaying across disjoint B-windows** = divergent-BC signature (value 33.67% per `O10_HALTER.md`; my
  reimpl ~1/6 flagged as a base-rule discrepancy).
- **Core soundness point:** the previously-suggestive "o10 halts ~1/3, o13 ~0" is **NOT a structural
  difference** — it compares o10's outer halt-prob against o13's inner safe-rate (confounded) under ≈4
  reachable epochs (small sample). Both share the always-safe inner; the discriminator (outer per-epoch
  halt-measure scaling) is extracted only for o10. o13 direction `[OPEN]`.
