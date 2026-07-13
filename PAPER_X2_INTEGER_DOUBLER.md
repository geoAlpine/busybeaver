# The Integer-Doubler Machine: a Machine-Checked Reduction of a BB(6)-Frontier Non-Halting Problem to a Single Recursive Lemma

**Yosuke Aoki (GeoAlpine LLC)** — ORCID 0009-0002-3791-2372 — research artifact (2026-07-13)

> **Epistemic banner.** The machine studied here is **NOT decided**. This document reports a
> *machine-checked reduction*: the machine's non-halting is reduced, in Lean 4 (zero `sorry`, zero
> `native_decide`, axiom audit `[propext, Quot.sound]`), to three explicit halt-free phase
> transports, of which the surrounding odometer structure is fully resolved and **one** genuinely
> recursive lemma (`carry_step`) remains open. Every claim carries a label: **[PROVEN]** = kernel-checked
> in `lean/X2.lean`; **[OBSERVED]** = measured on the exact-bigint orbit only; **[OPEN]/[DESIGN]** =
> stated, not proven. No label is upgraded on the strength of prose.

---

## 0. Summary

The 6-state Turing machine `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` (here the **integer-doubler**,
or **x2**) is a base-2 doubling odometer. Its non-halting is an open BB(6)-frontier problem, but —
unlike the 14 named "(K)-wall" cryptids whose halting encodes a normality/Collatz-type return problem
— its carry sequence is set by an explicit register rather than by an irreducible arithmetic orbit.
This makes it the frontier's best-mapped candidate for a machine whose halting is decidable *in
principle* (the **carry-transparent island**, §1).

We build the entire non-halting proof architecture in Lean 4 and reduce the machine to a single
recursive lemma:

- **[PROVEN]** A conditional top-level theorem `x2_nonhalt`: the machine never halts from the blank
  tape *given* three halt-free phase transports (initial, low phase `∀g`, doubling phase `∀g`) (§2).
- **[PROVEN]** The doubling phase is a **clean binary odometer**: an exact closed-form tick count
  `Tfaithful`, a power-of-2 comb-at-carry ladder, and a terminating well-founded recursion — the
  measure is clean on the pure register (§3). This **refutes** the possibility that the tick count is
  irreducibly tape-determined.
- **[PROVEN, ∀-parametric, on-path]** A library of the phase's building blocks: the odometer tick, the
  steady no-carry run, the carry's `sweepEF`-core, the fully-factored depth-1 carry, and the low
  phase's forward tile (§4).
- **[OPEN]** The one remaining deep wall is `carry_step`: the general-`j` carry is a well-founded
  **ripple recursion** (its block-regeneration EXIT re-runs a lower-scale doubling cascade; its ENTRY
  nests strictly-lower carries), not a bounded composite (§5).

The honest bottom line: **the machine is not decided**, but its non-halting is now a single, precisely
characterized, `Suffix.lean`-scale recursive lemma away from a machine-checked proof, with everything
around that lemma resolved and green.

---

## 1. The machine and the carry-transparent island

The blank-tape orbit passes through milestones `M1(1) → M1(2) → M1(3) → …`, each cycle
`M1(g) → M1(g+1)` splitting into a **low phase** `M1(g) → M6(g)` (register setup) and a **doubling
phase** `M6(g) → M1(g+1)` (the base-2 doubling). The machine halts iff state `B` ever reads a `1`
(`halt_gate`, [PROVEN]); non-halting is the assertion that this never happens.

**Why this machine, and not the (K)-wall cryptids.** The BB(6) frontier's hardest machines (Antihydra
and its ×3/2, ×4/3, ×5/2 relatives) have a *carry-opaque* dynamics: the carry itinerary is the residue
sequence of an affine `×(p/q)` orbit, whose statistics are the subject of the Andrieu–Eliahou–Vivion
Normality Conjecture (arXiv:2510.11723). No known tool crosses that wall. The integer-doubler is
`×2` with integer multiplier `q = 1` — a clean binary shift with **no bit-mixing**, so its carry
sequence is *carry-transparent*: driven by an explicit register (the cascade of stored blocks), not by
an opaque orbit residue. This transparent/opaque dichotomy draws the exact boundary of the (K) wall;
the doubler sits on the decidable-in-principle side of it. [OBSERVED — the classification; the
decision itself remains open.]

---

## 2. The non-halting architecture (a clean conditional theorem)

`lean/X2.lean` §5r builds the honest logical frame, isolating the open content as *hypotheses* (the
`Completion.lean` pattern — no `sorry`, no new axiom):

- **[PROVEN, pure]** `nonhalt_of_segments`: an infinite chain of nonempty halt-free segments from the
  blank tape ⟹ `∀N, steps N init ≠ none` (the machine never halts). A clean induction — a prefix of a
  halt-free run is halt-free, and the segments' cumulative reach exceeds any `N`.
- **[PROVEN, conditional]** `x2_nonhalt (M1 M6 : Nat → Cfg) (h_init) (h_low) (h_doub) : ∀N, steps N init ≠ none`.
  Given milestone families with the three halt-free transports (`blank → M1 1`; `∀g, M1 g → M6 g`;
  `∀g, M6 g → M1(g+1)`), the machine never halts. The per-generation cycle composes `h_low ∘ h_doub`
  by `steps_add`; the tail threading is discharged by the shared `Cfg` families.

This **decides nothing on its own** — it reduces the machine's non-halting to proving `h_low` and
`h_doub` for actual milestone configurations. The rest of the work is exactly those two transports.

---

## 3. The doubling phase is a clean binary odometer

The doubling phase `M6(K) → M1(K+1)` (`K = g+8`) chews a cascade of stored blocks
`[2^K−3, 2^{K−1}−3, …, 5, 1]` and rebuilds it doubled. Instrumented cell-for-cell on the exact-bigint
orbit (forward from a milestone construction *verified faithful*: an independent blank-tape simulation
reaches it), the phase is a **binary counter with ripple carry** on the cascade:

- **[OBSERVED, exact]** The **comb-at-carry ladder**: a carry at comb-count `2^m−1` fires exactly
  `2^{K−1−m}` times — the clean power-of-2 profile `128, 64, 32, 16, 8, 4, 2, 1` at `K=10`, verified
  across all 8 levels. This is a structural per-level law, not a numerical coincidence.
- **[OBSERVED, exact at K=10,11,12,13]** The **closed-form tick count**
  `Tfaithful K = (2K−5)·2^{K−2} + (K even: K+2 ; K odd: 2^{K−1} + (K−10))`,
  matching the real round-trip counts `3852 / 9729 / 19470 / 47107`; and the carry count
  `Cfaithful K = 3·2^{K−4} (+2 if K odd)` matching `192 / 386`. Encoded and `#eval`-cross-checked
  in `lean/X2.lean` §5o.
- **[PROVEN]** The pure register carries a **clean well-founded measure**: `odoValue` increments by
  exactly `+1` per tick (a ripple-incrementer correctness proof, `binInc_val`), so termination
  (`odo_terminates`) is a textbook `Nat` well-founded recursion, with ripple depth `≤ K`
  (`rippleDepth_le`). Crucially the measure lives on the *register*, not the tape: on 523 830 real
  ticks **every** physical tape scalar is non-monotone — the clean measure exists only on the
  abstracted counter (`X2_WELLFOUNDED_DESIGN`, §5n).

The upshot: the doubling phase's control structure is **fully resolved and clean**. An earlier
hypothesis that the tick count is "irreducibly tape-determined" was **refuted** by the ladder and
closed form (recorded in the correction trail, §6).

---

## 4. The proven on-path building blocks

All of the following are **[PROVEN]** in `lean/X2.lean`, `∀`-parametric, halt-free (`some ⇒`
halt-free), axiom audit `[propext, Quot.sound]`, and cross-checked against the real orbit (their
concrete instances occur cell-for-cell on the exact-bigint trajectory):

| lemma | statement | §
|---|---|---|
| `sweepEF` | the `×2` repack `(01)^m → 1^{2m}`, `∀m` | 5 |
| `ecombChewFold` | inner block-chew `1^{2v+1} → 1^1` depositing `(01)^v`, `∀v` | 5e |
| `outer_tick_noCarry` / `outer_tick_grounds` | one odometer no-carry tick, `∀t`, in register form | 5l |
| `outer_tick_noCarry_run` | the steady no-carry **run**, `∀n` ticks (`4nt+4n²+6n` steps) | 5p |
| `carry_repack` | the carry's **core** = `sweepEF(2^{j+2}−2)`, `∀j` | 5m |
| `carry_event_5to13_ECE` | the depth-1 carry factored **ENTRY ∘ CORE ∘ EXIT** (= the extracted on-path carry) | 5s |
| `lowMiddle_fwd` | the low phase's **forward tile run**, `∀` U-units | 5t |
| `nonhalt_of_segments`, `x2_nonhalt` | the logical non-halt frame + conditional theorem | 5r |

The depth-1 carry factorization (§5s) is the analogue, one level up, of the tick factorization:
`carry = entry ∘ sweepEF-core ∘ exit`, grounded inside the real carry rather than as an isolated
window.

---

## 5. The one remaining wall: `carry_step` (a well-founded ripple recursion)

Two braid structures were probed as the phase's potential walls. One largely fell; one is the genuine
remaining obstruction.

- **Low phase — forward pass is CLEAN [PROVEN].** The growing middle of `M1(g) → M6(g)` was suspected
  to be a growing accumulator. Re-instrumented, its forward pass is a **fixed 29-step tile** translated
  `+7` per register U-unit with constant length and reach (`lowMiddle_fwd`, `∀` units); the apparent
  growth was only the odd-`g` big-block trim. The low-phase wall is therefore small: only a fixed entry
  connector, a uniform return pass, and the odd-`g` trim remain [DESIGN].

- **Doubling phase — the carry ripple is the deep wall [OPEN].** The general-`j` carry is **not** a
  bounded `connector ∘ sweepEF ∘ connector`. Measured cell-for-cell: its **EXIT** regenerates the
  fresh block `1^{2^j−3}` by *re-running a `(j−1)`-scale doubling cascade* (`j=3` EXIT: one `sweepEF`;
  `j=4` EXIT: a nested `m=2,4,6` chain; `70 → 218` steps), and its **ENTRY** nests strictly-lower
  carries (the `j=4` carry window literally contains the whole `j=3` carry). So
  `carry_step(j) = ENTRY[run ⋈ carry(j−1)…] ∘ carry_repack(j) ∘ EXIT[carry_repack(j−1) ∘ EXIT(j−1)…]`
  is a **well-founded ripple recursion** (measure = cascade digits left, `≤ K`; termination is
  `odo_terminates`, already proven), a `Θ(4^j)`-length object — the project's `Suffix.lean`-scale
  lemma. Its `sweepEF`-core and its depth-1 base case are proven (§4); the recursion around them is
  open.

**`carry_step` is the single lemma whose closure would complete `h_doub`** — and, with the (smaller)
low-phase pieces, reduce the whole machine's non-halting to a finished machine-checked proof.

---

## 6. Epistemic status and the correction trail

**The machine is not decided.** `x2_nonhalt` is conditional on the three transports; `h_doub` hinges on
the open `carry_step`; `h_low` needs the (small) remaining low-phase pieces; and the proven
`∀`-parametric transports are tail-parametric primitives that still need assembling into the total
milestone `Cfg` families the hypotheses quantify over.

This artifact was produced under a strict zero-false-proof discipline; the audit trail is part of the
record and includes corrections the discipline caught, e.g.:

- **Off-path lemmas.** Several green `sorry`-free lemmas were *true but off the real trajectory* (the
  machine visits none of their configs); they were set aside once an exhaustive real-orbit scan caught
  them. A green step-lemma is not a proof about the machine.
- **The "tape-determined" over-claim, overturned.** A subagent concluded the doubling tick count was
  irreducibly tape-determined (from a flat-counter mismatch); independent analysis found the exact
  power-of-2 ladder and closed form, refuting it. The flat counter was the wrong model, not a wall.
- **Inflated numbers, corrected.** Declaration/axiom counts were re-derived by byte-level Lean audit
  whenever quoted.

`lean/X2.lean` contains **144 declarations** (107 theorems/lemmas, 37 definitions), **zero `sorry`,
zero `native_decide`**, axiom audit `[propext, Quot.sound]`.

---

## 7. Contents and verification

- `lean/X2.lean` — the full formalization (machine `step`/`steps`, `halt_gate`, the phase primitives of
  §4, the odometer of §3, the conditional non-halt theorem of §2). Build: `cd lean && lake build`
  (Lean 4.31.0 via `elan`, zero mathlib; green, `[propext, Quot.sound]`).
- The `#print axioms` block at the file's end kernel-audits every headline theorem; the `#eval` block
  kernel-executes the sanity and closed-form cross-checks at every build.
- The probes that extracted every config cell-for-cell from the exact-bigint orbit
  (`x2*.py`) are lab notes to the record, not part of the trusted kernel.

**Related work.** The (K) wall this machine sits outside of is the Andrieu–Eliahou–Vivion Normality
Conjecture (arXiv:2510.11723); the bbchallenge project's machine discoveries and prior analyses are
cited in the accompanying novelty audit.

No machine decided. No label upgraded.
