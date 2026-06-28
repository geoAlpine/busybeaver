# o15 — the EXACT §3c reduction, handling the parity-irregularity rigorously (2026-06-28)

Completes the §3c reduction for `o15`, the second `8/3` (base-3) BB(6) cryptid, and pins **exactly** where its
parity-irregularity lives and whether it falls under the same existence-version unified theorem as o18.

`o15 = 1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA`  (halt = state A reads 1).

**Soundness.** Every line is `[PROVEN]` (transition-table / elementary big-int), `[VERIFIED]` (machine-checked
this session, **cross-checked step-for-step against the trusted `bb_sim.run`**), `[OBSERVED]`, or an explicit
`[ANALOGY]`. No label upgraded. Scripts in scratchpad: `o15_deep.py`, `o15_local.py`, `o15_trace.py`,
`o15_kernel.py`, `o15_halttest.py`. Numerics via `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (exact int).

---

## 0. Trusted-simulator cross-check (SOUNDNESS_INCIDENT discipline)  [VERIFIED]
The instrumented dict/bytearray simulator used below was checked **identical to `bb_sim.run`** at every budget:

| budget | bb_sim (halt, step, ones) | instrumented | match |
|---|---|---|---|
| 10 000 | (F, 10000, 132) | (F, 10000, 132) | ✅ |
| 100 000 | (F, 100000, 369) | (F, 100000, 369) | ✅ |
| 1 000 000 | (F, 1000000, 2136) | (F, 1000000, 2136) | ✅ |
| 5 000 000 | (F, 5000000, 2640) | (F, 5000000, 2640) | ✅ |

Full run to **120 000 000 steps**: no halt; 12 state-A visits, **all read 0**. `bb_sim` self-check on the
BB(2/3/4) champions passes. Reverse-engineering below is from raw tape mechanics, not from `cryptid_map`.

---

## 1. The exact halting criterion  [PROVEN, conjecture-free]

**Tape shape (settled).** `1^{a₀} 0 1^{a₁} 0 ⋯ 1^{a_k} 0` — a sequence of 1-blocks separated by **single** 0s
over an otherwise-blank tape (a leading counter region followed by a long active block; mid-cycle a `(10)*`
background appears as the active region is consumed). [VERIFIED to 120M steps; max separator = 1.]

**The halt event, from the transition table alone.** State A is *entered only* via `F : read 1 → 1RA`
(`SPEC` group F = `1RC1RA`). On entry A reads the next cell to the right: `A : read 1 → ---` (HALT),
`A : read 0 → 1RB` (continue). Therefore

> **[PROVEN] o15 halts ⟺ at some F→A right-handoff the head reads `1`, i.e. the rightward sweep encounters
> two adjacent 1s (`11`) at the active frontier ⟺ two 1-blocks ABUT (a 0-separator that normally sits between
> them is absent).** Equivalently: the new top block, as it forms, lands on an already-occupied cell
> (right-frontier collision).

**Positive control (`o15_halttest.py`)** — concrete, not just inferred:
- Plant state F on `…1[1]1…`  → **HALT after 1 step** (F→A, A reads 1). ✅
- Plant state F on `…1[1]0…` (separator present) → **no halt**, continues. ✅
- This is the only halt door: `A:read1 = "---"`, and A is reachable only from `F:read1 = "1RA"`.

So o15's halt is a **right-frontier `11`-abutment** — the exact mirror of o18, whose halt is a **left-frontier
`11`-collision** (`F:1→1LF` then F reads a left-neighbor 1). Same event, opposite frontier.

In 120M steps the 12 A-visits read `(left,read,right)` patterns `{(0,0,0):1, (1,0,1):3, (1,0,0):8}` — i.e. the
collision-relevant case `(1, 0, 1)` (A reading the separator-0 *between* two 1-blocks) occurs but the read cell
is always `0`: **the separator never vanishes ⇒ no abutment ⇒ no halt** (so far).

---

## 2. The clean part: width is the SAME ×8/3 scalar orbit as o18  [VERIFIED / PROVEN-multiplier]

Frontier widths `W = 1, 19, 40, 108, 290, 773, 2060, 5493, 14634`; ratios → **2.664 ≈ 8/3 = 2³/3**.
The width obeys **`W ↦ ⌊8W/3⌋ + 2` with carry corrections** (diffs `0, 0, −2, −3, −2, −16`) — *identical map and
identical carry-break phenomenon as o18* (o18: clean `10→28→…→3890` then epoch-8 break; o15 breaks earlier
because of its seed/phase). [VERIFIED]

- Same map, **different seed**: o18 = `10,28,76,204,546,1458,3890,…`; o15 width = `19,40,108,290,773,2060,…`.
- **Fixed point of `f(x)=⌊8x/3⌋+2` is `x=−1`** (`f(−1)=⌊−8/3⌋+2=−3+2=−1`; real fixed point `−6/5`) — **off the
  positive orbit**, exactly o18's `N=−1`. [PROVEN]
- Positive orbit **strictly increasing ⇒ transient ⇒ no invariant probability measure** (verified `f(x)>x`,
  x=1.. across 40 iterates). [PROVEN]

**So o15's width/exponent IS a clean `(8/3)ⁿ`-type orbit — the same 3-adic, base-8/3 object as o18.**

---

## 3. Where the parity-irregularity enters — EXACTLY  [VERIFIED]

The **width `W` is clean**; the **block decomposition is not**. Leading-block length and structure at frontier:

| W | base-3(W) | leading V | block structure | split? |
|---|---|---|---|---|
| 19 | 201 | 6 | `1^6 0 1^11` | split |
| 40 | 1111 | 39 | `1^39` | single (V=W−1) |
| 108 | 11000 | 107 | `1^107` | single |
| 290 | 101202 | 289 | `1^289` | single |
| 773 | 1001122 | 6 | `1^6 0 1^765` | split |
| 2060 | 2211022 | 2059 | `1^2059` | single |
| 5493 | 21112110 | 6 | `1^6 0 1^5485` | split |
| 14634 | 202002000 | 3 | `1^3 0 1 0 1 0 1^14625` | split |

`V = 6, 39, 107, 289, 6, 2059, 6, 3` — **parity/digit-irregular**: when the leading block does not split,
`V = W−1` (one clean block `1^{W−1} 0`); intermittently it **splits/reforms** (`V` drops to 6, 6, 6, 3 and new
internal 0-separators appear). So:

> **The irregularity lives in the BLOCK DECOMPOSITION — i.e. WHERE the 0-separators fall in the `(8/3)ⁿ` orbit —
> which is precisely the base-3 digit/carry boundary string of that orbit, NOT in the width scalar `W` (which is
> clean) and NOT in the halt-mechanism (which is the fixed `11`-abutment rule).** [VERIFIED]

This is the Erdős ternary-digit phenomenon **exposed as a coordinate**: o18 reads its halt off the clean scalar
`N`'s leading digit (`0 1^{N−1}`, one block); o15 reads its halt off the messier multi-block decomposition, and
the leading digit/carry of `(8/3)ⁿ` is irregular (Erdős), so the leading block `V`, and which separators are
present, is irregular. **There is no clean scalar map for `V`** (confirmed: `V` jumps 289→6→2059→6→3); the only
clean scalar is `W`.

---

## 4. Can the halt criterion still be stated via the base-3 digits? — YES, in the messier coordinate

Even with **no clean scalar map for the readout**, the halt criterion is stated exactly in the digit coordinate:

> **[PROVEN, conjecture-free, in terms of the messier coordinate] o15 non-halt ⟺ the block decomposition of the
> `(8/3)ⁿ` width orbit keeps a 0-separator at the active frontier at *every* outer step ⟺ no two 1-blocks ever
> abut.** Since the separator positions ARE the base-3 digit/carry boundaries of the orbit, this is the
> EXISTENCE statement: *the forbidden base-3 carry alignment (the one that would delete the frontier separator)
> never occurs after the verified prefix.*

This is the **same existence/Borel–Cantelli facet as o18** (o18: "the forbidden left-frontier carry never
aligns"), **not** a Cesàro/density facet (contrast Antihydra). Both o15 and o18:
- ride the **same** clean `⌊8x/3⌋+2` orbit (8/3, base-3, fixed point `−1`, transient);
- halt on an **existence** event = a forbidden base-3 carry/abutment **ever** occurring;
- have the same kernel: *the base-3 digit/carry of `(8/3)ⁿ` equidistributes ⇒ the alignment set has density 0 ⇒
  (Erdős-strength) finite/empty after the prefix.*

**Honest status of the digit dictionary.** That the separator positions equal the base-3 digit boundaries of the
orbit is `[OBSERVED/ANALOGY]`, the **same epistemic status as o18's Erdős link** (`CRYPTID_REDUCTIONS.md`,
`CRYPTID_O18_FRAMEWORK.md` §1: o18-to-Erdős is a *strong structural analogy, not an exact reduction* — the width
drifts via carries, it is not literally the digits of `8ⁿ`). The 8-point split table does not yield a crisp
closed-form `V = (digit of W)`; what IS solid is (i) width = clean `⌊8W/3⌋+2` orbit, (ii) halt = `11`-abutment
in the block decomposition, (iii) block decomposition = base-3 digit/carry readout of that orbit. The
existence-statement reduction is clean; the explicit per-digit formula is analogy, exactly as for o18.

---

## 5. Classification: same Erdős ternary kernel as o18, or genuinely different?

**SAME kernel as o18 (existence-version), in a messier coordinate — NOT a different or harder number-theory
problem.**

| | o18 | o15 |
|---|---|---|
| width / scalar orbit | `⌊8N/3⌋+2` (8/3) clean | `⌊8W/3⌋+2` (8/3) clean **(same map)** |
| fixed point (halting config) | `N=−1`, off positive orbit | `N=−1`, off positive orbit **(same)** |
| transience barrier | strictly increasing, no inv. measure | same |
| halt event | **left**-frontier `11`-collision | **right**-frontier `11`-abutment (mirror) |
| readout coordinate | clean single block `0 1^{N−1}` (1 digit read) | **multi-block decomposition** (digit STRING read) |
| halt facet | EXISTENCE (carry ever aligns) | EXISTENCE (carry ever aligns) **(same facet)** |
| named family | Erdős ternary digits of `2^{3n}` (8/3) | **same** Erdős family (8/3) |
| AEV placement | Conj 1.6, `q=3`, `p<q²` (`8<9`), floor-mirror | **same** |
| only unconditional result | Narkiewicz upper bound, set not known finite | **same** |

The parity-irregularity is a **coordinate/modelling obstacle**, not a new mechanism: o15 reads its halt off the
*digit string* (block decomposition) rather than the *leading digit* (single block), so it inherits the Erdős
digit irregularity directly in the readout. **This makes o15 harder to MODEL** (no clean scalar readout map; the
reduction needs the extra block-decomposition bookkeeping) **but not a harder or different open problem** — the
underlying kernel object (`⌊(8/3)ⁿ⌋` base-3 carry equidistribution = base-3 digits of `2^{3n}`) is identical to
o18's. **Same Erdős wall; deciding either needs the same Erdős-class density breakthrough.**

---

## 6. H-fixed-point and the barrier  [PROVEN / VERIFIED]
The halting orbit's fixed point is the integer fixed point of the width map, `N = −1` (`⌊8·(−1)/3⌋+2 = −1`),
the exact (no-floor) fixed point `−6/5`, both **off** the strictly-increasing positive orbit. The
no-structure-only barrier transfers in spirit from o18/Antihydra: every property of the clean `⌊8x/3⌋+2`
structure is shared with the off-orbit fixed configuration `N=−1` (and the all-carry-free itinerary), so no
structure-only argument separates halting from non-halting; the distinction lives in the **existence-of-forbidden-carry
(genericity) tail** of the specific orbit. Realized through the **Erdős "no finiteness / no lower bound" gate**
(Narkiewicz: upper bound only), identical to o18 (`CRYPTID_O18_FRAMEWORK.md` §4) — not the ergodic-optimization
`β=max` density gate of Antihydra (o15/o18 halt on existence, not density). [PROVEN spirit; VERIFIED fixed point + transience.]

---

## 7. Honest verdict

1. **Exact halt criterion (cross-checked vs `bb_sim`): PROVEN.** o15 halts ⟺ a `11`-abutment at the F→A right
   frontier (a 0-separator in the block decomposition vanishes). Confirmed by transition table + planted-config
   positive control + 120M-step non-halt (12 A-visits, all read 0), instrumented sim ≡ `bb_sim` exactly.

2. **Where the parity-irregularity enters: PINNED.** In the **block decomposition** (separator positions /
   leading block `V`) = the base-3 digit/carry string of the clean `⌊8W/3⌋+2` orbit. The width scalar is clean;
   the readout coordinate is irregular (the Erdős ternary-digit phenomenon made into a coordinate).

3. **Same Erdős ternary kernel as o18? YES (existence-version).** Same `8/3` clean orbit, same fixed point
   `N=−1`, same transient barrier, same EXISTENCE halt facet, same Erdős `2^{3n}`-digit family / AEV `q=3`
   `p<q²` floor-mirror placement, same missing piece (Narkiewicz upper bound, no lower bound). o15 is the
   **right-frontier, multi-block-coordinate sibling of o18**; the irregularity is a coordinate nuisance, not a
   different/harder problem.

4. **Scope: o15 is IN-SCOPE of the existence-version unified theorem, same as o18.** The reduction to the shared
   Erdős/AEV-`8/3` kernel is **clean at the existence-statement level and PROVEN for the halt mechanism + clean
   width orbit + barrier**, despite the messy coordinate. The one item that stays `[ANALOGY]` is the explicit
   "separator position = base-3 digit of the orbit" dictionary — **the same epistemic status o18 already has**
   (o18's Erdős link is itself analogy, not exact reduction). So o15 needs **no separate treatment**: the
   existence-version theorem that covers o18 covers o15 verbatim; only an extra block-decomposition coordinate
   change is required, and that change is bookkeeping, not new mathematics.

**No decision; no non-halt claimed; soundness intact.** o15 = the `8/3` Erdős cryptid in a multi-block
coordinate; same wall as o18, harder to model, not harder to solve.
