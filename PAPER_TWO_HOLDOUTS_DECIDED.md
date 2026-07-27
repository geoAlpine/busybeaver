# Two BB(6) holdouts decided: unconditional machine-checked non-halting proofs in Lean 4

**Yosuke Aoki (GeoAlpine LLC)** — ORCID 0009-0002-3791-2372 — research artifact (2026-07-28)

> **Epistemic banner.** Two machines from the published BB(6) holdout list are proved **never to halt
> from the blank tape**, unconditionally, in Lean 4. The proofs are `sorry`-free, use no `native_decide`
> and no `decide`, import no Mathlib, and audit to `[propext, Quot.sound]`. Every other claim in this
> note carries its own label: **[PROVEN]** = kernel-checked in the accompanying Lean corpus;
> **[MEASURED]** = exact simulation only; **[OPEN]** = stated, not proven. No label is upgraded on the
> strength of prose. **No claim is made about BB(6) itself**, which remains open (§6).

---

## 1. Summary

The BB(6) frontier is a published list of undecided 6-state 2-symbol Turing machines, maintained on the
bbchallenge wiki; the current release is `BB6_holdouts_1094.txt` (1094 machines up to isomorphism,
shared 2026-06-29 by @mxdys). This note reports that two of its entries never halt:

| label | machine (bbchallenge notation) |
|---|---|
| **`x2`** | `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` |
| **`C`** | `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` |

Both are proved non-halting from the blank tape, in Lean 4, unconditionally.

The two are related but are **distinct entries of the list**: `C` runs `x2`'s transition graph started
from a different state, and their canonical forms (TNF + left–right reversal) differ, so neither is a
re-labelling of the other as the list counts machines. This relationship is the reason the second proof
was cheap, and it is the methodological point of §4.

---

## 2. Novelty — verified against the current published list

`[PROVEN]` Both machines are still on the list, checked today.

```
list      BB6_holdouts_1094.txt          (bbchallenge wiki, shared 2026-06-29 by @mxdys)
source    https://wiki.bbchallenge.org/w/images/9/90/BB6_holdouts_1094.txt
index     https://wiki.bbchallenge.org/wiki/Holdouts_lists   (re-read 2026-07-28; 1094 is the latest)
sha256    976415e041065fbde32d9d773eabed39b52866852b65e4717247cead775dbdd4
parsed    1094 lines  →  1094 canonical classes   (no collisions within the list)

x2  canonical = 1LB0LC_1LD---_1LE0RD_0RF1RC_0LA1LC_0LC1RF     STILL OPEN: True
C   canonical = 1LB---_0RC1RD_0LD1RC_1LE0RB_0LF1LD_1LA0LD     STILL OPEN: True

two distinct canonical classes: True
```

Matching is up to the same equivalence the list itself uses: Tree Normal Form (states relabelled by
order of first appearance in a `0`-before-`1` BFS from `A`, halt actions normalised to `---`) together
with left–right reversal, i.e. `canonical(M) = min(TNF(M), TNF(reverse(M)))`. Instrument:
`bb6_holdouts.py`.

**Standing caveat.** The wiki's list index was re-read on 2026-07-28 and `1094` is the most recent
published list; the previous ones are `1104` (2026-04-29), `1119`, `1161`, …. New lists have appeared
roughly monthly, so any external use of this note should re-run the check against the newest list
immediately before release, and should say "open as of the 2026-06-29 list" rather than "open".

---

## 3. The theorems

`[PROVEN]` Verbatim from the corpus, with the axiom audit Lean prints for each.

```lean
-- lean/T7Entry.lean:42
theorem x2_nonhalt_blank : ∀ N : Nat, steps N init ≠ none
-- 'x2_nonhalt_blank' depends on axioms: [propext, Quot.sound]

-- lean/CIso.lean:71
theorem C_machine_nonhalt : ∀ N : Nat, stepsC N ⟨.A, 0, ⟨[], false, []⟩⟩ ≠ none
-- 'CIso.C_machine_nonhalt' depends on axioms: [propext, Quot.sound]
```

`steps` / `stepsC` are the step functions of the two machines as literally transcribed from the specs in
§1, over the self-contained tape zipper defined in `lean/X2.lean` (that file has **no imports**);
`init` is the blank-tape start configuration; `none` is the halting result. So each statement says exactly *"for every number of steps, the machine has not
halted."*

**Corpus-wide audit.** `lake build` over the whole development: **EXIT 0**, 2,026 theorem declarations,
**`sorryAx` 0**, **`Classical.choice` 0**, no `native_decide`, no `decide`, no Mathlib import.

---

## 4. Method

### 4.1 How non-halting is obtained

Both proofs are of the same shape: exhibit a milestone family `P`, show every `P`-configuration reaches
another one in `≥ 1` steps, and enter `P` from the blank tape. The assembly lemma is
`T7OddBridge.nonhalt_of_invariant`, and the transports that let a run proved on a finite tape context be
lifted to the real orbit are the padding lemmas alongside it.

*A note on the corpus layout, since it is easy to guess wrong.* These two proofs are **self-contained**:
`lean/X2.lean` imports nothing and defines its own `St` / `Tape` / `Cfg` / `step` / `steps`, and the
whole `T7` development sits on top of that. The generic, machine-parameterised layer
`lean/TapeCalc.lean` (41 theorems over `Cfg S`) came *later* and is **not** used by `x2` or `C`; it
carries the newer machines and the §7 by-product.

### 4.2 The `∀`-parametric discipline — why the second machine was nearly free

Every lemma was stated `∀` in the indices that vary within a species, from the start, rather than being
proved at concrete levels and generalised afterwards. The payoff is measurable: `C`'s proof required
**zero new dynamics**. Its low phases (`X2FromB.hlowB_core`, `hlowBodd_core`) are the `x2` lemmas applied
*verbatim* — the `B`-orbit's tails are instances of the same `∀ TAIL` statements — and only the entry
segment and the doubling-phase indexing had to be redone.

Costs, `[MEASURED]` on this corpus: the first machine of a species ≈ 20,000 lines of Lean; the second
≈ 1,000.

### 4.3 The two proofs

**`x2`.** The blank-tape entry is a 732,733-step run into the first milestone `M1(2)`, done as eight
kernel-`rfl` chunks (`T7Entry.k1 … k8`; one-shot overflows the kernel stack), composed into
`entryM12 : steps 732733 init = some e8`. Above the entry sits the milestone induction of the `T7`
modules (`RegenLaw ∀k`, `oddSpineFull`, `doubPhaseOdd`), which supplies the `P`-to-`P` step.

> *Archaeological note, because the corpus can mislead a reader.* `lean/X2.lean` still carries prose
> saying `x2` is `[OPEN]` with a `[DESIGN ONLY]` gap at `carry_step`. That file records an **abandoned
> first construction** (a direct cascade-doubler with a `Θ(2^{2K})` ripple, which did not close). The
> decision goes through the `T7` route above. The stale prose has been left in place as a record; it is
> not the proof.

**`C`.** `EntryB.C_nonhalt_blank` proves non-halting of `x2`'s graph started from state `B` (entry
2,866,581 steps), reusing `X2FromB` as in §4.2. `lean/CIso.lean` then transports that to `C`'s own state
labelling through an explicit relabelling bijection `sg`/`sgi` with `sgi_sg`, `sg_sgi`, and the transport
`stepsC_rl : stepsC n (rl c) = (steps n c).map rl`. The isomorphism is **axiom-free** in Lean; it is not
an appeal to "obviously isomorphic".

---

## 5. Reproduction

```
lean/          Lean 4 (v4.31.0), zero-Mathlib, `lake build`
               the two results are lean/T7Entry.lean and lean/CIso.lean
bb6_holdouts.py       novelty check (TNF + left-right reversal) against a holdout list
```

The holdout list is **not bundled** — it is a third party's data file. Download it from the URL in
§2 (sha256 given there) and point `bb6_holdouts.py` at it to re-run the check.

The axiom audit is not a separate step: each file ends with `#print axioms` on its headline theorems, so
a clean `lake build` prints the audit lines quoted in §3.

---

## 6. Scope — what is **not** claimed

This is the part most likely to be over-read, so it is stated flatly.

1. **BB(6) is not decided, and this note does not shorten the distance to deciding it.** A complete BB(6)
   proof requires *every* holdout; 1092 of the 1094 remain, and the ~17 named cryptids among them are
   `[OPEN]` behind a single-orbit equidistribution statement — the floor-mirror, single-orbit fragment of
   the Andrieu–Eliahou–Vivion normality conjecture (arXiv:2510.11723). Two decided machines change the
   count, not the obstruction.
2. **No halting claim** is made about any machine.
3. The proofs are of *non-halting from the blank tape*, which is what the holdout list asks.
4. The relationship between `x2` and `C` is a same-graph/different-start relationship, not a claim that
   the list double-counts: their canonical forms differ (§2), so the list is correct to hold both.

---

## 7. A by-product: an exact structural classifier, and a caution about census-by-simulation

`[PROVEN]` `lean/RungCalc.lean` factors the "comb doubler" mechanism out of any particular machine. It
defines a six-atom interface `Atoms T sA sB cr mk ta s10 s01 tu` — only two state names occur in the
interface, every other state of the machine hiding *inside* an atom — and proves from it, for **every**
machine satisfying it: the rung tile, the tile at a whole ladder of `n` rungs (`tileIter`), the two turn
phases, and a descent. The per-machine cost is **six closed kernel `rfl`s**.

That interface is also an *exact structural classifier*: it can be checked against a machine's transition
table directly, with no simulation. `[MEASURED]` Scanning the 1104-entry list, **18 machines satisfy it**
and are tiled in `lean/IslandTiles.lean`; all 18 run 3·10⁵ steps without halting and fire the tile on
100 % of the matching configurations on their real orbits. Two independent checks: the interface scores
**0 hits** across the ~17 named cryptids, consistent with their `(K)` classification; and it holds for
machines whose transition graphs are **not** relabellings of one another (an exhaustive state-permutation
search over the two orientations returns zero isomorphisms between two of the hits), so the interface is
an invariant strictly coarser than graph isomorphism.

**The caution.** `[MEASURED]` Of those 18 machines, **14 are `UNRESOLVED`** under the epoch-width-ratio
census this program had been using to characterise the residual (5·10⁶ steps per machine; that census
left 673/1104 unresolved and nonetheless concluded the residual was dominated by carry-opaque ratios).
An exact structural test finds machines that 5·10⁶ steps of simulation cannot classify. We therefore
**withdraw any inference about the residual's composition drawn from that census**, and record only that
its composition is unknown. This is not a claim that the residual is mechanisable — 18/1104 = 1.6 % is
what is demonstrated.

---

## 8. Honest position

The defensible contribution of the wider program is not a step toward BB(6) but a *characterisation of
why its Collatz core resists*: exact machine-verified reductions of the named cryptids to a single-orbit
equidistribution kernel, together with proven barriers showing that structure-only, all-orbits and
finite-certificate arguments cannot decide them. That work is reported elsewhere
(`PAPER_MAIN.md`, `BB6_FRAMEWORK_PACKAGE.md`). The present note reports the one thing in the program that
is unconditional and checkable end-to-end: two machines removed from the world's open list.

**No further machine is decided by this note. No label is upgraded.**
