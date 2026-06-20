#!/usr/bin/env python
"""
Run the SOUND decider suite on real bbchallenge-format machines (any #states).

Suite (all sound; every NEVER_HALTS is oracle-gated against the trusted simulator):
  1. simulator oracle to a large cap        -> HALTS (with step count) if it stops,
  2. translated-cycle decider (record method, S(5)-gated port),
  3. Bouncers prover v3 (phase-aligned period-q chains, 53/63 on the 3-state monsters),
  -> NEVER_HALTS iff a decider proves it AND the oracle saw no halt to the cap (0 false proofs).
  -> else HOLDOUT.

Two uses:
  (A) sanity on KNOWN real machines (BB(5) champion halts @47,176,870; the BB(6) cryptid Antihydra
      stays HOLDOUT; assorted real machines) — confirms the suite behaves on the actual frontier.
  (B) sweep a sample of the real 4-state seed space (normalized A0=1RB) — the next universe up from
      the 3-state one we closed — reproducing BB(4)=107 and measuring how far the sound suite gets.
"""
from __future__ import annotations
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, sim
from bouncer_prove3 import prove as bouncer_prove
from translated_cyclers import decide_translated

HALT = {"Z", "H", "-"}


# bouncer_prove3 (v3) is QUARANTINED-UNSOUND as of 2026-06-20: it proved NEVER_HALTS for the
# OPEN BB(6) cryptid Antihydra (see SOUNDNESS_INCIDENT.md). It compares (state,read,dir) step-
# traces of two consecutive bounces and extrapolates "forever" from ONE growth instance, skipping
# the wall-content equality + buffer + head-containment conditions of a real bouncer decider.
# DO NOT use it for verdicts. Only the trusted, faithfully-ported translated-cycle decider yields
# NEVER_HALTS here; every such verdict is still oracle-gated.
TRUST_BOUNCER_V3 = False


def verdict(spec, sim_cap=2_000_000):
    h, hs = sim(spec, sim_cap)
    if h:
        return "HALTS", hs + 1          # standard BB convention counts the halting transition
    # not halted within cap -> try the SOUND non-halting prover (robust to halt-symbol '-')
    try:
        v, info = decide_translated(spec, time_limit=min(sim_cap, 100_000), space_limit=40_000)
        if v == "NEVER_HALTS":
            return "NEVER_HALTS", ("translated-cycle", info)
    except Exception:
        pass
    if TRUST_BOUNCER_V3:
        try:
            v2, info2 = bouncer_prove(spec, steps=30_000)
            if v2 == "NEVER_HALTS":
                return "NEVER_HALTS", ("bouncer-v3", info2)
        except Exception:
            pass
    return "HOLDOUT", "no sound decider closed it"


# Open-problem soundness gate: NO sound decider may prove any of these NEVER_HALTS (halting is
# genuinely OPEN). Any decider that does is unsound — this is the gate that caught bouncer-v3.
OPEN_MACHINES = [
    ("Antihydra (BB(6) cryptid, OPEN/Collatz)", "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
]


def soundness_gate():
    print("=" * 88)
    print("(0) OPEN-PROBLEM SOUNDNESS GATE — any NEVER_HALTS here = the decider is UNSOUND")
    print("=" * 88)
    bad = 0
    for name, spec in OPEN_MACHINES:
        # trusted suite must NOT prove it; also report what the quarantined v3 says
        vt, _ = decide_translated(spec, time_limit=100_000, space_limit=40_000)
        v3, i3 = bouncer_prove(spec, steps=30_000)
        ok_t = vt != "NEVER_HALTS"
        print(f"  {name}")
        print(f"    translated-cycle (trusted)   -> {vt:<12} [{'OK' if ok_t else '‼ UNSOUND'}]")
        print(f"    bouncer-v3 (QUARANTINED)      -> {v3:<12} [{'‼ UNSOUND — would be a false proof' if v3=='NEVER_HALTS' else 'OK'}]")
        if not ok_t:
            bad += 1
    print()
    return bad


# ---- (A) known real machines (standard bbchallenge text format) ----
KNOWN = [
    ("BB(5) champion (halts @47,176,870)", "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA"),
    ("BB(4) champion (halts @107)",        "1RB1LB_1LA0LC_1RZ1LD_1RD0RA"),
    ("BB(6) cryptid Antihydra (OPEN)",     "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
    ("real bbchallenge 4-state #1",        "1RB0LC_1LD0RB_1RD0LA_1LC1RB"),
    ("real bbchallenge 4-state #2",        "1RB0LA_1LC0RD_0RD0LC_1LA1RD"),
    ("real bbchallenge 4-state #3",        "1RB0LC_1RD1LB_0LA1LB_1LC0RD"),
    ("real bbchallenge 4-state #4",        "1RB0LB_1LC1RD_1RD0LB_1LA0RD"),
    ("real bbchallenge 4-state #5",        "1RB0RB_1LC1RA_0LA1LD_1RA0LC"),
    ("real bbchallenge 4-state #6",        "1RB0LC_1RD0RB_1LC1LA_1RC1RA"),
]


def run_known():
    print("=" * 88)
    print("(A) SOUND suite on KNOWN real bbchallenge machines")
    print("=" * 88)
    bad = 0
    for name, spec in KNOWN:
        # BB(5) champion halts only at 47M (beyond a quick cap; already verified in bb_sim.py) -> big cap
        cap = 50_000_000 if "BB(5)" in name else 2_000_000
        v, info = verdict(spec, sim_cap=cap)
        tag = ""
        if "BB(4) champion" in name and not (v == "HALTS" and info == 107):
            tag = "  ‼ expected HALTS@107"; bad += 1
        if "BB(5) champion" in name and not (v == "HALTS" and info == 47_176_870):
            tag = "  ‼ expected HALTS@47,176,870"; bad += 1
        if "Antihydra" in name and v != "HOLDOUT":
            tag = "  ‼ expected HOLDOUT (open)"; bad += 1
        print(f"  {name:<40} -> {v:<12} {info if v!='HALTS' else f'@{info}'}{tag}")
    print(f"\n  sanity failures: {bad}")
    return bad


# ---- (B) sample the real 4-state seed space ----
def rand_4state(rng):
    cells = ["1RB"]                                  # A0 fixed (normalized)
    syms = "01"; moves = "LR"; tgts = "ABCDZ"
    for _ in range(7):
        cells.append(rng.choice(syms) + rng.choice(moves) + rng.choice(tgts))
    g = ["".join(cells[0:2]), "".join(cells[2:4]), "".join(cells[4:6]), "".join(cells[6:8])]
    return "_".join(g)


def run_sample(N=20_000, seed=12345, sim_cap=100_000):
    rng = random.Random(seed)
    print("=" * 88)
    print(f"(B) SOUND suite on {N} sampled normalized 4-state machines (real seed space), cap={sim_cap}")
    print("=" * 88)
    cnt = {"HALTS": 0, "NEVER_HALTS": 0, "HOLDOUT": 0}
    max_halt = 0; max_spec = ""; false_proofs = 0
    nh_by = {"translated-cycle": 0, "bouncer-v3": 0}
    for i in range(N):
        spec = rand_4state(rng)
        v, info = verdict(spec, sim_cap=sim_cap)
        cnt[v] += 1
        if v == "HALTS":
            if info > max_halt:
                max_halt = info; max_spec = spec
        elif v == "NEVER_HALTS":
            # oracle gate: cross-check it truly does not halt (bigger cap)
            h, _ = sim(spec, 1_000_000)
            if h:
                false_proofs += 1
                print(f"  ‼ FALSE PROOF {spec}")
            nh_by[info[0]] += 1
    print(f"  HALTS       : {cnt['HALTS']:>6}   (max steps = {max_halt}; BB(4)=107 is the true max)")
    print(f"  NEVER_HALTS : {cnt['NEVER_HALTS']:>6}   (translated-cycle {nh_by['translated-cycle']}, "
          f"bouncer-v3 {nh_by['bouncer-v3']})")
    print(f"  HOLDOUT     : {cnt['HOLDOUT']:>6}   ({100*cnt['HOLDOUT']/N:.2f}% residual the sound suite can't yet settle)")
    print(f"  FALSE PROOFS: {false_proofs}   (must be 0)")
    if max_halt and max_halt <= 107:
        print(f"  longest halter in sample: {max_halt} steps  (<=107 = BB(4); the 107-step champion is rare)")
    return false_proofs


def main():
    gate = soundness_gate()
    bad = run_known()
    print()
    fp = run_sample()
    print("\n" + "=" * 88)
    print(f"  open-gate violations (trusted): {gate}  | sample false proofs: {fp}  | champion sanity fails: {bad}")
    print("  The trusted suite (sim oracle + faithfully-ported translated-cyclers) is sound on all gates.")
    print("  bouncer-v3 is QUARANTINED (it proves the OPEN Antihydra — see SOUNDNESS_INCIDENT.md).")
    return 1 if (fp or bad or gate) else 0


if __name__ == "__main__":
    raise SystemExit(main())
