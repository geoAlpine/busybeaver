# SOUNDNESS INCIDENT — bouncer_prove (v1/v2/v3) is UNSOUND. Caught by Antihydra. 2026-06-20.

## Verdict
`bouncer_prove.py` (v1), `bouncer_prove2.py` (v2), and `bouncer_prove3.py` (v3) are **KNOWN-UNSOUND
proof engines. DO NOT trust their `NEVER_HALTS` outputs as proofs.** They are quarantined, exactly
like `lin_decider.py` before them.

## How it was caught (the real-bbchallenge test earned its keep)
We pointed the suite at real bbchallenge machines (`bbchallenge_run.py`). On the **Antihydra** machine
`1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` — the canonical BB(6) **Cryptid**, the *smallest open
problem in mathematics on the BB scale* (halting ⇔ a Collatz-like conjecture; halting probability
≈ 4.84×10⁻²²⁴³⁹⁴³⁹⁵ but **UNPROVEN**) — **v3 returned `NEVER_HALTS`.**

A valid proof that Antihydra never halts would resolve a famous open problem. v3 did not do that;
**v3's proof is invalid.** No simulation oracle can flag this (Antihydra genuinely never halts within
any feasible cap), which is precisely why the synthetic 3-state halter audit (0 false proofs on
BB2/BB3/BB4) MISSED it. The open-problem machine is the oracle the synthetic set could not be.

**Ironclad confirmation (a false proof on a machine that PROVABLY HALTS).** Hardening the gate with
more binary BB(6) cryptids exposed the cleaner counterexample: on **Lucy's Moonlight**
`1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA` — a cryptid the community has shown **HALTS** (after
astronomically many steps) — **v3 returns `NEVER_HALTS`.** This is not "unprovable", it is **flatly
false**: v3 claims a halting machine never halts. Two independent classes of evidence now: (1) v3
"proves" the OPEN Antihydra; (2) v3 "proves" the HALTING Lucy's Moonlight never halts.

**Trusted decider passed the hardened gate AND a random audit.** The faithfully-ported
`translated_cyclers` returns HOLDOUT on all three binary cryptids tested (Antihydra, Space Needle,
Lucy's Moonlight) — 0 gate violations — AND a random audit of 20,000 four/five-state machines
produced **10,383 NEVER_HALTS claims, every one cross-checked against the simulator, 0 false proofs**
(`bbchallenge_run.audit_translated`). It also decides 0/63 of the hard 3-state monsters — the honest
current ceiling of the trusted suite: it handles cyclers, but the bouncers/counters need a real
(not-yet-built) sound decider. Contrast with v3: v3 *also* passed the 3-state halter audit, then died
on the first real cryptids. translated_cyclers passes both the random audit and the cryptid gate.

## The bug (why it's unsound)
v3 takes the last three tape-extreme records on a side that share a state (P0,P1,P2), tokenizes the
two bounce **step-traces** `(state, read, dir)` into CHAIN (period-q repeats) + WALL tokens, and
declares `NEVER_HALTS` if the two token sequences match with ≥1 CHAIN grown. **It extrapolates
"repeats forever" from a SINGLE growth instance, comparing only step-traces — never the actual tape
/ wall contents.** It omits every soundness condition a real bouncer decider requires (and that our
own `STEP2_PLAN.md` lists): wall-word equality across bounces, a buffer, `len(buf)==len(buf')`, and
the head-containment condition (head leaves the word+buffer window only on the last step). A machine
whose bounces are *locally* trace-identical but *globally* governed by a counter (Antihydra) is
therefore falsely "proven." Two configurations with the same `(state,read,dir)` trace but different
hidden tape structure are conflated.

## What this does and does NOT invalidate
- **Invalidated:** the claim "v2/v3 PROVES 40/53 of the monsters never-halt." Those are NOT sound
  proofs. (The verdicts are *probably* correct — those 53 are genuine bouncers by independent STEP-1
  measurement: width ∝ √steps, cross-confirmed by `counter_structure.py` — but they are **not proven**
  by these engines.)
- **Still sound (unaffected):**
  - `bb_sim.py` — verified simulator (reproduces BB(5) to the exact step).
  - `translated_cyclers.py` — a *faithful port* of the bbchallenge S(5)-gated reference; it returns
    HOLDOUT on Antihydra (behaves correctly) and is the only trusted non-halting decider in the suite.
  - The 2-state and 3-state **universe closures** (`enumerate2.py`/`enumerate3.py`) — they used only
    trivial + exact-repeat + translated-cycle, NOT the bouncer engines.
  - All STEP-1 detection/structure measurements (`bouncers.py`, `classify_monsters.py`,
    `counter_analyze.py`, `counter_structure.py`) — sound by construction (measurement, no claims).
  - `counter_prove.py` G1 — a validated symbolic simulator (no halting claims).

## Standing rule added
`bbchallenge_run.py` now runs an **OPEN-PROBLEM SOUNDNESS GATE**: no decider may return `NEVER_HALTS`
on Antihydra (or any listed open machine). This gate is permanent. Any future proof engine must pass
it before any `NEVER_HALTS` output is trusted.

## The lesson (the same one, sharper)
This is the lin_decider lesson again, one level up: **a synthetic audit of known halters cannot
certify a non-halting prover** — it can only catch false proofs on machines that *halt*. To trust a
non-halting decider you must also test it against machines that *provably cannot be proven*
(open/cryptid machines) and against a faithful reference. We shipped "40/53 proven" too confidently;
the real frontier corrected us within minutes. Build the SOUND bouncer decider per `STEP2_PLAN.md`
(walls/repeaters/buffer/containment), gate it on Antihydra, and only then re-claim proofs.

---

# INCIDENT 2 — wbounce/wbounce2 wsim-chain unfaithfulness. Caught by a REAL BB(6) holdout. 2026-06-22.

## What happened
We ran the suite on the real bbchallenge **BB(6) holdouts** list (1104 machines,
`wiki.bbchallenge.org`). `wbounce2` returned a lone `NEVER_HALTS` on
`1RB1LA_0LC0RE_1LD1LB_1RE1LF_1RC0RA_0RC---`. On rigorous concrete re-verification this was a
**FALSE PROOF**: `wbounce2` claimed the bouncer rule `C(n) -> C(n+1)` (repeater `W=101`, base `n=1`),
but the real machine maps `C(1) -> C(6)` (it never visits `C(2)..C(5)`). The symbolic `wsim`
simulation said macro-9 reaches `C(2)`; the trusted simulator reaches `C(6)`.

## Root cause
`wsim`'s **word-chain macro-steps (CHAINR/CHAINL) extrapolate a repeater `(W)^n` as if `n` is large**,
but the closure was asserted for `n >= base` with `base = 1` — a regime where the chain's boundary
behaviour is wrong. So `wsim` was unfaithful at small `n` on this 6-state structure; the G1 validation
(on other machines) had not exercised this case. This is the v3 lesson at the `wsim` layer: a symbolic
engine that is "validated" on a sample can still be unfaithful on an unseen structure.

## Blast radius — CHECKED, and it is ZERO for the 63 monsters
Every one of the **42 monster proofs `wbounce2` produces was concretely re-verified**: the real machine
really does map `C(base+j) -> C(base+j+d)` (exact, no halt) for `j = 0,1`. All 42 hold. `wbounce` (word)
did not false-prove the BB(6) machine either. **So 63/63 was never compromised** — the only false proof
was on the new BB(6) machine, which we caught before claiming anything.

## Fix — concrete-induction gate (`wbounce2.concrete_closure_ok`)
A symbolic `wsim` closure `C(n) => C(n+d)` is now trusted ONLY if the TRUSTED simulator confirms the
real machine maps `C(base+j) -> C(base+j+d)`, exactly and without halting, for `j = 0,1,2`. Added to
both `wbounce2` and `wbounce`. Result: the BB(6) false proof is rejected (-> HOLDOUT), all 42 valid
monster proofs are kept, cryptids still HOLDOUT, suite is **63/63, 0 false**.

## The lesson (again, sharper)
A "G1-validated" symbolic simulator is still only validated on its sample — real data outside the
sample can expose unfaithfulness. The durable defence is to **cross-check every symbolic proof against
the trusted simulator on concrete instances** (the concrete-induction gate), not to trust the symbolic
engine alone. Real BB(6) data earned its keep: it caught a latent false-proof generator that thousands
of synthetic-audit machines did not.

## ROOT FIX (2026-06-22, after the concrete-induction gate)
The gate above is a safety net; the root cause is now fixed in `wsim.cross`. The old chain extracted
the per-copy behaviour in a synthetic **all-W buffer** (K + 2·BUF copies of W), so the head could read
buffer-W cells during a crossing — masking dependence on whatever actually bounds the repeater. New
`cross`/`chain_cross`/`_sim_cross`: cross `(W)^K` with **NO buffer and head-containment** — the head
must enter at the near boundary in `state`, read ONLY the K copies, and exit at the far boundary in
`state`; reading any neighbour cell (outside `[0, K·|W|)`) returns STUCK. Uniformity is checked across
K=2,3,4 (same `W'`, same exit state, steps linear through the origin). A contained, uniform crossing is
sound for any m≥1 — the rigorous version of what the chain docstring always claimed.
**Verified:** wsim G1 self-validation still 1600 ops cell-for-cell; the BB(6) chain is now rejected at
the wsim level; in the `exps_valid` regime wsim matches the trusted sim cell-for-cell; full suite still
**63/63, 0 false**, coverage held (stricter chain dropped a few word/wall proofs; `halt_segment`+FAR
absorbed them). Both layers (root fix + concrete gate) are kept.
