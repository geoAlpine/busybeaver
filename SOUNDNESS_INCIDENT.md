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
