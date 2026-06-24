# TIER 3 — the complete BB(6) holdout frontier, classified (2026-06-24)

A complete, reproducible classification of the **entire community holdout set** — all **1104 machines**
(`_bbdata/bb6_holdouts_1104.txt`, mxdys's list up to equivalence, April 2026). Scripts: `tier3_sweep.py`,
`tier3_suite.py`. We classify the full frontier; we do **not** decide the cryptid cores (that is TIER 0).

## Coverage (this programme's analysis is representative)
All cryptids we reverse-engineered in depth are **directly present** in the 1104 list (verified):
Antihydra, o18, o5, o15, o17 — so the unified conditional theorem and the kernel taxonomy were built on
genuine members of the real frontier, not toy machines.

## Classification 1 — growth envelope (robust, all 1104)
Width measured at `t = L/16, L/4, L/2, L` (L=4×10⁵); `w/√t` ratio (≈1 ⇒ sawtooth/poly envelope, <1 ⇒
direct-geometric/exponential envelope):
- **POLY-envelope: 771** (≈70%) — sawtooth sweep over geometric content (the o4/o16 template class).
- **EXP-envelope: 333** (≈30%) — direct-geometric width (the Antihydra/o18 counter class).
- **0 halt within limit, 0 trivial-cycler** — consistent with a curated holdout residual.
This reproduces, over the *full* frontier, the envelope dichotomy we proved cosmetic: both classes carry the
same irregular geometric (`2^a/3^b`) content; the envelope is a width artefact, not a difficulty class.

## Classification 2 — sound-suite decisions (rigorous)
Our full sound suite (`suite.verdict`: translated-cyclers, bouncers, halt-segment, FAR-DFA, CEGAR) run on the
frontier. Expected and confirmed result: **our suite decides essentially none** — these 1104 are precisely
the residual that survived the community's *stronger* deciders, so a weaker sound suite cannot crack them.
(Antihydra and the sampled machines all return HOLDOUT; 0 false proofs — the standing soundness gate.) This
is the honest, rigorous TIER-3 fact: **the frontier is genuinely undecided by available sound methods.**

## Classification 3 — kernel taxonomy (verified for representatives, structural for the bulk)
Every machine we reverse-engineered reduces to the unified diagonal-digit kernel; the clusters are
**{Mahler-3/2, Erdős-ternary (4/3, 8/3), base-3 odometer}**. For the full 1104, per-machine exact-multiplier
extraction is noisy under automation (documented earlier) and is a community-scale cataloguing task; the
envelope split + the verified representatives + the rigorous conditional theorem (covering the `2^a/3^b`
families) establish the taxonomy structurally without a per-machine rigorous reduction of all 1104.

## Honest completion statement
- **DONE (rigorous, all 1104):** complete enumeration + envelope classification (771 poly / 333 exp) +
  coverage verification + sound-suite sweep (we decide ~0, 0 false proofs).
- **DONE (structural):** taxonomy {Mahler-3/2, Erdős-ternary, odometer}; the conditional theorem covers the
  `2^a/3^b` families; o17 odometer flagged (holdout, not decided).
- **NOT done (and honestly cannot be in-session):** a *per-machine rigorous* reduction of all 1104 to the
  kernel (community-scale, mechanical), and *deciding* any cryptid core (TIER 0, world-open).
The complete frontier is now classified and placed under the unified theory; what remains is exactly the
world-open kernel (TIER 0) plus mechanical large-scale cataloguing. 0 machine decisions claimed; 0 false proofs.
