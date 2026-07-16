# X2 UNIFIED RECURSION DESIGN — the doubly-nested EXIT recursion of `carry_step`

**Machine.** `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` (integer-doubler).
**Date.** 2026-07-16. **Scope.** FEASIBILITY DESIGN STUDY of the last open object of
`carry_step` — the doubly-nested EXIT recursion. On-path throughout: every structure claim
is grounded cell-for-cell on the faithful `build(2)` orbit; the j=3/j=4 cross-check
(`carry_exit_j3` = REGEN(4), `carry_exit_j4` = REGEN(5)) is reproduced. **No machine is
decided; no label is upgraded.** New probes: `x2ur_descent.py`, `x2ur_sweep.py`.

---

## 0. Where §5ab left it, and the one question this study answers

§5ab (GREEN) established that the EXIT is a growing-arity digit-tree recursion whose
**call-list** `exitList(k) = [4,…,k−2] ++ exitList(k−1)` is a clean total `Nat`/`List`
recursion and whose **step-count `List.foldl` closes**
(`exitSteps k = (glueSegs k).sum + foldRegenSteps k`). The single open object it localized
was the **transport-level fold**, blocked by the *per-position glue family* `glue(a,b)` — a
"growing CORE re-cascade" of unbounded, position-dependent height — plus its `toCfg`
threading. The doubly-nested shape: an OUTER list-fold over `REGEN` whose between-call glue
is ANOTHER instance of a growing re-cascade (the odometer carry-completion, the DESCENT
transitions `a→4`, growing `Θ(4^a)`).

This study answers the decisive question §5ab left open: **is the glue family reducible to a
finite, well-founded recursion that unifies with `REGEN` — or does the self-similarity
genuinely resist a finite Lean recursion?**

---

## Q1 — Is the descent glue `a→4` reducible to `REGEN`? **NO — it is a genuinely DIFFERENT, REGEN-FREE function (a pure cascade descent-fold).**

**Extraction (cell-for-cell, `x2ur_descent.py`, from `build(2)`, anchors to n≈141000).**
The descent glue `a→4` was located inside REGEN(7)/(8)/(9) and decomposed with the same
greedy largest-block REGEN/TERM/glue cover used in §5z/§5aa/§5ab:

```
  descent 5→4  [13453,14542]   len 1089   REGEN sub-calls = []   TERM sub-calls = [3,3]
  descent 6→4  [33830,37982]   len 4152   REGEN sub-calls = []   TERM sub-calls = [3,3]
  descent 7→4  [114703,131134] len 16431  REGEN sub-calls = []   TERM sub-calls = [3,3]
```

**DECISIVE FACT: every descent glue contains ZERO `REGEN` recursive calls** (only two
`TERM(3)=24` landmarks). Contrast `REGEN(k)` itself, whose arity `(k−5)(k−4)/2` is
UNBOUNDED (§5aa). So the glue is **not** a composition of lower `REGEN`s, and `REGEN` and
`glue` are **not** one self-referential recursion in the "glue = ∑ REGEN" sense.

**What the descent glue IS (`x2ur_sweep.py`).** A pure SWEEP with an arithmetic-progression
staircase — the classic odometer counting signature. Its anchor-gap "peaks" (>5) are exactly

```
  a=5:  8,12,16,…,60    (step 4, up to 2^{a+1}−4 = 60,  count 2^{a−1}−2 = 14)
  a=6:  8,12,16,…,124   (step 4, up to 124 = 2^7−4,     count 30)
  a=7:  8,12,16,…,252   (step 4, up to 252 = 2^8−4,     count 62)
```

The exponentially-many length-2 fillers between peaks dominate, giving a **clean closed
form** (unit leading coefficient — meaningful, not a fit artifact):

```
  descentSteps(a) = 4^a − 9·a + 110   =  1089, 4152, 16431   for a = 5,6,7   ✓ all three
```

Ratio `descentSteps(a) / exitSteps(a) → ∞` (4.99, 5.75, 6.49) — the descent is `Θ(4^a)`,
`≈8×` the `REGEN(a)` it descends from, NOT a sub-`REGEN`.

**VERDICT Q1.** The glue family is a genuinely different function from `REGEN`: a
**REGEN-free cascade descent-fold** (the odometer carry-completion re-cascade). The two
families are coupled **one-directionally** — `REGEN → {lower REGEN, descentGlue}` but
`descentGlue → {ticks / sweepEF / TERM only, NO REGEN}`. This one-directional coupling is
the linchpin of feasibility (see §Verdict): it makes the pair **stratifiable**, hence a
single finite WF recursion.

---

## Q2 — Does the self-similarity BOTTOM OUT into a FINITE recursion? **YES.**

Two independent finiteness facts:

1. **The OUTER `REGEN` recursion bottoms out at `REGEN(4)=carry_exit_j3`.** `exitList(k)`
   is a total structural `Nat` recursion (base `exitList(≤5)=[]`), every element `k'<k`
   (`exitList_wf_grounds`), reaching the base `4` in finitely many layers (§5ab, GREEN).

2. **The INNER descent glue bottoms out at cascade depth 0, calling NO new function type.**
   The descent `a→4` is a run over the descending cascade register (Q3), consuming one rung
   per phase, terminating at the base rung `1^1` (`TERM(3)` twice). It spawns **no** `REGEN`
   (Q1) and **no** deeper glue type — its self-similarity is a pure SWEEP:
   `x2ur_descent.py` finds `glue(6→4)` shares a **935-step common prefix** with `glue(5→4)`
   (of 1089) — the larger descent *replays the smaller descent's opening* then extends, the
   hallmark of a single WF sweep-recursion (measure = cascade depth), **not** a new function
   per layer.

So the nesting terminates: OUTER at `k=4`, INNER at depth `0`, after finitely many layers
for each `k`. No layer spawns a genuinely new function type — there are exactly **two**
function types (`REGEN`, `descentGlue`), both bottoming out. **A finite mutual/stratified WF
recursion is therefore constructible in Lean** (§Verdict).

---

## Q3 — The `toCfg` threading invariant. **A single cascade-register shape works, `carryCfg (k, a)`.**

**The descent register is EXACTLY a descending cascade (`x2ur_sweep.py`, Lean-`Cfg` snap).**
At the START of `descentGlue(a)` the right tape is, cell-for-cell,

```
  R = 0^3 · 1^{2^a−3} · 0^2 · 1^{2^{a−1}−3} · 0^2 · … · 0^2 · 1^5 · 0^2 · 1^1   (depth a)
        one-block heights (top→down):  a=5 → [29,13,5,1]  = [2^5−3,2^4−3,2^3−3,2^2−3] ✓
                                       a=6 → [61,29,13,5,1]                             ✓
```

This is precisely the **`cascadeTail` / `Odo` odometer register** already in the vocabulary
(`Odo.toCfg`, §5n: left `1^{2t+1} 0 M`, right `1^{work} 0^2 R`; here the whole descending
cascade is the register). At the END the register is consumed to `R = 0 1 0` and the block
is folded onto the left (`|L| : 2117→2180` for a=5, `dpos = +63`).

**The single invariant.** A `carryCfg (k, a)` whose decode is:
`⟨E, pos, ⟨ pow01-comb ++ 1^{2t+1} 0 M , false , cascadeReg(a) ++ tail ⟩⟩`,
where `cascadeReg(a) = 1^{2^a−3} 0^2 cascadeReg(a−1)` (base `cascadeReg(1)=1^1`) is the
descending-cascade register of depth `a`. This is preserved by every step of the fold:
each `REGEN(k')` and each `descentGlue` step maps `carryCfg` to `carryCfg` with the register
depth reduced by one rung (descent) or the comb extended (regen). It **reproduces the
`carry_exit` configs**: `carry_exit_j3` = REGEN(4) has `cascadeReg` depth 4 (`pow10 14 ++ …`
in `regen4_transport`); `carry_exit_j4` = REGEN(5) has depth 5 (`regen5_transport`). The
`pow10`/`cascadeTail`/`ones` vocabulary the invariant needs is exactly the existing one.

**VERDICT Q3.** YES — one tape-shape invariant (the descending-cascade register
`cascadeReg(a)`, an instance of `Odo.toCfg`/`cascadeTail`) threads every position of the
fold. Threading it is the transport obligation (§Hardest sub-object), but the invariant
itself is pinned and consistent with the two proven concrete EXITs.

---

## Q4 — The unified termination measure. **A single lexicographic `(k, a)`, encoded `k²+a`.**

The recursion has two decreasing quantities: the OUTER block height `k` (each `REGEN(k')`
call has `k'<k`) and the INNER cascade depth `a` (each descent step drops one rung). The
descent depth always satisfies `a < k` (the descended cascade sits below the current block;
grounded: in REGEN(9) the descents are 7→4, 6→4, 5→4 with `a ∈ {5,6,7} < 9`).

**Unified measure** (self-contained `Nat`, no Mathlib `Prod.Lex` needed, since `a < k`):

```
  uMeasure k a := k*k + a
```

- **OUTER step** (`REGEN(k)` calls `REGEN(k')`, `k'<k`, that call's own depth `a'<k'`):
  `uMeasure k' a' = k'² + a' < k² + a = uMeasure k a`  (since `k'²+a' ≤ k'²+k'−1 <
  (k'+1)² ≤ k²`). Proven GREEN as `uMeasure_outer`.
- **INNER step** (descent depth `a → a−1`, `k` fixed):
  `uMeasure k a < uMeasure k (a+1)` trivially. Proven GREEN as `uMeasure_inner`.

Both the outer list-fold and the inner glue re-cascade strictly decrease `uMeasure`, tied to
the §5n `odo_terminates` WF (which is exactly "digits-left-to-carry ≤ K"). **VERDICT Q4.**
A single well-founded measure closes BOTH nestings.

---

## THE UNIFIED RECURSION DESIGN (the type(s), measure, invariant, recursive step)

**Two function types, stratified (one-directional coupling from Q1):**

```
-- STRATUM 1 (defined FIRST, independent of REGEN — Q1: no REGEN calls):
descentGlue : (a : Nat) → Transport          -- the odometer carry-completion re-cascade
  -- step count  descentSteps a = 4^a − 9a + 110         (Q1, grounded a=5,6,7)
  -- toCfg       consumes cascadeReg(a) → cascadeReg(0), folds block onto left  (Q3)
  -- recursion   a run of the ∀-proven odometer sweep, WF on cascade depth a (Q2)
  --   descentGlue(a) = [sweep rung 2^a−3] ∘ descentGlue(a−1) ∘ … ∘ TERM(3)
  -- pieces      outer_tick_noCarry_at (§5t, ∀-proven), sweepEF (§4, ∀m), TERM(3)

-- STRATUM 2 (defined SECOND, uses STRATUM 1 + lower REGEN):
regen : (k : Nat) → Transport                -- the level-k regeneration (= REGEN(k))
  -- step count  exitSteps k = 2^{2k−3}+k·2^{k−1}+2^{k−2}+2   (§5z, grounded 5 pts)
  -- call-list   exitList k = [4,…,k−2] ++ exitList(k−1)      (§5ab, GREEN)
  -- recursion   regen(k) = descentGlue-open(k)
  --                        ∘ foldl over exitList(k) of [ regen(k') ∘ connectorGlue ]
  --                        ∘ TERM(k)
  --   connectorGlue = ascending b→b+1 (bounded, §5ab: 4→5=215, 5→6=935 fixed transports)
  --                 + descending a→4 = descentGlue(a)  (STRATUM 1)
```

**Unified measure** `uMeasure k a = k*k + a`, lexicographic `(k,a)`, `a<k` (Q4). Strictly
decreases through the STRATUM-2 outer fold (`k'<k`) AND the STRATUM-1 inner descent
(`a→a−1`). WF ⇒ both recursions total.

**`toCfg` invariant** `carryCfg (k,a)` = `Odo.toCfg`-shaped config with descending-cascade
register `cascadeReg(a)` (Q3), preserved at every fold position, reproducing
`carry_exit_j3/j4`.

**Recursive step, composing PROVEN pieces:**
- STRATUM 1 step: one `outer_tick_noCarry_at` (§5t, ∀-proven) + `sweepEF` (§4, ∀m) on the
  register, dropping depth `a→a−1`; step count peels `descentSteps a → descentSteps(a−1)`.
- STRATUM 2 step: `regen(k)` = opening descent-fold (§5w, ∀-proven) ∘ `List.foldl` over
  `exitList` of `regen(k')` (recursion, `k'<k`) with `descentGlue`/connector glue between,
  ∘ `TERM(k)` (§5y, `termSteps` closed form). Base `regen(4) = carry_exit_j3`
  (`regen4_transport`, GREEN), depth-1 `regen(5) = carry_exit_j4` (`regen5_transport`).

---

## THE HARDEST SUB-OBJECT

**Not** the recursion structure (constructible — see Verdict) and **not** the measure
(GREEN, Q4). It is the single **transport-assembly obligation**:

> Prove `descentGlue(a)` equals the composed run of the ∀-proven odometer-tick / `sweepEF`
> pieces, at exact length `descentSteps(a) = 4^a−9a+110`, threading the descending-cascade
> `carryCfg` invariant from depth `a` down to depth `0` — i.e. the `sweepEF`-composite
> induction over the cascade register (the project's `Suffix.lean`-scale assembly).

Everything this obligation needs is in hand: the per-rung primitive is ∀-proven
(`outer_tick_noCarry_at`, `sweepEF`), the step-count peels cleanly (closed form), the measure
is WF (`uMeasure`), the invariant is pinned (`cascadeReg`), and the base is grounded
(`TERM(3)`). What remains is the *definitional threading* — the same character of work as
`Suffix.lean`, now with a fully specified type, measure, and invariant.

---

## FEASIBILITY VERDICT

**A single unified finite well-founded recursion that closes `carry_step`'s EXIT IS
CONSTRUCTIBLE.** The self-similarity does **not** resist a finite Lean recursion. The
decisive reason is Q1: the descent glue family is **REGEN-free** (verified cell-for-cell at
a=5,6,7), so the coupling `REGEN ↔ glue` is **one-directional** and the pair **stratifies**
into (1) `descentGlue` — a self-contained WF cascade-descent-fold, and (2) `regen` — a WF
list-fold over `exitList` using `descentGlue` + lower `regen`. Both bottom out (Q2), share
one `carryCfg` cascade-register invariant (Q3), and one lexicographic measure `k²+a` (Q4).
This is a *finite* recursion (two function types, both terminating), hence constructible —
in contrast to an infinitely-deepening tower, which is **not** what the orbit exhibits.

**The single remaining proof obligation** is the transport-assembly of `descentGlue` (the
`sweepEF`-composite cascade induction) — the hardest sub-object above. It is bounded,
composed of ∀-proven primitives, with a specified type/measure/invariant; it is
`Suffix.lean`-scale definitional work, not a new mathematical obstruction.

The GREEN Lean skeleton of this design — `descentSteps` closed form + grounding, the
glueSeg tie-in, and the unified WF measure `uMeasure` with both strict-decrease lemmas — is
added as **§5ac** in `lean/X2.lean`, `[DESIGN]`-labeled for the (unproven) transport, axiom
audited (`[propext, Quot.sound]`; no `sorry`/`native_decide`/`partial def`). The base (k=4)
and depth-1 (k=5) EXIT transports stay GREEN and reproduce `carry_exit_j3`/`carry_exit_j4`.

**No machine decided. No label upgraded.**
