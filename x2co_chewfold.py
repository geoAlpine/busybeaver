#!/usr/bin/env python3
"""x2co_chewfold.py -- mechanize the WITHIN-BLOCK chew fold (uniform in r):
   (01)^(k+1) [D] 0^3 1^(2r+5) 0^2 [TAIL]  ->*  (01)^(k+r+3) [D] 0^3 1^3 0^2 [TAIL]
by C1 applied r+1 times.  C1 is a proven 6-step closed form (x2cc_prove obligation 3);
the fold is a uniform single-parameter (r) loop, so the Prover loop-accelerates it.
TAIL is a concrete next-block stub (never read by C1: read span is the current block)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, Machine, Split, Halted, E
from x2cc_faith import T, Prover, GoalConfig


def loc(c):
    def rr(runs):
        return ' '.join(f"{p}^{cc}" if not (cc.is_const() and cc.c == 1) else p for p, cc in runs)
    return f"...{rr(c.left[-3:])} [{c.state}] {rr(c.right[:6])}..."


def main():
    print("=== within-block chew fold, symbolic r (Prover loop-accel) ===")
    # left stub (01)^(k+1) with k symbolic; TAIL = 0^2 1^99 0^2 guard (concrete next block)
    start = Config(T("01^k+1"), 'D', T("0^3 1^2r+5 0^2 1^99 0^2"))
    kr = E.var('k', 1, 0) + E.var('r', 1, 0) + E(2)   # comb count after r+1 chews
    goal = Config([('01', kr)], 'D', T("0^3 1^3 0^2 1^99 0^2"))
    print("start:", loc(start))
    print("goal :", loc(goal))
    P = Prover("chew-fold", verbose=True)
    try:
        P.prove(start, GoalConfig(goal), max_ops=20000)
        print(f"\nRESULT: {len(P.results)} branch(es) reached goal")
        allsafe = True
        for case, fc, ev in P.results:
            gaps = [str(e[2]) for e in ev if e[1] == 'gap']
            loops = [e[2] for e in ev if e[1] == 'loop']
            if gaps:
                allsafe = False
            print(f"  case {case or '(base)'}: gaps {gaps} loops {loops}")
        print("PROVEN, 0 gap events, all branches" if P.results and allsafe else "INCOMPLETE")
    except Exception as e:
        print(f"Prover FAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
