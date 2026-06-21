# Why the trusted suite is SOUND — the positive argument

The counterpart to `SOUNDNESS_INCIDENT.md` (which explains why `bouncer_prove v1/v2/v3` are UNSOUND).
This file states, explicitly and auditably, why every `NEVER_HALTS` the trusted suite emits is rigorous.
Trusted deciders: `translated_cyclers`, `bouncer_prove_sound`, `wbounce` (run by `suite.py`).

## 0. The oracle: `bb_sim`
A literal Turing-machine executor. **Verified** by reproducing BB(2)=6, BB(3)=21, BB(4)=107, and the
2024 world result BB(5)=47,176,870 to the exact step. Every `NEVER_HALTS` below is additionally
cross-checked against it (a machine flagged non-halting must not halt within a large cap).

## 1. `translated_cyclers` — translated cycles
A faithful port of the bbchallenge S(5)-gated reference decider (`decider-translated-cyclers`). It
snapshots the configuration only at new tape extremes, buckets by (side, state, read), and declares
non-halting only when two snapshots are head-relative identical over exactly the cells visited since
the earlier one (the proof's "distance L"). A matched pair is a genuine translated cycle: the machine
reproduces its configuration shifted in space, hence loops forever. Audited: 0 false proofs on the
known halters and (this session) 10,383 NEVER_HALTS claims on random machines, all cross-checked.

## 2. The symbolic simulators are FAITHFUL (the "G1" guarantee)
`wsim` (word-block) and `counter_prove`/`counter_induct` (single-symbol) represent the tape with
run-length blocks carrying a symbolic exponent `n`, and step by: faithful micro-steps; exact
self-loop / period-q CHAIN steps (crossing a uniform run `b^e` = exactly the same real steps); and
boundary-bounce materialisation (`(W)^e = (W)^(e-1)·W`, sound re-bracketing). **G1 validation**:
instantiate a symbolic config at several concrete `n`, run the symbolic sim and the trusted simulator
in LOCKSTEP, compare cell-for-cell. Passing (wsim: 1600 ops; counter from blank: 300; counter C(n):
632) means **a symbolic derivation IS a faithful simulation** for every `n` in the valid regime.
Two real bugs were caught BY this lockstep (a CHAIN cost off-by-one; `compress` relocating the head
via absolute positions that depend on `n`) — and a tempting but FALSE "clean recursion" was rejected
when lockstep showed the symbolic sim diverging from reality. This is the load-bearing guarantee.

## 3. `bouncer_prove_sound` / `wbounce` — bouncers, by induction
From a real tape-extreme record, build the symbolic configuration `C(n) = [walls · (W)^n · walls]`
where `n` is the repeater's length at that record (= the base value). Simulate ONE period with the
G1-faithful simulator. Emit `NEVER_HALTS` **only** on a structural CLOSURE: the config returns to the
START form with the repeater exponent strictly larger, `C(n) ⇒ C(n+d)` with `d ≥ 1`, comparing the
ACTUAL block structure (not step-traces). Soundness:
- The derivation `C(n) ⇒ C(n+d)` uses only faithful steps, so it holds for the symbolic `n`.
- Exponents are `a·n + b` with `a ≥ 0`, hence monotonic; valid at `n = base` ⇒ valid for all `n ≥ base`
  (`exps_valid` is checked).
- The real trajectory IS at `C(base)` (the record is on the path from the blank tape).
- Therefore `C(base) ⇒ C(base+d) ⇒ C(base+2d) ⇒ …` forever, tape growing, no halt ⇒ never halts.
This is a genuine induction, not an extrapolation. It compares configurations, which is exactly the
hole that made v3 unsound (v3 compared `(state,read,dir)` step-traces and extrapolated from ONE match —
so it "proved" the OPEN Antihydra and the HALTING Lucy's Moonlight).

## 4. The gates (defence in depth) — `suite.py`
Even granting 1–3, every verdict passes two independent gates:
- **Open-problem gate**: the binary BB(6) cryptids Antihydra, Space Needle, Lucy's Moonlight must all
  be HOLDOUT. A `NEVER_HALTS` there is a false proof by definition (their halting is open, or — Lucy —
  provably halts). This is the gate that exposed v3.
- **Random audit**: thousands of random 4/5-state machines; every `NEVER_HALTS` is cross-checked
  against the oracle to a large cap. 0 false proofs required.
A halter audit alone cannot certify a non-halting prover (it only catches false proofs on machines
that HALT) — which is why the cryptid gate is mandatory, and why both are run together.

## 5. Honest scope
The suite proves **46/63** of the three-state monsters. The remaining **17 are HOLDOUT, never falsely
proven**: ~10 binary counters (need nested induction — `counter_induct.py` has the validated substrate
and the decoded self-recursive rule `D(k)→D(k+1)`, but the proof engine is WIP and HARD-WIRED never to
emit a trusted proof) and ~7 boundary-coupled bouncers (context-dependent crossings beyond the current
chain model). HOLDOUT means "not decided", never a halting claim. No result here depends on the
quarantined v1/v2/v3.
