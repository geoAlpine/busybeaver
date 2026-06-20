# Bouncers decider — STEP 2 build plan (the PROOF engine)

**Build this with a CLEAR HEAD. Gate every NEVER_HALTS against the oracle. Do NOT ship a
"looks right" version (the night's lesson: Lin-Rado emitted false proofs twice).**

Spec source: Iijil1/Bouncers README (verbatim) + arXiv 2504.20563 §7. We already have STEP 1
(detection, `bouncers.py`) and the test set (`holdouts3_reps.txt`, 53 bouncers) + the oracle
(known halters must NEVER be flagged NEVER_HALTS).

## Data structures
- Tape in **run-length form**: `w_0 (w_1)^n w_2 (w_3)^n ... w_k` — even-index = **walls** (fixed
  words), odd-index = **repeaters** (copied n times). Plus a small **buffer** word split off w_0,
  treated like extra state ("backward-symbol macro machine").
- A config `C(n) = w_0 buf S> w_1^n w_2 ... w_{k-1}^n w_k` (head at left repeater boundary, state S).

## Pipeline
1. **Detection (have it):** simulate; record-breaking configs (new tape extreme). Find records whose
   step-counts fit `a + b n + c n²`. (STEP 1 already flags structure + growth.)
2. **Split into walls/repeaters:** compare two successive records; "color" each cell by the sequence
   of states that visited its neighborhood since the last record; greedily split into matching
   walls + repeaters. (Detection heuristic — soundness-irrelevant; a bad split just fails to close.)
3. **Pick buffer size:** from the turn-around step sequence between records; enlarge until each term
   covers a full repeater (so the head never turns around outside the buffer during a chain rule).
4. **Derive the rule list** `r_0..r_l` (l odd; r_i a chain rule for even i): each rule is
   `buf S> word -> word' buf' S'>` (or the mirror), found by direct simulation over the
   (word+buffer) window.
5. **VERIFY (the sound core — checks that MUST all hold):**
   - **Base:** simulate to `C(0)` exactly (state, head, tape), no halt before it.
   - **Each transition rule** holds by direct simulation, and the head **leaves the (word+buffer)
     window only on the LAST step** (except the leftmost-wall rule). ‼ critical for soundness.
   - **`len(buf) == len(buf')`** every rule.
   - **Chain rules** (repeaters): start/end buffer, state, direction identical; `len(word) != 0`.
   - **Apply the rules** to `C(n)`, checking each rule's precondition at the current position.
   - **Close the induction:** right-align repeaters via `(xy)^n x = x (yx)^n`; verify the result
     equals `C(n+1)` (w_0, buf, S, pos, dir equal AND every aligned segment v_i == v'_i).
   - Only then return NEVER_HALTS (with settle time S = t0+1, period P = t1-t0).
6. **Mirror fallback:** for "translated-right" bouncers that never reach the fixed left-boundary
   position, swap all L<->R transitions and prove the mirror instead.

## Gate (non-negotiable)
- Build a harness: for every machine, if STEP 2 returns NEVER_HALTS, cross-check with the trusted
  simulator up to a big cap. **Any NEVER_HALTS on a machine that HALTS = STOP, the engine is
  unsound.** Run against: the known halters (BB2/BB3/BB4) AND a few random halters AND the 53
  bouncers (which should become NEVER_HALTS) + the 10 counters (should stay HOLDOUT — bouncers
  ≠ counters).
- Success = 0 false proofs on halters, and as many of the 53 bouncers proven as the
  implementation covers.

## After STEP 2
- counter-induction decider for the 10 counters (sligocki 2022).
- Plug the full suite into the real bbchallenge BB(6) undecided list → the new-contribution entry.

## The discipline (why this file exists)
STEP 2 is the one piece that must be built clear-headed and oracle-gated. The detection (STEP 1)
and everything before it is sound by construction (measurement). The proof engine is where
soundness is earned — and where, tired, it is easily lost. Resume here, fresh.
