# Busy Beaver — status (2026-06-21)

Deciding the **63 distinct 3-state "monster" holdouts** (`holdouts3_reps.txt`) — the hard residual the
trivial + cycler deciders leave behind. Every claim here is SOUND: machine-checked and gated.

## Headline
- **46 / 63 monsters PROVEN never-halt — SOUNDLY** (0 false proofs).
- Remaining 17 = **10 counters** (need nested induction) + **7 bouncers** (boundary-coupled crossings).
- The earlier "53/63" from `bouncer_prove v1/v2/v3` was **UNSOUND and is RETRACTED** — those engines
  proved the OPEN cryptid Antihydra and the HALTING cryptid Lucy's Moonlight. See `SOUNDNESS_INCIDENT.md`.

## Run it / read it
- **`python suite.py`** — the one runner: open-problem gate + 63 monsters (46/63, 0 false) + random audit.
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
