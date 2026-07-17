# `h_init` blueprint — `blank → M1(1)`, sized and decomposed by TRANSPORT

**2026-07-17.** Every number below is reproduced by probes committed alongside this
doc, all driven by a simulator **verified against `lean/X2.lean`'s kernel-checked
`sanity50`/`sanity100`** before one step was trusted. Labels are rigorous:
**[PROVEN]** = green in `X2.lean`; **[OBSERVED]** = measured on the exact on-path
orbit; **[OPEN]** = stated, not proven. No machine is decided; no label is upgraded.

Target obligation (one of `x2_nonhalt`'s **three** hypotheses, `X2.lean:3095`):

```lean
h_init : ∃ n, 1 ≤ n ∧ steps n init = some (M1 1)
```

## Reproduce

```
python x2hi_sim.py        # simulator, self-checks vs sanity50/sanity100  -> PASS
python x2hi_transport.py  # 13 lemma transcriptions, each IN->machine->OUT -> PASS
python x2hi_m1.py         # M1(1) read off cell-for-cell at raw step 188 099
python x2hi_cover.py      # greedy-maximal transport cover of the 188 099 run
python x2hi_gaps.py       # residue grouped BY WORD (never by length)
python x2hi_classify.py   # residue split: fixed tiles vs bounded singletons
```

---

## 1. What `M1(1)` is, cell-for-cell  [OBSERVED, exact]

The blank-tape orbit reaches `M1(1)` at **raw step 188 099** (confirmed
independently: the run has exactly one earlier `E`-config whose leading `0`-gap is
`22`, at step 52 159, and 188 099 is the second — so 188 099 is the milestone
`X2.lean:1094` names, cross-checked by the gap-22 spec, not merely quoted):

```
state E, pos -25, head on the leading 0.  Full tape (left of head is blank):

  0^22 1 0^4 (10)^6 1^503 0^2 1^253 0^2 1^125 0^2 1^61 0^2 1^29 0^2 1^13 0^2 1^5 0^2 1

  extent [-25, 1017] = 1043 cells ; 997 ones ; odd generation, K = 9.
```

This matches `X2.lean:1094`'s quoted `M1(1)` form **exactly**
(`0^22 (1 0^4 (10)^6) 1^503 0^2 1^253 …`). The trailing cascade
`1^503 0² 1^253 0² 1^125 0² 1^61 0² 1^29 0² 1^13 0² 1^5 0² 1` is the doubled register
`[2^9−9, 2^8−3, …, 5, 1]` — i.e. `M1(1)` is the first mature milestone, and the whole
prefix run is the machine *building the first generation's cascade from nothing.*

> **Milestone-family caveat (roadmap §1.4, [OPEN]).** This is the concrete config
> `M1(1)`. `h_init` needs it to be defeq to the `M1 1` of the *same* `M1 : Nat → Cfg`
> family `h_low`/`h_doub` quantify over. That identification is a cross-cutting
> obligation, not part of `h_init`'s step count, and is not discharged here.

---

## 2. The transport decomposition of the 188 099 steps  [OBSERVED, exact]

**Method (non-negotiable, roadmap §1.5).** A window is a sub-call **only** if it is a
*specific proven `∀` theorem* whose IN pattern matches the on-path config
cell-for-cell **and** whose asserted OUT the machine actually produces (checked by
simulation). Identification is never by length. The 13 lemma transcriptions each pass
an IN→machine→OUT self-check (`x2hi_transport.py`, PASS) — a wrong transcription
cannot silently produce a hit, because the OUT check would fail. Tape extent is
derived from the tape (`min`/`max` of set cells), never from a caller `lo`/`hi`.

Greedy-maximal cover (`x2hi_cover.py`):

```
raw steps            : 188 099
covered by proven ∀  : 182 028   (96.8%)      in 398 theorem instances
uncovered residue    :   6 071   ( 3.2%)      in 118 gaps / 25 distinct motifs
```

**`∀`-lemma-carried fraction: 96.8%.** (Calibration: `REGEN(7)` was 66%, `REGEN(6)`
10%. `h_init` is far *more* carried than either, because it is a long run made almost
entirely of mature `TOPGRIND` rounds.)

Per-lemma budget (all [PROVEN], all `[propext, Quot.sound]` in `X2.lean`):

| lemma (§ in X2.lean) | steps | % | instances |
|---|---:|---:|---:|
| `braid_topgrind` (§ braid) | 155 486 | 82.7 | 58 |
| `regen7_factored` | 7 590 | 4.0 | 3 |
| `regen6_transport` | 5 054 | 2.7 | 7 |
| `descent_std_tile` | 4 890 | 2.6 | 82 |
| `descent_final_tile` | 2 700 | 1.4 | 27 |
| `regen5_transport` (=`carry_exit_j4`) | 2 398 | 1.3 | 11 |
| `sweepEF` | 2 040 | 1.1 | 87 |
| `regen4_transport` (=`carry_exit_j3`) | 1 190 | 0.6 | 17 |
| `ecombChewFold` | 222 | 0.1 | 5 |
| `braid_tile` | 220 | 0.1 | 10 |
| `braid_entry` | 164 | 0.1 | 82 |
| `outer_tick_noCarry_at` | 58 | 0.0 | 1 |
| `ecfold` | 16 | 0.0 | 8 |

**Structural answer to the task's second question.** The blank→M1(1) run is **NOT a
distinct start-up phase with its own motifs.** It is 82.7% `braid_topgrind` and is
otherwise built from exactly the doubling-phase library — `DESCENT` std/final tiles,
`REGEN(4/5/6/7)`, `sweepEF`, `ecombChewFold`. `h_init` **reuses the `carry_step`
building blocks**; it introduces no new large-scale structure. The recognizable
`REGEN`/`TOPGRIND`/`DESCENT` motifs are all present and dominant.

---

## 3. The named gaps — the only new work  [OBSERVED]

The 3.2% residue is 25 distinct motifs (grouped by `(st,h)` word, `x2hi_gaps.py`;
word-identity is equivalent to trace-identity, method inv. 2). Every residue gap is
**bounded** — the largest head-excursion span over *any* residue gap is 1015 cells,
the longest gap is 1043 steps. Each is pinned by BOTH endpoints (the covered lemma
before/after it, method inv. 3). `x2hi_classify.py` splits them:

**(A) 8 repeated fixed-window tiles — 2 855 steps.** Each is one motif recurring
identically, so each is **one new bounded `∀L∀R` tile lemma (kernel `rfl`)**, reused:

| tile | steps × count | span | role (pinned by endpoints) |
|---|---:|---:|---|
| descent-entry turnaround | 36 × 59 | 32 | `braid_entry` → … → `sweepEF`: `E` inside a `1`-block turns and lays the descent comb (`1^30[1]1^117… → 0²1·(10)^…`) |
| descent-entry, short block | 34 × 8 | 30 | same shape, smaller block |
| register-setup tile | 15 × 12 | 6 | `descent_std_tile` → `braid_topgrind` connector |
| block-cross turnaround | 16 × 6 | 12 | `braid_entry` → `sweepEF` |
| block-cross turnaround | 14 × 6 | 10 | `braid_entry` → `sweepEF` |
| tick connector | 20 × 3 | 11 | `braid_topgrind` → `descent_std_tile` |
| comb re-entry | 6 × 4 | 3 | `ecombChewFold` → `braid_topgrind` |
| seam | 5 × 3 | 4 | → `ecfold` |

**(B) 17 singleton motifs — 3 216 steps.** Distinct words, each occurring once, each a
**bounded concrete kernel run** (`steps n cfg = some cfg'`, fully concrete tape — no
`∀`-tail, so kernel `rfl` is linear in `n`, not exponential-in-`p`; cf. `X2.lean` §1.8
warning applies only to *symbolic* `p`). Lengths 9…1043. They are the **inter-round
carry-completion connectors**: 12 of the 17 sit `braid_topgrind → … → braid_topgrind`
(or `→ ecfold`/`ecombChewFold`), entry word `1^8 0 1^5 [0] 0…` (head at the far-right
boundary `0`, blank to the right, growing doubled cascade to the left). They grow with
the cascade height because the head rides back across it — the same growing-arity
signature as `RegenLaw ∀k`. **But for `h_init` there are only finitely many** (K=9),
so no `∀k` law is invoked: 17 concrete configs, each ≤ 1043 steps.

The longest, 1043 steps, is *below* the kernel budget the paper already spent on
`regen6_transport` (a 722-step brute kernel `rfl`) — feasibility is established by
precedent.

---

## 4. Is `h_init` mechanical? — VERDICT

**Yes, mechanical, and it needs NO new mathematics and NO `∀k` `RegenLaw`.** The
reason is structural: `h_init` is a **single finite trajectory** (not a `∀g` family),
so it is a finite composition. 96.8% of it is discharged by *reusing the proof terms*
of the existing `∀` primitives (`steps_add` + `steps_pos_shift` threading, exactly the
paper's §5j `lowPhaseEven_g2` style); the remaining 3.2% is 8 small bounded tiles plus
17 bounded concrete kernel runs — all kernel-checkable, none requiring the open
`carry_step`.

This is a genuine finding, not a restatement: the worry that `h_init` might be a
distinct hard phase is **refuted** — it is the same TOPGRIND/DESCENT/REGEN machinery,
and its one growing feature (the inter-round connectors) is finite here.

### Concrete Lean blueprint

Prove `steps 188099 init = some ⟨.E, -25, M1(1)-tape⟩` by `steps_add`-chaining ~423
segments left-to-right, in on-path order (extract the exact ordered list with
`x2hi_cover.py`; each entry carries its start step, lemma, params, count):

1. **Skeleton.** `steps (Σ cᵢ) init = some M1(1)` via repeated
   `steps_add`/`someBind`, one rewrite per segment. `Σ cᵢ = 188099` (checked).
2. **Covered segments (398, = 96.8%).** Each rewrite is one existing theorem at its
   on-path instantiation, positions carried by `steps_pos_shift` (translation in
   `pos` is `∀`, `X2.lean:6892`) and tails by the segment's concrete `L`/`R`:
   - `braid_topgrind N Lc …` ×58 (the bulk), `descent_std_tile v …` ×82,
     `descent_final_tile …` ×27, `sweepEF m …` ×87, `braid_entry` ×82,
     `regen4/5/6/7` transports ×(17/11/7/3), `braid_tile` ×10, `ecombChewFold` ×5,
     `ecfold` ×8, `outer_tick_noCarry_at` ×1.
   - No new lemma; these are proof-term reuse. (Instantiation params per instance
     are emitted by the probe.)
3. **New tile lemmas (8, = 1.5%).** For each fixed motif in table (A), one
   `theorem hinit_tile_<name> (p) (L R) : steps <len> ⟨.E, p, ⟨L, false, <IN>⟩⟩
   = some ⟨.E, p+<dp>, ⟨<OUT>⟩⟩ := by rfl` (windows ≤ 36 steps, bounded span). Each
   is reused at all its sites via `steps_pos_shift`.
4. **Concrete residue runs (17, = 1.7%).** For each singleton, one
   `theorem hinit_seg_<k> : steps <len> <concrete cfg> = some <concrete cfg> := by rfl`
   (fully concrete tape, `len` ≤ 1043; chunk the longest if `whnf` depth needs it,
   per §1.8). These are the inter-round connectors; they do **not** generalize `∀k`
   and do not need to — 17 concrete instances suffice for K=9.

### Honest gaps / caveats

- **Engineering, not mathematics.** Assembling ~423 `steps_add` compositions with
  correct position/tail threading is real work (comparable to one mature `X2.lean`
  section), but every ingredient is bounded and kernel-checkable. "Mechanical" =
  no new math and no open object; it is **not** "free" (roadmap §1.1 was right).
- **Milestone-family identification** (§1 caveat) is separate and still [OPEN].
- The 17 singletons *look like* `RegenLaw ∀k` fragments; if one later wanted a
  *uniform* proof they would route through that open object — but `h_init` does not
  require it, because K is fixed.

---

## 5. Summary line

`h_init` is **mechanical**; **96.8%** (182 028 / 188 099 steps, 398 instances) is
already carried by existing `∀` lemmas, dominated by `braid_topgrind`. The 3.2%
residue is **8 new bounded `∀L∀R` tiles + 17 bounded concrete kernel runs**, none
needing new mathematics or the open `carry_step`/`RegenLaw ∀k`. `M1(1)` is
`0^22 1 0^4 (10)^6 1^503 0² 1^253 0² 1^125 0² 1^61 0² 1^29 0² 1^13 0² 1^5 0² 1` at
`E, pos −25`, matching `X2.lean:1094` cell-for-cell. It is the doubling-phase library
reused, not a distinct start-up phase.

**No machine decided. No label upgraded.**
