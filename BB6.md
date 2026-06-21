# BB(6) — what the sound suite actually establishes

Honest accounting of the BB(6)-relevant results. **We did NOT decide any open BB(6) machine** — those
are open for a reason and our deciders are weaker than the bbchallenge frontier. What we DID:

## 1. The sound suite is SOUND on the real BB(6) frontier (0 false proofs)
Ran the trusted suite (`suite.py`) on **20 real BB(6) machines taken verbatim from the bbchallenge
wiki** — the current Champion, the top halter, and all 18 named Cryptids (Antihydra, Space Needle,
Lucy's Moonlight, and the rest), both "probviously non-halting" (Open) and "probviously halting".

**Result: all 20 → HOLDOUT. 0 false proofs.**

This is the meaningful soundness result: on the hardest known 6-state machines — the actual open
frontier of mathematics on the BB scale — our suite makes **zero false claims**. It never asserts
non-halting for a machine whose halting is open or that provably halts. This is exactly what the
quarantined `bouncer_prove v3` got wrong: v3 would "prove" Antihydra (Open) and Lucy's Moonlight
(Halts) never halt — false proofs. The sound suite correctly HOLDS OUT every one.

These machines are now a permanent frontier gate (in `suite.py`): no decider may ever return
NEVER_HALTS on the Open/Halts cryptids.

## 2. Sound on a sample of the real BB(6) seed space
The 6-state seed space IS the BB(6) search space. Running the suite on a large random sample:
0 false proofs (every NEVER_HALTS cross-checked against the trusted simulator), ~6–7% HOLDOUT
(genuine 6-state holdouts for our tools), the rest HALTS / proven-non-halting. Confirms the suite is
sound at scale 6, not just on the 3-state monsters. (Random sampling finds only short halters, so the
sampled lower bound is tiny — records come from construction, not random search; cf. `hunt6.py`.)

## 3. Portability
The bouncer / counter techniques here are the SAME family bbchallenge uses for BB(6). The suite parses
the standard format at any state count and reproduces BB(4)=107, BB(5)=47,176,870 exactly. So it is
ready to run against the real bbchallenge BB(6) undecided database.

## What a genuine BB(6) CONTRIBUTION would need
Deciding a machine in the official `bb6_undecided_index` that no existing decider has settled. That
needs the binary undecided index + the 88M-machine seed database (a data-acquisition step not done
here). Our HOLDOUT on the frontier cryptids shows our current deciders won't crack those specific
hard machines — a real contribution would more likely come from the counter engine (once PIECE 3 is
finished, sound) applied to the broad undecided set, not from the cryptids.
