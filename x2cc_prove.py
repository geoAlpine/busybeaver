#!/usr/bin/env python3
"""x2cc_prove.py -- CARRY CALCULUS: the mechanized proof obligations (reproducible run).

  LOW-EVEN   M1(g) ->* M6(g), g even, for ALL g (n = g-1 >= 1 symbolic, B = 4b+4001)
  LOW-ODD    M1(g) ->* M6(g), g odd,  for ALL g (B = 4b+4003)
  C1         doubling chew-cycle body, ALL k, r   (6 steps, 0 events)
  C2         cascade-separator crossing, ALL k, s (15 steps, 0 events)

Each obligation is closed by the certified symbolic executor (x2cc_symb: raw TM table +
three exhaustively certified cycle closed-forms) under exhaustive case splitting and
certified loop induction (x2cc_faith).  A completed derivation contains NO gap-3 event by
construction (the executor raises Halted on the halt gate), so each is a non-halt proof
for the covered segment.  See X2_CARRY_CALCULUS_2026-07-11.md."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, check_rules, check_fold
from x2cc_faith import T, Prover, GoalRight, GoalConfig


def main():
    check_rules()
    check_fold()
    ok = 0

    print("\n[1] LOW-EVEN: 0^22 U^(n+1) 1 0^10 1^(4b+4001) 0^2|guard  ->*  M6(even)")
    P = Prover("low-even", verbose=False)
    P.prove(Config([], 'E', T("0^22 1000000^n+1 1 0^10 1^4b+4001 0^2")),
            GoalRight(T("0^2 10^4 1^9 0^2 1111100^n+3 1 0^2 1^4b+4001 0^2")),
            max_ops=100000)
    for case, fc, ev in P.results:
        gaps = [str(e[2]) for e in ev if e[1] == 'gap']
        loops = [e[2] for e in ev if e[1] == 'loop']
        print(f"    case {case or '(base)'}: gaps {gaps} loops {loops}")
    print(f"  PROVEN in {len(P.results)} branches; ledger {{18,10,2x(g+1),6}}, no 3")
    ok += 1

    print("\n[2] LOW-ODD: 0^22 U^(n+1) 1 0^4 (10)^6 1^(4b+4003) 0^2|guard  ->*  M6(odd)")
    P = Prover("low-odd", verbose=False)
    P.prove(Config([], 'E', T("0^22 1000000^n+1 1 0^4 10^6 1^4b+4003 0^2")),
            GoalRight(T("0^2 10^4 1^9 0^2 1111100^n+2 10^10 1^4b+3999 0^2")),
            max_ops=100000)
    for case, fc, ev in P.results:
        gaps = [str(e[2]) for e in ev if e[1] == 'gap']
        loops = [e[2] for e in ev if e[1] == 'loop']
        print(f"    case {case or '(base)'}: gaps {gaps} loops {loops}")
    print(f"  PROVEN in {len(P.results)} branches; ledger {{18,10,2x(g+1)}}, no 6, no 3")
    ok += 1

    print("\n[3] C1 chew body: [stub (01)^(k+1)] D [0^3 1^(2r+5) 0^2]  ->6->  (k+2, 2r+3)")
    for stub in ("1 0^2 1^21", "0^2 1"):
        P = Prover("C1", verbose=False)
        P.prove(Config(T(f"{stub} 01^k+1"), 'D', T("0^3 1^2r+5 0^2")),
                GoalConfig(Config(T(f"{stub} 01^k+2"), 'D', T("0^3 1^2r+3 0^2"))),
                max_ops=3000, allow_loops=False)
        assert all(not ev for _, _, ev in P.results)
        print(f"    stub '{stub}': PROVEN, 0 events")
    ok += 1

    print("\n[4] C2 separator crossing: [stub (01)^(k+1)] D [0^3 1^3 0^2 1^(2s+5) 0^2]")
    for stub in ("1 0^2 1^21", "0^2 1"):
        P = Prover("C2", verbose=False)
        P.prove(Config(T(f"{stub} 01^k+1"), 'D', T("0^3 1^3 0^2 1^2s+5 0^2")),
                GoalConfig(Config(T(f"{stub} 01^k+3 0^2 1"), 'D', T("0^3 1^2s+3 0^2"))),
                max_ops=3000, allow_loops=False)
        assert all(not ev for _, _, ev in P.results)
        print(f"    stub '{stub}': PROVEN, 0 events")
    ok += 1

    print(f"\nALL {ok}/4 OBLIGATIONS CLOSED.  (Doubling-phase full composition: see "
          f"x2cc_gencheck.py, exact per generation g=2..6; symbolic chain OPEN.)")
    print("No machine decided. No label upgraded.")


if __name__ == "__main__":
    main()
