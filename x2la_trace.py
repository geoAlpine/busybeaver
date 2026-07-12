#!/usr/bin/env python3
"""x2la_trace.py -- step-by-step micro-trace of the non-carry tick for a given
odd `built`, to reveal the tile structure for a Lean induction proof.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim


def make(built, L, R):
    rstr = '0' + '11' + ''.join('1' if b else '0' for b in R)
    sim = Sim(rstr, state='E', pos=0)
    Lfull = [1] * built + [0] + list(L)
    sim.L = Lfull[::-1]
    return sim


def show(sim, width=10):
    Lnf = [sim.L[-1 - k] for k in range(min(width, len(sim.L)))]
    Rnf = [sim.R[-1 - k] for k in range(min(width, len(sim.R)))]
    lstr = ''.join(str(b) for b in Lnf[::-1])  # print left-to-right
    rstr = ''.join(str(b) for b in Rnf)
    return f"n={sim.n:2} st={sim.st} pos={sim.pos:3}  ...{lstr}[{sim.h}]{rstr}..."


def trace(built, nsteps):
    L = [1, 0, 1, 0, 1, 0]
    R = [1]*9 + [0, 0] + [1]*5 + [0, 0, 1, 0]
    sim = make(built, L, R)
    print(f"--- built={built}, {nsteps} steps ---")
    print("  start:", show(sim))
    for i in range(nsteps):
        sim.step()
        print(f"  {show(sim)}")


if __name__ == "__main__":
    built = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    trace(built, 2 * built + 8)
