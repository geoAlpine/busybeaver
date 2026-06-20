# Counter decider — STEP 2 build plan (the nested-induction PROOF engine)

**Build this with a CLEAR HEAD. Gate every NEVER_HALTS against the oracle. Do NOT reconstruct
the induction from memory — implement against the spec below (the night's cardinal lesson:
lin_decider emitted false proofs twice from memory; translated_cyclers + bouncer_prove succeeded
by porting a spec and gating on the oracle).**

Spec source: **sligocki, "BB Counters and Proof by Induction" (2022-06-14)**
<https://www.sligocki.com/2022/06/14/counter-induction.html> — fetched 2026-06-20, transcribed below.
Background: bbchallenge deciders repo; CTL is the alternative framework (a fallback, see end).

## What we already have (STEP 1 + 1.5 — all SOUND, no halting claim)
- `holdouts3_reps.txt` — the test set. After `bouncer_prove3.py` (v3) the residual is **exactly 10
  counters** (the 53 bouncers are proven).
- `counter_structure.py` — for each of the 10: regular growing family `LEFT·sym^k·RIGHT`, op-segment
  DOUBLING (binary-counter signature), zero halt-ops to ~2^17–2^34 micro-steps. And the decoded
  recursive op-grammar for the canonical machine (see below).
- The **oracle**: the trusted simulator (`bouncer_prove2.sim`). Any NEVER_HALTS on a machine that
  HALTS = STOP, the engine is unsound.

## The canonical target (fully decoded — build/test against THIS first)
`1RB1LA_0LA0RB_0LA0LZ`. Carry-out config family (0^∞ both sides):
  `C(n) =  A> 0 1^n 0`   →   `C(n+1) = A> 0 1^(n+1) 0`
Decoded op-grammar between carry-outs (this IS the nested recursion the induction must certify):
  `S(k) = [k] ++ MID(k) ++ [k+1]`,  `MID(k) = MID(k-1) ++ [pivot] ++ MID(k-1)`,  `MID(1)=[]`
  (verified: MID(3)++[3,3]++MID(3) = MID(4)). op-segment length doubles: 12,24,48,96,...

## sligocki's method (transcribed spec — implement THIS)

### Configuration notation
`left_tape STATE> right_tape` (head faces right, reads right[0]) or `left_tape <STATE right_tape`
(faces left, reads left[-1]). Blocks carry exponents: `0^∞ 1^n 00 B> 0^∞`. `0^∞` = blanks.

### A rule is `P(n): LHS(n) -> RHS(n) in f(n) steps`
Example proven in the post (TM #11,004,366 `1RB1LA_0LC0RB_0LD0LB_1RE---_1LE1LA`):
  `P(n):  0^n 1 00 B> 0  ->  1^(n+1) 00 B> 0   in  f(n) = 20·2^n − 2n − 20 steps`

### Proof = induction on n, with TWO step kinds
- **Base Step**: one concrete TM transition (peel the symbol under the head, apply δ).
- **Chain Step**: invoke an ALREADY-justified rule — crucially the induction hypothesis `P(k)`
  applied to a STRICTLY SMALLER argument. This is the well-founded recursion.

Base case (n=0): `00 1 00 B> 0 -> 11 00 B> 0` in 0 steps (LHS already equals RHS form).

Inductive step — the verbatim derivation table (LHS uses P(k) twice ⇒ f(n+1)=2f(n)+…):

| step          | left tape        | state | right | via        |
|---------------|------------------|-------|-------|------------|
| 0             | `0 0^k 1 00`     | `B>`  | `0`   | —          |
| f(k)+0        | `0 1^(k+1) 00`   | `B>`  | `0`   | **P(k)**   |
| f(k)+1        | `0 1^(k+1) 00`   | `<C`  | `0`   | Base Step  |
| f(k)+2        | `0 1^(k+1) 0`    | `<D`  | `00`  | Base Step  |
| f(k)+18       | `1 0^k 1 00`     | `B>`  | `0`   | Chain Step |
| 2f(k)+2k+18   | `1 1^(k+1) 00`   | `B>`  | `0`   | **P(k)**   |

Reaches `1^(k+2) 00 B> 0` = RHS(k+1). Recurrence `f(0)=0, f(n+1)=2f(n)+2n+18`; sub `g=f+2n` ⇒
`h(n+1)=2h(n)` ⇒ closed form `f(n)=20·2^n−2n−20`.

### Non-halting argument
`P(n)` holds for all n ⇒ from the start config the machine reaches `C(n)` for every n, writing an
unbounded number of 1s, never reaching a halt transition ⇒ NEVER_HALTS.

## Build pipeline (mirror the bouncer STEP-2 discipline)
1. **Symbolic config + simulator** (the foundation, soundness-light): blocks `(sym, count)` where
   count ∈ ℤ≥1 or linear `a·n+b`; state + direction. `base_step` = peel one symbol (handle symbolic
   peel: needs count≥1; `sym^n` faced head ⇒ this is where a rule/chain must apply, not a peel) and
   apply δ. Merge adjacent equal-sym blocks. **VALIDATE against the concrete sim at fixed n** before
   trusting it.
2. **Rule discovery (heuristic, soundness-irrelevant):** from concrete runs at n=base..base+2, read
   off the candidate `P(n): C(n) -> C(n+1)` (shape already known from `counter_structure.py`).
3. **Rule PROOF by induction (the sound core — every check MUST hold):**
   - Base case: simulate `C(base)` concretely, confirm it reaches `C(base+1)`, no halt before.
   - Inductive step: symbolically simulate `LHS(n+1)`; allow applying `P(m)` ONLY for `m < n+1` and
     `m ≥ base` (‼ assert strictly-smaller argument — the well-foundedness guard); base-step
     elsewhere; confirm it reaches `RHS(n+1)` and **never crosses a halt transition**.
   - Block-exponent arithmetic correct; no peel of a possibly-zero symbolic block.
4. **Only then NEVER_HALTS.** Settle time + the rule witness recorded.

## Gate (non-negotiable)
- Cross-check EVERY NEVER_HALTS against the trusted simulator to a big cap. Run against: known
  halters (BB2/BB3/BB4) + random halters (**must stay HALTS — 0 false proofs**); the 10 counters
  (target: become NEVER_HALTS); the 53 bouncers (already done by v3 — sanity, should not regress).
- Also cross-validate each proven `f(n)` against the concrete step count at several n (a wrong rule
  is caught even if the induction code has a bug).
- Success = **0 false proofs on halters**, and as many of the 10 counters proven as the engine covers.

## Fallback if the induction engine is too intricate to get sound in one sitting
**CTL (Closed Tape Language)**: find a regular language L of tape configs with (a) start ∈ L,
(b) L closed under δ, (c) no halting config in L ⇒ never halts. Soundness = a finite closure check
(no induction-on-n subtlety), which is why bbchallenge's CTL deciders prove many counters. More
mechanical, possibly less bug-prone than the inductive prover. Consider if (3) stalls.

## After STEP 2
63/63 three-state monsters settled → plug the full suite (translated-cyclers + bouncer_prove3 +
counter decider) into the real bbchallenge BB(6) undecided list = the new-contribution entry.

## The discipline (why this file exists)
Same as the bouncer STEP-2 plan: the proof engine is where soundness is earned and, tired, easily
lost. The spec is now in hand (no memory reconstruction). Resume here, fresh.
