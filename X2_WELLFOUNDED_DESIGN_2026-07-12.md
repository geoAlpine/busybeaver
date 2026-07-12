# The WellFounded recursion for the general-`j` symbolic carry / outer step of the
# integer-×2 doubling phase — a DESIGN BLUEPRINT (2026-07-12)

*Machine `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`. This designs (does NOT
formalize, does NOT edit `lean/X2.lean`) the well-founded recursion that closes
the doubling phase `M6(K) → M1(K+1)` by decomposing every odometer tick into the
already on-path-proven inner sweeps. STRICT labels: [OBSERVED] = read off the raw
exact-bigint orbit (`x2wf_*.py`, matching `X2.step`); [PROVEN-elsewhere] = a
kernel-checked lemma already in `lean/X2.lean`; [DESIGN] = proposed, not yet built.
Complements `X2_BRAID_DESIGN_2026-07-12.md` (the Odo structure) and X2.lean §5h–§5k.*

---

## 0. Executive verdict

The recursion splits **cleanly into three layers**, and the crux — the
well-founded MEASURE — is clean **only when it is placed on the PURE odometer
register, not on the tape**. The single most important empirical finding of this
session is a NEGATIVE one: **every naive tape-decoded scalar (total ones, comb
pairs, weighted block-value) is NON-monotone on the real orbit** — the odometer's
carries push them up and down exactly like the bits of a binary counter (§2,
`x2wf_value2.py`: the weighted value decreases at 516 122 of 523 830 ticks). So
there is *no* one-line "watch this tape number shrink" measure. The clean measure
is `μ = T − t` on an abstract counter `odoNext : Odo → Odo`, whose faithfulness to
the tape is the real work. This makes the object **strictly harder than, and
structurally different from, o4's `generation_odometer`** — which is NOT a
well-founded recursion at all (it proves ONE step and leaves the iteration open).
Here we would actually CLOSE the iteration. Feasibility: implementable, the
measures on both recursions are textbook, but the tape↔register faithfulness of
the general-`j` carry is a multi-session lemma.

---

## 1. The exact per-tick decomposition [OBSERVED, raw g=2,3]

**Provenance.** `x2wf_measure.py`, `x2wf_counter.py` on the real `M6(2)→M1(3)`
orbit (phase = 2 119 015 steps, K=10). The post-entry M6 cascade is
`[2^K−3, 2^{K−1}−3, …, 2^2−3, 1] = [1021,509,253,125,61,29,13,5,1]`; the M1(K+1)
cascade is the **shifted-up (doubled)** `[2039,1021,509,…,5,1]` — the leading
digit is `2^{K+1}−9 = 2039`, not `2^{K+1}−3 = 2045` (the odd-g `−6` correction,
already isolated as `bigCascade_not_doubling`'s Θ(K) residual). Every other digit
is the previous digit doubled by `d ↦ 2d+3` [OBSERVED, `x2wf_counter.py`].

**The odometer is a binary counter on the cascade.** [OBSERVED] Carries fire at
left-comb count `= 2^j − 1` and regenerate the working block `2^j−3 ↦ 2^{j+1}−3`
(`doubling_id` realized physically); the number of carries at each level HALVES
as the level rises (level-4: 255, level-5: 127, level-6: 63, … level-(K+1): once)
— the exact bit-flip profile of a binary counter (`x2wf_counter.py`). Total
carries ≈ 2 953 ≈ Θ(2^K); chew-starts 3 852 (g=2) / 9 729 (g=3) ≈ Θ(2^K) (up to
the slow ~K constant); each chew-start runs a Θ(2^K)-length inner sweep ⇒
Θ(2^{2K}) total.

**ONE tick, as a composition of PROVEN inner lemmas** [DESIGN, factors PROVEN-elsewhere]:

```
outer_step(Odo) =
  chew   : ecombChewFold v      -- leading block 1^{2v+1} → 1^1, deposit pow01 v   [X2.lean §5i, ∀v]
  turn   : dSweepTurn / gap-cross over the 0^2 separator to the next cascade digit  [X2.lean §5,  ∀n]
  carry  : carry_step           -- IF comb hit 2^j−1: sweepEF-repack (01)^m → 1^{2m}, ripple  [∀m via sweepEF §4]
```

- **No-carry tick** (the common case, ~7/8 of ticks): `chew` deposits one comb
  pair (or descends the block by 2), `turn` re-anchors E-on-0. No `sweepEF`.
- **Carry tick** (comb `= 2^j−1`): the accumulated comb `(01)^m` is repacked by
  `sweepEF` (`m → 2m`, PROVEN ∀m) into the doubled block `1^{2^{j+1}−3}`, and a
  fresh `1^{2^2−3}=1^1` is seeded below.

**Is the general-`j` carry the same shape as the concrete `carry_event_5to13`?**
[OBSERVED] SAME arithmetic shape (`d_j ↦ 2d_j+3`), but **NOT the same tape
window** — `carry_event_5to13` is the `j=3` instance in a *fixed* 117-step,
bounded-`[−8,+20]`-window `rfl` chunk; the general-`j` carry repacks a comb of
`Θ(2^{j−1})` pairs, so its window and step-count GROW with `j`. Therefore the
general carry is **NOT** the concrete 117-step lemma re-used per `j`; it must be
rebuilt as a `sweepEF`-composite (which IS proven ∀ length). `carry_event_5to13`
survives only as the `#eval`-anchor that the general shape reduces to at `j=3`.

- **The carry can RIPPLE** [OBSERVED, `x2wf_pure.py`]: usually depth 1, but a
  depth-2 ripple appears already at g=3. A single tick may thus propagate the
  carry through a data-dependent number of digits (≤ K). This is the classic
  variable-length binary-counter carry, and forces `carry_step` to be a **bounded
  inner recursion**, not a straight-line composite.

---

## 2. The well-founded measure — the crux [OBSERVED + DESIGN]

**Negative result (the decisive measurement).** [OBSERVED, `x2wf_value2.py`, g=2,
523 830 ticks] None of the tape-visible scalars is monotone:

| candidate            | increases | DECREASES | comment |
|----------------------|-----------|-----------|---------|
| total ones           | 515 863   | **7 319** | halves then doubles |
| comb pairs           | 7 959     | **4 362** | resets to 0 at every carry |
| Lones (left ones)    | 519 723   | **3 851** | dips one per carry |
| weighted block-value | 4 619     | **516 122** | my `2^{level}` decode is not the counter |

So **there is no clean measure decodable directly from the raw tape** — the
carries make every physical scalar oscillate exactly like the bits of a binary
counter (where `0111+1 = 1000` drops the one-count 3→1 yet increments the value).

**The clean measure lives on the PURE register.** [DESIGN] Define the abstract
counter `odoNext : Odo → Odo` (§4). Because `odoNext` is a genuine mixed-radix
increment with fixpoint `odoFinal`, the standard binary-counter measure

```
μ(o) = odoValue(odoFinal) − odoValue(o)        -- strictly −1 each odoNext tick
```

is well-founded on `Nat` and **decreases by exactly 1 every outer tick, hitting 0
at the base case `odoFinal = M1(K+1)`** — trivially clean, because `odoValue` is
DEFINED so that `odoNext` increments it (not read off a noisy tape). The base case
is `μ = 0 ⇔ comb exhausted and cascade = the doubled vector` — the M1(K+1) shape.
The subtlety is therefore **displaced entirely off the measure** and onto the
faithfulness lemma "the tape at tick `t` is exactly `(odoNext^t o₀).toCfg`" (§4,
hardest sub-lemma). For the ripple sub-recursion, the inner measure is the number
of digits still to carry (`≤ K`), also clean and decreasing.

This is why `X2_BRAID_DESIGN` §2's "the genuine invariant is the odometer VALUE,
not a tape scalar" is exactly right, and now has a quantified refutation of the
tape-scalar alternatives behind it.

---

## 3. Termination + net-doubling [OBSERVED + PROVEN-elsewhere]

**Termination.** `μ` is a `Nat` strictly decreasing each tick ⇒ the outer
recursion terminates in `T = μ(o₀) = Θ(2^K)` ticks [OBSERVED: chew-starts 3 852 at
K=10, 9 729 at K=11]. The inner ripple terminates in ≤ K carries [OBSERVED: max
depth 1–2]. The inner sweeps terminate by their own length induction
[PROVEN-elsewhere: `ecombChewFold`, `sweepEF`, `dSweepTurn` are total ∀ length].

**Net-doubling arithmetic (closes at the base case).** The per-carry digit law is
already ∀`n`:
- `carryDigit_closed : carryDigit n = 2^{n+2} − 3` [PROVEN-elsewhere] — the
  `1,5,13,29,61,…` regeneration chain, i.e. `n` carries drive the bottom digit to
  `2^{n+2}−3`. The general cascade doubling is the List-lift of this.
- `doubling_id : 2·(2^K−3)+3 = 2^{K+1}−3` [PROVEN-elsewhere] — one digit's ×2.
- `cascadeBlocks_sum : Σ digits = 2^{K−1} − 4K + 8` [PROVEN-elsewhere] — the
  telescoping accumulator with the `−4K+8` correction that accounts for the
  observed leading `2039 = 2^{K+1}−9` (not `2045`).

The missing piece is a **`carry_sum` lemma** [DESIGN]: `Σ` over the Θ(2^K) tick
carries `= 2^{K+1}−3` (mod the isolated Θ(K) correction), which is the List-valued
iterate of `carryDigit_closed` proved by the SAME `Nat` induction one dimension up.
No new tape reasoning enters the arithmetic — it is pure `Nat`/`List`, exactly the
separation `carryDigit_closed` already demonstrates.

---

## 4. The Lean encoding blueprint [DESIGN]

**Recommended: THREE separated layers (not one monolithic tape-WF).** This isolates
each measure where it is clean.

```lean
/-- Pure odometer register: descending cascade being consumed, doubled cascade
    being built, and the low comb accumulator. -/
structure Odo where
  todo  : List Nat    -- remaining descending digits [2^j−3] not yet consumed
  built : List Nat    -- doubled digits already deposited (big→small)
  comb  : Nat         -- (01)-pairs pending on the left  (the low counter digit)

/-- LAYER B (pure, CLEAN WF).  One counter increment with ripple carry. -/
def odoNext : Odo → Odo := …          -- binary-counter step; carry when comb = 2^j−1
def odoValue : Odo → Nat := …         -- DEFINED so odoValue (odoNext o) = odoValue o + 1
def odoFinal (K) : Odo := …           -- the doubled cascade, comb = 0

theorem odo_terminates (K) :
    ∃ T, (odoNext^[T]) (odoEntry K) = odoFinal K
  -- WF recursion on μ o = odoValue (odoFinal K) − odoValue o, −1 each step.  CLEAN.

/-- LAYER A (tape, NO measure — a parametric STEP lemma, o4-style).  ONE tick
    realizes ONE odoNext, for arbitrary opaque tails L,R. `some ⇒ HALT-FREE`. -/
theorem outer_step (o : Odo) (pos) (L R) :
    ∃ N pos', steps N (o.toCfg pos L R) = some ((odoNext o).toCfg pos' L R)
  -- = ecombChewFold v  (∘ dSweepTurn)  (∘ carry_step)   — the branch on comb = 2^j−1.

/-- carry_step: the general-j carry, a BOUNDED inner recursion (ripple ≤ K). -/
theorem carry_step (o) (pos) (L R) (h : o.comb = 2^(o.level) − 1) : … 
  -- sweepEF-repack (01)^m → 1^{2m}; recurse on ripple-depth (measure = #digits left).

/-- GLUE: iterate Layer A along Layer B's T, accumulating steps_add. -/
theorem doubling_phase (K) (pos) (L R) :
    ∃ N pos', steps N ((odoEntry K).toCfg pos L R) = some (M1 (K+1) …)
```

**Shape-preservation invariant.** Carried as the predicate `o.toCfg` itself: the
claim is that the on-anchor Cfg is ALWAYS `Odo.toCfg` of *some* register — the
left deposit is exactly `pow01 o.comb ++ (bounded residue)` and the right is the
`casc` of `o.todo ++ o.built`. `outer_step` must both consume and re-establish
this shape; that IS the invariant threaded through the outer recursion.

**THE SINGLE HARDEST SUB-LEMMA: `outer_step` at a carry (the general-`j`
`carry_step`).** Two coupled difficulties, both real:
1. **Left-deposit summarization** — proving the unbounded left stays
   `pow01 comb ++ (bounded residue)` across every tick, so `Odo` is a *faithful*
   (non-leaky) abstraction. [OBSERVED true — bounded shape-vocabulary — but needs
   a preserved-shape induction over the whole phase.]
2. **The ripple carry** — `carry_step` is not one closed form; it branches on
   whether the repack overflows into the next digit and recurses (≤K deep), each
   "bit flip" being a Θ(2^j)-length `sweepEF`, not a constant. A verified
   ripple-carry incrementer whose carry unit is an unbounded sweep.

Difficulty estimate: `carry_step` is the `Suffix.lean`-scale object of the whole
project — comparable to one full `suffix_g5` (the 90-line `rfl`-chain generic
class) but with a genuine inner recursion on top. The inner sweep factors are
DONE; the faithfulness + ripple is **~1.5–2× a single `generation` map**.

**Contrast with `generation_odometer`.** [PROVEN-elsewhere] `Suffix.lean`'s
`generation_odometer` is **NOT a well-founded recursion** — it is a single
case-split `M(G,a) → M(⌊4G/3⌋+c, a+δ)` composing FIXED episodes (`intro2`,
`seam8`, `capEnter4`, …) with parametric-but-LINEAR sweeps (`sweepBF`, `sweepAD`),
and it explicitly **leaves the iteration open** (the a-ledger conjecture). It has
no `μ`, no `termination_by`, no recursion at all past one generation. The x2
object is categorically bigger: it must (a) define a `List`-valued counter, (b)
prove it terminates by WF, and (c) prove a data-dependent ripple carry composes
the proven sweeps — i.e. it CLOSES exactly the iteration o4 never attempted.

---

## 5. Honest verdict [DESIGN]

**Is the WF recursion clean and implementable?** *Partly — with one genuine
subtlety, now precisely located.*

- **The MEASURE is clean, but ONLY on the pure register.** [decisive] The measure
  `μ = T − odoValue` is textbook and decreases by exactly 1 per tick; the ripple's
  inner measure (`#digits ≤ K`) is likewise clean. There is nothing subtle about
  *termination*. **But** the measure does **NOT** decode from the raw tape — every
  physical scalar is non-monotone (§2, quantified refutation on 523 830 real
  ticks). So a naive "shrinking tape number" WF does not exist; the cleanliness is
  bought by defining the counter abstractly and paying for it in faithfulness.

- **The genuine subtlety is faithfulness, not termination.** The shape-invariant
  `o.toCfg` must be preserved through a *data-dependent* carry whose tape window
  GROWS with the carried level and whose depth ripples (≤K). This is bounded and
  inductive — not non-localizable, not unbounded-data — but it is the biggest
  single Lean lemma the project has specified.

- **Feasibility.** The three inner sweeps (`ecombChewFold`, `sweepEF`,
  `dSweepTurn`) and the two arithmetic cores (`doubling_id`, `carryDigit_closed`,
  `cascadeBlocks_sum`) are DONE. The remaining build is: `odoNext`/`odoValue`
  (pure, ~1 session), `odo_terminates` (clean WF, ~1 session), `carry_step` (the
  hard one, the general-`j` ripple + left-summarization, ~2–3 sessions), and the
  `outer_step`+`doubling_phase` glue (~1–2 sessions). Total: a focused multi-
  session effort, dominated by `carry_step`.

**Bottom line.** The well-founded recursion is real, its termination is clean, and
its blueprint is above. It is NOT a single lemma and NOT the same species as
`generation_odometer` — it is the *closed* odometer iteration o4 left open, one
dimension up, gated on the general-`j` `carry_step`. The wall is now fully
specified: a verified ripple-carry incrementer whose carry unit is a proven
unbounded sweep, plus its left-deposit shape invariant.

No machine decided. No label upgraded.

**Probe scripts (this session):** `x2wf_measure.py` (odometer digit-vectors +
carry marks), `x2wf_counter.py` (binary-counter confirmation: cascade doubling,
level-halving carry profile), `x2wf_value2.py` (the monotonicity refutation of all
tape scalars), `x2wf_pure.py` (ripple-depth histogram). Built on
`x2bd_sim.py`/`x2bd_outer.py` (raw exact-bigint simulator = `X2.step`).
