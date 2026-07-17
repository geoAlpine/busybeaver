# The growing-arity impossibility: an audit of §5z / §5aa

**Date:** 2026-07-17
**Snapshot audited:** `lean/X2.lean` @ md5 `bcf2b4e2fb842d1d8d63c02414e329cc`, 6277 lines
(repo `HEAD` = `17ae7fc`; the file is being edited concurrently by another agent — md5
re-verified identical before and after the audit, and every line anchor below re-checked
against the live file).
**Probes (this audit, in repo root):** `x2az_tree9.py`, `x2az_gluelaw.py`, `x2az_tree10.py`,
`x2az_verify10.py`, `x2az_tree_ti.py`. All read-only w.r.t. `lean/`.

---

## Verdict in one paragraph

**§5z and §5aa, read literally, are SOUND — and they do not claim an impossibility.**
§5z's own words are "REGEN(k) is a genuine **WELL-FOUNDED TREE recursion**" whose closure is
"the **DEFINITIONAL NAMING** of that odometer-tree recursion". That is a statement of *work*,
not of impossibility. What it rules out — "a total structural `carryExit : Nat → transport`
with a **FIXED tuple** of recursive calls" — is true, and is a shape nobody needs.
**The artifact is not in §5z's Lean or its prose; it is in the program's RECORD of §5z.**
The zenodo v2.0 gloss ("growing-arity impossibility"; `carry_step`'s EXIT "admits no bounded
closure") escalates §5z/§5aa's narrow true claims into an impossibility they never proved and
that §5z's own text contradicts. That escalation is the fifth artifact — a **record-level**
one. Meanwhile the audit produced a **positive** result the program did not have: the ∀k glue
law, verified cell-for-cell two levels beyond the grounded range (§6). And `ebec409`'s
retraction of `da81f15`'s feasibility verdict does **not** survive (§4).

---

## 1. Method note: a real defect in how the tree was measured

`x2dt_tree8.py` / `x2ck_regen_seg.py` — the probes grounding `exitSteps_tree_5/6/7/8`,
`exitArity_grounds`, `exitList_grounds` — identify a "`REGEN(k')` recursive call" **by step
count alone**: an anchor gap of length `termSteps k'`, minus `exitSteps k'`. They never check
the window *is* the `REGEN(k')` transport.

**That criterion admits false positives** (`x2az_verify10.py`, `x2az_tree_ti.py`). Applying
the project's own translation-invariance criterion (`x2ck_regen_ti.py`: byte-identical
relative `(state, head, Δpos)` trace — which is what the Lean `∀ L R` statements mean), over
the first 620k steps of `build(2)`:

```
  REGEN(4):  32/32  windows are the genuine transport
  REGEN(5):  16/16
  REGEN(6):   8/8
  REGEN(7):   4/8   <-- FOUR FALSE POSITIVES
  REGEN(8):   2/2
  REGEN(9):   1/1
```

The false `REGEN(7)`-length windows are at `(55825,58355)`, `(155802,158332)`,
`(451865,454395)`, `(552867,555397)`: same length `2530`, ending in a `termSteps 7 = 139`
anchor gap, **different transport** — they are the descent re-cascade coincidentally matching
`exitSteps 7`.

*Consequence, stated fairly:* the `k ≤ 8` groundings **survive** — the false positives at
`k ≤ 9` all fall outside the decomposed windows, and the TI-filtered re-extraction reproduces
`exitSteps_tree_5/6/7/8` and `exitArity_grounds` exactly (`x2az_tree_ti.py`). But one false
positive **does** land inside `REGEN(10)` and inflates its apparent arity 15 → 16. **The
program should identify sub-calls by TI trace, not by step count.** This audit's own first
pass (`x2az_tree10.py`) was fooled by exactly this before the TI filter was applied — the
correction is recorded rather than hidden.

---

## 2. Q1 — What §5z actually establishes vs. infers

### (a) Machine-checked (all `[propext, Quot.sound]`-only, no `sorry`/axiom/`native_decide`)

| Theorem | Line | What it actually is |
|---|---|---|
| `exitSteps_grounds` | 4185 | `2^{2k−3}+k·2^{k−1}+2^{k−2}+2 = 70,218,722,2530,9282`, `k=4..8`. **Pure `Nat` `decide` on measured constants.** |
| `termSteps_grounds` | 4192 | ditto, `TERM(k)=24,41,74,139,268`. |
| `exitSteps_recurrence` | 4199 | the order-4 recurrence. Pure `Nat`. |
| `exitSteps_tree_5/6/7` | 4250/4256/4263 | **arithmetic identities among measured constants** (`by decide`). They do not mention the machine. |
| `regen4_transport` / `regen5_transport` | 4207/4221 | **real transports** — `carry_exit_j3`/`carry_exit_j4` re-stated `∀ L R` at `exitSteps 4/5`. Genuine content. |
| `regen_TI_generic` | 4238 | `⟨T L₁ R₁, T L₂ R₂⟩` — **applying a `∀`-statement twice.** A tautology of instantiation, not evidence of TI. (The TI *evidence* is `x2ck_regen_ti.py`, simulator.) |
| `carryExit_wf_frame` | 4275 | `= carry_level_rec hbase hstep`, i.e. `Nat.le_induction`. |
| `exitArity_grounds` | 4413 | `(k−5)(k−4)/2 = 0,1,3,6`. Pure `Nat`. |
| `exitArity_exceeds_four` | 4422 | **`4 < 6 ∧ 6 < 10`** (evaluated: `exitArity 8 = 3·4/2 = 6`, `exitArity 9 = 4·5/2 = 10`). Arithmetic on constants. |
| `exitSteps_tree_8` | 4429 | arithmetic identity. |
| `exitList_grounds` etc. | 4611+ | `[], [4], [4,5,4], [4,5,6,4,5,4]`. Pure `List`. |
| `exitSteps_foldl_closure` | 4652 | `exitSteps k = (glueSegs k).sum + foldRegenSteps k` **at k=5,6,7,8 only** — see §5. |

### (b) Simulator-measured

The `REGEN(k)` window segmentation, the call lists, the glue segment lengths, and REGEN(4)/(5)
translation-invariance — all from `build(2)` via the greedy step-count cover (§1's caveat).

### (c) Inferred — and the inference examined

The load-bearing sentence (**line 4157–4161**):

> "So `REGEN(k)` is a genuine WELL-FOUNDED TREE recursion whose arity is not `∀k`-constant;
> it is NOT a straight-line `∀k` transport, and a total structural `carryExit : Nat →
> transport` with a **FIXED tuple** of recursive calls does not exist."

and (**line 4304–4315**):

> "`REGEN(k)` is translation-invariant (PROVEN reusable) and well-founded (each call strictly
> lowers `k`), but its recursive-call ARITY grows with `k` …, so the closure is the
> **DEFINITIONAL naming** of that odometer-tree recursion — the project's `Suffix.lean`-scale
> object."

**These are sound.** They say: no *fixed-arity straight-line* transport; the object is a WF
tree recursion; closing it is a naming/definitional task. §5z explicitly calls it
**well-founded** and explicitly calls the remaining work **definitional naming**. It never
says "no closure exists".

**Is a named support a tautology on constants?** Yes — `exitArity_exceeds_four` is literally
`4 < 6 ∧ 6 < 10`, the same *pattern* as §5ab's retracted `glue_height_grows` (`28+4 = 2^5`)
and `descent_glue_unbounded` (`3·1089 < 4152`). **But the logical situation differs.** §5ab
adduced its tautologies for a conclusion they did not support (non-parametricity) — a
non-sequitur. §5aa adduces `exitArity_exceeds_four` for the claim *"the arity is not ≤4"*,
which it does support. It is **weak, not fallacious**.

**Where the fallacy actually lives:** in the escalation, recorded in commit `d190117` /
zenodo v2.0, from

- §5z/§5aa: *"no **fixed-arity** transport recursion"* (true, narrow), to
- the record: *"the **growing-arity impossibility**; `carry_step`'s EXIT **admits no bounded
  closure**"* (a non-sequitur of precisely §5ab's shape: growing arity ⇒ no closure).

**Growing arity ≠ non-closability**, exactly as growing length ≠ non-parametricity.

---

## 3. Q2 — Does growing arity obstruct a Lean recursion? **No — and the file proves it.**

The decisive refutation is **already inside `lean/X2.lean`**, at §5ab line 4589:

```lean
def exitList : Nat → List Nat
  | k + 6 => List.range' 4 (k + 1) ++ exitList (k + 5)
  | _ => []
```

This is a **total, structural, Lean-accepted definition whose output length is unbounded**
(`exitList_length_eq_arity`: length = `exitArity k`, which §5aa proves exceeds every
constant). The growing-arity object §5aa said had "no ≤4 closure" **is defined, GREEN, in the
same file**, together with a total fold over it (`foldRegenSteps`, line 4626). §5ab says so in
terms (line 4497): *"§5aa's arity obstruction dissolves."*

So §5aa's successor section **already conceded** the point, and the zenodo record did not
follow. A `∀k` WF recursion over `Nat.strongRecOn` with a `foldl` over `exitList k` handles
unbounded arity **by construction** — each element is `< k`, so each supplies the IH.

**What SPECIFICALLY fails (naming obligations, not growth):**

1. **`∀k` well-foundedness of the fold.** `exitList_wf_grounds` (line 4624) proves
   `∀ x ∈ exitList k, x < k` **only at `k = 7,8`, by `decide`.** The `∀k` version is unproven.
   *Assessment: trivial* — the max element of `exitList k` is `k−2`; a one-line induction on
   the `exitList` equation. (Lean will want `List.attach`/`Nat.strongRecOn` to thread the
   membership proof into the fold — routine.)
2. **`∀k` glue law.** `glueSegs` (line 4640) is **a 4-entry lookup table**, not a function
   (§5). **This is the real gap** — and this audit closes it empirically (§6).
3. **`∀k` transport-level induction** — the actual substance (§7).

**None of these is "the arity grows".**

---

## 4. Q3 — Does `ebec409`'s retraction of `da81f15` survive? **No.**

- `da81f15` (2026-07-16): the doubly-nested EXIT recursion *"STRATIFIES into a finite
  constructible WF recursion"*; unified measure `k²+a` PROVEN; **named remaining work: "the
  descentGlue transport (bounded, no new math)"**.
- `ebec409` (2026-07-16) retracted that as over-optimism. **Its stated reason:** "the TOPGRIND
  is `Θ(4^a)` = the CORE doubling-braid wall re-encountered INSIDE the descent".

**That reason is now void, by the file itself:**

- §5af (line 5387, 2026-07-17): *"THE TOPGRIND CLOSES"*.
- §5ag (line 5637, 2026-07-17): `descent_glue` (line 5889) — *"TOPGRIND ∘ lower fold ∘ FINAL
  as ONE `∀N d Lc` transport"* — proves the **whole descent family**, including the `1089`/
  `4152` that §5ab adduced as unbounded.
- The measure `uMeasure k a = k² + a` (line 4816) is proven (`uMeasure_outer`/`uMeasure_inner`).

So `da81f15`'s **named remaining work is DONE**, and the only objection ever raised against
its verdict has been withdrawn by the file. **`ebec409`'s retraction is void; `da81f15`'s
feasibility verdict is restored** — not by optimism, but because its successor's sole stated
reason is now a proven theorem in the opposite direction.

*Honest qualifier:* "restored" means the *feasibility* verdict, i.e. "no new mathematics is
required". It does **not** mean the recursion is closed. §7 states what is left.

---

## 5. A concrete, reproducible defect: `exitSteps_foldl_closure` does not extend

`glueSegs` (line 4640) is a table with `| _ => []`. Therefore at `k = 9`
(`x2az_gluelaw.py`, and directly):

```
  exitSteps 9                       = 35202
  (glueSegs 9).sum + foldRegenSteps 9 = 0 + 4908 = 4908       ->  35202 ≠ 4908
```

`exitSteps_foldl_closure` is a **4-point grounded statement that is FALSE at `k=9` as
currently defined** — not because the mathematics fails, but because `glueSegs` has no `∀k`
definition. The missing glue sum is exactly `30294`, which is precisely the sum of the
measured `glueSegs 9 = [799,215,935,3911,16431,215,935,4152,215,1089,1397]`
(`x2az_tree9.py`). **This — not the arity — is the `∀k` object that was missing.**

Related: `exitArity_exceeds_four` cites `exitArity 9 = 10`, but `exitArity` was grounded in
Lean only at `k ≤ 8` (`exitArity_grounds`). Until this audit, `exitArity 9 = 10` was an
**ungrounded extrapolation of a 4-point fit**. It is now confirmed on the orbit (§6) — the
theorem was not entitled to it when written, and now is.

---

## 6. The positive result: the `∀k` glue law, confirmed **two levels beyond** the grounded range

### 6a. `exitList` / `exitArity` continue at `k = 9` and `k = 10` (`x2az_tree9.py`, `x2az_tree_ti.py`)

TI-filtered extraction from `build(2)` (620k steps):

```
k=5   arity=0  (exitArity 0 )  calls=OK glue=OK sum=OK
k=6   arity=1  (exitArity 1 )  calls=OK glue=OK sum=OK
k=7   arity=3  (exitArity 3 )  calls=OK glue=OK sum=OK
k=8   arity=6  (exitArity 6 )  calls=OK glue=OK sum=OK
k=9   arity=10 (exitArity 10)  calls=OK glue=OK sum=OK   <-- BEYOND the Lean grounding range
k=10  arity=15 (exitArity 15)  calls=OK glue=OK sum=OK   <-- BEYOND the Lean grounding range
```

`REGEN(9)` window `(105303,140505)`, `REGEN(10)` window `(401120,537570)`.
`exitList 10 = [4,5,6,7,8,4,5,6,7,4,5,6,4,5,4]` — **confirmed cell-for-cell**.

### 6b. Every glue segment is a fixed transport keyed by its `(from → to)` transition

`x2az_tree9.py` classifies all segments at `k=5..9`; each transition type has ONE length at
every occurrence. Fitting closed forms and testing them:

| transition | closed form | grounded at |
|---|---|---|
| `START→4` | `3·2^{k−1} − 9k + 112` | `k=6,7,8,9` → `154, 241, 424, 799` |
| `4→END` | `termSteps k + 359 = 2^{k+1}+k+364` | `k=6,7,8,9` → `498, 627, 884, 1397` |
| `a→a+1` (ascend) | **`4^a − 3·2^a + 7`** | `a=4,5,6` → `215, 935, 3911` |
| `a→4` (descend) | `descentSteps a = 4^a − 9a + 110` | `a=5,6,7` → `1089, 4152, 16431` |

The last is **already `∀`-proven** (§5ag `descent_glue`, `descentSteps_grounds`). The `4→END`
form decomposes as the `∀`-proven `TERM(k)` plus a **fixed** `359` motif — exactly what §5ab's
prose asserted, now exact. `START→4` is the `∀`-proven descent-fold.

### 6c. The law is **predictive**, not a fit (`x2az_tree10.py` + `x2az_tree_ti.py`)

Fitted on `k ≤ 9`, the law predicted the **entire** `k=10` decomposition with no free
parameters — including two transitions occurring **nowhere in the fit data**:

```
  7→8 (ascend)  = 4^7 − 3·2^7 + 7 = 16007     CONFIRMED on the orbit
  8→4 (descend) = descentSteps 8   = 65574     CONFIRMED on the orbit
  glueSegs 10 = [1558,215,935,3911,16007,65574,215,935,3911,16431,215,935,4152,215,1089,2422]
```

All confirmed cell-for-cell after TI filtering. **This is genuine predictive confirmation.**

### 6d. The fold closes `∀k` as an exact arithmetic identity (`x2az_gluelaw.py`)

```
  exitSteps k  ==  sum(glueSegs_law k) + foldRegenSteps k
```
holds **exactly for every `k` in 5..40** (arity up to `exitArity 40 = 630`; `k=40` both sides
`= 151115727474093757300738`).

**Status discipline:** `k=5..10` is *orbit-measured, TI-verified*. `k=11..40` is the
*arithmetic identity of the closed forms* — it shows the law is not a coincidence of the
measured levels; it is **not** orbit evidence. The identity is `∀k`-provable in Lean by
induction on the `exitList` equation (both sides have closed forms) — **bounded work, not new
mathematics** — but it is **not proven** and I do not claim it.

---

## 7. The honest core: what actually remains

The growing arity is not the obstruction; the `exitList` recursion carries it, GREEN. The
remaining object is **ONE strong-induction step**:

> `∀ k ≥ 6, (∀ k' < k, P k') → P k`, where
> `P k := REGEN(k)` carries `cascadeReg`-shape IN to `cascadeReg(k+1)`-shape OUT in
> `exitSteps k` steps, halt-free.

with the fold over `exitList k` supplying the lower calls (each `< k` ⇒ IH).

**The apparent circularity is not one.** §5ab says the transport fold's open piece is the
`toCfg` threading = `∀k` reachability of `cascadeReg(k)`; §5ah (line 6024) says `∀k`
reachability needs `REGEN(k)`'s OUT `∀k`, which is the tree. Read as separate obligations
that is a cycle — but read as **one simultaneous strong induction on `k`** it is the normal
shape of an inductive proof. This is worth stating plainly: the program has been treating a
single induction as two mutually-blocking walls.

**The four inputs, with honest status:**

| input | status |
|---|---|
| the call-list recursion `exitList`, arity, self-similarity | **GREEN** (§5ab), + confirmed `k=9,10` here |
| `∀k` fold well-foundedness (`∀ x ∈ exitList k, x < k`) | **OPEN, trivial** — grounded `k=7,8` only |
| descend glue `a→4` | **`∀`-PROVEN** (§5ag `descent_glue`, `∀N d Lc`) |
| `START→4` (descent-fold), `TERM(k)` | **`∀`-PROVEN** (§5w, §5y) |
| **ascend glue `a→a+1 = 4^a − 3·2^a + 7`** | **OPEN — and it has no lemma and no name** |
| `∀k` glue-law arithmetic identity (§6d) | **OPEN, bounded** — law supplied here, unproven |
| `cascadeReg(k)` shape threading | **OPEN at `∀k`**; GREEN at `k=4,5` (§5ah) |

**The sharpest constructive finding: the ascending glue is the one unnamed object.** §5ab
recorded `4→5 = 215` and `5→6 = 935` as *"CONSTANT byte-identical"* fixed motifs and stopped
there — it never noticed they are one family. They are: `4^a − 3·2^a + 7`, confirmed at
`a=4,5,6` and *predicted then confirmed* at `a=7` (`16007`). It is §5ab's "CORE `sweepEF`
build-up of height `2^h−4`" — and `sweepEF` is already a `∀m` lemma over exactly such a
family, so this is **plausibly** the same move as §5ag's. *Plausibly. Unproven.* **This is
where the program should spend next.**

---

## 8. Answers, direct

1. **What does §5z argue; is it valid?** That `REGEN(k)` is a well-founded tree recursion of
   non-constant arity, so no *fixed-tuple straight-line* `carryExit` exists, and closing it is
   a definitional naming task. **Valid, and not an impossibility claim.**
   `exitArity_exceeds_four` **is** arithmetic on constants (`4 < 6 ∧ 6 < 10`) — weak, but
   adduced for a claim it supports, unlike §5ab's.
2. **Does growing arity obstruct a Lean recursion?** **No.** `exitList` — a total Lean
   definition of unbounded length, in this very file — is the counterexample. §5ab already
   conceded it ("§5aa's arity obstruction dissolves"). The failing obligations are the `∀k`
   glue law, `∀k` fold well-foundedness, and the `cascadeReg` threading — none is growth.
3. **Does `ebec409`'s retraction survive?** **No.** Its sole stated reason (TOPGRIND =
   `Θ(4^a)` wall) is refuted by §5af/§5ag. `da81f15`'s named remaining work is done.
   Its feasibility verdict stands.
4. **The honest inverse.** The wall is **not** confirmed. What remains is real but is one
   strong induction with one unnamed input (the ascending glue `4^a − 3·2^a + 7`), and there
   is no evidence it needs new mathematics.

**The program's `[OPEN]` label is correct and must stay** — the `∀j` carry is not
machine-checked. But the *reason recorded* for it — a growing-arity impossibility — is not
sound, and the open object is **substantially smaller** than the record states.

---

## 9. Reproduction

```bash
PY=/Users/aokiyousuke/quantum-ecc/.venv/bin/python
$PY x2az_tree9.py 200000      # exitList/exitArity continue at k=9; transition-typed glue
$PY x2az_gluelaw.py           # the four closed forms; the fold closes k=5..40; k=10 prediction
$PY x2az_tree10.py 620000 10  # k=10 by step-count cover -> apparent arity 16 (false positive)
$PY x2az_verify10.py          # TI test: 4/8 REGEN(7)-length windows are false positives
$PY x2az_tree_ti.py 620000 10 # TI-filtered: exitList/exitArity/glue law exact at k=5..10
```

No machine decided. No label upgraded.
