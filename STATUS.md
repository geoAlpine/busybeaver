# Busy Beaver — status (2026-06-21)

Deciding the **63 distinct 3-state "monster" holdouts** (`holdouts3_reps.txt`) — the hard residual the
trivial + cycler deciders leave behind. Every claim here is SOUND: machine-checked and gated.

> **Big-picture map / consolidation: see `MAP.md`** (BB(6)-goal oriented, the single source of truth).

## Headline
- **61 / 63 monsters PROVEN never-halt — SOUNDLY** (0 false proofs): **23 halt-dead** ((state,symbol)
  of the halt can never occur), **14 single-symbol + 16 word-repeater + 3 wall-repeater bouncers**,
  **5 halt-segment** (bounded backward reachability: halt not backward-reachable to the blank start).
- The 2 boundary-coupled bouncers (`1RB0LC_0LA0RA_1LA0LZ`, `1RB0LZ_1LC0RA_0RB0LB`) are now PROVEN by
  **`wbounce2.py`**: it finds a period-q repeater wedged between fixed walls via a two-record diff
  (`x1 == (W)^m + x0`, repeater grows at the head end), builds `C(n)=[head (W)^n wall]`, and closes
  `C(n)=>C(n+d)` on the G1-validated `wsim`. A **faithfulness gate** (`cfg_to_tape(C(base))` must equal
  the real record) blocks closures on configs the machine never reaches — the key soundness link.
- Remaining **2** = the genuinely-hard residual: 2 live-halt **binary counters**
  (`1RB0LZ_1LC1RA_0RA0LC`, `1RB1LC_0LA0RB_1LA0LZ`). Structure fully cracked (`far.py` analysis):
  C-turn family `0 1^(2m) -> 0 1^(2m+2)`, time **doubles** (gaps `2^(k+4)-2`); single-pass symbolic
  closure is provably impossible (the `0^n` carry materialises a size-n counter block). Non-halt reason
  = "state A never reads 1" (machine 1), a REGULAR invariant — but a non-local one.

## FAR engine (the route to the last 2) — in progress, soundness-first
`far.py` (LAYER 0, **validated** cell-for-cell vs the trusted sim, 5 machines x 4000 steps) gives a
config-string single-step rewrite. `far_dfa.py` builds an m-gram invariant `L` and **verifies**
soundly: start in L, closure `succ(L) subset L` (reduced to per-context suffix-language inclusions,
no transducer), no halt in L. The verifier correctly HOLDS OUT Antihydra/Lucy and says HALTS on the
BB4 halter. **Finding (computed, fundamental): pure m-gram `L` is too weak** — the binary counter's
carry is non-local. Witness: `L` wrongly accepts `001B1001` (a single 1 before B, not boundary-
anchored); its successor escapes `L`. The TRUE reachable invariant (read off the data): B-configs are
`1^(odd) B ...` with the 1-run **anchored at the left boundary** (run lengths 1,3,5,...). So the
finder needs a small **memory-DFA** (boundary-anchored + parity), which is exactly real FAR.
**Next:** build/verify that memory-DFA finder, THEN audit the verifier on the cryptid gate + random
machines (0 false) before claiming any 62/63. Do NOT trust a NEVER_HALTS from `far_dfa` until audited.

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
