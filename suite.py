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
from halt_segment import halt_segment

HERE = os.path.dirname(__file__)

# Real BB(6) frontier machines from the bbchallenge wiki (verbatim): the Champion, the named Cryptids
# (Open or provably Halting), and a top halter. Halting is OPEN or known — so NO sound decider may
# ever return NEVER_HALTS on any of them. This is the permanent BB(6)-frontier soundness gate.
CRYPTIDS = [
    ("Antihydra",        "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
    ("Space Needle",     "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"),
    ("Lucy's Moonlight", "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"),
    ("BB6 champion",     "1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE"),
    ("cryptid o2",       "1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA"),
    ("cryptid o3",       "1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC"),
    ("cryptid o4",       "1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---"),
    ("cryptid o5",       "1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB"),
    ("cryptid o7",       "1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"),
    ("cryptid o8",       "1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE"),
    ("cryptid o10",      "1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC"),
    ("cryptid o11",      "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF"),
    ("cryptid o12",      "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB"),
    ("cryptid o13",      "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA"),
    ("cryptid o14",      "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE"),
    ("cryptid o15",      "1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"),
    ("cryptid o16",      "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE"),
    ("cryptid o17",      "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"),
    ("cryptid o18",      "1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"),
]
HALTERS = [("BB(2)", "1RB1LB_1LA1RZ"), ("BB(3)", "1RB1RZ_1LB0RC_1LC1LA"),
           ("BB(4)", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]


HALT_SYMS = {"Z", "H", "-"}


def halt_unreachable(spec):
    """SOUND trivial non-halt: the machine never halts iff every halting transition is DEAD (its
    (state,symbol) configuration never occurs). We decide deadness with a sound abstraction:
      - states reachable from A are `live`; a halt in a non-live state is dead (never entered);
      - a state s!=A is live only if some transition targets it (`re-entered`), so it may read 0 or 1
        (conservative: a halt there is treated as possibly-live);
      - the START state A, if NOT re-entered, occurs ONLY at the start reading the blank 0 — so a halt
        on A,1 is DEAD (A,1 never executes), while A,0 is live.
    Returns True only if ALL halts are dead. (Generalises the bare reachability check: it additionally
    kills the very common 'halt on symbol 1 in the never-re-entered start state' pattern.)"""
    M = parse(spec)
    live = {"A"}; stack = ["A"]
    while stack:
        s = stack.pop()
        for sym in (0, 1):
            tr = M[s][sym]
            if tr is None or tr[2] in HALT_SYMS:
                continue
            if tr[2] not in live:
                live.add(tr[2]); stack.append(tr[2])
    reentered = {tr[2] for s in live for sym in (0, 1)
                 if (tr := M[s][sym]) and tr[2] not in HALT_SYMS}
    for s in live:
        for sym in (0, 1):
            tr = M[s][sym]
            if not (tr is None or tr[2] in HALT_SYMS):
                continue                             # not a halt transition
            if s == "A" and s not in reentered:
                if sym == 0:
                    return False                     # A,0 fires at the start (head reads blank 0)
            elif s in reentered:
                return False                         # s re-entered -> may read sym -> halt may fire
    return True


def verdict(spec, sim_cap=1_000_000, bsteps=15_000, bmacro=2000):
    """HALTS / NEVER_HALTS / HOLDOUT via the trusted suite. Returns (verdict, which)."""
    h, hs = sim(spec, sim_cap)
    if h:
        return "HALTS", ("sim", hs + 1)
    if halt_unreachable(spec):
        return "NEVER_HALTS", ("halt-unreachable",)
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
    try:
        if halt_segment(spec, W=10) is True:
            return "NEVER_HALTS", ("halt-segment",)
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
    by = {"halt-unreachable": 0, "translated-cycle": 0, "bouncer-single": 0, "bouncer-word": 0, "halt-segment": 0}
    proven = 0; false_proofs = 0; held = []
    for spec in reps:
        v, w = verdict(spec)
        if v == "NEVER_HALTS":
            h, _ = sim(spec, 2_000_000)
            if h:
                false_proofs += 1; print(f"  ‼ FALSE PROOF {spec}")
            else:
                proven += 1; by[w[0]] = by.get(w[0], 0) + 1
        elif v == "HOLDOUT":
            held.append(spec)
    print(f"  PROVEN never-halt: {proven}/{len(reps)}  "
          f"(unreachable {by['halt-unreachable']}, translated {by['translated-cycle']}, single {by['bouncer-single']}, word {by['bouncer-word']}, segment {by['halt-segment']})")
    print(f"  HOLDOUT          : {len(held)}  (the ~10 counters + ~7 boundary-coupled bouncers)")
    print(f"  FALSE PROOFS     : {false_proofs}   (MUST be 0)")
    return false_proofs


def random_audit(N=5000, seed=1, check_cap=2_000_000):
    print("=" * 78)
    print(f"(3) RANDOM SOUNDNESS AUDIT — {N} machines, every NEVER_HALTS cross-checked")
    print("=" * 78)
    rng = random.Random(seed)
    nh = 0; checked = 0; fp = []
    by = {"halt-unreachable": 0, "translated-cycle": 0, "bouncer-single": 0, "bouncer-word": 0, "halt-segment": 0}
    for i in range(N):
        if i and i % 1000 == 0:
            print(f"  ...{i}/{N}  NEVER_HALTS={nh}  false={len(fp)}", flush=True)
        spec = rand_machine(rng, rng.choice([4, 5]))
        v, w = verdict(spec, sim_cap=500_000, bsteps=8000, bmacro=1200)
        if v == "NEVER_HALTS":
            nh += 1; by[w[0]] = by.get(w[0], 0) + 1
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
