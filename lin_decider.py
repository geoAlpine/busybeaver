#!/usr/bin/env python
"""
Lin-Rado translated-cycle decider — the second tool, kills the drifting holdouts.

The first decider (decider.py) only catches *stationary* cyclers: the configuration
must repeat EXACTLY. Drifting machines (e.g. 1RA1RA, which marches right forever)
never repeat exactly, so they slipped through as HOLDOUT.

Lin & Rado (1965) — the method that settled BB(3) and BB(4) — catches *translated*
cycles. A machine never halts if there are two times t' < t with:
  - the same state, and
  - the tape, over the segment the head SWEPT during (t', t], is identical to the
    tape one period earlier SHIFTED by the head's net displacement d = head_t - head_t'.
If so, the swept segment regenerates itself shifted by d, forever. This is a sound
proof of non-halting from finite observation — the exact "certify an infinite property"
move (same instinct as the quantum genuineness limit theorem), now for the halting
problem.

Usage:  python3 lin_decider.py
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bb_sim import parse


def decide_lin(spec: str, max_steps: int = 20_000, max_period: int = 2_000):
    """('HALTS',k) | ('NEVER_HALTS', (t_prime, period, drift)) | ('HOLDOUT', max_steps)."""
    machine = parse(spec)
    tape: dict[int, int] = {}
    head, state = 0, "A"
    HALT = {"Z", "H", "-"}

    # history[t] = (state, head, frozen tape snapshot as dict), plus swept-window tracking
    hist_state = ["A"]
    hist_head = [0]
    hist_tape = [dict()]                       # tape BEFORE step t (t=0 is blank)
    # for each pair we need the swept window; track per-step head positions
    for steps in range(1, max_steps + 1):
        sym = tape.get(head, 0)
        write, move, nxt = machine[state][sym]
        tape[head] = write
        head += 1 if move == "R" else -1
        if nxt in HALT:
            return ("HALTS", steps)
        state = nxt

        hist_state.append(state)
        hist_head.append(head)
        hist_tape.append(dict(tape))           # snapshot AFTER this step

        # Lin-Rado check: compare current time `steps` with earlier same-state times.
        t = steps
        lo_t = max(0, t - max_period)
        for tp in range(t - 1, lo_t - 1, -1):
            if hist_state[tp] != state:
                continue
            d = head - hist_head[tp]           # net head displacement over the period
            # swept window during (tp, t]: absolute cells the head touched in that range
            seg = hist_head[tp + 1 : t + 1]
            L, R = min(seg), max(seg)
            cur, old = hist_tape[t], hist_tape[tp]
            # For the future to replay the period shifted by d, the tape NOW at the
            # shifted swept cells must equal the tape one period ago at the swept cells:
            #   T_t[a + d] == T_tp[a]   for every swept cell a in [L, R].
            # (The earlier version compared the wrong window, [L-d,R-d], and unsoundly
            #  flagged HALTING machines as NEVER_HALTS — caught by the known-halter oracle.)
            match = all(cur.get(a + d, 0) == old.get(a, 0) for a in range(L, R + 1))
            if match:
                return ("NEVER_HALTS", (tp, t - tp, d))
    return ("HOLDOUT", max_steps)


CASES = [
    ("BB(4) champion",      "1RB1LB_1LA0LC_1RZ1LD_1RD0RA"),  # HALTS @107
    ("trivial eraser loop", "0RA0RA"),                        # stationary -> NEVER
    ("runaway right",       "1RA1RA"),                        # DRIFTS -> the old holdout
    ("flip-in-place",       "1RB1LA_1LA1RB"),                 # was holdout in decider.py
    ("BB(5) champion",      "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA"),  # halts (47M) -> HOLDOUT@cap
]


def main() -> int:
    """SOUNDNESS AUDIT. A non-halting decider must NEVER say NEVER_HALTS for a halting
    machine. We cross-check every NEVER_HALTS claim against the trusted simulator. This
    version is KNOWN-UNSOUND (it misfires on BB(4)/BB(5), which demonstrably halt) — kept
    as a documented failed attempt. Do NOT trust its NEVER_HALTS verdicts."""
    from bb_sim import run
    ORACLE_CAP = 200_000
    print("=" * 78)
    print("Lin-Rado decider — SOUNDNESS AUDIT (cross-checking each claim vs the simulator)")
    print("=" * 78)
    print(f"{'machine':>20}  {'verdict':>12}  {'oracle':>22}  sound?")
    unsound = 0
    for name, spec in CASES:
        verdict, info = decide_lin(spec)
        halted, osteps, _ = run(spec, max_steps=ORACLE_CAP)
        flag = ""
        if verdict == "NEVER_HALTS" and halted:
            flag = "‼ UNSOUND (false proof!)"; unsound += 1
            oracle = f"HALTS @ {osteps}"
        elif verdict == "NEVER_HALTS":
            oracle = f"no halt < {ORACLE_CAP}"; flag = "(unconfirmed)"
        elif verdict == "HALTS":
            oracle = f"HALTS @ {osteps}"; flag = "OK"
        else:
            oracle = f"no halt < {ORACLE_CAP}"; flag = "OK (holdout)"
        print(f"{name:>20}  {verdict:>12}  {oracle:>22}  {flag}")
    print("\n" + "=" * 78)
    if unsound:
        print(f"VERDICT: this decider is UNSOUND — {unsound} false NON-HALT 'proofs' on machines")
        print("that demonstrably HALT (caught by the known-halter oracle). The Lin-Rado tape-")
        print("comparison condition is subtler than reconstructed here. DO NOT TRUST it.")
        print("Sound tool tonight: decider.py (exact-config repeat — weaker but correct).")
        print("Next: implement Lin recurrence against the published spec/Coq reference, gated")
        print("by this very oracle. (This is exactly why BB(5) needed a machine-checked proof.)")
    else:
        print("No false proofs detected on this case set (still: verify against the spec).")
    return 1 if unsound else 0


if __name__ == "__main__":
    raise SystemExit(main())
