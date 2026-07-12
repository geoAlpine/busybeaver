# The outer-braid induction of the integer-×2 doubling phase — a DESIGN BLUEPRINT (2026-07-12)

*Machine `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`. Analysis + design for a future Lean
formalization of the OUTER induction of the doubling phase `M6(g) → M1(g+1)`. The inner
comb-shrink (`ecombChewFold`, lean/X2.lean §5i) is formalized on-path; this document
characterizes what the OUTER induction needs, from RAW traces (`x2bd_*.py`, raw simulator
matching `X2.step`, exact big-int). STRICT [OBSERVED]/[PROVEN]/[DESIGN]. This decides no
machine and edits no Lean. Supersedes nothing; complements X2_STATUS_2026-07-12.md §2–4.*

---

## 0. Executive verdict (§5 in full below)

**A clean FINITE-DIMENSIONAL outer state EXISTS, so the braid IS formalizable in
principle** — but as a NESTED ODOMETER induction, NOT a `steps_add`-tile and NOT a
`List`-fold. The outer index ranges over **Θ(2^K)** ticks (not the ~K cascade blocks), each
tick invoking the inner `ecombChewFold`/`sweepEF` over Θ(2^K) cells — the Θ(2^{2K}) double
induction. The state localizes to `(cascade-digit list : List Nat, comb-pairs : Nat, a
bounded head-window, pos)`; the register is consumed once in the entry and is NOT carried.
The obstruction is not non-localizability — it is that `outer_step` is itself an
unbounded-length sweep with **data-dependent carry propagation**, so the outer induction is
an odometer exactly like o4's `generation_odometer`, but with a **`List`-valued (K-dimensional)
carry register** instead of o4's 2-D linear `(G,a)`. Feasibility: **strictly harder than
o4-Suffix, but the same species** — a multi-session Lean effort, not a single lemma, and not
non-inductive.

---

## 1. The outer state, characterized exactly [OBSERVED, raw g=2,3,4]

**Provenance.** `x2bd_sim.py` raw-simulates `X2.step` with exact big-int; it reproduces the
documented anchors exactly: M6(2) at raw step 343, M1(3) at 2 119 358, phase = 2 119 015 =
Θ(2^{2K}), K=10 (`x2bd_sim.py 2`). All numbers below are from `x2bd_trace.py`,
`x2bd_outer.py`, `x2bd_odom.py`, `x2bd_value.py`.

**The recurring anchor.** During the phase the head returns, Θ(2^K) times, to **state `E`
reading a `0`** at the boundary between a growing `(01)`-comb on the LEFT and the leading
cascade block `1^{2v+1}` on the RIGHT. This is the outer round-trip boundary. Between two
consecutive anchors the machine runs one inner `ecombChewFold` (block → comb) plus a
repack/carry.

**The outer index.** The number of anchors that are *chew-starts* (local maxima of the
leading block length) — i.e. the odometer **tick count** — scales as (`x2bd_odom.py scale`):

| g | K | 2^K | round-trips | ratio to 2^K | E-on-0 anchors | ratio to 2^{2K} |
|---|---|-----|-------------|--------------|-----------------|-----------------|
| 2 | 10 | 1024 | 3 852 | 3.76 | 523 831 | ~0.5 |
| 3 | 11 | 2048 | 9 729 | 4.75 | 2 106 355 | ~0.5 |
| 4 | 12 | 4096 | 19 470 | 4.75 | 8 386 623 | ~0.5 |

Round-trips **≈ double per g = Θ(2^K)**; anchors **≈ ×4 per g = Θ(2^{2K})**. The outer loop
is therefore **exponentially long in K** — the decisive fact: it is NOT a fold over the
`K−2 = g+6` cascade blocks (that would be linear in K). The extra factor is the odometer
re-creating and re-chewing blocks via carries.

**The outer-state tuple (the localization).** At every anchor the full config is captured by
a fixed-shape tuple (`x2bd_odom.py digits`, `x2bd_value.py`):

```
OuterState(K) =
  ( digits : List Nat        -- cascade block lengths, big→small (the odometer register)
  , comb   : Nat             -- pending (01)-comb pairs deposited on the LEFT
  , resid  : Nat             -- 1^1 chew residues / separators (bounded shape-vocabulary)
  , pos    : Int )
```

- At M6: `digits = [2^K−3, 2^{K−1}−3, …, 2^2−3] = [1021,509,253,125,61,29,13,5,1]` (g=2),
  `comb = 0` (`x2bd_odom.py digits 2`, row n=490).
- The **register `(1^5 0^2)^{g−1}`** (`1000000^{g-1}` in `m1_spec`) is consumed in the entry
  (raw steps ~352–490 for g=2, blocks 9,7,5,5,5,1) and **does NOT reappear** — the steady
  odometer runs purely on the cascade. [OBSERVED: post-entry digit-vectors contain no
  register unit.]

**Finite-dimensionality is real despite unbounded tape length.** The LEFT deposit grows to
Θ(2^K) cells (`x2bd` left-skeleton length up to 2058 at K=10), but its *shape vocabulary is
bounded*: it is a `(01)^comb` comb with a bounded set of `1^1`/separator decorations. Hence
the whole left side is summarized by the single Nat `comb` (+ a bounded `resid`), exactly as
`sweepEF` re-reads `(01)^m` uniformly. **So the outer state is a fixed tuple of Nats/Lists —
not the whole tape.**

---

## 2. The invariant [OBSERVED + PROVEN pieces already in Lean]

**No single `+c` scalar telescopes** (the encoding is redundant and head-relative: the
right-value first-differences are `±2^{Θ(K)}·(data-dependent)`, `x2bd_value.py`). What DOES
behave cleanly:

- **`comb` (the accumulator) climbs monotonically** across the phase (`Lones`: 7,8,9,…,534,
  789,916,979,1010,1025,… with only small dips at carries) — the odometer OUTPUT register
  filling. [OBSERVED]
- **`total-ones` roughly DOUBLES**: 2046 at M6 → 4065 at M1(g+1) — the `2^K−3 → 2^{K+1}−3`
  net, realized as the sum over Θ(2^K) ticks. [OBSERVED] (It dips to ~1036 mid-phase: each
  chew HALVES the one-count `2v+1 → v+1`, each `sweepEF` DOUBLES it `m → 2m`; net over a
  tick ≈ neutral, and the doubling comes from the carry recombination, not any single tick.)

**The genuine invariant is the odometer VALUE, not a tape scalar.** The cascade `digits`
form a mixed-radix counter; one tick performs `value ↦ value + carry`. The net boundary
values are the milestone values, and the Lean arithmetic core is ALREADY proven:
- `doubling_id`: `2·(2^K−3)+3 = 2^{K+1}−3` (the big-block ×2 law). [PROVEN, Lean]
- `cascadeBlocks_sum`: `Σ digits = 2^{K−1} − 4K + 8` (the telescoping accumulator closed
  form). [PROVEN, Lean]
- `inner_is_linear_not_quadratic`: `2·(2^{K−1}−2)+1 = 2^K−3` (the inner chew length).
  [PROVEN, Lean]

These are the boundary/telescoping identities the outer invariant must hit; the missing
piece is the **value-accounting lemma** wiring the Θ(2^K)-tick carry sum to them.

**Candidate "register-remaining + cascade-remaining + comb-built = const" is REFUTED as
posed**: that sum is `total-ones`, which doubles, not constant [OBSERVED]. The correct
conserved object is the *weighted* odometer value, whose weights are the `2^j` gap positions
— exactly what makes it un-representable in the affine Python executor and why it needs Lean
`Nat`/`2^K` arithmetic (as `doubling_id` already demonstrates).

---

## 3. The nesting structure [DESIGN]

```
outer_phase :  OuterState_entry  --Θ(2^K) ticks-->  OuterState_exit(= M1(g+1))

outer_step(t) :  OuterState(t) → OuterState(t+1)          -- ONE odometer tick
   = ecombChewFold  (INNER: chew leading block 1^{2v+1} → (01)^v · 1^1, 6v steps)   -- §5i, PROVEN ∀v
   ∘ sweepEF        (INNER: repack a (01)^m comb → 1^{2m}, 2m steps)                -- §4, PROVEN ∀m
   ∘ carry          (add 1 to the next digit; if it overflows, RECURSE into the next digit)
```

- `outer_step` is **NOT a fixed-length tile**: its inner factors sweep Θ(2^K) cells, and the
  `carry` recurses through a **data-dependent number of digits** (the classic binary-counter
  variable carry length). [OBSERVED: carries regenerate blocks 5→13→29→61→… at comb-pair
  counts 3,7,15,31 = `2^j−1`, `x2bd_outer.py`.]
- The double induction is: **inner** = length induction over one block (both inner factors
  already PROVEN ∀ length in Lean); **outer** = odometer induction over `digits` with a
  carry sub-recursion. Θ(2^K) outer × Θ(2^K) inner = Θ(2^{2K}), matching the raw counts.

This is precisely the shape of o4's `generation_odometer` (`lean/Suffix.lean`) — an
odometer whose per-tick map is proven by inner sweep lemmas — **except** o4's register is the
2-D linear `(G, a)` with the affine ledger `a ↦ a + δ(G mod 3)`, whereas x2's register is the
**`List Nat` cascade with a carry-propagating update**. Same species, higher dimension.

---

## 4. The Lean blueprint [DESIGN]

```lean
/-- The outer odometer register: cascade block lengths big→small, + pending comb. -/
structure Odo where
  digits : List Nat          -- e.g. [2^K−3, 2^{K−1}−3, …, 1]
  comb   : Nat               -- (01)-pairs on the left (summary of the unbounded deposit)

/-- Decode an Odo (+ opaque tail T, + head pos) to the on-anchor Cfg:
    state E on the boundary 0, left = pow01 comb ++ residues, right = casc digits T. -/
def Odo.toCfg (o : Odo) (pos : Int) (T : List Bool) : Cfg := …

/-- ONE ODOMETER TICK.  Chew the leading digit (ecombChewFold), repack (sweepEF),
    propagate the carry into `digits`.  `some ⇒ HALT-FREE`. -/
theorem outer_step (o : Odo) (pos) (T) :
    ∃ N pos', steps N (o.toCfg pos T) = some ((odoNext o).toCfg pos' T)      -- the hard lemma

/-- odoNext : the pure-arithmetic carry update on the register (the odometer law). -/
def odoNext : Odo → Odo := …          -- binary-counter increment with carry

/-- THE OUTER INDUCTION: iterate outer_step to the fixpoint = M1(K+1). -/
theorem doubling_phase (K) (pos) (T) :
    ∃ N pos', steps N (odoEntry K |>.toCfg pos T) = some (M1 (K+1) …)
  -- by well-founded recursion on the odometer value (strictly decreasing to the milestone),
  -- net value 2^K−3 → 2^{K+1}−3 supplied by doubling_id + cascadeBlocks_sum + the carry sum.
```

Assembly of the boundary value: `doubling_id` (big-block ×2) + `cascadeBlocks_sum`
(telescoping accumulator, carrying the `−4K+8` correction) + a new `carry_sum` lemma
(Σ of the Θ(2^K) tick carries = the residual `Θ(K)` that `bigCascade_not_doubling` isolated)
⟹ the net `2^{K+1}−3`. `sweepEF`, `ecombChewFold`, `dSweepTurn` (all PROVEN ∀ length)
discharge the inner factors of `outer_step`.

**HARDEST SUB-LEMMA: `outer_step` with the carry.** Two coupled difficulties:
1. **The left-deposit summarization** — proving the unbounded left stays a clean
   `pow01 comb ++ (bounded residue)` across every tick, so `Odo` really is a faithful
   invariant (not a leaky abstraction). Empirically true [OBSERVED: bounded shape-vocabulary]
   but needs a preserved-shape invariant lemma over the whole odometer, itself an induction.
2. **The data-dependent carry** — `outer_step` is not one closed form: it branches on whether
   the leading digit's repack overflows into the next, recursing. In Lean this is a
   `WellFounded` recursion on the register with the carry as an inner induction — analogous
   to a verified binary-incrementer, but with each "bit flip" being a Θ(2^K)-step
   `sweepEF`/`ecombChewFold` composite rather than a constant.

**Feasibility estimate.** `outer_step`'s inner factors are DONE (o4-scale, already in the
file). The carry-recursion + left-summarization + value-telescoping is **1.5–2× the
`generation_odometer` effort** (that was ~700 lines for a 2-D linear odometer; x2 adds a
`List`-valued register and a carry recursion, but reuses the proven sweep lemmas). Estimate:
a focused multi-session effort, comparable to porting the whole `Suffix.lean` generation map.
**Not** a single lemma; **not** intractable; **not** non-inductive.

---

## 5. Honest verdict [DESIGN]

**A clean finite-dimensional outer invariant EXISTS.** The outer state is the tuple
`(digits : List Nat, comb : Nat, resid : Nat, pos)` — the register consumed in entry, the
left deposit summarized by a single Nat (bounded shape-vocabulary, [OBSERVED]), the cascade a
`List Nat`. The braid is therefore **formalizable in principle**, as an **odometer double
induction**: an outer well-founded recursion on the odometer value (Θ(2^K) ticks), each tick
the proven inner `ecombChewFold ∘ sweepEF` plus a data-dependent carry, with the net
`2^K−3 → 2^{K+1}−3` assembled from the already-proven `doubling_id` + `cascadeBlocks_sum`
plus a new carry-sum lemma.

**The braid is NOT genuinely non-localizable** — X2_STATUS §5h's "does not localize into a
`steps_add`-tile or `List`-fold" is CORRECT and remains correct (it is neither of those), but
the stronger reading "irreducibly the whole tape" is **too pessimistic**: the state reduces to
a fixed tuple. What §5h correctly identified is that `outer_step` is not a *fixed-length tile*
and the outer loop is not a *K-length fold* — both true, and both consistent with an odometer
formalization. The right frame is **o4's `generation_odometer`, one dimension up**: a
`List`-valued carry register instead of a 2-D linear one.

**Consequence for the first decision.** This route IS reachable, but the remaining work is a
genuine odometer-with-carry formalization (the hardest sub-lemma being `outer_step`'s carry
recursion + the left-deposit preserved-shape invariant), on top of the still-open low-phase
port (`H_entry`) and the top-level `x2_nonhalt` assembly. The wall is now a *specified*
induction, not an unknown — but it is the biggest single Lean object the project has faced.

No machine decided. No label upgraded.

**Probe scripts (this session):** `x2bd_sim.py` (raw exact-bigint simulator = `X2.step`),
`x2bd_trace.py` (C-turn snapshots), `x2bd_outer.py` (E-on-0 anchors + scalar candidates),
`x2bd_odom.py` (round-trip scaling + digit-vectors), `x2bd_value.py` (value-telescoping test).
