# x2 weapon inventory + gap map (2026-07-19)

Full re-analysis of `lean/X2.lean` (green baseline 18d7904, cold-built, axiom-clean) to catalogue
the reusable `∀`-machinery and pin, per remaining problem, *exactly* what is missing. Every "have"
below is a GREEN `[propext, Quot.sound]` theorem verified in the cold build. Labels are strict.

## The decisive structural finding

The program already has, `∀k`/`∀n`:
- **the entire ARITHMETIC + STRUCTURE layer**, and
- **every PER-UNIT machine transport** (one block / one comb / one cascade level / one leg).

What is missing — and it is the *whole* remaining gap for `RegenLaw ∀k` — is the **`∀k` MACHINE
ASSEMBLY**: composing the per-unit transports along the growing `exitList`/`descCascade` structure.
The "closed forms in hand" (Track 1) live in the arithmetic layer (done); the machine composition is
the wall. `regenLaw_7` shows the composition succeeds at ONE level; nothing yet runs it `∀k`.

## HAVE — arithmetic / structure layer (GREEN, `∀k`)

| object | what it gives |
|---|---|
| `exitList`, `exitList_selfsimilar`, `exitList_grounds`, `exitList_wf_grounds` | the odometer call-list `∀k` (`exitList 7=[4,5,4]`, `8=[4,5,6,4,5,4]`), self-similar recursion |
| `exitArity`, `exitList_length_eq_arity` | arity `(k−5)(k−4)/2` `∀k`, tied to the list length |
| `foldRegenSteps`, `foldRegenSteps_grounds` | the interior step-count fold over `exitList` `∀k` |
| `exitSteps`, `termSteps` | REGEN(k) / TERM(k) closed-form step counts `∀k` |
| `leadRec`, `leadRec_closed`, `leadSteps`, `trailSteps`, `trailSteps_closed` (§5al, Track 1) | lead/trailing closed forms `∀k` (`lead=3·2^{k−1}−9k+112`, `trail=2^{k+1}+k+364`) |
| `descCascade`, `cascadeReg_block`, `cascadeReg_collapse` | the descending-cascade tape family + its block/collapse arithmetic `∀k` |
| `CascadeRegReached`, `cascadeRegReached_{4,5,6}`, `carry_descends_of_reach`, `cascadeRegReached_of_regenLaw` | the reachability predicate; the reduction `RegenLaw k → CascadeRegReached k` `∀k` |
| `RegenLaw`, `regenIn`, `regenLaw_{4,5,6,7}` | the target invariant + 4 grounded levels (k=7 first recursive) |

## HAVE — per-unit MACHINE transports (GREEN, `∀`)

| weapon | signature (schematic) | role |
|---|---|---|
| `sweepEF (m)` | `steps (2m) [E]·pow10 m·R = [E]·ones(2m)·` | the ×2 comb→block repack |
| `dSweepTurn (n)` | `steps (n+2) [D]·ones n·(0::L) → [E]` turn | cross one block, turn at boundary |
| `chewFold (m)` | `steps (6m) [D]·1^{2m+3} → pow10 m` | chew one block into a comb |
| `braid_topgrind (N,Lc)` | ascending: `1^{2N+1} → 1^{4N+4}`, +5+2N pos | the ASCEND leg body |
| `descent_glue_expl (N,d,Lc)` | descending: `descCascade(d+1) → foldDep d` | the DESCEND leg body |
| `carry_descent_fold (m)` | `ones(2^{m+2}−3) → pow01(2^{m+1}−2)` | fold one carry-block |
| `regenAscend (a)` [ant. `RegenLaw a`] | `regenIn a → regenIn (a+1)` | interior ASCEND leg, `∀a` |
| `regenDescend (a)` [ant. `RegenLaw a`] | `regenIn a → regenIn 4` | interior DESCEND leg, `∀a` |
| `steps_pos_shift`, `steps_add`, `someBind` | pos-translation invariance; run-splitting | glue plumbing |

## GAP — the `∀k` MACHINE ASSEMBLY (all OPEN; this is the whole crux)

`REGEN(k) = LEAD(k) ∘ (interior fold over exitList k) ∘ TRAILING(k)`. All three machine `∀k` laws
are unbuilt; the per-level `rfl` runs at k=6,7 (`r{6,7}f_glue1/glue2`) are bespoke, not a `∀k` step.

- **(B) LEAD machine `∀k`** — `regenIn k → interior-start` in `leadSteps k`. Blockers (verified):
  (1) **no `leadOut k` config family exists** — the statement can't even be *written* `∀k`;
  (2) the per-level prefix `P_k` (`|P_k|=3·2^{k−1}−9`) is an **exponential-length left-block sweep**,
  `[OBSERVED]`-only, with **no applicable existing `∀`-lemma** (`carry_descent_fold` is right-tape,
  count `−12≠−9`); (3) the "reuse regen6" induction **does not exist** (regen7 reuses regen4/5/braid/
  descent, not regen6). → needs a NEW left-geometry sweep transport + the `leadOut k` family.
- **(C) TRAILING machine `∀k` / TERM(k)** — NOT "the easy half". Measured: TERM(k) is a **leftward
  `descCascade` collapse with per-block doubling**, block count grows with k, count `= 2^{k+1}+k+5`
  (the `+k` = one turnaround per block = odometer height). It is a **`descCascade` cascade-collapse
  induction** — a different shape than `descent_glue_expl` — i.e. a core slice of the crux itself.
- **(D) INTERIOR FOLD `∀k`** — chain `regenAscend`/`regenDescend` (both `∀a`, HAVE) along `exitList k`,
  threading the marker decoration (`00 1 (01)^{2^a−2} ++ m`) and pad between legs. The legs and the
  list/arith scaffolding exist; the **`∀k` induction that runs the fold** with bookkeeping is unbuilt.
  This is the most "assembly-ready" crux piece (its legs are done) but still needs B and C to frame it.

`A = B ∧ C ∧ D` ⟹ `RegenLaw ∀k` (via `carryExit_strong_frame`, the green induction skeleton).

## GAP — anchoring (independent of the crux)

- **(G-blocker) boundary-blank / pos normalization** — §5am `M1/M6` are canonical (pos 0, blank-trimmed);
  the real orbit reaches them at drifting negative pos WITH explicit boundary blanks, so
  `steps n init = some (M1 1)` is FALSE as stated (kernel-proved). `step` ignores pos and boundary
  blanks ride harmlessly (`mvR ⟨l,h,[]⟩ = mvR ⟨l,h,[false]⟩`), so a **blank-normalization congruence**
  reconciles them. *(Weapon under construction 2026-07-19.)* Unblocks `h_init` and milestone anchoring.

## Reading of the map

The frontier is NOT "missing lemmas" scattered across the file — it is **one kind of missing thing**:
a `∀k` induction that composes already-proven per-unit transports along the already-characterized
`exitList`/`descCascade` structure, with exact step-count arithmetic (already closed-form) and tape
bookkeeping. B, C, D are three faces of that single assembly. TERM(k) (C) is the hardest face
(genuine cascade-doubling); the interior fold (D) is the most tractable (legs done); the lead (B)
needs one new left-sweep transport + a config family. No step needs mathematics outside the
machine's own combinatorics — but the assembly is `Suffix.lean`-scale, exactly as the file records.
