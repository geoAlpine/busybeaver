# Real bbchallenge data — the suite (with the FAR engine) on genuine machines (2026-06-22)

We pointed the sound suite at REAL bbchallenge machines, not just our 63 monsters. Two datasets.
`bb5db.py` reads the official seed DB; the BB(6) frontier list is from `wiki.bbchallenge.org/wiki/BB(6)`.

## 1. The real BB(6) frontier (26 machines, verbatim from the wiki)
Champion + all named/potential Cryptids (Antihydra, Space Needle, Lucy, Hydra variants, …) + 2 top
halters. **Result: all 26 → HOLDOUT, 0 false proofs.** Correct and sound:
- the open Cryptids are Collatz-hard — no sound decider may (or does) prove them; we HOLD OUT every one;
- the two halters halt only after astronomically many steps (>> our 2M cap), so HOLDOUT is the sound
  answer — we never falsely claim non-halting.
This is the meaningful soundness result on the actual open frontier: **zero false claims.** The famous
BB(6) cryptids are beyond FAR (they are open mathematics, not a regular/counter non-halting reason).

## 2. The real BB(5) seed database (88,664,064 machines, downloadable, all proven non-halting)
The genuine bbchallenge "undecided machines" database (30-byte records; `bb5db.py` decodes it). BB(5)
is closed, so every machine here is non-halting — clean ground truth. **Random sample of 2000:**

| stage | decided non-halt | how |
|---|---|---|
| fast deciders | **1871 / 2000 (93.6%)** | translated-cycle 1394, halt-unreachable 303, halt-segment 142, word-bouncer 19, single 9, wall 4 |
| **+ FAR (memory-DFA)** | **+70 of the 129 holdouts** | k-tails state-merge invariant, each VERIFIED |
| **TOTAL** | **1941 / 2000 = 97.0%** | **0 false proofs** (0 HALTS; every FAR claim cross-checked vs a 5M-step sim) |

**FAR cracked 54% of the residual holdouts on real bbchallenge-hard machines, soundly.** This is the
concrete payoff: the FAR engine is a genuine decider that extends our reach on real data beyond the
cyclers/bouncers, with the soundness discipline intact (0 false across the whole run). The remaining
~3% need CEGAR (slower) or harder analysis.

## Honest reading
- BB(6) itself is NOT advanced by this — its frontier is open mathematics (Antihydra = Collatz), and we
  correctly HOLD OUT all of it. No false step there is the win.
- On the real BB(5) undecided DB, the suite (esp. FAR) is strong: 97% of a real hard sample, 0 false.
- Caveat: this is REACH on a known-non-halting set, not a halting-soundness test (that is covered by the
  random audits with halters: FAR 1494 claims / 0 false, CEGAR 243 / 0 false). Together they show the
  FAR engine is both strong and sound.

## Repro
`python bb5db.py` (decoder). Sampling/measurement scripts are local (`_bb5_run.py`, gitignored with the
2.9 GB `_bbdata/`). DB: `docs.bbchallenge.org/all_5_states_undecided_machines_with_global_header.zip`.

## 3. The real BB(6) holdout list (1104 machines, wiki, "up to equivalence")
The hard residual that survived the community's deciders (incl. their own FAR). We ran the full suite
(fast deciders + our FAR + CEGAR). **Fast deciders + FAR + CEGAR decided 0 of the 1104** — expected,
these survived stronger deciders, and the rest are open cryptids (Collatz-hard). 0 false from those.

**BUT `wbounce2` returned one `NEVER_HALTS` — and it was a FALSE PROOF.** Rigorous concrete
re-verification showed the claimed bouncer rule `C(n)->C(n+1)` does not hold (real machine does
`C(1)->C(6)`); `wsim`'s chain macro-step was unfaithful at small `n`. See `SOUNDNESS_INCIDENT.md`
INCIDENT 2. We **caught it before claiming any contribution**, verified the 63/63 monsters are all
still concretely sound (blast radius zero), and added a **concrete-induction gate** to `wbounce`/
`wbounce2` (a `wsim` closure is trusted only if the trusted simulator confirms `C(base+j)->C(base+j+d)`
for j=0,1,2). After the fix: the BB(6) machine -> HOLDOUT, suite still **63/63, 0 false**.

**Honest outcome:** we did NOT decide any genuine BB(6) holdout (consistent with them surviving the
community pipeline). The real payoff was the opposite of a contribution and more valuable to the
project: **real BB(6) data exposed a latent false-proof generator that all synthetic audits missed**,
and the soundness discipline caught and fixed it. That is exactly what this project is for.
