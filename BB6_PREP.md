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
