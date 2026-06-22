# Preparing for BB(6) — what we built and what the data says (2026-06-22)

Goal: prove BB(6) = decide every undecided 6-state machine. The frontier is the **holdout list**
(~1104 reps up to equivalence, wiki; ~17.8M raw). Two sub-paths: (A) engineering — decide bulk
holdouts; (B) mathematics — the cryptids (Collatz-hard, the real wall). Preparations built:

## ① BB(6) novelty oracle — `bb6_holdouts.py`  ✅
The piece we lacked in INCIDENT 2: when a sound decider returns NEVER_HALTS on a 6-state machine,
is it still open (a contribution) or already decided? `is_holdout(spec)` answers it, up to machine
isomorphism (TNF relabel + left-right reversal — the same dedup the holdout list uses). Validated:
reversed/relabeled variants of a holdout still match; the decided champion does not. **Now any
NEVER_HALTS on a 6-state machine can be checked for novelty (never auto-claim — scrutinise).**

## ② Run our deciders on the real holdouts — DONE, honest result: 0
Ran FAR (k-tails) + CEGAR on **300 of the 1104 holdouts: 0 decided.** They survived the community's
pipeline (which includes their own, stronger, FAR — mxdys decided 113/1534 with it). Conclusion,
now data-backed: **our current deciders are not ahead of the community's; the engineering path (more
of the same deciders) will not yield a BB(6) contribution.** A contribution needs either a decider in
a class they have not exploited, or the mathematics of path (B).

## ⑤ Cryptid characteriser — `cryptid_map.py`  ✅
Maps the frontier to the number theory it encodes. For a machine it extracts the milestone orbit
(width / binary value at successive turning points) and classifies the update rule: LINEAR (bouncer),
AFFINE/GEOMETRIC (counter), PARITY-PIECEWISE-AFFINE (Collatz-like = cryptid), or IRREGULAR. Validated:
Antihydra & Lucy → IRREGULAR/candidate-cryptid (correctly: open); our counter → `v->4v+6`; our
bouncer → linear width. This is the tool for path (B): it shows *which* Collatz-like object each
cryptid is, so the open frontier can be catalogued (not proved).

## ⑤′ Cryptid census — the frontier is heterogeneous (`cryptid_census.py`, `CRYPTID_CENSUS.md`)  ✅
Ran ⑤ over all 19 open cryptids. **Not monolithic:** a small **exponential-Collatz core** (Antihydra,
o10, o15, o17, o18 — width jumps ~2–3×, few milestones, clean Collatz orbits) vs a **slow-width
majority** (15 machines, near-linear width over hundreds–thousands of milestones — the auto-milestone
is the wrong event). Directs path (B): apply the §3c exact-reduction (`antihydra_attack.md` §3c, which
reduced Antihydra to `v2(c_n-1) ≥ balance_n+1`) to the Collatz core first → catalogue the BB(6) core as
named open arithmetic problems; lottery upside if one reduces to a decidable family. Recon only, no
decidability claim (the slow-width tags are extraction artifacts; all survived the community pipeline).

## ③④ Scale / missing deciders — DEFERRED
Premature: ② shows our deciders don't crack holdouts, so optimising/scaling them or porting more
(WFA, etc.) chases the community's lead. Revisit only if a genuinely novel decider appears.

## ⑥ Limit theorem / certification hierarchy — NEXT (the original contribution)
The honest leverage: not competing on deciders, but proving **why** BB(6) is hard. The hierarchy
`regular ⊊ semilinear ⊊ Collatz-like`, and that specific cryptids provably escape the lower classes
(their reachable-config language is non-regular; their orbit is not semilinear). This does NOT prove
BB(6), but rigorises "no finite/regular certificate exists" — the Turing-machine avatar of the quantum
genuineness limit theorem (finite observation cannot certify the infinite property; the spoofer game).
`cryptid_map.py` supplies the orbits this theory reasons about.

## Bottom line
BB(6) itself remains open mathematics (the cryptids). We are now properly equipped for the parts we
CAN advance: recognise a contribution if we ever decide a holdout (①), know our deciders don't (②),
and map + theorise the cryptid frontier (⑤ → ⑥). The soundness discipline (INCIDENT 2 caught + fixed)
is intact throughout.

## Feasibility verdict — "is a BB(6) proof possible?" (2026-06-22, tested)

Tested directly, not asserted. Evidence:
1. **Proven** (`LIMIT_THEOREM.md`): the tame certificate hierarchy is strict — k-window ⊊ regular ⊊
   semilinear (conjecture-free witnesses). Tame certificates do not reach the cryptid ceiling.
2. **Computed** (`certification_cost.py`): the certification cost of a cryptid is `K* = ∞` — its update
   map is non-parametric, so no finite observation/certificate pins it (Antihydra orbit 2240 pts, no
   parity-mod-2..6 affine model predicts it).
3. **Empirical, uniform**: a random sample of **80 holdouts → 80 non-parametric** (`certification_cost`),
   and the orbits are genuine super-exponential irregular Collatz-like sequences (e.g.
   `[3,43,235,2031,32427,261819]`), not extraction noise. **No tractable (finite-parameter) holdout
   was found.**
4. **Our deciders**: 0 of 300 holdouts decided (FAR k-tails + CEGAR).

**Verdict — precise (could-not vs cannot).** BB(6) has a definite value, so a proof exists *in
principle*. What is established and what is NOT:
- **WE COULD NOT prove it** (a fact, not an impossibility): our deciders settled 0/300 holdouts; a
  random 80-holdout sample is uniformly non-parametric (genuine Collatz-like orbits); the community's
  deployed pipeline left exactly this residual. This is failure-of-current-tools.
- **It is NOT proven impossible.** We did NOT show "no certificate exists" for any cryptid. What is
  *proven* is only that the tame hierarchy is **strict** (k-window ⊊ regular ⊊ semilinear). The
  claim "cryptids escape ALL tame classes / have no certificate" is **[OPEN]** in `LIMIT_THEOREM.md`
  (the over-approximation gap) — conjectured, not proven. `K*=∞` concerns one method (fitting the
  milestone map); the 80/80 figure is an empirical classification. None of these prove impossibility.
- So: a cryptid is an **open problem**, not an impossibility. "Collatz-hard" = as hard as a known open
  problem; open ≠ impossible — the community keeps shrinking the holdout list, and any cryptid could be
  settled by new mathematics.

**Bottom line: we *could not* (current tools fail, barrier identified) — NOT *cannot* (no impossibility
proven).** Honest routes forward unchanged: (i) resolve a named cryptid mathematically (Collatz-hard
research), or (ii) find a non-cryptid holdout the pipeline missed — our sweep found none.
