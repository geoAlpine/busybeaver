#!/usr/bin/env python3
"""x2la_param.py -- test whether the non-carry tick is a CLEAN parametric lemma
(provable by induction on the left solid-block length `built`) or DATA-DEPENDENT.

Conjecture (from the on-path extraction):
  steps (2*built+8) <E,0, ones built ++ (0 :: L), head 0, 1::1::R>
    = <E,2, ones (built+3) ++ L, head 0, R>     for arbitrary built, L, R.

We test many `built` values and several tail paddings L,R.  If it holds for ALL
built (including off-path parities) and all tails, the tick is a clean
block-parametric lemma; if it fails, the connector is data-dependent.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim


def make(built, L, R):
    """build <E,0, ones built ++ (0::L), head 0, 1::1::R>."""
    rstr = '0' + '11' + ''.join('1' if b else '0' for b in R)  # head 0, then 1 1, then R
    sim = Sim(rstr, state='E', pos=0)
    Lfull = [1] * built + [0] + list(L)   # nearest-first
    sim.L = Lfull[::-1]
    return sim


def expected(built, L, R):
    """<E,2, ones (built+3) ++ L, head 0, R>."""
    left = [1] * (built + 3) + list(L)
    return ('E', 2, tuple(left), tuple(R))


def actual(sim, nsteps):
    for _ in range(nsteps):
        if not sim.step():
            return ('HALT', sim.n)
    Lnf = [sim.L[-1 - k] for k in range(len(sim.L))]
    Rnf = [sim.R[-1 - k] for k in range(len(sim.R))]
    return (sim.st, sim.pos, tuple(Lnf), tuple(Rnf))


def test():
    combs = {
        'comb(10)^k': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        'zeros':      [0, 0, 0, 0, 0, 0],
        'ones':       [1, 1, 1, 1, 1, 1],
        'empty':      [],
    }
    Rpads = {
        'block+casc': [1]*9 + [0, 0] + [1]*5 + [0, 0, 1, 0],
        'zeros':      [0]*8,
        'ones':       [1]*8,
        'empty':      [],
    }
    print("built | comb        | Rpad        | steps | result")
    allok = True
    for built in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20]:
        nsteps = 2 * built + 8
        for cname, L in combs.items():
            for rname, R in Rpads.items():
                sim = make(built, L, R)
                got = actual(sim, nsteps)
                exp = expected(built, L, R)
                # compare on the touched window only: state,pos, left prefix up to
                # built+3, right prefix. Trailing tails may extend; compare prefixes.
                ok = (got[0] == exp[0] and got[1] == exp[1]
                      and got[2][:built+3] == exp[2][:built+3]
                      and got[3][:len(R)] == tuple(R))
                if not ok:
                    allok = False
                    print(f"{built:5} | {cname:11} | {rname:11} | {nsteps:5} | FAIL got={got}")
        # one summary line per built with the canonical on-path tails
        sim = make(built, combs['comb(10)^k'], Rpads['block+casc'])
        got = actual(sim, nsteps)
        exp = expected(built, combs['comb(10)^k'], Rpads['block+casc'])
        tag = 'OK' if (got[0]==exp[0] and got[1]==exp[1] and got[2][:built+3]==exp[2][:built+3]) else 'FAIL'
        print(f"{built:5} | on-path canonical                    | {nsteps:5} | {tag}  "
              f"st{got[0]} pos{got[1]} leftpref={got[2][:built+3]}")
    print("\nALL configs (all built x comb x Rpad):", "CLEAN PARAMETRIC" if allok else "DATA-DEPENDENT (some FAIL)")


if __name__ == "__main__":
    test()
