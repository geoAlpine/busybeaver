# E2 — `champion_lower` scoping report

**Date:** 2026-07-22
**Task:** assess what it would take to turn `axiom champion_lower : championSteps ≤ BB6`
(`lean/Completion.lean:342`) into a theorem. **Scoping only — nothing built.**

**Verdict up front:** **GO, but not as stated.** The axiom as written is *unprovable in
principle*; the tractable target is a restatement plus a halting proof. Recommended
representation: **(iii) opaque `championSteps`, defined by description, inequality proven
structurally.** Scale: **3–6 weeks.** Hardest sub-obstacle: **not the tower — it is the
repo's step-exact `Option`-valued `steps` discipline**, which must be supplemented with a
count-free reachability layer before any of this is expressible.

---

## 0. Two factual corrections to the repo's premises (soundness-relevant)

Both should be fixed regardless of whether E2 proceeds.

### 0.1 The machine is misattributed and its magnitude is understated

`lean/Completion.lean:328-330` says:

> `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` halts at a **Kropitz-class value ≈ 10↑↑15**.

This is wrong on both counts. Per the BusyBeaverWiki page for this exact machine:

- **Discoverer:** mxdys, **25 June 2025** — not Pavel Kropitz.
- **Magnitude:** `2↑↑↑5 < 2↑↑2↑↑2↑↑10 < 2↑↑2↑↑((2^)^8 6) < 2↑↑2↑↑2↑↑11 < 2↑↑↑6`,
  i.e. **`S(6) > 2↑↑↑5` — pentational**, not tetrational.

The Kropitz `10↑↑15` machine is a *different, superseded* record (June 2022). The wiki's
BB(6) history table records the former tetration champion at `10↑↑15.60465` (Σ) as having
been **surpassed** by the present one.

The same erroneous figure propagates to `BB6_COMPLETE_ROADMAP_2026-07-22.md:42,85`,
`COMPLETION_SKELETON_2026-07-10.md:91,151`, and `README.md:166`. It does not affect any
theorem (`championSteps` is opaque, so no proof depends on its value) but it is a factual
claim stated in a docstring and in the roadmap, and this repo's discipline is that such
claims carry labels.

### 0.2 A machine-checked halting proof already exists

The community has **already formalized this machine's halt in Rocq (Coq)**:

> `https://github.com/ccz181078/busycoq/blob/3f302b87f5fb933c46e97672ffbb6907f373fb6e/verify/SOBCv5.v#L10210-L11283`

That is a **1,073-line** region of an 11,283-line file, inside `busycoq` — the same codebase
family as Coq-BB5. Its final statement is

```coq
Lemma halt: halts tm c0.
```

**It proves halting only. It does not state a step count.** This is the single most
important datum in this report: the reference formalization, produced by the people who
found the machine, deliberately declines to express the value. Our representation choice
should not be more ambitious than theirs.

---

## 1. The obstacle, stated precisely

### 1.1 The stated axiom is unprovable, and not because of the tower

```lean
axiom championSteps : Nat          -- Completion.lean:331
axiom BB6 : Nat                    -- Completion.lean:335
axiom champion_lower : championSteps ≤ BB6   -- Completion.lean:342
```

**Both sides are opaque axioms.** There is no content to prove: `≤` between two `Nat`s about
which nothing is known is not a theorem, it is a hypothesis. Discharging E2 therefore is not
"prove an inequality" — it is **"give `BB6` a definition"**, and that is the real shape of
the task. Concretely you need, in Lean:

1. A type of 6-state 2-symbol machines `TM6` (a transition table, not a hardcoded `step`).
2. A generic `stepOf : TM6 → Cfg → Option Cfg` and `stepsOf`.
3. `Halts (M : TM6) : Prop := ∃ n, stepsOf M n init = none`, and `haltTime M`.
4. `BB6 : Nat` **defined** as the supremum of `haltTime M` over halting `M` — which requires
   knowing the sup exists, i.e. that the halting set is finite-and-bounded. Since `TM6` is a
   *finite* type (6·2 cells × 13 outcomes), `BB6` is a max over a finite set of a partial
   function, so this is definable without any decidability of halting: take the max over the
   finite subtype `{M // Halts M}`, using `Nat.find` for `haltTime`. **This is routine and is
   the cheap part.**

Once `BB6` is *defined*, `champion_lower` becomes near-trivial:

```lean
theorem champion_lower : championSteps ≤ BB6 :=
  le_sup_of_mem ⟨champion, champion_halts⟩
```

i.e. **the champion is a member of the family the sup ranges over**. All the difficulty
collapses into the single hypothesis `champion_halts : Halts champion`.

### 1.2 Consequence: the exact value is never needed

This is the key tractability finding. Define

```lean
noncomputable def championSteps : Nat := haltTime champion   -- given champion_halts
```

Then `championSteps ≤ BB6` follows from membership alone. **The tower is never written
down.** The `≈ 2↑↑↑5` magnitude is a fact *about* `championSteps`, not a fact the proof
consumes. The representational obstacle in the task brief — "you cannot `rfl` through 10↑↑15
steps" — is real for the *value*, but the value is not on the critical path for
`champion_lower`.

(It *is* on the critical path for `enumeration_upper`, which must compare every other
machine's halt time against `championSteps`. That is a separate axiom and a separate,
strictly harder problem. E2 does not touch it.)

### 1.3 What is genuinely hard: `Halts champion`

The champion's halt is reached only after `> 2↑↑↑5` steps. Proving `∃ n, steps n init = none`
requires an accelerated, inductive certificate. The published structural analysis (wiki,
verbatim) reduces it to a **5-register machine** `S1(len0, a0, phase, a, b)`:

```
start:  S1(3, 7, 2, 6, 63)

Inc2:   S1(len0, a0+1, 2, a, b) --> S1(len0, a0,   1, a+b+2, 2^b - 1)
Inc1:   S1(len0, a0+1, 1, a, b) --> S1(len0, a0,   0, a+b+2, 2^b - 1)
Inc0:   S1(len0, a0+1, 0, a, b) --> S1(len0, a0,   2, a+b+1, 2^b - 1)
Rst1:   S1(a0,   0,    1, a, b) --> S1(a0+a+2, (2^(a0+2)-1)*2^a - 1, 2, b, 2^b - 1)
Rst0:   S1(a0,   0,    0, a, b) --> halt
```

Read this carefully, because it determines everything downstream:

- **The halt is a structural event, not a step count.** `Rst0` fires when the `a0` counter is
  exhausted while `phase = 0`. Proving the halt means proving this configuration is *reached*.
  No arithmetic on the total step count is involved.
- **The `Inc*` rules are a 3-phase odometer** decrementing `a0` and folding `b` into `a`.
- **`Rst1` is the level transition** and the sole source of the growth: it resets `a0` to
  `(2^(a0+2)-1)*2^a - 1`, exponential in the *previous* level's parameters. Iterating `Rst1`
  is what produces the tower-of-towers; the pentational magnitude is the composition of
  ~a tower's worth of these.
- **The recursion terminates** because the `phase` cycles `2→1→0→2` and `Rst0` is reachable
  from `phase = 0`; termination is a parity/phase argument on a well-founded descent of `a0`,
  not a size argument.

So the required Lean artifact is: (a) the tape-level proof that each of the five rules holds
as a macro-transition of the actual TM, and (b) the arithmetic/termination argument that the
5-register system reaches `Rst0`. Part (b) is small. Part (a) is the work.

---

## 2. Reusable machinery inventory

The repo's assets are real but sit at the wrong layer for this job. Inventory with pointers.

### 2.1 Directly reusable

| Asset | Location | Reuse for E2 |
|---|---|---|
| `Tape` / `Cfg` / `wr` / `mvR` / `mvL` | `lean/Template.lean:74-98` | verbatim copy; identical across all 6 machine files |
| `steps : Nat → Cfg → Option Cfg` | `lean/Template.lean:122-124` | verbatim |
| **`steps_add`** | `lean/Template.lean:133`, `lean/X2.lean:122`, `O3.lean:145`, `O2.lean:121`, `O18.lean:139`, `O17.lean:124` | **the chaining discipline exists and is uniform**; `rw [steps_add, <leg>, someBind]` is the corpus idiom |
| `someBind` / `noneBind` | `lean/X2.lean:118` | verbatim |
| `steps_shift` (translation equivariance) | `lean/Template.lean:429`; x2 variants `X2.lean:7014, 7029, 11094` | verbatim; the reason every tile is stated `∀ p : Int`. **Essential** — the champion's right-growing tape means every macro-rule must be position-parametric |
| `strong_ind` | `Template.lean:367`, `RunStructure.lean:164`, `Mirror.lean:32` | verbatim (already triplicated) |
| `pow01` / `pow10` word algebra + commuting lemmas | `lean/Template.lean:181-229` | **directly applicable** — see §5, the champion's tape is literally a `(100)^n` word |
| `BlankNorm` tail-padding congruence: `steps_rpad_zeros` | `lean/BlankNorm.lean:256`, `:285`; single-step bisimulation `step_crtail` at `:78` | **highly applicable** — lets a macro-rule proved on a finite tape be transported across an arbitrary blank tail. The only machine-touching part (`step_crtail`) is discharged by exhaustive case split, so porting is mechanical |
| `steps_prefix_ne_none` | `lean/X2.lean:3156` | prefix of a `some`-run is halt-free; needed to certify no *premature* halt |
| `steps_left_mono` / `steps_right_mono` | `lean/X2.lean:10337`, `:10357` | tape-length monotonicity / anchor squeeze |

### 2.2 Reusable as *pattern*, not as code — the tile-and-fold idiom

This is the repo's strongest asset and it maps onto the champion's `Inc*`/`Rst*` rules almost
one-to-one. The idiom: prove a fixed-shape **tile** by kernel `rfl`, then a `∀ n` **fold** by
induction gluing tiles with `steps_add`.

| tile (`rfl`) | fold (`∀ n`, induction) |
|---|---|
| `sweepEF_tile` `X2.lean:215` | `sweepEF` `X2.lean:229` |
| `chew_tile` `X2.lean:325` | `chewFold` `X2.lean:341` |
| `sepCross_tile` `X2.lean:395` / `blockStep` `:416` | **`cascadeFold` `X2.lean:459`** (folds over a `List Nat` of block sizes) |
| `braid_tile` `X2.lean:5484` | `braid_run` `X2.lean:5533` (double induction, `N` outer round-trips) |
| `trailTrans`/`trailCycle` `X2.lean:9589`/`:9601` | `trailFold` `X2.lean:9630` |
| `leadTile` `X2.lean:11115` | `leadTransit` `:11130` → `genLead` `:11230` |
| `sweepDE` | `Template.lean:261` — `steps (2*j) ⟨.D, p, ⟨pow01 j ++ L, true, R⟩⟩ = some ⟨.D, p - 2*j, ⟨L, true, pow10 j ++ R⟩⟩` |

The closest existing analogue to a champion macro-rule is `X2.lean:1777`:

```lean
theorem outer_tick_noCarry_run : ∀ (n : Nat) (p : Int) (t work : Nat) (M' R : List Bool),
    steps (runSteps t n) ((⟨t, work + 2 * n⟩ : Odo).toCfg p (pow10 n ++ M') R)
      = some ((⟨t + 2 * n, work⟩ : Odo).toCfg (p + 2 * (n : Int)) M' R)
```

This is *exactly* the shape of `Inc2` — an odometer tick advancing a register, tail-parametric
in `M'`/`R`, position-parametric in `p`. **The idiom transfers. The step count does not (§3).**

Higher-order folds parametrized by a *list* of block sizes — `cascadeFold` (`X2.lean:459`),
`trailFold` (`:9630`), `ascSpine` (`:8758`), `interiorFold` (`:8932`) — are the right shape for
the champion's `(100)^n` block region.

### 2.3 Reusable as *pattern* — the strong-induction level assembly

The x2 track's just-closed `regenLaw_closed` is structurally the same manoeuvre the champion
needs for `Rst1` (level transition, conditional on strictly-lower levels):

- `RegenLaw` def — `X2.lean:6746`; `TrailLaw` — `X2.lean:10537`; `LeadLaw` — `X2.lean:9909`.
- `regenLaw_of_trailLaw` — `X2.lean:11578`: the four-summand split of `exitSteps k`, glued by
  four `steps_add`, **conditional on `RegenLaw m` for `m ≤ k-2`**.
- `framingArith` — `X2.lean:9245`: the arithmetic identity making the split type-check.
- `regenLaw_all_of_trailLaw_all` — `X2.lean:11635`, strong induction via
  `carryExit_strong_frame_ge` (`X2.lean:6845`), bases `regenLaw_4/5/6`.
- **`regenLaw_closed`** — `X2.lean:12191`: `∀ k, 4 ≤ k → RegenLaw k`.
- Anti-vacuity controls at `X2.lean:12195-12199` (`RegenLaw 8`, `RegenLaw 100`) and the
  cross-check `assembly_agrees_7` (`X2.lean:11609`).

**The `Rst1` level-transition proof is the same shape as `regenLaw_of_trailLaw`.** That is a
genuine, earned, transferable asset — the team has done this manoeuvre once and it worked.

### 2.4 Reusable arithmetic — `Mirror.lean` (and why it does *not* apply)

`Mirror.lean` is the one truly machine-agnostic file: `bmap`/`orb` (`:198-208`), the generic
`q`-adic valuation `vqn`/`vq` (`:46`/`:139`), `branch_conj` (`:208`), `run_closed_form`
(`:266`), and the 17-corollary census (`:286-412`) where each machine's run law is a one-line
`decide`/`omega` instantiation.

**It does not apply to the champion.** `Mirror` models *affine-over-`q`* maps `v ↦ (pv+e)/q` —
the Collatz-class `×3/2`, `×4/3`, `×8/3` dynamics of the cryptids. The champion's `Rst1` is
`a0 ↦ (2^(a0+2)-1)·2^a - 1`, which is **exponential in `a0`**, not affine. No `q`-adic
valuation argument reaches it. `RunStructure.lean` is likewise hardcoded to o4's base-4/3
odometer (`RunStructure.lean:28-35`, literals 3/4/9/14/1) and is explicitly superseded by
`Mirror`. **Neither file contributes to E2.**

### 2.5 The critical gap: closed-form step arithmetic tops out at `Θ(4^k)`

Everything closed-form in the corpus is polynomial × `2^k` or `4^k`:

- `runSteps_closed` `X2.lean:1754` — `4nt + 4n² + 6n`
- `carryDigit_closed` `X2.lean:1298` — `2^(n+2) - 3`
- `exitSteps` `X2.lean:4316` — `2^(2k-3) + k·2^(k-1) + 2^(k-2) + 2`, with an order-4 linear
  recurrence certificate at `:4348` and 5 grounded levels at `:4322`
- `trailSteps_closed` `X2.lean:8023` — `2^(k+1) + k + 364`
- `leadRec_closed` `X2.lean:8048` — `3·2^(j+5) - 9(j+6) + 112`
- `interiorFoldSteps_closed` `X2.lean:9204` — `Θ(4^k)`, **the corpus maximum**

**There is no iterated-exponential, tower, or Knuth-arrow arithmetic anywhere in the Lean
corpus.** Tower language appears only in prose (`O17_GATE_LAW_2026-07-07.md:53`, explicitly
`[OBSERVED]`) and in the `Completion.lean:329` comment behind the `championSteps` axiom.

### 2.6 The corpus has essentially no halting proofs

Two, both gate-local and trivial:

- `lean/O17.lean:213` — `seam_halts ... : steps 3 ... = none`
- `lean/X2.lean:1142` — `gap3_halts : steps 4 ⟨.E, 0, ⟨[], false, [false,false,true]⟩⟩ = none := rfl`

Everything else is **non-halting** (`∀ N, steps N init ≠ none`). The largest concrete run from
a blank tape is `lean/HInit.lean:575` — `h_init_reached : steps 188099 init = some c189`, built
from 189 hardcoded configs chained in 1000-step `rfl` chunks (`HInit.lean:386-573`). That is
the corpus's high-water mark for *concrete* certified simulation: **1.9 × 10^5 steps.**

The target is `> 2↑↑↑5`. The gap is not quantitative; it is a change of kind.

---

## 3. The representational problem, and the three options assessed

### Option (i) — closed-form tower expression (Knuth arrow in Lean)

Define `tower`/`hyper` in Lean, state `championSteps = <tower expression>`.

**Assessment: NO-GO.** Three independent reasons.

1. **No such expression is known.** The wiki records only the *bounds*
   `2↑↑↑5 < 2↑↑2↑↑((2^)^8 6) < 2↑↑↑6` — an **estimate**, explicitly approximate ("halt with
   time/score ≈"). There is no exact closed form in the literature to formalize. Formalizing an
   approximation as an equality would be a false claim.
2. **The reference formalization declines to do it.** busycoq's `SOBCv5.v` proves
   `halts tm c0` and stops. If the people who found the machine and wrote 1,073 lines of Rocq
   about it did not state the value, we should not assume it is cheap.
3. **The corpus has zero tower arithmetic** (§2.5) and would need it built from nothing:
   `hyper`, monotonicity, the composition laws relating `Rst1`'s `(2^(a0+2)-1)·2^a - 1` to
   tower height. That is a research-grade arithmetic library, not engineering.

### Option (ii) — output of a proven recurrence

Define `championSteps` as the value of an explicit recurrence over the 5-register system
(`Inc0/1/2`, `Rst0/1`) with per-rule step costs, prove the TM realizes it.

**Assessment: technically possible, but strictly dominated.** The recurrence is definable in
Lean (it is primitive recursive; the register system above is literally a Lean `def` with a
termination proof). But:

- It requires assigning an **exact step cost to every rule**, which means every macro-rule
  lemma must carry a closed-form count. Those counts are themselves tetrational (the `Rst1`
  cost involves `2^(a0+2)` at a nesting depth that is itself a tower), so §2.5's gap bites in
  full.
- It buys nothing. `champion_lower` does not consume the value (§1.2). You would be paying
  the entire tower-arithmetic cost for a number no downstream theorem reads.
- It is the *only* option that would help `enumeration_upper` — but `enumeration_upper` is
  Coq-BB5-scale and out of scope, and even there a comparison lemma would likely be cheaper
  than a value.

**Verdict: defer. Do not pay for this now.** Note that if it is ever wanted, the register
system in §1.3 is the right skeleton and the work in option (iii) is a strict prerequisite —
so nothing is lost by deferring.

### Option (iii) — opaque `championSteps`, inequality proven structurally ✅

Keep `championSteps` without a numeral. Define it *by description* as the champion's halt time,
and prove the inequality from membership in the sup.

```lean
-- 1. generic machine type + generic step (new; replaces the hardcoded per-machine `step`)
structure TM6 where table : St → Bool → Option (Bool × Dir × St)
def stepOf (M : TM6) : Cfg → Option Cfg := ...
def stepsOf (M : TM6) : Nat → Cfg → Option Cfg := ...

-- 2. halting, halt time, BB6 as a max over a finite type
def Halts (M : TM6) : Prop := ∃ n, stepsOf M n init = none
noncomputable def haltTime (M : TM6) (h : Halts M) : Nat := Nat.find h
noncomputable def BB6 : Nat := <max of haltTime over the finite subtype {M // Halts M}>

-- 3. the champion
def champion : TM6 := ⟨fun s b => ...⟩   -- 1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE

-- 4. THE ONE HARD THEOREM
theorem champion_halts : Halts champion := ...

-- 5. now trivial
noncomputable def championSteps : Nat := haltTime champion champion_halts
theorem champion_lower : championSteps ≤ BB6 := le_max_of_mem ...
```

**Assessment: GO. This is the tractable route and it is the only tractable route.**

- It matches the reference Rocq formalization exactly (`Lemma halt: halts tm c0`).
- It removes the tower from the statement entirely — no Knuth arrows, no closed forms, no
  `Θ(4^k)` ceiling problem in the *statement*.
- It converts `champion_lower` from "unprovable relation between two axioms" into "one halting
  theorem plus a finite-max definition".
- It is honest: `championSteps` remains a number we cannot write, and the docstring can say so
  truthfully, with the correct magnitude (`> 2↑↑↑5`) cited to the wiki as `[OBSERVED]`.

---

## 4. Scale estimate

### 4.1 Calibration points

| Artifact | Size | Time | Outcome |
|---|---|---|---|
| busycoq `SOBCv5.v` champion region | **1,073 lines Rocq** | unknown | `halts tm c0` — **done** |
| repo `X2.lean` | 12,208 lines / 1.24 MB | ~2 weeks | `regenLaw_closed`; x2 still `[OPEN]` |
| repo `Template.lean` + `Suffix.lean` (o4) | 1,442 lines | — | o4 *not* closed; `o4_ledger` still an axiom |
| repo `HInit.lean` | 633 lines | — | 188,099 concrete steps |

### 4.2 Reasoning

**Arguments that E2 is cheaper than x2:**

- **No discovery risk.** x2's 12k lines are overwhelmingly *search* — hand-finding sweep
  invariants, guessing tile shapes, fitting pads (`regenPad_law` `X2.lean:6758`,
  `trailLaw_pad_forced` `X2.lean:10469`). For the champion, **the rule set is published**
  (§1.3, five rules, verbatim). You are transcribing a known proof, not finding one. In my
  estimation this removes the majority of the cost.
- **A reference implementation exists** and is 1,073 lines in a system with comparable
  expressiveness. Lean-without-mathlib is more verbose than Rocq-with-tactics, so scale up —
  but 1,073 lines is a hard anchor, not a guess.
- **The hardest structural manoeuvre has already been rehearsed.** `regenLaw_of_trailLaw` +
  strong induction (`X2.lean:11578`, `:11635`) is the exact shape `Rst1` needs.
- **The tape is benign** (§5): one-sided, fixed left boundary, uniform `(100)^n` alphabet.

**Arguments that E2 is more expensive than 1,073 Rocq lines:**

- **No mathlib.** `Nat.find`, finite types, max-over-finite-subtype, `2^n` arithmetic — all
  from scratch. The corpus already re-derives Euclid by hand (`Mirror.lean:87`).
- **No generic TM.** Every machine in the repo is a copy-pasted 12-case `step`
  (`Template.lean:104-117`, `X2.lean:97`, `O3.lean:117`, ...). There is **no** `TM6` /
  transition-table type. Introducing one and re-basing the existing machinery on it is a
  refactor with blast radius across six files — or, if `steps_shift`/`BlankNorm` are simply
  re-proved for the champion namespace, a seventh copy (cheaper, uglier, and the repo's
  established practice).
- **No `-->*` reachability closure and no `follow`/`finish` automation.** busycoq leans hard on
  these; every step of the port is more manual without them.
- **The `steps_add` re-architecture** (§4.4) — the real cost.

**Estimate: 3–6 weeks of focused work**, i.e. roughly the x2 track's duration, with materially
lower variance because the target is specified rather than searched for.

- **Not days.** The count-free reachability layer alone is a new proof discipline for this
  corpus, and 5 macro-rules × (tile + fold + position-parametricity + blank-tail transport) is
  well past a week even with the rules handed to you.
- **Not months**, *provided* option (iii) is chosen. If option (i) or (ii) is attempted, it
  becomes months and possibly unbounded, because tower arithmetic would have to be built from
  nothing with no reference implementation to copy.

### 4.3 Decomposition and rough weighting

| # | Task | Est. | Risk |
|---|---|---|---|
| 1 | Count-free reachability layer: `Reaches c c' := ∃ n, steps n c = some c'`, transitivity, `Halts`, interaction with `steps_add` | 3–5 d | **high** (new discipline, §4.4) |
| 2 | `TM6` transition-table type + generic `stepOf`/`stepsOf`; decide refactor-vs-copy | 2–4 d | med (blast radius) |
| 3 | `BB6` as max over finite subtype; `Nat.find` halt time; `le_max_of_mem` | 2–4 d | low (routine, but no mathlib) |
| 4 | Champion `step`, sanity anchors, Python cross-check (cf. `template_crosscheck.py`) | 1–2 d | low |
| 5 | Tape encoding: the `(100)^n` block word, `S0`/`S1` decoder, `pow01`/`pow10` reuse, `BlankNorm` transport | 4–7 d | med |
| 6 | The three `Inc0/1/2` macro-rules as tile+fold, position- and tail-parametric | 5–8 d | med |
| 7 | `Rst1` level transition (the `regenLaw_of_trailLaw` analogue) + strong induction over levels | 5–10 d | **high** |
| 8 | `Rst0` halt event + termination of the 5-register system | 2–4 d | low |
| 9 | Assembly, anti-vacuity controls, axiom audit, docstring corrections (§0) | 2–3 d | low |

### 4.4 The single hardest sub-obstacle

**It is not the tower. It is the corpus's step-exact `Option`-valued `steps` discipline.**

Every load-bearing lemma in this repo carries an **explicit `Nat` step count as an argument**:

```lean
steps (exitSteps k) (regenIn k p (2^(k-1) + 9) marker R) = some (cascadeReg k 1 (p - 2^k) marker R)
                                                            -- RegenLaw, X2.lean:6746
steps (trailSteps k) (cascadeReg 4 1 ...) = some (cascadeReg k 1 ...)
                                                            -- TrailLaw, X2.lean:10537
steps (runSteps t n) (...) = some (...)                     -- X2.lean:1777
```

This is a genuine strength — it makes the counts *checkable* and forces identities like
`framingArith` (`X2.lean:9245`) that catch errors. **But it is exactly the wrong discipline
here.** To state the champion's `Rst1` rule in this style you must write

```lean
steps (RST1_COST len0 a0 a b) (champCfg ...) = some (champCfg ...)
```

and `RST1_COST` at nesting depth ~15 is a tower. You cannot write it (no closed form exists,
§3(i)), and even if you could, `framingArith`-style arithmetic identities over towers do not
exist in the corpus (§2.5). **The entire corpus idiom breaks at `Rst1`.**

The fix is not deep, but it is a **re-architecture, not a lemma**: introduce

```lean
def Reaches (c c' : Cfg) : Prop := ∃ n, steps n c = some c'
theorem Reaches.trans : Reaches a b → Reaches b c → Reaches a c   -- via steps_add
def Halts (c : Cfg) : Prop := ∃ n, steps n c = none
theorem halts_of_reaches : Reaches c c' → Halts c' → Halts c
```

and restate every champion macro-rule in `Reaches` form, existentially quantifying the count
away. `steps_add` (`Template.lean:133`) is exactly what makes `Reaches.trans` go through, so
the foundation is in place — this is `busycoq`'s `-->*` and `halts_evstep`, which is why their
proof is 1,073 lines and not 12,000.

**This is the crux, and it must be done first.** It is ~100–200 lines. Everything downstream
depends on it, and attempting the macro-rules before it will produce unstatable goals. It is
also the reason a naive estimate ("we did x2 in 2 weeks, so ~2 weeks") is wrong in *both*
directions: the discipline change is unbudgeted cost, but it also makes each subsequent rule
much cheaper than its x2 analogue, since no closed-form count has to be found or verified.

**Runner-up obstacle:** §1.1 — `BB6` must be *defined*, which nothing in the repo currently
does, and which changes `Completion.lean`'s interface. Low technical risk, non-trivial design
churn, and it is the part that makes `champion_lower` a theorem *at all*.

---

## 5. Structure: is the champion a nested odometer/cascade?

**Yes — and it is structurally *friendlier* than the cryptids in every respect except depth.**
Empirically verified by direct simulation (300M steps, this session):

| Observation | Value |
|---|---|
| Left expansions | **exactly 10**, all within the first 744 steps; left boundary fixed at `pos = -10` thereafter |
| Return to left boundary after step 744 | **never** (0 in 300M steps) |
| Tape span at 60M / 200M / 300M steps | 9,703 / 17,539 / 21,430 cells |
| Growth law | span ≈ `Θ(√steps)` — a sweeping machine, cost ≈ 4 × distance per macro-step |
| Tape alphabet (RLE, at 20M steps) | `(1,3)(0,1)(1,3)(0,2)(1,1)(0,2)(1,4)(0,2)(1,1)(0,1)(1,26)` then **`(1,1)(0,2)` repeated** — i.e. a fixed prefix followed by `(100)^n` |
| Block count at span ≈ 5,690 | oscillates 126 / 128 / 130 — a counter incrementing near the left while the right end extends |
| Right-edge extension rate | ~1 cell per ~21,850 steps at that scale (≈ one round trip) |

**Reading.** After a 744-step preamble the machine is a **one-sided, right-growing sweeper**
over a uniform `(100)^n` block word, with a counter region near the (now fixed) left boundary.
Each macro-step is a sweep out to the right end and back, performing one odometer tick. That is
precisely `sweepDE`/`sweepEF`/`cascadeFold` territory.

**Consequences for E2 — all favourable:**

- **The `pow01`/`pow10` word algebra (`Template.lean:181-229`) applies directly.** The `(100)^n`
  region is a `pow`-word; the corpus already has the commuting lemmas.
- **The left boundary is fixed after 744 steps** — so a `prefix744` concrete run (the
  `HInit.lean` / `prefix471` pattern, `Template.lean:585`) suffices to reach the periodic
  regime, and *nothing* to the left ever needs modelling again. Note `Template.lean:475-480`
  warns a monolithic symbolic-tail `rfl` blows the `whnf` budget at ~60 steps, so expect ~25
  chunked `rfl` lemmas — cheap and mechanical, and 744 is well under `HInit`'s 188,099.
- **One-sided growth means `BlankNorm.steps_rpad_zeros` (`BlankNorm.lean:256`) is exactly the
  right transport** — all growth is into the right blank tail.
- **`steps_shift` (`Template.lean:429`) is essential and already exists** — the sweep region
  translates rightward without bound, so every rule must be `∀ p : Int`.
- **The halt is a single clean event:** the only halting transition is `B` on symbol `1`
  (`1RZ`). Throughout the periodic regime `B` always reads `0`. So `Rst0` = "the one time `B`
  meets a `1`". This is a *local, structural* condition — exactly what makes option (iii)
  work.

**Where it differs from the cryptids.** The cryptid odometers (o4's base-4/3, x2's nested
odometer) have **fixed nesting depth**, which is why their closed forms cap at `Θ(4^k)`. The
champion's `Rst1` **creates a new level whose size is exponential in the previous level's
parameters**, and iterating that is what produces `> 2↑↑↑5`. So:

- the **mirror-ladder machinery does *not* apply** (§2.4 — `Mirror` handles affine `(pv+e)/q`,
  not exponential `(2^(a0+2)-1)·2^a - 1`);
- the **`RunStructure` odometer does not apply** (hardcoded to o4's 4/3);
- but the **tile-and-fold idiom and the strong-induction level assembly *do*** (§2.2, §2.3),
  and they are the parts that matter.

---

## 6. Recommendation

### GO — with a mandatory restatement.

**Recommended representation: option (iii)** — `championSteps` opaque, defined by description
as `haltTime champion`; `BB6` **defined** as a max over the finite subtype of halting machines;
`champion_lower` proved by membership. The exact value is never written and never needed.

**Reasons:**

1. It is the only option that is actually reachable. Options (i) and (ii) both require tower
   arithmetic that does not exist in the corpus, has no reference implementation, and — for
   (i) — has no known exact expression in the literature to formalize.
2. It matches the community reference formalization exactly (`Lemma halt: halts tm c0`,
   `busycoq/verify/SOBCv5.v`), which is 1,073 lines and *deliberately* states no count.
3. It is the only option under which `champion_lower` is a theorem at all — as currently
   stated it relates two opaque axioms and has no content (§1.1).
4. The champion's structure is favourable (§5) and the repo's strongest transferable asset —
   the tile-and-fold + strong-induction level assembly just proven out on `regenLaw_closed` —
   maps onto it directly.

**Scale: 3–6 weeks.** Lower variance than x2 because the rule set is published; higher floor
than "port 1,073 Rocq lines" because there is no mathlib, no generic TM type, and no `-->*`
layer.

**Hardest sub-obstacle: the step-exact `steps` discipline** (§4.4). Build the count-free
`Reaches` layer **first**; it is ~150 lines, it is what makes every downstream rule statable,
and it is the difference between a 1,073-line proof and an impossible one. Runner-up: giving
`BB6` a definition (§1.1) — low risk, but it changes `Completion.lean`'s interface.

**Sequencing note.** E2 is genuinely independent of the mathematics — it touches no holdout,
no `NormalityPQ`, no `(K)`-band. It can be started at any time and by anyone, and unlike the
17 named conjuncts it is **guaranteed to close**. Its value is proportional to how much the
project wants `BB6_eq_championSteps`'s axiom list to shrink: E2 removes 1 of the 2 engineering
axioms, leaving `enumeration_upper` (Coq-BB5-scale) as the sole engineering residue.

**Caveat, stated plainly.** E2 does *not* move BB(6) toward resolution. `champion_lower` is
the easy half of an inequality whose hard half (`enumeration_upper`) is Coq-BB5-scale and
whose hypothesis (`AllHoldoutsNonHalt`) contains 17 open problems. E2 buys **axiom hygiene and
a credible claim of self-containedness**, not mathematical progress. If the 3–6 weeks compete
directly with work on the (K)-band, the (K)-band should win.

**Immediate no-cost action regardless of go/no-go:** fix §0.1. The docstring at
`Completion.lean:328-330` and the four propagated copies attribute the machine to the wrong
person and understate its magnitude by an entire hyperoperation level (`10↑↑15` vs `> 2↑↑↑5`).

---

## Sources

- [BusyBeaverWiki: `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE`](https://wiki.bbchallenge.org/wiki/1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE) — discoverer, magnitude bounds, the five `Inc`/`Rst` rules, Rocq proof link
- [BusyBeaverWiki: BB(6)](https://wiki.bbchallenge.org/wiki/BB(6)) — record history, `S(6) > Σ(6) > 2↑↑↑5`
- [busycoq `verify/SOBCv5.v` L10210-11283](https://github.com/ccz181078/busycoq/blob/3f302b87f5fb933c46e97672ffbb6907f373fb6e/verify/SOBCv5.v#L10210-L11283) — the existing machine-checked halting proof
- [sligocki: BB(6,2) > 10↑↑15](https://www.sligocki.com/2022/06/21/bb-6-2-t15.html) — the superseded Kropitz record
