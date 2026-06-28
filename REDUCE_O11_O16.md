# Exact halt-predicate attempt for the 5 nested Mahler-3/2 machines o11,o12,o13,o14,o16 (2026-06-29)

*Goal: derive the EXACT halt predicate for each nested machine and honestly decide which (if any) become
IN-SCOPE (halt couples only to the inner ×3/2 orbit ⇒ clean 2^k predicate) vs which stay IN-FAMILY (blocked
by the doubly-exponential outer refill, like o10-FULL). Soundness paramount; labels `[PROVEN]` (machine-checked,
exact) / `[VERIFIED]` (bb_sim-faithful numerics, not promoted) / `[OPEN]`. Every mechanic was reverse-engineered
against the raw TM with bb_sim-identical parse/step semantics and exact big-ints
(`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`). No machine is decided; no non-halting is asserted.
Scratchpad: `o1116_anat.py`, `o1116_halt.py`, `o1116_instr.py`, `o1116_refine.py`, `o1116_inner.py`.*

Specs (from `suite.py`):
- o11 `1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF`  (halt = **C reads 0**)
- o12 `1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB`  (halt = **F reads 0**)
- o13 `1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA`  (halt = **E reads 0**)
- o14 `1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE`  (halt = **F reads 0**)
- o16 `1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE`  (halt = **F reads 0**)

---

## 0. Headline

> **NEW (this run): the EXACT halt MECHANIC was derived and unit-tested for all five** (not just "reads 0"):
> three are a `00`-gap collision (o11,o12,o14), one is a clean parity eat-sweep that is the structural TWIN of
> o10 (o13), and one is a `(10)`-sea phase-alignment race (o16).
>
> **Verdict: 0 of 5 become in-scope; all 5 stay IN-FAMILY-not-in-scope, blocked by the outer refill, exactly
> like o10-FULL.** For every one, the halt event was machine-verified to **never occur within a normal inner
> epoch** — it can only occur at a rare OUTER refill/boundary reconfiguration, and evaluating "does it ever
> occur" requires the doubly-exponential, non-eventually-periodic outer orbit. **None is confirmed a
> probabilistic halter** (unlike o10-FULL); direction `[OPEN]` for all five (and, unlike o10, the outer epoch
> model is not even cleanly extractable, so no heuristic direction can be assigned).

| machine | exact halt mechanic `[PROVEN, unit-tested]` | inner orbit ever triggers it? `[VERIFIED]` | outer refill | exact predicate derivable? | scope |
|---|---|---|---|---|---|
| **o11** | B reads `0` whose **left** neighbor is `0` (a `00`-gap) | NO — neighbor `=1` in 2330/2330 precursor visits (5M steps) | `3,9,26,303` doubly-exp | only via outer | **IN-FAMILY** |
| **o12** | E reads `0` whose **right** neighbor is `0` (a `00`-gap) | NO — neighbor `=1` in 3516/3516 visits | `4,10,28,370` doubly-exp | only via outer | **IN-FAMILY** |
| **o13** | D→E leftward eat-sweep consumes an **EVEN-length** run of 1s | NO — run **ODD** in **7214/7214** sweeps (50M steps) | `3,6,10,64` doubly-exp | clean predicate, but composite/outer | **IN-FAMILY** (o10 twin) |
| **o14** | C reads `0` whose **left** neighbor is `0` (a `00`-gap) | NO — neighbor `=1` in 1996/1996 visits | sea-countdown + marker | only via outer | **IN-FAMILY** |
| **o16** | E/F rightward alternation reads `0` at an **F-phase** cell (a `00` vs `11` race) before `1` at an E-phase cell | NO — sweep EXITS (E reads 1) in all 22 events; only 15 F-visits / 5M | `k→k−1` doubly-exp | only via outer | **IN-FAMILY** |

---

## 1. The exact halt mechanics  [PROVEN, unit-tested vs raw TM]

Each halt state is entered from a **single** predecessor transition (verified by predecessor analysis,
`o1116_anat.py`); this pins the local halt mechanic, which was then unit-tested by crafted runs
(`o1116_halt.py`).

### o11 — `00`-gap collision (state C entered only from `B:0→1LC`)
`B:0→1LC` (B reads 0, writes 1, moves L→C); then `C:0→HALT`, `C:1→1LA`. So after B consumes a `0`, C reads the
cell immediately to the **left**. **HALT ⟺ that left cell is `0`** ⟺ B read the right `0` of a `00` block.
`[VERIFIED]`: left=0 → HALT in 2 steps; left=1 → continues. **This is an existence (`00`-gap) event**, the
o2-type halt, not a run-parity event.

### o12 — `00`-gap collision (state F entered only from `E:0→1RF`)
`E:0→1RF` then `F:0→HALT`, `F:1→1LB`. After E consumes a `0`, F reads the cell to the **right**. **HALT ⟺ that
right cell is `0`** ⟺ E read the left `0` of a `00` block. `[VERIFIED]`: right=0 → HALT; right=1 → continues.

### o13 — clean parity eat-sweep (state E entered only from `D:1→1LE`) — THE o10 TWIN
`D:1→1LE`, `E:1→0LD` (eat a 1), `E:0→HALT`, `D:0→0RA` (exit), `D:1→1LE` (continue). Moving **left** from a D-entry
over a run of 1s, the state alternates D,E,D,E…; the terminating `0` is read in state **E** at odd offset
(→HALT) or **D** at even offset (→exit). Therefore:

> **(o13 HALT-MECHANIC) [PROVEN].** A D→E eat-sweep that scans a maximal left-run of `L` ones **HALTS iff `L`
> is EVEN**; if `L` is odd it exits to A and the machine continues. `[VERIFIED]`: crafted blocks give immediate
> HALT in exactly `L+2` steps for `L ∈ {0,2,4,6,8,10}` and clean exit for odd `L`.

This is the **exact mirror of o10's** `(HALT-MECHANIC)` (o10 = leftward C/F eat-sweep, halts iff run **odd**).
o13 is structurally o10 with the opposite halting parity.

### o14 — `00`-gap collision (state F entered only from `C:0→1LF`)
`C:0→1LF`, `F:1→0LE` (eat), `F:0→HALT`; after F eats it goes to E, which only continues left over 1s or exits to
B on a 0 — **F can fire only on the first cell**. So **HALT ⟺ C read a `0` whose left neighbor is `0`** (the
first cell F reads is `0`). `[VERIFIED]`: left=0 → HALT in 2 steps. (`00`-gap event, like o11/o12.)

### o16 — `(10)`-sea phase-alignment race (state F entered only from `E:0→1RF`)
`E:0→1RF`, `F:0→HALT`, `F:1→1RE`, `E:1→0RC` (exit). Moving **right**, the state alternates F,E,F,E…; **F-phase**
cells (odd offsets) HALT on `0` / continue on `1`; **E-phase** cells (even offsets) EXIT on `1` / continue on
`0`. A perfectly phased sea `1 0 1 0 …` is traversed until it deviates. **HALT ⟺ the sweep reads a `0` at an
F-phase cell** (a `00`-type defect / right boundary at the lethal phase) **before reading a `1` at an E-phase
cell** (a `11`-type defect / the leading block, which causes a safe exit). `[VERIFIED]`: a perfect finite
`(10)^m` sea HALTS at its trailing boundary `0` (step `2m+2`); a `0` planted at any F-phase cell HALTS there.
So o16's non-halting in the real orbit is a **phase race won by the `11`/leading-block exit** — again an
existence/alignment event, not a clean inner-orbit parity.

---

## 2. The inner ×3/2 engines  [VERIFIED, exact big-int, reproduces documented seas]

Re-confirmed this run (`o1116_inner.py`), consistent with `CATALOGUE_IRREGULAR.md`:
- **o11**: inner sea `2,7,14,25,41,65,101,155,236,358,541,815,1226`, exact `m' = ⌊3m/2⌋ + 4` (12/12).
- **o16**: inner sea `73,111,168`, exact `s' = ⌊3s/2⌋ + 2` on consecutive steps.
- **o12**: a-start `44,68,…,9584`, `a' = ⌊3a/2⌋ + (3δ−1)`, `δ∈{1,2}`; ratios → 1.5008.
- **o13**: a-start `40,67,…,4411`; ratios → 1.5024.
- **o14**: a-start `3,10,…,2764` + accreting `4,4,2` marker tail; ratios → 1.5030.

All five carry a clean **μ = 3/2 (p=2)** inner engine. No new multiplier. (Unchanged from catalogue;
re-verified for soundness.)

---

## 3. The decisive coupling test — inner vs outer  [VERIFIED]

The decisive question (per the brief): does the halt event couple ONLY to the inner ×3/2 orbit (⇒ in-scope,
clean 2^k predicate) or to the outer refill alignment (⇒ in-family, like o10)? Answered by instrumenting the
real blank-tape orbit (`o1116_instr.py`, `o1116_refine.py`) and recording, at **every** visit to the halt
precursor, the halt-determining quantity:

- **o11**: precursor `B reads 0` visited **2330×** in 5M steps; the **left neighbor was `1` every single time**
  (`{1: 2330}`). The `00`-gap never even approaches. → halt impossible within inner epochs.
- **o12**: precursor `E reads 0` visited **3516×**; right neighbor `= 1` every time. → same.
- **o14**: precursor `C reads 0` visited **1996×**; left neighbor `= 1` every time. → same.
- **o13**: **7214 eat-sweeps over 50M steps; the determining left-run was ODD (=safe) in 7214/7214**, even-run
  (=HALT) count `= 0`, max run `L = 65`. The inner orbit **never** produces the even run the halt needs — the
  exact analog of o10's `L = 2m−8` being always even. → halt impossible within inner epochs.
- **o16**: state F visited only **15×** in 5M steps (the alternation sweep is a rare outer event); F read `0`
  (halt) **0×**, while the E-phase safe-exit (`E reads 1`) fired **22×**. The `11`/leading-block exit wins the
  phase race every time. → halt impossible within inner epochs.

**Conclusion `[VERIFIED]`:** for all five, the halt event is **structurally absent from every observed inner
epoch**; it can occur ONLY at a rare OUTER refill/boundary reconfiguration. The halt **couples to the outer
orbit, not the inner ×3/2 orbit** in every case.

---

## 4. The outer refill orbits — doubly-exponential, blocking the predicate  [VERIFIED]

The outer (leading-block collapse) orbits are the catalogue's "irregular" sequences and are
**doubly-exponential / not eventually periodic**:

| machine | outer refill orbit (pure-block `k`, with `t`) | structure |
|---|---|---|
| o11 | `3,9,26,303` (`t=10,47,272,28101`) | `k→k−4` countdown; collapse every ≈`k₀/4` inner ×3/2 steps ⇒ next ≈`(3/2)^{k₀/4}` |
| o12 | `4,10,28,370` (`t=17,95,565,58083`) | sea countdown; `δ`-coupled |
| o13 | `3,6,10,64` (`t=20,51,122,3519`) | sea countdown |
| o14 | sea countdown + accreting `4,4,2` marker (never a pure single block) | marker accretion |
| o16 | `k→k−1` doubly-exp refill ("o11 with step −1") | leading counter decays by 1/epoch |

Because each epoch runs ≈`(leading counter)/Δ` inner ×3/2 steps, the next collapse is ≈`(3/2)^{k₀/Δ}` — so the
outer orbit jumps doubly-exponentially (`26→303` is ×11.6; the next collapse is `≳10¹³` steps away, unreachable
by simulation). **This is the exact obstruction of o10-FULL** (`O10_REDUCTION.md` §3): the inner engine is
clean, but the halt predicate needs the alignment of the inner-orbit phase against a **dynamically-determined,
doubly-exponentially sparse** set of outer reconfiguration events, across infinitely many restarting epochs.
No finite-state / semilinear over-approximation closes (consistent with `far_dfa`/`far_finder`/`far_cegar` all
HOLDOUT).

---

## 5. The exact halt predicates  [PROVEN mechanic + VERIFIED inner; composite ⇒ blocked]

Combining §1 (mechanic) + §3 (inner never triggers) + §4 (outer doubly-exp):

> **o11 `[PROVEN]`:** halts ⟺ the B-sweep ever reads a `00`-gap. `[VERIFIED]` the inner `1^a 0 1^b 0 (10)^m`
> field contains no `00` (only isolated 0s); a `00` can form only at an outer refill ⇒ predicate = "∃ refill
> producing a `00` alignment", governed by the doubly-exp orbit `3,9,26,303`. **Composite/existence — BLOCKED.**
>
> **o12 `[PROVEN]`:** halts ⟺ the E-sweep ever reads a `00`-gap (right). Same structure (refill `4,10,28,370`).
> **Composite/existence — BLOCKED.**
>
> **o13 `[PROVEN]`:** halts ⟺ **some D→E eat-sweep ever consumes an EVEN-length run of 1s**. This is a CLEAN,
> exact predicate (the direct mirror of o10's "∃ epoch landing on b=0 at odd m"). `[VERIFIED]` the inner orbit
> yields only odd runs (7214/7214 over 50M), so realization requires an even-run at an outer collapse (orbit
> `3,6,10,64`, doubly-exp). **Composite/existence — BLOCKED. This is the cleanest of the five and the exact
> structural twin of o10.**
>
> **o14 `[PROVEN]`:** halts ⟺ the C-sweep ever reads a `00`-gap (left). The accreting `4,4,2` marker tail means
> o14 never even forms a pure single block, so the outer orbit is the least clean. **Composite/existence —
> BLOCKED.**
>
> **o16 `[PROVEN]`:** halts ⟺ the E/F alternation sweep ever reads a `0` at an F-phase cell before a `1` at an
> E-phase cell (a `00`-defect/right-boundary winning the phase race against the `11`/leading-block exit).
> `[VERIFIED]` the leading-block exit wins in every observed epoch; realization requires an outer-refill phase
> misalignment (refill doubly-exp). **Composite/existence — BLOCKED.**

**None couples only to the inner ×3/2 orbit. None yields a clean 2^k predicate on the inner orbit alone.** So
**none becomes in-scope.**

---

## 6. Direction check (soundness-critical)  [OPEN for all five]

Per the brief, for refill-coupled halts I checked the heuristic halting direction but make **no decision**.

- **o13** (the o10 twin): over 50M steps every eat-sweep run is ODD (safe); the halt-parity is never realized.
  This is **opposite** to o10-FULL's signal (o10 each epoch halts w.p. ≈1/3 ⇒ heuristically HALTS). o13's
  observed signal leans **non-halting** — but only ≈4 outer epochs are reachable, and whether a far (unreachable)
  collapse ever produces an even run is exactly the doubly-exp existence question. **Direction `[OPEN]`.** I do
  **not** claim o13 is a non-halter; the all-odd observation is suggestive, not a proof (it would become a proof
  only if "the determining run is structurally always odd" were established, the analog of o10's provable
  `L=2m−8` even — NOT established here).
- **o11,o12,o14** (`00`-gap): the field is `…1^a 0 1^b 0 (10)^m…` with only isolated single 0s; a `00` is never
  observed in millions of steps. Heuristically the orbit **avoids** the `00` target (non-halting-leaning), but
  realization depends on the outer refill. **Direction `[OPEN]`.**
- **o16** (phase race): the `11`/leading-block exit wins every observed race; heuristically non-halting-leaning,
  but outer-coupled. **Direction `[OPEN]`.**

**Crucially, unlike o10-FULL, none of the five admits a cleanly extractable abstract outer-epoch model** (o10's
b-countdown refill was piecewise-affine and could be iterated to estimate a per-epoch halt probability; here the
outer reconfigurations are messier — `δ`-coupled / marker-accreting / phase-dependent — and not reduced to a
clean map). So I cannot even assign o10's kind of heuristic per-epoch halt probability. These five are at least
as blocked as o10-FULL, and **no machine is confirmed a probabilistic halter (OUT).**

---

## 7. Honest tally

| outcome | count | machines |
|---|---|---|
| **IN-SCOPE** (exact predicate couples only to inner ×3/2 ⇒ clean 2^k) | **0** | — |
| **IN-FAMILY, not in-scope** (exact mechanic derived; halt composite/existence, blocked by doubly-exp outer refill, like o10-FULL) | **5** | o11, o12, o13, o14, o16 |
| confirmed probabilistic HALTER (OUT, like o10-FULL direction) | **0** | none confirmed; o13 is the structural twin but its observed direction leans the opposite way; `[OPEN]` |

**So: 0 in-scope, 5 in-family, 0 confirmed OUT.** Every one stays exactly where o10-FULL sits: clean inner
×3/2 engine `[VERIFIED]`, exact halt **mechanic** `[PROVEN, unit-tested]`, but the full halt **predicate** is a
composite/existence event over a doubly-exponential outer refill orbit, which blocks the exact criterion. The
scope set of `BB6_STRUCTURAL_LIMIT_THEOREM.md` ({Antihydra, o18, o15, o10-inner}) is **unchanged**; these five
do not join it. The `MAHLER_3_2_DOMINANCE.md` placement (all five `[VERIFIED]` 3/2, in-family-not-in-scope) is
confirmed and sharpened with explicit unit-tested halt mechanics.

---

## 8. What is genuinely NEW this run (vs the catalogue)

1. **Exact halt MECHANICS** (not just "state X reads 0"), unit-tested vs the raw TM, for all five:
   o11/o12/o14 = `00`-gap collision; **o13 = clean parity eat-sweep (halt iff even run) = the exact mirror of
   o10**; o16 = `(10)`-sea phase-alignment race.
2. **The inner-never-halts fact, measured for each** (the analog of o10's always-even inner eat): the halt
   event is absent from every observed inner epoch (neighbor `=1` always; o13 run odd 7214/7214; o16 exit wins).
   This is the precise reason the predicate is outer-coupled.
3. **A clean exact predicate for o13** ("halts ⟺ ∃ even-run eat-sweep"), establishing o13 as the closest BB(6)
   analog to o10 — same composite/existence structure, opposite halting parity, opposite (non-halt-leaning)
   observed direction.

**Soundness:** every mechanic is unit-tested against the raw TM; every inner/outer measurement uses the exact
bb_sim-identical simulator with big-ints. No label upgraded; no machine decided; no non-halting asserted. The
five remain `[OPEN]`, in-family, blocked by the doubly-exponential outer refill.
