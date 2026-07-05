# Accelerated macro-machine for o4 — validated RLE sim + a robust closed macro-graph; strong certificate, but NOT a proof (2026-07-05)

*Carefully implementing the accelerated macro-machine to decide o4. **Built and validated a sound run-length (RLE)
simulator** (matches the concrete TM step-for-step, 200k steps), and a **closed observational macro-graph** (finite,
halt-free, escape-free, robust to window size). This is a **compelling certificate that o4 does not halt** — but it is
**not a rigorous proof at the FAR/CTL bar**, because the closure is verified over the *observed orbit*, not the
*abstract transition relation*, and the macro-transition is non-deterministic (non-local big-gap). Per the
zero-false-proof discipline, **o4 is NOT claimed decided.** SOUNDNESS: `[OBSERVED]`/`[VALIDATED]`; halting `[OPEN]`.*

## What was built and validated `[VALIDATED / OBSERVED]`
1. **Sound RLE simulator.** Run-length tape simulator (tape = list of `[symbol,length]`, head at `(run,offset)`),
   **validated step-for-step against the concrete bytearray simulator over 200k steps — exact match** on `(state,
   read-symbol)`. Trustworthy accelerated substrate.
2. **Closed observational macro-graph.** Abstract each config to `(state, local run-window ±RW, 0-runs clamped to
   CLAMP)`. Over millions of steps:
   | window | macro-states | all-new-by | halt-macros | escaping transitions |
   |---|---|---|---|---|
   | `RW=4, CLAMP=4` | **313** | step 3758 (0.1%) | **0** | **0** |
   | `RW=6, CLAMP=6` | **728** | step 20544 (1.0%) | **0** | **0** |
   The set is **finite, appears entirely in the first ~1%, is halt-free, and is closed** (no observed transition
   escapes) — and **robust to window size** (larger window → more states, same closed/halt-free verdict), indicating a
   genuine finite-state description, not an aliasing artifact.

## Why this is NOT yet a proof `[the honest soundness gap]`
- **Observational vs abstract closure.** The escape-free result checks that every transition *taken on the observed
  orbit* lands in the set. A FAR/CTL **proof** requires closure over the **abstract relation**: from each macro-state,
  for **every** concrete tape consistent with it, the successor is in the set. The observed orbit samples only some
  such tapes.
- **Non-determinism from the non-local big gap.** The macro-transition is **not** functional (a macro-state has several
  successors, depending on the big-gap position/length outside the window — verified earlier). So a future config
  mapping to a seen macro-state could, in principle, take an **unobserved** successor (outside the set or a halt); the
  observed closure does not exclude this.
- Hence this is a **strong candidate invariant**, not a verified one. The rigorous step — verify abstract closure over
  the reachable-config invariant (resolving the boundary incoming-cell via the tape language) — is exactly what a
  formal FAR/CTL certificate does, and is **not completed here**.

## Honest verdict `[SOUNDNESS FIRST]`
**o4 is NOT decided. I do not claim it.** The accelerated macro-machine yields a **compelling, window-robust,
halt-free closed observational certificate** (validated RLE sim + explicit `0^G(10)^a1001` invariant + exact base-4/3
odometer + finite closed macro-graph), which makes non-halting **extremely likely** — but the **abstract-closure
verification** required for a rigorous decision (given the non-deterministic non-local big gap) is the remaining step,
and asserting a decision without it would be a false proof. o4 stands as the BB(6) cryptid with the **strongest
decidability certificate short of a formal FAR/CTL proof**. **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `/tmp/o4_rle.py` (RLE sim validated vs concrete, 200k, exact match), `/tmp/o4_macrograph2.py` / `_3.py`
  (`RW=4→313`, `RW=6→728` macro-states, halt-free, escape=0). Basis: `O4_COUNTER_CERTIFICATE_2026-07-05`,
  `O4_CLOSURE_PROOF_ATTEMPT_2026-07-05`, `o4_transducer.py`.
