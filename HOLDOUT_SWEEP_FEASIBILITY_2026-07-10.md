# Outer-moat feasibility probe: the un-catalogued BB(6) holdouts (2026-07-10)

*Task C1 SCOPING probe (`ATTACK_PLAN_2026-07-10.md` §C1). Goal: what is the real holdout count, what do
our certified sound tools hit, and is an internal sweep feasible. Discipline: [PROVEN]/[OBSERVED]/[OPEN];
this decides nothing. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`. No posting.*

## 1. The real holdout landscape [OBSERVED — from the local record]

- **Total: 1104**, not "~1090". A machine-readable list IS present locally: `_bbdata/bb6_holdouts_1104.txt`
  (1104 lines, standard bbchallenge TNF text `1RB1RF_..._1RA0RA`, 42 chars/line, deduped up to
  isomorphism). Provenance (`bb6_holdouts.py` header): the **April 2026 bbchallenge-wiki curated
  still-open residual**, up to state-relabel + L/R-mirror equivalence. A newer 17.8M raw list exists; 1104
  is the curated open set. So the list is already obtained — no bbchallenge fetch needed.
- **Named: 17 open cryptids** (`suite.CRYPTIDS` = 19 entries = 17 open + BB6 champion (halts) + Lucy's
  Moonlight (halts, a false-proof gate test)). Completeness audit `O7_AND_CENSUS_COMPLETENESS_2026-07-09.md`:
  16 are Type-I ×p/q depth processes, o7 the sole non-Type-I. **Un-catalogued ≈ 1104 − 17 = 1087** (the "~1090").
- **The rest is structurally surveyed, not decided** (`BB6_FRONTIER_CENSUS_2026-07-04.md`, `holdout_census*.py`):
  all 1104 are slow polynomial-width counters (√t peak 665, sub-√t 399, log 33; 0 halt-in-cap, 0
  exponential-width). Block axis: ~522 bounded-digit (o3-class), ~540 digit-string, 22 unary-counter.
  These are `[OBSERVED]` growth/block proxies — they decide nothing.

## 2. Tool-reach on a fresh sample [OBSERVED]

Our certified sound suite is `suite.verdict` (the trusted battery: concrete sim, halt-unreachable,
translated-cycler, bouncer single/word/wall, halt-segment, FAR-DFA, FAR-CEGAR). Ran it on a 10-machine
even-spread sample of the 1104 (fresh, this session):

- **Decisions: 0/10 — all HOLDOUT.** Every machine exhausted the full battery and fell through.
- Cost: mean ~26 s/machine, range 4.6–129 s; the tail is dominated by **FAR-DFA/CEGAR** (129 s, 55 s).
- Consistent with the record: `tier3_suite` sampled 0/15, `cryptid_census` 0/300, all named cryptids HOLDOUT.

Failure mode is structural, not a cap artifact: the reach-tools (FAR, translated-cycler, bouncers) are the
**same decider class the bbchallenge community already ran to PRODUCE this residual**. The list is, by
construction, the survivors of exactly these tools. The bespoke certifiers that DID crack named structure
(`o4_bouncer_macro.py`, `o4_closure_certificate.py`, `o*_template_scan.py`) are hand-built per machine and
still terminate at `[OPEN]` protection — they are not push-button deciders and do not scale to a sweep.

## 3. Feasibility verdict [OBSERVED]

**Compute-wise bounded, yield-wise ~0.** A full sweep is 1104 × ~26 s ≈ **8 h single-threaded** (≈1–2 h on
8 cores; naive parallel pool needs `fork` context — the spawn default crashed here). So it is *runnable*,
but the expected new-decision yield is **essentially zero**, because our suite ⊆ the community's decider set.

**This is community-scale, not a weekend.** Genuinely clearing the outer moat needs either (a) the full
formal decider pipeline (Coq-BB5-scale) to certify the mechanically-decidable-but-unlabeled machines, or
(b) per-machine mathematical reduction for the cryptid-hard remainder. The structural census indicates the
residual is uniformly (K)-type / thin-set generalized-Collatz — i.e. **the mechanically-decidable fraction
our tools add beyond FAR ≈ 0**; the hard fraction is plausibly the whole set `[OPEN]`.

## 4. Recommended next step for the outer moat

Do **not** run the 8-h sweep-for-decisions — it re-derives 0. Instead: (i) run `holdout_census*.py` to
completion to partition all 1104 into (K)-Type-I vs thin-set-Type-II bands — the achievable *cataloguing*
contribution; (ii) frame C2 (BB(6)=N(champion) ⟸ the protections) as the honest completion skeleton, since a
full internal decision of the residual is out of reach with certified tools; (iii) reserve decider effort for
a genuinely NEW invariant outside the FAR/CTL class (cf. B1 o7 deep-2-power look-ahead), not a re-sweep.

No machine decided. No label upgraded.
