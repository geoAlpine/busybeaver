#!/usr/bin/env python3
"""x2co_blockstep.py -- the full PER-BLOCK cascade step as ONE parametric lemma:
   (01)^(k+1) [D] 0^3 1^(2r+5) 0^2 1^(2s+5) 0^2 [TAIL]
     ->*  (01)^(k+r+4) 0^2 1 [D] 0^3 1^(2s+3) 0^2 [TAIL]
i.e. chew the current block (2r+5) down to 3 (chew-fold, uniform in r), then C2 cross
the separator into the next block (2s+5 -> 2s+3), depositing 0^2 1 and growing the comb.
Proven by the certified Prover for ALL r, s, k (loop-accel + certified C2), 0 gap events.
TAIL is an opaque next-next block stub (never read: read span is current+next block)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, Machine, Split, Halted, E
from x2cc_faith import T, Prover, GoalConfig


def loc(c):
    def rr(runs):
        return ' '.join(f"{p}^{cc}" if not (cc.is_const() and cc.c == 1) else p for p, cc in runs)
    return f"...{rr(c.left[-3:])} [{c.state}] {rr(c.right[:7])}..."


def main():
    print("=== PER-BLOCK cascade step, symbolic (r,s,k), Prover ===")
    start = Config(T("01^k+1"), 'D', T("0^3 1^2r+5 0^2 1^2s+5 0^2 1^97 0^2"))
    kf = E.var('k', 1, 0) + E.var('r', 1, 0) + E(4)   # comb after chew(r+1)+C2
    goal = Config([('01', kf), ('0', E(2)), ('1', E(1))], 'D',
                  T("0^3 1^2s+3 0^2 1^97 0^2"))
    print("start:", loc(start))
    print("goal :", loc(goal))
    P = Prover("block-step", verbose=True)
    try:
        P.prove(start, GoalConfig(goal), max_ops=20000)
        allsafe = all(not [e for e in ev if e[1] == 'gap' and not (e[2].is_const() and e[2].c < 3)]
                      for _, _, ev in P.results)
        print(f"\nRESULT: {len(P.results)} branch(es) reached goal")
        for case, fc, ev in P.results:
            gaps = [str(e[2]) for e in ev if e[1] == 'gap']
            loops = [e[2] for e in ev if e[1] == 'loop']
            print(f"  case {case or '(base)'}: gaps {gaps} loops {loops}")
        print("PROVEN, no gap>=3" if P.results and allsafe else "INCOMPLETE")
    except Exception as e:
        print(f"Prover FAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
