# REGEN reach map — does the last x2 obstruction already exist in the file?

**Date** 2026-07-17 · **Snapshot** `e1dfbc7` (`lean/X2.lean`, 5982 lines, md5 `c0c20d5a4848d22111b278fcfe72cd7e`)
**Method** snapshot built in isolation (`scratchpad/snap`, `lake build X2` green); all Lean claims below are
kernel-checked via `lake env lean` against that snapshot. **No file under `lean/` was read-only-violated,
edited, staged or committed.**

> **Concurrency note.** While this audit ran, the sibling agent added **§5ah** (working tree, lines 5982–6261,
> uncommitted) which reaches the *same* core conclusion independently. My snapshot **predates** §5ah, so the
> Lean results in §1 below are an **independent replication**, not a restatement. Where they differ, mine is
> strictly more general (§1.4). Divergences are reported as *convergence*, not as defects.

---

## VERDICT (one line)

**YES — the last obstruction is already proven at `k=4` and `k=5`.** `regen4_transport` /
`regen5_transport`'s OUT **is literally** `descent_glue`'s IN. No connector, no new transport: it is an
**instantiation of already-`∀`-quantified tails**, `rfl`-level — the identical move that dissolved §5ag's
seam 1, §5ae, §5ad and §5ab. The `∀k` statement remains **[OPEN]**, and its residue is *exactly* §5z's
growing-arity odometer tree — not a new obstruction, and not a shape problem.

---

## 1. Q1 — do `regen4/5_transport` DELIVER the target shape?

### 1.1 The target (`descent_glue` IN, §5ag, X2.lean:5889)

```lean
⟨.E, p, ⟨pow01 (Lc + N) ++ marker, false,
    false::false::false::(ones (2*N+1) ++ (false::false::
      (descCascade (d+1) ++ (false::false::(zeros 7 ++ R)))))⟩⟩
```
with `N = 2^{k−1}−2`, `d+1 = k−3`. All of `N, d, Lc, p, marker, R` are **`∀`-quantified**.

### 1.2 Symbol-by-symbol (mechanical, `x2rm_regen_reach.py` — parses the cons-lists out of the source, no hand transcription)

| | `regen4_transport` OUT | `descent_glue` IN @ a=4 (N=6, d=0) | verdict |
|---|---|---|---|
| state | `.E` | `.E` | ✅ |
| head | `false` (boundary 0) | `false` | ✅ |
| pos | `-7` | `p` (∀) | ✅ `p := -7` |
| left | `0 1 0 ++ L` (L ∀) | `pow01 (Lc+6) ++ marker` | ✅ `L := 1 :: (pow01 (Lc+4) ++ marker)` |
| right | `0³ 1^13 0² 1^5 0² 1 0³ ++ R` (R ∀) | `0³ 1^13 0² 1^5 0² 1 0⁹ ++ R` | ✅ `R := zeros 6 ++ R'` |

| | `regen5_transport` OUT | `descent_glue` IN @ a=5 (N=14, d=1) | verdict |
|---|---|---|---|
| pos | `-22` | `p` (∀) | ✅ `p := -22` |
| left | `0 ++ L` | `pow01 (Lc+14) ++ marker` | ✅ `L := 1 :: (pow01 (Lc+13) ++ marker)` |
| right | `0³ 1^29 0² 1^13 0² 1^5 0² 1 0¹ ++ R` | `0³ 1^29 0² 1^13 0² 1^5 0² 1 0⁹ ++ R` | ✅ `R := zeros 8 ++ R'` |

The right words agree **cell-for-cell** on every explicit cell; the only residue is **trailing zeros absorbed
into the `∀`-quantified `R`**. `2^4−3 = 13`, `2^5−3 = 29` land the top block; `descCascade 1 = 1^5 0² 1` and
`descCascade 2 = 1^13 0² 1^5 0² 1` land the cascade **exactly**.

*Run-length ambiguity ruled out:* the comparison is on **list data**, not on run tokens — `0³ ++ (zeros 6 ++ R')`
and `zeros 9 ++ R'` are equal as `List Bool` by `rfl`, no maximal-split judgement enters.

### 1.3 Kernel-checked (the decisive artefact)

Against the pinned snapshot, all four `[propext, Quot.sound]`-only — **no `sorry`, no axiom, no `native_decide`**:

```lean
theorem regen4_lands_descent_IN (Lc : Nat) (marker R' : List Bool) : … := by rw [regen4_transport]; rfl
theorem regen5_lands_descent_IN (Lc : Nat) (marker R' : List Bool) : … := by rw [regen5_transport]; rfl
theorem regen4_then_descent (Lc) (marker R') :   -- END-TO-END, one transport
    ∃ dep, steps (exitSteps 4 + ((7 + braidRunSteps 0 6 + (4*6+4)) + lowerFoldSteps (0+1) + 100)) IN₄
      = some ⟨.E, …, ⟨ones 12 ++ dep, false, false::true::false::R'⟩⟩ := by
  obtain ⟨dep, hdep⟩ := descent_glue 6 0 Lc (-7) marker R'
  exact ⟨dep, by rw [steps_add, regen4_lands_descent_IN, someBind]; exact hdep⟩
theorem regen5_then_descent … -- same, a=5
```
The proofs are **`rw` + `rfl`**. That is the whole content: the registers match **literally**.

**The gap at k=4,5 is: NONE.** Not a reparse, not a different config — a pure instantiation.

### 1.4 Where my result is stronger than §5ah's

§5ah's `descent_reach_4` / `descent_reach_5` fix **`Lc = 1`** (`cascadeReg 4 1 (−7)`). My
`regen4/5_lands_descent_IN` are **`∀ Lc`** and build green. The generality is **free** — the same `rfl`
closes it, because `pow01 (Lc+6) ≡ false::true::pow01 (Lc+5)` by iota *regardless of `Lc`*. `Lc = 1` is the
**on-path** value (measured, §3), so §5ah is not wrong — but `CascadeRegReached` existentially binds `Lc`, and
carrying `∀Lc` costs nothing and removes a per-level constant from the `∀k` induction. **Recommended 1-line
strengthening** (owner's call — I did not edit `lean/`).

---

## 2. Q2 — what is already `∀`, and what is bespoke-per-level?

**Already `∀`** (all `[propext, Quot.sound]`-only):
- `descent_glue` (§5ag) — `∀ N d Lc p marker R`. The **consumer** is fully general.
- `descentGlue_steps` — `∀ a ≥ 4`, length `= descentSteps a`.
- `regen_TI_generic` — translation-invariance: any `∀ L R` transport is reusable in any context. **This is
  the enabling lemma**: it is *why* the instantiation in §1 is legitimate.
- `carry_level_rec` / `carryExit_wf_frame` — a genuine `Nat.le_induction` (`P 1`, `∀n≥1, P n → P (n+1)` ⊢
  `∀n≥1, P n`). No `sorry`, no `partial`. **The control flow is done.**
- `carry_descent_fold`, `carry_level_middle`, `carry_level_core` (§5w) — the DESCENT/MIDDLE/CORE connectors.
- `exitSteps` / `termSteps` closed forms + `exitSteps_recurrence`. **The arithmetic is done.**

**Bespoke-per-level** (the real residue):
- `regen4_transport` / `regen5_transport` are the **only two** REGEN transports that exist. They are
  `carry_exit_j3` / `carry_exit_j4` re-indexed — two *concrete* theorems, not a family.
- The per-level instantiation data is bespoke and shows **no closed form** across the two known levels:

  | k | N | trailing-zero residue | pow01 offset | p |
  |---|---|---|---|---|
  | 4 | 6 | `zeros 6` | `Lc+4` | −7 |
  | 5 | 14 | `zeros 8` | `Lc+13` | −22 |

  These are *readouts of* `carry_exit_j3/j4`, not instances of a pattern. **The k=4→5 step is NOT a
  `∀`-parametric pattern that just needs generalizing.**

**So `hstep : P n → P (n+1)` is not almost-there.** The frame is instantiable the moment `REGEN(k)`'s OUT
exists `∀k`; that object is §5z's growing-arity odometer tree (`exitSteps_tree_5/6/7`: branching arity
**0, 1, 3**). Reachability is **downstream** of it, not independent of it.

**The honest inverse.** The residual gap **is real**. But it is *not* a new obstruction and *not* a shape
problem — §1 shows the shape falls out for free once REGEN(k)'s OUT is known. The gap is **exactly** the
already-identified §5z object, no more and no less. Reachability was never a *second* wall; §5ag's framing of
it as "the single remaining obstruction" is, strictly, a **re-description of §5z's**.

---

## 3. Q3 — is any part of Q3/`cascadeReg` proven elsewhere?

`grep -rn "cascadeReg" lean/` over the **whole tree** (`Template/Suffix/RunStructure/Completion/O2/O3/O17/O18/Mirror`):
**zero hits outside `X2.lean`.** At snapshot `e1dfbc7` it was **prose-only** (comments at 4569, 4725, 4767,
4882, 4892, 4999, 5960) — never a `def`. §5ah has since named it (`def cascadeReg`, line 6034). No other
module carries any part of it.

The nearest pre-existing relative is §5w's **`cascadeTail`** (X2.lean:3637) with
`cascadeTail_grounds_carry_j3/_j4` — which reproduce `carry_exit_j3/j4`'s RIGHT sides by `rfl`. **This is the
same content as §1, one register-half short and never connected to the descent.** The file has had half of
this finding since §5w.

**Independently corroborated (`x2rm_preg_ladder.py`, `build(2)`, maximal parse):** at the real descent starts
`n = 13453 / 33830 / 114703`, state `E`, head `0`, comb `(01)^m` with `m = 15, 31, 63` and
`N = 14, 30, 62` ⇒ **`Lc = m − N = 1` uniformly at k=5,6,7**. Confirms §5ah's `Lc=1` claim from an
independent probe. Position `p(k) = 2111, 2144, 2209` — diffs `33, 65` = `2^k+1`, i.e. `p(k) = 2^k + k + 2074`
on this orbit **[OBSERVED]**. *Not load-bearing*: `p` is `∀`-quantified in `descent_glue` and `∃`-bound in
`CascadeRegReached`, so no closed form for it is needed.

---

## 4. Q4 — prose vs reality

| Locus | Claim | Verdict |
|---|---|---|
| §5ag, X2.lean:5952-5960 | "THE SINGLE REMAINING OBSTRUCTION IS NOW REACHABILITY … That obligation is OPEN and is NOT claimed here." | **INCOMPLETE, not false.** True `∀k`. But its **base and depth-1 were already discharged** by theorems 1 700 lines earlier in the same file. Reads as wholly open; is not. (§5ah now fixes this.) |
| §5ag:5886-5888 | "REACHABILITY IS NOT CLAIMED … on-path by simulator evidence only" | **Understated.** At k=4,5 it is not simulator evidence — it is `rfl`. |
| §5z:4272 | base "discharged concretely by `regen4_transport`" | **Correct** — the file *knew* regen4 was the base, but never compared its OUT to the descent's IN. |
| §5o:2653-2656 | "the load-bearing evidence is the comb-at-**carry** LADDER" | **WRONG DOMAIN — see §5.** |
| §5o:2664-2666 | closed forms `[OBSERVED]` at 4 points, "weakest-fit part" flagged | **Honest and correctly labelled.** |
| §5ah:6014-6017 | "`Lc = 1` UNIFORMLY at every measured level" | **Independently confirmed** (§3). |

No non-sequitur of the §5ab type found in the reachability prose. **Closed-form spot-checks all passed**:
`2^4−3=13`, `2^5−3=29`, `descCascade 1 = 1^5 0² 1`, `descCascade 2 = 1^13 0² 1^5 0² 1`,
`2(2^{k−1}−2)+1 = 2^k−3` @k=4,5,6,7 → 13,29,61,125. No `1089`/`4152`-style slip survives here.

---

## 5. Audit item B1 — §5o's "comb-at-carry LADDER": **CONFIRMED (mislabel), with two corrections**

### The tell
§5o claims carries fire at `comb=2^m−1` with multiplicities `128,64,32,16,8,4,2,1` — which **sum to 255**.
But `Cfaithful(10) = 3·2^{K−4} = 192`. **A histogram of carry events must sum to the number of carry events.**
`255 ≠ 192` ⇒ it cannot be a carry histogram.

### Root cause — found by reading, confirmed by measuring
`x2fr_counts.py:46-47`:
```python
    # comb-at-carry (comb=2^m-1) profile
    combhist = Counter(c for b,c in cs if c > 0)
```
`cs` is the **chew-start** list. The carry events are only ever accumulated into `ncarry` — their comb values
are **never histogrammed**. The `if c > 0` filter additionally discards the `comb=0` events.

### Measured (`x2rm_b1_ladder.py`, `x2bd_sim.build(2)`, K=10) — `T=3852`, `C=192`, depths `{1:192}`
| domain | histogram | sum |
|---|---|---|
| (a) what `x2fr_counts.py` computes, labelled "comb-at-carry" | `{1:1, 3:128, 5:1, 7:64, 15:32, 31:16, 63:8, 127:4, 255:2, 511:1}` | **257** ≠ C |
| (b) chew-starts, unfiltered | `{0:3595, 1:1, 3:128, 5:1, 7:64, …, 511:1}` | 3852 **= T** ✅ |
| (c) **TRUE comb-at-carry** | `{0:64, 1:1, 7:64, 15:32, 31:16, 63:8, 127:4, 255:2, 511:1}` | 192 **= C** ✅ |

**The allegation is confirmed exactly**: the true carry histogram has **64 events at `comb=0`** and
**ZERO at `comb=3`** — precisely where §5o puts its leading `128`. The `128` is the **chew-start** count at
`comb=3`. The alleged true histogram `{0:64, 1:1, 7:64, …}` matches my measurement **verbatim**.

### Correction 1 — to the B1 report
It states the mislabeled figure sums to `255`. The **ladder entries** (m=2..9) sum to 255; the histogram
`x2fr_counts.py` actually computes sums to **257** (it also picks up singletons at `comb=1` and `comb=5`).
The tell stands either way.

### Correction 2 — the ladder law is NOT exact at m=2..9 over chew-starts (B1 overstates)
B1 claims "the ladder law itself is exact (m=2..9) over chew-starts". At K=10 yes; **at K=11 it fails at m=2**
(257 vs predicted 256). Exactness over chew-starts is **m=2..9 at K=10, m=3..9 at K=11**.

**Constructive finding.** The law is *more* robust over **carries** than over chew-starts:
`multiplicity(comb=2^m−1) = 2^{K−1−m}` holds **exactly for m=3..9 at BOTH K=10 and K=11**, with the
remainder a clean `2^{K−4}` at `comb=0`:
- K=10: `64+32+16+8+4+2+1 = 127` (m=3..9) `+ 64` (comb=0) `+ 1` (comb=1) `= 192 = C` ✅
- K=11: `128+64+32+16+8+4+2 = 254` (m=3..9) `+ 129` `+ 1 + 1 + 1 = 386 = C` ✅

So §5o's ladder **can be restated correctly over carries**, keeping 7 exact levels — the leading entry is
`2^{K−4}` at `comb=0`, not `128` at `comb=3`. **[OBSERVED]**

### B1 verdict
**§5o's VERDICT SURVIVES.** The binary-ladder structure is real and clean on *both* domains, so
"the tick count is a clean pure register, not irreducibly tape-determined" stands. **Only the sentence naming
the evidence is wrong** (domain: chew-starts, not carries; and the leading `128 @ comb=3` does not exist among
carries). Same mislabel at `x2fr_register.py:13`. Both are **prose/comment defects, not proof defects** —
nothing in Lean depends on them (`Tfaithful`/`Cfaithful` are `[OBSERVED]` `def`s cross-checked against the raw
orbit, and those cross-checks pass).

---

## 6. Ranked list — what would close reachability

1. **[free, ~1 line] Generalize `descent_reach_4/5` to `∀Lc`.** Proven green in my probe. Removes a per-level
   constant from the eventual induction.
2. **[decisive de-risk] Prove `REGEN(6)` ⇒ `cascadeRegReached_6`.** `k=6` is the **first level with a
   recursive call** (`exitSteps_tree_6`: `REGEN(6) ⊇ REGEN(4)`, arity 1). k=4,5 are arity-0 leaves and prove
   *nothing* about the recursion. **This is the only experiment that tests the actual open object.** If
   REGEN(6) assembles from `regen4_transport` + `∀`-level CORE/glue, arity-1 is real and `∀k` is in reach; if
   it does not, the wall is confirmed and *located*. **Highest information-per-unit-work in the program.**
3. **[the ∀k object] `REGEN(k)`'s OUT, `∀k`.** `cascadeReg_collapse` (§5ah) says exactly what it must be:
   the right register is `0³ descCascade(k−2) 0⁹ R`, so **REGEN(k) prepends exactly one cascade layer**
   (`descCascade(k−3) ↦ descCascade(k−2)`). This is a **self-similar IH in one register** — the right shape
   for an induction, and much better than "two coupled registers". The obstruction is the growing arity
   `0,1,3` (`exitSteps_tree_5/6/7`), i.e. the odometer digit tree — **not** the shape.
4. **[structural] Reconcile the arity tree with `carry_level_rec`.** `Nat.le_induction` gives a *fixed* step;
   arity `0,1,3,…` needs strong induction (`Nat.strong_induction_on`) over `k`, since REGEN(7) calls
   REGEN(5) **and** REGEN(4). **`carryExit_wf_frame` as stated may be the wrong frame** — worth checking
   before more weight is put on it. (Flagged, not proven.)
5. **[cheap hygiene] Fix the §5o / `x2fr_register.py:13` attribution** per §5; optionally restate the ladder
   over carries (7 exact levels, K=10 **and** 11).
6. **[cheap] Retire §5ag:5886-5888's "simulator evidence only"** — at k=4,5 it is `rfl`.

---

## Reproduce

```bash
# Lean (isolated snapshot; NEVER touches lean/)
SNAP=…/scratchpad/snap
git archive e1dfbc7 lean/ | tar -x -C $SNAP && cp -R lean/.lake $SNAP/lean/.lake
cd $SNAP/lean && lake build X2 && lake env lean Probe.lean
#   -> regen4_lands_descent_IN / regen5_lands_descent_IN
#      regen4_then_descent / regen5_then_descent   all: [propext, Quot.sound]

python x2rm_regen_reach.py    # symbol-by-symbol REGEN OUT vs descent_glue IN
python x2rm_b1_ladder.py      # B1: chew-start vs TRUE carry comb histograms (K=10, 11)
python x2rm_preg_ladder.py    # Lc(k)=1 and p(k) at the real descent starts
```

---

**No machine decided. No label upgraded.**
