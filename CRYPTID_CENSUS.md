# Cryptid census — the BB(6) open frontier is heterogeneous (2026-06-22)

Reconnaissance for the **mathematics road** to BB(6). The decider-engineering road is a proven dead
end (`BB6_PREP.md` ②: 0/300 holdouts decided; the community's stronger FAR already ran). The honest
remaining contributions are (i) resolve a named cryptid mathematically, or (ii) **catalogue** the
frontier as the named number theory it encodes — the §3c-style exact-reduction programme
(`antihydra_attack.md` §3c reduced Antihydra to the exact 2-adic criterion `v2(c_n-1) ≥ balance_n+1`).

To direct that effort, the first question is: **are all 19 open cryptids equally hard?** Run
`cryptid_census.py` (`cryptid_map.characterise` over `suite.CRYPTIDS`):

## Finding — NOT monolithic. Two clusters.

| cluster | machines | width growth | milestones | reading |
|---|---|---|---|---|
| **exponential-Collatz core** | Antihydra, o10, o15, o17, o18 | jumps ~2–3× (o15 `4,6,18,107,289,772`; o18 `2,9,27,75,203,545,1457`) | few (5–17) | genuine Collatz-like; o10/o17/o18 tagged COLLATZ on the binary value. **The Antihydra-class.** |
| **slow-width majority** | Space Needle, o2,o3,o4,o7,o11,o12,o13,o14,o16 (+o5,o8 borderline) | near-linear (ratio ≈1.0–1.1) | hundreds–thousands (o12: 1617) | the crude extractor finds a near-linear milestone; the real growth event is elsewhere / slower. |

(Full table reproduced by `python3.11 cryptid_census.py`.)

## What this means for the math road (prioritisation, not a claim)

1. **Exact-reduction programme (Route ii) → target the Collatz core first.** Antihydra, o10, o15, o17,
   o18 have clean, fast Collatz-like orbits, so the §3c method (derive tape mechanics → exact arithmetic
   halting criterion) is most likely to yield a **named open problem per machine** — turning the BB(6)
   core into an explicit catalogue "these N specific equidistribution/Collatz statements." This is novel
   (the community decides machines; it does not catalogue them as number theory) and achievable
   (cataloguing ≠ solving). **Lottery upside:** if any one reduces to a *decidable* arithmetic family,
   that decides a real holdout = a genuine BB(6) contribution via route (i).
2. **Slow-width majority → closer per-machine analysis.** Hundreds of near-linear milestones means the
   automatic milestone is the wrong event; these need hand-picked milestones before any reduction.
   Higher effort, lower yield-per-hour — defer behind cluster 1.
3. **Certificate hierarchy (`LIMIT_THEOREM.md` ⑥) → the original contribution, independent of solving
   any cryptid.** Push the [OPEN] "no REG certificate for a cryptid" toward [PROVEN] for one machine.
   §3c already pinned Antihydra's barrier to a named 2-adic statement (brick b′); the hierarchy work is
   where "don't give up on BB(6)" pays off *without* needing a Collatz breakthrough.

## Soundness caveat (mandatory)
This is **recon, not a decidability claim.** Every machine here survived the community's strong
deciders; a "LINEAR"/slow-width tag (e.g. o13) is almost certainly a milestone-extraction artifact, not
tractability. The census only *prioritises* where the math road looks; it asserts nothing about any
machine's status. (Discipline per `SOUNDNESS_INCIDENT.md`.)

## Status
- **[done]** census built + reproducible (`cryptid_census.py`); frontier shown heterogeneous.
- **[next, achievable]** apply the §3c exact-reduction to the Collatz core (o10/o15/o17/o18) → catalogue.
- **[open]** everything those reductions land on (Collatz-hard) + the hierarchy [OPEN] top.
