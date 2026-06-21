#!/usr/bin/env python
"""
SOUND decider suite — single regression runner & soundness gate.

Trusted deciders ONLY (the quarantined bouncer_prove v1/v2/v3 are excluded):
  - translated_cyclers      (faithful port of the bbchallenge S(5) reference)
  - bouncer_prove_sound     (single-symbol-repeater bouncers, on the G1-validated symbolic sim)
  - wbounce                 (multi-symbol-repeater bouncers, on the G1-validated word-block sim)

Every NEVER_HALTS is cross-checked against the trusted simulator (0 false proofs is the bar).
Run:  python suite.py            (gates + 63 monsters + a random audit)
      python suite.py 20000      (random audit of N machines)
"""
from __future__ import annotations
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, sim
from translated_cyclers import decide_translated
from bouncer_prove_sound import prove as ss_prove
from wbounce import prove as wb_prove

HERE = os.path.dirname(__file__)

# binary BB(6) cryptids: halting is OPEN or (Lucy) provably late — no sound decider may prove these
CRYPTIDS = [
    ("Antihydra",        "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
    ("Space Needle",     "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"),
    ("Lucy's Moonlight", "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"),
]
HALTERS = [("BB(2)", "1RB1LB_1LA1RZ"), ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA"),
           ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]


def verdict(spec, sim_cap=1_000_000, bsteps=15_000, bmacro=2000):
    """HALTS / NEVER_HALTS / HOLDOUT via the trusted suite. Returns (verdict, which)."""
    h, hs = sim(spec, sim_cap)
    if h:
        return "HALTS", ("sim", hs + 1)
    try:
        if decide_translated(spec, time_limit=min(sim_cap, 100_000), space_limit=40_000)[0] == "NEVER_HALTS":
            return "NEVER_HALTS", ("translated-cycle",)
    except Exception:
        pass
    try:
        if ss_prove(spec, steps=bsteps, max_macro=bmacro)[0] == "NEVER_HALTS":
            return "NEVER_HALTS", ("bouncer-single",)
    except Exception:
        pass
    try:
        if wb_prove(spec, steps=bsteps, max_macro=bmacro)[0] == "NEVER_HALTS":
            return "NEVER_HALTS", ("bouncer-word",)
    except Exception:
        pass
    return "HOLDOUT", ()


def rand_machine(rng, n):
    cells = ["1RB"]; tg = "ABCDEF"[:n] + "Z"
    for _ in range(2 * n - 1):
        cells.append(rng.choice("01") + rng.choice("LR") + rng.choice(tg))
    return "_".join("".join(cells[2 * i:2 * i + 2]) for i in range(n))


def gate():
    print("=" * 78)
    print("(0) OPEN-PROBLEM GATE — no trusted decider may prove these (false proof => UNSOUND)")
    print("=" * 78)
    bad = 0
    for name, spec in CRYPTIDS:
        v, _ = verdict(spec, sim_cap=2_000_000)
        ok = v != "NEVER_HALTS"
        if not ok:
            bad += 1
        print(f"  {name:<18} -> {v:<12} [{'OK' if ok else '‼ UNSOUND'}]")
    print("=" * 78)
    print("(1) KNOWN HALTERS — must not be proven NEVER_HALTS")
    for name, spec in HALTERS:
        v, w = verdict(spec)
        flag = "‼ UNSOUND" if v == "NEVER_HALTS" else "OK"
        print(f"  {name:>6} -> {v:<12} {w}  [{flag}]")
        if v == "NEVER_HALTS":
            bad += 1
    return bad


def monsters():
    reps = [l.strip() for l in open(os.path.join(HERE, "holdouts3_reps.txt")) if l.strip()]
    print("=" * 78)
    print(f"(2) THE {len(reps)} THREE-STATE MONSTERS")
    print("=" * 78)
    by = {"translated-cycle": 0, "bouncer-single": 0, "bouncer-word": 0}
    proven = 0; false_proofs = 0; held = []
    for spec in reps:
        v, w = verdict(spec)
        if v == "NEVER_HALTS":
            h, _ = sim(spec, 2_000_000)
            if h:
                false_proofs += 1; print(f"  ‼ FALSE PROOF {spec}")
            else:
                proven += 1; by[w[0]] += 1
        elif v == "HOLDOUT":
            held.append(spec)
    print(f"  PROVEN never-halt: {proven}/{len(reps)}  "
          f"(translated {by['translated-cycle']}, single {by['bouncer-single']}, word {by['bouncer-word']})")
    print(f"  HOLDOUT          : {len(held)}  (the ~10 counters + ~7 boundary-coupled bouncers)")
    print(f"  FALSE PROOFS     : {false_proofs}   (MUST be 0)")
    return false_proofs


def random_audit(N=5000, seed=1, check_cap=2_000_000):
    print("=" * 78)
    print(f"(3) RANDOM SOUNDNESS AUDIT — {N} machines, every NEVER_HALTS cross-checked")
    print("=" * 78)
    rng = random.Random(seed)
    nh = 0; checked = 0; fp = []
    by = {"translated-cycle": 0, "bouncer-single": 0, "bouncer-word": 0}
    for i in range(N):
        if i and i % 1000 == 0:
            print(f"  ...{i}/{N}  NEVER_HALTS={nh}  false={len(fp)}", flush=True)
        spec = rand_machine(rng, rng.choice([4, 5]))
        v, w = verdict(spec, sim_cap=500_000, bsteps=8000, bmacro=1200)
        if v == "NEVER_HALTS":
            nh += 1; by[w[0]] += 1
            h, hs = sim(spec, check_cap); checked += 1
            if h:
                fp.append((spec, hs + 1)); print(f"  ‼ FALSE PROOF {spec} HALTS@{hs + 1}", flush=True)
    print(f"  NEVER_HALTS claims: {nh}  (translated {by['translated-cycle']}, single "
          f"{by['bouncer-single']}, word {by['bouncer-word']})")
    print(f"  cross-checked: {checked}   FALSE PROOFS: {len(fp)}   -> "
          f"{'SOUND on this audit' if not fp else 'UNSOUND ‼'}")
    return len(fp)


def main():
    if len(sys.argv) > 1:
        return 1 if random_audit(int(sys.argv[1])) else 0
    g = gate(); print(); f = monsters(); print(); a = random_audit(2000)
    print("\n" + "=" * 78)
    bad = g + f + a
    print(f"  gate+halter violations: {g}   monster false proofs: {f}   audit false proofs: {a}")
    print(f"  SUITE {'SOUND (0 false proofs across all checks)' if bad == 0 else 'UNSOUND ‼'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
