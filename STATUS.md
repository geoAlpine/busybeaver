# Busy Beaver — status (2026-06-21)

Deciding the **63 distinct 3-state "monster" holdouts** (`holdouts3_reps.txt`) — the hard residual the
trivial + cycler deciders leave behind. Every claim here is SOUND: machine-checked and gated.

> **Big-picture map / consolidation: see `MAP.md`** (BB(6)-goal oriented, the single source of truth).

## Headline
- **63 / 63 monsters PROVEN never-halt — SOUNDLY** (0 false proofs). The hard 3-state residual is
  CLOSED. Breakdown: **23 halt-dead**, **14 single + 16 word + 3 wall bouncers**, **5 halt-segment**,
  **1 FAR (k-tails memory-DFA)**, **1 FAR-CEGAR**.
- The two binary **counters** fell to FAR memory-DFA invariants (automaton-recognised regular
  non-halting reasons), VERIFIED sound: `1RB1LC_0LA0RB_1LA0LZ` by k-tails state-merging, and
  `1RB0LZ_1LC1RA_0RA0LC` by **CEGAR** (its invariant needs a boundary-anchored prefix-parity that
  suffix-merging can't learn; CEGAR discovers it from the verifier's own counterexamples).
- Soundness audited the v3 way: all 19 cryptids HOLDOUT, halters HALTS; FAR random audit 1494 claims
  / 0 false, CEGAR random audit 243 claims / 0 false.
- The 2 boundary-coupled bouncers (`1RB0LC_0LA0RA_1LA0LZ`, `1RB0LZ_1LC0RA_0RB0LB`) are now PROVEN by
  **`wbounce2.py`**: it finds a period-q repeater wedged between fixed walls via a two-record diff
  (`x1 == (W)^m + x0`, repeater grows at the head end), builds `C(n)=[head (W)^n wall]`, and closes
  `C(n)=>C(n+d)` on the G1-validated `wsim`. A **faithfulness gate** (`cfg_to_tape(C(base))` must equal
  the real record) blocks closures on configs the machine never reaches — the key soundness link.
- The two binary counters (`1RB0LZ_1LC1RA_0RA0LC`, `1RB1LC_0LA0RB_1LA0LZ`) were the last residual.
  Structure (`far.py` analysis): C-turn family `0 1^(2m) -> 0 1^(2m+2)`, time **doubles** (gaps
  `2^(k+4)-2`); single-pass symbolic closure is provably impossible (the `0^n` carry materialises a
  size-n counter block). Non-halt reason = "state A never reads 1", a REGULAR but non-local invariant
  — proven by the FAR memory-DFA engine below.

## FAR engine (cracked BOTH counters) — SOUND, audited
Three layers, soundness-first:
- `far.py` (LAYER 0): config-string single-step rewrite, **validated** cell-for-cell vs the trusted
  sim (5 machines x 4000 steps).
- `far_dfa.py`: the **sound verifier** (`Invariant.verify`) — checks start in L, closure
  `succ(L) subset L` (per-context suffix-language inclusion, no transducer), no halt in L, on ANY DFA.
  Decider-agnostic: a wrong DFA fails verification, never a false proof.
- `far_finder.py`: auto-builds a **memory-DFA invariant** by RPNI-style k-tails state merging on the
  reachable-config sample (folds the counter loop), then hands it to the verifier. Leading
  blank-invariance = root `0`-self-loop; trailing = `endable` follows the `0`-chain.
- **Result: cracked `1RB1LC_0LA0RB_1LA0LZ`** (|Q|=8 invariant, k=2). **Audited (the v3 discipline):
  all 19 cryptids HOLDOUT, BB4 halter HALTS, random audit 1494 NEVER_HALTS claims cross-checked,
  0 false.** Integrated into `suite.py` as the `far-dfa` decider.
- **`far_cegar.py`:** RPNI Blue-Fringe state merging with NEGATIVE examples — a merge is kept only if
  the result accepts no known-bad string. Negatives come from the verifier itself (`self.witness`: a
  concrete spurious config per failed check). Loop build->verify->add witness->rebuild. Cracked
  `1RB0LZ_1LC1RA_0RA0LC` in 18 rounds (|Q|=6, 17 negatives) — the prefix-parity k-tails can't learn.
  Made deterministic (sorted samples) so it converges regardless of hash seed. Audited: cryptids
  HOLDOUT, 243 random claims / 0 false.

## The remaining 4 all reduce to one thing — and why we did NOT rush it
All four are non-halting because a specific halt **(state,symbol)** configuration never occurs (e.g.
`1RB0LC_0LA0RA_1LA0LZ`: state C only ever reads 0, never 1 — the "0101" pattern always has a 0 left of
each 1). This is a structural invariant beyond the forward (`halt-dead`) and bounded-backward
(`halt-segment`) over-approximations — it needs a **CTL (Closed Tape Language)** decider.
**Soundness analysis (why CTL is a careful build, not a quick add):** a CTL is sound only if its
abstraction OVER-approximates reachability. A naive n-gram CTL (track the grams seen as head-window
snapshots) has a real HOLE: a tape's L-cell gram is built from cells written at DIFFERENT times, so it
need not equal any single window snapshot — so the gram set can MISS a reachable gram → the window set
misses a reachable config → halts get wrongly excluded → UNSOUND. (A small random audit can pass while
this hole hides — exactly the v3 failure mode.) The right path is the bbchallenge CTL/FAR construction
(DFA-based reachability), ported and reference-validated like `translated_cyclers` — a careful research
build, not rushed. So the suite stops at 59/63 by choice, soundly.
- The earlier "53/63" from `bouncer_prove v1/v2/v3` was **UNSOUND and is RETRACTED** — those engines
  proved the OPEN cryptid Antihydra and the HALTING cryptid Lucy's Moonlight. See `SOUNDNESS_INCIDENT.md`.

## Run it / read it
- **`python suite.py`** — the one runner: open-problem gate + 63 monsters (61/63, 0 false) + random audit.
- **`SOUNDNESS.md`** — the explicit, auditable argument for why every `NEVER_HALTS` is rigorous.
- **`SOUNDNESS_INCIDENT.md`** — why v1/v2/v3 are unsound (caught by Antihydra/Lucy).

## Soundness discipline (every decider must pass BOTH)
1. **Open-problem gate** — must return HOLDOUT on the binary BB(6) cryptids Antihydra, Space Needle,
   Lucy's Moonlight (a NEVER_HALTS there is a false proof, since their halting is open / Lucy halts).
2. **Random audit** — on thousands of random 4/5-state machines, every NEVER_HALTS is cross-checked
   against the trusted simulator; 0 false proofs required.
   (v3 passed the synthetic 3-state halter audit but died on the real cryptids — a halter audit alone
   cannot certify a non-halting prover. That is the core lesson of this work.)

## The sound tools
| file | role | status |
|---|---|---|
| `bb_sim.py` | trusted simulator (reproduces BB(5)=47,176,870 exactly) | sound, the oracle |
| `translated_cyclers.py` | faithful port of the bbchallenge S(5) reference | sound; 10,383-claim audit, 0 false |
| `wchain.py` | word-chain extraction (period-q crossing, verified on concrete copies) | sound core |
| `wsim.py` | **word-block symbolic simulator** (segment model) | **G1-validated** (1600 ops cell-for-cell) |
| `bouncer_prove_sound.py` | single-symbol-repeater bouncer prover (on the validated sim) | sound, 27/63 |
| `wbounce.py` | multi-symbol-repeater bouncer prover (on `wsim`) | sound, 31/63 |
| `bbchallenge_run.py` | runs the suite + the two gates on real machines | the harness |

Union of the two bouncer provers = **46/63**. How it is sound: each builds a symbolic config
`C(n)=[ walls + (W)^n ]` from a real record, runs the FAITHFUL simulator one period (micro-steps +
verified word-chains + boundary-bounce materialization), and declares NEVER_HALTS only on a structural
closure `C(n) => C(n+d)` (d>=1) — a genuine induction valid for all n>=base, with the trajectory at
C(base). It compares ACTUAL tape structure, never step-traces (the v3 sin).

`wsim.cross` was generalized in five sound steps (each re-validated by G1 and the cryptid gate):
basic word-chain → wiggle (step-period q != cell-advance |adv|, W' read from the net result) →
|adv| divides |W| (direction-dependent crossings, e.g. 1^n swept left as a 2-wiggle / right as a
self-loop) → boundary-bounce materialization ((W)^e = (W)^(e-1)·W, re-folded by absorb).

## QUARANTINED (do not trust)
`bouncer_prove.py` (v1), `bouncer_prove2.py` (v2), `bouncer_prove3.py` (v3), `lin_decider.py` —
all carry KNOWN-UNSOUND banners. They compared step-traces and extrapolated "forever" from one match.

## Remaining 17 — precisely scoped
- **10 counters** (binary counters, time DOUBLES per carry-out). No fixed-period closure exists; the
  recursion is at the SWEEP level (`Sweep(k)=Sweep(k-1)·pivot·Sweep(k-1)`), NOT at the carry-out level
  (`C(n)->C(n+1)` does not contain `C(m)`). So they need a **nested multi-rule induction engine**
  (sligocki "BB Counters and Proof by Induction") — prove an inner Sweep rule by induction, then the
  carry-out rule uses it. Spec transcribed in `STEP2_COUNTER_PLAN.md`; the G1-validated single-variable
  simulator `counter_prove.py` is the substrate. This is the next major (soundness-critical) build.
- **7 bouncers** with **boundary-coupled crossings**: the head's net advance comes from interacting
  with the wall/boundary, not a context-free repeater (e.g. on pure 1^n the head oscillates net-0; the
  real advance needs the boundary 0s). A context-free word-chain (the soundness basis of `wsim`) does
  not exist, so the prover correctly HOLDS OUT. These need either a wider "chain with buffer/wall"
  notion or per-machine analysis.

## After this
Plug the trusted suite into the real bbchallenge BB(6) undecided database (the index is binary +
needs the 88M seed DB). The harness `bbchallenge_run.py` already runs on standard-format machines and
reproduces BB(4)=107, BB(5)=47,176,870 on real ones.

## Complete-proof construction — capstone (2026-06-27)
The full "what remains for the complete proof" record is **`PROOF_STATUS.md`** (read first) + the new
framework **`NEW_FRAMEWORK.md`**. Summary of where the complete proof stands:
- **Reduction chain [PROVEN, machine-checked]:** non-halt ⟺ even-density ≥ 1/3 (all n; finite check + 1/6
  effective tail) ⟺ parity identity `c_n mod 2 = bit_n(8·3ⁿ) ⊕ bit_n(T_n)` ⟺ orbit Haar-genericity.
- **Gibbs–Markov proof skeleton (`gm_skeleton.py`):** COMPLETE modulo ONE line — the renewal partition,
  the GM induced map, and the Haar-level spectral gap (one-step exact) are [PROVEN]; the only [OPEN] step
  is (5) the specified orbit's Haar-genericity = single-orbit equidistribution = Mahler 3/2 / AEV 2025.
- **(5)'s handle search EXHAUSTED:** soft a.e.-specialization (computable ⇒ never random), provable-surrogate
  coupling (`coupling_brick.py`), and leading-phase conditioning (`handle_brick.py`, even-density flat) all
  closed. No auxiliary handle.
- **New framework [DESIGN]:** the self-consistent / mean-field transfer operator `ν = L_ν ν`; the complete
  proof reduces to ONE explicit inequality `‖F‖<1` (sub-criticality of the self-generation feedback).
  Empirically `‖F‖ ≈ 0.04` (deeply sub-critical, robust across correlation structures: `selfconsistent_operator.py`,
  `perturbation_F.py`). PROVING it = the closed loop = Mahler; the analytic object's exact form is open
  (`sensitivity_profile.py` was inconclusive — the smallness is a nonlinear cancellation, over-claims retracted).
- **Family theorems (`family_floor.py`):** the proven complexity floors generalize to the `⌊ac/p⌋` family.
- **DISPOSITION:** the elementary surroundings are fully crushed; the remaining (5)/`‖F‖<1` is generational
  analytic research (effective single-orbit equidistribution). Front fixed at a precisely-mapped edge.
