# `lean/X2.lean` — adversarial claim audit, 2026-07-17

**Scope.** Prose-vs-reality audit of the whole file: phantom identifiers, rotting evidence
citations, closed-form arithmetic vs its own instances, simulator-contradicted orbit claims,
label integrity. **Read-only on `lean/`** — no fixes applied; the owning agent applies them.

**Snapshot.** `lean/X2.lean` @ 5852 lines, sha256 prefix `2baf5a39c6eff802`, repo HEAD `59749fb`.
The file was being edited concurrently during the audit (it grew 5575 → 5852 lines while I
worked; a new §5ag appeared at line 5808). **All line numbers below are from the snapshot and
were re-verified stable** — the growth is appended after line 5575, so every anchor I cite still
resolves. Copy of the snapshot: `scratchpad/X2_snapshot.lean`.

**Transient states explicitly NOT reported as defects.** At snapshot time `lake env lean X2.lean`
reported a syntax error at `X2.lean:5727`, a `whnf` timeout at `5741`, and
`'X2.descent_final_tile' depends on axioms: [sorryAx]` /
`'X2.descent_glue' depends on axioms: [propext, sorryAx, Quot.sound]`. These are all inside the
in-progress §5ag the owning agent is writing right now. Per the audit brief these are the other
agent's business and are **not** findings. Everything up to line 5575 built clean.

**Probes written (mine, committed):** `x2au_phantom.py`, `x2au_topgrind.py`, `x2au_ladder.py`.

---

## Ranked defect ledger

### (A) Findings that dissolve or weaken a stated obstruction

---

#### A1 — §5ad's `[DESIGN]` TOPGRIND obstruction is STALE: it was closed by §5af

**Lines 4895–4898 and 5111–5113.**

Claim @ 4895:
> **WHAT REMAINS `[DESIGN]`:** the TOPGRIND quadratic term `topGrindSteps a = 4^a−3·2^a+7` —
> the nested doubling, the project's core wall, now LOCALIZED as the single obstruction inside
> `descentGlue`.

Claim @ 5111:
> • the TOPGRIND transport `[DESIGN]` — the nested doubling — is the SINGLE remaining obstruction
> inside `descentGlue`, and it is the project's core wall re-encountered, NOT a bounded
> connector. `descentGlue` is therefore NOT machine-checked `∀a`; only its linear skeleton is.

**Check that fails.** §5af (line 5325, dated 2026-07-17 — one day *after* §5ad) **proves the
TOPGRIND transport `∀`**:

```
X2.lean:5489  theorem braid_topgrind (N Lc : Nat) (p : Int) (marker casc : List Bool) :
                  steps (7 + braidRunSteps 0 N + (4 * N + 4)) ⟨.E, p, ⟨pow01 (Lc + N) ++ marker, …⟩⟩
                    = some ⟨.E, p + 5 + 2 * (N : Int), ⟨ones (4*N+4) ++ (pow10 Lc ++ (true :: marker)), …⟩⟩
X2.lean:5531  theorem topGrindSteps_split (a : Nat) (ha : 2 ≤ a) :
                  topGrindSteps a = 7 + braidRunSteps 0 (2^(a-1) - 2) + (4 * (2^(a-1) - 2) + 4)
```

Both are green (`[propext, Quot.sound]`-only; no `sorry`/axiom/`native_decide`). So the TOPGRIND
**transport** is *not* `[DESIGN]` any more — it is a single `∀N Lc` lemma. The arithmetic split is
exact at every `a` (`x2au_topgrind.py`):

```
  a=2 N=0  : 7+0+4      = 11    = topGrindSteps 2   OK
  a=3 N=2  : 7+28+12    = 47    = topGrindSteps 3   OK
  a=4 N=6  : 7+180+28   = 215   = topGrindSteps 4   OK
  a=5 N=14 : 7+868+60   = 935   = topGrindSteps 5   OK
  a=6 N=30 : 7+3780+124 = 3911  = topGrindSteps 6   OK
  a=7 N=62 : 7+15748+252= 16007 = topGrindSteps 7   OK
  a=8 N=126: 7+64260+508= 64775 = topGrindSteps 8   OK
```

And I independently re-verified `braid_topgrind`'s IN shape, OUT shape, step count and head
displacement **against the real orbit at two independent generations** (`x2au_topgrind.py`, both
in `build(2)`):

```
=== a=5  N=14  raw_in=13453 ===
  topGrindSteps(5) = 935;  7 + braidRunSteps 0 14 + (4*14+4) = 935   -> MATCH
  IN  st=E h=0  pow01(15) prefix=True (maximal=True)  0^3 1^29 0^2 prefix=True
  OUT st=E h=0  ones(60) ++ pow10(1) ++ 1 prefix=True  right starts 0=True
  steps 13453 -> 14388 = 935
  VERDICT a=5: braid_topgrind matches the real orbit: True

=== a=6  N=30  raw_in=33830 ===
  topGrindSteps(6) = 3911;  7 + braidRunSteps 0 30 + (4*30+4) = 3911   -> MATCH
  IN  st=E h=0  pow01(31) prefix=True (maximal=True)  0^3 1^61 0^2 prefix=True
  OUT st=E h=0  ones(124) ++ pow10(1) ++ 1 prefix=True  right starts 0=True
  steps 33830 -> 37741 = 3911
  VERDICT a=6: braid_topgrind matches the real orbit: True
```

(The `pow01(Lc+N)` split was checked **maximal** in both cases, so this is not a run-length
mis-parse.)

**Why this matters.** §5ad names the TOPGRIND *transport* as "the project's core wall
re-encountered" and "the SINGLE remaining obstruction inside `descentGlue`". That transport is
now a proven `∀N Lc` lemma. With `descent_lower_fold` (§5ad, `∀d`, green) already covering the
linear skeleton, the residual for `descentGlue` is **not** the nested-doubling wall; it is only
(i) the `FINAL` 100-step residue and (ii) the composition + the `∀a` claim that the descent's
TOPGRIND-start actually has `braid_topgrind`'s IN shape (reachability). §5af's own scope note is
honest about exactly this:

> **WHAT REMAINS `[DESIGN]`.** `braid_topgrind`'s IN config is REACHED on the real orbit only by
> SIMULATOR evidence … This section closes the TOPGRIND's INTERNAL transport `∀`, not its
> reachability.

**Proposed correction.** Rewrite 4895–4898 and 5111–5113 to state the *post-§5af* position: the
TOPGRIND transport is GREEN `∀N Lc` (`braid_topgrind`) and its step count splits exactly
(`topGrindSteps_split`); what remains for `descentGlue` is the `FINAL` residue, the composition,
and the `∀a` **shape/reachability** of the TOPGRIND entry — a materially different (and smaller)
object than "the project's core wall". Do **not** upgrade any label; this is a prose correction.
(Note: the in-progress §5ag appears to be attacking exactly the `FINAL`/composition piece, so the
owning agent may already be mid-fix here.)

---

#### A2 — §5ab's "DECISIVE OBSTRUCTION" inference is a non-sequitur, refuted in-file by §5af

**Lines 4536–4542, and the two theorems at 4656–4670.**

Claim @ 4538–4542:
> the transition's CORE `sweepEF` build-up rebuilds a block of height `2^h−4` where `h` GROWS
> with the odometer position (`2^5,2^6,2^7` …; `glue_height_grows`), and the descent glue `a→4`
> grows `Θ(4^a)` (`1089 → 4152`, `descent_glue_unbounded`). So as `k→∞` there are UNBOUNDEDLY
> MANY DISTINCT transition types …, each a fixed transport but of `Θ(4^h)` growing length — **NO
> finite set of glue lemmas covers them**, and NO fixed per-element glue function closes the
> `foldl`.

**Check that fails.** The inference "growing length ⇒ no finite set of glue lemmas covers them"
is invalid, and it is refuted by a lemma **in this same file**. §5af's `braid_topgrind` (line
5489) is *one* lemma, `∀N Lc`, that covers precisely a `Θ(4^a)`-growing family of transports —
the same family §5ab calls uncoverable. Likewise `descent_lower_fold` (4967, `∀d`) covers a
growing fold, and `sweepEF` (§4, `∀m`) covers growing sweeps. Unbounded *length* is not
unbounded *description*: a single `∀`-parametric lemma is exactly how this file already handles
growing objects.

This is concrete, not abstract. §5ab's own glue table contains the entry `935` at
`glueSegs 8` index 2, and `935 = topGrindSteps 5` — i.e. **that specific "unbounded, growing"
glue segment is now covered `∀` by `braid_topgrind`** (verified on-path above). Similarly
`glueSegs 7`[2] = `glueSegs 8`[5] = `1089` = `descentSteps 5` and `glueSegs 8`[3] = `4152` =
`descentSteps 6` — the file proves this itself in `descentSteps_is_glueSeg`. So the growing glue
entries are exactly the descent/TOPGRIND objects, one of which is now `∀`-proven.

Furthermore the two theorems cited as the obstruction have **no content beyond arithmetic on
hard-coded constants**:

```
X2.lean:4656  /-- **THE DECISIVE OBSTRUCTION (1/2): the CORE build-up height GROWS** … -/
X2.lean:4661  theorem glue_height_grows :
                  (28 + 4 = 2 ^ 5) ∧ (60 + 4 = 2 ^ 6) ∧ (124 + 4 = 2 ^ 7) := by …

X2.lean:4665  /-- **THE DECISIVE OBSTRUCTION (2/2): the DESCENT glue `a→4` grows `Θ(4^a)`** … -/
X2.lean:4670  theorem descent_glue_unbounded : 3 * 1089 < 4152 := by decide
```

`28+4 = 32` and `3·1089 < 4152` are true but establish only that three measured constants grow.
They do not — and cannot — establish non-`∀`-parametricity. Labelling them "THE DECISIVE
OBSTRUCTION (1/2)" and "(2/2)" overstates what a `decide` on `28+4=2^5` can support. (The
docstrings do honestly say "Pure `Nat`", so this is a framing defect, not a false theorem.)

**Proposed correction.** Retract the inference at 4538–4542: growth does not imply
non-parametricity, and §5af exhibits the counterexample within the file. Rename/reframe
`glue_height_grows` and `descent_glue_unbounded` as *measurements* of growth (which they are)
rather than "THE DECISIVE OBSTRUCTION". The genuine residual content of §5ab is the `toCfg`
threading across the fold and the `∀a` reachability of each glue's IN shape — not the fact that
lengths grow. **No label upgrade is proposed**: §5ab's overall verdict ("the transport-level
`foldl` does not close") may well still stand, but the *stated reason* does not.

---

### (B) Claims that are false or unsupported as worded

---

#### B1 — §5o: the "comb-at-carry LADDER" is measured over CHEW-STARTS, not carries

**Lines 2634–2635 and 2653–2656.**

Claim @ 2634:
> the comb-at-carry profile is a clean power-of-2 ladder (carry at `comb=2^m−1` fires
> exactly `2^(K−1−m)` times)

Claim @ 2653–2656 (presented as the section's *load-bearing evidence*):
> The load-bearing evidence is the comb-at-carry LADDER (main-loop independently inspected,
> g=2 K=10): **carries** fire at `comb = 2^m−1` with multiplicities `128,64,32,16,8,4,2,1 =
> 2^(K−1−m)` across 8 levels — a clean binary structure, not a 4-point fit.

**Check that fails.** `128+64+32+16+8+4+2+1 = 255`, but `Cfaithful 10 = 3·2^6 + 0 = 192`. A
histogram of the carry population cannot sum to 255 when there are 192 carries. Measuring both
populations separately (`x2au_ladder.py`, g=2, K=10) settles it:

```
  total chew-starts        = 3852
  total carries (Cfaithful)= 192   closed form Cfaithful(10) = 192   -> MATCH

  (a) comb histogram over ALL CHEW-STARTS  (what x2fr_counts.py's `combhist` computes):
      {1: 1, 3: 128, 5: 1, 7: 64, 15: 32, 31: 16, 63: 8, 127: 4, 255: 2, 511: 1}
      restricted to comb = 2^m-1 : sum = 256
        comb=3 (m=2) measured=128  2^(10-1-2)=128  OK
        comb=7 (m=3) measured= 64  2^(10-1-3)= 64  OK
        … through comb=511 (m=9) measured=1  2^(10-1-9)=1  OK      [8 levels, m=2..9]

  (b) comb histogram over CARRY EVENTS only:
      {0: 64, 1: 1, 7: 64, 15: 32, 31: 16, 63: 8, 127: 4, 255: 2, 511: 1}   sum = 192
```

The `128,64,32,16,8,4,2,1` ladder is population **(a)**, chew-starts. The actual carry population
**(b)** is a *different* histogram: it has **64 events at `comb = 0`** (not of the form `2^m−1` at
all), and **zero** carries at `comb = 3` — precisely where the prose puts the ladder's leading
`128`. The source probe confirms the provenance: `x2fr_counts.py` builds
`combhist = Counter(c for b,c in cs if c > 0)` where `cs` is the **chew-start** list, and the same
mislabel is inherited from `x2fr_register.py:13`.

**What survives.** The ladder law itself is real and I confirmed it exactly at all 8 levels
(m=2..9) — over chew-starts. `Tfaithful`/`Cfaithful` reproduce the measured 3852/9729/19470/47107
and 192/386/768/1538 exactly (verified). So §5o's VERDICT ("a CLEAN pure-register quantity, NOT
irreducibly tape-determined") is **not** threatened; only the sentence naming the evidence is
wrong.

**Proposed correction.** Replace "comb-at-carry" / "carries fire at" with "comb-at-**chew-start**"
/ "**chew-starts** occur at" in both places (2634, 2653–2656). Optionally note that the true
comb-at-carry profile is `{0:64, 1:1, 7:64, 15:32, 31:16, 63:8, 127:4, 255:2, 511:1}`, sum 192.
Consider fixing the same wording in `x2fr_register.py:13` and `x2fr_counts.py`'s comment.

---

#### B2 — §5ac: `uMeasure_outer`'s hypothesis excludes the very instance §5ac grounds it on

**Lines 4784–4785 (prose), 4799 (`uMeasure_outer`), 4813–4818 (`uMeasure_grounds`).**

Claim @ 4784:
> `uMeasure k a = k² + a`, the lexicographic `(k,a)` encoded as a single `Nat` (**valid since the
> descent depth `a < k` always** — the descended cascade sits below the current block)

The theorem takes that as a hypothesis:

```
X2.lean:4799  theorem uMeasure_outer {k k' a a' : Nat} (hk : k' < k) (ha' : a' < k') :
                  uMeasure k' a' < uMeasure k a
```

But the section's own grounding on the real orbit is:

```
X2.lean:4813  … the STRATUM-2 outer call `REGEN(9) → REGEN(7)` (that call's descent depth 7):
                `uMeasure 7 7 < uMeasure 9 7` …
X2.lean:4817  theorem uMeasure_grounds :
                  uMeasure 7 7 < uMeasure 9 7 ∧ uMeasure 9 6 < uMeasure 9 7 := by …
```

**Check that fails.** The grounded outer call has `k' = 7` and descent depth `a' = 7`. The
hypothesis `ha' : a' < k'` requires `7 < 7`, which is **false**. So `uMeasure_outer` **cannot be
applied to the one real-orbit call `uMeasure_grounds` exhibits**. Correspondingly the prose
invariant "the descent depth `a < k` always" is contradicted by §5ac's own instance (`a = 7`,
`k = 7`). `uMeasure_grounds` is still true (`49+7 = 56 < 88 = 81+7`), but it is proved by `decide`
on constants — it is *not* an instance of `uMeasure_outer`, despite being presented as its
grounding.

This matters because §5ac's headline is "**Q4: one measure `k²+a` closes both nestings**" and the
FEASIBILITY VERDICT rests on it. As stated, the outer lemma is vacuous at the only real-orbit
level the section cites.

**Proposed correction.** Weaken the hypothesis to `ha' : a' ≤ k'` — the proof still goes through,
since `k'*k' + a' ≤ k'*k' + k' = k'*(k'+1) ≤ k*k` needs only `k'+1 ≤ k`, which `hk` already gives.
(The existing proof's chain `h1` becomes `Nat.add_le_add_left ha' _` with a strict step supplied
by `h3`; the arithmetic is unchanged.) Then fix the prose at 4784 to say `a ≤ k`, and
`uMeasure_grounds` becomes a genuine instance. Alternatively, if the intended invariant really is
`a < k`, then the grounding at 4813 is misdescribed and the real descent depth of the
`REGEN(9)→REGEN(7)` call needs restating.

---

### (C) Citation rot / cosmetic

---

#### C1 — §5ac: "the descent is `≈8× REGEN(a)`" is asymptotic, but stated pointwise

**Line 4773.**

> the ratio `descentSteps/exitSteps` STRICTLY INCREASES (`4 < ratio`, and increasing
> 4.99→5.75→6.49), so the descent is `≈8× REGEN(a)` and is not any lower `REGEN`

**Check.** At the three grounded levels the ratio is 4.995 / 5.751 / 6.494 — the docstring quotes
these correctly. But `≈8×` holds only in the limit (`descentSteps ~ 4^a`, `exitSteps ~ 4^a/8`).
At no grounded `a` is the descent ≈8× REGEN; the sentence's own adjacent numbers contradict its
"≈8×". The theorem `descentSteps_exceeds_regen` correctly proves only `4 * exitSteps a <
descentSteps a` (verified true at a=5,6,7).

**Proposed correction.** "the descent is `→8×` REGEN(a) asymptotically (4.99→5.75→6.49 at the
grounded levels, rising toward 8)".

---

## Audited and found CLEAN (coverage record)

So that the audit's coverage is legible, the following were checked and **pass**:

### Evidence citations (rotting-`.py` check) — CLEAN
All **51** distinct `.py` files cited anywhere in `X2.lean` were extracted and checked with
`git ls-files --error-unmatch`. **Every one is tracked in the repo root.** Zero broken, zero
untracked, zero `scratchpad/`-only citations. The §5ae rot noted in the audit brief
(`x2qb_measure.py`, `x2qb_left.py`, `x2qb_rt.py`) has been fixed — all three, plus
`x2qb_exact.py`, are now tracked. **This defect class is closed.**

### Phantom identifiers — CLEAN (no citation pretends to be proven)
`x2au_phantom.py` extracted all 348 distinct backticked identifiers appearing in docstrings/
comments and diffed them against the 262 declarations. The 184 unresolved names were triaged by
hand; **none is a citation that pretends to be a proven theorem.** They break down as:
Lean/Mathlib core (`rfl`, `decide`, `omega`, `Nat.repeat`, `List.foldl`, `Nat.le_induction`,
`Nat.mul_le_mul`, `sorryAx`, `native_decide`, …); single-letter metavariables (`E`, `D`, `m`,
`n`, `k`, `j`, `L`, `R`, `p`, …); `.py` probe names (all tracked, above); other-file references
(`Template.lean`, `Suffix.lean`, `O3.lean`, `Completion.lean`); binder/hypothesis names local to
theorem statements (`H_entry`, `H_repack`, `h_low`, `h_doub`, `h_init`); Python-side names
explicitly flagged as such (`m1_spec`, `try_R_cycle`, `try_L_cycle`, `try_D_loop`); and prose
phase names (`REGEN`, `TERM`, `EXIT`, `TOPGRIND`, `descentGlue`, `carryExit`, `carry_step`,
`outer_step`, `carry_exit`, `doubling_phase`, `rebuild_transport`).

Critically, **the `[DESIGN]` signatures are correctly written as comments, not as
`theorem … := sorry`** (lines 1523, 1530, 1644, 3780, 3960, 4312) — the deliberate feature noted
in the brief, confirmed present and correctly used. `rebuild_transport` @ 935 is cited *as not
existing* ("why `rebuild_transport` does not exist as this file's kind"), which is honest.
`braidCfg` — the phantom `def` flagged in the brief — **now genuinely exists** at line 5192.

### Arithmetic vs its own instances — CLEAN except as noted in A/B/C above
Every closed-form-with-instance claim I could find was evaluated at its stated `a`/`m`/`k`/`K`:

| Section | Claim | Instance check | Verdict |
|---|---|---|---|
| §5ac 4750 | `descentSteps a = 2^{2a}+110−9a` | a=5,6,7 → 1089, 4152, 16431 | **exact** |
| §5ac 4767 | `descentSteps_is_glueSeg` | `glueSegs 7`[2]=`glueSegs 8`[5]=1089; `glueSegs 8`[3]=4152 | **exact** |
| §5ac 4771 | `4·exitSteps a < descentSteps a`, ratio increasing | a=5,6,7: 4.995 < 5.751 < 6.494 | **true** (wording → C1) |
| §5ad 4877 | `TOPGRIND(a) = 4^a−3·2^a+7` | a=5,6,7 → 935, 3911, 16007 | **exact** |
| §5ad 4878 | `STD(m) = 3·2^m−9` | m=3,4,5,6 → 15, 39, 87, 183 | **exact** |
| §5ad 4881 | full table `935+(39+15)+100 = 1089` etc. | all three a=5,6,7 reproduce `descentSteps` | **exact** |
| §5ad 4888 | "block 29: 87 vs 935; block 61: 183 vs 3911" | m=5: 2^5−3=29 ✓; m=6: 2^6−3=61 ✓ | **exact** |
| §5ad 4941 | `descent_std_tile` `6v+3`, `1^{2v+1}` | v=2,6,14,30 → 15,39,87,183; blocks 5,13,29,61 | **exact** |
| §5ad 4957 | `lowerFoldSteps` grounds 54,141,324 | d=2,3,4 (= a−3 for a=5,6,7) | **exact** |
| §5ad 4949 | `descCascade d` docstring vs def | `descCascade 1 = 1^5 0² 1^1` ✓ | **exact** |
| §5ae 5158 | `braid_run` `runS 0 N = 4N²+6N` | N=14 → 868; Σ(8r+10, r=0..13) = 868 | **exact** |
| §5ae 5163 | RT lengths `10,18,…,114` | AP 14 terms, last 114, sum 868 | **exact** |
| §5ae 5166 | `868 + (2^6+3) = topGrindSteps 5 = 935` | 868+67 = 935 | **exact** |
| §5ae 5175 | the *self-correction*: `2^{a+1}−4 = 60 ≠ 126`; true block `2^{a+2}−2` | a=5→126, a=6→254 | **correct** |
| §5af 5340 | exit `= 4N+4 = 2^{a+1}−4` | N=14→60, N=30→124 | **exact** |
| §5af 5345 | deposit `1^{4N+5} = 1^{2^{a+1}−3}` | N=14→61, N=30→125 | **exact** (see note) |
| §5af 5531 | `topGrindSteps_split` | a=2..8, all 7 levels | **exact** |
| §5aa 4386 | arity `(k−5)(k−4)/2` = 0,1,3,6; `exitArity 9 = 10` | k=5..9 | **exact** |
| §5aa 4383 | `2^k−3` binary one-bit counts 4,5,6,7 | k=5..8: 29,61,125,253 | **exact** |
| §5aa 4379 | `exitSteps 8 = 9282` | `2^13+8·2^7+2^6+2 = 9282` | **exact** |
| §5aa 4398 | char. poly `(x−4)(x−2)²(x−1)` → coeffs `(9,−28,36,−16)` | expands to `x⁴−9x³+28x²−36x+16` ✓; recurrence verified k=8..12 | **exact** |
| §5aa 4402 | `3·exitSteps k < exitSteps(k+1) < 4·exitSteps k` | k=4..7 all true | **exact** |
| §5ab 4507 | `exitList` grounds `[],[4],[4,5,4],[4,5,6,4,5,4]` | k=5..8 from the def | **exact** |
| §5ab 4509 | `exitList` length = §5aa arity | 0,1,3,6 | **exact** |
| §5ab 4640 | `exitSteps k = (glueSegs k).sum + foldRegenSteps k` | k=5: 218=218+0; k=6: 722=652+70; k=7: 2530=2172+358; k=8: 9282=7914+1368 | **exact** |
| §5y 3991 | `TERM(k) = 2^{k+1}+k+5` | k=4..7 → 41,74,139,268; blocks 13,29,61,125; first diffs 33,65,129 `= 2^{k+1}+1` | **exact** |
| §5o 2630 | flat counter `2^K−1` = 1023/2047/4095 | K=10,11,12 | **exact** |
| §5o 2673 | `Tfaithful K` | K=10..13 → 3852, 9729, 19470, 47107 | **exact** |
| §5o 2677 | `Cfaithful K` | K=10..13 → 192, 386, 768, 1538 | **exact** |
| §5o 2634 | the ladder law `2^(K−1−m)`, 8 levels | m=2..9 at K=10, measured | **exact** (but mislabelled → B1) |

Note on §5af's deposit: `braid_exit` concludes `ones (4*N+4)` while the prose says the exit lays
`1^{4N+5}`. These **reconcile** and are not a defect: `pow10 Lc` begins with a `1`, so the
*visible run-length* is `4N+5`. My probe confirms the real orbit's OUT left tape reads
`[(1,61),(0,1),(1,126),…]` at a=5 and `[(1,125),(0,1),(1,254),…]` at a=6 — matching the prose
exactly. `braid_exit_a5` (5402) makes the reparse explicit via `ones_append_true`. This is
handled correctly.

### Simulator cross-checks — CLEAN
- `braid_topgrind` IN/OUT/step-count/head-shift verified bit-for-bit on the real `build(2)` orbit
  at **a=5 (13453→14388, 935 steps)** and **a=6 (33830→37741, 3911 steps)** — `x2au_topgrind.py`.
  Both generations in one orbit, as the brief noted. The `pow01(Lc+N)` splits were verified
  **maximal**, so no run-length ambiguity.
- §5o's `Tfaithful`/`Cfaithful` reproduced from the raw orbit (3852 / 192 at K=10) —
  `x2au_ladder.py`.
- §5ae's *self-corrections* (the `1^126` / `2^{a+1}−4` retraction and the "exit lays the long
  block" retraction) are themselves **correct** and are properly recorded at 5174–5186 so they
  are not reintroduced. Good practice; no action.

### Label integrity — CLEAN except A1/A2
- No claim labelled `[PROVEN]` was found that is not a green theorem.
- `#print axioms` for everything up to line 5575 returns only `[propext, Quot.sound]` /
  `[propext]` / "does not depend on any axioms". **No `sorryAx`, no `native_decide`, no
  `Classical.choice`** in the audited region. (The `sorryAx` at 5727/5741 is the in-progress
  §5ag — transient, excluded, see above.)
- The `[DESIGN]`-as-comment discipline (no injected `sorryAx`) is correctly maintained
  throughout.
- §5r's conditional framing (`x2_nonhalt` conditional on `h_low`/`h_doub`/`h_init`) is honestly
  stated at 2990–3003 and 3073–3080; the hypotheses are real binders, not phantom citations.
- Line 54 and 3594 correctly keep x2 at `[OPEN]`.

---

## Summary

- **1 stated obstruction dissolves (A1):** §5ad's `[DESIGN]` TOPGRIND — "the SINGLE remaining
  obstruction inside `descentGlue`, the project's core wall re-encountered" — was closed by
  §5af's `braid_topgrind` a day later, and I independently re-verified that lemma against the
  real orbit at a=5 **and** a=6. §5ad's prose is stale.
- **1 stated obstruction is weakened (A2):** §5ab's "DECISIVE OBSTRUCTION" rests on the inference
  "growing length ⇒ no finite set of glue lemmas covers them", which `braid_topgrind` refutes
  from inside the same file; its two supporting theorems are arithmetic tautologies on hard-coded
  constants.
- **2 false-as-worded claims (B1, B2):** §5o's load-bearing "comb-at-carry ladder" is actually a
  chew-start ladder (255 ≠ 192); §5ac's `uMeasure_outer` hypothesis `a' < k'` excludes its own
  grounding instance `uMeasure 7 7 < uMeasure 9 7`.
- **1 cosmetic (C1).**
- **Citation rot: fully clean** (51/51 tracked). **Phantom identifiers: none.** The two defect
  classes that cracked §5ae have both been eliminated file-wide.

The audit hypothesis — that more `[DESIGN]`/`[OPEN]` walls are artifacts of stale prose or bad
inference — is **confirmed twice** (A1, A2), though in both cases the underlying object had
already been correctly analysed elsewhere in the file; the defect is that the obstruction prose
was not retracted.

No machine decided. No label upgraded.
