# The integer-×2 frontier machine — consolidated map (2026-07-11)

*Honest consolidation of the whole ×2 investigation (2026-07-10/11): the machine, the two independent
cross-validated reductions, what is PROVEN vs the open core, and its honest place on the BB(6) frontier. No optimism.
No machine decided. This maps a machine reduced two ways to a single sharp invariant — a real contribution — while
being exact that it is NOT decided and the residual is o4-wall-class.*

## 0. What this machine is

`1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` — an integer-**×2** base-2 doubling odometer, found in the 1104-holdout
census (`CANDIDATE_NEW_INVESTIGATION`) as the first multiplier beyond {3/2, 4/3, 8/3, 5/2} to survive scrutiny. It was
pursued because **q=1 (integer multiplier)** puts it OUTSIDE the (K)/Mahler ×(p/q)-normality wall, and ×2 in binary is
a clean SHIFT that does not mix bits (the structural opposite of o7/Space-Needle's ×3/2 Collatz-coupling). It is the
frontier's cleanest decidability CANDIDATE.

## 1. What is PROVEN `[PROVEN, main-loop re-verified]`

- **Clean doubling / closed form.** Super-blocks `b = 2^k − 3` (`b′=2b+3`); leading maxrun `v = 2^k − 2 = 111…10₂`
  (`v′=2v+2`). A pure binary shift, no bit-mixing. Verified exactly to `2¹²−2 = 4094`.
- **Milestone form** (both routes agree): `M(k)` = the nested cascade `[low-part] 1^(2^k−2) 0^3 1^(2^(k−2)−5) 0^2 … 0^2
  1^5 0^2 1`; the right-cascade recurrence `b_i = 2^(i+2)−3` matched to captured peaks k=5..11.
- **Halt gate** (sharpened, both routes): `HALT ⟺ the rightward E-scanner meets a maximal 0-run of length EXACTLY 3`
  (`1 000 1`). Gaps 1,2 continue; 4 turns via C; 5,6,7,8 turn via D — all safe. Only length-3 halts.
- **Finite-state control:** the block-crossing routing is a function of block-length PARITY alone (uniform in the
  length) — a bounded-information controller. The doubling sweeps (comb-repack `(01)^m→1^{2m}`, D-sweep, turnarounds)
  are arbitrary-length uniform-crossing lemmas by 2-transition induction.
- **The eraser opens EVEN gaps:** `(01)^j → 0^{2j}` (`[OBSERVED j=1..40 + provable by 2-transition induction; Lean
  formalization in progress]`). Comb separators give length 1.

## 2. The two independent reductions — cross-validated `[both routes agree]`

- **Route A (tape trace-template, `X2_TEMPLATE_PROOF`):** milestone + transport + covering; reduces non-halt to "the
  E-scanner never meets a length-3 gap."
- **Route B (exact arithmetic, `X2_ARITHMETIC_PROOF`):** milestone value + halt-gate arithmetic; reduces non-halt to
  the identical statement, and adds the reason — the halt is a **head-PHASE** event, not a value bit-pattern: `v_k =
  2^k−2` contains no `000`, yet gap-3 (`0001`) is dense on the tape (~2.4% of steps), forming transiently as the
  eraser zeros a block through `0^1,0^2,0^3,…,0^{2j}`. Halt is avoided because E scans a gap only AFTER the eraser
  finished it at even `2j`, never mid-erasure at odd 3.

**The bet refuted:** the "clean-shift bit test" (halt = a predictable bit-pattern of `v_n`) is FALSE — the clean shift
makes the VALUE predictable but not the gap-meeting PHASE.

## 3. The open core `[OPEN, 0 counterexamples to 3·10⁸]`

**The global head-phase invariant:** *the E-scanner never scans a half-erased (odd-length) gap* — equivalently *every
E-met gap is length 1 or eraser-even (2j)*, never the transient odd 3.

- **Route A proved** the even-gap LENGTHS are **counter-dependent** (the same block-pair `1^5 0^L 1^13` gives
  `L ∈ {4,6,8,10,14,18,22}` across generations; the even-gap multiset differs every generation), and that the invariant
  **resists every uniform / local / parity argument tried** (no conserved mod-2 invariant among 7 candidates; no
  bounded-radius local certificate at R≤8 — the `o4_closure_fixpoint` phenomenon, HALT-in-closure).
- **This is structurally the o4 wall reproduced with a base-2 odometer** in place of base-4/3. The clean ×2 doubling
  removed the (K)/Mahler ledger obstruction — but a DIFFERENT obstruction (this counter-dependent head-phase
  invariant) took its place.

## 4. The sharpest remaining shot `[under test 2026-07-11]`

Separate **parity from length**: the LENGTHS are counter-dependent (hard), but every entry is EVEN in every generation.
If the ORDERING lemma — *the eraser always completes a block (to even 2j) before the E-scanner traverses it* — is
provable from the finite-state control, then non-halt follows from PARITY ALONE, sidestepping the counter-dependent
lengths. Honest prior: the ordering may itself be counter-dependent (⟹ genuinely o4-wall-hard). Under test.

## 5. Honest place on the frontier

The ×2 machine is **NOT decided**. It is the frontier's best-mapped decidability candidate: reduced two independent,
cross-validated ways to a single razor-sharp head-phase invariant, with the local channels (doubling, halt gate,
eraser-even, finite-state routing) proven, and the exact open core pinned. But "candidate" honestly means "reduced to
one hard counter-dependent invariant," NOT "about to fall." The residual is o4-wall-class. **A caution recorded in the
log:** the pursuit twice ran ahead of the evidence ("outside the (K) wall ⟹ decidable"; "the template proves non-halt
outright") — both refuted by the careful work; the honest status is a precise reduction, not a decision.

## Sources
`CANDIDATE_NEW_INVESTIGATION_2026-07-10` (discovery), `X2_DECIDABILITY_2026-07-10` (structure), `X2_CLOSURE_2026-07-10`
(local-closure impossibility), `X2_TEMPLATE_PROOF_2026-07-11` (route A), `X2_ARITHMETIC_PROOF_2026-07-11` (route B),
`X2_PARITY_ORDERING_2026-07-11` (the shot, in progress), `lean/X2.lean` (eraser formalization, in progress). No machine
decided. No label upgraded.
