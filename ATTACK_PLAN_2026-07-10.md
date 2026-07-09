# Attack plan toward the complete BB(6) proof — full move enumeration + hand-off (2026-07-10)

*Hand-off document for the next session/model. Captures: the state snapshot, the completed (K)-wall attack record
(all six build attempts + the final u₀-exclusion verdict), and — the key strategic finding of the 07-10 analysis —
the COMPLETE enumeration of remaining moves, including the never-attempted Category B (thin-set machines), which is
the recommended next strike. Discipline: ZERO false proofs; labels [PROVEN]/[OBSERVED]/[OPEN]; every subagent result
independently re-verified before commit; corrections logged in place; end reports with "No machine decided. No label
upgraded." unless a machine IS decided. Interpreter: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`. Policy: NO
bbchallenge community posting (reading public data is fine); AEV outreach gated on explicit user go-ahead.*

## 0. State snapshot

~75 commits (07-06→07-10). Zenodo v1.0 published (DOI 10.5281/zenodo.21252622), v1.5 draft ready (auto-release on
`git tag`). Lean: 8 modules, 324 theorems, sorry-free, axioms `[propext, Quot.sound]`. Papers: 6 (RUN_STRUCTURE,
TEMPLATE_METHOD, SPECIES_SURVEY, MIRROR_LADDER, CENSUS, RIGIDITY_LIMITS). Census: 17 named open cryptids, 16 Type-I
(one ×p/q fixed-point depth process each), o7 the sole non-Type-I. Master index: `CAMPAIGN_2026-07-06_TEMPLATE_LEDGER.md`.
One-page problem statement: `OPEN_PROBLEM_2026-07-10.md`.

## 1. The (K) wall — attack record COMPLETE (7 build attempts, all coordinates closed with proofs)

The wall: per-seed ℤ_q^×-equidistribution of reload units ⟺ a-priori E[K²] bound ⟺ base-p/q normality ⟺ AEV
Conj 1.6. Every angle now has a precise closure:

| angle | verdict | note |
|---|---|---|
| run-cap potential / heavy-tail | both weapons ORTHOGONAL to the 1st-moment fatal direction (C-S gap √n) | `O4_NEWMATH_BUILD` |
| weighted sub-action on B(3,k) | closes on the δ₋₁₄ fixed point, growth-independent | 〃 |
| digit theory (Mahler/DS/Koksma) | cryptid provably on the OPEN side of the autonomy split; SML empty | `NEWMATH_DIGIT_BRIDGE` |
| excursion via exact reload map | carry-coupling ABSENT (unit refresh decouples depths) | `RELOAD_EXCURSION_BUILD` |
| cross-machine transfer | none — even the IDENTICAL ×3/2 engine is per-seed | `RELOAD_MAP_UNIFIED` |
| measure rigidity (EKL/IP/op-norm) | inapplicable to the whole {2,3}-host, uniformly | `PAPER_RIGIDITY_LIMITS` |
| **solenoid diagonal (u₀ exclusion)** — the last un-tried | the diagonal IS real (yesterday's u₀ was an **archimedean phantom**, corrected in place) but delivers exactly the run-cap = first-moment ⊕ support; a cap-legal E[K²]=∞ adversary survives | `U0_EXCLUSION_BUILD_2026-07-10` |

**Conclusion [honest]: the internal structural attack surface of (K) is exhausted with proofs.** What remains for the
14 (K)-machines: (i) external — the AEV/Eliahou hand-off (letter ready, o4-easiest instance `freq{3∣W_n}≤4/5−ε`,
seed 57, margin 2.4); (ii) genuinely new mathematics per the design spec (`NEWMATH_BUILD_SYNTHESIS` §"design spec" +
the u₀ refinement: must exclude the CAP-LEGAL adversary class).

## 2. THE KEY STRATEGIC FINDING: Category B — the thin-set machines were NEVER attacked

All banked no-gos (No-Structure, AIU, coisometry, excursion, digit) are obstructions to **density/frequency**
statements. But the census completeness audit (`O7_AND_CENSUS_COMPLETENESS_2026-07-09.md`) established that **o7 and
Space Needle are NOT (K)-species** — their protections are **thin-set REACHABILITY** walls, a different species the
no-go corpus does not cover. Reachability walls sometimes FALL to finite congruence/automaton invariants. **These are
the only named machines where an actual DECISION might be internally reachable.** Never attempted.

### B1. o7 congruence-invariant attack (the prime target)
- Machine: o7 (spec in `o7c_o7_chain.py` / `X32_CLEANUP_2026-07-08.md`). Milestone automaton [OBSERVED, 0-mismatch,
  30 milestones to 2·10⁷]: state D at left frontier, tape `0 1^a 0 1^b`. HALT ⟺ `u = a+3 = 2^k` ever (oddpart(u)=1);
  `b` never tested. Dynamics on u: even step `u → 3u/2`, odd step `u → (u+1)/2` (verify exact from the chain script).
  Measured: min oddpart(u) at entries = 7.
- The attack: for moduli `M = 2^j · m` (m odd smooth, j up to ~20+), compute the forward-reachable set of
  `(u mod M, phase)` from the actual seed under the certified milestone dynamics. With M containing 2^j, the next j
  parities are DETERMINED by the residue — so branching only occurs at depth-j exhaustion (a sound finite-state
  over-approximation, far sharper than naive both-branches). If the reachable set avoids the halting-consistent
  residues `{2^k mod M : k ≥ bitlen-floor}` → **o7 NON-HALT [PROVEN given automaton]** → then certify the milestone
  automaton via the trace-template method (as done for o2/o11 etc.) → **o7 DECIDED** — the first cryptid decision.
- Prior-art caution: bbchallenge holdouts survived community FAR/CTL deciders, which subsume SHALLOW tape-level
  regular invariants. o7's u is unary-encoded, so a pure mod-m invariant would likely have been found. The NEW room:
  (i) large 2-power components 2^j (deep parity look-ahead) beyond FAR's searched automaton sizes; (ii) the invariant
  need only hold at MILESTONE moments (our automaton), not all tape configs — a much weaker requirement than FAR's;
  (iii) joint (u mod M, phase) products. Be honest if the reachable set is full (= the thin-set wall is real for this
  machine too; measure the closure growth).
- Also try: backward analysis (which residues can REACH 2^k), and the "u ≡ 0 mod small-prime persists" family.

### B2. Space Needle invariant attack (same species)
- From `O16_SPACENEEDLE_FIXEDPOINT_2026-07-08.md` + `o16sn_*.py`: ×5/2 on the even branch (run = v₂(b+4)); odd branch
  has NO single fixed point (v-indexed carry); fatal set measured SPORADIC: `{2^k−1} ∪ {6,102,311,351,371}` (re-derive
  the exact fatal condition from the note before attacking). Cumulative, summable lean.
- Same congruence-automaton method on SN's counter at gate moments, plus: is the sporadic finite part `{6,102,...}`
  already passed (orbit beyond)? If the residual fatal set is exactly `{2^k−1}`, the same 2-power look-ahead attack
  applies. If SN falls → second decision.

### B3. o17 symbolic gate extension (timing wall — possibly also non-density)
- From `O17_GATE_LAW_2026-07-07.md` + `lean/O17.lean`: no template (proven), gate-to-gate map exact, gates
  tower-sparse (next ~10^60). The wall was labeled "(K)-shaped timing" — RE-EXAMINE: if the gate-to-gate map on the
  halting-relevant residue is eventually periodic or admits an invariant, o17 is DECIDED. Gate values are
  tower-represented — compute gates SYMBOLICALLY far beyond 10^60 (mod small M via tower exponent reduction,
  Euler/CRT) and test for periodicity/invariant of the safety condition. Honest outcome may be "aperiodic, counter-
  dependent = the (K) shape confirmed at gate level" — but the symbolic-mod computation is untried.

### C. The outer moat (needed for the COMPLETE proof regardless of (K))
- **C1. The ~1090 un-catalogued holdouts**: the full BB(6) holdout list (source: bbchallenge public data — reading is
  policy-OK; check `BB6_FRONTIER_CENSUS_2026-07-04.md` first for what's already local). Sweep with OUR certified
  tools (trace-template certifier, bouncer macro, translated-cycler certificates, fixed-point run laws). Goal:
  classify all; decide any that fall to our machinery; measure what fraction is genuinely cryptid-hard. Without this,
  "complete proof" has an unmapped flank.
- **C2. Conditional completion skeleton**: formalize "BB(6) = N(champion) ⟸ the 17 named protections" — the maximal
  internal structure: every holdout decided-or-reduced, champion step count computed, the reduction Lean-checked.
  (Champion: verify the known BB(6) champion's halt + step count locally as a first step.)
- **C3. External**: AEV letter (READY, gated on user go-ahead — never send autonomously). arXiv of
  PAPER_RIGIDITY_LIMITS + PAPER_MIRROR_LADDER is the natural (K)-independent publication; needs user decision.

## 3. Recommended execution order (if continuing autonomously)

1. **B1 (o7)** — the highest-value untried internal move; a decision is genuinely possible.
2. **B2 (SN)** + **B3 (o17)** in parallel — same session.
3. **C1 (holdout sweep probe)** — feasibility first (is the list obtainable? what do our tools hit?).
4. On any DECISION: red-team it (adversarial verification, the milestone automaton must be certified, Lean if
   possible), then it is the campaign's first decided machine — update PAPER_CENSUS, the ladder, and memory.
5. (K)-machines: park (internal surface exhausted with proofs); revisit only with the cap-legal-adversary-excluding
   design spec or external input.

## 4. Verification battery
`verify_all.py --quick` (7/7 PASS as of a5ced05); full battery 12 items. Lean: `~/.elan/bin/lake build` (17 jobs
green). Zenodo: `zenodo/build_package.py --version X.Y` self-tests; release = `git tag vX.Y && git push origin vX.Y`
(draft-by-default, publish is the user's click at https://zenodo.org/uploads/21253229).
