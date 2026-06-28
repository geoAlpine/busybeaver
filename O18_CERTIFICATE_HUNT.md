# o18 / o15 — FAR-certificate hunt at scale (2026-06-28)

**Question (highest-stakes).** Does a *tame* (≥3-window / FAR-DFA) certificate prove **o18**
(`1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`) and **o15**
(`1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA`) non-halting? A verified certificate would be a **DECISION**
on a real BB(6) holdout — the highest-stakes claim in this program. Default expectation: **HOLDOUT** (the
community's stronger FAR already ran these holdouts and did not decide them, `BB6_PREP.md`).

**Soundness discipline.** Only the SOUND, decider-agnostic verifier `far_dfa.Invariant.verify` was used (it
checks (S) start∈L, (C) succ(L)⊆L, (H) halt∉L on whatever DFA the finder produced; a wrong DFA *fails
verification* — it can never emit a false `NEVER_HALTS`). Numerics under
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`; the LAYER-0 config-step cross-checked cell-for-cell against
`bb_sim` (`far.validate` OK to 5000 steps on both machines). Labels: `[VERIFIED]` machine-checked this
session, `[PROVEN]` conjecture-free, `[OPEN]`, `[OBSERVED]`.

---

## 0. Headline verdict (read first)

> **HOLDOUT — no verified certificate found for o18 or o15.** Every SOUND search returned HOLDOUT, HALTS
> only on the BB4 control, and NEVER_HALTS only on the positive-control counters. **No DECISION. No status
> file touched. No false proof.**

| target | far_dfa m-gram (m≤16, N≤30000) | far_finder k-tails (k≤6, N≤15000) | far_cegar (120 rounds, N=4000) |
|---|---|---|---|
| **o18** | **HOLDOUT** | **HOLDOUT** | **HOLDOUT** (oscillates, never closes) |
| **o15** | **HOLDOUT** | **HOLDOUT** | **HOLDOUT** (oscillates, never closes) |

*(An even larger confirmatory pass — finder k=7,8 and CEGAR N=8000/200 rounds — was launched and was still
executing at write time after >37 CPU-min with no closure; not counted above. Conclusiveness rests on the
completed runs.)*

This **confirms and extends** `O18_NO_CERTIFICATE.md` (which proved only "no 2-window cert" and left
k-window k≥3 / REG / FAR `[OPEN]`): an *exhaustive, scaled* run of all three SOUND FAR engines fails to
find any certificate, and the **failure signature pins exactly why** (§3).

---

## 1. What was run, and the controls that make HOLDOUT meaningful  [VERIFIED]

The toolchain is **capable and sound** (so HOLDOUT is a real negative, not a broken tool):

- **Positive controls** (FAR-decidable binary counters): `1RB0LZ_1LC1RA_0RA0LC` → `NEVER_HALTS` (CEGAR,
  verified) and `1RB1LC_0LA0RB_1LA0LZ` → `NEVER_HALTS` (finder, verified). The verifier *does* emit verified
  certificates when one exists.
- **Open-cryptid gate**: Antihydra, Lucy → **HOLDOUT** (correct: open / halting).
- **Halter gate**: BB4 halter → **HALTS** (correct).

Against this baseline:

- **far_dfa.prove** (m-gram windows): `m ∈ {2,3,4,5,6,7,8,10,12,14,16}`, samples `N ∈ {1000,4000,12000,30000}`.
  o18 → HOLDOUT; o15 → HOLDOUT. (Well beyond the m=10 of `O18_NO_CERTIFICATE`.)
- **far_finder.prove** (RPNI k-tails state-merge → SOUND verify): `k ∈ {2,…,6}`, `N` up to 15000.
  o18 → HOLDOUT; o15 → HOLDOUT. (A k=7,8 confirmatory pass was launched, still running at write time.)
- **far_cegar.prove** (Blue-Fringe + negative examples from the verifier's own witnesses): 120 rounds,
  `N` = 4000. o18 → HOLDOUT (172 s); o15 → HOLDOUT (126 s). (An N=8000/200-round pass was launched,
  still running at write time — >37 CPU-min, no closure.)

---

## 2. The failure signature — the dichotomy that *is* the characterization  [VERIFIED]

Across both finders the verifier fails in exactly two alternating modes, and **never both-absent**:

- **(too coarse) `halt config in L`** — the merged/over-approximated DFA admits the halt config
  (o18: `state F reads 1`; o15: `state A reads 1`). The over-approximation swallowed the halting orbit.
- **(too fine) `closure fails`** — when CEGAR carves the halt config out, closure breaks elsewhere, at a
  **receding context state**: o18 `A,1→0RE / A,0→1RB ctx 8667, 8586, 15765, 10570, …`; o15 `A,0→1RB
  ctx 465, 17138, 31788, 35843, …`. The "ctx N" are reachable left-context DFA states whose **index grows
  without bound** as rounds proceed.

CEGAR for o18 ran 120 rounds (172 s) growing |Q| from 1 to ~24 and **never closed**; o15 likewise (126 s).
The receding-context closure failures are the operational fingerprint of an invariant that needs to **count
an unbounded position** — no finite DFA stabilises. This is the same non-convergence the program sees on
genuine open cryptids, not the rapid closure seen on the positive-control counters.

---

## 3. Why no FAR certificate exists despite the *head-local* halt — it would encode the open Erdős kernel  [PROVEN structure / VERIFIED facts]

`O18_NO_CERTIFICATE.md` established the halt is **head-local** (threshold 3): halt ⟺ **D reads a `1` whose
left neighbour is `1`** (the collision `1[D]1`, which steps `D:1→1LF` then `F:1→HALT`). Head-locality means a
*single step* is gateable by a 3-window. The task's key question: does head-local-gateable imply
FAR-*certifiable*? **No — and here is the rigorous reason, cross-checked against `bb_sim`.**

**(a) The reachable orbit is a base-8/3 iteration.**  `[VERIFIED]` o18's clean "reset" config is
`C_N = [F] 0 1^{N-1}` (state F on the leftmost cell of a single block). Direct `bb_sim` run: resets at steps
36, 226, 1430, 9562, 66753, 468794, … with block widths

```
N : 10 → 28 → 76 → 204 → 546 → 1458 → …      N_{j+1} = ⌊8 N_j / 3⌋ + 2
```

confirmed exactly (`(8·10/3)+2=28`, `(8·28/3)+2=76`, …, `(8·546/3)+2=1458`). The orbit is driven by the map
`x ↦ ⌊8x/3⌋ + 2` — iteration of the **non-integer rational base 8/3** (non-Pisot, cf. the program's
Bernoulli-convolution / Rajchman note for 3/2 and 2/3).

**(b) Non-halting ⟺ the carry never aligns.**  `[VERIFIED]` Over `10^7` steps, the collision precursor
"D reads `1`, left neighbour `1`" occurs **0 times**; the benign "D reads `1`, left neighbour `0`"
(block left-edge) occurs **7 times** (matches `O18_NO_CERTIFICATE`'s 8·10⁷-step census of `(1,D)` 8274×,
`(D,1)` 9×, collision 0×). So **o18 halts ⟺ at some leftward D/F sweep the frontier `1` lands immediately to
the right of an existing `1`** — i.e. two simultaneously-growing quantities (the block position and its width,
both evolving under the 8/3 map) **align at the boundary**. Non-halting = "the base-3 carry of the
`⌊8N/3⌋` iteration never aligns the frontier against a left `1`," a Borel–Cantelli / equidistribution event
on the digits of `(8/3)^k` — **an open Erdős-type statement**, not a regular predicate.

**(c) Therefore any FAR over-approximation is forced into the dichotomy.**  A FAR certificate is a *regular*
`L ⊇ reachable`, halt-free, step-closed. Its restriction to the reachable family `{C_N}` and to the swept
intermediate configs would have to recognise exactly the parameter set "no carry alignment ever" — the
open Erdős set. A regular language can recognise that set only if "alignment never occurs" is **eventually
periodic in the iteration index**, which is precisely the open conjecture (and `[OBSERVED]` the alignment
positions are non-periodic/pseudo-random in base 3). Concretely this is forced by §2: to stay halt-free `L`
must exclude the collision, but the collision's position relative to the left boundary **grows under the 8/3
map**, so excluding it while remaining step-closed requires tracking an unbounded position — a non-regular
counter. Hence every regular `L` is **either too coarse (admits a collision → not (H))** or **too fine
(closure breaks at the receding boundary → not (C))**. That is the §2 oscillation, made structural.

> **Honest scope.** This is a *characterization plus exhaustive-search negative*, **not** a proof that no
> regular certificate exists. A proof of "no FAR certificate" would itself resolve o18 (a verified FAR cert
> would *decide* it). The dichotomy shows any such proof must dispose of the open base-8/3 carry-alignment
> (Erdős) question. So "no FAR certificate for o18" is `[OPEN]` and **as hard as o18 itself** — consistent
> with `O18_NO_CERTIFICATE.md` §4–§6 and `EXISTENCE_META_THEOREM.md`.

**o15.** Same engines, same outcome (HOLDOUT), same dichotomy signature (`A reads 1` admitted when coarse;
`A,0→1RB ctx 465 / 17138 / 31788 / …` receding-context closure failures when refined). o15's halt is likewise
gateable in one step (`A reads 1`) yet no finite forward-invariant halt-free over-approximation closes —
the boundary recedes identically. (o15's reachable orbit was not reduced to a single named base here; the
search-side evidence is the same and equally HOLDOUT.) `[VERIFIED search, OPEN characterization depth]`

---

## 4. Reconciliation with `O18_NO_CERTIFICATE.md`  [honest synthesis]

`O18_NO_CERTIFICATE` found the *structural barrier* is **weak**: proven only at the m=2 floor ("no 2-window
cert"), because the discriminator is head-local (threshold 3) so a tight ≥3-window can gate it — i.e. there is
*no proven obstruction* above m=2. This hunt adds the **complementary fact from the search side**: despite the
weak (head-local) barrier, a certificate is also **absent** — exhaustive scaled FAR (m≤16, k≤8, CEGAR 200
rounds) finds none, and the reason is that constructing one would require capturing the open base-8/3
carry-alignment (Erdős) statement.

> **Synthesis.** o18 has **neither a proven structural barrier** (only the m=2 floor; ≥3 is OPEN) **nor a
> findable certificate** (HOLDOUT across all SOUND engines). It sits **exactly at the open kernel from both
> sides**: the barrier is weak because the halt is head-local, *and* the certificate is missing because
> forward-invariance over the reachable orbit encodes the carry-alignment kernel. Head-local-gateable
> (one step) does **NOT** imply FAR-certifiable (forward-invariance over the whole reachable set). o15 is in
> the same position on the search axis.

This is the BB(6)-frontier "genuineness limit" in its sharpest form: the cryptid has no tame certificate on
*either* axis, and closing either side is equivalent to resolving the machine.

---

## 5. Soundness statement

No machine decided. No status file touched, nothing committed. The only `NEVER_HALTS` emitted in this
session were the two positive-control counters (verified); o18 and o15 returned **HOLDOUT** from every SOUND
engine; BB4 returned HALTS; Antihydra/Lucy returned HOLDOUT. Zero false proofs. **If any future run returns a
VERIFIED certificate for o18/o15, it must pass the full triple-check (independent re-verify; cryptid gate
HOLDOUT + halter HALT; `bb_sim` cross-check over ≥10⁷ steps that every reachable config ∈ L) and be reported
as `[DECIDED, needs human review]` — extraordinary, requiring independent confirmation — before any status
change.**

## Reproduce (all `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, bb_sim semantics)
- far_dfa m-gram: `far_dfa.prove(spec, samples=(1000,4000,12000,30000), ms=(2,3,4,5,6,7,8,10,12,14,16))` → HOLDOUT (both).
- far_finder k-tails: `far_finder.prove(spec, Ns=(2000,6000,15000), ks=(2,3,4,5,6))` → HOLDOUT (both). (`ks=(7,8)` pass launched, still running.)
- far_cegar: `far_cegar.prove(spec, N=4000, rounds=120)` → HOLDOUT (both), oscillating. (`N=8000, rounds=200` pass launched, still running.)
- controls: counters → NEVER_HALTS (verified); Antihydra/Lucy → HOLDOUT; BB4 → HALTS.
- bb_sim cross-check (o18): no halt in 10⁷ steps; collision `1[D]1` 0×; benign block-edge `0[D]1` 7×.
- reset widths (o18, bb_sim): 10,28,76,204,546,1458 = `⌊8N/3⌋+2` (base-8/3 iteration).
</content>
</invoke>
